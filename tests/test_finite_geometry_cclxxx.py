"""Tests for Part CCLXXX: Finite Geometry over GF(3), Incidence Structures,
and the W(3,3) Configuration Bridge.
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "exploration"))

from PART_CCLXXX_FINITE_GEOMETRY_BRIDGE import (
    verify_gf3_field_arithmetic,
    verify_pg_point_counts,
    verify_ag_point_line_counts,
    verify_steiner_system_s_2_3_9,
    verify_steiner_system_s_2_4_13,
    verify_pg3_3_atlas,
    verify_collineation_groups,
    verify_psl2q_orders_atlas,
    verify_elliptic_quadric,
    verify_gq_2_4_atlas,
    verify_hermitian_variety,
    verify_spread_in_pg3_3,
    verify_design_theory,
    verify_resolvability,
    verify_oval_arc,
    verify_witt_design_s_5_6_12,
    verify_mathieu_groups,
    verify_projective_line_atlas,
    verify_unital_u3,
    verify_transport_incidence,
    verify_combinatorial_identities,
    verify_w33_geo_atlas,
    build_cclxxx_bridge_summary,
)


def _assert_all(d: dict) -> None:
    failed = [k for k, v in d.items() if not v]
    assert not failed, f"Failed checks: {failed}"


def test_verify_gf3_field_arithmetic():
    _assert_all(verify_gf3_field_arithmetic())


def test_verify_pg_point_counts():
    _assert_all(verify_pg_point_counts())


def test_verify_ag_point_line_counts():
    _assert_all(verify_ag_point_line_counts())


def test_verify_steiner_system_s_2_3_9():
    _assert_all(verify_steiner_system_s_2_3_9())


def test_verify_steiner_system_s_2_4_13():
    _assert_all(verify_steiner_system_s_2_4_13())


def test_verify_pg3_3_atlas():
    _assert_all(verify_pg3_3_atlas())


def test_verify_collineation_groups():
    _assert_all(verify_collineation_groups())


def test_verify_psl2q_orders_atlas():
    _assert_all(verify_psl2q_orders_atlas())


def test_verify_elliptic_quadric():
    _assert_all(verify_elliptic_quadric())


def test_verify_gq_2_4_atlas():
    _assert_all(verify_gq_2_4_atlas())


def test_verify_hermitian_variety():
    _assert_all(verify_hermitian_variety())


def test_verify_spread_in_pg3_3():
    _assert_all(verify_spread_in_pg3_3())


def test_verify_design_theory():
    _assert_all(verify_design_theory())


def test_verify_resolvability():
    _assert_all(verify_resolvability())


def test_verify_oval_arc():
    _assert_all(verify_oval_arc())


def test_verify_witt_design_s_5_6_12():
    _assert_all(verify_witt_design_s_5_6_12())


def test_verify_mathieu_groups():
    _assert_all(verify_mathieu_groups())


def test_verify_projective_line_atlas():
    _assert_all(verify_projective_line_atlas())


def test_verify_unital_u3():
    _assert_all(verify_unital_u3())


def test_verify_transport_incidence():
    _assert_all(verify_transport_incidence())


def test_verify_combinatorial_identities():
    _assert_all(verify_combinatorial_identities())


def test_verify_w33_geo_atlas():
    _assert_all(verify_w33_geo_atlas())


def test_build_cclxxx_bridge_summary():
    summary = build_cclxxx_bridge_summary()
    assert summary["part"] == "CCLXXX"
    assert summary["all_checks_pass"] is True
    assert summary["total_checks"] == 247
    assert summary["failed_checks"] == []
