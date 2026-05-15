"""Part DCCXXIV -- Loop-closure origin tests."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxxiv_loop_closure_origin import (  # noqa: E402
    OUT_PATH,
    Q,
    QP1,
    build_bridge,
    loop_closure_argument,
    rigidity_argument,
    subcells_of_simplex,
    tetrahedron_subcells,
    triangle_subcells,
    two_sided_bound,
    write_bridge,
)


def test_minimum_loop_vertices_is_3():
    assert Q == 3


def test_triangle_subcells_are_3_3_1():
    tri = triangle_subcells()
    assert tri["dim_0"] == 3
    assert tri["dim_1"] == 3
    assert tri["dim_2"] == 1
    assert tri["total"] == 7


def test_tetrahedron_subcells_are_4_6_4_1():
    tet = tetrahedron_subcells()
    assert tet["dim_0"] == 4
    assert tet["dim_1"] == 6
    assert tet["dim_2"] == 4
    assert tet["dim_3"] == 1
    assert tet["total"] == 15


def test_triangle_total_is_mersenne_q():
    assert triangle_subcells()["total"] == (1 << Q) - 1 == 7


def test_tetrahedron_total_is_mersenne_q_plus_one():
    assert tetrahedron_subcells()["total"] == (1 << QP1) - 1 == 15


def test_heawood_equals_triangle_total():
    # Heawood = q + (q+1) = 7, also = 2^q - 1 = 7 at q = 3
    assert triangle_subcells()["total"] == Q + QP1 == 7
    assert triangle_subcells()["total"] == (1 << Q) - 1 == 7


def test_g_eigen_mult_equals_tetrahedron_total():
    # W(3,3) eigenvalue -4 has multiplicity 15
    assert tetrahedron_subcells()["total"] == 15


def test_simplex_total_formula():
    for n in range(1, 6):
        s = subcells_of_simplex(n)
        assert s["total"] == (1 << (n + 1)) - 1


def test_rigidity_argument_at_q_3():
    rig = rigidity_argument()
    # q! = 2q at q = 3
    assert math.factorial(Q) == 2 * Q == 6
    # 4 steps
    assert len(rig) == 4


def test_loop_closure_5_steps():
    loop = loop_closure_argument()
    assert len(loop) == 5
    assert "minimum" in loop[0]["claim"].lower() or "at least" in loop[0]["claim"].lower()


def test_two_sided_bound_intersection():
    bounds = two_sided_bound()
    assert bounds["intersection"] == [Q]
    assert bounds["lower_bound"]["source"].startswith("loop closure")
    assert bounds["upper_bound"]["source"].startswith("rigidity")


def test_consecutive_pair_3_4():
    assert (Q, QP1) == (3, 4)


def test_summary_all_identities_hold():
    b = build_bridge()
    assert b["summary"]["all_identities_hold"] is True


def test_identities_all_pass():
    b = build_bridge()
    failed = [k for k, v in b["identities"].items() if not v]
    assert failed == []


def test_user_quote_present():
    b = build_bridge()
    quote = b["user_insight_quote"]
    assert "3" in quote
    assert "4th" in quote
    assert "triangle" in quote.lower()


def test_mersenne_block_present():
    b = build_bridge()
    m = b["mersenne_connection"]
    assert m["M_q"] == 7
    assert m["M_q_plus_1"] == 15


def test_theorem_and_one_line_present():
    b = build_bridge()
    assert "Loop-Closure Theorem" in b["theorem"]
    assert "M_3" in b["one_line"] or "Heawood" in b["one_line"]


def test_honesty_boundary_explicit():
    b = build_bridge()
    boundary = b["honesty_boundary"].lower()
    assert "does not" in boundary


def test_write_and_reload():
    out = write_bridge()
    assert out.exists()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["summary"]["all_identities_hold"] is True
    assert data["summary"]["triangle_total"] == 7
    assert data["summary"]["tetrahedron_total"] == 15


def test_json_has_expected_keys():
    if not OUT_PATH.exists():
        write_bridge()
    data = json.loads(OUT_PATH.read_text(encoding="utf-8"))
    for key in (
        "summary",
        "triangle_subcells",
        "tetrahedron_subcells",
        "loop_closure_argument",
        "rigidity_argument",
        "two_sided_bound",
        "user_insight_quote",
        "mersenne_connection",
        "identities",
        "theorem",
        "one_line",
        "honesty_boundary",
    ):
        assert key in data
