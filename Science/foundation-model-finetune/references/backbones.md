# Backbone notes (TerraTorch)

Verify names against your install:
```python
from terratorch.registry import BACKBONE_REGISTRY
print([m for m in BACKBONE_REGISTRY if "prithvi" in m or "terramind" in m])
```

## Prithvi-EO (NASA/IBM)
Documented TerraTorch names: `prithvi_eo_v1_100`, `prithvi_eo_v2_tiny_tl`, `prithvi_eo_v2_100_tl`,
`prithvi_eo_v2_300`, `prithvi_eo_v2_300_tl`, `prithvi_eo_v2_600`, `prithvi_eo_v2_600_tl`.
`_tl` variants accept optional time and location metadata.

| Setting | Value |
|---|---|
| Pretraining bands (HLS) | BLUE, GREEN, RED, NIR_NARROW, SWIR_1, SWIR_2 |
| `backbone_bands` | Your bands, in on-disk order; extra/missing bands get new or dropped patch-embed weights |
| `backbone_num_frames` | 1 for single date; T for time series (input shape B,C,T,H,W) |
| Necks (UNet/UperNet decoders) | `SelectIndices` → `ReshapeTokensToImage` → `LearnedInterpolateToPyramidal` |
| `SelectIndices` | 300M/600M (24/32 layers): e.g. `[5, 11, 17, 23]`; 100M (12 layers): `[2, 5, 8, 11]` |
| Input scaling | Match the model card (HLS reflectance); a scale mismatch fails silently |

## TerraMind (IBM/ESA)
Multimodal (S2, S1, DEM, LULC…). Uses `backbone_modalities` (e.g. `[S2L1C, S1GRD]`) instead of `backbone_bands`;
set `backbone_bands: null` in the matrix run to remove the recipe default. See the TerraMind configs in IBM/terramind.

## Other backbones
Any timm/SMP backbone in the registry can serve as a baseline encoder. For SatMAE, Clay, DOFA etc.,
check the registry first; if a model isn't registered, document how it was wrapped in the report.

## Baselines (required)
| Task | Minimum baseline |
|---|---|
| Segmentation | UNet (ResNet-34) from scratch, same chips (`SMPModelFactory`) |
| Pixel regression | UNet from scratch **and** a random forest on per-pixel features from the same chips |
| Classification | ResNet-50 from scratch or ImageNet |
