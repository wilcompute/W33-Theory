"""Round10 regression certificates: five independent research fronts."""
from __future__ import annotations
import sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
@pytest.fixture(scope="module")
def pair():
    from w33_20261019_round10_pair_orbit_schreier import run
    return run()
@pytest.fixture(scope="module")
def triple():
    from w33_20261019_round10_three_tick_falsification import run
    return run()
def test_exact_2916_stabilizer_17_pair_orbits(pair):
    assert pair["all_checks_pass"]
    assert pair["stabilizer_order"]==2916
    assert pair["stabilizer_orbit_count"]==17
    assert sum(x["size"] for x in pair["stabilizer_pair_orbits"])==1440
def test_pair_overlap_invariant_in_stabilizer_classes(pair):
    assert pair["overlap_constant_max_residual"]<1e-9
    assert any(abs(x["overlap_to_reference"]-4/9)<1e-8 for x in pair["stabilizer_pair_orbits"])
def test_triple_support_adversarial_search_no_spurious_counterexample(triple):
    assert triple["all_checks_pass"]
    assert not triple["tests"]["three_tick_counterexample_to_local_kappa"]
    assert triple["best_feasible_three_tick_crossing_kappa"]<=triple["local_two_tick_instability_kappa"]+1e-5
def test_octonionic_intertwiner_monomial_obstruction():
    from w33_20261019_round10_E6_sparse_intertwiner_obstruction import run
    d=run()
    assert d["all_checks_pass"]
    assert d["trinification_cubic_support"]==45
    assert d["Jordan_Cayley_Dickson_cubic_support"]==89
def test_detector_false_clicks_and_stale_phase_reference():
    from w33_20261019_round10_optical_detector_and_drift import run
    d=run()
    assert d["all_checks_pass"]
    assert d["analytic_cases"][2]["contrast_bias"]>.005
    assert d["synthetic_photon_statistics"]["repetitions_per_case"]==70
def test_explicit_gauge_invariance_of_scalar_cubics_quartics():
    from w33_20261019_round10_gauge_invariant_action import run
    d=run()
    assert d["all_checks_pass"]
    assert d["max_random_gauge_invariance_residual"]<1e-9
def test_noncompact_full_E8_ym_kinetic_indefinite():
    from w33_20261019_round10_gauge_invariant_action import run
    d=run()
    assert d["E8minus24_Killing_signature"]=={"positive":112,"negative":136,"rank":248}
