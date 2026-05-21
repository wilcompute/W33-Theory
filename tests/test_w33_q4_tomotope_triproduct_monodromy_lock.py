from __future__ import annotations

from analysis.w33_q4_tomotope_triproduct_monodromy_lock import (
    q4_tomotope_triproduct_monodromy_lock_packet,
)


def test_mclxxxv_triproduct_packets() -> None:
    packet = q4_tomotope_triproduct_monodromy_lock_packet()

    assert packet["router_packet"] == {
        "q4_vertices": 16,
        "q4_faces": 24,
        "medial_incidences": 48,
        "triproduct": 18432,
        "identity": "16*24*48 = 18432",
    }
    assert packet["tomotope_packet"] == {
        "tomotope_edges": 12,
        "tomotope_triangles": 16,
        "tomotope_automorphism": 96,
        "triproduct": 18432,
        "identity": "12*16*96 = 18432",
    }
    assert packet["lock"] == {
        "monodromy": 18432,
        "identity": "18432 = 16*24*48 = 12*16*96",
    }


def test_mclxxxv_all_checks_pass() -> None:
    packet = q4_tomotope_triproduct_monodromy_lock_packet()

    assert packet["checks"] == {
        "router_triproduct_matches_monodromy": True,
        "tomotope_triproduct_matches_monodromy": True,
        "router_and_tomotope_triproducts_match": True,
        "router_triproduct_identity": True,
        "tomotope_triproduct_identity": True,
        "monodromy_is_18432": True,
        "monodromy_over_q4_vertices_is_face_medial_sheet": True,
        "monodromy_over_tomotope_edges_is_triangle_aut_sheet": True,
        "q4_face_to_tomotope_edge_ratio_is_2": True,
        "q4_vertex_to_tomotope_triangle_ratio_is_1": True,
    }
    assert packet["n_verified"] == 10
