# PINECONe TEV model (pinecone-fire 0.1.0)

Source: `pinecone/economics/tev_calculator.py` → `TEVCalculator.calculate_tev`.

For each Monte Carlo draw, every `(mean, std)` parameter is sampled from `Normal(mean, std)`.
Scalars are used as they are. TEV per acre is:

```
TEV/acre = PV_timber + PVC_carbon + PE_ecosystem + L_lease

PV_timber    = (E_Pt + epsilon_t) * V_t - g
PVC_carbon   = pvc_per_acre                          = CO2_mean_tons_per_acre * carbon_credit_price
PE_ecosystem = water_quality_value + endangered_species_WTP
L_lease      = sum_{t=1..T_lease} R_t_lease[t] / (1 + r_lease)^t

TEV (scenario) = TEV/acre * case_acres[zone]
```

## Parameters

| Key | Source | Units | Meaning |
|---|---|---|---|
| `V_t` | Script 1 `AGB_per_acre_tons` ± `AGB_StdDev_per_acre_tons` | tons/acre | Standing biomass, used as the timber volume |
| `pvc_per_acre` | Script 2 `CO2_mean_tons_per_acre` × price | $/acre | Carbon value of the biomass change (post − pre) |
| `water_quality_value` | Script 4 `water_yield_per_acre_usd` ± std, or the fallback $100 ± 2 | $/acre | (PRISM ppt − 0.1·MODIS ET) × water price |
| `E_Pt` | user | $/ton | Stumpage price |
| `epsilon_t` | user | $/ton | Price shock added to `E_Pt` |
| `g` | user | $/acre | Regeneration cost |
| `endangered_species_WTP` | user | $/acre | Willingness to pay, e.g. for red-cockaded woodpecker habitat |
| `R_t_lease` | user | $/acre/yr | Hunting and lease revenue for years 1..T (missing years count as 0) |
| `T_lease` | user | years | Lease horizon |
| `r_lease` | user | fraction | Discount rate (may be `[mean, std]`) |
| `carbon_credit_price` | user | $/t CO₂e | Multiplies the CO₂ change |
| `case_acres` | user | acres | Scales TEV per acre to the scenario total |

## Earth Engine stages
- **Script 1, biomass** (`BiomassStatsCalculator`): sums biomass per pixel (Mg/ha × pixel ha × 1.10231, which gives US tons) over the vectorized focal-species polygons, then divides by polygon acres. The zone value is the mean of the per-polygon values.
- **Script 2, emissions** (`BiomassChangeCalculator`): ESA-CCI AGB post minus pre, converted with ×0.51 C, then ×44/12 CO₂. The QF==3 pixels in `ESA_CCI_AGB_DIFF` ("improbable change") are masked. The SD comes from `AGB_DIFF_SD`.
- **Script 4, water yield** (`WaterYieldCalculator`): the annual sum of PRISM `ppt` minus the annual sum of MODIS `MOD16A2GF` ET × 0.1, converted to kL per acre and multiplied by the $/kL price.

## Simulation interval
`ci_low` and `ci_high` in `metrics.json` are the 2.5 and 97.5 percentiles of the simulated
TEV. They describe the spread of the **parameter uncertainty that was entered**. They are not
a sampling confidence interval, so call them a "95% simulation interval" in reports.
