from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_158_macro_tail_sieve import macro_tail_sieve_packet


PACKET = macro_tail_sieve_packet()


def test_bt158_tail_sieve_counts() -> None:
    assert PACKET["tail_size"] == 151
    assert PACKET["admissible_macro_count"] == 143
    assert PACKET["forbidden_macro_count"] == 8


def test_bt158_forbidden_binary_pocket() -> None:
    assert PACKET["failure_trace_distribution"] == {0: 8}
    assert PACKET["failure_order_distribution"] == {2: 4, 12: 4}
    assert all(row["diameter"] == 7 for row in PACKET["forbidden_macros"])


def test_bt158_best_macros_are_order9_trace1() -> None:
    best = PACKET["best_macros"]

    assert len(best) == 2
    assert all(row["depth_6_count"] == 890 for row in best)
    assert all(row["order"] == 9 for row in best)
    assert all(row["trace_mod3"] == 1 for row in best)


def test_bt158_admissible_distribution() -> None:
    assert PACKET["success_order_distribution"] == {
        2: 1,
        4: 6,
        5: 6,
        6: 52,
        8: 14,
        9: 14,
        10: 6,
        12: 42,
        18: 2,
    }


def test_bt158_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 12
    assert all(PACKET["checks"].values())


if __name__ == "__main__":
    test_bt158_tail_sieve_counts()
    test_bt158_forbidden_binary_pocket()
    test_bt158_best_macros_are_order9_trace1()
    test_bt158_admissible_distribution()
    test_bt158_all_checks_pass()
