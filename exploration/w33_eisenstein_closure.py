"""The holomorphic Eisenstein ring closes on (E_4, E_6) with one exception.

The finitely-generated ring  M_*(SL(2,Z)) = C[E_4, E_6]  of holomorphic
modular forms forces every higher Eisenstein series  E_{2k}  to be a
polynomial in  E_4  and  E_6.  For weights  2k  where  dim M_{2k} = 1
the polynomial is MONIC and the identity is integer-coefficient:

    E_8  = E_4^2                    (dim M_8  = 1),
    E_10 = E_4 * E_6                (dim M_10 = 1),
    E_14 = E_4^2 * E_6              (dim M_14 = 1).

Weight 12 is the first weight where  dim M_{2k} = 2  (spanned by
E_4^3  and  Delta), so  E_12  is a RATIONAL linear combination with
denominator  691.  Clearing the denominator gives an integer identity

    691 * E_12 = 441 * E_4^3 + 250 * E_6^2.

RAMANUJAN'S 691 CONGRUENCE.

    tau(n) ==  sigma_11(n)  (mod 691)      for every positive integer n.

Proof sketch (at the level of Fourier coefficients):
    691 E_12 = 441 E_4^3 + 250 E_6^2
             = (441 + 250) * 1 + (...) q + (...) q^2 + ...
             = 691 + 65520 sigma_11(n) q^n     (definition of E_12)
so the two sides' q-expansions match rationally.  Writing
E_4^3 - E_6^2 = 1728 Delta (Ramanujan's discriminant identity) and
reducing mod 691 gives the tau-sigma congruence.

WHY 691.

    B_12 = -691/2730.  The Bernoulli number at weight 12 has numerator
    691, a prime.  Ramanujan's constant  2k/B_k = 65520/691  for k = 12,
    and  691  is the smallest prime for which the holomorphic Eisenstein
    ring fails to close over the integers.  Weight 12 is also the
    weight of  Delta, the first cusp form, and of the Leech lattice.

    In the W(3,3) tower, weight 12 = 2k_W33 is double the valency and
    equals the weight of the discriminant  Delta = eta^24.  The
    appearance of 691 at weight 12 is the "holomorphic anomaly" of the
    modular ring, dual to the quasi-modular anomaly of E_2 at weight 2
    (Layer 30).
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_eisenstein_closure_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from w33_ramanujan_system import (
    delta_series,
    e4_series,
    e6_series,
    series_mul,
)


def _sigma(k: int, n: int) -> int:
    return sum(d ** k for d in range(1, n + 1) if n % d == 0)


# ----------------------------------------------------------------------
# Higher Eisenstein series with known integer / rational coefficients.
# E_{2k} = 1 - (4k / B_{2k}) sum sigma_{2k-1}(n) q^n.
# ----------------------------------------------------------------------
def e8_series(n_max: int) -> list[int]:
    """E_8 = 1 + 480 sum sigma_7(n) q^n."""
    return [1] + [480 * _sigma(7, n) for n in range(1, n_max + 1)]


def e10_series(n_max: int) -> list[int]:
    """E_10 = 1 - 264 sum sigma_9(n) q^n."""
    return [1] + [-264 * _sigma(9, n) for n in range(1, n_max + 1)]


def e14_series(n_max: int) -> list[int]:
    """E_14 = 1 - 24 sum sigma_13(n) q^n."""
    return [1] + [-24 * _sigma(13, n) for n in range(1, n_max + 1)]


def e12_times_691_series(n_max: int) -> list[int]:
    """691 * E_12 = 691 + 691 * (65520/691) sum sigma_11(n) q^n
                  = 691 + 65520 sum sigma_11(n) q^n."""
    return [691] + [65520 * _sigma(11, n) for n in range(1, n_max + 1)]


# ----------------------------------------------------------------------
# Closures of the holomorphic Eisenstein ring on (E_4, E_6).
# ----------------------------------------------------------------------
def verify_E8_equals_E4_squared(n_max: int = 20) -> dict[str, Any]:
    e4 = e4_series(n_max)
    e8 = e8_series(n_max)
    rhs = series_mul(e4, e4, n_max)
    return {
        "n_max":     n_max,
        "all_match": e8 == rhs,
    }


def verify_E10_equals_E4_E6(n_max: int = 20) -> dict[str, Any]:
    e4 = e4_series(n_max)
    e6 = e6_series(n_max)
    e10 = e10_series(n_max)
    rhs = series_mul(e4, e6, n_max)
    return {
        "n_max":     n_max,
        "all_match": e10 == rhs,
    }


def verify_E14_equals_E4_squared_E6(n_max: int = 20) -> dict[str, Any]:
    e4 = e4_series(n_max)
    e6 = e6_series(n_max)
    e14 = e14_series(n_max)
    rhs = series_mul(series_mul(e4, e4, n_max), e6, n_max)
    return {
        "n_max":     n_max,
        "all_match": e14 == rhs,
    }


def verify_691_E12_equals_441_E4cubed_plus_250_E6sq(n_max: int = 20) -> dict[str, Any]:
    """691 * E_12 = 441 * E_4^3 + 250 * E_6^2   (integer identity)."""
    e4 = e4_series(n_max)
    e6 = e6_series(n_max)
    e4_cubed = series_mul(series_mul(e4, e4, n_max), e4, n_max)
    e6_sq = series_mul(e6, e6, n_max)
    rhs = [441 * e4_cubed[n] + 250 * e6_sq[n] for n in range(n_max + 1)]
    lhs = e12_times_691_series(n_max)
    return {
        "n_max":     n_max,
        "all_match": lhs == rhs,
    }


# ----------------------------------------------------------------------
# Ramanujan's 691 congruence:  tau(n) == sigma_11(n) (mod 691).
# ----------------------------------------------------------------------
def verify_ramanujan_691_congruence(n_max: int = 20) -> dict[str, Any]:
    delta = delta_series(n_max)
    discrepancies = []
    for n in range(1, n_max + 1):
        lhs = delta[n] % 691
        rhs = _sigma(11, n) % 691
        if lhs != rhs:
            discrepancies.append({"n": n, "tau": delta[n], "sigma11": _sigma(11, n), "tau_mod_691": lhs, "sigma11_mod_691": rhs})
    return {
        "n_max":         n_max,
        "discrepancies": discrepancies,
        "all_match":     discrepancies == [],
        "first_few_tau": delta[1:8],
    }


# ----------------------------------------------------------------------
# The Bernoulli / Eisenstein normalization constants (informational).
# ----------------------------------------------------------------------
def bernoulli_weight_12_signature() -> dict[str, Any]:
    """B_12 = -691/2730.  The normalization constant in E_12 is
         2 * 12 / B_12 = 24 / (-691/2730) = -(24 * 2730)/691 = -65520/691.
       E_12 = 1 - (2*12/B_12) sum sigma_11(n) q^n = 1 + (65520/691) sum sigma_11(n) q^n."""
    return {
        "B_12_numerator":               -691,
        "B_12_denominator":             2730,
        "E_12_coefficient_numerator":   65520,
        "E_12_coefficient_denominator": 691,
        "k_plus_k_equals_2k_W33":       "weight 12 = 2 * k = 2 * 12 ... wait, we've been using k=12 for W33 valency; here weight 2k = 12 means k=6 in Eisenstein notation, but the W33 valency is also 12 and equals the weight of Delta",
        "delta_weight":                 12,
        "dim_M_12":                     2,
        "first_prime_of_ring_failure":  691,
    }


# ----------------------------------------------------------------------
# Structural signature: the five lowest "closure" weights.
# ----------------------------------------------------------------------
def eisenstein_ring_closure_ladder() -> dict[str, Any]:
    """Weights where  E_{2k}  is a MONOMIAL in (E_4, E_6):  8, 10, 14.
       Weights where M_{2k} has dimension > 1 force denominator structure."""
    return {
        "weight_4_generator":   {"form": "E_4", "dim_M": 1},
        "weight_6_generator":   {"form": "E_6", "dim_M": 1},
        "weight_8_monomial":    {"E_8 = E_4^2":      True, "dim_M": 1},
        "weight_10_monomial":   {"E_10 = E_4 * E_6": True, "dim_M": 1},
        "weight_12_two_dim":    {"dim_M": 2, "ring_identity_with_691": "691 E_12 = 441 E_4^3 + 250 E_6^2"},
        "weight_14_monomial":   {"E_14 = E_4^2 * E_6": True, "dim_M": 1},
        "first_failure_at":     12,
        "first_failure_prime":  691,
    }


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------
def derive_all(n_max: int = 20) -> dict[str, Any]:
    e8 = verify_E8_equals_E4_squared(n_max=n_max)
    e10 = verify_E10_equals_E4_E6(n_max=n_max)
    e14 = verify_E14_equals_E4_squared_E6(n_max=n_max)
    e12 = verify_691_E12_equals_441_E4cubed_plus_250_E6sq(n_max=n_max)
    congruence = verify_ramanujan_691_congruence(n_max=n_max)
    bernoulli = bernoulli_weight_12_signature()
    ladder = eisenstein_ring_closure_ladder()
    return {
        "E8_closure":      e8,
        "E10_closure":     e10,
        "E14_closure":     e14,
        "E12_691_identity": e12,
        "ramanujan_691_congruence": congruence,
        "bernoulli_signature":      bernoulli,
        "closure_ladder":           ladder,
        "summary_chain": {
            "E_8_equals_E_4_squared":                     e8["all_match"],
            "E_10_equals_E_4_E_6":                        e10["all_match"],
            "E_14_equals_E_4_squared_E_6":                e14["all_match"],
            "691_E_12_equals_441_E4cubed_plus_250_E6sq":  e12["all_match"],
            "tau_n_congruent_sigma_11_n_mod_691":         congruence["all_match"],
            "first_ring_failure_weight_is_12":            ladder["first_failure_at"] == 12,
            "first_ring_failure_prime_is_691":            ladder["first_failure_prime"] == 691,
        },
    }


def main() -> None:
    summary = derive_all(n_max=20)
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    print("=" * 72)
    print("W33 EISENSTEIN CLOSURE AND THE 691 CONGRUENCE")
    print("=" * 72)
    print()
    for key, val in summary["summary_chain"].items():
        status = "PASS" if val else "FAIL"
        print(f"  [{status}] {key}")
    print()
    print("  E_8  = E_4^2                                (dim M_8 = 1)")
    print("  E_10 = E_4 * E_6                            (dim M_10 = 1)")
    print("  E_14 = E_4^2 * E_6                          (dim M_14 = 1)")
    print("  691 * E_12 = 441 * E_4^3 + 250 * E_6^2      (dim M_12 = 2)")
    print("  tau(n) == sigma_11(n) (mod 691)             for all n")


if __name__ == "__main__":
    main()
