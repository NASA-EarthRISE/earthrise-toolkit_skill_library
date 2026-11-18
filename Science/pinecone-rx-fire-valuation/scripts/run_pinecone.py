#!/usr/bin/env python3
"""Run the PINECONe Earth Engine stages (biomass, emissions, water yield) and cache them.

Writes ONE file, stage_stats.json, that run_tev.py consumes offline. Splitting the
GEE part from the Monte Carlo part means TEV scenarios can be re-run in seconds
without touching Earth Engine.

Stages (PINECONe numbering):
  Script 1  biomass statistics   -> biomass[<AOI>_<suffix>], biomass[<AOI>_Non<suffix>]
  Script 2  carbon emissions     -> emissions[<AOI>_<suffix>]
  Script 4  water yield          -> water_yield[<AOI>]   (null if it fails; flagged)

Usage
  python run_pinecone.py --config config.yaml --out results/
  python run_pinecone.py --config config.yaml --out results/ --check   # validate config only, no GEE
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

import yaml

SKILL = "pinecone-rx-fire-valuation"
SKILL_VERSION = "0.1.0"
PRODUCTS = ("esa_cci_agb", "gedi_l4b", "whrc")


def fail(msg: str) -> None:
    sys.exit(f"ERROR: {msg}")


def check_config(cfg: dict) -> list[str]:
    errs: list[str] = []
    if not cfg.get("aois"):
        errs.append("aois: at least one {name: asset_id_or_geojson_path} required")
    for name, src in (cfg.get("aois") or {}).items():
        if not str(src).startswith("projects/") and not Path(str(src)).exists():
            errs.append(f"aois.{name}: '{src}' is neither a GEE asset id (projects/...) nor an existing file")
        if "_" in name and name.endswith(("_LLP", "_NonLLP")):
            errs.append(f"aois.{name}: don't put the species suffix in the AOI name; it is added automatically")
    fs = cfg.get("focal_species") or {}
    if not fs.get("layer"):
        errs.append("focal_species.layer: GEE image asset id required")
    bio = cfg.get("biomass") or {}
    if bio.get("product", "esa_cci_agb") not in PRODUCTS:
        errs.append(f"biomass.product must be one of {PRODUCTS}")
    em = cfg.get("emissions") or {}
    for k in ("pre", "post"):
        v = em.get(k)
        if not (isinstance(v, list) and len(v) == 2):
            errs.append(f"emissions.{k}: [start, end] as YYYY-MM-DD required")
    try:
        pre = [dt.date.fromisoformat(str(d)) for d in em["pre"]]
        post = [dt.date.fromisoformat(str(d)) for d in em["post"]]
        if not (pre[0] < pre[1] <= post[0] < post[1]):
            errs.append("emissions: need pre_start < pre_end <= post_start < post_end")
        if pre[0].year == post[0].year:
            errs.append("emissions: pre and post fall in the same year; ESA-CCI AGB is annual, change will be ~0")
    except (KeyError, ValueError, TypeError):
        pass
    wy = cfg.get("water_yield") or {}
    if wy.get("enabled", True) and not (wy.get("start") and wy.get("end")):
        errs.append("water_yield: start and end required when enabled")
    return errs


def load_aoi(ee, src: str):
    if str(src).startswith("projects/"):
        return ee.FeatureCollection(src)
    gj = json.loads(Path(src).read_text())
    if gj.get("type") != "FeatureCollection":
        gj = {"type": "FeatureCollection", "features": [gj if gj.get("type") == "Feature" else {"type": "Feature", "geometry": gj, "properties": {}}]}
    return ee.FeatureCollection(gj)


def need(value, what: str):
    if value is None:
        fail(f"{what} came back null from Earth Engine (empty mask, AOI outside coverage, or null propagation). "
             "Check the AOI overlaps the focal-species layer and the product covers the year.")
    return value


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--check", action="store_true", help="validate config and exit (no Earth Engine calls)")
    a = ap.parse_args()

    cfg = yaml.safe_load(a.config.read_text()) or {}
    errs = check_config(cfg)
    if errs:
        print("\n".join(f"CONFIG {e}" for e in errs))
        return 1
    if a.check:
        print("Config OK")
        return 0

    import ee
    try:
        from pinecone.data.biomass import BiomassData
        from pinecone.data.focal_species import FocalSpeciesLayer
        from pinecone.carbon.biomass_stats import BiomassStatsCalculator
        from pinecone.carbon.biomass_change import BiomassChangeCalculator
        from pinecone.ecosystem.water_yield import WaterYieldCalculator
    except ImportError as e:
        fail(f"{e}. Install PINECONe: pip install pinecone-fire  (note: the Pinecone vector-DB SDK also "
             "installs a 'pinecone' module and will shadow it; uninstall it in this env)")

    ee.Initialize(project=cfg.get("gee_project")) if cfg.get("gee_project") else ee.Initialize()

    fs_cfg = cfg["focal_species"]
    sfx = fs_cfg.get("suffix", "LLP")
    focal = FocalSpeciesLayer(layer_source=fs_cfg["layer"], binary_threshold=fs_cfg.get("threshold", 0),
                              name=fs_cfg.get("name", "Focal Species"))
    bio_cfg = cfg.get("biomass") or {}
    em_cfg = cfg["emissions"]
    wy_cfg = cfg.get("water_yield") or {}
    aois = {n: load_aoi(ee, s) for n, s in cfg["aois"].items()}

    out = {"biomass": {}, "emissions": {}, "water_yield": {}, "flags": []}

    # ---- Script 1: biomass ----
    biomass = BiomassData(product=bio_cfg.get("product", "esa_cci_agb"), year=bio_cfg.get("year", 2019))
    calc = BiomassStatsCalculator(biomass)
    vec_scale = bio_cfg.get("vectorize_scale", 30)
    red_scale = bio_cfg.get("reduce_scale", 100)
    for name, fc in aois.items():
        print(f"[biomass] {name}")
        sp = focal.vectorize(fc, scale=vec_scale)
        non = focal.get_non_species_areas(fc, sp.union(1).geometry())
        stats = calc.calculate_stats(sp, f"{name}_{sfx}", scale=red_scale).merge(
            calc.calculate_stats(non, f"{name}_Non{sfx}", scale=red_scale))
        for f in calc.calculate_zone_summary(stats).getInfo()["features"]:
            p = f["properties"]
            out["biomass"][p["AOI_Zone"]] = {
                "AGB_per_acre_tons": need(p.get("mean_AGB_per_acre_tons"), f"{p['AOI_Zone']} mean AGB"),
                "AGB_StdDev_per_acre_tons": p.get("mean_StdDev_per_acre_tons") or 0.0,
                "total_area_acres": p.get("total_area_acres"),
                "total_biomass_tons": p.get("total_biomass_tons"),
            }

    # ---- Script 2: emissions ----
    if bio_cfg.get("product", "esa_cci_agb") != "esa_cci_agb":
        out["flags"].append("emissions_product_fixed: PINECONe emissions always use ESA-CCI AGB regardless of biomass.product")
    em_calc = BiomassChangeCalculator(biomass_data=None, focal_species=focal,
                                      carbon_fraction=em_cfg.get("carbon_fraction", 0.51), credit_price_per_ton=1.0)
    for name, fc in aois.items():
        print(f"[emissions] {name}")
        r = em_calc.calculate_change(em_cfg["pre"][0], em_cfg["pre"][1], em_cfg["post"][0], em_cfg["post"][1],
                                     fc, resolution=em_cfg.get("resolution", 100),
                                     apply_quality_filter=em_cfg.get("quality_filter", True))
        out["emissions"][f"{name}_{sfx}"] = {
            "CO2_mean_tons_per_acre": need(r.get("CO2_mean_tons_per_acre"), f"{name} CO2 mean"),
            "CO2_std_tons_per_acre": r.get("CO2_std_tons_per_acre") or 0.0,
            "CO2_total_tons": r.get("CO2_total_tons"),
            "area_acres": r.get("area_acres"),
        }

    # ---- Script 4: water yield ----
    if wy_cfg.get("enabled", True):
        wc = WaterYieldCalculator(water_price_per_kl=wy_cfg.get("price_per_kl", 0.018),
                                  et_scale_factor=wy_cfg.get("et_scale_factor", 0.1))
        for name, fc in aois.items():
            print(f"[water] {name}")
            try:
                out["water_yield"][name] = wc.calculate_water_yield(fc, wy_cfg["start"], wy_cfg["end"],
                                                                    scale=wy_cfg.get("scale", 500))
            except Exception as e:  # noqa: BLE001 - PINECONe raises bare ValueError/EEException
                out["water_yield"][name] = None
                out["flags"].append(f"water_yield_failed:{name}: {e}")
    else:
        out["flags"].append("water_yield_disabled")

    out["provenance"] = {
        "config": cfg,
        "species_suffix": sfx,
        "created": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "skill": SKILL,
        "skill_version": SKILL_VERSION,
    }
    a.out.mkdir(parents=True, exist_ok=True)
    (a.out / "stage_stats.json").write_text(json.dumps(out, indent=2, default=str))
    print(f"Wrote {a.out / 'stage_stats.json'}  ({len(out['flags'])} flag(s))")
    for f in out["flags"]:
        print(f"FLAG  {f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
