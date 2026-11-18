#!/usr/bin/env python3
"""Area-adjusted accuracy assessment for a classified map (Olofsson et al. 2014).

Stratified random sampling with strata = map classes.

Inputs
  --samples  samples.csv with columns: sample_id, map_class, ref_class  (x, y, stratum optional)
  --areas    CSV with columns: class, area   (mapped area per map class, any unit; pixels ok)
Outputs (in --out dir)
  metrics.json             overall / user's / producer's accuracy + area estimates, 95% CI
  confusion_matrix.csv     sample counts, rows = map, cols = reference
  area_proportions.csv     estimated area proportions p_ij

Usage
  python accuracy_assessment.py --samples samples.csv --areas areas.csv --out results/ [--unit ha] [--z 1.96]
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import math
from collections import defaultdict
from pathlib import Path

SKILL = "classification-accuracy-assessment"
SKILL_VERSION = "0.1.0"


def read_samples(path: Path) -> list[tuple[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        missing = {"map_class", "ref_class"} - set(r.fieldnames or [])
        if missing:
            raise SystemExit(f"samples file missing columns: {sorted(missing)}")
        return [(row["map_class"].strip(), row["ref_class"].strip()) for row in r]


def read_areas(path: Path) -> dict[str, float]:
    with path.open(newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        if not {"class", "area"} <= set(r.fieldnames or []):
            raise SystemExit("areas file needs columns: class, area")
        return {row["class"].strip(): float(row["area"]) for row in r}


def assess(samples, areas, z=1.96):
    classes = sorted(set(areas) | {m for m, _ in samples} | {r for _, r in samples})
    n = defaultdict(lambda: defaultdict(int))
    for m, r in samples:
        n[m][r] += 1
    n_i = {i: sum(n[i].values()) for i in classes}
    for i in classes:
        if areas.get(i, 0) > 0 and n_i[i] < 2:
            raise SystemExit(f"map class '{i}' has area but {n_i[i]} sample(s); need >= 2 per stratum")
    A = sum(areas.values())
    W = {i: areas.get(i, 0.0) / A for i in classes}
    p = {i: {j: (W[i] * n[i][j] / n_i[i]) if n_i[i] else 0.0 for j in classes} for i in classes}
    p_row = {i: sum(p[i].values()) for i in classes}
    p_col = {j: sum(p[i][j] for i in classes) for j in classes}

    oa = sum(p[j][j] for j in classes)
    v_oa = sum(W[i] ** 2 * (n[i][i] / n_i[i]) * (1 - n[i][i] / n_i[i]) / (n_i[i] - 1)
               for i in classes if n_i[i] > 1)

    N_map = {i: areas.get(i, 0.0) for i in classes}           # mapped area of class i
    N_est = {j: sum(N_map[i] * n[i][j] / n_i[i] for i in classes if n_i[i]) for j in classes}

    def ci(val, var):
        se = math.sqrt(max(var, 0.0))
        return {"value": round(val, 6), "se": round(se, 6),
                "ci_low": round(val - z * se, 6), "ci_high": round(val + z * se, 6)}

    metrics = {"overall_accuracy": ci(oa, v_oa)}
    for j in classes:
        if n_i[j] > 1:
            U = n[j][j] / n_i[j]
            metrics[f"users_accuracy.{j}"] = ci(U, U * (1 - U) / (n_i[j] - 1))
        if p_col[j] > 0:
            P = p[j][j] / p_col[j]
            term1 = (N_map[j] ** 2 * (1 - P) ** 2 * (n[j][j] / n_i[j]) * (1 - n[j][j] / n_i[j]) / (n_i[j] - 1)
                     if n_i[j] > 1 else 0.0)
            term2 = P ** 2 * sum(
                N_map[i] ** 2 * (n[i][j] / n_i[i]) * (1 - n[i][j] / n_i[i]) / (n_i[i] - 1)
                for i in classes if i != j and n_i[i] > 1)
            metrics[f"producers_accuracy.{j}"] = ci(P, (term1 + term2) / N_est[j] ** 2)
        v_pk = sum((W[i] * p[i][j] - p[i][j] ** 2) / (n_i[i] - 1) for i in classes if n_i[i] > 1)
        metrics[f"area_proportion.{j}"] = ci(p_col[j], v_pk)
        a = ci(p_col[j] * A, v_pk * A ** 2)
        metrics[f"area.{j}"] = a
    return classes, n, p, metrics, A


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--samples", required=True, type=Path)
    ap.add_argument("--areas", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--unit", default="map units", help="area unit label, e.g. ha, km2, pixels")
    ap.add_argument("--z", type=float, default=1.96, help="z for CI (1.96 = 95%%)")
    ap.add_argument("--dataset", default="", help="dataset name/id for metrics.json")
    a = ap.parse_args()

    samples = read_samples(a.samples)
    areas = read_areas(a.areas)
    classes, n, p, metrics, A = assess(samples, areas, a.z)
    a.out.mkdir(parents=True, exist_ok=True)

    with (a.out / "confusion_matrix.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["map\\ref"] + classes + ["total"])
        for i in classes:
            w.writerow([i] + [n[i][j] for j in classes] + [sum(n[i].values())])
    with (a.out / "area_proportions.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["map\\ref"] + classes)
        for i in classes:
            w.writerow([i] + [round(p[i][j], 6) for j in classes])

    doc = {
        "task": "classification_accuracy_assessment",
        "method": "Olofsson et al. 2014, stratified estimator, strata = map classes",
        "dataset": a.dataset,
        "n_samples": len(samples),
        "total_area": A,
        "area_unit": a.unit,
        "confidence": round(2 * (0.5 * (1 + math.erf(a.z / math.sqrt(2)))) - 1, 4),
        "metrics": metrics,
        "created": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "skill": SKILL,
        "skill_version": SKILL_VERSION,
    }
    (a.out / "metrics.json").write_text(json.dumps(doc, indent=2))
    oa = metrics["overall_accuracy"]
    print(f"Overall accuracy {oa['value']:.3f} (95% CI {oa['ci_low']:.3f}-{oa['ci_high']:.3f}), n={len(samples)}")
    print(f"Wrote {a.out}/metrics.json, confusion_matrix.csv, area_proportions.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
