---
name: classification-accuracy-assessment
description: Run an area-adjusted accuracy assessment (Olofsson et al. 2014 stratified estimator) for a land-cover, land-use or change map from reference samples, producing overall, user's and producer's accuracy and area estimates with confidence intervals. Use when someone asks for map accuracy, a confusion or error matrix, validation of a classification, or unbiased area estimates with CIs.
---

# Classification Accuracy Assessment

## Purpose
Produce the program-standard, statistically defensible accuracy and area report
for any classified map: stratified estimator with strata = map classes, 95% CIs,
written to the shared `metrics.json` contract so GIT and Solution Management
skills can consume it without re-interpretation.

## Inputs
- `samples.csv` — one row per reference sample with `sample_id, map_class, ref_class` (`x, y, stratum` optional). Reference labels come from interpretation, never from the map itself.
- A per-class **mapped area** table (`class, area`), typically exported from the `dataset.raster` (pixel counts are fine).

## Outputs
- `metrics.json` — overall / user's / producer's accuracy and area per class, each `{value, se, ci_low, ci_high}`.
- `report.md` — Methods / Results / Limitations section ready to paste into a technical report.
- Also written: `confusion_matrix.csv`, `area_proportions.csv`.

## Steps
1. **Check inputs.** Confirm both files exist and class names match between them. If the mapped-area table is missing, ask for it or, if the user has the raster in GEE, give them the `ee.Image.reduceRegion(ee.Reducer.frequencyHistogram())` snippet to get pixel counts. Do not proceed without areas — unweighted accuracy is not the program standard.
2. **Check the design.** Ask (once) whether sampling was stratified by map class. If it was simple random or systematic, note it in Limitations; the estimator remains valid with strata = map classes when samples are labeled by map class. Every mapped class needs ≥ 2 samples (script enforces this).
3. **Run the estimator** — never compute by hand:
   ```bash
   python scripts/accuracy_assessment.py --samples samples.csv --areas areas.csv --out results/ --unit ha --dataset "<name>"
   ```
4. **Write `report.md`** using `references/report_template.md`: one table of user's/producer's accuracy with ± (1.96·SE), one table of estimated area vs mapped area, and the confusion matrix of counts.
5. **Interpret in 3–5 lines:** which classes are weakest, whether mapped area over/under-estimates the reference-based estimate, and whether any CI is wide enough to change a decision.
6. **Hand off:** tell the user `metrics.json` can go straight to `partner-status-brief` (Solution_Management) and `reproducible-release` (GIT).

## Guardrails
- Never fabricate, round away, or "smooth" accuracy numbers; every number must come from `metrics.json`.
- Never report accuracy without its confidence interval or without stating n.
- Never use map pixel counts as the area estimate; report the sample-based estimate and show mapped area only for comparison.
- Do not include sample coordinates in outputs if `data_sensitivity` of the source is `partner-restricted`.

## Example
**Input:** 640 samples across 4 classes; mapped areas 200,000 / 150,000 / 3,200,000 / 6,450,000 px (Olofsson et al. 2014, §5).
**Output:** overall accuracy 0.947 ± 0.018; deforestation user's 0.88 ± 0.07, producer's 0.75 ± 0.21; estimated deforestation area 235,086 ± 68,418 px vs 200,000 mapped.

## Hand-offs
- Upstream: any Science mapping skill that emits `dataset.raster`.
- Downstream: `partner-status-brief` (consumes `metrics.json`), `reproducible-release` (attaches `metrics.json` to release notes).

## References
- `references/report_template.md` — read at step 4.
- `references/method_notes.md` — read when the user asks about the math, sample size, or non-stratified designs.
