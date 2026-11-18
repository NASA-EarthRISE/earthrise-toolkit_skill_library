---
name: sco-03-economic-impact-assessment
description: "Scope and run an Economic Impact Assessment for an EO solution — choose high-level valuation vs. in-depth analysis, define baseline and attribution data, pick methods (VOI, RCT, CBA, decision models, SROI, benefits transfer), and compute a transparent value estimate. Use from Phase 1 (baseline) through Phase 4 (post-implementation). Use when someone asks for ROI, economic value, value of information, cost-benefit, socio-economic benefit, or economic impact of an Earth observation solution."
---

# Tool 3 — Economic Impact Assessments (Agent Guide)

Read `references/conventions.md` first (shared rules: provenance tags, output format, commands, tool-number → skill-id map). State schema: `references/solution-profile.template.yaml`.

## Purpose
An EIA evaluates real-world effects of a project, tool, policy, or technology by translating scientific data into social and economic metrics. Predictive (before), ongoing, or retrospective. **EIAs are hardest late — integrate at the start.**


## Inputs
- `partner.request` — Decision context and users.
- `project.plan` — Results framework and indicators.
- Optional: `solution-profile.yaml` from any earlier toolkit skill (reused, never re-asked).

## Outputs
- `metrics.json` — Economic value estimates as {direct, total} with ci_low/ci_high from sensitivity range.
- `report.md` — EIA scoping sheet, variables table, data collection plan.
- Exact table layouts: see **Output Spec** below.


## Why do one (ask the user which apply)
1. **Proving Value of Information (VOI)** — quantify changes in decisions and longer-term outcomes (e.g., prevented losses).
2. **Attributing Downstream Success** — link partner outcomes (cost reduction, lives saved) back to the service.
3. **Optimizing Product Development** — prioritize updates for tools informing high-stakes decisions.
4. **Demonstrating Operational Cost-Savings** — justify upgrades; communicate taxpayer benefits.

## Steps by phase

| Phase | Agent actions |
|---|---|
| 1 Assessment | Discuss potential EIA outcomes, data expectations, stakeholder motivations → **decide depth** (high-level / in-depth) → list pre- and post-implementation socio-economic data requirements → push them into `05` interview guides |
| 2 Co-Design | Choose key EIA indicators → baseline data plan → constant monitoring plan → add to `12` / SIIMP §12.1 |
| 3 Prototyping | Build/continue economic model; run preliminary analysis |
| 4 Transition | Collect & analyze post-implementation data; EIA outcomes in final report; valuation training if needed; plan continued evaluation |

**Depth decision rule (suggest, user decides):** High-level if goal is to decide whether deeper analysis is worthwhile, data are anecdotal/estimates, or budget is minimal. In-depth if attribution must be defensible (HQ budget justification, publication), a counterfactual is obtainable, and partners can share outcome data.

## Approach 1 — High-Level Valuation
**Info required:** user profiles (baseline, Phase 2) · testimonials (Phase 3/4) · market multipliers · reach metrics (downloads, API hits, users/partners).
**Methods:** Value Chain Analysis (upstream/midstream/downstream users) · Benefits Transfer ($ from similar tools; population in coverage area) · Reach Estimation · Qualitative (KIIs on tool criticality; testimonials).

**Calculator** (variable names disambiguated from the source, which reused "R"):
```
Direct savings  D = N × A × C × r
Total impact    T = D × M
N = # users/units · A = avg size per unit · C = cost per size unit · r = % reduction · M = socio-economic multiplier
```
Toolkit example (Alabama farms, NASA soil moisture): N=5,000 farmers, A=200 acres, C=$25/acre irrigation, r=15%, M=1.4 → D = **$3,750,000**, T = **$5,250,000**.
Always run arithmetic in code when available and print inputs, formula, result, and a **sensitivity range** (low/base/high for r and M).

```python
def eia_high_level(N, A, C, r, M):
    D = N * A * C * r
    return {"direct": D, "total": D * M}
for r, M in [(0.10, 1.2), (0.15, 1.4), (0.20, 1.6)]:
    print(r, M, eia_high_level(5000, 200, 25, r, M))
```

## Approach 2 — In-Depth Analysis
**Baseline:** Counterfactual (collection frequency, lead time, error rates) · Socio-economic (infrastructure inventory, economic activity, historical damage costs, resources) · Behavioral (resource allocation, insurance benchmarks, SOPs).
**Attribution:** Direct performance (accesses, data requests, trainings, session durations, time-to-action change) · Operational decision data (interventions, efficiency gains, preparation costs) · Economic outcomes (avoided damage claims, resource conservation, improved production).

| Method | Data needed |
|---|---|
| Value of information (VOI) | Outcome data and probabilities |
| Randomized control trials (RCTs) | Treatment and control group data |
| Cost-benefit analysis (CBA) | Costs, benefits, willingness to pay (WTP) |
| Decision models | Consumer behavior, production costs, investment returns |
| Social return on investment (SROI) | Outcome and investment data |

Example: extension officers interview 500 farmers pre/post (e.g., 12% reduction in water pumping); economic models estimate net gains by county/state.

## Output Spec — EIA Scoping Sheet

| Field | Entry |
|---|---|
| EIA purpose(s) (VOI / Attribution / Optimization / Cost-savings) | |
| Depth (High-level / In-depth) + rationale | |
| Value chain (upstream / midstream / downstream users) | |
| Decision(s) improved | |
| Counterfactual (what happens without the solution) | |
| Method(s) | |
| Variables & sources | |
| Phase timing (baseline / monitoring / post) | |
| Partner data-sharing needs | |
| Limitations & attribution caveats | |

**Variables table**

| Variable | Symbol | Value / Range | Unit | Source | Phase Collected | Confidence |
|---|---|---|---|---|---|---|

**Data collection plan**

| Data Need | Baseline or Post | Method | Responsible | Due | Feeds Indicator ID |
|---|---|---|---|---|---|

**Result block** (when computing): formula · inputs · direct · total · sensitivity table · caveats.

**Profile patch:** `eia.*`; add Impact-tier `indicators[]`.

## Quality Gate
- [ ] Purpose and depth chosen with rationale.
- [ ] Counterfactual explicit.
- [ ] Every variable has a source and confidence; no unsourced numbers presented as fact.
- [ ] Arithmetic shown and reproducible; sensitivity range given.
- [ ] Baseline collection scheduled before deployment.
- [ ] Attribution caveats stated.

Refs: Basu et al. 2025 (EIA Review) https://www.sciencedirect.com/science/article/pii/S0195925525001726 · Basu et al. 2024 https://arxiv.org/abs/2405.15672 · Bernknopf et al. 2025 (Natural Hazards) https://ntrs.nasa.gov/api/citations/20250006450/downloads/NHAZ-D-24-02237_R1.pdf · Pakhtigian et al. 2024 (JEEM) https://www.sciencedirect.com/science/article/abs/pii/S0095069624000408

## Guardrails
- Never present unsourced numbers as fact; every variable carries a source and confidence.
- Always compute arithmetic with code and show formula, inputs, and sensitivity range.
- Never invent people, organizations, quotes, budgets, or baselines; use `<<placeholders>>` and tag AI-drafted rows `[AI-DRAFT]`.
- AI drafts prepare for stakeholder engagement; never present them as stakeholder evidence.
- Never store or echo PII, CUI, or ITAR/EAR-controlled data; replace with placeholders and warn the user.
- Never send, post, or share outputs; produce them for the user to review.

## Example
**Prompt:** High-level EIA: 5000 farmers, 200 acres each, $25/acre irrigation, 15% reduction, multiplier 1.4.
**Result:** Direct = $3,750,000 and Total = $5,250,000; Shows a low/base/high sensitivity range; Writes metrics.json-shaped result.

## Hand-offs
- Upstream: `sco-01-designing-for-impact`, `sco-05-needs-assessment`
- Downstream: `sco-12-meaningful-metrics`, `sco-10-implementation-monitoring-plan`, `sco-02-capturing-communicating-impact`

## Source
- Toolkit page: https://science.data.nasa.gov/earth-science-solution-co-development-toolkit/economic-impact-assessments/
- Phase: Foundational (1 baseline → 2 SIIMP → 3 model → 4 analysis)
- Derived from NASA Earth Action Solution Co-Development Toolkit v0.1 (DOI 10.5281/zenodo.19866469).

## References
- `references/conventions.md` — read first, every run.
- `references/solution-profile.template.yaml` — when creating or patching the shared profile.
