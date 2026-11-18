# User-Centered Design

![status](https://img.shields.io/badge/skill-draft-lightgrey) ![domain](https://img.shields.io/badge/domain-Solution__Management-purple) ![toolkit](https://img.shields.io/badge/SCO%20toolkit-v0.1-informational)

**What:** Builds decision-anchored personas and runs the four-step UCD method through validation under decision conditions.
**When to use:** for personas, UI or dashboard design requirements, alert threshold presentation, usability testing, or behavioral hypotheses for an EO decision tool.
**Owner:** @MayerT1
**Source:** [https://science.data.nasa.gov/earth-science-solution-co-development-toolkit/user-centered-design/](https://science.data.nasa.gov/earth-science-solution-co-development-toolkit/user-centered-design/)

Part of the **Solution Co-Development Toolkit** skill set (`sco-*`). Install `sco-toolkit-orchestrator` alongside any `sco-*` skill for routing and `/status`.

## Install
- **Claude Code:** copy this folder to `~/.claude/skills/sco-07-user-centered-design/` (or a project's `.claude/skills/`).
- **Claude app:** `python scripts/package_skill.py Solution_Management/sco-07-user-centered-design` → upload the zip.

## Inputs → Outputs
| In | Out |
|---|---|
| `partner.request`, `report.md` | `report.md` |

Every run also emits Markdown tables with the NASA fillable template headers, a pasteable CSV, a `solution-profile.yaml` patch, and a Quality Gate checklist.

## Example
Prompt: "Build a persona for the district officer who decides when to evacuate."
Result: Passes the 4-part design-ready test; Has a behavioral hypothesis in 'If we design ___, then this persona will ___' form.

## Chains with
- Upstream: `sco-04-stakeholder-mapping`, `sco-05-needs-assessment`, `sco-06-information-chain-analysis`, `sco-01-designing-for-impact`
- Downstream: `sco-08-technical-requirements`, `sco-10-implementation-monitoring-plan`, `sco-12-meaningful-metrics`, `sco-11-adoption-sustainability`

## Changelog
- 0.1.0 — initial draft, converted from the AI-ready Solution Co-Development Toolkit guides.
