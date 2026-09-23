#!/usr/bin/env python3
"""Reduce the full Clifford Hesse compiler at (1-omega) and lift it to E6.

The exact 36-state compiler is unitary up to scale over Q(omega), but the
ramified Eisenstein reduction omega -> 1 in F3 turns each three-point Fourier
fiber into a rank-one all-ones column.  Its rank therefore drops from 36 to
12.  This script tests, rather than infers from matching dimensions, how that
12-space meets the independent 24-dimensional line-side kernel of the Cartan
cubic incidence matrix.

In the physical Clifford gauge the reduced image is contained in the
ordinary-36 projection of the cubic line kernel.  Every reduced Fourier fiber
has a unique correction on the nine distinguished center-coset tritangents.
The twelve corrected vectors are weight-six relations and span an explicit
ternary [45,12,6]_3 subcode of the Cartan-cubic line-holonomy code.

The two 24-dimensional spaces in the construction remain explicitly
firewalled: compiler nullity is on safe-plane coordinates, whereas cubic
line nullity is on tritangent coordinates.  Only the rank-12 image and its
unique nine-line correction are identified.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_ramified_hesse_cubic_holonomy_bridge.json"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def canonical(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value) -> str:
    return "sha256:" + hashlib.sha256(canonical(value).encode()).hexdigest()


def gf3_rref(rows: list[list[int]]) -> tuple[list[list[int]], list[int]]:
    matrix = [[int(value) % 3 for value in row] for row in rows]
    pivots: list[int] = []
    pivot_row = 0
    if not matrix:
        return matrix, pivots
    for column in range(len(matrix[0])):
        pivot = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        inverse = pow(matrix[pivot_row][column], -1, 3)
        matrix[pivot_row] = [inverse * value % 3 for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or matrix[row][column] == 0:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                (left - factor * right) % 3
                for left, right in zip(matrix[row], matrix[pivot_row])
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return matrix, pivots


def gf3_rank(rows: list[list[int]]) -> int:
    return len(gf3_rref(rows)[1])


def gf3_kernel(rows: list[list[int]]) -> list[list[int]]:
    reduced, pivots = gf3_rref(rows)
    columns = len(rows[0])
    free = [column for column in range(columns) if column not in pivots]
    basis = []
    for free_column in free:
        vector = [0] * columns
        vector[free_column] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free_column] % 3
        assert all(
            sum(left * right for left, right in zip(source, vector)) % 3 == 0
            for source in rows
        )
        basis.append(vector)
    return basis


def gf3_unique_solve(rows: list[list[int]], rhs: list[int]) -> list[int]:
    columns = len(rows[0])
    reduced, pivots = gf3_rref(
        [row[:] + [value % 3] for row, value in zip(rows, rhs)]
    )
    assert all(
        any(row[column] for column in range(columns)) or row[-1] == 0
        for row in reduced
    )
    variable_pivots = [pivot for pivot in pivots if pivot < columns]
    assert variable_pivots == list(range(columns))
    solution = [0] * columns
    for row, pivot in enumerate(pivots):
        if pivot < columns:
            solution[pivot] = reduced[row][-1]
    assert all(
        sum(left * right for left, right in zip(row, solution)) % 3 == value % 3
        for row, value in zip(rows, rhs)
    )
    return solution


def code_weight_enumerator(
    basis: list[list[int]],
) -> tuple[dict[int, int], set[tuple[int, ...]]]:
    array = np.asarray(basis, dtype=np.int16)
    dimension = len(basis)
    total = 3**dimension
    census: Counter[int] = Counter()
    small_words: set[tuple[int, ...]] = set()
    batch_size = 20_000
    for start in range(0, total, batch_size):
        size = min(batch_size, total - start)
        numbers = np.arange(start, start + size, dtype=np.int64)
        coefficients = np.empty((size, dimension), dtype=np.int16)
        for column in range(dimension):
            coefficients[:, column] = numbers % 3
            numbers //= 3
        words = (coefficients @ array) % 3
        weights = np.count_nonzero(words, axis=1)
        values, counts = np.unique(weights, return_counts=True)
        census.update({int(value): int(count) for value, count in zip(values, counts)})
        for word in words[weights <= 6]:
            small_words.add(tuple(map(int, word)))
    return dict(sorted(census.items())), small_words


def systematic_weight_enumerator(corrections: list[list[int]]) -> dict[int, int]:
    """Use wt(cG)=3 wt(c)+wt(cA) for G=[2A | I12 tensor 111]."""
    array = np.asarray(corrections, dtype=np.int16)
    dimension = len(corrections)
    census: Counter[int] = Counter()
    batch_size = 20_000
    for start in range(0, 3**dimension, batch_size):
        size = min(batch_size, 3**dimension - start)
        numbers = np.arange(start, start + size, dtype=np.int64)
        coefficients = np.empty((size, dimension), dtype=np.int16)
        for column in range(dimension):
            coefficients[:, column] = numbers % 3
            numbers //= 3
        fiber_words = (coefficients @ array) % 3
        weights = (
            3 * np.count_nonzero(coefficients, axis=1)
            + np.count_nonzero(fiber_words, axis=1)
        )
        values, counts = np.unique(weights, return_counts=True)
        census.update({int(value): int(count) for value, count in zip(values, counts)})
    return dict(sorted(census.items()))


def main(write: bool = True) -> dict:
    pappus = load(
        ROOT / "analysis/w33_maximal_compiler_symmetry_pappus.py",
        "ramified_bridge_pappus",
    )
    common = load(
        ROOT / "analysis/w33_pass4992_4999_common.py",
        "ramified_bridge_cubic",
    )
    compiler = json.loads(
        (ROOT / "data/w33_hesse36_full_clifford648_fourier_compiler.json").read_text()
    )
    address = json.loads(
        (ROOT / "data/w33_e8_matter81_h27_address_operator_compiler.json").read_text()
    )
    steiner = json.loads(
        (ROOT / "data/w33_steiner_trinification_qpsi_normalizer.json").read_text()
    )

    sparse_columns = compiler["compiler"][
        "target_column_to_source_rows_and_omega_exponents"
    ]
    assert len(sparse_columns) == 36
    assert all(len(column) == 3 for column in sparse_columns)
    assert digest(sparse_columns) == compiler["compiler"]["matrix_digest"]

    # Q(omega)/(1-omega) = F3 and omega maps to 1.  Hence phase exponents
    # disappear and each sparse Fourier column becomes a support indicator.
    reduced = [[0] * 36 for _ in range(36)]
    support_multiplicity: Counter[tuple[int, ...]] = Counter()
    for target, column in enumerate(sparse_columns):
        support = tuple(row for row, _exponent in column)
        assert len(set(support)) == 3
        support_multiplicity[support] += 1
        for row, exponent in column:
            assert exponent in range(3)
            reduced[row][target] = 1
    reduced_rank = gf3_rank(reduced)
    right_kernel = gf3_kernel(reduced)
    transpose_reduced = [list(column) for column in zip(*reduced)]
    left_kernel = gf3_kernel(transpose_reduced)
    reduced_gram = [
        [sum(reduced[row][left] * reduced[row][right] for row in range(36)) % 3
         for right in range(36)]
        for left in range(36)
    ]
    assert reduced_rank == 12
    assert len(right_kernel) == len(left_kernel) == 24
    assert not any(any(row) for row in reduced_gram)
    assert len(support_multiplicity) == 12
    assert set(support_multiplicity.values()) == {3}

    # Reconstruct the exact source-line order used by the compiler.  The first
    # direction is the center and gives the distinguished orbit of nine; the
    # remaining four directions give the ordinary orbit of 36.
    directions = ((0, 0, 1), (0, 1, 1), (1, 0, 1), (1, 1, 0), (1, 2, 2))

    def cyclic(generator):
        return frozenset(
            (pappus.ID, generator, pappus.hmul(generator, generator))
        )

    def cosets(subgroup):
        return {
            frozenset(pappus.hmul(g, h) for h in subgroup) for g in pappus.H
        }

    fiber_lines = sorted(cosets(cyclic(directions[0])), key=lambda line: tuple(sorted(line)))
    ordinary_direction: dict[frozenset[tuple[int, int, int]], int] = {}
    for direction_index, direction in enumerate(directions[1:]):
        for line in cosets(cyclic(direction)):
            assert line not in ordinary_direction
            ordinary_direction[line] = direction_index
    ordinary_lines = sorted(ordinary_direction, key=lambda line: tuple(sorted(line)))
    assert len(fiber_lines) == 9 and len(ordinary_lines) == 36

    # The compiler supports are exactly the three center translates within
    # one of four Hesse direction classes; the 12 supports partition ordinary36.
    support_direction = []
    for support in sorted(support_multiplicity):
        direction_set = {ordinary_direction[ordinary_lines[row]] for row in support}
        assert len(direction_set) == 1
        support_direction.append(next(iter(direction_set)))
    assert Counter(support_direction) == Counter({0: 3, 1: 3, 2: 3, 3: 3})
    assert Counter(row for support in support_multiplicity for row in support) == Counter(
        {row: 1 for row in range(36)}
    )

    all_address_lines = fiber_lines + ordinary_lines
    incidence_address = [
        [int(point in line) for line in all_address_lines] for point in pappus.H
    ]
    fiber_incidence = [row[:9] for row in incidence_address]
    ordinary_incidence = [row[9:] for row in incidence_address]
    address_line_kernel = gf3_kernel(incidence_address)
    projected_line_kernel = [vector[9:] for vector in address_line_kernel]
    image_basis = [
        [int(row in support) for row in range(36)]
        for support in sorted(support_multiplicity)
    ]
    assert gf3_rank(fiber_incidence) == 9
    assert gf3_rank(ordinary_incidence) == 21
    assert gf3_rank(incidence_address) == 21
    assert len(address_line_kernel) == 24
    assert gf3_rank(projected_line_kernel) == 24
    assert gf3_rank(image_basis) == 12
    assert gf3_rank(projected_line_kernel + image_basis) == 24

    # Lift the reduced compiler image uniquely through the injective fiber-nine
    # incidence map, then transport the address GQ(2,4) labeling to the frozen
    # cubic-surface tritangent labeling.
    address_to_frame = {
        tuple(map(int, key.split(","))): value
        for key, value in address["address_space"]["address_to_complete_frame"].items()
    }
    assert set(address_to_frame) == set(pappus.H)
    base = common.build_base()
    tritangents = [frozenset(line) for line in base["tritangents"]]
    tritangent_index = {line: index for index, line in enumerate(tritangents)}
    address_line_to_tritangent = [
        tritangent_index[frozenset(address_to_frame[point] for point in line)]
        for line in all_address_lines
    ]
    assert len(set(address_line_to_tritangent)) == 45

    relation_basis_address = []
    relation_basis = []
    relation_records = []
    correction_vectors = []
    for support_index, (ordinary, direction_index) in enumerate(
        zip(image_basis, support_direction)
    ):
        rhs = [
            -sum(row[column] * ordinary[column] for column in range(36)) % 3
            for row in ordinary_incidence
        ]
        correction = gf3_unique_solve(fiber_incidence, rhs)
        correction_vectors.append(correction)
        address_relation = correction + ordinary
        assert all(
            sum(row[column] * address_relation[column] for column in range(45)) % 3
            == 0
            for row in incidence_address
        )
        relation = [0] * 45
        for address_line, value in enumerate(address_relation):
            relation[address_line_to_tritangent[address_line]] = value
        assert sum(value != 0 for value in relation) == 6
        relation_basis_address.append(address_relation)
        relation_basis.append(relation)
        relation_records.append(
            {
                "basis_index": support_index,
                "hesse_direction_class": direction_index,
                "fiber_tritangents": [
                    {
                        "tritangent_index": address_line_to_tritangent[index],
                        "coefficient_F3": correction[index],
                    }
                    for index in range(9)
                    if correction[index]
                ],
                "ordinary_tritangents": [
                    {
                        "tritangent_index": address_line_to_tritangent[9 + index],
                        "coefficient_F3": ordinary[index],
                    }
                    for index in range(36)
                    if ordinary[index]
                ],
            }
        )

    cubic_incidence = [
        [int(point in line) for line in tritangents] for point in range(27)
    ]
    assert all(
        all(sum(row[column] * relation[column] for column in range(45)) % 3 == 0
            for row in cubic_incidence)
        for relation in relation_basis
    )
    assert gf3_rank(relation_basis) == 12
    assert gf3_rank(correction_vectors) == 6
    assert Counter(
        index
        for correction in correction_vectors
        for index, value in enumerate(correction)
        if value
    ) == Counter({index: 4 for index in range(9)})

    # The nine fiber cosets are canonically H27/Z(H27)=AG(2,3).  The twelve
    # correction supports are exactly all affine lines.  Since every nonzero
    # correction coefficient is 2 and the ordinary triples are disjoint, a
    # coordinate permutation puts the generator in systematic graph form
    # [2 A_AG(2,3) | I12 tensor (1,1,1)].
    fiber_points = []
    for line in fiber_lines:
        quotient_points = {(a, b) for a, b, _c in line}
        assert len(quotient_points) == 1
        fiber_points.append(next(iter(quotient_points)))
    assert set(fiber_points) == set(pappus.V)
    affine_lines = {
        frozenset(
            index
            for index, point in enumerate(fiber_points)
            if pappus.symp(direction, point) == level
        )
        for direction in pappus.DIRECTIONS
        for level in pappus.F
    }
    correction_supports = {
        frozenset(index for index, value in enumerate(row) if value)
        for row in correction_vectors
    }
    assert correction_supports == affine_lines
    assert all(value in (0, 2) for row in correction_vectors for value in row)

    gram = [
        [sum(left * right for left, right in zip(a, b)) % 3 for b in relation_basis]
        for a in relation_basis
    ]
    assert gf3_rank(gram) == 3
    gram_classes: defaultdict[tuple[int, ...], list[int]] = defaultdict(list)
    for index, row in enumerate(gram):
        gram_classes[tuple(row)].append(index)
    classes = sorted(gram_classes.values())
    assert sorted(map(len, classes)) == [3, 3, 3, 3]
    assert {tuple(sorted(support_direction[index] for index in group)) for group in classes} == {
        (0, 0, 0), (1, 1, 1), (2, 2, 2), (3, 3, 3)
    }
    representatives = [group[0] for group in classes]
    gram_quotient = [[gram[left][right] for right in representatives] for left in representatives]
    assert gram_quotient == [
        [int(left != right) for right in range(4)] for left in range(4)
    ]

    weight_enumerator, small_words = code_weight_enumerator(relation_basis)
    weight_enumerator_from_systematic_formula = systematic_weight_enumerator(
        correction_vectors
    )
    assert weight_enumerator_from_systematic_formula == weight_enumerator
    expected_minimum_words = {
        tuple(multiplier * value % 3 for value in relation)
        for relation in relation_basis
        for multiplier in (1, 2)
    }
    assert sum(weight_enumerator.values()) == 3**12
    assert weight_enumerator[0] == 1 and weight_enumerator[6] == 24
    assert not any(weight in weight_enumerator for weight in range(1, 6))
    assert small_words == {(0,) * 45} | expected_minimum_words

    line_kernel_dimension = steiner["ternary_kernel"]["line_side_kernel_dimension_F3"]
    assert line_kernel_dimension == len(address_line_kernel) == 24

    out = {
        "schema": "w33.ramified_hesse_cubic_holonomy_bridge.v2",
        "status": "PASS_RAMIFIED_CLIFFORD_IMAGE_LIFTS_TO_TERNARY_45_12_6_CUBIC_HOLONOMY_CODE",
        "headline": (
            "Reducing the exact full-Clifford Hesse36 compiler modulo the ramified "
            "Eisenstein prime (1-omega) sends omega to 1 and collapses its twelve "
            "three-point Fourier fibers from rank 36 to rank 12. In the frozen "
            "Clifford/address-to-cubic gauge, that image is the ordinary-36 projection "
            "of twelve uniquely corrected Cartan-cubic line relations. They span an "
            "explicit ternary [45,12,6]_3 subcode of the 24-dimensional line-holonomy "
            "kernel. Its 24 minimum words are exactly plus/minus the twelve generator "
            "hexads, each with three ordinary and three distinguished tritangents."
        ),
        "ramified_compiler_reduction": {
            "coefficient_map": "Z[omega] -> Z[omega]/(1-omega) = F3; omega -> 1",
            "characteristic_zero_rank": compiler["compiler"]["rank"],
            "reduced_matrix_shape": [36, 36],
            "reduced_rank_F3": reduced_rank,
            "right_nullity_safe36_F3": len(right_kernel),
            "left_nullity_ordinary36_F3": len(left_kernel),
            "distinct_column_supports": len(support_multiplicity),
            "multiplicity_per_support": sorted(set(support_multiplicity.values()))[0],
            "support_size": 3,
            "support_direction_class_sizes": {
                str(direction): count
                for direction, count in sorted(Counter(support_direction).items())
            },
            "ordinary36_partitioned_once_by_supports": True,
            "reduced_gram": "Tbar^T Tbar = 0 over F3",
            "reduced_matrix_digest": digest(reduced),
        },
        "cubic_line_holonomy": {
            "Cartan_incidence_shape": [27, 45],
            "Cartan_incidence_rank_F3": gf3_rank(cubic_incidence),
            "full_line_kernel_dimension_F3": len(address_line_kernel),
            "Clifford_line_orbit_split": [9, 36],
            "fiber9_incidence_rank_F3": gf3_rank(fiber_incidence),
            "ordinary36_incidence_rank_F3": gf3_rank(ordinary_incidence),
            "ordinary_projection_of_line_kernel_rank_F3": gf3_rank(projected_line_kernel),
            "reduced_compiler_image_contained_in_projection": True,
            "fiber9_correction_is_unique": True,
            "fiber9_correction_map_rank_F3": gf3_rank(correction_vectors),
            "address_line_to_tritangent_digest": digest(address_line_to_tritangent),
        },
        "lifted_code": {
            "parameters": "[45,12,6]_3",
            "ambient_code": "ker_F3(Cartan 27x45 point-tritangent incidence)",
            "dimension": gf3_rank(relation_basis),
            "minimum_distance": 6,
            "word_count": 3**12,
            "weight_enumerator": {
                str(weight): count for weight, count in weight_enumerator.items()
            },
            "minimum_word_count": weight_enumerator[6],
            "minimum_words_are_exactly_plus_minus_generators": True,
            "generator_support_split": "3 ordinary36 + 3 fiber9 tritangents",
            "ordinary_coordinate_multiplicity_across_generators": 1,
            "fiber_coordinate_multiplicity_across_generators": 4,
            "generator_gram_rank_F3": gf3_rank(gram),
            "generator_gram_zero_classes": classes,
            "gram_quotient_on_four_hesse_directions": gram_quotient,
            "gram_description": "After grouping by Hesse direction, Gram=(J4-I4) tensor J3.",
            "systematic_coordinate_form": "[2*A_AG(2,3) | I12 tensor (1,1,1)]",
            "systematic_weight_formula": "wt(cG)=3*wt(c)+wt(c*A_AG(2,3))",
            "fiber9_model": "the nine points H27/Z(H27)=AG(2,3)",
            "fiber_correction_supports": "all twelve affine lines of AG(2,3)",
            "fiber_correction_coefficients": "constant 2 on every affine line",
            "fiber_point_to_tritangent": [
                {
                    "AG23_point": list(point),
                    "tritangent_index": address_line_to_tritangent[index],
                }
                for index, point in enumerate(fiber_points)
            ],
            "relation_records": relation_records,
            "relation_basis_digest": digest(relation_basis),
            "weight_enumerator_digest": digest(weight_enumerator),
        },
        "kernel_firewall": {
            "compiler_nullity24_coordinates": "safe36 compiler-target coordinates",
            "cubic_line_nullity24_coordinates": "45 tritangent coordinates",
            "equal_dimensions_imply_identification": False,
            "identified_object": (
                "Only the rank-12 reduced compiler image on ordinary36 is lifted, "
                "through the unique fiber9 correction, into the cubic line kernel."
            ),
        },
        "interpretation": (
            "The three complex C3 characters remain distinct over Q(omega), but coalesce "
            "at the prime above 3. Their modular residue is not lost arbitrarily: it "
            "becomes twelve exact six-tritangent conservation laws organized as four "
            "Hesse direction classes. This supplies an arithmetic interface between the "
            "Clifford virtual-machine compiler and the Cartan cubic without identifying "
            "their unrelated 24-dimensional kernels."
        ),
        "external_prior_art_audit": {
            "same_parameters_published": True,
            "citation": "S. H. Saif and A. A. Alhomaidhi, Cyclic Codes over a Split Local Ring of Type (2,2), Mathematics 14 (2026) 2019",
            "doi": "https://doi.org/10.3390/math14112019",
            "published_construction": "a length-45 ternary Gray image from a length-9 cyclic code over a split cube-zero local ring",
            "equivalence_to_present_code_checked": False,
            "parameter_novelty_claimed": False,
            "repository_increment": "the explicit embedding in the Cartan point-tritangent kernel, the ramified Clifford origin, the complete weight enumerator and minimum shell, and the AG(2,3) systematic form",
        },
        "boundary": (
            "Exact finite arithmetic in the repository's frozen Clifford gauge. The "
            "[45,12,6]_3 code is an explicit subcode, not asserted to be a globally new "
            "code or a W(E6)-invariant submodule. Modular reduction is not a physical "
            "loss/noise model, and no particle or coupling interpretation is inferred."
        ),
        "parents": [
            "data/w33_hesse36_full_clifford648_fourier_compiler.json",
            "data/w33_e8_matter81_h27_address_operator_compiler.json",
            "data/w33_steiner_trinification_qpsi_normalizer.json",
        ],
        "checks": {
            "full_compiler_sparse_certificate_consumed": True,
            "ramified_reduction_rank_is_12_and_nullities_are_24": True,
            "reduced_gram_is_zero": True,
            "twelve_support_triples_partition_ordinary36": True,
            "compiler_image_is_contained_in_projected_cubic_kernel": True,
            "all_twelve_fiber9_corrections_exist_uniquely": True,
            "all_lifted_relations_annihilate_Cartan_incidence": True,
            "lifted_code_is_45_12_6": True,
            "minimum_shell_is_exactly_plus_minus_twelve_hexads": True,
            "fiber_corrections_are_all_twelve_AG23_lines": True,
            "systematic_weight_formula_reproduces_complete_enumerator": True,
            "four_hesse_direction_gram_quotient_is_K4": True,
            "two_dimension24_kernels_are_not_identified": True,
        },
    }
    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n")
    return out


if __name__ == "__main__":
    print(json.dumps(main(True), indent=2))
