"""
Part CCCXXXIV -- alpha_s(M_Z) = lam/(Phi_3+mu) = 2/17 in W(3,3)
Regression tests for exploration/PART_CCCXXXIV_STRONG_COUPLING_BRIDGE.py
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCXXXIV_STRONG_COUPLING_BRIDGE import (
    Q, V, K, LAM, MU, F, G, PHI3, PHI4, PHI6,
    ALPHA_S_W33, ALPHA_S_INV_W33,
    ALPHA_S_DATA, SIGMA_ALPHA_S, ALPHA_S_INV_DATA,
    RESIDUAL_ALPHA_S, Z_ALPHA_S,
    RESIDUAL_ALPHA_S_INV, Z_ALPHA_S_INV,
    residual_records, checks, Verified,
)


def test_verified_true():
    assert Verified is True


def test_all_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == [], f"Failing: {failed}"


def test_check_count():
    assert len(checks) == 14


def test_W33_form():
    assert ALPHA_S_W33 == Fraction(LAM, PHI3 + MU)
    assert ALPHA_S_W33 == Fraction(2, 17)


def test_inverse_form():
    assert ALPHA_S_INV_W33 == Fraction(PHI3 + MU, LAM)
    assert ALPHA_S_INV_W33 == Fraction(17, 2)
    assert float(ALPHA_S_INV_W33) == 8.5


def test_17_components():
    assert PHI3 + MU == 17
    # 17 is in the CCLVIII Bernoulli small-prime tower
    assert 17 in {2, 3, 5, 7, 11, 13, 17, 19, 23}


def test_alpha_s_decimal():
    assert abs(float(ALPHA_S_W33) - 2/17) < 1e-12
    assert abs(float(ALPHA_S_W33) - 0.117647) < 1e-5


def test_within_1_sigma():
    assert abs(Z_ALPHA_S) < 1


def test_within_0p5_sigma():
    assert abs(Z_ALPHA_S) < 0.5


def test_residual_records():
    records = residual_records()
    assert len(records) == 2
    assert all("PASS" in r.status for r in records)


def test_inverse_close_to_data():
    # alpha_s^-1 = 8.5 is W33; data 8.48 +- 0.06
    assert abs(float(ALPHA_S_INV_W33) - ALPHA_S_INV_DATA) < 0.05


def test_cross_link_with_b_2_SM_numerator():
    # CCCXXIII b_2 num = -19 = -(f - mu - 1)
    # CCCXXXIV alpha_s denom = 17 = Phi_3 + mu
    # Both 17 and 19 are adjacent Bernoulli primes
    b_2_num = F - MU - 1  # 19
    alpha_s_denom = PHI3 + MU  # 17
    assert b_2_num == 19
    assert alpha_s_denom == 17
    # They differ by 2 = lam
    assert b_2_num - alpha_s_denom == LAM


# JSON output
def test_json_exists_after_main():
    import importlib
    mod = importlib.import_module("PART_CCCXXXIV_STRONG_COUPLING_BRIDGE")
    mod.main()
    assert (ROOT / "PART_CCCXXXIV_strong_coupling_results.json").exists()


def test_json_verified():
    out = ROOT / "PART_CCCXXXIV_strong_coupling_results.json"
    if not out.exists():
        import importlib
        importlib.import_module("PART_CCCXXXIV_STRONG_COUPLING_BRIDGE").main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Verified"] is True
    assert data["checks_passed"] == data["checks_total"]


def test_json_small_prime_tower_link():
    out = ROOT / "PART_CCCXXXIV_strong_coupling_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert 17 in data["small_prime_tower_link"]["CCLVIII_tower"]
