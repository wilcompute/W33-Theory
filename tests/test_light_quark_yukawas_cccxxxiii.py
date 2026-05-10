"""
Part CCCXXXIII -- Light-quark Yukawas y_d, y_u in W(3,3)
Regression tests for exploration/PART_CCCXXXIII_LIGHT_QUARK_YUKAWAS_BRIDGE.py
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCXXXIII_LIGHT_QUARK_YUKAWAS_BRIDGE import (
    Q, V, K, LAM, MU, F, G, PHI3, PHI4, PHI6, H_0, ALPHA_INV,
    Y_D_W33, Y_U_W33,
    Y_D_DATA, Y_U_DATA, SIGMA_Y_D_DATA, SIGMA_Y_U_DATA,
    M_D_MEV, M_U_MEV, V_EW_GEV,
    M_D_PRED_MEV, M_U_PRED_MEV,
    Z_Y_D, Z_Y_U,
    residual_records, checks, Verified,
)


def test_verified_true():
    assert Verified is True


def test_all_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == [], f"Failing: {failed}"


def test_check_count():
    assert len(checks) == 21


def test_y_d_form():
    assert Y_D_W33 == Fraction(H_0, ALPHA_INV ** 3)
    assert Y_D_W33 == Fraction(70, 137 ** 3)


def test_y_u_form():
    assert Y_U_W33 == Fraction(LAM ** 5, ALPHA_INV ** 3)
    assert Y_U_W33 == Fraction(32, 137 ** 3)


def test_H_0_value():
    assert H_0 == 70 == PHI6 * PHI4


def test_alpha_inv_137_cubed():
    assert ALPHA_INV ** 3 == 2571353


def test_lam5_eq_32():
    assert LAM ** 5 == 32


def test_y_d_within_1_sigma():
    assert abs(Z_Y_D) < 1


def test_y_u_within_1_sigma():
    assert abs(Z_Y_U) < 1


def test_y_u_within_0p1_sigma():
    assert abs(Z_Y_U) < 0.1


def test_m_d_pred_value():
    assert 4.4 < M_D_PRED_MEV < 5.0


def test_m_u_pred_value():
    assert 1.7 < M_U_PRED_MEV < 2.6


def test_up_down_ratio():
    ratio = Fraction(LAM ** 5, H_0)
    assert ratio == Fraction(16, 35)


def test_137_power_progression():
    # CCCXXIX: y_c = 1/137^1
    Y_C = Fraction(1, 137)
    # CCCXXX: y_s = Phi_4/137^2
    Y_S = Fraction(PHI4, 137 ** 2)
    # This part: y_d, y_u = */137^3
    assert Y_C.denominator == 137
    assert Y_S.denominator == 137 ** 2
    assert Y_D_W33.denominator == 137 ** 3
    assert Y_U_W33.denominator == 137 ** 3


def test_y_d_numerator_equals_H_0():
    # This is the cosmology coincidence
    assert Y_D_W33.numerator == H_0
    assert H_0 == 70


def test_residual_records():
    records = residual_records()
    assert len(records) == 2
    assert all("PASS" in r.status for r in records)


# JSON output
def test_json_exists_after_main():
    import importlib
    mod = importlib.import_module("PART_CCCXXXIII_LIGHT_QUARK_YUKAWAS_BRIDGE")
    mod.main()
    assert (ROOT / "PART_CCCXXXIII_light_quark_yukawas_results.json").exists()


def test_json_verified():
    out = ROOT / "PART_CCCXXXIII_light_quark_yukawas_results.json"
    if not out.exists():
        import importlib
        importlib.import_module("PART_CCCXXXIII_LIGHT_QUARK_YUKAWAS_BRIDGE").main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Verified"] is True
    assert data["checks_passed"] == data["checks_total"]


def test_json_predictions_present():
    out = ROOT / "PART_CCCXXXIII_light_quark_yukawas_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["predictions"]["y_u_over_y_d_W33"] == "16/35"
