"""
Part CCCCXXXI -- W(3,3) Uniqueness Theorem from the Master Equation
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCCXXXI_W33_UNIQUENESS_THEOREM import (
    Q, V, K, LAM, MU, F, G, PHI3, PHI4, PHI6,
    master_eq_prime_solutions, gq_to_srg, sp4_order,
    checks, Verified,
)


def test_verified_true():
    assert Verified is True


def test_all_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == [], f"Failing: {failed}"


def test_master_equation_unique_prime():
    sols = master_eq_prime_solutions(100)
    assert sols == [3]


def test_GQ_3_3_yields_W33_parameters():
    v, k, lam, mu = gq_to_srg(3, 3)
    assert (v, k, lam, mu) == (40, 12, 2, 4)


def test_sp4_F3_order():
    assert sp4_order(3) == 51840


def test_master_equation_q_3():
    assert Q ** Q == Q ** 3 == 27


def test_other_primes_fail_master_eq():
    for p in [2, 5, 7, 11]:
        assert p ** p != p ** 3


def test_W33_parameters():
    assert V == 40
    assert K == 12
    assert LAM == 2
    assert MU == 4


def test_cyclotomic_primes():
    assert PHI3 == 13  # prime
    assert PHI4 == 10  # = 2 * 5
    assert PHI6 == 7   # prime


def test_edges_240():
    assert V * K // 2 == 240


def test_aut_order_equals_W_E6():
    assert sp4_order(3) == 51840  # |Sp(4,F_3)| = |W(E_6)|


def test_gq_to_srg_general():
    # GQ(s,t) -> SRG((s+1)(st+1), s(t+1), s-1, t+1)
    v, k, lam, mu = gq_to_srg(2, 2)
    # GQ(2,2) = doily, SRG(15, 6, 1, 3)
    assert (v, k, lam, mu) == (15, 6, 1, 3)


# JSON output
def test_json_exists_after_main():
    import importlib
    mod = importlib.import_module("PART_CCCCXXXI_W33_UNIQUENESS_THEOREM")
    mod.main()
    assert (ROOT / "PART_CCCCXXXI_w33_uniqueness_theorem_results.json").exists()


def test_json_verified():
    out = ROOT / "PART_CCCCXXXI_w33_uniqueness_theorem_results.json"
    if not out.exists():
        import importlib
        importlib.import_module("PART_CCCCXXXI_W33_UNIQUENESS_THEOREM").main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Verified"] is True


def test_axioms_listed():
    out = ROOT / "PART_CCCCXXXI_w33_uniqueness_theorem_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    axioms = data["axioms"]
    assert "A1_master_equation" in axioms
    assert "A2_q_prime" in axioms
    assert "A3_GQ" in axioms
    assert "A4_symplectic" in axioms
    assert "A5_connected" in axioms
