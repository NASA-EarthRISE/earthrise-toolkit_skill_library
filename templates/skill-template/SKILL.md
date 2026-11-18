---
name: your-skill-name
description: One or two sentences on WHAT this skill does, then WHEN to use it with the phrases people actually say (e.g. "Use when someone asks for X, Y, or Z"). Max 1024 characters, no angle brackets.
---

# Your Skill Title

## Purpose
One paragraph: the job this skill does, for whom, and the program standard it encodes.

## Inputs
- `artifact.type` — what it is and where it comes from (must match `skill.yaml`)

## Outputs
- `artifact.type` — file name / location and shape (see `standards/ARTIFACT_TYPES.md`)

## Steps
1. Confirm the inputs exist and are in the expected format. If not, ask for exactly what is missing.
2. Run `scripts/<helper>.py --in <input> --out <output>` for the deterministic part.
3. …
4. Write outputs to the declared paths and summarize results in 3–5 lines.

## Guardrails
- Never invent numbers, citations, or results that were not produced by a step above.
- Never write credentials, tokens, or partner-restricted data into outputs or commits.
- If the request is outside this skill's scope, say so and name the skill that fits (by id).

## Example
**Input:** …
**Output:** …

## Hand-offs
- Upstream: `skill-id` produces my input `artifact.type`.
- Downstream: pass `artifact.type` to `skill-id`.

## References
- `references/details.md` — read only when <condition>.
