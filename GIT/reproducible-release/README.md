# Reproducible Research Release

![status](https://img.shields.io/badge/skill-draft-lightgrey) ![domain](https://img.shields.io/badge/domain-GIT-blue)

**What:** Cut a versioned, citable, reproducible release of a research repo.
**When to use:** "cut a release", "tag v1.3", "make this citable", "freeze the env for the paper", "package for the partner".
**Owner:** @MayerT1

## Install
- **Claude Code:** copy to `~/.claude/skills/reproducible-release/`.
- **Claude app:** `python scripts/package_skill.py GIT/reproducible-release` → upload the zip.

## Inputs → Outputs
| In | Out |
|---|---|
| `code.repo`, `metrics.json`?, `model.checkpoint`? | `release.notes`, `env.lock` |

## Chains with
- Upstream: `classification-accuracy-assessment`
- Downstream: `partner-status-brief`

## Changelog
- 0.1.0 — initial seed skill.
