"""BT1133 regression tests for finite W33 heat moments.

These tests lock the finite Hodge--Dirac square spectrum used by the K3 product
heat split.  They prevent future paper edits from confusing the pure K3
coefficients A_i with the product coefficients C_i.
"""

from fractions import Fraction

SPECTRUM_DF_SQUARED = {
    0: 122,
    4: 240,
    10: 48,
    16: 30,
}


def _moment(power: int) -> int:
    return sum((lam ** power) * mult for lam, mult in SPECTRUM_DF_SQUARED.items())


def test_finite_dimension_and_moments_are_locked():
    assert sum(SPECTRUM_DF_SQUARED.values()) == 440
    assert _moment(1) == 1920
    assert _moment(2) == 16320


def test_raw_moment_ratios_are_exact():
    n = sum(SPECTRUM_DF_SQUARED.values())
    f2 = _moment(1)
    f4 = _moment(2)
    assert Fraction(f2, n) == Fraction(48, 11)
    assert Fraction(f4, f2) == Fraction(17, 2)
    assert Fraction(f4, n) == Fraction(408, 11)


def test_product_heat_coefficients_are_exact_strings():
    n = sum(SPECTRUM_DF_SQUARED.values())
    f2 = _moment(1)
    f4 = _moment(2)
    assert f"{n}*A0" == "440*A0"
    assert f"{n}*A2 - {f2}*A0" == "440*A2 - 1920*A0"
    assert f"{n}*A4 - {f2}*A2 + {f4 // 2}*A0" == "440*A4 - 1920*A2 + 8160*A0"


def test_ricci_flat_k3_specialization_keeps_product_c2_nonzero():
    n = sum(SPECTRUM_DF_SQUARED.values())
    f2 = _moment(1)
    f4 = _moment(2)
    a2 = 0
    assert f"{n}*A0" == "440*A0"
    assert f"{a2 * n - f2}*A0" == "-1920*A0"
    assert f"440*A4 + {f4 // 2}*A0" == "440*A4 + 8160*A0"
