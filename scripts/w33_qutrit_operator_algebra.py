#!/usr/bin/env python3
"""Canonical operator-algebra layer for the exact W33 qutrit kernel.

This module packages the exact finite-quantum-information layer that is already
verified elsewhere in the repo:

1. The full 81-element 2-qutrit Weyl-Heisenberg basis on F_3^4.
2. The projective non-identity quotient of 40 points, whose commutation graph
   is W33.
3. A small exact symplectic/Clifford generator set acting on the projective
   points.
4. A canonical quadratic operator on the 40 projective observables,
   H_can = 12 I - A = 16 I - B B^T,
   where A is the W33 adjacency matrix and B is the point-line incidence matrix.

The point of this module is not to add new physics. It isolates the exact
operator layer that should precede any later constant-matching claims.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from itertools import product
import json
from pathlib import Path
import sys
import time
from typing import Dict, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.e8_embedding_group_theoretic import build_w33
from scripts.w33_heisenberg_qutrit import build_f3_cube, compute_local_structure
from scripts.w33_homology import build_clique_complex
from scripts.w33_two_qutrit_pauli import (
    build_commutation_graph,
    build_pauli_operators,
    find_isomorphism,
    symplectic_form,
)

F = 3
OMEGA = np.exp(2j * np.pi / 3)
Vector = Tuple[int, int, int, int]
Matrix4 = Tuple[Tuple[int, int, int, int], ...]


def _single_qutrit_shift_clock() -> Tuple[np.ndarray, np.ndarray]:
    x_op = np.zeros((3, 3), dtype=complex)
    for column in range(3):
        x_op[(column + 1) % 3, column] = 1.0 + 0.0j
    z_op = np.diag([1.0 + 0.0j, OMEGA, OMEGA**2])
    return x_op, z_op


def add_phase_space_vectors(left: Vector, right: Vector) -> Vector:
    return tuple((lval + rval) % F for lval, rval in zip(left, right))


def pauli_product_phase(left: Vector, right: Vector) -> int:
    return int((left[1] * right[0] + left[3] * right[2]) % F)


def pauli_commutator_phase(left: Vector, right: Vector) -> int:
    return int((pauli_product_phase(left, right) - pauli_product_phase(right, left)) % F)


@lru_cache(maxsize=1)
def build_two_qutrit_weyl_basis() -> Dict[Vector, np.ndarray]:
    x_op, z_op = _single_qutrit_shift_clock()
    x_powers = [np.eye(3, dtype=complex), x_op, x_op @ x_op]
    z_powers = [np.eye(3, dtype=complex), z_op, z_op @ z_op]

    basis: Dict[Vector, np.ndarray] = {}
    for vector in product(range(F), repeat=4):
        a_exp, b_exp, c_exp, d_exp = vector
        left = x_powers[a_exp] @ z_powers[b_exp]
        right = x_powers[c_exp] @ z_powers[d_exp]
        basis[vector] = np.kron(left, right)
    return basis


def verify_full_weyl_product_law(
    basis: Dict[Vector, np.ndarray] | None = None,
) -> bool:
    matrices = basis if basis is not None else build_two_qutrit_weyl_basis()
    for left in matrices:
        for right in matrices:
            phase = pauli_product_phase(left, right)
            target = (OMEGA**phase) * matrices[add_phase_space_vectors(left, right)]
            if np.linalg.norm(matrices[left] @ matrices[right] - target) > 1e-10:
                return False
    return True


def verify_commutator_phase_matches_symplectic() -> bool:
    for left in product(range(F), repeat=4):
        for right in product(range(F), repeat=4):
            if pauli_commutator_phase(left, right) != (-symplectic_form(left, right)) % F:
                return False
    return True


def canonical_projective_point(vector: Vector) -> Vector:
    for value in vector:
        if value % F != 0:
            inverse = 1 if value % F == 1 else 2
            return tuple((inverse * entry) % F for entry in vector)
    raise ValueError("zero vector has no projective representative")


def apply_symplectic_matrix(matrix: Matrix4, vector: Vector) -> Vector:
    return tuple(
        int(sum(row[index] * vector[index] for index in range(4)) % F) for row in matrix
    )


def selected_symplectic_generators() -> Dict[str, Matrix4]:
    return {
        "S1": ((0, 2, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
        "T1": ((1, 0, 0, 0), (1, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
        "S2": ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 2), (0, 0, 1, 0)),
        "T2": ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 1, 1)),
        "SWAP": ((0, 0, 1, 0), (0, 0, 0, 1), (1, 0, 0, 0), (0, 1, 0, 0)),
    }


def verify_selected_symplectic_generators() -> Dict[str, Dict[str, object]]:
    projective_points, _ = build_pauli_operators()
    adjacency = build_commutation_graph(projective_points)
    adjacency_sets = [set(row) for row in adjacency]
    point_index = {point: idx for idx, point in enumerate(projective_points)}
    phase_space_vectors = tuple(product(range(F), repeat=4))

    checks: Dict[str, Dict[str, object]] = {}
    for name, matrix in selected_symplectic_generators().items():
        preserves_form = True
        for left in phase_space_vectors:
            image_left = apply_symplectic_matrix(matrix, left)
            for right in phase_space_vectors:
                image_right = apply_symplectic_matrix(matrix, right)
                if symplectic_form(image_left, image_right) != symplectic_form(left, right):
                    preserves_form = False
                    break
            if not preserves_form:
                break

        images = [
            canonical_projective_point(apply_symplectic_matrix(matrix, point))
            for point in projective_points
        ]
        permutation = tuple(point_index[image] for image in images)

        preserves_graph = True
        for source in range(len(projective_points)):
            image_source = permutation[source]
            mapped_neighbors = {permutation[target] for target in adjacency_sets[source]}
            if mapped_neighbors != adjacency_sets[image_source]:
                preserves_graph = False
                break

        checks[name] = {
            "matrix": tuple(tuple(int(value) for value in row) for row in matrix),
            "preserves_symplectic_form": preserves_form,
            "preserves_projective_points": len(set(permutation)) == len(projective_points),
            "preserves_commutation_graph": preserves_graph,
        }
    return checks


def summarize_local_heisenberg_shell(base_vertex: int = 0) -> Dict[str, object]:
    n_vertices, _, adjacency, _ = build_w33()
    adjacency_sets = [set(row) for row in adjacency]
    neighbors, nonneighbors, triangles, _ = compute_local_structure(
        base_vertex, n_vertices, adjacency_sets
    )
    fibers, _ = build_f3_cube(neighbors, nonneighbors, triangles, adjacency_sets)

    nonneighbor_set = set(nonneighbors)
    schlafli = {vertex: set() for vertex in nonneighbors}
    for index, left in enumerate(nonneighbors):
        for right in nonneighbors[index + 1 :]:
            common = len((adjacency_sets[left] & adjacency_sets[right]) & nonneighbor_set)
            if common == 3:
                schlafli[left].add(right)
                schlafli[right].add(left)

    lambda_values = set()
    mu_values = set()
    for index, left in enumerate(nonneighbors):
        for right in nonneighbors[index + 1 :]:
            common = len(schlafli[left] & schlafli[right])
            if right in schlafli[left]:
                lambda_values.add(common)
            else:
                mu_values.add(common)

    return {
        "base_vertex": base_vertex,
        "neighbor_count": len(neighbors),
        "nonneighbor_count": len(nonneighbors),
        "mub_class_count": len(triangles),
        "mub_class_sizes": tuple(len(triangle) for triangle in triangles),
        "fiber_count": len(fibers),
        "fiber_size": len(next(iter(fibers.values()))),
        "schlafli_parameters": (
            len(nonneighbors),
            len(next(iter(schlafli.values()))),
            next(iter(lambda_values)),
            next(iter(mu_values)),
        ),
    }


def adjacency_matrix_from_lists(n_vertices: int, adjacency: list[list[int]]) -> np.ndarray:
    matrix = np.zeros((n_vertices, n_vertices), dtype=int)
    for source, neighbors in enumerate(adjacency):
        for target in neighbors:
            matrix[source, target] = 1
    return matrix


def build_line_incidence_matrix() -> Tuple[np.ndarray, Tuple[Tuple[int, ...], ...]]:
    n_vertices, _, adjacency, _ = build_w33()
    simplices = build_clique_complex(n_vertices, adjacency)
    lines = tuple(simplices[3])
    incidence = np.zeros((n_vertices, len(lines)), dtype=int)
    for line_index, line in enumerate(lines):
        for vertex in line:
            incidence[vertex, line_index] = 1
    return incidence, lines


def summarize_canonical_projective_hamiltonian() -> Dict[str, object]:
    n_vertices, _, adjacency, _ = build_w33()
    adjacency_matrix = adjacency_matrix_from_lists(n_vertices, adjacency)
    incidence, lines = build_line_incidence_matrix()
    incidence_gram = incidence @ incidence.T
    laplacian = 12 * np.eye(n_vertices, dtype=int) - adjacency_matrix
    incidence_laplacian = 16 * np.eye(n_vertices, dtype=int) - incidence_gram

    eigenvalue_counts = Counter(
        int(round(value)) for value in np.linalg.eigvalsh(laplacian.astype(float))
    )
    eigenpairs = tuple(sorted((int(value), int(mult)) for value, mult in eigenvalue_counts.items()))

    return {
        "point_count": n_vertices,
        "line_count": len(lines),
        "line_size": len(lines[0]),
        "lines_per_point": int(incidence.sum(axis=1)[0]),
        "incidence_identity_holds": bool(
            np.array_equal(incidence_gram, adjacency_matrix + 4 * np.eye(n_vertices, dtype=int))
        ),
        "laplacian_matches_incidence_form": bool(np.array_equal(laplacian, incidence_laplacian)),
        "laplacian_eigenpairs": eigenpairs,
        "positive_semidefinite": bool(all(value >= 0 for value, _ in eigenpairs)),
        "kernel_dimension": int(eigenvalue_counts[0]),
    }


@lru_cache(maxsize=1)
def analyze(base_vertex: int = 0) -> Dict[str, object]:
    basis = build_two_qutrit_weyl_basis()
    projective_points, _ = build_pauli_operators()
    projective_adjacency = build_commutation_graph(projective_points)
    identity_isomorphism_holds, mismatches = find_isomorphism(
        projective_points, projective_adjacency
    )
    symplectic_checks = verify_selected_symplectic_generators()
    all_generators_verified = all(
        record["preserves_symplectic_form"]
        and record["preserves_projective_points"]
        and record["preserves_commutation_graph"]
        for record in symplectic_checks.values()
    )

    return {
        "status": "ok",
        "exact_pauli_algebra": {
            "weyl_basis_size": len(basis),
            "product_law_holds": verify_full_weyl_product_law(basis),
            "commutator_phase_matches_symplectic": verify_commutator_phase_matches_symplectic(),
            "projective_point_count": len(projective_points),
            "identity_isomorphism_holds": bool(identity_isomorphism_holds),
            "label_mismatch_count": int(mismatches if mismatches >= 0 else len(projective_points)),
        },
        "local_shell": summarize_local_heisenberg_shell(base_vertex=base_vertex),
        "symplectic_action": {
            "generator_names": tuple(symplectic_checks.keys()),
            "all_generators_verified": all_generators_verified,
            "generator_checks": symplectic_checks,
        },
        "canonical_hamiltonian": summarize_canonical_projective_hamiltonian(),
    }


def main() -> None:
    started = time.time()
    payload = analyze()
    payload["analysis_duration_sec"] = round(time.time() - started, 6)

    output_dir = ROOT / "checks"
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"PART_CVIII_qutrit_operator_algebra_{timestamp}.json"
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("Canonical W33 qutrit operator layer")
    print(f"  Weyl basis size: {payload['exact_pauli_algebra']['weyl_basis_size']}")
    print(f"  Projective point count: {payload['exact_pauli_algebra']['projective_point_count']}")
    print(f"  All symplectic generators verified: {payload['symplectic_action']['all_generators_verified']}")
    print(f"  Hamiltonian eigenpairs: {payload['canonical_hamiltonian']['laplacian_eigenpairs']}")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()