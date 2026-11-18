# EarthRISE Skill Standard (v1.0)

This is the design contract every skill in the library must meet. The validator
(`scripts/validate_skill.py`) enforces the **MUST** rules automatically; reviewers
enforce the **SHOULD** rules using the rubric in [`VERIFICATION.md`](VERIFICATION.md).

---

## 1. What a skill is

A **skill** is a folder of instructions, plus optional scripts and reference
files, that teaches Claude how to do one repeatable job the way our program does
it. Claude loads the `SKILL.md` only when the task matches the skill's
`description`, so a good skill is **narrow, triggerable, and self-contained**.

| A skill IS | A skill is NOT |
|---|---|
| One job, done our way (e.g. "run an area-adjusted accuracy assessment") | A whole project or a grab-bag of tips |
| Reusable across projects and partners | A one-off prompt for a single task |
| Declares what it consumes and produces | A black box other skills can't chain to |
| Owned and reviewed on a schedule | Uploaded once and forgotten |

## 2. Required folder layout

```
<Domain>/<skill-name>/
├── SKILL.md            # MUST  — instructions Claude reads (frontmatter + body)
├── skill.yaml          # MUST  — library manifest: owner, version, badge, I/O contract
├── README.md           # MUST  — human-facing: what, when, example, changelog
├── evals/
│   └── evals.json      # MUST for badge ≥ Peer-Reviewed — test prompts + expectations
├── scripts/            # OPTIONAL — deterministic helpers (python/R/js) the skill calls
├── references/         # OPTIONAL — long docs Claude reads on demand (keep SKILL.md lean)
└── assets/             # OPTIONAL — templates, logos, sample data (small, no secrets)
```

- `<Domain>` MUST be one of `GIT`, `Science`, `Solution_Management`.
- `<skill-name>` MUST be kebab-case, ≤ 64 chars, and MUST NOT contain `claude` or `anthropic`.
- Folder name MUST equal `SKILL.md` `name` and `skill.yaml` `id`.

## 3. `SKILL.md` rules

```markdown
---
name: classification-accuracy-assessment
description: Run an area-adjusted accuracy assessment (Olofsson et al. 2014) for a land-cover or change map from reference samples. Use when someone asks for map accuracy, confusion matrix, area estimates with confidence intervals, or validation of a classification.
---
```

| Rule | Level |
|---|---|
| Frontmatter has exactly `name` and `description` (portable across Claude surfaces) | MUST |
| `description` ≤ 1024 chars, no `<` or `>`, says **what it does AND when to use it** (trigger phrases) | MUST |
| Body ≤ 500 lines; move long material into `references/` and link it | MUST |
| Opens with a one-paragraph **Purpose** and an **Inputs / Outputs** section matching `skill.yaml` | MUST |
| Steps are numbered, imperative, and executable ("Run `scripts/x.py --in …`"), not essays | SHOULD |
| States **Guardrails**: what the skill must never do (e.g. never commit credentials, never fabricate accuracy numbers) | MUST |
| Includes at least one worked **Example** (input → output) | SHOULD |
| Deterministic work (math, file conversion, validation) lives in `scripts/`, not in prose | SHOULD |
| No secrets, tokens, internal hostnames, PII, or partner-restricted data anywhere in the folder | MUST |
| References other skills by `id` (e.g. "hand off to `partner-status-brief`"), never by copying their content | SHOULD |

## 4. `skill.yaml` manifest

The manifest is what makes skills **discoverable, verifiable, and chainable**.
See the annotated version in [`templates/skill-template/skill.yaml`](../templates/skill-template/skill.yaml).

| Field | Required | Notes |
|---|---|---|
| `id` | ✅ | = folder name |
| `title` | ✅ | Human title |
| `domain` | ✅ | `GIT` \| `Science` \| `Solution_Management` (= parent folder) |
| `version` | ✅ | SemVer. Bump MAJOR when the I/O contract changes |
| `owner` | ✅ | GitHub handle accountable for the skill |
| `maintainers` | ✅ | ≥ 1 handle; ≥ 2 for Verified and above |
| `status` | ✅ | Badge level — see `VERIFICATION.md` |
| `summary` | ✅ | One line for the catalog |
| `tags` | ✅ | Free-form search tags |
| `inputs` / `outputs` | ✅ | List of `{type, description}`; `type` MUST come from [`ARTIFACT_TYPES.md`](ARTIFACT_TYPES.md) |
| `composes_with` | ⬜ | `upstream` / `downstream` skill ids this skill is designed to chain with |
| `requires` | ⬜ | Runtimes/packages/connectors (e.g. `python>=3.10`, `earthengine-api`, `GitHub connector`) |
| `data_sensitivity` | ✅ | `public` \| `internal` \| `partner-restricted` |
| `verification` | ✅ | Reviewers, dates, rubric score, eval pass rate, `review_due` |

## 5. The I/O contract (how skills connect)

Every skill declares typed **inputs** and **outputs** from one shared vocabulary
([`ARTIFACT_TYPES.md`](ARTIFACT_TYPES.md)). If skill A outputs `metrics.json` and
skill B inputs `metrics.json`, they chain — even when A is a Science skill and B
is a Solution Management skill. This is the backbone of cross-team workflows
([`workflows/`](../workflows/)).

Rules:
1. Use an existing artifact type before inventing one. New types are added by PR to `ARTIFACT_TYPES.md` with one reviewer from **each** domain.
2. A skill MUST write its outputs in the declared format (schema/file layout in `ARTIFACT_TYPES.md`).
3. Changing an output's shape is a **breaking change** → MAJOR version bump + notify `composes_with.downstream` owners in the PR.

## 6. Versioning & changelog

- SemVer in `skill.yaml`. PATCH = wording/typo; MINOR = new capability, compatible; MAJOR = I/O contract change.
- Every change adds a line to the `## Changelog` in the skill's `README.md`.
- A MAJOR bump drops the badge one level until re-reviewed (see `VERIFICATION.md §5`).

## 7. Naming conventions

| Thing | Convention | Example |
|---|---|---|
| Skill id | `verb-object` or `object-action`, kebab-case | `reproducible-release`, `partner-status-brief` |
| Workflow | `<trigger>-to-<outcome>` | `model-to-partner-delivery` |
| Scripts | snake_case, CLI with `--help` | `scripts/accuracy_assessment.py` |
