"""Pin the Z(x) = (1-5x)^10 (1+x)^16 (1+7x)^6 master polynomial from
Part XXII, the q-cyclotomic master lock (c_EH, a_2, c_6, Weinberg),
and the atmospheric sum rule selecting q=3.

Tests cover:
    (1) Z(0) = 1, Z(-1) = 0, Z(1) = 2^54, deg Z = 32;
    (2) Z'(0) = 8 (dim O), Z''(0)/2 = -248 (-dim E_8), -Z''(0) = 496;
    (3) |Z(i)|^2 = 2^32 . 13^10 . 5^12;
    (4) Trace tower Tr(D^n) = 10.5^n + 16.(-1)^n + 6.(-7)^n at n=1,2,3;
    (5) q-cyclotomic lock: c_EH(3)=320, a_2(3)=2240, c_6(3)=12480;
    (6) Weinberg identity 9 c_EH / c_6 = q / Phi_3 (= 3/13 at q=3);
    (7) Atmospheric sum rule q(q-3)=0 uniquely selects q=3 in positives.
"""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_z_master_polynomial import (  # noqa: E402
    DIRAC_EIGS,
    Phi_3,
    Phi_6,
    Z_at,
    Z_double_prime_at_zero,
    Z_poly_sym,
    Z_prime_at_zero,
    a_2_curved,
    abs_Z_of_i_squared,
    atmospheric_sum_rule_gap,
    c_6_curved,
    c_EH,
    derive_all,
    trace_D_power,
    v_of_q,
    verify_atmospheric_sum_rule,
    verify_modulus_of_Z_of_i,
    verify_q_cyclotomic_master_lock,
    verify_special_values,
    verify_trace_tower,
    weinberg_polynomial_identity,
    weinberg_raw,
)


# ----------------------------------------------------------------------
# Z(x) special values.
# ----------------------------------------------------------------------
def test_Z_at_0_is_1():
    assert Z_at(0) == 1


def test_Z_at_minus_1_is_0():
    """Anomaly cancellation: factor (1 + x)^16 kills x = -1."""
    assert Z_at(-1) == 0


def test_Z_at_1_is_2_to_54():
    """2^54 = 2^{2 q^3} at q=3 (spinor degeneracy over GQ(3,3))."""
    assert Z_at(1) == 2**54


def test_Z_degree_is_32():
    """deg Z = 10 + 16 + 6 = 32 = dim Spin(10) Weyl spinor."""
    assert Z_poly_sym().degree() == 32


# ----------------------------------------------------------------------
# Leading Taylor coefficients.
# ----------------------------------------------------------------------
def test_Z_prime_at_0_is_8():
    """Z'(0) = 8 = dim O (octonion dimension)."""
    assert Z_prime_at_zero() == 8


def test_Z_double_prime_at_0_over_2_is_minus_248():
    """Z''(0)/2 = -248 = -dim E_8."""
    assert Z_double_prime_at_zero() // 2 == -248


def test_minus_Z_double_prime_is_496():
    """-Z''(0) = 496 = third perfect number = 2^(q+1) (2^(q+lambda) - 1)."""
    assert -Z_double_prime_at_zero() == 496


def test_496_factors_as_16_times_31():
    """496 = 16 * 31, with 16 = 2^(q+1) and 31 = 2^(q+lambda) - 1 = 2^5 - 1."""
    assert 16 * 31 == 496


# ----------------------------------------------------------------------
# |Z(i)|^2 factorisation.
# ----------------------------------------------------------------------
def test_abs_Z_of_i_squared_matches_cyclotomic_factorisation():
    """|Z(i)|^2 = 2^32 . 13^10 . 5^12."""
    assert abs_Z_of_i_squared() == 2**32 * 13**10 * 5**12


def test_abs_Z_of_i_squared_raw_product():
    """|1-5i|^20 |1+i|^32 |1+7i|^12 = 26^10 . 2^16 . 50^6."""
    assert abs_Z_of_i_squared() == 26**10 * 2**16 * 50**6


def test_modulus_verifier_matches():
    r = verify_modulus_of_Z_of_i()
    assert r["match"] is True


# ----------------------------------------------------------------------
# Trace tower.
# ----------------------------------------------------------------------
def test_dirac_eigenvalues_are_5_minus_1_minus_7():
    eigs = [eig for eig, _ in DIRAC_EIGS]
    assert eigs == [5, -1, -7]


def test_dirac_multiplicities_are_10_16_6():
    mults = [m for _, m in DIRAC_EIGS]
    assert mults == [10, 16, 6]


def test_trace_D_1_is_minus_8():
    """Tr(D) = 10.5 + 16.(-1) + 6.(-7) = 50 - 16 - 42 = -8."""
    assert trace_D_power(1) == -8


def test_trace_D_2_is_560():
    """Tr(D^2) = 10.25 + 16.1 + 6.49 = 250 + 16 + 294 = 560."""
    assert trace_D_power(2) == 560


def test_trace_D_3_is_minus_824():
    """Tr(D^3) = 10.125 - 16 - 6.343 = 1250 - 16 - 2058 = -824."""
    assert trace_D_power(3) == -824


def test_trace_tower_verifier_pins_hold():
    r = verify_trace_tower()
    assert r["all_pins_hold"] is True


# ----------------------------------------------------------------------
# q-cyclotomic master lock at q=3.
# ----------------------------------------------------------------------
def test_v_of_3_is_40():
    """v(3) = (3+1)(9+1) = 40 = |W(3,3) vertices|."""
    assert v_of_q(3) == 40


def test_Phi_3_at_3_is_13():
    assert Phi_3(3) == 13


def test_Phi_6_at_3_is_7():
    assert Phi_6(3) == 7


def test_c_EH_at_3_is_320():
    """c_EH(3) = v(3) . (q^2 - 1) = 40 . 8 = 320."""
    assert c_EH(3) == 320


def test_a_2_at_3_is_2240():
    """a_2(3) = Phi_6(3) . c_EH(3) = 7 . 320 = 2240."""
    assert a_2_curved(3) == 2240


def test_c_6_at_3_is_12480():
    """c_6(3) = 3 . Phi_3(3) . c_EH(3) = 3 . 13 . 320 = 12480."""
    assert c_6_curved(3) == 12480


def test_weinberg_polynomial_identity_at_3_is_3_over_13():
    """9 c_EH(3) / c_6(3) = 9.320 / 12480 = 2880 / 12480 = 3/13."""
    w = weinberg_polynomial_identity(3)
    assert w == Fraction(3, 13)


def test_weinberg_raw_at_3_is_3_over_13():
    """q / Phi_3(q) at q=3 is 3/13, matching sin^2 theta_W."""
    assert weinberg_raw(3) == Fraction(3, 13)


def test_weinberg_identity_equals_raw_only_at_q_3():
    """9 c_EH / c_6 = 9/(q Phi_3) and q/Phi_3 coincide iff q^2 = 9, i.e., q=3.
    This is the sharpest statement of why q=3 is forced by the Weinberg lock."""
    assert weinberg_polynomial_identity(3) == weinberg_raw(3)
    assert weinberg_polynomial_identity(5) != weinberg_raw(5)
    assert weinberg_polynomial_identity(7) != weinberg_raw(7)


def test_master_lock_verifier_at_3():
    r = verify_q_cyclotomic_master_lock(3)
    assert r["c_EH(3) == 320"] is True
    assert r["a_2(3) == 2240"] is True
    assert r["c_6(3) == 12480"] is True
    assert r["weinberg_lock_holds"] is True


# ----------------------------------------------------------------------
# Atmospheric sum rule.
# ----------------------------------------------------------------------
def test_atmospheric_gap_vanishes_at_q_3():
    assert atmospheric_sum_rule_gap(3) == 0


def test_atmospheric_gap_nonzero_at_q_5():
    assert atmospheric_sum_rule_gap(5) != 0


def test_atmospheric_gap_nonzero_at_q_2():
    assert atmospheric_sum_rule_gap(2) != 0


def test_atmospheric_sum_rule_selects_q_3_uniquely():
    r = verify_atmospheric_sum_rule([1, 2, 3, 4, 5, 6, 7])
    assert r["q_for_which_it_holds"] == [3]


# ----------------------------------------------------------------------
# Driver chain.
# ----------------------------------------------------------------------
def test_driver_all_five_pins():
    s = derive_all()
    for key, val in s["summary_chain"].items():
        assert val is True, f"{key} = {val}"


def test_driver_includes_all_subresults():
    s = derive_all()
    for key in [
        "Z_special_values",
        "Z_modulus_at_i",
        "trace_tower",
        "q_cyclotomic_master_lock",
        "atmospheric_sum_rule",
        "summary_chain",
    ]:
        assert key in s


# ----------------------------------------------------------------------
# Sanity: special values driver matches individual pins.
# ----------------------------------------------------------------------
def test_special_values_verifier_reports_correctly():
    r = verify_special_values()
    assert r["Z(0)"] == 1
    assert r["Z(-1)"] == 0
    assert r["Z(1) == 2^54"] is True
    assert r["Z'(0) == 8 (dim O)"] is True
    assert r["Z''(0)/2 == -248 (-dim E_8)"] is True
    assert r["-Z''(0) == 496 (third perfect number)"] is True
    assert r["degree == 32"] is True
