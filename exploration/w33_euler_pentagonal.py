"""
EULER'S PENTAGONAL THEOREM AND THE PARTITION RECURRENCE
==========================================================

EULER'S PENTAGONAL NUMBER THEOREM.

    prod_{n>=1} (1 - q^n)  =  sum_{k in Z}  (-1)^k q^{k(3k-1)/2}
                            =  1 - q - q^2 + q^5 + q^7 - q^{12} - q^{15} + q^{22}
                               + q^{26} - q^{35} - q^{40} + ...

The exponents are the generalized pentagonal numbers  k(3k-1)/2
for  k = 0, 1, -1, 2, -2, 3, -3, ...  (giving 0, 1, 2, 5, 7, 12, 15, 22, 26, ...).

PARTITION RECURRENCE.

Multiplying  prod (1-q^n) * sum p(n) q^n  =  1  gives

    p(n)  =  sum_{k>=1}  (-1)^{k-1}  [ p(n - k(3k-1)/2)  +  p(n - k(3k+1)/2) ]
           =  p(n-1) + p(n-2) - p(n-5) - p(n-7) + p(n-12) + p(n-15) - ...

with  p(0) = 1  and  p(m) = 0  for  m < 0.  This is Euler's recurrence,
which computes p(n) in  O(n sqrt(n))  operations.

24-COLOR PARTITION RECURRENCE.

    1 / Delta(tau)  =  q^{-1} * sum p_24(n) q^n
    Delta(tau) * (1/Delta)  =  1

Setting  Delta  coefficients  d_n = tau(n)  and  p = p_24,  we get

    p_24(n)  =  -  sum_{m=1}^{n}  tau(m+1) * p_24(n-m)  /  tau(1)
             =  -  sum_{m=1}^{n}  tau(m+1) * p_24(n-m).

(Since tau(1) = 1, this divides exactly.)

CONNECTION TO  zeta(-1) = -1/12  AND  eta(tau).

    eta(tau)  =  q^{1/24}  prod (1 - q^n).

The  q^{1/24}  prefactor comes from the zeta-regularized sum

    1 + 2 + 3 + ... =  zeta(-1)  =  -1/12,

so the "Virasoro vacuum shift"  -c/24  for c=1 gives  -1/24.  The 24
in the exponent is the SAME 2k = 24 from the W(3, 3) valency.

BRIDGE TO W(3, 3).

    k = 12 = W(3, 3) valency
    2k = 24 = exponent in Delta = eta^24
    -1/24 = zeta(-1) / 2 = vacuum energy of c = 1 CFT
    Pentagonal exponents k(3k-1)/2 generate the expansion of prod(1-q^n).
"""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


# ======================================================================
#  Pentagonal exponents and Euler's theorem.
# ======================================================================
def generalized_pentagonal(k: int) -> int:
    """k(3k - 1)/2  for  k in Z."""
    return k * (3 * k - 1) // 2


def euler_pentagonal_series(order: int) -> list:
    """Coefficients of  prod (1 - q^n)  via Euler's theorem."""
    coeffs = [0] * (order + 1)
    coeffs[0] = 1
    k = 1
    while True:
        e1 = generalized_pentagonal(k)
        e2 = generalized_pentagonal(-k)
        if e1 > order and e2 > order:
            break
        sign = 1 if (k % 2 == 1) else -1
        # Wait: sign for k=1 is -1 (since (-1)^1 = -1).
        # General: (-1)^k
        sign = (-1) ** k
        if e1 <= order:
            coeffs[e1] += sign
        if e2 <= order:
            coeffs[e2] += sign
        k += 1
    return coeffs


def first_pentagonal_exponents(n_terms: int = 10) -> list:
    """Return the first n_terms pentagonal exponents  k(3k-1)/2  ordered, starting with k=0."""
    exps = {0}   # k=0 gives 0
    k = 1
    while len(exps) < n_terms * 2:
        exps.add(generalized_pentagonal(k))
        exps.add(generalized_pentagonal(-k))
        k += 1
    return sorted(exps)[:n_terms]


# ======================================================================
#  Partition number p(n) via Euler's recurrence.
# ======================================================================
def partition_numbers(n_max: int) -> list:
    """Compute p(0..n_max) via Euler's pentagonal recurrence."""
    p = [0] * (n_max + 1)
    p[0] = 1
    for n in range(1, n_max + 1):
        k = 1
        while True:
            e1 = generalized_pentagonal(k)
            e2 = generalized_pentagonal(-k)
            if e1 > n and e2 > n:
                break
            sign = (-1) ** (k - 1)
            if e1 <= n:
                p[n] += sign * p[n - e1]
            if e2 <= n:
                p[n] += sign * p[n - e2]
            k += 1
    return p


# First 15 partition numbers (A000041): 1, 1, 2, 3, 5, 7, 11, 15, 22, 30, 42,
# 56, 77, 101, 135.
OEIS_A000041 = [1, 1, 2, 3, 5, 7, 11, 15, 22, 30, 42, 56, 77, 101, 135, 176,
                231, 297, 385, 490, 627, 792, 1002, 1255, 1575, 1958]


def verify_partition_recurrence(n_max: int = 25) -> list:
    """Verify our computed p(n) matches OEIS A000041."""
    p = partition_numbers(n_max)
    results = []
    for n in range(min(n_max + 1, len(OEIS_A000041))):
        results.append({
            "n":        n,
            "computed": p[n],
            "oeis":     OEIS_A000041[n],
            "match":    p[n] == OEIS_A000041[n],
        })
    return results


# ======================================================================
#  Direct multiplication check:  prod(1-q^n) * sum p(n) q^n = 1.
# ======================================================================
def verify_product_inverse(order: int = 25) -> dict:
    """Multiply euler series times partition series; expect 1 + 0q + 0q^2 + ..."""
    euler = euler_pentagonal_series(order)
    p = partition_numbers(order)
    product = [0] * (order + 1)
    for i in range(order + 1):
        for j in range(order + 1 - i):
            product[i + j] += euler[i] * p[j]

    constant_is_1 = product[0] == 1
    higher_all_zero = all(c == 0 for c in product[1:])
    return {
        "constant":       product[0],
        "higher_nonzero": [(i, product[i]) for i in range(1, order + 1) if product[i] != 0],
        "constant_is_1":  constant_is_1,
        "higher_all_zero": higher_all_zero,
        "inverse_check":   constant_is_1 and higher_all_zero,
    }


# ======================================================================
#  zeta(-1) = -1/12  and the q^{1/24} prefactor of eta.
# ======================================================================
def zeta_neg_1_equals_minus_1_over_12() -> dict:
    """zeta(-1) = -1/12 via zeta(s) = -B_{s+1}/(s+1) at s=-1, so zeta(-1) = -B_2/2.
    B_2 = 1/6, so zeta(-1) = -1/12.  This gives the -c/24 = -1/24 shift in eta."""
    from w33_bernoulli_zeta import bernoulli
    B2 = bernoulli(2)
    zeta_neg_1 = -B2 / 2
    return {
        "B_2":               str(B2),
        "zeta(-1)":          str(zeta_neg_1),
        "zeta(-1) = -1/12":  zeta_neg_1 == Fraction(-1, 12),
        "vacuum_shift":      "-c/24 = -1/24 for c = 1",
        "eta_prefactor":     "q^{1/24} = q^{-zeta(-1)/2}",
        "zeta_neg_1_over_2": str(-zeta_neg_1 / 2),
        "is_1_over_24":      -zeta_neg_1 / 2 == Fraction(1, 24),
    }


# ======================================================================
#  Driver.
# ======================================================================
def derive_all_pentagonal(n_max: int = 25) -> dict:
    euler_coef = euler_pentagonal_series(n_max)
    part_check = verify_partition_recurrence(n_max)
    prod_check = verify_product_inverse(n_max)
    zeta_check = zeta_neg_1_equals_minus_1_over_12()
    pent_exps = first_pentagonal_exponents(12)

    return {
        "pentagonal_exponents":   pent_exps,
        "euler_product_coefs":    euler_coef,
        "partition_recurrence":   part_check,
        "recurrence_all_match":   all(r["match"] for r in part_check),
        "product_inverse_check":  prod_check,
        "zeta_neg_1_check":       zeta_check,
        "summary_chain": {
            "partition_recurrence_matches_OEIS":     all(r["match"] for r in part_check),
            "euler_times_partitions_equals_1":       prod_check["inverse_check"],
            "zeta(-1)_equals_minus_1_over_12":       zeta_check["zeta(-1) = -1/12"],
            "eta_prefactor_q_to_1_over_24":          zeta_check["is_1_over_24"],
            "pentagonal_exponents_begin_0_1_2_5_7":  pent_exps[:5] == [0, 1, 2, 5, 7],
        },
    }


def main() -> None:
    print("=" * 72)
    print("  EULER'S PENTAGONAL THEOREM AND PARTITIONS")
    print("=" * 72)
    print()

    pent_exps = first_pentagonal_exponents(10)
    print(f"  First pentagonal exponents:  {pent_exps}")
    print()

    euler = euler_pentagonal_series(30)
    print("  prod(1 - q^n) coefficients (first 30):")
    print(f"    {euler[:30]}")
    print()

    p = partition_numbers(25)
    print("  Partition numbers via Euler recurrence:")
    for n in range(26):
        print(f"    p({n:>2d}) = {p[n]:>5d}")
    print()

    prod = verify_product_inverse(25)
    print(f"  prod * p = 1:  constant={prod['constant']},  higher zero={prod['higher_all_zero']}")
    print()

    zeta_c = zeta_neg_1_equals_minus_1_over_12()
    print(f"  zeta(-1) = {zeta_c['zeta(-1)']}  (eta prefactor q^{{1/24}} from -zeta(-1)/2)")
    print()

    chain = derive_all_pentagonal(25)
    print("  SUMMARY CHAIN:")
    for key, val in chain["summary_chain"].items():
        print(f"    {key}: {val}")
    print()

    out = Path(__file__).resolve().parent.parent / "data" / "w33_euler_pentagonal.json"
    out.write_text(json.dumps(chain, indent=2, default=str))
    print(f"  wrote {out}")


if __name__ == "__main__":
    main()
