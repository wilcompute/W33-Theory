from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_274_gray_projection_selector_phase_lock import (  # noqa: E402
    gray_projection_selector_phase_lock_packet,
)


PACKET = gray_projection_selector_phase_lock_packet()


def test_bt274_bt176_initial_direction_word() -> None:
    assert PACKET["bt176_even_projection"] == [0, 3, 6, 5, 12, 15, 10, 9]
    assert PACKET["initial_segment_before_all_ones"] == [3, 6, 5, 12]
    assert PACKET["initial_direction_word"] == [5, 3, 9]
    assert PACKET["initial_direction_alphabet"] == [3, 5, 9]


def test_bt274_alphabet_rule_selects_base_14_pair() -> None:
    assert PACKET["alphabet_match_count"] == 2
    assert [row["selector_index"] for row in PACKET["alphabet_match_selectors"]] == [6, 7]
    assert {row["base_direction"] for row in PACKET["alphabet_match_selectors"]} == {14}


def test_bt274_prefix_rule_selects_selector_7() -> None:
    selected = PACKET["selected_selector"]
    assert selected["selector_index"] == 7
    assert selected["base_direction"] == 14
    assert selected["direction_word"][:3] == [5, 3, 9]
    assert selected["moving_cycle"] == [3, 6, 5, 12, 9, 10]


def test_bt274_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 12
    assert all(PACKET["checks"].values())


if __name__ == "__main__":
    test_bt274_bt176_initial_direction_word()
    test_bt274_alphabet_rule_selects_base_14_pair()
    test_bt274_prefix_rule_selects_selector_7()
    test_bt274_all_checks_pass()
