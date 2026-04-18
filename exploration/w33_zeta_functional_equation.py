"""Riemann zeta: Euler product, Basel / Euler values, functional equation.

The Riemann zeta function

    zeta(s) = sum_{n >= 1} n^{-s},  Re(s) > 1,

extends meromorphically to C with a single simple pole at s = 1 of
residue 1.  Four pillars pinned here:

(I)   Euler product.  For Re(s) > 1,
          zeta(s) = prod_p  (1 - p^{-s})^{-1}.

(II)  Euler's evaluation at even positive integers:
          zeta(2k) = (-1)^{k+1} B_{2k} (2 pi)^{2k} / (2 (2k)!),
      whence
          zeta(2) = pi^2 / 6      (Basel problem, 1735),
          zeta(4) = pi^4 / 90,
          zeta(6) = pi^6 / 945,
          zeta(8) = pi^8 / 9450,
          zeta(10) = pi^{10} / 93555.

(III) Values at negative integers:
          zeta(-2k) = 0                  for k >= 1  (trivial zeros),
          zeta(1 - 2k) = -B_{2k} / (2k)  for k >= 1.
      In particular
          zeta(0)  = -1/2,
          zeta(-1) = -1/12,
          zeta(-3) = 1/120,
          zeta(-5) = -1/252,
          zeta(-7) = 1/240,
          zeta(-9) = -1/132.

(IV)  Functional equation.  Define the completed zeta
          xi(s) = (1/2) s (s-1) pi^{-s/2} Gamma(s/2) zeta(s).
      Then xi is entire and satisfies
          xi(s) = xi(1 - s).
      Equivalently
          zeta(s) = 2^s pi^{s-1} sin(pi s / 2) Gamma(1 - s) zeta(1 - s).

(V)   First nontrivial zero.  The Riemann hypothesis asserts every non-
      trivial zero lies on Re(s) = 1/2.  Numerically the first is
          rho_1 = 1/2 + i * 14.1347251417... .

This is the ground zero of analytic number theory, the abelian twin of
Layer 58 (L-function of Delta) and Layer 60 (Dirichlet L-series).

Layer 61.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any

import mpmath as mp


# ----------------------------------------------------------------------
# Bernoulli numbers B_n as exact rationals (via recursion).
# ----------------------------------------------------------------------
def bernoulli(n: int) -> Fraction:
    """B_n (negative convention: B_1 = -1/2) via the standard recurrence
         B_n = -(1/(n+1)) sum_{k=0}^{n-1} C(n+1, k) B_k.
    B_0 = 1.  B_{2k+1} = 0 for k >= 1.
    """
    from math import comb
    B: list[Fraction] = []
    for m in range(n + 1):
        total = Fraction(0)
        for k in range(m):
            total += comb(m + 1, k) * B[k]
        if m == 0:
            B.append(Fraction(1))
        else:
            B.append(-total / (m + 1))
    return B[n]


# ----------------------------------------------------------------------
# Euler's formula for zeta(2k).
# ----------------------------------------------------------------------
def zeta_even_closed_form(k: int) -> mp.mpf:
    """zeta(2k) = (-1)^{k+1} B_{2k} (2 pi)^{2k} / (2 (2k)!)."""
    if k < 1:
        raise ValueError("k must be >= 1 for zeta(2k).")
    B = bernoulli(2 * k)
    fact = mp.factorial(2 * k)
    val = (-1) ** (k + 1) * mp.mpf(B.numerator) / mp.mpf(B.denominator)
    val *= mp.power(2 * mp.pi, 2 * k) / (2 * fact)
    return val


# ----------------------------------------------------------------------
# Closed form at negative odd integers:  zeta(1 - 2k) = -B_{2k}/(2k).
# ----------------------------------------------------------------------
def zeta_neg_odd_closed_form(k: int) -> Fraction:
    """zeta(1 - 2k) = -B_{2k} / (2k), exactly as a Fraction."""
    if k < 1:
        raise ValueError("k must be >= 1.")
    B = bernoulli(2 * k)
    return -B / Fraction(2 * k)


# ----------------------------------------------------------------------
# Partial Dirichlet sum and partial Euler product.
# ----------------------------------------------------------------------
def zeta_partial_dirichlet(s: complex, N: int = 200) -> mp.mpc:
    total = mp.mpc(0)
    s_mp = mp.mpc(s)
    for n in range(1, N + 1):
        total += mp.power(n, -s_mp)
    return total


def _primes_up_to(N: int) -> list[int]:
    if N < 2:
        return []
    sieve = [True] * (N + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(N ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, N + 1, i):
                sieve[j] = False
    return [i for i in range(N + 1) if sieve[i]]


def zeta_partial_euler(s: complex, P: int = 200) -> mp.mpc:
    s_mp = mp.mpc(s)
    result = mp.mpc(1)
    for p in _primes_up_to(P):
        result *= 1 / (1 - mp.power(p, -s_mp))
    return result


# ----------------------------------------------------------------------
# Completed zeta xi(s) = (1/2) s (s-1) pi^{-s/2} Gamma(s/2) zeta(s).
# ----------------------------------------------------------------------
def xi(s: complex) -> mp.mpc:
    s_mp = mp.mpc(s)
    return (mp.mpf("0.5") * s_mp * (s_mp - 1)
            * mp.power(mp.pi, -s_mp / 2)
            * mp.gamma(s_mp / 2)
            * mp.zeta(s_mp))


# ----------------------------------------------------------------------
# Verifiers.
# ----------------------------------------------------------------------
def verify_basel_and_euler_even_values(k_max: int = 6,
                                          dps: int = 50) -> dict[str, Any]:
    """zeta(2k) = (-1)^{k+1} B_{2k} (2 pi)^{2k} / (2 (2k)!) for k=1..k_max."""
    mp.mp.dps = dps
    rows: list[dict[str, Any]] = []
    all_match = True
    for k in range(1, k_max + 1):
        mpz = mp.zeta(2 * k)
        closed = zeta_even_closed_form(k)
        diff = abs(mpz - closed)
        tol = mp.mpf("1e-40")
        match = diff < tol
        rows.append({
            "k": k,
            "s": 2 * k,
            "zeta_2k": str(mpz),
            "closed_form": str(closed),
            "abs_diff": float(diff),
            "match": bool(match),
        })
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows}


def verify_trivial_zeros(k_max: int = 6, dps: int = 50) -> dict[str, Any]:
    """zeta(-2k) = 0 for k=1..k_max."""
    mp.mp.dps = dps
    rows = []
    all_match = True
    for k in range(1, k_max + 1):
        val = mp.zeta(-2 * k)
        match = abs(val) < mp.mpf("1e-40")
        rows.append({"s": -2 * k, "zeta": str(val), "match": bool(match)})
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows}


def verify_negative_odd_closed_form(k_max: int = 6,
                                      dps: int = 50) -> dict[str, Any]:
    """zeta(1 - 2k) = -B_{2k}/(2k) for k=1..k_max."""
    mp.mp.dps = dps
    rows = []
    all_match = True
    expected_rationals = {
        1: Fraction(-1, 12),   # zeta(-1)
        2: Fraction(1, 120),   # zeta(-3)
        3: Fraction(-1, 252),  # zeta(-5)
        4: Fraction(1, 240),   # zeta(-7)
        5: Fraction(-1, 132),  # zeta(-9)
        6: Fraction(691, 32760),  # zeta(-11) = 691/32760
    }
    for k in range(1, k_max + 1):
        closed = zeta_neg_odd_closed_form(k)
        expected = expected_rationals.get(k)
        mpz = mp.zeta(1 - 2 * k)
        closed_mp = mp.mpf(closed.numerator) / mp.mpf(closed.denominator)
        diff = abs(mpz - closed_mp)
        match_num = diff < mp.mpf("1e-40")
        match_exp = True if expected is None else closed == expected
        rows.append({
            "k": k,
            "s": 1 - 2 * k,
            "zeta": str(mpz),
            "closed_form_rational": str(closed),
            "matches_expected_rational": bool(match_exp),
            "numerical_match": bool(match_num),
        })
        all_match = all_match and bool(match_num) and bool(match_exp)
    return {"all_match": all_match, "rows": rows}


def verify_zeta_at_zero_is_minus_one_half(dps: int = 50) -> dict[str, Any]:
    """zeta(0) = -1/2."""
    mp.mp.dps = dps
    val = mp.zeta(0)
    expected = mp.mpf("-0.5")
    return {
        "zeta_0": str(val),
        "expected": "-1/2",
        "abs_diff": float(abs(val - expected)),
        "match": bool(abs(val - expected) < mp.mpf("1e-40")),
    }


def verify_euler_product_at_s(s: float = 3.0,
                                P: int = 500,
                                dps: int = 40) -> dict[str, Any]:
    """Partial Euler product matches zeta(s) at s = 3 within 1e-4."""
    mp.mp.dps = dps
    dir_sum = zeta_partial_dirichlet(s, N=3000)
    eul = zeta_partial_euler(s, P=P)
    diff = abs(eul - dir_sum)
    return {
        "s": s,
        "P": P,
        "zeta_dirichlet_partial": str(dir_sum),
        "zeta_mp": str(mp.zeta(s)),
        "euler_partial": str(eul),
        "abs_diff": float(diff),
        "match": bool(diff < mp.mpf("1e-4")),
    }


def verify_functional_equation(dps: int = 50) -> dict[str, Any]:
    """xi(s) = xi(1 - s) at a few off-line test points."""
    mp.mp.dps = dps
    test_points = [mp.mpc("2", "3"),
                    mp.mpc("0.7", "1.4"),
                    mp.mpc("-0.3", "5.1"),
                    mp.mpc("3.5", "0"),
                    mp.mpc("0.5", "14")]
    rows = []
    all_match = True
    for s in test_points:
        lhs = xi(s)
        rhs = xi(1 - s)
        diff = abs(lhs - rhs)
        scale = max(abs(lhs), mp.mpf(1))
        match = diff / scale < mp.mpf("1e-20")
        rows.append({
            "s": str(s),
            "xi_s": str(lhs),
            "xi_1_minus_s": str(rhs),
            "abs_diff": float(diff),
            "match": bool(match),
        })
        all_match = all_match and bool(match)
    return {"all_match": all_match, "rows": rows}


def verify_first_nontrivial_zero(dps: int = 30) -> dict[str, Any]:
    """The first nontrivial zero of zeta lies at s = 1/2 + i t_1,
    t_1 = 14.134725141734693...  We check |zeta(1/2 + i t_1)| < 1e-10
    and that Im is close to 14.1347251417."""
    mp.mp.dps = dps
    t1 = mp.mpf("14.1347251417346937904572519836")
    s = mp.mpc(mp.mpf("0.5"), t1)
    z = mp.zeta(s)
    on_line = abs(z) < mp.mpf("1e-10")
    return {
        "s": str(s),
        "zeta_at_s": str(z),
        "abs_zeta": float(abs(z)),
        "match": bool(on_line),
    }


def verify_bernoulli_values() -> dict[str, Any]:
    """Spot-check B_n for small n as exact Fractions."""
    expected = {
        0: Fraction(1, 1),
        1: Fraction(-1, 2),
        2: Fraction(1, 6),
        4: Fraction(-1, 30),
        6: Fraction(1, 42),
        8: Fraction(-1, 30),
        10: Fraction(5, 66),
        12: Fraction(-691, 2730),
        14: Fraction(7, 6),
    }
    rows = []
    all_match = True
    for n, v in expected.items():
        computed = bernoulli(n)
        match = computed == v
        rows.append({"n": n, "B_n_expected": str(v),
                     "B_n_computed": str(computed), "match": match})
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows}


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------
def derive_all() -> dict[str, Any]:
    bern = verify_bernoulli_values()
    even = verify_basel_and_euler_even_values(k_max=6, dps=50)
    triv = verify_trivial_zeros(k_max=6, dps=50)
    neg_odd = verify_negative_odd_closed_form(k_max=6, dps=50)
    z_at_0 = verify_zeta_at_zero_is_minus_one_half(dps=50)
    euler = verify_euler_product_at_s(s=3.0, P=500, dps=40)
    feq = verify_functional_equation(dps=50)
    zero_1 = verify_first_nontrivial_zero(dps=30)
    chain = {
        "bernoulli_values_match_B_0_through_B_14":
            bern["all_match"],
        "zeta_at_even_positive_integers_matches_Euler_formula":
            even["all_match"],
        "zeta_at_negative_even_integers_is_zero":
            triv["all_match"],
        "zeta_at_1_minus_2k_equals_minus_B_2k_over_2k":
            neg_odd["all_match"],
        "zeta_at_0_equals_minus_one_half":
            z_at_0["match"],
        "euler_product_matches_zeta_at_s_3_within_1e_4":
            euler["match"],
        "completed_xi_satisfies_xi_s_equals_xi_1_minus_s":
            feq["all_match"],
        "zeta_vanishes_at_first_nontrivial_zero_14p134725":
            zero_1["match"],
    }
    return {
        "bernoulli": bern,
        "euler_even_values": even,
        "trivial_zeros": triv,
        "negative_odd_values": neg_odd,
        "zeta_at_zero": z_at_0,
        "euler_product": euler,
        "functional_equation": feq,
        "first_nontrivial_zero": zero_1,
        "summary_chain": chain,
    }


if __name__ == "__main__":
    s = derive_all()
    print("summary_chain:")
    for k, v in s["summary_chain"].items():
        print(f"  {k}: {v}")
    print("\nEuler formula for zeta(2k), k = 1..6:")
    for row in s["euler_even_values"]["rows"]:
        print(f"  k={row['k']}: zeta({row['s']}) = {row['zeta_2k'][:20]},"
              f"  match={row['match']}")
    print("\nzeta at negative odd integers (closed form):")
    for row in s["negative_odd_values"]["rows"]:
        print(f"  zeta({row['s']:>3}) = {row['closed_form_rational']}")
    print(f"\nzeta(0) = {s['zeta_at_zero']['zeta_0'][:20]} "
          f"(expected -1/2, match={s['zeta_at_zero']['match']})")
    print(f"\nEuler product @ s=3: diff = {s['euler_product']['abs_diff']:.3e}")
    print(f"\nFirst zero: |zeta(1/2 + i 14.134725...)| = "
          f"{s['first_nontrivial_zero']['abs_zeta']:.3e}")
