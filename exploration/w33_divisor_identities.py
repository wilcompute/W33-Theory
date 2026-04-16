"""
DIVISOR-SUM IDENTITIES FORCED BY THE MODULAR FORM RING
=========================================================

Because  M_*(SL(2, Z)) = C[E_4, E_6]  and  dim M_k = 1  for
k in {4, 6, 8, 10, 14},  monomial identities like  E_8 = E_4^2
and  E_10 = E_4 * E_6  are FORCED.  Matching q-coefficients on both
sides converts these polynomial identities into arithmetic
identities among divisor sums  sigma_s(n) = sum d^s  (d | n).

E_8 = E_4^2  identity.

    E_4  =  1 + 240 sum sigma_3(n) q^n
    E_8  =  1 + 480 sum sigma_7(n) q^n

    E_4^2[q^n]  =  2 * 240 * sigma_3(n)  +  240^2 * sum_{m=1}^{n-1} sigma_3(m) sigma_3(n-m)

Matching with  E_8[q^n] = 480 sigma_7(n)  gives

    sigma_7(n)  =  sigma_3(n)  +  120 * sum_{m=1}^{n-1} sigma_3(m) sigma_3(n-m).

E_10 = E_4 * E_6  identity.

    E_6  =  1 - 504 sum sigma_5(n) q^n
    E_10 =  1 - 264 sum sigma_9(n) q^n

Gives the classical Ramanujan identity

    11 sigma_9(n)  =  21 sigma_5(n)  -  10 sigma_3(n)
                     +  5040 sum_{m=1}^{n-1} sigma_3(m) sigma_5(n-m).

DELTA IDENTITY.

    1728 Delta  =  E_4^3 - E_6^2,

so for each n >= 1,

    1728 tau(n)  =  [q^n] E_4^3  -  [q^n] E_6^2,

giving tau(n) as an explicit rational combination of convolutions of
sigma_3 and sigma_5.  In particular tau(n) is an integer because the
right-hand side is always divisible by 1728.

BRIDGE TO W(3, 3).

    The two generators E_4, E_6 with Eisenstein constants 240 = 20k
    and -504 = -42k (at k = 12) force ALL these divisor-sum relations.
    Every identity in this module is a consequence of  dim M_k = 1.
"""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

from w33_eisenstein import (
    delta_qseries,
    eisenstein_qseries,
    qmul,
    qpow,
    sigma_k,
)


# ======================================================================
#  sigma_7(n) = sigma_3(n) + 120 * convolution
# ======================================================================
def verify_sigma_7_identity(n_max: int = 15) -> list:
    """Ramanujan / Glaisher:  sigma_7(n) = sigma_3(n) + 120 * sum_{m=1}^{n-1} sigma_3(m) sigma_3(n-m)."""
    results = []
    for n in range(1, n_max + 1):
        lhs = sigma_k(n, 7)
        conv = sum(sigma_k(m, 3) * sigma_k(n - m, 3) for m in range(1, n))
        rhs = sigma_k(n, 3) + 120 * conv
        results.append({
            "n":        n,
            "sigma_7":  lhs,
            "rhs":      rhs,
            "conv":     conv,
            "match":    lhs == rhs,
        })
    return results


# ======================================================================
#  11 sigma_9(n) = 21 sigma_5(n) - 10 sigma_3(n) + 5040 * convolution
# ======================================================================
def verify_sigma_9_identity(n_max: int = 15) -> list:
    """11 sigma_9(n) = 21 sigma_5(n) - 10 sigma_3(n) + 5040 sum sigma_3(m) sigma_5(n-m)."""
    results = []
    for n in range(1, n_max + 1):
        lhs = 11 * sigma_k(n, 9)
        conv = sum(sigma_k(m, 3) * sigma_k(n - m, 5) for m in range(1, n))
        rhs = 21 * sigma_k(n, 5) - 10 * sigma_k(n, 3) + 5040 * conv
        results.append({
            "n":         n,
            "11*sigma_9": lhs,
            "rhs":       rhs,
            "conv":      conv,
            "match":     lhs == rhs,
        })
    return results


# ======================================================================
#  sigma_{11}(n) identity from E_12 decomposition.
#  M_12 has basis {E_4^3, E_6^2}, so E_12 and Delta both live here.
#
#  E_12(tau) = 1 + (65520/691) sum sigma_{11}(n) q^n.
#
#  Since M_12 = span(E_4^3, E_6^2), we can write
#      E_12 = alpha E_4^3 + beta E_6^2
#  with alpha + beta = 1  (constant terms all equal 1).
#  Matching q^1 coefficients determines alpha, beta.
# ======================================================================
def verify_E12_combination(order: int = 5) -> dict:
    """Decompose E_12 = alpha E_4^3 + beta E_6^2."""
    E4 = eisenstein_qseries(2, order)
    E6 = eisenstein_qseries(3, order)
    E12 = eisenstein_qseries(6, order)

    E4_cubed = qpow(E4, 3, order)
    E6_sq = qpow(E6, 2, order)

    # E_12 = alpha E_4^3 + beta E_6^2
    # At q^0: 1 = alpha + beta
    # At q^1: E_12[1] = alpha * E_4^3[1] + beta * E_6^2[1]
    #       = alpha * 720 + beta * (-1008)
    # Solve:  alpha + beta = 1
    #         720 alpha - 1008 beta = E_12[1]
    # => 720 alpha - 1008 (1 - alpha) = E_12[1]
    # => 1728 alpha = E_12[1] + 1008
    alpha = (E12[1] + Fraction(1008)) / Fraction(1728)
    beta = 1 - alpha

    # Verify at higher orders
    matches = []
    for n in range(order + 1):
        predicted = alpha * E4_cubed[n] + beta * E6_sq[n]
        actual = E12[n]
        matches.append({
            "n":         n,
            "predicted": str(predicted),
            "actual":    str(actual),
            "match":     predicted == actual,
        })

    return {
        "alpha":      str(alpha),
        "beta":       str(beta),
        "sum":        str(alpha + beta),
        "q_coefficient_checks": matches,
        "all_match":  all(m["match"] for m in matches),
    }


# ======================================================================
#  1728 tau(n) = [q^n] E_4^3 - [q^n] E_6^2.
# ======================================================================
def verify_tau_from_E4_E6(n_max: int = 10) -> list:
    """Show 1728 tau(n) = [q^n] E_4^3 - [q^n] E_6^2."""
    order = n_max + 1
    E4 = eisenstein_qseries(2, order)
    E6 = eisenstein_qseries(3, order)
    E4_cubed = qpow(E4, 3, order)
    E6_sq = qpow(E6, 2, order)
    D = delta_qseries(order)

    results = []
    for n in range(1, n_max + 1):
        lhs = 1728 * int(D[n])
        rhs = int(E4_cubed[n] - E6_sq[n])
        results.append({
            "n":           n,
            "tau(n)":      int(D[n]),
            "1728*tau(n)": lhs,
            "E4^3 - E6^2": rhs,
            "match":       lhs == rhs,
        })
    return results


# ======================================================================
#  Driver.
# ======================================================================
def derive_all_divisor_identities(n_max: int = 15) -> dict:
    sig7 = verify_sigma_7_identity(n_max)
    sig9 = verify_sigma_9_identity(n_max)
    e12 = verify_E12_combination(5)
    tau_id = verify_tau_from_E4_E6(10)

    return {
        "sigma_7_identity":      sig7,
        "sigma_7_all_match":     all(r["match"] for r in sig7),
        "sigma_9_identity":      sig9,
        "sigma_9_all_match":     all(r["match"] for r in sig9),
        "E12_combination":       e12,
        "E12_all_match":         e12["all_match"],
        "tau_from_E4_E6":        tau_id,
        "tau_all_match":         all(r["match"] for r in tau_id),
        "summary_chain": {
            "sigma_7_eq_sigma_3_plus_120_conv":    all(r["match"] for r in sig7),
            "11_sigma_9_eq_21_sigma_5_minus_10_sigma_3_plus_5040_conv":
                all(r["match"] for r in sig9),
            "E12_in_span_E4cubed_E6sq":            e12["all_match"],
            "1728_tau_eq_E4cubed_minus_E6sq":      all(r["match"] for r in tau_id),
        },
    }


def main() -> None:
    print("=" * 72)
    print("  DIVISOR-SUM IDENTITIES FROM THE MODULAR RING")
    print("=" * 72)
    print()

    print("  sigma_7(n) = sigma_3(n) + 120 * sum_{m<n} sigma_3(m) sigma_3(n-m):")
    for r in verify_sigma_7_identity(10):
        print(f"    n={r['n']:>2d}:  sigma_7={r['sigma_7']:>12d}  rhs={r['rhs']:>12d}  match={r['match']}")
    print()

    print("  11 sigma_9(n) = 21 sigma_5(n) - 10 sigma_3(n) + 5040 * conv:")
    for r in verify_sigma_9_identity(8):
        print(f"    n={r['n']:>2d}:  11*sigma_9={r['11*sigma_9']:>14d}  rhs={r['rhs']:>14d}  match={r['match']}")
    print()

    e12 = verify_E12_combination(5)
    print(f"  E_12 = {e12['alpha']} * E_4^3 + {e12['beta']} * E_6^2")
    print(f"    sum = {e12['sum']},  all_match = {e12['all_match']}")
    print()

    print("  1728 tau(n) = [q^n] (E_4^3 - E_6^2):")
    for r in verify_tau_from_E4_E6(8):
        print(f"    n={r['n']:>2d}:  tau={r['tau(n)']:>10d}  1728*tau={r['1728*tau(n)']:>14d}"
              f"  E4^3-E6^2={r['E4^3 - E6^2']:>14d}  match={r['match']}")
    print()

    chain = derive_all_divisor_identities(n_max=15)
    print("  SUMMARY CHAIN:")
    for key, val in chain["summary_chain"].items():
        print(f"    {key}: {val}")
    print()

    out = Path(__file__).resolve().parent.parent / "data" / "w33_divisor_identities.json"
    out.write_text(json.dumps(chain, indent=2, default=str))
    print(f"  wrote {out}")


if __name__ == "__main__":
    main()
