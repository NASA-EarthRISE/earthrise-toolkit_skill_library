# <Site>: Prescribed-Fire Total Economic Value (PINECONe)

## Purpose
One or two sentences: the decision being supported, the scenarios compared, and who asked.

## Methods
Total Economic Value (TEV) was estimated with PINECONe (Mayer et al. 2026,
https://doi.org/10.5281/zenodo.18419563), v<pinecone version>, run through the EarthRISE skill
`pinecone-rx-fire-valuation` v<skill_version>.
- **Biomass:** <product> <year>, over <focal species> polygons vectorized at <vectorize_scale> m from <layer id>.
- **Carbon:** ESA-CCI AGB change from <pre> to <post> at <resolution> m, carbon fraction 0.51, ×44/12, with quality flag 3 masked <yes/no>. Carbon credit price $<price>/t CO₂e.
- **Water yield:** PRISM precipitation minus MODIS MOD16A2GF ET over <start> to <end>, priced at $<price_per_kl>/kL.
- **Economics:** TEV = timber + carbon + ecosystem services + lease NPV. <n_sim> Monte Carlo draws for each scenario, seed <seed>. Parameter values are in Table A1 (from `metrics.json` → `params.economic_params`).

## Results
<paste the tables from report_draft.md unchanged>

<3–5 lines: the dominant component in each scenario, whether scenarios are distinguishable (Cohen's d, overlap), and how wide the intervals are.>

Figure 1. `figures/tev_distributions.png`: <caption from the .txt file>
Figure 2. `figures/tev_boxplots.png`: <caption from the .txt file>

## Limitations
- Every entry in `metrics.json` → `flags`, written in plain language.
- The intervals are 95% **simulation** intervals that reflect only the parameter uncertainty entered. They are not sampling confidence intervals.
- Per-acre CO₂ depends on the analysis resolution (see pitfalls §1), and the biomass SD is not a true per-acre SD (§3).
- Carbon values are remote-sensing estimates for valuation. They are not verified offsets.
- <AOI outside UTM 16N? water fallback? defaults used?>
