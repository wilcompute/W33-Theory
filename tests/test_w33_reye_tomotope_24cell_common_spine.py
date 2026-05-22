from __future__ import annotations

from analysis.w33_reye_tomotope_24cell_common_spine import (
    reye_tomotope_24cell_common_spine_packet,
)


PACKET = reye_tomotope_24cell_common_spine_packet()


def test_mcxcIII_twenty_four_cell_reye_model() -> None:
    model = PACKET["twenty_four_cell_model"]

    assert model["vertices"] == 24
    assert model["d4_root_formula"] == "permutations of (+/-1,+/-1,0,0)"
    assert model["axes"] == 12
    assert model["hexagon_planes"] == 16
    assert model["axis_hexagon_incidences"] == 48
    assert model["degree_profile"] == {3: 16, 4: 12}
    assert model["automorphism_count"] == 576


def test_mcxcIII_tomotope_and_24cell_have_same_reye_spine() -> None:
    match = PACKET["tomotope_match"]

    assert match["tomotope_edges"] == 12
    assert match["tomotope_triangles"] == 16
    assert match["tomotope_medial_incidences"] == 48
    assert match["tomotope_automorphism_order"] == 96
    assert match["reye_automorphism_over_tomotope_automorphism"] == 6


def test_mcxcIII_symmetry_lock() -> None:
    lock = PACKET["symmetry_lock"]

    assert lock["reye_automorphism_order"] == 576
    assert lock["twenty_four_cell_rotational_symmetry_order"] == 576
    assert lock["weyl_f4_order"] == 1152
    assert lock["identity"] == "576 = 6*96 = |W(F4)|/2"


def test_mcxcIII_horizon_anchor_uses_same_reye_spine() -> None:
    anchor = PACKET["horizon_anchor"]

    assert anchor["mcxcii_k12_reye_points"] == 12
    assert anchor["mcxcii_k12_reye_lines"] == 16
    assert "K12 horizon" in anchor["reading"]


def test_mcxcIII_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 18
    assert all(PACKET["checks"].values())
