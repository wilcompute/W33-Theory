"""Part DCCXXII -- Mod-12 toroidal synthesis tests."""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxxii_mod12_toroidal_synthesis import (  # noqa: E402
    CODEC,
    HEAWOOD,
    OUT_PATH,
    Q,
    QP1,
    ZETA_MINUS_ONE,
    build_bridge,
    classify_small_fractions,
    csaszar_VEF,
    fano_plane,
    genus_via_euler,
    heawood_graph,
    szilassi_VEF,
    tesla_missing_digits,
    tetrahedron_VEF,
    write_bridge,
    z3_grading_of_codec,
)


def test_consecutive_pair_at_q_3():
    assert (Q, QP1) == (3, 4)


def test_sum_is_heawood():
    assert Q + QP1 == HEAWOOD == 7


def test_product_is_codec():
    assert Q * QP1 == CODEC == 12


def test_quadratic_discriminant_is_one():
    assert HEAWOOD * HEAWOOD - 4 * CODEC == 1


def test_quadratic_has_q_and_qp1_as_roots():
    # (x - 3)(x - 4) = x^2 - 7x + 12
    for r in (Q, QP1):
        assert r * r - HEAWOOD * r + CODEC == 0


def test_tetrahedron_g0():
    t = tetrahedron_VEF()
    assert (t["V"], t["E"], t["F"]) == (4, 6, 4)
    assert genus_via_euler(t["V"], t["E"], t["F"]) == 0


def test_csaszar_g1_K7():
    cz = csaszar_VEF()
    assert cz["V"] == HEAWOOD == 7
    assert cz["E"] == 21
    assert cz["F"] == 14
    assert genus_via_euler(cz["V"], cz["E"], cz["F"]) == 1


def test_szilassi_g1_dual():
    sz = szilassi_VEF()
    assert sz["V"] == 14
    assert sz["E"] == 21
    assert sz["F"] == HEAWOOD == 7
    assert genus_via_euler(sz["V"], sz["E"], sz["F"]) == 1


def test_csaszar_szilassi_dual():
    cz = csaszar_VEF()
    sz = szilassi_VEF()
    assert cz["V"] == sz["F"]
    assert cz["F"] == sz["V"]
    assert cz["E"] == sz["E"]


def test_fano_plane_is_7_7_3():
    f = fano_plane()
    assert f["points"] == f["lines"] == 7
    assert f["points_per_line"] == f["lines_per_point"] == Q
    assert f["incidence_edges"] == 21


def test_heawood_graph():
    h = heawood_graph()
    assert h["vertices"] == 14
    assert h["edges"] == 21
    assert h["girth"] == 6


def test_z3_zero_class_is_3_6_9_12():
    z = z3_grading_of_codec()
    assert z[0] == [3, 6, 9, 12]
    assert len(z[0]) == 4
    assert len(z[1]) == 4
    assert len(z[2]) == 4


def test_tesla_missing_digits():
    assert tesla_missing_digits() == [0, 3, 6, 9]


def test_tesla_missing_matches_z3_zero_class_modulo_zero():
    missing = tesla_missing_digits()
    nonzero_missing = [d for d in missing if d > 0]
    z = z3_grading_of_codec()
    assert nonzero_missing == [3, 6, 9]
    assert all(d in z[0] for d in nonzero_missing)


def test_one_over_three_six_nine_decimal_classes():
    rows = classify_small_fractions()
    one_over_3 = rows[2]
    one_over_6 = rows[5]
    one_over_9 = rows[8]
    assert one_over_3["rep_block"] == "3"
    assert one_over_3["leading_digits"] == ""
    assert one_over_6["rep_block"] == "6"
    assert one_over_6["leading_digits"] == "1"
    assert one_over_9["rep_block"] == "1"
    assert one_over_9["leading_digits"] == ""


def test_zeta_minus_one_is_minus_one_over_codec():
    assert ZETA_MINUS_ONE == Fraction(-1, CODEC)


def test_codec_size_in_z3_zero_class():
    assert CODEC % 3 == 0


def test_spacetime_dim_product():
    assert Q * QP1 == CODEC == 12


def test_summary_all_identities_hold():
    b = build_bridge()
    assert b["summary"]["all_identities_hold"] is True


def test_identities_all_pass():
    b = build_bridge()
    failed = [k for k, v in b["identities"].items() if not v]
    assert failed == []


def test_write_and_reload():
    out = write_bridge()
    assert out.exists()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["summary"]["all_identities_hold"] is True
    assert data["summary"]["heawood"] == 7
    assert data["summary"]["codec"] == 12


def test_theorem_and_one_line_present():
    b = build_bridge()
    assert "Toroidal Synthesis Theorem" in b["theorem"]
    assert "Heawood" in b["one_line"]


def test_json_has_expected_keys():
    if not OUT_PATH.exists():
        write_bridge()
    data = json.loads(OUT_PATH.read_text(encoding="utf-8"))
    for key in (
        "summary",
        "consecutive_pair_quadratic",
        "polyhedra",
        "fano_plane",
        "heawood_graph",
        "z3_grading_of_codec",
        "tesla_missing_digits",
        "small_fraction_decimal_classes",
        "spacetime_factorisation",
        "zeta_minus_one_reading",
        "identities",
        "theorem",
        "one_line",
        "honesty_boundary",
    ):
        assert key in data
