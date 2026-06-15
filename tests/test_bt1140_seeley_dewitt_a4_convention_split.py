"""BT1140 regression tests for convention-specific a4 lanes."""

from fractions import Fraction

K_NORM = 24
N = 440
F4_OVER_2 = 8160


def a4_from_coeffs(rank, omega_coeff, e2_coeff):
    return Fraction(K_NORM, 720) * (2 * rank + 30 * omega_coeff + 180 * e2_coeff)


def test_scalar_positive_laplacian_is_not_corpus_normalization():
    scalar_a4 = a4_from_coeffs(1, Fraction(0), Fraction(0))
    assert scalar_a4 == Fraction(1, 15)
    assert scalar_a4 != K_NORM


def test_corpus_product_and_scalar_product_are_distinct():
    corpus_product = N * K_NORM + F4_OVER_2
    scalar_product = N * Fraction(1, 15) + F4_OVER_2
    assert corpus_product == 18720
    assert scalar_product == Fraction(122408, 15)
    assert corpus_product != scalar_product


def test_generic_laplace_type_formula_templates():
    # Spin Dirac square on Ricci-flat 4D: rank=4 and E=R/4=0,
    # leaving only the spin connection-curvature trace coefficient.
    assert a4_from_coeffs(4, Fraction(0), Fraction(0)) == Fraction(4, 15)
    # All-form Hodge bundle has rank 16 before adding representation-specific
    # Weitzenbock curvature coefficients.
    assert a4_from_coeffs(16, Fraction(0), Fraction(0)) == Fraction(16, 15)
