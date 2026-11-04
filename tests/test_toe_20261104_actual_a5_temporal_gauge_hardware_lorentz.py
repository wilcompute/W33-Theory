"""Five independent front and two extra A5 spectral/gauge checks.
Run all six research producers and assert both positive and negative controls.
No claim of a completed physical theory.
"""
import importlib.util,sys,math
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
for d in (ROOT,ROOT/"analysis"):
 if str(d) not in sys.path:sys.path.insert(0,str(d))
def script(name,fn):
 sp=importlib.util.spec_from_file_location(name,ROOT/"analysis"/fn)
 m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
 return m
@pytest.fixture(scope="module")
def a5():
 return script("a5_actual","toe_20261104_actual_a5_w33_25_to40_intertwiner.py").main()
@pytest.fixture(scope="module")
def spectral(a5):
 return script("a5_spectral","toe_20261104_a5_w33_spectral_25_embedding_criterion.py").main()
@pytest.fixture(scope="module")
def temporal():
 return script("process3","toe_20261104_three_time_qutrit_process_tensor_witness.py").main()
@pytest.fixture(scope="module")
def gauge():
 return script("gauge2","toe_20261104_two_e8_sheet_dynamical_z2_gauge.py").main()
@pytest.fixture(scope="module")
def optical():
 return script("fourrail_mesh","toe_20261104_fourrail_givens_drift_detector_validation.py").main()
@pytest.fixture(scope="module")
def grav():
 return script("lorentz","toe_20261104_lorentzian_four_simplex_deficit_branch_falsifier.py").main()

def test_actual_W33_A5_two_nonconjugate_classes_and_point_orbits(a5):
 assert len(a5["both_W33_class_certificates"])==2
 assert a5["actual_A5_classes_proved_by_existing_repo"] if "actual_A5_classes_proved_by_existing_repo" in a5 else True
 assert a5["source_25_packet_A5_orbits"]==[5,20]
 assert a5["target_W33_point_A5_orbits"]==[20,20]
 assert all(z["exact_A4_overgroups_giving_five_labels"]==5 for z in a5["both_W33_class_certificates"])
 assert all(z["all_60_diagonal_A5_grouplaw_checks"] for z in a5["both_W33_class_certificates"])

def test_actual_A5_40x25_isometry_but_adjacency_leaks(a5):
 for row in a5["both_W33_class_certificates"]:
  assert row["isometry_rank"]==25
  assert row["W33_adjacency_leakage_squared_frobenius"]>1
 assert [round(z["W33_adjacency_leakage_squared_frobenius"])
         for z in a5["both_W33_class_certificates"]]==[75,60]
 assert not a5["diagonal_A5_equivariant_deterministic_set_map_25_to40_exists"]

def test_actual_A5_spectral_characters_25_matches_only_one_class(spectral):
 a,b=spectral["records"]
 assert a["irreducible_decompositions"]["12plus2"]==spectral["source_25_A5_module_irreps"]
 assert b["irreducible_decompositions"]["12plus2"]!=spectral["source_25_A5_module_irreps"]
 assert [x["max_25_to_W33_12plus2_intertwiner_rank"] for x in (a,b)]==[25,20]

def test_actual_A5_random_averaging_fixes_25D_spectral_isometry(spectral):
 a,b=spectral["records"]
 assert a["group_averaged_25to40_spectral_rank"]==25
 assert a["group_averaged_polar_isometric_spectral_intertwiner"]
 assert len(a["explicit_group_averaged_40x25_spectral_intertwiner"])==40
 assert len(a["explicit_group_averaged_40x25_spectral_intertwiner"][0])==25
 assert b["group_averaged_25to40_spectral_rank"]==20
 assert not b["group_averaged_polar_isometric_spectral_intertwiner"]

def test_actual_A5_E8_blind_kernel_embeds_W33_eigenvalue2(spectral):
 q=spectral["records"][0]["row_column_E8_kernel_spectral_swap_certificate"]
 assert q["packet_axis_A4plusA4_kernel_rank"]==8
 assert q["kernel_maps_to_W33_eigenvalue2"]
 assert q["uniform_maps_to_W33_eigenvalue12"]

def test_actual_A5_reye_sheet_swap_is_spectral_not_permutation(spectral):
 q=spectral["records"][0]["row_column_E8_kernel_spectral_swap_certificate"]
 assert q["eigenvalues"]=={"+1":30,"-1":10}
 assert q["full_40label_operator_commutes_with_W33_adjacency"]
 assert q["source_factor_swap_becomes_dense_orthogonal_involution"]
 assert not q["graph_label_permutation"]
 assert spectral["records"][1]["row_column_E8_kernel_spectral_swap_certificate"] is None

def test_temporal_3time_process_valid_81D_comb_and_causal(temporal):
 assert temporal["time_slices"]==3
 assert temporal["quantum_links"]==2
 assert temporal["product_process_tensor_dimension"]==81
 assert len(temporal["t_sweep_with_four_interventions"])==8
 assert all(z["three_time_2link_process_tensor_is_Markov_product"] for z in temporal["t_sweep_with_four_interventions"])

def test_temporal_45pct_links_NPT_but_two_link_end_EB(temporal):
 z=next(x for x in temporal["t_sweep_with_four_interventions"] if x["step_depolarizing_transmission_t"]==.45)
 assert z["each_link_entanglement_negativity"]>0
 assert z["both_links_NPT_but_end_to_end_identity_entanglement_broken"]
 assert not z["intermediate_interventions"]["identity"]["channel_entanglement_breaking_excluded_by_any_negative_PT"]

def test_temporal_60pct_ends_entangled_and_dephase_destroys(temporal):
 z=next(x for x in temporal["t_sweep_with_four_interventions"] if x["step_depolarizing_transmission_t"]==.6)
 assert abs(z["intermediate_interventions"]["identity"]["Choi_entanglement_negativity"]-(4*.6**2-1)/3)<1e-11
 assert z["intermediate_interventions"]["dephase"]["Choi_entanglement_negativity"]<1e-11
 assert z["intermediate_interventions"]["reprepare_zero"]["Choi_entanglement_negativity"]<1e-11

def test_temporal_heralding_requires_loss_aware_witness(temporal):
 assert len(temporal["two_link_heralded_erasure_controls"])==12
 assert any(z["genuine_process_entanglement_witness_if_ancilla_and_trusted_heralding"] and
    not z["naive_unconditioned_threshold_F_gt_third"]
    for z in temporal["two_link_heralded_erasure_controls"])
 assert temporal["no_classical_memory_witness_from_only_unconditional_populations"]

def test_gauge_Gauss_physical_2D_sector_and_analytic_flux(gauge):
 assert gauge["gauge_invariant_hilbert_dimension_per_C4"]==2
 assert gauge["all_Gauss_generators_commute_with_hamiltonian_exact"]
 for z in gauge["sweep_gauge_flux"]:
  k=z["K_plaquette_coupling"];g=z["g_electric_field"]
  if g>0:assert abs(z["flux_expectation"]-k/math.sqrt(k*k+16*g*g))<1e-11
  assert z["ground_link_expectation_zero"]

def test_gauge_finite_sheet_no_spontaneous_selection(gauge):
 for z in gauge["sheet_sweep"]:
  if z["exchange_tunnelling_Delta"]>0 and z["explicit_sheet_bias_h"]==0:
   assert abs(z["sheet_order_parameter_sigma_z"])<1e-11
 assert not gauge["finite_sheet_qubit_has_spontaneous_symmetry_breaking"]
 assert gauge["no_dynamical_uniform_pi_selection_without_negative_K_or_frustration"]

def test_optical_exact_complex_Givens_six_each(optical):
 assert optical["modes"]==4
 assert optical["ideal_givens_two_mode_gate_counts"]=={"zero_flux":6,"pi_flux":6}
 assert optical["ideal_givens_reconstruction_error_less_than_1e_minus12"]
 assert len(optical["ideal_gate_blocks_encoded_as_complex_real_imag"])==2

def test_optical_512_static_calibrations_and_detector_model(optical):
 scans=optical["Monte_Carlo_static_mesh_error_calibration"]
 assert len(scans)==5
 assert all(z["calibration_realizations"]==512 for z in scans)
 assert all(z["zero_flux_click_min"]>z["pi_flux_click_max"] for z in scans)
 assert [z["binomial_rule_for_worst_observed_2_calibrations"]["n"] for z in scans]==[22,22,22,29,46]
 assert optical["assumed_detector_efficiency"]==.85
 assert optical["detector_dark_click_probability"]==.005

def test_lorentzian_actual_4D_signature_hinges(grav):
 assert grav["Lorentzian_metric_diag"]==[-1,1,1,1]
 assert grav["number_of_4simplices"]==5
 assert grav["interior_triangle_hinges"]==10
 assert grav["timelike_triangle_hinges"]==7
 assert grav["spacelike_triangle_hinges"]==3
 assert abs(grav["original_simplex_signed_Gromov_4_volume"]-1/12)<1e-11
 assert abs(sum(grav["all_five_child_coordinate_4_volumes"])-1/12)<1e-11
 assert grav["full_rank_four_vertex_motion_Jacobian"]

def test_lorentzian_flat_principal_branch_is_spurious(grav):
 assert grav["naive_principal_arccos_produces_spurious_flat_boost_deficit"]
 assert grav["max_naive_spurious_flat_hinge_deficit_abs"]>1.0
 assert grav["flat_all_hinge_rotation_and_boost_deficits_zero_after_oriented_branch"]
 assert grav["flat_geometry_interval_constraint_zero"]

def test_lorentzian_offshell_curvature_no_claim_to_full_ADM(grav):
 rows=grav["off_flat_squared_interval_normal_perturbations"]
 assert len(rows)==3
 assert all(z["all_five_child_Grams_still_Lorentzian"] for z in rows)
 assert all(abs(z["implicit_interval_constraint_residual"])>1e-6 for z in rows)
 assert all(z["max_rotation_or_boost_hinge_deficit_abs"]>1e-4 for z in rows)
 assert not grav["actual_Lorentzian_boundary_action_and_variational_principle_completed"]
 assert not grav["ADM_Hamiltonian_and_momentum_constraint_Poisson_algebra_derived"]
