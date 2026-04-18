"""Pin the Dirichlet class number formula for imaginary quadratic fields.

Tests cover:
    (1) Kronecker symbol chi_D(.) well-defined and totally multiplicative;
    (2) chi_D has period |D|;
    (3) Dirichlet finite formula h(D) = -w/(2|D|) * sum chi(a) a
        reproduces the class number from reduced forms over 30 D;
    (4) Partial L(1, chi_D) converges to the closed form 2 pi h / (w sqrt |D|);
    (5) Leibniz series L(1, chi_{-4}) = pi/4 (closed-form side only);
    (6) Specific character sums: S(-7) = -7, S(-23) = -69, S(-15) = -30;
    (7) Heegner class-number-1 D = -163 via forms matches.
"""

from __future__ import annotations

import sys
from pathlib import Path

import mpmath as mp


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_dirichlet_class_number import (  # noqa: E402
    FUND_D_LIST,
    L_1_chi_D,
    L_1_chi_D_formula,
    character_sum,
    chi_D,
    class_number_dirichlet,
    derive_all,
    is_fundamental_discriminant,
    kronecker,
    verify_chi_has_period_abs_D,
    verify_chi_is_totally_multiplicative,
    verify_finite_dirichlet_formula,
    verify_fundamental_flag_consistency,
    verify_L1_vs_closed_form,
    verify_leibniz_special_case,
    w_of,
)

from w33_hilbert_class_polynomials import class_number  # noqa: E402


# ----------------------------------------------------------------------
# Kronecker symbol sanity.
# ----------------------------------------------------------------------
def test_kronecker_at_1():
    for n in [1, 2, 3, 5, 7, 15]:
        assert kronecker(1, n) == 1


def test_kronecker_even_split():
    """(2/n) = 1 if n % 8 in {1, 7}, -1 if n % 8 in {3, 5}."""
    assert kronecker(2, 7) == 1
    assert kronecker(2, 3) == -1
    assert kronecker(2, 5) == -1


def test_kronecker_minus_one_at_odd_prime():
    """(-1/p) = 1 if p == 1 mod 4, -1 if p == 3 mod 4."""
    assert kronecker(-1, 5) == 1
    assert kronecker(-1, 7) == -1


# ----------------------------------------------------------------------
# Character chi_D.
# ----------------------------------------------------------------------
def test_chi_minus_3_values():
    """chi_{-3}(1) = 1, chi_{-3}(2) = -1."""
    assert chi_D(-3, 1) == 1
    assert chi_D(-3, 2) == -1


def test_chi_minus_4_values():
    """chi_{-4}(1) = 1, chi_{-4}(2) = 0, chi_{-4}(3) = -1."""
    assert chi_D(-4, 1) == 1
    assert chi_D(-4, 2) == 0
    assert chi_D(-4, 3) == -1


def test_chi_minus_7_values():
    """chi_{-7} is Legendre symbol (a/7) for gcd(a,7)=1."""
    expected = {1: 1, 2: 1, 3: -1, 4: 1, 5: -1, 6: -1}
    for a, v in expected.items():
        assert chi_D(-7, a) == v


def test_chi_totally_multiplicative():
    r = verify_chi_is_totally_multiplicative()
    assert r["all_match"] is True
    assert r["ok_count"] > 0


def test_chi_periodic():
    r = verify_chi_has_period_abs_D()
    assert r["all_match"] is True


# ----------------------------------------------------------------------
# Unit counts.
# ----------------------------------------------------------------------
def test_unit_counts():
    assert w_of(-3) == 6
    assert w_of(-4) == 4
    assert w_of(-7) == 2
    assert w_of(-163) == 2


# ----------------------------------------------------------------------
# Character sums and class numbers.
# ----------------------------------------------------------------------
def test_character_sum_minus_3():
    assert character_sum(-3) == -1


def test_character_sum_minus_7():
    assert character_sum(-7) == -7


def test_character_sum_minus_15():
    assert character_sum(-15) == -30


def test_character_sum_minus_23():
    assert character_sum(-23) == -69


def test_dirichlet_h_minus_163_is_1():
    """Famous Heegner class-number-1 discriminant."""
    assert class_number_dirichlet(-163) == 1


def test_dirichlet_h_agrees_with_forms_on_FUND_list():
    r = verify_finite_dirichlet_formula()
    assert r["all_match"] is True
    # Spot-check a handful.
    for row in r["rows"]:
        assert row["h_from_forms"] == row["h_from_dirichlet"]


# ----------------------------------------------------------------------
# L(1, chi_D) closed form.
# ----------------------------------------------------------------------
def test_L1_closed_form_leibniz():
    """L(1, chi_{-4}) = pi/4 exactly in closed form."""
    mp.mp.dps = 30
    val = L_1_chi_D_formula(-4)
    assert abs(val - mp.pi / 4) < mp.mpf("1e-25")


def test_L1_closed_form_minus_3():
    """L(1, chi_{-3}) = pi / (3 sqrt 3)."""
    mp.mp.dps = 30
    val = L_1_chi_D_formula(-3)
    expected = mp.pi / (3 * mp.sqrt(3))
    assert abs(val - expected) < mp.mpf("1e-25")


def test_L1_closed_form_minus_7():
    """L(1, chi_{-7}) = pi / sqrt 7 (w = 2, h = 1)."""
    mp.mp.dps = 30
    val = L_1_chi_D_formula(-7)
    expected = mp.pi / mp.sqrt(7)
    assert abs(val - expected) < mp.mpf("1e-25")


def test_L1_partial_converges_to_closed_form():
    r = verify_L1_vs_closed_form(dps=30, N=40000)
    assert r["all_match"] is True


def test_leibniz_pin():
    r = verify_leibniz_special_case()
    assert r["match"] is True


# ----------------------------------------------------------------------
# Fundamental discriminant predicate.
# ----------------------------------------------------------------------
def test_is_fundamental_minus_3():
    assert is_fundamental_discriminant(-3) is True


def test_is_fundamental_minus_4():
    assert is_fundamental_discriminant(-4) is True


def test_is_fundamental_minus_12_false():
    """-12 = 4 * -3, but -3 mod 4 = 1 (not 2 or 3), so -12 is NOT fundamental."""
    assert is_fundamental_discriminant(-12) is False


def test_is_fundamental_verifier():
    r = verify_fundamental_flag_consistency()
    assert r["all_match"] is True


# ----------------------------------------------------------------------
# Driver chain.
# ----------------------------------------------------------------------
def test_driver_all_pins_green():
    s = derive_all()
    for key, val in s["summary_chain"].items():
        assert val is True, f"{key} = {val}"


def test_driver_subresults():
    s = derive_all()
    for key in [
        "finite_formula",
        "L1_numerical",
        "leibniz",
        "chi_multiplicative",
        "chi_periodic",
        "fundamental_flag",
        "summary_chain",
    ]:
        assert key in s


def test_summary_chain_has_six_pins():
    s = derive_all()
    assert len(s["summary_chain"]) == 6


def test_fund_D_list_length():
    assert len(FUND_D_LIST) == 30
