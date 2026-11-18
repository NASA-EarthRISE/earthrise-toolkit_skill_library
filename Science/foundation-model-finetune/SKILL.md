---
name: foundation-model-finetune
description: Fine-tune and fairly intercompare geospatial foundation models (Prithvi-EO-2.0, TerraMind and other TerraTorch backbones) against a non-foundation-model baseline on a segmentation, regression or classification task, using a locked data recipe, spatially blocked splits, multiple seeds and the TerraTorch CLI. Use when someone asks to fine-tune Prithvi or another GeoFM, compare foundation models, run a TerraTorch experiment or benchmark, or check whether a foundation model beats a UNet or random forest baseline.
---

# Foundation Model Fine-tune & Intercomparison

## Purpose
Give the program one defensible way to answer "does a foundation model help
here, and which one?" Every backbone sees identical data (same bands in the same
order, same scaling, chips, splits and norm stats), is run over ≥ 3 seeds, and
is scored against a non-FM baseline. Most bad GeoFM results we've seen came
from mismatched inputs, not from the model, so the recipe is locked and checked
before any GPU time is spent.

## Inputs
- `dataset.raster` — image chips (GeoTIFF) for train / val / test, plus label chips (segmentation/regression).
- Optional `partner.request` — the decision the model must support (sets the primary metric and the bar).

## Outputs
- `metrics.json` — per-backbone test metrics, mean ± std over seeds, ranking, baseline, tie warnings (from `collect_results.py`).
- `model.checkpoint` — best run's `best.ckpt` + `model_card.md` (from `references/model_card_template.md`).
- `report.md` — experiment report (from `references/report_template.md`).

## Steps
1. **Frame the task (ask once).** Task type, classes or target variable, primary metric (mIoU / F1 / RMSE…), and what result would change a decision. Write it at the top of the report. Don't start training without a primary metric.
2. **Lock the data recipe.** Copy `assets/data_recipe.yaml` to the experiment folder and fill it in: band names **in on-disk order** matching the backbone's model card, dtype and scaling, chip size, resolution, CRS, nodata, classes and split roots. Splits must be **spatially blocked** (or predefined by the dataset), never random chips.
3. **Compute norm stats from TRAIN only:**
   `python scripts/check_recipe.py --recipe data_recipe.yaml --compute-stats` → paste `norm:` into the recipe.
4. **Check the recipe:** `python scripts/check_recipe.py --recipe data_recipe.yaml`. All checks must PASS (band count, dtype, size, CRS, resolution, labels, per-band drift, band-swap heuristic). **Stop and report** any FAIL; don't train around it.
5. **Define the matrix.** Copy `assets/matrix.yaml`: list the backbones (see `references/backbones.md` for names and neck indices), ≥ 3 seeds, and **at least one non-FM baseline** (UNet from scratch; for regression, also a random forest on the same pixels). Add a frozen-encoder run when the question is "is the pretrained encoder doing the work?"
6. **Generate configs:**
   `python scripts/make_configs.py --template assets/config_template.yaml --recipe data_recipe.yaml --matrix matrix.yaml --out experiments/`
   Then smoke-test one config for 1 epoch (`terratorch fit -c <cfg> --trainer.max_epochs 1 --trainer.limit_train_batches 5`) before launching everything.
7. **Run.** `experiments/<exp>/run_matrix.sh` runs `terratorch fit` then `terratorch test` for each config. On HPC, wrap these lines in the cluster's job script; keep one config per job.
8. **Collect:** `python scripts/collect_results.py --runs experiments/<exp>/runs --baseline <baseline-name> --dataset "<name>"` → `leaderboard.md`, `metrics.json`. Report mean ± std, and say **"tie"** when the gap is within seed std (the script flags it).
9. **Write the report and model card** from `references/`. Include the leaderboard, the recipe name, the check_recipe PASS report, and limitations.
10. **Inference on new areas:** run `check_recipe.py --root <inference_chips>` against the **same** recipe before `terratorch predict`. A FAIL means the inference chips don't match training; fix the chips, not the model.
11. **Hand off.** If the output is a classified map, send predictions + reference samples to `classification-accuracy-assessment` (patch-level test mIoU is not map accuracy). Send code + `metrics.json` + checkpoint to `reproducible-release`.

## Guardrails
- Never compare runs trained on different recipes, splits or norm stats. One recipe name per experiment.
- Never fit norm stats, tune hyperparameters or choose epochs on the test split. Test is run once per final config.
- Never claim one model "wins" from a single seed or when the gap is within seed std.
- Never drop the non-FM baseline from the results, even when it wins.
- Never fabricate or hand-edit metrics; all numbers come from `collect_results.py` output.
- Don't run `check_recipe` once and assume it holds: re-run it on every new chip batch (new AOI, new export).
- Respect `data_sensitivity`: no partner-restricted chips or labels in commits, model cards or reports.
- Large checkpoints (> 50 MB) go to release assets or shared storage, never into git.

## Example
**Input:** HLS burn-scar chips (6 bands, 512 px, 30 m), spatially blocked train/val/test.
**Matrix:** `prithvi_eo_v2_300_tl`, `prithvi_eo_v2_100_tl`, `prithvi_300_frozen`, `unet_resnet34_baseline` × seeds 0, 1, 2 → 12 configs.
**Output:** `leaderboard.md` with test mIoU mean ± std per backbone, a tie note if the top two overlap, `metrics.json`, `model_card.md` for the best run, and a report recommending a backbone or saying the baseline is enough.

## Hand-offs
- Downstream: `classification-accuracy-assessment` (map-level accuracy and area estimates), `reproducible-release` (code + `metrics.json` + checkpoint), `partner-status-brief` (via `metrics.json`).

## References
- `references/backbones.md` — read at step 5 (backbone names, necks, band handling).
- `references/report_template.md`, `references/model_card_template.md` — step 9.
- `references/pitfalls.md` — read when results look implausible (e.g. negative R², checkerboard artefacts, a big train/test gap).
