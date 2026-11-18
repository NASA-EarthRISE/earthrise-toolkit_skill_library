# Needs Assessment

![status](https://img.shields.io/badge/skill-draft-lightgrey) ![domain](https://img.shields.io/badge/domain-Solution__Management-purple) ![toolkit](https://img.shields.io/badge/SCO%20toolkit-v0.1-informational)

**What:** Captures, codes, themes, and prioritizes user needs per user group and translates them into draft EO requirements.
**When to use:** to assess user needs, write a needs-assessment interview guide, code interview notes into themes, prioritize needs, or derive EO requirements from users.
**Owner:** @MayerT1
**Source:** [https://science.data.nasa.gov/earth-science-solution-co-development-toolkit/needs-assessment/](https://science.data.nasa.gov/earth-science-solution-co-development-toolkit/needs-assessment/)

Part of the **Solution Co-Development Toolkit** skill set (`sco-*`). Install `sco-toolkit-orchestrator` alongside any `sco-*` skill for routing and `/status`.

## Install
- **Claude Code:** copy this folder to `~/.claude/skills/sco-05-needs-assessment/` (or a project's `.claude/skills/`).
- **Claude app:** `python scripts/package_skill.py Solution_Management/sco-05-needs-assessment` → upload the zip.

## Inputs → Outputs
| In | Out |
|---|---|
| `report.md`, `partner.request` | `partner.request`, `report.md` |

Every run also emits Markdown tables with the NASA fillable template headers, a pasteable CSV, a `solution-profile.yaml` patch, and a Quality Gate checklist.

## Example
Prompt: "Here are notes from 4 interviews with district water managers. Code and prioritize the needs."
Result: Produces codes, 3–7 themes, need statements mapped to decisions; Each need has Value, Feasibility, and Do now / Do next / Nice to have / Avoid.

## Chains with
- Upstream: `sco-04-stakeholder-mapping`
- Downstream: `sco-01-designing-for-impact`, `sco-06-information-chain-analysis`, `sco-07-user-centered-design`, `sco-08-technical-requirements`, `sco-03-economic-impact-assessment`

## Changelog
- 0.1.0 — initial draft, converted from the AI-ready Solution Co-Development Toolkit guides.
