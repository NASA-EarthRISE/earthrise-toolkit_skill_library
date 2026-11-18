# Classification Accuracy Assessment

![status](https://img.shields.io/badge/skill-draft-lightgrey) ![domain](https://img.shields.io/badge/domain-Science-teal)

**What:** Program-standard accuracy assessment and area estimation (Olofsson et al. 2014) for classified maps.
**When to use:** "how accurate is this map", "confusion matrix", "validate my classification", "area estimate with CIs".
**Owner:** @MayerT1

## Install
- **Claude Code:** copy this folder to `~/.claude/skills/classification-accuracy-assessment/`.
- **Claude app:** `python scripts/package_skill.py Science/classification-accuracy-assessment` → upload `dist/classification-accuracy-assessment.zip` in Claude's skills settings.

## Inputs → Outputs
| In | Out |
|---|---|
| `samples.csv`, `dataset.raster` (mapped areas) | `metrics.json`, `report.md` |

## Run the script directly
```bash
python scripts/accuracy_assessment.py --samples evals/files/samples.csv --areas evals/files/areas.csv --out results/ --unit pixels
# Overall accuracy 0.947 (95% CI 0.928-0.965), n=640
```
The bundled eval data is the worked example from Olofsson et al. (2014) §5; the script reproduces its published overall/user's/producer's accuracy and deforestation area.

## Chains with
- Downstream: `partner-status-brief` (Solution_Management), `reproducible-release` (GIT).

## Changelog
- 0.1.0 — initial seed skill.
