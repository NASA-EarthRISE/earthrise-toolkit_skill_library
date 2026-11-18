# Partner Status Brief

![status](https://img.shields.io/badge/skill-draft-lightgrey) ![domain](https://img.shields.io/badge/domain-Solution__Management-purple)

**What:** One-page partner/leadership status brief built from technical artifacts.
**When to use:** "partner update", "status brief", "one-pager for leadership", "explain these results to the partner".
**Owner:** @MayerT1

## Install
- **Claude Code:** copy to `~/.claude/skills/partner-status-brief/`.
- **Claude app:** `python scripts/package_skill.py Solution_Management/partner-status-brief` → upload the zip.

## Inputs → Outputs
| In | Out |
|---|---|
| `metrics.json`, `release.notes`, `report.md`, `project.plan`, `partner.request` | `stakeholder.brief` |

## Chains with
- Upstream: `classification-accuracy-assessment`, `reproducible-release`

## Changelog
- 0.1.0 — initial seed skill.
