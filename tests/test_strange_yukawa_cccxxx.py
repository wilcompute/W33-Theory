"""
Part CCCXXX -- Strange Yukawa  y_s(MSbar, 2 GeV) = Phi_4 / 137^2 = Phi_4 * y_c^2
Regression tests for exploration/PART_CCCXXX_STRANGE_YUKAWA_BRIDGE.py
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

from PART_CCCXXX_STRANGE_YUKAWA_BRIDGE import (
    Q, V, K, LAM, MU, F, G, PHI3, PHI4, PHI6,
    Y_S_W33, ALPHA_INV_W33,
    M_S_MEV, SIGMA_M_S_MEV, V_EW_GEV,
    Y_S_DATA, SIGMA_Y_S_DATA,
    M_S_PRED_MEV, RESIDUAL_M_S, Z_M_S,
    RESIDUAL_Y_S, Z_Y_S,
    y_s_from_m_s,
    residual_records,
    checks, Verified,
)


def test_verified_true():
    assert Verified is True


def test_all_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == [], f"Failing: {failed}"


def test_check_count():
    assert len(checks) == 16


def test_W33_form():
    assert Y_S_W33 == Fraction(PHI4, ALPHA_INV_W33 ** 2)
    assert Y_S_W33 == Fraction(10, 18769)


def test_y_s_eq_phi4_y_c_squared():
    Y_C = Fraction(1, 137)
    assert Y_S_W33 == PHI4 * Y_C ** 2


def test_137_squared():
    assert ALPHA_INV_W33 == 137
    assert ALPHA_INV_W33 ** 2 == 18769


def test_phi4_value():
    assert PHI4 == 10


def test_y_s_within_1_sigma():
    assert abs(Z_Y_S) < 1


def test_y_s_within_0p1_sigma():
    assert abs(Z_Y_S) < 0.1


def test_m_s_within_1_sigma():
    assert abs(Z_M_S) < 1


def test_m_s_pred_in_window():
    assert 85 < M_S_PRED_MEV < 100


def test_m_s_pred_value():
    expected = float(Y_S_W33) * V_EW_GEV / math.sqrt(2) * 1000
    assert abs(M_S_PRED_MEV - expected) < 1e-6


def test_yukawa_hierarchy():
    Y_T_CUBED = Fraction(V, V + 1)
    Y_B = Fraction(Q, (MU + 1) ** 3)
    Y_C = Fraction(1, 137)
    assert float(Y_T_CUBED) > float(Y_B) > float(Y_C) > float(Y_S_W33)


def test_extraction_function():
    val = y_s_from_m_s(0.0934, 246.21965)
    assert abs(val - 5.366e-4) < 1e-5


def test_residual_records():
    records = residual_records()
    assert len(records) == 2
    assert all("PASS" in r.status for r in records)


# Cross-link with Higgs quartic CCCXXIV
def test_phi4_in_higgs_and_strange():
    LAMBDA_H = Fraction(PHI3, PHI4 ** 2)
    # Phi_4^2 in lambda_H denom; Phi_4 in y_s numerator
    assert LAMBDA_H.denominator == PHI4 ** 2
    assert Y_S_W33.numerator == PHI4


# JSON output
def test_json_exists_after_main():
    import importlib
    mod = importlib.import_module("PART_CCCXXX_STRANGE_YUKAWA_BRIDGE")
    mod.main()
    assert (ROOT / "PART_CCCXXX_strange_yukawa_results.json").exists()


def test_json_verified():
    out = ROOT / "PART_CCCXXX_strange_yukawa_results.json"
    if not out.exists():
        import importlib
        importlib.import_module("PART_CCCXXX_STRANGE_YUKAWA_BRIDGE").main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Verified"] is True
    assert data["checks_passed"] == data["checks_total"]


def test_json_second_gen_hierarchy():
    out = ROOT / "PART_CCCXXX_strange_yukawa_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["second_generation_hierarchy"]["y_s_over_y_c_squared"] == "Phi_4 = 10"
