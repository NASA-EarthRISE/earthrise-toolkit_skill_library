# Technical Requirements

![status](https://img.shields.io/badge/skill-draft-lightgrey) ![domain](https://img.shields.io/badge/domain-Solution__Management-purple) ![toolkit](https://img.shields.io/badge/SCO%20toolkit-v0.1-informational)

**What:** Completes the Technical Requirements Template: partner questions, data source specs, architecture, I/O, platforms, validation, capacities.
**When to use:** for technical requirements, data source specs, system architecture, MVP definition, processing or deployment platforms, or partner agreements for an EO solution.
**Owner:** @MayerT1
**Source:** [https://science.data.nasa.gov/earth-science-solution-co-development-toolkit/technical-requirements/](https://science.data.nasa.gov/earth-science-solution-co-development-toolkit/technical-requirements/)

Part of the **Solution Co-Development Toolkit** skill set (`sco-*`). Install `sco-toolkit-orchestrator` alongside any `sco-*` skill for routing and `/status`.

## Install
- **Claude Code:** copy this folder to `~/.claude/skills/sco-08-technical-requirements/` (or a project's `.claude/skills/`).
- **Claude app:** `python scripts/package_skill.py Solution_Management/sco-08-technical-requirements` → upload the zip.

## Inputs → Outputs
| In | Out |
|---|---|
| `partner.request`, `report.md` | `report.md` |

Every run also emits Markdown tables with the NASA fillable template headers, a pasteable CSV, a `solution-profile.yaml` patch, and a Quality Gate checklist.

## Example
Prompt: "Fill the technical requirements template for a daily flood extent product for district officials."
Result: Includes both template tables with exact row labels; Data source table has access, resolution, latency, processing level.

## Chains with
- Upstream: `sco-05-needs-assessment`, `sco-06-information-chain-analysis`, `sco-07-user-centered-design`, `sco-04-stakeholder-mapping`
- Downstream: `sco-09-data-governance-storage`, `sco-10-implementation-monitoring-plan`, `sco-11-adoption-sustainability`

## Changelog
- 0.1.0 — initial draft, converted from the AI-ready Solution Co-Development Toolkit guides.
