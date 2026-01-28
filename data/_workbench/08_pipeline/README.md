# Pipeline

Existing scripts:
- `scripts/toe_status.ps1`: generates `data/_docs/toe_status.md`
- `scripts/toe_checkpoint_digest.ps1`: generates `data/_docs/toe_checkpoint_summary.md`
- `scripts/toe_status.py`: Python version of status generator (if Python is installed)
- `scripts/bundle_inventory.ps1`: generates `data/_workbench/00_meta/BUNDLE_INDEX.md`
- `scripts/w33_phase_stats.ps1`: generates `data/_workbench/02_geometry/W33_phase_stats.md`
- `scripts/w33_line_phase_map.ps1`: generates `data/_workbench/02_geometry/W33_line_phase_map.csv` + `.md`
- `scripts/w33_line_phase_flux_join.ps1`: generates `data/_workbench/02_geometry/W33_line_phase_flux_join.csv` + `.md`
- `scripts/line_feature_table.ps1`: generates `data/_workbench/02_geometry/line_feature_table.csv` + `.md`
- `scripts/line_feature_regression.py`: generates `data/_workbench/02_geometry/line_feature_regression.csv` + `.md`
- `scripts/projective_phase_alignment.py`: generates `data/_workbench/02_geometry/projective_phase_alignment.md`
- `scripts/w33_line_phase_k12_atlas.py`: generates `data/_workbench/02_geometry/W33_line_phase_k12_map.md`
- `scripts/tau_phase_shift_analysis.py`: generates `data/_workbench/04_measurement/tau_phase_shift_report.md`
- `scripts/action_candidate_predictor.py`: generates `data/_workbench/04_measurement/action_candidate_summary.md`
- `scripts/dedupe_suffix_files.ps1`: generates `data/_workbench/00_meta/DEDUP_REPORT.md`
- `scripts/reorg_group_and_normalize.ps1`: generates `data/_workbench/00_meta/ALIASES.md`
- `scripts/update_references_from_aliases.ps1`: generates `data/_workbench/00_meta/ALIASES_APPLIED.md`
- `scripts/n12_extended_summary.ps1`: generates `data/_workbench/05_symmetry/N12_extended_summary.md`
- `scripts/verify_2T_A4_quotient.py`: generates `data/_workbench/05_symmetry/2T_to_A4_quotient_check.md`

WSL note:
- Python analysis scripts assume a WSL venv with `numpy` and `pandas` available.
- `scripts/native_c24_summary.ps1`: generates `data/_workbench/04_measurement/native_C24_summary.md`
- `scripts/native_c24_fullgrid_summary.ps1`: generates `data/_workbench/04_measurement/native_C24_fullgrid_summary.md`
- `scripts/native_vs_reduced_alignment.ps1`: generates `data/_workbench/04_measurement/native_vs_reduced_alignment.md`
- `scripts/native_c24_winner_signature.ps1`: generates `data/_workbench/04_measurement/native_C24_winner_signature.md`
- `scripts/u_k_sweep_summary.ps1`: generates `data/_workbench/04_measurement/u_k_sweep_summary.md`

Next pipeline targets (suggested):
- regenerate Q12 variance stats directly from `data/_toe/w33_orthonormal_phase_solution_20260110`
- re-derive mincut/domain-wall spillover from `orbit0_edges_Z2_cocycle.csv`
