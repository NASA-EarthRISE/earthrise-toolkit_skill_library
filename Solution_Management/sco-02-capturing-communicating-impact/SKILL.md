---
name: sco-02-capturing-communicating-impact
description: "Plan who needs to hear about an EO solution's impact and draft the right product — internal NASA highlight, use case, case study, EIA summary, activity/assessment report, NASA blog, or press release — balancing breadth and depth of impact evidence. Use in early planning and again in Phase 4. Use when someone asks for a use case, case study, impact story, NASA blog post, press release, internal HQ highlight, communications plan, or how to show impact to an audience."
---

# Tool 2 — Capturing & Communicating Impact (Agent Guide)

Read `references/conventions.md` first (shared rules: provenance tags, output format, commands, tool-number → skill-id map). State schema: `references/solution-profile.template.yaml`.

## Purpose
Anticipate potential impact and plan how, where, and to whom outcomes will be communicated: **audience · how to show impact · format**.


## Inputs
- `project.plan` — Results framework, indicators, and comms plan.
- `metrics.json` — Indicator actuals or EIA values as evidence.
- `report.md` — Activity or assessment reports.
- Optional: `solution-profile.yaml` from any earlier toolkit skill (reused, never re-asked).

## Outputs
- `stakeholder.brief` — Product draft at the toolkit's required length with evidence ledger.
- `report.md` — Communications plan table.
- Exact table layouts: see **Output Spec** below.


## Two modes
- **Plan mode** (early / SIIMP §13–14): build a Communications Plan — what evidence to start collecting now.
- **Draft mode** (Phase 3–4): produce a specific product from the evidence in the profile.

## Guiding questions (ask throughout)
- Who **needs** to know about this? Why?
- Who **wants** to know about this?
- Who can **advocate** as spokesperson or champion?

## Audiences

| Audience | Messaging Considerations |
|---|---|
| Scientists & experts / potential data users (GIS specialists, forecasters, ag extension, emergency responders) | How it affects their work |
| Decision-makers (mayors, legislators, civil servants, tribal leaders, private-sector execs) | Social, economic, environmental impacts explained |
| Other scientists (journals, conference panels, NASA R&A) | Innovation leads; real-world impact still matters |
| "Science curious" public (blog readers, event attendees, students) | Impact stories engage non-experts and extend reach |
| NASA leadership & USG (HQ, program leads, MAL/PALs, comms) | Emphasize economic benefits for budget justification |

## How to show impact
- Start articulating intended impacts at the beginning of co-design.
- **Breadth** — quantitative reach (downloads, population served); often required, surface-level. Use administrative-level organizations.
- **Depth** — specific positive change for individuals/communities; more compelling; EIA can quantify (ROI, $ saved). Use local users/beneficiaries.
- Impact pyramid: outputs (base) → outcomes → societal/policy impacts (top).
- Tailor evidence: testimony, photos, satellite imagery, maps, data viz — only where the audience understands them.
- Example: a USDA geospatial scientist values hours saved by a NASA drought tool; a broad audience is moved by the farmer who withstood drought using it.

## Product types (exact spec from toolkit)

| Type | Format | Key content requirements |
|---|---|---|
| Internal NASA Reporting | 150–200 words + contact info | Need and desired impact; clear links to NASA assets; images optional |
| Use Cases | 1–2 page narrative | Some sustained use and outcomes; quantitative indicators; user testimony |
| Case Studies | 2–4 pages, usually one user | Complete life cycle; thorough impact documentation; specific decisions + quantitative indicators; thorough testimony |
| Economic Impact Assessments | Analysis 2–4 pp · report 20+ pp · academic paper | Direct (downloads, active users, API calls) + indirect socio-economic impacts |
| Solution Activity Reports | 1–5 pages | Agenda, notes/actions, findings, participant feedback, evaluation results, photos, participant demographics |
| Solution Assessment Reports | 5–20 pages | Final indicator data, activity reports, stakeholder feedback, EIA data where relevant |
| NASA Blogs | ~700–800 words (narrative up to ~1,500) | Impacts or strong outcomes; accessible language; quality visuals |
| Press Releases | 1 page, 300–500 words | Who/what/when/where/why; "about us" boilerplate; 1–2 prepared quotes; contact info; **prepared with NASA Office of Communications** |

## Steps
**Plan mode:** (1) list audiences from `04` stakeholders + the five audience types; (2) for each, pick product type(s), key message, breadth vs depth evidence, champion; (3) map evidence → indicator IDs from `12` and EIA from `03`; (4) schedule.
**Draft mode:** (1) pick product; (2) **readiness check** — does the evidence meet the product's minimum (e.g., Use Case requires sustained use + quantitative indicators + testimony)? If not, say which and suggest a lower-tier product; (3) draft at the exact length; (4) list every claim with its evidence source; (5) quotes: only real, user-supplied quotes, marked `[QUOTE — confirm consent]`; never fabricate testimony.

## Output Spec

**Communications Plan**

| Audience | Why they need/want to know | Product Type | Key Message | Breadth Evidence | Depth Evidence | Champion / Spokesperson | Indicator / EIA Link | Due |
|---|---|---|---|---|---|---|---|---|

**Evidence ledger** (draft mode)

| Claim in Draft | Evidence | Source (indicator ID / doc / interview) | Verified? |
|---|---|---|---|

**Product draft** at specified length, with word count printed. For Internal NASA Reporting include a **NASA assets** line (missions, sensors, programs).

**Profile patch:** `communications[]`.

## Quality Gate
- [ ] Each draft meets its product's length and content requirements.
- [ ] Every quantitative claim maps to an evidence ledger row.
- [ ] No fabricated quotes, beneficiaries, or numbers.
- [ ] Breadth and depth both represented where the product calls for it.
- [ ] NASA assets clearly linked (internal reporting).
- [ ] Press releases flagged for NASA Office of Communications.

## Guardrails
- Never fabricate quotes, testimony, beneficiaries, or numbers; quotes only if user-supplied and consent-confirmed.
- Flag press releases for NASA Office of Communications; never send or post anything.
- Never invent people, organizations, quotes, budgets, or baselines; use `<<placeholders>>` and tag AI-drafted rows `[AI-DRAFT]`.
- AI drafts prepare for stakeholder engagement; never present them as stakeholder evidence.
- Never store or echo PII, CUI, or ITAR/EAR-controlled data; replace with placeholders and warn the user.
- Never send, post, or share outputs; produce them for the user to review.

## Example
**Prompt:** Draft a 150–200 word internal NASA highlight for our flood alert pilot using these indicator results.
**Result:** Word count within 150–200 plus contact info; Names NASA assets; Every number appears in the evidence ledger.

## Hand-offs
- Upstream: `sco-12-meaningful-metrics`, `sco-03-economic-impact-assessment`, `sco-10-implementation-monitoring-plan`
- Downstream: `partner-status-brief`

## Source
- Toolkit page: https://science.data.nasa.gov/earth-science-solution-co-development-toolkit/capturing-communicating-impact/
- Phase: Foundational (best early; core in Phase 4)
- Derived from NASA Earth Action Solution Co-Development Toolkit v0.1 (DOI 10.5281/zenodo.19866469).

## References
- `references/conventions.md` — read first, every run.
- `references/solution-profile.template.yaml` — when creating or patching the shared profile.
