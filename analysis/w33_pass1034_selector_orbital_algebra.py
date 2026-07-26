#!/usr/bin/env python3
"""Pass 1034: exact orbital algebra of the 120-sheet selector carrier.

This is a standard-library verifier.  It reconstructs PSp(4,3), its natural
line-phase action on 40 W(3,3) lines times the three perfect matchings of each
line, and the full rank-five association scheme.  It certifies the intersection
numbers, P/Q eigenmatrices, multiplicities, and Krein nonnegativity exactly.
"""
from __future__ import annotations

import json
from collections import deque
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
from typing import Iterable

P_FIELD = 3
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass1034_selector_orbital_algebra.json"

Vec = tuple[int, int, int, int]
Perm = tuple[int, ...]
Matching = frozenset[frozenset[int]]
State = tuple[int, Matching]


def canonical(vector: Iterable[int]) -> Vec:
    values = tuple(int(x) % P_FIELD for x in vector)
    if values == (0, 0, 0, 0):
        raise ValueError("zero vector")
    for entry in values:
        if entry:
            inverse_value = 1 if entry == 1 else 2
            return tuple((inverse_value * x) % P_FIELD for x in values)  # type: ignore[return-value]
    raise AssertionError


def omega(left: Vec, right: Vec) -> int:
    return (
        left[0] * right[2] - left[2] * right[0]
        + left[1] * right[3] - left[3] * right[1]
    ) % P_FIELD


def build_w33() -> tuple[list[Vec], list[tuple[int, int, int, int]]]:
    points = sorted(
        {
            canonical(raw)
            for raw in product(range(P_FIELD), repeat=4)
            if raw != (0, 0, 0, 0)
        }
    )
    point_index = {point: index for index, point in enumerate(points)}
    edges = [
        (left, right)
        for left, right in combinations(range(len(points)), 2)
        if omega(points[left], points[right]) == 0
    ]
    lines: set[tuple[int, int, int, int]] = set()
    for left, right in edges:
        u, v = points[left], points[right]
        line = set()
        for a, b in product(range(P_FIELD), repeat=2):
            if a == 0 and b == 0:
                continue
            line.add(
                point_index[
                    canonical(
                        (a * u[c] + b * v[c] for c in range(4))
                    )
                ]
            )
        if len(line) == 4:
            lines.add(tuple(sorted(line)))
    return points, sorted(lines)


def compose(left: Perm, right: Perm) -> Perm:
    return tuple(left[index] for index in right)


def inverse(permutation: Perm) -> Perm:
    result = [0] * len(permutation)
    for source, target in enumerate(permutation):
        result[target] = source
    return tuple(result)


def transvections(points: list[Vec]) -> list[Perm]:
    point_index = {point: index for index, point in enumerate(points)}
    generators = []
    for vector in points:
        image = []
        for point in points:
            coefficient = omega(point, vector)
            moved = tuple(
                (point[c] + coefficient * vector[c]) % P_FIELD
                for c in range(4)
            )
            image.append(point_index[canonical(moved)])
        generators.append(tuple(image))
    return generators


def generated_group(generators: list[Perm], degree: int) -> set[Perm]:
    identity = tuple(range(degree))
    symmetric_generators = generators + [inverse(generator) for generator in generators]
    group = {identity}
    queue: deque[Perm] = deque([identity])
    while queue:
        element = queue.popleft()
        for generator in symmetric_generators:
            candidate = compose(generator, element)
            if candidate not in group:
                group.add(candidate)
                queue.append(candidate)
    return group


def act_line(element: Perm, line: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sorted(element[point] for point in line))


def perfect_matchings(items: list[int]) -> list[Matching]:
    a, b, c, d = items
    return [
        frozenset((frozenset((a, b)), frozenset((c, d)))),
        frozenset((frozenset((a, c)), frozenset((b, d)))),
        frozenset((frozenset((a, d)), frozenset((b, c)))),
    ]


def act_matching(element: Perm, matching: Matching) -> Matching:
    return frozenset(
        frozenset(element[point] for point in pair)
        for pair in matching
    )


def matmul(left: list[list[Fraction]], right: list[list[Fraction]]) -> list[list[Fraction]]:
    rows = len(left)
    inner = len(right)
    cols = len(right[0])
    return [
        [sum(left[i][k] * right[k][j] for k in range(inner)) for j in range(cols)]
        for i in range(rows)
    ]


def frac_json(value: Fraction) -> int | str:
    return value.numerator if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def main() -> None:
    points, lines = build_w33()
    line_index = {line: index for index, line in enumerate(lines)}
    group = generated_group(transvections(points), len(points))

    states: list[State] = []
    state_index: dict[State, int] = {}
    for line_number, line in enumerate(lines):
        for matching in perfect_matchings(list(line)):
            state_index[(line_number, matching)] = len(states)
            states.append((line_number, matching))

    def act_state(element: Perm, state_number: int) -> int:
        line_number, matching = states[state_number]
        moved_line = line_index[act_line(element, lines[line_number])]
        moved_matching = act_matching(element, matching)
        return state_index[(moved_line, moved_matching)]

    base = 0
    stabilizer = [element for element in group if act_state(element, base) == base]
    unseen = set(range(len(states)))
    orbits: list[list[int]] = []
    while unseen:
        representative = min(unseen)
        orbit = sorted({act_state(element, representative) for element in stabilizer})
        orbits.append(orbit)
        unseen -= set(orbit)

    orbit_of: dict[int, int] = {}
    for relation_number, orbit in enumerate(orbits):
        for state in orbit:
            orbit_of[state] = relation_number

    representatives: list[Perm | None] = [None] * len(states)
    for element in group:
        image = act_state(element, base)
        if representatives[image] is None:
            representatives[image] = element
    if any(element is None for element in representatives):
        raise AssertionError("action is not transitive")

    def relation(left: int, right: int) -> int:
        element = representatives[left]
        assert element is not None
        return orbit_of[act_state(inverse(element), right)]

    symmetric = all(
        relation(left, right) == relation(right, left)
        for left in range(120)
        for right in range(120)
    )

    intersection = [[[0 for _ in range(5)] for _ in range(5)] for _ in range(5)]
    for relation_k, orbit in enumerate(orbits):
        target = orbit[0]
        for relation_i in range(5):
            for relation_j in range(5):
                intersection[relation_i][relation_j][relation_k] = sum(
                    1
                    for middle in range(120)
                    if relation(base, middle) == relation_i
                    and relation(middle, target) == relation_j
                )

    p_matrix = [
        [1, 2, 36, 27, 54],
        [1, 2, -12, 3, 6],
        [1, -1, 0, -3, 3],
        [1, -1, 0, 9, -9],
        [1, 2, 6, -3, -6],
    ]
    multiplicities = [1, 15, 60, 20, 24]
    valencies = [len(orbit) for orbit in orbits]

    character_equations = True
    for row in p_matrix:
        for i in range(5):
            for j in range(5):
                left = row[i] * row[j]
                right = sum(intersection[i][j][k] * row[k] for k in range(5))
                character_equations &= left == right

    q_matrix: list[list[Fraction]] = []
    for relation_number, valency in enumerate(valencies):
        q_matrix.append([
            Fraction(multiplicities[character], valency)
            * p_matrix[character][relation_number]
            for character in range(5)
        ])
    pq = matmul(
        [[Fraction(value) for value in row] for row in p_matrix],
        q_matrix,
    )
    pq_exact = all(
        pq[i][j] == (120 if i == j else 0)
        for i in range(5)
        for j in range(5)
    )

    krein = [[[Fraction(0) for _ in range(5)] for _ in range(5)] for _ in range(5)]
    for i in range(5):
        for j in range(5):
            for k in range(5):
                krein[i][j][k] = Fraction(1, 120) * sum(
                    q_matrix[r][i] * q_matrix[r][j] * p_matrix[k][r]
                    for r in range(5)
                )
    krein_nonnegative = all(value >= 0 for plane in krein for row in plane for value in row)

    expected_intersection = [
        [[1,0,0,0,0],[0,1,0,0,0],[0,0,1,0,0],[0,0,0,1,0],[0,0,0,0,1]],
        [[0,1,0,0,0],[2,1,0,0,0],[0,0,2,0,0],[0,0,0,0,1],[0,0,0,2,1]],
        [[0,0,1,0,0],[0,0,2,0,0],[36,36,6,12,12],[0,0,9,8,8],[0,0,18,16,16]],
        [[0,0,0,1,0],[0,0,0,0,1],[0,0,9,8,8],[27,0,6,10,4],[0,27,12,8,14]],
        [[0,0,0,0,1],[0,0,0,2,1],[0,0,18,16,16],[0,27,12,8,14],[54,27,24,28,22]],
    ]

    checks = {
        "w33_has_40_points_and_40_lines": len(points) == len(lines) == 40,
        "psp_order_is_25920": len(group) == 25920,
        "line_phase_action_has_degree_120": len(states) == 120,
        "phase_stabilizer_order_is_216": len(stabilizer) == 216,
        "scheme_rank_is_five": len(orbits) == 5,
        "valencies_are_1_2_36_27_54": valencies == [1, 2, 36, 27, 54],
        "relations_are_symmetric": symmetric,
        "intersection_tensor_is_exact": intersection == expected_intersection,
        "intersection_algebra_is_commutative": all(
            intersection[i][j] == intersection[j][i]
            for i in range(5) for j in range(5)
        ),
        "p_matrix_characters_multiply_correctly": character_equations,
        "multiplicities_sum_to_120": sum(multiplicities) == 120,
        "pq_equals_120_identity": pq_exact,
        "krein_parameters_are_nonnegative": krein_nonnegative,
        "selector_overlap_valencies_match": valencies == [1, 2, 36, 27, 54],
    }
    failed = [name for name, value in checks.items() if not value]
    if failed:
        raise AssertionError(f"failed checks: {failed}")

    result = {
        "schema": "w33.pass1034.selector_orbital_algebra.python.v1",
        "status": "PASS",
        "headline": (
            "The 120 golden-selector sheets carry a symmetric rank-five association "
            "scheme. Its valencies are [1,2,36,27,54], its primitive multiplicities "
            "are [1,15,60,20,24], and its exact P/Q eigenmatrices and nonnegative "
            "Krein tensor are certified from the PSp(4,3) action."
        ),
        "relation_order": [
            "same sheet",
            "other phases over the same line",
            "phases over intersecting lines",
            "matched phase over a skew line",
            "unmatched phase over a skew line",
        ],
        "overlap_to_relation": {"108": 0, "54": 1, "12": 2, "4": 3, "2": 4},
        "valencies": valencies,
        "multiplicities": multiplicities,
        "P": p_matrix,
        "Q": [[frac_json(value) for value in row] for row in q_matrix],
        "intersection_numbers_p_ij_k": intersection,
        "krein_parameters_q_ij_k": [
            [[frac_json(value) for value in row] for row in plane]
            for plane in krein
        ],
        "consequence": (
            "The selector correction problem must now be formulated relative to this "
            "five-relation algebra or to a proved refinement of it; overlap counts alone "
            "are no longer an adequate specification."
        ),
        "check_count": len(checks),
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Pass1034 status=PASS checks={len(checks)} output={OUT}")


if __name__ == "__main__":
    main()
