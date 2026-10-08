"""Cross-program tests: W33 60-edge CSS, BC 600-cell 30-ring torus,
A5 Clifford torsor, F20 modular S, decoder, routing, gauge, photon."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261008_BC_ring_CSS_comparison as bc
import w33_20261008_F20_A5_600cell_antipodal_bridge as a5
import w33_20261008_20apt_decoder_routing as dec
import w33_20261008_20apt_local_SWAP_schedule as local
import w33_20261008_20apt_Hamiltonian_Z6 as model
import w33_20261008_20apt_integral_modular_S as modS
import w33_20261008_photon_calibrated_coupler_mc as photon

def saved(name):return json.loads((ROOT/"data"/name).read_text())

def test_BC_ring_is_distinct_exact_CSS():
 x=bc.css()
 assert x["V_E_F"]==[30,90,60]
 assert (x["n"],x["k"],x["X_distance"],x["Z_distance"],x["CSS_distance"])==(90,2,6,3,3)
 assert len(x["Z_witness_edges"])==3
 assert len(x["X_witness_boundary_edges"])==6

def test_BC_symmetry_and_face_adjacency_no_go():
 x=saved("w33_20261008_BC_ring_CSS_vs_apartment.json")
 assert x["BC_torus_1_skeleton_aut_order"]==60
 assert not x["BC_full_automorphism_has_order_four"]
 assert x["F20_order4_elements_in_W33"]==10
 assert x["no_full_F20_action_as_BC_ring_geometric_automorphisms"]
 assert (x["BC_face_dual_graph_degree"],x["W33_edge_line_graph_degree"])==(3,4)
 assert not x["BC_face_dual_and_W33_edge_line_graph_isomorphic"]

def test_F20_A5_60_address_equivariant_bridge():
 x=saved("w33_20261008_F20_A5_antipodal_60_bijection.json")
 assert x["W33_F20_edge_orbit_sizes"]==[20,20,20]
 assert x["S5_coset_F20_orbit_sizes"]==[20,20,20]
 assert x["F20_equivariant_bijection_verified_for_all_1200_edge_group_pairs"]
 assert len(set(x["W33_edge_index_to_S5_coset_index"]))==60
 assert x["abstract_A5_order_hist"]=={"1":1,"2":15,"3":20,"5":24}
 assert x["600cell_Clifford_A5_order_hist_from_actual_repo"]==x["abstract_A5_order_hist"]
 assert x["canonical_geometry_proven"] is False

def test_decoder_all_t2_Pauli_and_t3_Z():
 x=dec.main()
 assert x["Z_errors_exhaustively_corrected"]==36051
 assert x["X_errors_exhaustively_corrected"]==1831
 assert x["Z_distinct_syndromes"]==36051
 assert x["X_distinct_syndromes"]==1591
 assert x["X_degenerate_same_syndrome_distinct_error_counts"]=={2:240}
 assert x["no_circuit_level_fault_tolerance_or_threshold_proven"]

def test_60_local_SWAP_schedule_actually_routes_tokens():
 x=local.main()
 assert x["verified_physical_permutation_exact"]
 assert x["F20_order4_physical_qubit_4cycles"] if "F20_order4_physical_qubit_4cycles" in x else x["logical_swap_as_15_disjoint_4cycles"]
 assert x["nearest_neighbor_SWAP_count_lower_bound"]==98
 assert x["constructive_nearest_neighbor_SWAP_upper_bound"]==259
 assert x["parallel_disjoint_SWAPS_depth_upper_bound"]==103
 assert len(x["explicit_local_SWAP_gates"])==259
 assert x["not_optimized_or_fault_tolerant"]

def test_F20_invariant_binary_torus_Hamiltonian_and_Z6_obstruction():
 x=model.main()
 assert x["Pauli_commutators_zero"]
 assert x["ground_energy_exact"]==-60 and x["ground_space_dimension_exact"]==4
 assert x["energy_gap_exact"]==4
 assert x["Hamiltonian_invariant_under_all_20_F20_permutations"]
 assert x["full_F20_invariant_flat_Z6_Wilson_line_characters"]==[[0,0],[3,3]]
 assert x["full_F20_invariant_flat_Z6_order_six_characters"]==0
 assert not x["relativistic_or_Einstein_dynamics_derived"]

def test_Gaussian_torus_integral_modular_S_in_three_residue_fields():
 x=saved("w33_20261008_20apt_integral_C4_modular_S.json")
 M={v["p"]:v for v in x["field_actions"]}
 assert M[2]["matrix_order4_action"]==[[0,1],[1,0]]
 assert M[3]["matrix_order4_action"]==[[0,2],[1,0]]
 assert M[5]["matrix_order4_action"]==[[0,4],[1,0]]
 assert M[3]["matrix_squared"]==[[2,0],[0,2]]
 assert M[5]["matrix_squared"]==[[4,0],[0,4]]
 assert x["mod2_logical_SWAP_is_reduction_of_modular_S"]
 assert x["F20_on_integral_H1_image"]=="C4"
 assert x["order4_squared_on_integral_H1"]=="-Identity"

def test_27_port_mc_true_ideal_margins_and_sampled_noise_boundary():
 x=saved("w33_20261008_photon_calibrated_coupler_mc.json")
 assert x["samples_per_scenario"]==12
 assert len(x["scenarios"])==12
 ideal={r["stages"]:r for r in x["scenarios"] if r["phase_noise_std_rad_per_coupler"]==0}
 assert abs(ideal[72]["nominal_sorted_min_margin"]-.2279950020)<1e-7
 assert all(r["sampled_min_calibrated_margin"]>0 for r in x["scenarios"])
 assert all(len(r["calibration_samples"])==12 for r in x["scenarios"])
 assert x["no_physical_device_measurements"]
 assert x["no_worst_case_guarantee_from_monte_carlo"]

def test_sparse_tetraquadric_gaussian_sieve_is_not_a_smoothness_proof():
 x=saved("w33_20261008_tetraquadric_Gaussian_singular_sieve.json")
 assert x["total_examined"]==1296
 assert x["hypersurface_points_in_sieve"]==576
 assert not x["particular_sparse_polynomial_proven_singular_over_Qi"]
 assert x["no_singular_witness_not_smoothness_proof"]

def test_previous_parity_and_tetraquadric_physical_guards():
 old=saved("w33_20261008_F20_binary_proton_hexality_no_go.json")
 assert not old["physical_P6_constructed"]
 tetra=saved("w33_20261008_tetraquadric_sparse_good_reduction.json")
 assert tetra["fixed_point_audit"]["fixed_points_checked"]==48
 assert not tetra["complex_smoothness_proven"]
