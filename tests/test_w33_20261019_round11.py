"""Round11 reproducibility tests across all five requested independent fronts."""
from __future__ import annotations
import sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
@pytest.fixture(scope="module")
def algebra():
    from w33_20261019_round11_vacuum_intersection_algebra import run
    return run()
def test_exact_17_class_coherent_configuration_structure(algebra):
    assert algebra["all_checks_pass"]
    assert algebra["number_classes"]==17
    assert algebra["intersection_count"]==4913
    assert algebra["left_regular_associativity_max_integer"]==0
    assert algebra["commutator_max_integer"]>0
def test_exact_center_and_Wedderburn_C5_plus_three_M2(algebra):
    assert algebra["center_dimension"]==8
    assert algebra["checks"]["exact_rational_center_dimension_8"]
    assert sum(algebra["valencies"])==1440
    assert 5*1**2+3*2**2==algebra["number_classes"]
def test_all_7021_three_tick_pairs_per_15_fixed_slices():
    from w33_20261019_round11_phase_local_triplet import run
    d=run()
    assert d["all_checks_pass"]
    assert len(d["slices"])==15
    assert d["best"]["candidate_count"]==7021
    assert not d["adversarial_counterexample_at_two_tick_kcrit"]
def test_first_Tits_cubic_and_exact_quadratic_adjoint():
    from w33_20261019_round11_first_tits_jordan import run
    d=run()
    assert d["all_checks_pass"]
    assert d["monomial_count"]==45
    assert d["samples_exact_integer"]==40
def test_photon_multinomial_covariance_matches_empirical():
    from w33_20261019_round11_photon_covariance import run
    d=run()
    assert d["all_checks_pass"]
    assert d["settings_per_run"]==36
    assert len(d["tested"][1]["variance_detailed_36_settings"])==36
def test_compact_gauging_Cartan_positive_inner_product_and_brackets():
    from w33_20261019_round11_cartan_positive_compact_gauge import run
    d=run()
    assert d["all_checks_pass"]
    assert d["dimensions"]["K_E7_compact_plus_su2"]==136
    assert d["dimensions"]["P_56_tensor_2"]==112
    assert max(d["Z2_grade_residuals"].values())<1e-10
