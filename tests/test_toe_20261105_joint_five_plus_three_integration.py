"""November 2026: five TOE integration fronts and three orthogonal guards.

All six source modules recomputed from scratch under a scoped
module fixture; JSON certificates compared to current live results.
NO global conftest, no dependence on stale cached certificates.
"""
from __future__ import annotations
import importlib,json,math,sys
from pathlib import Path
import numpy as np
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
SOURCES={
 "pq":"toe_20261105_abelian_seesaw_pq_operator_theorem",
 "rge":"toe_20261105_two_loop_gauge_matrix_nonabelian",
 "flavor":"toe_20261105_flavor_inverse_mass_map_no_prediction",
 "causal":"toe_20261105_causal_bdg_history_interference",
 "page":"toe_20261105_gauss_dressed_page_information",
 "extra":"toe_20261105_three_independent_home_run_guards"}
DATA={
 "pq":"toe_20261105_abelian_seesaw_pq_operator_no_go.json",
 "rge":"toe_20261105_full_u1matrix_su2_su3_gaugeonly_two_loop.json",
 "flavor":"toe_20261105_x_flavor_inverse_seesaw_surjectivity.json",
 "causal":"toe_20261105_causal_bdg_exact_history_interference.json",
 "page":"toe_20261105_gauss_dressed_evaporation_page_curve.json",
 "extra":"toe_20261105_three_home_run_physics_no_gos.json"}
@pytest.fixture(scope="module")
def z():
    return {k:importlib.import_module(m).main() for k,m in SOURCES.items()}
def test_pq_operator_identity_with_bare_mass(z):
    a=z["pq"]["formal_charge_identities"]
    assert a["cubic_charge"]=="-2*m"
    assert a["quartic_with_Rdag_charge"]=="0"
    assert z["pq"]["derived"].startswith("Allowed three")

def test_pq_modular_complete_exhaustive(z):
    a=z["pq"]["exhaustive_Zn_charge_assignments_n2_through50"]
    assert len(a)==49
    assert sum(v["charge_pairs_checked"] for v in a.values())==42924
    for key,row in a.items():
        n=int(key)
        assert row["charge_pairs_checked"]==n*n
        assert row["bare_mass_compatible_pairs"]==n*math.gcd(n,2)
        assert row["cubic_allowed_when_bare_mass"]

def test_pq_replacing_bare_still_quartic(z):
    a=z["pq"]["exhaustive_Zn_charge_assignments_n2_through50"]
    assert all(row["quartic_allowed_with_R_when_mass_is_from_R"] for row in a.values())
    assert z["pq"]["formal_charge_identities"]["possible_replacement_R"]=="-2*m"

def test_scalar_only_charge_quality_not_sufficient(z):
    a=z["pq"]["delayed_scalar_only_comparators_without_yukawa_constraints"]
    assert [r["first_scalar_phase_sensitive_degree"] for r in a]==[7,11,15,21,27]
    assert "scalar/fermion phases" in z["pq"]["physics_boundary"]
def test_rge_sm_rawY_independent_coefficients(z):
    a=z["rge"]["reproduced_exact_SM_rawY_two_loop_coefficients"]
    assert a["one_loop_bYY"]==pytest.approx(41/6)
    assert a["two_loop_YY_YY"]==pytest.approx(199/18,rel=1e-10)
    assert a["two_loop_YY_SU2"]==pytest.approx(4.5)
    assert a["two_loop_YY_SU3"]==pytest.approx(44/3)
    assert a["two_loop_SU2_YY"]==pytest.approx(1.5)
    assert a["two_loop_SU3_YY"]==pytest.approx(11/6)
def test_rge_two_loop_multifactor_changes_K(z):
    a=z["rge"]
    K1=np.array(a["one_loop_whole_gauge_4factor"]["K_high"])
    K2=np.array(a["two_loop_gauge_only_whole_4factor"]["K_high"])
    assert K2[0,0]<K1[0,0]-.008
    assert K2[1,1]<K1[1,1]-1.
    assert min(np.linalg.eigvalsh(K2))>0
def test_rge_basis_covariance_two_loop(z):
    a=z["rge"]
    assert a["basis_covariance_error_K_infinity"]<1e-10
    for K in (a["two_loop_gauge_only_whole_4factor"]["K_high"],
              a["basis_transformed_two_loop"]["K_high"]):
        assert min(np.linalg.eigvalsh(K))>0
def test_rge_missing_yukawa_threshold_not_misreported(z):
    assert "OMITTED" in z["rge"]["critical_missing"]
    assert "no Higgs vev or physical prediction" in z["rge"]["physical_scope"]
    assert "no matching" in z["rge"]["critical_missing"].lower()
def test_seesaw_all_twelve_inverse_reconstructions(z):
    rows=z["flavor"]["scan"]
    assert len(rows)==12
    assert max(r["max_reconstruction_relative_error"] for r in rows)<1e-14
    assert all(min(r["heavy_singular_masses_GeV"])>1e9 for r in rows)
def test_seesaw_all_allowed_scalar_sources(z):
    for row in z["flavor"]["scan"]:
        assert row["MR_allowed_source_by_X"]==[
          ["S","T","T"],["T","bare","bare"],["T","bare","bare"]]
    assert z["flavor"]["random_nonspecial_complex_symmetric_matrix_relative_error"]<1e-13
def test_seesaw_phases_and_absolute_scale_not_predicted(z):
    rows=z["flavor"]["scan"]
    m0={r["masses_eV"][0] for r in rows}
    mee={round(r["mee_eV"],6) for r in rows}
    assert len(m0)==3 and len(mee)>=5
    assert "inputs" in z["flavor"]["limitations"]
def test_causal_exact_exhaustive_history_count(z):
    a=z["causal"]
    assert a["edge_bit_histories"]==2**15==32768
    assert a["count_unique_B4"]==54
    assert a["B4_min_max"][0]<a["B4_min_max"][1]
def test_causal_same_action_different_chain(z):
    r=z["causal"]["same_action_different_chain_height_counterexample"]
    assert r["different_longest_chains"][0]!=r["different_longest_chains"][1]
    assert r["histories"][0]!=r["histories"][1]
def test_causal_phase_cancellation(z):
    a=z["causal"]["unitary_phase_weighted_partition_averages"]
    assert a[0]["absolute_amplitude"]==pytest.approx(1,abs=1e-14)
    assert a[4]["absolute_amplitude"]==pytest.approx(.114987802009664,rel=1e-11)
    assert a[4]["effective_coherence_fraction_modulus_squared"]<.02
def test_causal_not_uniform_poset_measure(z):
    assert "NOT uniform" in z["causal"]["measure"]
    assert "no path-integral measure" in z["causal"]["limitations"]
def test_page_dressed_local_flip_exact_gauss(z):
    a=z["page"]
    assert a["physical_gauss_sector_dimension"]==8
    assert a["reference_gauss_eigenvalues"]==[-1,1,-1,1]
    assert "preserves Gauss exactly" in a["microscopic_local_dressed_flip_rule"]
def test_page_entropy_returns_after_three_emissions(z):
    for row in z["page"]["samplings"]:
        S=row["radiation_entropy_after_0_1_2_3_emissions_bits"]
        assert len(S)==4
        assert abs(S[0])<1e-10 and abs(S[-1])<1e-10
def test_page_intermediate_entropy_and_bare_leakage(z):
    a=z["page"]["best_nonzero_intermediate_entropy_benchmark"]
    S=a["radiation_entropy_after_0_1_2_3_emissions_bits"]
    assert .95<S[1]<=1.000000000001
    assert .95<S[2]<=1.000000000001
    assert a["bare_link_swap_gauge_leakage_probability_if_radiation_starts_vacuum"]>.5
def test_bell_lossy_local_postselection_fake_chsh(z):
    a=z["extra"]["operational_Bell"]
    assert a["postselected_apparent_CHSH"]==4
    assert a["each_side_single_detection_efficiency"]==.5
    assert a["joint_detection_probability_each_setting_pair"]==.25
    assert a["postselected_correlations"]=={"00":1,"01":1,"10":1,"11":-1}
def test_bell_quantum_optimum_and_fixed_settings(z):
    a=z["extra"]["operational_Bell"]["quantum_CHSH_sweep"]
    assert a[0]["CHSH_optimal"]==pytest.approx(2.)
    assert a[-1]["CHSH_optimal"]==pytest.approx(2*math.sqrt(2))
    assert not a[1]["fixed_settings_violate"]
    assert a[-1]["fixed_settings_violate"]
def test_vacuum_radiative_sensitivity(z):
    a=z["extra"]["vacuum_energy"]["reference_thresholds"]
    assert len(a)==5
    assert a[2]["deltaV_over_observed_rhoLambda"]>1e50
    assert a[-1]["deltaV_over_observed_rhoLambda"]>1e85
    assert all(row["deltaV_over_observed_rhoLambda"]>1 for row in a)
def test_leptogenesis_sign_not_determined(z):
    a=z["extra"]["leptogenesis"]
    b=a["benchmarks"]
    assert a["same_light_spectrum_opposite_leptogenesis_cp_asymmetry"]
    for i in (0,2):
        assert b[i]["approx_hierarchical_unflavored_epsilon1"]==pytest.approx(-b[i+1]["approx_hierarchical_unflavored_epsilon1"],rel=1e-12)
    assert all(x["reconstruction_error_GeV"]<1e-24 for x in b)
def test_all_six_live_certificates_reproduced(z):
    for key,name in DATA.items():
        actual=json.loads((ROOT/"data"/name).read_text(encoding="utf8"))
        assert actual==json.loads(json.dumps(z[key]))
def test_scope_separation_all_sources(z):
    assert all(v["status"].startswith("PASS_") for v in z.values())
    assert "not" in z["page"]["crucial_novelty_boundary"].lower()
    assert "Not the full" in z["rge"]["critical_missing"]
    assert "no continuum" in z["causal"]["limitations"]
