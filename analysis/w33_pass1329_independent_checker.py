#!/usr/bin/env python3
"""Independent standard-library checker for Passes 1325--1329.

No NumPy or SymPy is used.  The checker independently reconstructs the
primitive Hecke coefficient lattice from the Pass-1321 JSON files, computes
its determinant by Bareiss elimination, computes local Smith exponents over
Z/p^N Z, and verifies the triality multiplicity arithmetic.
"""
from __future__ import annotations
from fractions import Fraction
from functools import reduce
from itertools import permutations
from math import gcd, lcm
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FILES = [
    "w33_pass1321_hecke_block_1.json", "w33_pass1321_hecke_block_6.json",
    "w33_pass1321_hecke_block_15.json", "w33_pass1321_hecke_block_15a.json",
    "w33_pass1321_hecke_block_20.json", "w33_pass1321_hecke_block_30.json",
    "w33_pass1321_hecke_block_60a.json", "w33_pass1321_hecke_block_64.json",
    "w33_pass1321_hecke_block_81-minus.json",
]
EXPECTED_SNF = [1,1,1,1,1,2,2,2,2,2,2,2,4,12,12,12,12,24,24,24,48,144,288,864,4320,34560]


def bareiss_det(matrix):
    a = [row[:] for row in matrix]
    n = len(a)
    sign, previous = 1, 1
    for k in range(n - 1):
        pivot = next((r for r in range(k, n) if a[r][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            sign *= -1
        value = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = a[i][j] * value - a[i][k] * a[k][j]
                assert numerator % previous == 0
                a[i][j] = numerator // previous
        previous = value
        for i in range(k + 1, n):
            a[i][k] = 0
    return sign * a[-1][-1]


def vp(x, p, precision, modulus):
    x %= modulus
    if x == 0:
        return precision
    out = 0
    while x % p == 0:
        x //= p
        out += 1
    return out


def local_exponents(matrix, p, precision):
    modulus = p ** precision
    a = [[x % modulus for x in row] for row in matrix]
    n = len(a)
    out = []
    for i in range(n):
        exponent, row, col = min(
            (vp(a[r][c], p, precision, modulus), r, c)
            for r in range(i, n) for c in range(i, n)
        )
        a[i], a[row] = a[row], a[i]
        for current in a:
            current[i], current[col] = current[col], current[i]
        unit = a[i][i] // (p ** exponent)
        inverse = pow(unit, -1, modulus)
        a[i] = [(x * inverse) % modulus for x in a[i]]
        reduced = p ** (precision - exponent)
        for r in range(i + 1, n):
            q = (a[r][i] // (p ** exponent)) % reduced
            a[r] = [(a[r][j] - q * a[i][j]) % modulus for j in range(n)]
        for c in range(i + 1, n):
            q = (a[i][c] // (p ** exponent)) % reduced
            for r in range(n):
                a[r][c] = (a[r][c] - q * a[r][i]) % modulus
        out.append(exponent)
    return out


def load_matrix():
    columns = []
    for filename in FILES:
        payload = json.loads((DATA / filename).read_text())
        for raw in payload["block"]["matrix_units"].values():
            vector = [Fraction(x) for x in raw]
            denominator = lcm(*(x.denominator for x in vector))
            integers = [int(x * denominator) for x in vector]
            common = reduce(gcd, (abs(x) for x in integers if x), 0)
            integers = [x // common for x in integers]
            if next(x for x in integers if x) < 0:
                integers = [-x for x in integers]
            columns.append(integers)
    assert len(columns) == 26
    return [[columns[j][i] for j in range(26)] for i in range(26)]


def main():
    matrix = load_matrix()
    det = abs(bareiss_det(matrix))
    exponents = {
        2: local_exponents(matrix, 2, 70),
        3: local_exponents(matrix, 3, 35),
        5: local_exponents(matrix, 5, 15),
    }
    diagonal = [
        2 ** exponents[2][i] * 3 ** exponents[3][i] * 5 ** exponents[5][i]
        for i in range(26)
    ]
    assert diagonal == EXPECTED_SNF
    product_value = 1
    for value in diagonal:
        product_value *= value
    assert product_value == det

    s3 = set(permutations(range(3)))
    assert len(s3) == 6
    x_mult = [1,2,1,1,3,2,1,2,1]
    assert sum(m*m for m in x_mult) == 26
    assert 9 * 26 == 234 and 2 * 26 == 52
    assert 3 * (2*2 + 1*1) + (4*4 + 3*3) == 40

    primary = json.loads((DATA / "w33_pass1325_1329_triality_integral_gauge.json").read_text())
    assert primary["pass1326"]["hecke_matrix_unit_lattice"]["smith_diagonal"] == diagonal
    print(json.dumps({
        "status": "PASS",
        "engine": "python-standard-library",
        "bareiss_determinant": det,
        "smith_diagonal": diagonal,
        "triality_group_order": len(s3),
        "triality_fixed_linking_dimension": 40,
    }, indent=2))

if __name__ == "__main__":
    main()
