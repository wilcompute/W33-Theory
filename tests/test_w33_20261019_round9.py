"""Round9 independent research regressions across all five requested fronts."""
from __future__ import annotations
import sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
@pytest.fixture(scope="module")
def frame():
    from w33_20261019_round9_vacuum_frame_potential import run
    return run()
@pytest.fixture(scope="module")
def phase():
    from w33_20261019_round9_two_tick_convexity import run
    return run()
def test_1440_vacua_tight_frame_and_on_site_no_selection(frame):
    assert frame["all_checks_pass"]
    assert frame["size"]==1440
    assert frame["frame_spectrum_predicted"]=={"identity":640,"traceless_80":28}
    assert frame["frame_spectrum_max_residual"]<1e-8
def test_nontrivial_two_vacuum_relative_invariant(frame):
    assert len(frame["fixed_Q_pair_overlap_histogram"])>=7
    assert abs(frame["single_Q_moments"]["4"]["TrQcenteredpower"]-182/243)<1e-12
def test_exact_two_tick_phase_threshold_all_temperatures(phase):
    assert phase["all_checks_pass"]
    assert phase["noncommuting_pauli_outcome_pairs_tested"]==4860
    assert phase["PQP_equals_Pover3_max_frobenius_residual"]<1e-12
def test_two_tick_secantrate_convexity_samples(phase):
    for r in phase["temperatures"]:
        assert r["ratios_increase_with_u"]
        assert all(x["ratio_Gibbs_cost_per_commutator"]>=-r["two_tick_exact_critical_kappa"]-1e-5 for x in r["secant_ratios"])
def test_E6_45_weight_monoms_octonion_triality_preexisting_clock_pass():
    from w33_20261019_round9_triality_cubic_texture import run
    d=run()
    assert d["all_checks_pass"]
    assert d["monomial_counts"]=={"determinants":18,"cross":27,"total":45}
    assert d["max_Jordan_cubic_cyclic_residual"]<1e-10
def test_real_multinomial_optical_tomography_model():
    from w33_20261019_round9_photon_tomography_shots import run
    d=run()
    assert d["all_checks_pass"]
    assert d["settings"]==36
    assert d["photons_per_full_run"]==1440000
    assert abs(d["estimated_deficit_mean"]-8/27)<.008
def test_permutation_symmetric_radial_Higgs_and_threshold_freedom():
    from w33_20261019_round9_symmetric_higgs_thresholds import run
    d=run()
    assert d["all_checks_pass"]
    assert [r["phase"] for r in d["rows"]]==["equal","equal","equal","flat_two_simplex","single_condensate","single_condensate","single_condensate"]
