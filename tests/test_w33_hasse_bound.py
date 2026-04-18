"""Pin the Hasse bound for elliptic curves and Eichler-Shimura for E_11.

Tests cover:
    (1) Hasse bound |a_p| <= 2 sqrt(p) for y^2 = x^3 - x over a range
        of primes;
    (2) Hasse bound for E_11: y^2 + y = x^3 - x^2 over primes 2..61;
    (3) Eichler-Shimura: a_p(E_11) = a_p(f_11) where
        f_11 = q prod (1-q^n)^2 (1-q^{11n})^2
        is the unique newform in S_2(Gamma_0(11));
    (4) leading f_11 coefficients match the LMFDB table;
    (5) CM curve y^2 = x^3 - x supersingular iff p == 3 mod 4;
    (6) specific a_p values.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_hasse_bound import (  # noqa: E402
    a_p_E11,
    a_p_weierstrass,
    count_points_E11,
    count_points_weierstrass,
    derive_all,
    f_11_q_expansion,
    legendre,
    verify_curve_y2_x3_minus_x,
    verify_eichler_shimura_E11,
    verify_f_11_leading_coefficients,
    verify_hasse_bound_E11,
    verify_hasse_bound_weierstrass,
)


# ----------------------------------------------------------------------
# Legendre symbol sanity.
# ----------------------------------------------------------------------
def test_legendre_1_is_1():
    for p in [3, 5, 7, 11, 13]:
        assert legendre(1, p) == 1


def test_legendre_of_QR():
    """(4/7) = 1 since 4 = 2^2 mod 7."""
    assert legendre(4, 7) == 1


def test_legendre_of_nonQR():
    """(3/7) = -1."""
    assert legendre(3, 7) == -1


def test_legendre_of_zero():
    assert legendre(0, 5) == 0


# ----------------------------------------------------------------------
# Hasse bound for y^2 = x^3 - x (CM curve).
# ----------------------------------------------------------------------
def test_count_E_cm_at_p_5():
    """E : y^2 = x^3 - x over F_5; count by enumeration."""
    assert count_points_weierstrass(-1, 0, 5) == 5 + 1 - a_p_weierstrass(-1, 0, 5)


def test_hasse_bound_cm_curve_over_small_primes():
    r = verify_hasse_bound_weierstrass(-1, 0)
    assert r["all_match"] is True


def test_cm_curve_supersingular_at_p_equiv_3_mod_4():
    r = verify_curve_y2_x3_minus_x()
    assert r["all_match"] is True
    for row in r["rows"]:
        if row["p_mod_4"] == 3:
            assert row["a_p"] == 0, f"p={row['p']}"


# ----------------------------------------------------------------------
# E_11 point counting.
# ----------------------------------------------------------------------
def test_count_E11_at_p_2():
    """#E_11(F_2) = 2 + 1 - a_2 = 3 - (-2) = 5."""
    assert count_points_E11(2) == 5


def test_a_p_E11_at_p_2_is_minus_2():
    assert a_p_E11(2) == -2


def test_a_p_E11_at_p_3_is_minus_1():
    assert a_p_E11(3) == -1


def test_a_p_E11_at_p_5_is_1():
    assert a_p_E11(5) == 1


def test_a_p_E11_at_p_13_is_4():
    assert a_p_E11(13) == 4


def test_hasse_bound_E11_holds():
    r = verify_hasse_bound_E11()
    assert r["all_match"] is True


def test_hasse_bound_triangle_2_sqrt_p():
    """Check Hasse inequality strictly: |a_p| <= 2 sqrt(p)."""
    for p in [2, 3, 5, 7, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61]:
        ap = a_p_E11(p)
        assert abs(ap) <= 2 * math.sqrt(p), f"p={p}, a_p={ap}"


# ----------------------------------------------------------------------
# f_11 q-expansion as eta(q)^2 eta(q^11)^2.
# ----------------------------------------------------------------------
def test_f_11_starts_with_q():
    f = f_11_q_expansion(5)
    assert f[0] == 0
    assert f[1] == 1


def test_f_11_coefficient_at_q2_is_minus_2():
    f = f_11_q_expansion(5)
    assert f[2] == -2


def test_f_11_first_16_coefficients_match_newform_table():
    r = verify_f_11_leading_coefficients(N=30)
    assert r["all_match"] is True


def test_f_11_coefficient_at_q11_is_1():
    """a_{11}(f_11) = 1 (W_11 eigenvalue)."""
    f = f_11_q_expansion(15)
    assert f[11] == 1


# ----------------------------------------------------------------------
# Eichler-Shimura: a_p(E_11) = a_p(f_11).
# ----------------------------------------------------------------------
def test_eichler_shimura_pin():
    r = verify_eichler_shimura_E11()
    assert r["all_match"] is True


def test_eichler_shimura_matches_over_17_primes():
    r = verify_eichler_shimura_E11()
    rows = r["rows"]
    assert len(rows) >= 17
    for row in rows:
        assert row["a_p_E11"] == row["a_p_f11"], f"p={row['p']}"


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
        "hasse_generic",
        "hasse_E11",
        "eichler_shimura",
        "f_11_leading",
        "cm_curve",
        "summary_chain",
    ]:
        assert key in s


def test_summary_chain_has_five_pins():
    s = derive_all()
    assert len(s["summary_chain"]) == 5
