---
name: pinecone-rx-fire-valuation
description: Run the PINECONe workflow (Pine Ecosystem Carbon and ECOnomics) to value prescribed-fire and wildfire scenarios for a pine ecosystem. It computes focal-species biomass, carbon emissions or sequestration from biomass change, and water yield in Google Earth Engine, then estimates Total Economic Value (timber, carbon credits, ecosystem services, lease NPV) with Monte Carlo uncertainty. Use when someone asks for PINECONe, the TEV of burn vs no-burn or wildfire scenarios, prescribed fire economics, carbon credit value from a burn, longleaf pine ecosystem service valuation, or wants TEV re-run with new prices or parameters.
---

# PINECONe Prescribed-Fire Valuation

## Purpose
Produce the program-standard PINECONe valuation for one or more management
scenarios (e.g. severe wildfire, mitigated wildfire, prescribed burn) over a
focal-species stand. The Earth Engine stages run once and are cached, the TEV Monte
Carlo re-runs in seconds, and every number is written to the shared
`metrics.json` contract so `partner-status-brief` and `reproducible-release` can
use it directly. The run calls the released `pinecone-fire` package. It never
re-implements the model, and its numbers match `TEVCalculator.run_monte_carlo`
exactly for the same seed.

## Inputs
- `aoi.geojson` or `dataset.vector`: one AOI per scenario, either a GEE FeatureCollection id or a GeoJSON file in EPSG:4326.
- `dataset.raster`: the focal-species layer as a GEE image id, where values above the threshold count as the species (e.g. LEO extant LLP significance).
- The economic parameters for each scenario and the acres for each scenario, written to `tev_params.yaml`.

## Outputs
- `metrics.json`: mean TEV per scenario (`<zone>.tev_usd`, `<zone>.tev_usd_per_acre`), with `ci_low` and `ci_high` set to the 2.5 and 97.5 simulation percentiles. It also holds the component breakdown, the scenario comparison, the full parameters, `flags`, and upstream provenance.
- `report.md`: Purpose, Methods, Results and Limitations, built from `references/report_template.md`.
- `figure.png`: `figures/tev_distributions.png` and `figures/tev_boxplots.png`, each with a `.txt` caption.
- Also written: `stage_stats.json`, `tev_summary.csv`, `tev_components.csv`, `scenario_comparison.csv`, `tev_simulations.npz`, `report_draft.md`.

## Steps
1. **Intake.** Collect the AOIs, the focal-species layer, the biomass year, the pre and post date windows for emissions, the water-yield window, the carbon credit price, and the acres for each scenario. Ask once for anything that is missing. If the user has no economic parameters, offer `assets/tev_params_template.yaml` and tell them its values are the Gulf State Park EIA CS1–CS3 scenarios, not general defaults.
2. **Configure.** Copy `assets/config_template.yaml` to `config.yaml` and `assets/tev_params_template.yaml` to `tev_params.yaml`, then fill both in. Zone keys in the params file are `<AOI>_<suffix>` (e.g. `EIA_CS2_LLP`).
3. **Validate the config without Earth Engine:**
   ```bash
   python scripts/run_pinecone.py --config config.yaml --out results/ --check
   ```
   Fix every `CONFIG` line before you go on.
4. **Run the Earth Engine stages** (needs `pip install pinecone-fire` and an authenticated `ee`):
   ```bash
   python scripts/run_pinecone.py --config config.yaml --out results/
   ```
   If this session has no Earth Engine credentials, give the user that command to run in Colab or on their HPC, ask for `results/stage_stats.json` back, and continue from step 5. If `stage_stats.json` already exists and only the economics changed, skip this step.
5. **Inspect `stage_stats.json` before running TEV.** Read every entry in `flags`. Any null or missing zone is a stop: report it and do not continue. Check the sign of `CO2_mean_tons_per_acre`: it is post minus pre, so a **negative value means biomass loss (emissions)** and a positive value means gain. Read `references/pitfalls.md` §1–3 before you quote any per-acre carbon figure.
6. **Run the TEV Monte Carlo.** Never compute TEV by hand:
   ```bash
   python scripts/run_tev.py --stats results/stage_stats.json --params tev_params.yaml --out results/ --dataset "<site name>"
   ```
   Fix every `PARAMS` error the script reports. It refuses to run on zones without acres, on zones missing from the biomass stats, and when there is no `zones` block.
7. **Write `report.md`** from `references/report_template.md`. Paste in the tables from `report_draft.md` unchanged. Add 3–5 lines of interpretation: which component drives each scenario (from `tev_components.csv`), whether any two scenarios overlap (Cohen's d and the overlap coefficient), and how wide the intervals are. Every `flags` entry goes into Limitations.
8. **Summarize in at most 5 lines.** Give the mean TEV and the 95% interval for each scenario, the dominant component, and any flags. Point to the output files.
9. **Hand off.** `metrics.json`, `report.md` and the figures can go straight to `partner-status-brief`, and `metrics.json` to `reproducible-release`.

For a **parameter sensitivity** request (e.g. "what if carbon is $25/t"), copy `tev_params.yaml`, change only the stated values, re-run step 6 into a new `--out` folder, and compare the two `tev_summary.csv` files. Do not re-run step 4.

## Guardrails
- Never invent, round away, or adjust TEV, biomass, CO₂ or water figures. Every number must come from `stage_stats.json` or the outputs of `run_tev.py`.
- Never report a TEV without its 95% interval, the number of simulations, the seed, and the carbon price.
- Never hide the water-value fallback. If `flags` contains `water_value_fallback`, the ecosystem-services term for that zone is PINECONe's hard-coded $100 ± 2 per acre, not a measurement, and the report must say so.
- Never present the GEE stage outputs as credit-eligible carbon offsets. They are remote-sensing estimates for valuation, not a VCS, CAR or Gold Standard verification.
- Never silently rely on PINECONe's built-in CS1, CS2 or CS3 defaults. They are picked by substring match on the zone name, so state them as an explicit choice or replace them.
- Don't put partner AOI geometry or restricted asset ids into outputs that are bound for `partner-status-brief` when the source is `partner-restricted`.
- Out of scope: map accuracy (use `classification-accuracy-assessment`), model training (use `foundation-model-finetune`), and editing or patching the PINECONe package itself.

## Example
**Input:** `evals/files/stage_stats.json`, a synthetic fixture for three EIA cases where CS2 water yield failed, plus `evals/files/tev_params.yaml`, the Gulf State Park CS1–CS3 parameters at a carbon price of $10/t, 10,000 simulations and seed 42.
**Output:**
| Scenario | Mean TEV | 95% interval | $/acre |
|---|---:|---:|---:|
| EIA_CS1_LLP | -$660,522 | -$1,043,435 to -$266,965 | -$1,015 |
| EIA_CS2_LLP | $673,511 | $364,524 to $987,228 | $719 |
| EIA_CS3_LLP | $2,608,352 | $2,339,224 to $2,899,912 | $4,794 |

Flags: `water_value_fallback:EIA_CS2_LLP`. Lease NPV ($3,031/acre) dominates CS3, and carbon (-$950/acre) dominates CS1.

## Hand-offs
- Upstream: an intake `partner.request` or `aoi.geojson` from Solution_Management. Focal-species rasters come from Science mapping work.
- Downstream: `partner-status-brief` (`metrics.json`, `report.md`, `figure.png`) and `reproducible-release` (`metrics.json`).

## References
- `references/tev_model.md`: read when the user asks how TEV is computed, what a parameter means, or which units apply.
- `references/pitfalls.md`: read at step 5, and whenever a number looks off or a stage fails.
- `references/report_template.md`: read at step 7.
