"""Part MCCCLXXXVIII: exact E8 root system from the W33 tetracode.

MCCCLXXXVII showed that the 27 nonneighbors of a W33 point, read through the
four lines through that point, collapse to the ternary tetracode [4,2,3]_3.
This verifier takes that W33-derived code and performs the standard
Eisenstein/A2 lift:

    four A2 root planes + ternary tetracode glue -> 240 norm-2 roots.

All arithmetic is exact over Q in four A2 simple-root coordinate blocks.  The
checks verify not just the count, but the rank, inner-product profile, E8
simple-root determinant, Dynkin degree profile, and closure under root
reflections.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import sys
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_affine_tetracode_e8_glue_bridge import (  # noqa: E402
    affine_tetracode_e8_glue_packet,
    standard_tetracode,
)


OUTPUT_PATH = ROOT / "PART_MCCCLXXXVIII_TETRACODE_E8_ROOT_SYSTEM_BRIDGE_results.json"

A2_GRAM = ((Fraction(2), Fraction(-1)), (Fraction(-1), Fraction(2)))
A2_POSITIVE_ROOTS = (
    (Fraction(1), Fraction(0)),
    (Fraction(0), Fraction(1)),
    (Fraction(1), Fraction(1)),
)
A2_COSET_ONE_MINIMA = (
    (Fraction(2, 3), Fraction(1, 3)),
    (Fraction(-1, 3), Fraction(1, 3)),
    (Fraction(-1, 3), Fraction(-2, 3)),
)
CHAMBER_VECTOR = tuple(Fraction(value) for value in (1, 3, 9, 27, 2, 6, 18, 54))


Vector = tuple[Fraction, ...]


def frac_to_str(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def vector_to_str(vector: Vector) -> list[str]:
    return [frac_to_str(entry) for entry in vector]


def counter_to_json(counter: Counter[Any]) -> dict[str, int]:
    return {str(key): int(value) for key, value in sorted(counter.items(), key=lambda item: str(item[0]))}


def block_vector(block_index: int, pair: tuple[Fraction, Fraction]) -> Vector:
    vector = [Fraction(0)] * 8
    vector[2 * block_index] = pair[0]
    vector[2 * block_index + 1] = pair[1]
    return tuple(vector)


def inner(left: Vector, right: Vector) -> Fraction:
    total = Fraction(0)
    for block_index in range(4):
        left_0 = left[2 * block_index]
        left_1 = left[2 * block_index + 1]
        right_0 = right[2 * block_index]
        right_1 = right[2 * block_index + 1]
        total += left_0 * (2 * right_0 - right_1) + left_1 * (-right_0 + 2 * right_1)
    return total


def add(left: Vector, right: Vector) -> Vector:
    return tuple(a + b for a, b in zip(left, right))


def subtract(left: Vector, right: Vector) -> Vector:
    return tuple(a - b for a, b in zip(left, right))


def scale(coefficient: Fraction, vector: Vector) -> Vector:
    return tuple(coefficient * entry for entry in vector)


def rational_rank(rows: Iterable[Vector]) -> int:
    matrix = [list(row) for row in rows if any(row)]
    if not matrix:
        return 0

    row_count = len(matrix)
    col_count = len(matrix[0])
    rank = 0

    for col in range(col_count):
        pivot = None
        for row in range(rank, row_count):
            if matrix[row][col]:
                pivot = row
                break
        if pivot is None:
            continue

        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][col]
        matrix[rank] = [entry / pivot_value for entry in matrix[rank]]

        for row in range(row_count):
            if row == rank or not matrix[row][col]:
                continue
            factor = matrix[row][col]
            matrix[row] = [matrix[row][idx] - factor * matrix[rank][idx] for idx in range(col_count)]

        rank += 1
        if rank == col_count:
            break

    return rank


def determinant(matrix: list[list[Fraction]]) -> Fraction:
    work = [row[:] for row in matrix]
    n_rows = len(work)
    det = Fraction(1)

    for col in range(n_rows):
        pivot = None
        for row in range(col, n_rows):
            if work[row][col]:
                pivot = row
                break
        if pivot is None:
            return Fraction(0)
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]
            det = -det

        pivot_value = work[col][col]
        det *= pivot_value
        for row in range(col + 1, n_rows):
            if not work[row][col]:
                continue
            factor = work[row][col] / pivot_value
            for idx in range(col, n_rows):
                work[row][idx] -= factor * work[col][idx]

    return det


def w33_tetracode_words() -> set[tuple[int, int, int, int]]:
    packet = affine_tetracode_e8_glue_packet()
    return {tuple(int(entry) for entry in word) for word in packet["representative_point"]["unique_words"]}


def e8_roots_from_w33_tetracode() -> dict[Vector, str]:
    code = w33_tetracode_words()
    roots: dict[Vector, str] = {}

    for block_index in range(4):
        for root in A2_POSITIVE_ROOTS:
            positive = block_vector(block_index, root)
            negative = scale(Fraction(-1), positive)
            roots[positive] = f"A2_block_{block_index}"
            roots[negative] = f"A2_block_{block_index}"

    for codeword in sorted(code):
        if not any(codeword):
            continue

        block_choices: list[list[tuple[Fraction, Fraction]]] = []
        for entry in codeword:
            if entry == 0:
                block_choices.append([(Fraction(0), Fraction(0))])
            elif entry == 1:
                block_choices.append(list(A2_COSET_ONE_MINIMA))
            elif entry == 2:
                block_choices.append([(-left, -right) for left, right in A2_COSET_ONE_MINIMA])
            else:
                raise ValueError(codeword)

        for choices in product(*block_choices):
            vector = [Fraction(0)] * 8
            for block_index, pair in enumerate(choices):
                vector[2 * block_index] = pair[0]
                vector[2 * block_index + 1] = pair[1]
            roots[tuple(vector)] = f"tetracode_{codeword}"

    return roots


def simple_roots_from_chamber(roots: Iterable[Vector]) -> list[Vector]:
    root_list = list(roots)
    positive = {root for root in root_list if inner(CHAMBER_VECTOR, root) > 0}
    if len(positive) != len(root_list) // 2:
        raise AssertionError("chamber vector is not regular")

    simple_roots: list[Vector] = []
    for root in sorted(positive):
        decomposable = False
        for first in positive:
            second = subtract(root, first)
            if second in positive:
                decomposable = True
                break
        if not decomposable:
            simple_roots.append(root)

    return simple_roots


def graph_connected(edge_pairs: list[tuple[int, int]], vertex_count: int) -> bool:
    if vertex_count == 0:
        return False
    neighbors = {idx: set() for idx in range(vertex_count)}
    for left, right in edge_pairs:
        neighbors[left].add(right)
        neighbors[right].add(left)

    seen = {0}
    frontier = [0]
    while frontier:
        current = frontier.pop()
        for neighbor in neighbors[current]:
            if neighbor not in seen:
                seen.add(neighbor)
                frontier.append(neighbor)
    return len(seen) == vertex_count


def reflection_closure_failure_count(root_list: list[Vector], root_set: set[Vector]) -> int:
    failures = 0
    for alpha in root_list:
        for beta in root_list:
            reflected = subtract(beta, scale(inner(beta, alpha), alpha))
            if reflected not in root_set:
                failures += 1
    return failures


def tetracode_e8_root_system_packet() -> dict[str, Any]:
    code = w33_tetracode_words()
    root_sources = e8_roots_from_w33_tetracode()
    roots = sorted(root_sources)
    root_set = set(roots)

    norm_profile = Counter(inner(root, root) for root in roots)
    ordered_pair_profile = Counter(inner(left, right) for left in roots for right in roots)
    per_root_profiles = Counter(tuple(sorted(Counter(inner(root, other) for other in roots).items())) for root in roots)
    source_profile = Counter("A2" if source.startswith("A2") else "tetracode_glue" for source in root_sources.values())

    simple_roots = simple_roots_from_chamber(roots)
    simple_gram = [[inner(left, right) for right in simple_roots] for left in simple_roots]
    dynkin_edges = [
        (idx, jdx)
        for idx in range(len(simple_roots))
        for jdx in range(idx + 1, len(simple_roots))
        if simple_gram[idx][jdx] == -1
    ]
    dynkin_degrees = Counter(
        sum(1 for edge in dynkin_edges if idx in edge)
        for idx in range(len(simple_roots))
    )
    simple_off_diagonal_values = {
        simple_gram[idx][jdx]
        for idx in range(len(simple_roots))
        for jdx in range(len(simple_roots))
        if idx != jdx
    }

    reflection_failures = reflection_closure_failure_count(roots, root_set)
    representative_inner_profile = Counter(inner(roots[0], other) for other in roots)

    checks = {
        "w33_code_equals_standard_tetracode": code == standard_tetracode(),
        "root_count_is_240": len(roots) == 240,
        "roots_are_unique": len(root_set) == 240,
        "source_decomposition_is_24_plus_216": source_profile == {"A2": 24, "tetracode_glue": 216},
        "rank_is_8": rational_rank(roots) == 8,
        "all_roots_have_norm_2": norm_profile == {Fraction(2): 240},
        "ordered_inner_products_are_e8_values": ordered_pair_profile
        == {Fraction(-2): 240, Fraction(-1): 13440, Fraction(0): 30240, Fraction(1): 13440, Fraction(2): 240},
        "all_roots_have_e8_local_profile": representative_inner_profile
        == {Fraction(-2): 1, Fraction(-1): 56, Fraction(0): 126, Fraction(1): 56, Fraction(2): 1}
        and len(per_root_profiles) == 1,
        "reflection_closure_holds": reflection_failures == 0,
        "simple_root_count_is_8": len(simple_roots) == 8,
        "simple_gram_determinant_is_1": determinant(simple_gram) == 1,
        "simple_off_diagonal_values_are_0_or_minus_1": simple_off_diagonal_values <= {Fraction(0), Fraction(-1)},
        "dynkin_graph_is_connected_tree": len(dynkin_edges) == 7 and graph_connected(dynkin_edges, 8),
        "dynkin_degree_profile_is_e8": dynkin_degrees == {1: 3, 2: 4, 3: 1},
    }

    return {
        "part": "MCCCLXXXVIII",
        "theorem": "Exact E8 root system from the W33 tetracode",
        "input_bridge": "MCCCLXXXVII affine tetracode E8 glue bridge",
        "w33_tetracode": {
            "words": [list(word) for word in sorted(code)],
            "standard_generators": [[0, 1, 1, 1], [1, 0, 1, 2]],
            "equals_standard_tetracode": code == standard_tetracode(),
        },
        "root_system": {
            "count": len(roots),
            "rank": rational_rank(roots),
            "source_profile": dict(source_profile),
            "norm_profile": counter_to_json(norm_profile),
            "ordered_pair_inner_product_profile": counter_to_json(ordered_pair_profile),
            "representative_local_inner_product_profile": counter_to_json(representative_inner_profile),
            "unique_local_profile_count": len(per_root_profiles),
            "reflection_closure_failures": reflection_failures,
            "sample_a2_roots": [vector_to_str(root) for root, source in root_sources.items() if source.startswith("A2")][:6],
            "sample_glue_roots": [vector_to_str(root) for root, source in root_sources.items() if source.startswith("tetracode")][:6],
        },
        "simple_root_system": {
            "chamber_vector": vector_to_str(CHAMBER_VECTOR),
            "simple_root_count": len(simple_roots),
            "simple_roots": [vector_to_str(root) for root in simple_roots],
            "gram_matrix": [[frac_to_str(entry) for entry in row] for row in simple_gram],
            "gram_determinant": frac_to_str(determinant(simple_gram)),
            "dynkin_edges": [list(edge) for edge in dynkin_edges],
            "dynkin_edge_count": len(dynkin_edges),
            "dynkin_degree_profile": counter_to_json(dynkin_degrees),
            "dynkin_connected": graph_connected(dynkin_edges, 8),
        },
        "claim_boundary": (
            "exact finite root-system theorem: W33 supplies the tetracode, and the "
            "standard A2/Eisenstein lift supplies the metric root coordinates; this "
            "does not assert a continuum physical gauge group without the separate "
            "identification bridge"
        ),
        "reading": (
            "MCCCLXXXVII gave the W33-native tetracode glue code. Lifting that code "
            "over four A2 coordinate planes produces an exact rank-8, 240-root, "
            "reflection-closed simply-laced root system with determinant-1 simple "
            "root Gram matrix and E8 Dynkin degree profile. This upgrades the prior "
            "count identity to an exact finite E8 root-system witness."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = tetracode_e8_root_system_packet()
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCCCLXXXVIII: Tetracode E8 Root System Bridge ===")
    print("root count:", packet["root_system"]["count"])
    print("rank:", packet["root_system"]["rank"])
    print("source profile:", packet["root_system"]["source_profile"])
    print("local profile:", packet["root_system"]["representative_local_inner_product_profile"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
