"""Part DCCXXVI -- Critical-dimension hierarchy tests."""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxxvi_critical_dimension_hierarchy import (  # noqa: E402
    CODEC,
    DIM_E6,
    DIM_E8,
    OUT_PATH,
    Q,
    QP1,
    RANK_E8,
    TETRAHEDRON_FLAGS,
    TOMOTOPE_CELLS,
    W33_E,
    ZETA_MINUS_ONE,
    build_bridge,
    critical_dimension_table,
    e6_dimensional_breakdown,
    e8_dimensional_breakdown,
    renormalised_tetrahedron,
    universal_pattern,
    write_bridge,
)


def test_zeta_minus_one_is_minus_one_over_codec():
    assert ZETA_MINUS_ONE == Fraction(-1, CODEC)


def test_tetrahedron_24_times_zeta_is_minus_two():
    assert Fraction(TETRAHEDRON_FLAGS) * ZETA_MINUS_ONE == Fraction(-2)


def test_renormalised_tetrahedron_returns_minus_two():
    r = renormalised_tetrahedron()
    assert r["equals_delta_chi_per_handle"] is True


def test_bosonic_critical_dim_26():
    table = critical_dimension_table()
    bosonic = next(r for r in table if r["theory"] == "bosonic string")
    assert bosonic["D_critical"] == 26
    assert bosonic["transverse_modes"] == 24
    assert bosonic["transverse_modes"] == TETRAHEDRON_FLAGS


def test_super_critical_dim_10():
    table = critical_dimension_table()
    sup = next(r for r in table if r["theory"] == "superstring")
    assert sup["D_critical"] == 10
    assert sup["transverse_modes"] == 8
    assert sup["transverse_modes"] == TOMOTOPE_CELLS


def test_M_theory_dim_11():
    table = critical_dimension_table()
    m = next(r for r in table if r["theory"] == "M-theory")
    assert m["D_critical"] == 11
    assert m["transverse_modes"] == 9 == Q * Q


def test_F_theory_dim_12():
    table = critical_dimension_table()
    f = next(r for r in table if r["theory"] == "F-theory")
    assert f["D_critical"] == 12 == CODEC
    assert f["transverse_modes"] == 10


def test_universal_pattern_all_match():
    p = universal_pattern()
    assert p["all_match"] is True
    for r in p["rows"]:
        assert r["matches"] is True


def test_e6_is_three_times_26():
    e6 = e6_dimensional_breakdown()
    assert e6["dim_E6"] == DIM_E6 == 78
    assert e6["matches"] is True
    assert DIM_E6 == 3 * 26 == Q * 26


def test_e8_is_240_plus_8():
    e8 = e8_dimensional_breakdown()
    assert e8["dim_E8"] == DIM_E8 == 248
    assert e8["matches"] is True
    assert e8["root_count"] == 240
    assert e8["cartan_rank"] == RANK_E8 == 8


def test_cartan_e8_equals_tomotope_cells():
    assert RANK_E8 == TOMOTOPE_CELLS == 8


def test_e8_roots_equal_w33_edges():
    assert 240 == W33_E


def test_two_offset_is_q_q_plus_one():
    assert (Q, QP1) == (3, 4)


def test_summary_all_identities_hold():
    b = build_bridge()
    assert b["summary"]["all_identities_hold"] is True


def test_identities_all_pass():
    b = build_bridge()
    failed = [k for k, v in b["identities"].items() if not v]
    assert failed == []


def test_table_has_four_theories():
    assert len(critical_dimension_table()) == 4


def test_theorem_and_one_line_present():
    b = build_bridge()
    assert "Critical-Dimension Hierarchy Theorem" in b["theorem"]
    assert "(D_critical - 2)" in b["one_line"]


def test_honesty_boundary_explicit():
    b = build_bridge()
    boundary = b["honesty_boundary"].lower()
    assert "not a derivation" in boundary or "structural" in boundary


def test_write_and_reload():
    out = write_bridge()
    assert out.exists()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["summary"]["all_identities_hold"] is True


def test_json_has_expected_keys():
    if not OUT_PATH.exists():
        write_bridge()
    data = json.loads(OUT_PATH.read_text(encoding="utf-8"))
    for key in (
        "summary",
        "renormalised_tetrahedron_identity",
        "critical_dimension_table",
        "universal_pattern",
        "e6_breakdown",
        "e8_breakdown",
        "two_offset_interpretation",
        "identities",
        "theorem",
        "one_line",
        "honesty_boundary",
    ):
        assert key in data
