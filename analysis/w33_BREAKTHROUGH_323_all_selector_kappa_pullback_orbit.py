"""W(3,3) BREAKTHROUGH 323: all-selector kappa pullback orbit.

BT272 classified the eight Mobius-Kantor selectors in the weight-3 complement
of Q4 inside K8,8.  BT322 pulled one selected witness back through the BT320/321
complement involution kappa and found a second Mobius-Kantor sheet inside Q4.

BT323 closes the classifier:

    every one of the eight BT272 selectors pulls back through kappa
    to a Q4-side perfect matching whose complement in Q4 is again
    a connected cubic girth-6 Mobius-Kantor graph.

The eight Q4-side selectors form one affine coordinate orbit of size 8, with
the same stabilizer order 48 = mu*k as the BT272 weight-3 selectors.

Their intersection geometry is sharper still:

    disjointness graph      = K4 disjoint-union K4
    two-overlap graph       = K4,4

Each Q4 edge appears in exactly two of the eight selector matchings and exactly
six of the eight Mobius-Kantor complements.  This is the exact finite route
compression suggested by the external router hints: raw edge-level motion
collapses to an eight-state selector orbit with a two-fiber 4+4 split and
cross-fiber transport graph K4,4.
"""

from __future__ import annotations

from collections import Counter, defaultdict, deque
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_271_k88_q4_mobius_kantor_decomposition import (  # noqa: E402
    adjacency,
    degree_distribution,
    girth,
    q4_edges,
    xor_weight_distribution,
)
from analysis.w33_BREAKTHROUGH_272_mobius_kantor_selector_classification import (  # noqa: E402
    K,
    MU,
    affine_coordinate_automorphisms,
    apply_affine_to_matching,
    mobius_kantor_selector_classification_packet,
    weight3_complement_edges,
)
from analysis.w33_BREAKTHROUGH_321_q4_reye_complement_lift_duality import (  # noqa: E402
    kappa,
    pair,
)


Q = 3
OCTONION = 8
F = 24


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


def xor_direction_counts(edge_set: set[tuple[int, int]]) -> dict[int, int]:
    return dict(sorted(Counter(left ^ right for left, right in edge_set).items()))


def orbit_sizes(
    matchings: list[frozenset[tuple[int, int]]],
    automorphisms: list[tuple[tuple[int, ...], int]],
) -> list[int]:
    matching_set = set(matchings)
    visited = set()
    sizes = []
    for matching in matchings:
        if matching in visited:
            continue
        queue = deque([matching])
        visited.add(matching)
        size = 0
        while queue:
            current = queue.popleft()
            size += 1
            for automorphism in automorphisms:
                image = apply_affine_to_matching(current, automorphism)
                if image in matching_set and image not in visited:
                    visited.add(image)
                    queue.append(image)
        sizes.append(size)
    return sorted(sizes)


def intersection_graph(
    matchings: list[frozenset[tuple[int, int]]],
    intersection_size: int,
) -> dict[int, set[int]]:
    graph = {index: set() for index in range(len(matchings))}
    for left_index, left in enumerate(matchings):
        for right_index in range(left_index + 1, len(matchings)):
            right = matchings[right_index]
            if len(left & right) == intersection_size:
                graph[left_index].add(right_index)
                graph[right_index].add(left_index)
    return graph


def component_sizes(graph: dict[int, set[int]]) -> list[int]:
    seen = set()
    sizes = []
    for node in graph:
        if node in seen:
            continue
        queue = deque([node])
        seen.add(node)
        size = 0
        while queue:
            current = queue.popleft()
            size += 1
            for nxt in graph[current]:
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
        sizes.append(size)
    return sorted(sizes)


def is_complete_on_components(graph: dict[int, set[int]], sizes: list[int]) -> bool:
    return sorted(len(neighbors) for neighbors in graph.values()) == sorted(size - 1 for size in sizes for _ in range(size))


def is_k44(graph: dict[int, set[int]], parts: tuple[set[int], set[int]]) -> bool:
    left, right = parts
    return all(graph[node] == right for node in left) and all(graph[node] == left for node in right)


def all_selector_kappa_pullback_orbit_packet() -> dict:
    bt272 = mobius_kantor_selector_classification_packet()
    q4 = q4_edges()
    weight3 = weight3_complement_edges()
    source_selectors = [_edge_set(rows) for rows in bt272["selector_matchings"]]
    q4_selectors = [frozenset(kappa_image(selector)) for selector in source_selectors]
    q4_mobius_kantor_layers = [q4 - set(selector) for selector in q4_selectors]
    source_mk_layers = [weight3 - selector for selector in source_selectors]
    automorphisms = affine_coordinate_automorphisms()

    selector_rows = []
    for index, (source_selector, q4_selector, q4_mk) in enumerate(
        zip(source_selectors, q4_selectors, q4_mobius_kantor_layers)
    ):
        selector_rows.append(
            {
                "selector_index": index,
                "source_weight3_matching": sorted([list(edge) for edge in source_selector]),
                "q4_pullback_matching": sorted([list(edge) for edge in q4_selector]),
                "q4_mobius_kantor_layer": sorted([list(edge) for edge in q4_mk]),
                "q4_matching_xor_profile": xor_direction_counts(q4_selector),
                "q4_mk_girth": girth(q4_mk),
            }
        )

    disjoint_graph = intersection_graph(q4_selectors, 0)
    two_overlap_graph = intersection_graph(q4_selectors, 2)
    disjoint_components = component_sizes(disjoint_graph)
    disjoint_parts = []
    seen = set()
    for node in disjoint_graph:
        if node in seen:
            continue
        queue = deque([node])
        seen.add(node)
        part = set()
        while queue:
            current = queue.popleft()
            part.add(current)
            for nxt in disjoint_graph[current]:
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
        disjoint_parts.append(part)
    disjoint_parts = sorted(disjoint_parts, key=lambda part: sorted(part))

    q4_selector_edge_frequency = Counter(edge for selector in q4_selectors for edge in selector)
    q4_mk_edge_frequency = Counter(edge for layer in q4_mobius_kantor_layers for edge in layer)
    source_selector_edge_frequency = Counter(edge for selector in source_selectors for edge in selector)
    source_mk_edge_frequency = Counter(edge for layer in source_mk_layers for edge in layer)
    pair_intersections = Counter(
        len(left & right)
        for left_index, left in enumerate(q4_selectors)
        for right in q4_selectors[left_index + 1 :]
    )

    checks = {
        "bt272_source_selector_count_is_8": bt272["mobius_kantor_selector_count"] == 2**Q == 8,
        "q4_pullback_selector_count_is_8": len(q4_selectors) == 2**Q == 8,
        "q4_pullbacks_are_unique": len(set(q4_selectors)) == 2**Q,
        "each_q4_pullback_is_perfect_matching": all(
            len(selector) == OCTONION and degree_distribution(selector) == {1: 16}
            for selector in q4_selectors
        ),
        "each_q4_pullback_has_balanced_coordinate_xor_profile": all(
            xor_direction_counts(selector) == {1: 2, 2: 2, 4: 2, 8: 2}
            for selector in q4_selectors
        ),
        "each_q4_complement_is_mobius_kantor": all(
            len(layer) == F
            and degree_distribution(layer) == {Q: 16}
            and is_connected(layer)
            and girth(layer) == 6
            for layer in q4_mobius_kantor_layers
        ),
        "kappa_maps_source_selectors_to_q4_pullbacks": all(
            kappa_image(source_selector) == set(q4_selector)
            for source_selector, q4_selector in zip(source_selectors, q4_selectors)
        ),
        "kappa_maps_q4_pullbacks_back_to_source": all(
            kappa_image(set(q4_selector)) == source_selector
            for source_selector, q4_selector in zip(source_selectors, q4_selectors)
        ),
        "kappa_maps_q4_mk_layers_to_source_mk_layers": all(
            kappa_image(q4_mk) == source_mk
            for q4_mk, source_mk in zip(q4_mobius_kantor_layers, source_mk_layers)
        ),
        "q4_selectors_form_one_affine_orbit": orbit_sizes(q4_selectors, automorphisms) == [2**Q],
        "q4_selector_stabilizer_order_is_mu_k": len(automorphisms) // len(q4_selectors) == MU * K == 48,
        "pairwise_intersections_are_12_zero_and_16_two": pair_intersections == {0: 12, 2: 16},
        "disjoint_graph_is_two_K4": component_sizes(disjoint_graph) == [4, 4]
        and is_complete_on_components(disjoint_graph, [4, 4]),
        "two_overlap_graph_is_K4_4": is_k44(two_overlap_graph, (disjoint_parts[0], disjoint_parts[1])),
        "q4_selector_edges_cover_Q4_twice": set(q4_selector_edge_frequency) == q4
        and Counter(q4_selector_edge_frequency.values()) == {2: 32},
        "q4_mk_edges_cover_Q4_six_times": set(q4_mk_edge_frequency) == q4
        and Counter(q4_mk_edge_frequency.values()) == {6: 32},
        "source_selector_edges_cover_weight3_twice": set(source_selector_edge_frequency) == weight3
        and Counter(source_selector_edge_frequency.values()) == {2: 32},
        "source_mk_edges_cover_weight3_six_times": set(source_mk_edge_frequency) == weight3
        and Counter(source_mk_edge_frequency.values()) == {6: 32},
        "intersection_fiber_sizes_are_4_plus_4": [len(part) for part in disjoint_parts] == [4, 4],
        "raw_edge_to_selector_compression_is_64_to_8": 64 // len(q4_selectors) == 8,
    }

    return {
        "breakthrough": 323,
        "title": "All-selector kappa pullback orbit",
        "selector_rows": selector_rows,
        "q4_selector_count": len(q4_selectors),
        "q4_mobius_kantor_count": len(q4_mobius_kantor_layers),
        "affine_automorphism_order": len(automorphisms),
        "q4_selector_orbit_sizes": orbit_sizes(q4_selectors, automorphisms),
        "q4_selector_stabilizer_order": len(automorphisms) // len(q4_selectors),
        "pair_intersection_distribution": dict(sorted(pair_intersections.items())),
        "disjointness_graph": {str(node): sorted(neighbors) for node, neighbors in disjoint_graph.items()},
        "two_overlap_graph": {str(node): sorted(neighbors) for node, neighbors in two_overlap_graph.items()},
        "disjointness_components": [sorted(part) for part in disjoint_parts],
        "coverage": {
            "q4_selector_edge_frequency": dict(sorted((str(edge), count) for edge, count in q4_selector_edge_frequency.items())),
            "q4_mk_edge_frequency_distribution": dict(sorted(Counter(q4_mk_edge_frequency.values()).items())),
            "source_selector_edge_frequency_distribution": dict(sorted(Counter(source_selector_edge_frequency.values()).items())),
            "source_mk_edge_frequency_distribution": dict(sorted(Counter(source_mk_edge_frequency.values()).items())),
        },
        "router_hint_reading": (
            "Following the external router hint, the effective state is not the "
            "raw 64-edge K8,8 carrier.  It compresses to an eight-selector route "
            "orbit.  The orbit has two four-state fibers under disjointness, and "
            "the cross-fiber transition graph is K4,4."
        ),
        "boundary": (
            "This is an exact finite classifier for BT272 selector pullbacks. "
            "The external router repositories were used only as search heuristics "
            "for phase/fiber compression language, not as proof dependencies."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = all_selector_kappa_pullback_orbit_packet()

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 323: ALL-SELECTOR KAPPA PULLBACK ORBIT")
    print("=" * 78)
    print()
    print(f"q4 selectors        = {packet['q4_selector_count']}")
    print(f"orbit sizes         = {packet['q4_selector_orbit_sizes']}")
    print(f"stabilizer order    = {packet['q4_selector_stabilizer_order']}")
    print(f"intersections       = {packet['pair_intersection_distribution']}")
    print(f"disjoint components = {packet['disjointness_components']}")
    print(f"verified            = {packet['n_verified']} / {len(packet['checks'])}")
    print()
    print("ROUTER-HINT READING:")
    print(f"  {packet['router_hint_reading']}")

    out = ROOT / "data" / "w33_BREAKTHROUGH_323_all_selector_kappa_pullback_orbit.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print()
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
