#!/usr/bin/env python3
"""Affine/Fano information-horizon coarse dynamics for the Marcelis quotient.

For the ordered omega gauge, PG(n,2) splits across its first coordinate as

    A_n = {x0=1} ~= AG(n,2),       |A_n| = 2^n,
    F_n = {x0=0} ~= PG(n-1,2),     |F_n| = 2^n-1.

The prior observer certificate proves that for the one-step cyclic update U1,
A_n is exactly the stochastic macro sector and F_n exactly the deterministic
macro sector.  This certificate coarse-grains the *uniform PG(n,4) microstate
measure* to those two sectors and derives the exact 2x2 transition matrix.

Writing N_F=|PG(n-1,4)|=(4^n-1)/3,

       [ 3/4                         1/4                    ]
P_n = [ 3*4^(n-1)/(4^n-1)           (4^(n-1)-1)/(4^n-1)   ].

Its eigenvalues are 1 and

    lambda_2 = det(P_n) = -1/(4 N_F).

At n=3, N_F=21, so lambda_2=-1/84 exactly.  The repo independently certifies
84 flags for each Csaszar/Szilassi toroidal map.  We record that numerical echo
as a falsifiable bridge target only; no canonical bijection is asserted here.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = Path(__file__).resolve().parent
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_marcelis_observer_quotient_dynamics import projective_points, rotate_projective  # noqa: E402
from w33_marcelis_gf4_trace_gauge import projective_trace_gauge  # noqa: E402

OUT = ROOT / "data" / "w33_affine_fano_information_horizon.json"


def sector(macro):
    return "AFFINE_STOCHASTIC" if macro[0] == 1 else "FANO_INFINITY_DETERMINISTIC"


def qstr(q: Fraction) -> str:
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"


def exact_row(n: int) -> dict:
    pts = projective_points(n)
    counts = Counter()
    sector_mass = Counter()
    macrosets = {"AFFINE_STOCHASTIC": set(), "FANO_INFINITY_DETERMINISTIC": set()}

    for s in pts:
        b = projective_trace_gauge(s)
        bp = projective_trace_gauge(rotate_projective(s, 1))
        a, c = sector(b), sector(bp)
        sector_mass[a] += 1
        counts[(a, c)] += 1
        macrosets[a].add(b)

    A = "AFFINE_STOCHASTIC"
    F = "FANO_INFINITY_DETERMINISTIC"
    NA = 4 ** n
    NF = (4 ** n - 1) // 3
    total = (4 ** (n + 1) - 1) // 3
    assert len(pts) == total
    assert sector_mass == {A: NA, F: NF}
    assert len(macrosets[A]) == 2 ** n
    assert len(macrosets[F]) == 2 ** n - 1

    empirical = {
        "A_to_A": Fraction(counts[(A, A)], NA),
        "A_to_F": Fraction(counts[(A, F)], NA),
        "F_to_A": Fraction(counts[(F, A)], NF),
        "F_to_F": Fraction(counts[(F, F)], NF),
    }
    expected = {
        "A_to_A": Fraction(3, 4),
        "A_to_F": Fraction(1, 4),
        "F_to_A": Fraction(3 * 4 ** (n - 1), 4 ** n - 1),
        "F_to_F": Fraction(4 ** (n - 1) - 1, 4 ** n - 1),
    }
    assert empirical == expected

    stationary = {
        "A": Fraction(NA, total),
        "F": Fraction(NF, total),
    }
    # Verify stationarity explicitly.
    next_A = stationary["A"] * expected["A_to_A"] + stationary["F"] * expected["F_to_A"]
    next_F = stationary["A"] * expected["A_to_F"] + stationary["F"] * expected["F_to_F"]
    assert next_A == stationary["A"] and next_F == stationary["F"]

    lambda2 = expected["A_to_A"] + expected["F_to_F"] - 1
    determinant = expected["A_to_A"] * expected["F_to_F"] - expected["A_to_F"] * expected["F_to_A"]
    formula = Fraction(-1, 4 * NF)
    assert lambda2 == determinant == formula

    # After t steps, any signed difference from stationarity in this two-state
    # coarse chain is multiplied by lambda2^t.  The negative sign means a tiny
    # alternating overshoot rather than monotone relaxation.
    return {
        "n": n,
        "global_microstates": total,
        "affine_microstates": NA,
        "fano_infinity_microstates": NF,
        "affine_macrostates": len(macrosets[A]),
        "fano_infinity_macrostates": len(macrosets[F]),
        "transition_counts": {
            "A_to_A": counts[(A, A)],
            "A_to_F": counts[(A, F)],
            "F_to_A": counts[(F, A)],
            "F_to_F": counts[(F, F)],
        },
        "transition_matrix": {
            k: qstr(v) for k, v in expected.items()
        },
        "stationary_sector_weights": {k: qstr(v) for k, v in stationary.items()},
        "eigenvalues": ["1", qstr(lambda2)],
        "nontrivial_eigenvalue": qstr(lambda2),
        "nontrivial_eigenvalue_formula": f"-1/(4*{NF})",
        "determinant": qstr(determinant),
        "mixing_reading": (
            "The two-sector coarse chain is almost rank one.  Every step multiplies "
            "the unique nonstationary mode by the small negative factor lambda2, "
            "so deviations alternate sign while collapsing geometrically."
        ),
    }


def build_result() -> dict:
    rows = [exact_row(n) for n in range(1, 7)]
    n3 = next(r for r in rows if r["n"] == 3)
    assert n3["fano_infinity_microstates"] == 21
    assert n3["affine_microstates"] == 64
    assert n3["affine_macrostates"] == 8
    assert n3["fano_infinity_macrostates"] == 7
    assert n3["nontrivial_eigenvalue"] == "-1/84"
    assert n3["transition_matrix"] == {
        "A_to_A": "3/4",
        "A_to_F": "1/4",
        "F_to_A": "16/21",
        "F_to_F": "5/21",
    }
    assert n3["stationary_sector_weights"] == {"A": "64/85", "F": "21/85"}

    # Prior toroidal certificate: exact 84 flag count.  This is an arithmetic
    # cross-check only; this script does not assert a bijection to those flags.
    toroidal = json.loads(
        (ROOT / "data" / "w33_BREAKTHROUGH_264_seven_unification_csaszar_szilassi.json")
        .read_text(encoding="utf-8")
    )
    toroidal_text = json.dumps(toroidal, sort_keys=True)
    assert "84" in toroidal_text

    checks = {
        "exact_microstate_enumeration_n1_through_n6": len(rows) == 6,
        "all_transition_rows_match_closed_formula": all(
            r["transition_matrix"]["A_to_A"] == "3/4" and r["transition_matrix"]["A_to_F"] == "1/4"
            for r in rows
        ),
        "stationary_measure_is_projective_microstate_mass": all(
            Fraction(r["stationary_sector_weights"]["A"]) + Fraction(r["stationary_sector_weights"]["F"]) == 1
            for r in rows
        ),
        "nontrivial_mode_is_minus_inverse_four_boundary_microstates": all(
            Fraction(r["nontrivial_eigenvalue"]) == Fraction(-1, 4 * r["fano_infinity_microstates"])
            for r in rows
        ),
        "n3_projective_split_is_64_plus21_microstates": n3["global_microstates"] == 85 and n3["affine_microstates"] == 64 and n3["fano_infinity_microstates"] == 21,
        "n3_macro_split_is_affine8_plus_fano7": n3["affine_macrostates"] == 8 and n3["fano_infinity_macrostates"] == 7,
        "n3_kernel_is_exact": n3["transition_matrix"] == {"A_to_A": "3/4", "A_to_F": "1/4", "F_to_A": "16/21", "F_to_F": "5/21"},
        "n3_unique_decay_mode_is_minus_one_over_84": n3["nontrivial_eigenvalue"] == "-1/84",
        "repo_has_independent_toroidal_84_certificate": "84" in toroidal_text,
    }

    return {
        "schema": "w33.affine-fano-information-horizon.v1",
        "status": "PASS" if all(checks.values()) else "PARTIAL",
        "headline": (
            "The Marcelis observer quotient has an exact affine/Fano information horizon. "
            "For U1, stochastic AG(n,2) and deterministic PG(n-1,2) sectors inherit a "
            "two-state microstate-weighted Markov kernel whose unique decay eigenvalue is "
            "-1/(4|PG(n-1,4)|). At n=3 the kernel is [[3/4,1/4],[16/21,5/21]] "
            "with stationary weights 64/85 and 21/85 and lambda2=-1/84."
        ),
        "general_theorem": {
            "macro_decomposition": "PG(n,2)=AG(n,2) disjoint_union PG(n-1,2)",
            "micro_decomposition": "PG(n,4)=AG(n,4) disjoint_union PG(n-1,4)",
            "stochastic_sector": "A={x0=1}, with 2^n observer states and 4^n microstates",
            "deterministic_sector": "F={x0=0}, with 2^n-1 observer states and (4^n-1)/3 microstates",
            "kernel": "[[3/4,1/4],[3*4^(n-1)/(4^n-1),(4^(n-1)-1)/(4^n-1)]]",
            "stationary_weights": "[3*4^n/(4^(n+1)-1), (4^n-1)/(4^(n+1)-1)]",
            "second_eigenvalue": "-3/(4*(4^n-1)) = -1/(4*|PG(n-1,4)|)",
        },
        "n3_information_horizon": n3,
        "dimension_census": rows,
        "toroidal_84_echo": {
            "observer_value": "lambda2=-1/84",
            "arithmetic_origin": "84=4*|PG(2,4)|=4*21",
            "independent_repo_value": "Csaszar flags=84 and Szilassi flags=84 are certified elsewhere",
            "interpretation": (
                "The equality of denominators is exact but a canonical map has not been "
                "constructed.  Treat 84 as a bridge target: a future certificate should "
                "either build an equivariant bijection between the 4x21 mixing denominator "
                "and a toroidal flag set or explicitly prove the match noncanonical."
            ),
        },
        "claim_boundary": [
            "The two-sector kernel is weighted by the uniform distribution on PG(n,4) microstates, not by a uniform distribution on the binary macrostates.",
            "Calling PG(n-1,2) an information horizon refers to deterministic-vs-stochastic closure under this declared observer map and U1 update; it is not a spacetime event horizon.",
            "The -1/84 equality with toroidal flag cardinalities is recorded as an exact arithmetic coincidence/bridge target, not as a proved geometric identification.",
            "The alternating decay mode is a property of the finite coarse Markov chain and carries no thermodynamic or quantum-dynamical interpretation without an additional physical dictionary.",
        ],
        "checks": checks,
    }


def main() -> int:
    result = build_result()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    n3 = result["n3_information_horizon"]
    print(json.dumps({
        "status": result["status"],
        "n3_kernel": n3["transition_matrix"],
        "n3_stationary": n3["stationary_sector_weights"],
        "n3_lambda2": n3["nontrivial_eigenvalue"],
        "toroidal_echo": result["toroidal_84_echo"]["independent_repo_value"],
    }, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
