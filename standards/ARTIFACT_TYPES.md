# Shared Artifact Types (v1.0)

The common vocabulary for skill `inputs` and `outputs`. When two skills share an
artifact type, they can be chained, regardless of which team built them.

> **Adding a type:** open a PR editing this file **and** `standards/artifact_types.yaml`.
> Needs one approval from each domain. Keep types few and general.

| Type | Format / shape | Typical producer | Typical consumer |
|---|---|---|---|
| `aoi.geojson` | GeoJSON FeatureCollection, EPSG:4326 | Solution_Management (intake) | Science |
| `dataset.raster` | Cloud-Optimized GeoTIFF or GEE asset id, with a `dataset.meta.json` sidecar | Science / GIT | Science |
| `dataset.vector` | GeoParquet / GeoPackage / GEE FeatureCollection id | Science | Science / GIT |
| `samples.csv` | CSV, one row per reference sample: `sample_id, x, y, map_class, ref_class, stratum` | Science | Science |
| `model.checkpoint` | Weights file + `model_card.md` | Science | GIT / Science |
| `metrics.json` | JSON: `{"task", "dataset", "metrics": {name: {value, ci_low?, ci_high?}}, "created", "skill", "skill_version"}` | Science | Solution_Management / GIT |
| `figure.png` | PNG ≥ 150 dpi, with caption in a sibling `.txt` | Science | Solution_Management |
| `code.repo` | Git repository URL or local path, with `README.md` | GIT | GIT / Science |
| `release.notes` | Markdown: version, date, changes, DOI/tag link | GIT | Solution_Management |
| `env.lock` | `environment.yml` / `requirements.txt` with pinned versions | GIT | GIT / Science |
| `report.md` | Markdown technical report with sections Purpose / Methods / Results / Limitations | Science | Solution_Management |
| `stakeholder.brief` | Markdown ≤ 1 page: headline, status (🟢🟡🔴), impact, asks, next milestone | Solution_Management | Partners / leadership |
| `project.plan` | Markdown or Sheet: milestones, owners, dates, risks | Solution_Management | All |
| `partner.request` | Markdown: partner, need, decision it supports, AOI, deadline, data constraints | Solution_Management | Science / GIT |
| `issue.list` | Markdown or GitHub issue URLs | Any | Any |

Machine-readable copy: [`artifact_types.yaml`](artifact_types.yaml) (the validator reads it).
