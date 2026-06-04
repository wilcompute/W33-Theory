from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_154_4x4_lattice_n4_generalization import (
    lattice_4x4_packet,
)


PACKET = lattice_4x4_packet()


def test_bt154_cl4_frame_identity() -> None:
    assert PACKET["n_cells"] == 16
    assert PACKET["clifford_grade_profile"] == [1, 4, 6, 4, 1]
    assert sum(PACKET["clifford_grade_profile"]) == 16
    assert PACKET["even_grade_count"] == 8
    assert PACKET["odd_grade_count"] == 8


def test_bt154_seed_spacing_and_directed_state_budget() -> None:
    assert PACKET["seed_grid"][1][2] == 661
    assert PACKET["min_seed_spacing"] == 100
    assert PACKET["expected_cross_talk"] == 0
    assert PACKET["directed_state_total"] == 7680


def test_bt154_scaling_boundary_is_explicit() -> None:
    assert PACKET["full_4d_toric_cells"] == 81
    assert PACKET["n_cells"] < PACKET["full_4d_toric_cells"]
    assert "operator-basis frame" in PACKET["reading"]
    assert "not a claim" in PACKET["reading"]


def test_bt154_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 12
    assert all(PACKET["checks"].values())


if __name__ == "__main__":
    test_bt154_cl4_frame_identity()
    test_bt154_seed_spacing_and_directed_state_budget()
    test_bt154_scaling_boundary_is_explicit()
    test_bt154_all_checks_pass()
