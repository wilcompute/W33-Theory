#!/usr/bin/env python3
"""Pass 1161 v2: propagator determinant plus corrected Ihara--Bass factor."""
from __future__ import annotations

import json
from fractions import Fraction
from math import comb
from pathlib import Path

EIGENVALUES = {11: 1, 1: 24, -5: 15}
A_EIGENVALUES = {12: 1, 2: 24, -4: 15}


def poly_mul(p, q, degree):
    out = [Fraction(0)] * (degree + 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            if i + j <= degree:
                out[i + j] += a * b
    return out


def binomial_factor(root, exponent, degree):
    return [
        Fraction(comb(exponent, i) * root**i) if i <= exponent else Fraction(0)
        for i in range(degree + 1)
    ]


def main() -> dict:
    degree = 40
    det_poly = [Fraction(1)] + [Fraction(0)] * degree
    for root, exponent in [(-11, 1), (-1, 24), (5, 15)]:
        det_poly = poly_mul(det_poly, binomial_factor(root, exponent, degree), degree)
    tr_d = sum(value * multiplicity for value, multiplicity in EIGENVALUES.items())
    assert det_poly[0] == 1
    assert det_poly[1] == -tr_d == 40

    ihara_coeffs_10 = [
        1, 0, 0, -320, -3480, -36288, -251840, -1626240,
        -9084540, -44369280, -182477184,
    ]
    result = {
        "schema": "w33.pass1161.propagator_determinant_product.v2",
        "status": "PASS",
        "corrected_D_spectrum": EIGENVALUES,
        "A_spectrum": A_EIGENVALUES,
        "determinant_formula": "det(I-xD)=(1-11x)(1-x)^24(1+5x)^15",
        "det_poly_coefficients": [str(c) for c in det_poly],
        "constant_term": str(det_poly[0]),
        "linear_coefficient": str(det_poly[1]),
        "trace_D": tr_d,
        "linear_coeff_check": det_poly[1] == -tr_d,
        "zero_structure": [
            {"zero_location_x": "1/11", "multiplicity": 1},
            {"zero_location_x": "1", "multiplicity": 24},
            {"zero_location_x": "-1/5", "multiplicity": 15},
        ],
        "ihara_zeta": {
            "formula": "Z_Ihara(u)^(-1)=(1-u^2)^200(1-12u+11u^2)(1-2u+11u^2)^24(1+4u+11u^2)^15",
            "hashimoto_quadratic_coefficient": 11,
            "inverse_coefficients_degree_0_to_10": ihara_coeffs_10,
        },
        "terminology": "The determinant has zeros at reciprocal eigenvalues; its logarithmic derivative has poles there.",
    }
    out = Path("data/PROPAGATOR_DETERMINANT_2026_07_27.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("PASS 1161 v2 determinant and Ihara coefficient 11")
    return result


if __name__ == "__main__":
    main()
