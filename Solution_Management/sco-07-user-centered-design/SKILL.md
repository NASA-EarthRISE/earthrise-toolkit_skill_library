---
name: sco-07-user-centered-design
description: "Build decision-anchored personas and run the four-step UCD method (decision use case, point-of-use tasks and comprehension risks, design requirements and behavioral hypotheses, validation under decision conditions) for an EO solution. Use in Phases 2–3 for design, prototyping, and testing. Use when someone asks for personas, UI or dashboard design requirements, alert threshold presentation, usability testing, or behavioral hypotheses for an EO decision tool."
---

# Tool 7 — User-Centered Design (Agent Guide)

Read `references/conventions.md` first (shared rules: provenance tags, output format, commands, tool-number → skill-id map). State schema: `references/solution-profile.template.yaml`.

## Purpose
Translate stakeholder and workflow insights into design requirements and **testable hypotheses about how better information delivery changes decisions**. Builds on — does not replace — Stakeholder Mapping, Needs Assessment, ICA, Designing for Impact.


## Inputs
- `partner.request` — Needs and decisions.
- `report.md` — Stakeholder map and ICA results.
- Optional: `solution-profile.yaml` from any earlier toolkit skill (reused, never re-asked).

## Outputs
- `report.md` — Persona blocks (Steps 1–4), design requirements, hypotheses, validation metrics, plus a YAML patch to `solution-profile.yaml` (schema in `references/solution-profile.template.yaml`).
- Exact table layouts: see **Output Spec** below.


## Personas (decision-anchored)
A persona = structured summary of **decision conditions** tied to a specific action, timing, authority, and consequence.
Not: job descriptions, broad stakeholder categories, demographics, fictional backstories. Reject those politely and reframe. Use the **minimum** number needed (worksheet supports up to 5).

Seed personas from `user_groups[]` × `needs[]` (Do now) × `decision_pathways[]` endpoints.

## Steps — repeat Steps 1–4 per persona (tabs `Persona 1`…`Persona 5`)

**Step 1 — Define the Decision Use Case.** Core decision · decision window · authority level · what successful decision performance looks like.
*Design-ready test:* decision is specific, timing explicit, authority clear, success definable. Don't proceed until all four pass.

**Step 2 — Point-of-Use Tasks & Comprehension Risks.** Tasks needed to reach action · information that must be interpreted correctly · likely misinterpretations · what must be unambiguous. **Exclude system-wide flows** (those belong in ICA `06`).

**Step 3 — Translate into Design Requirements.** Information hierarchy · threshold presentation (*threshold logic* = how clearly the solution signals when to act) · interaction flow · automation opportunities · trust signals · accessibility constraints. Then write ≥1 behavioral hypothesis:
> If we design ___, then this persona will ___.

**Step 4 — Validate Under Decision Conditions.** Plan or record a test under realistic conditions measuring: time to correct decision · interpretation errors or hesitation · escalation behavior · confidence · whether the hypothesis holds.
If performance falls short → revise hierarchy, clarify thresholds, simplify flow, revisit persona assumptions, retest. Track iterations.

## Output Spec (one block per persona)

**Step 1 — Decision Use Case**

| Field | Entry |
|---|---|
| Persona ID / Label | |
| Core decision | |
| Decision window | |
| Authority level | |
| Successful decision performance | |
| Design-ready? (specific / timing / authority / success) | |

**Step 2 — Point-of-Use Tasks & Comprehension Risks**

| Task to Reach Action | Information to Interpret Correctly | Likely Misinterpretation | Must Be Unambiguous |
|---|---|---|---|

**Step 3 — Design Requirements**

| Design Dimension | Requirement | Linked Need / Risk | Priority |
|---|---|---|---|
| Information hierarchy | | | |
| Threshold presentation | | | |
| Interaction flow | | | |
| Automation opportunities | | | |
| Trust signals | | | |
| Accessibility constraints | | | |

Behavioral hypothesis: `If we design ___, then this persona will ___.`

**Step 4 — Validation**

| Metric | Target | Result | Hypothesis Holds? | Revision |
|---|---|---|---|---|
| Time to correct decision | | | | |
| Interpretation errors / hesitation | | | | |
| Escalation behavior | | | | |
| Confidence | | | | |

Optional: generate a low-fidelity wireframe description or Mermaid user flow for the interaction flow.

**Profile patch:** `personas[]`; add Step 4 metrics as candidate Outcome indicators to `indicators[]` (`[AI-DRAFT]`).

## Quality Gate
- [ ] Each persona passes the 4-part design-ready test.
- [ ] Comprehension risks are point-of-use, not system flow.
- [ ] Every requirement traces to a decision use case.
- [ ] ≥1 testable behavioral hypothesis per persona.
- [ ] Validation metrics defined (less ambiguity, fewer errors, faster time to appropriate action).

## Design outputs UCD shapes
Information hierarchy · when-to-act thresholds · interaction flow · feature prioritization · accessibility & usability · behavioral assumptions in technical development.

> Note: Persona-tab field layout is reconstructed from the worksheet's Instructions tab (exact step names and contents).

## Guardrails
- Reject demographic or job-description personas; reframe around decision conditions.
- Keep system-wide flows out of point-of-use tasks (send to ICA).
- Never invent people, organizations, quotes, budgets, or baselines; use `<<placeholders>>` and tag AI-drafted rows `[AI-DRAFT]`.
- AI drafts prepare for stakeholder engagement; never present them as stakeholder evidence.
- Never store or echo PII, CUI, or ITAR/EAR-controlled data; replace with placeholders and warn the user.
- Never send, post, or share outputs; produce them for the user to review.

## Example
**Prompt:** Build a persona for the district officer who decides when to evacuate.
**Result:** Passes the 4-part design-ready test; Has a behavioral hypothesis in 'If we design ___, then this persona will ___' form.

## Hand-offs
- Upstream: `sco-04-stakeholder-mapping`, `sco-05-needs-assessment`, `sco-06-information-chain-analysis`, `sco-01-designing-for-impact`
- Downstream: `sco-08-technical-requirements`, `sco-10-implementation-monitoring-plan`, `sco-12-meaningful-metrics`, `sco-11-adoption-sustainability`

## Source
- Toolkit page: https://science.data.nasa.gov/earth-science-solution-co-development-toolkit/user-centered-design/
- Phase: 2–3 (applies across all phases)
- Template — UCD_Decision_Focused_Design_Worksheet.xlsx (Google Sheets; tabs Instructions, Persona 1–5): https://docs.google.com/spreadsheets/d/1B8Lv5qZIBNhnLC8uzXgwRpArfZ45tWQZ/edit?gid=661282415
- Template — User Personas Exercise (Google Doc): https://docs.google.com/document/d/1wcuIpfrIRVRzkEh7N6wowmHXGqj-rY73remACFMLKnU
- Derived from NASA Earth Action Solution Co-Development Toolkit v0.1 (DOI 10.5281/zenodo.19866469).

## References
- `references/conventions.md` — read first, every run.
- `references/solution-profile.template.yaml` — when creating or patching the shared profile.
