# Contributing a Skill

Five steps from idea to badge. Plan ~1–2 hours for a first draft.

## 1. Claim it
Open a **Skill proposal** issue (domain, id, one job, inputs → outputs, owner).
Check [`registry/CATALOG.md`](registry/CATALOG.md) first so you don't duplicate an existing skill — extend it instead.

## 2. Scaffold it
```bash
git clone https://github.com/NASA-EarthRISE/earthrise-toolkit_skill_library.git
cd earthrise-toolkit_skill_library
pip install -r scripts/requirements.txt
git checkout -b skill/<skill-id>
python scripts/new_skill.py Science <skill-id> --owner @you
```
Windows (Command Prompt) works the same; use `python` from your conda env.

## 3. Write it
- **`SKILL.md`** — follow [`standards/SKILL_STANDARD.md`](standards/SKILL_STANDARD.md). The `description` decides when Claude uses it: say **what + when**.
- **`skill.yaml`** — owner, version, I/O types from [`standards/ARTIFACT_TYPES.md`](standards/ARTIFACT_TYPES.md), `composes_with`.
- **`evals/evals.json`** — ≥ 3 positive prompts, ≥ 1 near-miss negative.
- Put math, conversions and validation in `scripts/` (deterministic beats prose).

> **Tip:** you can build the first draft with Claude itself: ask it to use the skill-creator skill with this repo's template and standard, then edit.

## 4. Test it
```bash
python scripts/validate_skill.py Science/<skill-id>
python scripts/package_skill.py Science/<skill-id>      # -> dist/<skill-id>.zip
```
Install the zip in your own Claude account (or copy the folder to `~/.claude/skills/` for Claude Code), run each eval prompt in a **fresh** conversation, and note what passed.

## 5. Open a PR
```bash
python scripts/build_registry.py
git add . && git commit -m "Add <skill-id> skill"
git push origin skill/<skill-id>
```
Fill in the PR template. CI runs Gate 1. Your team's CODEOWNERS are auto-requested for Gate 2.

## Getting a higher badge
| Want | Do |
|---|---|
| `peer-reviewed` | Ask a teammate to run your evals and score the rubric in the PR |
| `verified` | Ask a reviewer from **another team** to do the same on **their** Claude account; add a 2nd maintainer |
| `certified` | Use the skill in a `workflows/*.md` on real work, log the run, request Council review |

The reviewer records the result in your `skill.yaml` `verification:` block; the validator checks it meets the bar.

## Updating someone else's skill
Open a PR; the owner + domain CODEOWNERS review. MAJOR changes (I/O contract) must notify `composes_with.downstream` owners.

## Questions
Open a discussion or ping the Skill Council in the program channel.
