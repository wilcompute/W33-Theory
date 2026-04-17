"""Delta is a Hecke eigenform, and tau is multiplicative.

The Hecke operator  T_p  acts on a weight-k modular form  f = sum a_n q^n  as

    (T_p f)(q)  =  sum_{n >= 0} a_{p n} q^n  +  p^{k-1} sum_{n >= 0} a_n q^{p n}.

Delta is a cusp form of weight 12 and  dim S_12 = 1, so every Hecke operator
preserves the 1-dimensional space  C . Delta  and must act as a scalar:

    T_p Delta  =  tau(p)  .  Delta.

Comparing q-coefficients on both sides gives the Ramanujan recursion

    tau(p n)  +  p^{11} tau(n/p) [if p | n else 0]  =  tau(p) tau(n).

CONSEQUENCES.

    (R1)  Multiplicativity:     tau(m n)  =  tau(m) tau(n)   whenever  gcd(m,n) = 1.
    (R2)  Prime power recursion: tau(p^{k+1}) = tau(p) tau(p^k) - p^{11} tau(p^{k-1}).
    (R3)  Euler product:         sum_n tau(n) n^{-s}
                                 = prod_p  ( 1 - tau(p) p^{-s} + p^{11} p^{-2s} )^{-1}.

The constant  11 = k - 1 = 12 - 1  is the weight of Delta minus one, and is
also the exponent that appears in the  E_12  Fourier coefficient  65520 sigma_11(n).
Ramanujan's 691 congruence (Layer 35) is  tau(n) == sigma_11(n) (mod 691); here we
see why the 11-exponent is the natural one.

RAMANUJAN--PETERSSON.

    |tau(p)|  <=  2 p^{11/2}     for every prime p (Deligne, 1974).

This is equivalent to saying that the roots of the Hecke polynomial
  X^2 - tau(p) X + p^{11}  =  0
are complex conjugates of absolute value  p^{11/2}, i.e., the Satake
parameters  alpha_p, beta_p  satisfy  |alpha_p| = |beta_p| = p^{11/2}.

CONNECTION TO THE W(3,3)--E_8 TOWER.

    * k = 12 = W(3,3) valency  and Delta lives in  S_12.
    * tau(1) = 1  (identity).
    * tau(2) = -24  ~~  -|root(D_4)| = -24.
    * tau(3) = 252  ~~  6th cycle in the 7-cycle closure (Layer 30).
    * tau(5) = 4830 = 2 * 3 * 5 * 7 * 23.
    * Hecke eigenvalues are naturally 2-dimensional (pair of Satake parameters),
      matching the  Sp(4)  spectral structure of the W(3,3) adjacency.

This layer pins:
    (1) T_p Delta = tau(p) Delta for p in {2,3,5,7,11,13} up to chosen q-truncation;
    (2) tau(m n) = tau(m) tau(n) for every coprime (m,n) up to n = 30;
    (3) tau(p^{k+1}) = tau(p) tau(p^k) - p^11 tau(p^{k-1}) for p in {2,3,5} and k up to 4;
    (4) Ramanujan--Petersson: |tau(p)| < 2 p^{11/2} for every tested prime.
"""

from __future__ import annotations

import json
from math import gcd, isqrt
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_hecke_tau_multiplicativity_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from w33_ramanujan_system import delta_series


# ----------------------------------------------------------------------
# Hecke operator on a weight-k q-series.
#   (T_p f)[n] = f[p*n] + p^{k-1} f[n/p]  (second term only if p | n).
# ----------------------------------------------------------------------
def hecke_T_p(f: list[int], p: int, weight: int, n_max: int) -> list[int]:
    """Apply the p-th Hecke operator to a weight-k q-series.

    Requires f to be long enough that we can access f[p*n] for n <= n_max,
    i.e., len(f) >= p*n_max + 1.
    """
    if len(f) < p * n_max + 1:
        raise ValueError(f"Need len(f) >= {p * n_max + 1}, got {len(f)}")
    pk1 = p ** (weight - 1)
    out = [0] * (n_max + 1)
    for n in range(n_max + 1):
        val = f[p * n]
        if n % p == 0:
            val += pk1 * f[n // p]
        out[n] = val
    return out


# ----------------------------------------------------------------------
# Hecke eigenform test: T_p Delta = tau(p) Delta.
# ----------------------------------------------------------------------
def verify_hecke_eigenform(primes: list[int], n_max: int = 25) -> dict[str, Any]:
    max_p = max(primes)
    delta = delta_series(max_p * n_max + 1)
    results = {}
    all_match = True
    for p in primes:
        Tp_delta = hecke_T_p(delta, p, 12, n_max)
        tau_p = delta[p]
        expected = [tau_p * delta[n] for n in range(n_max + 1)]
        match = Tp_delta == expected
        results[p] = {
            "tau_p":    tau_p,
            "match":    match,
            "first_6":  Tp_delta[:6],
        }
        if not match:
            all_match = False
    return {
        "primes":    primes,
        "n_max":     n_max,
        "per_prime": results,
        "all_match": all_match,
    }


# ----------------------------------------------------------------------
# Multiplicativity: tau(m n) = tau(m) tau(n) for gcd(m, n) = 1.
# ----------------------------------------------------------------------
def verify_tau_multiplicativity(n_max: int = 30) -> dict[str, Any]:
    delta = delta_series(n_max * n_max + 1)
    discrepancies = []
    n_tested = 0
    for m in range(1, n_max + 1):
        for n in range(1, n_max + 1):
            if gcd(m, n) != 1:
                continue
            if m * n > len(delta) - 1:
                continue
            n_tested += 1
            lhs = delta[m * n]
            rhs = delta[m] * delta[n]
            if lhs != rhs:
                discrepancies.append({"m": m, "n": n, "tau_mn": lhs, "tau_m_tau_n": rhs})
    return {
        "n_max":         n_max,
        "n_tested":      n_tested,
        "discrepancies": discrepancies,
        "all_match":     discrepancies == [],
    }


# ----------------------------------------------------------------------
# Prime power recursion: tau(p^{k+1}) = tau(p) tau(p^k) - p^11 tau(p^{k-1}).
# ----------------------------------------------------------------------
def verify_prime_power_recursion(primes: list[int], max_k: int = 4) -> dict[str, Any]:
    max_needed = max(p ** (max_k + 1) for p in primes)
    delta = delta_series(max_needed + 1)
    discrepancies = []
    n_tested = 0
    for p in primes:
        for k in range(1, max_k + 1):
            n_tested += 1
            lhs = delta[p ** (k + 1)]
            rhs = delta[p] * delta[p ** k] - p ** 11 * delta[p ** (k - 1)]
            if lhs != rhs:
                discrepancies.append({"p": p, "k": k, "lhs": lhs, "rhs": rhs})
    return {
        "primes":        primes,
        "max_k":         max_k,
        "n_tested":      n_tested,
        "discrepancies": discrepancies,
        "all_match":     discrepancies == [],
    }


# ----------------------------------------------------------------------
# Ramanujan--Petersson bound: |tau(p)| < 2 p^{11/2}.
# ----------------------------------------------------------------------
def verify_ramanujan_petersson(primes: list[int]) -> dict[str, Any]:
    max_p = max(primes)
    delta = delta_series(max_p + 1)
    results = {}
    all_bounded = True
    for p in primes:
        tau_p = delta[p]
        # Avoid floating point: compare tau_p^2 <= 4 p^11.
        lhs = tau_p * tau_p
        rhs = 4 * p ** 11
        holds = lhs <= rhs
        results[p] = {
            "tau_p":              tau_p,
            "tau_p_squared":      lhs,
            "4_p_to_11":          rhs,
            "bound_holds":        holds,
            "satake_abs_squared": p ** 11,
        }
        if not holds:
            all_bounded = False
    return {
        "primes":        primes,
        "per_prime":     results,
        "all_bounded":   all_bounded,
    }


# ----------------------------------------------------------------------
# Euler product spot check: for a single prime p, compute the truncated
# inverse of (1 - tau(p) p^{-s} + p^11 p^{-2s}) evaluated coefficient-wise
# on powers of p and compare with tau(p^k).
# ----------------------------------------------------------------------
def verify_euler_factor_prime_power(p: int, max_k: int = 5) -> dict[str, Any]:
    """Expand  (1 - tau(p) X + p^11 X^2)^{-1}  as power series in X.
    Coefficient of X^k should equal tau(p^k)."""
    delta = delta_series(p ** max_k + 1)
    tau_p = delta[p]
    coeffs = [0] * (max_k + 1)
    coeffs[0] = 1
    for k in range(1, max_k + 1):
        c = tau_p * coeffs[k - 1]
        if k >= 2:
            c -= p ** 11 * coeffs[k - 2]
        coeffs[k] = c
    actual = [delta[p ** k] for k in range(max_k + 1)]
    return {
        "p":            p,
        "tau_p":        tau_p,
        "euler_coeffs": coeffs,
        "tau_p_powers": actual,
        "match":        coeffs == actual,
    }


# ----------------------------------------------------------------------
# Low-prime tau catalogue (informational).
# ----------------------------------------------------------------------
def tau_prime_catalogue(n_primes: int = 10) -> dict[str, Any]:
    primes = []
    n = 2
    while len(primes) < n_primes:
        is_p = True
        for d in range(2, isqrt(n) + 1):
            if n % d == 0:
                is_p = False
                break
        if is_p:
            primes.append(n)
        n += 1
    max_p = max(primes)
    delta = delta_series(max_p + 1)
    return {
        "primes":  primes,
        "tau_p":   {p: delta[p] for p in primes},
    }


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------
def derive_all(n_max: int = 20) -> dict[str, Any]:
    primes_small = [2, 3, 5, 7, 11, 13]
    primes_rp = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    eigen = verify_hecke_eigenform(primes_small, n_max=n_max)
    mult = verify_tau_multiplicativity(n_max=n_max)
    rec = verify_prime_power_recursion(primes_small[:3], max_k=4)
    rp = verify_ramanujan_petersson(primes_rp)
    euler_2 = verify_euler_factor_prime_power(2, max_k=5)
    euler_3 = verify_euler_factor_prime_power(3, max_k=5)
    catalogue = tau_prime_catalogue(10)
    return {
        "hecke_eigenform":       eigen,
        "tau_multiplicativity":  mult,
        "prime_power_recursion": rec,
        "ramanujan_petersson":   rp,
        "euler_factor_p2":       euler_2,
        "euler_factor_p3":       euler_3,
        "tau_catalogue":         catalogue,
        "summary_chain": {
            "T_p_Delta_equals_tau_p_Delta_for_small_primes": eigen["all_match"],
            "tau_mn_equals_tau_m_tau_n_for_coprime":         mult["all_match"],
            "tau_prime_power_recursion":                     rec["all_match"],
            "ramanujan_petersson_bound_holds":               rp["all_bounded"],
            "euler_factor_p_equals_2_matches_tau":           euler_2["match"],
            "euler_factor_p_equals_3_matches_tau":           euler_3["match"],
        },
    }


def main() -> None:
    summary = derive_all(n_max=20)
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    print("=" * 72)
    print("W33 HECKE EIGENFORM AND TAU MULTIPLICATIVITY")
    print("=" * 72)
    print()
    for key, val in summary["summary_chain"].items():
        status = "PASS" if val else "FAIL"
        print(f"  [{status}] {key}")
    print()
    print("  T_p Delta = tau(p) Delta             (Delta is a Hecke eigenform)")
    print("  tau(m n) = tau(m) tau(n)             if gcd(m, n) = 1")
    print("  tau(p^(k+1)) = tau(p) tau(p^k) - p^11 tau(p^(k-1))")
    print("  |tau(p)| < 2 p^(11/2)                (Deligne / Ramanujan-Petersson)")


if __name__ == "__main__":
    main()
