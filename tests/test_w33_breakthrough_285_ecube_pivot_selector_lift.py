from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_285_ecube_pivot_selector_lift import (  # noqa: E402
    ecube_pivot_selector_lift_packet,
)


PACKET = ecube_pivot_selector_lift_packet()


def test_bt285_ecube_pivot_word() -> None:
    assert PACKET["gray_step_word"] == [1, 2, 1, 4, 1, 2, 1, 8, 1, 2, 1, 4, 1, 2, 1, 8]
    assert PACKET["even_step_word"] == [3, 5, 3, 9, 3, 5, 3, 9]
    assert all(pair[0] == 1 for pair in PACKET["two_hop_pairs"])


def test_bt285_scalar_to_now_deletes_cap_edges() -> None:
    assert PACKET["scalar_to_now_path"] == [0, 3, 6, 5, 12, 15]
    assert PACKET["scalar_to_now_word"] == [3, 5, 3, 9, 3]
    assert PACKET["cap_direction"] == 3
    assert PACKET["internal_q_word"] == [5, 3, 9]


def test_bt285_ecube_pivot_selects_base14_selector7() -> None:
    assert PACKET["pivot_base_direction"] == 14
    assert [
        (row["selector_index"], row["prefix_matches"])
        for row in PACKET["base14_orientations"]
    ] == [(6, False), (7, True)]
    assert PACKET["selected_selector"]["selector_index"] == 7


def test_bt285_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 15
    assert all(PACKET["checks"].values())


if __name__ == "__main__":
    test_bt285_ecube_pivot_word()
    test_bt285_scalar_to_now_deletes_cap_edges()
    test_bt285_ecube_pivot_selects_base14_selector7()
    test_bt285_all_checks_pass()
