"""
Part CCCXXIV -- Higgs Quartic lambda_H = Phi_3 / Phi_4^2
Regression tests for exploration/PART_CCCXXIV_HIGGS_QUARTIC_BRIDGE.py
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCXXIV_HIGGS_QUARTIC_BRIDGE import (
    Q, V, K, LAM, MU, F, PHI3, PHI4, PHI6,
    LAMBDA_H_W33,
    M_H, SIGMA_M_H, V_EW, SIGMA_V_EW,
    LAMBDA_H_TREE, SIGMA_LAMBDA_H_TREE,
    LAMBDA_H_MZ_REF, SIGMA_LAMBDA_H_MZ,
    LAMBDA_H_MTOP_REF,
    M_H_PRED,
    RESIDUAL_LAMBDA_TREE, Z_LAMBDA_TREE,
    RESIDUAL_LAMBDA_MZ,   Z_LAMBDA_MZ,
    RESIDUAL_M_H,         Z_M_H,
    lambda_H_from_mH,
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
    assert len(checks) == 18


# The W33 form
def test_lambda_H_W33_value():
    assert LAMBDA_H_W33 == Fraction(13, 100)


def test_lambda_H_W33_form():
    assert LAMBDA_H_W33 == Fraction(PHI3, PHI4 ** 2)


def test_lambda_H_W33_decimal():
    assert float(LAMBDA_H_W33) == 0.13


def test_phi3_value():
    assert PHI3 == 13
    assert PHI3 == Q * Q + Q + 1


def test_phi4_squared():
    assert PHI4 ** 2 == 100
    assert PHI4 == Q * Q + 1


def test_lambda_H_W33_numerator_denominator():
    assert LAMBDA_H_W33.numerator == PHI3
    assert LAMBDA_H_W33.denominator == PHI4 ** 2


# Tree-relation extraction
def test_tree_extraction_function():
    # Test the helper function
    assert abs(lambda_H_from_mH(125.20, 246.21965) - 0.12928) < 1e-4
    # Symmetry: lambda_H ~ (m_H/v)^2/2
    assert lambda_H_from_mH(0, 100) == 0


def test_tree_extraction_value():
    # m_H = 125.20, v = 246.22 -> lambda_H = (125.20/246.22)^2/2 = 0.1293
    expected = (M_H / V_EW) ** 2 / 2
    assert abs(LAMBDA_H_TREE - expected) < 1e-12


def test_tree_uncertainty_positive():
    assert SIGMA_LAMBDA_H_TREE > 0
    assert SIGMA_LAMBDA_H_TREE < 0.001  # ~0.0002


# MS-bar at M_Z (Buttazzo reference value)
def test_msbar_central_consistent_with_W33():
    # Reference value at M_Z is 0.13050, W33 is 0.13000 — within 1 sigma.
    assert abs(Z_LAMBDA_MZ) < 2


def test_msbar_residual_small():
    assert abs(RESIDUAL_LAMBDA_MZ) < 0.005


# Higgs mass prediction
def test_m_H_predicted_within_1_GeV():
    assert abs(M_H_PRED - M_H) < 1.0


def test_m_H_predicted_value():
    import math
    expected = V_EW * math.sqrt(2.0 * float(LAMBDA_H_W33))
    assert abs(M_H_PRED - expected) < 1e-9


def test_m_H_predicted_in_PDG_window():
    # Predicted 125.55 GeV is within the LHC 2010-era central uncertainty window.
    assert 124 < M_H_PRED < 127


# Cross-link with W33 weak mixing 3/8 (CCCXXIII)
def test_both_W33_targets_have_q_in_numerator():
    # sin^2 theta_W = q / lam^q   (numerator q)
    # lambda_H     = Phi_3 / Phi_4^2  (numerator Phi_3 = q^2+q+1)
    sin2_GUT = Fraction(Q, LAM ** Q)
    assert sin2_GUT.numerator == Q
    # lambda_H numerator is Phi_3 = q^2 + q + 1, contains q implicitly
    assert LAMBDA_H_W33.numerator == Q * Q + Q + 1


def test_lambda_H_times_phi4_squared_equals_phi3():
    # The theorem in integer form
    assert LAMBDA_H_W33 * PHI4 ** 2 == PHI3


# Buttazzo near-criticality
def test_lambda_H_M_t_close_to_W33():
    # Buttazzo reports lambda_H(M_t) ~ 0.126; W33 0.130 is within 5 %.
    assert abs(LAMBDA_H_MTOP_REF - float(LAMBDA_H_W33)) / float(LAMBDA_H_W33) < 0.05


# Residual records
def test_three_residual_records():
    records = residual_records()
    assert len(records) == 3
    ids = [r.id for r in records]
    assert "HIGGS_QUARTIC_TREE_RELATION_FROM_MH_V" in ids
    assert "HIGGS_QUARTIC_MSBAR_AT_MZ_REF" in ids
    assert "HIGGS_MASS_FROM_LAMBDA_H_W33_AND_V" in ids


def test_msbar_record_passes():
    records = residual_records()
    msbar = next(r for r in records if r.id == "HIGGS_QUARTIC_MSBAR_AT_MZ_REF")
    assert "PASS" in msbar.status


# JSON output
def test_json_exists_after_main():
    import importlib
    mod = importlib.import_module("PART_CCCXXIV_HIGGS_QUARTIC_BRIDGE")
    mod.main()
    assert (ROOT / "PART_CCCXXIV_higgs_quartic_results.json").exists()


def test_json_verified():
    out = ROOT / "PART_CCCXXIV_higgs_quartic_results.json"
    if not out.exists():
        import importlib
        importlib.import_module("PART_CCCXXIV_HIGGS_QUARTIC_BRIDGE").main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Verified"] is True
    assert data["checks_passed"] == data["checks_total"]


def test_json_boundary_target():
    out = ROOT / "PART_CCCXXIV_higgs_quartic_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["boundary_target"]["expression"] == "Phi_3 / Phi_4^2"
    assert data["boundary_target"]["decimal"] == 0.13
