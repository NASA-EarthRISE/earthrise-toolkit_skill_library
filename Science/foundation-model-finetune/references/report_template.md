# GeoFM Intercomparison — {experiment}

## Purpose
{Task, classes/target, decision it supports, primary metric and the bar that matters.}

## Data
- Recipe: `{recipe name}` · bands (on-disk order): {bands} · {resolution} m · chips {H}×{W} · {CRS}
- Scaling: {scale_note} · Norm stats from train split only
- Splits: {method}, {n_train}/{n_val}/{n_test} chips · {block_note}
- `check_recipe.py`: PASS on train/val/test {and inference roots}

## Methods
- TerraTorch {version}, Lightning CLI; decoder {UNet/UperNet}; AdamW lr {lr}; ≤ {max_epochs} epochs, early stopping on val/loss
- Runs: {list} × seeds {seeds}; baseline: {baseline}
- Test split evaluated once per final config

## Results
{paste leaderboard.md}

## Interpretation
- {Does any FM beat the baseline by more than seed noise? By how much, and does that change the decision?}
- {Frozen vs fine-tuned: is the pretrained encoder doing the work?}
- {Compute cost vs gain}

## Limitations
- {Domain shift to new AOIs, label quality, temporal mismatch, patch-level vs map-level accuracy}

## Next
- {e.g. hand predictions to classification-accuracy-assessment for map accuracy; release via reproducible-release}
