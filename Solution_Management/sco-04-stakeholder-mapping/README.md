# Stakeholder Mapping & Analysis

![status](https://img.shields.io/badge/skill-draft-lightgrey) ![domain](https://img.shields.io/badge/domain-Solution__Management-purple) ![toolkit](https://img.shields.io/badge/SCO%20toolkit-v0.1-informational)

**What:** Identifies, categorizes, and scores stakeholders (influence/interest 1–4) and assigns Collaborate/Align/Validate/Monitor strategies.
**When to use:** who to involve, for a stakeholder map, influence-interest matrix, partner prioritization, or engagement strategy for an Earth observation solution.
**Owner:** @MayerT1
**Source:** [https://science.data.nasa.gov/earth-science-solution-co-development-toolkit/stakeholder-mapping/](https://science.data.nasa.gov/earth-science-solution-co-development-toolkit/stakeholder-mapping/)

Part of the **Solution Co-Development Toolkit** skill set (`sco-*`). Install `sco-toolkit-orchestrator` alongside any `sco-*` skill for routing and `/status`.

## Install
- **Claude Code:** copy this folder to `~/.claude/skills/sco-04-stakeholder-mapping/` (or a project's `.claude/skills/`).
- **Claude app:** `python scripts/package_skill.py Solution_Management/sco-04-stakeholder-mapping` → upload the zip.

## Inputs → Outputs
| In | Out |
|---|---|
| `partner.request` | `report.md` |

Every run also emits Markdown tables with the NASA fillable template headers, a pasteable CSV, a `solution-profile.yaml` patch, and a Quality Gate checklist.

## Example
Prompt: "Map stakeholders for a flood early warning service: national met office, district DRM, local NGOs, World Bank."
Result: Every row has category, readiness, influence, interest, strategy; Includes influence-interest matrix with Collaborate/Align/Validate/Monitor.

## Chains with
- Upstream: `sco-01-designing-for-impact`
- Downstream: `sco-05-needs-assessment`, `sco-06-information-chain-analysis`, `sco-10-implementation-monitoring-plan`, `sco-11-adoption-sustainability`

## Changelog
- 0.1.0 — initial draft, converted from the AI-ready Solution Co-Development Toolkit guides.
