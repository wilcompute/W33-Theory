Dataset backup for TOE development

This repository contains a dataset snapshot and supporting files used to implement the TOE project. It is a direct export of the user's local `data/` folder.

Quick navigation
1) TOE docs (entry points)
   - `_docs/toe_story.md`: narrative walkthrough tying the datasets together
   - `_docs/toe_index.md`: structured index with per-folder entry points
   - `_docs/toe_status.md`: concise status derived from key checkpoints
   - `_docs/toe_checkpoint_summary.md`: auto-digest of JSON checkpoints (long but searchable)
   - `_docs/toe_atlas.md`: CSV/JSON atlas per bucket

2) TOE datasets (analysis outputs)
   - `_toe/coupling_20260110`: coupling between 2T transport, projective classes, and W33 lines (see `README_TOE_coupling.md`).
   - `_toe/flux_response_rankings_20260110`: line stability ranking and winner flips (see `report.md`).
   - `_toe/flux_response_law_20260110`: regression response law for flux sensitivity (see `README_flux_response_law.md`).
   - `_toe/flux_toggle_node0_20260110`: node0 sensitivity under flux toggle (see `README_flux_toggle_node0.md`).
   - `_toe/true_projector_w33_20260110`: rank-1 projector flux toggle test (see `README_true_projector_flux_test.md`).
   - `_toe/native_w33_projectors_c24_20260110`: native C24 projectors (see `checkpoint_native_C24_projectors_20260110.json`).
   - `_toe/native_fullgrid_20260110`: native C24 full-grid scan (see `README.md`).
   - `_toe/geometric_reduction_20260110`: geometry-only reductions and cocycle analysis (see `README.md`).
   - `_toe/harmonic_lift_geometry_predictor_20260110`: harmonic lift + geometry-only predictor (see `REPORT.md`).
   - `_toe/domainwall_to_w33_sensors_20260110`: domain-wall mincut + Q12 variance sensitivity (see `REPORT.md`).
   - `_toe/projector_recon_20260110`: reconstruction scripts + NPZ/CSV artifacts (no readme).
   - `_toe/w33_orthonormal_phase_solution_20260110`: phase solution outputs + reconstruction script.
   - `_toe/take_it_all_way_20260110`: incidence/aut group + final report (`toe_take_it_all_way_report.md`).
   - `_toe/canonical_w33_coupling_20260110`: canonical coupling csvs + `checkpoint_manifest.json`.

3) Incidence / PG(3,2) supporting datasets
   - `_is/*` folders are incremental analysis snapshots (incidence, stabilizers, etc.).
   - `_pg32/*` folders contain PG(3,2) artifacts.

4) Bundles
   - `_archives/bundles/*` are packaged snapshots of the analysis folders.

How to push to GitHub (recommended):
1. Open PowerShell in this folder.
2. Run `prepare_push.bat <your-git-remote-url>` or add a remote manually and push (see below).

Manual push example:
```
git remote add origin https://github.com/username/repo.git
git branch -M main
git push -u origin main
```

Notes:
- This README is minimal; add more project documentation as we build the TOE codebase.

Workbench:
- `data/_workbench/README.md` is the organized entry point for ongoing TOE work.
- `data/_workbench/TOE_MAP.md` is a concept-to-files map.

Notebook & reports:
- `notebooks/toe_exploration.ipynb` — exploratory notebook (saves figures to `data/_docs/figures/`).
- `data/_docs/toe_report.md` — short exploratory report embedding the notebook figures and short interpretations.

Local organization:
- `data/_docs` holds project summaries and digests.
- `data/_toe` contains core TOE analysis runs.
- `data/_is` and `data/_pg32` hold supporting incidence/PG32 work.
- `data/_checkpoints` groups checkpoint JSONs.
- `data/_embeddings` groups embedding CSVs.
- `data/_tomotope` groups tomotope CSVs.
- `data/_algebra` holds 24-cell and group tables.
- `data/_sources` holds canonical extracted inputs used by scripts.
- `data/_archives` stores zip backups and extracted bundles.
- `data/_variants` keeps non-identical duplicates for audit.
- `data/_n12`, `data/_w33`, `data/_witting` group normalized datasets.
