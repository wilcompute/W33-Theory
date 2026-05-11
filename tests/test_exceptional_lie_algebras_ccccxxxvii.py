"""
Part CCCCXXXVII -- Exceptional Lie Algebra Dimensions in W(3,3)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCCXXXVII_EXCEPTIONAL_LIE_ALGEBRAS_W33 import (
    Q, V, K, LAM, MU, F, G, PHI3, PHI4, PHI6,
    DIM_SU5, DIM_SO10, DIM_E6, DIM_E7, DIM_E8,
    EDGES_W33, TR_A_SQUARED,
    dim_SU5_W33, dim_SO10_W33, dim_E6_W33, dim_E7_W33,
    dim_E8_W33_a, dim_E8_W33_b,
    checks, Verified,
)


def test_verified_true():
    assert Verified is True


def test_all_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == [], f"Failing: {failed}"


def test_dim_SU5():
    assert DIM_SU5 == 24 == F == dim_SU5_W33()


def test_dim_SO10():
    assert DIM_SO10 == 45 == Q ** 2 * (MU + 1) == dim_SO10_W33()


def test_dim_E6():
    assert DIM_E6 == 78 == dim_E6_W33()


def test_dim_E7():
    assert DIM_E7 == 133 == PHI6 * (F - MU - 1) == dim_E7_W33()


def test_dim_E8_two_forms():
    assert DIM_E8 == 248
    assert dim_E8_W33_a() == 248
    assert dim_E8_W33_b() == 248


def test_W33_edges_240():
    assert EDGES_W33 == V * K // 2 == 240


def test_E_8_roots_match_edges():
    """The deepest combinatorial identification: 240 = W33 edges = E_8 root count."""
    E_8_root_count = 240  # standard
    assert EDGES_W33 == E_8_root_count


def test_E_8_dim_decomposition():
    """248 = 240 (roots) + 8 (Cartan rank)"""
    rank_E8 = 8
    assert DIM_E8 == 240 + rank_E8
    assert rank_E8 == LAM ** 3


def test_Tr_A_squared_equals_a_0():
    """Tr(A^2) = 2 * |edges| = 480 = a_0"""
    assert TR_A_SQUARED == 2 * EDGES_W33 == 480
    a_0 = 480
    assert TR_A_SQUARED == a_0


def test_Coxeter_E8_equals_q_Phi4():
    """h(E_8) = 30 = q * Phi_4"""
    h_E8 = 30
    assert h_E8 == Q * PHI4


def test_19_in_E_7():
    """19 = f - mu - 1 in E_7 dim factorization"""
    assert F - MU - 1 == 19
    assert DIM_E7 == 7 * 19


# JSON output
def test_json_exists_after_main():
    import importlib
    mod = importlib.import_module("PART_CCCCXXXVII_EXCEPTIONAL_LIE_ALGEBRAS_W33")
    mod.main()
    assert (ROOT / "PART_CCCCXXXVII_exceptional_lie_algebras_w33_results.json").exists()


def test_json_verified():
    out = ROOT / "PART_CCCCXXXVII_exceptional_lie_algebras_w33_results.json"
    if not out.exists():
        import importlib
        importlib.import_module("PART_CCCCXXXVII_EXCEPTIONAL_LIE_ALGEBRAS_W33").main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Verified"] is True


def test_json_all_dimensions():
    out = ROOT / "PART_CCCCXXXVII_exceptional_lie_algebras_w33_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    algs = data["exceptional_lie_algebras"]
    assert algs["SU(5)"]["dim"] == 24
    assert algs["SO(10)"]["dim"] == 45
    assert algs["E_6"]["dim"] == 78
    assert algs["E_7"]["dim"] == 133
    assert algs["E_8"]["dim"] == 248


def test_json_edge_root_correspondence():
    out = ROOT / "PART_CCCCXXXVII_exceptional_lie_algebras_w33_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    corr = data["edge_root_correspondence"]
    assert corr["W33_edges"] == 240
    assert corr["E_8_roots"] == 240
    assert corr["match"] is True
