# Solution Co-Development Toolkit — Orchestrator

![status](https://img.shields.io/badge/skill-draft-lightgrey) ![domain](https://img.shields.io/badge/domain-Solution__Management-purple) ![toolkit](https://img.shields.io/badge/SCO%20toolkit-v0.1-informational)

**What:** Routes Earth Action solution teams to the right Co-Development Toolkit skill and tracks progress in a shared solution profile.
**When to use:** where to start, which toolkit tool to use, /status, or /next.
**Owner:** @MayerT1
**Source:** [https://science.data.nasa.gov/earth-science-solution-co-development-toolkit/](https://science.data.nasa.gov/earth-science-solution-co-development-toolkit/)

Part of the **Solution Co-Development Toolkit** skill set (`sco-*`). Install `sco-toolkit-orchestrator` alongside any `sco-*` skill for routing and `/status`.

## Install
- **Claude Code:** copy this folder to `~/.claude/skills/sco-toolkit-orchestrator/` (or a project's `.claude/skills/`).
- **Claude app:** `python scripts/package_skill.py Solution_Management/sco-toolkit-orchestrator` → upload the zip.

## Inputs → Outputs
| In | Out |
|---|---|
| `partner.request` | `project.plan`, `issue.list` |

Every run also emits Markdown tables with the NASA fillable template headers, a pasteable CSV, a `solution-profile.yaml` patch, and a Quality Gate checklist.

## Example
Prompt: "Where do we start? We're building a soil-moisture drought advisory with a state ag agency."
Result: Asks at most 4 setup questions (title, phase, ARL, today's need); Recommends sco-01-designing-for-impact or sco-04-stakeholder-mapping with a one-sentence reason.

## Chains with
- Upstream: none (entry point)
- Downstream: `sco-00-trust-marker`, `sco-01-designing-for-impact`, `sco-02-capturing-communicating-impact`, `sco-03-economic-impact-assessment`, `sco-04-stakeholder-mapping`, `sco-05-needs-assessment`, `sco-06-information-chain-analysis`, `sco-07-user-centered-design`, `sco-08-technical-requirements`, `sco-09-data-governance-storage`, `sco-10-implementation-monitoring-plan`, `sco-11-adoption-sustainability`, `sco-12-meaningful-metrics`

## Changelog
- 0.1.0 — initial draft, converted from the AI-ready Solution Co-Development Toolkit guides.
