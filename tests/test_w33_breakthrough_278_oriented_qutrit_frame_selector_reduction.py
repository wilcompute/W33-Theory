from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_278_oriented_qutrit_frame_selector_reduction import (  # noqa: E402
    oriented_qutrit_frame_selector_reduction_packet,
)


PACKET = oriented_qutrit_frame_selector_reduction_packet()


def test_bt278_gauge_factorization() -> None:
    assert PACKET["factorization"] == "48 = q! * 2^q = 6 axis orderings * 8 selector lifts"
    assert len(PACKET["axis_sequence_distribution"]) == 6
    assert {row["count"] for row in PACKET["axis_sequence_distribution"]} == {8}


def test_bt278_orientation_halves() -> None:
    assert PACKET["positive_orientation_lift_count"] == 24
    assert PACKET["negative_orientation_lift_count"] == 24
    assert len(PACKET["positive_c3_sequences"]) == 3
    assert len(PACKET["negative_reversal_sequences"]) == 3


def test_bt278_oriented_frame_leaves_selector_count() -> None:
    assert PACKET["selected_positive_axis_sequence"] == [0, 1, 2, 0, 1, 2]
    assert PACKET["selected_positive_lift_count"] == 8
    assert PACKET["bt272_selector_count"] == 8


def test_bt278_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 13
    assert all(PACKET["checks"].values())


if __name__ == "__main__":
    test_bt278_gauge_factorization()
    test_bt278_orientation_halves()
    test_bt278_oriented_frame_leaves_selector_count()
    test_bt278_all_checks_pass()
