from __future__ import annotations

from analysis.w33_self_entangled_qutrit_q4_router import (
    self_entangled_qutrit_q4_router_packet,
)


PACKET = self_entangled_qutrit_q4_router_packet()


def test_mclxxx_self_entangled_qutrit_context_square() -> None:
    qutrit = PACKET["self_entangled_qutrit_input"]
    board = PACKET["context_square_board"]

    assert qutrit["q"] == 3
    assert qutrit["history_cells"] == 9
    assert qutrit["now_context_rays"] == 4
    assert qutrit["erased_single_qutrit_nonidentity_paulis"] == 8
    assert qutrit["w33_projective_rays"] == 40
    assert qutrit["w33_edges"] == 240

    assert board["side_length"] == 4
    assert board["vertices"] == 16
    assert board["toroidal_boundary"] is True


def test_mclxxx_q4_network_metrics() -> None:
    router = PACKET["q4_router"]

    assert router["vertices"] == 16
    assert router["degree"] == 4
    assert router["edges"] == 32
    assert router["diameter"] == 4
    assert router["parity_partition"] == {"even": 8, "odd": 8}
    assert router["spectrum"] == {4: 1, 2: 4, 0: 6, -2: 4, -4: 1}
    assert router["square_faces"] == 24
    assert router["dimension_edge_counts"] == {0: 8, 1: 8, 2: 8, 3: 8}


def test_mclxxx_toroidal_knight_edges_are_q4_edges() -> None:
    iso = PACKET["knight_to_q4_isomorphism"]

    assert iso["mapped_edges_equal_q4_edges"] is True
    assert len(iso["mapping"]) == 16
    assert iso["mapping"]["(0, 0)"] == (0, 0, 0, 0)
    assert iso["mapping"]["(2, 2)"] == (1, 1, 1, 1)


def test_mclxxx_knight_tour_is_gray_hamilton_clock() -> None:
    clock = PACKET["gray_knight_clock"]

    assert len(clock["knight_tour"]) == 16
    assert len({tuple(vertex) for vertex in clock["q4_tour"]}) == 16
    assert clock["flip_sequence"] == [1, 2, 1, 3, 1, 2, 1, 0] * 2
    assert clock["flip_counts"] == {0: 2, 1: 8, 2: 4, 3: 2}


def test_mclxxx_bridge_boundary_keeps_q4_as_router() -> None:
    bridge = PACKET["ternary_binary_bridge"]

    assert bridge["payload"] == "self-entangled qutrit / F3^4 W33 Pauli geometry"
    assert bridge["router"] == "binary Q4 hypercube network on the 4x4 toroidal now-context square"
    assert bridge["key_identity"] == "4 now rays -> 4 Q4 dimensions; 8 erased Pauli directions -> 8 edges per dimension"
    assert "not a replacement for W33" in bridge["boundary"]


def test_mclxxx_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 18
    assert all(PACKET["checks"].values())
