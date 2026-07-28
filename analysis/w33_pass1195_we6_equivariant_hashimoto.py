#!/usr/bin/env python3
"""Pass 1195: exact W(E6)-equivariant Hashimoto spectral decomposition."""
from __future__ import annotations

from collections import Counter, deque
from itertools import product
import json
import math
from pathlib import Path

import numpy as np

from w33_pass1135_cubic_kernel_decomposition import ATLAS, CLASS_SIZES, IRR

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass1195_we6_equivariant_hashimoto.json"
Q = 3
GROUP_ORDER = 51840


def canon(vector: tuple[int, ...]) -> tuple[int, ...]:
    vector = tuple(x % Q for x in vector)
    for x in vector:
        if x:
            inverse = 1 if x == 1 else 2
            return tuple(inverse * y % Q for y in vector)
    raise ValueError("zero vector")


def symp(x: tuple[int, ...], y: tuple[int, ...]) -> int:
    return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % Q


def compose(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a[b[i]] for i in range(len(a)))


def inverse(permutation: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * len(permutation)
    for i, value in enumerate(permutation):
        out[value] = i
    return tuple(out)


def permutation_order(permutation: tuple[int, ...]) -> int:
    seen = [False] * len(permutation)
    result = 1
    for i in range(len(permutation)):
        if seen[i]:
            continue
        j, length = i, 0
        while not seen[j]:
            seen[j] = True
            j = permutation[j]
            length += 1
        result = math.lcm(result, length)
    return result


def enumerate_group(generators: tuple[tuple[int, ...], ...], outer_index: int | None = None):
    identity = tuple(range(len(generators[0])))
    elements = [identity]
    index = {identity: 0}
    parity = [0]
    queue = deque([0])
    while queue:
        i = queue.popleft()
        x = elements[i]
        for generator_index, generator in enumerate(generators):
            y = compose(generator, x)
            py = parity[i] ^ int(outer_index is not None and generator_index == outer_index)
            if y not in index:
                index[y] = len(elements)
                elements.append(y)
                parity.append(py)
                queue.append(len(elements) - 1)
            elif outer_index is not None:
                assert parity[index[y]] == py
    return tuple(elements), index, tuple(parity)


def generated_order(generators: tuple[tuple[int, ...], ...]) -> int:
    return len(enumerate_group(generators)[0])


def conjugacy_classes(group, index, generators):
    conjugation_maps = []
    for generator in generators:
        gi = inverse(generator)
        conjugation_maps.append([
            index[compose(gi, compose(element, generator))]
            for element in group
        ])
    unseen = set(range(len(group)))
    classes = []
    class_of = [0] * len(group)
    while unseen:
        seed = min(unseen)
        orbit = {seed}
        queue = deque([seed])
        while queue:
            x = queue.popleft()
            for mapping in conjugation_maps:
                y = mapping[x]
                if y not in orbit:
                    orbit.add(y)
                    queue.append(y)
        unseen -= orbit
        class_index = len(classes)
        for x in orbit:
            class_of[x] = class_index
        classes.append(tuple(sorted(orbit)))
    return tuple(classes), tuple(class_of)


def permutation_power(permutation: tuple[int, ...], exponent: int) -> tuple[int, ...]:
    result = tuple(range(len(permutation)))
    base = permutation
    while exponent:
        if exponent & 1:
            result = compose(result, base)
        base = compose(base, base)
        exponent //= 2
    return result


def evaluate_word(expression: str, c: tuple[int, ...], d: tuple[int, ...]) -> tuple[int, ...]:
    if expression.startswith("("):
        word, exponent = expression[1:].split(")^")
        exponent = int(exponent)
    else:
        word, exponent = expression, 1
    result = tuple(range(len(c)))
    for letter in word:
        result = compose(result, c if letter == "c" else d)
    return permutation_power(result, exponent)


def point_model():
    points = sorted({canon(tuple(x)) for x in product(range(Q), repeat=4) if any(x)})
    point_index = {point: i for i, point in enumerate(points)}
    vectors = [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1), (1, 1, 0, 0)]
    psp_generators = []
    for vector in vectors:
        permutation = []
        for point in points:
            scalar = symp(point, vector)
            image = tuple((point[i] + scalar * vector[i]) % Q for i in range(4))
            permutation.append(point_index[canon(image)])
        psp_generators.append(tuple(permutation))
    outer = tuple(point_index[canon((p[0], p[1], 2 * p[2], 2 * p[3]))] for p in points)
    return points, tuple(psp_generators), outer


def atlas_representatives(group, group_index, parity, classes, class_of):
    c_class = next(
        i for i, cls in enumerate(classes)
        if permutation_order(group[cls[0]]) == 2
        and GROUP_ORDER // len(cls) == 1440
        and parity[cls[0]] == 1
    )
    d_class = next(
        i for i, cls in enumerate(classes)
        if permutation_order(group[cls[0]]) == 9
        and GROUP_ORDER // len(cls) == 9
        and parity[cls[0]] == 0
    )
    c = group[classes[c_class][0]]
    d = None
    for candidate_index in classes[d_class]:
        candidate = group[candidate_index]
        if permutation_order(compose(c, candidate)) == 10 and generated_order((c, candidate)) == GROUP_ORDER:
            d = candidate
            break
    assert d is not None

    representatives = []
    for name, word, expected_order, expected_centralizer in ATLAS:
        element = evaluate_word(word, c, d)
        cls = classes[class_of[group_index[element]]]
        assert permutation_order(element) == expected_order
        assert GROUP_ORDER // len(cls) == expected_centralizer
        representatives.append(element)
    return tuple(representatives)


def character_decomposition(character: list[int]) -> list[dict[str, int | str]]:
    answer = []
    for degree, irreducible, _, name in IRR:
        multiplicity = sum(
            int(size) * int(value) * int(chi)
            for size, value, chi in zip(CLASS_SIZES, character, irreducible)
        ) // GROUP_ORDER
        if multiplicity:
            answer.append({"irrep": name, "degree": degree, "multiplicity": multiplicity})
    assert sum(item["degree"] * item["multiplicity"] for item in answer) == character[0]
    return answer


def poly_multiply(left: list[int], right: list[int]) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] += a * b
    return out


def polynomial_value(coefficients: list[int], x: int) -> int:
    return sum(value * x**i for i, value in enumerate(coefficients))


def main() -> dict:
    points, psp_generators, outer = point_model()
    generators = psp_generators + (outer,)
    group, group_index, parity = enumerate_group(generators, outer_index=len(generators) - 1)
    assert len(group) == GROUP_ORDER
    assert Counter(parity) == Counter({0: 25920, 1: 25920})
    classes, class_of = conjugacy_classes(group, group_index, generators)
    assert len(classes) == 25
    representatives = atlas_representatives(group, group_index, parity, classes, class_of)

    adjacency = np.zeros((40, 40), dtype=np.int64)
    for i, x in enumerate(points):
        for j, y in enumerate(points):
            adjacency[i, j] = int(i != j and symp(x, y) == 0)
    assert np.all(adjacency.sum(axis=1) == 12)
    edges = [(i, j) for i in range(40) for j in range(i + 1, 40) if adjacency[i, j]]
    directed_edges = [(i, j) for i, j in edges for i, j in ((i, j), (j, i))]
    directed_index = {edge: i for i, edge in enumerate(directed_edges)}
    assert len(edges) == 240 and len(directed_edges) == 480

    vertex_character = []
    edge_character = []
    directed_character = []
    for representative in representatives:
        vertex_character.append(sum(representative[i] == i for i in range(40)))
        edge_character.append(sum(tuple(sorted((representative[i], representative[j]))) == (i, j) for i, j in edges))
        directed_character.append(sum(representative[i] == i and representative[j] == j for i, j in directed_edges))

    hashimoto = np.zeros((480, 480), dtype=np.int64)
    for row, (i, j) in enumerate(directed_edges):
        for k in range(40):
            if k != i and adjacency[j, k]:
                hashimoto[row, directed_index[(j, k)]] = 1
    assert np.all(hashimoto.sum(axis=1) == 11)

    plus_numerator = [1]
    for factor in ([1, 1], [-11, 1], [11, -2, 1], [11, 4, 1]):
        plus_numerator = poly_multiply(plus_numerator, list(factor))
    plus_denominator = polynomial_value(plus_numerator, 1)
    assert plus_numerator == [-1331, -1452, -253, -140, -17, -8, 1]
    assert plus_denominator == -3200

    minus_numerator = [1]
    for factor in ([-1, 1], [-11, 1], [11, -2, 1], [11, 4, 1]):
        minus_numerator = poly_multiply(minus_numerator, list(factor))
    minus_denominator = polynomial_value(minus_numerator, -1)
    assert minus_numerator == [1331, -1210, 11, -124, 1, -10, 1]
    assert minus_denominator == 2688

    powers = [np.eye(480, dtype=np.int64)]
    for _ in range(1, 7):
        powers.append(powers[-1] @ hashimoto)

    plus_character = []
    minus_character = []
    for representative in representatives:
        directed_action = tuple(directed_index[(representative[i], representative[j])] for i, j in directed_edges)
        twisted_traces = [
            sum(int(matrix[directed_action[i], i]) for i in range(480))
            for matrix in powers
        ]
        plus_n = sum(a * b for a, b in zip(plus_numerator, twisted_traces))
        minus_n = sum(a * b for a, b in zip(minus_numerator, twisted_traces))
        assert plus_n % plus_denominator == 0
        assert minus_n % minus_denominator == 0
        plus_character.append(plus_n // plus_denominator)
        minus_character.append(minus_n // minus_denominator)

    vertex_decomposition = character_decomposition(vertex_character)
    edge_decomposition = character_decomposition(edge_character)
    directed_decomposition = character_decomposition(directed_character)
    plus_decomposition = character_decomposition(plus_character)
    minus_decomposition = character_decomposition(minus_character)

    assert vertex_decomposition == [
        {"irrep": "1", "degree": 1, "multiplicity": 1},
        {"irrep": "15_outer_negative", "degree": 15, "multiplicity": 1},
        {"irrep": "24", "degree": 24, "multiplicity": 1},
    ]
    assert plus_decomposition == [
        {"irrep": "30_outer_negative", "degree": 30, "multiplicity": 1},
        {"irrep": "81_plus", "degree": 81, "multiplicity": 1},
        {"irrep": "90", "degree": 90, "multiplicity": 1},
    ]
    assert minus_decomposition == [
        {"irrep": "15a", "degree": 15, "multiplicity": 1},
        {"irrep": "20", "degree": 20, "multiplicity": 1},
        {"irrep": "24", "degree": 24, "multiplicity": 1},
        {"irrep": "60a", "degree": 60, "multiplicity": 1},
        {"irrep": "81_plus", "degree": 81, "multiplicity": 1},
    ]

    spectral_packets = {
        "x_minus_11": {"dimension": 1, "module": "1", "eigenvalue": 11},
        "x_minus_1": {"dimension": 201, "module": "30_outer_negative + 81_plus + 90", "decomposition": plus_decomposition},
        "x_plus_1": {"dimension": 200, "module": "15a + 20 + 24 + 60a + 81_plus", "decomposition": minus_decomposition},
        "x2_minus_2x_plus_11": {"dimension": 48, "module": "2*24", "reason": "two Hashimoto lifts of the adjacency lambda=2 constituent"},
        "x2_plus_4x_plus_11": {"dimension": 30, "module": "2*15_outer_negative", "reason": "two Hashimoto lifts of the adjacency lambda=-4 constituent"},
    }
    assert sum(packet["dimension"] for packet in spectral_packets.values()) == 480

    result = {
        "schema": "w33.pass1195.we6_equivariant_hashimoto.v1",
        "status": "PASS",
        "headline": "The 480-dimensional directed-edge Hashimoto module splits exactly into five W(E6)-equivariant spectral packets.",
        "group": {"name": "W(E6)=PSp(4,3):2", "order": GROUP_ORDER, "classes": len(classes)},
        "atlas_class_order": [row[0] for row in ATLAS],
        "characters": {
            "vertices40": vertex_character,
            "edges240": edge_character,
            "directed_edges480": directed_character,
            "hashimoto_plus1": plus_character,
            "hashimoto_minus1": minus_character,
        },
        "module_decompositions": {
            "vertices40": vertex_decomposition,
            "edges240": edge_decomposition,
            "directed_edges480": directed_decomposition,
        },
        "projector_polynomials": {
            "plus1": {"numerator_coefficients_ascending": plus_numerator, "denominator": plus_denominator},
            "minus1": {"numerator_coefficients_ascending": minus_numerator, "denominator": minus_denominator},
        },
        "spectral_packets": spectral_packets,
        "factorization": "(x-11)(x-1)^201(x+1)^200(x^2-2x+11)^24(x^2+4x+11)^15",
        "checks": {
            "we6_order_51840": len(group) == GROUP_ORDER,
            "directed_edge_dimension_480": directed_character[0] == 480,
            "plus_rank_201": plus_character[0] == 201,
            "minus_rank_200": minus_character[0] == 200,
            "packet_dimensions_sum_480": sum(packet["dimension"] for packet in spectral_packets.values()) == 480,
            "nonbacktracking_outdegree_11": int(hashimoto[0].sum()) == 11,
        },
        "scope": "Exact finite permutation characters and exact polynomial spectral projectors. This is an equivariant spectral classification; literal primitive-cycle orbit enumeration is handled separately in Pass 1196.",
    }
    assert all(result["checks"].values())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("PASS 1195 W(E6)-equivariant Hashimoto packets: 1|201|200|48|30")
    return result


if __name__ == "__main__":
    main()
