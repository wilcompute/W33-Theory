from __future__ import annotations

from analysis.w33_spread_negative_polar_selector_signature import (
    spread_negative_polar_selector_signature_packet,
)


PACKET = spread_negative_polar_selector_signature_packet()


def test_mdclxxxiv_global_negative_polar_signature() -> None:
    assert PACKET["selector_signature"] == (
        "W33 spreads form NO^-(6,2), not a Latin-square third direction on the 6x6 Clifford grid"
    )
    assert PACKET["n_verified"] == 9
    assert all(PACKET["checks"].values())


def test_mdclxxxiv_w33_and_negative_polar_graphs_match() -> None:
    expected = {
        "vertices": 36,
        "degree_profile": {"15": 36},
        "edge_count": 270,
        "adjacent_common_neighbor_profile": {"6": 270},
        "nonadjacent_common_neighbor_profile": {"6": 360},
    }
    assert PACKET["w33_spread_graph_parameters"] == expected
    assert PACKET["negative_polar_graph_parameters"] == expected
    assert len(PACKET["w33_to_negative_polar_isomorphism"]) == 36
    assert sorted(PACKET["w33_to_negative_polar_isomorphism"]) == list(range(36))


def test_mdclxxxiv_latin_square_selector_is_obstructed() -> None:
    assert PACKET["w33_spread_clique_number"] == 4
    assert PACKET["w33_spread_independence_number"] == 5
    assert PACKET["raw_rook_clique_number"] == 6
    assert PACKET["checks"]["latin_square_third_direction_is_obstructed"]


def test_mdclxxxiv_we6_order_and_boundary() -> None:
    assert PACKET["negative_polar_vertex_count"] == 36
    assert PACKET["negative_polar_quadratic_form"] == "Q=x0*x1+x2*x3+x4+x4*x5+x5 over F2"
    assert PACKET["o_minus_6_2_order"] == 51840
    assert "does not yet lift the A5 antipodal torsor" in PACKET["claim_boundary"]
