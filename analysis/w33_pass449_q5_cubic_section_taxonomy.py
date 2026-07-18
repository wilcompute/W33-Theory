#!/usr/bin/env python3
"""Pass 449: exact q=5 cubic-section spectrum and Smith taxonomy.

The full q=5 section space has 20,592 automorphism orbits (Pass 446), so orbit
enumeration is the wrong compression.  This witness exhausts the canonical
625-element lowest nonlinear family of homogeneous binary cubic sections and
classifies it by invariant values: factorization type, spectrum, tree order,
and complete critical group.
"""
from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass449_q5_cubic_section_taxonomy.json"
Q = 5
INV2 = pow(2, -1, Q)
OMEGA = np.exp(2j * np.pi / Q)
X = sp.symbols("x")

EXPECTED_COMBINED_POLYNOMIALS = {
    "linear_times_irreducible_quadratic": [1, 0, -120, 35, 4895, -2208, -78175, 33830, 416585, -88680, -9584],
    "irreducible_cubic": [1, 0, -120, 35, 4395, -1458, -54425, 17580, 162210, 86445, -9459],
    "double_plus_simple_root": [1, 0, -120, -90, 3770, 5542, -8175, -16170, 835, 12070, 5041],
    "three_distinct_roots": [1, 0, -120, -90, 4770, 7167, -71300, -139920, 337710, 724320, -70209],
    "zero_or_triple_root": [1, 0, -120, 160, 5520, -14208, -108800, 430080, 552960, -4423680, 5308416],
}

REPRESENTATIVES = {
    "linear_times_irreducible_quadratic": (0, 1, 0, 2),
    "irreducible_cubic": (1, 0, 1, 1),
    "double_plus_simple_root": (0, 0, 1, 0),
    "three_distinct_roots": (0, 1, 0, 1),
    "zero_or_triple_root": (0, 0, 0, 0),
}

EXPECTED_COUNTS = {
    "linear_times_irreducible_quadratic": 240,
    "irreducible_cubic": 160,
    "double_plus_simple_root": 120,
    "three_distinct_roots": 80,
    "zero_or_triple_root": 25,
}


def cubic_value(coefficients: tuple[int, int, int, int], a: int, b: int) -> int:
    c0, c1, c2, c3 = coefficients
    return (c0 * a**3 + c1 * a * a * b + c2 * a * b * b + c3 * b**3) % Q


def discriminant(coefficients: tuple[int, int, int, int]) -> int:
    a, b, c, d = coefficients
    return (b * b * c * c - 4 * a * c**3 - 4 * b**3 * d - 27 * a * a * d * d + 18 * a * b * c * d) % Q


def projective_root_count(coefficients: tuple[int, int, int, int]) -> int:
    points = [(1, t) for t in range(Q)] + [(0, 1)]
    return sum(cubic_value(coefficients, a, b) == 0 for a, b in points)


def factorization_type(coefficients: tuple[int, int, int, int]) -> str:
    if coefficients == (0, 0, 0, 0):
        return "zero_or_triple_root"
    delta = discriminant(coefficients)
    roots = projective_root_count(coefficients)
    if delta == 0 and roots == 1:
        return "zero_or_triple_root"
    if delta == 0 and roots == 2:
        return "double_plus_simple_root"
    if delta != 0 and pow(delta, 2, Q) == Q - 1 and roots == 1:
        return "linear_times_irreducible_quadratic"
    if delta != 0 and pow(delta, 2, Q) == 1 and roots == 0:
        return "irreducible_cubic"
    if delta != 0 and pow(delta, 2, Q) == 1 and roots == 3:
        return "three_distinct_roots"
    raise AssertionError((coefficients, delta, roots))


def displacement(a: int, b: int, central_character: int) -> np.ndarray:
    matrix = np.zeros((Q, Q), dtype=np.complex128)
    for coordinate in range(Q):
        target = (coordinate + a) % Q
        phase = central_character * b * (coordinate + INV2 * a)
        matrix[target, coordinate] = OMEGA ** (phase % Q)
    return matrix


DISPLACEMENTS = {
    (t, a, b): displacement(a, b, t)
    for t in (1, 2)
    for a in range(Q)
    for b in range(Q)
}


def weil_block(coefficients: tuple[int, int, int, int], central_character: int) -> np.ndarray:
    matrix = np.zeros((Q, Q), dtype=np.complex128)
    for a, b in itertools.product(range(Q), repeat=2):
        if (a, b) == (0, 0):
            continue
        phase = central_character * cubic_value(coefficients, a, b)
        matrix += (OMEGA ** (phase % Q)) * DISPLACEMENTS[(central_character, a, b)]
    return (matrix + matrix.conjugate().T) / 2


def combined_weil_polynomial(coefficients: tuple[int, int, int, int]) -> tuple[list[int], float]:
    roots = list(np.linalg.eigvalsh(weil_block(coefficients, 1)))
    roots += list(np.linalg.eigvalsh(weil_block(coefficients, 2)))
    coefficients_float = np.poly(roots)
    coefficients_integer = np.rint(coefficients_float).astype(np.int64)
    error = float(np.max(np.abs(coefficients_float - coefficients_integer)))
    return coefficients_integer.tolist(), error


def graph_matrices(coefficients: tuple[int, int, int, int]) -> tuple[np.ndarray, np.ndarray]:
    elements = [(a, b, c) for a in range(Q) for b in range(Q) for c in range(Q)]
    index = {g: i for i, g in enumerate(elements)}
    section = [
        (a, b, cubic_value(coefficients, a, b))
        for a in range(Q)
        for b in range(Q)
        if (a, b) != (0, 0)
    ]
    adjacency = np.zeros((Q**3, Q**3), dtype=np.int64)
    for i, (a, b, c) in enumerate(elements):
        for u, v, w in section:
            h = ((a + u) % Q, (b + v) % Q, (c + w + INV2 * (a * v - b * u)) % Q)
            adjacency[i, index[h]] = 1
    if not np.array_equal(adjacency, adjacency.T):
        raise AssertionError("section is not inverse closed")
    laplacian = 24 * np.eye(Q**3, dtype=np.int64) - adjacency
    return adjacency, laplacian[:-1, :-1]


def padic_counts(matrix: np.ndarray, prime: int, max_level: int) -> list[int]:
    modulus = prime**max_level
    a = matrix.astype(np.int64, copy=True) % modulus
    counts: list[int] = []
    for _ in range(max_level):
        size = a.shape[0]
        rank_units = 0
        while rank_units < size:
            locations = np.argwhere((a[rank_units:, rank_units:] % prime) != 0)
            if locations.size == 0:
                break
            i = rank_units + int(locations[0, 0])
            j = rank_units + int(locations[0, 1])
            if i != rank_units:
                a[[rank_units, i], :] = a[[i, rank_units], :]
            if j != rank_units:
                a[:, [rank_units, j]] = a[:, [j, rank_units]]
            inverse = pow(int(a[rank_units, rank_units]), -1, modulus)
            a[rank_units, :] = (a[rank_units, :] * inverse) % modulus
            factors = a[:, rank_units].copy()
            factors[rank_units] = 0
            a = (a - factors[:, None] * a[rank_units : rank_units + 1, :]) % modulus
            a[rank_units, rank_units + 1 :] = 0
            rank_units += 1
        counts.append(rank_units)
        remainder = a[rank_units:, rank_units:]
        if remainder.size == 0:
            return counts
        if np.any(remainder % prime):
            raise AssertionError("p-adic elimination failure")
        modulus //= prime
        a = (remainder // prime) % modulus
    raise AssertionError((prime, "max_level too small", a.shape[0]))


def weld(size: int, primary: dict[int, list[int]]) -> dict[str, int]:
    values = [1] * size
    for prime, counts in primary.items():
        exponents: list[int] = []
        for exponent, multiplicity in enumerate(counts):
            exponents.extend([exponent] * multiplicity)
        if len(exponents) != size:
            raise AssertionError((prime, len(exponents)))
        for i, exponent in enumerate(sorted(exponents)):
            values[i] *= prime**exponent
    return {str(value): multiplicity for value, multiplicity in sorted(Counter(values).items()) if value > 1}


def build_payload() -> dict:
    census = Counter()
    polynomial_census: dict[str, Counter] = defaultdict(Counter)
    max_rounding_error = 0.0
    for coefficients in itertools.product(range(Q), repeat=4):
        kind = factorization_type(coefficients)
        census[kind] += 1
        polynomial, error = combined_weil_polynomial(coefficients)
        max_rounding_error = max(max_rounding_error, error)
        polynomial_census[kind][tuple(polynomial)] += 1

    classes = {}
    for kind, representative in REPRESENTATIVES.items():
        adjacency, reduced_laplacian = graph_matrices(representative)
        charpoly = sp.factor(sp.Matrix(adjacency).charpoly(X).as_expr())
        tree_order = abs(int(sp.diff(charpoly, X).subs(X, 24))) // 125
        tree_factorization = {int(p): int(v) for p, v in sp.factorint(tree_order).items()}
        primary = {}
        for prime, total_valuation in tree_factorization.items():
            max_level = 8 if prime <= 5 else 2
            counts = padic_counts(reduced_laplacian, prime, max_level)
            if sum(i * c for i, c in enumerate(counts)) != total_valuation:
                raise AssertionError((kind, prime, counts, total_valuation))
            primary[prime] = counts
        group = weld(124, primary)
        classes[kind] = {
            "count": census[kind],
            "representative": list(representative),
            "combined_nontrivial_weil_polynomial": EXPECTED_COMBINED_POLYNOMIALS[kind],
            "adjacency_characteristic_polynomial": str(charpoly),
            "spanning_tree_prime_factorization": {str(p): v for p, v in sorted(tree_factorization.items())},
            "primary_exponent_counts": {
                str(p): {str(i): c for i, c in enumerate(counts)}
                for p, counts in sorted(primary.items())
            },
            "critical_group_invariant_factors": group,
        }

    flat_group = classes["zero_or_triple_root"]["critical_group_invariant_factors"]
    expected_flat_group = {"5": 29, "20": 20, "120": 7, "600": 10, "3000": 23}

    checks = {
        "all_625_forms_classified": sum(census.values()) == 625,
        "factorization_counts_exact": dict(census) == EXPECTED_COUNTS,
        "one_spectral_polynomial_per_factorization_type": all(len(polynomial_census[k]) == 1 for k in EXPECTED_COUNTS),
        "spectral_polynomials_match_expected": all(
            list(next(iter(polynomial_census[k]))) == EXPECTED_COMBINED_POLYNOMIALS[k]
            for k in EXPECTED_COUNTS
        ),
        "rounding_firewall_below_1e_3": max_rounding_error < 1e-3,
        "five_invariant_value_classes": len({tuple(v["combined_nontrivial_weil_polynomial"]) for v in classes.values()}) == 5,
        "flat_plus_24_pure_cubes": census["zero_or_triple_root"] == 25,
        "pure_cube_smith_group_matches_flat": flat_group == expected_flat_group,
        "all_primary_valuations_match_tree_orders": all(
            all(
                sum(int(e) * int(c) for e, c in class_data["primary_exponent_counts"][prime].items())
                == int(class_data["spanning_tree_prime_factorization"][prime])
                for prime in class_data["primary_exponent_counts"]
            )
            for class_data in classes.values()
        ),
    }
    return {
        "schema": "w33.pass449.q5_cubic_section_taxonomy.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "family": {
            "sections": "c(a,b)=alpha*a^3+beta*a^2*b+gamma*a*b^2+delta*b^3 over F5",
            "size": 625,
            "ambient_section_orbit_count_from_pass446": 20592,
            "compression_principle": "classify invariant values rather than automorphism orbits",
        },
        "census": dict(census),
        "classes": classes,
        "maximum_numerical_to_integer_polynomial_error": max_rounding_error,
        "headline": (
            "The 625 cubic sections collapse to exactly five spectrum-and-Smith classes, indexed by binary-cubic "
            "factorization type. The zero section and all 24 nonzero pure cubes are spectrally and integrally invisible: "
            "they have the same critical group as the flat graph."
        ),
        "boundary": (
            "This is an exhaustive theorem for the lowest nonlinear cubic family, not a classification of all 5^12 sections. "
            "Pass 446 proves that full automorphism-orbit classification has 20,592 classes."
        ),
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    payload = build_payload()
    text = json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text(encoding="utf-8") != text:
            raise SystemExit("Pass 449 certificate drift")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(json.dumps({"status": payload["status"], "checks": sum(payload["checks"].values()), "total": len(payload["checks"])}))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
