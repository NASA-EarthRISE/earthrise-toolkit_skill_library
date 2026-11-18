---
name: sco-12-meaningful-metrics
description: "Develop SMART input/output/outcome/impact metrics tied to the results framework and fill the Fillable Indicator Template (indicator, type, baseline, target, source, frequency, unit, POC, method, rationale, yearly values). Use in Phase 2 when building the SIIMP; track in Phases 3–4. Use when someone asks for indicators, KPIs, metrics, an indicator matrix, SMART metrics, baselines and targets, or to fill the NASA Fillable Indicator Template."
---

# Tool 12 — Meaningful Metrics Development (Agent Guide)

Read `references/conventions.md` first (shared rules: provenance tags, output format, commands, tool-number → skill-id map). State schema: `references/solution-profile.template.yaml`.

## Purpose
A **metric** is a specific, measurable variable giving systematic evidence about solution progress, performance, effectiveness, and impact, embedded in the results framework. Use metrics to track progress, validate results-framework steps, support management, and demonstrate value. **"Don't count only for the sake of counting."**


## Inputs
- `project.plan` — Results framework and expected outcomes.
- `metrics.json` — Optional actuals for yearly columns.
- Optional: `solution-profile.yaml` from any earlier toolkit skill (reused, never re-asked).

## Outputs
- `project.plan` — Fillable Indicator Template rows grouped by expected outcome with CSV and SMART audit, plus a YAML patch to `solution-profile.yaml` (schema in `references/solution-profile.template.yaml`).
- Exact table layouts: see **Output Spec** below.


## Four tiers

| Level | Name | Purpose | Examples |
|---|---|---|---|
| 1 | Input | Track implementation/delivery steps | Trainings conducted; participants; needs identified; code developed; stakeholders consulted; partnerships developed |
| 2 | Output | Deliverables from inputs | Solutions developed; users trained and able to adopt/sustain; institutions adopting; publications; information products |
| 3 | Outcome | Immediate results; behavior/capacity/condition change; tests assumptions | Solutions adopted; uptake confirmed; greater access to timely trusted data; applications used in decisions |
| 4 | Impact | Longer-term breadth/depth; often via EIA; may exceed team capacity | Improved resilience via early action; # people evacuated before floods; crop savings from pre-flood harvest |

## Steps
1. **Pull the results framework** (`impact.results_framework`). If missing, run a 5-minute version of `01` Step 4.
2. **Size the suite.** Ask/assess: solution complexity · level of effort/inputs · number/types of outputs & outcomes · required reporting & collection methods. Recommend a count (typical: 2–4 per outcome, 1–2 per impact, inputs/outputs only as reporting requires).
3. **Draft indicators per tier**, linked to Expected Outcome #1…#n. Pull candidates from `07` Step 4 metrics and `01` candidates.
4. **SMART check** each: Specific · Measurable (data exists, capacity to collect) · Achievable · Relevant · Time-bound. Rewrite failures; show before → after.
5. **Fill operational columns**: baseline (+ timeframe), target, data source, frequency, unit, POC, collection method, rationale. **Never invent baselines** — if unknown, set `TBD — collect by <date> via <method>` and log an open item (often → `03 EIA` baseline data).
6. **Suite checklist** (print results):
   - Does it measure what funding reporting requires?
   - Is it insightful, not just easy to measure?
   - Is the insight worth the time spent?
   - Does it balance breadth and depth?
   - Is the information source accessible at reasonable effort?

## Output Spec — Fillable Indicator Template (exact)

Header block: `FILLABLE INDICATOR TEMPLATE` · Solution Title · Company Name · Solution Manager · Date

Columns (exact order, 15):

| INDICATOR | INDICATOR TYPE | BASELINE | TARGET | DATA SOURCE | COLLECTION AND REPORTING FREQUENCY | UNIT OF MEASURE (#, %, $) | POC / RESPONDIBLE INDIVIDUAL | INDICATOR DATA COLLECTION METHOD | RATIONALE | BASELINE TIMEFRAME | YEAR ONE | YEAR TWO | YEAR THREE | YEAR FOUR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

(`RESPONDIBLE` typo is preserved to match the source sheet for paste-compatibility.)

Row grouping (matches template):
```
Solution-Level Expected Outcome #1 (from Results Framework): <text>
  Indicator #1 (Outcome) ...
  Indicator #2 (Output) ...
  Indicator #3 (Input) ...
Solution-Level Expected Outcome #2 (from Results Framework): <text>
  ...
Impact Indicators (from Results Framework)
  ...
```
In CSV, add a leading `GROUP` column holding the outcome label so rows paste cleanly under each heading.

**SMART audit table**

| ID | Indicator | S | M | A | R | T | Fix |
|---|---|---|---|---|---|---|---|

**Profile patch:** `indicators[]`.

## Worked example (toolkit)
- **Training:** # individuals trained → % showing sustained skill use 3–6 months later; % self-reporting a new skill immediately after.
- **Capacity building:** % trainees completing pre/post surveys → # needs-assessment or lessons-learned docs; % increase in ability to apply geospatial tools for water-quality modeling (pre/post test).
- **Solution readiness:** # solutions achieving an ARL goal → # showing sustained decision use 1 yr after implementation → # leading to intended benefits 1 yr after (Impact).
- **Products:** # products (publications, training materials, tools) → # training materials used by end users via training-of-trainers; # co-developed products adopted for early warning alerts.
- **Template example rows (flood):** Outcome — share of local institutions with improved flood-risk management capacity, baseline 2/10, target 9/10, case studies/KIIs/post-training tests, annual · Outcome — # institutions reporting faster evacuation & resource mobilization, 0 → 8, feedback forms/after-action reviews · Outcome — # local officials using updated risk maps in decisions, 0 → 10, surveys/bulletin reviews, annual · Output — share of trained officials who can interpret warnings and use maps, pre/post tests · Input — # needs-assessment documents identifying partner needs · Input — # co-design sessions with disaster mgmt agencies, session reports.

## Quality Gate
- [ ] Every outcome in the results framework has ≥1 Outcome indicator.
- [ ] Impact indicators present (or justified as beyond scope → EIA).
- [ ] All indicators pass SMART or have a logged fix.
- [ ] Each has data source, frequency, POC, method.
- [ ] Baselines known or have a dated collection plan.
- [ ] Suite checklist printed.

## Guardrails
- Never invent baselines; set TBD with a dated collection plan.
- Keep the template's exact 15 column headers, including the RESPONDIBLE typo, for paste compatibility.
- Never invent people, organizations, quotes, budgets, or baselines; use `<<placeholders>>` and tag AI-drafted rows `[AI-DRAFT]`.
- AI drafts prepare for stakeholder engagement; never present them as stakeholder evidence.
- Never store or echo PII, CUI, or ITAR/EAR-controlled data; replace with placeholders and warn the user.
- Never send, post, or share outputs; produce them for the user to review.

## Example
**Prompt:** Build our indicator matrix from this results framework.
**Result:** Table has exactly the 15 template columns in order; Rows grouped under Solution-Level Expected Outcome headings; CSV block included.

## Hand-offs
- Upstream: `sco-01-designing-for-impact`, `sco-07-user-centered-design`, `sco-03-economic-impact-assessment`
- Downstream: `sco-10-implementation-monitoring-plan`, `sco-02-capturing-communicating-impact`

## Source
- Toolkit page: https://science.data.nasa.gov/earth-science-solution-co-development-toolkit/meaningful-metrics/
- Phase: 2 (used through 3–4)
- Template — Fillable Indicator Template (Google Sheets; tabs IndicatorTemplate, IndicatorTemplate w/Examples, Instructions and Helpful Hints): https://docs.google.com/spreadsheets/d/1VGShXy_S_h8P5l0_Lh2ltbeq2Z423EpB/edit?gid=427899109
- Template — Results framework slides: https://docs.google.com/presentation/d/1LY2tE5McwaIL48I5LAu-AV9ANFbLD0qh
- Derived from NASA Earth Action Solution Co-Development Toolkit v0.1 (DOI 10.5281/zenodo.19866469).

## References
- `references/conventions.md` — read first, every run.
- `references/solution-profile.template.yaml` — when creating or patching the shared profile.
