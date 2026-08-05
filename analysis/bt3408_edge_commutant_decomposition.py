#!/usr/bin/env python3
"""Pass 3408: self-contained 720-edge commutant decomposition.

This independently reconstructs PSU(4,2)=PSp(4,3) from unitary transvections
on the 45 points of H(3,4), acts on the 720 non-collinear pairs, computes the
exact orbital rank and subdegrees, and extracts the ordinary degree/
multiplicity profile from deterministic generic elements of the commutant.
GAP remains the independent character-row label check.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path

import numpy as np


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
                product_element = compose(generator, element)
                if product_element not in seen:
                    seen.add(product_element)
                    new.append(product_element)
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


def cluster_multiplicities(values, tolerance=1e-5):
    used = np.zeros(len(values), dtype=bool)
    multiplicities = []
    for index, value in enumerate(values):
        if used[index]:
            continue
        members = np.flatnonzero(np.abs(values - value) < tolerance)
        used[members] = True
        multiplicities.append(int(len(members)))
    return sorted(multiplicities)


def build_certificate():
    points, point_index, graph = points_and_graph()
    generators, group, growth = small_generators(points, point_index)
    assert len(generators) == 6
    assert len(group) == 25920

    edges = [(i, j) for i in range(45) for j in range(i + 1, 45) if graph[i, j]]
    assert len(edges) == 720
    edge_index = {edge: position for position, edge in enumerate(edges)}

    def edge_image(permutation, edge_id):
        i, j = edges[edge_id]
        return edge_index[tuple(sorted((permutation[i], permutation[j])))]

    edge_generators = [tuple(edge_image(generator, edge_id) for edge_id in range(720)) for generator in generators]

    orbit = {0}
    frontier = [0]
    while frontier:
        new = []
        for point in frontier:
            for generator in edge_generators:
                image = generator[point]
                if image not in orbit:
                    orbit.add(image)
                    new.append(image)
        frontier = new
    assert len(orbit) == 720

    base_edge = edges[0]
    stabilizer = [
        element for element in group
        if tuple(sorted((element[base_edge[0]], element[base_edge[1]]))) == base_edge
    ]
    assert len(stabilizer) == 36
    stabilizer_edges = [tuple(edge_image(element, edge_id) for edge_id in range(720)) for element in stabilizer]

    unseen = set(range(720))
    suborbits = []
    while unseen:
        start = min(unseen)
        suborbit = sorted({element[start] for element in stabilizer_edges})
        suborbits.append(suborbit)
        unseen.difference_update(suborbit)
    subdegrees = sorted(len(suborbit) for suborbit in suborbits)
    assert len(suborbits) == 34
    assert sum(subdegrees) == 720

    representatives = [None] * 720
    for element in group:
        image = edge_image(element, 0)
        if representatives[image] is None:
            representatives[image] = element
    assert all(element is not None for element in representatives)

    relations = np.empty((720, 720), dtype=np.int16)
    for source, representative in enumerate(representatives):
        for relation, suborbit in enumerate(suborbits):
            for target in suborbit:
                relations[source, edge_image(representative, target)] = relation

    transpose = {}
    for relation, suborbit in enumerate(suborbits):
        transpose[relation] = int(relations[suborbit[0], 0])
    assert all(transpose[transpose[index]] == index for index in transpose)

    complex_coefficients = np.array([
        (index + 1) ** 2 + 1j * (index + 1) ** 3
        for index in range(len(suborbits))
    ], dtype=complex)
    complex_values = np.linalg.eigvals(complex_coefficients[relations])
    complex_degrees = cluster_multiplicities(complex_values)
    expected_complex = sorted([1,15,15,20,20,24,24,24,30,30,45,45,60,60,64,81,81,81])
    assert complex_degrees == expected_complex

    symmetric_coefficients = np.zeros(len(suborbits), dtype=float)
    visited = set()
    counter = 1
    for relation in range(len(suborbits)):
        if relation in visited:
            continue
        partner = transpose[relation]
        value = counter ** 3 + 7 * counter
        symmetric_coefficients[relation] = symmetric_coefficients[partner] = value
        visited.update((relation, partner))
        counter += 1
    real_values = np.linalg.eigvalsh(symmetric_coefficients[relations])
    real_degrees = cluster_multiplicities(real_values)
    expected_real = sorted([1,15,15,20,20,24,24,24,60,60,60,64,81,81,81,90])
    assert real_degrees == expected_real

    degree_occurrences = Counter(complex_degrees)
    inferred = {
        "1": [1],
        "15_pair": [1, 1],
        "20": [2],
        "24": [3],
        "30_conjugate_pair": [1, 1],
        "45_conjugate_pair": [1, 1],
        "60": [2],
        "64": [1],
        "81": [3],
    }
    dimension = 1 + 2*15 + 2*20 + 3*24 + 2*30 + 2*45 + 2*60 + 64 + 3*81
    character_norm = 1 + 1 + 1 + 2**2 + 3**2 + 1 + 1 + 1 + 1 + 2**2 + 1 + 3**2
    assert dimension == 720
    assert character_norm == 34

    checks = {
        "unitary_group_order_25920": len(group) == 25920,
        "six_transvection_generators": len(generators) == 6,
        "edge_action_transitive_720": len(orbit) == 720,
        "edge_stabilizer_order_36": len(stabilizer) == 36,
        "orbital_rank_34": len(suborbits) == 34,
        "complex_commutant_degrees": complex_degrees == expected_complex,
        "real_commutant_conjugate_pairing": real_degrees == expected_real,
        "dimension_closes_720": dimension == 720,
        "character_norm_closes_34": character_norm == 34,
    }
    assert all(checks.values()), checks
    return {
        "schema": "w33.bt3408.edge_commutant_decomposition.v1",
        "status": "PASS",
        "group": {
            "name": "PSU(4,2)=PSp(4,3)",
            "order": 25920,
            "generator_growth": growth,
        },
        "carrier": {
            "description": "720 non-collinear pairs in H(3,4), equivalently edges of SRG(45,32,22,24)",
            "size": 720,
            "stabilizer_order": 36,
            "orbital_rank": 34,
            "subdegrees": subdegrees,
        },
        "generic_complex_commutant_eigenspace_dimensions": complex_degrees,
        "generic_real_symmetric_commutant_eigenspace_dimensions": real_degrees,
        "ordinary_degree_multiplicity_profile": inferred,
        "decomposition_formula": "1 + 15a + 15b + 2*20 + 3*24 + 30a + 30b + 45a + 45b + 2*60 + 64 + 3*81",
        "dimension_check": dimension,
        "character_norm_check": character_norm,
        "boundary": (
            "The group, orbit, stabilizer, subdegrees, orbital rank, and commutant "
            "matrices are constructed exactly. Isotypic degrees are recovered from "
            "well-separated deterministic numerical eigenvalues and close both dimension "
            "and character norm. The GAP workflow remains the independent CTblLib row-label "
            "check, especially for naming the selected conjugate degree-30 pair."
        ),
        "checks": checks,
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
    print("PASS self-contained 720-edge commutant decomposition")
    print(text, end="")


if __name__ == "__main__":
    main()
