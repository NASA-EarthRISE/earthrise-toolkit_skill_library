#!/usr/bin/env python3
"""Collect test metrics from Lightning CSV logs into a leaderboard + metrics.json.

Expects runs named <run>_s<seed> (as written by make_configs.py), with
CSVLogger output at <runs>/<run>_s<seed>/version_*/metrics.csv.

Usage
  python collect_results.py --runs experiments/<exp>/runs [--metric test/mIoU] [--lower-is-better]
      [--baseline unet_scratch] [--out experiments/<exp>/results]
Writes leaderboard.csv, leaderboard.md, metrics.json (shared metrics.json contract).
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import glob
import json
import math
import os
import re
from collections import defaultdict
from statistics import mean, stdev

SKILL, SKILL_VERSION = "foundation-model-finetune", "0.1.0"
AUTO_METRICS = ["test/mIoU", "test/Multiclass_Jaccard_Index", "test/Multiclass_F1_Score",
                "test/RMSE", "test/MAE", "test/Accuracy", "test/Overall_Accuracy"]
LOWER_BETTER = {"test/RMSE", "test/MAE", "test/loss"}


def last_values(csv_path: str) -> dict[str, float]:
    out = {}
    with open(csv_path, newline="") as f:
        for row in csv.DictReader(f):
            for k, v in row.items():
                if k and k.startswith("test/") and v not in ("", None):
                    try:
                        out[k] = float(v)
                    except ValueError:
                        pass
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs", required=True)
    ap.add_argument("--metric", help="primary metric column (default: auto-detect)")
    ap.add_argument("--lower-is-better", action="store_true")
    ap.add_argument("--baseline", help="run name of the non-foundation-model baseline")
    ap.add_argument("--out", help="output dir (default: <runs>/../results)")
    ap.add_argument("--dataset", default="")
    a = ap.parse_args()
    out = a.out or os.path.join(os.path.dirname(os.path.abspath(a.runs)), "results")
    os.makedirs(out, exist_ok=True)

    per_run: dict[str, dict[int, dict[str, float]]] = defaultdict(dict)
    for d in sorted(glob.glob(os.path.join(a.runs, "*"))):
        m = re.match(r"(.+)_s(\d+)$", os.path.basename(d))
        if not m:
            continue
        vals = {}
        for c in sorted(glob.glob(os.path.join(d, "version_*", "metrics.csv"))):
            vals.update(last_values(c))
        if vals:
            per_run[m.group(1)][int(m.group(2))] = vals
    if not per_run:
        raise SystemExit(f"No test metrics found under {a.runs}/<run>_s<seed>/version_*/metrics.csv")

    cols = sorted({k for r in per_run.values() for v in r.values() for k in v})
    metric = a.metric or next((m for m in AUTO_METRICS if m in cols), cols[0])
    lower = a.lower_is_better or metric in LOWER_BETTER

    rows = []
    for name, seeds in per_run.items():
        row = {"run": name, "n_seeds": len(seeds), "seeds": sorted(seeds)}
        for c in cols:
            xs = [s[c] for s in seeds.values() if c in s]
            if xs:
                row[c] = (mean(xs), stdev(xs) if len(xs) > 1 else float("nan"), len(xs))
        rows.append(row)
    rows.sort(key=lambda r: r.get(metric, (math.inf if lower else -math.inf,))[0], reverse=not lower)

    notes = []
    if len(rows) > 1 and metric in rows[0] and metric in rows[1]:
        (m1, s1, _), (m2, s2, _) = rows[0][metric], rows[1][metric]
        noise = max(x for x in (s1, s2) if not math.isnan(x)) if not (math.isnan(s1) and math.isnan(s2)) else float("nan")
        gap = abs(m1 - m2)
        if math.isnan(noise):
            notes.append("Single seed per run: ranking is not interpretable.")
        elif gap <= noise:
            notes.append(f"Top two ({rows[0]['run']}, {rows[1]['run']}) differ by {gap:.4f}, within seed std ({noise:.4f}): treat as a tie.")
    if a.baseline:
        b = next((r for r in rows if r["run"] == a.baseline), None)
        if not b:
            notes.append(f"Baseline '{a.baseline}' not found in runs — comparison incomplete.")
        elif metric in b:
            notes.append(f"Baseline {a.baseline}: {metric} = {b[metric][0]:.4f} ± {b[metric][1]:.4f}.")
    else:
        notes.append("No --baseline given: results lack a non-foundation-model reference.")
    for r in rows:
        if r["n_seeds"] < 3:
            notes.append(f"{r['run']} has {r['n_seeds']} seed(s); >= 3 recommended.")

    def fmt(t):
        return "" if t is None else (f"{t[0]:.4f}" if math.isnan(t[1]) else f"{t[0]:.4f} ± {t[1]:.4f}")

    with open(os.path.join(out, "leaderboard.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["rank", "run", "n_seeds"] + sum([[c + "_mean", c + "_std"] for c in cols], []))
        for i, r in enumerate(rows, 1):
            w.writerow([i, r["run"], r["n_seeds"]] + sum([[r[c][0], r[c][1]] if c in r else ["", ""] for c in cols], []))
    md = [f"| Rank | Run | Seeds | {metric} (mean ± std) |", "|---|---|---|---|"]
    md += [f"| {i} | `{r['run']}`{' (baseline)' if r['run'] == a.baseline else ''} | {r['n_seeds']} | {fmt(r.get(metric))} |"
           for i, r in enumerate(rows, 1)]
    md += ["", *[f"- {n}" for n in notes]]
    open(os.path.join(out, "leaderboard.md"), "w").write("\n".join(md) + "\n")

    metrics = {}
    for r in rows:
        for c in cols:
            if c in r:
                mu, sd, n = r[c]
                key = f"{r['run']}.{c.removeprefix('test/')}"
                metrics[key] = {"value": round(mu, 6), "std_over_seeds": None if math.isnan(sd) else round(sd, 6), "n_seeds": n}
    doc = {"task": "geofm_finetune_intercomparison", "dataset": a.dataset, "primary_metric": metric,
           "higher_is_better": not lower, "ranking": [r["run"] for r in rows], "baseline": a.baseline,
           "notes": notes, "metrics": metrics,
           "created": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
           "skill": SKILL, "skill_version": SKILL_VERSION}
    json.dump(doc, open(os.path.join(out, "metrics.json"), "w"), indent=2)
    print("\n".join(md))
    print(f"\nWrote {out}/leaderboard.csv, leaderboard.md, metrics.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
