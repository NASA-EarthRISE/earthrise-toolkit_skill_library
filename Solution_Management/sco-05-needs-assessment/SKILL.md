---
name: sco-05-needs-assessment
description: "Capture, code, theme, and prioritize the needs, decision contexts, and constraints of priority user groups, and translate them into draft EO requirements; includes an interview guide. Use in Phase 1 after stakeholder mapping, once per priority user group. Use when someone asks to assess user needs, write a needs-assessment interview guide, code interview notes into themes, prioritize needs, or derive EO requirements from users."
---

# Tool 5 — Needs Assessment (Agent Guide)

Read `references/conventions.md` first (shared rules: provenance tags, output format, commands, tool-number → skill-id map). State schema: `references/solution-profile.template.yaml`.

## Purpose
Rapid, activity-level capture of user needs, decision contexts, and constraints to decide what the solution **must do, should do, and should not attempt**. Run once per priority user group. Template tabs: `Step1_User_Groups` … `Step7_Summary`.


## Inputs
- `report.md` — Stakeholder map and/or interview notes, survey results.
- `partner.request` — Partner need if no stakeholder map.
- Optional: `solution-profile.yaml` from any earlier toolkit skill (reused, never re-asked).

## Outputs
- `partner.request` — Prioritized needs with decision affected, constraints, and spatial/temporal/latency/format requirements.
- `report.md` — Step1–Step7 tables, interview guide, summary with CSV, plus a YAML patch to `solution-profile.yaml` (schema in `references/solution-profile.template.yaml`).
- Exact table layouts: see **Output Spec** below.


## Modes
- **Plan mode** — user hasn't interviewed yet → generate interview guide, survey, and recruitment list (Steps 1–2 prep).
- **Analyze mode** — user pastes notes/transcripts/survey results → code, theme, prioritize (Steps 2–7).
- **Draft mode** — no data yet, team wants hypotheses → everything `[AI-DRAFT]`, ends with a validation plan.
Ask which mode in the first turn (default: detect from what the user provides).

## Workflow (from toolkit)

| Step | Activity | Led By | Duration | Output |
|---|---|---|---|---|
| 1 | Identify & prioritize user groups | Needs Assessment Lead + EO Specialist | 1–2 days | Prioritized user list + decision contexts |
| 2 | Map tasks & current workflow (interviews + walkthroughs) | Engagement Lead + EO Specialist | 3–10 days | Workflow snapshots + pain points log |
| 3 | Identify needs & decision friction | Needs Assessment Lead | 2–3 days | Categorized needs (3–7 per group) + initial priorities |
| 4 | Identify institutional & feasibility constraints | Technical Lead + Engagement Lead | 1–2 days | Constraints log |
| 5 | Translate needs into draft EO requirements | EO Specialist | 2–3 days | Draft EO attributes + delivery requirements |
| 6 | Validate draft snapshot with user group | Needs Assessment Lead | 2–3 days | Reviewed and refined needs + requirements |
| 7 | Finalize Needs Assessment Snapshot | Core Team | 1–2 days | Phase 1 Needs Assessment Summary |

## Steps

**Step 1 — Identify Priority User Groups & Background.** Pull Users with Collaborate/Validate strategy from `stakeholders`. For each group capture role in the system, key decisions, decision type (Ops / Analytical / Policy / Advisory), operational rhythm (daily / seasonal / crisis), Data/EO literacy (Low / Med / High). Target 1–5 core groups.

**Step 2 — Map Tasks & Current Workflow.** Capture chains of *workflow step → decision → consequence*. Log pain points and workarounds. Recommend methods (below). In Analyze mode, extract these from notes.

**Step 3 — Needs & Decision Friction.** Apply the analysis method:
1. *Notes → Codes* — short labels (e.g., Data latency, Verification burden, Threshold ambiguity, Approval dependency).
2. *Codes → Themes* — 3–7 themes per group (e.g., Decision-ready timing, Clear defensible thresholds, Authority clarity).
3. *Themes → Decisions* — for each theme: decision affected, consequence if unmet. **A theme that can't map to a decision is low priority or poorly defined — say so.**
4. *Prioritize* — rate Value (decision impact, burden reduction) and Feasibility (technical, data, partner) H/M/L, then place on the matrix below.
Run an **Assessment Check** before Step 4: every need is tied to a decision, a group, and evidence.

| | Low feasibility | Medium feasibility | High feasibility |
|---|---|---|---|
| **High value** | Challenging but Important | Wins worth the extra effort | Major Wins / Quick Wins |
| **Medium value** | Mostly Avoid | Nice to Have | Valuable Wins |
| **Low value** | Avoid | Mostly Avoid | Optional, Easy Wins if Resources Allow |

Map to final priority: **Do now / Do next / Nice to have / Avoid**.

**Step 4 — Constraints.** Feasibility lens; separate user frustrations from structural realities. Types: technical, institutional, cultural, access, intermediary, team/science.

**Step 5 — Draft EO Requirements.** For each Do-now/Do-next need: minimum viable spatial, temporal, latency, and format attributes. Each requirement links to one need ID.

**Step 6 — Validation.** Generate a 30–45 min validation call/workshop script (not full co-design) confirming priorities, usability, constraints. Record confirm / revise / reject.

**Step 7 — Summary.** Top needs, workflow implications, feasibility guardrails, EO opportunity areas, must / should / should-not.

## Methods (recommend ≥2)

| Method | Most Useful Steps | Support Level |
|---|---|---|
| Surveys & Questionnaires (<2 min gets best response) | 3, 6 | 1–2 |
| Focus Groups (5–8 people) | 3, 6 | 2–3 |
| Discovery Interviews | 1–4 | 1–3 |
| Workflow Walkthroughs | 2–4 | 2–3 |
| Observation / Shadowing (optional) | 2–4 | 3 |
| Document & System Review (optional) | 1, 2, 4 | 1 |
| Usage Analytics (optional) | 2–4 | 2 |
| Participatory Mapping (optional) | 1, 3, 6 | 2–4 |

Support levels: 1 structured w/ templates · 2 applied social research · 3 advanced facilitation · 4 specialized expertise.

## Interview guide generator
When asked, produce a semi-structured guide tailored to the user group using this prompt menu (compass, not script). Principles: anchor in recent specific experiences; delay proposing solutions; signal curiosity not evaluation; compare said vs. done; surface constraints; triangulate; accept partial coverage.

| # | Section | Purpose |
|---|---|---|
| 1 | Ground the Conversation in Real Work | Role, authority, which decisions depend on satellite/geospatial data |
| 2 | Walk Through a Recent Decision | Anchor in real workflow ("last time you…") |
| 3 | Surface Gaps (Indirectly) | Difficulties during that decision |
| 4 | Explore EO / Geospatial Use | Which maps/satellite products used; fit-for-use |
| 5 | Surface Workarounds | Hidden must-haves (probe: what if the workaround disappeared?) |
| 6 | Clarify What "Useful" Means | Scale, timing, format |
| 7 | Understand Confidence & Comfort | How confident justifying a decision with this info |
| 8 | Surface Constraints Naturally | What makes changing the work hard even with better tools |
| 9 | Shift to Priorities | One improvement that would matter most |
| 10 | Close the Loop | Does summary reflect experience? What was missed? Who else to talk to? |

Write 1 core prompt + 2 probes per section in plain language for the specific decision context.

## Output Spec (one set per user group)

**Step1_User_Groups** (exact headers from template)

| User Group | Role in the System | Key Decisions | Decision Type | Operational Rhythm | Data/EO Literacy |
|---|---|---|---|---|---|

**Step2_Workflow**

| User Group | Workflow Step | Decision | Information Used | Consequence | Pain Point / Workaround | Evidence Source |
|---|---|---|---|---|---|---|

**Step3_Needs**

| Need ID | User Group | Codes | Theme | Need Statement | Decision Affected | Consequence if Unmet | Value (H/M/L) | Feasibility (H/M/L) | Matrix Cell | Priority | Source |
|---|---|---|---|---|---|---|---|---|---|---|---|

**Step4_Constraints**

| ID | User Group | Constraint Type | Description | Frustration or Structural Reality | Implication for Solution |
|---|---|---|---|---|---|

**Step5_Requirements**

| Req ID | Linked Need ID | Spatial | Temporal | Latency | Format / Delivery | Minimum Viable? |
|---|---|---|---|---|---|---|

**Step6_Validation**

| Item (Need/Req ID) | Validation Method | Result (Confirmed / Revised / Rejected) | Feedback | Change Made |
|---|---|---|---|---|

**Step7_Summary** — headings: Top Needs · Workflow Implications · Feasibility Guardrails · EO Opportunity Areas · Must Do / Should Do / Should Not Attempt.

CSV for each table. **Profile patch:** `user_groups[]`, `needs[]`, `constraints[]`, `eo_requirements[]`, `impact.need` (if empty).

## Quality Gate
- [ ] 1–5 groups; each with decision type, rhythm, literacy.
- [ ] 3–7 needs per group, each mapped to a decision + consequence.
- [ ] Every need has Value, Feasibility, Priority.
- [ ] Constraints separate structural realities from frustrations.
- [ ] Every EO requirement links to a Do-now/Do-next need.
- [ ] Step 6 validation planned or done; `[AI-DRAFT]` count shown.
- [ ] No identifiable quotes without consent.

> Note: column headers for Steps 2–7 are reconstructed from published step guidance; Step 1 headers are exact. Paste a CSV export to align exactly.

## Guardrails
- Never reproduce identifiable quotes without consent; summarize into codes.
- Every need must map to a decision; flag those that don't.
- Never invent people, organizations, quotes, budgets, or baselines; use `<<placeholders>>` and tag AI-drafted rows `[AI-DRAFT]`.
- AI drafts prepare for stakeholder engagement; never present them as stakeholder evidence.
- Never store or echo PII, CUI, or ITAR/EAR-controlled data; replace with placeholders and warn the user.
- Never send, post, or share outputs; produce them for the user to review.

## Example
**Prompt:** Here are notes from 4 interviews with district water managers. Code and prioritize the needs.
**Result:** Produces codes, 3–7 themes, need statements mapped to decisions; Each need has Value, Feasibility, and Do now / Do next / Nice to have / Avoid.

## Hand-offs
- Upstream: `sco-04-stakeholder-mapping`
- Downstream: `sco-01-designing-for-impact`, `sco-06-information-chain-analysis`, `sco-07-user-centered-design`, `sco-08-technical-requirements`, `sco-03-economic-impact-assessment`

## Source
- Toolkit page: https://science.data.nasa.gov/earth-science-solution-co-development-toolkit/needs-assessment/
- Phase: 1 (secondary in Phase 2)
- Template — Needs_Assessment_Template_and_Guidance.xlsx (Google Sheets): https://docs.google.com/spreadsheets/d/1Yi0ScvjPthAMr1fQNkLX50kDHNTalrHz/edit?gid=78278432
- Derived from NASA Earth Action Solution Co-Development Toolkit v0.1 (DOI 10.5281/zenodo.19866469).

## References
- `references/conventions.md` — read first, every run.
- `references/solution-profile.template.yaml` — when creating or patching the shared profile.
