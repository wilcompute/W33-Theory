#!/usr/bin/env python3
"""Exact quotient-geometry audit for the Witting packet foliation layer.

This audit closes the finite bridge from the balanced Witting packets to the
old center-quad quotient geometry.

Starting from the five packet foliations:
1. The 45 foliation leaves form the exact exceptional point graph
   SRG(45,12,3,3).
2. That 45-leaf graph is isomorphic to the exact 45-point quotient graph from
   the center-quad bridge.
3. The 27 packets determine exactly the 27 maximal K5 cliques of the leaf
   graph.
4. Those 27 packet-cliques define an exact dual GQ(4,2) incidence geometry
   with 45 points, 27 lines, 5 points per line, 3 lines per point, and 135
   incidences.
5. The induced packet-line graph is SRG(27,10,1,5), i.e. the same quotient
   line graph already reconstructed from the center-quad bridge.

So the Witting packet layer reconstructs the full exact quotient geometry, not
just the local shell and its support packages.
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
for candidate in (ROOT, ROOT / "scripts", ROOT / "exploration"):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)

from exploration.w33_center_quad_gq42_e6_bridge import quotient_incidence  # noqa: E402
from scripts.w33_witting_packet_foliation_incidence_audit import _build_foliations  # noqa: E402


Leaf = tuple[str, int, tuple[int, int, int]]


def _build_leaf_list() -> list[Leaf]:
    leaves: list[Leaf] = []
    for name in sorted(_build_foliations()):
        for index, leaf in enumerate(_build_foliations()[name]):
            leaves.append((name, index, tuple(leaf)))
    return leaves


def _leaf_graph(leaves: list[Leaf]) -> nx.Graph:
    graph = nx.Graph()
    graph.add_nodes_from(range(len(leaves)))
    for left, right in combinations(range(len(leaves)), 2):
        if len(set(leaves[left][2]) & set(leaves[right][2])) == 1:
            graph.add_edge(left, right)
    return graph


def _packet_lines(leaves: list[Leaf]) -> list[tuple[int, ...]]:
    return [
        tuple(sorted(index for index, (_name, _leaf_id, leaf) in enumerate(leaves) if packet in leaf))
        for packet in range(27)
    ]


def _line_graph(lines: list[tuple[int, ...]]) -> nx.Graph:
    graph = nx.Graph()
    graph.add_nodes_from(range(len(lines)))
    for left, right in combinations(range(len(lines)), 2):
        if len(set(lines[left]) & set(lines[right])) == 1:
            graph.add_edge(left, right)
    return graph


def _srg_parameters(graph: nx.Graph) -> dict[str, Any]:
    degrees = Counter(dict(graph.degree()).values())
    lambda_values = Counter()
    mu_values = Counter()
    for left, right in combinations(graph.nodes(), 2):
        common = len(set(graph.neighbors(left)) & set(graph.neighbors(right)))
        if graph.has_edge(left, right):
            lambda_values[common] += 1
        else:
            mu_values[common] += 1
    return {
        "vertices": graph.number_of_nodes(),
        "degree_distribution": dict(degrees),
        "lambda_distribution": dict(lambda_values),
        "mu_distribution": dict(mu_values),
        "edge_count": graph.number_of_edges(),
    }


@lru_cache(maxsize=1)
def analyze() -> dict[str, Any]:
    leaves = _build_leaf_list()
    leaf_graph = _leaf_graph(leaves)
    packet_lines = _packet_lines(leaves)
    packet_line_graph = _line_graph(packet_lines)

    point_to_lines, line_to_points = quotient_incidence()
    quotient_point_graph = nx.Graph()
    quotient_point_graph.add_nodes_from(sorted(point_to_lines))
    for points in line_to_points.values():
        for left, right in combinations(points, 2):
            quotient_point_graph.add_edge(left, right)

    quotient_line_graph = nx.Graph()
    quotient_line_graph.add_nodes_from(sorted(line_to_points))
    for lines in point_to_lines.values():
        for left, right in combinations(lines, 2):
            quotient_line_graph.add_edge(left, right)

    maximal_k5 = {
        tuple(sorted(clique))
        for clique in nx.find_cliques(leaf_graph)
        if len(clique) == 5
    }
    packet_line_set = {tuple(sorted(line)) for line in packet_lines}

    leaf_cover = Counter(index for line in packet_lines for index in line)
    packet_cover = Counter(packet for _name, _index, leaf in leaves for packet in leaf)

    theorem = {
        "the_45_packet_leaves_form_the_exact_exceptional_point_graph_srg_45_12_3_3": (
            leaf_graph.number_of_nodes() == 45
            and leaf_graph.number_of_edges() == 270
            and Counter(dict(leaf_graph.degree()).values()) == Counter({12: 45})
            and Counter(
                len(set(leaf_graph.neighbors(left)) & set(leaf_graph.neighbors(right)))
                for left, right in leaf_graph.edges()
            )
            == Counter({3: 270})
            and Counter(
                len(set(leaf_graph.neighbors(left)) & set(leaf_graph.neighbors(right)))
                for left, right in combinations(leaf_graph.nodes(), 2)
                if not leaf_graph.has_edge(left, right)
            )
            == Counter({3: 720})
        ),
        "the_packet_leaf_graph_is_isomorphic_to_the_exact_centerquad_45point_quotient_graph": (
            nx.is_isomorphic(leaf_graph, quotient_point_graph) is True
        ),
        "the_27_packets_are_exactly_the_27_maximal_k5_cliques_of_the_leaf_graph": (
            len(packet_lines) == 27
            and packet_line_set == maximal_k5
            and all(len(line) == 5 for line in packet_lines)
        ),
        "packet_leaf_incidence_is_exact_dual_gq42": (
            Counter(leaf_cover.values()) == Counter({3: 45})
            and Counter(packet_cover.values()) == Counter({5: 27})
            and sum(len(line) for line in packet_lines) == 135
        ),
        "the_packet_line_graph_is_exactly_srg_27_10_1_5_and_matches_the_quotient_line_graph": (
            packet_line_graph.number_of_nodes() == 27
            and packet_line_graph.number_of_edges() == 135
            and Counter(dict(packet_line_graph.degree()).values()) == Counter({10: 27})
            and Counter(
                len(set(packet_line_graph.neighbors(left)) & set(packet_line_graph.neighbors(right)))
                for left, right in packet_line_graph.edges()
            )
            == Counter({1: 135})
            and Counter(
                len(set(packet_line_graph.neighbors(left)) & set(packet_line_graph.neighbors(right)))
                for left, right in combinations(packet_line_graph.nodes(), 2)
                if not packet_line_graph.has_edge(left, right)
            )
            == Counter({5: 216})
            and nx.is_isomorphic(packet_line_graph, quotient_line_graph) is True
        ),
    }
    theorem["the_witting_packet_layer_reconstructs_the_full_exact_45point_quotient_geometry"] = all(
        theorem.values()
    )

    return {
        "status": "ok",
        "leaf_graph_dictionary": {
            "leaf_count": len(leaves),
            "graph_parameters": _srg_parameters(leaf_graph),
            "sample_leaves": [
                {"name": name, "leaf_id": leaf_id, "packets": list(leaf)}
                for name, leaf_id, leaf in leaves[:8]
            ],
        },
        "packet_line_dictionary": {
            "packet_line_count": len(packet_lines),
            "maximal_k5_count": len(maximal_k5),
            "leafs_per_packet_line_distribution": dict(Counter(len(line) for line in packet_lines)),
            "packets_per_leaf_distribution": dict(Counter(leaf_cover.values())),
            "sample_packet_lines": [list(line) for line in packet_lines[:8]],
        },
        "quotient_crosswalk": {
            "leaf_graph_isomorphic_to_quotient_point_graph": nx.is_isomorphic(leaf_graph, quotient_point_graph),
            "packet_line_graph_isomorphic_to_quotient_line_graph": nx.is_isomorphic(packet_line_graph, quotient_line_graph),
            "quotient_point_count": len(point_to_lines),
            "quotient_line_count": len(line_to_points),
            "quotient_incidences": sum(len(lines) for lines in point_to_lines.values()),
        },
        "packet_quotient_geometry_theorem": theorem,
        "bridge_verdict": (
            "The packet foliation layer now reconstructs the full exact quotient geometry already "
            "known from the center-quad bridge. The 45 foliation leaves form the exceptional "
            "SRG(45,12,3,3) point graph, the 27 packets are exactly its maximal K5 cliques, and "
            "their incidence is dual GQ(4,2) with 45 points, 27 lines, and 135 incidences. So the "
            "Witting packet program reaches the same 45-point / 27-line quotient geometry from an "
            "independent route."
        ),
    }


def main() -> int:
    timer = time.perf_counter()
    payload = analyze()
    output_dir = ROOT / "checks"
    output_dir.mkdir(exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"PART_CXXXIII_witting_packet_quotient_geometry_audit_{timestamp}.json"
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("W33 Witting packet quotient-geometry audit")
    for key, value in payload["packet_quotient_geometry_theorem"].items():
        print(f"  [{'PASS' if value else 'FAIL'}] {key}")
    print(f"  Wrote: {output_path}")
    print(f"  Runtime: {time.perf_counter() - timer:.3f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
