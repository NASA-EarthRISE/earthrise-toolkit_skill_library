# Adoption & Sustainability Plan

![status](https://img.shields.io/badge/skill-draft-lightgrey) ![domain](https://img.shields.io/badge/domain-Solution__Management-purple) ![toolkit](https://img.shields.io/badge/SCO%20toolkit-v0.1-informational)

**What:** Drafts the Solution Adoption and Sustainability Plan sections 1–8 with all template tables.
**When to use:** for an adoption plan, sustainability plan, handover or transition plan, long-term ownership, maintenance, training and onboarding plan, or exit/retirement plan.
**Owner:** @MayerT1
**Source:** [https://science.data.nasa.gov/earth-science-solution-co-development-toolkit/adoption-sustainability/](https://science.data.nasa.gov/earth-science-solution-co-development-toolkit/adoption-sustainability/)

Part of the **Solution Co-Development Toolkit** skill set (`sco-*`). Install `sco-toolkit-orchestrator` alongside any `sco-*` skill for routing and `/status`.

## Install
- **Claude Code:** copy this folder to `~/.claude/skills/sco-11-adoption-sustainability/` (or a project's `.claude/skills/`).
- **Claude app:** `python scripts/package_skill.py Solution_Management/sco-11-adoption-sustainability` → upload the zip.

## Inputs → Outputs
| In | Out |
|---|---|
| `project.plan`, `report.md`, `release.notes` | `project.plan` |

Every run also emits Markdown tables with the NASA fillable template headers, a pasteable CSV, a `solution-profile.yaml` patch, and a Quality Gate checklist.

## Example
Prompt: "Draft our adoption and sustainability plan for handing the flood tool to the district DRM."
Result: Includes sections 1–8 with exact template table rows; Adoption goals are time-bound.

## Chains with
- Upstream: `sco-04-stakeholder-mapping`, `sco-05-needs-assessment`, `sco-07-user-centered-design`, `sco-08-technical-requirements`, `sco-09-data-governance-storage`
- Downstream: `sco-10-implementation-monitoring-plan`, `sco-00-trust-marker`

## Changelog
- 0.1.0 — initial draft, converted from the AI-ready Solution Co-Development Toolkit guides.
