"""
Part CCCXXIX -- Charm Yukawa  y_c(MSbar, m_c) = 1/137
Regression tests for exploration/PART_CCCXXIX_CHARM_YUKAWA_BRIDGE.py
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

from PART_CCCXXIX_CHARM_YUKAWA_BRIDGE import (
    Q, V, K, LAM, MU, F, G, PHI3, PHI4, PHI6,
    Y_C_W33,
    ALPHA_INV_W33, ALPHA_INV_ALT,
    M_C_MSBAR, SIGMA_M_C_MSBAR, V_EW, ALPHA_EM_INV_0,
    Y_C_DATA, SIGMA_Y_C_DATA,
    M_C_PRED, RESIDUAL_M_C, Z_M_C,
    RESIDUAL_Y_C, Z_Y_C,
    y_c_from_m_c,
    residual_records,
    checks, Verified,
)


def test_verified_true():
    assert Verified is True


def test_all_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == [], f"Failing: {failed}"


def test_check_count():
    assert len(checks) == 13


def test_W33_form():
    assert Y_C_W33 == Fraction(1, 137)


def test_137_W33_forms():
    # Two independent W(3,3) forms for 137
    assert ALPHA_INV_W33 == Q ** Q * (MU + 1) + LAM == 137
    assert ALPHA_INV_ALT == Q ** 2 * G + LAM == 137
    assert ALPHA_INV_W33 == ALPHA_INV_ALT


def test_135_equivalence():
    # 135 = q^q*(mu+1) = q^2*g
    assert Q ** Q * (MU + 1) == 135
    assert Q ** 2 * G == 135
    # 137 = 135 + lam
    assert 135 + LAM == 137


def test_decimal():
    assert abs(float(Y_C_W33) - 1/137) < 1e-12


def test_y_c_within_1_sigma():
    assert abs(Z_Y_C) < 1


def test_y_c_within_0p1_sigma():
    assert abs(Z_Y_C) < 0.1


def test_m_c_within_1_sigma():
    assert abs(Z_M_C) < 1


def test_m_c_pred_value():
    expected = float(Y_C_W33) * V_EW / math.sqrt(2)
    assert abs(M_C_PRED - expected) < 1e-9
    assert 1.2 < M_C_PRED < 1.4


# Fine structure relation
def test_y_c_W33_close_to_alpha_em():
    # y_c_W33 = 1/137 exact;  alpha_em(0) ~ 1/137.036
    assert abs(float(Y_C_W33) - 1/ALPHA_EM_INV_0) / (1/ALPHA_EM_INV_0) < 0.0005


# Cross-link with bottom Yukawa CCCXXVIII
def test_y_b_y_c_relation():
    Y_B = Fraction(Q, (MU + 1) ** 3)         # 3/125 from CCCXXVIII
    # 137 - 125 = 12 = k
    assert 137 - 125 == K == 12


def test_y_c_extraction_function():
    val = y_c_from_m_c(1.27, 246.21965)
    assert abs(val - 0.00730) < 1e-3


def test_residual_records():
    records = residual_records()
    assert len(records) == 2
    assert all("PASS" in r.status for r in records)


# JSON output
def test_json_exists_after_main():
    import importlib
    mod = importlib.import_module("PART_CCCXXIX_CHARM_YUKAWA_BRIDGE")
    mod.main()
    assert (ROOT / "PART_CCCXXIX_charm_yukawa_results.json").exists()


def test_json_verified():
    out = ROOT / "PART_CCCXXIX_charm_yukawa_results.json"
    if not out.exists():
        import importlib
        importlib.import_module("PART_CCCXXIX_CHARM_YUKAWA_BRIDGE").main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Verified"] is True
    assert data["checks_passed"] == data["checks_total"]


def test_json_fine_structure_link():
    out = ROOT / "PART_CCCXXIX_charm_yukawa_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["fine_structure_link"]["y_c_inv"] == 137
    assert "Suzuki" in data["fine_structure_link"]["comment"] or "fine-structure" in data["fine_structure_link"]["comment"]
