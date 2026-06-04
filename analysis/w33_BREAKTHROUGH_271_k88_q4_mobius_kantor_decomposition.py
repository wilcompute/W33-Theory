"""W(3,3) BREAKTHROUGH 271: K8,8 = Q4 + Mobius-Kantor + M8.

BT270 showed that Q_4 and the Mobius-Kantor graph form a 16-vertex
quartic/cubic complementary pair by parameter count.  BT271 makes the
complementarity explicit on one shared vertex set.

Use vertices F_2^4 = {0,...,15}, split by parity into 8 even and 8 odd
vertices.  Then K_{8,8} is the full cross-parity graph with 64 edges.

  Q_4 uses the 32 cross edges whose XOR difference has Hamming weight 1.
  The cross-parity complement uses the 32 edges whose XOR difference has
  Hamming weight 3.

Inside that weight-3 complement there is an explicit Mobius-Kantor graph
with 24 edges.  The remaining 8 edges form a perfect matching M8.

Therefore:

    K_{8,8} = Q_4  disjoint-union  MK  disjoint-union  M8

At each vertex the degrees split as:

    8 = 4 + 3 + 1 = mu + q + 1 = 2^q.

This is the first explicit edge-level realization of the BT269 Hopf identity
Phi_6 = mu + q inside the complete past/future octonion bipartite carrier:
the heptad degree 7 is Q_4 + Mobius-Kantor, and the remaining identity
matching closes it to the full 8-dimensional octonion cross-space.
"""

from __future__ import annotations

from collections import Counter, deque
from itertools import combinations
import json
from pathlib import Path


Q = 3
MU = 4
PHI6 = 7
F = 24

# Isomorphism from the standard GP(8,3) Mobius-Kantor labels to F_2^4 labels.
MK_TO_F2_4 = {
    0: 0,
    1: 7,
    2: 9,
    3: 2,
    4: 15,
    5: 8,
    6: 6,
    7: 13,
    8: 11,
    9: 10,
    10: 14,
    11: 12,
    12: 4,
    13: 5,
    14: 1,
    15: 3,
}


def hamming_weight(value: int) -> int:
    return bin(value).count("1")


def parity(value: int) -> int:
    return hamming_weight(value) % 2


def edge(left: int, right: int) -> tuple[int, int]:
    return tuple(sorted((left, right)))


def complete_bipartite_edges() -> set[tuple[int, int]]:
    evens = [vertex for vertex in range(16) if parity(vertex) == 0]
    odds = [vertex for vertex in range(16) if parity(vertex) == 1]
    return {edge(even, odd) for even in evens for odd in odds}


def q4_edges() -> set[tuple[int, int]]:
    return {
        edge(vertex, vertex ^ (1 << bit))
        for vertex in range(16)
        for bit in range(4)
    }


def mobius_kantor_standard_edges() -> set[tuple[int, int]]:
    edges = set()
    for index in range(8):
        edges.add(edge(index, (index + 1) % 8))
        edges.add(edge(8 + index, 8 + ((index + 3) % 8)))
        edges.add(edge(index, 8 + index))
    return edges


def relabel_edges(
    edges: set[tuple[int, int]],
    mapping: dict[int, int],
) -> set[tuple[int, int]]:
    return {edge(mapping[left], mapping[right]) for left, right in edges}


def adjacency(edge_set: set[tuple[int, int]]) -> dict[int, set[int]]:
    adj = {vertex: set() for vertex in range(16)}
    for left, right in edge_set:
        adj[left].add(right)
        adj[right].add(left)
    return adj


def girth(edge_set: set[tuple[int, int]]) -> int:
    adj = adjacency(edge_set)
    best = 10**9
    for source in range(16):
        distance = {source: 0}
        parent = {source: None}
        queue = deque([source])
        while queue:
            current = queue.popleft()
            for nxt in adj[current]:
                if nxt not in distance:
                    distance[nxt] = distance[current] + 1
                    parent[nxt] = current
                    queue.append(nxt)
                elif parent[current] != nxt and parent[nxt] != current:
                    best = min(best, distance[current] + distance[nxt] + 1)
    return best


def degree_distribution(edge_set: set[tuple[int, int]]) -> dict[int, int]:
    return dict(sorted(Counter(len(neighbors) for neighbors in adjacency(edge_set).values()).items()))


def xor_weight_distribution(edge_set: set[tuple[int, int]]) -> dict[int, int]:
    return dict(sorted(Counter(hamming_weight(left ^ right) for left, right in edge_set).items()))


def k88_q4_mobius_kantor_decomposition_packet() -> dict:
    k88 = complete_bipartite_edges()
    q4 = q4_edges()
    cross_complement = k88 - q4
    mk_standard = mobius_kantor_standard_edges()
    mk = relabel_edges(mk_standard, MK_TO_F2_4)
    residual = cross_complement - mk
    union = q4 | mk | residual

    residual_adj = adjacency(residual)
    residual_xor_counts = dict(sorted(Counter(left ^ right for left, right in residual).items()))
    edge_parts = {
        "Q4": sorted([list(edge_) for edge_ in q4]),
        "Mobius_Kantor": sorted([list(edge_) for edge_ in mk]),
        "M8_matching": sorted([list(edge_) for edge_ in residual]),
    }

    checks = {
        "k88_has_64_edges": len(k88) == 64 == 2 ** (2 * Q),
        "q4_has_32_weight1_edges": len(q4) == 32 and xor_weight_distribution(q4) == {1: 32},
        "cross_complement_has_32_weight3_edges": len(cross_complement) == 32
        and xor_weight_distribution(cross_complement) == {3: 32},
        "mobius_kantor_has_24_edges": len(mk) == F,
        "mobius_kantor_lies_in_weight3_complement": mk <= cross_complement,
        "mobius_kantor_is_cubic": degree_distribution(mk) == {Q: 16},
        "mobius_kantor_girth_is_q_factorial": girth(mk) == 6,
        "residual_has_8_edges": len(residual) == 2**Q,
        "residual_is_perfect_matching": degree_distribution(residual) == {1: 16}
        and all(len(neighbors) == 1 for neighbors in residual_adj.values()),
        "parts_are_disjoint": len(q4 & mk) == len(q4 & residual) == len(mk & residual) == 0,
        "parts_union_to_k88": union == k88,
        "degree_split_is_mu_q_1": 4 + Q + 1 == 2**Q == 8,
        "edge_split_is_32_24_8": len(q4) + len(mk) + len(residual) == 64,
        "heptad_layer_edges_are_56": len(q4) + len(mk) == 56 == 2**Q * PHI6,
        "residual_xor_directions_are_balanced": residual_xor_counts == {7: 2, 11: 2, 13: 2, 14: 2},
    }

    return {
        "breakthrough": 271,
        "title": "K8,8 decomposes as Q4 plus Mobius-Kantor plus matching",
        "vertex_model": "F_2^4 labels 0..15, even/odd parity bipartition",
        "mobius_kantor_embedding": MK_TO_F2_4,
        "edge_counts": {
            "K8_8": len(k88),
            "Q4": len(q4),
            "Mobius_Kantor": len(mk),
            "M8_matching": len(residual),
            "Q4_plus_MK": len(q4) + len(mk),
        },
        "degree_split": {"Q4": MU, "Mobius_Kantor": Q, "M8_matching": 1, "total": 2**Q},
        "xor_weight_distributions": {
            "Q4": xor_weight_distribution(q4),
            "cross_complement": xor_weight_distribution(cross_complement),
            "Mobius_Kantor": xor_weight_distribution(mk),
            "M8_matching": xor_weight_distribution(residual),
        },
        "residual_xor_direction_counts": residual_xor_counts,
        "girths": {"Q4": girth(q4), "Mobius_Kantor": girth(mk)},
        "edge_parts": edge_parts,
        "architectural_reading": (
            "On the parity bipartition of F_2^4, the full octonion cross-space "
            "K8,8 splits into three disjoint layers: Q4 contributes degree mu=4, "
            "Mobius-Kantor contributes degree q=3, and the residual perfect "
            "matching contributes the identity degree. Thus 8 = mu + q + 1 and "
            "the heptad layer Phi_6 = mu + q is the Q4+MK edge carrier of size "
            "56 = 2^q * Phi_6. This makes BT269/270's Hopf identity edge-level "
            "and explicit."
        ),
        "boundary": (
            "This packet proves one explicit F_2^4 labeling of the decomposition. "
            "It does not yet classify all such Mobius-Kantor embeddings in the "
            "weight-3 complement."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = k88_q4_mobius_kantor_decomposition_packet()

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 271: K8,8 = Q4 + MOBIUS-KANTOR + M8")
    print("=" * 78)
    print()
    print(f"edge counts     = {packet['edge_counts']}")
    print(f"degree split    = {packet['degree_split']}")
    print(f"girths          = {packet['girths']}")
    print(f"residual XORs   = {packet['residual_xor_direction_counts']}")
    print(f"verified        = {packet['n_verified']} / {len(packet['checks'])}")
    print()
    print("ARCHITECTURAL READING:")
    print(f"  {packet['architectural_reading']}")

    out = Path("data") / "w33_BREAKTHROUGH_271_k88_q4_mobius_kantor_decomposition.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print()
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
