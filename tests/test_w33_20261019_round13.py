"""Five independent research-front regressions, Round13."""
from __future__ import annotations
import sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
def test_auxiliary_stable_boson_sign_and_17class_no_go():
    from w33_20261019_round13_auxiliary_mediator import run
    x=run()
    assert x["all_checks_pass"]
    assert x["num_17_orbits"]==17
    assert x["distinct_overlap_values"]==7
    assert x["distinct_overlap_and_quartic_signatures"]==9
    assert x["sampled_max_mixed_norm_sq"]<x["single_centered_norm_sq"]+1e-9
def test_certified_finite_temperature_strip_counterexample():
    from w33_20261019_round13_rigorous_temperature_strip import run
    x=run()
    assert x["all_checks_pass"]
    assert x["T_interval"]==["9999/10000","10001/10000"]
    assert x["rigorous_minimum_singleton_energy_advantage_over_strip_exact"]
    assert x["T1_positive_energy_advantage_lower_bound_float"]>1/1500
    assert x["maximum_interval_energy_variation_upper_bound_float"]<.00042
def test_exact_SO10_branching_projectors_and_U1_cubic_transport():
    from w33_20261019_round13_so10_transport import run
    x=run()
    assert x["all_checks_pass"]
    assert [a["traces"] for a in x["clock_sectors"]]==[[1,10,16]]*3
    assert x["cubic_monomial_support_count"]==89
    assert len(x["charge_matrices_in_first_Tits_27_basis"])==3
def test_SNSPD_literature_anchored_design_assumptions_explicit():
    from w33_20261019_round13_photon_hardware_budget import run
    x=run()
    assert x["all_checks_pass"]
    assert abs(x["baseline_810000_source_pulses_expected_dark_counts_in_1ns_gates"]-.2916)<1e-12
    assert len(x["illustrative_design_sweep"])==4
    assert min(t["projected_Z_after_0_02_bias"] for t in x["illustrative_design_sweep"])>=5
def test_SO10_SU5_chiral_anomaly_and_mass_selection_rules():
    from w33_20261019_round13_chiral_anomaly_27 import run
    x=run()
    assert x["all_checks_pass"]
    assert all(v==0 for v in x["cancelled_anomaly_polynomials"].values())
    assert all(v==0 for v in x["SU5_anomaly_polynomials"].values())
    assert all(v==0 for v in x["E6_cubic_allowed_Yukawa_charge_sums"].values())
    assert x["single_SO10_spinor16_U1_anomalies"]["U1_cubic"]!=0
