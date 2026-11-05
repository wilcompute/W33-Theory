"""Eight independently executable TOE falsification fronts, 2026-11-05.

All eight producer main() functions run from scratch in a scoped module
fixture; cached JSON cannot manufacture a passing test. Repo pytest
conftest intentionally excluded to avoid unrelated global fixtures.
"""
from __future__ import annotations
import importlib,json,math,sys
from pathlib import Path
import numpy as np
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
FILES={
 "matrix":"toe_20261105_new_front1_abelian_matrix",
 "causal":"toe_20261105_new_front2_causal_manifold_guard",
 "pairs":"toe_20261105_new_front3_z2_gauge_pairs",
 "flavor":"toe_20261105_new_front4_flavor_rank2",
 "speed":"toe_20261105_new_front5_gapless_velocity_lock",
 "z9":"toe_20261105_new_swingA_z9_proton_rule",
 "page":"toe_20261105_new_swingB_page_information",
 "cosmo":"toe_20261105_new_swingC_de_calibration"}
DATA={
 "matrix":"toe_20261105_new_front1_abelian_coupling_matrix.json",
 "causal":"toe_20261105_new_front2_causal_matching_no_manifold.json",
 "pairs":"toe_20261105_new_front3_z2_gauss_pairs.json",
 "flavor":"toe_20261105_new_front4_flavor_rank2_selection.json",
 "speed":"toe_20261105_new_front5_gapless_velocity_locking.json",
 "z9":"toe_20261105_new_swingA_z9_proton_quality.json",
 "page":"toe_20261105_new_swingB_page_information_transfer.json",
 "cosmo":"toe_20261105_new_swingC_cosmology_calibration_guard.json"}
@pytest.fixture(scope="module")
def r():
    return {k:importlib.import_module(v).main() for k,v in FILES.items()}

def test_matrix_two_U1_beta_has_required_mixing(r):
    x=r["matrix"]
    assert x["B_Y_BL"]==pytest.approx(52/9)
    assert x["B_full"][1][1]==pytest.approx(116/9)
    assert x["B_SM_minimal_no_N"][0][0]==pytest.approx(41/6)

def test_matrix_symmetric_positive_and_covariant(r):
    x=r["matrix"]
    assert min(x["K_high_eigenvalues"])>0
    assert x["exact_basis_covariance_max_error"]<1e-12
    assert all(abs(row["difference"])<5e-14 for row in x["charge_current_basis_invariance"])

def test_abelian_threshold_mixing_nonzero(r):
    x=r["matrix"]
    assert -.09<x["effective_chi_K12_over_sqrtK11K22"]<-.04
    assert x["vectorlike_log_threshold_deltaK"][0][1]<-.05
    assert "NOT_IMPLEMENTED" in x["second_loop_status"]

def test_causal_global_relation_calibrated(r):
    x=r["causal"]
    assert abs(x["calibration_grid"][-1]["global_relation_fraction"]-x["target_Minkowski4_global_comparability"])<.002 or abs(
     min(x["calibration_grid"],key=lambda z:abs(z["global_relation_fraction"]-x["target_Minkowski4_global_comparability"]))["global_relation_fraction"]-x["target_Minkowski4_global_comparability"])<.001
    a=x["ensemble_summary"]["Minkowski_4_supplied"]
    b=x["ensemble_summary"]["causal_percolation_metric_free"]
    assert abs(a["related_fraction"]-b["related_fraction"])<.02

def test_causal_local_dim_not_simply_global_fraction(r):
    x=r["causal"]["ensemble_summary"]
    a=x["Minkowski_4_supplied"]
    b=x["causal_percolation_metric_free"]
    assert abs(a["local_dimension"]-4)<.45
    assert abs(b["local_dimension"]-4)>1.
    assert b["chain_height"]>a["chain_height"]+3

def test_causal_endpoints_artifact_removed(r):
    a=r["causal"]["independent_seed_replicates"]["Minkowski_4_supplied"]
    assert len(a)==5
    vals=[v["naive_endpoint_included_dimension_median"] for v in a if v["naive_endpoint_included_dimension_median"]]
    assert len(vals)>2
    assert np.median(vals)<3.5
    assert np.median([v["local_interval_dimension_median"] for v in a])>3.5

def test_local_fermion_gauss_sector_dim(r):
    x=r["pairs"]
    assert x["full_Hilbert_dimension"]==128
    assert x["gauss_sector_dim_all_parity_even"]==8
    assert x["gauss_sector_dim_fixed_fermion_number_2"]==6
    assert max(x["full_gauge_generator_commutator_infinity_norms"])==0

def test_gauge_coupled_hopping_preserves_gauss(r):
    x=r["pairs"]
    assert x["gauge_preserving_leakage_full_evolution"]<1e-12
    assert x["gauge_violating_bare_hopping_leakage"]>.1
    assert x["bare_hopping_without_gauge_link_max_commutator"]>0

def test_relative_pair_creation_in_number_conserving_sector(r):
    a=r["pairs"]["time_series"]
    assert a[0]["mean_staggered_particle_antiparticle_pair_count"]==0
    assert a[3]["mean_staggered_particle_antiparticle_pair_count"]>.5
    assert a[3]["specific_neighbor_pair_probability"]>.01

def test_flavor_exact_TM2_excluded_TM1_solar_only_not(r):
    x=r["flavor"]
    assert x["TM2_exact_model_solar_prediction_range"][0]>x["ranges_used"]["s12"][1]
    assert x["TM1_exact_model_solar_prediction_range"][0]>x["ranges_used"]["s12"][0]
    assert x["TM1_exact_model_solar_prediction_range"][1]<x["ranges_used"]["s12"][1]

def test_rank2_neutrinoless_mass_zero_excluded_under_assumptions(r):
    x=r["flavor"]["rank_two_see_saw_massless_lightest_prediction"]
    assert x["normal_ordering"]["strict_lower_bound_mee_eV"]>.001
    assert x["inverted_ordering"]["strict_lower_bound_mee_eV"]>.015
    assert x["normal_ordering"]["sampled_minimum_mee_eV"]>x["normal_ordering"]["strict_lower_bound_mee_eV"]

def test_2gapless_modes_not_equalized_by_gradient_coupling(r):
    a=r["speed"]["two_species_all_gapless_sweep"]
    assert all(v["both_modes_gapless"] and v["gapless_boson_branches"]==2 for v in a)
    assert a[0]["normal_mode_velocities"]==pytest.approx([1,1.2])
    assert all(a[i+1]["velocity_split"]>a[i]["velocity_split"] for i in range(len(a)-1))

def test_bare_speed_equality_alone_not_sufficient(r):
    b=r["speed"]["identical_bare_speeds_offdiagonal_coupling_sweep"]
    assert b[0]["velocity_split"]==0
    assert all(v["velocity_split"]>0 for v in b[1:])
    assert len(r["speed"]["higher_species_matrix_controls"])==3

def test_z9_forbids_proton_decay_operators(r):
    z=r["z9"]
    assert z["screened_DeltaB_1_or_2_all_forbidden"]==202
    assert z["number_necessary_SM_gauge_singlet_nonzero_B_operator_monomials"]==202
    assert all(v["Z9_charge"] in (3,6) for v in z["explicit_dim6_forbidden_SM_operators"])

def test_Z9_different_from_minimal_BL_Higgs_remnant(r):
    z=r["z9"]
    assert z["cannot_get_Z9_proton_selection_from_unchanged_minimal_BL_S_vev"]
    assert z["minimal_BL_3BL_integer_charges"]["S"]==-6
    assert z["explicit_schematic_DeltaB3_operator"]["dim"]==15
    assert z["explicit_schematic_DeltaB3_operator"]["Z9_charge"]==0

def test_Page_curve_pure_global_information_returns(r):
    a=r["page"]["rows"]
    assert len(a)==9
    assert a[4]["Page_exact_Haar_mean_entropy_bits"]>3.25
    assert a[5]["Page_exact_Haar_mean_entropy_bits"]<a[4]["Page_exact_Haar_mean_entropy_bits"]
    assert abs(a[-1]["observed_random_state_mean_entropy_bits"])<1e-12

def test_permanently_hidden_hawking_partners_do_not_purify_radiation(r):
    a=r["page"]["rows"]
    assert a[-1]["hidden_partner_never_released_entropy_bits"]==8
    assert [z["hidden_partner_never_released_entropy_bits"] for z in a]==list(range(9))

def test_random_entanglement_matches_exact_Page_average(r):
    a=r["page"]["rows"]
    assert all(abs(x["observed_random_state_mean_entropy_bits"]-
       x["Page_exact_Haar_mean_entropy_bits"])<.11 for x in a)

def test_cosmology_synthetic_calibration_degeneracy(r):
    z=r["cosmo"]["synthetic_calibration"]
    assert z["max_abs_post_calibration_SN_residual_mag"]<.02
    assert z["synthetic_SN_chi2_difference_versus_CPL_for_drift_LCDM"]<3
    assert z["BAO_one_percent_fractional_uncertainty_LCDM_vs_CPL_expected_chi2"]>10
    assert z["BAO_three_percent_fractional_uncertainty_LCDM_vs_CPL_expected_chi2"]<3

def test_cosmology_ppd_survivorship_bias_audit(r):
    rows=r["cosmo"]["repo_posterior_predictive_failure_audit"]["rows"]
    exp=next(x for x in rows if x["model"]=="exp_infl1")
    assert exp["zero_failed_draws_total_elpd"]<exp["reported_total_elpd"]-1.
    fade=next(x for x in rows if x["model"]=="free_neg_infl2")
    assert fade["zero_failed_draws_total_elpd"]<fade["reported_total_elpd"]-.6
    cpl=next(x for x in rows if x["model"]=="cpl_infl1")
    assert cpl["zero_failed_draws_total_elpd"]==cpl["reported_total_elpd"]

def test_all_eight_certificates_recomputed_current_run(r):
    for k,name in DATA.items():
        p=ROOT/"data"/name
        assert p.exists(),name
        saved=json.loads(p.read_text(encoding="utf8"))
        assert saved==json.loads(json.dumps(r[k])),name

def test_epistemic_scope_present_all_fronts(r):
    for k,x in r.items():
        assert "status" in x and x["status"].startswith("PASS_"),k
    assert r["page"]["limitations"].startswith("Uniform Haar")
    assert "NOT_IMPLEMENTED" in r["matrix"]["second_loop_status"]
    assert "No fresh statistical evidence" in r["cosmo"]["scientific_boundary"]
