from __future__ import annotations

from analysis.w33_boerdijk_gamma_brass_steiner_return_graph import (
    boerdijk_gamma_brass_steiner_return_graph_packet,
)


PACKET = boerdijk_gamma_brass_steiner_return_graph_packet()


def test_mcccxcviii_global_return_identity() -> None:
    assert (
        PACKET["return_identity"]
        == "240 Steiner trihedra -> 40 components x 6 trihedra -> srg(40,12,2,4)"
    )
    assert PACKET["n_verified"] == 4
    assert all(PACKET["checks"].values())
    assert len(PACKET["matter_sector_reports"]) == 8


def test_mcccxcviii_disjoint_cover_components() -> None:
    for report in PACKET["matter_sector_reports"]:
        assert report["n_verified"] == 8
        assert all(report["checks"].values())
        assert report["trihedron_count"] == 240
        assert report["component_count"] == 40
        assert report["component_profiles"]["component_size_profile"] == {"6": 40}
        assert report["component_profiles"]["cover_group_count_profile"] == {"3": 40}
        assert report["component_profiles"]["cover_union_size_profile"] == {"27": 40}
        assert report["component_profiles"]["component_tritangent_count_profile"] == {"18": 40}


def test_mcccxcviii_return_graph_has_w33_srg_parameters() -> None:
    for report in PACKET["matter_sector_reports"]:
        assert report["intersection_9_graph"] == {
            "relation": "component_tritangent_intersection_9",
            "vertices": 40,
            "degree_profile": {"12": 40},
            "edge_count": 240,
            "adjacent_common_neighbor_profile": {"2": 240},
            "nonadjacent_common_neighbor_profile": {"4": 540},
        }
        assert report["intersection_6_graph"] == {
            "relation": "component_tritangent_intersection_6",
            "vertices": 40,
            "degree_profile": {"27": 40},
            "edge_count": 540,
            "adjacent_common_neighbor_profile": {"18": 540},
            "nonadjacent_common_neighbor_profile": {"18": 240},
        }


def test_mcccxcviii_gamma_brass_source_count_dictionary() -> None:
    external = PACKET["external_count_dictionary"]
    assert external["n_verified"] == 12
    assert all(external["checks"].values())
    gamma = external["source_facts"]["gamma_brass_2004"]["counts"]
    assert gamma["cluster_atoms"] == 26
    assert gamma["augmented_cluster_atoms"] == 38
    assert gamma["augmented_cluster_tetrahedra"] == 81
    assert gamma["original_helix_local_neighbors"] == 12
    assert gamma["initial_tetrahedron_shared_icosahedra"] == 4


def test_mcccxcviii_six_hundred_cell_count_dictionary() -> None:
    external = PACKET["external_count_dictionary"]
    cell = external["source_facts"]["regular_600_cell"]["counts"]
    assert cell["vertices"] == 120
    assert cell["edges"] == 720
    assert cell["tetrahedral_cells"] == 600
    assert cell["boerdijk_coxeter_ring_count"] == 20
    assert cell["tetrahedra_per_ring"] == 30


def test_mcccxcviii_claim_boundary() -> None:
    assert "no canonical isomorphism" in PACKET["claim_boundary"]
    assert "source-count dictionary" in PACKET["claim_boundary"]
