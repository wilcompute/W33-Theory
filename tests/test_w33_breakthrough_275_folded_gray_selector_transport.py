from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_275_folded_gray_selector_transport import (  # noqa: E402
    folded_gray_selector_transport_packet,
)


PACKET = folded_gray_selector_transport_packet()


def test_bt275_projection_is_folded_selector_7() -> None:
    assert PACKET["bt176_even_projection"] == [0, 3, 6, 5, 12, 15, 10, 9]
    assert PACKET["selected_selector_7_cycle"] == [3, 6, 5, 12, 9, 10]
    assert PACKET["folded_from_selector_7"] == PACKET["bt176_even_projection"]
    assert PACKET["fold_split"] == {"head": 4, "tail": 2}


def test_bt275_reflected_gray_word_is_exact() -> None:
    assert PACKET["reflected_gray_period"] == [3, 5, 3, 9]
    assert PACKET["target_step_word"] == [3, 5, 3, 9, 3, 5, 3, 9]
    assert PACKET["selected_cycle_step_word"] == [5, 3, 9, 5, 3, 9]
    assert PACKET["cap_directions"] == {
        "real_cap_to_head": 3,
        "head_to_all_ones_cap": 3,
    }


def test_bt275_exact_matches_are_only_inverse_base_14_pair() -> None:
    assert PACKET["cap_splice_search_space"] == 960
    assert PACKET["exact_step_match_count"] == 2
    assert PACKET["exact_projection_match_count"] == 2
    assert [
        (row["selector_index"], row["base_direction"], row["orientation"])
        for row in PACKET["exact_step_matches"]
    ] == [
        (6, 14, "atlas_reverse"),
        (7, 14, "atlas_forward"),
    ]
    assert {tuple(row["projection"]) for row in PACKET["exact_step_matches"]} == {
        tuple(PACKET["bt176_even_projection"])
    }


def test_bt275_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 13
    assert all(PACKET["checks"].values())


if __name__ == "__main__":
    test_bt275_projection_is_folded_selector_7()
    test_bt275_reflected_gray_word_is_exact()
    test_bt275_exact_matches_are_only_inverse_base_14_pair()
    test_bt275_all_checks_pass()
