#!/usr/bin/env python3
"""PINECONe Total Economic Value (TEV) Monte Carlo from cached stage stats. No Earth Engine.

Uses PINECONe's own TEVCalculator (pinecone.economics.tev_calculator) so numbers match
the package, and adds what the package does not: fallback detection, per-component
breakdown, scenario comparison, saved figures, and the shared metrics.json contract.

Outputs (in --out)
  metrics.json              mean TEV per zone with 95% simulation interval (+ per acre, components, flags)
  tev_summary.csv           package summary columns + P2.5/P97.5 + per-acre
  tev_components.csv        expected $/acre of timber, carbon, ecosystem services, lease NPV
  scenario_comparison.csv   pairwise Cohen's d, P(A > B), overlap coefficient
  figures/tev_distributions.png (+ .txt caption), figures/tev_boxplots.png (+ .txt)
  report_draft.md           tables filled from the numbers above; interpretation left to the analyst

Usage
  python run_tev.py --stats results/stage_stats.json --params tev_params.yaml --out results/
"""
from __future__ import annotations

import argparse
import datetime as dt
import itertools
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

SKILL = "pinecone-rx-fire-valuation"
SKILL_VERSION = "0.1.0"
TUPLE_KEYS = ("E_Pt", "g", "endangered_species_WTP", "epsilon_t", "r_lease", "water_quality_value")
WATER_FALLBACK = (100.0, 2.0)  # hard-coded in PINECONe create_economic_parameters


def fail(msg: str) -> None:
    sys.exit(f"ERROR: {msg}")


def as_param(k, v):
    if k in TUPLE_KEYS and isinstance(v, (list, tuple)):
        if len(v) != 2:
            fail(f"{k} must be a scalar or [mean, std], got {v}")
        return (float(v[0]), float(v[1]))
    return v


def check_params(zones: dict, acres: dict, biomass: dict) -> list[str]:
    errs = []
    for z, p in zones.items():
        if z not in acres:
            errs.append(f"{z}: no case_acres entry (PINECONe silently skips it)")
        if z not in biomass:
            errs.append(f"{z}: not in stage_stats biomass (have {sorted(biomass)})")
        R, T = p.get("R_t_lease"), p.get("T_lease")
        if R is not None and T is not None and len(R) < T:
            errs.append(f"{z}: R_t_lease has {len(R)} values but T_lease={T}; missing years count as $0")
        for k in TUPLE_KEYS:
            v = p.get(k)
            if isinstance(v, (list, tuple)) and len(v) == 2 and v[1] < 0:
                errs.append(f"{z}.{k}: negative std")
    return errs


def lease_npv(R, T, r):
    r = r[0] if isinstance(r, tuple) else r
    return sum((R[t - 1] if t - 1 < len(R) else 0) / (1 + r) ** t for t in range(1, T + 1))


def mean_of(v):
    return v[0] if isinstance(v, tuple) else (v or 0.0)


def overlap(a, b, bins=200):
    lo, hi = min(a.min(), b.min()), max(a.max(), b.max())
    ha, edges = np.histogram(a, bins=bins, range=(lo, hi), density=True)
    hb, _ = np.histogram(b, bins=bins, range=(lo, hi), density=True)
    return float(np.minimum(ha, hb).sum() * (edges[1] - edges[0]))


def money(x):
    return f"-${-x:,.0f}" if x < 0 else f"${x:,.0f}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--stats", type=Path, required=True, help="stage_stats.json from run_pinecone.py")
    ap.add_argument("--params", type=Path, required=True, help="tev_params.yaml")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--dataset", default="", help="label for metrics.json (e.g. 'Gulf State Park EIA cases')")
    ap.add_argument("--no-figures", action="store_true")
    a = ap.parse_args()

    try:
        from pinecone.economics.tev_calculator import TEVCalculator
    except ImportError as e:
        fail(f"{e}. Install PINECONe: pip install pinecone-fire (uninstall the Pinecone vector-DB SDK if present; "
             "it shadows the 'pinecone' module)")

    stats = json.loads(a.stats.read_text())
    P = yaml.safe_load(a.params.read_text()) or {}
    zones_cfg = P.get("zones") or {}
    acres = {k: float(v) for k, v in (P.get("case_acres") or {}).items()}
    price = float(P.get("carbon_credit_price", 10.0))
    n_sim = int(P.get("num_simulations", 10000))
    seed = int(P.get("random_seed", 42))
    sfx = (stats.get("provenance") or {}).get("species_suffix", "LLP")

    biomass = stats.get("biomass") or {}
    emissions = stats.get("emissions") or {}
    water = stats.get("water_yield") or {}
    if not zones_cfg:
        fail("tev_params.yaml has no 'zones'; refusing to run on PINECONe's built-in CS1/CS2/CS3 defaults silently")
    errs = check_params(zones_cfg, acres, biomass)
    if errs:
        print("\n".join(f"PARAMS {e}" for e in errs))
        return 1

    flags = list(stats.get("flags") or [])
    user_params, water_for_pkg = {}, {}
    for z, p in zones_cfg.items():
        p = {k: as_param(k, v) for k, v in p.items()}
        user_params[z] = p
        base = z[: -len(f"_{sfx}")] if z.endswith(f"_{sfx}") else z
        w = water.get(base)
        # PINECONe looks water up by zone.replace('_LLP',''); re-key so any suffix works.
        if w:
            water_for_pkg[z.replace("_LLP", "")] = w
        if "water_quality_value" in p:
            flags.append(f"water_value_user_override:{z}")
        elif not w:
            flags.append(f"water_value_fallback:{z}: no water-yield result, PINECONe used default "
                         f"${WATER_FALLBACK[0]:.0f}±{WATER_FALLBACK[1]:.0f}/acre")
        if z not in emissions:
            flags.append(f"emissions_missing:{z}: carbon term set to $0")

    calc = TEVCalculator(random_seed=seed)
    bio_sel = {z: biomass[z] for z in zones_cfg}
    econ = calc.create_economic_parameters(bio_sel, emissions, water_for_pkg or None, user_params, price)
    for z, p in user_params.items():  # package ignores a user water value; honour it
        if "water_quality_value" in p:
            v = p["water_quality_value"]
            econ[z]["water_quality_value"] = v if isinstance(v, tuple) else (float(v), 0.0)

    rows, comp_rows, sims, metrics = [], [], {}, {}
    for z, zp in econ.items():
        ac = acres[z]
        tev = calc.calculate_tev(zp, ac, n_sim)
        sims[z] = tev
        q = np.percentile(tev, [2.5, 25, 50, 75, 97.5])
        rows.append({"Case": z, "Acres": ac, "Mean_TEV": tev.mean(), "Std_TEV": tev.std(), "Median_TEV": q[2],
                     "Q25_TEV": q[1], "Q75_TEV": q[3], "P2_5_TEV": q[0], "P97_5_TEV": q[4],
                     "Min_TEV": tev.min(), "Max_TEV": tev.max(), "Mean_TEV_per_acre": tev.mean() / ac,
                     "P_TEV_negative": float((tev < 0).mean())})
        timber = (mean_of(zp["E_Pt"]) + mean_of(zp.get("epsilon_t", 0))) * mean_of(zp["V_t"]) - mean_of(zp["g"])
        carbon = mean_of(zp["pvc_per_acre"])
        eco = mean_of(zp["water_quality_value"]) + mean_of(zp["endangered_species_WTP"])
        lease = lease_npv(zp["R_t_lease"], zp["T_lease"], zp["r_lease"])
        comp_rows.append({"Case": z, "timber_usd_per_acre": timber, "carbon_usd_per_acre": carbon,
                          "ecosystem_services_usd_per_acre": eco, "lease_npv_usd_per_acre": lease,
                          "total_usd_per_acre": timber + carbon + eco + lease,
                          "V_t_tons_per_acre": mean_of(zp["V_t"]),
                          "CO2_tons_per_acre": carbon / price if price else None})
        metrics[f"{z}.tev_usd"] = {"value": float(tev.mean()), "ci_low": float(q[0]), "ci_high": float(q[4])}
        metrics[f"{z}.tev_usd_per_acre"] = {"value": float(tev.mean() / ac), "ci_low": float(q[0] / ac),
                                            "ci_high": float(q[4] / ac)}

    summary = pd.DataFrame(rows)
    comps = pd.DataFrame(comp_rows)
    pairs = []
    for x, y in itertools.combinations(sims, 2):
        A, B = sims[x], sims[y]
        sd = np.sqrt((A.var(ddof=1) + B.var(ddof=1)) / 2)
        pairs.append({"A": x, "B": y, "mean_diff_usd": A.mean() - B.mean(),
                      "cohens_d": (A.mean() - B.mean()) / sd if sd else np.nan,
                      "P_A_gt_B": float((A[:, None] > B[None, :2000]).mean()) if len(B) else np.nan,
                      "overlap_coef": overlap(A, B)})
    comp_df = pd.DataFrame(pairs)

    out = a.out
    out.mkdir(parents=True, exist_ok=True)
    summary.to_csv(out / "tev_summary.csv", index=False)
    comps.to_csv(out / "tev_components.csv", index=False)
    comp_df.to_csv(out / "scenario_comparison.csv", index=False)
    np.savez_compressed(out / "tev_simulations.npz", **sims)

    if not a.no_figures:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.ticker as mt
        (out / "figures").mkdir(exist_ok=True)
        fmt = mt.FuncFormatter(lambda v, _: f"${v / 1000:,.0f}k")
        fig, ax = plt.subplots(figsize=(11, 6))
        for z, t in sims.items():
            ax.hist(t, bins=80, density=True, alpha=0.45, label=z)
        ax.xaxis.set_major_formatter(fmt)
        ax.set(xlabel="Total Economic Value (USD)", ylabel="Density", title="TEV distribution by scenario")
        ax.legend(); ax.grid(ls="--", alpha=0.5); fig.tight_layout()
        fig.savefig(out / "figures/tev_distributions.png", dpi=200); plt.close(fig)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.boxplot(list(sims.values()), showfliers=False)
        ax.set_xticks(range(1, len(sims) + 1), list(sims), rotation=15)
        ax.yaxis.set_major_formatter(fmt)
        ax.set(ylabel="Total Economic Value (USD)", title="TEV by scenario (whiskers 1.5 IQR, outliers hidden)")
        ax.grid(ls="--", alpha=0.5); fig.tight_layout()
        fig.savefig(out / "figures/tev_boxplots.png", dpi=200); plt.close(fig)
        cap = f"{n_sim:,} Monte Carlo draws per scenario, seed {seed}, carbon price ${price}/t CO2e. PINECONe TEVCalculator."
        (out / "figures/tev_distributions.txt").write_text("Distribution of simulated TEV per scenario. " + cap + "\n")
        (out / "figures/tev_boxplots.txt").write_text("Simulated TEV per scenario (box = IQR, line = median). " + cap + "\n")

    doc = {
        "task": "prescribed_fire_total_economic_value",
        "method": "PINECONe TEV = timber + carbon + ecosystem services + lease NPV; Monte Carlo, ci = 2.5/97.5 simulation percentiles",
        "dataset": a.dataset,
        "metrics": metrics,
        "zones": {r["Case"]: {**r, **comps.set_index("Case").loc[r["Case"]].to_dict()} for r in rows},
        "scenario_comparison": pairs,
        "params": {"carbon_credit_price": price, "num_simulations": n_sim, "random_seed": seed,
                   "case_acres": acres, "economic_params": {z: {k: list(v) if isinstance(v, tuple) else v
                                                                 for k, v in p.items()} for z, p in econ.items()}},
        "flags": flags,
        "upstream_provenance": stats.get("provenance"),
        "created": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "skill": SKILL,
        "skill_version": SKILL_VERSION,
    }
    (out / "metrics.json").write_text(json.dumps(doc, indent=2, default=float))

    # ---- report draft: numbers only, interpretation is the analyst's job ----
    L = ["## Results (draft: numbers generated by run_tev.py)", "",
         f"{n_sim:,} simulations per scenario; seed {seed}; carbon credit price ${price:g}/t CO2e.", "",
         "| Scenario | Acres | Mean TEV | 95% interval | Mean $/acre | P(TEV<0) |", "|---|---:|---:|---:|---:|---:|"]
    for r in rows:
        L.append(f"| {r['Case']} | {r['Acres']:,.0f} | {money(r['Mean_TEV'])} | {money(r['P2_5_TEV'])} to "
                 f"{money(r['P97_5_TEV'])} | {money(r['Mean_TEV_per_acre'])} | {r['P_TEV_negative']:.1%} |")
    L += ["", "Expected value per acre by component (at parameter means):", "",
          "| Scenario | Timber | Carbon | Ecosystem services | Lease NPV | Total |", "|---|---:|---:|---:|---:|---:|"]
    for c in comp_rows:
        L.append(f"| {c['Case']} | {money(c['timber_usd_per_acre'])} | {money(c['carbon_usd_per_acre'])} | "
                 f"{money(c['ecosystem_services_usd_per_acre'])} | {money(c['lease_npv_usd_per_acre'])} | "
                 f"{money(c['total_usd_per_acre'])} |")
    if pairs:
        L += ["", "| A vs B | Mean diff | Cohen's d | P(A>B) | Overlap |", "|---|---:|---:|---:|---:|"]
        for p in pairs:
            L.append(f"| {p['A']} vs {p['B']} | {money(p['mean_diff_usd'])} | {p['cohens_d']:.2f} | "
                     f"{p['P_A_gt_B']:.2f} | {p['overlap_coef']:.2f} |")
    if flags:
        L += ["", "**Flags (must appear in Limitations):**", ""] + [f"- {f}" for f in flags]
    (out / "report_draft.md").write_text("\n".join(L) + "\n")

    print(summary[["Case", "Acres", "Mean_TEV", "P2_5_TEV", "P97_5_TEV", "Mean_TEV_per_acre"]].to_string(index=False))
    for f in flags:
        print(f"FLAG  {f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
