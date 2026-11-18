# Information Chain Analysis

![status](https://img.shields.io/badge/skill-draft-lightgrey) ![domain](https://img.shields.io/badge/domain-Solution__Management-purple) ![toolkit](https://img.shields.io/badge/SCO%20toolkit-v0.1-informational)

**What:** Traces one decision pathway as numbered chain links, stress-tests handoffs, prioritizes breakdowns, and assigns actions and assumptions.
**When to use:** how information reaches decision-makers, to map an alert or dissemination chain, find bottlenecks or breakdowns, or stress-test delivery of EO products to end users.
**Owner:** @MayerT1
**Source:** [https://science.data.nasa.gov/earth-science-solution-co-development-toolkit/information-chain-analysis/](https://science.data.nasa.gov/earth-science-solution-co-development-toolkit/information-chain-analysis/)

Part of the **Solution Co-Development Toolkit** skill set (`sco-*`). Install `sco-toolkit-orchestrator` alongside any `sco-*` skill for routing and `/status`.

## Install
- **Claude Code:** copy this folder to `~/.claude/skills/sco-06-information-chain-analysis/` (or a project's `.claude/skills/`).
- **Claude app:** `python scripts/package_skill.py Solution_Management/sco-06-information-chain-analysis` → upload the zip.

## Inputs → Outputs
| In | Out |
|---|---|
| `partner.request`, `report.md` | `report.md` |

Every run also emits Markdown tables with the NASA fillable template headers, a pasteable CSV, a `solution-profile.yaml` patch, and a Quality Gate checklist.

## Example
Prompt: "Map the information chain from flood forecast to household evacuation."
Result: Step 1 Anchor table with the six exact fields; Links C1..Cn with breakdown types from delay/capacity/access/trust/distortion.

## Chains with
- Upstream: `sco-04-stakeholder-mapping`, `sco-05-needs-assessment`
- Downstream: `sco-07-user-centered-design`, `sco-08-technical-requirements`, `sco-12-meaningful-metrics`, `sco-11-adoption-sustainability`

## Changelog
- 0.1.0 — initial draft, converted from the AI-ready Solution Co-Development Toolkit guides.
