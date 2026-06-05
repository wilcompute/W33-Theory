from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_321_q4_reye_complement_lift_duality import (  # noqa: E402
    COMPLEMENT_INVOLUTION,
    q4_reye_complement_lift_duality_packet,
)


PACKET = q4_reye_complement_lift_duality_packet()


def test_bt321_kappa_vertex_orbits() -> None:
    assert PACKET["kappa"]["row_masks"] == [14, 13, 11, 7]
    assert COMPLEMENT_INVOLUTION == (14, 13, 11, 7)
    assert len(PACKET["vertex_action"]["fixed_vertices"]) == 8
    assert len(PACKET["vertex_action"]["moved_vertices"]) == 8
    assert PACKET["vertex_action"]["orbit_size_distribution"] == {1: 8, 2: 4}


def test_bt321_axis_action_is_reye_invisible() -> None:
    assert len(PACKET["axis_action"]["axes"]) == 8
    assert len(PACKET["axis_action"]["even_axes_pointwise_fixed"]) == 4
    assert len(PACKET["axis_action"]["odd_axes_endpoint_swapped"]) == 4
    assert PACKET["axis_action"]["quotient_action"] == "identity on all 8 antipodal axes"


def test_bt321_lift_duality_counts() -> None:
    lift = PACKET["lift_duality"]
    assert lift["q4_edges"] == 32
    assert lift["distance3_body_diagonals"] == 32
    assert lift["quotient_edges"] == 16
    for profile in lift["profiles"].values():
        assert len(profile["q4_edge_lifts"]) == 2
        assert len(profile["distance3_diagonal_lifts"]) == 2
        assert len(profile["all_cross_pairs"]) == 4


def test_bt321_cubical_cell_layer() -> None:
    layer = PACKET["cubical_cell_layer"]
    assert layer["cubical_3faces"] == 8
    assert layer["body_diagonals_total"] == 32
    assert layer["body_diagonals_per_face"] == [4] * 8


def test_bt321_tomotope_reye_fvector() -> None:
    reading = PACKET["tomotope_reye_reading"]
    assert reading["hinge_axis"] == 0
    assert len(reading["affine_point_axes"]) == 4
    assert len(reading["direction_axes"]) == 3
    assert reading["f_vector"] == [4, 12, 16, 8]


def test_bt321_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 24
    assert all(PACKET["checks"].values())


if __name__ == "__main__":
    test_bt321_kappa_vertex_orbits()
    test_bt321_axis_action_is_reye_invisible()
    test_bt321_lift_duality_counts()
    test_bt321_cubical_cell_layer()
    test_bt321_tomotope_reye_fvector()
    test_bt321_all_checks_pass()
