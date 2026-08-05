#!/usr/bin/env python3
"""Passes 3444--3457: radius reduction, modular descent, five-channel closure."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from itertools import combinations, permutations, product
from pathlib import Path

import numpy as np
from sympy import Matrix

P = 3
Q = 3 ** 5


def add(a: int, b: int) -> int:
    return a ^ b


def multiply(x: int, y: int) -> int:
    a0, a1 = x & 1, (x >> 1) & 1
    b0, b1 = y & 1, (y >> 1) & 1
    c0 = (a0 * b0) ^ (a1 * b1)
    c1 = (a0 * b1) ^ (a1 * b0) ^ (a1 * b1)
    return c0 | (c1 << 1)


def inverse(x: int) -> int:
    assert x
    return multiply(x, x)


def conjugate(x: int) -> int:
    return multiply(x, x)


def canonical(vector: tuple[int, ...]) -> tuple[int, ...]:
    pivot = next(value for value in vector if value)
    scale = inverse(pivot)
    return tuple(multiply(scale, value) for value in vector)


def hermitian(x, y) -> int:
    result = 0
    for left, right in zip(x, y):
        result = add(result, multiply(left, conjugate(right)))
    return result


def points_and_graph():
    points = sorted({
        canonical(vector)
        for vector in product(range(4), repeat=4)
        if any(vector) and sum(value != 0 for value in vector) % 2 == 0
    })
    assert len(points) == 45
    index = {point: position for position, point in enumerate(points)}
    collinear = np.zeros((45, 45), dtype=np.int8)
    for left, right in combinations(range(45), 2):
        if hermitian(points[left], points[right]) == 0:
            collinear[left, right] = collinear[right, left] = 1
    graph = np.ones((45, 45), dtype=np.int8) - np.eye(45, dtype=np.int8) - collinear
    assert set(graph.sum(axis=1).tolist()) == {32}
    return points, index, graph


def transvection(points, index, vector):
    image = []
    for point in points:
        scalar = hermitian(point, vector)
        moved = tuple(add(point[i], multiply(scalar, vector[i])) for i in range(4))
        image.append(index[canonical(moved)])
    return tuple(image)


def compose(left, right):
    return tuple(left[right[i]] for i in range(len(left)))


def close_group(generators, size=45):
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


def small_generators(points, index):
    transvections = sorted({transvection(points, index, vector) for vector in points})
    selected = []
    last_size = 1
    growth = []
    for candidate in transvections:
        group = close_group(selected + [candidate])
        if len(group) > last_size:
            selected.append(candidate)
            last_size = len(group)
            growth.append(last_size)
        if last_size == 25920:
            return selected, group, growth
    raise RuntimeError("unitary transvections did not generate PSU(4,2)")


def rank_mod(matrix, p=3) -> int:
    a = np.array(matrix, dtype=np.int64) % p
    rows, cols = a.shape
    rank = 0
    for col in range(cols):
        pivot = next((row for row in range(rank, rows) if a[row, col] % p), None)
        if pivot is None:
            continue
        if pivot != rank:
            a[[rank, pivot]] = a[[pivot, rank]]
        a[rank] = a[rank] * pow(int(a[rank, col]), -1, p) % p
        for row in range(rows):
            if row != rank and a[row, col] % p:
                a[row] = (a[row] - a[row, col] * a[rank]) % p
        rank += 1
        if rank == rows:
            break
    return rank


def geometry_objects():
    points, point_index, graph = points_and_graph()
    generators, group, growth = small_generators(points, point_index)
    triangles = [
        triple for triple in combinations(range(45), 3)
        if graph[triple[0], triple[1]]
        and graph[triple[0], triple[2]]
        and graph[triple[1], triple[2]]
    ]
    assert len(triangles) == 5280
    triangle_index = {triangle: i for i, triangle in enumerate(triangles)}
    triangle_generators = [
        tuple(
            triangle_index[tuple(sorted(generator[v] for v in triangle))]
            for triangle in triangles
        )
        for generator in generators
    ]
    unseen = set(range(len(triangles)))
    triangle_orbits = []
    while unseen:
        start = min(unseen)
        orbit = {start}
        frontier = [start]
        while frontier:
            new = []
            for item in frontier:
                for generator in triangle_generators:
                    image = generator[item]
                    if image not in orbit:
                        orbit.add(image)
                        new.append(image)
            frontier = new
        unseen.difference_update(orbit)
        triangle_orbits.append(sorted(orbit))
    orbit_sizes = sorted(len(orbit) for orbit in triangle_orbits)
    assert orbit_sizes == [240, 2160, 2880]
    filled_ids = next(orbit for orbit in triangle_orbits if len(orbit) == 240)
    faces = [triangles[index] for index in filled_ids]

    edges = [(i, j) for i in range(45) for j in range(i + 1, 45) if graph[i, j]]
    edge_index = {edge: i for i, edge in enumerate(edges)}
    assert len(edges) == 720
    relation = np.zeros((720, 240), dtype=np.int8)
    edge_multiplicity = Counter()
    for face_id, face in enumerate(faces):
        for edge in combinations(face, 2):
            edge = tuple(sorted(edge))
            relation[edge_index[edge], face_id] = 1
            edge_multiplicity[edge] += 1
    assert len(edge_multiplicity) == 720
    assert set(edge_multiplicity.values()) == {1}

    incidence = np.zeros((720, 45), dtype=np.int8)
    for edge_id, (left, right) in enumerate(edges):
        incidence[edge_id, left] = 1
        incidence[edge_id, right] = 1

    relation_rank = rank_mod(relation)
    incidence_rank = rank_mod(incidence)
    combined = np.concatenate([relation, incidence], axis=1)
    combined_rank = rank_mod(combined)
    assert (relation_rank, incidence_rank, combined_rank) == (240, 45, 284)

    ones_edges = np.ones(720, dtype=np.int8)
    assert np.array_equal(relation @ np.ones(240, dtype=np.int8) % 3, ones_edges)
    assert np.array_equal(incidence @ np.ones(45, dtype=np.int8) % 3, 2 * ones_edges % 3)

    return {
        "points": points,
        "graph": graph,
        "generators": generators,
        "group": group,
        "growth": growth,
        "faces": faces,
        "edges": edges,
        "relation": relation,
        "incidence": incidence,
        "orbit_sizes": orbit_sizes,
        "ranks": [relation_rank, incidence_rank, combined_rank],
    }


def integer_digest(value: int) -> dict:
    text = str(value)
    return {
        "decimal_digits": len(text),
        "bit_length": value.bit_length(),
        "sha256_decimal": hashlib.sha256(text.encode("ascii")).hexdigest(),
    }


def sphere_threshold(local_enumerator: tuple[int, int, int], factors: int, target: int):
    coefficients = [1]
    for _ in range(factors):
        updated = [0] * (len(coefficients) + 2)
        for degree, value in enumerate(coefficients):
            updated[degree] += local_enumerator[0] * value
            updated[degree + 1] += local_enumerator[1] * value
            updated[degree + 2] += local_enumerator[2] * value
        coefficients = updated
    cumulative = 0
    for radius, value in enumerate(coefficients):
        cumulative += value
        if cumulative >= target:
            return radius, cumulative - value, cumulative
    raise AssertionError("sphere threshold not reached")


def radius_certificate(objects) -> dict:
    from math import comb

    q = Q
    local = (1, 3 * (q - 1), q * q - 1 - 3 * (q - 1))
    assert local == (1, 726, 58322)
    target = q ** 436
    radius, before, at = sphere_threshold(local, 240, target)

    cumulative = 0
    ordinary = None
    for r in range(721):
        cumulative += comb(720, r) * (q - 1) ** r
        if cumulative >= target:
            ordinary = r
            break
    assert ordinary == 347
    assert radius == 389

    local_srg = {
        "vertices": q * q,
        "degree": 3 * (q - 1),
        "lambda": q,
        "mu": 6,
        "spectrum": {
            str(3 * (q - 1)): 1,
            str(q - 3): 3 * (q - 1),
            "-3": (q - 1) * (q - 2),
        },
    }
    assert local_srg == {
        "vertices": 59049,
        "degree": 726,
        "lambda": 243,
        "mu": 6,
        "spectrum": {"726": 1, "240": 726, "-3": 58322},
    }

    return {
        "coefficient_identification": (
            "Choose any F3-linear identification F3^5 ~= F243. "
            "The labelled support metric is the fifth generalized covering radius "
            "R5(K), equivalently the ordinary covering radius of K extended to F243."
        ),
        "support_code": {
            "length": 720,
            "dimension_over_F3": 284,
            "redundancy": 436,
            "presentation": "K = im([face_relation_720x240, vertex_incidence_720x45])",
        },
        "local_A2_metric": {
            "description": "three-direction Latin-square Cayley graph on F243^2",
            "length_enumerator": list(local),
            "strongly_regular_parameters": local_srg,
        },
        "bounds": {
            "relation_aware_sphere_lower_bound": radius,
            "ordinary_F243_Hamming_sphere_lower_bound": ordinary,
            "basis_upper_bound": 436,
            "exact_interval": [389, 436],
        },
        "threshold_digests": {
            "radius_388": integer_digest(before),
            "radius_389": integer_digest(at),
            "quotient_size": integer_digest(target),
        },
        "status": (
            "The exact radius is not closed. The executed reduction identifies the "
            "correct generalized-covering and Latin-square association-scheme problem."
        ),
    }


def algebra_dimension(generators) -> int:
    size = generators[0].shape[0]
    basis = [np.eye(size, dtype=int)]
    changed = True
    while changed:
        changed = False
        for left in list(basis):
            for right in generators:
                for candidate in (left @ right, right @ left):
                    columns = [Matrix(matrix.reshape(size * size, 1)) for matrix in basis + [candidate]]
                    rank = Matrix.hstack(*columns).rank()
                    if rank > len(basis):
                        basis.append(candidate)
                        changed = True
    return len(basis)


def five_channel_certificate() -> dict:
    M = np.array([[0, 2], [1, 1]], dtype=int)
    I2 = np.eye(2, dtype=int)
    K1 = np.kron(I2, M)
    K2 = np.kron(M, I2)
    I4 = np.eye(4, dtype=int)
    swap = np.array([
        [1, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
    ], dtype=int)
    dual_sign = np.diag([1, 1, -1, -1])

    dimensions = {
        "torus_commutative": algebra_dimension([K1, K2]),
        "plus_swap": algebra_dimension([K1, K2, swap]),
        "plus_conic_dual_sign": algebra_dimension([K1, K2, dual_sign]),
        "plus_swap_and_conic_dual_sign": algebra_dimension([K1, K2, swap, dual_sign]),
    }
    assert dimensions == {
        "torus_commutative": 4,
        "plus_swap": 6,
        "plus_conic_dual_sign": 8,
        "plus_swap_and_conic_dual_sign": 16,
    }

    symbol_table = {}
    fingerprints = Counter()
    reduced_symbols = []
    for zero_mask in product((0, 1), repeat=3):
        c1, c2, c3 = (2 if bit else -1 for bit in zero_mask)
        block = c1 * K1 + c2 * K2 + c3 * I4
        hidden = c3 - c1 - c2
        full = np.zeros((5, 5), dtype=int)
        full[:4, :4] = block
        full[4, 4] = hidden
        key = "".join(map(str, zero_mask))
        symbol_table[key] = full.tolist()
        eigenvalues = []
        for value, multiplicity in Matrix(full).eigenvals().items():
            assert value.is_Integer
            eigenvalues.extend([int(value)] * int(multiplicity))
        fingerprints[tuple(sorted(eigenvalues))] += 1
        reduced_symbols.append(full % 3)

    assert len(fingerprints) == 6
    assert all(np.array_equal(reduced_symbols[0], item) for item in reduced_symbols[1:])
    J5 = reduced_symbols[0]
    nilpotent = (J5 - np.eye(5, dtype=int)) % 3
    ranks = [
        rank_mod(nilpotent),
        rank_mod(nilpotent @ nilpotent % 3),
        rank_mod(nilpotent @ nilpotent @ nilpotent % 3),
    ]
    assert ranks == [2, 1, 0]
    assert np.array_equal(np.linalg.matrix_power(J5, 3) % 3, np.eye(5, dtype=int))

    return {
        "binary_quotient_primitive": {
            "matrix": M.tolist(),
            "interpretation": "equitable 1+2 quotient of K3",
            "eigenvalues": [-1, 2],
        },
        "kronecker_sum": "B(k)=c1(I2 tensor M)+c2(M tensor I2)+c3 I4",
        "symbol_count": 8,
        "spectral_fingerprint_count": 6,
        "spectral_fingerprints": {
            str(key): value for key, value in sorted(fingerprints.items())
        },
        "symbol_table": symbol_table,
        "amplitude_algebra_dimensions": dimensions,
        "mod3_collapse": {
            "all_27_momenta_share_one_symbol": True,
            "matrix": J5.tolist(),
            "nilpotent_ranks_N_N2_N3": ranks,
            "jordan_type": "J3(1) + J1(1) + J1(1)",
            "order": 3,
        },
        "boundary": (
            "The torus amplitudes alone form a four-dimensional commutative algebra. "
            "The conic dual sign and one S4 coordinate swap generate full M4, providing "
            "a concrete noncommuting amplitude extension but not yet a chromatic certificate."
        ),
    }


def normalize_projective(vector, p):
    for value in vector:
        if value % p:
            scale = pow(int(value % p), -1, p)
            return tuple((scale * int(item)) % p for item in vector)
    raise ValueError("zero vector")


def conic_fano_d5_certificate() -> dict:
    conic = sorted({
        normalize_projective(vector, 3)
        for vector in product(range(3), repeat=3)
        if vector != (0, 0, 0)
        and (vector[0] ** 2 + vector[1] ** 2 - vector[2] ** 2) % 3 == 0
    })
    assert len(conic) == 4
    conic_index = {point: i for i, point in enumerate(conic)}
    conic_permutations = set()
    seen_projective = set()
    for entries in product(range(3), repeat=9):
        matrix = np.array(entries, dtype=int).reshape(3, 3)
        if rank_mod(matrix, 3) != 3:
            continue
        flat = tuple(int(x) for x in matrix.flatten())
        neg = tuple((-int(x)) % 3 for x in matrix.flatten())
        canonical_matrix = min(flat, neg)
        if canonical_matrix in seen_projective:
            continue
        seen_projective.add(canonical_matrix)
        images = tuple(
            normalize_projective(tuple((matrix @ np.array(point)) % 3), 3)
            for point in conic
        )
        if set(images) == set(conic):
            conic_permutations.add(tuple(conic_index[image] for image in images))
    assert len(conic_permutations) == 24

    fano_points = [vector for vector in product(range(2), repeat=3) if any(vector)]
    def xor(left, right):
        return tuple(a ^ b for a, b in zip(left, right))
    fano_lines = sorted({
        frozenset((left, right, xor(left, right)))
        for left, right in combinations(fano_points, 2)
        if left != right
    }, key=lambda line: sorted(line))
    assert len(fano_lines) == 7
    chosen_point = (1, 0, 0)
    outside_lines = [line for line in fano_lines if chosen_point not in line]
    assert len(outside_lines) == 4
    outside_index = {line: i for i, line in enumerate(outside_lines)}
    fano_permutations = set()
    stabilizer_order = 0
    for entries in product(range(2), repeat=9):
        matrix = np.array(entries, dtype=int).reshape(3, 3)
        if rank_mod(matrix, 2) != 3:
            continue
        image_point = tuple((matrix @ np.array(chosen_point)) % 2)
        if image_point != chosen_point:
            continue
        stabilizer_order += 1
        images = []
        for line in outside_lines:
            image_line = frozenset(tuple((matrix @ np.array(point)) % 2) for point in line)
            images.append(outside_index[image_line])
        fano_permutations.add(tuple(images))
    assert stabilizer_order == 24
    assert len(fano_permutations) == 24

    symmetric_four = set(permutations(range(4)))
    assert conic_permutations == symmetric_four
    assert fano_permutations == symmetric_four

    return {
        "conic": {
            "points": [list(point) for point in conic],
            "faithful_action_order": len(conic_permutations),
        },
        "fano": {
            "chosen_point": list(chosen_point),
            "nonincident_lines": [sorted(map(list, line)) for line in outside_lines],
            "point_stabilizer_order": stabilizer_order,
            "faithful_action_order": len(fano_permutations),
        },
        "D5": {
            "W_D5_order": 1920,
            "chosen_coordinate_stabilizer_order": 384,
            "sign_kernel_order": 16,
            "quotient_action": "S4 on the remaining four coordinates",
        },
        "bridge": (
            "After choosing one Fano point and one D5 coordinate, the conic points, "
            "the four Fano lines avoiding the point, and the four remaining D5 coordinates "
            "carry the same full S4 permutation action."
        ),
        "boundary": "The choices are essential; no canonical ambient-geometry identification is claimed.",
    }


def nullspace_basis_mod(matrix, p=3):
    a = np.array(matrix, dtype=int) % p
    rows, cols = a.shape
    rank = 0
    pivots = []
    for col in range(cols):
        pivot = next((row for row in range(rank, rows) if a[row, col]), None)
        if pivot is None:
            continue
        a[[rank, pivot]] = a[[pivot, rank]]
        a[rank] = a[rank] * pow(int(a[rank, col]), -1, p) % p
        for row in range(rows):
            if row != rank and a[row, col]:
                a[row] = (a[row] - a[row, col] * a[rank]) % p
        pivots.append(col)
        rank += 1
    free = [col for col in range(cols) if col not in pivots]
    basis = []
    for free_col in free:
        vector = np.zeros(cols, dtype=int)
        vector[free_col] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = (-a[row, free_col]) % p
        basis.append(vector)
    return np.array(basis, dtype=int)


def product_code_certificate() -> dict:
    inner = np.array([[1, 0, 2], [0, 1, 2]], dtype=int)
    outer = np.array([
        [1, 2, 0, 0],
        [0, 0, 1, 2],
        [1, 1, 1, 1],
    ], dtype=int)
    generator = np.kron(outer, inner) % 3
    assert rank_mod(generator) == 6
    weights = Counter()
    for message in product(range(3), repeat=6):
        word = np.array(message, dtype=int) @ generator % 3
        weights[int(np.count_nonzero(word))] += 1
    assert min(weight for weight in weights if weight) == 4

    dual = nullspace_basis_mod(generator)
    assert dual.shape == (6, 12)
    dual_weights = Counter()
    for message in product(range(3), repeat=6):
        word = np.array(message, dtype=int) @ dual % 3
        dual_weights[int(np.count_nonzero(word))] += 1

    return {
        "construction": "A2 [3,2,2]_3 tensor null-conic [4,3,2]_3",
        "parameters": "[12,6,4]_3",
        "generator_matrix": generator.tolist(),
        "weight_enumerator": {str(key): value for key, value in sorted(weights.items())},
        "dual_parameters": "[12,6,3]_3",
        "dual_weight_enumerator": {
            str(key): value for key, value in sorted(dual_weights.items())
        },
        "visible_coordinate_action": "S3 x S4 on the 3 x 4 slot grid",
        "boundary": (
            "The length twelve matches several repository carriers, including the tomotope "
            "edge count, but no tomotope incidence identification is promoted."
        ),
    }


def build_certificate() -> dict:
    objects = geometry_objects()
    relation, incidence = objects["relation"], objects["incidence"]
    dual_constraint_rank = rank_mod(np.concatenate([relation.T, incidence.T], axis=0))
    assert dual_constraint_rank == 284

    sections = {
        "generalized_covering_radius": radius_certificate(objects),
        "modular_exact_sequence": {
            "group": "PSU(4,2)=PSp(4,3)",
            "triangle_orbit_sizes": objects["orbit_sizes"],
            "filled_faces": 240,
            "edges": 720,
            "face_relation_rank": objects["ranks"][0],
            "vertex_incidence_rank": objects["ranks"][1],
            "combined_rank": objects["ranks"][2],
            "intersection_dimension": objects["ranks"][0] + objects["ranks"][1] - objects["ranks"][2],
            "flat_dimension": 720 - objects["ranks"][0],
            "coboundary_dimension_in_flat_quotient": objects["ranks"][2] - objects["ranks"][0],
            "cohomology_dimension": 720 - objects["ranks"][2],
            "exact_sequence": (
                "0 -> 1 -> F3[240 faces] + F3[45 vertices] -> "
                "F3[720 supports] -> H1 -> 0"
            ),
            "dual_conservation_code": (
                "H1* = {edge functions with zero sum on every filled face "
                "and zero sum at every vertex}"
            ),
            "dual_constraint_rank": dual_constraint_rank,
        },
        "five_channel_and_amplitudes": five_channel_certificate(),
        "S4_crosswalk": conic_fano_d5_certificate(),
        "A2_conic_product_code": product_code_certificate(),
    }

    checks = {
        "radius_reduced_to_generalized_covering": sections["generalized_covering_radius"]["bounds"]["exact_interval"] == [389, 436],
        "local_A2_SRG": sections["generalized_covering_radius"]["local_A2_metric"]["strongly_regular_parameters"]["mu"] == 6,
        "modular_ranks_240_45_284": objects["ranks"] == [240, 45, 284],
        "H1_dimension_436": sections["modular_exact_sequence"]["cohomology_dimension"] == 436,
        "dual_conservation_dimension_436": 720 - dual_constraint_rank == 436,
        "torus_algebra_dim4": sections["five_channel_and_amplitudes"]["amplitude_algebra_dimensions"]["torus_commutative"] == 4,
        "conic_crossed_algebra_full_M4": sections["five_channel_and_amplitudes"]["amplitude_algebra_dimensions"]["plus_swap_and_conic_dual_sign"] == 16,
        "all_symbols_mod3_order3": sections["five_channel_and_amplitudes"]["mod3_collapse"]["order"] == 3,
        "S4_bridge_24": sections["S4_crosswalk"]["conic"]["faithful_action_order"] == 24,
        "product_code_12_6_4": sections["A2_conic_product_code"]["parameters"] == "[12,6,4]_3",
    }
    assert all(checks.values()), checks
    return {
        "schema": "w33.bt3444_3457.radius_modular_fivechannel.v1",
        "status": "PASS",
        "sections": sections,
        "checks": checks,
        "boundaries": {
            "covering_radius": "still open in [389,436]",
            "chromatic_number": "still in {10,11}",
            "hardware": "RTL source and exhaustive simulation target only until remote synthesis evidence is observed",
            "physics": "finite root, conic, and modular correspondences are not physical identifications",
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    payload = build_certificate()
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(text, encoding="utf-8")
    print("PASS 10/10 radius, modular, five-channel, S4, and product-code checks")
    print(text, end="")


if __name__ == "__main__":
    main()
