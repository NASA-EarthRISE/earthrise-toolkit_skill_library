# When results look wrong

Check these in order. Most "the model is bad" findings are input problems.

| Symptom | Likely cause | Check |
|---|---|---|
| Great val/test, terrible on a new AOI (e.g. negative R² vs independent reference) | Inference chips built with a different recipe (bands, resolution, CRS, chip size, scaling, norm stats) | `check_recipe.py --root <inference chips>`; compare z-scores and the band-swap line |
| One or two bands drift by many σ | Band order swapped, or a band from a different sensor/level | Band-swap heuristic; compare to the export script |
| All bands shifted by ~×10,000 | DN vs reflectance scaling | `dtype`, `scale_note`, band means |
| Checkerboard / patch-grid artefacts | ViT patch tokens reshaped without enough decoder upsampling, or inference stride/overlap differs from training | Necks (`LearnedInterpolateToPyramidal`), predict tiling/overlap |
| Output follows sample geometry (e.g. GEDI track lines) | Sparse supervision leaks sampling pattern; model learns where labels are, not what they are | Score against wall-to-wall independent reference, not only held-out samples |
| FM barely beats or loses to the UNet | Task may not need pretraining; or frozen/LR settings off | Frozen-encoder run, LR sweep on val only |
| Huge train/val gap | Spatial leakage or overfitting | Confirm splits are spatially blocked; augmentations |
| Seeds disagree a lot | Small data / unstable LR | Report std; more seeds before ranking |

Principle: fix **one** thing at a time and re-score against the same independent reference
(e.g. ALS plus field anchors) after each fix.
