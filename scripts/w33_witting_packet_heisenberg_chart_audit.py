#!/usr/bin/env python3
"""Exact Heisenberg-chart audit for the balanced Witting packet shell.

This audit sharpens the balanced-packet bridge from the 36-deck communication
layer to the local H27 shell.

Exact content:
1. The 27 balanced packets split canonically into 9 fibers of size 3, indexed
   by the first two sector-triangle labels (a,b) in F_3^2.
2. The remaining two sector-triangle labels are forced affinely:
      c = 1 - a + b,   d = 2 + a + b  (mod 3).
   So the allowed 4-sector triangle patterns form an affine plane inside F_3^4.
3. In the balanced shell graph there are no edges within a fiber, and between
   any two distinct fibers there are exactly 3 edges, i.e. a perfect matching
   of the 3-state fibers.
4. There exists a fiber-preserving graph isomorphism from this packet shell to
   the canonical local H27 shell coming from the repo's Heisenberg chart.

So the balanced packet layer carries an exact F_3^2 x F_3 chart of its own and
recovers the local Heisenberg/fiber decomposition, not just the abstract shell.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from functools import lru_cache
from itertools import combinations, product
import json
from pathlib import Path
import sys
import time
from typing import Any

import networkx as nx
import numpy as np
from networkx.algorithms import isomorphism as iso


ROOT = Path(__file__).resolve().parents[1]
for candidate in (ROOT, ROOT / "scripts", ROOT / "exploration"):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)

from exploration.w33_witting_srg_bridge import symplectic_lines  # noqa: E402
from scripts.w33_heisenberg_qutrit import build_f3_cube, compute_local_structure  # noqa: E402
from scripts.w33_homology import build_w33  # noqa: E402
from scripts.w33_symplectic_spread_frame_audit import symplectic_spreads  # noqa: E402


Packet = tuple[int, ...]


def _build_balanced_packet_rows() -> list[dict[str, Any]]:
    lines = list(symplectic_lines())
    decks = symplectic_spreads(lines, n_points=40)
    anchor_line_indices = [index for index, line in enumerate(lines) if 0 in line]

    incidence = np.zeros((40, 36), dtype=int)
    for deck_index, deck in enumerate(decks):
        for line_index in deck:
            incidence[line_index, deck_index] = 1
    overlaps = incidence.T @ incidence

    sectors = {
        sector_index: [deck_index for deck_index, deck in enumerate(decks) if anchor_line_index in deck]
        for sector_index, anchor_line_index in enumerate(anchor_line_indices)
    }

    sector_triangles: dict[int, list[tuple[int, ...]]] = {}
    for sector_index, deck_indices in sectors.items():
        graph = nx.Graph()
        graph.add_nodes_from(deck_indices)
        for left, right in combinations(deck_indices, 2):
            if int(overlaps[left, right]) == 1:
                graph.add_edge(left, right)
        sector_triangles[sector_index] = [
            tuple(sorted(component)) for component in nx.connected_components(graph)
        ]
        sector_triangles[sector_index].sort()

    triangle_lookup = {
        sector_index: {
            deck_index: triangle_index
            for triangle_index, triangle in enumerate(sector_triangles[sector_index])
            for deck_index in triangle
        }
        for sector_index in sectors
    }

    overlap4_graph = nx.Graph()
    overlap4_graph.add_nodes_from(range(36))
    for left, right in combinations(range(36), 2):
        if int(overlaps[left, right]) == 4:
            overlap4_graph.add_edge(left, right)

    rows: list[dict[str, Any]] = []
    for packet in combinations(range(36), 4):
        if not all(overlap4_graph.has_edge(left, right) for left, right in combinations(packet, 2)):
            continue
        by_sector = {}
        for deck_index in packet:
            sector_index = next(index for index, deck_indices in sectors.items() if deck_index in deck_indices)
            by_sector[sector_index] = deck_index
        if len(by_sector) != 4:
            continue

        triangle_pattern = tuple(
            triangle_lookup[sector_index][by_sector[sector_index]] for sector_index in range(4)
        )
        local_position_pattern = tuple(
            sector_triangles[sector_index][triangle_pattern[sector_index]].index(by_sector[sector_index])
            for sector_index in range(4)
        )
        rows.append(
            {
                "packet": tuple(sorted(packet)),
                "fiber_xy": (triangle_pattern[0], triangle_pattern[1]),
                "triangle_pattern": triangle_pattern,
                "local_position_pattern": local_position_pattern,
            }
        )
    return rows


def _build_balanced_shell_graph(rows: list[dict[str, Any]]) -> nx.Graph:
    graph = nx.Graph()
    graph.add_nodes_from(range(len(rows)))
    for left, right in combinations(range(len(rows)), 2):
        if len(set(rows[left]["packet"]) & set(rows[right]["packet"])) == 1:
            graph.add_edge(left, right)
    return graph


def _local_h27_shell_graph() -> tuple[nx.Graph, dict[tuple[int, int], list[int]], dict[int, tuple[int, int, int]]]:
    n_vertices, _vertices, adjacency, _edges = build_w33()
    adjacency_sets = [set(row) for row in adjacency]
    neighbors, nonneighbors, triangles, _h27_neighbors = compute_local_structure(
        0, n_vertices, adjacency_sets
    )
    fibers, vertex_to_xyz = build_f3_cube(neighbors, nonneighbors, triangles, adjacency_sets)

    graph = nx.Graph()
    index = {vertex: offset for offset, vertex in enumerate(nonneighbors)}
    for vertex in nonneighbors:
        graph.add_node(index[vertex], fiber=str(vertex_to_xyz[vertex][:2]))
    for left, vertex_left in enumerate(nonneighbors):
        for right, vertex_right in enumerate(nonneighbors[left + 1 :], start=left + 1):
            if vertex_right in adjacency_sets[vertex_left]:
                graph.add_edge(left, right)

    fiber_indices = {
        xy: [index[vertex] for vertex in fiber_vertices] for xy, fiber_vertices in fibers.items()
    }
    indexed_xyz = {index[vertex]: vertex_to_xyz[vertex] for vertex in nonneighbors}
    return graph, fiber_indices, indexed_xyz


@lru_cache(maxsize=1)
def analyze() -> dict[str, Any]:
    rows = _build_balanced_packet_rows()
    shell = _build_balanced_shell_graph(rows)

    fiber_to_nodes: dict[tuple[int, int], list[int]] = defaultdict(list)
    for node_index, row in enumerate(rows):
        fiber_to_nodes[row["fiber_xy"]].append(node_index)

    fiber_sizes = Counter(len(nodes) for nodes in fiber_to_nodes.values())
    triangle_patterns = Counter(row["triangle_pattern"] for row in rows)

    affine_pattern_failures = []
    for row in rows:
        a, b, c, d = row["triangle_pattern"]
        if c != (1 - a + b) % 3 or d != (2 + a + b) % 3:
            affine_pattern_failures.append(row["triangle_pattern"])

    within_fiber_edges = Counter()
    between_fiber_edge_counts = Counter()
    fibers = sorted(fiber_to_nodes)
    for fiber in fibers:
        nodes = fiber_to_nodes[fiber]
        for left, right in combinations(nodes, 2):
            within_fiber_edges[shell.has_edge(left, right)] += 1
    for left_fiber, right_fiber in combinations(fibers, 2):
        left_nodes = fiber_to_nodes[left_fiber]
        right_nodes = fiber_to_nodes[right_fiber]
        count = sum(1 for left in left_nodes for right in right_nodes if shell.has_edge(left, right))
        between_fiber_edge_counts[count] += 1

    local_shell, local_fibers, local_xyz = _local_h27_shell_graph()

    balanced_colored = nx.Graph()
    balanced_colored.add_nodes_from(
        (node, {"fiber": str(rows[node]["fiber_xy"])}) for node in shell.nodes()
    )
    balanced_colored.add_edges_from(shell.edges())

    matcher = iso.GraphMatcher(
        balanced_colored,
        local_shell,
        node_match=lambda left, right: left["fiber"] == right["fiber"],
    )
    isomorphic = matcher.is_isomorphic()
    mapping = matcher.mapping if isomorphic else {}

    theorem = {
        "the_27_balanced_packets_split_canonically_as_9_fibers_of_size_3": (
            len(rows) == 27
            and fiber_sizes == Counter({3: 9})
        ),
        "the_allowed_sector_triangle_patterns_form_an_affine_plane_in_f3_4": (
            len(triangle_patterns) == 9
            and Counter(triangle_patterns.values()) == Counter({3: 9})
            and not affine_pattern_failures
        ),
        "the_balanced_shell_has_no_edges_within_a_fiber_and_exactly_3_between_any_two_fibers": (
            within_fiber_edges == Counter({False: 27})
            and between_fiber_edge_counts == Counter({3: 36})
        ),
        "the_balanced_shell_is_fiber_preserving_isomorphic_to_the_canonical_local_h27_shell": (
            isomorphic is True
            and len(mapping) == 27
        ),
    }
    theorem["the_balanced_packet_layer_carries_an_exact_f3_squared_times_f3_chart"] = all(
        theorem.values()
    )

    sample_mapping = {}
    if isomorphic:
        for balanced_node in sorted(mapping)[:9]:
            sample_mapping[str(balanced_node)] = {
                "fiber_xy": rows[balanced_node]["fiber_xy"],
                "packet": rows[balanced_node]["packet"],
                "local_h27_index": mapping[balanced_node],
                "local_xyz": local_xyz[mapping[balanced_node]],
            }

    return {
        "status": "ok",
        "fiber_dictionary": {
            "fiber_count": len(fiber_to_nodes),
            "fiber_size_distribution": dict(fiber_sizes),
            "fiber_keys": [tuple(key) for key in fibers],
        },
        "affine_triangle_plane": {
            "triangle_pattern_count": len(triangle_patterns),
            "triangle_pattern_multiplicity_distribution": dict(Counter(triangle_patterns.values())),
            "exact_triangle_pattern_equations": {
                "c": "1 - a + b mod 3",
                "d": "2 + a + b mod 3",
            },
            "affine_pattern_failures": [tuple(pattern) for pattern in affine_pattern_failures[:10]],
        },
        "fiber_adjacency_dictionary": {
            "within_fiber_edge_distribution": dict(within_fiber_edges),
            "between_fiber_edge_count_distribution": dict(between_fiber_edge_counts),
        },
        "fiber_preserving_isomorphism": {
            "exists": isomorphic,
            "sample_mapping": sample_mapping,
        },
        "packet_heisenberg_chart_theorem": theorem,
        "bridge_verdict": (
            "The 27 balanced packets now carry an explicit Heisenberg-style chart. They split "
            "canonically into 9 fibers of size 3 indexed by F_3^2, the four-sector triangle "
            "patterns lie on an affine plane inside F_3^4, the balanced shell has no intra-fiber "
            "edges and exactly three inter-fiber edges for every fiber pair, and there is a "
            "fiber-preserving graph isomorphism to the canonical local H27 shell. So the Witting "
            "packet layer recovers the repo's local F_3^2 x F_3 chart, not just the abstract 27-node shell."
        ),
    }


def main() -> None:
    started = time.time()
    payload = analyze()
    payload["analysis_duration_sec"] = round(time.time() - started, 6)

    output_dir = ROOT / "checks"
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"PART_CXXIX_witting_packet_heisenberg_chart_audit_{timestamp}.json"
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("W33 Witting packet Heisenberg-chart audit")
    for key, value in payload["packet_heisenberg_chart_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")
    print(f"  Wrote: {output_path}")


if __name__ == "__main__":
    main()
