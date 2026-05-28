"""Part MDCLXXXIV: W33 spread negative-polar selector signature.

MDCLXXXIII identifies the raw Clifford antipodal selector as the degree-six
action of A5.  That makes the 36 raw L/R cells a 6 x 6 rook grid.  The next
tempting hypothesis is that the missing W33 spread selector is just a third
Latin-square direction on that grid.

This verifier checks that hypothesis and rules it out.

The W33 spread overlap-4 graph has parameters srg(36,15,6,6), but it has
clique number 4.  A 6 x 6 Latin-square graph would contain K6 row, column, and
symbol cliques.  Therefore the W33 spread selector is not a Latin/Euler third
direction on the raw Clifford grid.

The correct replacement is the negative orthogonal polar graph NO^-(6,2).
The verifier constructs that graph directly from a minus-type quadratic form
over F2 and finds an explicit isomorphism from the W33 spread graph to it.
The associated orthogonal-group order is 51840 = |W(E6)|.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_spread_double_six_association_scheme import w33_spreads  # noqa: E402


OUTPUT_PATH = ROOT / "PART_MDCLXXXIV_W33_SPREAD_NEGATIVE_POLAR_SELECTOR_SIGNATURE_results.json"


def counter_to_json(counter: Counter[Any]) -> dict[str, int]:
    return {str(key): int(value) for key, value in sorted(counter.items(), key=lambda item: str(item[0]))}


def adjacency_from_edges(vertex_count: int, edges: list[tuple[int, int]]) -> list[int]:
    adjacency = [0] * vertex_count
    for left, right in edges:
        adjacency[left] |= 1 << right
        adjacency[right] |= 1 << left
    return adjacency


def graph_parameters(adjacency: list[int]) -> dict[str, Any]:
    vertex_count = len(adjacency)
    degrees = Counter(mask.bit_count() for mask in adjacency)
    adjacent_common = Counter()
    nonadjacent_common = Counter()
    for left, right in combinations(range(vertex_count), 2):
        common = (adjacency[left] & adjacency[right]).bit_count()
        if (adjacency[left] >> right) & 1:
            adjacent_common[common] += 1
        else:
            nonadjacent_common[common] += 1

    return {
        "vertices": vertex_count,
        "degree_profile": counter_to_json(degrees),
        "edge_count": sum(mask.bit_count() for mask in adjacency) // 2,
        "adjacent_common_neighbor_profile": counter_to_json(adjacent_common),
        "nonadjacent_common_neighbor_profile": counter_to_json(nonadjacent_common),
    }


def clique_number(adjacency: list[int]) -> int:
    vertex_count = len(adjacency)
    best = 0

    def expand(size: int, candidates: int) -> None:
        nonlocal best
        if size + candidates.bit_count() <= best:
            return
        if not candidates:
            best = max(best, size)
            return

        while candidates:
            if size + candidates.bit_count() <= best:
                return
            bit = candidates & -candidates
            vertex = bit.bit_length() - 1
            candidates ^= bit
            expand(size + 1, candidates & adjacency[vertex])
        best = max(best, size)

    expand(0, (1 << vertex_count) - 1)
    return best


def complement_adjacency(adjacency: list[int]) -> list[int]:
    vertex_count = len(adjacency)
    all_vertices = (1 << vertex_count) - 1
    return [all_vertices ^ (1 << index) ^ mask for index, mask in enumerate(adjacency)]


def w33_spread_graph() -> tuple[list[int], list[frozenset[int]]]:
    spreads = w33_spreads()
    edges = [
        (left, right)
        for left, right in combinations(range(len(spreads)), 2)
        if len(spreads[left] & spreads[right]) == 4
    ]
    return adjacency_from_edges(len(spreads), edges), spreads


def rook_6_by_6_graph() -> list[int]:
    edges = []
    for left, right in combinations(range(36), 2):
        left_row, left_column = divmod(left, 6)
        right_row, right_column = divmod(right, 6)
        if left_row == right_row or left_column == right_column:
            edges.append((left, right))
    return adjacency_from_edges(36, edges)


Vector = tuple[int, int, int, int, int, int]


def q_minus(vector: Vector) -> int:
    x0, x1, x2, x3, x4, x5 = vector
    return (x0 * x1 + x2 * x3 + x4 + x4 * x5 + x5) % 2


def polar_bilinear(left: Vector, right: Vector) -> int:
    added = tuple((lhs ^ rhs) for lhs, rhs in zip(left, right))
    return q_minus(added) ^ q_minus(left) ^ q_minus(right)


def no_minus_6_2_graph() -> tuple[list[int], list[Vector]]:
    vectors = [
        vector
        for vector in product((0, 1), repeat=6)
        if any(vector) and q_minus(vector) == 1
    ]
    edges = [
        (left, right)
        for left, right in combinations(range(len(vectors)), 2)
        if polar_bilinear(vectors[left], vectors[right]) == 0
    ]
    return adjacency_from_edges(len(vectors), edges), vectors


def find_graph_isomorphism(source: list[int], target: list[int]) -> list[int]:
    if len(source) != len(target):
        raise ValueError("graph orders differ")

    vertex_count = len(source)
    all_targets = (1 << vertex_count) - 1
    source_to_target = [-1] * vertex_count
    target_to_source = [-1] * vertex_count

    def unmapped_targets() -> int:
        mask = all_targets
        for target_index, source_index in enumerate(target_to_source):
            if source_index != -1:
                mask &= ~(1 << target_index)
        return mask

    def candidates(source_vertex: int) -> int:
        mask = unmapped_targets()
        for mapped_source, mapped_target in enumerate(source_to_target):
            if mapped_target == -1:
                continue
            if (source[source_vertex] >> mapped_source) & 1:
                mask &= target[mapped_target]
            else:
                mask &= ~target[mapped_target]
        return mask

    def search(depth: int) -> bool:
        if depth == vertex_count:
            return True

        best_source = -1
        best_candidates = 0
        best_count = vertex_count + 1
        for source_vertex in range(vertex_count):
            if source_to_target[source_vertex] != -1:
                continue
            source_candidates = candidates(source_vertex)
            count = source_candidates.bit_count()
            if count == 0:
                return False
            if count < best_count:
                best_source = source_vertex
                best_candidates = source_candidates
                best_count = count
                if count == 1:
                    break

        remaining = best_candidates
        while remaining:
            bit = remaining & -remaining
            target_vertex = bit.bit_length() - 1
            remaining ^= bit

            source_to_target[best_source] = target_vertex
            target_to_source[target_vertex] = best_source

            if all(
                source_to_target[source_vertex] != -1 or candidates(source_vertex)
                for source_vertex in range(vertex_count)
            ) and search(depth + 1):
                return True

            source_to_target[best_source] = -1
            target_to_source[target_vertex] = -1

        return False

    # The constructed graphs are vertex-transitive, and this deterministic seed
    # makes the certificate stable.  If the seed ever fails, try all targets.
    for target_seed in range(vertex_count):
        source_to_target[0] = target_seed
        target_to_source[target_seed] = 0
        if search(1):
            break
        source_to_target[0] = -1
        target_to_source[target_seed] = -1

    if any(target == -1 for target in source_to_target):
        raise AssertionError("no isomorphism found")

    return source_to_target


def verify_isomorphism(source: list[int], target: list[int], mapping: list[int]) -> bool:
    return all(
        ((source[left] >> right) & 1) == ((target[mapping[left]] >> mapping[right]) & 1)
        for left, right in combinations(range(len(source)), 2)
    )


def o_minus_6_2_order() -> int:
    # |O^-(2m,2)| = 2 * 2^(m(m-1)) * (2^m + 1) * product_{i=1}^{m-1}(2^(2i)-1), m=3.
    m = 3
    product_term = 1
    for index in range(1, m):
        product_term *= 2 ** (2 * index) - 1
    return 2 * 2 ** (m * (m - 1)) * (2**m + 1) * product_term


def spread_negative_polar_selector_signature_packet() -> dict[str, Any]:
    spread_graph, spreads = w33_spread_graph()
    polar_graph, polar_vectors = no_minus_6_2_graph()
    rook_graph = rook_6_by_6_graph()
    mapping = find_graph_isomorphism(spread_graph, polar_graph)

    spread_parameters = graph_parameters(spread_graph)
    polar_parameters = graph_parameters(polar_graph)
    rook_parameters = graph_parameters(rook_graph)
    spread_clique_number = clique_number(spread_graph)
    spread_independence_number = clique_number(complement_adjacency(spread_graph))
    rook_clique_number = clique_number(rook_graph)

    checks = {
        "w33_spread_graph_is_srg_36_15_6_6": spread_parameters
        == {
            "vertices": 36,
            "degree_profile": {"15": 36},
            "edge_count": 270,
            "adjacent_common_neighbor_profile": {"6": 270},
            "nonadjacent_common_neighbor_profile": {"6": 360},
        },
        "no_minus_graph_has_36_nonsingular_vectors": len(polar_vectors) == 36,
        "no_minus_graph_is_srg_36_15_6_6": polar_parameters == spread_parameters,
        "explicit_w33_to_no_minus_isomorphism_verifies": verify_isomorphism(spread_graph, polar_graph, mapping),
        "w33_spread_clique_number_is_4": spread_clique_number == 4,
        "w33_spread_independence_number_is_5": spread_independence_number == 5,
        "raw_rook_graph_has_k6_rows_and_columns": rook_parameters["degree_profile"] == {"10": 36}
        and rook_clique_number == 6,
        "latin_square_third_direction_is_obstructed": spread_clique_number < 6 == rook_clique_number,
        "orthogonal_group_order_is_we6": o_minus_6_2_order() == 51840,
    }

    return {
        "part": "MDCLXXXIV",
        "theorem": "W33 spread negative-polar selector signature",
        "input_bridge": "MDCLXXXIII Clifford antipodal A5 selector group",
        "selector_signature": "W33 spreads form NO^-(6,2), not a Latin-square third direction on the 6x6 Clifford grid",
        "w33_spread_graph_parameters": spread_parameters,
        "negative_polar_graph_parameters": polar_parameters,
        "raw_rook_graph_parameters": rook_parameters,
        "w33_spread_clique_number": spread_clique_number,
        "w33_spread_independence_number": spread_independence_number,
        "raw_rook_clique_number": rook_clique_number,
        "negative_polar_quadratic_form": "Q=x0*x1+x2*x3+x4+x4*x5+x5 over F2",
        "negative_polar_vertex_count": len(polar_vectors),
        "w33_to_negative_polar_isomorphism": mapping,
        "sample_spread_to_vector_map": {
            str(index): list(polar_vectors[mapping[index]])
            for index in range(12)
        },
        "o_minus_6_2_order": o_minus_6_2_order(),
        "claim_boundary": (
            "constructs an explicit W33 spread graph isomorphism to NO^-(6,2) "
            "and rules out a Latin-square/K6 selector; it does not yet lift the "
            "A5 antipodal torsor to a canonical 60-to-40 incidence transport"
        ),
        "reading": (
            "The raw Clifford antipodal selector supplies a 6x6 rook grid. "
            "A first guess is that the W33 spread graph adds a third Latin "
            "direction, but that would force K6 row, column, and symbol cliques. "
            "The W33 spread overlap-4 graph has clique number 4 and independence "
            "number 5, so the Latin/Euler direction is impossible. The verifier "
            "constructs the minus-type quadratic form Q over F2, takes its 36 "
            "nonsingular vectors, joins orthogonal pairs under the polar form, "
            "and finds an explicit isomorphism from the W33 spread graph to this "
            "NO^-(6,2) graph. The selector twist is therefore negative-polar / "
            "W(E6), not Latin-square."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = spread_negative_polar_selector_signature_packet()
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MDCLXXXIV: W33 Spread Negative-Polar Selector Signature ===")
    print("signature:", packet["selector_signature"])
    print("W33 clique number:", packet["w33_spread_clique_number"])
    print("raw rook clique number:", packet["raw_rook_clique_number"])
    print("O^-(6,2) order:", packet["o_minus_6_2_order"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])} checks")


if __name__ == "__main__":
    main()
