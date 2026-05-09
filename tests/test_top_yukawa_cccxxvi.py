"""
Part CCCXXVI -- Top Yukawa  y_t(pole)^3 = v / (v+1)
Regression tests for exploration/PART_CCCXXVI_TOP_YUKAWA_BRIDGE.py
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

from PART_CCCXXVI_TOP_YUKAWA_BRIDGE import (
    Q, V, K, LAM, MU, F, PHI3, PHI4, PHI6,
    Y_T_CUBED_W33, Y_T_W33,
    M_TOP_POLE, SIGMA_M_TOP_POLE, V_EW,
    Y_T_DATA, SIGMA_Y_T_DATA,
    M_TOP_PRED, RESIDUAL_M, Z_M,
    RESIDUAL_Y_T, Z_Y_T,
    y_t_from_m_top,
    residual_records,
    checks, Verified,
)


# Master gates
def test_verified_true():
    assert Verified is True


def test_all_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == [], f"Failing checks: {failed}"


def test_check_count():
    assert len(checks) == 20


# Closed-form W33 value
def test_y_t_cubed_W33():
    assert Y_T_CUBED_W33 == Fraction(V, V + 1)
    assert Y_T_CUBED_W33 == Fraction(40, 41)


def test_y_t_value():
    assert abs(Y_T_W33 ** 3 - float(Y_T_CUBED_W33)) < 1e-12
    # Numerical: (40/41)^(1/3) ~ 0.99180
    assert 0.991 < Y_T_W33 < 0.992


def test_components():
    assert V == 40
    assert V + 1 == 41


def test_y_t_W33_in_window():
    expected = (40/41) ** (1/3)
    assert abs(Y_T_W33 - expected) < 1e-12


# Tree-relation extraction
def test_tree_extraction_function():
    # m_t = 172.69, v = 246.22 -> y_t ≈ 0.9919
    val = y_t_from_m_top(172.69, 246.21965)
    assert abs(val - 0.99188) < 1e-4


def test_tree_extraction_value():
    expected = M_TOP_POLE * math.sqrt(2) / V_EW
    assert abs(Y_T_DATA - expected) < 1e-12


# Residual checks vs PDG
def test_y_t_within_1_sigma():
    assert abs(Z_Y_T) < 1


def test_y_t_within_0p1_sigma():
    assert abs(Z_Y_T) < 0.1   # actually within ~0.05 sigma


def test_m_top_within_1_sigma():
    assert abs(Z_M) < 1


def test_m_top_within_1_GeV():
    assert abs(RESIDUAL_M) < 1.0


def test_m_top_predicted_value():
    expected = (V_EW / math.sqrt(2)) * Y_T_W33
    assert abs(M_TOP_PRED - expected) < 1e-9
    assert 172.0 < M_TOP_PRED < 173.0


# Cross-link with CCCXXIII
def test_b1_SM_numerator():
    # b_1^SM = (v+1) / Phi_4 = 41/10
    b1 = Fraction(V + 1, PHI4)
    assert b1 == Fraction(41, 10)
    # Same numerator as y_t^3 denominator
    assert Y_T_CUBED_W33.denominator == b1.numerator == 41


# Equivalent inverse form: V = y_t^3 / (1 - y_t^3)
def test_v_recovered_from_y_t():
    v_recover = Y_T_W33 ** 3 / (1.0 - Y_T_W33 ** 3)
    assert abs(v_recover - V) < 1e-9


# Cross-link with CCCXXV (CKM lambda)
def test_v_appears_in_two_targets():
    # CKM lambda = q^2/v -> v in denominator
    LAM_CKM = Fraction(Q ** 2, V)
    assert LAM_CKM.denominator == V == 40
    # Top Yukawa cubed: y_t^3 = v/(v+1) -> v in numerator
    assert Y_T_CUBED_W33.numerator == V == 40


# Residual records
def test_three_residual_records():
    records = residual_records()
    assert len(records) == 3
    ids = {r.id for r in records}
    assert "TOP_YUKAWA_CUBED_W33" in ids
    assert "TOP_YUKAWA_LINEAR_W33" in ids
    assert "TOP_MASS_FROM_W33_AND_V" in ids


def test_all_records_pass():
    for rec in residual_records():
        assert "PASS" in rec.status, f"Record {rec.id} did not pass: {rec.status}"


# JSON output
def test_json_exists_after_main():
    import importlib
    mod = importlib.import_module("PART_CCCXXVI_TOP_YUKAWA_BRIDGE")
    mod.main()
    assert (ROOT / "PART_CCCXXVI_top_yukawa_results.json").exists()


def test_json_verified():
    out = ROOT / "PART_CCCXXVI_top_yukawa_results.json"
    if not out.exists():
        import importlib
        importlib.import_module("PART_CCCXXVI_TOP_YUKAWA_BRIDGE").main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Verified"] is True
    assert data["checks_passed"] == data["checks_total"]


def test_json_boundary_target():
    out = ROOT / "PART_CCCXXVI_top_yukawa_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["boundary_target"]["expression_cubed"] == "v / (v + 1)"
    assert data["boundary_target"]["value_cubed"] == "40/41"
