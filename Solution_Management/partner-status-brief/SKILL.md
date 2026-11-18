---
name: partner-status-brief
description: Turn technical project outputs such as accuracy metrics, release notes, technical reports and milestone plans into a one-page partner or leadership status brief with headline, RAG status, decision-relevant impact, asks and next milestone. Use when someone asks for a partner update, status brief, stakeholder summary, leadership one-pager, or to explain technical results to a non-technical audience.
---

# Partner Status Brief

## Purpose
Give partners and leadership a consistent, one-page, decision-focused view of
where a project stands, built only from the artifacts the Science and GIT teams
produced, so nothing is lost or invented in translation.

## Inputs
- Any of: `metrics.json`, `release.notes`, `report.md`, `project.plan`, and the original `partner.request` (to anchor on the decision the partner needs to make).

## Outputs
- `stakeholder.brief` — `brief_<project>_<YYYY-MM-DD>.md`, ≤ 1 page, structure in `references/brief_template.md`.

## Steps
1. **Collect inputs.** Ask which project and audience (partner technical lead, partner executive, program leadership). If no `partner.request` is available, ask: "What decision does this partner need to make with this product?"
2. **Pull facts only from inputs.** Extract: what was delivered (from `release.notes`), quality (from `metrics.json`: overall accuracy ± CI, weakest class), schedule (from `project.plan`).
3. **Translate.** Express each metric as decision impact, e.g. "OA 0.95 ± 0.02 → reliable for district-level planning; the 'forest gain' class (UA 0.73) should be field-checked before use." Keep CIs; never drop uncertainty.
4. **Set RAG status:** 🟢 on track, 🟡 at risk (state the risk), 🔴 off track (state recovery plan). Base it on `project.plan` dates and the quality bar in `partner.request` if given.
5. **Write the brief** with `references/brief_template.md`: headline (one sentence), status, what's new, what it means for you, risks/asks, next milestone + date, links.
6. **Check:** ≤ 400 words, no jargon without a plain gloss, every number traceable to an input file. List the source files at the bottom.

## Guardrails
- Never invent progress, dates, or numbers not present in the inputs; mark gaps as "TBD — owner".
- Never remove confidence intervals or caveats to make results look better.
- Respect `data_sensitivity`: no partner-restricted data in briefs addressed to other partners.
- Do not send or post the brief anywhere; produce it for the user to review.

## Example
**Input:** `metrics.json` (OA 0.947 ± 0.018; forest-gain UA 0.73 ± 0.10), `RELEASE_NOTES_v1.3.0.md`, plan with field validation due 2026-12-15.
**Output:** 🟢 "The v1.3 forest change map is delivered and meets the 90% accuracy target." + impact, one ask (field-check gain areas), next milestone.

## Hand-offs
- Upstream: `classification-accuracy-assessment` (`metrics.json`, `report.md`), `reproducible-release` (`release.notes`).
- Downstream: none (end of chain, goes to people).

## References
- `references/brief_template.md` — step 5.
