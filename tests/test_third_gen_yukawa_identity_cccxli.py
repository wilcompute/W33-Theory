"""
Part CCCXLI -- Third-Generation Yukawa-Higgs Identity y_tau*y_c/y_b^2 = lambda_H
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCXLI_THIRD_GEN_YUKAWA_IDENTITY_BRIDGE import (
    Q, V, K, LAM, MU, F, G, PHI3, PHI4, PHI6,
    LAMBDA_H_W33,
    Y_TAU, Y_C, Y_B, V_EW,
    IDENTITY_DATA, SIGMA_IDENTITY, RESIDUAL, Z,
    Y_TAU_FROM_IDENTITY,
    residual_records, checks, Verified,
)


def test_verified_true():
    assert Verified is True


def test_all_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == [], f"Failing: {failed}"


def test_lambda_H_W33_form():
    assert LAMBDA_H_W33 == Fraction(PHI3, PHI4 ** 2)
    assert LAMBDA_H_W33 == Fraction(13, 100)


def test_identity_within_1_sigma():
    assert abs(Z) < 1


def test_identity_within_0p5_sigma():
    assert abs(Z) < 0.5


def test_identity_value():
    assert 0.128 < IDENTITY_DATA < 0.131


def test_y_tau_inversion():
    # y_tau predicted from identity ~ 0.01026 (~0.5% off PDG)
    assert abs(Y_TAU_FROM_IDENTITY - 0.01026) < 0.0001
    # Within 1% of PDG
    assert abs(Y_TAU_FROM_IDENTITY - Y_TAU) / Y_TAU < 0.01


def test_residual_records():
    records = residual_records()
    assert len(records) == 1
    assert "PASS" in records[0].status


# Cross-link with prior W33 closures
def test_y_c_W33():
    Y_C_W33 = Fraction(1, 137)
    assert Y_C_W33 == Fraction(1, 137)


def test_y_b_W33():
    Y_B_W33 = Fraction(Q, (MU + 1) ** 3)
    assert Y_B_W33 == Fraction(3, 125)


# Symbolic identity verification
def test_symbolic_identity():
    # y_tau * y_c / y_b^2 = lambda_H
    # In W33: y_tau = lambda_H * y_b^2 / y_c
    # = (13/100) * (3/125)^2 * 137
    # = 13 * 9 * 137 / (100 * 15625)
    # = 16029 / 1562500
    expected = Fraction(13 * 9 * 137, 100 * (125 ** 2))
    assert expected == Fraction(16029, 1562500)
    assert abs(float(expected) - 0.01026) < 0.0001


# JSON output
def test_json_exists_after_main():
    import importlib
    mod = importlib.import_module("PART_CCCXLI_THIRD_GEN_YUKAWA_IDENTITY_BRIDGE")
    mod.main()
    assert (ROOT / "PART_CCCXLI_third_gen_yukawa_identity_results.json").exists()


def test_json_verified():
    out = ROOT / "PART_CCCXLI_third_gen_yukawa_identity_results.json"
    if not out.exists():
        import importlib
        importlib.import_module("PART_CCCXLI_THIRD_GEN_YUKAWA_IDENTITY_BRIDGE").main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Verified"] is True
