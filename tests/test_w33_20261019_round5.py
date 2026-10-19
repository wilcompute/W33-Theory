"""Round 5 reproducible frontiers; no actual device/TOE claim."""
from __future__ import annotations
import sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
@pytest.fixture(scope="module")
def census():
    from w33_20261019_round5_e8_fermion_center_and_heptad import run
    return run()
def test_e8_center_kernel_precludes_fundamental9_from_adj248(census):
    x=census["matter_sector_center_obstruction"]
    assert x["pass"]
    assert x["fundamental_nontrivial_center_residual"]>1
    assert x["full_248_central_element_identity_residual"]<1e-12
def test_all_2187_outcomes_on_uniform_noncommuting_heptad(census):
    x=census["heptad_outcome_exhaustive"]
    assert x["pass"]
    assert x["outcome_assignments_enumerated"]==3**7
    assert x["distinct_eigenspectra_at_10_decimal_precision"]==5
    assert all(q["all_zero_outcome_rank"]>1 for q in x["temperature_census"])
def test_single_photon_18mode_normalized_trace():
    from w33_20261019_round5_single_photon_18mode_trace import run
    x=run()
    assert x["all_checks_pass"]
    assert len(x["per_input_signal"])==9
    assert abs(x["ideal_deficit"]-8/27)<1e-12
def test_e8_repository_248_map_and_full_bracket_jacobi():
    from w33_20261019_round5_e8_repo_248_jacobi import run
    x=run()
    assert x["all_checks_pass"]
    assert x["J248_rank"]==80
    assert x["jacobi_27_grade_case_max_residual"]<1e-9
def test_hypothetical_anomaly_is_only_conditionally_identifiable():
    from w33_20261019_round5_conditional_anomaly_identifiability import run
    x=run()
    assert x["all_checks_pass"]
    assert len(x["angles_rad"])==8
    assert x["multi_angle_singular_values"][-1]>.01
