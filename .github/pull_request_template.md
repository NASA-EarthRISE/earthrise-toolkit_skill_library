## Skill PR

**Skill(s):** `Domain/skill-id`
**Type:** ☐ New skill ☐ Update (PATCH / MINOR / MAJOR) ☐ Badge promotion → `status:` ______ ☐ Workflow ☐ Standards
**Downstream skills affected (MAJOR only):** @owners notified ☐

### Author checklist
- [ ] `python scripts/validate_skill.py <path>` passes locally
- [ ] `python scripts/build_registry.py` run and `registry/` committed
- [ ] Inputs/outputs use types from `standards/ARTIFACT_TYPES.md`
- [ ] `README.md` changelog updated and `version` bumped
- [ ] No secrets, PII or partner-restricted data
- [ ] Evals added/updated (`evals/evals.json`, ≥ 3 positive + ≥ 1 negative)

---

### Reviewer rubric (copy one block per reviewer)

**Reviewer:** @handle · **Team:** GIT / Science / Solution_Management · **Claude account used:** ______
**Evals run:** __ / __ expectations met → pass rate ____

| # | Dimension | Max | Score | Notes |
|---|---|---|---|---|
| 1 | Trigger clarity ⚠️ | 15 | | |
| 2 | Instruction quality ⚠️ | 20 | | |
| 3 | Correctness & evals ⚠️ | 20 | | |
| 4 | Guardrails & data handling ⚠️ | 15 | | |
| 5 | Composability (I/O contract) | 15 | | |
| 6 | Documentation | 10 | | |
| 7 | Maintainability | 5 | | |
| | **Total** | 100 | | |

⚠️ = critical; a 0 blocks the badge. Thresholds: peer-reviewed ≥ 70 · verified ≥ 85 (cross-team). See `standards/VERIFICATION.md`.
