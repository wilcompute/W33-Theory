from __future__ import annotations

from analysis.w33_bridge_line_affine_cayley_cube import (
    bridge_line_affine_cayley_cube_packet,
)


PACKET = bridge_line_affine_cayley_cube_packet()


def test_mmccclxxi_all_checks_verify() -> None:
    assert PACKET["part"] == "MMCCCLXXI"
    assert PACKET["n_verified"] == 12
    assert all(PACKET["checks"].values())


def test_mmccclxxi_bridge_words_are_affine_subspace() -> None:
    assert PACKET["bridge_line_count"] == 27
    assert PACKET["linear_relation"] == "x0 + x1 + 2*x2 + x3 = 0 over F3"
    assert all(profile == {"1": 27} for profile in PACKET["projection_profiles"].values())


def test_mmccclxxi_intersection_graph_profile() -> None:
    graph = PACKET["intersection_graph"]
    assert graph["degree_profile"] == {"8": 27}
    assert graph["edge_count"] == 108
    assert graph["common_neighbor_profiles"] == {
        "adjacent": {"1": 108},
        "nonadjacent": {"2": 162, "4": 81},
    }


def test_mmccclxxi_cayley_model_matches_cdiv_spectrum() -> None:
    cayley = PACKET["cayley_model"]
    assert len(cayley["generators"]) == 8
    assert cayley["spectrum"] == {"-4": 6, "-1": 8, "2": 12, "8": 1}
    assert cayley["standardizing_gl3_matrix"] == [[0, 1, 1], [1, 0, 1], [2, 2, 2]]


def test_mmccclxxi_boundary_is_not_coset_map_yet() -> None:
    assert "actual affine qutrit cube" in PACKET["reading"]
    assert "does not identify the four K2,2 cross-pair copies" in PACKET["claim_boundary"]
