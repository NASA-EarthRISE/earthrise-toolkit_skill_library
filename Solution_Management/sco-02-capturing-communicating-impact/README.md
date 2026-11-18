# Capturing & Communicating Impact

![status](https://img.shields.io/badge/skill-draft-lightgrey) ![domain](https://img.shields.io/badge/domain-Solution__Management-purple) ![toolkit](https://img.shields.io/badge/SCO%20toolkit-v0.1-informational)

**What:** Plans audiences and evidence for impact communication and drafts NASA-format products (highlight, use case, case study, blog, press release).
**When to use:** for a use case, case study, impact story, NASA blog post, press release, internal HQ highlight, communications plan, or how to show impact to an audience.
**Owner:** @MayerT1
**Source:** [https://science.data.nasa.gov/earth-science-solution-co-development-toolkit/capturing-communicating-impact/](https://science.data.nasa.gov/earth-science-solution-co-development-toolkit/capturing-communicating-impact/)

Part of the **Solution Co-Development Toolkit** skill set (`sco-*`). Install `sco-toolkit-orchestrator` alongside any `sco-*` skill for routing and `/status`.

## Install
- **Claude Code:** copy this folder to `~/.claude/skills/sco-02-capturing-communicating-impact/` (or a project's `.claude/skills/`).
- **Claude app:** `python scripts/package_skill.py Solution_Management/sco-02-capturing-communicating-impact` → upload the zip.

## Inputs → Outputs
| In | Out |
|---|---|
| `project.plan`, `metrics.json`, `report.md` | `stakeholder.brief`, `report.md` |

Every run also emits Markdown tables with the NASA fillable template headers, a pasteable CSV, a `solution-profile.yaml` patch, and a Quality Gate checklist.

## Example
Prompt: "Draft a 150–200 word internal NASA highlight for our flood alert pilot using these indicator results."
Result: Word count within 150–200 plus contact info; Names NASA assets; Every number appears in the evidence ledger.

## Chains with
- Upstream: `sco-12-meaningful-metrics`, `sco-03-economic-impact-assessment`, `sco-10-implementation-monitoring-plan`
- Downstream: `partner-status-brief`

## Changelog
- 0.1.0 — initial draft, converted from the AI-ready Solution Co-Development Toolkit guides.
