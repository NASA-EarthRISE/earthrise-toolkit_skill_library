# Verification & Badging Process (v1.0)

Every skill carries a **status badge** that tells a user, at a glance, how much
they can trust it. Badges are earned through automated checks + human review and
**expire** if a skill isn't re-reviewed on schedule.

## 1. Badge levels

| Badge | `status` value | Meaning | Who can use it |
|---|---|---|---|
| ![Draft](https://img.shields.io/badge/skill-draft-lightgrey) | `draft` | Passes the validator. Not reviewed. | Author + early testers |
| ![Peer-Reviewed](https://img.shields.io/badge/skill-peer--reviewed-blue) | `peer-reviewed` | One in-domain reviewer scored ≥ 70 on the rubric; evals exist and pass ≥ 80% | Own team |
| ![Verified](https://img.shields.io/badge/skill-verified-brightgreen) | `verified` | + one **cross-domain** reviewer; rubric ≥ 85; evals pass ≥ 90% on **two different Claude accounts**; ≥ 2 maintainers | Whole program |
| ![Certified](https://img.shields.io/badge/skill-program--certified-gold) | `certified` | + used in ≥ 1 published cross-team workflow on real work; signed off by the Skill Council | Program + partners |
| ![Stale](https://img.shields.io/badge/skill-stale-orange) | *(computed)* | `review_due` date has passed. Treated as one level lower until re-reviewed | — |
| ![Deprecated](https://img.shields.io/badge/skill-deprecated-red) | `deprecated` | Superseded or unsafe. Kept for history; points to replacement | Nobody (read-only) |

`stale` is computed by `scripts/build_registry.py`; nobody sets it by hand.

## 2. The pipeline

```
 author PR ──► [1 Automated gate] ──► [2 Domain review] ──► [3 Cross-domain review] ──► [4 Council sign-off]
                 validator + CI          → peer-reviewed        → verified                  → certified
```

### Gate 1 — Automated (every PR, required to merge)
`validate-skills.yml` runs:
- `scripts/validate_skill.py` — layout, frontmatter, manifest schema, I/O types, badge prerequisites, secret scan
- `scripts/build_registry.py --check` — catalog regenerated and committed

### Gate 2 — Domain review → `peer-reviewed`
- Reviewer from the skill's own team (enforced by `CODEOWNERS`).
- Runs the evals in a fresh Claude session with the skill installed; records the pass rate.
- Scores the rubric (§3). Needs **≥ 70 / 100** and no zero in a critical row.

### Gate 3 — Cross-domain review → `verified`
- Reviewer from a **different** team runs the evals on their own Claude account (proves portability) and reviews the I/O contract and README for clarity to an outsider.
- Needs rubric **≥ 85**, eval pass **≥ 90%** on both accounts, **≥ 2 maintainers**.

### Gate 4 — Skill Council → `certified`
- The Skill Council (one rep per team + the Geo-AI Working Group lead) meets monthly.
- Requires: the skill is a step in a merged `workflows/*.md` that has been run on real project work, with a short evidence note (link to the outcome, issue or report).

## 3. Review rubric (100 points)

| # | Dimension | Pts | Critical? | What "full marks" looks like |
|---|---|---|---|---|
| 1 | **Trigger clarity** | 15 | ✅ | `description` states what + when; Claude loads it for the eval prompts and NOT for the negative prompts |
| 2 | **Instruction quality** | 20 | ✅ | Numbered, executable steps; no ambiguity; long material in `references/` |
| 3 | **Correctness & evals** | 20 | ✅ | ≥ 3 positive + ≥ 1 negative eval; expectations are checkable; pass-rate meets the level |
| 4 | **Guardrails & data handling** | 15 | ✅ | Clear "never do" list; `data_sensitivity` is accurate; no secrets/PII |
| 5 | **Composability (I/O contract)** | 15 | | Inputs/outputs typed from `ARTIFACT_TYPES.md`; outputs written in the declared shape; `composes_with` filled |
| 6 | **Documentation** | 10 | | README has purpose, install, example, changelog; an outsider can use it in 5 min |
| 7 | **Maintainability** | 5 | | Scripts have `--help`, pinned deps in `requires`, owner + maintainers active |

A **0 in any critical row blocks the badge**, regardless of total.

Reviewers paste the scored rubric into the PR using the review checklist in
`.github/pull_request_template.md` and record the result in `skill.yaml`:

```yaml
verification:
  reviewers:
    - {handle: "@sci-reviewer", domain: Science, date: 2026-11-18, rubric: 88, eval_pass: 1.0, account: "science-team"}
    - {handle: "@git-reviewer", domain: GIT, date: 2026-11-20, rubric: 86, eval_pass: 0.92, account: "git-team"}
  last_reviewed: 2026-11-20
  review_due: 2027-05-20
```

## 4. Evals format (`evals/evals.json`)

```json
{
  "skill": "classification-accuracy-assessment",
  "evals": [
    {
      "id": "pos-01",
      "type": "positive",
      "prompt": "Here are my reference samples and map strata areas. Give me area-adjusted accuracy with 95% CIs.",
      "files": ["evals/files/samples.csv"],
      "expectations": [
        "Uses scripts/accuracy_assessment.py rather than computing by hand",
        "Reports overall, user's and producer's accuracy with 95% CI",
        "Writes metrics.json matching the ARTIFACT_TYPES schema"
      ]
    },
    {
      "id": "neg-01",
      "type": "negative",
      "prompt": "Write a press release about our new land cover map.",
      "expectations": ["Skill is NOT triggered"]
    }
  ]
}
```

- **positive** evals: the skill should trigger and every expectation must hold.
- **negative** evals: prompts that sound close but belong to another skill; the skill must not trigger.
- Pass rate = expectations met ÷ expectations total, across all evals.

## 5. Keeping badges honest (maintenance)

| Event | Effect |
|---|---|
| `review_due` passes (6 months for Verified/Certified, 12 for Peer-Reviewed) | Shown as **stale**; treated one level lower |
| MAJOR version bump | Drops one level until the relevant gate is re-run |
| Owner leaves / no maintainer activity for 6 months | Council reassigns or deprecates |
| Eval failure reported by a user (issue labeled `skill-regression`) | Owner has 30 days to fix or the badge drops one level |
| Security / data-handling issue | Immediately `deprecated` until fixed |

## 6. Roles

| Role | Who | Responsibility |
|---|---|---|
| Author / Owner | Anyone | Builds the skill, answers reviews, keeps it current |
| Maintainer | ≥ 1 besides owner (for Verified+) | Backup owner; reviews issues |
| Domain reviewer | Team CODEOWNERS | Gate 2 |
| Cross-domain reviewer | Any other team's CODEOWNER | Gate 3 |
| Skill Council | GIT rep, Science rep, Solution Management rep, Geo-AI WG lead | Gate 4, artifact-type vocabulary, disputes, deprecations |
