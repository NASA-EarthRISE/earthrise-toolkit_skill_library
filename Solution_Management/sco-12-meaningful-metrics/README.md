# Meaningful Metrics

![status](https://img.shields.io/badge/skill-draft-lightgrey) ![domain](https://img.shields.io/badge/domain-Solution__Management-purple) ![toolkit](https://img.shields.io/badge/SCO%20toolkit-v0.1-informational)

**What:** Develops SMART input/output/outcome/impact indicators and fills the 15-column Fillable Indicator Template.
**When to use:** for indicators, KPIs, metrics, an indicator matrix, SMART metrics, baselines and targets, or to fill the NASA Fillable Indicator Template.
**Owner:** @MayerT1
**Source:** [https://science.data.nasa.gov/earth-science-solution-co-development-toolkit/meaningful-metrics/](https://science.data.nasa.gov/earth-science-solution-co-development-toolkit/meaningful-metrics/)

Part of the **Solution Co-Development Toolkit** skill set (`sco-*`). Install `sco-toolkit-orchestrator` alongside any `sco-*` skill for routing and `/status`.

## Install
- **Claude Code:** copy this folder to `~/.claude/skills/sco-12-meaningful-metrics/` (or a project's `.claude/skills/`).
- **Claude app:** `python scripts/package_skill.py Solution_Management/sco-12-meaningful-metrics` → upload the zip.

## Inputs → Outputs
| In | Out |
|---|---|
| `project.plan`, `metrics.json` | `project.plan` |

Every run also emits Markdown tables with the NASA fillable template headers, a pasteable CSV, a `solution-profile.yaml` patch, and a Quality Gate checklist.

## Example
Prompt: "Build our indicator matrix from this results framework."
Result: Table has exactly the 15 template columns in order; Rows grouped under Solution-Level Expected Outcome headings; CSV block included.

## Chains with
- Upstream: `sco-01-designing-for-impact`, `sco-07-user-centered-design`, `sco-03-economic-impact-assessment`
- Downstream: `sco-10-implementation-monitoring-plan`, `sco-02-capturing-communicating-impact`

## Changelog
- 0.1.0 — initial draft, converted from the AI-ready Solution Co-Development Toolkit guides.
