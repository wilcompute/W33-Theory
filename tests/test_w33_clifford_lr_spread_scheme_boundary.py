from __future__ import annotations

from analysis.w33_clifford_lr_spread_scheme_boundary import (
    clifford_lr_spread_scheme_boundary_packet,
)


PACKET = clifford_lr_spread_scheme_boundary_packet()


def test_mdclxxxi_global_boundary_identity() -> None:
    assert (
        PACKET["boundary_identity"]
        == "36 Clifford L/R pairs are count-equal to 36 W33 spreads, but their natural schemes differ"
    )
    assert PACKET["n_verified"] == 4
    assert all(PACKET["checks"].values())


def test_mdclxxxi_clifford_lr_grid_scheme() -> None:
    report = PACKET["clifford_lr_report"]
    assert report["n_verified"] == 8
    assert all(report["checks"].values())
    assert report["lr_pair_count"] == 36
    assert report["shared_decagon_count_profile"] == {"2": 36}
    assert report["vertex_union_size_profile"] == {"20": 36}
    assert report["decagon_overlap_profile"] == {"0": 630}
    assert report["vertex_overlap_profile"] == {"0": 180, "4": 450}


def test_mdclxxxi_clifford_zero_overlap_graph_is_rook_scheme() -> None:
    assert PACKET["clifford_lr_report"]["overlap_0_graph"] == {
        "vertices": 36,
        "overlap_value": 0,
        "degree_profile": {"10": 36},
        "edge_count": 180,
        "adjacent_common_neighbor_profile": {"4": 180},
        "nonadjacent_common_neighbor_profile": {"2": 450},
    }
    assert PACKET["clifford_lr_report"]["overlap_4_graph"] == {
        "vertices": 36,
        "overlap_value": 4,
        "degree_profile": {"25": 36},
        "edge_count": 450,
        "adjacent_common_neighbor_profile": {"16": 450},
        "nonadjacent_common_neighbor_profile": {"20": 180},
    }


def test_mdclxxxi_w33_spread_scheme_is_different() -> None:
    report = PACKET["w33_spread_report"]
    assert report["n_verified"] == 4
    assert all(report["checks"].values())
    assert report["spread_count"] == 36
    assert report["spread_overlap_profile"] == {"1": 360, "4": 270}
    assert report["overlap_4_graph"]["degree_profile"] == {"15": 36}
    assert report["overlap_1_graph"]["degree_profile"] == {"20": 36}


def test_mdclxxxi_missing_selector_boundary() -> None:
    assert "count-level correspondence only" in PACKET["claim_boundary"]
    assert "6x6 rook scheme" in PACKET["claim_boundary"]
    assert "extra symplectic selector" in PACKET["reading"]
