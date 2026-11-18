# Designing for Impact

![status](https://img.shields.io/badge/skill-draft-lightgrey) ![domain](https://img.shields.io/badge/domain-Solution__Management-purple) ![toolkit](https://img.shields.io/badge/SCO%20toolkit-v0.1-informational)

**What:** Builds the if/then pathway, results framework (inputs→outputs→outcomes→impact), and assumption record.
**When to use:** for a results framework, logic model, theory of change, if/then pathway, problem statement, or assumptions log for an Earth observation solution.
**Owner:** @MayerT1
**Source:** [https://science.data.nasa.gov/earth-science-solution-co-development-toolkit/designing-for-impact/](https://science.data.nasa.gov/earth-science-solution-co-development-toolkit/designing-for-impact/)

Part of the **Solution Co-Development Toolkit** skill set (`sco-*`). Install `sco-toolkit-orchestrator` alongside any `sco-*` skill for routing and `/status`.

## Install
- **Claude Code:** copy this folder to `~/.claude/skills/sco-01-designing-for-impact/` (or a project's `.claude/skills/`).
- **Claude app:** `python scripts/package_skill.py Solution_Management/sco-01-designing-for-impact` → upload the zip.

## Inputs → Outputs
| In | Out |
|---|---|
| `partner.request` | `project.plan` |

Every run also emits Markdown tables with the NASA fillable template headers, a pasteable CSV, a `solution-profile.yaml` patch, and a Quality Gate checklist.

## Example
Prompt: "Build a results framework for our NASA soil-moisture drought tool for state ag extension."
Result: Produces Impact / Outcome long / Outcome short / Output / Input table; Every outcome is a behavior or decision change by a user type; Assumption record has monitor and action-if-fails per link.

## Chains with
- Upstream: `sco-05-needs-assessment`, `sco-04-stakeholder-mapping`
- Downstream: `sco-10-implementation-monitoring-plan`, `sco-12-meaningful-metrics`, `sco-06-information-chain-analysis`, `sco-07-user-centered-design`

## Changelog
- 0.1.0 — initial draft, converted from the AI-ready Solution Co-Development Toolkit guides.
