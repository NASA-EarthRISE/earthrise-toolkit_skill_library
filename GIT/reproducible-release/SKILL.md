---
name: reproducible-release
description: Prepare a versioned, citable, reproducible release of an EarthRISE research code repository, covering SemVer bump, CHANGELOG, pinned environment, CITATION.cff, model or metrics attachments, git tag and GitHub release notes. Use when someone asks to cut a release, tag a version, make a repo citable or Zenodo-ready, freeze the environment for a paper, or package results for a partner delivery.
---

# Reproducible Release

## Purpose
Turn a working research repo into a release that anyone on any team can rerun
and cite: same code, same environment, same results. Produces `release.notes`
that Solution Management can hand straight to partners.

## Inputs
- `code.repo` — local path or GitHub URL of the repository (must have a README).
- `metrics.json` — optional; results to attach (e.g. from `classification-accuracy-assessment`).
- `model.checkpoint` — optional; weights + `model_card.md` to attach.

## Outputs
- `release.notes` — `RELEASE_NOTES_vX.Y.Z.md`: version, date, changes, environment, results, DOI/tag link.
- `env.lock` — pinned `environment.yml` or `requirements.txt` committed at the tag.

## Steps
1. **Inspect the repo.** `git status` must be clean; list commits since the last tag (`git log $(git describe --tags --abbrev=0)..HEAD --oneline`, or all commits if no tag).
2. **Choose the version** with the user: MAJOR for breaking API/output changes, MINOR for features, PATCH for fixes. Show the proposed number and why.
3. **Freeze the environment.** Conda: `conda env export --no-builds > environment.yml`, then remove the `prefix:` line. Pip: `pip freeze > requirements.txt` in a clean venv. Never include local paths.
4. **Update `CHANGELOG.md`** (Keep a Changelog format) from the commit list, grouped Added / Changed / Fixed.
5. **Create or update `CITATION.cff`** using `references/CITATION.cff.template`; set `version` and `date-released`.
6. **Attach results.** If `metrics.json` or a checkpoint was provided, put it under `release_assets/` (or plan to upload as release assets if > 50 MB; never commit large weights to git).
7. **Write `RELEASE_NOTES_vX.Y.Z.md`** from `references/release_notes_template.md`.
8. **Show the user the exact commands and wait for confirmation** before tagging or pushing:
   ```bash
   git add CHANGELOG.md CITATION.cff environment.yml RELEASE_NOTES_vX.Y.Z.md
   git commit -m "Release vX.Y.Z"
   git tag -a vX.Y.Z -m "vX.Y.Z"
   git push upstream main --tags
   gh release create vX.Y.Z --notes-file RELEASE_NOTES_vX.Y.Z.md release_assets/*
   ```
9. **Hand off** `RELEASE_NOTES_vX.Y.Z.md` to `partner-status-brief`.

## Guardrails
- Never push, tag, or create a release without explicit user confirmation.
- Never commit credentials, `.env`, service-account JSON, or partner-restricted data; check `git diff --cached --name-only` before committing.
- Never rewrite published tags or force-push `main`.
- Do not invent metrics for release notes; copy them from `metrics.json` only.

## Example
**Input:** repo with 14 commits since v1.2.0 incl. a new `--tile-size` flag; `metrics.json` with OA 0.947 ± 0.018.
**Output:** v1.3.0, updated CHANGELOG/CITATION.cff, pinned `environment.yml`, `RELEASE_NOTES_v1.3.0.md` with the accuracy table, and the command block for review.

## Hand-offs
- Upstream: `classification-accuracy-assessment` (`metrics.json`).
- Downstream: `partner-status-brief` (`release.notes`).

## References
- `references/release_notes_template.md` — step 7.
- `references/CITATION.cff.template` — step 5.
