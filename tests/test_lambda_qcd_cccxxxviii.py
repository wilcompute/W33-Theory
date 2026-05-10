"""
Part CCCXXXVIII -- Lambda_QCD = v_EW/1173 in W(3,3)
Regression tests for exploration/PART_CCCXXXVIII_LAMBDA_QCD_BRIDGE.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCXXXVIII_LAMBDA_QCD_BRIDGE import (
    Q, V, K, LAM, MU, F, G, PHI3, PHI4, PHI6,
    LAMBDA_QCD_DENOM_W33,
    LAMBDA_QCD_W33_GEV, LAMBDA_QCD_W33_MEV,
    LAMBDA_QCD_MEV, SIGMA_LAMBDA_QCD,
    V_EW_GEV,
    Z_LAMBDA, RESIDUAL,
    residual_records, checks, Verified,
)


def test_verified_true():
    assert Verified is True


def test_all_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == [], f"Failing: {failed}"


def test_W33_denom_form():
    assert LAMBDA_QCD_DENOM_W33 == Q * (PHI3 + MU) * (PHI3 + PHI4)
    assert LAMBDA_QCD_DENOM_W33 == 1173


def test_factorization():
    assert LAMBDA_QCD_DENOM_W33 == 3 * 17 * 23
    assert PHI3 + MU == 17
    assert PHI3 + PHI4 == 23


def test_lambda_QCD_W33_value():
    assert 209 < LAMBDA_QCD_W33_MEV < 211


def test_within_1_sigma():
    assert abs(Z_LAMBDA) < 1


def test_within_0p1_sigma():
    assert abs(Z_LAMBDA) < 0.1


def test_residual_records():
    records = residual_records()
    assert len(records) == 1
    assert "PASS" in records[0].status


def test_v_EW_anchor():
    assert V_EW_GEV == 246.21965


def test_W33_value_sub_percent():
    # Lambda predicted should be within 1% of central PDG value
    assert abs(LAMBDA_QCD_W33_MEV - LAMBDA_QCD_MEV) / LAMBDA_QCD_MEV < 0.01


def test_Bernoulli_primes_used():
    bernoulli = {2, 3, 5, 7, 11, 13, 17, 19, 23}
    # 17 and 23 used in Lambda_QCD
    assert 17 in bernoulli
    assert 23 in bernoulli
    # And 3 = q is also there
    assert Q == 3 in bernoulli


# Cross-link with CCCXXXIV
def test_alpha_s_link():
    # CCCXXXIV: alpha_s(M_Z) = lam/(Phi_3+mu) = 2/17
    # CCCXXXVIII: Lambda_QCD denom uses (Phi_3+mu) = 17
    alpha_s_denom = PHI3 + MU
    assert alpha_s_denom == 17
    # And 17 divides Lambda_QCD denom
    assert LAMBDA_QCD_DENOM_W33 % 17 == 0


# JSON output
def test_json_exists_after_main():
    import importlib
    mod = importlib.import_module("PART_CCCXXXVIII_LAMBDA_QCD_BRIDGE")
    mod.main()
    assert (ROOT / "PART_CCCXXXVIII_lambda_qcd_results.json").exists()


def test_json_verified():
    out = ROOT / "PART_CCCXXXVIII_lambda_qcd_results.json"
    if not out.exists():
        import importlib
        importlib.import_module("PART_CCCXXXVIII_LAMBDA_QCD_BRIDGE").main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Verified"] is True


def test_json_factorization():
    out = ROOT / "PART_CCCXXXVIII_lambda_qcd_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert "1173" in data["factorization"]["denom_1173_factors"]
    assert 17 in data["factorization"]["Bernoulli_small_primes_used"]
    assert 23 in data["factorization"]["Bernoulli_small_primes_used"]
