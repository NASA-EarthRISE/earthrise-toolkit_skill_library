# Solution Implementation & Impact Monitoring Plan (SIIMP)

![status](https://img.shields.io/badge/skill-draft-lightgrey) ![domain](https://img.shields.io/badge/domain-Solution__Management-purple) ![toolkit](https://img.shields.io/badge/SCO%20toolkit-v0.1-informational)

**What:** Assembles the 15-section SIIMP from other toolkit outputs with Gantt, budget tables 1–5, and indicator matrix.
**When to use:** for a SIIMP, implementation plan, monitoring plan, project schedule or Gantt chart, budget tables, roles and responsibilities, or to assemble co-development outputs into one plan.
**Owner:** @MayerT1
**Source:** [https://science.data.nasa.gov/earth-science-solution-co-development-toolkit/implementation-monitoring/](https://science.data.nasa.gov/earth-science-solution-co-development-toolkit/implementation-monitoring/)

Part of the **Solution Co-Development Toolkit** skill set (`sco-*`). Install `sco-toolkit-orchestrator` alongside any `sco-*` skill for routing and `/status`.

## Install
- **Claude Code:** copy this folder to `~/.claude/skills/sco-10-implementation-monitoring-plan/` (or a project's `.claude/skills/`).
- **Claude app:** `python scripts/package_skill.py Solution_Management/sco-10-implementation-monitoring-plan` → upload the zip.

## Inputs → Outputs
| In | Out |
|---|---|
| `project.plan`, `report.md`, `metrics.json` | `project.plan` |

Every run also emits Markdown tables with the NASA fillable template headers, a pasteable CSV, a `solution-profile.yaml` patch, and a Quality Gate checklist.

## Example
Prompt: "Assemble our SIIMP from this solution profile."
Result: Prints a coverage table for sections 1–15; Offers to run missing owning skills by id.

## Chains with
- Upstream: `sco-01-designing-for-impact`, `sco-04-stakeholder-mapping`, `sco-06-information-chain-analysis`, `sco-08-technical-requirements`, `sco-09-data-governance-storage`, `sco-11-adoption-sustainability`, `sco-12-meaningful-metrics`, `sco-03-economic-impact-assessment`
- Downstream: `sco-02-capturing-communicating-impact`, `sco-00-trust-marker`, `partner-status-brief`

## Changelog
- 0.1.0 — initial draft, converted from the AI-ready Solution Co-Development Toolkit guides.
