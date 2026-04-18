"""Jacobi's eight-squares theorem and theta_3^8 divisor formula.

Theorem (Jacobi, 1829).  For n >= 1,

    r_8(n) := #{(x_1,...,x_8) in Z^8 : x_1^2 + ... + x_8^2 = n}
           = 16  sum_{d | n}  (-1)^{n - d}  d^3.

As q-series:

    theta_3(q)^8 = 1 + 16 sum_{n>=1} sigma_3^*(n) q^n,
    sigma_3^*(n) = sum_{d | n} (-1)^{n - d} d^3.

Corollaries:
    r_8(1) = 16,
    r_8(2) = 16 (-1 + 8)   = 112    (C(8,2) * 4  lattice count),
    r_8(3) = 16 ( 1 + 27)  = 448,
    r_8(4) = 16 (-1 - 8 + 64) = 880.

Connection to the E_8 lattice (Layer 51).  The E_8 theta series has
leading coefficient 240 (number of norm-2 roots).  Jacobi's formula for
theta_3^8 gives lattice counts in the unit cubic lattice Z^8 — but E_8
is a different (even unimodular) lattice whose theta coincides with
E_4.  The contrast is instructive: 112 norm-2 vectors in Z^8 vs
240 in E_8, with the 128 extra half-integer coset vectors closing the
gap (Layer 51).

This is Layer 56 — the high-rank square-sum closure of the theta
ladder: r_2 (Jacobi two-squares, Layer 55), r_4 (four-squares),
r_8 (this Layer).
"""

from __future__ import annotations

from typing import Any

from w33_squares_theorems import (
    _mul_series,
    theta3_series,
    theta3_squared,
)


# ----------------------------------------------------------------------
# theta_3^8 and theta_3^6 as q-series.
# ----------------------------------------------------------------------
def theta3_sixth(N: int) -> list[int]:
    """theta_3(q)^6 = sum r_6(n) q^n."""
    t2 = theta3_squared(N)
    t4 = _mul_series(t2, t2, N)
    return _mul_series(t4, t2, N)


def theta3_eighth(N: int) -> list[int]:
    """theta_3(q)^8 = sum r_8(n) q^n."""
    t2 = theta3_squared(N)
    t4 = _mul_series(t2, t2, N)
    return _mul_series(t4, t4, N)


# ----------------------------------------------------------------------
# Direct enumeration via convolution.
# ----------------------------------------------------------------------
def r8_direct(n: int) -> int:
    """r_8(n) via convolution: r_8(n) = sum_k r_2(k) r_6(n-k)
       (well, via theta power)."""
    return theta3_eighth(n + 1)[n]


# ----------------------------------------------------------------------
# Jacobi divisor sigma_3^*(n).
# ----------------------------------------------------------------------
def sigma_3_star(n: int) -> int:
    """sigma_3^*(n) = sum_{d | n} (-1)^{n - d} d^3."""
    total = 0
    for d in range(1, n + 1):
        if n % d == 0:
            total += ((-1) ** (n - d)) * d ** 3
    return total


def r8_formula(n: int) -> int:
    """Jacobi eight-squares: r_8(n) = 16 sigma_3^*(n) for n >= 1."""
    if n == 0:
        return 1
    return 16 * sigma_3_star(n)


# ----------------------------------------------------------------------
# Direct lattice enumeration (brute force) for small n, as sanity.
# ----------------------------------------------------------------------
def r8_brute_force(n: int) -> int:
    """Exact count by iterating all 8-tuples of signed integers with
    squared norm n.  Only use for small n (say n <= 6) — cost blows
    up fast."""
    import math
    if n == 0:
        return 1
    count = 0
    lim = int(math.isqrt(n))
    rng = list(range(-lim, lim + 1))

    def rec(dim: int, remaining: int) -> int:
        if dim == 1:
            import math as _m
            s = int(_m.isqrt(remaining))
            if s * s == remaining:
                return 2 if s != 0 else 1
            return 0
        c = 0
        r_lim = int(_m_isqrt(remaining))
        for v in range(-r_lim, r_lim + 1):
            c += rec(dim - 1, remaining - v * v)
        return c
    import math as _m
    _m_isqrt = _m.isqrt
    return rec(8, n)


# ----------------------------------------------------------------------
# Verifiers.
# ----------------------------------------------------------------------
def verify_jacobi_eight_squares(N: int = 40) -> dict[str, Any]:
    """theta_3(q)^8 coefficient == 16 sigma_3^*(n) for n = 1..N-1."""
    th8 = theta3_eighth(N)
    rows: list[dict[str, Any]] = []
    all_match = True
    for n in range(1, N):
        theta_coef = th8[n]
        jacobi = r8_formula(n)
        match = theta_coef == jacobi
        rows.append({"n": n, "theta3_eighth": theta_coef,
                     "jacobi_formula": jacobi, "match": match})
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows}


def verify_r8_brute_force_small(up_to: int = 5) -> dict[str, Any]:
    """For n = 1..up_to, r_8 from theta_3^8 equals the brute-force
    enumeration of all sign/position patterns."""
    rows: list[dict[str, Any]] = []
    all_match = True
    th8 = theta3_eighth(up_to + 1)
    for n in range(1, up_to + 1):
        theta_coef = th8[n]
        brute = r8_brute_force(n)
        match = theta_coef == brute
        rows.append({"n": n, "theta3_eighth": theta_coef,
                     "brute_force": brute, "match": match})
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows}


def verify_specific_small_values() -> dict[str, Any]:
    """r_8(1) = 16, r_8(2) = 112, r_8(3) = 448, r_8(4) = 1136, r_8(5) = ?"""
    expected = {1: 16, 2: 112, 3: 448, 4: 1136, 5: 2016, 6: 3136, 7: 5504,
                 8: 9328}
    rows: list[dict[str, Any]] = []
    all_match = True
    th8 = theta3_eighth(max(expected) + 1)
    for n, e in expected.items():
        v = th8[n]
        match = v == e
        rows.append({"n": n, "computed": v, "expected": e, "match": match})
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows}


def verify_sigma_3_star_small() -> dict[str, Any]:
    """sigma_3^*(1..6) table."""
    rows: list[dict[str, Any]] = []
    all_match = True
    expected = {
        1: 1,                 # (-1)^0 * 1
        2: -1 + 8,            # (-1)^1 * 1 + (-1)^0 * 8 = -1+8 = 7
        3: 1 + 27,            # (-1)^2 + (-1)^0 * 27 = 1+27 = 28
        4: -1 - 8 + 64,       # (-1)^3 + (-1)^2*8 + (-1)^0*64 = -1-... wait
        # n=4: d=1 -> (-1)^{4-1}*1 = -1; d=2 -> (-1)^{4-2}*8 = 8; d=4 -> (-1)^0*64 = 64.
        # sum = -1 + 8 + 64 = 71.  Hmm expected 71, corrected below.
    }
    expected[4] = -1 + 8 + 64  # = 71
    expected[5] = 1 + 125     # (-1)^4*1 + (-1)^0*125 = 126
    expected[6] = -1 + 8 - 27 + 216  # d=1,2,3,6 signs: -1, +8, -27, +216 = 196
    for n, e in expected.items():
        v = sigma_3_star(n)
        match = v == e
        rows.append({"n": n, "computed": v, "expected": e, "match": match})
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows, "expected_table": expected}


def verify_r8_always_positive(N: int = 60) -> dict[str, Any]:
    th8 = theta3_eighth(N)
    zeros = [n for n in range(1, N) if th8[n] == 0]
    return {
        "no_zero_values": zeros == [],
        "zero_positions": zeros,
        "checked_up_to": N - 1,
    }


# ----------------------------------------------------------------------
# Contrast with E_8 lattice (Layer 51).
# ----------------------------------------------------------------------
def compare_r8_to_e8_theta() -> dict[str, Any]:
    """r_8(2) from Z^8 vs coefficient of q in E_4 (E_8 norm-2 count).
    Z^8 norm-2: 112.  E_8 norm-2: 240.  Gap: 128 (half-integer coset)."""
    th8 = theta3_eighth(3)
    z8_norm_2 = th8[2]   # r_8(2)
    e8_norm_2 = 240
    gap = e8_norm_2 - z8_norm_2
    return {
        "Z8_norm_2_count_r8_of_2": z8_norm_2,
        "E8_norm_2_count_E4_q1_coeff": e8_norm_2,
        "gap_half_integer_coset": gap,
        "matches_128_equals_2_to_7": gap == 128,
    }


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------
def derive_all() -> dict[str, Any]:
    jacobi8 = verify_jacobi_eight_squares(N=40)
    brute = verify_r8_brute_force_small(up_to=5)
    small = verify_specific_small_values()
    sigma = verify_sigma_3_star_small()
    positive = verify_r8_always_positive(N=60)
    e8_gap = compare_r8_to_e8_theta()
    chain = {
        "theta3_eighth_equals_16_sigma_3_star_jacobi":
            jacobi8["all_match"],
        "r_8_matches_brute_force_up_to_n_5":
            brute["all_match"],
        "r_8_specific_small_values_1_through_8":
            small["all_match"],
        "sigma_3_star_small_values_1_through_6":
            sigma["all_match"],
        "r_8_positive_for_all_n_up_to_59":
            positive["no_zero_values"],
        "Z8_norm_2_of_112_plus_128_halfinteger_equals_240_E8":
            e8_gap["matches_128_equals_2_to_7"],
    }
    return {
        "jacobi_eight_squares": jacobi8,
        "brute_force": brute,
        "specific_values": small,
        "sigma_3_star": sigma,
        "positivity": positive,
        "e8_gap": e8_gap,
        "summary_chain": chain,
    }


if __name__ == "__main__":
    s = derive_all()
    print("summary_chain:")
    for k, v in s["summary_chain"].items():
        print(f"  {k}: {v}")
    print("\ntheta_3(q)^8 first 15 coefficients = r_8(n):")
    print(" ", theta3_eighth(15))
    print("\nsigma_3^*(n) for n=1..6:")
    for n in range(1, 7):
        print(f"  sigma_3^*({n}) = {sigma_3_star(n)},  r_8({n}) = {r8_formula(n)}")
    print(f"\nE_8 vs Z^8 norm-2 gap: {s['e8_gap']}")
