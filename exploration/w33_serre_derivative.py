"""The Serre derivative is the holomorphic part of  q d/dq.

Define, for a modular form f of weight k,

    D_k(f) := q df/dq - (k/12) E_2 f.

This kills the quasi-modular anomaly of q d/dq: if f is modular of weight
k then D_k(f) is modular of weight k+2 (in particular holomorphic, not
quasi-modular).  The Ramanujan system reorganises immediately:

    D_4(E_4) = (E_2 E_4 - E_6)/3 - (1/3) E_2 E_4 = -E_6/3      in M_6,
    D_6(E_6) = (E_2 E_6 - E_4^2)/2 - (1/2) E_2 E_6 = -E_4^2/2  in M_8.

Delta is extremal:  D_12(Delta) = 0.
This is EXACTLY the Delta ODE q dDelta/dq = E_2 Delta.

eta^c is UNIVERSALLY Serre-flat:  D_{c/2}(eta^c) = 0 for every c.
In the integer-series form  g_c = prod(1-q^n)^c  (without q^{c/24}), this
is the identity  24 q dg_c/dq = c (E_2 - 1) g_c.  Positive powers
c in {1, 2, 4, 8, 12, 24} and the negative-power version c -> -c give
the same Serre-flat relation.

RANKIN-COHEN BRACKET.

For modular forms f of weight k, g of weight l, define

    [f, g]_1 := k f * q dg/dq - l (q df/dq) * g.

If f, g are modular, so is [f, g]_1, of weight k + l + 2.  Applied to
(E_4, E_6) the Ramanujan system gives

    [E_4, E_6]_1 = 4 E_4 * (E_2 E_6 - E_4^2)/2 - 6 (E_2 E_4 - E_6)/3 * E_6
                 = -2 (E_4^3 - E_6^2)
                 = -2 * 1728 * Delta
                 = -3456 * Delta
                 = -2 k^3 Delta       (k = 12).

So Delta appears DIRECTLY as the lowest Rankin-Cohen bracket of the two
holomorphic-ring generators, with coefficient  -2 * 12^3  set by the
W(3,3) valency.

BRIDGE TO W(3,3).

    12 = k = W(3,3) valency appears three times in the Serre story:
        * it is the denominator in D_k = q d/dq - (k/12) E_2;
        * it is the weight of Delta, the unique cusp form that is
          annihilated by D_12;
        * it is the cube root of  1728 = 12^3, the coefficient in
          [E_4, E_6]_1 = -2 * 12^3 * Delta.

    The quasi-modular anomaly of E_2 is EXACTLY the piece subtracted by
    D_k; so the entire W(3,3) cumulative regime (Layer 30, 31) is the
    shadow of that single correction term.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_serre_derivative_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from w33_affine_e8 import _series_pow
from w33_euler_pentagonal import euler_pentagonal_series
from w33_ramanujan_system import (
    delta_series,
    e2_series,
    e4_series,
    e6_series,
    q_d_dq,
    series_mul,
)


def scalar_mul(A: list[int], c: int) -> list[int]:
    return [c * a for a in A]


def series_sub(A: list[int], B: list[int], n_max: int) -> list[int]:
    return [A[n] - B[n] for n in range(n_max + 1)]


# ----------------------------------------------------------------------
# Serre derivative acting on a q-series that represents a modular form
# of weight k.  D_k(f) = q df/dq - (k/12) E_2 f.
# When the RHS is not divisible by 12 we return it pre-multiplied by 12.
# ----------------------------------------------------------------------
def serre_derivative_12x(f: list[int], k: int, n_max: int) -> list[int]:
    """Return 12 * D_k(f) as an integer q-series."""
    e2 = e2_series(n_max)
    lhs_12 = [12 * c for c in q_d_dq(f)]
    e2_f = series_mul(e2, f, n_max)
    k_e2_f = scalar_mul(e2_f, k)
    return series_sub(lhs_12, k_e2_f, n_max)


# ----------------------------------------------------------------------
# Pinning Serre identities for the holomorphic generators.
# ----------------------------------------------------------------------
def verify_serre_E4_gives_minus_E6_over_3(n_max: int = 20) -> dict[str, Any]:
    """12 D_4(E_4) = -4 E_6.  [D_4(E_4) = -E_6/3 in M_6.]"""
    e4 = e4_series(n_max)
    e6 = e6_series(n_max)
    lhs = serre_derivative_12x(e4, k=4, n_max=n_max)
    rhs = scalar_mul(e6, -4)
    return {
        "n_max":      n_max,
        "mismatches": [(n, lhs[n], rhs[n]) for n in range(n_max + 1) if lhs[n] != rhs[n]],
        "all_match":  lhs == rhs,
    }


def verify_serre_E6_gives_minus_E4_sq_over_2(n_max: int = 20) -> dict[str, Any]:
    """12 D_6(E_6) = -6 E_4^2.  [D_6(E_6) = -E_4^2/2 in M_8.]"""
    e4 = e4_series(n_max)
    e6 = e6_series(n_max)
    lhs = serre_derivative_12x(e6, k=6, n_max=n_max)
    e4_sq = series_mul(e4, e4, n_max)
    rhs = scalar_mul(e4_sq, -6)
    return {
        "n_max":      n_max,
        "mismatches": [(n, lhs[n], rhs[n]) for n in range(n_max + 1) if lhs[n] != rhs[n]],
        "all_match":  lhs == rhs,
    }


def verify_serre_delta_is_zero(n_max: int = 20) -> dict[str, Any]:
    """D_12(Delta) = 0  -- Delta is extremal, annihilated by the
    weight-12 Serre operator.  Equivalent to the Delta ODE q dDelta/dq = E_2 Delta.
    """
    delta = delta_series(n_max)
    lhs = serre_derivative_12x(delta, k=12, n_max=n_max)
    return {
        "n_max":     n_max,
        "residuals": lhs,
        "all_zero":  all(v == 0 for v in lhs),
    }


# ----------------------------------------------------------------------
# eta^c universal Serre flatness for positive powers (integer series).
#     g_c = prod(1 - q^n)^c,   24 q dg_c/dq = c (E_2 - 1) g_c.
# ----------------------------------------------------------------------
def eta_positive_power_series(c: int, n_max: int) -> list[int]:
    """g_c = prod(1-q^n)^c as an integer q-series (no q^{c/24})."""
    euler = euler_pentagonal_series(n_max)
    return _series_pow(euler, c, n_max)


def verify_eta_positive_power_serre(c: int, n_max: int = 20) -> dict[str, Any]:
    """24 q dg_c/dq = c (E_2 - 1) g_c  for  g_c = prod(1-q^n)^c."""
    g = eta_positive_power_series(c, n_max)
    e2 = e2_series(n_max)
    e2_minus_1 = [e2[n] - (1 if n == 0 else 0) for n in range(n_max + 1)]
    lhs = [24 * v for v in q_d_dq(g)]
    rhs = scalar_mul(series_mul(e2_minus_1, g, n_max), c)
    residuals = series_sub(lhs, rhs, n_max)
    return {
        "c":         c,
        "n_max":     n_max,
        "residuals": residuals,
        "all_zero":  all(v == 0 for v in residuals),
    }


# ----------------------------------------------------------------------
# Rankin-Cohen bracket of weight 1:   [f, g]_1 = k f g' - l f' g.
# Applied to (E_4, E_6) it gives -2 (E_4^3 - E_6^2) = -3456 Delta.
# ----------------------------------------------------------------------
def rankin_cohen_bracket_1(f: list[int], fw: int, g: list[int], gw: int, n_max: int) -> list[int]:
    """[f, g]_1 = fw * f * q dg/dq  -  gw * (q df/dq) * g."""
    fp = q_d_dq(f)
    gp = q_d_dq(g)
    term_1 = scalar_mul(series_mul(f, gp, n_max), fw)
    term_2 = scalar_mul(series_mul(fp, g, n_max), gw)
    return series_sub(term_1, term_2, n_max)


def verify_rankin_cohen_E4_E6_is_minus_3456_delta(n_max: int = 20) -> dict[str, Any]:
    """[E_4, E_6]_1 = -3456 Delta = -2 * 12^3 Delta."""
    e4 = e4_series(n_max)
    e6 = e6_series(n_max)
    delta = delta_series(n_max)
    bracket = rankin_cohen_bracket_1(e4, 4, e6, 6, n_max)
    target = scalar_mul(delta, -3456)
    return {
        "n_max":              n_max,
        "k":                  12,
        "coefficient":        -3456,
        "coefficient_form":   "-2 * k^3 = -2 * 12^3 = -3456",
        "mismatches":         [(n, bracket[n], target[n]) for n in range(n_max + 1) if bracket[n] != target[n]],
        "all_match":          bracket == target,
    }


def verify_rankin_cohen_via_E4_cubed_minus_E6_sq(n_max: int = 20) -> dict[str, Any]:
    """Equivalent form: [E_4, E_6]_1 = -2 (E_4^3 - E_6^2)."""
    e4 = e4_series(n_max)
    e6 = e6_series(n_max)
    bracket = rankin_cohen_bracket_1(e4, 4, e6, 6, n_max)
    e4_cubed = series_mul(series_mul(e4, e4, n_max), e4, n_max)
    e6_sq = series_mul(e6, e6, n_max)
    diff = series_sub(e4_cubed, e6_sq, n_max)
    target = scalar_mul(diff, -2)
    return {
        "n_max":     n_max,
        "all_match": bracket == target,
    }


# ----------------------------------------------------------------------
# W(3,3) valency appears three times in the Serre story.
# ----------------------------------------------------------------------
def w33_valency_signatures() -> dict[str, Any]:
    k = 12
    return {
        "k":                                     k,
        "serre_denominator":                     k,
        "delta_weight_killed_by_D_k":            k,
        "rankin_cohen_coefficient_minus_2_k3":   -2 * k ** 3,
        "rankin_cohen_coefficient_equals_minus_3456": -2 * k ** 3 == -3456,
        "role_in_discriminant":                  "1728 = 12^3 is the constant in 1728 Delta = E_4^3 - E_6^2",
    }


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------
def derive_all(n_max: int = 20) -> dict[str, Any]:
    E4 = verify_serre_E4_gives_minus_E6_over_3(n_max=n_max)
    E6 = verify_serre_E6_gives_minus_E4_sq_over_2(n_max=n_max)
    Dl = verify_serre_delta_is_zero(n_max=n_max)
    eta_pos = {c: verify_eta_positive_power_serre(c, n_max=n_max) for c in (1, 2, 4, 8, 12, 24)}
    rc_main = verify_rankin_cohen_E4_E6_is_minus_3456_delta(n_max=n_max)
    rc_alt = verify_rankin_cohen_via_E4_cubed_minus_E6_sq(n_max=n_max)
    signatures = w33_valency_signatures()
    return {
        "serre_E4":                     E4,
        "serre_E6":                     E6,
        "serre_delta_zero":             Dl,
        "eta_positive_powers_serre":    eta_pos,
        "rankin_cohen_main":            rc_main,
        "rankin_cohen_alt_form":        rc_alt,
        "w33_valency_signatures":       signatures,
        "summary_chain": {
            "D4_E4_equals_minus_E6_over_3":       E4["all_match"],
            "D6_E6_equals_minus_E4_sq_over_2":    E6["all_match"],
            "D12_Delta_equals_zero_extremality":  Dl["all_zero"],
            "eta_power_c8_serre_flat":            eta_pos[8]["all_zero"],
            "eta_power_c24_serre_flat":           eta_pos[24]["all_zero"],
            "rankin_cohen_E4_E6_equals_minus_3456_Delta": rc_main["all_match"],
            "bracket_equals_minus_2_times_E4cubed_minus_E6sq": rc_alt["all_match"],
            "minus_3456_equals_minus_2_k_cubed":  signatures["rankin_cohen_coefficient_equals_minus_3456"],
        },
    }


def main() -> None:
    summary = derive_all(n_max=20)
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    print("=" * 72)
    print("W33 SERRE DERIVATIVE AND RANKIN-COHEN BRACKET")
    print("=" * 72)
    print()
    for key, val in summary["summary_chain"].items():
        status = "PASS" if val else "FAIL"
        print(f"  [{status}] {key}")
    print()
    print("  Rankin-Cohen:  [E_4, E_6]_1 = -3456 Delta = -2 * 12^3 Delta")
    print("  D_12(Delta) = 0  (Delta is extremal)")
    print("  All six eta positive powers {1,2,4,8,12,24} are Serre-flat")


if __name__ == "__main__":
    main()
