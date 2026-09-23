#!/usr/bin/env python3
"""Recover every trinification chart and close the Qpsi normalizer question.

The 45 Cartan-cubic supports are viewed as a 45 by 27 incidence matrix over
F3.  Its six-dimensional kernel contains 240 labelled colourings whose cubic
supports split as 18 monochromatic determinant terms and 27 rainbow trace
terms.  Modulo the six colour relabellings these are the classical 40 Steiner
triple systems.  The result is cross-checked against the repository's earlier
120 Steiner trihedral pairs and their 40 triads.

Projectivizing the kernel modulo its constant word gives 121 rays.  Their
three W(E6) orbits are identified objectwise, not merely numerically:

    121 = 36 double-sixes + 40 Steiner triads + 45 tritangents.

This realizes the repository's earlier abstract 40/45/36 norm-class census
inside one ternary cubic-conservation code.

Each unordered 9+9+9 partition has 6 sector assignments and 6^3 shared-factor
coordinate labellings.  The resulting 40*1296=51840 labelled tensor charts
form one regular W(E6) orbit.  This is the complete Weyl-compatible monomial
atlas for

    27 = (3,3bar,1) + (1,3,3bar) + (3bar,1,3).

For every chart, pull the anchored Qpsi clock into the exact
9_multiplicity by 3_internal factorization used by the Pauli243 execution
algebra.  A diagonal unitary normalizes I9 tensor M9 only if its 9 by 3 phase
table is multiplicatively rank one (equivalently, its exponent table is
additively separable modulo 12).  Exhaustion of the atlas gives

    <D12> intersect N(I9 tensor M9) = <D12^4> = C3.

Thus matter parity D12^6 does not normalize the execution algebra in any
W(E6)-compatible trinification chart.  In the best 5760 charts it differs
from a separable normalizer by one internal (m,q) phase cell, replicated over
the three external-qutrit states.  This is a finite chart theorem, not a
vacuum selection or a physical implementation of that interface phase.
Separate representation audits bound H27-equivariant and K-equivariant
address-to-operator maps by ranks 9 and 27, respectively.  The remaining
root-coordinate compiler must therefore change or reduce the symmetry.
"""
from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_steiner_trinification_qpsi_normalizer.json"
SECTORS = ("A_Bbar", "B_Cbar", "Abar_C")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def gf3_rref(rows: list[list[int]]) -> tuple[list[list[int]], list[int]]:
    matrix = [[entry % 3 for entry in row] for row in rows]
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        inverse = pow(matrix[pivot_row][column], -1, 3)
        matrix[pivot_row] = [(inverse * value) % 3 for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                (left - factor * right) % 3
                for left, right in zip(matrix[row], matrix[pivot_row])
            ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return matrix, pivot_columns


def gf3_kernel(rows: list[list[int]]) -> tuple[int, list[list[int]]]:
    reduced, pivots = gf3_rref(rows)
    free = [column for column in range(len(rows[0])) if column not in pivots]
    basis = []
    for free_column in free:
        vector = [0] * len(rows[0])
        vector[free_column] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = (-reduced[row][free_column]) % 3
        assert all(sum(a * b for a, b in zip(source, vector)) % 3 == 0 for source in rows)
        basis.append(vector)
    return len(pivots), basis


def gf3_rank(rows: list[list[int]]) -> int:
    return len(gf3_rref(rows)[1])


def gf3_inverse(matrix: list[list[int]]) -> list[list[int]]:
    size = len(matrix)
    augmented = [
        [value % 3 for value in row]
        + [int(row_index == column) for column in range(size)]
        for row_index, row in enumerate(matrix)
    ]
    for column in range(size):
        pivot = next(
            row for row in range(column, size) if augmented[row][column]
        )
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        inverse = pow(augmented[column][column], -1, 3)
        augmented[column] = [(inverse * value) % 3 for value in augmented[column]]
        for row in range(size):
            if row == column or not augmented[row][column]:
                continue
            factor = augmented[row][column]
            augmented[row] = [
                (left - factor * right) % 3
                for left, right in zip(augmented[row], augmented[column])
            ]
    assert all(
        augmented[row][column] == int(row == column)
        for row in range(size)
        for column in range(size)
    )
    return [row[size:] for row in augmented]


def row_times_matrix(row: tuple[int, ...] | list[int], matrix: list[list[int]]) -> tuple[int, ...]:
    return tuple(
        sum(row[index] * matrix[index][column] for index in range(len(row))) % 3
        for column in range(len(matrix[0]))
    )


def linear_combination(
    coefficients: tuple[int, ...] | list[int], basis: list[list[int]]
) -> tuple[int, ...]:
    return tuple(
        sum(coefficients[index] * basis[index][column] for index in range(len(basis))) % 3
        for column in range(len(basis[0]))
    )


def permute_word(word: tuple[int, ...], permutation: tuple[int, ...]) -> tuple[int, ...]:
    image = [0] * len(word)
    for point, value in enumerate(word):
        image[permutation[point]] = value
    return tuple(image)


def projective(vector: tuple[int, ...] | list[int]) -> tuple[int, ...]:
    vector = tuple(value % 3 for value in vector)
    leading = next(value for value in vector if value)
    inverse = pow(leading, -1, 3)
    return tuple((inverse * value) % 3 for value in vector)


def quotient_ray_key(word: tuple[int, ...]) -> tuple[int, ...] | None:
    shifted = tuple((value - word[0]) % 3 for value in word)
    if not any(shifted):
        return None
    return min(shifted, tuple((-value) % 3 for value in shifted))


def invariant_symmetric_form(matrices: list[list[list[int]]]) -> list[list[int]]:
    dimension = len(matrices[0])
    pairs = [
        (left, right)
        for left in range(dimension)
        for right in range(left, dimension)
    ]
    equations = []
    for matrix in matrices:
        for row in range(dimension):
            for column in range(row, dimension):
                equation = []
                for left, right in pairs:
                    coefficient = matrix[row][left] * matrix[column][right]
                    if left != right:
                        coefficient += matrix[row][right] * matrix[column][left]
                    if (left, right) == (row, column):
                        coefficient -= 1
                    equation.append(coefficient % 3)
                equations.append(equation)
    _, kernel = gf3_kernel(equations)
    assert len(kernel) == 1
    vector = kernel[0]
    form = [[0] * dimension for _ in range(dimension)]
    for value, (left, right) in zip(vector, pairs):
        form[left][right] = form[right][left] = value
    assert gf3_rank(form) == dimension
    return form


def canonical_partition(word: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(
        sorted(tuple(index for index, value in enumerate(word) if value == colour) for colour in range(3))
    )


def steiner_triads(base: dict) -> tuple[set[frozenset[int]], set[tuple[tuple[int, ...], ...]]]:
    all_points = frozenset(range(27))
    double_sixes = base["DS"]
    nonets = {
        all_points - frozenset().union(*(double_sixes[index] for index in triple))
        for triple in base["steiner"]
    }
    assert len(nonets) == 120
    ordered = sorted(nonets, key=lambda block: tuple(sorted(block)))
    triads = set()
    for left_index, left in enumerate(ordered):
        for right in ordered[left_index + 1 :]:
            if left & right:
                continue
            third = all_points - left - right
            if third in nonets:
                triads.add(
                    tuple(
                        sorted(
                            (tuple(sorted(left)), tuple(sorted(right)), tuple(sorted(third)))
                        )
                    )
                )
    assert len(triads) == 40
    return nonets, triads


def pair_components(
    lines: list[frozenset[int]], left: tuple[int, ...], right: tuple[int, ...]
) -> list[frozenset[int]]:
    left_set, right_set = set(left), set(right)
    neighbours = {point: set() for point in left_set | right_set}
    for line in lines:
        if len(line & left_set) == 1 and len(line & right_set) == 1:
            x = next(iter(line & left_set))
            y = next(iter(line & right_set))
            neighbours[x].add(y)
            neighbours[y].add(x)
    assert set(map(len, neighbours.values())) == {3}
    unseen = set(neighbours)
    components = []
    while unseen:
        stack = [min(unseen)]
        component = set()
        while stack:
            point = stack.pop()
            if point in component:
                continue
            component.add(point)
            stack.extend(neighbours[point] - component)
        unseen -= component
        components.append(frozenset(component))
    components.sort(key=lambda component: min(component))
    assert len(components) == 3
    assert all(len(component & left_set) == len(component & right_set) == 3 for component in components)
    return components


def chart_from_components(
    blocks: tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]],
    i_components: list[frozenset[int]],
    j_components: list[frozenset[int]],
    k_components: list[frozenset[int]],
    i_labels: tuple[int, ...],
    j_labels: tuple[int, ...],
    k_labels: tuple[int, ...],
) -> tuple[int, ...]:
    labels: dict[int, dict[str, int]] = {}
    for name, components, values in (
        ("i", i_components, i_labels),
        ("j", j_components, j_labels),
        ("k", k_components, k_labels),
    ):
        for component_index, component in enumerate(components):
            for point in component:
                labels.setdefault(point, {})[name] = values[component_index]

    encoded = [-1] * 27
    for sector, block in enumerate(blocks):
        for point in block:
            u = labels[point]["i"] if sector in (0, 2) else labels[point]["j"]
            v = labels[point]["j"] if sector == 0 else labels[point]["k"]
            encoded[point] = 9 * sector + 3 * u + v
    assert sorted(encoded) == list(range(27))
    return tuple(encoded)


def build_atlas(
    partitions: set[tuple[tuple[int, ...], ...]], lines: list[frozenset[int]]
) -> tuple[set[tuple[int, ...]], Counter[tuple[tuple[int, ...], ...]]]:
    coordinate_permutations = list(itertools.permutations(range(3)))
    atlas: set[tuple[int, ...]] = set()
    counts: Counter[tuple[tuple[int, ...], ...]] = Counter()
    for partition in sorted(partitions):
        for blocks in itertools.permutations(partition):
            ab, bc, ac = blocks
            i_components = pair_components(lines, ab, ac)
            j_components = pair_components(lines, ab, bc)
            k_components = pair_components(lines, bc, ac)
            for i_labels, j_labels, k_labels in itertools.product(
                coordinate_permutations, repeat=3
            ):
                chart = chart_from_components(
                    blocks,
                    i_components,
                    j_components,
                    k_components,
                    i_labels,
                    j_labels,
                    k_labels,
                )
                atlas.add(chart)
                counts[partition] += 1
    return atlas, counts


def decode(code: int) -> tuple[int, int, int]:
    sector, residue = divmod(code, 9)
    u, v = divmod(residue, 3)
    return sector, u, v


def mq(code: int) -> tuple[int, int]:
    sector, u, v = decode(code)
    if sector == 0:
        return (u - v) % 3, (2 * (u + v)) % 3
    if sector == 1:
        return 3 + v, u
    return 6 + v, u


def charge_matrix(chart: tuple[int, ...], graph, anchor: int) -> list[int]:
    table: list[int | None] = [None] * 27
    for point, code in enumerate(chart):
        multiplicity, qutrit = mq(code)
        table[3 * multiplicity + qutrit] = (
            1 + 3 * int(point == anchor) - 3 * int(graph.has_edge(anchor, point))
        )
    assert all(value is not None for value in table)
    return [int(value) for value in table]


def exponent_table_factorizes(charges: list[int], power: int) -> bool:
    exponents = [(power * charge) % 12 for charge in charges]
    return all(
        (
            exponents[3 * multiplicity + qutrit]
            - exponents[3 * multiplicity]
            - exponents[qutrit]
            + exponents[0]
        )
        % 12
        == 0
        for multiplicity in range(9)
        for qutrit in range(3)
    )


def parity_mask(charges: list[int]) -> int:
    return sum(1 << index for index, charge in enumerate(charges) if charge % 2)


def separable_binary_tables() -> dict[int, tuple[int, int]]:
    tables: dict[int, tuple[int, int]] = {}
    # Fix alpha_0=0 to remove the simultaneous global complement redundancy.
    for alpha in range(1 << 9):
        if alpha & 1:
            continue
        for beta in range(1 << 3):
            mask = 0
            for multiplicity in range(9):
                for qutrit in range(3):
                    if ((alpha >> multiplicity) & 1) ^ ((beta >> qutrit) & 1):
                        mask |= 1 << (3 * multiplicity + qutrit)
            tables[mask] = (alpha, beta)
    assert len(tables) == 2048
    return tables


def rows_digest(rows: set[tuple[int, ...]]) -> str:
    digest = hashlib.sha256()
    for row in sorted(rows):
        digest.update(bytes(row))
        digest.update(b"\xff")
    return digest.hexdigest()


def main(write: bool = True) -> dict:
    h27_obstruction = json.loads(
        (ROOT / "data/w33_address_operator_h27_intertwiner_obstruction.json").read_text()
    )
    k81_obstruction = json.loads(
        (ROOT / "data/w33_scheduler_operator_k81_intertwiner_obstruction.json").read_text()
    )
    assert h27_obstruction["intertwiner"]["maximum_rank"] == 9
    assert h27_obstruction["intertwiner"]["invertible_intertwiner_exists"] is False
    assert k81_obstruction["intertwiner"]["maximum_rank"] == 27
    assert k81_obstruction["intertwiner"]["invertible_equivariant_compiler_exists"] is False
    common = load(
        ROOT / "analysis/w33_pass4992_4999_common.py",
        "steiner_trinification_common",
    )
    base = common.build_base()
    graph = base["G27"]
    lines = [frozenset(line) for line in base["tritangents"]]
    assert len(lines) == 45

    incidence = [[int(point in line) for point in range(27)] for line in lines]
    rank, kernel_basis = gf3_kernel(incidence)
    assert rank == 21 and len(kernel_basis) == 6

    balanced = 0
    special_words = []
    ordinary_words = []
    codeword_to_coefficients: dict[tuple[int, ...], tuple[int, ...]] = {}
    weight_census: Counter[int] = Counter()
    content_census: Counter[tuple[int, int, int]] = Counter()
    partitions: set[tuple[tuple[int, ...], ...]] = set()
    ordinary_partitions: set[tuple[tuple[int, ...], ...]] = set()
    partition_multiplicity: Counter[tuple[tuple[int, ...], ...]] = Counter()
    ordinary_partition_multiplicity: Counter[
        tuple[tuple[int, ...], ...]
    ] = Counter()
    partition_monochromatic_lines: dict[
        tuple[tuple[int, ...], ...], frozenset[int]
    ] = {}
    for coefficients in itertools.product(range(3), repeat=6):
        word = linear_combination(coefficients, kernel_basis)
        codeword_to_coefficients[word] = coefficients
        counts = Counter(word)
        weight_census[sum(value != 0 for value in word)] += 1
        content_census[tuple(counts[colour] for colour in range(3))] += 1
        if Counter(word) != Counter({0: 9, 1: 9, 2: 9}):
            continue
        balanced += 1
        patterns = Counter(tuple(sorted(word[point] for point in line)) for line in lines)
        monochromatic_lines = frozenset(
            index
            for index, line in enumerate(lines)
            if len({word[point] for point in line}) == 1
        )
        monochromatic = sum(
            count for pattern, count in patterns.items() if len(set(pattern)) == 1
        )
        rainbow = patterns[(0, 1, 2)]
        partition = canonical_partition(word)
        partition_monochromatic_lines[partition] = monochromatic_lines
        if (monochromatic, rainbow) == (18, 27):
            special_words.append(word)
            partitions.add(partition)
            partition_multiplicity[partition] += 1
        elif (monochromatic, rainbow) == (12, 33):
            ordinary_words.append(word)
            ordinary_partitions.add(partition)
            ordinary_partition_multiplicity[partition] += 1
        else:
            raise AssertionError((monochromatic, rainbow))
    assert len(codeword_to_coefficients) == 729
    assert weight_census == Counter({0: 1, 12: 72, 18: 510, 21: 144, 27: 2})
    assert content_census == Counter(
        {
            (27, 0, 0): 1,
            (0, 27, 0): 1,
            (0, 0, 27): 1,
            (15, 6, 6): 72,
            (6, 15, 6): 72,
            (6, 6, 15): 72,
            (9, 9, 9): 510,
        }
    )
    assert balanced == 510
    assert len(special_words) == 240
    assert len(ordinary_words) == 270
    assert len(partitions) == 40
    assert len(ordinary_partitions) == 45
    assert set(partition_multiplicity.values()) == {6}
    assert set(ordinary_partition_multiplicity.values()) == {6}

    steiner_nonets, prior_triads = steiner_triads(base)
    assert prior_triads == partitions

    # The other 45 balanced partitions are objectwise the 45 tritangents:
    # their twelve monochromatic cubics are exactly the twelve other cubics
    # meeting the distinguished tritangent.
    tritangent_stars = {
        frozenset(
            other
            for other, other_line in enumerate(lines)
            if other != index and line & other_line
        ): index
        for index, line in enumerate(lines)
    }
    assert set(map(len, tritangent_stars)) == {12}
    ordinary_partition_to_tritangent = {
        partition: tritangent_stars[partition_monochromatic_lines[partition]]
        for partition in ordinary_partitions
    }
    assert set(ordinary_partition_to_tritangent.values()) == set(range(45))

    # Weight-twelve words recover the 36 double-six supports exactly.
    double_six_supports = {
        frozenset(index for index, value in enumerate(word) if value)
        for word in codeword_to_coefficients
        if sum(value != 0 for value in word) == 12
    }
    assert double_six_supports == set(base["DS"])

    # The transpose is the same cubic incidence map used by the earlier
    # line-holonomy calculation: its line-side kernel has dimension 24.
    transpose = [list(column) for column in zip(*incidence)]
    transpose_rank, line_kernel_basis = gf3_kernel(transpose)
    assert transpose_rank == 21 and len(line_kernel_basis) == 24

    # Each block has six determinant supports; the other 27 supports are
    # rainbow traces.  Pairwise rainbow incidence reconstructs three K3,3
    # component systems, hence shared i,j,k coordinates without root data.
    for partition in partitions:
        assert [
            sum(1 for line in lines if line <= set(block)) for block in partition
        ] == [6, 6, 6]
        assert sum(
            1 for line in lines if all(len(line & set(block)) == 1 for block in partition)
        ) == 27

    atlas, chart_counts = build_atlas(partitions, lines)
    assert len(atlas) == 51840
    assert set(chart_counts.values()) == {1296}

    group_data = common.build_group(base)
    weyl_generators = group_data["gp"] + [group_data["trans"][0]]
    we6 = common.closure(weyl_generators, 27)
    assert len(we6) == 51840
    assert len({permutation[0] for permutation in we6}) == 27

    # Projectivize the six-dimensional conservation code modulo its invariant
    # constant word.  The resulting PG(4,3) has a complete objectwise
    # 36+40+45 dictionary.
    constants = {
        word for word in codeword_to_coefficients if len(set(word)) == 1
    }
    assert len(constants) == 3
    all_ones = (1,) * 27
    constant_coefficients = codeword_to_coefficients[all_ones]
    coefficient_basis = [list(constant_coefficients)]
    for index in range(6):
        candidate = [int(index == column) for column in range(6)]
        if gf3_rank(coefficient_basis + [candidate]) > len(coefficient_basis):
            coefficient_basis.append(candidate)
        if len(coefficient_basis) == 6:
            break
    assert len(coefficient_basis) == 6
    coefficient_basis_inverse = gf3_inverse(coefficient_basis)

    def quotient_coordinates(word: tuple[int, ...]) -> tuple[int, ...]:
        coefficients = codeword_to_coefficients[word]
        coordinates = row_times_matrix(coefficients, coefficient_basis_inverse)
        return coordinates[1:]

    ray_members: defaultdict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
    for word in codeword_to_coefficients:
        ray_key = quotient_ray_key(word)
        if ray_key is not None:
            ray_members[ray_key].append(word)
    assert len(ray_members) == 121
    assert set(map(len, ray_members.values())) == {6}

    ray_points = sorted(
        {projective(quotient_coordinates(members[0])) for members in ray_members.values()}
    )
    assert len(ray_points) == 121
    ray_point_index = {point: index for index, point in enumerate(ray_points)}
    ray_kind_by_point: dict[tuple[int, ...], str] = {}
    for members in ray_members.values():
        point = projective(quotient_coordinates(members[0]))
        weight_twelve = [
            word for word in members if sum(value != 0 for value in word) == 12
        ]
        if weight_twelve:
            assert len(weight_twelve) == 2
            support = frozenset(
                index for index, value in enumerate(weight_twelve[0]) if value
            )
            assert support in double_six_supports
            kind = "double_six"
        else:
            assert all(Counter(word) == Counter({0: 9, 1: 9, 2: 9}) for word in members)
            partition = canonical_partition(members[0])
            if partition in partitions:
                kind = "steiner_triad"
            else:
                assert partition in ordinary_partitions
                assert ordinary_partition_to_tritangent[partition] in range(45)
                kind = "tritangent"
        ray_kind_by_point[point] = kind
    assert Counter(ray_kind_by_point.values()) == Counter(
        {"double_six": 36, "steiner_triad": 40, "tritangent": 45}
    )

    induced_matrices: list[list[list[int]]] = []
    for permutation in weyl_generators:
        matrix = []
        for coefficients in coefficient_basis[1:]:
            word = linear_combination(coefficients, kernel_basis)
            image = permute_word(word, permutation)
            image_coordinates = row_times_matrix(
                codeword_to_coefficients[image], coefficient_basis_inverse
            )
            matrix.append(list(image_coordinates[1:]))
        assert gf3_rank(matrix) == 5
        induced_matrices.append(matrix)

    ray_generators = []
    for matrix in induced_matrices:
        ray_generators.append(
            tuple(
                ray_point_index[projective(row_times_matrix(point, matrix))]
                for point in ray_points
            )
        )
    ray_action = common.closure(ray_generators, 121)
    assert len(ray_action) == 51840

    orbit_sizes = []
    unseen_points = set(range(121))
    while unseen_points:
        seed = min(unseen_points)
        orbit = {permutation[seed] for permutation in ray_action}
        unseen_points -= orbit
        orbit_sizes.append(len(orbit))
    assert sorted(orbit_sizes) == [36, 40, 45]

    invariant_form = invariant_symmetric_form(induced_matrices)

    def norm(point: tuple[int, ...]) -> int:
        return sum(
            point[left] * invariant_form[left][right] * point[right]
            for left in range(5)
            for right in range(5)
        ) % 3

    double_six_point = next(
        point for point, kind in ray_kind_by_point.items() if kind == "double_six"
    )
    scale = 2 * pow(norm(double_six_point), -1, 3) % 3
    invariant_form = [
        [(scale * value) % 3 for value in row] for row in invariant_form
    ]
    norm_by_kind = {
        kind: {norm(point) for point, point_kind in ray_kind_by_point.items() if point_kind == kind}
        for kind in ("double_six", "steiner_triad", "tritangent")
    }
    assert norm_by_kind == {
        "double_six": {2},
        "steiner_triad": {0},
        "tritangent": {1},
    }
    assert Counter(norm(point) for point in ray_points) == Counter({0: 40, 1: 45, 2: 36})

    seed_partition = frozenset(frozenset(block) for block in min(partitions))
    partition_stabilizer = sum(
        frozenset(frozenset(permutation[point] for point in block) for block in seed_partition)
        == seed_partition
        for permutation in we6
    )
    assert partition_stabilizer == 1296

    seed_chart = min(atlas)
    chart_orbit = set()
    for permutation in we6:
        image = [-1] * 27
        for point, code in enumerate(seed_chart):
            image[permutation[point]] = code
        chart_orbit.add(tuple(image))
    assert chart_orbit == atlas

    # All Qpsi anchors have the same one-nonet/two-nonet charge profile.
    profile_census = Counter()
    for anchor in range(27):
        charges = {
            point: 1 + 3 * int(point == anchor) - 3 * int(graph.has_edge(anchor, point))
            for point in range(27)
        }
        for partition in partitions:
            profile = tuple(
                sorted(tuple(sorted(Counter(charges[point] for point in block).items())) for block in partition)
            )
            profile_census[profile] += 1
    expected_profile = (
        ((-2, 3), (1, 6)),
        ((-2, 3), (1, 6)),
        ((-2, 4), (1, 4), (4, 1)),
    )
    assert profile_census == Counter({expected_profile: 27 * 40})

    # Directly exhaust the complete labelled atlas for one anchor.  W(E6)
    # transitivity and Qpsi equivariance make this the census for every anchor.
    normalizing_counts = [0] * 12
    parity_tables: Counter[int] = Counter()
    charge_tables: dict[tuple[int, ...], list[int]] = {}
    for chart in atlas:
        charges = charge_matrix(chart, graph, 0)
        charge_tables[chart] = charges
        for power in range(12):
            normalizing_counts[power] += int(exponent_table_factorizes(charges, power))
        parity_tables[parity_mask(charges)] += 1
    assert normalizing_counts == [51840, 0, 0, 0, 51840, 0, 0, 0, 51840, 0, 0, 0]
    assert len(parity_tables) == 27
    assert Counter(parity_tables.values()) == Counter({1920: 27})

    separable = separable_binary_tables()
    distance_census: Counter[int] = Counter()
    best_witness = None
    for chart in sorted(atlas):
        mask = parity_mask(charge_tables[chart])
        distance = min((mask ^ candidate).bit_count() for candidate in separable)
        distance_census[distance] += 1
        if distance == 1 and best_witness is None:
            nearest = min(
                candidate
                for candidate in separable
                if (mask ^ candidate).bit_count() == 1
            )
            alpha, beta = separable[nearest]
            defect_position = (mask ^ nearest).bit_length() - 1
            best_witness = {
                "anchor": 0,
                "chart": [
                    {
                        "point": point,
                        "sector": SECTORS[decode(code)[0]],
                        "u": decode(code)[1],
                        "v": decode(code)[2],
                        "multiplicity_m": mq(code)[0],
                        "internal_q": mq(code)[1],
                    }
                    for point, code in enumerate(chart)
                ],
                "separable_alpha_negative_m": [
                    index for index in range(9) if (alpha >> index) & 1
                ],
                "separable_beta_negative_q": [
                    index for index in range(3) if (beta >> index) & 1
                ],
                "single_defect_mq": [defect_position // 3, defect_position % 3],
                "matter81_defect_support": [
                    [defect_position // 3, defect_position % 3, external]
                    for external in range(3)
                ],
            }
    assert distance_census == Counter({1: 5760, 5: 34560, 6: 11520})
    assert best_witness is not None

    # A fixed labelled chart sees the same relative orbit census 3+18+6;
    # multiplying by the order-1920 anchor stabilizer gives the atlas census.
    seed_distances = Counter()
    for anchor in range(27):
        mask = parity_mask(charge_matrix(seed_chart, graph, anchor))
        seed_distances[min((mask ^ candidate).bit_count() for candidate in separable)] += 1
    assert seed_distances == Counter({1: 3, 5: 18, 6: 6})

    partition_rows = {
        tuple(value for block in partition for value in (*block, 255))
        for partition in partitions
    }
    ordinary_map_rows = {
        tuple(value for block in partition for value in (*block, 255))
        + (ordinary_partition_to_tritangent[partition],)
        for partition in ordinary_partitions
    }
    double_six_rows = {tuple(sorted(support)) for support in double_six_supports}
    out = {
        "schema": "w33.steiner_trinification_qpsi_normalizer.v3",
        "status": "PASS_ALL_WE6_TRINIFICATION_CHARTS_EXCLUDE_NONFI_QPSI_NORMALIZERS",
        "headline": (
            "The ternary kernel of the 45 Cartan-cubic supports is a [27,6,12]_3 "
            "conservation code. Projectivizing it modulo constants gives the objectwise "
            "PG(4,3) dictionary 121=36 double-sixes+40 Steiner triads+45 tritangents. "
            "The 40 Steiner partitions expand to 51840 tensor charts, exactly one regular "
            "W(E6) orbit. Across that complete atlas and all 27 Qpsi anchors, D12^k "
            "normalizes I9 tensor M9 exactly for k=0,4,8. Matter parity k=6 is never a "
            "normalizer, although 5760 charts reduce it to a separable normalizer times "
            "one address-conditioned phase cell."
        ),
        "ternary_kernel": {
            "incidence_matrix_shape": [45, 27],
            "rank_F3": rank,
            "nullity_F3": len(kernel_basis),
            "code_parameters": "[27,6,12]_3",
            "kernel_word_count": 3 ** len(kernel_basis),
            "weight_enumerator": {
                str(weight): count for weight, count in sorted(weight_census.items())
            },
            "complete_content_census": {
                ",".join(map(str, content)): count
                for content, count in sorted(content_census.items())
            },
            "balanced_9_9_9_words": balanced,
            "special_labelled_words": len(special_words),
            "special_support_split": {
                "monochromatic_determinant_terms": 18,
                "rainbow_trace_terms": 27,
            },
            "ordinary_labelled_words": len(ordinary_words),
            "ordinary_support_split": {
                "monochromatic_terms": 12,
                "rainbow_terms": 33,
            },
            "unlabelled_partitions": len(partitions),
            "other_unlabelled_partitions": len(ordinary_partitions),
            "colourings_per_partition": 6,
            "kernel_basis": kernel_basis,
            "partition_digest_sha256": rows_digest(partition_rows),
            "line_side_transpose_rank_F3": transpose_rank,
            "line_side_kernel_dimension_F3": len(line_kernel_basis),
        },
        "projective_121_dictionary": {
            "construction": "P(ker_F3(C) / <all-ones>) = PG(4,3)",
            "quotient_vector_dimension": 5,
            "projective_ray_count": len(ray_points),
            "codeword_lifts_per_ray": 6,
            "W_E6_projective_action_order": len(ray_action),
            "W_E6_projective_orbit_sizes": sorted(orbit_sizes),
            "invariant_quadratic_form_matrix_F3": invariant_form,
            "norm_class_dictionary": {
                "norm_0": "40 Steiner triads",
                "norm_1": "45 tritangents",
                "norm_2": "36 double-sixes",
            },
            "objectwise_checks": {
                "36_weight12_supports_equal_36_prior_double_sixes": True,
                "40_eighteen_monochromatic_partitions_equal_40_prior_steiner_triads": True,
                "45_twelve_monochromatic_partitions_equal_45_tritangent_stars": True,
            },
            "weight12_double_six_digest_sha256": rows_digest(double_six_rows),
            "steiner_partition_digest_sha256": rows_digest(partition_rows),
            "tritangent_partition_map_digest_sha256": rows_digest(ordinary_map_rows),
            "projective_points_digest_sha256": rows_digest(set(ray_points)),
            "prior_owner_of_abstract_norm_classes": (
                "analysis/PASS4857_4864_EXECUTED_OUTCOMES.md and "
                "analysis/w33_pass4863_4864_o5_adjoint_homology.py"
            ),
            "increment": (
                "The cubic-conservation code supplies one objectwise carrier for all three "
                "norm classes; Pass4863 previously identified only the 36-class with double-sixes."
            ),
        },
        "steiner_prior_crosscheck": {
            "prior_owner": "analysis/w33_e6_120_steiner_trihedral_pairs.py",
            "prior_steiner_nonets": len(steiner_nonets),
            "prior_triads": len(prior_triads),
            "kernel_partitions_equal_prior_40_triads": True,
            "prior_art_boundary": (
                "The 120 Steiner sets, their 40 triple systems, the A2^3 interpretation, "
                "and the index-40 W(E6) orbit are classical and already owned in the repository."
            ),
        },
        "trinification_atlas": {
            "partition_block_sizes": [9, 9, 9],
            "cubic_support_split_per_partition": "3*6 determinant + 27 rainbow trace",
            "charts_per_partition": 1296,
            "chart_count_factorization": "6 sector assignments * 6^3 shared-factor relabellings",
            "total_labelled_charts": len(atlas),
            "W_E6_order": len(we6),
            "partition_stabilizer_order": partition_stabilizer,
            "W_E6_action_on_labelled_atlas": "regular",
            "atlas_digest_sha256": rows_digest(atlas),
        },
        "qpsi_nonet_profile": {
            "distinguished_nonet": {"4": 1, "-2": 4, "1": 4},
            "other_two_nonets_each": {"-2": 3, "1": 6},
            "anchor_partition_pairs_checked": 27 * 40,
        },
        "normalizer_closure": {
            "execution_algebra": "I9_multiplicity tensor M9_internal_external",
            "criterion": (
                "A diagonal normalizer must factor across multiplicity versus active registers; "
                "equivalently its 9x3 Qpsi exponent table has vanishing additive 2x2 minors mod 12."
            ),
            "normalizing_chart_counts_by_D12_power": {
                str(power): count for power, count in enumerate(normalizing_counts)
            },
            "normalizing_powers_mod12": [0, 4, 8],
            "intersection": "<D12> intersect N(I9 tensor M9) = <D12^4> = C3",
            "matter_parity_D12_power6_normalizes_in_any_chart": False,
            "all_27_anchors_follow_by_W_E6_equivariance": True,
        },
        "minimal_interface_repair": {
            "separable_binary_phase_tables": len(separable),
            "distinct_matter_parity_tables_over_atlas": len(parity_tables),
            "multiplicity_of_each_parity_table": 1920,
            "hamming_distance_to_separable_table_census": {
                str(distance): count for distance, count in sorted(distance_census.items())
            },
            "relative_anchor_distance_census_in_one_chart": {
                str(distance): count for distance, count in sorted(seed_distances.items())
            },
            "minimum_phase_cells": min(distance_census),
            "best_chart_count": distance_census[1],
            "best_witness": best_witness,
            "meaning": (
                "In the best Weyl gauges, matter parity is one internal (m,q) sign cell away "
                "from a tensor normalizer. On matter81 that cell is replicated over the three "
                "external-qutrit states, so the minimal diagonal interface correction has support 3."
            ),
        },
        "equivariant_compiler_obstruction": {
            "H27_maximum_rank": h27_obstruction["intertwiner"]["maximum_rank"],
            "H27_target_dimension": h27_obstruction["intertwiner"]["target_dimension"],
            "K81_maximum_rank": k81_obstruction["intertwiner"]["maximum_rank"],
            "K81_target_dimension": k81_obstruction["intertwiner"]["target_dimension"],
            "invertible_H27_equivariant_intertwiner_exists": False,
            "invertible_K81_equivariant_compiler_exists": False,
            "surviving_frontier": (
                "The finite normalizer is closed independently of the root gauge. A physical "
                "root-coordinate compiler must be non-equivariant, proper-subgroup-covariant, "
                "or otherwise symmetry-changing."
            ),
        },
        "ownership_and_increment": {
            "classical_and_repo_prior": [
                "40 Steiner triple systems / A2^3 subsystems",
                "120 Steiner trihedral pairs grouped into 40 triads",
                "W(E6) order 51840 and index-40 A2^3 stabilizer",
                "abstract PG(4,3) orthogonal norm-class sizes 40,45,36 and the 36-class double-six identification",
                "the representation-dimension triangle 40+36+45=121",
            ],
            "new_executable_composition": [
                "the ternary [27,6,12] cubic-conservation code and its full weight enumerator",
                "the objectwise projective dictionary 121=36 double-sixes+40 Steiner triads+45 tritangents",
                "the dual-kernel bridge between six point charges and 24 line holonomies",
                "the F3 balanced-kernel census 510=240+270 -> 40+45 partitions",
                "the complete 51840-chart coordinate atlas as a regular W(E6) torsor",
                "the all-chart Qpsi normalizer intersection C3",
                "the exact one-cell/three-matter-state minimal interface repair",
            ],
            "external_checks": [
                "https://arxiv.org/abs/math/0507118",
                "https://sites.lsa.umich.edu/idolga/wp-content/uploads/sites/1334/2024/08/CAG.21.pdf",
            ],
        },
        "boundary": (
            "This exhausts Weyl-compatible monomial trinification charts and diagonal Qpsi "
            "powers. It does not select a physical chart or vacuum, prove that the one-cell "
            "repair is dynamically available, select a symmetry-changing root-coordinate "
            "compiler, or identify observed particles with individual weights. Full H27/K "
            "equivariant basis conjugacies are already excluded by the rank-9/rank-27 obstructions."
        ),
        "parents": [
            "data/w33_address_operator_h27_intertwiner_obstruction.json",
            "data/w33_scheduler_operator_k81_intertwiner_obstruction.json",
        ],
        "checks": {
            "incidence_rank21_nullity6": True,
            "ternary_code_is_27_6_12_with_frozen_weight_enumerator": True,
            "kernel_census_729_and_balanced_split_510_equals240_plus270": True,
            "projective_quotient_has_121_rays_in_36_40_45_orbits": True,
            "projective_dictionary_is_objectwise_double_six_steiner_tritangent": True,
            "invariant_O5_norm_classes_are_40_45_36": True,
            "same_incidence_has_point_nullity6_and_line_nullity24": True,
            "kernel_partitions_equal_prior_steiner_triads": True,
            "each_partition_has_18_determinant_27_rainbow_supports": True,
            "atlas_has_40_times1296_equals51840_charts": True,
            "atlas_is_one_regular_W_E6_orbit": True,
            "all_anchor_nonet_profiles_agree": True,
            "only_D12_powers_0_4_8_normalize": True,
            "matter_parity_never_normalizes": True,
            "minimal_interface_repair_is_one_phase_cell": True,
            "H27_equivariant_intertwiner_is_rank_obstructed": True,
            "K81_equivariant_compiler_is_rank_obstructed": True,
            "symmetry_changing_compiler_remains_open": True,
        },
    }
    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(
        json.dumps(
            {
                "status": out["status"],
                "kernel": out["ternary_kernel"],
                "projective_dictionary": out["projective_121_dictionary"],
                "atlas": out["trinification_atlas"],
                "normalizer": out["normalizer_closure"],
                "repair": {
                    key: out["minimal_interface_repair"][key]
                    for key in (
                        "hamming_distance_to_separable_table_census",
                        "minimum_phase_cells",
                        "best_chart_count",
                    )
                },
            },
            indent=2,
        )
    )
    return out


if __name__ == "__main__":
    main(True)
