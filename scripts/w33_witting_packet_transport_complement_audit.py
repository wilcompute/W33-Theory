#!/usr/bin/env python3
"""Exact transport-complement audit for the Witting packet foliation layer.

This pushes the Witting packet program one step beyond quotient geometry.

Starting from the 45 packet leaves and the 27 packet-induced K5 cliques:
1. The disjointness graph on the 45 packet leaves is exactly SRG(45,32,22,24).
2. That packet transport graph is isomorphic to the reconstructed center-quad
   transport graph.
3. Packet transport adjacency is exactly leaf disjointness, while the
   non-transport pairs are exactly the singleton-intersection pairs of the
   quotient point graph.
4. The 27 packet lines become exact 5-cocliques in the transport graph.
5. Every packet transport edge induces a unique local S3 matching between the
   three packet lines through its endpoints, and all six permutations occur
   under the canonical sorted packet labels.

So the Witting packet layer now reconstructs the full exact 45-point transport
graph, not just the 45-point / 27-line quotient geometry beneath it.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from itertools import combinations
import json
from pathlib import Path
import sys
import time
from typing import Any

import networkx as nx


ROOT = Path(__file__).resolve().parents[1]
for candidate in (ROOT, ROOT / "scripts", ROOT / "exploration", ROOT / "pillars"):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)

from exploration.w33_center_quad_transport_bridge import reconstructed_quotient_graph  # noqa: E402
from scripts.w33_witting_packet_quotient_geometry_audit import (  # noqa: E402
    _build_leaf_list,
    _leaf_graph,
    _line_graph,
    _packet_lines,
    _srg_parameters,
)


def _leaf_packet_lines(packet_lines: list[tuple[int, ...]], leaf_count: int) -> list[tuple[int, int, int]]:
    memberships: list[tuple[int, int, int]] = []
    for leaf in range(leaf_count):
        memberships.append(tuple(sorted(index for index, line in enumerate(packet_lines) if leaf in line)))
    return memberships


def _permutation_parity(permutation: tuple[int, int, int]) -> int:
    inversions = 0
    for i in range(3):
        for j in range(i + 1, 3):
            inversions += permutation[i] > permutation[j]
    return inversions % 2


def _local_s3_matching(
    transport_graph: nx.Graph,
    leaf_packet_lines: list[tuple[int, int, int]],
    packet_line_graph: nx.Graph,
) -> dict[str, Any]:
    permutation_counts = Counter()
    parity_counts = Counter()
    example_edges: dict[tuple[int, int, int], dict[str, Any]] = {}
    every_edge_has_unique_matching = True

    for left, right in sorted(transport_graph.edges()):
        source = leaf_packet_lines[left]
        target = leaf_packet_lines[right]
        permutation = []
        for packet_line in source:
            matches = [index for index, other in enumerate(target) if packet_line_graph.has_edge(packet_line, other)]
            if len(matches) != 1:
                every_edge_has_unique_matching = False
                break
            permutation.append(matches[0])
        permutation_tuple = tuple(permutation)
        if len(set(permutation_tuple)) != 3:
            every_edge_has_unique_matching = False
            break
        permutation_counts[permutation_tuple] += 1
        parity_counts[_permutation_parity(permutation_tuple)] += 1
        example_edges.setdefault(
            permutation_tuple,
            {
                "transport_edge": [left, right],
                "source_packet_lines": list(source),
                "target_packet_lines": list(target),
            },
        )

    return {
        "every_transport_edge_has_unique_matching": every_edge_has_unique_matching,
        "all_six_permutations_realized_under_sorted_packet_labels": len(permutation_counts) == 6,
        "permutation_counts_under_sorted_packet_labels": {
            "".join(map(str, permutation)): count
            for permutation, count in sorted(permutation_counts.items())
        },
        "permutation_parity_distribution": dict(sorted(parity_counts.items())),
        "example_edges": {
            "".join(map(str, permutation)): payload
            for permutation, payload in sorted(example_edges.items())
        },
    }


@lru_cache(maxsize=1)
def analyze() -> dict[str, Any]:
    leaves = _build_leaf_list()
    leaf_graph = _leaf_graph(leaves)
    transport_graph = nx.complement(leaf_graph)

    packet_lines = _packet_lines(leaves)
    packet_line_graph = _line_graph(packet_lines)
    leaf_packet_lines = _leaf_packet_lines(packet_lines, len(leaves))

    quotient_transport_graph, _raw_z2 = reconstructed_quotient_graph()

    edge_intersections = Counter()
    nonedge_intersections = Counter()
    for left, right in combinations(range(len(leaves)), 2):
        intersection = len(set(leaves[left][2]) & set(leaves[right][2]))
        if transport_graph.has_edge(left, right):
            edge_intersections[intersection] += 1
        else:
            nonedge_intersections[intersection] += 1

    packet_line_edge_counts = Counter(
        sum(1 for left, right in combinations(line, 2) if transport_graph.has_edge(left, right))
        for line in packet_lines
    )

    local_matching = _local_s3_matching(transport_graph, leaf_packet_lines, packet_line_graph)

    theorem = {
        "the_packet_leaf_disjointness_graph_is_exactly_srg_45_32_22_24": (
            transport_graph.number_of_nodes() == 45
            and transport_graph.number_of_edges() == 720
            and Counter(dict(transport_graph.degree()).values()) == Counter({32: 45})
            and Counter(
                len(set(transport_graph.neighbors(left)) & set(transport_graph.neighbors(right)))
                for left, right in transport_graph.edges()
            )
            == Counter({22: 720})
            and Counter(
                len(set(transport_graph.neighbors(left)) & set(transport_graph.neighbors(right)))
                for left, right in combinations(transport_graph.nodes(), 2)
                if not transport_graph.has_edge(left, right)
            )
            == Counter({24: 270})
        ),
        "the_packet_transport_graph_is_isomorphic_to_the_exact_centerquad_transport_graph": (
            nx.is_isomorphic(transport_graph, quotient_transport_graph) is True
        ),
        "packet_transport_edges_are_exactly_disjoint_leaf_pairs": (
            edge_intersections == Counter({0: 720}) and nonedge_intersections == Counter({1: 270})
        ),
        "the_27_packet_lines_become_exact_5cocliques_in_transport": (
            all(len(line) == 5 for line in packet_lines) and packet_line_edge_counts == Counter({0: 27})
        ),
        "every_packet_transport_edge_has_a_unique_local_s3_packetline_matching": (
            local_matching["every_transport_edge_has_unique_matching"] is True
        ),
        "all_six_s3_permutations_occur_under_sorted_packet_labels": (
            local_matching["all_six_permutations_realized_under_sorted_packet_labels"] is True
        ),
    }
    theorem["the_witting_packet_layer_reconstructs_the_full_exact_45point_transport_graph"] = all(
        theorem.values()
    )

    return {
        "status": "ok",
        "transport_graph_dictionary": {
            "leaf_count": len(leaves),
            "graph_parameters": _srg_parameters(transport_graph),
            "intersection_profile_by_transport_adjacency": {
                "true": dict(sorted(edge_intersections.items())),
                "false": dict(sorted(nonedge_intersections.items())),
            },
        },
        "packet_transport_dictionary": {
            "packet_line_count": len(packet_lines),
            "packet_lines_per_leaf_distribution": dict(Counter(len(lines) for lines in leaf_packet_lines)),
            "transport_edges_inside_packet_line_distribution": dict(sorted(packet_line_edge_counts.items())),
            "sample_leaf_packet_lines": {
                str(index): list(lines) for index, lines in enumerate(leaf_packet_lines[:8])
            },
        },
        "transport_crosswalk": {
            "packet_transport_isomorphic_to_centerquad_transport": nx.is_isomorphic(
                transport_graph, quotient_transport_graph
            ),
            "packet_transport_vertices": transport_graph.number_of_nodes(),
            "packet_transport_edges": transport_graph.number_of_edges(),
            "centerquad_transport_vertices": quotient_transport_graph.number_of_nodes(),
            "centerquad_transport_edges": quotient_transport_graph.number_of_edges(),
        },
        "local_s3_packet_matching": local_matching,
        "packet_transport_theorem": theorem,
        "bridge_verdict": (
            "The Witting packet layer now reconstructs the exact 45-point transport graph as well as the "
            "45-point / 27-line quotient geometry. On the packet side alone, transport adjacency is "
            "exactly leaf disjointness, giving SRG(45,32,22,24), the 27 packet lines become exact "
            "5-cocliques, and every transport edge already carries a unique local S3 matching between "
            "the three packet lines through its endpoints. So the old transport package is no longer "
            "anchored only on the center-quad route: it is already present in the Witting communication "
            "layer itself."
        ),
    }


def main() -> int:
    timer = time.perf_counter()
    payload = analyze()
    output_dir = ROOT / "checks"
    output_dir.mkdir(exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"PART_CXXXIV_witting_packet_transport_complement_audit_{timestamp}.json"
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("W33 Witting packet transport-complement audit")
    for key, value in payload["packet_transport_theorem"].items():
        print(f"  [{'PASS' if value else 'FAIL'}] {key}")
    print(f"  Wrote: {output_path}")
    print(f"  Runtime: {time.perf_counter() - timer:.3f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
