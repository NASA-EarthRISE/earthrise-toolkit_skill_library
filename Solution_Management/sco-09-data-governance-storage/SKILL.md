---
name: sco-09-data-governance-storage
description: "Draft a FAIR, NASA Open Science (SPD-41a) compliant Data Governance and Storage Plan — inputs/outputs, formats and metadata, sharing and release timeline, DAAC repositories, preservation, open-source software, roles, licensing, volume, security — plus the 15-row compliance checklist. Use at the start of Phase 2 and maintain through Phase 3. Use when someone asks for a data management plan, Open Science or SPD-41a compliance, DAAC archiving, metadata standards, file naming, licensing, or data release timelines."
---

# Tool 9 — Data Governance & Storage Plan (Agent Guide)

Read `references/conventions.md` first (shared rules: provenance tags, output format, commands, tool-number → skill-id map). State schema: `references/solution-profile.template.yaml`.

## Purpose
Guide data formation, use, sharing, version control, storage, and publication across intake data, intermediate datasets, and outputs, following FAIR (Findable, Accessible, Interoperable, Reusable) and NASA data management plan guidance. Start early: hard-to-find or disorganized data reduces long-term use.


## Inputs
- `report.md` — Technical requirements (inputs, outputs, platforms).
- Optional: `solution-profile.yaml` from any earlier toolkit skill (reused, never re-asked).

## Outputs
- `report.md` — Plan sections 1–10, data inventory, compliance checklist, plus a YAML patch to `solution-profile.yaml` (schema in `references/solution-profile.template.yaml`).
- Exact table layouts: see **Output Spec** below.


## Steps
Pre-fill from `technical.data_sources`, `technical.outputs`, `technical.processing_env`. Then walk Sections 1–10, asking only for decisions — use the template defaults below and ask the user to **accept / modify** each.

1. **Data Inputs.** Classify each input: 1.1 NASA satellite RS (e.g., MODIS, VIIRS, Landsat, OCO-2/3, GEDI, ECOSTRESS; Earthdata/DAACs) · 1.1.2 NASA modeling/analysis (GEOS/GMAO, NLDAS, GLDAS) · 1.1.3 NASA airborne (AVIRIS, AirMOSS, CARVE, ACT-America; ORNL DAAC, GHRC) · 1.1.4 **PII & sensitive data** (ask explicitly: any PII, CUI, ITAR/EAR-sensitive asset locations, socio-economic microdata?) · 1.1.5 Commercial (e.g., CSDA) → provider license terms.
   **1.2 New outputs:** derived parameters, QC'd subsets, model–observation fusion, ML outputs + uncertainty, scripts/workflows/notebooks/visualizations — public under NASA Open-Source Science policy.
2. **Standards.** Formats: NetCDF4 (CF), HDF5, GeoTIFF/COG, CSV, JSON/YAML, PNG/JPEG. Metadata: CF ≥1.7, NASA DIF or ISO 19115/19139 per DAAC, DOI metadata, OGC spatial, W3C PROV. File naming by partner consensus — reflects contents + version. **Propose a concrete naming pattern** (e.g., `<project>_<product>_<region>_<YYYYMMDD>_v<MAJOR>.<MINOR>.nc`). Restricted files: Need-to-Know only. Validate data + metadata before archiving.
3. **Sharing & Access.** No proprietary period. Release timeline: inputs already public; derived datasets within **N days** of validation and no later than project end (**ask for N** — template leaves "XX"); software at/before first publication or presentation; documentation at data release. Repositories: GES DISC, LP DAAC/LAADS DAAC, PO.DAAC, ORNL DAAC; else NASA-sponsored portals or institutional servers. No paywalls/logins/embargoes.
4. **Preservation & Archiving.** DAACs long-term (redundancy, integrity, DOIs). During project: institutional secure servers, GitHub/NASA-approved VCS, cloud + local replicas, immutable tagged releases.
5. **Software/Tools/Workflows.** OSS license (MIT, BSD-3, Apache 2.0); public GitHub/GitLab with README, install, example data, containers (Docker/Singularity), CI; reproducibility (provenance, Conda/Dockerfile/requirements.txt, notebooks, Earthdata API retrieval scripts).
6. **Responsibilities.** PI: QC, Open Science compliance, metadata validation, repository submission, DOI, DAAC liaison. Data Manager/Co-I: version control, code review, packaging, archival submission, documentation. Ask for names/roles.
7. **Re-use & Citation.** CC-BY-4.0 data; MIT/BSD/Apache code; cite dataset DOI, repos (GitHub/Zenodo), publications, NASA DAAC sources. **Generate the citation text.**
8. **Expected Volume.** Defaults: satellite subsets + model 1–5 TB · airborne 0.1–3 TB · derived 50–500 GB · software/docs <5 GB. Offer to estimate from AOI × resolution × timesteps × bands if user gives them (show the arithmetic).
9. **Restrictions, Ethics, Security.** Template default states no restrictions/PII/controlled data and compliance with ROSES, Open Science, SPD-41a, DAAC requirements. **Reconcile with 1.1.4** — if any PII/sensitive data exists, replace default text with handling plan (NASA Records Retention Schedules NRRS 1441.1, NPR 2810.7 for CUI destruction, ITAR/EAR).
10. **Branding/Acknowledgements.** Acknowledge NASA; OCOMM provides statement — leave placeholder `<<OCOMM acknowledgement statement>>`.

## Output Spec

**Section 1 — Plan narrative** with headings exactly: 1. Data Inputs (1.1–1.1.5, 1.2) · 2. Standards to Be Used for Data and Metadata (2.1 File Formats, 2.2 Metadata Standards, 2.3 File Naming Conventions) · 3. Data Sharing and Access (3.1 Compliance With NASA Open Science, 3.2 Release Timeline, 3.3 Data Repositories) · 4. Data Preservation and Archiving (4.1, 4.2) · 5. Software, Tools, and Workflows (5.1–5.3) · 6. Data Management Responsibilities · 7. Policies for Re-Use, Redistribution, and Citation · 8. Expected Data Volume · 9. Restrictions, Ethics, and Security · 10. Branding/acknowledgements.

**Data inventory**

| Dataset | Role (Input / Intermediate / Output) | Type (Satellite / Model / Airborne / Commercial / In situ / Derived) | Source / DAAC | Format | Metadata Std | Est. Volume | Access (Open / Restricted) | License | Release By |
|---|---|---|---|---|---|---|---|---|---|

**Section 2 — Data Governance and Plan Checklist** (exact headers and rows; add Status column)

| Category | Requirement / Best Practice | Checklist Items | Status (✅/⚠️/❌) | Notes |
|---|---|---|---|---|
| Solution Name | | | | |
| Data Types & Sources | Identify NASA input and derived data | List satellite datasets; list model data; list airborne data; describe derived outputs; confirm DAAC sources are public | | |
| Data & Metadata Standards | Use standard formats and metadata | NetCDF4/CF; HDF5; GeoTIFF; CSV; ISO 19115/19139; DIF; OGC spatial metadata; W3C PROV | | |
| Open Science Compliance | Meet SPD-41a requirements | No embargo; public release; open access; no login required | | |
| Data Sharing | Provide access pathways and documentation | Identify DAAC; provide DOI; include README; release notebooks and workflows | | |
| Repositories | Use NASA DAACs and open repositories | Submit to GES DISC / LP DAAC / ORNL DAAC / PO.DAAC; use Zenodo/GitHub for prereleases | | |
| Preservation | Ensure long-term data integrity | Integrity checks; backed-up servers; immutable version tagging | | |
| Documentation | Provide complete documentation | READMEs; processing steps; uncertainties; QA/QC; workflow diagrams | | |
| Software & Tools | Release all code as open-source | Public GitHub; MIT/BSD/Apache license; examples; notebooks; containers | | |
| Reproducibility | Ensure workflows are replicable | Document workflows; data retrieval scripts; versioned code; automated tests | | |
| Data Volume | Estimate and manage storage | Estimate raw/intermediate/final sizes; confirm storage resources | | |
| Roles | Assign team responsibilities | PI oversight; Data Manager for metadata and QA/QC | | |
| Licensing & Reuse | Enable broad reuse | CC-BY 4.0 for data; MIT/BSD/Apache for code; citation instructions | | |
| Ethics & Security | Ensure compliance | No PII; no restricted data; policy-compliant | | |
| QA/QC & Validation | Provide validation processes | QA/QC steps; validation; uncertainty estimates | | |

**Optional AI-ready extras** (offer): `README.md` skeleton for the data repo · `CITATION.cff` · STAC/collection metadata stub · `.zenodo.json`.

**Profile patch:** `data_governance.*`.

## Quality Gate
- [ ] Every input and output in the inventory with format, source, license.
- [ ] Release window N is a number, not "XX".
- [ ] Target repository/DAAC named (or justified alternative).
- [ ] PII/sensitive data question answered; Section 9 consistent with 1.1.4.
- [ ] Named PI + Data Manager roles.
- [ ] Naming convention and versioning pattern concrete.
- [ ] Checklist has no ❌ without an accepted open item.

Refs: NASA Records Retention Schedules https://nodis3.gsfc.nasa.gov/NPR_attachments/NRRS_1441.1_03122025.pdf · NASA Records Management https://www.nasa.gov/nasa-records-management/

## Guardrails
- Never leave the release window as XX; require a number.
- Reconcile PII/sensitive data answers with Section 9; never claim 'no PII' without asking.
- Never invent people, organizations, quotes, budgets, or baselines; use `<<placeholders>>` and tag AI-drafted rows `[AI-DRAFT]`.
- AI drafts prepare for stakeholder engagement; never present them as stakeholder evidence.
- Never store or echo PII, CUI, or ITAR/EAR-controlled data; replace with placeholders and warn the user.
- Never send, post, or share outputs; produce them for the user to review.

## Example
**Prompt:** Write our data governance plan; inputs are Landsat and GPM, output is a COG flood map.
**Result:** Data inventory includes inputs and outputs with format and license; Checklist has all 15 rows with status.

## Hand-offs
- Upstream: `sco-08-technical-requirements`
- Downstream: `sco-10-implementation-monitoring-plan`, `sco-11-adoption-sustainability`, `reproducible-release`

## Source
- Toolkit page: https://science.data.nasa.gov/earth-science-solution-co-development-toolkit/data-governance/
- Phase: 2–3
- Template — Data_Governance_and_Storage_Template.docx: https://science.data.nasa.gov/earth-science-solution-co-development-toolkit/static/toolkit_documents/Data_Governance_and_Storage_Template.docx
- Derived from NASA Earth Action Solution Co-Development Toolkit v0.1 (DOI 10.5281/zenodo.19866469).

## References
- `references/conventions.md` — read first, every run.
- `references/solution-profile.template.yaml` — when creating or patching the shared profile.
