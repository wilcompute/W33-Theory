#!/usr/bin/env python3
from __future__ import annotations
from collections import deque
from fractions import Fraction
import hashlib
import numpy as np
import sympy as sp
import w33_pass1315_1319_exact_frontiers as prior
from w33_pass1320_1324_common import COMMON_SPECIES,GROUP_ORDER,RelationAlgebra,fstr,primitive_integer_vector
def build_transport_orbitals(hecke: dict, hashi: dict) -> dict:
    Xc, Xd = hecke["Xc"], hecke["Xd"]
    Yc, Yd = hashi["Yc"], hashi["Yd"]
    generators = (
        (Xc, Yc),
        (Xd, Yd),
        (prior.invperm(Xc), prior.invperm(Yc)),
        (prior.invperm(Xd), prior.invperm(Yd)),
    )
    nx, ny = 432, 480
    total = nx * ny
    unseen = np.ones(total, dtype=bool)
    labels = np.empty(total, dtype=np.int8)
    sizes = []
    representatives = []
    orbit_id = 0
    for seed in range(total):
        if not unseen[seed]:
            continue
        representatives.append(divmod(seed, ny))
        unseen[seed] = False
        queue = deque([seed])
        orbit = []
        while queue:
            z = queue.popleft()
            orbit.append(z)
            x, y = divmod(z, ny)
            for gx, gy in generators:
                image = int(gx[x]) * ny + int(gy[y])
                if unseen[image]:
                    unseen[image] = False
                    queue.append(image)
        labels[orbit] = orbit_id
        sizes.append(len(orbit))
        orbit_id += 1
    assert orbit_id == 6
    labels = labels.reshape(nx, ny)
    matrices = tuple((labels == i).astype(np.int8) for i in range(6))
    assert all(int(matrix.sum()) == sizes[i] for i, matrix in enumerate(matrices))
    return {
        "labels": labels,
        "sizes": sizes,
        "representatives": representatives,
        "matrices": matrices,
        "sha256": hashlib.sha256(labels.tobytes()).hexdigest(),
    }


def build_left_action(hecke: dict, transport: dict) -> np.ndarray:
    R = hecke["R"]
    labels = transport["labels"]
    hom_reps = transport["representatives"]
    relation_reps = [tuple(np.argwhere(R == i)[0]) for i in range(26)]
    action = np.zeros((26, 6, 6), dtype=np.int16)
    for relation in range(26):
        for hom_basis in range(6):
            for target_orbit, (x, y) in enumerate(hom_reps):
                action[relation, hom_basis, target_orbit] = int(
                    np.sum((R[x, :] == relation) & (labels[:, y] == hom_basis))
                )
    # Identity relation must act identically.
    identity = int(R[0, 0])
    assert np.array_equal(action[identity], np.eye(6, dtype=np.int16))
    return action


def algebra_action_on_hom(
    element: list[Fraction], vector: list[Fraction], left_action: np.ndarray
) -> list[Fraction]:
    out = [Fraction(0) for _ in range(6)]
    for relation, coefficient in enumerate(element):
        if not coefficient:
            continue
        for source, source_coefficient in enumerate(vector):
            if not source_coefficient:
                continue
            for target in range(6):
                value = int(left_action[relation, source, target])
                if value:
                    out[target] += coefficient * source_coefficient * value
    return out


def species_projection_matrices(
    alg: RelationAlgebra, left_action: np.ndarray
) -> dict[str, list[list[Fraction]]]:
    projections = {}
    for name in COMMON_SPECIES:
        center = alg.central[name]
        matrix = []
        for source in range(6):
            vector = [Fraction(int(i == source)) for i in range(6)]
            matrix.append(algebra_action_on_hom(center, vector, left_action))
        # Rows encode P(T_source) in the orbital basis.
        sympy_matrix = sp.Matrix(
            [[sp.Rational(x.numerator, x.denominator) for x in row] for row in matrix]
        )
        expected_rank = 3 if name == "20" else 1
        assert sympy_matrix.rank() == expected_rank
        assert sympy_matrix * sympy_matrix == sympy_matrix
        projections[name] = matrix
    total = [
        [sum(projections[name][i][j] for name in COMMON_SPECIES) for j in range(6)]
        for i in range(6)
    ]
    assert total == [
        [Fraction(int(i == j)) for j in range(6)] for i in range(6)
    ]
    for i, name in enumerate(COMMON_SPECIES):
        left = sp.Matrix(
            [[sp.Rational(x.numerator, x.denominator) for x in row] for row in projections[name]]
        )
        for other in COMMON_SPECIES[i + 1 :]:
            right = sp.Matrix(
                [[sp.Rational(x.numerator, x.denominator) for x in row] for row in projections[other]]
            )
            assert left * right == sp.zeros(6)
    return projections


def aligned_transport_channels(
    alg: RelationAlgebra,
    matrix_units: dict,
    projections: dict[str, list[list[Fraction]]],
    left_action: np.ndarray,
    transport_sizes: list[int],
) -> list[dict]:
    channels = []
    species_degrees = {name: prior.IRR_BY_NAME[name][0] for name in COMMON_SPECIES}
    for name in COMMON_SPECIES:
        degree = species_degrees[name]
        multiplicity = 3 if name == "20" else 1
        projectors = (
            [matrix_units["units"][name][(i, i)] for i in range(multiplicity)]
            if multiplicity > 1
            else [alg.central[name]]
        )
        for copy_index, projector in enumerate(projectors):
            vector = None
            seed_index = None
            for source in range(6):
                seed = [Fraction(int(i == source)) for i in range(6)]
                candidate = algebra_action_on_hom(projector, seed, left_action)
                if any(candidate):
                    vector = primitive_integer_vector(candidate)
                    seed_index = source
                    break
            assert vector is not None
            # Verify species and copy support.
            projected = [
                sum(projections[name][i][j] * vector[i] for i in range(6))
                for j in range(6)
            ]
            assert projected == vector
            supported = algebra_action_on_hom(projector, vector, left_action)
            assert supported == vector
            squared_norm = sum(
                vector[i] * vector[i] * transport_sizes[i] for i in range(6)
            )
            squared_singular_scale = squared_norm / degree
            assert squared_singular_scale > 0
            channels.append(
                {
                    "species": name,
                    "copy": copy_index,
                    "source_seed": seed_index,
                    "orbital_coefficients": vector,
                    "degree": degree,
                    "squared_singular_scale": squared_singular_scale,
                    "singular_value": f"sqrt({fstr(squared_singular_scale)})",
                    "singular_value_multiplicity": degree,
                }
            )
    assert len(channels) == 6
    # Orthogonality of aligned channels under the Hilbert--Schmidt form.
    for i, left in enumerate(channels):
        for right in channels[i + 1 :]:
            inner = sum(
                left["orbital_coefficients"][k]
                * right["orbital_coefficients"][k]
                * transport_sizes[k]
                for k in range(6)
            )
            assert inner == 0
    return channels


def x_composition_tensor(hecke: dict, transport: dict) -> np.ndarray:
    R = hecke["R"]
    labels = transport["labels"]
    relation_reps = [tuple(np.argwhere(R == k)[0]) for k in range(26)]
    out = np.zeros((6, 6, 26), dtype=np.int16)
    for relation, (x, y) in enumerate(relation_reps):
        code = 6 * labels[x, :].astype(np.int16) + labels[y, :].astype(np.int16)
        counts = np.bincount(code, minlength=36).reshape(6, 6)
        out[:, :, relation] = counts
    return out


def right_hashimoto_action(transport: dict, B: np.ndarray) -> np.ndarray:
    labels = transport["labels"]
    representatives = transport["representatives"]
    action = np.zeros((6, 6), dtype=np.int16)
    for source in range(6):
        for target, (x, y) in enumerate(representatives):
            action[source, target] = int(np.sum((labels[x, :] == source) * B[:, y]))
    return action


def build_hashimoto_matrix(hashi: dict) -> np.ndarray:
    points = hashi["points"]
    directed = hashi["directed"]
    lookup = hashi["lookup"]
    adjacency = np.zeros((40, 40), dtype=np.int8)
    for i, x in enumerate(points):
        for j, y in enumerate(points):
            adjacency[i, j] = int(i != j and prior.symp(x, y) == 0)
    B = np.zeros((480, 480), dtype=np.int8)
    for row, (i, j) in enumerate(directed):
        for k in range(40):
            if k != i and adjacency[j, k]:
                B[row, lookup[j, k]] = 1
    assert np.all(B.sum(axis=1) == 11)
    return B


def y_projector_numerator(point: tuple, hashi: dict, name: str) -> np.ndarray:
    _, _, G, _, _, _, _, _, _, _, atlas_of_element = point
    degree, character = prior.IRR_BY_NAME[name]
    src, dst, lookup = hashi["src"], hashi["dst"], hashi["lookup"]
    columns = np.arange(480)
    numerator = np.zeros((480, 480), dtype=np.int64)
    for index, g in enumerate(G):
        value = int(character[int(atlas_of_element[index])])
        if value:
            action = lookup[g[src], g[dst]]
            numerator[action, columns] += degree * value
    assert np.array_equal(numerator, numerator.T)
    assert np.array_equal(numerator @ numerator, GROUP_ORDER * numerator)
    rank = int(np.linalg.matrix_rank(numerator.astype(float), tol=1e-6))
    expected = prior.IRR_BY_NAME[name][0]
    assert rank == expected
    return numerator


def restricted_species20_dynamics(point: tuple, hashi: dict, B: np.ndarray) -> dict:
    numerator = y_projector_numerator(point, hashi, "20")
    pivots = prior.pivot_columns_mod(numerator, 1000003, 20)
    U = numerator[:, pivots]
    pivot_rows = prior.pivot_columns_mod(U.T, 1000003, 20)
    minor = sp.Matrix(U[pivot_rows, :].tolist())
    dual = (minor.inv() * sp.Matrix(numerator[pivot_rows, :].tolist())) / GROUP_ORDER
    assert dual * sp.Matrix(U.tolist()) == sp.eye(20)
    restricted = dual * sp.Matrix((B @ U).tolist())
    assert restricted == -sp.eye(20)
    assert np.array_equal(B @ U, -U)
    return {
        "projector_numerator_sha256": hashlib.sha256(numerator.tobytes()).hexdigest(),
        "basis_pivots": pivots,
        "pivot_rows": pivot_rows,
        "restricted_matrix": [[int(restricted[i, j]) for j in range(20)] for i in range(20)],
        "minimal_polynomial": "x+1",
        "characteristic_polynomial": "(x+1)^20",
        "hashimoto_eigenvalue": -1,
        "selects_unique_432_copy": False,
        "selection_obstruction": "Hashimoto is -I on the unique 480-side species-20 copy, so it is scalar across all three equivariant transports into the three 432-side copies.",
    }


