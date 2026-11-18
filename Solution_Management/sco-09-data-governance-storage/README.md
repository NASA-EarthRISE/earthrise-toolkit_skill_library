# Data Governance & Storage Plan

![status](https://img.shields.io/badge/skill-draft-lightgrey) ![domain](https://img.shields.io/badge/domain-Solution__Management-purple) ![toolkit](https://img.shields.io/badge/SCO%20toolkit-v0.1-informational)

**What:** Drafts a FAIR, SPD-41a-compliant Data Governance and Storage Plan with data inventory and 15-row checklist.
**When to use:** for a data management plan, Open Science or SPD-41a compliance, DAAC archiving, metadata standards, file naming, licensing, or data release timelines.
**Owner:** @MayerT1
**Source:** [https://science.data.nasa.gov/earth-science-solution-co-development-toolkit/data-governance/](https://science.data.nasa.gov/earth-science-solution-co-development-toolkit/data-governance/)

Part of the **Solution Co-Development Toolkit** skill set (`sco-*`). Install `sco-toolkit-orchestrator` alongside any `sco-*` skill for routing and `/status`.

## Install
- **Claude Code:** copy this folder to `~/.claude/skills/sco-09-data-governance-storage/` (or a project's `.claude/skills/`).
- **Claude app:** `python scripts/package_skill.py Solution_Management/sco-09-data-governance-storage` → upload the zip.

## Inputs → Outputs
| In | Out |
|---|---|
| `report.md` | `report.md` |

Every run also emits Markdown tables with the NASA fillable template headers, a pasteable CSV, a `solution-profile.yaml` patch, and a Quality Gate checklist.

## Example
Prompt: "Write our data governance plan; inputs are Landsat and GPM, output is a COG flood map."
Result: Data inventory includes inputs and outputs with format and license; Checklist has all 15 rows with status.

## Chains with
- Upstream: `sco-08-technical-requirements`
- Downstream: `sco-10-implementation-monitoring-plan`, `sco-11-adoption-sustainability`, `reproducible-release`

## Changelog
- 0.1.0 — initial draft, converted from the AI-ready Solution Co-Development Toolkit guides.
