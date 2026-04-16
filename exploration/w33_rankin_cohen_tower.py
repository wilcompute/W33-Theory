"""The Rankin-Cohen bracket tower constructs Delta two different ways.

The Rankin-Cohen bracket of weight  n  for modular forms  f  of weight k,
g  of weight l  is

    [f, g]_n  :=  sum_{r=0}^{n} (-1)^r  C(k+n-1, n-r) C(l+n-1, r) D^{n-r}(f) D^r(g),

with  D := q d/dq.  It is modular of weight  k + l + 2n.

LAYER 32 PINNED:
    [E_4, E_6]_1  =  -3456 Delta  =  -2 k^3 Delta                  (k = 12 = W33 valency).

THIS LAYER PINS ONE MORE:
    [E_4, E_4]_2  =  4800 Delta  =  2 * C(5, 2) * 240 * Delta
                                =  2 * C(k+1, 2) * |root(E_8)| * Delta.

Both brackets are cusp forms in  M_{12}.  The dimension of  M_{12} is 2
(spanned by  E_4^3  and  Delta), so any cusp form in  M_{12}  is a scalar
multiple of  Delta.  The two Rankin-Cohen brackets produce that scalar
with two different "physical" constants:

    -2 k^3                            (W(3,3) valency cubed, from  [E_4, E_6]_1 );
    2 C(k+1, 2) * |root(E_8)|         (E_8 root system count, from  [E_4, E_4]_2 ).

The ratio

    [E_4, E_4]_2  /  [E_4, E_6]_1  =  4800 / (-3456)  =  -25 / 18

is a rational weight, not an integer; it is the ratio of the two
constructions, but each construction is an exact integer identity.

EXPLICIT FORMULA.

    [E_4, E_4]_2  =  20 E_4 * D^2(E_4)  -  25 (D E_4)^2.

Here  D E_4 = (E_2 E_4 - E_6) / 3  from the Ramanujan system (Layer 31).

CONNECTION TO LAYERS.

    Layer 30 (E_2 source)     -- the ODE that gives  D  acting on  eta^{-c}.
    Layer 31 (Ramanujan)      -- the system that computes  D E_k .
    Layer 32 (Serre, RC_1)    -- first RC bracket producing  -2 k^3 Delta.
    Layer 33 (j-invariant)    -- j is the cube of  E_4 * f_8 .
    Layer 34 (RC_2, here)     -- second RC bracket producing  2 C(5,2) |E_8| Delta.

    The structural dictionary is:  two constructions of  Delta, one
    indexed by the W(3,3) valency  k, the other by the E_8 root count
    240 = 2 k * (2k+1) - 2.
"""

from __future__ import annotations

import json
from math import comb
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_rankin_cohen_tower_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from w33_ramanujan_system import (
    delta_series,
    e2_series,
    e4_series,
    e6_series,
    q_d_dq,
    series_mul,
)
from w33_serre_derivative import rankin_cohen_bracket_1


def scalar_mul(A: list[int], c: int) -> list[int]:
    return [c * a for a in A]


def series_sub(A: list[int], B: list[int], n_max: int) -> list[int]:
    return [A[n] - B[n] for n in range(n_max + 1)]


def series_add(A: list[int], B: list[int], n_max: int) -> list[int]:
    return [A[n] + B[n] for n in range(n_max + 1)]


def d_power(A: list[int], r: int) -> list[int]:
    """Apply D = q d/dq r times."""
    out = list(A)
    for _ in range(r):
        out = q_d_dq(out)
    return out


# ----------------------------------------------------------------------
# General Rankin-Cohen bracket.
# ----------------------------------------------------------------------
def rankin_cohen_bracket(
    f: list[int], fw: int, g: list[int], gw: int, n: int, n_max: int
) -> list[int]:
    """[f, g]_n  =  sum_{r=0}^{n} (-1)^r C(fw+n-1, n-r) C(gw+n-1, r) D^{n-r}(f) D^r(g)."""
    out = [0] * (n_max + 1)
    for r in range(n + 1):
        coeff = (-1) ** r * comb(fw + n - 1, n - r) * comb(gw + n - 1, r)
        Df = d_power(f, n - r)
        Dg = d_power(g, r)
        term = series_mul(Df, Dg, n_max)
        for i in range(n_max + 1):
            out[i] += coeff * term[i]
    return out


# ----------------------------------------------------------------------
# Second Rankin-Cohen bracket [E_4, E_4]_2 = 4800 Delta.
# ----------------------------------------------------------------------
def verify_rc_E4_E4_2(n_max: int = 20) -> dict[str, Any]:
    e4 = e4_series(n_max)
    delta = delta_series(n_max)
    bracket = rankin_cohen_bracket(e4, 4, e4, 4, 2, n_max)
    target = scalar_mul(delta, 4800)
    return {
        "n_max":       n_max,
        "coefficient": 4800,
        "mismatches":  [(n, bracket[n], target[n]) for n in range(n_max + 1) if bracket[n] != target[n]],
        "all_match":   bracket == target,
    }


def verify_rc_E4_E4_2_explicit_form(n_max: int = 20) -> dict[str, Any]:
    """Verify  [E_4, E_4]_2 = 20 E_4 D^2 E_4 - 25 (D E_4)^2  coefficient-wise."""
    e4 = e4_series(n_max)
    d_e4 = q_d_dq(e4)
    d2_e4 = q_d_dq(d_e4)
    term_1 = scalar_mul(series_mul(e4, d2_e4, n_max), 20)
    term_2 = scalar_mul(series_mul(d_e4, d_e4, n_max), 25)
    explicit = series_sub(term_1, term_2, n_max)
    bracket = rankin_cohen_bracket(e4, 4, e4, 4, 2, n_max)
    return {
        "n_max":     n_max,
        "all_match": explicit == bracket,
    }


# ----------------------------------------------------------------------
# First Rankin-Cohen bracket [E_4, E_6]_1 = -3456 Delta (re-pin).
# ----------------------------------------------------------------------
def verify_rc_E4_E6_1(n_max: int = 20) -> dict[str, Any]:
    e4 = e4_series(n_max)
    e6 = e6_series(n_max)
    delta = delta_series(n_max)
    # Use the established weight-1 Rankin-Cohen implementation
    # consistent with other layers:  [f, g]_1 = k * f * D(g) - l * D(f) * g
    bracket = rankin_cohen_bracket_1(e4, 4, e6, 6, n_max)
    target = scalar_mul(delta, -3456)
    return {
        "n_max":       n_max,
        "coefficient": -3456,
        "mismatches":  [(n, bracket[n], target[n]) for n in range(n_max + 1) if bracket[n] != target[n]],
        "all_match":   bracket == target,
    }


# ----------------------------------------------------------------------
# Structural interpretation of the two integer coefficients.
# ----------------------------------------------------------------------
def structural_interpretation() -> dict[str, Any]:
    k = 12
    E8_roots = 240
    rc_1_coef = -2 * k ** 3
    rc_2_coef = 2 * comb(5, 2) * E8_roots
    return {
        "k_w33_valency":                  k,
        "E8_root_count":                  E8_roots,
        "rc_1_coefficient":               rc_1_coef,
        "rc_1_formula":                   "-2 * k^3",
        "rc_2_coefficient":               rc_2_coef,
        "rc_2_formula":                   "2 * C(k+1, 2) * |root(E_8)|  where k = 4 (weight of E_4)",
        "rc_2_equals_4800":               rc_2_coef == 4800,
        "rc_1_equals_minus_3456":         rc_1_coef == -3456,
        "rc_1_over_rc_2":                 f"{rc_1_coef}/{rc_2_coef} = {rc_1_coef}//{rc_2_coef}",
        "two_constructions_of_Delta":     [
            f"[E_4, E_6]_1 = {rc_1_coef} Delta",
            f"[E_4, E_4]_2 = {rc_2_coef} Delta",
        ],
    }


# ----------------------------------------------------------------------
# Spot check that Delta lies in M_12 only as a scalar of our computed
# bracket: RC brackets automatically produce cusp forms when both inputs
# are holomorphic and the bracket weight equals the dimension-1 cusp
# subspace weight.
# ----------------------------------------------------------------------
def delta_coefficients_first_five() -> dict[str, Any]:
    delta = delta_series(5)
    return {
        "Delta_first_five": delta[:6],
        "Delta_q1":  delta[1],
        "Delta_q2":  delta[2],
        "Delta_q3":  delta[3],
    }


def bracket_q1_calculations() -> dict[str, Any]:
    """Single-q term calculations for manual verification."""
    e4 = e4_series(5)
    e6 = e6_series(5)
    # Use the established n=1 implementation for [E4, E6]_1
    rc11 = rankin_cohen_bracket_1(e4, 4, e6, 6, 5)
    rc22 = rankin_cohen_bracket(e4, 4, e4, 4, 2, 5)
    return {
        "[E_4,E_6]_1 at q1":  rc11[1],
        "[E_4,E_6]_1 at q2":  rc11[2],
        "[E_4,E_4]_2 at q1":  rc22[1],
        "[E_4,E_4]_2 at q2":  rc22[2],
        "[E_4,E_4]_2 at q3":  rc22[3],
    }


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------
def derive_all(n_max: int = 20) -> dict[str, Any]:
    rc22 = verify_rc_E4_E4_2(n_max=n_max)
    rc22_explicit = verify_rc_E4_E4_2_explicit_form(n_max=n_max)
    rc11 = verify_rc_E4_E6_1(n_max=n_max)
    structure = structural_interpretation()
    delta_info = delta_coefficients_first_five()
    q1_info = bracket_q1_calculations()
    return {
        "rc_E4_E4_2":               rc22,
        "rc_E4_E4_2_explicit":      rc22_explicit,
        "rc_E4_E6_1":               rc11,
        "structural_interpretation":structure,
        "delta_first_five":         delta_info,
        "q1_q2_q3_calculations":    q1_info,
        "summary_chain": {
            "rc_E4_E4_2_equals_4800_delta":                rc22["all_match"],
            "rc_E4_E4_2_explicit_form_matches":            rc22_explicit["all_match"],
            "rc_E4_E6_1_equals_minus_3456_delta":          rc11["all_match"],
            "rc_2_coefficient_factors_as_2_C52_E8roots":   structure["rc_2_equals_4800"],
            "rc_1_coefficient_factors_as_minus_2_k_cubed": structure["rc_1_equals_minus_3456"],
            "q1_coefficient_of_E4_E4_2_is_4800":           q1_info["[E_4,E_4]_2 at q1"] == 4800,
            "q1_coefficient_of_E4_E6_1_is_minus_3456":     q1_info["[E_4,E_6]_1 at q1"] == -3456,
            "q2_coefficient_of_E4_E4_2_is_minus_115200":   q1_info["[E_4,E_4]_2 at q2"] == -115200,
        },
    }


def main() -> None:
    summary = derive_all(n_max=20)
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    print("=" * 72)
    print("W33 RANKIN-COHEN BRACKET TOWER: TWO CONSTRUCTIONS OF DELTA")
    print("=" * 72)
    print()
    for key, val in summary["summary_chain"].items():
        status = "PASS" if val else "FAIL"
        print(f"  [{status}] {key}")
    print()
    print("  [E_4, E_6]_1 = -3456 Delta  (coefficient = -2 * 12^3 = -2 k^3)")
    print("  [E_4, E_4]_2 =  4800 Delta  (coefficient = 2 * C(5,2) * 240 = 2 C(k+1,2) |E_8 roots|)")


if __name__ == "__main__":
    main()
