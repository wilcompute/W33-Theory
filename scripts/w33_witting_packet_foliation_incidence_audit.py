#!/usr/bin/env python3
"""Exact foliation-incidence audit for the balanced Witting packet layer.

This audit packages the next exact layer behind the packet Hessian split.

On the 27 balanced packets there are five canonical 9-triple foliations:
  - 1 fiber foliation,
  - 4 affine-direction foliations.

The exact pairwise leaf-incidence laws are:
1. Every foliation partitions the 27 packets into 9 disjoint triples.
2. For every fiber/affine pair, the 9-by-9 leaf-intersection graph is exactly
   3 K_{3,3}.
3. For every affine/affine pair, the 9-by-9 leaf-intersection graph is exactly
   the Pappus graph.

So the Witting packet layer carries a canonical five-foliation incidence
architecture with classical Pappus control on the affine side.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from functools import lru_cache
from itertools import combinations
import json
from pathlib import Path
import sys
import time
from typing import Any

import networkx as nx
from networkx.algorithms import isomorphism as iso


ROOT = Path(__file__).resolve().parents[1]
for candidate in (ROOT, ROOT / "scripts", ROOT / "exploration"):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)

from scripts.e6_hessian_tritangents import _u_line_direction  # noqa: E402
from scripts.w33_witting_packet_heisenberg_chart_audit import (  # noqa: E402
    _build_balanced_packet_rows,
    _build_balanced_shell_graph,
    _local_h27_shell_graph,
)


Triple = tuple[int, int, int]
FoliationName = str


def _norm_triple(nodes) -> Triple:
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


def _fiber_preserving_mapping(
    rows: list[dict[str, Any]],
    shell: nx.Graph,
) -> tuple[bool, dict[int, int], dict[int, tuple[int, int, int]]]:
    local_shell, _local_fibers, local_xyz = _local_h27_shell_graph()

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
    return isomorphic, mapping, local_xyz


def _build_foliations() -> dict[FoliationName, list[Triple]]:
    rows = _build_balanced_packet_rows()
    shell = _build_balanced_shell_graph(rows)
    isomorphic, mapping, local_xyz = _fiber_preserving_mapping(rows, shell)
    if not isomorphic:
        raise ValueError("expected fiber-preserving shell isomorphism")

    foliations: dict[FoliationName, list[Triple]] = {}

    by_fiber: dict[tuple[int, int], list[int]] = defaultdict(list)
    for node_index, row in enumerate(rows):
        by_fiber[tuple(row["fiber_xy"])].append(node_index)
    foliations["fiber"] = [_norm_triple(nodes) for _, nodes in sorted(by_fiber.items())]

    by_direction: dict[tuple[int, int], list[Triple]] = defaultdict(list)
    for triangle in sorted(_triangle_cliques(shell)):
        xyz = tuple(sorted(local_xyz[mapping[node]] for node in triangle))
        u_line = tuple(sorted({(x, y) for x, y, _z in xyz}))
        by_direction[_u_line_direction(u_line)].append(triangle)
    for direction, triangles in sorted(by_direction.items()):
        foliations[f"dir_{direction[0]}_{direction[1]}"] = sorted(triangles)

    return foliations


def _leaf_intersection_graph(left: list[Triple], right: list[Triple]) -> nx.Graph:
    graph = nx.Graph()
    left_nodes = [("L", index) for index in range(len(left))]
    right_nodes = [("R", index) for index in range(len(right))]
    graph.add_nodes_from(left_nodes, bipartite=0)
    graph.add_nodes_from(right_nodes, bipartite=1)

    for left_index, left_leaf in enumerate(left):
        for right_index, right_leaf in enumerate(right):
            if len(set(left_leaf) & set(right_leaf)) == 1:
                graph.add_edge(("L", left_index), ("R", right_index))
    return graph


@lru_cache(maxsize=1)
def analyze() -> dict[str, Any]:
    foliations = _build_foliations()
    foliation_cover = {}
    for name, leaves in foliations.items():
        cover = Counter(node for leaf in leaves for node in leaf)
        foliation_cover[name] = {
            "leaf_count": len(leaves),
            "leaf_size_distribution": dict(Counter(len(leaf) for leaf in leaves)),
            "packet_cover_distribution": dict(Counter(cover.values())),
        }

    expected_fiber_affine = nx.disjoint_union_all(
        [nx.complete_bipartite_graph(3, 3) for _ in range(3)]
    )
    expected_pappus = nx.pappus_graph()

    pair_records = []
    theorem_fiber_affine = True
    theorem_affine_affine = True

    for left_name, right_name in combinations(sorted(foliations), 2):
        graph = _leaf_intersection_graph(foliations[left_name], foliations[right_name])
        degrees = Counter(dict(graph.degree()).values())
        components = sorted(len(component) for component in nx.connected_components(graph))
        edge_count = graph.number_of_edges()

        is_fiber_affine = (left_name == "fiber") ^ (right_name == "fiber")
        is_affine_affine = left_name != "fiber" and right_name != "fiber"

        fiber_affine_match = False
        affine_affine_match = False

        if is_fiber_affine:
            fiber_affine_match = nx.is_isomorphic(graph, expected_fiber_affine)
            theorem_fiber_affine &= fiber_affine_match
        if is_affine_affine:
            affine_affine_match = nx.is_isomorphic(graph, expected_pappus)
            theorem_affine_affine &= affine_affine_match

        pair_records.append(
            {
                "left": left_name,
                "right": right_name,
                "edge_count": edge_count,
                "degree_distribution": dict(degrees),
                "component_sizes": components,
                "fiber_affine_match_3k33": fiber_affine_match,
                "affine_affine_match_pappus": affine_affine_match,
            }
        )

    theorem = {
        "the_balanced_packet_layer_has_exactly_five_canonical_9triple_foliations": (
            len(foliations) == 5
            and all(record["leaf_count"] == 9 for record in foliation_cover.values())
            and all(record["leaf_size_distribution"] == {3: 9} for record in foliation_cover.values())
            and all(record["packet_cover_distribution"] == {1: 27} for record in foliation_cover.values())
        ),
        "every_fiber_affine_leaf_intersection_graph_is_exactly_3k33": theorem_fiber_affine,
        "every_affine_affine_leaf_intersection_graph_is_exactly_the_pappus_graph": theorem_affine_affine,
        "every_pair_of_distinct_foliations_has_the_uniform_27edge_singleton_intersection_law": (
            all(record["edge_count"] == 27 for record in pair_records)
            and all(record["degree_distribution"] == {3: 18} for record in pair_records)
        ),
    }
    theorem["the_witting_packet_layer_carries_a_canonical_fivefoliation_pappus_architecture"] = all(
        theorem.values()
    )

    return {
        "status": "ok",
        "foliation_dictionary": {
            "foliation_names": sorted(foliations),
            "foliation_records": foliation_cover,
        },
        "pair_incidence_dictionary": {
            "pair_count": len(pair_records),
            "fiber_affine_pair_count": sum(
                1
                for record in pair_records
                if (record["left"] == "fiber") ^ (record["right"] == "fiber")
            ),
            "affine_affine_pair_count": sum(
                1
                for record in pair_records
                if record["left"] != "fiber" and record["right"] != "fiber"
            ),
            "pair_records": pair_records,
        },
        "packet_foliation_incidence_theorem": theorem,
        "bridge_verdict": (
            "The packet Hessian split hides a stronger exact control geometry. The 27 balanced "
            "packets carry five canonical foliations by triples: one fiber foliation and four "
            "affine-direction foliations. Every fiber/affine leaf-incidence graph is exactly "
            "3K_{3,3}, every affine/affine leaf-incidence graph is exactly the Pappus graph, "
            "and every distinct foliation pair has the same 27-edge singleton-intersection law. "
            "So the Witting packet layer carries a canonical five-foliation Pappus architecture."
        ),
    }


def main() -> int:
    timer = time.perf_counter()
    payload = analyze()
    output_dir = ROOT / "checks"
    output_dir.mkdir(exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"PART_CXXXII_witting_packet_foliation_incidence_audit_{timestamp}.json"
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("W33 Witting packet foliation-incidence audit")
    for key, value in payload["packet_foliation_incidence_theorem"].items():
        print(f"  [{'PASS' if value else 'FAIL'}] {key}")
    print(f"  Wrote: {output_path}")
    print(f"  Runtime: {time.perf_counter() - timer:.3f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
