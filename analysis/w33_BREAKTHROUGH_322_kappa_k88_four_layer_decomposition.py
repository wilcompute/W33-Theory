"""W(3,3) BREAKTHROUGH 322: kappa K8,8 four-layer decomposition.

BT271 decomposes the parity bipartite cross-space as

    K8,8 = Q4 disjoint-union MK disjoint-union M8,

where Q4 is the weight-1 layer and MK + M8 is the weight-3 layer.

BT321 identifies the BT320 complement involution

    kappa = J + I = [14, 13, 11, 7]

as the lift-duality that swaps weight-1 Q4 edges with weight-3 cubical
body-diagonal edges over the same Reye quotient edge.

This packet fuses those facts.  Pull the BT271 selected weight-3 layers back
through kappa:

    MK_Q4 = kappa(MK_weight3)  subset Q4, 24 edges, cubic, girth 6
    M8_Q4 = kappa(M8_weight3)  subset Q4, 8 edges, perfect matching.

Then

    Q4 = MK_Q4 disjoint-union M8_Q4,

and the full K8,8 carrier becomes a kappa-swapped four-layer decomposition:

    K8,8 = MK_Q4 + M8_Q4 + MK_weight3 + M8_weight3.

The kappa edge-orbit quotient has 32 orbits split as 24 Mobius-Kantor orbits
and 8 matching orbits.  This is the exact edge-level form of the statement
that the Q4 router and the Mobius-Kantor selector are two lift-sheets of the
same Reye quotient carrier.
"""

from __future__ import annotations

from collections import Counter, deque
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_271_k88_q4_mobius_kantor_decomposition import (  # noqa: E402
    adjacency,
    complete_bipartite_edges,
    degree_distribution,
    girth,
    k88_q4_mobius_kantor_decomposition_packet,
    q4_edges,
    xor_weight_distribution,
)
from analysis.w33_BREAKTHROUGH_321_q4_reye_complement_lift_duality import (  # noqa: E402
    kappa,
    pair,
)


Q = 3
F = 24
OCTONION = 8
K88_EDGES = 64


def _edge_set(rows: list[list[int]]) -> set[tuple[int, int]]:
    return {tuple(row) for row in rows}


def kappa_edge(edge: tuple[int, int]) -> tuple[int, int]:
    return pair(kappa(edge[0]), kappa(edge[1]))


def kappa_image(edge_set: set[tuple[int, int]]) -> set[tuple[int, int]]:
    return {kappa_edge(edge) for edge in edge_set}


def is_connected(edge_set: set[tuple[int, int]]) -> bool:
    adj = adjacency(edge_set)
    start = next(iter(adj))
    seen = {start}
    queue = deque([start])
    while queue:
        current = queue.popleft()
        for nxt in adj[current]:
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return len(seen) == 16


def matching_xor_direction_counts(edge_set: set[tuple[int, int]]) -> dict[int, int]:
    return dict(sorted(Counter(left ^ right for left, right in edge_set).items()))


def edge_orbits_under_kappa(edge_set: set[tuple[int, int]]) -> list[tuple[tuple[int, int], ...]]:
    seen = set()
    orbits = []
    for edge in sorted(edge_set):
        if edge in seen:
            continue
        orbit = tuple(sorted({edge, kappa_edge(edge)}))
        seen.update(orbit)
        orbits.append(orbit)
    return orbits


def kappa_k88_four_layer_decomposition_packet() -> dict:
    bt271 = k88_q4_mobius_kantor_decomposition_packet()
    q4 = q4_edges()
    k88 = complete_bipartite_edges()
    mk_weight3 = _edge_set(bt271["edge_parts"]["Mobius_Kantor"])
    m8_weight3 = _edge_set(bt271["edge_parts"]["M8_matching"])
    weight3 = mk_weight3 | m8_weight3
    mk_q4 = kappa_image(mk_weight3)
    m8_q4 = kappa_image(m8_weight3)
    four_layer_union = mk_q4 | m8_q4 | mk_weight3 | m8_weight3
    edge_orbits = edge_orbits_under_kappa(k88)
    mk_orbits = [orbit for orbit in edge_orbits if set(orbit) & mk_weight3]
    matching_orbits = [orbit for orbit in edge_orbits if set(orbit) & m8_weight3]

    checks = {
        "bt271_original_counts_hold": bt271["edge_counts"] == {
            "K8_8": 64,
            "Q4": 32,
            "Mobius_Kantor": 24,
            "M8_matching": 8,
            "Q4_plus_MK": 56,
        },
        "kappa_maps_q4_to_weight3": kappa_image(q4) == weight3,
        "kappa_maps_weight3_to_q4": kappa_image(weight3) == q4,
        "mk_q4_has_24_edges": len(mk_q4) == F,
        "m8_q4_has_8_edges": len(m8_q4) == OCTONION,
        "q4_splits_as_mk_q4_plus_m8_q4": mk_q4 | m8_q4 == q4 and len(mk_q4 & m8_q4) == 0,
        "mk_q4_is_connected_cubic": is_connected(mk_q4) and degree_distribution(mk_q4) == {Q: 16},
        "mk_q4_has_girth_6": girth(mk_q4) == 6,
        "m8_q4_is_perfect_matching": degree_distribution(m8_q4) == {1: 16},
        "m8_q4_balanced_coordinate_directions": matching_xor_direction_counts(m8_q4)
        == {1: 2, 2: 2, 4: 2, 8: 2},
        "mk_q4_uses_weight1_edges": xor_weight_distribution(mk_q4) == {1: F},
        "m8_q4_uses_weight1_edges": xor_weight_distribution(m8_q4) == {1: OCTONION},
        "mk_weight3_uses_weight3_edges": xor_weight_distribution(mk_weight3) == {3: F},
        "m8_weight3_uses_weight3_edges": xor_weight_distribution(m8_weight3) == {3: OCTONION},
        "kappa_swaps_mk_layers": kappa_image(mk_q4) == mk_weight3 and kappa_image(mk_weight3) == mk_q4,
        "kappa_swaps_matching_layers": kappa_image(m8_q4) == m8_weight3
        and kappa_image(m8_weight3) == m8_q4,
        "four_layers_are_disjoint": (
            len(mk_q4 & m8_q4)
            == len(mk_q4 & mk_weight3)
            == len(mk_q4 & m8_weight3)
            == len(m8_q4 & mk_weight3)
            == len(m8_q4 & m8_weight3)
            == len(mk_weight3 & m8_weight3)
            == 0
        ),
        "four_layers_union_to_k88": four_layer_union == k88,
        "four_layer_counts_are_24_8_24_8": [len(mk_q4), len(m8_q4), len(mk_weight3), len(m8_weight3)]
        == [24, 8, 24, 8],
        "kappa_edge_orbits_count_32": len(edge_orbits) == 32,
        "kappa_edge_orbits_have_size_2": all(len(orbit) == 2 for orbit in edge_orbits),
        "orbit_quotient_splits_24_plus_8": len(mk_orbits) == 24 and len(matching_orbits) == 8,
        "two_mobius_kantor_layers_total_48": len(mk_q4) + len(mk_weight3) == 2 * F == 48,
        "two_matching_layers_total_16": len(m8_q4) + len(m8_weight3) == 2 * OCTONION == 16,
        "all_layers_sum_to_k88": 24 + 8 + 24 + 8 == K88_EDGES,
    }

    return {
        "breakthrough": 322,
        "title": "Kappa K8,8 four-layer decomposition",
        "layers": {
            "MK_Q4": sorted([list(edge) for edge in mk_q4]),
            "M8_Q4": sorted([list(edge) for edge in m8_q4]),
            "MK_weight3": sorted([list(edge) for edge in mk_weight3]),
            "M8_weight3": sorted([list(edge) for edge in m8_weight3]),
        },
        "layer_counts": {
            "MK_Q4": len(mk_q4),
            "M8_Q4": len(m8_q4),
            "MK_weight3": len(mk_weight3),
            "M8_weight3": len(m8_weight3),
            "total": len(four_layer_union),
        },
        "layer_xor_weight_distributions": {
            "MK_Q4": xor_weight_distribution(mk_q4),
            "M8_Q4": xor_weight_distribution(m8_q4),
            "MK_weight3": xor_weight_distribution(mk_weight3),
            "M8_weight3": xor_weight_distribution(m8_weight3),
        },
        "matching_direction_counts": {
            "M8_Q4": matching_xor_direction_counts(m8_q4),
            "M8_weight3": matching_xor_direction_counts(m8_weight3),
        },
        "kappa_orbit_quotient": {
            "edge_orbits": [[list(edge) for edge in orbit] for orbit in edge_orbits],
            "orbit_count": len(edge_orbits),
            "mk_orbits": len(mk_orbits),
            "matching_orbits": len(matching_orbits),
            "quotient_split": "24 Mobius-Kantor orbits + 8 matching orbits",
        },
        "architectural_reading": (
            "Kappa does not merely map Q4 to an undifferentiated weight-3 shell. "
            "It pulls the BT271 selector back through the lift, splitting Q4 "
            "itself into a Mobius-Kantor cubic plus a perfect matching. The full "
            "K8,8 cross-space is therefore two kappa-swapped sheets, each with "
            "a 24-edge cubic layer and an 8-edge identity layer."
        ),
        "boundary": (
            "This uses the explicit BT271 selector. BT272 proves there are eight "
            "Mobius-Kantor selectors in one affine orbit; this packet does not "
            "yet classify the kappa pullbacks of all eight selectors."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = kappa_k88_four_layer_decomposition_packet()

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 322: KAPPA K8,8 FOUR-LAYER DECOMPOSITION")
    print("=" * 78)
    print()
    print(f"layer counts   = {packet['layer_counts']}")
    print(f"orbit quotient = {packet['kappa_orbit_quotient']['quotient_split']}")
    print(f"verified       = {packet['n_verified']} / {len(packet['checks'])}")
    print()
    print("ARCHITECTURAL READING:")
    print(f"  {packet['architectural_reading']}")

    out = ROOT / "data" / "w33_BREAKTHROUGH_322_kappa_k88_four_layer_decomposition.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print()
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
