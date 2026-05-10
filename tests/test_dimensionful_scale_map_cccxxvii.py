"""
Part CCCXXVII -- Dimensionful Scale Map and SM Closure Audit
Regression tests for exploration/PART_CCCXXVII_DIMENSIONFUL_SCALE_MAP_BRIDGE.py
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCXXVII_DIMENSIONFUL_SCALE_MAP_BRIDGE import (
    Q, V, K, LAM, MU, F, G, PHI3, PHI4, PHI6,
    KOIDE_W33, SIN2_GUT_W33, LAMBDA_H_W33,
    LAMBDA_W33, A_W33, RHO_BAR_W33, ETA_BAR_W33,
    Y_T_CUBED_W33,
    V_EW, PDG_DIM,
    M_H_PRED, M_TOP_PRED,
    CLOSURES, DIM_CLOSURES, OPEN_BOUNDARIES,
    predict_m_H, predict_m_top,
    checks, Verified,
)


# Master gates
def test_verified_true():
    assert Verified is True


def test_all_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == [], f"Failing checks: {failed}"


# Closure inventory
def test_eight_dimensionless_closures():
    assert len(CLOSURES) == 8


def test_two_dimensional_closures():
    assert len(DIM_CLOSURES) == 2


def test_six_or_more_within_1_sigma():
    within = sum(1 for c in CLOSURES if abs(c.z_score) < 1)
    assert within >= 6


def test_seven_or_more_within_2_sigma():
    within = sum(1 for c in CLOSURES if abs(c.z_score) < 2)
    assert within >= 7


# Open boundaries
def test_open_boundaries_enumerated():
    assert len(OPEN_BOUNDARIES) >= 7


def test_open_boundaries_include_lambda_QCD():
    text = " ".join(OPEN_BOUNDARIES)
    assert "Lambda_QCD" in text or "QCD" in text


def test_open_boundaries_include_M_Pl():
    text = " ".join(OPEN_BOUNDARIES)
    assert "M_Pl" in text


# Single anchor
def test_v_EW_anchor():
    assert V_EW == 246.21965


# m_H prediction
def test_m_H_prediction_value():
    expected = V_EW * (2 * 13 / 100) ** 0.5
    assert abs(M_H_PRED - expected) < 1e-9


def test_m_H_within_1_GeV():
    assert abs(M_H_PRED - PDG_DIM["m_H_GeV"][0]) < 1.0


def test_m_H_predict_function():
    assert abs(predict_m_H(V_EW) - M_H_PRED) < 1e-12


# m_top prediction
def test_m_top_prediction_value():
    expected = (V_EW / (2 ** 0.5)) * (40 / 41) ** (1 / 3)
    assert abs(M_TOP_PRED - expected) < 1e-9


def test_m_top_within_1_sigma():
    z = (M_TOP_PRED - PDG_DIM["m_t_pole_GeV"][0]) / PDG_DIM["m_t_pole_GeV"][1]
    assert abs(z) < 1


def test_m_top_predict_function():
    assert abs(predict_m_top(V_EW) - M_TOP_PRED) < 1e-12


# All eight W33 closure forms
def test_koide_W33():
    assert KOIDE_W33 == Fraction(2, 3)


def test_sin2_GUT_W33():
    assert SIN2_GUT_W33 == Fraction(3, 8)


def test_lambda_H_W33():
    assert LAMBDA_H_W33 == Fraction(13, 100)


def test_CKM_lambda_W33():
    assert LAMBDA_W33 == Fraction(9, 40)


def test_CKM_A_W33():
    assert A_W33 == Fraction(81, 100)


def test_CKM_rho_bar_W33():
    assert RHO_BAR_W33 == Fraction(4, 25)


def test_CKM_eta_bar_W33():
    assert ETA_BAR_W33 == Fraction(343, 1000)


def test_y_t_cubed_W33():
    assert Y_T_CUBED_W33 == Fraction(40, 41)


# Cross-link integers
def test_v_in_three_closures():
    # CKM lambda: q^2/v -> v in denominator
    assert LAMBDA_W33.denominator == V == 40
    # y_t^3: v/(v+1) -> v in numerator
    assert Y_T_CUBED_W33.numerator == V == 40


def test_phi4_squared_in_two_closures():
    # lambda_H denominator and A denominator both = Phi_4^2
    assert LAMBDA_H_W33.denominator == 100
    assert A_W33.denominator == 100
    assert PHI4 ** 2 == 100


def test_41_links_gauge_and_top_yukawa():
    # b_1^SM numerator = (v+1) = 41
    # y_t^3 denominator = (v+1) = 41
    b1_num = V + 1  # numerator of b_1^SM = (v+1)/Phi_4
    yt_denom = Y_T_CUBED_W33.denominator
    assert b1_num == yt_denom == 41


# Closure record structure
def test_closure_records_have_required_fields():
    for c in CLOSURES:
        assert c.part
        assert c.sector
        assert c.observable
        assert c.W33_form
        assert isinstance(c.W33_value, float)
        assert isinstance(c.PDG_value, float)
        assert isinstance(c.PDG_sigma, float)
        assert "PASS" in c.status or "DISFAVORED" in c.status


# JSON output
def test_json_exists_after_main():
    import importlib
    mod = importlib.import_module("PART_CCCXXVII_DIMENSIONFUL_SCALE_MAP_BRIDGE")
    mod.main()
    assert (ROOT / "PART_CCCXXVII_dimensionful_scale_map_results.json").exists()


def test_json_verified():
    out = ROOT / "PART_CCCXXVII_dimensionful_scale_map_results.json"
    if not out.exists():
        import importlib
        importlib.import_module("PART_CCCXXVII_DIMENSIONFUL_SCALE_MAP_BRIDGE").main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Verified"] is True
    assert data["checks_passed"] == data["checks_total"]


def test_json_anchor():
    out = ROOT / "PART_CCCXXVII_dimensionful_scale_map_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["dimensional_anchor"]["v_EW_GeV"] == V_EW


def test_json_eight_closures():
    out = ROOT / "PART_CCCXXVII_dimensionful_scale_map_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert len(data["dimensionless_closures"]) == 8
