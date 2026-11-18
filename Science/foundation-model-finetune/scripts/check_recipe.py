#!/usr/bin/env python3
"""Check that image/label chips match a locked data recipe (data_recipe.yaml).

Catches the failures that silently wreck GeoFM fine-tuning and inference:
wrong band count/order, wrong dtype or scaling, chip size, resolution or CRS
mismatch, bad label values, and per-band distribution drift vs the training
normalization stats (which is how band swaps usually show up).

Usage
  python check_recipe.py --recipe data_recipe.yaml                    # check every split root in the recipe
  python check_recipe.py --recipe data_recipe.yaml --root inference/  # check another folder (e.g. inference chips)
  python check_recipe.py --recipe data_recipe.yaml --compute-stats    # print train means/stds to paste into the recipe
Options
  --sample N   max chips per root to read for stats (default 200)
  --out FILE   write a JSON report (default recipe_check.json)
Exit code 1 if any check FAILS.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import random
import sys

import numpy as np
import yaml

try:
    import rasterio
except ImportError:  # pragma: no cover
    sys.exit("rasterio is required: pip install rasterio")


def find(root: str, pattern: str) -> list[str]:
    return sorted(glob.glob(os.path.join(root, "**", pattern), recursive=True))


def band_stats(paths, nodata, nb, sample):
    """Per-band mean/std over valid pixels of up to `sample` chips (streamed)."""
    paths = paths if len(paths) <= sample else random.Random(0).sample(paths, sample)
    s = np.zeros(nb)
    s2 = np.zeros(nb)
    n = np.zeros(nb)
    for p in paths:
        with rasterio.open(p) as ds:
            a = ds.read().astype("float64")
        if a.shape[0] != nb:
            continue
        for b in range(nb):
            v = a[b]
            m = np.isfinite(v) if nodata is None else (np.isfinite(v) & (v != nodata))
            v = v[m]
            s[b] += v.sum()
            s2[b] += (v * v).sum()
            n[b] += v.size
    n = np.maximum(n, 1)
    mean = s / n
    std = np.sqrt(np.maximum(s2 / n - mean ** 2, 0))
    return mean, std


def check_root(root, R, sample):
    res = {"root": root, "checks": [], "n_images": 0, "n_labels": 0}

    def add(name, ok, detail=""):
        res["checks"].append({"check": name, "status": "PASS" if ok else "FAIL", "detail": detail})

    bands = R["bands"]
    nb = len(bands)
    imgs = find(root, R["image_glob"])
    res["n_images"] = len(imgs)
    add("images found", len(imgs) > 0, f"{len(imgs)} matching {R['image_glob']}")
    if not imgs:
        return res

    probe = imgs if len(imgs) <= sample else random.Random(1).sample(imgs, sample)
    counts, dtypes, shapes, crss, ress, nds = set(), set(), set(), set(), set(), set()
    for p in probe:
        with rasterio.open(p) as ds:
            counts.add(ds.count)
            dtypes.add(ds.dtypes[0])
            shapes.add((ds.height, ds.width))
            crss.add(ds.crs.to_string() if ds.crs else None)
            ress.add(round(abs(ds.transform.a), 3))
            nds.add(ds.nodata)
    add("band count", counts == {nb}, f"found {sorted(counts)}, recipe {nb} ({', '.join(bands)})")
    if R.get("dtype"):
        add("dtype", dtypes == {R["dtype"]}, f"found {sorted(dtypes)}, recipe {R['dtype']}")
    if R.get("chip_size"):
        cs = tuple(R["chip_size"])
        add("chip size", shapes == {cs}, f"found {sorted(shapes)[:5]}, recipe {cs}")
    if len(crss) > 1:
        add("single CRS", False, f"mixed CRS: {sorted(map(str, crss))}")
    elif R.get("crs"):
        add("CRS", crss == {R["crs"]}, f"found {crss}, recipe {R['crs']}")
    if R.get("resolution_m"):
        tgt = float(R["resolution_m"])
        projected = all(c and "4326" not in c for c in crss)
        if projected:
            bad = [r for r in ress if abs(r - tgt) / tgt > 0.01]
            add("resolution", not bad, f"found {sorted(ress)} m, recipe {tgt} m")
        else:
            add("resolution", False, "chips are not in a projected CRS; cannot verify metres")
    if "nodata" in R:
        add("nodata value", nds <= {R["nodata"], None}, f"found {sorted(map(str, nds))}, recipe {R['nodata']}")

    # labels
    if R.get("label_glob") and R.get("task") in ("segmentation", "regression"):
        labs = find(root, R["label_glob"])
        res["n_labels"] = len(labs)
        add("label count matches images", len(labs) == len(imgs), f"{len(labs)} labels vs {len(imgs)} images")
        if R.get("task") == "segmentation" and labs:
            allowed = set(range(int(R["num_classes"]))) | {R.get("label_nodata", -1)}
            seen = set()
            for p in labs[:sample]:
                with rasterio.open(p) as ds:
                    seen |= set(np.unique(ds.read(1)).tolist())
            extra = sorted(v for v in seen if v not in allowed)
            add("label values", not extra, f"unexpected values {extra[:10]}" if extra else f"values {sorted(seen)[:12]}")

    # distribution drift vs training norm stats (band order / scaling)
    norm = R.get("norm") or {}
    if norm.get("means") and norm.get("stds") and counts == {nb}:
        mu, sd = band_stats(imgs, R.get("nodata"), nb, sample)
        ref_mu = np.array(norm["means"], float)
        ref_sd = np.maximum(np.array(norm["stds"], float), 1e-12)
        z = np.abs(mu - ref_mu) / ref_sd
        zmax = float(R.get("drift_z_max", 3.0))
        drift = [f"{bands[i]} z={z[i]:.1f}" for i in range(nb) if z[i] > zmax]
        add("band distribution vs train stats", not drift,
            "; ".join(drift) if drift else f"max z={z.max():.2f} (limit {zmax})")
        # band-swap heuristic: does each band's (mean, std) signature match a DIFFERENT
        # recipe band much better than its own? Catches swaps between similar bands
        # (e.g. NIR/SWIR1) that the drift test alone is too lenient to flag.
        dd = (np.abs(mu[:, None] - ref_mu[None, :]) + np.abs(sd[:, None] - ref_sd[None, :])) / ref_sd[None, :]
        best = dd.argmin(axis=1)
        swaps = [f"{bands[i]}≈{bands[best[i]]}" for i in range(nb)
                 if best[i] != i and dd[i, i] > 0.25 and dd[i, best[i]] < 0.5 * dd[i, i]]
        add("band order (swap heuristic)", not swaps,
            ("possible swap: " + ", ".join(swaps)) if swaps else "no swap signature")
        res["band_means"] = mu.round(6).tolist()
        res["band_stds"] = sd.round(6).tolist()
        res["z_vs_train"] = z.round(3).tolist()
    return res


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--recipe", required=True)
    ap.add_argument("--root", action="append", help="folder(s) to check; default: all split roots in recipe")
    ap.add_argument("--compute-stats", action="store_true")
    ap.add_argument("--sample", type=int, default=200)
    ap.add_argument("--out", default="recipe_check.json")
    a = ap.parse_args()
    R = yaml.safe_load(open(a.recipe))
    splits = R.get("splits", {})

    if a.compute_stats:
        train = splits.get("train_root")
        if not train:
            sys.exit("recipe.splits.train_root is required for --compute-stats")
        mu, sd = band_stats(find(train, R["image_glob"]), R.get("nodata"), len(R["bands"]), a.sample)
        print("# paste into data_recipe.yaml (computed from TRAIN split only)")
        print(yaml.safe_dump({"norm": {"means": [round(float(x), 6) for x in mu],
                                       "stds": [round(float(x), 6) for x in sd]}}, sort_keys=False))
        return 0

    roots = a.root or [splits[k] for k in ("train_root", "val_root", "test_root") if splits.get(k)]
    report = {"recipe": R.get("name"), "results": [check_root(r, R, a.sample) for r in roots]}
    fails = 0
    for r in report["results"]:
        print(f"\n== {r['root']}  ({r['n_images']} images)")
        for c in r["checks"]:
            fails += c["status"] == "FAIL"
            print(f"  {c['status']:4}  {c['check']:<34} {c['detail']}")
    report["status"] = "PASS" if fails == 0 else "FAIL"
    json.dump(report, open(a.out, "w"), indent=2)
    print(f"\n{report['status']}: {fails} failing check(s). Report -> {a.out}")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
