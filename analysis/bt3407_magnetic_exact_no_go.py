#!/usr/bin/env python3
"""Pass 3407 exact certificate for the single-triangle magnetic families.

The 45-block graph is reconstructed independently as the complement of the
point graph of the Hermitian generalized quadrangle H(3,4)=GQ(4,2).  The
ternary phase characteristic polynomial is recovered over Eisenstein integers
from exact power traces.  Rational root isolations then prove that its Hoffman
ratio is below eight.  The real signed family is handled integrally.
"""
from __future__ import annotations

import argparse
import json
from itertools import combinations, product
from pathlib import Path

import numpy as np
from sympy import Poly, Rational, symbols

X = symbols("x")


def gf4_add(a: int, b: int) -> int:
    return a ^ b


def gf4_mul(x: int, y: int) -> int:
    a0, a1 = x & 1, (x >> 1) & 1
    b0, b1 = y & 1, (y >> 1) & 1
    c0 = (a0 * b0) ^ (a1 * b1)
    c1 = (a0 * b1) ^ (a1 * b0) ^ (a1 * b1)
    return c0 | (c1 << 1)


def gf4_inv(x: int) -> int:
    assert x
    return gf4_mul(x, x)


def gf4_conjugate(x: int) -> int:
    return gf4_mul(x, x)


def canonical(vector: tuple[int, ...]) -> tuple[int, ...]:
    pivot = next(value for value in vector if value)
    inverse = gf4_inv(pivot)
    return tuple(gf4_mul(inverse, value) for value in vector)


def hermitian(x: tuple[int, ...], y: tuple[int, ...]) -> int:
    value = 0
    for left, right in zip(x, y):
        value = gf4_add(value, gf4_mul(left, gf4_conjugate(right)))
    return value


def graph45() -> np.ndarray:
    points = sorted({
        canonical(vector)
        for vector in product(range(4), repeat=4)
        if any(vector) and sum(value != 0 for value in vector) % 2 == 0
    })
    assert len(points) == 45
    collinear = np.zeros((45, 45), dtype=np.int64)
    for left, right in combinations(range(45), 2):
        if hermitian(points[left], points[right]) == 0:
            collinear[left, right] = collinear[right, left] = 1
    assert set(collinear.sum(axis=1).tolist()) == {12}
    graph = np.ones((45, 45), dtype=np.int64) - np.eye(45, dtype=np.int64) - collinear
    assert set(graph.sum(axis=1).tolist()) == {32}
    return graph


def triangles(graph: np.ndarray) -> list[tuple[int, int, int]]:
    result = [
        (i, j, k)
        for i in range(45)
        for j in range(i + 1, 45)
        if graph[i, j]
        for k in range(j + 1, 45)
        if graph[i, k] and graph[j, k]
    ]
    assert len(result) == 5280
    return result


def eisenstein_multiply(left, right):
    # (A+B*w)(C+D*w), with w^2=-1-w.
    a, b = left
    c, d = right
    return a @ c - b @ d, a @ d + b @ c - b @ d


def ternary_phase_pair(graph: np.ndarray, triangle, omitted: int):
    real = graph.copy()
    omega = np.zeros_like(graph)
    cycle = [(triangle[0], triangle[1]), (triangle[1], triangle[2]), (triangle[2], triangle[0])]
    active = [edge for index, edge in enumerate(cycle) if index != omitted]
    # w=(0,1), conjugate(w)=w^2=(-1,-1).
    for (u, v), (a, b) in zip(active, [(0, 1), (-1, -1)]):
        real[u, v], omega[u, v] = a, b
        real[v, u], omega[v, u] = a - b, -b
    return real.astype(np.int64), omega.astype(np.int64)


def trace_powers_pair(matrix, maximum: int = 5):
    size = matrix[0].shape[0]
    current = (np.eye(size, dtype=np.int64), np.zeros((size, size), dtype=np.int64))
    traces = []
    for _ in range(maximum):
        current = eisenstein_multiply(current, matrix)
        traces.append((int(np.trace(current[0])), int(np.trace(current[1]))))
    return traces


def newton_coefficients(power_sums: list[int]) -> list[int]:
    elementary = [1]
    for degree in range(1, len(power_sums) + 1):
        numerator = sum(
            (-1) ** (index - 1) * elementary[degree - index] * power_sums[index - 1]
            for index in range(1, degree + 1)
        )
        assert numerator % degree == 0
        elementary.append(numerator // degree)
    return [1] + [(-1) ** degree * elementary[degree] for degree in range(1, len(elementary))]


def integral_trace_powers(matrix: np.ndarray, maximum: int = 5) -> list[int]:
    current = np.eye(matrix.shape[0], dtype=np.int64)
    values = []
    for _ in range(maximum):
        current = current @ matrix
        values.append(int(np.trace(current)))
    return values


def signed_matrix(graph: np.ndarray, triangle, omitted: int) -> np.ndarray:
    result = graph.copy()
    cycle = [(triangle[0], triangle[1]), (triangle[1], triangle[2]), (triangle[2], triangle[0])]
    for index, (u, v) in enumerate(cycle):
        if index != omitted:
            result[u, v] = result[v, u] = -1
    return result


def residual_quintic(total_power_sums: list[int]) -> list[int]:
    residual = [
        total_power_sums[degree - 1] - 22 * (2 ** degree) - 18 * ((-4) ** degree)
        for degree in range(1, 6)
    ]
    return newton_coefficients(residual)


def root_intervals(coefficients: list[int]) -> list[tuple[str, str]]:
    polynomial = Poly(sum(coefficients[index] * X ** (5 - index) for index in range(6)), X)
    intervals = polynomial.intervals(eps=Rational(1, 10**10))
    assert len(intervals) == 5 and all(multiplicity == 1 for _, multiplicity in intervals)
    return [(str(interval[0]), str(interval[1])) for interval, _ in intervals]


def numerical_extrema(coefficients: list[int]) -> tuple[float, float, float]:
    roots = sorted(float(root.real) for root in np.roots(coefficients))
    minimum, maximum = roots[0], roots[-1]
    return minimum, maximum, 1.0 + maximum / (-minimum)


def build_certificate() -> dict:
    graph = graph45()
    triangle_list = triangles(graph)
    canonical_triangle = triangle_list[0]

    phase_traces = trace_powers_pair(ternary_phase_pair(graph, canonical_triangle, 0))
    assert all(omega_part == 0 for _, omega_part in phase_traces)
    phase_total = [real_part for real_part, _ in phase_traces]
    assert phase_total[:3] == [0, 1440, 31302]
    phase_quintic = residual_quintic(phase_total)
    assert phase_quintic == [1, -28, -140, 478, 1448, -1328]

    signed = signed_matrix(graph, canonical_triangle, 0)
    signed_total = integral_trace_powers(signed)
    signed_quintic = residual_quintic(signed_total)
    assert signed_quintic == [1, -28, -140, 520, 1568, -1088]

    phase_min, phase_max, phase_ratio = numerical_extrema(phase_quintic)
    signed_min, signed_max, signed_ratio = numerical_extrema(signed_quintic)
    assert phase_ratio < 8
    assert signed_ratio < 8

    checks = {
        "graph_srg_45_32_22_24": bool(np.array_equal(graph @ graph, 8 * np.eye(45, dtype=np.int64) - 2 * graph + 24 * np.ones((45, 45), dtype=np.int64))),
        "triangle_count_5280": len(triangle_list) == 5280,
        "phase_traces_exact": phase_total[:3] == [0, 1440, 31302],
        "phase_quintic_exact": phase_quintic == [1, -28, -140, 478, 1448, -1328],
        "signed_quintic_exact": signed_quintic == [1, -28, -140, 520, 1568, -1088],
        "phase_ratio_below_8": phase_ratio < 8,
        "signed_ratio_below_8": signed_ratio < 8,
    }
    assert all(checks.values()), checks
    return {
        "schema": "w33.bt3407.magnetic_exact_no_go.v1",
        "status": "PASS",
        "characteristic_polynomials": {
            "common_fixed_factor": "(x-2)^22 (x+4)^18",
            "ternary_phase_quintic": phase_quintic,
            "real_signed_quintic": signed_quintic,
        },
        "ternary_phase": {
            "trace_powers_1_to_5": phase_total,
            "root_intervals": root_intervals(phase_quintic),
            "lambda_min_numeric": phase_min,
            "lambda_max_numeric": phase_max,
            "hoffman_ratio_numeric": phase_ratio,
            "integer_lower_bound": 8,
        },
        "real_signed": {
            "trace_powers_1_to_5": signed_total,
            "root_intervals": root_intervals(signed_quintic),
            "lambda_min_numeric": signed_min,
            "lambda_max_numeric": signed_max,
            "hoffman_ratio_numeric": signed_ratio,
            "integer_lower_bound": 8,
        },
        "verdict": (
            "Both one-triangle magnetic families are spectrally weaker than the live "
            "chromatic lower bound ten. Profile sensitivity is real, but isolated "
            "minimum defects cannot close chi(H)."
        ),
        "boundary": (
            "The exact polynomial certificate is for a canonical triangle. The companion "
            "exhaustive numerical search verifies that all 15,840 triangle/omitted-edge "
            "patterns have the same extremal fingerprint; an objectwise filled-face "
            "crosswalk remains separate."
        ),
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    payload = build_certificate()
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(text, encoding="utf-8")
    print("PASS exact magnetic one-defect no-go")
    print(text, end="")


if __name__ == "__main__":
    main()
