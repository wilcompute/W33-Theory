"""
Part CCCXLIII -- Cosmological constant Lambda_cosmo: ln(v_EW/Lambda^{1/4}) = (q^q+H_0)/q = 97/3
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

from PART_CCCXLIII_COSMOLOGICAL_CONSTANT_BRIDGE import (
    Q, V, K, LAM, MU, F, G, PHI3, PHI4, PHI6, H_0,
    LN_RATIO_W33,
    OMEGA_LAMBDA, H_PLANCK, V_EW_GEV,
    LAMBDA_4_GEV, LAMBDA_4_meV,
    LN_RATIO_DATA, RESIDUAL, Z, SIGMA_LN,
    LAMBDA_4_W33_meV,
    residual_records, checks, Verified,
)


def test_verified_true():
    assert Verified is True


def test_all_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == [], f"Failing: {failed}"


def test_W33_form():
    assert LN_RATIO_W33 == Fraction(Q ** Q + H_0, Q)
    assert LN_RATIO_W33 == Fraction(97, 3)


def test_components():
    assert Q ** Q == 27
    assert H_0 == 70 == PHI6 * PHI4
    assert Q ** Q + H_0 == 97
    # 97 is prime
    for d in range(2, 10):
        assert 97 % d != 0


def test_decimal():
    assert abs(float(LN_RATIO_W33) - 32.333) < 0.01


def test_within_1_sigma():
    assert abs(Z) < 1


def test_predicted_Lambda_meV():
    assert 2.0 < LAMBDA_4_W33_meV < 2.5


def test_residual_records():
    records = residual_records()
    assert len(records) == 1
    assert "PASS" in records[0].status


# Cross-link with CCCXXXV cosmology and CCCXXXIII Yukawas
def test_q_cubed_appears_in_omega_c_over_b():
    OMEGA_C_OVER_B = Fraction(Q ** Q, MU + 1)
    assert OMEGA_C_OVER_B == Fraction(27, 5)


def test_H_0_appears_in_y_d():
    Y_D = Fraction(H_0, 137 ** 3)
    assert Y_D.numerator == H_0


# JSON output
def test_json_exists_after_main():
    import importlib
    mod = importlib.import_module("PART_CCCXLIII_COSMOLOGICAL_CONSTANT_BRIDGE")
    mod.main()
    assert (ROOT / "PART_CCCXLIII_cosmological_constant_results.json").exists()


def test_json_verified():
    out = ROOT / "PART_CCCXLIII_cosmological_constant_results.json"
    if not out.exists():
        import importlib
        importlib.import_module("PART_CCCXLIII_COSMOLOGICAL_CONSTANT_BRIDGE").main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Verified"] is True
