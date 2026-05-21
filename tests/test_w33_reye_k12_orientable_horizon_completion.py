from __future__ import annotations

from analysis.w33_reye_k12_orientable_horizon_completion import (
    reye_k12_orientable_horizon_completion_packet,
)


PACKET = reye_k12_orientable_horizon_completion_packet()


def test_mcxcii_input_anchor_is_mclxxxii_reye_tomotope_layer() -> None:
    anchor = PACKET["input_anchor"]

    assert anchor["q4_antipodal_quotient"] == "MCLXXXII"
    assert anchor["reye_points"] == 12
    assert anchor["reye_lines"] == 16
    assert anchor["tomotope_medial_incidences"] == 48


def test_mcxcii_oriented_completion_contains_reye_and_residual_faces() -> None:
    completion = PACKET["oriented_completion"]

    assert completion["vertices"] == 12
    assert completion["edges"] == 66
    assert completion["reye_triangles"] == 16
    assert completion["residual_triangles"] == 28
    assert completion["total_triangles"] == 44
    assert completion["directed_edge_count"] == 132
    assert completion["reye_pair_profile"] == {0: 18, 1: 48}


def test_mcxcii_completion_is_orientable_twofold_triple_system() -> None:
    completion = PACKET["oriented_completion"]

    assert completion["directed_edge_profile"] == {1: 132}
    assert completion["unordered_edge_profile"] == {2: 66}


def test_mcxcii_surface_is_k12_genus_six_horizon() -> None:
    surface = PACKET["surface"]

    assert surface["V"] == 12
    assert surface["E"] == 66
    assert surface["F"] == 44
    assert surface["chi"] == -10
    assert surface["genus"] == 6
    assert surface["information_hole_cost"] == 12


def test_mcxcii_horizon_code_and_residual_packet() -> None:
    code = PACKET["horizon_code"]
    residual = PACKET["residual_packet"]

    assert code["total"] == 72
    assert code["payload"] == 66
    assert code["parity"] == 6
    assert code["rate"] == "11/12"
    assert residual["residual_triangles"] == 28
    assert residual["residual_edge_incidences"] == 84


def test_mcxcii_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 20
    assert all(PACKET["checks"].values())
