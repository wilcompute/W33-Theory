from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_166_optimal_macro_e6_trace1_receipt import (  # noqa: E402
    optimal_macro_e6_trace1_receipt_packet,
)


PACKET = optimal_macro_e6_trace1_receipt_packet()


def test_bt166_best_pair_is_unique_inverse_pair() -> None:
    assert PACKET["best_depth_6_count"] == 890
    assert len(PACKET["best_macros"]) == 2
    assert PACKET["best_pair_inverse"] is True
    assert [row["index"] for row in PACKET["best_macros"]] == [51706, 51765]


def test_bt166_best_pair_lives_in_e6_trace1_shell() -> None:
    for row in PACKET["best_macros"]:
        assert row["boundary"] == "outside"
        assert row["polarization"] == "mixed"
        assert row["trace_mod3"] == 1
        assert row["order"] == 9


def test_bt166_outside_trace1_order9_profile() -> None:
    assert PACKET["outside_trace1_count"] == 26
    assert PACKET["outside_trace1_order9_count"] == 14
    assert PACKET["outside_trace1_order9_depth_distribution"] == {
        890: 2,
        1217: 2,
        1448: 2,
        1572: 2,
        1915: 2,
        2360: 2,
        3375: 2,
    }


def test_bt166_quality_profiles_keep_best_outside() -> None:
    assert PACKET["quality_by_boundary_trace"]["('inside', 0)"]["min"] > 890
    assert PACKET["quality_by_boundary_trace"]["('outside', 0)"]["min"] > 890
    assert PACKET["quality_by_boundary_trace"]["('outside', 2)"]["min"] > 890


def test_bt166_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 16
    assert all(PACKET["checks"].values())


if __name__ == "__main__":
    test_bt166_best_pair_is_unique_inverse_pair()
    test_bt166_best_pair_lives_in_e6_trace1_shell()
    test_bt166_outside_trace1_order9_profile()
    test_bt166_quality_profiles_keep_best_outside()
    test_bt166_all_checks_pass()
