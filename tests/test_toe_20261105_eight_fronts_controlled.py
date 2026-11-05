"""All eight independent frontiers run as controlled executable falsifiers."""
import importlib.util
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis"/"toe_20261105_eight_fronts_controlled.py"
spec=importlib.util.spec_from_file_location("eightfronts",SCRIPT)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

@pytest.fixture(scope="module")
def record():
    return mod.main()["results"]

@pytest.mark.parametrize("key", [
    "1_native_gauge_action","2_continuum_locality","3_temporal_memory",
    "4_chirality_vacuum","5_optical_falsifier",
    "6_orthogonal_nonhermitian_skin",
    "7_orthogonal_quasiperiodic_localization",
    "8_orthogonal_postselection_collider"])
def test_front_runs_and_passes(record,key):
    assert record[key]["status"].startswith("PASS_")
    assert record[key]["boundary"]

def test_gauge_gap_cannot_stay_finite(record):
    rows=record["1_native_gauge_action"]["rows"]
    assert rows[-1]["delta"]<rows[0]["delta"]/10

def test_witting_povm_not_helstrom_optimal(record):
    for c in record["5_optical_falsifier"]["comparisons"]:
        assert c["POVM_optimal_decision_success"] < c["Helstrom_optimal_success"]

def test_memory_power_carries_false_alarm(record):
    r=record["3_temporal_memory"]
    assert r["exact_one_sided_false_alarm"] < 0.01
    assert r["true_positive_power"] > 0.99

def test_postselected_pr_not_loophole_free(record):
    r=record["8_orthogonal_postselection_collider"]
    assert r["conditional_CHSH"]==4 and r["all_trials_random_noclick_CHSH"]<=2


def test_skin_metric_is_not_right_metric(record):
    r=record["6_orthogonal_nonhermitian_skin"]
    assert r["OBC_similarity_to_real_symmetric_verified"]
    assert r["OBC_mean_right_eigenstate_center"]<3
    assert abs(r["OBC_biorthogonal_mean_center"]-r["symmetric_control_center"])<1e-10
    assert r["OBC_similarity_condition_number"]>1e8

def test_quasiperiodic_scaling_not_just_one_size(record):
    e=record["7_orthogonal_quasiperiodic_localization"]["effective_IPR_decay_exponents"]
    assert e["1"]>e["2"]>e["3"]>=0

def test_setting_independent_herald_does_not_fake_PR(record):
    r=record["8_orthogonal_postselection_collider"]
    assert r["setting_independent_herald_control_CHSH"]==2
