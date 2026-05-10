"""
Part CCCCXXXII -- W(3,3) -> E_6 GUT Embedding Theorem
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCCXXXII_W33_E6_EMBEDDING_THEOREM import (
    Q, V, K, LAM, MU, F, G, PHI3, PHI4, PHI6,
    Sp4_Fq_order, W_E6_order,
    E_6_dim, E_6_fundamental_dim, SU_5_dim,
    E_6_27_decomposition, total_fermion_dim_3_gen,
    checks, Verified,
)


def test_verified_true():
    assert Verified is True


def test_all_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == [], f"Failing: {failed}"


def test_sp4_F3_equals_W_E6_order():
    assert Sp4_Fq_order(3) == W_E6_order() == 51840


def test_E_6_dim_78():
    assert E_6_dim() == 78


def test_E_6_fundamental_27_eq_q_q():
    assert E_6_fundamental_dim() == Q ** Q == 27


def test_SU_5_dim_24_eq_f():
    assert SU_5_dim() == F == 24


def test_three_generations_81():
    assert total_fermion_dim_3_gen() == 81 == Q ** 4


def test_sin2_theta_W_GUT():
    sin2_GUT = Q / LAM ** Q
    assert sin2_GUT == 3 / 8 == 0.375


def test_decomposition_sums_to_27():
    decomp = E_6_27_decomposition()
    # 10 + 5_bar + 1 + 11 = 27
    assert decomp["10"] + decomp["5_bar"] + decomp["1"] + decomp["11"] == 27


def test_alpha_GUT_inv_equals_dim_SU_5():
    # alpha_GUT^{-1} = f = 24 (CCCXXXII)
    # = dim SU(5) (this part)
    assert F == SU_5_dim() == 24


def test_q_3_ternary():
    assert Q == 3


def test_27_eq_q_q():
    assert Q ** Q == 27


def test_81_eq_q_fourth():
    assert Q ** 4 == 81


# JSON output
def test_json_exists_after_main():
    import importlib
    mod = importlib.import_module("PART_CCCCXXXII_W33_E6_EMBEDDING_THEOREM")
    mod.main()
    assert (ROOT / "PART_CCCCXXXII_w33_e6_embedding_results.json").exists()


def test_json_verified():
    out = ROOT / "PART_CCCCXXXII_w33_e6_embedding_results.json"
    if not out.exists():
        import importlib
        importlib.import_module("PART_CCCCXXXII_W33_E6_EMBEDDING_THEOREM").main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Verified"] is True


def test_group_chain_in_results():
    out = ROOT / "PART_CCCCXXXII_w33_e6_embedding_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert "Sp(4, F_3)" in data["group_chain"]["Aut_W33"]
    assert "W(E_6)" in data["group_chain"]["W_E6"]
