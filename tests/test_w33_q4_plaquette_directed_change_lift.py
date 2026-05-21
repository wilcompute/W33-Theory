from __future__ import annotations

from analysis.w33_q4_plaquette_directed_change_lift import (
    q4_plaquette_directed_change_packet,
)


PACKET = q4_plaquette_directed_change_packet()


def test_mclxxxi_input_context() -> None:
    context = PACKET["input_context"]

    assert context["q"] == 3
    assert context["history_cells"] == 9
    assert context["directed_change_histories"] == 6
    assert context["now_context_rays"] == 4
    assert context["q4_vertices"] == 16
    assert context["q4_edges"] == 32
    assert context["w33_gap_multiplicity"] == 24


def test_mclxxxi_q4_plaquette_formula() -> None:
    formula = PACKET["plaquette_formula"]

    assert formula["identity"] == "faces(Q4) = C(4,2)*2^(4-2) = 6*4 = 24"
    assert formula["face_count"] == 24
    assert formula["direction_pairs"] == 6
    assert formula["frozen_now_slots"] == 4
    assert formula["directed_change_factor"] == 6
    assert formula["now_context_factor"] == 4


def test_mclxxxi_incidence_laws() -> None:
    laws = PACKET["incidence_laws"]

    assert laws["face_edge_incidence"] == "24 faces * 4 edges = 32 edges * 3 faces = 96"
    assert laws["vertex_face_incidence"] == "24 faces * 4 vertices = 16 vertices * 6 directed changes = 96"
    assert laws["edge_face_counts"] == {3: 32}
    assert laws["vertex_face_counts"] == {6: 16}


def test_mclxxxi_each_directed_change_owns_four_faces() -> None:
    packet = PACKET["directed_change_face_packet"]

    assert packet["directed_changes"] == [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]
    assert packet["direction_pairs"] == [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    assert packet["now_slots"] == [(0, 0), (0, 1), (1, 0), (1, 1)]
    assert [row["face_count"] for row in packet["rows"]] == [4, 4, 4, 4, 4, 4]


def test_mclxxxi_w33_gap_lock() -> None:
    lock = PACKET["w33_lock"]

    assert lock["q4_plaquettes"] == 24
    assert lock["w33_gap_multiplicity"] == 24
    assert lock["su5_adjoint_dimension"] == 24
    assert "positive gap/gauge shell" in lock["reading"]


def test_mclxxxi_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 15
    assert all(PACKET["checks"].values())
