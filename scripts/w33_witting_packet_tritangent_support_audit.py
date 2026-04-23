#!/usr/bin/env python3
"""Exact tritangent-support audit for the balanced Witting packet layer.

This audit closes the next exact bridge behind the original Witting
communication picture.

Starting from the 27 balanced four-deck packets:
1. The shell graph on those packets carries exactly 36 graph triangles.
2. Together with the 9 packet fibers from the Heisenberg chart, these give
   exactly 45 support triples:
      45 = 36 shell triangles + 9 fiber triples.
3. Every balanced packet lies on exactly 5 such triples.
4. The rank-intersection-16 graph on the same 27 packets has exactly those
   same 45 triangles and no others.
5. Under a fiber-preserving shell isomorphism, this 45-triple package
   transports to the canonical local H27 support package already isolated by
   the Albert-shadow audit.

So the Witting communication layer reconstructs not only the local shell and
its Heisenberg chart, but the full exact local 45-tritangent support package.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from itertools import combinations
import json
from pathlib import Path
import sys
import time
from typing import Any, Iterable

import networkx as nx
from networkx.algorithms import isomorphism as iso


ROOT = Path(__file__).resolve().parents[1]
for candidate in (ROOT, ROOT / "scripts", ROOT / "exploration"):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)

from exploration.w33_witting_srg_bridge import symplectic_lines  # noqa: E402
from scripts.w33_symplectic_spread_frame_audit import symplectic_spreads  # noqa: E402
from scripts.w33_witting_packet_heisenberg_chart_audit import (  # noqa: E402
    _build_balanced_packet_rows,
    _build_balanced_shell_graph,
    _local_h27_shell_graph,
)


Triple = tuple[int, int, int]


def _norm_triple(nodes: Iterable[int]) -> Triple:
    a, b, c = sorted(int(node) for node in nodes)
    return (a, b, c)


def _triangle_cliques(graph: nx.Graph) -> set[Triple]:
    triangles: set[Triple] = set()
    for left, middle, right in combinations(graph.nodes(), 3):
        if (
            graph.has_edge(left, middle)
            and graph.has_edge(left, right)
            and graph.has_edge(middle, right)
        ):
            triangles.add(_norm_triple((left, middle, right)))
    return triangles


def _fiber_triples(rows: list[dict[str, Any]]) -> set[Triple]:
    by_fiber: dict[tuple[int, int], list[int]] = {}
    for node_index, row in enumerate(rows):
        by_fiber.setdefault(tuple(row["fiber_xy"]), []).append(node_index)
    return {_norm_triple(nodes) for nodes in by_fiber.values()}


def _packet_rank_unions(rows: list[dict[str, Any]]) -> list[set[int]]:
    decks = symplectic_spreads(list(symplectic_lines()), n_points=40)
    return [{rank for deck_index in row["packet"] for rank in decks[deck_index]} for row in rows]


def _rank_intersection_graph(rank_unions: list[set[int]], intersection_size: int) -> nx.Graph:
    graph = nx.Graph()
    graph.add_nodes_from(range(len(rank_unions)))
    for left, right in combinations(range(len(rank_unions)), 2):
        if len(rank_unions[left] & rank_unions[right]) == intersection_size:
            graph.add_edge(left, right)
    return graph


def _fiber_preserving_mapping(
    rows: list[dict[str, Any]],
    shell: nx.Graph,
) -> tuple[bool, dict[int, int], nx.Graph, dict[tuple[int, int], list[int]]]:
    local_shell, local_fibers, _local_xyz = _local_h27_shell_graph()

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
    return isomorphic, mapping, local_shell, local_fibers


@lru_cache(maxsize=1)
def analyze() -> dict[str, Any]:
    rows = _build_balanced_packet_rows()
    shell = _build_balanced_shell_graph(rows)
    shell_triangles = _triangle_cliques(shell)
    fibers = _fiber_triples(rows)
    support = shell_triangles | fibers

    rank16_graph = _rank_intersection_graph(_packet_rank_unions(rows), intersection_size=16)
    rank16_triangles = _triangle_cliques(rank16_graph)

    packet_incidence = Counter(node for triple in support for node in triple)

    isomorphic, mapping, local_shell, local_fibers = _fiber_preserving_mapping(rows, shell)
    local_shell_triangles = _triangle_cliques(local_shell)
    local_fiber_triples = {_norm_triple(nodes) for nodes in local_fibers.values()}
    local_support = local_shell_triangles | local_fiber_triples
    local_support_incidence = Counter(node for triple in local_support for node in triple)

    transported_support = (
        {_norm_triple(mapping[node] for node in triple) for triple in support}
        if isomorphic
        else set()
    )
    transported_shell_triangles = (
        {_norm_triple(mapping[node] for node in triple) for triple in shell_triangles}
        if isomorphic
        else set()
    )
    transported_fibers = (
        {_norm_triple(mapping[node] for node in triple) for triple in fibers}
        if isomorphic
        else set()
    )

    theorem = {
        "the_27_balanced_packets_carry_exactly_36_shell_triangles_plus_9_fiber_triples": (
            len(rows) == 27
            and len(shell_triangles) == 36
            and len(fibers) == 9
            and len(support) == 45
        ),
        "the_rank_intersection_16_graph_has_exactly_the_same_45_support_triples": (
            len(rank16_triangles) == 45
            and rank16_triangles == support
        ),
        "each_balanced_packet_lies_on_exactly_five_support_triples": (
            len(set(packet_incidence.values())) == 1
            and next(iter(set(packet_incidence.values()))) == 5
        ),
        "the_packet_support_transports_fiber_preservingly_to_the_canonical_local_h27_support_package": (
            isomorphic is True
            and transported_support == local_support
            and transported_shell_triangles == local_shell_triangles
            and transported_fibers == local_fiber_triples
        ),
        "the_balanced_packet_support_matches_the_canonical_local_45_support_package": (
            len(local_support) == 45
            and len(local_shell_triangles) == 36
            and len(local_fiber_triples) == 9
            and len(set(local_support_incidence.values())) == 1
            and next(iter(set(local_support_incidence.values()))) == 5
            and next(iter(set(packet_incidence.values()))) == 5
        ),
    }
    theorem["the_witting_communication_layer_reconstructs_the_exact_local_albert_shadow_support"] = all(
        theorem.values()
    )

    sample_mapping = {}
    if isomorphic:
        for balanced_node in sorted(mapping)[:9]:
            sample_mapping[str(balanced_node)] = {
                "fiber_xy": rows[balanced_node]["fiber_xy"],
                "packet": rows[balanced_node]["packet"],
                "local_h27_index": mapping[balanced_node],
            }

    return {
        "status": "ok",
        "balanced_packet_support_dictionary": {
            "packet_count": len(rows),
            "shell_triangle_count": len(shell_triangles),
            "fiber_triple_count": len(fibers),
            "support_total": len(support),
            "packet_support_incidence_distribution": dict(Counter(packet_incidence.values())),
            "sample_shell_triangles": [tuple(triple) for triple in sorted(shell_triangles)[:6]],
            "sample_fiber_triples": [tuple(triple) for triple in sorted(fibers)[:6]],
        },
        "rank16_support_dictionary": {
            "rank16_edge_count": rank16_graph.number_of_edges(),
            "rank16_triangle_count": len(rank16_triangles),
            "rank16_triangles_equal_support": rank16_triangles == support,
        },
        "local_support_crosswalk": {
            "transport_isomorphism_exists": isomorphic,
            "transported_support_matches_local_support": transported_support == local_support,
            "transported_shell_triangles_match_local_affine_support": (
                transported_shell_triangles == local_shell_triangles
            ),
            "transported_fibers_match_local_fiber_support": transported_fibers == local_fiber_triples,
            "local_support_total": len(local_support),
            "local_shell_triangle_count": len(local_shell_triangles),
            "local_fiber_triple_count": len(local_fiber_triples),
            "local_support_incidence_distribution": dict(Counter(local_support_incidence.values())),
            "canonical_local_support_counts": {
                "support_total": 45,
                "shell_triangle_count": 36,
                "fiber_triple_count": 9,
                "point_support_incidence": 5,
            },
            "sample_mapping": sample_mapping,
        },
        "packet_tritangent_support_theorem": theorem,
        "bridge_verdict": (
            "The Witting packet layer now reaches the exact local determinant-support package, "
            "not just the local shell. On the 27 balanced packets the 36 shell triangles plus "
            "9 fibers give the full 45-triple support package, every packet lies on exactly 5 "
            "support triples, the rank-intersection-16 graph has exactly those same 45 triangles, "
            "and a fiber-preserving shell isomorphism transports the whole package to the "
            "canonical local H27 tritangent support certified by the Albert-shadow audit."
        ),
    }


def main() -> int:
    timer = time.perf_counter()
    payload = analyze()
    output_dir = ROOT / "checks"
    output_dir.mkdir(exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"PART_CXXX_witting_packet_tritangent_support_audit_{timestamp}.json"
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("W33 Witting packet tritangent-support audit")
    for key, value in payload["packet_tritangent_support_theorem"].items():
        print(f"  [{'PASS' if value else 'FAIL'}] {key}")
    print(f"  Wrote: {output_path}")
    print(f"  Runtime: {time.perf_counter() - timer:.3f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
