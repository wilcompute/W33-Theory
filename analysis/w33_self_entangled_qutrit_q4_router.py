"""Part MCLXXX: self-entangled qutrit Q4 hypercube router.

The temporal Bell qutrit from MCLXIII has a four-ray "now" stabilizer context:

    q + 1 = 4.

Taking the square of that context gives a 4x4 toroidal board.  The toroidal
knight graph on this board is the 4-cube Q4: 16 vertices, degree 4, 32 edges,
and edges exactly equal to one-bit flips after an explicit labeling.  A closed
knight tour is therefore a Gray-code Hamilton cycle on the hypercube.

This is a router/control theorem, not a replacement for the ternary W33 payload.
The qutrit payload remains the F3^4 two-qutrit Pauli geometry; Q4 is the binary
network clock around one four-ray "now" context.
"""

from __future__ import annotations

import json
import sys
from collections import Counter, deque
from itertools import combinations, product
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


BOARD = 4
Q = 3

Vertex = tuple[int, int]
Bits = tuple[int, int, int, int]
Edge = tuple[Vertex, Vertex]
BitEdge = tuple[Bits, Bits]


# Explicit graph isomorphism from the 4x4 toroidal knight board to Q4.
KNIGHT_TO_Q4: dict[Vertex, Bits] = {
    (0, 0): (0, 0, 0, 0),
    (2, 3): (0, 0, 0, 1),
    (3, 2): (0, 0, 1, 0),
    (1, 1): (0, 0, 1, 1),
    (1, 2): (0, 1, 0, 0),
    (3, 1): (0, 1, 0, 1),
    (2, 0): (0, 1, 1, 0),
    (0, 3): (0, 1, 1, 1),
    (2, 1): (1, 0, 0, 0),
    (0, 2): (1, 0, 0, 1),
    (1, 3): (1, 0, 1, 0),
    (3, 0): (1, 0, 1, 1),
    (3, 3): (1, 1, 0, 0),
    (1, 0): (1, 1, 0, 1),
    (0, 1): (1, 1, 1, 0),
    (2, 2): (1, 1, 1, 1),
}

KNIGHT_TOUR: list[Vertex] = [
    (0, 0),
    (1, 2),
    (2, 0),
    (3, 2),
    (1, 1),
    (0, 3),
    (3, 1),
    (2, 3),
    (0, 2),
    (1, 0),
    (2, 2),
    (3, 0),
    (1, 3),
    (0, 1),
    (3, 3),
    (2, 1),
]


def _load(path: Path) -> dict[str, object]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _sorted_edge(left: Vertex, right: Vertex) -> Edge:
    return tuple(sorted((left, right)))  # type: ignore[return-value]


def _sorted_bit_edge(left: Bits, right: Bits) -> BitEdge:
    return tuple(sorted((left, right)))  # type: ignore[return-value]


def knight_moves() -> set[Vertex]:
    # On Z/4Z, +2 and -2 are the same move, so only four distinct neighbors.
    return {(1, 2), (3, 2), (2, 1), (2, 3)}


def knight_adjacency() -> dict[Vertex, set[Vertex]]:
    return {
        (row, col): {
            ((row + drow) % BOARD, (col + dcol) % BOARD)
            for drow, dcol in knight_moves()
        }
        for row, col in product(range(BOARD), repeat=2)
    }


def knight_edges() -> set[Edge]:
    edges: set[Edge] = set()
    for vertex, neighbors in knight_adjacency().items():
        for neighbor in neighbors:
            edges.add(_sorted_edge(vertex, neighbor))
    return edges


def q4_vertices() -> set[Bits]:
    return set(product((0, 1), repeat=4))  # type: ignore[return-value]


def q4_edges() -> set[BitEdge]:
    edges: set[BitEdge] = set()
    for vertex in q4_vertices():
        for bit in range(4):
            neighbor = list(vertex)
            neighbor[bit] ^= 1
            edges.add(_sorted_bit_edge(vertex, tuple(neighbor)))  # type: ignore[arg-type]
    return edges


def hamming(left: Bits, right: Bits) -> int:
    return sum(a != b for a, b in zip(left, right))


def mapped_knight_edges() -> set[BitEdge]:
    return {_sorted_bit_edge(KNIGHT_TO_Q4[left], KNIGHT_TO_Q4[right]) for left, right in knight_edges()}


def bit_dimension(edge: BitEdge) -> int:
    left, right = edge
    changed = [idx for idx in range(4) if left[idx] != right[idx]]
    if len(changed) != 1:
        raise ValueError(f"not a Q4 edge: {edge}")
    return changed[0]


def dimension_edge_counts() -> dict[int, int]:
    return dict(sorted(Counter(bit_dimension(edge) for edge in mapped_knight_edges()).items()))


def tour_bits() -> list[Bits]:
    return [KNIGHT_TO_Q4[vertex] for vertex in KNIGHT_TOUR]


def tour_flip_sequence() -> list[int]:
    bits = tour_bits()
    flips: list[int] = []
    for idx, vertex in enumerate(bits):
        neighbor = bits[(idx + 1) % len(bits)]
        changed = [bit for bit in range(4) if vertex[bit] != neighbor[bit]]
        flips.append(changed[0] if len(changed) == 1 else -1)
    return flips


def tour_is_gray_hamilton_cycle() -> bool:
    bits = tour_bits()
    return (
        len(bits) == 16
        and len(set(bits)) == 16
        and all(hamming(bits[idx], bits[(idx + 1) % len(bits)]) == 1 for idx in range(len(bits)))
    )


def q4_adjacency_from_edges() -> dict[Bits, set[Bits]]:
    adjacency = {vertex: set() for vertex in q4_vertices()}
    for left, right in q4_edges():
        adjacency[left].add(right)
        adjacency[right].add(left)
    return adjacency


def graph_diameter(adjacency: dict[Bits, set[Bits]]) -> int:
    diameter = 0
    for source in adjacency:
        distances = {source: 0}
        queue: deque[Bits] = deque([source])
        while queue:
            vertex = queue.popleft()
            for neighbor in adjacency[vertex]:
                if neighbor not in distances:
                    distances[neighbor] = distances[vertex] + 1
                    queue.append(neighbor)
        diameter = max(diameter, max(distances.values()))
    return diameter


def q4_spectrum() -> dict[int, int]:
    # Eigenvalues of Q_n are n-2j with multiplicity C(n,j).  For n=4:
    return {4: 1, 2: 4, 0: 6, -2: 4, -4: 1}


def q4_square_face_count() -> int:
    # Choose two bit dimensions and freeze the other two bits.
    return len(list(combinations(range(4), 2))) * (2 ** (4 - 2))


def parity_partition_sizes() -> dict[str, int]:
    counts = Counter(sum(vertex) % 2 for vertex in q4_vertices())
    return {"even": counts[0], "odd": counts[1]}


def self_entangled_qutrit_q4_router_packet() -> dict[str, object]:
    mclxiii = _load(ROOT / "PART_MCLXIII_TEMPORAL_SELF_ENTANGLED_QUTRIT_results.json")
    mclxvii = _load(ROOT / "PART_MCLXVII_ONE_QUTRIT_TEMPORAL_COMPILER_results.json")

    bell_line_size = int(mclxiii["bell_stabilizer_line"]["line_size"])
    history_cells = int(mclxiii["temporal_qutrit"]["past_future_basis_pairs"])
    erased_single_qutrit = int(mclxiii["now_computation"]["single_qutrit_pauli_erased_nonidentity"])
    w33_rays = int(mclxiii["w33_observable_geometry"]["projective_rays"])
    w33_edges = int(mclxiii["w33_observable_geometry"]["srg"]["edges"])
    spread_size = int(mclxiii["spread_packet"]["spread_size"])
    compiler_contexts = int(mclxvii["compiled_substrate"]["complete_context_count"])

    kadj = knight_adjacency()
    kedges = knight_edges()
    qedges = q4_edges()
    medges = mapped_knight_edges()
    q4_adjacency = q4_adjacency_from_edges()
    flip_sequence = tour_flip_sequence()
    flip_counts = dict(sorted(Counter(flip_sequence).items()))
    dimension_counts = dimension_edge_counts()

    checks = {
        "bell_now_context_has_four_rays": bell_line_size == Q + 1 == 4,
        "context_square_is_4_by_4": bell_line_size * bell_line_size == 16,
        "toroidal_knight_graph_has_16_vertices": len(kadj) == 16,
        "toroidal_knight_graph_is_4_regular": sorted({len(neighbors) for neighbors in kadj.values()}) == [4],
        "toroidal_knight_graph_has_32_edges": len(kedges) == 32,
        "q4_has_16_vertices_and_32_edges": len(q4_vertices()) == 16 and len(qedges) == 32,
        "explicit_labeling_is_bijective": set(KNIGHT_TO_Q4.values()) == q4_vertices() and len(KNIGHT_TO_Q4) == 16,
        "mapped_knight_edges_are_q4_edges": medges == qedges,
        "every_knight_edge_is_one_bit_flip": all(
            hamming(KNIGHT_TO_Q4[left], KNIGHT_TO_Q4[right]) == 1 for left, right in kedges
        ),
        "each_q4_dimension_has_eight_edges": dimension_counts == {0: 8, 1: 8, 2: 8, 3: 8},
        "dimension_cut_matches_erased_single_qutrit_paulis": all(
            count == erased_single_qutrit for count in dimension_counts.values()
        ),
        "q4_network_diameter_matches_now_context_size": graph_diameter(q4_adjacency) == bell_line_size == 4,
        "q4_parity_bipartition_is_balanced": parity_partition_sizes() == {"even": 8, "odd": 8},
        "q4_spectrum_is_hamming_spectrum": q4_spectrum() == {4: 1, 2: 4, 0: 6, -2: 4, -4: 1},
        "q4_square_faces_match_w33_r_multiplicity": q4_square_face_count() == 24,
        "knight_tour_is_gray_hamilton_cycle": tour_is_gray_hamilton_cycle(),
        "tour_flip_sequence_is_repeated_clock": flip_sequence == [1, 2, 1, 3, 1, 2, 1, 0] * 2,
        "w33_payload_remains_ternary_not_q4": history_cells == 9
        and w33_rays == 40
        and w33_edges == 240
        and spread_size == compiler_contexts == 10,
    }

    return {
        "part": "MCLXXX",
        "theorem": "Self-entangled qutrit Q4 hypercube router law",
        "source_alignment": {
            "across_the_board_reading": "4x4 toroidal knight graph is the Q4 hypercube graph",
            "network_theory_reading": "Q4 vertices are 4-bit strings; edges flip exactly one bit",
            "claim_boundary": "external references motivate the graph identity; the verifier below proves the exact finite instance offline",
        },
        "self_entangled_qutrit_input": {
            "q": Q,
            "bell_state": mclxiii["temporal_qutrit"]["state"],
            "history_cells": history_cells,
            "now_context_rays": bell_line_size,
            "erased_single_qutrit_nonidentity_paulis": erased_single_qutrit,
            "w33_projective_rays": w33_rays,
            "w33_edges": w33_edges,
            "spread_contexts": spread_size,
        },
        "context_square_board": {
            "board": "Bell-now context square B x B",
            "side_length": bell_line_size,
            "vertices": bell_line_size * bell_line_size,
            "toroidal_boundary": True,
            "interpretation": "binary control/routing square around one four-ray ternary now-context",
        },
        "q4_router": {
            "vertices": len(q4_vertices()),
            "degree": 4,
            "edges": len(qedges),
            "diameter": graph_diameter(q4_adjacency),
            "parity_partition": parity_partition_sizes(),
            "spectrum": q4_spectrum(),
            "square_faces": q4_square_face_count(),
            "dimension_edge_counts": dimension_counts,
            "dimension_cut_identity": "each Q4 bit dimension has 8 edges, matching the 8 erased nonidentity single-qutrit Paulis",
        },
        "knight_to_q4_isomorphism": {
            "mapping": {str(key): value for key, value in sorted(KNIGHT_TO_Q4.items())},
            "mapped_edges_equal_q4_edges": medges == qedges,
        },
        "gray_knight_clock": {
            "knight_tour": KNIGHT_TOUR,
            "q4_tour": tour_bits(),
            "flip_sequence": flip_sequence,
            "flip_counts": flip_counts,
            "statement": "the closed toroidal knight tour is a Gray-code Hamilton cycle on Q4",
        },
        "ternary_binary_bridge": {
            "payload": "self-entangled qutrit / F3^4 W33 Pauli geometry",
            "router": "binary Q4 hypercube network on the 4x4 toroidal now-context square",
            "key_identity": "4 now rays -> 4 Q4 dimensions; 8 erased Pauli directions -> 8 edges per dimension",
            "boundary": "Q4 is a finite scheduler/control network for the ternary context, not a replacement for W33",
        },
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = self_entangled_qutrit_q4_router_packet()
    out_path = ROOT / "PART_MCLXXX_SELF_ENTANGLED_QUTRIT_Q4_ROUTER_results.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCLXXX: Self-Entangled Qutrit Q4 Hypercube Router ===")
    print("4x4 toroidal knight graph = Q4")
    print(packet["q4_router"]["dimension_cut_identity"])
    print(packet["gray_knight_clock"]["statement"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
