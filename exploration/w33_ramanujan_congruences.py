"""
RAMANUJAN CONGRUENCES AND THE 691 THAT LINKS Delta TO E_12
===========================================================

The prime 691 already appeared in this project as the denominator of the
E_12 Eisenstein constant  65520 / 691  (see w33_eisenstein.py).  This is
not a coincidence -- 691 divides the numerator of B_12 = -691/2730 and
forces a modular congruence between the cusp form Delta and an Eisenstein
series of the same weight.

WHY 691 APPEARS IN E_12.

    E_12(tau)  =  1  +  (65520 / 691)  sum  sigma_{11}(n)  q^n.

The denominator of the Eisenstein constant  -4 * 6 / B_12 = -24 / (-691/2730)
=  24 * 2730 / 691  =  65520 / 691.

WHY 691 CONGRUES Delta TO E_12.

The space of weight-12 modular forms for SL(2, Z) has dimension 2 with basis
E_12, Delta.  Normalize so that both have integer coefficients mod a small
denominator.  The form  691 E_12 - 65520 sigma_11  is an INTEGER cusp form
up to an overall  691 / 65520  scaling, and cusp forms of weight 12 have
dimension 1 (spanned by Delta).  Matching constant terms produces the
Ramanujan congruence

    tau(n)  ==  sigma_{11}(n)   (mod 691),           for all n >= 1.

CONSEQUENCE FOR PRIMES.

For prime p, sigma_{11}(p) = 1 + p^{11}, so

    tau(p)  ==  1  +  p^{11}   (mod 691).

HOW THE MODULAR FORM TOWER LOCKS THIS IN.

    65520 * Delta   ==   65520 * E_12 * a_1  -  65520 * E_12 * a_0     (mod 691)
    ->  Delta coefficients equal sigma_11 coefficients  (mod 691).

This is a pure consequence of the ring  Z[E_4, E_6] / (dim 12 relation).
BRIDGE TO W(3, 3).

    24   =  2 k                (k = 12 = SRG valency)
    12   =  k = valency of W(3, 3)
    2730 =  2 * 3 * 5 * 7 * 13   (5 of the 6 smallest primes, including  k + 1 = 13)
    691  =  prime,  dim(M_12 / S_12) = 1  forces the Delta/E_12 congruence.
"""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

from w33_bernoulli_zeta import bernoulli
from w33_eisenstein import (
    delta_qseries,
    eisenstein_constant,
    eisenstein_qseries,
    sigma_k,
)


# ======================================================================
#  The magic number 691.
# ======================================================================
def bernoulli_B12() -> Fraction:
    """B_12 = -691 / 2730."""
    return bernoulli(12)


def E12_eisenstein_constant() -> Fraction:
    """-4 * 6 / B_12 = 65520 / 691."""
    return eisenstein_constant(6)


def factor_B12_numerator() -> dict:
    B12 = bernoulli_B12()
    # B_12 = -691 / 2730.
    assert B12 == Fraction(-691, 2730)
    return {
        "B_12":               str(B12),
        "numerator_abs":      691,
        "denominator":        2730,
        "2730_factorization": "2 * 3 * 5 * 7 * 13",
        "691_is_prime":       True,
    }


# ======================================================================
#  Ramanujan 691-congruence:  tau(n) == sigma_11(n)  (mod 691).
# ======================================================================
def verify_691_congruence_at_n(n: int) -> dict:
    """Return whether tau(n) equals sigma_{11}(n) mod 691."""
    D = delta_qseries(n)
    tau_n = int(D[n])
    s11_n = sigma_k(n, 11)
    return {
        "n":           n,
        "tau":         tau_n,
        "sigma_11":    s11_n,
        "tau_mod_691":  tau_n % 691,
        "sigma_mod_691": s11_n % 691,
        "match":       (tau_n - s11_n) % 691 == 0,
        "quotient":    (s11_n - tau_n) // 691,
    }


def verify_691_congruence_range(n_max: int = 20) -> list:
    return [verify_691_congruence_at_n(n) for n in range(1, n_max + 1)]


# ======================================================================
#  Prime case:  tau(p) == 1 + p^11  (mod 691).
# ======================================================================
def first_primes_up_to(limit: int) -> list:
    """Return list of primes <= limit (simple sieve)."""
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, limit + 1, i):
                sieve[j] = False
    return [i for i in range(2, limit + 1) if sieve[i]]


def verify_tau_prime_congruence(p: int) -> dict:
    """For prime p, check tau(p) == 1 + p^11 (mod 691)."""
    D = delta_qseries(p)
    tau_p = int(D[p])
    predicted = 1 + p ** 11
    return {
        "p":              p,
        "tau(p)":         tau_p,
        "1 + p^11":       predicted,
        "tau mod 691":    tau_p % 691,
        "pred mod 691":   predicted % 691,
        "match":          (tau_p - predicted) % 691 == 0,
    }


# ======================================================================
#  Reconstructing Delta from E_12 modulo 691.
# ======================================================================
def e12_mod_691_coefficients(order: int) -> list:
    """Return [E_12[n] mod 691 after clearing the 65520/691 denominator].

    In Z / 691 Z, we have:

        E_12(tau) * 691  ==  691  +  65520 * sum sigma_11(n) q^n   (mod 691)
                         ==   0    +    0     *  ...                (mod 691)
                         ==   0.

    But the TRACE-FREE part coincides with Delta up to an integer multiple,
    giving tau(n) == sigma_11(n) (mod 691).
    """
    E12 = eisenstein_qseries(6, order)
    # E12[n] = (65520/691) * sigma_11(n)  for n >= 1.
    # Clear denominator: 691 * E12[n] = 65520 * sigma_11(n) for n >= 1.
    out = []
    for n in range(order + 1):
        val = E12[n]
        # val = c / 691 with c integer for n >= 1.
        if n == 0:
            out.append(1)
        else:
            # 691 * val = 65520 * sigma_11(n).
            c = 691 * val
            assert c.denominator == 1
            out.append(int(c))
    return out


def delta_mod_691_equals_negative_sigma_times_65520_over_691() -> dict:
    """691 * Delta  congruent to  -65520 * (E_12 - 1) / 65520 * 691  ...

    Equivalently:  tau(n) - sigma_11(n)  is divisible by 691 for all n.
    This is what the structural theorem asserts.
    """
    results = []
    for n in range(1, 21):
        r = verify_691_congruence_at_n(n)
        results.append(r)
    return {
        "all_match":          all(r["match"] for r in results),
        "first_20_congrues":  results,
    }


# ======================================================================
#  Driver.
# ======================================================================
def derive_all_ramanujan(n_max: int = 30) -> dict:
    congr = verify_691_congruence_range(n_max)
    primes = first_primes_up_to(50)
    prime_checks = [verify_tau_prime_congruence(p) for p in primes]

    return {
        "the_prime_691":          factor_B12_numerator(),
        "E_12_constant":          str(E12_eisenstein_constant()),
        "ramanujan_691_congruence": {
            "all_match":          all(c["match"] for c in congr),
            "first_n":            congr,
        },
        "prime_congruence_tau_p_equiv_1_plus_p11": {
            "all_match":          all(c["match"] for c in prime_checks),
            "primes_checked":     [c["p"] for c in prime_checks],
            "details":            prime_checks,
        },
    }


def main() -> None:
    print("=" * 72)
    print("  RAMANUJAN CONGRUENCES:  tau(n) == sigma_11(n)  (mod 691)")
    print("=" * 72)
    print()

    print("  B_12 = ", bernoulli_B12())
    print("  E_12 Eisenstein constant =", E12_eisenstein_constant())
    print()

    print("  RAMANUJAN 691-CONGRUENCE  tau(n) == sigma_11(n)  (mod 691):")
    print(f"    {'n':>3s}  {'tau(n)':>13s}  {'sigma_11(n)':>20s}  {'diff':>10s}  match")
    for n in range(1, 11):
        r = verify_691_congruence_at_n(n)
        diff = r['sigma_11'] - r['tau']
        q = r['quotient']
        print(f"    {r['n']:>3d}  {r['tau']:>13d}  {r['sigma_11']:>20d}  "
              f"{diff:>10d}  match={r['match']}  (= 691 * {q})")
    print()

    print("  PRIME CASE  tau(p) == 1 + p^11  (mod 691):")
    for p in first_primes_up_to(30):
        r = verify_tau_prime_congruence(p)
        print(f"    p={p:>2d}:  tau(p)={r['tau(p)']:<15d}  1+p^11={r['1 + p^11']:<15d}  match={r['match']}")
    print()

    print("  This congruence is forced by the weight-12 modular form structure:")
    print("    dim M_12 = 2 (E_12, Delta), dim S_12 = 1 (Delta).")
    print("    Clearing the 65520/691 denominator in E_12's Eisenstein constant")
    print("    forces Delta's coefficients (tau) to match sigma_11 mod 691.")
    print()

    chain = derive_all_ramanujan(n_max=30)
    out = Path(__file__).resolve().parent.parent / "data" / "w33_ramanujan_congruences.json"
    out.write_text(json.dumps(chain, indent=2, default=str))
    print(f"  wrote {out}")


if __name__ == "__main__":
    main()
