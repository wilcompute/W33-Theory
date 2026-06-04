from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_171_gap_full_e6_outer_lift import (  # noqa: E402
    gap_full_e6_outer_lift_packet,
)


PACKET = gap_full_e6_outer_lift_packet()


def test_bt171_lifts_projective_half_to_full_w_e6() -> None:
    assert PACKET["projective_order"] == 25_920
    assert PACKET["full_order"] == 51_840
    assert PACKET["h4_structure"] == "O(5,3)"
    assert PACKET["h5_structure"] == "O(5,3) : C2"


def test_bt171_full_stabilizer_cascade() -> None:
    assert PACKET["point_count"] == 45
    assert PACKET["line_count"] == 27
    assert PACKET["full_point_stabilizer"] == 1_152
    assert PACKET["full_line_stabilizer"] == 1_920
    assert PACKET["full_point_stabilizer_suborbits"] == [1, 12, 32]


def test_bt171_outer_involution_witness() -> None:
    assert PACKET["outer_order"] == 2
    assert sorted(PACKET["outer_permutation_zero_based"]) == list(range(45))
    assert PACKET["outer_cycle_structure_zero_based"]["cycle_length_distribution"] == {
        1: 7,
        2: 19,
    }


def test_bt171_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 20
    assert all(PACKET["checks"].values())


if __name__ == "__main__":
    test_bt171_lifts_projective_half_to_full_w_e6()
    test_bt171_full_stabilizer_cascade()
    test_bt171_outer_involution_witness()
    test_bt171_all_checks_pass()
