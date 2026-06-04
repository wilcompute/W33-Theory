from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_172_outer_involution_temporal_qutrit import (  # noqa: E402
    outer_involution_temporal_qutrit_packet,
)


PACKET = outer_involution_temporal_qutrit_packet()


def test_bt172_fixed_heptad_now_fan() -> None:
    assert len(PACKET["fixed_points"]) == 7
    assert PACKET["now_point"] in PACKET["fixed_points"]
    assert PACKET["fixed_degrees"][PACKET["now_point"]] == 6
    assert len(PACKET["fixed_edges"]) == 9


def test_bt172_fixed_lines_are_temporal_axes() -> None:
    assert len(PACKET["fixed_lines"]) == 3
    assert all(
        PACKET["now_point"] in points
        for points in PACKET["fixed_line_fixed_points"].values()
    )
    assert all(len(points) == 3 for points in PACKET["fixed_line_fixed_points"].values())


def test_bt172_past_future_pairs_split_as_q_mu_k() -> None:
    assert PACKET["point_cycle_length_distribution"] == {1: 7, 2: 19}
    assert PACKET["named_pair_classes"] == {
        "axis_past_future_pairs_q": 3,
        "off_axis_rich_pairs_mu": 4,
        "residual_pairs_k": 12,
    }


def test_bt172_line_orbits_split_as_q_and_k() -> None:
    assert PACKET["line_cycle_length_distribution"] == {1: 3, 2: 12}
    assert PACKET["line_orbit_signature"]["(1, (3,))"] == 3
    assert PACKET["line_orbit_signature"]["(2, (1, 1))"] == 6
    assert PACKET["line_orbit_signature"]["(2, (0, 0))"] == 6


def test_bt172_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 15
    assert all(PACKET["checks"].values())


if __name__ == "__main__":
    test_bt172_fixed_heptad_now_fan()
    test_bt172_fixed_lines_are_temporal_axes()
    test_bt172_past_future_pairs_split_as_q_mu_k()
    test_bt172_line_orbits_split_as_q_and_k()
    test_bt172_all_checks_pass()
