"""Recompute eight-front TOE claims from generators rather than trusting
frozen JSON: genus53 F20 surface, exact spherical quotient, shared CY
Fourier duality, poly-stable index3 bundle candidate, native-locality
invariance obstruction, continuous photon bounds, CSS limited diagnostics.
"""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261008_chiral_face_checkerboard_repair as repair
import w33_20261008_chiral_surface_orientability_F20 as surface
import w33_20261008_genus53_F20_orbifold as orbifold
import w33_20261008_chiral_CY_duality_character_SWAP as duality
import w33_20261008_CY_SU5_linebundle_index3_search as bundle
import w33_20261008_chiral_odd_edge_H1_F20_isometry as parity
import w33_20261008_F20_chiral_locality_kinetic as kinetic
import w33_20261008_photon_continuous_detuning_guard as photon
import w33_20261008_CSS_repeated_measurement_null_control as majority
import w33_20261008_CSS_twofault_check as qec

def test_checkerboard_and_decagon_exact_2manifold():
 x=repair.main()
 assert x["octagon_face_dual_graph_bipartite"]
 assert x["octagon_dual_components"]==[40,40]
 assert x["new_cycle_face_count"]==16
 assert x["new_cycle_face_sizes"]==[10]*16
 assert x["candidate_closed_surface_f_vector"]==[240,480,136]
 assert x["candidate_Euler_char"]==-104
 assert x["vertex_links_simple_closed_circles_count"]==240
 assert x["CW_face_selective_manifold_repair_proved"]

def test_all_F20_orientation_and_four_53_or_106_selections():
 x=surface.main()
 assert x["complete_closed_connected_surface_f_vector"]==[240,480,136]
 assert x["F20_full_action_preserved_by_some_selection"]
 assert [v["orientable"] for v in x["selection_results"]]==[True,False,False,True]
 assert all(v["preserving_subgroup_order"]==20 for v in x["selection_results"])
 assert all(v["H1_over_F2_dimension"]==106 for v in x["selection_results"])
 assert all(v["H2_over_F2_dimension"]==1 for v in x["selection_results"])

def test_53handle_to_F20_spherical_orbifold_all_branchpoints():
 x=orbifold.main()
 assert x["F20_preserves_orientation"]
 assert x["orientation_reversing_group_elements"]==0
 assert x["quotient_cell_orbit_f_vector"]==[12,24,14]
 assert x["quotient_cell_Euler_characteristic"]==2
 assert x["underlying_orientable_quotient_surface_genus"]==0
 assert x["elliptic_branch_orders"]==[2,2,4,4,4,4,5,5,5,5]
 assert x["face_orbit_sizes_by_polygon_n"]=={"6":[20]*4,"8":[5,5,5,5,10,10],"10":[4]*4}

def test_CY_vacuum_exchange_is_duality_not_same_fiber_symmetry():
 x=duality.main()
 assert x["certified_free_polynomial_a2b3_maps_to_a3b2_distinct"]
 assert x["uniform_Hadamard_as_C4_chiral_swap_on_same_smooth_free_X23"] is False
 assert x["a_equal_b_causes_original_gh_fixedpoint_locus_on_hypersurface"]
 assert x["SWAP_intertwines_deck_char_Fourier_transform"]
 assert x["SWAP_conjugates_both_X_and_Z_logical_Paulis_by_qubit_exchange"]

def test_explicit_rank5_CY_index_three_topological_bundle():
 x=bundle.main();v=x["chosen"]
 assert v["line_bundles_multidegree"]==[(-1,1,0,0),(0,-2,1,1),(0,1,-2,1),(0,-1,1,0),(1,1,0,-2)]
 assert v["upstairs_Dirac_index"]==-12
 assert v["downstairs_net_index_if_equivariant_free_quotient"]==-3
 assert v["Bianchi_c2TX_minus_c2V_nef_pairings"]==[6,18,14,14]
 assert v["c1V_zero"] and v["each_slope_zero_at_equal_t"]
 assert v["each_line_bundle_Klein_linearization_parity_even"]
 assert x["actual_anomaly_cancellation_and_physical_Z6_not_proved"]

def test_native_H4_chirality_has_no_full_F20_kinetic_symmetry():
 x=kinetic.main()
 assert x["plus_native_600cell_edges_in_selected_W33_support"]==60
 assert x["minus_nonnative_mirror_edges_in_selected_W33_support"]==60
 assert x["F20_order4_exchanges_native_plus_and_nonnative_minus"]
 assert x["F20_invariant_two_class_couplings_iff_equal_a_b"]
 assert x["symmetric_chiral_Laplacian_smallest_eigenvalue"]>-1e-9
 assert x["this_F20_symmetric_operator_not_native_600cell_nearest_neighbor_Laplacian"]

def test_all_edges_GF2_H1_obstruction_retracted_and_repaired():
 x=parity.main()
 assert x["full_CW_two_boundary_rank"]==158
 assert x["all_edges_one_chain_is_nontrivial_H1_class"] is False
 assert x["all_edges_boundary_of_sum_80_hexagon_faces"]
 assert x["all_edges_one_chain_reduced_witness_hamming_weight"]==0
 assert x["repair_requires_integer_incidence_adjustment_not_mod2_homology"]

def test_optics_entire_continuous_interval_not_just_discrete_grid():
 x=photon.main()
 assert x["number_of_scenarios"]==27
 def find(b,e):
  return next(q for q in x["rows"] if q["layers"]==36 and q["uniform_noise_fraction"]==b and q["independently_adversarial_l1_error"]==e)
 assert find(0,0)["minimum_launched_photons_for_joint_95percent"]==62
 assert find(.05,.01)["minimum_launched_photons_for_joint_95percent"]==111
 assert find(.10,.01)["minimum_launched_photons_for_joint_95percent"]==155
 assert x["finite_grid_baseline_cannot_be_claimed_continuous_without_interpolation_guard"]
 assert x["not_actual_physical_device_or_unknown_source"]

def test_static_80check_majority_readout_null_control():
 x=majority.main()
 assert x["readout_only_scenarios"]==24
 def prob(r):return next(q["at_least_one_of_80_measured_bits_wrong_probability"] for q in x["rows"] if q["independent_readout_flip_probability"]==.01 and q["odd_readout_rounds"]==r)
 assert .55<prob(1)<.56 and .023<prob(3)<.024
 assert .0007<prob(5)<.0009 and .00002<prob(7)<.00003
 assert not x["complete_circuit_level_fault_tolerance_or_threshold"]

def test_css_twofault_search_does_not_overclaim_exhaustivity():
 x=qec.main()
 assert x["single_fault_records"]==7641
 assert x["unique_single_records"]==2039
 assert x["distinct_single_fault_signature_pairs_examined"]==250000
 assert x["ambiguity"] is None
 assert x["not_exhaustive_two_fault_model"]
 assert x["distinct_physical_gate_locations_NOT_verified_for_pairs"]

def test_eight_front_report_preserves_physics_and_novelty_limits():
 x=(ROOT/"analysis/2026-10-08_eight_front_TOE_genus53_CY_index3_duality.md").read_text(encoding="utf-8")
 assert "Pass11767" in x and "Pass11768" in x
 assert "53" in x and "106" in x and "250,000" in x
 assert "not" in x and "anomaly" in x and "Yukawa" in x
