"""Gauss sums, quadratic reciprocity, and the sign of g(chi_D).

For a Dirichlet character chi modulo N the Gauss sum is

    g(chi) = sum_{a = 0}^{N - 1} chi(a) e^{2 pi i a / N}.

For a primitive character (which chi_D is, at N = |D|),

    |g(chi)|^2 = N.                                              (*)

Gauss's theorem on the sign: for chi_D with D a fundamental
discriminant,

    g(chi_D) =    sqrt(D)     if D > 0,
                i sqrt(|D|)   if D < 0.                          (**)

So for every imaginary quadratic discriminant D < 0,
    g(chi_D) = i sqrt(|D|).

Consequences pinned:

(1)  The identity |g(chi_D)|^2 = |D| for every fundamental D in our test
     set.

(2)  Gauss's imaginary-sign formula (**) for all our imaginary-quadratic
     D, cross-checked numerically to high precision.

(3)  Real positive-discriminant case:  g(chi_5) = sqrt(5),
     g(chi_8) = sqrt(8), g(chi_{13}) = sqrt(13).

(4)  Quadratic reciprocity.  For odd primes p != q,
         (p/q)(q/p) = (-1)^{(p-1)/2 . (q-1)/2}.
     This is a direct corollary of (**): Gauss's original proof chains
     the two Legendre symbols through g(chi_{(-1)^{(p-1)/2} p}).

(5)  Supplementary laws.
         (-1/p) = (-1)^{(p - 1)/2},
         ( 2/p) = (-1)^{(p^2 - 1)/8}.

(6)  Connection to L(1, chi_D): g(chi) appears in the finite evaluation
         L(1, chi) = -g(chi)/N  *  sum_{a=1}^{N-1} chi(a) log(1 - e^{2 pi i a/N})
     (we merely pin the squared-modulus side here.)

This is Layer 62 -- the analytic underpinning of the Dirichlet class
number formula (Layer 60) and the quadratic-reciprocity backbone of
every CM / Heegner argument (Layers 52, 54).
"""

from __future__ import annotations

from typing import Any

import mpmath as mp

from w33_dirichlet_class_number import chi_D, kronecker


# ----------------------------------------------------------------------
# Gauss sum g(chi_D) = sum_{a=0}^{|D|-1} chi_D(a) exp(2 pi i a / |D|).
# ----------------------------------------------------------------------
def gauss_sum(D: int, dps: int = 50) -> mp.mpc:
    mp.mp.dps = dps
    N = abs(D)
    total = mp.mpc(0)
    twopi_i_over_N = mp.mpc(0, 2 * mp.pi) / N
    for a in range(N):
        c = chi_D(D, a)
        if c != 0:
            total += c * mp.exp(twopi_i_over_N * a)
    return total


# ----------------------------------------------------------------------
# Legendre symbol (a/p) for odd prime p.
# ----------------------------------------------------------------------
def legendre(a: int, p: int) -> int:
    """(a/p) via Euler's criterion a^{(p-1)/2} mod p; 0 if p | a."""
    if p < 2:
        raise ValueError("p must be an odd prime >= 3.")
    a = a % p
    if a == 0:
        return 0
    r = pow(a, (p - 1) // 2, p)
    return r if r <= 1 else r - p


# ----------------------------------------------------------------------
# Quadratic reciprocity verifier.
# ----------------------------------------------------------------------
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


def verify_quadratic_reciprocity(prime_limit: int = 100) -> dict[str, Any]:
    """For every pair of distinct odd primes p, q with p, q <= prime_limit,
    (p/q)(q/p) = (-1)^{(p-1)/2 (q-1)/2}."""
    primes = [p for p in _primes_up_to(prime_limit) if p > 2]
    rows: list[dict[str, Any]] = []
    all_match = True
    count = 0
    for i, p in enumerate(primes):
        for q in primes[i + 1:]:
            lhs = legendre(p, q) * legendre(q, p)
            rhs = (-1) ** (((p - 1) // 2) * ((q - 1) // 2))
            match = lhs == rhs
            count += 1
            if not match:
                rows.append({"p": p, "q": q, "lhs": lhs, "rhs": rhs})
            all_match = all_match and match
    return {"all_match": all_match,
            "check_count": count,
            "failures": rows}


def verify_supplementary_minus_one(prime_limit: int = 200) -> dict[str, Any]:
    """(-1 / p) = (-1)^{(p-1)/2} for every odd prime p."""
    primes = [p for p in _primes_up_to(prime_limit) if p > 2]
    rows: list[dict[str, Any]] = []
    all_match = True
    for p in primes:
        lhs = legendre(-1, p)
        rhs = (-1) ** ((p - 1) // 2)
        match = lhs == rhs
        rows.append({"p": p, "lhs": lhs, "rhs": rhs, "match": match})
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows}


def verify_supplementary_two(prime_limit: int = 200) -> dict[str, Any]:
    """(2 / p) = (-1)^{(p^2 - 1)/8} for every odd prime p."""
    primes = [p for p in _primes_up_to(prime_limit) if p > 2]
    rows: list[dict[str, Any]] = []
    all_match = True
    for p in primes:
        lhs = legendre(2, p)
        rhs = (-1) ** ((p * p - 1) // 8)
        match = lhs == rhs
        rows.append({"p": p, "lhs": lhs, "rhs": rhs, "match": match})
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows}


# ----------------------------------------------------------------------
# |g(chi_D)|^2 = |D|.
# ----------------------------------------------------------------------
def verify_gauss_squared_modulus(dps: int = 60) -> dict[str, Any]:
    """|g(chi_D)|^2 = |D| for every fundamental D in our list."""
    mp.mp.dps = dps
    D_list = [-3, -4, -7, -8, -11, -15, -19, -20, -23, -24,
              5, 8, 12, 13, 17, 21, 24, 28, 29, 33]
    rows: list[dict[str, Any]] = []
    all_match = True
    for D in D_list:
        # quick fundamental-discriminant filter
        if D % 4 not in (0, 1):
            continue
        g = gauss_sum(D, dps=dps)
        sq = abs(g) ** 2
        diff = abs(sq - abs(D))
        tol = mp.mpf("1e-30")
        match = diff < tol
        rows.append({
            "D": D,
            "abs_g_sq": float(sq),
            "abs_D": abs(D),
            "abs_diff": float(diff),
            "match": bool(match),
        })
        all_match = all_match and bool(match)
    return {"all_match": all_match, "rows": rows}


# ----------------------------------------------------------------------
# Gauss's sign formula g(chi_D) = i sqrt|D| for D<0 fundamental.
# ----------------------------------------------------------------------
def verify_gauss_sign_negative(dps: int = 60) -> dict[str, Any]:
    """g(chi_D) = i sqrt(|D|) for every fundamental D < 0."""
    mp.mp.dps = dps
    D_list = [-3, -4, -7, -8, -11, -15, -19, -20, -23, -24,
              -31, -35, -39, -40, -43, -47, -67, -163]
    rows: list[dict[str, Any]] = []
    all_match = True
    for D in D_list:
        g = gauss_sum(D, dps=dps)
        expected = mp.mpc(0, mp.sqrt(abs(D)))
        diff = abs(g - expected)
        tol = mp.mpf("1e-30")
        match = diff < tol
        rows.append({
            "D": D,
            "gauss_sum": str(g),
            "expected": str(expected),
            "abs_diff": float(diff),
            "match": bool(match),
        })
        all_match = all_match and bool(match)
    return {"all_match": all_match, "rows": rows}


def verify_gauss_sign_positive(dps: int = 60) -> dict[str, Any]:
    """g(chi_D) = sqrt(D) for D > 0 fundamental."""
    mp.mp.dps = dps
    D_list = [5, 8, 12, 13, 17, 21, 24, 28, 29, 33, 37, 40, 41, 44, 53]
    rows: list[dict[str, Any]] = []
    all_match = True
    for D in D_list:
        g = gauss_sum(D, dps=dps)
        expected = mp.mpc(mp.sqrt(D), 0)
        diff = abs(g - expected)
        tol = mp.mpf("1e-30")
        match = diff < tol
        rows.append({
            "D": D,
            "gauss_sum": str(g),
            "expected": str(expected),
            "abs_diff": float(diff),
            "match": bool(match),
        })
        all_match = all_match and bool(match)
    return {"all_match": all_match, "rows": rows}


# ----------------------------------------------------------------------
# Cross-check legendre() (Euler criterion) against kronecker() (Jacobi).
# ----------------------------------------------------------------------
def verify_legendre_equals_kronecker(prime_limit: int = 100) -> dict[str, Any]:
    """For odd prime p, (a/p)_Legendre == kronecker(a, p) for a = -5..20."""
    primes = [p for p in _primes_up_to(prime_limit) if p > 2]
    rows: list[dict[str, Any]] = []
    all_match = True
    for p in primes:
        for a in range(-5, 21):
            leg = legendre(a, p)
            kro = kronecker(a, p)
            if leg != kro:
                rows.append({"a": a, "p": p, "legendre": leg, "kronecker": kro})
                all_match = False
    return {"all_match": all_match, "failures": rows}


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------
def derive_all() -> dict[str, Any]:
    sq = verify_gauss_squared_modulus(dps=60)
    sign_neg = verify_gauss_sign_negative(dps=60)
    sign_pos = verify_gauss_sign_positive(dps=60)
    qr = verify_quadratic_reciprocity(prime_limit=100)
    sup_m1 = verify_supplementary_minus_one(prime_limit=200)
    sup_2 = verify_supplementary_two(prime_limit=200)
    leg_kro = verify_legendre_equals_kronecker(prime_limit=100)
    chain = {
        "abs_gauss_sum_squared_equals_abs_D":
            sq["all_match"],
        "gauss_sum_equals_i_sqrt_abs_D_for_fundamental_D_negative":
            sign_neg["all_match"],
        "gauss_sum_equals_sqrt_D_for_fundamental_D_positive":
            sign_pos["all_match"],
        "quadratic_reciprocity_for_all_odd_prime_pairs_up_to_100":
            qr["all_match"],
        "supplementary_minus_one_up_to_p_200":
            sup_m1["all_match"],
        "supplementary_two_up_to_p_200":
            sup_2["all_match"],
        "legendre_symbol_equals_kronecker_symbol_on_odd_primes":
            leg_kro["all_match"],
    }
    return {
        "gauss_squared": sq,
        "gauss_sign_negative": sign_neg,
        "gauss_sign_positive": sign_pos,
        "quadratic_reciprocity": qr,
        "supplementary_minus_one": sup_m1,
        "supplementary_two": sup_2,
        "legendre_kronecker": leg_kro,
        "summary_chain": chain,
    }


if __name__ == "__main__":
    s = derive_all()
    print("summary_chain:")
    for k, v in s["summary_chain"].items():
        print(f"  {k}: {v}")
    print("\nGauss sum g(chi_D) for D < 0 (first 5):")
    for row in s["gauss_sign_negative"]["rows"][:5]:
        print(f"  D={row['D']:>4}: g = {row['gauss_sum'][:30]},"
              f"  |g - i sqrt|D|| = {row['abs_diff']:.3e}")
    print(f"\nQR: {s['quadratic_reciprocity']['check_count']} pairs tested, "
          f"all match: {s['quadratic_reciprocity']['all_match']}")
