#!/usr/bin/env python3
"""Passes 3458--3471: face tower, Delsarte deck, modular descent, and tomotope falsifier."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from itertools import combinations, permutations, product
from pathlib import Path

import numpy as np
from sympy import Matrix

from analysis.bt3444_3457_radius_modular_fivechannel import (
    geometry_objects,
    rank_mod,
    sphere_threshold,
)

P = 3
Q = 3 ** 5


def compose(left, right):
    return tuple(left[right[i]] for i in range(len(right)))


def close_group(generators, size):
    identity = tuple(range(size))
    seen = {identity}
    frontier = [identity]
    while frontier:
        new = []
        for element in frontier:
            for generator in generators:
                candidate = compose(generator, element)
                if candidate not in seen:
                    seen.add(candidate)
                    new.append(candidate)
        frontier = new
    return seen


def orbit_partition(size, generators):
    unseen = set(range(size))
    result = []
    while unseen:
        start = min(unseen)
        orbit = {start}
        frontier = [start]
        while frontier:
            new = []
            for item in frontier:
                for generator in generators:
                    image = generator[item]
                    if image not in orbit:
                        orbit.add(image)
                        new.append(image)
            frontier = new
        unseen.difference_update(orbit)
        result.append(sorted(orbit))
    return result


def stabilizer_suborbits(group, base, size):
    stabilizer = [element for element in group if element[base] == base]
    unseen = set(range(size))
    suborbits = []
    while unseen:
        start = min(unseen)
        suborbit = sorted({element[start] for element in stabilizer})
        suborbits.append(suborbit)
        unseen.difference_update(suborbit)
    return stabilizer, suborbits


def orbital_relations(group, suborbits, size):
    representatives = [None] * size
    for element in group:
        image = element[0]
        if representatives[image] is None:
            representatives[image] = element
    assert all(element is not None for element in representatives)
    relations = np.empty((size, size), dtype=np.int16)
    for source, representative in enumerate(representatives):
        for relation, suborbit in enumerate(suborbits):
            for target in suborbit:
                relations[source, representative[target]] = relation
    return relations, representatives


def components(adjacency):
    unseen = set(range(adjacency.shape[0]))
    result = []
    while unseen:
        start = min(unseen)
        component = {start}
        frontier = [start]
        while frontier:
            new = []
            for item in frontier:
                for image in np.flatnonzero(adjacency[item]):
                    image = int(image)
                    if image not in component:
                        component.add(image)
                        new.append(image)
            frontier = new
        unseen.difference_update(component)
        result.append(sorted(component))
    return result


def span_rank_mod(matrices, p=3):
    if not matrices:
        return 0
    rows = np.stack([matrix.reshape(-1) % p for matrix in matrices], axis=0)
    return rank_mod(rows, p)


def independent_basis(matrices, p=3):
    basis = []
    indices = []
    rank = 0
    for index, matrix in enumerate(matrices):
        candidate = matrix % p
        new_rank = span_rank_mod(basis + [candidate], p)
        if new_rank > rank:
            basis.append(candidate)
            indices.append(index)
            rank = new_rank
    return indices, basis


def coordinates_in_basis(matrix, basis, p=3):
    columns = np.stack([item.reshape(-1) % p for item in basis], axis=1)
    target = matrix.reshape(-1) % p
    rows = []
    rank = 0
    for row in range(columns.shape[0]):
        new_rank = rank_mod(columns[rows + [row], :], p)
        if new_rank > rank:
            rows.append(row)
            rank = new_rank
            if rank == len(basis):
                break
    augmented = np.concatenate(
        [columns[rows, :] % p, target[rows, None] % p], axis=1
    )
    n = len(basis)
    for column in range(n):
        pivot = next(row for row in range(column, n) if augmented[row, column] % p)
        augmented[[column, pivot]] = augmented[[pivot, column]]
        augmented[column] = (
            augmented[column]
            * pow(int(augmented[column, column]), -1, p)
            % p
        )
        for row in range(n):
            if row != column and augmented[row, column] % p:
                augmented[row] = (
                    augmented[row]
                    - augmented[row, column] * augmented[column]
                ) % p
    solution = augmented[:, -1] % p
    assert np.array_equal(columns @ solution % p, target)
    return solution.tolist()


def algebra_dimension(generators):
    size = generators[0].shape[0]
    basis = [np.eye(size, dtype=int)]
    vectors = [Matrix(basis[0].reshape(size * size, 1))]
    changed = True
    while changed:
        changed = False
        for left in list(basis):
            for right in generators:
                for candidate in (left @ right, right @ left):
                    columns = vectors + [Matrix(candidate.reshape(size * size, 1))]
                    if Matrix.hstack(*columns).rank() > len(basis):
                        basis.append(candidate)
                        vectors.append(columns[-1])
                        changed = True
    return len(basis)


def cycle_type(permutation):
    unseen = set(range(len(permutation)))
    lengths = []
    while unseen:
        start = min(unseen)
        item = start
        length = 0
        while item in unseen:
            unseen.remove(item)
            length += 1
            item = permutation[item]
        lengths.append(length)
    return tuple(sorted(lengths))


def face_tower_certificate(objects):
    faces = objects["faces"]
    point_generators = objects["generators"]
    face_index = {face: index for index, face in enumerate(faces)}
    face_generators = [
        tuple(
            face_index[tuple(sorted(generator[vertex] for vertex in face))]
            for face in faces
        )
        for generator in point_generators
    ]
    face_group = close_group(face_generators, 240)
    assert len(face_group) == 25920

    face_stabilizer, face_suborbits = stabilizer_suborbits(face_group, 0, 240)
    assert len(face_stabilizer) == 108
    assert sorted(map(len, face_suborbits)) == [1, 1, 4, 18, 18, 18, 18, 27, 27, 108]
    face_relations, face_representatives = orbital_relations(
        face_group, face_suborbits, 240
    )

    singleton = next(
        suborbit[0]
        for suborbit in face_suborbits
        if len(suborbit) == 1 and suborbit[0] != 0
    )
    antipode = [
        face_representatives[source][singleton]
        for source in range(240)
    ]
    assert all(antipode[antipode[item]] == item and antipode[item] != item for item in range(240))
    pairs = sorted({tuple(sorted((item, antipode[item]))) for item in range(240)})
    assert len(pairs) == 120
    pair_index = {pair: index for index, pair in enumerate(pairs)}
    pair_generators = [
        tuple(
            pair_index[tuple(sorted((generator[left], generator[right])))]
            for left, right in pairs
        )
        for generator in face_generators
    ]
    pair_group = close_group(pair_generators, 120)
    assert len(pair_group) == 25920
    pair_stabilizer, pair_suborbits = stabilizer_suborbits(pair_group, 0, 120)
    assert len(pair_stabilizer) == 216
    assert list(map(len, pair_suborbits)) == [1, 36, 27, 2, 54]

    pair_relations, _ = orbital_relations(pair_group, pair_suborbits, 120)
    adjacency_matrices = [
        (pair_relations == relation).astype(np.int64)
        for relation in range(5)
    ]
    assert all(np.array_equal(matrix, matrix.T) for matrix in adjacency_matrices)

    intersection = np.zeros((5, 5, 5), dtype=np.int64)
    for left, A in enumerate(adjacency_matrices):
        for right, B in enumerate(adjacency_matrices):
            product_matrix = A @ B
            for relation in range(5):
                values = product_matrix[pair_relations == relation]
                assert len(set(map(int, values))) == 1
                intersection[left, right, relation] = int(values[0])

    generic = sum((index + 1) * matrix for index, matrix in enumerate(adjacency_matrices))
    values, vectors = np.linalg.eigh(generic.astype(float))
    used = np.zeros(120, dtype=bool)
    eigenmatrix = []
    for index, value in enumerate(values):
        if used[index]:
            continue
        members = np.flatnonzero(np.abs(values - value) < 1e-6)
        used[members] = True
        space = vectors[:, members]
        character = [
            int(round(np.trace(space.T @ matrix @ space) / len(members)))
            for matrix in adjacency_matrices
        ]
        eigenmatrix.append([len(members), character])
    eigenmatrix.sort()
    expected_eigenmatrix = [
        [1, [1, 36, 27, 2, 54]],
        [15, [1, -12, 3, 2, 6]],
        [20, [1, 0, 9, -1, -9]],
        [24, [1, 6, -3, 2, -6]],
        [60, [1, 0, -3, -1, 3]],
    ]
    assert eigenmatrix == expected_eigenmatrix

    valency_two_relation = next(
        relation for relation, suborbit in enumerate(pair_suborbits)
        if len(suborbit) == 2
    )
    fibres = components(adjacency_matrices[valency_two_relation])
    assert len(fibres) == 40 and {len(fibre) for fibre in fibres} == {3}
    fibre_index = {item: index for index, fibre in enumerate(fibres) for item in fibre}

    quotient_generators = [
        tuple(fibre_index[generator[fibre[0]]] for fibre in fibres)
        for generator in pair_generators
    ]
    quotient_group = close_group(quotient_generators, 40)
    quotient_stabilizer, quotient_suborbits = stabilizer_suborbits(
        quotient_group, 0, 40
    )
    assert len(quotient_group) == 25920
    assert len(quotient_stabilizer) == 648
    assert list(map(len, quotient_suborbits)) == [1, 12, 27]

    quotient_adjacency = np.zeros((40, 40), dtype=np.int64)
    for left, right in combinations(range(40), 2):
        block = adjacency_matrices[1][np.ix_(fibres[left], fibres[right])]
        if int(block.sum()) == 9:
            quotient_adjacency[left, right] = quotient_adjacency[right, left] = 1
    assert set(map(int, quotient_adjacency.sum(axis=1))) == {12}
    square = quotient_adjacency @ quotient_adjacency
    assert set(map(int, square[quotient_adjacency == 1])) == {2}
    mask = (quotient_adjacency == 0) & (~np.eye(40, dtype=bool))
    assert set(map(int, square[mask])) == {4}

    block_checks = {}
    for relation in (1, 2, 4):
        patterns = Counter()
        for left, right in combinations(range(40), 2):
            block = adjacency_matrices[relation][np.ix_(fibres[left], fibres[right])]
            patterns[
                (
                    tuple(map(int, block.sum(axis=1))),
                    tuple(map(int, block.sum(axis=0))),
                    int(block.sum()),
                )
            ] += 1
        block_checks[str(relation)] = {
            str(key): value for key, value in sorted(patterns.items(), key=lambda item: str(item[0]))
        }
    assert sorted(value for value in block_checks["1"].values()) == [240, 540]
    assert sorted(value for value in block_checks["2"].values()) == [240, 540]
    assert sorted(value for value in block_checks["4"].values()) == [240, 540]

    def matching(left, right):
        block = adjacency_matrices[2][np.ix_(fibres[left], fibres[right])]
        assert np.all(block.sum(axis=1) == 1)
        assert np.all(block.sum(axis=0) == 1)
        return tuple(int(np.argmax(block[row])) for row in range(3))

    def compose_small(left, right):
        return tuple(left[right[index]] for index in range(len(right)))

    complement = np.ones((40, 40), dtype=np.int64) - np.eye(40, dtype=np.int64) - quotient_adjacency
    holonomy = Counter()
    for left, middle, right in combinations(range(40), 3):
        if complement[left, middle] and complement[middle, right] and complement[right, left]:
            loop = compose_small(
                matching(right, left),
                compose_small(matching(middle, right), matching(left, middle)),
            )
            holonomy[cycle_type(loop)] += 1
    assert holonomy == Counter({(1, 1, 1): 1080, (1, 2): 2160})

    base_faces = sorted(face for pair_id in fibres[0] for face in pairs[pair_id])
    assert base_faces == [0, 46, 83, 120, 148, 176]
    base_face_index = {face: index for index, face in enumerate(base_faces)}
    local_group = {
        tuple(base_face_index[element[face]] for face in base_faces)
        for element in face_group
        if {element[face] for face in base_faces} == set(base_faces)
    }
    tetrahedron_edges = list(combinations(range(4), 2))
    standard_edge_action = {
        tuple(
            tetrahedron_edges.index(
                tuple(sorted((permutation[left], permutation[right])))
            )
            for left, right in tetrahedron_edges
        )
        for permutation in permutations(range(4))
    }
    assert local_group == standard_edge_action
    antipodal_local_pairs = [(0, 5), (1, 4), (2, 3)]
    pair_labels = {pair: index for index, pair in enumerate(antipodal_local_pairs)}
    local_pair_actions = set()
    local_pair_kernel = []
    for element in local_group:
        action = tuple(
            pair_labels[tuple(sorted((element[left], element[right])))]
            for left, right in antipodal_local_pairs
        )
        local_pair_actions.add(action)
        if action == (0, 1, 2):
            local_pair_kernel.append(element)
    assert len(local_pair_actions) == 6
    assert len(local_pair_kernel) == 4
    assert all(cycle_type(element) in {(1, 1, 1, 1, 1, 1), (1, 1, 2, 2)} for element in local_pair_kernel)

    return {
        "face_action": {
            "degree": 240,
            "rank": len(face_suborbits),
            "stabilizer_order": len(face_stabilizer),
            "subdegrees": list(map(len, face_suborbits)),
            "antipodal_pairs": 120,
        },
        "pair_scheme": {
            "degree": 120,
            "rank": 5,
            "valencies": list(map(len, pair_suborbits)),
            "eigenmatrix_rows_with_multiplicity": eigenmatrix,
            "intersection_numbers": intersection.tolist(),
            "valency_two_relation_components": [40, 3],
        },
        "quotient": {
            "degree": 40,
            "subdegrees": list(map(len, quotient_suborbits)),
            "srg": [40, 12, 2, 4],
            "block_laws": {
                "W33_edge": "relation 1 is J3 on every quotient edge",
                "W33_nonedge_matching": "relation 2 is a 3x3 permutation matrix",
                "W33_nonedge_complement": "relation 4 is J3 minus relation 2",
            },
            "matching_triangle_holonomy": {
                "identity": holonomy[(1, 1, 1)],
                "transposition": holonomy[(1, 2)],
                "three_cycle": 0,
            },
        },
        "local_tetrahedral_chart": {
            "six_face_ids": base_faces,
            "tetrahedron_edge_labels": [list(edge) for edge in tetrahedron_edges],
            "induced_group": "S4 on six tetrahedron edges",
            "induced_group_order": len(local_group),
            "three_antipodal_pairs": [list(pair) for pair in antipodal_local_pairs],
            "pair_action": "S3",
            "pair_kernel": "V4",
            "point_stabilizer": "3^3:S4",
            "point_stabilizer_order": len(quotient_stabilizer),
        },
        "_matrices": {
            "face_relations": face_relations,
            "pair_relations": pair_relations,
            "pair_adjacencies": adjacency_matrices,
            "pairs": pairs,
        },
    }


def modular_certificate(tower):
    face_relations = tower["_matrices"]["face_relations"]
    pair_adjacencies = tower["_matrices"]["pair_adjacencies"]
    pairs = tower["_matrices"]["pairs"]

    common_characters = [
        [value % 3 for value in row]
        for _, row in tower["pair_scheme"]["eigenmatrix_rows_with_multiplicity"]
    ]
    assert len({tuple(row) for row in common_characters}) == 1
    assert common_characters[0] == [1, 0, 0, 2, 0]

    radical = [
        pair_adjacencies[1] % 3,
        pair_adjacencies[2] % 3,
        pair_adjacencies[4] % 3,
        (pair_adjacencies[0] + pair_adjacencies[3]) % 3,
    ]
    radical_square = [
        left @ right % 3 for left in radical for right in radical
    ]
    radical_cube = [
        left @ right % 3 for left in radical_square for right in radical
    ]
    radical_dims = [
        span_rank_mod(radical),
        span_rank_mod(radical_square),
        span_rank_mod(radical_cube),
    ]
    assert radical_dims == [4, 1, 0]

    face_adjacencies = [
        (face_relations == relation).astype(np.int64)
        for relation in range(10)
    ]
    plus_inclusion = np.zeros((240, 120), dtype=np.int64)
    minus_inclusion = np.zeros((240, 120), dtype=np.int64)
    plus_projection = np.zeros((120, 240), dtype=np.int64)
    minus_projection = np.zeros((120, 240), dtype=np.int64)
    for column, (left, right) in enumerate(pairs):
        plus_inclusion[left, column] = plus_inclusion[right, column] = 1
        minus_inclusion[left, column] = 1
        minus_inclusion[right, column] = -1
        plus_projection[column, left] = plus_projection[column, right] = 2
        minus_projection[column, left] = 2
        minus_projection[column, right] = 1
    plus_endomorphisms = [
        plus_projection @ adjacency @ plus_inclusion % 3
        for adjacency in face_adjacencies
    ]
    minus_endomorphisms = [
        minus_projection @ adjacency @ (minus_inclusion % 3) % 3
        for adjacency in face_adjacencies
    ]
    plus_indices, plus_basis = independent_basis(plus_endomorphisms)
    minus_indices, minus_basis = independent_basis(minus_endomorphisms)
    assert len(plus_basis) == 5
    assert len(minus_basis) == 3
    assert minus_indices == [0, 1, 2]

    multiplication = []
    for left in minus_basis:
        row = []
        for right in minus_basis:
            row.append(coordinates_in_basis(left @ right % 3, minus_basis))
        multiplication.append(row)
    assert multiplication == [
        [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
        [[0, 1, 0], [0, 0, 2], [0, 0, 1]],
        [[0, 0, 1], [0, 0, 1], [0, 0, 2]],
    ]
    identity, x, y = minus_basis
    idempotent_81 = 2 * y % 3
    assert np.array_equal(idempotent_81 @ idempotent_81 % 3, idempotent_81)
    assert rank_mod(idempotent_81) == 81
    assert rank_mod(identity - idempotent_81) == 39
    nilpotent_39 = (x + y) % 3
    complement_39 = (identity - idempotent_81) % 3
    nilpotent_39 = complement_39 @ nilpotent_39 @ complement_39 % 3
    assert np.any(nilpotent_39)
    assert not np.any(nilpotent_39 @ nilpotent_39 % 3)

    minus_projection_real = np.zeros((120, 240), dtype=float)
    for column, (left, right) in enumerate(pairs):
        minus_projection_real[column, left] = 0.5
        minus_projection_real[column, right] = -0.5
    minus_real = [
        minus_projection_real @ adjacency @ minus_inclusion
        for adjacency in face_adjacencies
    ]
    generic_minus = sum(
        (index + 1) * (matrix + matrix.T)
        for index, matrix in enumerate(minus_real)
    )
    eigenvalues = np.linalg.eigvalsh(generic_minus)
    used = np.zeros(120, dtype=bool)
    multiplicities = []
    for index, value in enumerate(eigenvalues):
        if used[index]:
            continue
        members = np.flatnonzero(np.abs(eigenvalues - value) < 1e-6)
        used[members] = True
        multiplicities.append(len(members))
    assert sorted(multiplicities) == [15, 24, 81]

    return {
        "pair_module": {
            "dimension": 120,
            "endomorphism_dimension": len(plus_basis),
            "ordinary_multiplicities": [1, 15, 20, 24, 60],
            "all_ordinary_characters_mod3": common_characters[0],
            "endomorphism_radical_dimensions_J_J2_J3": radical_dims,
            "endomorphism_loewy_layers": [1, 3, 1],
            "indecomposable": True,
        },
        "antisymmetric_module": {
            "dimension": 120,
            "endomorphism_dimension": len(minus_basis),
            "ordinary_multiplicities": sorted(multiplicities),
            "basis_indices": minus_indices,
            "multiplication_table": multiplication,
            "decomposition_dimensions": [81, 39],
            "rank_81_idempotent": 81,
            "rank_39_complement": 39,
            "rank_39_endomorphism_ring": "F3[epsilon]/(epsilon^2)",
            "ordinary_39_gluing": "15+24",
            "boundary": "The 81-dimensional brick is not promoted to a simple module without an independent MeatAxe composition-series calculation.",
        },
        "full_face_module": {
            "dimension": 240,
            "decomposition": "M_plus(120) direct-sum M_minus(81+39)",
            "ordinary_fingerprint": "1+15a+15b+20+2*24+60+81",
        },
    }


def delsarte_certificate(tower):
    local = (1, 726, 58322)
    target = Q ** 436
    threshold, before, at = sphere_threshold(local, 240, target)
    assert threshold == 389
    ratio = float(at / target)
    return {
        "fractional_cover_threshold": threshold,
        "sphere_388_below_target": before < target,
        "sphere_389_above_target": at >= target,
        "sphere_389_over_quotient_numeric": ratio,
        "level_zero_verdict": "The transitive fractional/Delsarte covering relaxation reproduces radius 389 and cannot improve the existing lower bound.",
        "level_two_exact_deck": {
            "face_coherent_rank": tower["face_action"]["rank"],
            "antipodal_pair_scheme_rank": tower["pair_scheme"]["rank"],
            "pair_valencies": tower["pair_scheme"]["valencies"],
            "pair_eigenmatrix_rows_with_multiplicity": tower["pair_scheme"]["eigenmatrix_rows_with_multiplicity"],
            "pair_intersection_numbers": tower["pair_scheme"]["intersection_numbers"],
        },
        "boundary": "The exact radius remains open in [389,436]; the packet closes the symmetry-reduced input deck, not the higher-level SDP optimum.",
    }


def m4_certificate(tower):
    transpositions = []
    for left, right in combinations(range(4), 2):
        permutation = list(range(4))
        permutation[left], permutation[right] = permutation[right], permutation[left]
        matrix = np.zeros((4, 4), dtype=int)
        for source, target in enumerate(permutation):
            matrix[target, source] = 1
        transpositions.append(matrix)
    dual_sign = np.diag([1, 1, -1, -1])
    group_algebra_dimension = algebra_dimension(transpositions)
    crossed_dimension = algebra_dimension(transpositions + [dual_sign])
    assert group_algebra_dimension == 10
    assert crossed_dimension == 16

    return {
        "untwisted_invariant_no_go": (
            "A PSp-invariant trivial-bundle M4 weighting twirls into the existing "
            "three block spectral cones, so enlarging the local algebra alone cannot "
            "improve the old Hoffman frontier."
        ),
        "objectwise_transport": {
            "local_tokens": "six filled faces over each W33 point",
            "local_matrices": "six S4 transposition permutation matrices on four channels",
            "antipodal_faces": "three pairs of disjoint commuting transpositions",
            "nonedge_transport": "S3-valued matching connection",
            "triangle_holonomy": tower["quotient"]["matching_triangle_holonomy"],
        },
        "algebra_dimensions": {
            "S4_transposition_group_algebra_image": group_algebra_dimension,
            "plus_null_conic_dual_sign": crossed_dimension,
            "target_full_M4": 16,
        },
        "verdict": (
            "The phase-only and untwisted full-M4 dead ends are closed. The first "
            "objectwise noncommuting amplitude compiler is now explicit, but it is "
            "not yet a chromatic certificate on the live 45-block carrier."
        ),
    }


def hardware_certificate():
    modular_symbol = np.array([
        [2, 1, 1, 0, 0],
        [2, 1, 0, 1, 0],
        [2, 0, 1, 1, 0],
        [0, 2, 2, 0, 0],
        [0, 0, 0, 0, 1],
    ], dtype=np.int64)
    assert np.array_equal(
        np.linalg.matrix_power(modular_symbol, 3) % 3,
        np.eye(5, dtype=np.int64),
    )
    factored_source_entries = 4
    literal_mask_entries = 8 * 25
    naive_momentum_entries = 27 * 25
    return {
        "mod3_order": 3,
        "valid_input_states": 3 ** 5,
        "formal_depth": 3,
        "literal_table_entries": literal_mask_entries,
        "naive_27_symbol_entries": naive_momentum_entries,
        "entry_reduction_factor": naive_momentum_entries / literal_mask_entries,
        "factored_primitive_entries": factored_source_entries,
        "workflow_targets": [
            "exhaustive Icarus equivalence for 8*25 entries",
            "Yosys SAT proof of J^3=I on all 3^5 ternary states",
            "Yosys ICE40 synthesis of factored and literal-table baselines",
        ],
        "boundary": "No FPGA area, timing, or optimality result is claimed before the remote evidence job completes.",
    }


def product_code_and_reye_certificate():
    generator = np.array([
        [1,0,2,2,0,1,0,0,0,0,0,0],
        [0,1,2,0,2,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,0,2,2,0,1],
        [0,0,0,0,0,0,0,1,2,0,2,1],
        [1,0,2,1,0,2,1,0,2,1,0,2],
        [0,1,2,0,1,2,0,1,2,0,1,2],
    ], dtype=np.int64) % 3
    words = np.array([
        np.array(coefficients, dtype=np.int64) @ generator % 3
        for coefficients in product(range(3), repeat=6)
    ])
    weight_histogram = Counter(int(np.count_nonzero(word)) for word in words)
    assert weight_histogram == Counter({0:1,4:36,6:84,7:144,8:162,9:152,10:144,12:6})
    weight_four_supports = {
        tuple(np.flatnonzero(word).tolist())
        for word in words if np.count_nonzero(word) == 4
    }
    assert len(weight_four_supports) == 18

    syndrome_counts = Counter()
    for support in combinations(range(12), 3):
        for values in product((1, 2), repeat=3):
            word = np.zeros(12, dtype=np.int64)
            word[list(support)] = values
            syndrome_counts[tuple((generator @ word) % 3)] += 1
    histogram = Counter(syndrome_counts.values())
    assert histogram == Counter({1:48,2:312,4:270,8:1})
    assert max(syndrome_counts.values()) == 8
    max_projective_weight_three_supports = 4

    matchings = [
        [(0,1),(2,3)],
        [(0,2),(1,3)],
        [(0,3),(1,2)],
    ]
    oriented_edges = []
    for matching in matchings:
        for vertex in range(4):
            edge = next(edge for edge in matching if vertex in edge)
            other = edge[0] if edge[1] == vertex else edge[1]
            oriented_edges.append((vertex, other))
    oriented_index = {edge: index for index, edge in enumerate(oriented_edges)}
    lines = []
    labels = []
    for vertex in range(4):
        lines.append(tuple(sorted(
            oriented_index[(vertex, other)]
            for other in range(4) if other != vertex
        )))
        labels.append(f"O{vertex}")
    for vertex in range(4):
        lines.append(tuple(sorted(
            oriented_index[(other, vertex)]
            for other in range(4) if other != vertex
        )))
        labels.append(f"I{vertex}")
    for vertices in combinations(range(4), 3):
        left, middle, right = vertices
        lines.append(tuple(sorted([
            oriented_index[(left, middle)],
            oriented_index[(middle, right)],
            oriented_index[(right, left)],
        ])))
        labels.append(f"C{left}{middle}{right}+")
        lines.append(tuple(sorted([
            oriented_index[(left, right)],
            oriented_index[(right, middle)],
            oriented_index[(middle, left)],
        ])))
        labels.append(f"C{left}{middle}{right}-")
    assert len(set(lines)) == 16
    incidences = Counter(item for line in lines for item in line)
    assert set(incidences.values()) == {4}

    line_set = set(lines)
    visible_stabilizer = []
    for matching_permutation in permutations(range(3)):
        for vertex_permutation in permutations(range(4)):
            coordinate_permutation = tuple(
                matching_permutation[matching] * 4 + vertex_permutation[vertex]
                for matching in range(3)
                for vertex in range(4)
            )
            transported = {
                tuple(sorted(coordinate_permutation[item] for item in line))
                for line in lines
            }
            if transported == line_set:
                visible_stabilizer.append(
                    [list(matching_permutation), list(vertex_permutation)]
                )
    assert len(visible_stabilizer) == 72

    return {
        "product_code_falsifier": {
            "parameters": [12, 6, 4],
            "weight_four_projective_supports": len(weight_four_supports),
            "weight_three_vectors_examined": 1760,
            "weight_three_coset_histogram": dict(sorted(histogram.items())),
            "maximum_weight_three_vectors_in_one_dual_coset": 8,
            "maximum_projective_triples_in_one_dual_coset": max_projective_weight_three_supports,
            "tomotope_triangular_faces_required": 16,
            "verdict": "No coset of the dual product code can supply the sixteen tomotope face supports.",
            "visible_product_action_order": 144,
            "tomotope_automorphism_order": 96,
            "faithful_visible_action_obstructed_by_lagrange": 144 % 96 != 0,
        },
        "oriented_tetrahedron_incidence": {
            "coordinates": [list(edge) for edge in oriented_edges],
            "line_labels": labels,
            "lines": [list(line) for line in lines],
            "configuration": [12, 4, 16, 3],
            "description": (
                "Four outgoing stars, four incoming stars, and eight directed "
                "3-cycles form a 12_4 16_3 oriented-tetrahedron incidence surface."
            ),
            "visible_parity_matched_S3xS4_subgroup_order": len(visible_stabilizer),
            "boundary": (
                "This is a concrete Reye-style coordinate surface. An isomorphism "
                "to the archived tomotope flag monodromy still requires the missing "
                "cell/orientation data; the Reye skeleton alone is known to be insufficient."
            ),
        },
    }


def build_certificate():
    objects = geometry_objects()
    tower = face_tower_certificate(objects)
    modular = modular_certificate(tower)
    delsarte = delsarte_certificate(tower)
    m4 = m4_certificate(tower)
    hardware = hardware_certificate()
    tomotope = product_code_and_reye_certificate()

    checks = {
        "face_tower_240_120_40": (
            tower["face_action"]["degree"] == 240
            and tower["face_action"]["antipodal_pairs"] == 120
            and tower["quotient"]["degree"] == 40
        ),
        "pair_scheme_rank5": tower["pair_scheme"]["rank"] == 5,
        "W33_recovered_objectwise": tower["quotient"]["srg"] == [40,12,2,4],
        "S3_holonomy_nontrivial": tower["quotient"]["matching_triangle_holonomy"] == {
            "identity": 1080, "transposition": 2160, "three_cycle": 0
        },
        "local_stabilizer_3cubed_S4": (
            tower["local_tetrahedral_chart"]["induced_group_order"] == 24
        ),
        "Delsarte_level0_no_improvement": delsarte["fractional_cover_threshold"] == 389,
        "pair_module_local_endomorphism_ring": (
            modular["pair_module"]["endomorphism_radical_dimensions_J_J2_J3"] == [4,1,0]
        ),
        "antisymmetric_81_plus_39": (
            modular["antisymmetric_module"]["decomposition_dimensions"] == [81,39]
        ),
        "objectwise_crossed_algebra_full_M4": (
            m4["algebra_dimensions"]["plus_null_conic_dual_sign"] == 16
        ),
        "formal_order3_source_target": hardware["mod3_order"] == 3,
        "product_code_tomotope_support_no_go": (
            tomotope["product_code_falsifier"]["maximum_projective_triples_in_one_dual_coset"] < 16
        ),
        "oriented_tetrahedron_12_4_16_3": (
            tomotope["oriented_tetrahedron_incidence"]["configuration"] == [12,4,16,3]
        ),
    }
    assert all(checks.values()), checks

    del tower["_matrices"]
    return {
        "schema": "w33.bt3458_3471.face_tower_brauer_tomotope.v1",
        "status": "PASS",
        "checks": checks,
        "sections": {
            "association_scheme_and_face_tower": tower,
            "delsarte_radius": delsarte,
            "characteristic_three_descent": modular,
            "full_M4_amplitude_compiler": m4,
            "formal_hardware": hardware,
            "tomotope_product_code": tomotope,
        },
        "boundaries": {
            "covering_radius": "open in [389,436]",
            "chromatic_number": "open in {10,11}",
            "modular": "no simple-module claim for the 81-dimensional brick without MeatAxe",
            "tomotope": "no flag-monodromy identification from the Reye-style skeleton alone",
            "hardware": "no observed synthesis, timing, or PDF result before remote evidence completes",
            "physics": "no physical fibre, particle, spacetime, or gauge-field identification",
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", type=Path)
    arguments = parser.parse_args()
    payload = build_certificate()
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if arguments.json:
        arguments.json.parent.mkdir(parents=True, exist_ok=True)
        arguments.json.write_text(text, encoding="utf-8")
    print("PASS 12/12 face tower, Delsarte, modular, M4, hardware, and tomotope checks")
    print(text, end="")


if __name__ == "__main__":
    main()
