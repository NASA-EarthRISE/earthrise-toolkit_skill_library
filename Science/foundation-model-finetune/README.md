# Foundation Model Fine-tune & Intercomparison

![status](https://img.shields.io/badge/skill-draft-lightgrey) ![domain](https://img.shields.io/badge/domain-Science-teal)

**What:** One defensible way to answer "does a geospatial foundation model help here, and which one?", using TerraTorch.
**When to use:** "fine-tune Prithvi", "compare foundation models", "TerraTorch experiment", "does a GeoFM beat our UNet/RF?"
**Owner:** @MayerT1

## What makes it different
- **Locked data recipe.** One `data_recipe.yaml` (bands, scaling, chips, CRS, splits, norm stats) shared by every run and by inference.
- **`check_recipe.py`** catches band-count/order, scaling, size, CRS, resolution and label problems, plus distribution drift, before any GPU time.
- **Fair matrix.** `make_configs.py` writes one config per backbone × seed from one template; only the backbone settings differ.
- **Honest leaderboard.** `collect_results.py` reports mean ± std over seeds, always includes the non-FM baseline, and flags ties.

## Install
- **Claude Code:** copy to `~/.claude/skills/foundation-model-finetune/`.
- **Claude app:** `python scripts/package_skill.py Science/foundation-model-finetune` → upload the zip.
- Python env: `pip install terratorch rasterio pyyaml`

## Quick run
```bash
cp assets/data_recipe.yaml assets/matrix.yaml my_exp/        # then edit both
python scripts/check_recipe.py --recipe my_exp/data_recipe.yaml --compute-stats   # paste norm: into recipe
python scripts/check_recipe.py --recipe my_exp/data_recipe.yaml                   # must PASS
python scripts/make_configs.py --template assets/config_template.yaml \
    --recipe my_exp/data_recipe.yaml --matrix my_exp/matrix.yaml --out experiments/
bash experiments/<exp>/run_matrix.sh
python scripts/collect_results.py --runs experiments/<exp>/runs --baseline unet_resnet34_baseline
```

## Inputs → Outputs
| In | Out |
|---|---|
| `dataset.raster` (chips + labels), `partner.request`? | `metrics.json`, `model.checkpoint`, `report.md` |

## Chains with
- Downstream: `classification-accuracy-assessment`, `reproducible-release`, `partner-status-brief`

## Changelog
- 0.1.0 — initial skill. Config keys follow TerraTorch 1.2.x docs; check them against your installed version.
