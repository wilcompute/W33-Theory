#!/usr/bin/env python3
"""Pass 1195: exact primitive reduced-cycle census through degree 40."""
from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass1195_ihara_primitive_cycle_census.json"

A_SPECTRUM = {12: 1, 2: 24, -4: 15}
K_MINUS_1 = 11
TRIVIAL_PM_MULT = 200
MAX_N = 40


def mobius(n: int) -> int:
    if n == 1:
        return 1
    p = 2
    factors = 0
    x = n
    while p * p <= x:
        if x % p == 0:
            x //= p
            factors += 1
            if x % p == 0:
                return 0
            while x % p == 0:
                x //= p
        p += 1
    if x > 1:
        factors += 1
    return -1 if factors % 2 else 1


def divisors(n: int) -> list[int]:
    return [d for d in range(1, n + 1) if n % d == 0]


def quadratic_power_sum(lam: int, n: int) -> int:
    if n == 0:
        return 2
    if n == 1:
        return lam
    a, b = 2, lam
    for _ in range(2, n + 1):
        a, b = b, lam * b - K_MINUS_1 * a
    return b


def hashimoto_trace(n: int) -> int:
    trivial = TRIVIAL_PM_MULT * (1 + (-1) ** n)
    spectral = sum(mult * quadratic_power_sum(lam, n) for lam, mult in A_SPECTRUM.items())
    return trivial + spectral


def primitive_oriented_classes(n: int, traces: dict[int, int]) -> int:
    numerator = sum(mobius(d) * traces[n // d] for d in divisors(n))
    assert numerator % n == 0
    return numerator // n


def main() -> dict[str, object]:
    traces = {n: hashimoto_trace(n) for n in range(1, MAX_N + 1)}
    primitive_oriented = {n: primitive_oriented_classes(n, traces) for n in range(1, MAX_N + 1)}
    primitive_unoriented = {}
    for n, count in primitive_oriented.items():
        assert count % 2 == 0
        primitive_unoriented[n] = count // 2

    for n in range(1, MAX_N + 1):
        assert traces[n] == sum(d * primitive_oriented[d] for d in divisors(n))

    assert traces[1] == 0
    assert traces[2] == 0
    assert primitive_unoriented[3] == 160
    assert primitive_unoriented[4] == 1740

    rows = []
    for n in range(1, MAX_N + 1):
        main_term = Fraction(K_MINUS_1**n, n)
        rows.append({
            "length": n,
            "Tr_Bn": traces[n],
            "primitive_oriented_rotation_classes": primitive_oriented[n],
            "primitive_unoriented_dihedral_classes": primitive_unoriented[n],
            "main_term_11n_over_n": str(main_term),
            "ratio_to_main_term": float(Fraction(primitive_oriented[n], 1) / main_term) if main_term else None,
        })

    result = {
        "schema": "w33.pass1195.ihara_primitive_cycle_census.v1",
        "status": "PASS",
        "graph": "W(3,3) collinearity graph SRG(40,12,2,4)",
        "directed_edge_count": 480,
        "hashimoto_outdegree": 11,
        "adjacency_spectrum": A_SPECTRUM,
        "hashimoto_factorization": "(x-1)^200 (x+1)^200 product_lambda (x^2-lambda*x+11)^m_lambda",
        "census": rows,
        "short_checks": {
            "triangles_unoriented": primitive_unoriented[3],
            "length4_unoriented": primitive_unoriented[4],
            "triangle_formula": "40 lines x C(4,3) = 160",
            "length4_formula": "120 line-internal K4 cycles + 1620 generalized-quadrangle apartments = 1740",
        },
        "scope": "Counts primitive tailless nonbacktracking cycles modulo rotation (oriented) and modulo rotation+reversal (unoriented). It does not enumerate individual cycles at large lengths.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "pi3": primitive_unoriented[3], "pi4": primitive_unoriented[4], "pi40": primitive_unoriented[40]}, indent=2))
    return result


if __name__ == "__main__":
    main()
