# TOE index (folders and key files)

This is a structured index for quick navigation. Each section points to the main doc or the key files.

## Meta docs
- `_docs/toe_story.md`: narrative walkthrough
- `_docs/toe_status.md`: checkpoint-derived status snapshot
- `_docs/toe_checkpoint_summary.md`: JSON checkpoint digest
- `_docs/toe_atlas.md`: CSV/JSON atlas per bucket
- `data/_workbench/README.md`: organized working surface
- `data/_workbench/TOE_MAP.md`: concept-to-files map
- `data/_workbench/05_symmetry/N12_extended_summary.md`: N12 extended symmetry summary
- `data/_workbench/05_symmetry/2T_to_A4_quotient_check.md`: 2T center quotient check

## Primary TOE outputs

- `_toe/coupling_20260110`
  - `README_TOE_coupling.md`: coupling between 2T transport, projective classes, and W33 lines
  - `orbit0_edges_with_projective_images.csv`: orbit-0 edge lift with projective images
  - `edge_elem_projective_visibility.csv`: which 2T elements act trivially projectively
  - `W33_lines_to_projective_quartets.csv`: line -> quartet map

- `_toe/flux_toggle_node0_20260110`
  - `README_flux_toggle_node0.md`: flux toggle and node0/global comparison
  - `scan_global_bestline_triplet_*.csv`: global stability scans
  - `scan_node0local_bestline_triplet_*.csv`: node0-local scans
  - `node0local_winner_changed_points.csv`: flip locations

- `_toe/true_projector_w33_20260110`
  - `README_true_projector_flux_test.md`: rank-1 projector test
  - `flux_scan_rank1_projector_global_stability.csv`
  - `noflux_scan_rank1_projector_global_stability.csv`

- `_toe/native_w33_projectors_c24_20260110`
  - `checkpoint_native_C24_projectors_20260110.json`
  - `native_C24_projector_stabilities_flux_vs_noflux_keypoints.csv`
  - `native_C24_projector_winners_keypoints.csv`
  - `u_k_parityminus_k_sweep_keypoints.csv`
  - `uvec_k0_parityminus_realimag.csv`

- `_toe/native_fullgrid_20260110`
  - `README.md`
  - `checkpoint_nativeC24_fullgrid_20260110.json`
  - `nativeC24_fullgrid_line_stabilities_flux_noflux.csv`
  - `nativeC24_fullgrid_winners_flux_vs_noflux.csv`
  - `nativeC24_line_flux_response_ranking_summary.csv`
  - `winner_surface_flux_lineid.csv`
  - `winner_surface_noflux_lineid.csv`

- `_toe/flux_response_rankings_20260110`
  - `report.md`: winner flips and top flux-sensitive lines
  - `line_flux_response_summary.csv`: per-line summary
  - `top15_flux_sensitive_lines.csv`

- `_toe/flux_response_law_20260110`
  - `README_flux_response_law.md`: regression model and predictors
  - `response_law_regression_coeffs_all40.csv`
  - `grid_flux_noflux_defectmass_coherence.csv`

- `_toe/geometric_reduction_20260110`
  - `README.md`: cocycle + quartet feature reduction
  - `orbit0_edges_Z2_cocycle.csv`
  - `lines_with_quartet_features_and_response_coeffs.csv`

- `_toe/harmonic_lift_geometry_predictor_20260110`
  - `REPORT.md`: harmonic lift + Q12 variance predictor
  - `orbit0_harmonic_lift_theta_and_mincut_labels.csv`
  - `geometry_predictor_vs_observed_flux_sensitivity.csv`

- `_toe/domainwall_to_w33_sensors_20260110`
  - `REPORT.md`: domain-wall mincut and Q12 variance sensitivity
  - `summary.json`: mincut cost + top-10 flux sensor overlap stats
  - `orbit0_mincut_labels.csv`
  - `orbit0_mincut_spillover_edges_nondefect.csv`
  - `W33_lines_flux_sensitivity_with_Q12_variance.csv`

- `_toe/projector_recon_20260110`
  - scripts: `apply_time_evolution_expm_multiply_*.py`, `apply_W33_measurements_to_time_evolution_*.py`
  - NPZ/CSV artifacts: `TOE_H_total_transport_plus_lambda_coin_*.npz`, `TOE_*_scan_*.csv`

- `_toe/w33_orthonormal_phase_solution_20260110`
  - `W33_point_rays_C4_12throot_phases.csv`
  - `W33_point_rays_C4_complex.csv`
  - `reconstruct_W33_rays_from_phase_csv.py`

- `_toe/take_it_all_way_20260110`
  - `toe_take_it_all_way_report.md`: D6, D8, and 1296 closure
  - `tomotope15_lines_table.csv`
  - `hyperplane27_phasefunctions.csv`

- `_toe/canonical_w33_coupling_20260110`
  - `checkpoint_manifest.json`
  - `canonical_projector_*_flux_vs_noflux.csv`

## Incidence and PG(3,2) supporting datasets

- `_is/incidence_autgroup_20260110`
  - `autgroup_report.md`
  - `automorphism_group_order12_point_maps.csv`
  - `incidence_12points_15lines.csv`

- `_is/axis_stabilizer_20260110`
  - `axis_stabilizer_report.md`
  - `axis_stabilizer_summary.json`

- `_is/axis_protection_group_20260110`
  - `axis_protection_group_report.md`

- `_pg32/shadow_20260110`
  - `report_pg32_shadow.md`
  - `canonical_pg32_lift_15_phase_functions.csv`

- `_pg32/continue_20260110`
  - `pg32_continuation_report.md`
  - `PG32_points_15.csv`
  - `PG32_lines_35.csv`

- `_pg32/doily_lift_20260110`
  - `pg32_doily_lift_report.md`
  - `tomotope15_quartets_with_coeffs_and_support.csv`

- `_pg32/polarity_20260110`
  - `pg32_symplectic_polarity_report.md`

- `_pg32/symplectic_polarity_20260110`
  - `pg32_symplectic_polarity_report.md`

- `_is/star_algebra_20260110`
  - `phase_function_model_report.md`
  - `tomotope_15_rainbow_lines_phase_function_model.csv`

- `_is/gauge_anomaly_20260110`
  - `gauge_anomaly_report.md`
  - `gauge_transform_search_results.csv`

- `_is/liftability_search_20260110`
  - `liftability_report.md`
  - `liftable_symplectic_lifts.csv`

- `_pg32/symplectic_continuation_20260110`
  - `pg32_symplectic_continuation_report.md`

## Grouped datasets

- `data/_n12`: normalized N12 datasets (formerly root `N12_*` files)
- `data/_w33`: normalized W33 datasets (formerly root `W33_*` files)
- `data/_witting`: normalized Witting datasets (formerly root `witting_*` files)

## Bundles and snapshots

- `_archives/bundles/*` mirror the analysis folders.
- `_archives/bundles/toe/toe_bundle.zip` is a zip-of-zips containing several bundles (including duplicates).
