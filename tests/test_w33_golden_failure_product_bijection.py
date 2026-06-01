from __future__ import annotations

from analysis.w33_golden_failure_product_bijection import (
    golden_failure_product_bijection_packet,
)


PACKET = golden_failure_product_bijection_packet()


def test_mmccclxxii_all_checks_verify() -> None:
    assert PACKET["part"] == "MMCCCLXXII"
    assert PACKET["n_verified"] == 12
    assert all(PACKET["checks"].values())


def test_mmccclxxii_product_counts() -> None:
    assert PACKET["unique_failure_count"] == 108
    assert PACKET["ordered_failure_count"] == 864
    assert PACKET["bridge_line_count"] == 27
    assert PACKET["active_pairs"] == [[0, 2], [0, 3], [1, 2], [1, 3]]
    assert PACKET["inactive_matching_pairs"] == [[0, 1], [2, 3]]


def test_mmccclxxii_profiles_are_complete_product() -> None:
    assert PACKET["pair_count_profile"] == {"27": 4}
    assert PACKET["bridge_count_profile"] == {"4": 27}
    assert all(profile == {"3": 9} for profile in PACKET["pair_projection_profiles"].values())


def test_mmccclxxii_forced_quadrangle_rule() -> None:
    assert PACKET["product_identity"]["unique"] == "|K2,2_edges| * |B27| = 4*27 = 108"
    assert PACKET["product_identity"]["forced_quadrangle"] == "{anchor, endpoint_line(a,B), B, endpoint_line(b,B)}"
    assert len(PACKET["sample_product_records"]) == 12


def test_mmccclxxii_boundary_is_not_o_minus_cosets_yet() -> None:
    assert "genuine product" in PACKET["reading"]
    assert "does not identify the product coordinates" in PACKET["claim_boundary"]
