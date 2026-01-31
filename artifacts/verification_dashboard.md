# Verification Dashboard

Generated: 2026-01-31T06:09:01.258752Z

## Verification Digest

# Verification Digest

Auto-generated summary of verification artifacts and baseline audits.

## Sage incidence + H1

- Field: QQ
- Group order: 51840
- Structure: O(5,3) : C2
- Abelian: False
- Solvable: False
- Generators: 8
- H1 dimension: 81
- H1 matrices: 8

## Final summary table (computed)

- Generated at: 2026-01-26
- Entries: 26
- By tier: {'Tier 1': 15, 'Tier 2': 5, 'Tier 3': 4, 'Tier 4': 2}
- Max error: 619.38% (rho_Lambda / M_Pl^4)

## Baseline audit (expression search)

- Expressions evaluated: 250000
- Tolerances (%): [0.1, 0.5, 1.0, 5.0, 10.0]
- alpha hits: {'0.1': 6, '0.5': 33, '1.0': 61, '5.0': 301, '10.0': 583}
- higgs_over_z hits: {'0.1': 15, '0.5': 67, '1.0': 156, '5.0': 874, '10.0': 1737}
- omega_lambda hits: {'0.1': 15, '0.5': 82, '1.0': 184, '5.0': 702, '10.0': 1337}
- cabibbo_deg hits: {'0.1': 26, '0.5': 135, '1.0': 255, '5.0': 1250, '10.0': 2569}

## Baseline suite (strict/medium)

- strict: 250000 expressions
  - alpha hits: {'0.1': 1, '0.5': 19, '1.0': 44, '5.0': 354, '10.0': 639}
  - higgs_over_z hits: {'0.1': 9, '0.5': 42, '1.0': 85, '5.0': 486, '10.0': 899}
  - omega_lambda hits: {'0.1': 3, '0.5': 31, '1.0': 65, '5.0': 341, '10.0': 668}
  - cabibbo_deg hits: {'0.1': 16, '0.5': 68, '1.0': 130, '5.0': 668, '10.0': 1154}
- medium: 250000 expressions
  - alpha hits: {'0.1': 8, '0.5': 52, '1.0': 92, '5.0': 612, '10.0': 1043}
  - higgs_over_z hits: {'0.1': 20, '0.5': 76, '1.0': 152, '5.0': 817, '10.0': 1610}
  - omega_lambda hits: {'0.1': 9, '0.5': 61, '1.0': 124, '5.0': 624, '10.0': 1217}
  - cabibbo_deg hits: {'0.1': 33, '0.5': 146, '1.0': 290, '5.0': 1489, '10.0': 2702}

## Repo verification results

- Timestamp: 2026-01-13T16:50:54.661921
- Verified count: 20
- Failed count: 0
- Verification rate: 1.0
- Verified sample:
  - P = 40
  - L = 40
  - Q45 = 45
  - K4/Q45 = 2
  - Tri = 5280
  - TC = 240
  - Ratio = 22
  - Ratio formula
  - |PGU(3,3)| = 6048
  - τ(6) = -6048 = -|PGU|

## Predictions Report

# Predictions Report

**Passed: 5/5**

| Key | Prediction | Reference | Δ | Allowed | Result |
|---|---:|---:|---:|---:|---:|
| H0_CMB | 67.0 | 67.4 | 0.4000000000000057 | 1.5 | ✅ |
| H0_local | 73.0 | 73.0 | 0.0 | 3.0 | ✅ |
| alpha_inv | 137.036004 | 137.035999084 | 4.915999994636877e-06 | 1e-05 | ✅ |
| sin2_theta_w | 0.216 | 0.231 | 0.015000000000000013 | 0.02 | ✅ |
| M_Higgs_GeV | 125.0 | 125.1 | 0.09999999999999432 | 1.0 | ✅ |

## Sage artifacts present

| File | Size (bytes) |
|---|---:|
| a2_4_decomposition.json | 758 |
| a2_triangle_adjacency.json | 2880 |
| a2_triangles_vs_coxeter_patterns.json | 4124 |
| a2_triangles_we6_orbits.json | 2114 |
| algebraic_bijection.json | 314 |
| antipodal_preservation.json | 966 |
| balanced_orbit_canonical_mapping.json | 3837 |
| balanced_orbit_color_graph.json | 322 |
| balanced_orbit_geometry.json | 624 |
| balanced_orbit_roots.json | 321 |
| balanced_orbit_schlafli_isomorphism.json | 4441 |
| balanced_orbit_stabilizer.json | 592 |
| balanced_orbit_subgraph.json | 2401 |
| balanced_triangle_phase_alignment.json | 4403 |
| balanced_vs_schlafli.json | 314 |
| composite_multiplet_optimizer.json | 241 |
| compute_explicit_bijection.json | 181 |
| constraint_multiplet_solver.json | 2317 |
| coxeter_gauge_search.json | 17665 |
| d4_d4_e8_decomposition.json | 629 |
| d4_d4_e8_decomposition.md | 4056 |
| d4_triality_action.json | 1078 |
| d4_triality_action.md | 1989 |
| d4_w33_structure_analysis.json | 1822 |
| d4_w33_structure_analysis.md | 1454 |
| derive_27_connection.json | 266 |
| derive_e6_e8_connection.json | 363 |
| e6_27_connection.json | 151 |
| e6_we6_orbit_refined.json | 205 |
| e8_coxeter6_orbits.json | 33927 |
| e8_coxeter_phase_vs_f3.json | 8520 |
| e8_edge_relation_search.json | 27119 |
| e8_edge_relation_search.md | 6585 |
| e8_linegraph_compare.json | 1374 |
| e8_linegraph_compare.md | 718 |
| e8_orbit_to_f3_point.json | 2438 |
| e8_order6_partition_found.json | 46 |
| e8_order6_partition_strict5000_found.json | 47 |
| e8_order6_partition_strict_found.json | 42 |
| e8_orthogonal_partition.json | 1928 |
| e8_partition_search.json | 432 |
| e8_partition_search.md | 242 |
| e8_partition_search_fullip_limited.json | 191 |
| e8_partition_search_fullip_limited.md | 168 |
| e8_partition_search_orthocount_deep.json | 196 |
| e8_partition_search_orthocount_deep.md | 173 |
| e8_partition_search_pattern_filter.json | 432 |
| e8_partition_search_pattern_filter.md | 242 |
| e8_root_to_edge.json | 14040 |
| e8_root_to_edge_we6_orbits.json | 13949 |
| e8_root_to_f3_point.json | 20447 |
| e8_root_to_w33_edge.json | 17702 |
| e8_rootline_partition.json | 1907 |
| e8_rootline_partition.md | 863 |
| e8_structured_partition.json | 3931 |
| e8_triality_partition.json | 4033 |
| e8_triple_relation_search.json | 168 |
| e8_triple_relation_search.md | 181 |
| e8_triple_relation_search_composite.json | 100 |
| e8_triple_relation_search_composite.md | 130 |
| e8_triple_relation_search_full.json | 634 |
| e8_triple_relation_search_full.md | 582 |
| e8_witting_compare.json | 769 |
| e8_witting_compare.md | 634 |
| edge_order6_element_full.json | 432 |
| edge_perms.g | 8601 |
| edge_root_bijection.csv | 18854 |
| edge_root_bijection.json | 92926 |
| edge_root_bijection_canonical.csv | 15489 |
| edge_root_bijection_canonical.json | 79151 |
| edge_root_bijection_stats.json | 949 |
| edge_root_bijection_stats_sage.json | 3626 |
| edge_root_bijection_summary.json | 668 |
| edge_root_canonical_orbit_bijection.json | 66190 |
| edge_root_system_analysis.json | 629 |
| edge_root_system_analysis.md | 2488 |
| edge_root_we6_orbit_mapping_summary.json | 664 |
| edge_to_e8_root.json | 21240 |
| edge_to_e8_root_we6_orbits.json | 24989 |
| edge_vertex_matching.json | 30753 |
| edge_we6_conjugacy.json | 75 |
| edgepair_we6line_conjugacy.json | 75 |
| eigenspace_d4_analysis.json | 705 |
| eigenspace_d4_analysis.md | 2574 |
| eigenvector_analysis.json | 331 |
| eigenvector_analysis.md | 2781 |
| equivariant_csp_orbit_iso.json | 70 |
| equivariant_search_result.json | 403 |
| equivariant_search_result_anneal.json | 402 |
| equivariant_search_result_s6.json | 469 |
| equivariant_single_gen_solution.json | 56 |
| exact_fractional_analysis.json | 482 |
| exact_fractional_analysis.md | 1928 |
| exceptional_we6_patterns.json | 1657 |
| explicit_bijection_decomposition.json | 27824 |
| explicit_bijection_e8_weyl.json | 24278 |
| explicit_bijection_even_weyl.json | 24453 |
| explicit_bijection_refined.json | 3922 |
| explicit_coset_bijection.json | 157 |
| final_summary_table.json | 7034 |
| final_summary_table.md | 2072 |
| global_edge_line_map.json | 644 |
| h12_h27_incidence_patterns.json | 406 |
| h12_h27_incidence_patterns.md | 581 |
| h12_triangle_label_functions.json | 1062 |
| h12_triangle_label_functions.md | 452 |
| h27_affine_hyperplane_search.json | 114 |
| h27_affine_hyperplane_search.md | 483 |
| h27_affine_plane_equations.json | 791 |
| h27_affine_plane_equations.md | 159 |
| h27_code_invariants.json | 205 |
| h27_code_invariants.md | 305 |
| h27_fiber_edge_rule.json | 6843 |
| h27_fiber_edge_rule.md | 328 |
| h27_fiber_translation_structure.json | 1681 |
| h27_fiber_translation_structure.md | 606 |
| h27_heisenberg_automorphisms.json | 82 |
| h27_heisenberg_automorphisms.md | 112 |
| h27_heisenberg_model.json | 125 |
| h27_heisenberg_model.md | 188 |
| h27_in_schlafli_intersection.json | 484 |
| h27_in_schlafli_skew.json | 34 |
| h27_jordan_algebra_test.json | 469 |
| h27_jordan_algebra_test.md | 1589 |
| h27_latin_cube_search.json | 91 |
| h27_latin_cube_search.md | 421 |
| h27_schlafli_leftover_cycles.json | 1711 |
| h27_schlafli_triangle_structure.json | 2221 |
| h27_triplet_structure.json | 1958 |
| h27_triplet_structure.md | 820 |
| job_60656079843_logs.zip | 13430 |
| line_point_duality_bijection.json | 11292 |
| multiplet_assignment_solver.json | 296 |
| NUMERIC_COMPARISONS.json | 198 |
| orbit_adj_gram_auts.json | 486 |
| orbit_bijection.json | 288 |
| orbit_gram_auts.json | 478 |
| pancharatnam_symplectic_invariants.json | 1916 |
| pattern_class_clusters.json | 916 |
| pattern_class_feature_table.json | 4982 |
| pattern_class_feature_table.md | 746 |
| pattern_class_h12_h27_profile.json | 4738 |
| pattern_class_k4_profile.json | 3210 |
| pattern_class_multiplet_inference.json | 925 |
| pattern_class_physics_profile.json | 5426 |
| pattern_class_support_sizes.json | 398 |
| pattern_class_vertex_k4_incidence.json | 3197 |
| pattern_preserving_subgroup.json | 602 |
| pattern_quotient_graph.json | 2168 |
| physical_multiplet_inference.json | 2089 |
| predictions_report.json | 1091 |
| predictions_report.md | 457 |
| psp43_index120_actions.json | 63 |
| psp43_index240_actions.json | 56 |
| quotient_graph_analysis.json | 1118 |
| qutrit_pauli_w33.json | 208 |
| qutrit_pauli_w33.md | 272 |
| root_line_sign_assignment.json | 34 |
| root_line_sign_cocycle.json | 411 |
| root_line_sign_cocycle_stats.json | 5272 |
| root_line_sign_negative_word.json | 75 |
| run_21088432299_logs.zip | 9301 |
| run_21088695676_logs.zip | 9501 |
| run_21088737371_logs.zip | 12707 |
| run_21089037504_logs.zip | 12724 |
| run_21089116847_logs.zip | 9850 |
| sage-part-jsons-21089037504.zip | 39189 |
| sage-part-jsons.zip | 39189 |
| sage_e6_h27_isomorphism.json | 1912 |
| schlafli_by_orbit.json | 4911 |
| schlafli_h27_switching.json | 1654 |
| schlafli_phase_formula.json | 48 |
| schlafli_phase_formula_perm.json | 48 |
| signed_line_extension.json | 124 |
| signed_line_extension_we6_true.json | 143 |
| signflip_group_order.json | 79 |
| skipped_optional_tests.json | 3859 |
| sp43_edge_generators.json | 36412 |
| sp43_edgepair_generators.json | 29859 |
| sp43_we6_bijection.json | 194 |
| sp43_we6_generator_map.json | 34013 |
| sp43_we6_generator_map_full_verify.json | 1156 |
| sp43_we6_generator_map_full_we6.json | 28011 |
| sp43_we6_generator_map_full_we6_verify.json | 501 |
| sp43_we6_generator_map_sage.json | 87 |
| sp43_we6_generator_map_sage_verify.json | 81 |
| spectral_cascade_summary.md | 2864 |
| spectral_connections.json | 430 |
| spectral_connections.md | 7748 |
| spectral_synthesis.md | 3188 |
| srg40_uniqueness.json | 5719 |
| srg40_uniqueness.md | 1561 |
| su3_a2_root_mapping.json | 935 |
| su3_phase_edge_lift.json | 3613 |
| su3_phase_orbit_bias.json | 1276 |
| summary-results-5162588446.zip | 112 |
| SUMMARY_RESULTS.json | 111091 |
| triangle_e8_correspondence.json | 690 |
| triangle_e8_correspondence.md | 1834 |
| triangle_relabeling_search.json | 457 |
| triangle_relabeling_search_exhaustive.json | 2161 |
| verification_digest.json | 6377 |
| verification_digest.md | 1999 |
| verify_coxeter6_numpy.json | 776 |
| vertex_type_vs_we6_pattern.json | 3286 |
| w33_e8_explicit_bijection.json | 916 |
| w33_e8_root_line_bijection.json | 748 |
| w33_e8_triality_bijection.json | 5291 |
| w33_k4_bargmann_phase.json | 277 |
| w33_lines_to_d4.json | 56901 |
| w33_local_heisenberg_model.json | 82 |
| w33_local_heisenberg_model.md | 305 |
| w33_local_heisenberg_table.json | 3547 |
| w33_local_heisenberg_table.md | 1340 |
| we6_coxeter6_intersection.json | 6722 |
| we6_line_perms.g | 5695 |
| we6_orbit_labels.json | 22238 |
| we6_orbits_on_e8_roots.json | 1296 |
| we6_order6_partition_found.json | 41 |
| we6_true_action.json | 81899 |
| weyl_e6_action.json | 269 |
| witting_24basis_exact_bound.json | 40 |
| witting_24basis_symmetry.json | 529 |
| witting_bargmann_phase.json | 35 |
| witting_basis_alignment_search.json | 127 |
| witting_configuration.json | 557 |
| witting_e8_realification.json | 685 |
| witting_external_unitary_search.json | 174 |
| witting_f3_projective_map_test.json | 168 |
| witting_graph_isomorphism.json | 5998 |
| witting_grid_triangle_phases.json | 155 |
| witting_isomorphism_orbit_check.json | 50 |
| witting_ks_criticality.json | 42 |
| witting_ks_minimize.json | 180 |
| witting_ks_reduce_bases.json | 126 |
| witting_ks_uncolorable.json | 23 |
| witting_monomial_symmetry.json | 65 |
| witting_overlap_phase_spectrum.json | 741 |
| witting_pair_phase_family_table.json | 1698 |
| witting_pair_phase_gauge_fit.json | 81 |
| witting_pair_phase_symplectic.json | 495 |
| witting_pancharatnam_structure.json | 642 |
| witting_pancharatnam_triangles.json | 245 |
| witting_pg32_alternating_form_search.json | 206 |
| witting_pg32_alternating_form_search.md | 239 |
| witting_pg32_augmented_lines_analysis.json | 259 |
| witting_pg32_augmented_lines_analysis.md | 257 |
| witting_pg32_config_aut.json | 249 |
| witting_pg32_config_aut.md | 239 |
| witting_pg32_config_invariants.json | 433 |
| witting_pg32_config_invariants.md | 357 |
| witting_pg32_fiber_analysis.json | 354 |
| witting_pg32_fiber_analysis.md | 286 |
| witting_pg32_fiber_graphs.json | 1725 |
| witting_pg32_fiber_graphs.md | 783 |
| witting_pg32_full_fiber_counts.json | 1179 |
| witting_pg32_full_fiber_counts.md | 590 |
| witting_pg32_hit_lines_analysis.json | 210 |
| witting_pg32_hit_lines_analysis.md | 194 |
| witting_pg32_hit_lines_spread_search.json | 77 |
| witting_pg32_hit_lines_spread_search.md | 121 |
| witting_pg32_incidence_relation_search.json | 269 |
| witting_pg32_incidence_relation_search.md | 252 |
| witting_pg32_line_orbit_intersections.json | 1516 |
| witting_pg32_line_orbit_intersections.md | 337 |
| witting_pg32_line_orbit_point_composition.json | 456 |
| witting_pg32_line_orbit_point_composition.md | 283 |
| witting_pg32_line_orbit_structure.json | 798 |
| witting_pg32_line_orbit_structure.md | 237 |
| witting_pg32_line_relation.json | 375 |
| witting_pg32_line_relation.md | 355 |
| witting_pg32_line_space_plucker.json | 421 |
| witting_pg32_line_space_plucker.md | 307 |
| witting_pg32_line_stabilizer.json | 211 |
| witting_pg32_line_stabilizer.md | 201 |
| witting_pg32_orbit_incidence_table.json | 960 |
| witting_pg32_orbit_incidence_table.md | 290 |
| witting_pg32_plane_cover_map.json | 194 |
| witting_pg32_plane_cover_map.md | 188 |
| witting_pg32_plane_relation.json | 190 |
| witting_pg32_plane_relation.md | 192 |
| witting_pg32_polarity_search.json | 376 |
| witting_pg32_polarity_search.md | 172 |
| witting_pg32_quadratic_rule_search.json | 1533 |
| witting_pg32_quadratic_rule_search.md | 202 |
| witting_pg32_ray_invariant_product.json | 537 |
| witting_pg32_ray_invariant_product.md | 405 |
| witting_pg32_ray_line_image.json | 193 |
| witting_pg32_ray_line_image.md | 227 |
| witting_pg32_ray_rule_analysis.json | 1770 |
| witting_pg32_ray_rule_analysis.md | 910 |
| witting_pg32_ray_trace.json | 419 |
| witting_pg32_ray_trace.md | 345 |
| witting_pg32_relation_search.json | 213 |
| witting_pg32_relation_search.md | 222 |
| witting_pg32_tetrahedral_rays.json | 3086 |
| witting_pg32_tetrahedral_rays.md | 339 |
| witting_pg32_weight_orbit_analysis.json | 959 |
| witting_pg32_weight_orbit_analysis.md | 487 |
| witting_phase_cubic_formula_search.json | 2669 |
| witting_phase_formula_search.json | 690 |
| witting_phase_law_full_aut.json | 5445 |
| witting_phase_law_invariance.json | 184 |
| witting_phase_law_monomial_subgroup.json | 101 |
| witting_phase_orbit_invariance.json | 482 |
| witting_phase_quadratic_formula_search.json | 1487 |
| witting_phase_symplectic_mapped.json | 791 |
| witting_ray_overlap_structure.json | 81 |
| witting_trace_map_pg32.json | 289 |
| witting_trace_map_pg32.md | 265 |
| witting_trace_map_pg32_full.json | 504 |
| witting_trace_map_pg32_full.md | 439 |
| witting_triangle_cocycle.json | 182 |
| witting_triangle_family_phase.json | 2371 |
| witting_triangle_phase_orbits.json | 327 |
| witting_triangle_phase_word.json | 339 |
| witting_unitary_grid_anneal.json | 2675 |
| witting_unitary_grid_score_search.json | 1176 |
| witting_w33_line_tetrahedron_analysis.json | 913 |
| witting_w33_line_tetrahedron_analysis.md | 257 |
| witting_w33_line_trace_tetra_analysis.json | 22533 |
| witting_w33_line_trace_tetra_analysis.md | 560 |
| witting_w33_tetra_subgraph.json | 796 |
| witting_w33_tetra_subgraph.md | 169 |
| z3_phase_linear_analysis.json | 1564 |
| z3_phase_linear_search.json | 28363 |
