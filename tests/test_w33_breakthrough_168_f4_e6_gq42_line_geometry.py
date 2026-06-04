from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_168_f4_e6_gq42_line_geometry import (  # noqa: E402
    f4_e6_gq42_line_geometry_packet,
)


PACKET = f4_e6_gq42_line_geometry_packet()


def test_bt168_gq42_counts() -> None:
    assert PACKET["point_count"] == 45
    assert PACKET["line_count"] == 27
    assert PACKET["line_size_distribution"] == {5: 27}
    assert PACKET["point_line_incidence_distribution"] == {3: 45}
    assert PACKET["incidence_count"] == 135


def test_bt168_lines_reconstruct_orbital_edges() -> None:
    assert PACKET["degree_distribution"] == {12: 45}
    assert PACKET["edge_count"] == 270
    assert PACKET["edge_line_incidence_distribution"] == {1: 270}
    assert PACKET["nonedge_line_incidence_distribution"] == {0: 720}


def test_bt168_gq_axiom_and_intersections() -> None:
    assert PACKET["line_intersection_distribution"] == {0: 216, 1: 135}
    assert PACKET["gq_axiom_holds"] is True
    assert PACKET["gq_parameters"] == {"s": 4, "t": 2, "points": 45, "lines": 27}


def test_bt168_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 13
    assert all(PACKET["checks"].values())


if __name__ == "__main__":
    test_bt168_gq42_counts()
    test_bt168_lines_reconstruct_orbital_edges()
    test_bt168_gq_axiom_and_intersections()
    test_bt168_all_checks_pass()
