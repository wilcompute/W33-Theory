#!/usr/bin/env python3
"""Pass 99: exact relation between the Construction-A lattice and the +2 eigenlattice."""

from __future__ import annotations

import json
from itertools import combinations, product
from pathlib import Path

import numpy as np

from analysis.bt926_plus2_eigenlattice import canon, snf_with_transforms
from w33_pass92_discriminant_e8 import rowspace_basis, to_int

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "w33_pass118_lattice_intersection.json"
L2_DET = 2**16 * 3**10 * 5


def gf2_basis_from_columns(matrix: np.ndarray) -> list[int]:
    return rowspace_basis([to_int(row) for row in (matrix.T % 2)])


def main() -> int:
    points = sorted({canon(v) for v in product(range(3), repeat=4) if any(v)})

    def symp(x: tuple[int, ...], y: tuple[int, ...]) -> int:
        return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3

    adjacency = np.zeros((40, 40), dtype=np.int64)
    for i, j in combinations(range(40), 2):
        if symp(points[i], points[j]) == 0:
            adjacency[i, j] = adjacency[j, i] = 1

    diagonal, _, right = snf_with_transforms(adjacency - 2 * np.eye(40, dtype=np.int64))
    zero_columns = [j for j in range(40) if int(diagonal[j, j]) == 0]
    kernel = np.array(
        [[int(right[row, col]) for col in zero_columns] for row in range(40)],
        dtype=np.int64,
    )

    image = gf2_basis_from_columns(kernel)
    code = rowspace_basis([to_int(adjacency[i]) for i in range(40)])
    combined = rowspace_basis(code + image)
    intersection_dim = len(code) + len(image) - len(combined)
    quotient_dim = len(image) - intersection_dim
    intersection_index = 2**quotient_dim

    # Lambda_C = {z/sqrt(2): z mod 2 in C}.  Let L2^C be the kernel
    # vectors reducing into C.  Then (1/sqrt(2))L2^C is the exact
    # intersection of the scaled eigenspace lattice with Lambda_C.
    scaled_intersection_det = intersection_index**2 * L2_DET // 2 ** kernel.shape[1]
    checks = {
        "integer_eigenlattice_rank_24": kernel.shape == (40, 24),
        "kernel_equation": bool(np.array_equal(adjacency @ kernel, 2 * kernel)),
        "mod2_image_is_Cperp_rank24": len(image) == 24,
        "binary_code_rank16": len(code) == 16,
        "code_contained_in_mod2_image": len(combined) == 24,
        "intersection_dimension_16": intersection_dim == 16,
        "intersection_index_2pow8": intersection_index == 256,
        "scaled_intersection_det": scaled_intersection_det == 2**8 * 3**10 * 5,
    }
    payload = {
        "schema": "w33.pass99.lattice_intersection.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "ranks": {
            "Lambda_C": 40,
            "L2": 24,
            "C": len(code),
            "L2_mod2_image": len(image),
            "C_intersection_L2_mod2": intersection_dim,
        },
        "exact_sequence": (
            "0 -> L2^C -> L2 -> Cperp/C -> 0, where " "L2^C={x in L2: x mod 2 in C}"
        ),
        "quotient": {
            "dimension": quotient_dim,
            "order": intersection_index,
            "identification": "L2/L2^C ~= Cperp/C ~= (Z/2)^8",
        },
        "lattice_chain": (
            "sqrt(2)L2 subset (1/sqrt(2))L2^C "
            "= Lambda_C intersection ((1/sqrt(2))L2_R)"
        ),
        "determinants": {
            "L2": L2_DET,
            "L2_factorization": "2^16 * 3^10 * 5",
            "scaled_intersection": scaled_intersection_det,
            "scaled_intersection_factorization": "2^8 * 3^10 * 5",
        },
        "reading": (
            "The two lattices are related by the full eight-dimensional glue "
            "quotient, not by equality: reduction mod 2 maps L2 onto Cperp, "
            "and the vectors that enter Lambda_C have index 2^8 in L2."
        ),
        "checks": checks,
    }
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
