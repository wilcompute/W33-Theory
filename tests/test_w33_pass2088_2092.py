"""Focused regression tests for Passes 2088-2092."""

from analysis.w33_pass2088_2092_complex_structure_controller import (
    build_certificate,
    controller_certificate,
    field_reduction_q3_certificate,
    regular_spread_orbit_size,
)


def test_field_reduction_q3() -> None:
    certificate = field_reduction_q3_certificate()
    assert certificate["projective_points"] == 40
    assert certificate["spread_lines"] == 10
    assert all(certificate["checks"].values())


def test_regular_spread_orbit_formula() -> None:
    assert [regular_spread_orbit_size(q) for q in (3, 5, 7, 11)] == [
        36,
        300,
        1176,
        7260,
    ]


def test_shared_inversion_controller() -> None:
    certificate = controller_certificate()
    assert certificate["order"] == 48
    assert certificate["D4_order"] == 8
    assert certificate["D12_order"] == 12
    assert certificate["D4_intersection_D12_order"] == 2
    assert all(certificate["checks"].values())


def test_frozen_release_certificate() -> None:
    certificate = build_certificate()
    assert certificate["status"] == "PASS"
    assert all(certificate["checks"].values())
