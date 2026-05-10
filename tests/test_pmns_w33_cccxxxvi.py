"""
Part CCCXXXVI -- PMNS lepton-mixing angles in W(3,3)
Regression tests for exploration/PART_CCCXXXVI_PMNS_W33_BRIDGE.py
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCXXXVI_PMNS_W33_BRIDGE import (
    Q, V, K, LAM, MU, F, G, PHI3, PHI4, PHI6,
    SIN2_THETA_12_W33, SIN2_THETA_23_W33, SIN2_THETA_13_W33,
    SIN2_RATIO_W33,
    THETA_12_DEG_W33, THETA_23_DEG_W33, THETA_13_DEG_W33,
    SIN2_THETA_12, SIGMA_THETA_12,
    SIN2_THETA_23, SIGMA_THETA_23,
    SIN2_THETA_13, SIGMA_THETA_13,
    Z_12, Z_23, Z_13,
    residual_records, checks, Verified,
)


def test_verified_true():
    assert Verified is True


def test_all_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == [], f"Failing: {failed}"


def test_check_count():
    assert len(checks) == 22


def test_theta_12_W33_form():
    assert SIN2_THETA_12_W33 == Fraction(MU, PHI3)
    assert SIN2_THETA_12_W33 == Fraction(4, 13)


def test_theta_23_W33_form():
    assert SIN2_THETA_23_W33 == Fraction(MU, PHI6)
    assert SIN2_THETA_23_W33 == Fraction(4, 7)


def test_theta_13_W33_form():
    assert SIN2_THETA_13_W33 == Fraction(Q ** 2, (LAM * PHI4) ** 2)
    assert SIN2_THETA_13_W33 == Fraction(9, 400)


def test_decimals():
    assert abs(float(SIN2_THETA_12_W33) - 4/13) < 1e-12
    assert abs(float(SIN2_THETA_23_W33) - 4/7) < 1e-12
    assert float(SIN2_THETA_13_W33) == 0.0225


def test_all_within_1_sigma():
    assert abs(Z_12) < 1
    assert abs(Z_23) < 1
    assert abs(Z_13) < 1


def test_predicted_angles_in_window():
    # Solar ~33.4 deg
    assert 33 < THETA_12_DEG_W33 < 34
    # Atmospheric ~49 deg (upper octant)
    assert 48 < THETA_23_DEG_W33 < 50
    # Reactor ~8.6 deg
    assert 8.5 < THETA_13_DEG_W33 < 8.7


def test_solar_atmospheric_ratio():
    # sin^2 theta_12 / sin^2 theta_23 = Phi_6/Phi_3 = 7/13
    assert SIN2_RATIO_W33 == Fraction(PHI6, PHI3) == Fraction(7, 13)


def test_shared_numerator_mu():
    # Both solar and atmospheric have numerator mu = 4
    assert SIN2_THETA_12_W33.numerator == MU
    assert SIN2_THETA_23_W33.numerator == MU


def test_residual_records():
    records = residual_records()
    assert len(records) == 3
    assert all("PASS" in r.status for r in records)


# Cross-link with CCCXXX (y_s)
def test_phi4_in_pmns_and_strange_yukawa():
    # Phi_4 = 10 in sin^2 theta_13 = q^2/(lam*Phi_4)^2 = 9/400
    # Also in y_s = Phi_4/137^2 = 10/18769 (CCCXXX)
    assert PHI4 == 10
    Y_S = Fraction(PHI4, 137 ** 2)
    assert Y_S.numerator == PHI4


# JSON output
def test_json_exists_after_main():
    import importlib
    mod = importlib.import_module("PART_CCCXXXVI_PMNS_W33_BRIDGE")
    mod.main()
    assert (ROOT / "PART_CCCXXXVI_pmns_w33_results.json").exists()


def test_json_verified():
    out = ROOT / "PART_CCCXXXVI_pmns_w33_results.json"
    if not out.exists():
        import importlib
        importlib.import_module("PART_CCCXXXVI_PMNS_W33_BRIDGE").main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Verified"] is True


def test_json_predictions():
    out = ROOT / "PART_CCCXXXVI_pmns_w33_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["predictions"]["sin2_theta_12_W33"] == "4/13"
    assert data["predictions"]["sin2_theta_23_W33"] == "4/7"
    assert data["predictions"]["sin2_theta_13_W33"] == "9/400"
    assert data["predictions"]["ratio_12_over_23"] == "7/13"
