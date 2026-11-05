"""Five orthogonal TOE research fronts, rebuilt under independent pytest.

Fixtures rerun sources and validate newly generated certificates, rather
than asserting preexisting JSON alone. Preserve external named physics
constraints; no claim of full TOE, completed UV, axion or black hole.
"""
from __future__ import annotations
import importlib,json,math,sys
from pathlib import Path
import numpy as np
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
SOURCES={
 "pq":("toe_20261105_extra_pq_proton_color_scan","toe_20261105_extra_pq_proton_color_scalar_scan.json"),
 "flavor":("toe_20261105_mu_tau_reflection_flavor_selector","toe_20261105_mu_tau_reflection_predictive_constraint.json"),
 "uv":("toe_20261105_threshold_bfb_uv_consistency","toe_20261105_threshold_gauge_scalar_stability_proton.json"),
 "causal":("toe_20261105_causal_poset_measure_correction","toe_20261105_causal_exact_measure_entropy_bias.json"),
 "emission":("toe_20261105_autonomous_gauss_energy_emission","toe_20261105_autonomous_gauss_energy_page_recurrence.json")}
@pytest.fixture(scope="module")
def out():
    return {k:importlib.import_module(v[0]).main() for k,v in SOURCES.items()}
def test_pq_exact_z9_with_added_scalar(out):
    rows=out["pq"]["add_scalar_A_charge_scan"]
    assert len(rows)==32
    assert all(r["scalar_vevs_leave_Z9"] for r in rows)
    assert all(r["A_charge"]%9==0 for r in rows)
def test_pq_dimension_formula_exhaustive(out):
    a=out["pq"]["add_scalar_A_charge_scan"]
    assert all(r["A_sensitive_min_dimension"]==math.ceil(r["A_charge"]/18)+1 for r in a)
    assert a[23]["A_charge"]==216
    assert a[23]["A_sensitive_min_dimension"]==13
def test_pq_preexisting_phase_breaker_not_removed(out):
    x=out["pq"]
    assert x["preexisting_cubic_breaks_original_relative_scalar_phase"]
    assert all(r["original_relative_phase_breaker_remains"].startswith("Sdag") for r in x["add_scalar_A_charge_scan"])
def test_color_anomaly_pair_not_cancellable_by_single_chiral_pair(out):
    a=out["pq"]
    assert a["one_QCD_colored_KSVZ_pair_color_mixed_X_anomaly"]=="-X_A/2"
    assert "X_A/2" in a["two_pairs_with_A_and_A_dagger_masses_color_mixed_X_anomaly"]
    assert "does NOT test mixed" in a["crucial_limitation"]
def test_mu_tau_exact_reflection_5_samples(out):
    a=out["flavor"]
    assert len(a["random_symmetric_nontrivial_models"])==5
    assert all(x["mu_tau_mode_probability_max_difference"]<1e-11 for x in a["random_symmetric_nontrivial_models"])
def test_mu_tau_theta23_and_deltaCP_predicted(out):
    a=out["flavor"]["random_symmetric_nontrivial_models"]
    assert all(abs(x["theta23_deg"]-45)<1e-9 for x in a)
    assert all(abs(abs(x["sin_delta_CP"])-1)<1e-8 for x in a)
def test_mu_tau_explicit_break_control(out):
    x=out["flavor"]["symmetry_violating_control"]
    assert x["mu_tau_mode_probability_max_difference"]>.001
    assert abs(x["theta23_deg"]-45)>.1
def test_flavor_symmetry_NOT_derived_from_previous_X(out):
    x=out["flavor"]
    assert x["original_X_seesaw_alone_enforces_reflection"] is False
    assert "No combined UV symmetry action" in x["not_done"]
def test_uv_oneloop_exact_threshold_match(out):
    a=out["uv"]
    rows=a["heavy_vectorlike_mass_scan"]
    assert len(rows)==6
    assert rows[0]["MQ_GeV"]==a["reference_mu_GeV"]
    assert all(x["K_min_eigenvalue"]>0 for x in rows)
    assert a["two_loop_reference_no_threshold_matches_prior_baseline"]
def test_uv_threshold_effect_monotone(out):
    rows=out["uv"]["heavy_vectorlike_mass_scan"]
    assert all(rows[i]["K_min_eigenvalue"]<rows[i+1]["K_min_eigenvalue"] for i in range(len(rows)-1))
    assert rows[-1]["MQ_GeV"]==1e13
def test_uv_tree_level_copositivity(out):
    x=out["uv"]["tree_level_bounded_below_examples"]
    assert [q["bounded_from_below_quartic"] for q in x]==[False,False,True,True,True]
    assert x[0]["quartic_at_analytic_test_direction"]<0
    assert x[-1]["quartic_at_analytic_test_direction"]>0
def test_uv_proton_Z9_screens_preserved(out):
    x=out["uv"]["exact_Z9_proton_dim6_charge_screens"]
    assert len(x)==3
    assert all(z["all_nonzero_mod_Z9"] for z in x)
def test_causal_poset_deduplication_counts(out):
    x=out["causal"]
    assert x["DAG_forward_edge_presentations"]==32768
    assert x["unique_transitively_closed_posets_with_fixed_natural_chronological_labels"]==4824
def test_causal_hasse_multiplicities_exact(out):
    x=out["causal"]
    assert x["exact_multiplicity_law"].startswith("m(C)=2^")
    assert x["maximum_presentation_multiplicity"]==1024
    h=x["multiplicity_distribution"]
    assert sum(int(k)*v for k,v in h.items())==32768
    assert sum(h.values())==4824
def test_causal_measure_dependent_phase(out):
    a=out["causal"]["phase_partition_function_measure_comparison"]
    z=next(x for x in a if x["kappa"]==1)
    assert z["presentation_measure_abs_amplitude"]==pytest.approx(.114987802009664,rel=1e-11)
    assert z["distinct_naturally_labeled_poset_measure_abs_amplitude"]==pytest.approx(.0273445250349723,rel=1e-11)
    assert z["absolute_complex_amplitude_disagreement"]>.08
def test_causal_measure_bias_height(out):
    x=out["causal"]
    assert x["mean_chain_height_DAG_presentation_measure"]>x["mean_chain_height_unique_naturally_labeled_poset_measure"]+.9
    assert "NOT quotient" in x["pitfalls"]
def test_emission_gauge_encoded_and_energy_conserved(out):
    x=out["emission"]
    assert x["combined_physical_dimension"]==64
    assert x["local_dressed_source_flip_checks"]==24
    assert x["max_energy_commutator_infinity_norm"]==0
    for model in ("identical_mode_pair_exchange","detuned_pair_exchange","superposed_input_GHZ"):
        for r in x[model]["time_series"]:
            assert abs(r["energy_conservation_error"])<1e-11
def test_emission_perfect_rabi_page_recurrence(out):
    a=out["emission"]["identical_mode_pair_exchange"]["time_series"]
    assert a[2]["S_radiation_bits"]==pytest.approx(3,abs=1e-10)
    assert abs(a[4]["S_radiation_bits"])<1e-10
    assert a[4]["P_source_completely_empty"]>1-1e-12
    assert a[-1]["mean_remaining_source_excitation_energy_over_omega"]==pytest.approx(3,abs=1e-10)
def test_emission_detuning_breaks_purification(out):
    a=out["emission"]["detuned_pair_exchange"]["time_series"]
    assert a[4]["S_radiation_bits"]>.01
    assert a[4]["P_source_completely_empty"]<.999
def test_emission_no_false_black_hole_claim(out):
    x=out["emission"]
    assert "No gravitational ADM mass" in x["number_energy_operator"]
    assert "horizon geometry" in x["limitation"].lower()
def test_all_five_fresh_certificates(out):
    for k,(_,file) in SOURCES.items():
        payload=json.loads((ROOT/"data"/file).read_text(encoding="utf8"))
        assert payload==json.loads(json.dumps(out[k])),file
def test_all_five_explicit_epistemic_limit(out):
    assert all(x["status"].startswith("PASS_") for x in out.values())
    assert out["pq"]["high_quality_candidate_example"]["cannot_infer_full_axion_quality"]
    assert "No Yukawa beta functions" in out["uv"]["missing_from_true_complete_uv"]
