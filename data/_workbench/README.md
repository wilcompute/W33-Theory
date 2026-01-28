# TOE workbench

This folder is the working surface for TOE analysis. It does not replace the original data;
it provides curated entry points, mapping notes, and lightweight docs to keep the workflow tight.

Start here:
- `data/_docs/toe_story.md` for the narrative.
- `data/_docs/toe_status.md` for a quick checkpoint-derived snapshot.
- `data/_docs/toe_checkpoint_summary.md` for the full JSON digest (searchable).
- `data/_docs/toe_atlas.md` for a CSV/JSON atlas per bucket.

Workbench layout:
- `00_meta`: meta docs and status.
- `01_core`: tomotope -> projective -> W33 linkage.
- `02_geometry`: cocycle, harmonic lift, domain-wall, geometry predictors.
- `03_transport`: 2T transport and coupling artifacts.
- `04_measurement`: W33 measurement, flux response, toggles.
- `05_symmetry`: incidence, D6/D8 closures, PG(3,2) shadow.
- `06_imports`: imported archives and external snapshots.
- `07_raw`: raw bundles and backups.
- `08_pipeline`: scripts and pipeline notes.

Conventions:
- Prefer referencing original files rather than moving them.
- Add short README notes in the subfolders if a new thread appears.

Supporting storage:
- `data/_sources` contains canonical inputs extracted from legacy archives.
- `data/_archives` stores legacy zip backups.
- `data/_n12`, `data/_w33`, `data/_witting` contain grouped, normalized datasets.
