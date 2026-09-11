#!/usr/bin/env python3
"""Projective lag law behind the affine/Fano -1/84 coefficient.

The earlier affine/Fano certificate correctly computed the one-step conditional
matrix between

    A = {x0 != 0}  and  F = {x0 = 0}

for a uniformly sampled point of PG(n,4), but the deterministic cyclic update
U has finite order n+1.  Therefore that 2x2 matrix must not be interpreted as a
Markov transition matrix whose powers describe the actual multistep dynamics.

This certificate gives the exact correction.

For a uniform projective point S in PG(n,4), let X_j indicate whether coordinate
j is nonzero.  Any two distinct coordinates have the same conditional table:

       P(X_j=1 | X_i=1) = 3/4,
       P(X_j=1 | X_i=0) = 3*4^(n-1)/(4^n-1).

Hence every nonzero cyclic lag k=1,...,n has the same two-sector pair kernel,
while lag n+1 is exactly the identity because U^(n+1)=1.  The nontrivial
2x2 eigenvalue

    rho_n = -1/(4 |PG(n-1,4)|)

is therefore the exact Pearson correlation of two distinct coordinate-occupancy
indicators, not an exponential temporal mixing eigenvalue.

At n=3:

    rho = -1/84,
    Corr(X_t,X_{t+k}) = -1/84 for k=1,2,3 mod 4,
    Corr(X_t,X_{t+4}) = 1.

This correction strengthens the geometry: 84 is the inverse scale of a uniform
projective anti-correlation among the four coordinate charts.
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

OUT = ROOT / "data" / "w33_projective_horizon_lag_law.json"


def qstr(x: Fraction) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def sector(s) -> int:
    # tau_omega(s)[0]=1 iff the first projective coordinate itself is nonzero.
    macro = projective_trace_gauge(s)
    by_trace = int(macro[0] == 1)
    by_support = int(s[0] != 0)
    assert by_trace == by_support
    return by_support


def two_sector_pair_kernel(points, lag: int):
    counts = Counter()
    mass = Counter()
    for s in points:
        a = sector(s)
        b = sector(rotate_projective(s, lag))
        counts[(a, b)] += 1
        mass[a] += 1
    return {
        "A_to_A": Fraction(counts[(1, 1)], mass[1]),
        "A_to_F": Fraction(counts[(1, 0)], mass[1]),
        "F_to_A": Fraction(counts[(0, 1)], mass[0]),
        "F_to_F": Fraction(counts[(0, 0)], mass[0]),
    }, counts, mass


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def matrix_from_kernel(K):
    return [
        [K["A_to_A"], K["A_to_F"]],
        [K["F_to_A"], K["F_to_F"]],
    ]


def exact_row(n: int) -> dict:
    points = projective_points(n)
    total = len(points)
    expected_total = (4 ** (n + 1) - 1) // 3
    assert total == expected_total

    NF = (4 ** n - 1) // 3
    expected = {
        "A_to_A": Fraction(3, 4),
        "A_to_F": Fraction(1, 4),
        "F_to_A": Fraction(3 * 4 ** (n - 1), 4 ** n - 1),
        "F_to_F": Fraction(4 ** (n - 1) - 1, 4 ** n - 1),
    }

    nonzero_lags = []
    for k in range(1, n + 1):
        K, counts, mass = two_sector_pair_kernel(points, k)
        assert K == expected
        assert mass[1] == 4 ** n
        assert mass[0] == NF
        nonzero_lags.append({
            "lag": k,
            "kernel": {name: qstr(value) for name, value in K.items()},
            "counts": {
                "A_to_A": counts[(1, 1)],
                "A_to_F": counts[(1, 0)],
                "F_to_A": counts[(0, 1)],
                "F_to_F": counts[(0, 0)],
            },
        })

    identity, _counts, _mass = two_sector_pair_kernel(points, n + 1)
    assert identity == {
        "A_to_A": Fraction(1, 1),
        "A_to_F": Fraction(0, 1),
        "F_to_A": Fraction(0, 1),
        "F_to_F": Fraction(1, 1),
    }

    lambda2 = expected["A_to_A"] + expected["F_to_F"] - 1
    assert lambda2 == Fraction(-1, 4 * NF)

    # Exact Pearson correlation of distinct coordinate nonzero indicators.
    pA = Fraction(4 ** n, total)
    joint_AA = Fraction(3 * 4 ** (n - 1), total)
    cov = joint_AA - pA * pA
    var = pA * (1 - pA)
    corr = cov / var
    assert corr == lambda2

    P = matrix_from_kernel(expected)
    P2 = matmul(P, P)
    actual_lag2 = matrix_from_kernel(expected if n >= 2 else identity)
    non_markov_witness = None
    if n >= 2:
        assert P2 != actual_lag2
        non_markov_witness = {
            "P_squared": [[qstr(x) for x in row] for row in P2],
            "actual_lag2": [[qstr(x) for x in row] for row in actual_lag2],
        }

    return {
        "n": n,
        "projective_microstates": total,
        "affine_sector_microstates": 4 ** n,
        "boundary_sector_microstates": NF,
        "nonzero_lag_kernel": {name: qstr(value) for name, value in expected.items()},
        "all_nonzero_lags": nonzero_lags,
        "return_lag": n + 1,
        "return_kernel": {name: qstr(value) for name, value in identity.items()},
        "pairwise_correlation": qstr(corr),
        "correlation_formula": f"-1/(4*{NF})",
        "non_markov_witness": non_markov_witness,
    }


def build_result() -> dict:
    rows = [exact_row(n) for n in range(1, 7)]
    n3 = rows[2]
    assert n3["projective_microstates"] == 85
    assert n3["boundary_sector_microstates"] == 21
    assert n3["pairwise_correlation"] == "-1/84"
    assert [x["lag"] for x in n3["all_nonzero_lags"]] == [1, 2, 3]
    assert n3["return_lag"] == 4
    assert n3["return_kernel"] == {"A_to_A": "1", "A_to_F": "0", "F_to_A": "0", "F_to_F": "1"}
    assert n3["non_markov_witness"]["P_squared"] == [["253/336", "83/336"], ["332/441", "109/441"]]
    assert n3["non_markov_witness"]["actual_lag2"] == [["3/4", "1/4"], ["16/21", "5/21"]]

    checks = {
        "enumerated_n1_through_n6": [r["n"] for r in rows] == list(range(1, 7)),
        "all_distinct_coordinate_lags_share_one_kernel": all(
            len({json.dumps(x["kernel"], sort_keys=True) for x in r["all_nonzero_lags"]}) == 1
            for r in rows
        ),
        "cyclic_return_is_identity": all(
            r["return_kernel"] == {"A_to_A": "1", "A_to_F": "0", "F_to_A": "0", "F_to_F": "1"}
            for r in rows
        ),
        "correlation_formula_exact": all(
            Fraction(r["pairwise_correlation"]) == Fraction(-1, 4 * r["boundary_sector_microstates"])
            for r in rows
        ),
        "n3_correlation_is_minus_one_over_84": n3["pairwise_correlation"] == "-1/84",
        "n3_lags_1_2_3_same_and_lag4_identity": len(n3["all_nonzero_lags"]) == 3 and n3["return_lag"] == 4,
        "one_step_kernel_is_not_multistep_markov_kernel": all(r["non_markov_witness"] is not None for r in rows if r["n"] >= 2),
    }

    return {
        "schema": "w33.projective-horizon-lag-law.v1",
        "status": "PASS" if all(checks.values()) else "PARTIAL",
        "headline": (
            "The affine/Fano -1/84 is a projective pair-correlation, not a temporal mixing rate. "
            "For PG(n,4), every pair of distinct coordinate-occupancy indicators has correlation "
            "-1/(4|PG(n-1,4)|); under cyclic U all nonzero lags share that kernel and lag n+1 is identity."
        ),
        "theorem": {
            "sector_definition": "A_i={projective points with coordinate i nonzero}; F_i={coordinate i zero}",
            "distinct_coordinate_kernel": "[[3/4,1/4],[3*4^(n-1)/(4^n-1),(4^(n-1)-1)/(4^n-1)]]",
            "pairwise_correlation": "rho_n=-1/(4*|PG(n-1,4)|)",
            "cyclic_lag_law": "for U rotating n+1 coordinates, lags 1..n have the same pair kernel; lag n+1 is identity",
            "correction": "The 2x2 one-lag kernel is a stationary pair-conditional table. Its powers do not give the actual deterministic multistep sector law unless one artificially re-randomizes inside sectors after each step.",
        },
        "n3_projective_anticorrelation": {
            **n3,
            "autocorrelation_over_one_period": ["1", "-1/84", "-1/84", "-1/84", "1"],
            "reading": "The four coordinate charts are uniformly weakly anti-correlated; cyclic time simply permutes those four chart tests and returns exactly after four steps.",
        },
        "dimension_census": rows,
        "claim_boundary": [
            "The -1/84 value remains exact; what changes is its interpretation from repeated-time decay to pairwise projective anti-correlation.",
            "The pair kernel becomes a genuine Markov chain only under an extra conditional re-randomization assumption that is absent from the deterministic U dynamics.",
            "No thermodynamic relaxation, quantum decoherence, or physical mixing timescale follows from this coefficient alone.",
        ],
        "checks": checks,
    }


def main() -> int:
    result = build_result()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    n3 = result["n3_projective_anticorrelation"]
    print(json.dumps({
        "status": result["status"],
        "n3_rho": n3["pairwise_correlation"],
        "n3_autocorrelation": n3["autocorrelation_over_one_period"],
        "P2_is_not_actual_lag2": n3["non_markov_witness"]["P_squared"] != n3["non_markov_witness"]["actual_lag2"],
    }, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
