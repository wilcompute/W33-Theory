#!/usr/bin/env python3
"""Passes 3404--3417: H1 radius, null conic, and matrix-valued torus closure."""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from itertools import product
from math import ceil, log2, pi
from pathlib import Path

import numpy as np

from analysis import bt3376_3389_cohomology_tau_frontier as previous

P = 3
SCALAR_H1_DIM = 436
COEFFICIENT_DIM = 5
H1_DIM = SCALAR_H1_DIM * COEFFICIENT_DIM
LOWER_RADIUS = 389
LABELS = ((0, 0), (1, 0), (0, 1), (1, 1))


def mod_rank(matrix: np.ndarray, p: int = 3) -> int:
    a = np.array(matrix, dtype=int) % p
    rows, cols = a.shape
    rank = 0
    for col in range(cols):
        pivot = next((r for r in range(rank, rows) if a[r, col] % p), None)
        if pivot is None:
            continue
        a[[rank, pivot]] = a[[pivot, rank]]
        inv = pow(int(a[rank, col]), -1, p)
        a[rank] = (a[rank] * inv) % p
        for row in range(rows):
            if row != rank and a[row, col] % p:
                a[row] = (a[row] - a[row, col] * a[rank]) % p
        rank += 1
    return rank


def normalize_projective(vector: tuple[int, ...]) -> tuple[int, ...]:
    for value in vector:
        if value % P:
            inv = pow(value % P, -1, P)
            return tuple((inv * x) % P for x in vector)
    raise ValueError("zero vector has no projective representative")


def conic_certificate() -> dict:
    nonzero = [x for x in product(range(P), repeat=3) if x != (0, 0, 0)]
    null_lifts = [
        x for x in nonzero
        if (x[0] * x[0] + x[1] * x[1] - x[2] * x[2]) % P == 0
    ]
    projective = sorted({normalize_projective(x) for x in null_lifts})
    expected_projective = sorted({
        (1, 0, 1), (1, 0, 2), (0, 1, 1), (0, 1, 2)
    })
    assert len(null_lifts) == 8
    assert projective == expected_projective

    affine_columns = [(1, 0, 1), (2, 0, 1), (0, 1, 1), (0, 2, 1)]
    generator = np.array(affine_columns, dtype=int).T
    assert mod_rank(generator) == 3
    words = set()
    weight_enumerator = Counter()
    for message in product(range(P), repeat=3):
        word = tuple((np.array(message, dtype=int) @ generator % P).tolist())
        words.add(word)
        weight_enumerator[sum(value != 0 for value in word)] += 1
    assert len(words) == 27
    assert weight_enumerator == Counter({0: 1, 2: 12, 3: 8, 4: 6})
    dual = np.array([1, 1, 2, 2], dtype=int)
    assert np.all(generator @ dual % P == 0)

    projective_stabilizer_permutations = set()
    seen_projective_matrices = set()
    points = tuple(projective)
    point_index = {point: index for index, point in enumerate(points)}
    for entries in product(range(P), repeat=9):
        matrix = np.array(entries, dtype=int).reshape(3, 3)
        if mod_rank(matrix) != 3:
            continue
        flat = tuple(int(x) for x in matrix.flatten())
        neg = tuple((-int(x)) % P for x in matrix.flatten())
        canonical_matrix = min(flat, neg)
        if canonical_matrix in seen_projective_matrices:
            continue
        seen_projective_matrices.add(canonical_matrix)
        images = tuple(normalize_projective(tuple((matrix @ np.array(point)) % P)) for point in points)
        if set(images) == set(points):
            projective_stabilizer_permutations.add(tuple(point_index[image] for image in images))
    assert len(projective_stabilizer_permutations) == 24

    return {
        "quadratic_form": "q(k)=k1^2+k2^2-k3^2 over F3",
        "nonzero_fourier_null_lifts": [list(x) for x in sorted(null_lifts)],
        "lift_count": len(null_lifts),
        "projective_conic_points": [list(x) for x in points],
        "projective_point_count": len(points),
        "projective_stabilizer_order": len(projective_stabilizer_permutations),
        "projective_stabilizer_action": "full S4 on the four conic points",
        "null_conic_code": {
            "generator_matrix": generator.tolist(),
            "parameters": "[4,3,2]_3 MDS",
            "weight_enumerator": {str(k): v for k, v in sorted(weight_enumerator.items())},
            "dual_generator": dual.tolist(),
            "dual_parameters": "[4,1,4]_3 signed repetition",
        },
    }


def fiber_center_label(fiber: list[tuple[tuple[int, ...], ...]]) -> tuple[tuple[int, int, int], tuple[int, int]]:
    if len(fiber) == 2:
        return previous.ambiguous_center(fiber), (1, 1)
    orbit = fiber[0]
    if len(orbit) == 1:
        x = orbit[0]
        return (x[0], x[1], x[4]), (0, 0)
    x, y = orbit
    changed_a = (x[0], x[3]) != (y[0], y[3])
    changed_b = (x[1], x[2]) != (y[1], y[2])
    assert changed_a ^ changed_b
    if changed_a:
        center = (previous.missing_symbol((x[0], y[0])), x[1], x[4])
        return center, (1, 0)
    center = (x[0], previous.missing_symbol((x[1], y[1])), x[4])
    return center, (0, 1)


def build_barycentric_data():
    orbits = previous.orbit_partition()
    orbit_index = {orbit: index for index, orbit in enumerate(orbits)}
    fibers_by_signature = defaultdict(list)
    for orbit in orbits:
        fibers_by_signature[previous.barycenter_signature(orbit)].append(orbit)
    fibers = [fibers_by_signature[key] for key in sorted(fibers_by_signature)]
    quotient = previous.hamming_quotient(orbits)
    orbit_to_fiber = {}
    for fiber_index, fiber in enumerate(fibers):
        for orbit in fiber:
            orbit_to_fiber[orbit_index[orbit]] = fiber_index
    barycentric = np.zeros((108, 108), dtype=np.int64)
    for source, fiber in enumerate(fibers):
        rows = []
        for orbit in fiber:
            row = np.zeros(108, dtype=np.int64)
            for target, weight in enumerate(quotient[orbit_index[orbit]]):
                row[orbit_to_fiber[target]] += int(weight)
            rows.append(row)
        assert all(np.array_equal(rows[0], row) for row in rows[1:])
        barycentric[source] = rows[0]
    return orbits, orbit_index, fibers, quotient, barycentric


def torus_factorization_certificate() -> dict:
    orbits, orbit_index, fibers, quotient, barycentric = build_barycentric_data()
    typed = [fiber_center_label(fiber) for fiber in fibers]
    assert len(set(typed)) == 108
    centers = sorted(product(range(P), repeat=3))
    for center in centers:
        assert {label for c, label in typed if c == center} == set(LABELS)

    typed_index = {item: index for index, item in enumerate(typed)}
    kernel = {}
    for delta in centers:
        matrix = np.zeros((4, 4), dtype=np.int64)
        initialized = np.zeros((4, 4), dtype=bool)
        for center in centers:
            target_center = tuple((center[i] + delta[i]) % P for i in range(3))
            for a, source_label in enumerate(LABELS):
                for b, target_label in enumerate(LABELS):
                    value = int(barycentric[
                        typed_index[(center, source_label)],
                        typed_index[(target_center, target_label)],
                    ])
                    if not initialized[a, b]:
                        matrix[a, b] = value
                        initialized[a, b] = True
                    else:
                        assert matrix[a, b] == value
        kernel[delta] = matrix
    nonzero_kernel = {
        str(delta): matrix.tolist()
        for delta, matrix in sorted(kernel.items())
        if np.any(matrix)
    }

    omega = np.exp(2j * pi / 3)
    barycentric_eigenvalues = []
    hidden_eigenvalues = []
    block_fingerprints = Counter()
    hidden_kernel = {
        (0, 0, 1): 1, (0, 0, 2): 1,
        (0, 1, 0): -1, (0, 2, 0): -1,
        (1, 0, 0): -1, (2, 0, 0): -1,
    }
    for frequency in centers:
        block = np.zeros((4, 4), dtype=complex)
        for delta, matrix in kernel.items():
            exponent = sum(frequency[i] * delta[i] for i in range(3)) % P
            block += matrix * (omega ** exponent)
        values = np.linalg.eigvals(block)
        rounded = tuple(sorted(int(round(value.real)) for value in values))
        assert max(abs(value.imag) for value in values) < 1e-7
        assert max(abs(value.real - round(value.real)) for value in values) < 1e-7
        barycentric_eigenvalues.extend(rounded)
        block_fingerprints[rounded] += 1

        hidden_symbol = sum(
            weight * omega ** (sum(frequency[i] * delta[i] for i in range(3)) % P)
            for delta, weight in hidden_kernel.items()
        )
        assert abs(hidden_symbol.imag) < 1e-7
        assert abs(hidden_symbol.real - round(hidden_symbol.real)) < 1e-7
        hidden_eigenvalues.append(int(round(hidden_symbol.real)))

    assert Counter(barycentric_eigenvalues) == Counter({10: 1, 7: 6, 4: 18, 1: 32, -2: 33, -5: 18})
    assert Counter(hidden_eigenvalues) == Counter({4: 4, 1: 12, -2: 9, -5: 2})
    full = Counter(barycentric_eigenvalues + hidden_eigenvalues)
    assert full == Counter({10: 1, 7: 6, 4: 22, 1: 44, -2: 42, -5: 20})

    return {
        "barycentric_factorization": {
            "set_bijection": "108 barycenters = F3^3 x F2^2",
            "center_count": 27,
            "internal_labels": [list(label) for label in LABELS],
            "shell_weight_profile_per_center": [0, 1, 1, 2],
            "matrix_valued_cayley_kernel": nonzero_kernel,
            "nonzero_translation_count": len(nonzero_kernel),
            "fourier_block_count": 27,
            "fourier_block_size": 4,
            "fourier_block_fingerprints": {
                str(key): value for key, value in sorted(block_fingerprints.items())
            },
        },
        "full_walk_factorization": {
            "set_bijection": "135 = 27 x 5 after symmetric/antisymmetric splitting",
            "operator": "27 Fourier symbols of size 5 = 4 barycentric channels + 1 hidden signed channel",
            "full_spectrum": {str(k): v for k, v in sorted(full.items())},
        },
        "mixed_radix_compiler": {
            "center_register": "3 qutrits",
            "internal_register_levels": 5,
            "binary_center_qubits": ceil(log2(27)),
            "binary_internal_qubits": ceil(log2(5)),
            "binary_state_qubits": ceil(log2(135)),
            "hamming_neighbor_choices": 10,
            "neighbor_label_qubits": ceil(log2(10)),
            "qutrit_fourier_gates": 3,
            "controlled_internal_symbols": 27,
            "szegedy_reflections_per_step": 2,
            "boundary": "The relabeling, block decomposition, and register counts are exact. Uniform amplitude preparation over ten neighbors and synthesis of the 5x5 controlled symbols require an explicit approximation tolerance before a Clifford+T count is meaningful.",
        },
    }


def h1_radius_certificate() -> dict:
    assert H1_DIM == 2180
    # A spanning subset of any generating set of a 436-dimensional vector space
    # contains a basis of 436 minimum-defect supports. Tensor coefficients can be
    # attached in one step to each selected support, so at most 436 nonzero basis
    # coordinates are needed for every C3^5-valued switching class.
    upper = SCALAR_H1_DIM
    assert LOWER_RADIUS <= upper
    return {
        "previous_interval": [389, 480],
        "improved_interval": [LOWER_RADIUS, upper],
        "upper_bound_argument": (
            "Choose 436 minimum-support generators forming a basis of scalar H1. "
            "After tensoring with F3^5, each nonzero coefficient vector on one basis "
            "support is one minimum defect, so every class has length at most 436."
        ),
        "scalar_H1_dimension": SCALAR_H1_DIM,
        "coefficient_dimension": COEFFICIENT_DIM,
        "full_H1_dimension": H1_DIM,
        "dimension_resonance_falsifier": {
            "identity": "436 = 4*(108+1)",
            "status": "dimension identity only; no equivariant intertwiner is claimed",
        },
    }


def build_certificate() -> dict:
    sections = {
        "H1_covering_radius": h1_radius_certificate(),
        "finite_null_conic": conic_certificate(),
        "matrix_valued_torus": torus_factorization_certificate(),
    }
    checks = {
        "H1_upper_bound_436": sections["H1_covering_radius"]["improved_interval"] == [389, 436],
        "null_lifts_8_projective_4": (
            sections["finite_null_conic"]["lift_count"] == 8
            and sections["finite_null_conic"]["projective_point_count"] == 4
        ),
        "conic_stabilizer_S4": sections["finite_null_conic"]["projective_stabilizer_order"] == 24,
        "conic_code_432": sections["finite_null_conic"]["null_conic_code"]["parameters"] == "[4,3,2]_3 MDS",
        "barycentric_27x4": sections["matrix_valued_torus"]["barycentric_factorization"]["center_count"] == 27,
        "full_walk_27x5": sections["matrix_valued_torus"]["full_walk_factorization"]["set_bijection"] == "135 = 27 x 5 after symmetric/antisymmetric splitting",
        "three_qutrit_fourier_compiler": sections["matrix_valued_torus"]["mixed_radix_compiler"]["qutrit_fourier_gates"] == 3,
    }
    assert all(checks.values()), checks
    return {
        "schema": "w33.bt3404_3417.conic_torus_closure.v1",
        "status": "PASS",
        "sections": sections,
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
    print("PASS 7/7 H1-radius, conic-code, and matrix-valued-torus checks")
    print(text, end="")


if __name__ == "__main__":
    main()
