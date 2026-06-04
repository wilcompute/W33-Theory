from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_276_now_fan_cap_pullback import (  # noqa: E402
    now_fan_cap_pullback_packet,
)


PACKET = now_fan_cap_pullback_packet()


def test_bt276_caps_and_moving_units() -> None:
    assert PACKET["bt275_caps"] == {
        "real_scalar_cap": 0,
        "now_cap_all_ones": 15,
        "moving_units": [3, 6, 5, 12, 9, 10],
    }
    assert PACKET["bt172_now_fan"]["now_point"] == 44
    assert len(PACKET["bt172_now_fan"]["peripheral_fixed_points"]) == 6


def test_bt276_four_cells_are_peripheral_anchors() -> None:
    anchors = [row["anchor_fixed_point"] for row in PACKET["four_cell_rows"]]
    assert anchors == [41, 3, 4, 1, 2, 0]
    assert sorted(anchors) == PACKET["bt172_now_fan"]["peripheral_fixed_points"]
    assert 44 not in anchors


def test_bt276_line_orbits_match_same_anchors() -> None:
    orbit_anchors = sorted(row["anchor"] for row in PACKET["one_anchor_line_orbits"])
    assert orbit_anchors == PACKET["bt172_now_fan"]["peripheral_fixed_points"]
    assert all(
        len(row["incident_one_anchor_line_orbits"]) == 1
        for row in PACKET["four_cell_rows"]
    )


def test_bt276_clock_table_and_option_word() -> None:
    assert [
        row["moving_unit"] for row in PACKET["clock_to_four_cell_table"]
    ] == [3, 6, 5, 12, 9, 10]
    assert [
        row["anchor_fixed_point"] for row in PACKET["clock_to_four_cell_table"]
    ] == [41, 3, 4, 1, 2, 0]
    assert PACKET["selected_option_word_bt173_order"] == [0, 0, 0, 0, 0, 1]


def test_bt276_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 15
    assert all(PACKET["checks"].values())


if __name__ == "__main__":
    test_bt276_caps_and_moving_units()
    test_bt276_four_cells_are_peripheral_anchors()
    test_bt276_line_orbits_match_same_anchors()
    test_bt276_clock_table_and_option_word()
    test_bt276_all_checks_pass()
