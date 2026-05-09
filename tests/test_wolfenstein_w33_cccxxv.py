"""
Part CCCXXV -- Wolfenstein CKM parameters in W(3,3) closed form
Regression tests for exploration/PART_CCCXXV_WOLFENSTEIN_W33_BRIDGE.py
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

from PART_CCCXXV_WOLFENSTEIN_W33_BRIDGE import (
    Q, V, K, LAM, MU, F, G, PHI3, PHI4, PHI6,
    LAMBDA_W33, A_W33, RHO_BAR_W33, ETA_BAR_W33,
    VCB_W33, VUB_W33, GAMMA_W33_DEG, GAMMA_W33_RAD,
    PDG,
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
    assert len(checks) == 36


# Closed-form W(3,3) parameter values
def test_lambda_form():
    assert LAMBDA_W33 == Fraction(Q ** 2, V)
    assert LAMBDA_W33 == Fraction(9, 40)


def test_A_form():
    assert A_W33 == Fraction(Q ** 4, PHI4 ** 2)
    assert A_W33 == Fraction(81, 100)


def test_rho_bar_form():
    assert RHO_BAR_W33 == Fraction(LAM, MU + 1) ** 2
    assert RHO_BAR_W33 == Fraction(4, 25)


def test_eta_bar_form():
    assert ETA_BAR_W33 == Fraction(PHI6, PHI4) ** 3
    assert ETA_BAR_W33 == Fraction(343, 1000)


def test_decimals():
    assert float(LAMBDA_W33) == 0.225
    assert float(A_W33) == 0.81
    assert float(RHO_BAR_W33) == 0.16
    assert float(ETA_BAR_W33) == 0.343


# Residual checks vs PDG 2024
def test_lambda_within_1_sigma():
    rec = next(r for r in residual_records() if r.parameter == "lambda")
    assert abs(rec.z_score) < 1


def test_A_within_1_sigma():
    rec = next(r for r in residual_records() if r.parameter == "A")
    assert abs(rec.z_score) < 1


def test_rho_bar_within_1_sigma():
    rec = next(r for r in residual_records() if r.parameter == "rho_bar")
    assert abs(rec.z_score) < 1


def test_eta_bar_within_1_sigma():
    rec = next(r for r in residual_records() if r.parameter == "eta_bar")
    assert abs(rec.z_score) < 1


# Derived predictions
def test_Vcb_value():
    expected = float(A_W33) * float(LAMBDA_W33) ** 2
    assert abs(VCB_W33 - expected) < 1e-12
    # Within 1 sigma of PDG
    meas, sigma = PDG["Vcb"]
    assert abs(VCB_W33 - meas) / sigma < 1


def test_Vub_value():
    expected = float(A_W33) * float(LAMBDA_W33) ** 3 * math.sqrt(
        float(RHO_BAR_W33) ** 2 + float(ETA_BAR_W33) ** 2
    )
    assert abs(VUB_W33 - expected) < 1e-12
    # Within 2 sigma (known PDG inclusive/exclusive band)
    meas, sigma = PDG["Vub"]
    assert abs(VUB_W33 - meas) / sigma < 2


def test_gamma_value():
    expected = math.degrees(math.atan2(float(ETA_BAR_W33), float(RHO_BAR_W33)))
    assert abs(GAMMA_W33_DEG - expected) < 1e-9
    meas, sigma = PDG["gamma_deg"]
    assert abs(GAMMA_W33_DEG - meas) / sigma < 1


def test_gamma_rad_consistent():
    assert abs(math.degrees(GAMMA_W33_RAD) - GAMMA_W33_DEG) < 1e-9


# W(3,3) form structure
def test_lambda_components():
    assert LAMBDA_W33.numerator == Q ** 2 == 9
    assert LAMBDA_W33.denominator == V == 40


def test_A_components():
    assert A_W33.numerator == Q ** 4 == 81
    assert A_W33.denominator == PHI4 ** 2 == 100


def test_rho_bar_components():
    assert RHO_BAR_W33.numerator == LAM ** 2 == 4
    assert RHO_BAR_W33.denominator == (MU + 1) ** 2 == 25


def test_eta_bar_components():
    assert ETA_BAR_W33.numerator == PHI6 ** 3 == 343
    assert ETA_BAR_W33.denominator == PHI4 ** 3 == 1000


# Cross-link with prior W33 parts
def test_A_and_lambda_H_share_denominator():
    # CCCXXIV: lambda_H = Phi_3 / Phi_4^2 = 13/100
    LAMBDA_H = Fraction(PHI3, PHI4 ** 2)
    assert A_W33.denominator == LAMBDA_H.denominator == PHI4 ** 2 == 100


def test_q_appears_in_three_W33_targets():
    # sin^2 theta_W = q/lam^q (CCCXXIII), num q
    SIN2 = Fraction(Q, LAM ** Q)
    assert SIN2.numerator == Q
    # lambda_W = q^2 / v (CCCXXV)
    assert LAMBDA_W33.numerator == Q ** 2
    # A = q^4 / Phi_4^2 (CCCXXV)
    assert A_W33.numerator == Q ** 4


# Residual records
def test_seven_residual_records():
    records = residual_records()
    assert len(records) == 7  # 4 Wolfenstein + V_cb + V_ub + gamma


def test_all_records_have_status_field():
    for rec in residual_records():
        assert rec.status.startswith("PASS") or rec.status == "DISFAVORED"


def test_pdg_dict_keys():
    keys = set(PDG.keys())
    assert {"lambda", "A", "rho_bar", "eta_bar", "Vcb", "Vub", "gamma_deg", "Vus"} <= keys


# JSON output
def test_json_exists_after_main():
    import importlib
    mod = importlib.import_module("PART_CCCXXV_WOLFENSTEIN_W33_BRIDGE")
    mod.main()
    assert (ROOT / "PART_CCCXXV_wolfenstein_w33_results.json").exists()


def test_json_verified():
    out = ROOT / "PART_CCCXXV_wolfenstein_w33_results.json"
    if not out.exists():
        import importlib
        importlib.import_module("PART_CCCXXV_WOLFENSTEIN_W33_BRIDGE").main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Verified"] is True
    assert data["checks_passed"] == data["checks_total"]


def test_json_wolfenstein_fractions():
    out = ROOT / "PART_CCCXXV_wolfenstein_w33_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["wolfenstein"]["lambda"]["fraction"] == "9/40"
    assert data["wolfenstein"]["A"]["fraction"] == "81/100"
    assert data["wolfenstein"]["rho_bar"]["fraction"] == "4/25"
    assert data["wolfenstein"]["eta_bar"]["fraction"] == "343/1000"


def test_json_derived_predictions():
    out = ROOT / "PART_CCCXXV_wolfenstein_w33_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert abs(data["derived"]["Vcb"]["value"] - 0.04101) < 1e-4
    assert abs(data["derived"]["gamma_deg"]["value"] - 64.99) < 0.1
