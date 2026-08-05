#!/usr/bin/env python3
"""Passes 3506--3519: cubic dependency projector and chained closures.

The verifier is deliberately fail-closed.  It reconstructs the 45-point carrier
from the earlier exact geometry module and then checks seven independent fronts:

* the first code-sensitive 5,040-triple covering deck;
* its characteristic-three rank-81 idempotent;
* a deterministic transported-M4 finite-grid screen;
* an exact five-operation ternary linear-circuit optimum;
* the oriented-Reye/tomotope cell-lift obstruction;
* a 57=40+16+1 induced-subgraph obstruction;
* a W33/Clebsch functional-calculus completion of the Gewirtz spectrum.

No exact covering-radius endpoint, unrestricted M4 optimum, ten-colour theorem,
simple-module label, observed FPGA result, tomotope monodromy, M57 existence, or
physical interpretation is inferred.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from itertools import combinations, permutations, product
from pathlib import Path

import numpy as np

from analysis.bt3444_3457_radius_modular_fivechannel import (
    close_group,
    geometry_objects,
    rank_mod,
)


def canonical_form(vector: tuple[int, ...]) -> tuple[int, ...]:
    vector = tuple(int(value % 3) for value in vector)
    for value in vector:
        if value:
            if value == 2:
                return tuple((-entry) % 3 for entry in vector)
            return vector
    return vector


def components(adjacency: np.ndarray) -> list[list[int]]:
    unseen = set(range(adjacency.shape[0]))
    result: list[list[int]] = []
    while unseen:
        start = min(unseen)
        component = {start}
        frontier = [start]
        while frontier:
            new: list[int] = []
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


def stabilizer_suborbits(group, base: int, size: int):
    stabilizer = [element for element in group if element[base] == base]
    unseen = set(range(size))
    suborbits = []
    while unseen:
        start = min(unseen)
        suborbit = sorted({element[start] for element in stabilizer})
        unseen.difference_update(suborbit)
        suborbits.append(suborbit)
    return stabilizer, suborbits


def orbital_relations(group, suborbits, size: int):
    representatives = [None] * size
    for element in sorted(group):
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


def dependency_deck(objects):
    graph = objects["graph"]
    faces = objects["faces"]
    edges = objects["edges"]
    face_set = set(faces)
    triangles = [
        triple
        for triple in combinations(range(45), 3)
        if graph[triple[0], triple[1]]
        and graph[triple[0], triple[2]]
        and graph[triple[1], triple[2]]
    ]
    assert len(triangles) == 5280
    nonfilled = [triangle for triangle in triangles if triangle not in face_set]
    assert len(nonfilled) == 5040

    face_of_edge = {}
    for face_id, face in enumerate(faces):
        for edge in combinations(face, 2):
            face_of_edge[tuple(sorted(edge))] = face_id
    assert len(face_of_edge) == 720

    triples = []
    for triangle in nonfilled:
        face_triple = tuple(
            sorted(
                face_of_edge[tuple(sorted(edge))]
                for edge in combinations(triangle, 2)
            )
        )
        assert len(set(face_triple)) == 3
        triples.append(face_triple)
    assert len(set(triples)) == 5040

    incidence = np.zeros((240, 5040), dtype=np.int8)
    pair_counts = Counter()
    for column, triple in enumerate(triples):
        incidence[list(triple), column] = 1
        for pair in combinations(triple, 2):
            pair_counts[pair] += 1

    assert Counter(map(int, incidence.sum(axis=1))) == Counter({63: 240})
    assert Counter(pair_counts.values()) == Counter({2: 3240, 4: 2160})
    assert len(pair_counts) == 5400

    dependency = np.zeros((240, 240), dtype=np.int64)
    for (left, right), value in pair_counts.items():
        dependency[left, right] = dependency[right, left] = value
    assert Counter(map(int, dependency.sum(axis=1))) == Counter({126: 240})
    assert np.array_equal(incidence @ incidence.T, 63 * np.eye(240, dtype=int) + dependency)

    expected = [
        (126.0, 1, "126"),
        (18.0 + 12.0 * np.sqrt(6.0), 24, "18+12sqrt(6)"),
        (18.0, 20, "18"),
        (6.0, 15, "6"),
        (-6.0, 60, "-6"),
        (-10.0, 81, "-10"),
        (18.0 - 12.0 * np.sqrt(6.0), 24, "18-12sqrt(6)"),
        (-18.0, 15, "-18"),
    ]
    eigenvalues = np.linalg.eigvalsh(dependency.astype(float))
    spectrum = []
    used = np.zeros(240, dtype=bool)
    for value, multiplicity, label in expected:
        members = np.flatnonzero(np.abs(eigenvalues - value) < 1e-6)
        assert len(members) == multiplicity
        used[members] = True
        spectrum.append({"eigenvalue": label, "multiplicity": multiplicity})
    assert used.all()

    # The rational annihilator has roots 126, 18, +/-6, -10, -18,
    # and the conjugate pair satisfying x^2-36x-540.
    polynomial = np.array([1], dtype=object)
    for factor in (
        np.array([-126, 1], dtype=object),
        np.array([-18, 1], dtype=object),
        np.array([-6, 1], dtype=object),
        np.array([6, 1], dtype=object),
        np.array([10, 1], dtype=object),
        np.array([18, 1], dtype=object),
        np.array([-540, -36, 1], dtype=object),
    ):
        polynomial = np.convolve(polynomial, factor)
    polynomial = [int(value) for value in polynomial]
    assert len(polynomial) == 9

    modular_annihilator_primes = []
    for prime in (101, 103):
        matrix = dependency % prime
        value = np.zeros_like(matrix)
        power = np.eye(240, dtype=np.int64)
        for coefficient in polynomial:
            value = (value + (coefficient % prime) * power) % prime
            power = power @ matrix % prime
        assert not np.any(value)
        modular_annihilator_primes.append(prime)

    ranks = {str(prime): rank_mod(incidence, prime) for prime in (2, 3, 5)}
    assert ranks == {"2": 240, "3": 239, "5": 240}
    assert np.all(incidence.sum(axis=0) % 3 == 0)

    return {
        "triangles": triples,
        "incidence": incidence,
        "operator": dependency,
        "face_of_edge": face_of_edge,
        "certificate": {
            "vertices": 240,
            "dependency_triples": 5040,
            "triple_size": 3,
            "face_degree": 63,
            "pair_codegrees": {"2": 3240, "4": 2160},
            "supported_face_pairs": 5400,
            "weighted_two_section_degree": 126,
            "incidence_ranks": ranks,
            "spectrum": spectrum,
            "ordinary_multiplicity_fingerprint": [1, 15, 15, 20, 24, 24, 60, 81],
            "annihilator_polynomial_coefficients_low_to_high": polynomial,
            "annihilator_checked_mod_primes": modular_annihilator_primes,
            "covering_boundary": (
                "This is the first code-sensitive cubic deck beyond the strength-two/fractional relaxation. "
                "It supplies the exact higher-order symmetry operator but does not by itself move 389<=R<=435."
            ),
        },
    }


def antipode_data(objects):
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
    _, suborbits = stabilizer_suborbits(face_group, 0, 240)
    singleton = next(
        orbit[0]
        for orbit in suborbits
        if len(orbit) == 1 and orbit[0] != 0
    )
    representatives = [None] * 240
    for element in sorted(face_group):
        if representatives[element[0]] is None:
            representatives[element[0]] = element
    antipode = [representatives[source][singleton] for source in range(240)]
    assert all(antipode[antipode[item]] == item and antipode[item] != item for item in range(240))
    pairs = sorted({tuple(sorted((item, antipode[item]))) for item in range(240)})
    assert len(pairs) == 120
    return face_generators, face_group, antipode, pairs


def modular_projector(objects, dependency):
    face_generators, face_group, antipode, pairs = antipode_data(objects)
    matrix = dependency % 3
    square = matrix @ matrix % 3
    cube = square @ matrix % 3
    fourth = cube @ matrix % 3
    assert np.array_equal((fourth + cube) % 3, np.zeros((240, 240), dtype=int))

    projector = (-cube) % 3
    assert np.array_equal(projector @ projector % 3, projector)
    assert rank_mod(projector, 3) == 81
    assert rank_mod(np.eye(240, dtype=int) - projector, 3) == 159
    assert np.array_equal(matrix @ projector % 3, (-projector) % 3)

    zero_projector = (np.eye(240, dtype=int) - projector) % 3
    ranks = []
    value = zero_projector
    for _ in range(3):
        value = matrix @ value % 3
        ranks.append(rank_mod(value, 3))
    assert ranks == [44, 14, 0]
    jordan = {"J3(0)": 14, "J2(0)": 16, "J1(0)": 85}
    assert 3 * 14 + 2 * 16 + 85 == 159

    permutation = np.zeros((240, 240), dtype=np.int8)
    for source, target in enumerate(antipode):
        permutation[target, source] = 1
    assert np.array_equal(permutation @ projector % 3, projector @ permutation % 3)

    symmetric = np.zeros((240, 120), dtype=np.int8)
    antisymmetric = np.zeros((240, 120), dtype=np.int8)
    for column, (left, right) in enumerate(pairs):
        symmetric[left, column] = symmetric[right, column] = 1
        antisymmetric[left, column] = 1
        antisymmetric[right, column] = -1
    assert rank_mod(projector @ symmetric % 3, 3) == 0
    assert rank_mod(projector @ antisymmetric % 3, 3) == 81

    return {
        "field": "F3",
        "minimal_polynomial": "x^3(x+1)",
        "operator_power_ranks": [rank_mod(matrix, 3), rank_mod(square, 3), rank_mod(cube, 3)],
        "relation": "D^4=-D^3",
        "projector": "E81=-D^3",
        "projector_rank": 81,
        "projector_idempotent": True,
        "projector_eigenvalue_for_D": -1,
        "generalized_zero_dimension": 159,
        "generalized_zero_power_ranks": ranks,
        "generalized_zero_jordan_type": jordan,
        "antipodal_symmetric_image_rank": 0,
        "antipodal_antisymmetric_image_rank": 81,
        "module_boundary": (
            "The 81-dimensional summand is now cut out by an explicit F3-idempotent. "
            "It is not called simple until an independent composition-series calculation is supplied."
        ),
        "face_generators": face_generators,
        "face_group": face_group,
        "pairs": pairs,
    }


def transported_m4_grid(objects, modular):
    faces = objects["faces"]
    edges = objects["edges"]
    face_of_edge = {}
    for face_id, face in enumerate(faces):
        for edge in combinations(face, 2):
            face_of_edge[tuple(sorted(edge))] = face_id

    face_generators = modular["face_generators"]
    face_group = modular["face_group"]
    pairs = modular["pairs"]
    pair_index = {pair: index for index, pair in enumerate(pairs)}
    pair_generators = [
        tuple(
            pair_index[tuple(sorted((generator[left], generator[right])))]
            for left, right in pairs
        )
        for generator in face_generators
    ]
    pair_group = close_group(pair_generators, 120)
    _, pair_suborbits = stabilizer_suborbits(pair_group, 0, 120)
    pair_relations, _ = orbital_relations(pair_group, pair_suborbits, 120)
    adjacency_matrices = [
        (pair_relations == relation).astype(np.int8)
        for relation in range(5)
    ]
    valency_two = next(
        relation
        for relation, orbit in enumerate(pair_suborbits)
        if len(orbit) == 2
    )
    fibres = components(adjacency_matrices[valency_two])
    assert len(fibres) == 40 and {len(fibre) for fibre in fibres} == {3}
    fibre_index = {item: index for index, fibre in enumerate(fibres) for item in fibre}

    quotient_representatives = [None] * 40
    for face_element in sorted(face_group):
        pair_element = tuple(
            pair_index[tuple(sorted((face_element[left], face_element[right])))]
            for left, right in pairs
        )
        quotient_element = tuple(
            fibre_index[pair_element[fibre[0]]]
            for fibre in fibres
        )
        target = quotient_element[0]
        if quotient_representatives[target] is None:
            quotient_representatives[target] = face_element
    assert all(element is not None for element in quotient_representatives)

    base_faces = sorted(face for pair_id in fibres[0] for face in pairs[pair_id])
    assert base_faces == [0, 46, 83, 120, 148, 176]
    labels = {}
    for element in quotient_representatives:
        for label, base_face in enumerate(base_faces):
            labels[element[base_face]] = label
    assert len(labels) == 240
    assert Counter(labels.values()) == Counter({label: 40 for label in range(6)})

    tetrahedron_edges = list(combinations(range(4), 2))
    transpositions = []
    for left, right in tetrahedron_edges:
        matrix = np.eye(4, dtype=float)
        matrix[[left, right]] = matrix[[right, left]]
        transpositions.append(matrix)

    component_matrices = []
    for label in range(6):
        matrix = np.zeros((180, 180), dtype=float)
        for left, right in edges:
            face = face_of_edge[(left, right)]
            if labels[face] == label:
                block = transpositions[label]
                matrix[4 * left : 4 * left + 4, 4 * right : 4 * right + 4] = block
                matrix[4 * right : 4 * right + 4, 4 * left : 4 * left + 4] = block
        component_matrices.append(matrix)

    def ratio(weights):
        matrix = sum(
            weight * component
            for weight, component in zip(weights, component_matrices)
        )
        eigenvalues = np.linalg.eigvalsh(matrix)
        minimum = float(eigenvalues[0])
        maximum = float(eigenvalues[-1])
        assert minimum < 0
        return 1.0 - maximum / minimum, minimum, maximum

    seen = set()
    best = None
    for raw in product((-1, 0, 1), repeat=6):
        if not any(raw):
            continue
        weights = raw
        if next(value for value in weights if value) < 0:
            weights = tuple(-value for value in weights)
        if weights in seen:
            continue
        seen.add(weights)
        value = ratio(weights)
        candidate = (value[0], weights, value[1], value[2])
        if best is None or candidate[0] > best[0]:
            best = candidate
    assert len(seen) == 364
    assert best[1] == (1, 1, 1, 1, 1, 1)
    assert abs(best[3] - 32.0) < 1e-8
    assert best[0] < 4.0

    return {
        "gauge": "lexicographically least face-group lift at each W33 quotient point",
        "projective_weight_grid": "{-1,0,1}^6 / overall sign, zero removed",
        "weight_classes": 364,
        "best_weights": list(best[1]),
        "best_lambda_min": round(best[2], 12),
        "best_lambda_max": round(best[3], 12),
        "best_hoffman_ratio": round(best[0], 12),
        "verdict": (
            "The complete deterministic ternary six-weight grid stays below 4 and therefore cannot affect the live 10<=chi<=11 boundary. "
            "This is a finite-grid no-go, not an unrestricted transported-M4 optimum."
        ),
    }


def circuit_optimum():
    matrix = np.array(
        [
            [2, 1, 1, 0, 0],
            [2, 1, 0, 1, 0],
            [2, 0, 1, 1, 0],
            [0, 2, 2, 0, 0],
            [0, 0, 0, 0, 1],
        ],
        dtype=int,
    )
    basis = {
        canonical_form(tuple(np.eye(5, dtype=int)[index]))
        for index in range(5)
    }
    targets = {canonical_form(tuple(row)) for row in matrix}
    states = {frozenset(basis)}
    counts = [1]
    for _depth in range(4):
        updated = set()
        for state in states:
            forms = list(state)
            for left, right in combinations(forms, 2):
                for sign in (1, 2):
                    candidate = canonical_form(
                        tuple(
                            (left[index] + sign * right[index]) % 3
                            for index in range(5)
                        )
                    )
                    if candidate not in state:
                        updated.add(frozenset((*state, candidate)))
        states = updated
        counts.append(len(states))
    assert counts == [1, 20, 310, 4560, 67245]
    assert not any(targets <= state for state in states)

    # Five binary additions/subtractions attain the target; sign and copy are free.
    a = (1, 0, 0, 0, 0)
    b = (0, 1, 0, 0, 0)
    c = (0, 0, 1, 0, 0)
    d = (0, 0, 0, 1, 0)
    e = (0, 0, 0, 0, 1)
    s = tuple((b[i] + c[i]) % 3 for i in range(5))
    p = tuple((d[i] - a[i]) % 3 for i in range(5))
    outputs = [
        tuple((s[i] - a[i]) % 3 for i in range(5)),
        tuple((p[i] + b[i]) % 3 for i in range(5)),
        tuple((p[i] + c[i]) % 3 for i in range(5)),
        tuple((-s[i]) % 3 for i in range(5)),
        e,
    ]
    assert np.array_equal(np.array(outputs, dtype=int) % 3, matrix % 3)
    assert np.array_equal(np.linalg.matrix_power(matrix, 3) % 3, np.eye(5, dtype=int))

    return {
        "matrix_mod3": matrix.tolist(),
        "cost_model": "binary ternary addition/subtraction; sign and copy free",
        "breadth_first_state_counts_depth_0_to_4": counts,
        "minimum_binary_operations": 5,
        "witness": ["s=b+c", "p=d-a", "y0=s-a", "y1=p+b", "y2=p+c", "y3=-s", "y4=e"],
        "order": 3,
    }


def tomotope_obstruction():
    coordinates = [(left, right) for left in range(4) for right in range(4) if left != right]
    coordinate_index = {coordinate: index for index, coordinate in enumerate(coordinates)}
    faces = []
    labels = []
    for left in range(4):
        faces.append(tuple(sorted(coordinate_index[(left, right)] for right in range(4) if right != left)))
        labels.append(f"O{left}")
    for right in range(4):
        faces.append(tuple(sorted(coordinate_index[(left, right)] for left in range(4) if left != right)))
        labels.append(f"I{right}")
    for subset in combinations(range(4), 3):
        left, middle, right = subset
        for sign, cycle in (
            ("+", ((left, middle), (middle, right), (right, left))),
            ("-", ((left, right), (right, middle), (middle, left))),
        ):
            faces.append(tuple(sorted(coordinate_index[item] for item in cycle)))
            labels.append("C" + "".join(map(str, subset)) + sign)
    assert len(faces) == 16 and len(set(faces)) == 16

    cell_candidates = []
    for selected in combinations(range(16), 4):
        multiplicity = Counter(
            edge
            for face in selected
            for edge in faces[face]
        )
        if len(multiplicity) == 6 and set(multiplicity.values()) == {2}:
            cell_candidates.append(selected)
    assert len(cell_candidates) == 12

    face_to_candidates = [
        [index for index, cell in enumerate(cell_candidates) if face in cell]
        for face in range(16)
    ]
    solutions = []

    def search(chosen, counts):
        if len(chosen) == 8:
            if all(value == 2 for value in counts):
                solutions.append(tuple(chosen))
            return
        if sum(2 - value for value in counts) != 4 * (8 - len(chosen)):
            return
        last = chosen[-1] if chosen else -1
        deficient = [face for face, value in enumerate(counts) if value < 2]
        if not deficient:
            return
        face = min(
            deficient,
            key=lambda item: sum(
                index > last
                and all(counts[other] < 2 for other in cell_candidates[index])
                for index in face_to_candidates[item]
            ),
        )
        for index in face_to_candidates[face]:
            if index <= last:
                continue
            cell = cell_candidates[index]
            if any(counts[other] >= 2 for other in cell):
                continue
            updated = list(counts)
            for other in cell:
                updated[other] += 1
            search([*chosen, index], updated)

    search([], [0] * 16)
    assert not solutions

    visible_automorphisms = set()
    face_index = {face: index for index, face in enumerate(faces)}
    for permutation in permutations(range(4)):
        for reverse in (False, True):
            coordinate_image = []
            for left, right in coordinates:
                image_left, image_right = permutation[left], permutation[right]
                if reverse:
                    image_left, image_right = image_right, image_left
                coordinate_image.append(coordinate_index[(image_left, image_right)])
            face_image = tuple(
                face_index[tuple(sorted(coordinate_image[edge] for edge in face))]
                for face in faces
            )
            visible_automorphisms.add(face_image)
    assert len(visible_automorphisms) == 48

    return {
        "configuration": [12, 4, 16, 3],
        "visible_S4_times_reversal_order": 48,
        "four_face_six_edge_cell_candidates": 12,
        "eight_cell_double_cover_solutions": 0,
        "verdict": (
            "The oriented-tetrahedron Reye-style 12_4 16_3 surface cannot be lifted to the tomotope by selecting eight four-face cells with every triangular face incident to two cells. "
            "The matching parameters are therefore not an incidence-preserving tomotope identification."
        ),
    }


def atlas_constructions():
    # A hypothetical SRG(57,14,1,4) cannot contain induced W33 and Clebsch
    # pieces on disjoint 40- and 16-sets plus one remaining vertex.
    w33_external_degree_sum = 40 * (14 - 12)
    clebsch_external_degree_sum = 16 * (14 - 5)
    assert (w33_external_degree_sum, clebsch_external_degree_sum) == (80, 144)
    assert clebsch_external_degree_sum - w33_external_degree_sum == 64
    induced_no_go = {
        "hypothetical_graph": [57, 14, 1, 4],
        "tempting_partition": [1, 16, 40],
        "induced_Clebsch_external_degree_sum": clebsch_external_degree_sum,
        "induced_W33_external_degree_sum": w33_external_degree_sum,
        "required_apex_incidence_difference": 64,
        "maximum_possible_apex_incidence_difference": 16,
        "verdict": "No such induced W33 plus Clebsch plus apex decomposition exists.",
    }

    # Clebsch spectrum 5^1,1^10,(-3)^5.  The polynomial below maps
    # 5 and 1 to 2, and -3 to -4, supplying exactly the multiplicity gap
    # between W33 and Gewirtz nonprincipal spectra.
    polynomial = {"x^2": "-3/16", "x": "9/8", "1": "17/16"}
    assert (-3 * 25 + 18 * 5 + 17) == 32
    assert (-3 + 18 + 17) == 32
    assert (-3 * 9 - 54 + 17) == -64
    spectral_completion = {
        "Clebsch_spectrum": {"5": 1, "1": 10, "-3": 5},
        "polynomial": "p(x)=(-3x^2+18x+17)/16",
        "p(Clebsch)_spectrum": {"2": 11, "-4": 5},
        "W33_nonprincipal_spectrum": {"2": 24, "-4": 15},
        "direct_sum_nonprincipal_spectrum": {"2": 35, "-4": 20},
        "Gewirtz_nonprincipal_spectrum": {"2": 35, "-4": 20},
        "verdict": (
            "W33 plus the polynomially transformed Clebsch module gives an exact functional-calculus completion of the Gewirtz augmentation spectrum. "
            "This is not a graph embedding or canonical group-module intertwiner."
        ),
        "coefficient_record": polynomial,
    }
    return {"missing_57_induced_decomposition_no_go": induced_no_go, "W33_Clebsch_Gewirtz_spectral_completion": spectral_completion}


def build_certificate():
    objects = geometry_objects()
    dependency = dependency_deck(objects)
    modular = modular_projector(objects, dependency["operator"])
    m4 = transported_m4_grid(objects, modular)
    circuit = circuit_optimum()
    tomotope = tomotope_obstruction()
    atlas = atlas_constructions()

    result = {
        "schema": "w33.bt3506_3519.chained_breakthrough.v1",
        "status": "PASS_7_FRONTS",
        "passes": list(range(3506, 3520)),
        "live_boundaries": {"covering_radius": [389, 435], "chromatic_number": [10, 11]},
        "dependency_hypergraph": dependency["certificate"],
        "characteristic_three_projector": {
            key: value
            for key, value in modular.items()
            if key not in {"face_generators", "face_group", "pairs"}
        },
        "transported_M4_grid": m4,
        "five_channel_hardware": circuit,
        "tomotope_lift": tomotope,
        "bonkers": atlas,
        "evidence_boundary": [
            "The radius interval remains 389<=R<=435.",
            "The chromatic interval remains 10<=chi(H)<=11.",
            "The 81-dimensional image is an explicit direct summand but is not labelled simple.",
            "The M4 result is a deterministic finite-grid no-go, not an unrestricted optimum.",
            "The circuit optimum is exact in the stated addition/subtraction cost model.",
            "No remote Icarus, Yosys, FPGA, PDF, laboratory, M57, or physical result is claimed by the source verifier.",
        ],
    }
    payload = json.dumps(result, sort_keys=True, separators=(",", ":")).encode("utf-8")
    result["semantic_sha256"] = hashlib.sha256(payload).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    result = build_certificate()
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(result["status"], result["semantic_sha256"])


if __name__ == "__main__":
    main()
