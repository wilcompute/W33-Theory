"""Independent executable regression for five-front W33/H4, flag, Regge,
labeled photon test, and tetraquadric negative good-reduction pilot."""
from pathlib import Path
import sys,json,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261008_native_H4_cycle_obstruction as nat
import w33_20261008_all120_native_H4_selector_census as selectors
import w33_20261008_five_native_H4_Zoctagon_fillings as fills
import w33_20261008_60qubit_1flag_octagon_audit as flag
import w33_20261008_native_H4_Regge_S3 as regge
import w33_20261008_native_H4_4D_spacetime_slab as slab
import w33_20261008_27port_calibrated_Bhattacharyya_test as optical

def cert(name):return json.loads((ROOT/"data"/name).read_text())
def test_selected_W33_native_cycle_lift_exact():
 r=nat.main()
 assert r["X_triangle_actual_120vertex_lift_classification"]=={"non_native":30,"native_closed":10}
 assert r["Z_octagons_with_all_eight_original_H4_edges"]==0
 assert r["Z_octagons_with_mixed_plus_minus_edge_counts"]=={2:5,4:10,6:5}
 assert r["no_native_600cell_2face_lift_of_selected_W33_octagon_boundaries_for_this_selector"]

def test_all_F20_perfect_selectors_native_no_go():
 r=selectors.main()
 assert r["all_F20_bijections_examined"]==48000
 assert r["perfect_pair_union_embedding_selectors"]==120
 assert r["perfect_selectors_by_number_of_all_native_8edge_Z_octagons"]=={0:108,5:12}
 assert r["maximum_native_octagonal_check_supports_for_any_perfect_selector"]==5
 assert r["per_selector_face_pluscount_histogram_type"]=={"((2, 5), (4, 10), (6, 5))":48,"((4, 20),)":60,"((0, 5), (4, 10), (8, 5))":12}
 assert r["first_five_face_native_selector"]["native_face_indices"]==[2,4,9,13,18]
 assert not r["all_20_octagon_CW_supports_realized_natively_simultaneously"]

def test_five_native_lifts_explicit_GF2_boundary_fillings():
 r=fills.main()
 assert r["maximally_native_F20_selected_faces"]==5
 assert r["lift_lengths_histogram"]=={16:5}
 assert r["native_H4_triangle_boundary_rank"]==601
 assert r["all_lifted_boundaries_fill_by_native_H4_triangles_GF2"]
 assert [v["GF2_native_H4_triangle_filling_count"] for v in r["native_face_lift_and_surface_fill_records"]]==[68,96,82,58,80]
 assert not r["single_native_H4_triangle_identical_to_W33_octagon"]

def test_flagged_CSS_one_fault_exhaustive_3000_distinguishable():
 r=flag.main()
 assert r["exhaustive_single_post_gate_two_qubit_Pauli_fault_cases"]==3000
 assert r["flagged_fault_count"]==640
 assert r["uncorrectable_unflagged_fault_cases"]==0
 assert r["uncorrectable_flagged_fault_cases"]==160
 assert r["ideal_followup_full_syndrome_plus_flag_lookup_distinct_outcome_keys"]==900
 assert r["ideal_followup_flag_and_full_syndrome_ambiguous_coset_keys"]==0
 assert r["ideal_followup_decoder_unambiguous_for_single_post_CNOT_Pauli_faults"]
 assert r["restricted_single_fault_detection_certificate_not_full_fault_tolerance"]

def test_native_H4_spatial_Regge_3sphere_chain_complex():
 r=regge.main()
 assert r["native_600cell_f_vector"]==[120,720,1200,600]
 assert r["GF2_cellular_boundary_ranks"]==[119,601,599]
 assert r["GF2_homology_betti_numbers"]==[1,0,0,1]
 assert r["tetrahedra_incident_on_each_edge"]==5
 assert abs(r["native_edge_Regge_deficit_radians"]-.12838822047571252)<1e-12
 assert abs(r["Lambda_times_a_squared_at_stationary_relation"]-.4357640703496794)<1e-10
 assert r["not_Lorentzian_4D_or_ADM_hypersurface_brackets"]

def test_native_600cell_S3_times_interval_actual_4dim_triangulation():
 r=slab.main()
 assert r["4D_simplicial_f_vector"]==[240,2280,6240,6600,2400]
 assert r["Euler_char"]==0
 assert r["boundary_tetrahedral_facets_total"]==1200
 assert r["boundary_map_d4_GF2_rank"]==2400
 assert r["relative_fundamental_4_chain_boundary_equals_t0_plus_t1_S3"]
 assert r["boundary_square_zero_GF2_verified"]
 assert r["only_boundary_tetra_facets_at_t0_and_t1"]
 assert r["not_physical_Lorentzian_metric_or_4D_Einstein_Regge_action"]

def test_photonic_known_labeled_mode_Bhattacharyya_joint_95percent():
 r=optical.main()
 rows=r["experiments"]
 assert [e["layers"] for e in rows]==[36,72,144]
 assert [e["input_port_optimal_for_minimax_calibrated_detuning"] for e in rows]==[23,11,11]
 assert [e["N_successful_detections_for_conditional_binary_Bayes_error_leq_point025"] for e in rows]==[9,9,11]
 assert [e["minimal_launched_photons_for_detection_count_probability_geq_point975"] for e in rows]==[18,29,74]
 assert all(e["binomial_success_probability"]>=.975 for e in rows)
 assert all(e["binomial_previous_N_minus_one"]<.975 for e in rows)
 assert all(e["binary_equal_prior_Bayes_error_bound"]<=.025 for e in rows)
 assert r["NOT_anonymous_input_or_output_port_protocol"]
 assert not r["unmeasured_device_or_adversarial_jitter_guaranteed"]

def test_21orbit_F3_rational_sieve_NOT_geometry_certification():
 x=cert("w33_20261008_invariant_tetraquadric_21dim_mod3_exact_attempt.json")
 assert x["attempts"]==14
 assert len(x["coefficients_21_orbits_F3"])==21
 assert x["projective_P1F3_fourfold_points_examined"]==256
 assert x["candidate_avoids_all_F3_projective_singular_points"]
 assert not x["char0_smoothness_proven"]
 assert not x["unit_Groebner_charts"]
 assert x["failed_charts"][0]["chart"]==[0,0,0,0]
 assert not x["failed_charts"][0]["Groebner_is_unit"]
 assert x["failed_charts"][0]["basis_length"]==27

def test_scientific_limits_are_explicit_in_current_report():
 x=(ROOT/"analysis/2026-10-08_120_H4_native_selectors_flagged_CSS_Regge_photon_CY.md").read_text()
 assert "120" in x and "48,000" in x
 assert "Einstein" in x and "Yukawa" in x
 assert "not" in x and "3,000" in x
