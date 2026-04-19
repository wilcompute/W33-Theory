"""Sato-Tate distribution for E_11 and the CM baseline y^2 = x^3 - x.

For a non-CM elliptic curve E over Q (e.g. E_11: y^2 + y = x^3 - x^2)
the Sato-Tate conjecture -- now the Sato-Tate *theorem* (Barnet-Lamb,
Geraghty, Harris, Taylor, 2011) -- asserts that as p ranges over primes
of good reduction, the normalised trace

    x_p = a_p / (2 sqrt p)  in [-1, 1]

is equidistributed with respect to the Sato-Tate density

    mu_ST(x) = (2 / pi) sqrt(1 - x^2) dx                   (semicircle).

Moments of mu_ST:
    E[x^{2k}]   = C_k / 4^k     (Catalan numbers),
    E[x^0]  = 1,    E[x^2] = 1/4,    E[x^4] = 1/8,
    E[x^6]  = 5/64, E[x^8] = 7/128.
All odd moments vanish by symmetry.

For a CM curve (e.g. y^2 = x^3 - x, CM by Z[i], extra endomorphisms)
the distribution is the *CM Sato-Tate law*: for half the primes (the
inert ones under the CM field, here p ≡ 3 mod 4) a_p = 0 identically,
and the other half splits into a uniform [-1, 1] along x_p.  Thus
    mu_{ST, CM}(x) = (1/2) delta_0(x) + (1/(2 pi sqrt(1 - x^2))) dx.

Diagnostic moments for the CM law:
    E[x^{2k}] = (1/2) * (1 / (2k + 0.5))  ...  no simpler:
                     = (1/2) * binom(2k, k) / 4^k
    E[x^0] = 1,  E[x^2] = 1/4,  E[x^4] = 3/16,  E[x^6] = 5/32.

So second moments agree (1/4 both cases), but the CM law gives
higher even moments that are strictly larger than the semicircle.
This is the cleanest numerical distinguisher.

Five summary-chain pins below.

Layer 65 -- closes the statistical face of the Eichler-Shimura /
modularity result of Layer 57, and pins the CM vs non-CM dichotomy
numerically over the first ~170 primes.
"""

from __future__ import annotations

from math import comb
from typing import Any

import mpmath as mp

from w33_hasse_bound import a_p_E11, a_p_weierstrass


# ----------------------------------------------------------------------
# Prime sieve.
# ----------------------------------------------------------------------
def primes_up_to(N: int) -> list[int]:
    if N < 2:
        return []
    sieve = [True] * (N + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(N ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, N + 1, i):
                sieve[j] = False
    return [i for i in range(N + 1) if sieve[i]]


# ----------------------------------------------------------------------
# Semicircle moments: E[x^{2k}] = C_k / 4^k.
# ----------------------------------------------------------------------
def semicircle_even_moment(k: int) -> mp.mpf:
    """E_mu_ST[x^{2k}] = C_k / 4^k where C_k = binom(2k, k) / (k + 1)."""
    Ck = mp.mpf(comb(2 * k, k)) / (k + 1)
    return Ck / mp.mpf(4 ** k)


def cm_even_moment(k: int) -> mp.mpf:
    """E_{mu_{ST, CM}}[x^{2k}] = (1/2) * binom(2k, k) / 4^k."""
    return mp.mpf(comb(2 * k, k)) / mp.mpf(2 * 4 ** k)


# ----------------------------------------------------------------------
# Sample moments for E_11 (non-CM) over primes of good reduction (p != 11).
# ----------------------------------------------------------------------
def E11_sample_moments(prime_limit: int = 1000,
                         k_max: int = 4) -> dict[str, Any]:
    primes = [p for p in primes_up_to(prime_limit) if p != 11]
    xs = [a_p_E11(p) / (2 * float(mp.sqrt(p))) for p in primes]
    moments: dict[int, float] = {}
    for k in range(k_max + 1):
        moments[k] = sum(x ** k for x in xs) / len(xs)
    return {"n_primes": len(xs),
            "moments": moments,
            "samples": xs[:20]}


def CM_sample_moments(prime_limit: int = 1000,
                       k_max: int = 4) -> dict[str, Any]:
    """Same for y^2 = x^3 - x (CM by Z[i])."""
    primes = [p for p in primes_up_to(prime_limit) if p > 2]
    # a_p for y^2 = x^3 + A x + B  with (A, B) = (-1, 0).
    xs = [a_p_weierstrass(-1, 0, p) / (2 * float(mp.sqrt(p))) for p in primes]
    moments: dict[int, float] = {}
    for k in range(k_max + 1):
        moments[k] = sum(x ** k for x in xs) / len(xs)
    frac_zero = sum(1 for x in xs if abs(x) < 1e-15) / len(xs)
    return {"n_primes": len(xs),
            "moments": moments,
            "samples": xs[:20],
            "fraction_a_p_zero": frac_zero}


# ----------------------------------------------------------------------
# Verifiers.
# ----------------------------------------------------------------------
def verify_E11_second_moment(prime_limit: int = 2000,
                                tol: float = 0.08) -> dict[str, Any]:
    """Second moment ~ 1/4 as p_max -> infinity.  For primes up to 2000
    the sample second moment should be within 0.08 of 1/4."""
    s = E11_sample_moments(prime_limit=prime_limit, k_max=2)
    m2 = s["moments"][2]
    target = 1.0 / 4
    diff = abs(m2 - target)
    return {
        "sample_second_moment": m2,
        "semicircle_second_moment": target,
        "abs_diff": diff,
        "n_primes": s["n_primes"],
        "match": bool(diff < tol),
    }


def verify_E11_fourth_moment(prime_limit: int = 2000,
                                tol: float = 0.05) -> dict[str, Any]:
    """Fourth moment -> 1/8 (semicircle) vs 3/16 (CM).  At p_max = 2000,
    sample fourth moment of E_11 should be within 0.05 of 1/8 = 0.125."""
    s = E11_sample_moments(prime_limit=prime_limit, k_max=4)
    m4 = s["moments"][4]
    target = 1.0 / 8
    diff = abs(m4 - target)
    return {
        "sample_fourth_moment": m4,
        "semicircle_fourth_moment": target,
        "cm_fourth_moment": 3.0 / 16,
        "abs_diff_to_semicircle": diff,
        "abs_diff_to_cm": abs(m4 - 3.0 / 16),
        "match": bool(diff < tol),
    }


def verify_E11_odd_moments_small(prime_limit: int = 2000,
                                   tol: float = 0.05) -> dict[str, Any]:
    """Odd moments -> 0 by symmetry.  For p_max = 2000, |m1|, |m3| < 0.05."""
    s = E11_sample_moments(prime_limit=prime_limit, k_max=3)
    m1 = abs(s["moments"][1])
    m3 = abs(s["moments"][3])
    return {
        "abs_m1": m1,
        "abs_m3": m3,
        "match": bool(m1 < tol and m3 < tol),
    }


def verify_CM_fraction_of_zero_traces(prime_limit: int = 2000,
                                         tol: float = 0.05) -> dict[str, Any]:
    """For y^2 = x^3 - x, a_p = 0 iff p ≡ 3 (mod 4) (the CM field Q(i)
    is inert).  Natural density is 1/2 by Dirichlet."""
    s = CM_sample_moments(prime_limit=prime_limit, k_max=0)
    frac = s["fraction_a_p_zero"]
    diff = abs(frac - 0.5)
    return {
        "fraction_a_p_zero": frac,
        "target_density_half": 0.5,
        "abs_diff": diff,
        "match": bool(diff < tol),
    }


def verify_CM_fourth_moment_larger(prime_limit: int = 2000,
                                      tol: float = 0.05) -> dict[str, Any]:
    """For CM curve, fourth moment ~ 3/16 = 0.1875 > 1/8 = 0.125 of
    semicircle.  Pin that the CM sample fourth moment lies in the
    expected band near 3/16."""
    s = CM_sample_moments(prime_limit=prime_limit, k_max=4)
    m4 = s["moments"][4]
    diff = abs(m4 - 3.0 / 16)
    return {
        "cm_fourth_moment_sample": m4,
        "cm_fourth_moment_theoretical": 3.0 / 16,
        "semicircle_fourth_moment": 1.0 / 8,
        "abs_diff_to_cm": diff,
        "match": bool(diff < tol),
    }


def verify_E11_xp_in_unit_interval(prime_limit: int = 1000) -> dict[str, Any]:
    """x_p = a_p / (2 sqrt p) in [-1, 1] — this is the Hasse bound again."""
    primes = [p for p in primes_up_to(prime_limit) if p != 11]
    rows = []
    all_match = True
    for p in primes:
        x = a_p_E11(p) / (2 * float(mp.sqrt(p)))
        match = -1 <= x <= 1
        if not match:
            rows.append({"p": p, "x_p": x})
        all_match = all_match and match
    return {"all_match": all_match, "n_primes": len(primes),
            "violations": rows}


def verify_moment_ladder_semicircle() -> dict[str, Any]:
    """Semicircle moments C_k / 4^k match the closed forms
       C_0 = 1, C_1 = 1, C_2 = 2, C_3 = 5, C_4 = 14
       so E[x^0]=1, E[x^2]=1/4, E[x^4]=1/8, E[x^6]=5/64, E[x^8]=7/128."""
    rows = []
    expected = {0: mp.mpf(1),
                1: mp.mpf(1) / 4,
                2: mp.mpf(1) / 8,
                3: mp.mpf(5) / 64,
                4: mp.mpf(7) / 128}
    all_match = True
    for k, exp in expected.items():
        computed = semicircle_even_moment(k)
        match = abs(computed - exp) < mp.mpf("1e-30")
        rows.append({"k": k, "computed": float(computed),
                     "expected": float(exp), "match": bool(match)})
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows}


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------
def derive_all() -> dict[str, Any]:
    hasse = verify_E11_xp_in_unit_interval(prime_limit=1000)
    m2 = verify_E11_second_moment(prime_limit=2000, tol=0.08)
    m4 = verify_E11_fourth_moment(prime_limit=2000, tol=0.05)
    odd = verify_E11_odd_moments_small(prime_limit=2000, tol=0.05)
    cm_frac = verify_CM_fraction_of_zero_traces(prime_limit=2000, tol=0.05)
    cm_m4 = verify_CM_fourth_moment_larger(prime_limit=2000, tol=0.05)
    ladder = verify_moment_ladder_semicircle()
    chain = {
        "E11_normalised_trace_x_p_in_minus_1_to_1":
            hasse["all_match"],
        "E11_sample_second_moment_matches_semicircle_quarter":
            m2["match"],
        "E11_sample_fourth_moment_matches_semicircle_eighth":
            m4["match"],
        "E11_sample_odd_moments_vanish_within_tolerance":
            odd["match"],
        "CM_curve_y2_x3_minus_x_half_primes_have_a_p_zero":
            cm_frac["match"],
        "CM_curve_fourth_moment_matches_3_over_16_not_1_over_8":
            cm_m4["match"],
        "semicircle_moment_ladder_matches_catalan_over_4k":
            ladder["all_match"],
    }
    return {
        "hasse": hasse,
        "E11_second_moment": m2,
        "E11_fourth_moment": m4,
        "E11_odd_moments": odd,
        "CM_fraction_zero": cm_frac,
        "CM_fourth_moment": cm_m4,
        "semicircle_ladder": ladder,
        "summary_chain": chain,
    }


if __name__ == "__main__":
    s = derive_all()
    print("summary_chain:")
    for k, v in s["summary_chain"].items():
        print(f"  {k}: {v}")
    print("\nE_11 sample moments vs semicircle targets (prime_limit=2000):")
    print(f"  E[x^2] sample = {s['E11_second_moment']['sample_second_moment']:.4f}"
          f"  target = {s['E11_second_moment']['semicircle_second_moment']}")
    print(f"  E[x^4] sample = {s['E11_fourth_moment']['sample_fourth_moment']:.4f}"
          f"  semi = {s['E11_fourth_moment']['semicircle_fourth_moment']},"
          f"  CM = {s['E11_fourth_moment']['cm_fourth_moment']}")
    print(f"  |E[x^1]| = {s['E11_odd_moments']['abs_m1']:.4f}")
    print(f"  |E[x^3]| = {s['E11_odd_moments']['abs_m3']:.4f}")
    print(f"\nCM baseline y^2 = x^3 - x:")
    print(f"  fraction a_p = 0 = {s['CM_fraction_zero']['fraction_a_p_zero']:.4f}"
          f"  (target 0.5)")
    print(f"  E[x^4] CM sample = {s['CM_fourth_moment']['cm_fourth_moment_sample']:.4f}"
          f"  theoretical = {s['CM_fourth_moment']['cm_fourth_moment_theoretical']}")
