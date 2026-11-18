# Cross-team Workflows

A **workflow** is a documented chain of skills, usually across teams, that
solves a recurring program problem end to end. Workflows are how skills
"connect": each step's output artifact is the next step's input.

## Workflow file format
Copy [`_template.md`](_template.md). Each workflow must:
1. Name the **problem** and the **trigger** (what starts it).
2. List steps as `skill-id` (team) → artifact handed off.
3. Name a **hand-off owner** per step (a person or role on that team).
4. Have every hand-off artifact type exist in `standards/ARTIFACT_TYPES.md`.
5. Record a **run log** entry each time it's used on real work (good evidence for a certification request).

## Workflows
| Workflow | Teams | Status |
|---|---|---|
| [`model-to-partner-delivery`](model-to-partner-delivery.md) | Science → GIT → Solution Management | draft |

## Ideas backlog (open an issue to claim one)
- `partner-request-to-pilot-map` — Sol Mgmt intake → Science mapping → Science accuracy → Sol Mgmt brief
- `new-dataset-to-academy-lesson` — GIT STAC/COG → Science notebook → Sol Mgmt training agenda
- `quarterly-reporting` — GIT repo activity + Science metrics → Sol Mgmt quarterly report
