"""
Part CCCCXLI -- alpha^{-1} Refined Spectral Identity (Gaussian Integer Form)
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCCXLI_ALPHA_GAUSSIAN_REFINED import (
    Q, V, K, LAM, MU, F, G, PHI3, PHI4, PHI6,
    Z_RE, Z_IM, Z_MOD_SQ, Z_SQUARED_RE, Z_SQUARED_IM,
    M_VAC, DELTA_M, M_EFF, CORRECTION,
    ALPHA_INV_W33_GAUSSIAN,
    ALPHA_INV_CODATA, SIGMA_CODATA,
    RESIDUAL, PPB,
    FORMS_137,
    checks, Verified,
)


def test_verified_true():
    assert Verified is True


def test_all_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == [], f"Failing: {failed}"


def test_gaussian_integer():
    assert Z_RE == 11
    assert Z_IM == 4
    assert Z_MOD_SQ == Z_RE ** 2 + Z_IM ** 2 == 137


def test_z_squared_decomp():
    """z^2 = 105 + 88i with Re = q*(mu+1)*Phi_6 and Im = 2*mu*(k-1)."""
    assert Z_SQUARED_RE == 105 == Q * (MU + 1) * PHI6
    assert Z_SQUARED_IM == 88 == 2 * MU * (K - 1)


def test_M_vac():
    assert M_VAC == (K - 1) * ((K - LAM) ** 2 + 1) == 1111


def test_Delta_M():
    assert DELTA_M == Fraction(Q, LAM * (K - 1))
    assert DELTA_M == Fraction(3, 22)


def test_M_eff():
    assert M_EFF == Fraction(24445, 22)


def test_alpha_inv_exact():
    assert ALPHA_INV_W33_GAUSSIAN == Fraction(669969, 4889)
    assert CORRECTION == Fraction(880, 24445) == Fraction(176, 4889)


def test_alpha_inv_decimal():
    assert abs(float(ALPHA_INV_W33_GAUSSIAN) - 137.035999) < 1e-6


def test_within_1_ppb():
    """Match CODATA to within 1 ppb."""
    assert PPB < 1.0


def test_137_is_33rd_prime():
    """133 = q*(k-1), and 137 is the 33rd prime."""
    def is_prime(n):
        return n > 1 and all(n % d != 0 for d in range(2, int(n**0.5) + 1))
    primes = [p for p in range(2, 200) if is_prime(p)]
    assert primes.index(137) + 1 == 33
    assert 33 == Q * (K - 1)


def test_five_W33_forms_for_137():
    assert len(FORMS_137) == 5
    # All five forms evaluate to 137:
    assert (K - 1) ** 2 + MU ** 2 == 137                # Gaussian
    assert PHI3 * PHI4 + PHI6 == 137                     # cyclotomic
    assert K ** 2 - 2 * MU + 1 == 137                     # spectral
    assert Q ** Q * (MU + 1) + LAM == 137                 # Suzuki
    assert Q ** 2 * G + LAM == 137                        # alt Suzuki


# JSON output
def test_json_exists_after_main():
    import importlib
    mod = importlib.import_module("PART_CCCCXLI_ALPHA_GAUSSIAN_REFINED")
    mod.main()
    assert (ROOT / "PART_CCCCXLI_alpha_gaussian_refined_results.json").exists()


def test_json_verified():
    out = ROOT / "PART_CCCCXLI_alpha_gaussian_refined_results.json"
    if not out.exists():
        import importlib
        importlib.import_module("PART_CCCCXLI_ALPHA_GAUSSIAN_REFINED").main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Verified"] is True


def test_json_three_derivations():
    out = ROOT / "PART_CCCCXLI_alpha_gaussian_refined_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    derivations = data["three_alpha_derivations"]
    assert "Gaussian_integer_paper" in derivations
    assert "spectral_identity_simple" in derivations
    assert "cyclotomic_sum_integer" in derivations
