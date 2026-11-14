#!/usr/bin/env python3
"""Exact rational upper bound for nine F8-regulus MUB certainty objective.

An exact arithmetic certificate constructed from a coordinatewise rounded,
previously published numerical unit vector. Does NOT prove the conjectured
algebraic optimum, global minimality, or an algebraic minimising state.
"""
from __future__ import annotations

import json
import hashlib
from decimal import Decimal, ROUND_HALF_EVEN, localcontext
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "w33_f8_constant_high_precision.json"
OUTPUT = ROOT / "data" / "toe_20261114_f8_exact_rational_witness_refinement.json"
POLY = 0b1011
Q = 8


def gf_mul(a: int, b: int) -> int:
    result = 0
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        if a & 8:
            a ^= POLY
    return result


def gf_trace(a: int) -> int:
    x, accum = a, 0
    for _ in range(3):
        accum ^= x
        x = gf_mul(x, x)
    assert accum in (0, 1)
    return accum


XI = tuple(tuple(1 - 2 * gf_trace(gf_mul(a, b)) for b in range(Q)) for a in range(Q))
PHI = tuple(
    tuple(tuple(1 - 2 * gf_trace(gf_mul(t, gf_mul(a, b))) for b in range(Q)) for a in range(Q))
    for t in range(Q)
)


def normalize_source_to_integer_vector(coords: list[str], decimals: int) -> list[tuple[int, int]]:
    assert len(coords) == 128
    factor = Decimal(10) ** decimals
    # A common integer denominator cancels in normalization, leaving an
    # explicitly exact algebraic state (integer complex entries)/sqrt(N).
    return [
        (
            int((Decimal(coords[2 * j]) * factor).to_integral_value(rounding=ROUND_HALF_EVEN)),
            int((Decimal(coords[2 * j + 1]) * factor).to_integral_value(rounding=ROUND_HALF_EVEN)),
        )
        for j in range(64)
    ]


def exact_objective(z: list[tuple[int, int]]) -> Fraction:
    assert len(z) == 64
    norm_sq = sum(re * re + im * im for re, im in z)
    assert norm_sq > 0
    original = sum((re * re + im * im) ** 2 for re, im in z)
    transformed_fourth = 0
    for t in range(Q):
        for k in range(Q):
            for ell in range(Q):
                re = im = 0
                for a in range(Q):
                    for b in range(Q):
                        sgn = XI[k][a] * PHI[t][a][b] * XI[b][ell]
                        x, y = z[Q * a + b]
                        re += sgn * x
                        im += sgn * y
                transformed_fourth += (re * re + im * im) ** 2
    # F = original/N^2 + transforms/(8^4*N^2) - 9/64.
    # c8(witness) = 64 F; minimising over ALL states can only be smaller.
    return Fraction(
        64 * (Q**4 * original + transformed_fourth) - 9 * Q**4 * norm_sq**2,
        Q**4 * norm_sq**2,
    )


def finite_field_checks() -> dict:
    trace_count = sum(gf_trace(a) for a in range(Q))
    hadamard = [
        [sum(XI[k][a] * XI[ell][a] for a in range(Q)) for ell in range(Q)]
        for k in range(Q)
    ]
    assert trace_count == 4
    assert hadamard == [[Q if k == ell else 0 for ell in range(Q)] for k in range(Q)]
    assert all(gf_mul(a, 1) == a for a in range(Q))
    # An independent exact Gauss-sum check gives |sum_{a,b}
    # (-1)^Tr(delta*a*b + k*a + ell*b)| = q for EVERY nonzero delta,
    # certifying mutual unbiasedness of the distinct chirped Walsh bases.
    for delta in range(1, Q):
        for k in range(Q):
            for ell in range(Q):
                gauss = sum(
                    1 - 2 * gf_trace(gf_mul(delta, gf_mul(a, b)) ^ gf_mul(k, a) ^ gf_mul(ell, b))
                    for a in range(Q) for b in range(Q)
                )
                assert abs(gauss) == Q
    return {"trace_one_elements": trace_count, "hadamard_orthogonal": True, "all_seven_nonzero_chirp_gauss_sums_abs_eight": True}


def certify(decimals: int = 18) -> dict:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    z = normalize_source_to_integer_vector(source["minimiser"], decimals)
    value = exact_objective(z)
    # The pre-existing rational bound was 2.4985086592218817; this decimal
    # is used strictly as a rational COMPARISON, not as a proof of an optimum.
    prior_rational_comparison = Fraction("2.4985086592218817")
    assert value < prior_rational_comparison, "Rounded witness failed to improve the previous threshold"
    with localcontext() as ctx:
        ctx.prec = 90
        full_decimal = format(Decimal(value.numerator) / Decimal(value.denominator), ".60f")
    result = {
        "status": "CERTIFIED_EXACT_RATIONAL_UPPER_BOUND",
        "scope": "A concrete 64-complex-component exact state in the nine F8 MUB CZ model, not a proof of global optimality",
        "source_file": "data/w33_f8_constant_high_precision.json",
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "coordinate_scale": 10**decimals,
        "integers_re_im": [list(pair) for pair in z],
        "norm_squared_before_normalization": str(sum(x*x + y*y for x, y in z)),
        "c8_exact_numerator": str(value.numerator),
        "c8_exact_denominator": str(value.denominator),
        "c8_decimal_60_digits": full_decimal,
        "strictly_below_prior_bound_2_4985086592218817": True,
        "field_controls": finite_field_checks(),
        "limitations": [
            "The minimizer is imported from a prior numerical optimization, then rounded; its components form a rigorous exact rational upper-bound witness.",
            "There is no global lower bound at this value and no exact proof the conjectural cyclotomic value is attained.",
            "The logical vector requires a square-root normalization but all probabilities and objective values are rational.",
        ],
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    d = certify()
    print("CERTIFIED exact c8 upper bound =", d["c8_decimal_60_digits"])
    print("fraction digits:", len(d["c8_exact_numerator"]), len(d["c8_exact_denominator"]))
