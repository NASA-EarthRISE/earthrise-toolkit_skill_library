# Economic Impact Assessment

![status](https://img.shields.io/badge/skill-draft-lightgrey) ![domain](https://img.shields.io/badge/domain-Solution__Management-purple) ![toolkit](https://img.shields.io/badge/SCO%20toolkit-v0.1-informational)

**What:** Scopes an EIA (high-level vs in-depth), plans baseline/attribution data, and computes transparent value estimates with sensitivity ranges.
**When to use:** for ROI, economic value, value of information, cost-benefit, socio-economic benefit, or economic impact of an Earth observation solution.
**Owner:** @MayerT1
**Source:** [https://science.data.nasa.gov/earth-science-solution-co-development-toolkit/economic-impact-assessments/](https://science.data.nasa.gov/earth-science-solution-co-development-toolkit/economic-impact-assessments/)

Part of the **Solution Co-Development Toolkit** skill set (`sco-*`). Install `sco-toolkit-orchestrator` alongside any `sco-*` skill for routing and `/status`.

## Install
- **Claude Code:** copy this folder to `~/.claude/skills/sco-03-economic-impact-assessment/` (or a project's `.claude/skills/`).
- **Claude app:** `python scripts/package_skill.py Solution_Management/sco-03-economic-impact-assessment` → upload the zip.

## Inputs → Outputs
| In | Out |
|---|---|
| `partner.request`, `project.plan` | `metrics.json`, `report.md` |

Every run also emits Markdown tables with the NASA fillable template headers, a pasteable CSV, a `solution-profile.yaml` patch, and a Quality Gate checklist.

## Example
Prompt: "High-level EIA: 5000 farmers, 200 acres each, $25/acre irrigation, 15% reduction, multiplier 1.4."
Result: Direct = $3,750,000 and Total = $5,250,000; Shows a low/base/high sensitivity range; Writes metrics.json-shaped result.

## Chains with
- Upstream: `sco-01-designing-for-impact`, `sco-05-needs-assessment`
- Downstream: `sco-12-meaningful-metrics`, `sco-10-implementation-monitoring-plan`, `sco-02-capturing-communicating-impact`

## Changelog
- 0.1.0 — initial draft, converted from the AI-ready Solution Co-Development Toolkit guides.
