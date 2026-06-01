from __future__ import annotations

from analysis.w33_a5_orbital_negative_polar_nogo import (
    a5_orbital_negative_polar_nogo_packet,
)


PACKET = a5_orbital_negative_polar_nogo_packet()


def test_mdclxxxv_global_orbital_nogo() -> None:
    assert PACKET["part"] == "MMCCCLXVIII"
    assert PACKET["n_pair_orbitals"] == 16
    assert PACKET["n_verified"] == 10
    assert all(PACKET["checks"].values())


def test_mdclxxxv_rook_and_orbital_solution() -> None:
    assert PACKET["raw_rook_orbit_indices"] == [0, 1, 5, 6, 10, 14]
    assert PACKET["raw_rook_edge_count"] == 180
    assert PACKET["a5_orbital_srg_solution_count"] == 1
    assert PACKET["a5_orbital_srg_solution_indices"] == [0, 1, 2, 5, 6, 7, 10, 12, 14]
    assert PACKET["a5_orbital_srg_extra_indices_beyond_rook"] == [2, 7, 12]


def test_mdclxxxv_a5_solution_has_target_parameters_but_wrong_cliques() -> None:
    assert PACKET["a5_orbital_srg_parameters"] == {
        "vertices": 36,
        "degree_profile": {"15": 36},
        "edge_count": 270,
        "adjacent_common_neighbor_profile": {"6": 270},
        "nonadjacent_common_neighbor_profile": {"6": 360},
    }
    assert PACKET["a5_orbital_srg_clique_number"] == 6
    assert PACKET["w33_negative_polar_clique_number"] == 4
    assert PACKET["negative_polar_model_clique_number"] == 4


def test_mdclxxxv_boundary_is_diagonal_a5_only() -> None:
    assert "unique diagonal-A5 orbital union" in PACKET["selector_nogo"]
    assert "does not rule out a non-diagonal A5 subgroup" in PACKET["claim_boundary"]
    assert "genuine negative-polar/symplectic twist" in PACKET["reading"]
