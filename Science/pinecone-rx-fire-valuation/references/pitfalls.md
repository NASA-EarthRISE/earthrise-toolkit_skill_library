# PINECONe pitfalls (verified against pinecone-fire 0.1.0 source)

Read these before quoting numbers. Items 1–3 change values. Items 4–9 change behavior.

## 1. Emissions "per acre" scales with resolution
`BiomassChangeCalculator._calculate_emissions_stats` converts AGB to Mg/acre, multiplies
by pixel area in acres (which gives Mg per pixel), and then takes the **mean over pixels**. The
result is labeled `CO2_mean_tons_per_acre`, but it is CO₂ per *pixel*. At `resolution: 100`
a pixel is about 2.47 acres, so the value is about 2.47× a true per-acre value. `CO2_total_tons`
(mean × AOI acres) is inflated by the same factor. Keep `resolution` the same across
scenarios being compared, and state the resolution in Methods. Do not compare these
values with per-acre carbon from other sources without dividing by pixel acres
(`(resolution**2)/4046.86`). Report this upstream instead of patching it in the skill.

## 2. Sign convention: negative means emissions
CO₂ change is post minus pre. **Negative = biomass loss = emissions** and lowers TEV.
**Positive = gain = sequestration.** The PINECONe README says the opposite. Follow the code.

## 3. Biomass SD is pixel SD divided by polygon acres
`AGB_StdDev_per_acre_tons` = stdDev(tons per pixel) / polygon acres. That is not a per-acre
SD. It shrinks as polygons grow, so the uncertainty in `V_t` is understated for large stands.
Biomass is in US tons, while the emissions stage uses Mg (metric tonnes). Say this in Limitations.

## 4. Water value falls back silently
If Script 4 fails, for example with `Dictionary does not contain key: 'ET'` or with no MODIS or
PRISM data in the window, PINECONe uses `water_quality_value = (100, 2)` without warning.
`run_tev.py` reports this as `water_value_fallback:<zone>`. PRISM covers only CONUS.
MOD16A2GF has gaps near the end of a year, so try shifting the window.

## 5. Water lookup is hard-wired to `_LLP`
The package matches water results to zones with `zone.replace('_LLP','')`, so any other
species suffix always falls back. `run_tev.py` re-keys the results so that any suffix works.

## 6. User `water_quality_value` is ignored by the package
`create_economic_parameters` never reads it. `run_tev.py` applies the override and
reports it as `water_value_user_override`.

## 7. Defaults chosen by substring
Zones missing from `user_params` get the CS1, CS2 or CS3 parameters if the name contains
`CS1`, `CS2` or `CS3`. A zone named `PARK_CS10` would get severe-wildfire (CS1) values.
Zones missing from `case_acres` are skipped silently. `run_tev.py` refuses both cases.

## 8. Emissions ignore `biomass.product`, and the CRS is fixed
Script 2 always uses ESA-CCI AGB and reprojects to **EPSG:32616 (UTM 16N)**. Outside about
84–90°W, area and pixel distortion grow. Flag this for AOIs outside that band. The
`AGB_DIFF` quality and SD layers are chosen by the year of `pre[0]`, so that start year must
exist in `ESA_CCI_AGB_DIFF`.

## 9. Import clash and nulls
- The Pinecone vector-DB SDK also installs a module named `pinecone`. If imports fail
  with odd attribute errors, run `pip uninstall pinecone pinecone-client` in that environment.
- An AOI that does not overlap the focal-species mask returns null stats, and nulls then
  propagate through `ee.Algorithms.If`. `run_pinecone.py` stops on the first null. Check the overlap
  and the threshold first.
- The README shows `run_monte_carlo(input_df=..., base_cases=...)`. That signature does not
  exist. The real one is `run_monte_carlo(biomass_stats, emissions_stats, case_acres,
  water_yield_stats, user_params, carbon_credit_price, num_simulations)`.
