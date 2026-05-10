"""
Part CCCXXVIII -- Bottom Yukawa  y_b(MSbar, m_b) = q/(mu+1)^3 = 3/125
Regression tests for exploration/PART_CCCXXVIII_BOTTOM_YUKAWA_BRIDGE.py
"""
from __future__ import annotations

import json
import math
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCXXVIII_BOTTOM_YUKAWA_BRIDGE import (
    Q, V, K, LAM, MU, F, PHI3, PHI4, PHI6,
    Y_B_W33,
    M_B_MSBAR, SIGMA_M_B_MSBAR, V_EW,
    Y_B_DATA, SIGMA_Y_B_DATA,
    M_B_PRED, RESIDUAL_M_B, Z_M_B,
    RESIDUAL_Y_B, Z_Y_B,
    y_b_from_m_b,
    residual_records,
    checks, Verified,
)


def test_verified_true():
    assert Verified is True


def test_all_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == [], f"Failing: {failed}"


def test_check_count():
    assert len(checks) == 17


def test_W33_form():
    assert Y_B_W33 == Fraction(Q, (MU + 1) ** 3)
    assert Y_B_W33 == Fraction(3, 125)


def test_decimal():
    assert float(Y_B_W33) == 0.024


def test_components():
    assert MU + 1 == 5
    assert (MU + 1) ** 3 == 125
    assert Y_B_W33.numerator == Q == 3
    assert Y_B_W33.denominator == 125


def test_y_b_extraction_function():
    val = y_b_from_m_b(4.18, 246.21965)
    assert abs(val - 0.024009) < 1e-4


def test_y_b_data_value():
    expected = M_B_MSBAR * math.sqrt(2) / V_EW
    assert abs(Y_B_DATA - expected) < 1e-12


def test_y_b_within_1_sigma():
    assert abs(Z_Y_B) < 1


def test_y_b_within_0p1_sigma():
    assert abs(Z_Y_B) < 0.1


def test_m_b_within_1_sigma():
    assert abs(Z_M_B) < 1


def test_m_b_pred_value():
    expected = float(Y_B_W33) * V_EW / math.sqrt(2)
    assert abs(M_B_PRED - expected) < 1e-9
    assert 4.0 < M_B_PRED < 4.4


def test_residual_records():
    records = residual_records()
    assert len(records) == 2
    assert all("PASS" in r.status for r in records)


# Cross-link with CCCXXV (rho_bar = (lam/(mu+1))^2 = 4/25)
def test_mu_plus_1_shared_with_rho_bar():
    rho_bar = Fraction(LAM, MU + 1) ** 2
    assert rho_bar == Fraction(4, 25)
    assert rho_bar.denominator == (MU + 1) ** 2
    assert Y_B_W33.denominator == (MU + 1) ** 3
    # y_b denom = rho_bar denom * (mu+1)
    assert Y_B_W33.denominator == rho_bar.denominator * (MU + 1)


# Cross-link with CCCXXVI (top Yukawa cubed)
def test_top_and_bottom_yukawa_structure():
    Y_T_CUBED = Fraction(V, V + 1)   # 40/41 from CCCXXVI
    # Both have an "n / (n+1)" or "n / (n+1)^k" shape
    assert Y_T_CUBED.denominator == V + 1 == 41
    assert Y_B_W33.denominator == (MU + 1) ** 3 == 125
    # Top Yukawa is CUBED (power 3 on Yukawa side, denom shift +1 on v)
    # Bottom Yukawa is LINEAR (power 1 on Yukawa side, denom CUBE of (mu+1))
    # The "cube" structure swaps between numerator and denominator


# JSON output
def test_json_exists_after_main():
    import importlib
    mod = importlib.import_module("PART_CCCXXVIII_BOTTOM_YUKAWA_BRIDGE")
    mod.main()
    assert (ROOT / "PART_CCCXXVIII_bottom_yukawa_results.json").exists()


def test_json_verified():
    out = ROOT / "PART_CCCXXVIII_bottom_yukawa_results.json"
    if not out.exists():
        import importlib
        importlib.import_module("PART_CCCXXVIII_BOTTOM_YUKAWA_BRIDGE").main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Verified"] is True
    assert data["checks_passed"] == data["checks_total"]
