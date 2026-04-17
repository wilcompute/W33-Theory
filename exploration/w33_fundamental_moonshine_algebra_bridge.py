"""The fundamental moonshine classes close on one linear/quadratic algebra spine.

The class 1A is already fixed by the weight-12 quotient algebra:

    j = Theta_Leech / Delta + 720,
    J = j - 744 = Theta_Leech / Delta - 24,
    196884 = 196560 + 324.

For the five prime Monster classes

    pA,   p in {2, 3, 5, 7, 13},

the McKay-Thompson Hauptmodul is the Atkin-Lehner trace of one eta-quotient
unit

    X_p := (eta(tau) / eta(p tau))^k,     k = 24 / (p - 1),
    Y_p := p^{k/2} (eta(p tau) / eta(tau))^k,

so that

    T_pA = X_p + k + Y_p,
    X_p Y_p = p^{k/2}.

Hence each prime Hauptmodul closes as a quadratic algebra:

    X_p^2 - (T_pA - k) X_p + p^{k/2} = 0.

So the six fundamental classes

    1A, 2A, 3A, 5A, 7A, 13A

are not six disconnected modular facts.  They sit on one algebraic spine:

    1A  = linear weight-12 quotient algebra,
    pA  = quadratic genus-zero trace/norm algebra.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_fundamental_moonshine_algebra_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from w33_mckay_thompson_eta_quotients import (
    ETA_QUOTIENT_PARAMS,
    dual_eta_quotient,
    eta_quotient_laurent,
    mckay_thompson_T_pA,
)
from w33_modular_curve_genera import GENUS_PLUS_TABLE
from w33_weight12_moonshine_gap_bridge import build_summary as build_weight12_summary


def _laurent_to_dict(coeffs: list[Fraction | int], start_exp: int) -> dict[int, Fraction]:
    return {
        start_exp + i: Fraction(c)
        for i, c in enumerate(coeffs)
        if Fraction(c) != 0
    }


def _laurent_add(*series: tuple[dict[int, Fraction], int]) -> dict[int, Fraction]:
    out: dict[int, Fraction] = {}
    for coeffs, scalar in series:
        for exp, coeff in coeffs.items():
            out[exp] = out.get(exp, Fraction(0)) + scalar * coeff
    return {exp: coeff for exp, coeff in out.items() if coeff != 0}


def _laurent_mul(a: dict[int, Fraction], b: dict[int, Fraction], exp_min: int, exp_max: int) -> dict[int, Fraction]:
    out: dict[int, Fraction] = {}
    for ea, ca in a.items():
        for eb, cb in b.items():
            exp = ea + eb
            if exp_min <= exp <= exp_max:
                out[exp] = out.get(exp, Fraction(0)) + ca * cb
    return {exp: coeff for exp, coeff in out.items() if coeff != 0}


def _series_window(series: dict[int, Fraction], exp_min: int, exp_max: int) -> list[int]:
    return [int(series.get(exp, 0)) for exp in range(exp_min, exp_max + 1)]


def _prime_row(p: int, k: int, n_terms: int = 6) -> dict[str, Any]:
    x_list = eta_quotient_laurent(p, k, n_terms)
    y_list = dual_eta_quotient(p, k, n_terms)
    t_list, c_p = mckay_thompson_T_pA(p, n_terms)
    norm = p ** (k // 2)

    x = _laurent_to_dict(x_list, -1)
    y = _laurent_to_dict(y_list, 0)
    t = _laurent_to_dict(t_list, -1)

    t_minus_k = dict(t)
    t_minus_k[0] = t_minus_k.get(0, Fraction(0)) - Fraction(k)
    if t_minus_k[0] == 0:
        del t_minus_k[0]

    stable_max = n_terms - 1

    xy = _laurent_mul(x, y, 0, stable_max)
    quadratic_residual = _laurent_add(
        (_laurent_mul(x, x, -2, stable_max), 1),
        (_laurent_mul(t_minus_k, x, -2, stable_max), -1),
        ({0: Fraction(norm)}, 1),
    )

    return {
        "p": p,
        "k": k,
        "genus_zero": GENUS_PLUS_TABLE[p] == 0,
        "norm_p_to_k_over_2": norm,
        "hauptmodul_constant_shift": int(c_p),
        "X_p_q_minus_1_to_q5": [int(c) for c in x_list[:7]],
        "Y_p_q0_to_q6": [int(c) for c in y_list[:7]],
        "T_pA_q_minus_1_to_q5": [int(c) for c in t_list[:7]],
        "stable_max_exponent": stable_max,
        "product_X_p_Y_p_q0_to_q5": _series_window(xy, 0, stable_max),
        "quadratic_residual_q_minus_2_to_q5": _series_window(quadratic_residual, -2, stable_max),
        "theorems": {
            "genus_zero_holds": GENUS_PLUS_TABLE[p] == 0,
            "constant_shift_equals_k": int(c_p) == k,
            "trace_identity_holds": _laurent_add((x, 1), (y, 1)) == t_minus_k,
            "norm_identity_holds": xy == {0: Fraction(norm)},
            "quadratic_identity_holds": quadratic_residual == {},
        },
    }


def build_summary(n_terms: int = 6) -> dict[str, Any]:
    one_a = build_weight12_summary()
    prime_rows = [_prime_row(p, k, n_terms=n_terms) for p, k in ETA_QUOTIENT_PARAMS]
    weights = [row["k"] for row in prime_rows]
    norms = [row["norm_p_to_k_over_2"] for row in prime_rows]

    return {
        "fundamental_moonshine_algebra_dictionary": {
            "oneA_linear_quotient": {
                "744_split": one_a["weight12_moonshine_gap_dictionary"]["constant_split_744"],
                "first_moonshine_split": one_a["weight12_moonshine_gap_dictionary"]["first_moonshine_split"],
            },
            "prime_pA_quadratic_rows": prime_rows,
            "prime_weight_ladder": weights,
            "prime_atkin_lehner_norms": norms,
        },
        "fundamental_moonshine_algebra_theorem": {
            "oneA_closes_as_the_weight12_linear_quotient_algebra": all(
                one_a["weight12_moonshine_gap_theorem"].values()
            ),
            "the_five_prime_classes_are_exactly_the_genus_zero_eta_quotient_classes_with_p_minus_1_dividing_24": (
                [row["p"] for row in prime_rows] == [2, 3, 5, 7, 13]
                and all(row["genus_zero"] for row in prime_rows)
                and weights == [24, 12, 6, 4, 2]
            ),
            "each_prime_hauptmodul_is_the_trace_of_an_atkin_lehner_eta_unit": all(
                row["theorems"]["trace_identity_holds"] for row in prime_rows
            ),
            "each_prime_eta_unit_has_exact_norm_p_to_the_k_over_2": all(
                row["theorems"]["norm_identity_holds"] for row in prime_rows
            ),
            "each_prime_hauptmodul_satisfies_the_quadratic_polynomial_X2_minus_TminuskX_plus_norm": all(
                row["theorems"]["quadratic_identity_holds"] for row in prime_rows
            ),
            "the_fundamental_classes_1A_2A_3A_5A_7A_13A_close_on_one_linear_quadratic_moonshine_spine": (
                all(one_a["weight12_moonshine_gap_theorem"].values())
                and all(all(row["theorems"].values()) for row in prime_rows)
            ),
        },
        "interpretation": (
            "The weight-12 line quotient gives the 1A moonshine class, while the "
            "five prime genus-zero classes are the Atkin-Lehner trace algebras of "
            "eta-quotient units. The base moonshine classes therefore close on one "
            "common algebraic spine: linear quotient at level 1, quadratic trace/norm "
            "at prime genus-zero levels."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 FUNDAMENTAL MOONSHINE ALGEBRA BRIDGE")
    print("=" * 72)
    for key, value in summary["fundamental_moonshine_algebra_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
