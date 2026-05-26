from __future__ import annotations

from analysis.w33_toroidal_dual_symmetry_groups import toroidal_dual_symmetry_packet


PACKET = toroidal_dual_symmetry_packet()


def test_mccxlvii_geometric_realizations_keep_c2() -> None:
    geometric = PACKET["symmetry_layers"]["geometric_realizations"]

    assert geometric["repo_recorded_c2_realizations"] == {
        "csaszar_c2_realizations": 5,
        "szilassi_c2_realizations": 2,
        "c2_symmetry_lines": 7,
    }
    assert geometric["coordinate_c2_checks"] == {
        "csaszar_coordinate_c2_preserves_faces": True,
        "szilassi_coordinate_c2_preserves_faces": True,
    }


def test_mccxlvii_abstract_map_group_is_order_42() -> None:
    abstract = PACKET["symmetry_layers"]["abstract_toroidal_maps"]

    assert abstract["csaszar_map_automorphism_order"] == 42
    assert abstract["szilassi_dual_map_automorphism_order"] == 42
    assert abstract["group_shape"] == "C7 semidirect C6 = AGL(1,7), order 42"
    assert abstract["element_order_profile"] == {"1": 1, "2": 7, "3": 14, "6": 14, "7": 6}
    assert abstract["orientation_profile"] == {"orientation_preserving": 42, "orientation_reversing": 0}


def test_mccxlvii_bare_graph_symmetry_is_larger_than_map_symmetry() -> None:
    bare = PACKET["symmetry_layers"]["bare_graphs"]

    assert bare["csaszar_skeleton"] == "K7, graph automorphism S7 if faces are forgotten"
    assert bare["szilassi_skeleton"] == "Heawood graph, graph automorphism PGL_2(7) of order 336"
    assert bare["heawood_to_map_symmetry_ratio"] == 8


def test_mccxlvii_w33_flag_bridge() -> None:
    bridge = PACKET["w33_bridge"]

    assert bridge["single_map_flags"] == 84
    assert bridge["dual_pair_flags"] == 168
    assert bridge["dual_pair_flags_identity"] == "168 = 4*42 = |Aut(Fano)|"
    assert bridge["pointed_split"] == "84 = 72 + 12 for either Csaszar vertex shell or Szilassi face shell"
    assert bridge["tomotope_link"] == "168 + 24 = 192, matching the tomotope flag carrier with tetrahedral 24 added"


def test_mccxlvii_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 14
    assert all(PACKET["checks"].values())
