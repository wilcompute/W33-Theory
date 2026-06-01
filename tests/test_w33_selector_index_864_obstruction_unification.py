from __future__ import annotations

from analysis.w33_selector_index_864_obstruction_unification import (
    selector_index_864_obstruction_unification_packet,
)


PACKET = selector_index_864_obstruction_unification_packet()


def test_mmccclxix_all_checks_verify() -> None:
    assert PACKET["part"] == "MMCCCLXIX"
    assert PACKET["n_verified"] == 12
    assert all(PACKET["checks"].values())


def test_mmccclxix_group_index_is_864() -> None:
    index = PACKET["group_index"]
    assert index["a5_order"] == 60
    assert index["a5_order_profile"] == {"1": 1, "2": 15, "3": 20, "5": 24}
    assert index["negative_polar_order"] == 51840
    assert index["negative_polar_over_a5"] == 864


def test_mmccclxix_signed_affine_shell_is_same_864() -> None:
    shell = PACKET["affine_search_shell"]
    assert shell["gl_2_3_order"] == 48
    assert shell["agl_2_3_order"] == 432
    assert shell["signed_agl_2_3_order"] == 864


def test_mmccclxix_golden_obstruction_is_same_864() -> None:
    obstruction = PACKET["golden_obstruction"]
    assert obstruction["ordered_quadrangles"] == 12960
    assert obstruction["ordered_failures"] == 864
    assert obstruction["unique_failures"] == 108
    assert obstruction["ordered_failures_over_unique_failures"] == 8
    assert obstruction["total_over_failures"] == 15


def test_mmccclxix_boundary_demands_bijection_not_count_only() -> None:
    assert "does not yet construct a canonical bijection" in PACKET["claim_boundary"]
    assert "next selector target" in PACKET["claim_boundary"]
    assert "108 unique golden failures" in PACKET["next_target"]
