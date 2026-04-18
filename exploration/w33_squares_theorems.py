"""Jacobi's two- and four-squares theorems via theta series.

Two-squares theorem (Jacobi).  For n >= 1,

    r_2(n) := #{(a, b) in Z^2 : a^2 + b^2 = n}
           = 4 (d_1(n) - d_3(n)),

where d_k(n) = #{divisors d of n with d ≡ k (mod 4)}.  As q-series:

    theta_3(q)^2 = sum_{n>=0} r_2(n) q^n,
    theta_3(q)   = sum_{m in Z} q^{m^2}.

Four-squares theorem (Jacobi).

    r_4(n) := #{(a, b, c, d) in Z^4 : a^2+b^2+c^2+d^2 = n}
           = 8  sum_{d | n,  4 does not divide d} d     (n >= 1).

Equivalently:
    r_4(n) =  8 sigma_1(n)               if  n  odd,
    r_4(n) = 24 sigma_1(m)                if  n = 2^k m, m odd, k >= 1.

Every positive integer is the sum of four squares (Lagrange, corollary
since r_4(n) > 0 for all n >= 1).

This is Layer 55 — the direct combinatorial face of theta_3 and its
powers.  Ties the modular-form side (Layer 50) to counting lattice
points on concentric spheres in Z^2 and Z^4.
"""

from __future__ import annotations

from typing import Any


# ----------------------------------------------------------------------
# theta_3 as a q-series.
# ----------------------------------------------------------------------
def theta3_series(N: int) -> list[int]:
    """theta_3(q) = sum_{m in Z} q^{m^2}, truncated to q^{N-1}.

    Equivalent to 1 + 2 q + 2 q^4 + 2 q^9 + 2 q^{16} + ...
    """
    out = [0] * N
    out[0] = 1
    m = 1
    while m * m < N:
        out[m * m] = 2
        m += 1
    return out


def _mul_series(a: list[int], b: list[int], N: int) -> list[int]:
    out = [0] * N
    for i in range(N):
        ai = a[i]
        if ai == 0:
            continue
        for j in range(N - i):
            out[i + j] += ai * b[j]
    return out


def theta3_squared(N: int) -> list[int]:
    """theta_3(q)^2 = sum r_2(n) q^n."""
    t = theta3_series(N)
    return _mul_series(t, t, N)


def theta3_fourth(N: int) -> list[int]:
    """theta_3(q)^4 = sum r_4(n) q^n."""
    t2 = theta3_squared(N)
    return _mul_series(t2, t2, N)


# ----------------------------------------------------------------------
# Direct enumeration: r_k(n) for small n by brute force.
# ----------------------------------------------------------------------
def r2_direct(n: int) -> int:
    """r_2(n) by iterating over all (a, b) with a^2 + b^2 = n."""
    import math
    if n == 0:
        return 1
    count = 0
    sqrt_n = int(math.isqrt(n))
    for a in range(-sqrt_n, sqrt_n + 1):
        rem = n - a * a
        if rem < 0:
            continue
        s = int(math.isqrt(rem))
        if s * s == rem:
            count += 2 if s != 0 else 1  # b = +s and b = -s
    return count


def r4_direct(n: int) -> int:
    """r_4(n) by enumerating (a, b, c, d) with a^2+b^2+c^2+d^2 = n.

    Efficient method: use r_2 convolution.
        r_4(n) = sum_{k=0}^{n} r_2(k) r_2(n - k).
    """
    if n == 0:
        return 1
    total = 0
    for k in range(n + 1):
        total += r2_direct(k) * r2_direct(n - k)
    return total


# ----------------------------------------------------------------------
# Divisor-based Jacobi formulas.
# ----------------------------------------------------------------------
def d_mod_4(n: int, k: int) -> int:
    """Number of positive divisors of n congruent to k mod 4."""
    count = 0
    for d in range(1, n + 1):
        if n % d == 0 and d % 4 == k:
            count += 1
    return count


def r2_formula(n: int) -> int:
    """Jacobi two-squares: r_2(n) = 4 (d_1(n) - d_3(n)) for n >= 1."""
    if n == 0:
        return 1
    return 4 * (d_mod_4(n, 1) - d_mod_4(n, 3))


def sigma1_not_div_4(n: int) -> int:
    """Sum of positive divisors d of n with 4 does not divide d."""
    total = 0
    for d in range(1, n + 1):
        if n % d == 0 and d % 4 != 0:
            total += d
    return total


def r4_formula(n: int) -> int:
    """Jacobi four-squares: r_4(n) = 8 sum_{d | n, 4∤d} d  (n >= 1)."""
    if n == 0:
        return 1
    return 8 * sigma1_not_div_4(n)


# ----------------------------------------------------------------------
# Verifiers.
# ----------------------------------------------------------------------
def verify_r2_matches_theta_squared(N: int = 50) -> dict[str, Any]:
    """[q^n] theta_3^2 = r_2(n) for n = 0..N-1."""
    th2 = theta3_squared(N)
    rows: list[dict[str, Any]] = []
    all_match = True
    for n in range(N):
        theta_coef = th2[n]
        direct = r2_direct(n)
        match = theta_coef == direct
        rows.append({"n": n, "theta3_sq": theta_coef, "r2_direct": direct,
                     "match": match})
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows}


def verify_r2_jacobi_two_squares(N: int = 50) -> dict[str, Any]:
    """r_2(n) = 4 (d_1(n) - d_3(n)) for n = 1..N-1."""
    th2 = theta3_squared(N)
    rows: list[dict[str, Any]] = []
    all_match = True
    for n in range(1, N):
        theta_coef = th2[n]
        jacobi = r2_formula(n)
        match = theta_coef == jacobi
        rows.append({"n": n, "theta3_sq": theta_coef, "jacobi_formula": jacobi,
                     "match": match})
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows}


def verify_r4_matches_theta_fourth(N: int = 40) -> dict[str, Any]:
    th4 = theta3_fourth(N)
    rows: list[dict[str, Any]] = []
    all_match = True
    for n in range(N):
        theta_coef = th4[n]
        direct = r4_direct(n)
        match = theta_coef == direct
        rows.append({"n": n, "theta3_fourth": theta_coef, "r4_direct": direct,
                     "match": match})
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows}


def verify_r4_jacobi_four_squares(N: int = 60) -> dict[str, Any]:
    """r_4(n) = 8 sum_{d|n, 4∤d} d for n = 1..N-1."""
    th4 = theta3_fourth(N)
    rows: list[dict[str, Any]] = []
    all_match = True
    for n in range(1, N):
        theta_coef = th4[n]
        jacobi = r4_formula(n)
        match = theta_coef == jacobi
        rows.append({"n": n, "theta3_fourth": theta_coef,
                     "jacobi_formula": jacobi, "match": match})
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows}


def verify_lagrange_four_square_nonzero(N: int = 100) -> dict[str, Any]:
    """r_4(n) > 0 for all n >= 1, N up to N-1."""
    th4 = theta3_fourth(N)
    zeros = [n for n in range(1, N) if th4[n] == 0]
    return {
        "no_zero_values": zeros == [],
        "zero_positions": zeros,
        "checked_up_to": N - 1,
    }


def verify_r2_p_for_small_primes() -> dict[str, Any]:
    """Fermat's theorem on sums of two squares:
       r_2(p) = 8 if p prime, p == 1 mod 4;
       r_2(p) = 0 if p prime, p == 3 mod 4;
       r_2(2) = 4."""
    rows: list[dict[str, Any]] = []
    all_match = True
    primes_1_mod4 = [5, 13, 17, 29, 37, 41, 53, 61, 73, 89, 97]
    primes_3_mod4 = [3, 7, 11, 19, 23, 31, 43, 47, 59, 67, 71, 79, 83]
    r2_at_2 = r2_direct(2)
    rows.append({"p": 2, "r2": r2_at_2, "expected": 4,
                 "match": r2_at_2 == 4})
    all_match = all_match and (r2_at_2 == 4)
    for p in primes_1_mod4:
        r = r2_direct(p)
        match = r == 8
        rows.append({"p": p, "class": "1 mod 4", "r2": r, "expected": 8,
                     "match": match})
        all_match = all_match and match
    for p in primes_3_mod4:
        r = r2_direct(p)
        match = r == 0
        rows.append({"p": p, "class": "3 mod 4", "r2": r, "expected": 0,
                     "match": match})
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows}


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------
def derive_all() -> dict[str, Any]:
    r2_theta = verify_r2_matches_theta_squared(N=50)
    r2_jacobi = verify_r2_jacobi_two_squares(N=50)
    r4_theta = verify_r4_matches_theta_fourth(N=40)
    r4_jacobi = verify_r4_jacobi_four_squares(N=60)
    lagrange = verify_lagrange_four_square_nonzero(N=100)
    fermat = verify_r2_p_for_small_primes()
    chain = {
        "theta3_squared_equals_r2_sum": r2_theta["all_match"],
        "r2_equals_4_times_d1_minus_d3_jacobi": r2_jacobi["all_match"],
        "theta3_fourth_equals_r4_sum": r4_theta["all_match"],
        "r4_equals_8_times_sigma_not_div_4_jacobi": r4_jacobi["all_match"],
        "lagrange_four_squares_no_exceptional_zeros_up_to_99":
            lagrange["no_zero_values"],
        "fermat_two_squares_prime_dichotomy":
            fermat["all_match"],
    }
    return {
        "r2_vs_theta_squared": r2_theta,
        "r2_vs_jacobi_formula": r2_jacobi,
        "r4_vs_theta_fourth": r4_theta,
        "r4_vs_jacobi_formula": r4_jacobi,
        "lagrange_check": lagrange,
        "fermat_check": fermat,
        "summary_chain": chain,
    }


if __name__ == "__main__":
    s = derive_all()
    print("summary_chain:")
    for k, v in s["summary_chain"].items():
        print(f"  {k}: {v}")
    print("\ntheta_3(q)^2 first 20 coefficients = r_2(n):")
    print(" ", theta3_squared(20))
    print("\ntheta_3(q)^4 first 20 coefficients = r_4(n):")
    print(" ", theta3_fourth(20))
    print("\nFermat two-squares dichotomy (p prime):")
    for row in s["fermat_check"]["rows"][:10]:
        print(f"  p={row['p']:>3}: r_2(p) = {row['r2']} "
              f"(expected {row['expected']})")
