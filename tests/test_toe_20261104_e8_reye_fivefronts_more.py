"""Exact and negative controls: E8/2E8, 25 Reye packets, quantum history,
compatibility-aware contextuality, Regge, and A4² -> two swapped E8 glues.
"""
import importlib.util,sys,math
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
for p in (ROOT,ROOT/"analysis"):
    if str(p) not in sys.path:sys.path.insert(0,str(p))
def source(name,rel):
    sp=importlib.util.spec_from_file_location(name,ROOT/rel)
    m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
    return m
@pytest.fixture(scope="module")
def e8():
    return source("e8_qF4","analysis/toe_20261104_e8_mod2_pg34_refinement.py").write()
@pytest.fixture(scope="module")
def orbits():
    return source("packet25","analysis/toe_20261104_h4_reye_25_orbits.py").main()
@pytest.fixture(scope="module")
def coherent():
    return source("coherent4","analysis/toe_20261104_coherent_witting_history_compression.py").run()
@pytest.fixture(scope="module")
def hardware():
    return source("compat","analysis/toe_20261104_contextuality_compatibility_detection_budget.py").run()
@pytest.fixture(scope="module")
def gravity():
    return source("regge","analysis/toe_20261104_regge_4simplex_1to5_action.py").main()
@pytest.fixture(scope="module")
def frame():
    return source("frame25","analysis/toe_20261104_reye_axis_frame_fusion_kernel.py").main()
@pytest.fixture(scope="module")
def glue():
    return source("e8glue","analysis/toe_20261104_reye_kernel_a4a4_e8_glue.py").main()

def test_e8_Cartan_quadratic_and_hermitian_orbit_counts(e8):
    assert e8["E8_Cartan_determinant"]==1
    assert e8["E8_nonzero_singular_q0"]==135
    assert e8["E8_anisotropic_q1"]==120
    assert e8["E8_order3_nonzero_orbits"]==85
    assert e8["resulting_Hermitian_GF4_projective_isotropic_points"]==45
    assert e8["resulting_Hermitian_GF4_projective_nonsingular_points"]==40
    assert len(e8["explicit_E8_hyperbolic_basis_bitmasks"])==8
    assert len(set(e8["binary_isometry_E8_to_F4_Hermitian"]))==256

def test_no_naive_e8_45point_versus_icosian_25point_equality(e8):
    assert e8["icosian_quadric25_vs_hermitian_q0_q1"]=={"q0":21,"q1":4}
    assert e8["icosian_invertible60_vs_hermitian_q0_q1"]=={"q0":24,"q1":36}
    assert e8["PGL2_left_shear_is_determinant_quadric_automorphism_but_not_qh_isometry"]
    ex=e8["qh_coordinate_example_not_invariant_under_PGL2_left_action"]
    assert ex["q_before"]!=ex["q_after"]

def test_H4_action_transitive_on_all_25_reye_packets(orbits):
    assert orbits["H4_full_order"]==14400
    assert orbits["induced_H4_permutation_group_order"]==7200
    assert orbits["point_orbit_size"]==25
    assert orbits["one_packet_stabilizer_effective"]==288
    assert orbits["all_H4_invariant_single_packet_selectors_constant"]

def test_H4_pair_and_threebody_orbits(orbits):
    assert sorted([x["orbit_size"] for x in orbits["pair_orbits"]])==[100,200]
    assert [x["orbit_size"] for x in orbits["triple_orbits"]]==[100,400,600,1200]
    assert orbits["triple_orbit_count"]==4
    assert sum(x["orbit_size"] for x in orbits["triple_orbits"])==2300
    assert [x["three_way_shared_vertices"] for x in orbits["triple_orbits"]]==[0,0,2,0]
    assert not orbits["H4_invariant_three_packet_choice_exists"]

def test_coherent_selective_9_to_4_instrument_isometry_and_limit(coherent):
    assert coherent["input_history_dimension"]==9
    assert coherent["success_output_dimension"]==4
    assert coherent["failure_subspace_dimension"]==5
    assert coherent["flagged_total_4plus5_map_isometry_exact"]
    assert coherent["quantum_map_deterministic_faithful_9_to_4_impossible_by_dimension"]
    assert abs(coherent["success_probability_maximally_mixed_history"]-4/9)<1e-12
    assert coherent["success_probability_ideal_identity_Choi"]==1

def test_coherent_history_beats_output_only_but_not_joint_Helstrom(coherent):
    assert abs(coherent["heralded_Witting_success_identity_vs_depolarizing"]-38/45)<1e-12
    assert abs(coherent["full_joint_Helstrom_success_identity_vs_depolarizing"]-17/18)<1e-12
    assert coherent["preceding_output_only_Witting_success"]==.5
    assert len(coherent["ideal_identity_outcome_probabilities"])==41
    assert len(coherent["fully_depolarized_outcome_probabilities"])==41
    assert abs(sum(coherent["ideal_identity_outcome_probabilities"])-1)<1e-9

def test_coherent_process_distinguishability_not_entanglement_witness(coherent):
    x=next(row for row in coherent["repeated_exchange_and_erasure_samples"]
        if row["exchange_count"]==14 and row["external_survival_eta"]==1)
    assert x["Choi_entanglement_negativity"]==0
    assert x["optimal_equal_prior_success_vs_fully_depolarized"]>.5

def test_hardware_onehot_parity_is_tautological_without_compatibility(hardware):
    assert hardware["ideal_single_click_four_port_context_product"]==-1
    assert hardware["context_dependent_classical_one_hot_hidden_variable_model_attains_beta9"]
    assert hardware["contextual_model_proves_no_compatibility_free_witness"]
    assert hardware["previous_independent_4_dichotomic_sign_flip_threshold_is_not_physical_single_click_noise_threshold"]

def test_hardware_cross_context_phase_drift_and_90percent_detection(hardware):
    rows=hardware["simulated_phase_and_beamsplitter_drift"]
    assert len(rows)==10
    assert all(z["avg_shared_ray_projector_infidelity"]<1e-12 for z in rows if z["sigma_angle_and_phase_rad"]==0)
    assert all(z["avg_shared_ray_projector_infidelity"]>0 for z in rows if z["sigma_angle_and_phase_rad"]>.0)
    eta=next(x for x in hardware["sample_no_click_and_trial_budget"]
        if abs(x["total_single_photon_detection_probability"]-.9)<1e-12)
    assert abs(eta["unconditional_beta_under_all_minus_no_click_assignment"]-7.2)<1e-12
    assert eta["independent_Bernoulli_5sigma_shots_per_context"]==2025
    assert abs(hardware["noncontextual_threshold_in_specific_no_click_assignment_eta_greater_than"]-8/9)<1e-12

def test_regge_explicit_4simplex_action_and_flat_vertex_gauge(gravity):
    assert gravity["new_4simplices"]==5
    assert gravity["internal_2simplices_triangle_hinges"]==10
    assert gravity["boundary_2simplices"]==10
    assert abs(gravity["flat_action_measured"]-(3*math.pi/2+4*math.pi*math.sqrt(3)/3))<1e-10
    assert gravity["flat_internal_deficit_max"]<1e-10
    assert gravity["flat_Action_gradient_norm"]<1e-10
    assert gravity["flat_action_Hessian_rank_approx"]==1
    vals=gravity["flat_action_Hessian_eigenvalues"]
    assert sum(abs(v)<1e-4 for v in vals)==4 and abs(vals[-1]-128)<.01

def test_regge_curvature_lifts_four_nulls_and_no_Lorentzian_claim(gravity):
    assert gravity["exact_4D_flat_vertex_motions_keep_action_constant"]
    assert len(gravity["off_shell_curved_normal_perturbations"])==3
    for x in gravity["off_shell_curved_normal_perturbations"]:
        assert x["four_vertex_translation_hessian_zeros_lifted"]
        assert all(abs(v)>.01 for v in x["action_Hessian_eigenvalues"][:4])
    assert not gravity["Lorentzian_signature_or_causality_constructed"]
    assert not gravity["exact_non_linear_Dirac_first_class_constraint_algebra_derived"]

def test_reye_axis_frame_25x60_exact_8_blind_modes(frame):
    assert [frame["packet_rows"],frame["icosian_axis_columns"]]==[25,60]
    assert frame["binary_matrix_rank_over_Q"]==17
    assert frame["nullspace_dimension"]==8
    assert frame["Gram_eigenvalues"]=={"0":8,"15":16,"60":1}
    assert frame["eight_dimensional_nullspace_from_row_col_zero_sum"]
    assert len(frame["all_8_explicit_kernel_vectors_25_entries"])==8
    assert frame["condition_on_nonzero_singular_values"]==2
    assert frame["triple_intersections_on_one_axis"]==600

def test_actual_e8_even_unimodular_index5_extension_from_reye_kernel(glue):
    assert glue["normalized_kernel_root_lattice"]=="A4 ⊕ A4"
    assert glue["packet_axis_kernel_dimension"]==8
    assert glue["normalized_kernel_Gram_determinant"]==25
    assert glue["E8_overlattice_index"]==5
    assert glue["discriminant_isotropic_slope_solutions_mod5"]==[2,3]
    assert glue["each_E8_has_240_norm2_roots"]
    for cert in glue["plus_and_minus_E8_lattice_certificates"].values():
        assert cert["Gram_determinant"]==1
        assert cert["norm2_roots"]==240
        assert cert["nonzero_anisotropic_mod2_classes"]==120
        assert cert["nonzero_isotropic_mod2_classes"]==135
        assert cert["even_unimodular"]

def test_H4_row_col_interchange_swaps_two_E8_glues(glue):
    assert glue["A5xA5_preserves_both_E8_glues"]
    assert glue["row_column_interchange_exchanges_the_two_E8_glues"]
    assert glue["full_icosian_H4_packet_action_cannot_fix_one_E8_glue"]
    assert glue["no_invariant_single_glue_selection_without_sheet_choice"]
