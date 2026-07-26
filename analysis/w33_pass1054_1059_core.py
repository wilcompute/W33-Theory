#!/usr/bin/env python3
"""Shared exact finite-geometry machinery for Passes 1054--1059.

This module intentionally rebuilds every object from F_3^4. It does not import
prior pass outputs, so the new certificates are independent regression witnesses.
"""
from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import Iterable

import numpy as np
from sympy import Matrix
from sympy.combinatorics import Permutation, PermutationGroup

Q = 3
J = np.array(
    [[0, 1, 0, 0], [-1, 0, 0, 0], [0, 0, 0, 1], [0, 0, -1, 0]],
    dtype=int,
) % Q


def normalize(vector: Iterable[int]) -> tuple[int, ...]:
    v = np.array(tuple(vector), dtype=int) % Q
    for coordinate in v:
        if int(coordinate):
            return tuple(int(x) for x in (v * pow(int(coordinate), -1, Q)) % Q)
    raise ValueError("zero has no projective representative")


def symplectic(x: tuple[int, ...], y: tuple[int, ...]) -> int:
    return int((np.array(x, dtype=int) @ J @ np.array(y, dtype=int)) % Q)


def cycle_partition(g: Permutation, degree: int) -> tuple[int, ...]:
    lengths = [len(cycle) for cycle in g.cyclic_form]
    lengths.extend([1] * (degree - sum(lengths)))
    return tuple(sorted(lengths, reverse=True))


def permutation_images(g: Permutation, degree: int) -> list[int]:
    return [int(g(index)) for index in range(degree)]


@dataclass(frozen=True)
class W33Bundle:
    points: list[tuple[int, ...]]
    lines: list[tuple[int, ...]]
    point_lines: tuple[tuple[int, ...], ...]
    point_generators: list[Permutation]
    group: PermutationGroup
    point_stabilizer: PermutationGroup
    line_stabilizer: PermutationGroup


def build_w33_bundle() -> W33Bundle:
    points = sorted(
        {normalize(v) for v in itertools.product(range(Q), repeat=4) if any(v)}
    )
    point_index = {point: index for index, point in enumerate(points)}

    line_set: set[tuple[int, ...]] = set()
    for index, x in enumerate(points):
        for y in points[index + 1 :]:
            if symplectic(x, y):
                continue
            span = {
                point_index[
                    normalize(
                        (a * np.array(x, dtype=int) + b * np.array(y, dtype=int)) % Q
                    )
                ]
                for a, b in itertools.product(range(Q), repeat=2)
                if (a, b) != (0, 0)
            }
            if len(span) == Q + 1:
                line_set.add(tuple(sorted(span)))
    lines = sorted(line_set)

    point_lines_lists: list[list[int]] = [[] for _ in points]
    for line_index, line in enumerate(lines):
        for point in line:
            point_lines_lists[point].append(line_index)
    point_lines = tuple(tuple(sorted(items)) for items in point_lines_lists)

    def transvection(v: tuple[int, ...]) -> Permutation:
        vv = np.array(v, dtype=int)
        images: list[int] = []
        for x in points:
            xx = np.array(x, dtype=int)
            image = (xx + symplectic(x, v) * vv) % Q
            images.append(point_index[normalize(image)])
        return Permutation(images)

    generators = [transvection(v) for v in points]
    group = PermutationGroup(generators)
    point_stabilizer = group.stabilizer(0)
    line_zero = set(lines[0])
    line_stabilizer = group.subgroup_search(
        lambda g: {g(point) for point in line_zero} == line_zero
    )

    return W33Bundle(
        points=points,
        lines=lines,
        point_lines=point_lines,
        point_generators=generators,
        group=group,
        point_stabilizer=point_stabilizer,
        line_stabilizer=line_stabilizer,
    )


def to_bitword(values: Iterable[int]) -> int:
    word = 0
    for index, value in enumerate(values):
        if int(value) & 1:
            word |= 1 << index
    return word


def rowspace_basis(rows: Iterable[int]) -> list[int]:
    basis: list[int] = []
    for row in rows:
        reduced = int(row)
        for pivot in basis:
            reduced = min(reduced, reduced ^ pivot)
        if reduced:
            basis.append(reduced)
            basis.sort(reverse=True)
    return basis


def nullspace_basis(matrix: np.ndarray) -> list[int]:
    rows = [[int(x) & 1 for x in matrix[index]] for index in range(matrix.shape[0])]
    columns = matrix.shape[1]
    pivots: dict[int, int] = {}
    rank = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, len(rows)) if rows[row][column]), None
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for row in range(len(rows)):
            if row != rank and rows[row][column]:
                rows[row] = [a ^ b for a, b in zip(rows[row], rows[rank])]
        pivots[column] = rank
        rank += 1
    free = [column for column in range(columns) if column not in pivots]
    result: list[int] = []
    for free_column in free:
        vector = [0] * columns
        vector[free_column] = 1
        for column, row in pivots.items():
            vector[column] = rows[row][free_column]
        result.append(to_bitword(vector))
    return result


def reduce_mod_basis(vector: int, basis: Iterable[int]) -> int:
    reduced = int(vector)
    for pivot in basis:
        reduced = min(reduced, reduced ^ pivot)
    return reduced


@dataclass(frozen=True)
class QuotientBundle:
    adjacency: np.ndarray
    code_basis: list[int]
    dual_basis: list[int]
    glue_basis: list[int]
    coordinate_representative: dict[int, int]
    canonical_to_coordinate: dict[int, int]
    quotient_generators: list[Permutation]
    quotient_group: PermutationGroup
    anisotropic: list[int]
    isotropic_nonzero: list[int]


def permute_word(word: int, permutation: Permutation, degree: int = 40) -> int:
    image = 0
    for index in range(degree):
        if (word >> index) & 1:
            image |= 1 << permutation(index)
    return image


def build_quotient(bundle: W33Bundle) -> QuotientBundle:
    adjacency = np.zeros((40, 40), dtype=np.int8)
    for line in bundle.lines:
        for left, right in itertools.combinations(line, 2):
            adjacency[left, right] = adjacency[right, left] = 1

    code_basis = rowspace_basis(to_bitword(row) for row in adjacency)
    dual_basis = nullspace_basis(adjacency)
    combined = list(code_basis)
    glue_basis: list[int] = []
    for vector in dual_basis:
        if reduce_mod_basis(vector, combined):
            combined.append(vector)
            combined.sort(reverse=True)
            glue_basis.append(vector)

    coordinate_representative: dict[int, int] = {}
    canonical_to_coordinate: dict[int, int] = {}
    for coordinate in range(256):
        representative = 0
        for index, vector in enumerate(glue_basis):
            if (coordinate >> index) & 1:
                representative ^= vector
        canonical = reduce_mod_basis(representative, code_basis)
        coordinate_representative[coordinate] = representative
        canonical_to_coordinate[canonical] = coordinate

    quotient_generators: list[Permutation] = []
    for generator in bundle.point_generators:
        images: list[int] = []
        for coordinate in range(256):
            moved = permute_word(coordinate_representative[coordinate], generator)
            canonical = reduce_mod_basis(moved, code_basis)
            images.append(canonical_to_coordinate[canonical])
        quotient_generators.append(Permutation(images))
    quotient_group = PermutationGroup(quotient_generators)

    def quadratic(coordinate: int) -> int:
        return (coordinate_representative[coordinate].bit_count() // 2) % 2

    anisotropic = [c for c in range(1, 256) if quadratic(c) == 1]
    isotropic_nonzero = [c for c in range(1, 256) if quadratic(c) == 0]

    return QuotientBundle(
        adjacency=adjacency,
        code_basis=code_basis,
        dual_basis=dual_basis,
        glue_basis=glue_basis,
        coordinate_representative=coordinate_representative,
        canonical_to_coordinate=canonical_to_coordinate,
        quotient_generators=quotient_generators,
        quotient_group=quotient_group,
        anisotropic=anisotropic,
        isotropic_nonzero=isotropic_nonzero,
    )


def matchings_of_four(items: Iterable[int]) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    a, b, c, d = tuple(items)
    return [
        tuple(sorted(((a, b), (c, d)))),
        tuple(sorted(((a, c), (b, d)))),
        tuple(sorted(((a, d), (b, c)))),
    ]


@dataclass(frozen=True)
class AxisBundle:
    axes: list[tuple[int, tuple[tuple[int, int], tuple[int, int]]]]
    axis_coordinates: list[int]
    endpoints: list[tuple[int, tuple[int, int]]]
    endpoint_axis_sign: dict[tuple[int, tuple[int, int]], tuple[int, int]]
    axis_generators: list[Permutation]
    endpoint_generators: list[Permutation]


def build_axes(bundle: W33Bundle, quotient: QuotientBundle) -> AxisBundle:
    axes: list[tuple[int, tuple[tuple[int, int], tuple[int, int]]]] = []
    axis_coordinates: list[int] = []
    endpoints: list[tuple[int, tuple[int, int]]] = []
    endpoint_axis_sign: dict[tuple[int, tuple[int, int]], tuple[int, int]] = {}

    for point in range(40):
        for matching in matchings_of_four(bundle.point_lines[point]):
            endpoint_words: list[int] = []
            endpoint_objects: list[tuple[int, tuple[int, int]]] = []
            for pair in matching:
                line_left, line_right = pair
                support = (
                    set(bundle.lines[line_left]) | set(bundle.lines[line_right])
                ) - {point}
                endpoint_words.append(sum(1 << vertex for vertex in support))
                endpoint_objects.append((point, tuple(sorted(pair))))
            canonical_left = reduce_mod_basis(endpoint_words[0], quotient.code_basis)
            canonical_right = reduce_mod_basis(endpoint_words[1], quotient.code_basis)
            if canonical_left != canonical_right:
                raise AssertionError("axis endpoints do not define one quotient class")
            axis_index = len(axes)
            axes.append((point, matching))
            axis_coordinates.append(quotient.canonical_to_coordinate[canonical_left])
            for sign, endpoint in zip((1, -1), endpoint_objects):
                endpoint_axis_sign[endpoint] = (axis_index, sign)
                endpoints.append(endpoint)

    line_index = {line: index for index, line in enumerate(bundle.lines)}
    axis_index = {axis: index for index, axis in enumerate(axes)}
    endpoint_index = {endpoint: index for index, endpoint in enumerate(endpoints)}

    def moved_line(line: int, g: Permutation) -> int:
        return line_index[tuple(sorted(g(point) for point in bundle.lines[line]))]

    def moved_axis(
        axis: tuple[int, tuple[tuple[int, int], tuple[int, int]]],
        g: Permutation,
    ) -> tuple[int, tuple[tuple[int, int], tuple[int, int]]]:
        point, matching = axis
        moved_matching = tuple(
            sorted(
                tuple(sorted((moved_line(left, g), moved_line(right, g))))
                for left, right in matching
            )
        )
        return g(point), moved_matching

    def moved_endpoint(
        endpoint: tuple[int, tuple[int, int]], g: Permutation
    ) -> tuple[int, tuple[int, int]]:
        point, pair = endpoint
        return g(point), tuple(sorted(moved_line(line, g) for line in pair))

    axis_generators = [
        Permutation([axis_index[moved_axis(axis, g)] for axis in axes])
        for g in bundle.point_generators
    ]
    endpoint_generators = [
        Permutation(
            [endpoint_index[moved_endpoint(endpoint, g)] for endpoint in endpoints]
        )
        for g in bundle.point_generators
    ]

    return AxisBundle(
        axes=axes,
        axis_coordinates=axis_coordinates,
        endpoints=endpoints,
        endpoint_axis_sign=endpoint_axis_sign,
        axis_generators=axis_generators,
        endpoint_generators=endpoint_generators,
    )


def e8_roots_scaled() -> list[tuple[int, ...]]:
    roots: list[tuple[int, ...]] = []
    for left in range(8):
        for right in range(left + 1, 8):
            for sign_left in (1, -1):
                for sign_right in (1, -1):
                    vector = [0] * 8
                    vector[left] = 2 * sign_left
                    vector[right] = 2 * sign_right
                    roots.append(tuple(vector))
    for signs in itertools.product((1, -1), repeat=8):
        if sum(sign == -1 for sign in signs) % 2 == 0:
            roots.append(tuple(signs))
    return sorted(set(roots))


E8_SIMPLE_ROOTS = [
    (1, -1, -1, -1, -1, -1, -1, 1),
    (2, 2, 0, 0, 0, 0, 0, 0),
    (-2, 2, 0, 0, 0, 0, 0, 0),
    (0, -2, 2, 0, 0, 0, 0, 0),
    (0, 0, -2, 2, 0, 0, 0, 0),
    (0, 0, 0, -2, 2, 0, 0, 0),
    (0, 0, 0, 0, -2, 2, 0, 0),
    (0, 0, 0, 0, 0, -2, 2, 0),
]
E8_CHAMBER = (1, 3, 9, 27, 2, 6, 18, 54)


def dot_scaled(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    return sum(a * b for a, b in zip(left, right))


@dataclass(frozen=True)
class E8ResidueBundle:
    roots: list[tuple[int, ...]]
    roots_by_residue: dict[int, tuple[tuple[int, ...], tuple[int, ...]]]
    positive_by_residue: dict[int, tuple[int, ...]]


def build_e8_residues() -> E8ResidueBundle:
    roots = e8_roots_scaled()
    simple_matrix = Matrix(8, 8, lambda row, col: E8_SIMPLE_ROOTS[col][row])
    inverse = simple_matrix.inv()
    roots_by_residue_lists: dict[int, list[tuple[int, ...]]] = {}
    for root in roots:
        coefficients = inverse * Matrix(root)
        if any(value.q != 1 for value in coefficients):
            raise AssertionError("root is not integral in the simple basis")
        residue = sum((int(value) % 2) << index for index, value in enumerate(coefficients))
        roots_by_residue_lists.setdefault(residue, []).append(root)
    roots_by_residue = {
        residue: tuple(sorted(pair))
        for residue, pair in roots_by_residue_lists.items()
    }
    positive_by_residue = {
        residue: max(pair, key=lambda root: dot_scaled(E8_CHAMBER, root))
        for residue, pair in roots_by_residue.items()
    }
    return E8ResidueBundle(
        roots=roots,
        roots_by_residue=roots_by_residue,
        positive_by_residue=positive_by_residue,
    )


def gf2_rank(vectors: Iterable[int]) -> int:
    return len(rowspace_basis(vectors))


def hyperbolic_basis(quadratic, bilinear) -> list[int]:
    def search(chosen: list[int]) -> list[int] | None:
        if len(chosen) == 8:
            return chosen
        first_candidates = [
            vector
            for vector in range(1, 256)
            if gf2_rank(chosen + [vector]) == len(chosen) + 1
            and quadratic(vector) == 0
            and all(bilinear(vector, previous) == 0 for previous in chosen)
        ]
        for first in first_candidates:
            for second in range(1, 256):
                if gf2_rank(chosen + [first, second]) != len(chosen) + 2:
                    continue
                if quadratic(second) or bilinear(first, second) != 1:
                    continue
                if any(bilinear(second, previous) for previous in chosen):
                    continue
                result = search(chosen + [first, second])
                if result is not None:
                    return result
        return None

    result = search([])
    if result is None:
        raise AssertionError("failed to find a hyperbolic basis")
    return result


def basis_coordinate_lookup(basis: list[int]) -> dict[int, int]:
    result: dict[int, int] = {}
    for mask in range(256):
        vector = 0
        for index, basis_vector in enumerate(basis):
            if (mask >> index) & 1:
                vector ^= basis_vector
        result[vector] = mask
    return result


def build_quadratic_isometry(
    quotient: QuotientBundle, e8: E8ResidueBundle
) -> tuple[dict[int, int], list[int], list[int]]:
    def source_q(coordinate: int) -> int:
        return (quotient.coordinate_representative[coordinate].bit_count() // 2) % 2

    def source_b(left: int, right: int) -> int:
        return (
            quotient.coordinate_representative[left]
            & quotient.coordinate_representative[right]
        ).bit_count() % 2

    def lattice_vector(residue: int) -> tuple[int, ...]:
        return tuple(
            sum(
                E8_SIMPLE_ROOTS[index][coordinate]
                for index in range(8)
                if (residue >> index) & 1
            )
            for coordinate in range(8)
        )

    def target_q(residue: int) -> int:
        vector = lattice_vector(residue)
        return (dot_scaled(vector, vector) // 8) % 2

    def target_b(left: int, right: int) -> int:
        return (dot_scaled(lattice_vector(left), lattice_vector(right)) // 4) % 2

    source_basis = hyperbolic_basis(source_q, source_b)
    target_basis = hyperbolic_basis(target_q, target_b)
    source_lookup = basis_coordinate_lookup(source_basis)

    images: dict[int, int] = {}
    for coordinate in range(256):
        mask = source_lookup[coordinate]
        image = 0
        for index, basis_vector in enumerate(target_basis):
            if (mask >> index) & 1:
                image ^= basis_vector
        images[coordinate] = image

    if set(images[c] for c in quotient.anisotropic) != set(e8.roots_by_residue):
        raise AssertionError("quadratic isometry misses E8 root residues")
    return images, source_basis, target_basis
