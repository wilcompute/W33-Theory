"""Five-front current research regression: colored F20 cover, full CSS
single-fault observed decoder, Lorentzian all-tau Gram, robust 27port
photon, and exact smooth free CY quotient + physical charge obstruction.
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261008_F20_chiral_Z2square_240cover as cover
import w33_20261008_240sheet_chiral_CW_octagon_homology as cw
import w33_20261008_240sheet_CSS_hex_oct_manifold_no_go as fullcw
import w33_20261008_full_CSS_13layer_singlefault as css
import w33_20261008_H4_4D_Lorentzian_Gram_certificate as lorentz
import w33_20261008_27port_dark_TV_robust_budget as photon
import w33_20261008_explicit_Klein_CY_smooth_proof as cy
import w33_20261008_Klein_CY_Chern_bundle_parity as bundle

def test_all_octagons_close_on_chiral_F20_equivariant_connected_240cover():
 x=cover.main()
 assert x["formal_chiral_Z2square_cover_vertices"]==240
 assert x["formal_cover_edges"]==480
 assert x["connected_component_sizes"]==[240]
 assert x["all_W33_20_Z_checks_lift_as_closed_eight_cycles_on_all_four_sheets"]
 assert x["all_40_W33_star_triangles_lift_as_length_six_not_length_three"]
 assert x["X_star_triangle_voltages_hist"]=={1:20,2:20}
 assert x["F20_C5_generator_preserves_voltage_basis"]
 assert x["F20_C4_generator_swaps_voltage_bits"]
 assert x["both_generators_act_as_true_240vertex_graph_automorphisms"]
 assert x["F20_relation_s_r_sinv_equals_r_squared_verified_on_240_vertices"]
 assert x["not_native_600cell_120vertex_cover"]

def test_chiral_voltage_octagon_CW_boundary_and_homology_nonmanifold():
 x=cw.main()
 assert x["CW_f_vector"]==[240,480,80]
 assert x["GF2_boundary_ranks"]==[239,78]
 assert x["GF2_homology_betti_numbers"]==[1,163,2]
 assert x["CW_edges_incidence_number_of_lifted_octagons_hist"]=={0:160,2:320}
 assert x["all_80_lifted_octagons_closed_8_edge_cycles"]
 assert x["boundary_square_zero"]
 assert not x["closed_two_manifold_CW_complex"]

def test_full_X_Z_160face_CW_graph_has_strict_manifold_incidence_obstruction():
 x=fullcw.main()
 assert x["CW_f_vector"]==[240,480,160]
 assert x["star_hexagon_lifts"]==80
 assert x["Z_octagon_lifts"]==80
 assert x["each_cover_edge_occurs_in_exactly_one_X_star_hexagon"]
 assert x["union_hexagon_plus_octagon_edge_face_incidence_hist"]=={1:160,3:320}
 assert x["GF2_boundary_ranks"]==[239,158]
 assert x["GF2_homology_betti_numbers"]==[1,83,2]
 assert not x["closed_two_manifold_possible_with_these_full_CSS_face_attachments"]

def test_7641_expanded_fullround_single_Pauli_fault_models():
 x=css.main()
 assert x["global_entangling_layers"]==13
 assert x["total_CNOTs"]==320
 assert x["single_fault_cases_including_no_fault"]==7641
 assert x["fault_cases_by_type"]=={"no_fault":1,"gate":4800,"prep":240,"idle":2520,"readout":80}
 assert x["ambiguous_joint_observation_stabilizer_coset_keys"]==0
 assert x["unique_joint_syndrome_flag_future_ideal_syndrome_keys"]==2039
 assert x["all_cases_correctable_given_perfect_followup_full_X_and_Z_syndromes"]
 assert x["no_finite_noise_threshold_or_true_noisy_detector_graph"]

def test_all_positive_tau_non_degenerate_2400_Lorentzian_4simplices():
 x=lorentz.main()
 assert x["4simplex_count"]==2400
 assert x["all_4simplices_Lorentzian_for_every_positive_tau_over_a"]
 assert x["exact_4simplex_Lorentzian_Gram_determinant_polynomials"]=={
  "1":"-(8*u + 3)/16","2":"-(12*u + 7)/16",
  "3":"-(12*u + 7)/16","4":"-(8*u + 3)/16"}
 assert x["hinge_spacetime_type_hist"]=={"(3, 0)":1200,"(0, 3)":1200,"(1, 2)":1920,"(2, 1)":1920}
 assert x["no_regge_deficit_angles_or_Einstein_equations_derived"]

def test_36_labeled_photon_noise_calibration_modelled_budgets():
 x=photon.main()
 assert x["number_of_model_conditional_scenarios"]==36
 def find(l,b,e):
  return next(r for r in x["rows"] if r["optical_layers"]==l and
     r["uniform_dark_background_fraction"]==b and r["maximum_l1_model_to_true_per_hypothesis"]==e)
 assert find(36,0.,0.)["joint_95percent_minimum_source_launches"]==18
 assert find(36,.05,.01)["joint_95percent_minimum_source_launches"]==38
 assert find(36,.1,.01)["joint_95percent_minimum_source_launches"]==44
 assert all(.5*r["worst_Bhattacharyya_upper_bound_with_bounded_errors"]**r["successful_photon_detections_required"]<=.025+1e-14 for r in x["rows"])
 assert x["not_anonymous_port_or_any_real_device_measurement"]

def test_exact_char0_smooth_Klein_free_CY_hodge_4_20():
 x=cy.main()
 assert x["complex_geometric_smoothness_proven_by_three_case_derivative_elimination"]
 assert x["all_three_products_vanish_derivatives_have_two_independent_nonzero_coordinates"]
 assert x["exactly_one_product_zero_requires_forbidden_finite_group_fixed_value"]
 assert x["none_zero_singular_parameter_b_candidates_for_a2"]==["-2","-2/3","2/3","2"]
 assert x["all_48_ambient_fixed_points_avoided"]
 assert x["Klein_group_canonical_residue_form_preserved"]
 assert x["original_euler_char"]==-128
 assert x["free_quotient_euler_char"]==-32
 assert x["free_quotient_hodge_numbers"]==[4,20]
 assert x["physical_heterotic_bundle_HYM_FI_anomalies_Yukawa_not_constructed"]

def test_CY_quotient_gauge_holonomy_Z3_Z6_and_linebundle_parity_no_go():
 x=bundle.main()
 assert x["c2TX_pairing_with_each_ambient_Hi"]==[24]*4
 assert set(x["triple_intersections_Hi_Hj_Hk_distinct"].values())=={2}
 assert x["all_flat_Abelian_U1_holonomies_have_order_dividing_2"]
 assert x["flat_pi1_Wilson_line_sole_source_of_Z3_or_Z6"] is False
 assert x["O_1_single_P1_factor_G_linearizable"] is False
 assert x["O_2_single_P1_factor_G_linearizable"]
 assert x["ambient_line_bundle_multidegree_G_linearization_criterion"]=="sum_i n_i even"
 assert x["no_FI_anomaly_free_nonAbelian_bundle_or_canonically_normalized_Yukawa_derived"]
