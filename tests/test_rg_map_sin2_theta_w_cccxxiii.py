"""
Part CCCXXIII -- RG Map for sin^2 theta_W = 3/8 -> M_Z
Regression tests for exploration/PART_CCCXXIII_RG_MAP_SIN2_THETA_W_BRIDGE.py
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCXXIII_RG_MAP_SIN2_THETA_W_BRIDGE import (
    Q, V, K, LAM, MU, F, PHI3, PHI4, PHI6,
    SIN2_THETA_W_GUT,
    B1_SM, B2_SM, B3_SM,
    B1_MSSM, B2_MSSM, B3_MSSM,
    M_Z, ALPHA_EM_INV_MZ, ALPHA_S_MZ,
    SIN2_THETA_EFF_LEPT, SIGMA_SIN2_EFF,
    SM_RESULT, MSSM_RESULT,
    predict_sin2_at_mz,
    run_inverse,
    find_unification_scale,
    split_em_into_12,
    checks, Verified,
)


# ---------------------------------------------------------------------------
# Master gates
# ---------------------------------------------------------------------------
def test_verified_true():
    assert Verified is True


def test_all_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == [], f"Failing checks: {failed}"


def test_check_count():
    assert len(checks) == 31


# ---------------------------------------------------------------------------
# Boundary value: sin^2(theta_W)(M_GUT) = 3/8
# ---------------------------------------------------------------------------
def test_boundary_value_exact():
    assert SIN2_THETA_W_GUT == Fraction(3, 8)


def test_boundary_value_W33_form():
    # 3/8 = q / lam^q
    assert SIN2_THETA_W_GUT == Fraction(Q, LAM ** Q)
    assert Q == 3
    assert LAM ** Q == 8


def test_boundary_value_decimal():
    assert float(SIN2_THETA_W_GUT) == 0.375


# ---------------------------------------------------------------------------
# SM beta functions in W(3,3) closed form
# ---------------------------------------------------------------------------
def test_b1_SM():
    assert B1_SM == Fraction(41, 10)
    assert B1_SM == Fraction(V + 1, PHI4)


def test_b2_SM():
    assert B2_SM == Fraction(-19, 6)
    assert B2_SM == Fraction(-(F - MU - 1), LAM * Q)


def test_b3_SM():
    assert B3_SM == Fraction(-7, 1)
    assert B3_SM == Fraction(-PHI6, 1)


# ---------------------------------------------------------------------------
# MSSM beta functions in W(3,3) closed form
# ---------------------------------------------------------------------------
def test_b1_MSSM():
    assert B1_MSSM == Fraction(33, 5)
    assert B1_MSSM == Fraction(Q * (K - 1), MU + 1)


def test_b2_MSSM():
    assert B2_MSSM == Fraction(1, 1)


def test_b3_MSSM():
    assert B3_MSSM == Fraction(-3, 1)
    assert B3_MSSM == Fraction(-Q, 1)


# ---------------------------------------------------------------------------
# 41 (the only beta-function prime above the CCLVIII Bernoulli tower)
# ---------------------------------------------------------------------------
def test_41_three_W33_forms():
    assert 41 == V + 1
    assert 41 == Q * K + (MU + 1)
    assert 41 == PHI4 * LAM ** 2 + 1


# ---------------------------------------------------------------------------
# RG running primitives
# ---------------------------------------------------------------------------
def test_run_inverse_at_MZ_is_identity():
    # alpha(M_Z)^{-1} should be unchanged when running to M_Z.
    assert run_inverse(float(B1_SM), 50.0, M_Z) == 50.0


def test_run_inverse_one_decade():
    # alpha^{-1}(10 M_Z) = alpha^{-1}(M_Z) - (b/2pi) ln(10).
    import math
    out = run_inverse(7.0, 100.0, 10 * M_Z)
    expected = 100.0 - (7.0 / (2 * math.pi)) * math.log(10.0)
    assert abs(out - expected) < 1e-10


def test_split_em_recovers_alpha_em():
    # 1/alpha_em = (5/3) * a1_inv + a2_inv ... actually: 1/alpha_em = 1/alpha_Y + 1/alpha_2
    # with alpha_1 = (5/3) alpha_Y, so alpha_Y = (3/5) alpha_1, 1/alpha_Y = (5/3)/alpha_1 ...
    # WAIT: alpha_Y = g'^2/4pi, alpha_1 = (5/3) alpha_Y, so 1/alpha_Y = (5/3) (1/alpha_1).
    a1_inv, a2_inv = split_em_into_12(127.952, 0.231)
    # 1/alpha_em = 1/alpha_Y + 1/alpha_2 = (5/3)/alpha_1 + 1/alpha_2
    em_inv_recover = (5.0 / 3.0) * a1_inv + a2_inv
    assert abs(em_inv_recover - 127.952) < 1e-9


# ---------------------------------------------------------------------------
# Numerical predictions
# ---------------------------------------------------------------------------
def test_SM_prediction_in_canonical_window():
    # SM one-loop prediction for sin^2 theta_W at M_Z is famously ~0.207.
    assert 0.20 < SM_RESULT.sin2_pred < 0.22


def test_MSSM_prediction_in_canonical_window():
    # MSSM one-loop prediction is famously ~0.231.
    assert 0.225 < MSSM_RESULT.sin2_pred < 0.235


def test_M_GUT_SM_in_canonical_window():
    # Famous SM unification scale ~10^14-10^15 GeV
    assert 1e13 < SM_RESULT.M_GUT_GeV < 1e16


def test_M_GUT_MSSM_in_canonical_window():
    # Famous MSSM unification scale ~2e16 GeV
    assert 1e15 < MSSM_RESULT.M_GUT_GeV < 1e17


def test_alpha_GUT_inv_reasonable():
    # alpha_GUT^{-1} ~ 24-27 in MSSM
    assert 20 < MSSM_RESULT.alpha_GUT_inv < 30


# ---------------------------------------------------------------------------
# Residuals vs measured Z-pole effective leptonic angle
# ---------------------------------------------------------------------------
def test_SM_residual_huge():
    # SM prediction is ~24 sigma below measured (one-loop) -- ruled out.
    assert SM_RESULT.z_score_vs_eff_lept < -100


def test_MSSM_residual_small():
    # MSSM is within one-loop precision (~5 sigma at one-loop, tightens at two-loop).
    assert abs(MSSM_RESULT.z_score_vs_eff_lept) < 10


def test_MSSM_dramatically_better_than_SM():
    # MSSM residual at least 30x smaller than SM residual.
    assert abs(MSSM_RESULT.residual_vs_eff_lept) * 30 <= abs(SM_RESULT.residual_vs_eff_lept)


# ---------------------------------------------------------------------------
# Internal consistency: SU(5) unification by construction
# ---------------------------------------------------------------------------
def test_SU5_unification_consistency_SM():
    assert SM_RESULT.M_GUT_consistency < 1e-6


def test_SU5_unification_consistency_MSSM():
    assert MSSM_RESULT.M_GUT_consistency < 1e-6


# ---------------------------------------------------------------------------
# Cross-check: consistency relation
# ---------------------------------------------------------------------------
def test_full_unification_relation_SM():
    # Manual cross-check of the closed-form solution.
    pred = predict_sin2_at_mz(float(B1_SM), float(B2_SM), float(B3_SM))
    s = pred["sin2_theta_W_pred"]
    assert abs(s - SM_RESULT.sin2_pred) < 1e-12


def test_full_unification_relation_MSSM():
    pred = predict_sin2_at_mz(float(B1_MSSM), float(B2_MSSM), float(B3_MSSM))
    s = pred["sin2_theta_W_pred"]
    assert abs(s - MSSM_RESULT.sin2_pred) < 1e-12


# ---------------------------------------------------------------------------
# JSON output
# ---------------------------------------------------------------------------
def test_json_exists_after_main():
    # Run main once to produce JSON
    import importlib
    mod = importlib.import_module("PART_CCCXXIII_RG_MAP_SIN2_THETA_W_BRIDGE")
    mod.main()
    assert (ROOT / "PART_CCCXXIII_rg_map_sin2_theta_w_results.json").exists()


def test_json_verified():
    out = ROOT / "PART_CCCXXIII_rg_map_sin2_theta_w_results.json"
    if not out.exists():
        import importlib
        importlib.import_module("PART_CCCXXIII_RG_MAP_SIN2_THETA_W_BRIDGE").main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Verified"] is True
    assert data["checks_passed"] == data["checks_total"]


def test_json_boundary_target():
    out = ROOT / "PART_CCCXXIII_rg_map_sin2_theta_w_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["boundary_target"]["value"] == "3/8"
    assert data["boundary_target"]["expression"] == "q / lam^q"


def test_json_beta_function_forms():
    out = ROOT / "PART_CCCXXIII_rg_map_sin2_theta_w_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    sm = data["beta_functions_W33"]["SM"]
    mssm = data["beta_functions_W33"]["MSSM"]
    assert sm["b1_form"] == "(v+1)/Phi_4"
    assert sm["b2_form"] == "-(f - mu - 1)/(lam*q)"
    assert sm["b3_form"] == "-Phi_6"
    assert mssm["b1_form"] == "q*(k-1)/(mu+1)"
    assert mssm["b2_form"] == "1"
    assert mssm["b3_form"] == "-q"


def test_json_external_inputs_present():
    out = ROOT / "PART_CCCXXIII_rg_map_sin2_theta_w_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    inp = data["external_inputs"]
    assert inp["M_Z_GeV"] == M_Z
    assert inp["alpha_em_inv_MZ"] == ALPHA_EM_INV_MZ
    assert inp["alpha_s_MZ"] == ALPHA_S_MZ
    assert "PDG" in inp["source"]
