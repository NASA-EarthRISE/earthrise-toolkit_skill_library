# Model card — {run name}

| | |
|---|---|
| Backbone | {e.g. prithvi_eo_v2_300_tl}, pretrained weights {source/version} |
| Task | {segmentation/regression/classification}: {classes or target} |
| Checkpoint | `{path or release asset URL}` (seed {n}, epoch {e}) |
| Data recipe | `{recipe name}` (include data_recipe.yaml with the checkpoint) |
| Inputs | {bands in order}, {scaling}, {chip size}, {resolution}, {CRS} |
| Test performance | {metric} = {mean ± std over seeds} (this checkpoint: {value}) |
| Baseline | {baseline}: {metric} = {value} |
| Training region / period | {AOIs, dates} |
| Intended use | {decision / product} |
| Out of scope | {regions, sensors, seasons not represented} |
| Known limitations | {…} |
| Owner / contact | {@handle} |

**Before using on new data:** run `check_recipe.py --recipe data_recipe.yaml --root <new chips>`; all checks must PASS.
