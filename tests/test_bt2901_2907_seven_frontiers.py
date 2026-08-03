from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "bt2901_2907", ROOT / "analysis" / "bt2901_2907_seven_frontiers.py"
)
assert SPEC and SPEC.loader
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


@pytest.fixture(scope="session")
def packet():
    return MOD.build_result()


def by_schema(packet, suffix):
    return next(p for p in packet["packets"] if p["schema"].endswith(suffix))


def test_pass2901_affine_line_torsor(packet):
    p = by_schema(packet, "intrinsic_channel_torsor.v1")
    assert p["group_orders"] == {
        "PSp_projective_action": 25920,
        "PGSp_projective_action": 51840,
    }
    assert len(p["sample"]["sp_induced_permutations"]) == 3
    assert len(p["sample"]["pgsp_induced_permutations"]) == 6


def test_pass2902_butterfly_engine(packet):
    p = by_schema(packet, "q3_hadamard_engine.v1")
    assert p["architecture"]["latency_model_cycles"] == 47
    assert p["architecture"]["dense_serial_reference_cycles"] == 225
    assert p["architecture"]["exact_cycle_saving"] == "178/225"


def test_pass2903_observer_congruences(packet):
    p = by_schema(packet, "observer_congruence_atlas.v1")
    full = next(r for r in p["operation_subset_atlas"] if len(r["operations"]) == 4)
    assert full["class_counts"] == [16, 40, 78, 81]
    assert full["stable_dimension"] == 81
    assert len(p["minimal_full_state_generator_sets"]) == 2


def test_pass2904_regular_twisted_action(packet):
    p = by_schema(packet, "regular_token_group.v1")
    assert p["natural_embedding"]["orbit_sizes"] == [48, 48]
    assert p["determinant_twisted_embedding"]["orbit_size"] == 96
    assert p["determinant_twisted_embedding"]["stabilizer_order"] == 1


def test_pass2905_optimal_passage_cycle(packet):
    p = by_schema(packet, "first_passage_scheduler.v1")
    assert p["optimal_cost"] == "315"
    assert p["rooted_optimal_cycle_count"] == 8336
    assert len(p["optimal_cycle"]) == 16


def test_pass2906_singer_gap(packet):
    p = by_schema(packet, "nonlinear_scheduler_singer_gap.v1")
    assert p["singer_element_count"] == 2688
    assert p["best_singer_cost"] == "1317/4"
    assert p["exact_gap"] == "57/4"


def test_pass2907_observer_mirage_falsifier(packet):
    p = by_schema(packet, "observer40_mirage_falsifier.v1")
    assert p["class_size_histogram"] == {"1": 7, "2": 29, "4": 4}
    assert p["ambiguous_orthogonality_unordered_pairs"] == 216
    assert p["W33_hits"] == 0
