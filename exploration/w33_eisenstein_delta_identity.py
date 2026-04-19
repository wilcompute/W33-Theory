"""Eisenstein series E_4, E_6 and the identity E_4^3 - E_6^2 = 1728 Delta.

Normalised Eisenstein series on SL_2(Z):

    E_{2k}(tau) = 1 - (4k / B_{2k}) sum_{n >= 1} sigma_{2k-1}(n) q^n,  q = e^{2 pi i tau}.

Leading coefficients:
    E_4 = 1 + 240 sum sigma_3(n) q^n,
    E_6 = 1 - 504 sum sigma_5(n) q^n,
    E_8 = 1 + 480 sum sigma_7(n) q^n,
    E_10 = 1 - 264 sum sigma_9(n) q^n,
    E_12 = 1 + (65520/691) sum sigma_11(n) q^n,   <-- 691 surfaces here,
    E_14 = 1 - 24 sum sigma_13(n) q^n.

Key identities on q-expansions:

    (I)  E_4^2 = E_8,          (dim M_8 = 1)
    (II) E_4 * E_6 = E_10,     (dim M_10 = 1)
    (III) E_4^3 - E_6^2 = 1728 Delta,   (the discriminant form)
    (IV) E_6^2 = E_12 - (... see relation in M_12 with 691).

(III) is the *structural* definition of Delta:  Delta(tau) = q prod (1 - q^n)^24.
The factor 1728 is the j-function normaliser:  j = E_4^3 / Delta = 1/q + 744 + ...

Layer 68 -- the modular-forms skeleton of Layers 63 and 67:
  * E_4^3 - E_6^2 = 1728 Delta pins the Ramanujan tau series to elementary
    Eisenstein data;
  * The 691 in E_12's leading coefficient is the *same* 691 of B_12,
    Kummer irregularity (Layer 67), and tau(n) mod 691 (Layer 63).

Seven summary_chain pins below.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any

from w33_zeta_functional_equation import bernoulli


# ----------------------------------------------------------------------
# Divisor sum helper.
# ----------------------------------------------------------------------
def sigma_k(n: int, k: int) -> int:
    if n < 1:
        return 0
    total = 0
    d = 1
    while d * d <= n:
        if n % d == 0:
            total += d ** k
            if d != n // d:
                total += (n // d) ** k
        d += 1
    return total


# ----------------------------------------------------------------------
# Eisenstein q-expansion coefficients (rational).
# ----------------------------------------------------------------------
def eisenstein_q_series(k: int, N: int) -> list[Fraction]:
    """Return list [a_0, a_1, ..., a_N] where
    E_{2k}(tau) = sum a_n q^n = 1 - (4k / B_{2k}) sum sigma_{2k-1}(n) q^n.
    Here input k corresponds to weight 2k (so E_4 -> k=2)."""
    if k < 1:
        raise ValueError("weight index k must be >= 1")
    B = bernoulli(2 * k)
    coeff_C = -Fraction(4 * k) / B
    out: list[Fraction] = [Fraction(1)]
    for n in range(1, N + 1):
        out.append(coeff_C * Fraction(sigma_k(n, 2 * k - 1)))
    return out


# ----------------------------------------------------------------------
# q-series product and power.
# ----------------------------------------------------------------------
def series_mul(a: list[Fraction], b: list[Fraction], N: int) -> list[Fraction]:
    """Truncated product up to q^N."""
    out = [Fraction(0)] * (N + 1)
    for i in range(min(len(a), N + 1)):
        if a[i] == 0:
            continue
        for j in range(min(len(b), N + 1 - i)):
            out[i + j] += a[i] * b[j]
    return out


def series_pow(a: list[Fraction], n: int, N: int) -> list[Fraction]:
    out = [Fraction(0)] * (N + 1)
    out[0] = Fraction(1)
    for _ in range(n):
        out = series_mul(out, a, N)
    return out


def series_sub(a: list[Fraction], b: list[Fraction], N: int) -> list[Fraction]:
    out = [Fraction(0)] * (N + 1)
    for i in range(N + 1):
        ai = a[i] if i < len(a) else Fraction(0)
        bi = b[i] if i < len(b) else Fraction(0)
        out[i] = ai - bi
    return out


# ----------------------------------------------------------------------
# Delta via eta^24 (product formula).
# ----------------------------------------------------------------------
def delta_q_series(N: int) -> list[Fraction]:
    """Delta(tau) = q prod_{n>=1} (1 - q^n)^24; return [a_0,...,a_N]
    where coefficients of q^k for 1 <= k <= N give the Ramanujan tau(k)."""
    # prod (1 - q^n)^24 up to q^{N-1}
    prod: list[Fraction] = [Fraction(0)] * (N + 1)
    prod[0] = Fraction(1)
    for n in range(1, N + 1):
        # multiply prod by (1 - q^n)^24 truncated.
        # First compute (1 - q^n)^24 as a list (sparse).
        factor = [Fraction(0)] * (N + 1)
        # (1 - x)^24 = sum_{j=0}^{24} C(24,j) (-1)^j x^j
        from math import comb
        for j in range(25):
            if j * n > N:
                break
            factor[j * n] = Fraction((-1) ** j * comb(24, j))
        prod = series_mul(prod, factor, N)
    # Now Delta = q * prod, shifted by one index.
    out = [Fraction(0)] * (N + 1)
    for i in range(N):
        out[i + 1] = prod[i]
    return out


# ----------------------------------------------------------------------
# Verifiers.
# ----------------------------------------------------------------------
def verify_E4_leading() -> dict[str, Any]:
    """E_4 = 1 + 240 sum sigma_3(n) q^n."""
    E4 = eisenstein_q_series(2, 5)
    expected = [
        Fraction(1),
        Fraction(240),                      # 240 * sigma_3(1) = 240 * 1
        Fraction(240 * 9),                  # sigma_3(2) = 9
        Fraction(240 * 28),                 # sigma_3(3) = 28
        Fraction(240 * 73),                 # sigma_3(4) = 73
        Fraction(240 * 126),                # sigma_3(5) = 126
    ]
    rows = []
    all_match = True
    for n, (got, want) in enumerate(zip(E4, expected)):
        match = got == want
        rows.append({"n": n, "got": str(got), "want": str(want), "match": match})
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows}


def verify_E6_leading() -> dict[str, Any]:
    """E_6 = 1 - 504 sum sigma_5(n) q^n."""
    E6 = eisenstein_q_series(3, 5)
    expected = [
        Fraction(1),
        Fraction(-504),                     # sigma_5(1) = 1
        Fraction(-504 * 33),                # sigma_5(2) = 33
        Fraction(-504 * 244),               # sigma_5(3) = 244
        Fraction(-504 * 1057),              # sigma_5(4) = 1057
        Fraction(-504 * 3126),              # sigma_5(5) = 3126
    ]
    rows = []
    all_match = True
    for n, (got, want) in enumerate(zip(E6, expected)):
        match = got == want
        rows.append({"n": n, "got": str(got), "want": str(want), "match": match})
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows}


def verify_E4_squared_equals_E8(N: int = 30) -> dict[str, Any]:
    """E_4^2 = E_8 since dim M_8(SL_2(Z)) = 1."""
    E4 = eisenstein_q_series(2, N)
    E8 = eisenstein_q_series(4, N)
    prod = series_mul(E4, E4, N)
    diff = series_sub(prod, E8, N)
    all_match = all(x == 0 for x in diff)
    return {
        "all_match": all_match,
        "N": N,
        "first_diff_nonzero":
            next((i for i, v in enumerate(diff) if v != 0), None),
    }


def verify_E4_E6_equals_E10(N: int = 30) -> dict[str, Any]:
    """E_4 E_6 = E_10 since dim M_10(SL_2(Z)) = 1."""
    E4 = eisenstein_q_series(2, N)
    E6 = eisenstein_q_series(3, N)
    E10 = eisenstein_q_series(5, N)
    prod = series_mul(E4, E6, N)
    diff = series_sub(prod, E10, N)
    all_match = all(x == 0 for x in diff)
    return {
        "all_match": all_match,
        "N": N,
        "first_diff_nonzero":
            next((i for i, v in enumerate(diff) if v != 0), None),
    }


def verify_E4_cubed_minus_E6_squared_is_1728_delta(N: int = 20) -> dict[str, Any]:
    """E_4^3 - E_6^2 = 1728 Delta, where Delta = q prod (1-q^n)^24."""
    E4 = eisenstein_q_series(2, N)
    E6 = eisenstein_q_series(3, N)
    E4_cubed = series_mul(E4, series_mul(E4, E4, N), N)
    E6_squared = series_mul(E6, E6, N)
    lhs = series_sub(E4_cubed, E6_squared, N)
    delta = delta_q_series(N)
    rhs = [Fraction(1728) * x for x in delta]
    diff = [lhs[i] - rhs[i] for i in range(N + 1)]
    all_match = all(x == 0 for x in diff)
    return {
        "all_match": all_match,
        "N": N,
        "first_diff_nonzero":
            next((i for i, v in enumerate(diff) if v != 0), None),
    }


def verify_delta_first_coefficients() -> dict[str, Any]:
    """Delta = q - 24 q^2 + 252 q^3 - 1472 q^4 + 4830 q^5 - 6048 q^6 + ..."""
    d = delta_q_series(10)
    expected = [
        Fraction(0),    # q^0
        Fraction(1),    # tau(1) = 1
        Fraction(-24),  # tau(2)
        Fraction(252),  # tau(3)
        Fraction(-1472),# tau(4)
        Fraction(4830), # tau(5)
        Fraction(-6048),# tau(6)
        Fraction(-16744), # tau(7)
        Fraction(84480),# tau(8)
        Fraction(-113643),# tau(9)
        Fraction(-115920),# tau(10)
    ]
    rows = []
    all_match = True
    for n, (got, want) in enumerate(zip(d, expected)):
        match = got == want
        rows.append({"n": n, "got": str(got), "want": str(want), "match": match})
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows}


def verify_E12_leading_coefficient_is_65520_over_691() -> dict[str, Any]:
    """E_12 = 1 + (65520/691) sum sigma_11(n) q^n -- the 691 appears here.
    Numerical check: coefficient of q is 65520/691, and sigma_11(1) = 1
    so the q-coefficient of E_12 is exactly 65520/691."""
    E12 = eisenstein_q_series(6, 2)
    expected_q1 = Fraction(65520, 691)
    q1_match = E12[1] == expected_q1
    # And coefficient of q^2: (65520/691) * sigma_11(2) = (65520/691) * 2049
    expected_q2 = Fraction(65520, 691) * Fraction(2049)
    q2_match = E12[2] == expected_q2
    return {
        "all_match": q1_match and q2_match,
        "E12_q1": str(E12[1]),
        "expected_q1": str(expected_q1),
        "q1_match": q1_match,
        "E12_q2": str(E12[2]),
        "expected_q2": str(expected_q2),
        "q2_match": q2_match,
    }


def verify_E4_coeff_formula_via_bernoulli() -> dict[str, Any]:
    """-4k / B_{2k} for k=2 gives 240:   -8 / B_4 = -8 / (-1/30) = 240."""
    B4 = bernoulli(4)
    c4 = -Fraction(8) / B4  # weight 4, k=2
    B6 = bernoulli(6)
    c6 = -Fraction(12) / B6
    B8 = bernoulli(8)
    c8 = -Fraction(16) / B8
    B10 = bernoulli(10)
    c10 = -Fraction(20) / B10
    B12 = bernoulli(12)
    c12 = -Fraction(24) / B12
    B14 = bernoulli(14)
    c14 = -Fraction(28) / B14
    rows = [
        {"weight": 4, "C": str(c4), "expected": "240",     "match": c4 == 240},
        {"weight": 6, "C": str(c6), "expected": "-504",    "match": c6 == -504},
        {"weight": 8, "C": str(c8), "expected": "480",     "match": c8 == 480},
        {"weight": 10, "C": str(c10), "expected": "-264",  "match": c10 == -264},
        {"weight": 12, "C": str(c12), "expected": "65520/691",
                        "match": c12 == Fraction(65520, 691)},
        {"weight": 14, "C": str(c14), "expected": "-24",   "match": c14 == -24},
    ]
    all_match = all(r["match"] for r in rows)
    return {"all_match": all_match, "rows": rows}


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------
def derive_all() -> dict[str, Any]:
    e4 = verify_E4_leading()
    e6 = verify_E6_leading()
    e4sq = verify_E4_squared_equals_E8(N=20)
    e4e6 = verify_E4_E6_equals_E10(N=20)
    cubic = verify_E4_cubed_minus_E6_squared_is_1728_delta(N=20)
    delta = verify_delta_first_coefficients()
    e12 = verify_E12_leading_coefficient_is_65520_over_691()
    coeffs = verify_E4_coeff_formula_via_bernoulli()
    chain = {
        "E4_leading_q_coefficient_is_240_sigma_3":
            e4["all_match"],
        "E6_leading_q_coefficient_is_negative_504_sigma_5":
            e6["all_match"],
        "E4_squared_equals_E8_on_q_series":
            e4sq["all_match"],
        "E4_times_E6_equals_E10_on_q_series":
            e4e6["all_match"],
        "E4_cubed_minus_E6_squared_equals_1728_Delta":
            cubic["all_match"],
        "Delta_first_ten_tau_coefficients":
            delta["all_match"],
        "E12_q_coefficient_is_65520_over_691":
            e12["all_match"],
        "bernoulli_based_coefficient_table_for_E_4_through_E_14":
            coeffs["all_match"],
    }
    return {
        "E4_leading": e4,
        "E6_leading": e6,
        "E4_squared_equals_E8": e4sq,
        "E4_E6_equals_E10": e4e6,
        "cubic_identity": cubic,
        "delta_coefficients": delta,
        "E12_coefficient": e12,
        "coefficient_table": coeffs,
        "summary_chain": chain,
    }


if __name__ == "__main__":
    s = derive_all()
    print("summary_chain:")
    for k, v in s["summary_chain"].items():
        print(f"  {k}: {v}")
    print("\nDelta first coefficients:")
    for row in s["delta_coefficients"]["rows"][:8]:
        print(f"  q^{row['n']}: tau = {row['got']} (expected {row['want']})")
    print(f"\nE_4^3 - E_6^2 = 1728 Delta verified to q^20: "
          f"{s['cubic_identity']['all_match']}")
    print(f"E_12 q-coefficient = 65520/691 ? "
          f"{s['E12_coefficient']['q1_match']}")
