"""
HECKE EIGENFORM STRUCTURE OF Delta
====================================

Delta is a simultaneous eigenform for ALL Hecke operators T_n on S_12.
Since  dim S_12 = 1,  this is forced -- T_n Delta = tau(n) Delta automatically,
with tau(n) BOTH the eigenvalue AND the q-coefficient of Delta.

THREE CONSEQUENCES THAT CLOSE tau(n).

    (1) Multiplicativity.
            tau(m n)  =  tau(m) tau(n)          whenever  gcd(m, n) = 1.

    (2) Hecke recursion at primes.
            tau(p^{r+1})  =  tau(p) tau(p^r)  -  p^11 tau(p^{r-1}).

    (3) Deligne's theorem (ex-Ramanujan-Petersson conjecture, 1974).
            |tau(p)|  <=  2 p^{11/2}          for every prime p.

Taken together these three reduce the infinite sequence  {tau(n)}  to the
FINITE set of values  {tau(p) : p prime},  each bounded by  2 p^{11/2}.

L-FUNCTION.

    L(s, Delta)  =  sum_{n >= 1}  tau(n) / n^s
                 =  prod_p  1 / (1  -  tau(p) p^{-s}  +  p^{11 - 2 s}).

The Euler product converges for Re(s) > 13/2, has analytic continuation to C,
and satisfies the functional equation

    Lambda(s, Delta)  =  (2 pi)^{-s}  Gamma(s)  L(s, Delta)  =  Lambda(12 - s, Delta).

BRIDGE TO W(3, 3) / PROJECT MEMORY.

Project memory already contains the observation  tau(4) = tau(2)^2 - 2^{11}
(Pillar 66 / test_eisenstein).  That is the Hecke recursion at p=2, r=1.
This module makes the recursion GENERAL and plugs it into the L-function
Euler factor.
"""
from __future__ import annotations

import json
from fractions import Fraction
from math import gcd, sqrt
from pathlib import Path

from w33_eisenstein import delta_qseries, ramanujan_tau


# ======================================================================
#  Cached Delta q-series for tau lookups.
# ======================================================================
_DELTA_CACHE = {"order": 0, "series": [0]}


def tau(n: int) -> int:
    """Return tau(n) via the Delta q-series (cached)."""
    if n <= 0:
        return 0
    if _DELTA_CACHE["order"] < n:
        _DELTA_CACHE["series"] = delta_qseries(max(n, 100))
        _DELTA_CACHE["order"] = max(n, 100)
    val = _DELTA_CACHE["series"][n]
    assert val.denominator == 1
    return int(val)


# ======================================================================
#  (1)  Multiplicativity of tau on coprime arguments.
# ======================================================================
def verify_multiplicativity(pairs: list) -> list:
    results = []
    for (m, n) in pairs:
        tm, tn, tmn = tau(m), tau(n), tau(m * n)
        g = gcd(m, n)
        results.append({
            "m":       m,
            "n":       n,
            "gcd":     g,
            "tau(m)":  tm,
            "tau(n)":  tn,
            "tau(mn)": tmn,
            "product": tm * tn,
            "match":   (tm * tn == tmn) if g == 1 else None,
            "applicable": g == 1,
        })
    return results


# ======================================================================
#  (2)  Hecke recursion at prime powers.
#
#      tau(p^{r+1})  =  tau(p) tau(p^r)  -  p^11 tau(p^{r-1}).
# ======================================================================
def verify_hecke_recursion(p: int, r_max: int = 5) -> list:
    results = []
    for r in range(1, r_max + 1):
        pr_plus_1 = p ** (r + 1)
        pr = p ** r
        pr_minus_1 = p ** (r - 1)
        lhs = tau(pr_plus_1)
        rhs = tau(p) * tau(pr) - (p ** 11) * tau(pr_minus_1)
        results.append({
            "p":                p,
            "r":                r,
            "tau(p^{r+1})":     lhs,
            "predicted":        rhs,
            "match":            lhs == rhs,
        })
    return results


# ======================================================================
#  (3)  Deligne bound  |tau(p)|  <=  2 p^{11/2}.
# ======================================================================
def verify_deligne_bound(p: int) -> dict:
    tp = tau(p)
    bound = 2 * (p ** Fraction(11, 2))          # exact-rational cannot do sqrt; use float
    abs_tp = abs(tp)
    bound_float = 2 * (p ** 5.5)
    return {
        "p":           p,
        "tau(p)":      tp,
        "|tau(p)|":    abs_tp,
        "2 p^{11/2}":  bound_float,
        "satisfies":   abs_tp <= bound_float,
        "ratio":       abs_tp / bound_float,
    }


# ======================================================================
#  L(s, Delta)  Dirichlet coefficients recovered from tau(p).
#
#      L(s)  =  prod_p  (1  -  a_p p^{-s}  +  p^{11 - 2 s})^{-1}
#           =  sum  tau(n) n^{-s}.
#
#  Given  tau(p),  the Euler factor generates tau(p^r) via the Hecke
#  recursion; combining them multiplicatively gives every  tau(n).
# ======================================================================
def reconstruct_tau_from_tau_p(primes: list, n_max: int) -> list:
    """Rebuild tau(n) for n = 1..n_max from {tau(p) : p prime} via Hecke."""
    # First, tau(p^r) for each prime p <= n_max.
    prime_power_tau = {}
    for p in primes:
        if p > n_max:
            break
        # r from 0 up to floor(log_p(n_max))
        r = 0
        pr = 1
        while pr <= n_max:
            if r == 0:
                prime_power_tau[(p, 0)] = 1
            elif r == 1:
                prime_power_tau[(p, 1)] = tau(p)
            else:
                prev = prime_power_tau[(p, r - 1)]
                prev2 = prime_power_tau[(p, r - 2)]
                prime_power_tau[(p, r)] = tau(p) * prev - (p ** 11) * prev2
            r += 1
            pr = p ** r

    # Now factor n into primes and use multiplicativity.
    def factor(n):
        factors = {}
        for p in primes:
            if p * p > n and n > 1:
                factors[n] = factors.get(n, 0) + 1
                return factors
            while n % p == 0:
                factors[p] = factors.get(p, 0) + 1
                n //= p
            if n == 1:
                return factors
        if n > 1:
            factors[n] = factors.get(n, 0) + 1
        return factors

    out = []
    for n in range(1, n_max + 1):
        facs = factor(n)
        prod = 1
        for p, r in facs.items():
            prod *= prime_power_tau[(p, r)]
        out.append({
            "n":             n,
            "factorization": facs,
            "predicted":     prod,
            "actual":        tau(n),
            "match":         prod == tau(n),
        })
    return out


def first_primes_up_to(limit: int) -> list:
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, limit + 1, i):
                sieve[j] = False
    return [i for i in range(2, limit + 1) if sieve[i]]


# ======================================================================
#  Driver.
# ======================================================================
def derive_all_hecke(n_max: int = 40) -> dict:
    primes = first_primes_up_to(n_max)

    # Multiplicativity checks: a few coprime pairs and a couple non-coprime.
    mult_pairs = [(2, 3), (2, 5), (3, 5), (3, 7), (2, 7), (5, 7),
                  (2, 9), (3, 4), (4, 9), (2, 15), (3, 20),
                  (2, 4),   # NOT coprime -- should be excluded
                  (3, 9)]   # NOT coprime
    mult_results = verify_multiplicativity(mult_pairs)

    # Hecke recursion at small primes.
    recursions = {}
    for p in (2, 3, 5, 7, 11):
        recursions[p] = verify_hecke_recursion(p, r_max=4)

    # Deligne bounds at first 10 primes.
    deligne = {p: verify_deligne_bound(p) for p in first_primes_up_to(30)}

    # Reconstruction.
    recon = reconstruct_tau_from_tau_p(primes, n_max=n_max)

    return {
        "multiplicativity":       mult_results,
        "hecke_recursion":        recursions,
        "deligne_bound":          deligne,
        "reconstruction":         recon,
        "reconstruction_all_match":  all(r["match"] for r in recon),
        "multiplicativity_all_match":
            all(r["match"] for r in mult_results if r["applicable"]),
    }


def main() -> None:
    print("=" * 72)
    print("  HECKE EIGENFORM STRUCTURE OF Delta")
    print("=" * 72)
    print()

    print("  MULTIPLICATIVITY  tau(mn) = tau(m) tau(n)  for gcd(m, n) = 1:")
    pairs = [(2, 3), (2, 5), (3, 5), (2, 7), (2, 15), (3, 20)]
    for r in verify_multiplicativity(pairs):
        print(f"    tau({r['m']}) * tau({r['n']}) = {r['product']:>15d}  ==  "
              f"tau({r['m'] * r['n']}) = {r['tau(mn)']:>15d}  match={r['match']}")
    print()

    print("  HECKE RECURSION  tau(p^{r+1}) = tau(p) tau(p^r) - p^11 tau(p^{r-1}):")
    for p in (2, 3, 5, 7):
        print(f"    prime p = {p}:")
        for r in verify_hecke_recursion(p, r_max=3):
            print(f"      r={r['r']}:  LHS = tau({p}^{r['r']+1}) = {r['tau(p^{r+1})']:>15d}"
                  f"   predicted = {r['predicted']:>15d}  match={r['match']}")
    print()

    print("  DELIGNE BOUND  |tau(p)|  <=  2 p^{11/2}:")
    for p in first_primes_up_to(30):
        b = verify_deligne_bound(p)
        print(f"    p={p:>2d}:  |tau(p)|={b['|tau(p)|']:>13d}  2 p^{{11/2}}={b['2 p^{11/2}']:>18.2f}"
              f"  ratio={b['ratio']:.4f}  ok={b['satisfies']}")
    print()

    print("  RECONSTRUCTING tau(n) FROM tau(p):")
    primes = first_primes_up_to(40)
    rec = reconstruct_tau_from_tau_p(primes, n_max=20)
    for r in rec[:15]:
        print(f"    n={r['n']:>2d}:  factored {r['factorization']}  ->  "
              f"predicted {r['predicted']:>15d}   actual {r['actual']:>15d}   match={r['match']}")
    print()

    print("  Every tau(n) is determined by {tau(p) : p prime} via Hecke.")
    print()

    chain = derive_all_hecke(n_max=40)
    out = Path(__file__).resolve().parent.parent / "data" / "w33_hecke_delta.json"
    out.write_text(json.dumps(chain, indent=2, default=str))
    print(f"  wrote {out}")


if __name__ == "__main__":
    main()
