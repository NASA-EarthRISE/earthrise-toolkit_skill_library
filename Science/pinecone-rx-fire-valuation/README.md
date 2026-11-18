# PINECONe Prescribed-Fire Valuation

![status](https://img.shields.io/badge/skill-draft-lightgrey) ![domain](https://img.shields.io/badge/domain-Science-teal)

**What:** Runs [PINECONe](https://github.com/NASA-EarthRISE/earthrise-toolkit_PINECONe) end to end. It computes focal-species biomass, carbon change and water yield in Earth Engine, then a Monte Carlo Total Economic Value for each management scenario, written to the shared `metrics.json` contract.
**When to use:** "run PINECONe", "TEV for burn vs wildfire", "prescribed fire economics", "carbon credit value of the burn", "re-run TEV with $25 carbon".
**Owner:** @MayerT1

## Install
- **Claude Code:** copy this folder to `~/.claude/skills/pinecone-rx-fire-valuation/`.
- **Claude app:** `python scripts/package_skill.py Science/pinecone-rx-fire-valuation`, then upload `dist/pinecone-rx-fire-valuation.zip` in Claude's skills settings.
- Runtime: `pip install pinecone-fire pyyaml`, plus an authenticated `earthengine-api` for the GEE stage only.

## Inputs → Outputs
| In | Out |
|---|---|
| `aoi.geojson` / `dataset.vector`, `dataset.raster` (focal species), `tev_params.yaml` | `metrics.json`, `report.md`, `figure.png` |

## Two-stage design
```
config.yaml ──run_pinecone.py (GEE, slow)──▶ stage_stats.json ──run_tev.py (offline, seconds)──▶ metrics.json, figures, report_draft.md
                                                                   ▲
                                                     tev_params.yaml (prices, costs, acres)
```
If only the economics change, re-run `run_tev.py` and leave the GEE stage alone.

## Run the scripts directly
```bash
python scripts/run_pinecone.py --config assets/config_template.yaml --out results/ --check   # config check, no GEE
python scripts/run_tev.py --stats evals/files/stage_stats.json --params evals/files/tev_params.yaml --out /tmp/tev
#        Case  Acres      Mean_TEV ...
# EIA_CS1_LLP 651.06 -6.605222e+05 ...
# FLAG  water_value_fallback:EIA_CS2_LLP: ...
```
`evals/files/stage_stats.json` is a **synthetic** fixture, not Gulf State Park results. For a fixed seed, `run_tev.py` gives exactly the same results as `pinecone.economics.tev_calculator.TEVCalculator.run_monte_carlo`.

## Known PINECONe issues surfaced by this skill
See `references/pitfalls.md`. The emissions per-acre value scales with resolution, the README's sign convention is inverted, the water value falls back silently to $100/acre, and defaults are chosen by substring match. The skill flags these; it does not patch the package.

## Chains with
- Downstream: `partner-status-brief` (Solution_Management), `reproducible-release` (GIT).

## Changelog
- 0.1.0: initial skill wrapping pinecone-fire 0.1.0 (Scripts 1, 2, 3 and 4).
