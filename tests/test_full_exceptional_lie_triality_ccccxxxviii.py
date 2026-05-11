"""
Part CCCCXXXVIII -- All 5 Exceptional Lie Groups + Triality + Master Axiom
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCCXXXVIII_FULL_EXCEPTIONAL_LIE_TRIALITY import (
    Q, V, K, LAM, MU, F, G, PHI3, PHI4, PHI6,
    EXCEPTIONAL_LIE_GROUPS, TRIALITY_CONNECTIONS,
    MASTER_AXIOM, MASTER_AXIOM_CONSEQUENCES,
    checks, Verified,
)


def test_verified_true():
    assert Verified is True


def test_all_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == [], f"Failing: {failed}"


def test_all_5_exceptional_lie_groups():
    expected = {"G_2", "F_4", "E_6", "E_7", "E_8"}
    assert set(EXCEPTIONAL_LIE_GROUPS.keys()) == expected


def test_dim_G2():
    assert EXCEPTIONAL_LIE_GROUPS["G_2"]["dim"] == 14 == LAM * PHI6


def test_dim_F4():
    assert EXCEPTIONAL_LIE_GROUPS["F_4"]["dim"] == 52 == LAM ** 2 * PHI3


def test_dim_E6():
    assert EXCEPTIONAL_LIE_GROUPS["E_6"]["dim"] == 78 == LAM * Q * PHI3


def test_dim_E7():
    assert EXCEPTIONAL_LIE_GROUPS["E_7"]["dim"] == 133 == PHI6 * (F - MU - 1)


def test_dim_E8():
    assert EXCEPTIONAL_LIE_GROUPS["E_8"]["dim"] == 248 == V * K // 2 + LAM ** 3


def test_all_ranks_W33():
    ranks = {"G_2": 2, "F_4": 4, "E_6": 6, "E_7": 7, "E_8": 8}
    for g, r in ranks.items():
        assert EXCEPTIONAL_LIE_GROUPS[g]["rank"] == r
    # W(3,3) forms
    assert 2 == LAM
    assert 4 == MU
    assert 6 == LAM * Q
    assert 7 == PHI6
    assert 8 == LAM ** 3


def test_all_coxeter_numbers_W33():
    coxeter = {"G_2": 6, "F_4": 12, "E_6": 12, "E_7": 18, "E_8": 30}
    for g, h in coxeter.items():
        assert EXCEPTIONAL_LIE_GROUPS[g]["coxeter_h"] == h
    # W(3,3) forms
    assert 6 == LAM * Q
    assert 12 == K
    assert 18 == LAM * Q ** 2
    assert 30 == Q * PHI4


def test_triality_connections():
    assert len(TRIALITY_CONNECTIONS) >= 5
    assert "common_origin" in TRIALITY_CONNECTIONS


def test_master_axiom_statement():
    assert "symplectic generalized quadrangle" in MASTER_AXIOM
    assert "q^q = q^3" in MASTER_AXIOM


def test_master_axiom_consequences():
    assert len(MASTER_AXIOM_CONSEQUENCES) >= 10
    assert any("q = 3" in c for c in MASTER_AXIOM_CONSEQUENCES)
    assert any("W(3,3)" in c for c in MASTER_AXIOM_CONSEQUENCES)


# JSON output
def test_json_exists_after_main():
    import importlib
    mod = importlib.import_module("PART_CCCCXXXVIII_FULL_EXCEPTIONAL_LIE_TRIALITY")
    mod.main()
    assert (ROOT / "PART_CCCCXXXVIII_full_exceptional_lie_triality_results.json").exists()


def test_json_verified():
    out = ROOT / "PART_CCCCXXXVIII_full_exceptional_lie_triality_results.json"
    if not out.exists():
        import importlib
        importlib.import_module("PART_CCCCXXXVIII_FULL_EXCEPTIONAL_LIE_TRIALITY").main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Verified"] is True


def test_json_all_5_groups():
    out = ROOT / "PART_CCCCXXXVIII_full_exceptional_lie_triality_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    groups = data["exceptional_lie_groups_full"]
    assert set(groups.keys()) == {"G_2", "F_4", "E_6", "E_7", "E_8"}


def test_json_master_axiom_present():
    out = ROOT / "PART_CCCCXXXVIII_full_exceptional_lie_triality_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert "master_axiom" in data
    assert "statement" in data["master_axiom"]
