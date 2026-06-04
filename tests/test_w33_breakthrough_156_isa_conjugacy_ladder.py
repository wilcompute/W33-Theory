from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_156_isa_conjugacy_ladder import (
    isa_conjugacy_ladder_packet,
)


PACKET = isa_conjugacy_ladder_packet()


def test_bt156_class_ladder_is_exact() -> None:
    assert PACKET["class_ladder"] == {
        "PSp(4,3)_projective": 20,
        "W(E6)_geometric": 25,
        "E8_Coxeter_cadence": 30,
        "Sp(4,3)_Clifford_lift": 34,
    }


def test_bt156_dispatch_model_corrects_fast_path_count() -> None:
    dispatch = PACKET["dispatch_model"]

    assert dispatch["geometric_fast_paths"] == 25
    assert dispatch["coxeter_epoch_slots"] == 30
    assert dispatch["lifted_clifford_refinements"] == 34
    assert dispatch["generator_lanes"] == 8


def test_bt156_substrate_gaps() -> None:
    ladder = PACKET["class_ladder"]

    assert ladder["W(E6)_geometric"] - ladder["PSp(4,3)_projective"] == 5
    assert ladder["E8_Coxeter_cadence"] - ladder["W(E6)_geometric"] == 5
    assert ladder["Sp(4,3)_Clifford_lift"] - ladder["E8_Coxeter_cadence"] == 4
    assert ladder["Sp(4,3)_Clifford_lift"] - ladder["W(E6)_geometric"] == 9


def test_bt156_boundary_says_30_is_not_conjugacy_count() -> None:
    correction = PACKET["architectural_correction"]

    assert "25 W(E6) geometric classes" in correction
    assert "30 is the E8 Coxeter cadence" in correction
    assert "not the ordinary conjugacy-class count" in correction


def test_bt156_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 12
    assert all(PACKET["checks"].values())


if __name__ == "__main__":
    test_bt156_class_ladder_is_exact()
    test_bt156_dispatch_model_corrects_fast_path_count()
    test_bt156_substrate_gaps()
    test_bt156_boundary_says_30_is_not_conjugacy_count()
    test_bt156_all_checks_pass()
