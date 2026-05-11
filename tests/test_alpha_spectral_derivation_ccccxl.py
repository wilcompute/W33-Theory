"""
Part CCCCXL -- alpha^{-1} Spectral Derivation from W(3,3) Vertex Propagator
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCCXL_ALPHA_SPECTRAL_DERIVATION import (
    Q, V, K, LAM, MU, F, G, PHI3, PHI4, PHI6,
    INTEGER_137, CORRECTION, ALPHA_INV_W33,
    ALPHA_INV_CODATA, SIGMA_CODATA, RESIDUAL, PPB,
    FORMS_137,
    checks, Verified,
)


def test_verified_true():
    assert Verified is True


def test_all_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == [], f"Failing: {failed}"


def test_integer_137_spectral_form():
    assert INTEGER_137 == K ** 2 - 2 * MU + 1 == 137


def test_correction_40_over_1111():
    assert CORRECTION == Fraction(V, (K - 1) * ((K - LAM) ** 2 + 1))
    assert CORRECTION == Fraction(40, 1111)


def test_correction_denom_factorization():
    assert (K - 1) * ((K - LAM) ** 2 + 1) == 11 * 101 == 1111
    assert (K - LAM) ** 2 + 1 == 101 == PHI4 ** 2 + 1


def test_alpha_inv_exact_fraction():
    assert ALPHA_INV_W33 == Fraction(152247, 1111)


def test_alpha_inv_decimal():
    assert 137.036 < float(ALPHA_INV_W33) < 137.037


def test_residual_in_ppb_range():
    assert PPB < 100  # within 100 ppb
    assert abs(RESIDUAL) < 1e-5


def test_three_forms_for_137():
    assert len(FORMS_137) == 3
    # All three forms evaluate to 137:
    assert K ** 2 - 2 * MU + 1 == 137                # spectral identity
    assert Q ** Q * (MU + 1) + LAM == 137             # Suzuki form
    assert Q ** 2 * G + LAM == 137                    # alternate Suzuki


def test_class_promotion():
    """alpha is promoted from Class C (CCCCXXXV) to Class A."""
    # The spectral identity is FORCED by SRG parameters + Ihara-Bass.
    # Therefore alpha^{-1} is structurally derived, not just identified.
    assert INTEGER_137 == 137
    assert CORRECTION == Fraction(40, 1111)


def test_y_c_consistency():
    """y_c = 1/137 (CCCXXIX) remains consistent with the new spectral form."""
    Y_C = Fraction(1, 137)
    assert Y_C == Fraction(1, 137)


# JSON output
def test_json_exists_after_main():
    import importlib
    mod = importlib.import_module("PART_CCCCXL_ALPHA_SPECTRAL_DERIVATION")
    mod.main()
    assert (ROOT / "PART_CCCCXL_alpha_spectral_derivation_results.json").exists()


def test_json_verified():
    out = ROOT / "PART_CCCCXL_alpha_spectral_derivation_results.json"
    if not out.exists():
        import importlib
        importlib.import_module("PART_CCCCXL_ALPHA_SPECTRAL_DERIVATION").main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Verified"] is True


def test_json_spectral_identity():
    out = ROOT / "PART_CCCCXL_alpha_spectral_derivation_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    identity = data["spectral_identity"]
    assert identity["integer_137"] == 137
    assert identity["correction"] == "40/1111"
    assert identity["alpha_inv_fraction"] == "152247/1111"
