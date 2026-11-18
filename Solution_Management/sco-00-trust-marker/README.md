# TRUST Marker for Co-development

![status](https://img.shields.io/badge/skill-draft-lightgrey) ![domain](https://img.shields.io/badge/domain-Solution__Management-purple) ![toolkit](https://img.shields.io/badge/SCO%20toolkit-v0.1-informational)

**What:** Scores co-development depth on five TRUST dimensions (0–4) with evidence, targets, and gap-closing actions.
**When to use:** how co-developed their solution is, for a TRUST score or self-assessment, a co-development baseline, or reflection at a phase gate.
**Owner:** @MayerT1
**Source:** [https://science.data.nasa.gov/earth-science-solution-co-development-toolkit/trust-marker/](https://science.data.nasa.gov/earth-science-solution-co-development-toolkit/trust-marker/)

Part of the **Solution Co-Development Toolkit** skill set (`sco-*`). Install `sco-toolkit-orchestrator` alongside any `sco-*` skill for routing and `/status`.

## Install
- **Claude Code:** copy this folder to `~/.claude/skills/sco-00-trust-marker/` (or a project's `.claude/skills/`).
- **Claude app:** `python scripts/package_skill.py Solution_Management/sco-00-trust-marker` → upload the zip.

## Inputs → Outputs
| In | Out |
|---|---|
| `project.plan`, `report.md` | `report.md` |

Every run also emits Markdown tables with the NASA fillable template headers, a pasteable CSV, a `solution-profile.yaml` patch, and a Quality Gate checklist.

## Example
Prompt: "Score our TRUST Marker. We've held two stakeholder interviews and nothing else."
Result: Trust-building scored 1 with interview evidence; Every gap has an action and a named sco- skill.

## Chains with
- Upstream: none (entry point)
- Downstream: `sco-toolkit-orchestrator`

## Changelog
- 0.1.0 — initial draft, converted from the AI-ready Solution Co-Development Toolkit guides.
