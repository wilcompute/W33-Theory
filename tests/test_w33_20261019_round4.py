"""Five independently checked research fronts for W33 October 19 round four."""
from __future__ import annotations
import importlib.util
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
def load(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/"analysis"/(name+".py"))
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
def test_fermionic_all_temperature_sign_and_equal_density():
    r=load("w33_20261019_round4_fermions_global").run()
    assert r["all_checks_pass"]
    assert r["checks"]["mu_equal_density_negative_all_temperatures"]
    assert r["checks"]["both_competing_spectra_same_mean_occupancy"]
    assert all(3<=s["mean_fermion_count_commuting"]<=4.5 for s in r["mu_equal_density_samples"])
def test_global_120_to_40_plus_discrete_outcomes():
    r=load("w33_20261019_round4_fermions_global").run()
    assert r["full_120_dimensional_reduction"]["conditional_p_vertex_strict_concavity_min_test_gap"]>0
    assert r["checks"]["global_stability_bound_random_checks"]
def test_block_paired_optical_controls():
    r=load("w33_20261019_round4_optical_correlated_noise").simulate()
    assert r["all_checks_pass"]
    assert r["simulated_results"]["paired_null_false_alarm_rate"]<.05
    assert r["simulated_results"]["paired_signal_detection_rate"]>.95
    assert r["synthetic_noise"]["hoeffding_shots_per_condition"]>1000
def test_e8_three_exterior_bracket_covariances():
    r=load("w33_20261019_round4_e8_exterior_brackets").run()
    assert r["all_checks_pass"]
    assert len(r["generators_tested"])==5
    assert r["worst_numerical_error"]<1e-10
def test_operational_toe_falsification_firewall():
    r=load("w33_20261019_round4_falsification_screen").run()
    assert r["all_checks_pass"]
    assert r["tested_clifford_circuits"]==240
    assert abs(r["gate_phase_calibration_confounder"]["one_percent_relative_effect_mimicked_by_phase_error_rad"]-.01)<1e-12
