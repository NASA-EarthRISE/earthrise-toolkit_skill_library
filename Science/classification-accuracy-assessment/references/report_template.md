# Accuracy Assessment — {dataset}

## Purpose
Assess the accuracy of {dataset} and estimate class areas with 95% confidence intervals.

## Methods
- Reference samples: n = {n_samples}, {design} sampling, strata = map classes.
- Reference labels: {interpretation source, e.g. visual interpretation of PlanetScope / NAIP, field data}.
- Estimator: stratified estimator of Olofsson et al. (2014); 95% CIs = ±1.96·SE.

## Results
**Overall accuracy:** {oa} ± {oa_ci}

| Class | User's accuracy | Producer's accuracy |
|---|---|---|
| {class} | {ua} ± {ua_ci} | {pa} ± {pa_ci} |

| Class | Mapped area ({unit}) | Estimated area ({unit}) | 95% CI |
|---|---|---|---|
| {class} | {mapped} | {est} | ± {est_ci} |

Confusion matrix (sample counts, rows = map, columns = reference): see `confusion_matrix.csv`.

## Limitations
- {sampling design caveats, reference data quality, temporal mismatch, wide CIs}

## Reference
Olofsson, P., Foody, G. M., Herold, M., Stehman, S. V., Woodcock, C. E., & Wulder, M. A. (2014). Good practices for estimating area and assessing accuracy of land change. *Remote Sensing of Environment*, 148, 42–57.
