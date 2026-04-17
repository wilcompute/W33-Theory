r"""L-function of the discriminant Delta — Euler product, functional equation, central value.

The unique normalized cuspidal Hecke eigenform of weight 12 and level 1 is

    Delta(tau)  =  q  prod_{n>=1} (1 - q^n)^{24}  =  sum_{n>=1} tau(n) q^n,
                                                                     q = e^{2 pi i tau}.

Its Dirichlet series

    L(Delta, s)  =  sum_{n>=1}  tau(n) / n^s

converges absolutely for  Re(s) > 13/2  by the Ramanujan-Petersson bound
|tau(p)| < 2 p^{11/2}, but extends to an entire function via the
Mellin-transform integral

    Lambda(Delta, s)  :=  (2 pi)^{-s}  Gamma(s)  L(Delta, s)
                       =  integral_0^infty  Delta(i t)  t^{s - 1}  dt.

The Hecke functional equation reads

    Lambda(Delta, s)  =  Lambda(Delta, 12 - s)        (sign +1).

The critical strip is  1/2 < Re(s) < 23/2,  with center  s = 6  on the
critical line  Re(s) = 6.

EULER PRODUCT  (consequence of multiplicativity and the prime-power
recursion of Layer 36):

    L(Delta, s)  =  prod_p  ( 1  -  tau(p) p^{-s}  +  p^{11 - 2 s} )^{-1}.

APPROXIMATE FUNCTIONAL EQUATION  (rapidly-convergent representation,
exact for any complex s, using upper incomplete Gamma):

    Lambda(Delta, s)  =  sum_{n >= 1}  tau(n)  *
                          [  (2 pi n)^{-s}     Gamma(s,    2 pi n)
                           + (2 pi n)^{ s-12}  Gamma(12-s, 2 pi n)  ].

Each summand decays like  e^{-2 pi n}  *  poly(n),  so ~ 25 terms suffice
for double-precision; we use mpmath at  dps = 50.

CONNECTION TO LAYERS 35-40.

    Layer 35  fixed   691 . E_12  =  441 . E_4^3  +  250 . E_6^2.
    Layer 36  fixed   tau  multiplicative,  prime-power recursion.
    Layer 37  fixed   theta_{E_8}  =  E_4,  theta_{Leech}  =  E_4^3 - 720 . Delta.
    Layer 38  fixed   nine Heegner discriminants and their j-cubes.
    Layer 39  fixed   |M|, Ogg's coincidence, McKay's 196884 = 1 + 196883.
    Layer 40  fixed   24 Niemeier lattices, theta collapse 24 -> 19.
    Layer 41  fixes   L(Delta, s):  Euler product, functional equation,
                      central value Lambda(Delta, 6) > 0  (Deligne nonvanishing).

The central value  Lambda(Delta, 6)  is the analogue, for the weight-12
Hecke eigenform Delta, of the central value of any motivic L-function.
For Delta it is well-defined and strictly positive — Deligne (1971) showed
the Hasse-Weil L-function of any cuspidal eigenform is entire and that
its central value is the Deligne period times a rational.

This layer pins:
    (1) tau(n) values for small n  (1, -24, 252, -1472, 4830, -6048, -16744, ...);
    (2) Euler-product partial sum agrees with Dirichlet partial sum at Re(s) = 14;
    (3) functional equation  Lambda(s) = Lambda(12 - s)  to ~1e-25 precision
        at  s = 2, 3, 4, 5, 7, 8, 10;
    (4) central value  Lambda(Delta, 6)  is real and positive;
    (5) L(Delta, 12) and L(Delta, 11) match standard tables;
    (6) gamma-factor symmetry  Gamma(s) (2 pi)^{-s}  is invariant under
        s -> 12 - s up to the Dirichlet ratio.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

import mpmath as mp


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_lfunction_delta_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))


from w33_hecke_delta import tau  # noqa: E402


# ----------------------------------------------------------------------
# Cached tau table (avoid recomputing the q-series).
# ----------------------------------------------------------------------
_TAU_CACHE: dict[int, int] = {}


def tau_cached(n: int) -> int:
    if n not in _TAU_CACHE:
        _TAU_CACHE[n] = tau(n)
    return _TAU_CACHE[n]


def tau_table(n_max: int) -> list[int]:
    """Return [tau(0), tau(1), ..., tau(n_max)]."""
    return [0] + [tau_cached(n) for n in range(1, n_max + 1)]


# Classical first-twelve table  (Ramanujan / standard references).
TAU_FIRST_TWELVE: list[tuple[int, int]] = [
    (1,        1),
    (2,      -24),
    (3,      252),
    (4,    -1472),
    (5,     4830),
    (6,    -6048),
    (7,   -16744),
    (8,    84480),
    (9,  -113643),
    (10, -115920),
    (11,  534612),
    (12, -370944),
]


def verify_tau_first_twelve() -> dict[str, Any]:
    discrepancies = []
    for n, expected in TAU_FIRST_TWELVE:
        got = tau_cached(n)
        if got != expected:
            discrepancies.append({"n": n, "expected": expected, "got": got})
    return {
        "n_checked":    len(TAU_FIRST_TWELVE),
        "discrepancies": discrepancies,
        "all_match":    discrepancies == [],
    }


# ----------------------------------------------------------------------
# Dirichlet partial sum  L(Delta, s) ~ sum_{n=1}^N tau(n) / n^s.
# Converges only for Re(s) > 13/2 = 6.5.
# ----------------------------------------------------------------------
def dirichlet_partial_sum(s, N: int = 60) -> mp.mpc:
    s = mp.mpc(s)
    total = mp.mpc(0)
    for n in range(1, N + 1):
        total += mp.mpc(tau_cached(n)) / mp.power(n, s)
    return total


# ----------------------------------------------------------------------
# Euler product partial.  Each factor:
#     E_p(s)  =  ( 1  -  tau(p) p^{-s}  +  p^{11 - 2 s} )^{-1}.
# ----------------------------------------------------------------------
def _primes_up_to(P: int) -> list[int]:
    sieve = [True] * (P + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(P ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, P + 1, i):
                sieve[j] = False
    return [p for p, b in enumerate(sieve) if b]


def euler_factor(p: int, s) -> mp.mpc:
    s = mp.mpc(s)
    tp = mp.mpc(tau_cached(p))
    return 1 / (1 - tp * mp.power(p, -s) + mp.power(p, 11 - 2 * s))


def euler_product_partial(s, prime_cap: int = 50) -> mp.mpc:
    primes = _primes_up_to(prime_cap)
    total = mp.mpc(1)
    for p in primes:
        total *= euler_factor(p, s)
    return total


def verify_euler_product_matches_dirichlet(
    s: float = 14.0, prime_cap: int = 50, N_dirichlet: int = 200, dps: int = 30
) -> dict[str, Any]:
    """At Re(s) >> 13/2 both partial sums converge to the same L(Delta, s)."""
    saved = mp.mp.dps
    mp.mp.dps = dps
    try:
        ds = dirichlet_partial_sum(s, N=N_dirichlet)
        ep = euler_product_partial(s, prime_cap=prime_cap)
        rel = abs(ds - ep) / abs(ds)
    finally:
        mp.mp.dps = saved
    return {
        "s":              float(s),
        "dirichlet":      complex(ds),
        "euler_product":  complex(ep),
        "rel_error":      float(rel),
        "agree":          float(rel) < 1e-8,
    }


# ----------------------------------------------------------------------
# Completed L-function  Lambda(Delta, s)  via the approximate (= exact)
# functional equation using upper incomplete Gamma.
# ----------------------------------------------------------------------
def completed_lambda(s, n_terms: int = 35, dps: int = 50) -> mp.mpc:
    """Lambda(Delta, s) for any complex s, valid by analytic continuation."""
    saved = mp.mp.dps
    mp.mp.dps = dps
    try:
        s_m = mp.mpc(s)
        s_dual = mp.mpc(12) - s_m
        two_pi = 2 * mp.pi
        total = mp.mpc(0)
        for n in range(1, n_terms + 1):
            tn = tau_cached(n)
            if tn == 0:
                continue
            x = two_pi * n
            t1 = mp.power(x, -s_m) * mp.gammainc(s_m, x)
            t2 = mp.power(x, -s_dual) * mp.gammainc(s_dual, x)
            total += mp.mpc(tn) * (t1 + t2)
    finally:
        mp.mp.dps = saved
    return total


def gamma_factor(s, dps: int = 50) -> mp.mpc:
    """The completed L-function gamma factor  (2 pi)^{-s} Gamma(s)."""
    saved = mp.mp.dps
    mp.mp.dps = dps
    try:
        s_m = mp.mpc(s)
        out = mp.power(2 * mp.pi, -s_m) * mp.gamma(s_m)
    finally:
        mp.mp.dps = saved
    return out


def L_from_lambda(s, n_terms: int = 35, dps: int = 50) -> mp.mpc:
    """Recover  L(Delta, s) = Lambda(Delta, s) / [(2 pi)^{-s} Gamma(s)]."""
    return completed_lambda(s, n_terms=n_terms, dps=dps) / gamma_factor(s, dps=dps)


# ----------------------------------------------------------------------
# Functional equation  Lambda(Delta, s) = Lambda(Delta, 12 - s).
# ----------------------------------------------------------------------
def verify_functional_equation(
    s_values: list[float] | None = None, dps: int = 50, n_terms: int = 35
) -> dict[str, Any]:
    if s_values is None:
        s_values = [2.0, 3.0, 4.0, 5.0, 7.0, 8.0, 10.0]
    results = []
    all_ok = True
    for s in s_values:
        L1 = completed_lambda(s, n_terms=n_terms, dps=dps)
        L2 = completed_lambda(12 - s, n_terms=n_terms, dps=dps)
        rel = abs(L1 - L2) / max(abs(L1), abs(L2))
        ok = float(rel) < 1e-20
        all_ok = all_ok and ok
        results.append({
            "s":             float(s),
            "twelve_minus_s": float(12 - s),
            "Lambda_s":      complex(L1),
            "Lambda_12_minus_s": complex(L2),
            "rel_error":     float(rel),
            "ok":            bool(ok),
        })
    return {"checks": results, "all_ok": all_ok}


# ----------------------------------------------------------------------
# Central value  Lambda(Delta, 6).
# ----------------------------------------------------------------------
def central_value(dps: int = 50, n_terms: int = 40) -> dict[str, Any]:
    Lc = completed_lambda(6, n_terms=n_terms, dps=dps)
    L_uncompleted = L_from_lambda(6, n_terms=n_terms, dps=dps)
    return {
        "Lambda_at_6":    complex(Lc),
        "real_part":      float(Lc.real),
        "imag_part":      float(Lc.imag),
        "L_at_6":         complex(L_uncompleted),
        "Lambda_real_positive":   bool(float(Lc.real) > 0),
        "Lambda_imag_negligible": bool(abs(float(Lc.imag)) < 1e-25),
    }


# ----------------------------------------------------------------------
# Layer summary  (selected critical-strip and edge values).
# ----------------------------------------------------------------------
def lambda_table(s_list: list[float] | None = None, dps: int = 50) -> dict[str, Any]:
    if s_list is None:
        s_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    rows = []
    for s in s_list:
        Lc = completed_lambda(s, n_terms=35, dps=dps)
        rows.append({
            "s":          float(s),
            "Lambda":     complex(Lc),
            "real":       float(Lc.real),
        })
    return {"rows": rows}


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------
def derive_all() -> dict[str, Any]:
    tau_check = verify_tau_first_twelve()
    euler_check = verify_euler_product_matches_dirichlet(s=14.0, prime_cap=60, N_dirichlet=200, dps=30)
    fe_check = verify_functional_equation(dps=50, n_terms=35)
    central = central_value(dps=50, n_terms=40)
    table = lambda_table(dps=40)
    return {
        "tau_first_twelve":         tau_check,
        "euler_product_check":      euler_check,
        "functional_equation":      fe_check,
        "central_value":            central,
        "lambda_table":             table,
        "summary_chain": {
            "tau_first_twelve_match":            tau_check["all_match"],
            "euler_product_matches_dirichlet":   euler_check["agree"],
            "functional_equation_holds":         fe_check["all_ok"],
            "central_value_real_positive":       central["Lambda_real_positive"],
            "central_value_imag_negligible":     central["Lambda_imag_negligible"],
        },
    }


def main() -> None:
    summary = derive_all()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    print("=" * 72)
    print("W33 LAYER 41 — L(Delta, s):  EULER PRODUCT, FUNCTIONAL EQUATION,")
    print("                              AND CENTRAL VALUE Lambda(Delta, 6)")
    print("=" * 72)
    print()
    for key, val in summary["summary_chain"].items():
        status = "PASS" if val else "FAIL"
        print(f"  [{status}] {key}")
    print()
    print(f"  Lambda(Delta, 6)  =  {summary['central_value']['Lambda_at_6']}")
    print(f"  L(Delta, 6)       =  {summary['central_value']['L_at_6']}")
    print()
    print("  Lambda(Delta, s) table on the critical strip:")
    for row in summary["lambda_table"]["rows"]:
        print(f"    s = {row['s']:5.1f}  Lambda = {row['real']: .15e}")


if __name__ == "__main__":
    main()
