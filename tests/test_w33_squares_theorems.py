"""Pin Jacobi's two-squares and four-squares theorems via theta_3.

Tests cover:
    (1) theta_3(q)^2 coefficients = r_2(n), via direct enumeration
        of lattice points on circles of radius sqrt(n);
    (2) r_2(n) = 4 (d_1(n) - d_3(n)) (Jacobi two-squares), up to q^49;
    (3) theta_3(q)^4 coefficients = r_4(n), via convolution;
    (4) r_4(n) = 8 sum_{d|n, 4∤d} d (Jacobi four-squares), up to q^59;
    (5) Lagrange four-squares: r_4(n) > 0 for n = 1..99;
    (6) Fermat two-squares prime dichotomy: r_2(p) = 8 if p == 1 mod 4,
        r_2(p) = 0 if p prime and p == 3 mod 4, r_2(2) = 4;
    (7) Specific small values.
"""

from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_squares_theorems import (  # noqa: E402
    d_mod_4,
    derive_all,
    r2_direct,
    r2_formula,
    r4_direct,
    r4_formula,
    sigma1_not_div_4,
    theta3_fourth,
    theta3_series,
    theta3_squared,
    verify_lagrange_four_square_nonzero,
    verify_r2_jacobi_two_squares,
    verify_r2_matches_theta_squared,
    verify_r2_p_for_small_primes,
    verify_r4_jacobi_four_squares,
    verify_r4_matches_theta_fourth,
)


# ----------------------------------------------------------------------
# theta_3 basic shape.
# ----------------------------------------------------------------------
def test_theta3_is_1_plus_2q_plus_2q4_plus_2q9():
    t = theta3_series(20)
    assert t[0] == 1
    assert t[1] == 2
    assert t[4] == 2
    assert t[9] == 2
    assert t[16] == 2


def test_theta3_is_zero_off_squares():
    t = theta3_series(20)
    for n in [2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 17, 18, 19]:
        assert t[n] == 0


# ----------------------------------------------------------------------
# r_2(n) from theta_3^2 and direct enumeration.
# ----------------------------------------------------------------------
def test_r2_of_1_is_4():
    """1 = (±1)^2 + 0 = 0 + (±1)^2: 4 reps."""
    assert r2_direct(1) == 4


def test_r2_of_2_is_4():
    """2 = (±1)^2 + (±1)^2: 4 reps."""
    assert r2_direct(2) == 4


def test_r2_of_5_is_8():
    """5 = (±1)^2 + (±2)^2 = (±2)^2 + (±1)^2: 8 reps."""
    assert r2_direct(5) == 8


def test_r2_of_3_is_0():
    """3 is not a sum of two squares."""
    assert r2_direct(3) == 0


def test_theta3_squared_matches_r2_up_to_50():
    r = verify_r2_matches_theta_squared(N=50)
    assert r["all_match"] is True


def test_theta3_squared_first_10_coefficients():
    t2 = theta3_squared(10)
    assert t2 == [1, 4, 4, 0, 4, 8, 0, 0, 4, 4]


# ----------------------------------------------------------------------
# Jacobi two-squares formula.
# ----------------------------------------------------------------------
def test_jacobi_two_squares_formula_up_to_50():
    r = verify_r2_jacobi_two_squares(N=50)
    assert r["all_match"] is True


def test_d1_and_d3_for_15():
    """15 = 1*15 = 3*5; divisors {1, 3, 5, 15}; d_1 = {1, 5} = 2;
       d_3 = {3, 15} = 2.  r_2(15) = 4 (2 - 2) = 0 — 15 is not a sum."""
    assert d_mod_4(15, 1) == 2
    assert d_mod_4(15, 3) == 2
    assert r2_formula(15) == 0


def test_d1_and_d3_for_25():
    """25 = 1*25 = 5*5; divisors {1, 5, 25}; d_1 = 3; d_3 = 0.
       r_2(25) = 12."""
    assert d_mod_4(25, 1) == 3
    assert d_mod_4(25, 3) == 0
    assert r2_formula(25) == 12
    assert r2_direct(25) == 12


# ----------------------------------------------------------------------
# Fermat two-squares prime dichotomy.
# ----------------------------------------------------------------------
def test_fermat_two_squares_dichotomy():
    r = verify_r2_p_for_small_primes()
    assert r["all_match"] is True


def test_r2_of_prime_97_is_8():
    """97 = 1 mod 4, so r_2(97) = 8."""
    assert r2_direct(97) == 8


def test_r2_of_prime_83_is_0():
    """83 = 3 mod 4, so r_2(83) = 0."""
    assert r2_direct(83) == 0


# ----------------------------------------------------------------------
# r_4(n) from theta_3^4.
# ----------------------------------------------------------------------
def test_r4_of_1_is_8():
    """1 = (±1)^2 + 0 + 0 + 0 in 4 positions, each with 2 signs: 8."""
    assert r4_direct(1) == 8


def test_r4_of_2_is_24():
    """2 = (±1)^2 + (±1)^2 + 0 + 0: C(4,2) = 6 positions, 2^2 signs: 24."""
    assert r4_direct(2) == 24


def test_r4_of_3_is_32():
    assert r4_direct(3) == 32


def test_theta3_fourth_first_10():
    t4 = theta3_fourth(10)
    assert t4 == [1, 8, 24, 32, 24, 48, 96, 64, 24, 104]


def test_theta3_fourth_matches_r4_up_to_40():
    r = verify_r4_matches_theta_fourth(N=40)
    assert r["all_match"] is True


# ----------------------------------------------------------------------
# Jacobi four-squares formula.
# ----------------------------------------------------------------------
def test_jacobi_four_squares_formula_up_to_60():
    r = verify_r4_jacobi_four_squares(N=60)
    assert r["all_match"] is True


def test_sigma_not_div_4_of_12():
    """12 divisors: 1, 2, 3, 4, 6, 12. 4 divides 4, 12. Keep 1, 2, 3, 6.
       sum = 12."""
    assert sigma1_not_div_4(12) == 12
    assert r4_formula(12) == 96


def test_r4_of_odd_n_is_8_sigma1_odd():
    """For odd n, r_4(n) = 8 sigma_1(n)."""
    for n in [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]:
        divisors_sum = sum(d for d in range(1, n + 1) if n % d == 0)
        assert r4_direct(n) == 8 * divisors_sum, f"n={n}"


# ----------------------------------------------------------------------
# Lagrange: four-squares theorem (no exceptional zero).
# ----------------------------------------------------------------------
def test_lagrange_four_squares_no_zeros_up_to_99():
    r = verify_lagrange_four_square_nonzero(N=100)
    assert r["no_zero_values"] is True
    assert r["zero_positions"] == []


def test_every_n_up_to_30_is_sum_of_four_squares():
    for n in range(1, 31):
        assert r4_direct(n) > 0, f"n={n} has no 4-square rep"


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------
def test_driver_all_pins_green():
    s = derive_all()
    for key, val in s["summary_chain"].items():
        assert val is True, f"{key} = {val}"


def test_driver_subresults():
    s = derive_all()
    for key in [
        "r2_vs_theta_squared",
        "r2_vs_jacobi_formula",
        "r4_vs_theta_fourth",
        "r4_vs_jacobi_formula",
        "lagrange_check",
        "fermat_check",
        "summary_chain",
    ]:
        assert key in s


def test_summary_chain_has_six_pins():
    s = derive_all()
    assert len(s["summary_chain"]) == 6
