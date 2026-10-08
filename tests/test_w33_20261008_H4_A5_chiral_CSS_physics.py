"""Independent regression controls: true H4 Clifford A5 chiral classes, CSS faults,
solvable thermal spectrum, photon drift and complex singularity witness."""
from pathlib import Path
import sys,json,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261008_H4_60_antipodal_incidence_obstruction as incidence
import w33_20261008_H4_A5_chiral_Cayley_pair as chiral
import w33_20261008_H4_A5_golden_spectral_fusion as spectral
import w33_20261008_60qubit_measurement_hook_audit as hooks
import w33_20261008_20apt_exact_thermal_spectrum as thermal
import w33_20261008_Klein_tetraquadric_pencil_nogo as tetra
def saved(filename):
 return json.loads((ROOT/"data"/filename).read_text())

def test_true_h4_graph_differs_from_w33_edge_line_graph():
 x=saved("w33_20261008_H4_60_antipodal_incidence_obstruction.json")
 h=x["H4_600cell_antipodal_graph"];w=x["W33_60_edge_qubit_line_graph"]
 assert (h["vertices"],h["edges"],h["degree_histogram"],h["triangles"])==(60,360,{"12":60},600)
 assert (w["vertices"],w["edges"],w["degree_histogram"],w["triangles"])==(60,120,{"4":60},40)
 assert not x["incidence_preserving_60vertex_graph_bijection_exists"]

def test_clifford_A5_all_left_and_right_translations_are_actual_H4_automorphisms():
 x=saved("w33_20261008_H4_Clifford_A5_Cayley_test.json")
 assert x["left_translations_edges_preserved_hist"]=={"360":60}
 assert x["right_translations_edges_preserved_hist"]=={"360":60}
 assert x["is_left_A5_Cayley"] and x["is_right_A5_Cayley"]

def test_H4_exact_order5_split_and_outer_C4_exchange():
 x=chiral.main()
 assert x["H4_neighbors_of_identity_are_A5_5cycles"]
 assert x["H4_adj_exactly_normal_Cayley_graph_A5_class_5a"]
 assert x["other_5cycle_class_size"]==12
 assert x["S6_normalizer_of_Clifford_A5_size"]==120
 assert x["S6_inner_normalizers_preserve_chiral_H4_graph"]==60
 assert x["S6_outer_normalizers_exchange_two_H4_graph_relations"]==60
 assert x["order4_witness_conjugates_order5_r_to_r_squared"]
 assert x["order4_outer_maps_original_360_edges_to_disjoint_mirror_360_edges"]
 assert not x["not_physical_parity_or_spacetime_chirality_derived"]==False

def test_golden_irrationality_cancels_under_chiral_pair_fusion():
 x=spectral.main()
 assert x["golden_irrationality_cancels_in_chiral_pair"]
 assert x["union_degree"]==24
 assert x["triangle_count_each_chiral"]==600
 assert max(x["independent_numeric_spectral_max_error"])<1e-12
 assert x["spectrum_union_chirality_fused"]=="24^1, 4^18, (-6)^16, 0^25"

def test_Konig_Edge_Colored_11_CNOT_layers_and_20_hook_risk():
 x=hooks.main()
 assert x["X_matching_layers"]==3 and x["Z_matching_layers"]==8
 assert x["total_CNOTs"]==280
 assert x["single_Z_ancilla_fault_effective_weight_histogram"]=={0:40,1:40,2:40,3:40,4:20}
 assert x["single_Z_ancilla_faults_effective_weight4_count"]==20
 assert x["single_Z_ancilla_fault_weight4_witness"]["exact_minimum_coset_weight_up_to_4"]==4
 assert x["Z_ancilla_hooks_exceed_unique_Z_correction_radius_3"]
 assert not x["fault_tolerant_syndrome_circuit_proven"]

def test_hamiltonian_full_2power60_spectrum_and_finite_beta_Z():
 x=thermal.spectrum()
 assert x["Hilbert_dimension_exact"]==2**60
 assert x["energy_levels"]==31
 assert x["first_excited_degeneracy"]==3880
 assert x["gap"]==4
 assert x["all_spectrum_accounted_for"]
 assert len(x["temperature_points"])==5
 assert x["finite_system_free_energy_analytic_for_all_finite_real_beta"]

def test_photon_correlated_miscalibration_all_21_scenarios():
 x=saved("w33_20261008_27port_correlated_coherent_drift.json")
 assert len(x["grid"])==21
 assert x["shared_phase_offset_same_for_each_gate_and_repetition"]
 at={(r["CNOTlike_2mode_optical_layers"],r["systematic_angle_offset_per_active_2mode_coupler_rad"]):r for r in x["grid"]}
 assert abs(at[72,0]["ideal_source_anonymous_min_supnorm_separation"]-.227995)<1e-5
 assert .208<at[72,-.002]["nominal_classifier_separation_lower_bound_for_this_synthetic_miscalibration"]<.212
 assert at[72,-.002]["expected_launches_at_eta_point99_per_layer"]>at[72,0]["expected_launches_at_eta_point99_per_layer"]
 assert x["no_real_photon_device_calibration"]

def test_Klein_four_free_action_does_not_imply_smooth_CY():
 x=tetra.main()
 assert x["b0_family_singular_for_all_a"]
 assert x["a2_b0_avoids_all_48_ambient_fixed_points"]
 assert x["a2_b0_geometrically_singular_over_Qi"]
 assert x["exact_global_singular_witness_P1_coordinates"]==["i","-i","1","-1"]
 assert x["global_defining_equation_and_all_four_affine_partials_zero_at_witness"]
 assert not x["a2_b3_smooth_over_C_proven"]
 assert not x["normalized_Yukawa_or_anomaly_free_UV_vacuum_constructed"]

def test_prior_W33_F20_and_Z6_boundaries_preserved():
 x=saved("w33_20261008_20apt_Hamiltonian_F20_Z6_guard.json")
 assert x["full_F20_invariant_flat_Z6_order_six_characters"]==0
 assert x["proton_hexality_cannot_be_entirely_F20_invariant_flat_Z6_holonomy"]
 old=saved("w33_20261008_F20_A5_antipodal_60_bijection.json")
 assert old["F20_equivariant_bijection_verified_for_all_1200_edge_group_pairs"]
 assert not old["canonical_geometry_proven"]

def test_repo_docs_explicit_positive_negative_boundaries():
 text=(ROOT/"analysis/2026-10-08_H4_A5_chiral_golden_CSS_tetraquadric_seven_fronts.md").read_text()
 assert "Cayley" in text
 assert "hook" in text.lower()
 assert "singular" in text.lower()
 assert "[[60,2,6]]" in text
 assert "180" in text
