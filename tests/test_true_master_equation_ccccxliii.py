"""
Part CCCCXLIII -- The True Master Equation q! = 2q
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCCXLIII_TRUE_MASTER_EQUATION import (
    Q, V, K, LAM, MU, F, G, PHI3, PHI4, PHI6, Q_FACTORIAL,
    SRG_DISCRIMINANT,
    OMEGA_LAMBDA_W33, OMEGA_DM_OVER_B_W33, H_0_FT3,
    V_EW_W33,
    Q_FACTORIAL_ROLES,
    master_eq_solutions,
    checks, Verified,
)


def test_verified_true():
    assert Verified is True


def test_all_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == [], f"Failing: {failed}"


def test_master_equation_unique_solution():
    """q! = 2q has unique positive-integer solution q = 3."""
    assert master_eq_solutions(20) == [3]


def test_q_factorial_equals_6():
    assert Q_FACTORIAL == 6 == math.factorial(3)


def test_master_equation_at_q_3():
    assert math.factorial(3) == 6 == 2 * 3


def test_master_equation_fails_at_other_q():
    for q in [1, 2, 4, 5, 6, 7]:
        assert math.factorial(q) != 2 * q


def test_SRG_quadratic_discriminant():
    """Discriminant (q!)^2 - 4*2^q = 4 = lam^2."""
    assert SRG_DISCRIMINANT == Q_FACTORIAL ** 2 - 4 * 2 ** Q == 4
    assert SRG_DISCRIMINANT == LAM ** 2


def test_SRG_quadratic_roots():
    """x^2 - 6x + 8 = 0 has roots 2 and 4."""
    # (x-2)(x-4) = x^2 - 6x + 8
    assert LAM == 2
    assert MU == 4
    assert LAM + MU == Q_FACTORIAL == 6
    assert LAM * MU == 2 ** Q == 8


def test_parameter_closure():
    assert V == (Q + 1) * (Q ** 2 + 1) == 40
    assert K == Q * (Q + 1) == 12
    assert V * K // 2 == 240


def test_omega_Lambda_FT3():
    assert OMEGA_LAMBDA_W33 == 41 / 60
    assert abs(OMEGA_LAMBDA_W33 - 0.685) < 0.01


def test_omega_DM_over_b_FT3():
    assert OMEGA_DM_OVER_B_W33 == 16 / 3
    assert abs(OMEGA_DM_OVER_B_W33 - 5.36) < 0.1


def test_H_0_FT3():
    """H_0 = Phi_12 - q! = 73 - 6 = 67"""
    Phi_12 = Q ** 4 - Q ** 2 + 1
    assert Phi_12 == 73
    assert H_0_FT3 == Phi_12 - Q_FACTORIAL == 67


def test_v_EW_anchor():
    """v_EW = E + q! = 246 GeV"""
    assert V_EW_W33 == V * K // 2 + Q_FACTORIAL == 246


def test_q_factorial_roles_count():
    assert len(Q_FACTORIAL_ROLES) >= 7


# Cross-link with CCCCXXXVIII
def test_q_q_equals_q_3_corollary():
    """q^q = q^3 still holds, but it's a derived corollary."""
    assert Q ** Q == Q ** 3 == 27


# JSON output
def test_json_exists_after_main():
    import importlib
    mod = importlib.import_module("PART_CCCCXLIII_TRUE_MASTER_EQUATION")
    mod.main()
    assert (ROOT / "PART_CCCCXLIII_true_master_equation_results.json").exists()


def test_json_verified():
    out = ROOT / "PART_CCCCXLIII_true_master_equation_results.json"
    if not out.exists():
        import importlib
        importlib.import_module("PART_CCCCXLIII_TRUE_MASTER_EQUATION").main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Verified"] is True


def test_json_master_equation():
    out = ROOT / "PART_CCCCXLIII_true_master_equation_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["master_equation"]["statement"] == "q! = 2q"
    assert data["master_equation"]["unique_solution"] == 3
