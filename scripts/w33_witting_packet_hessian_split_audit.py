#!/usr/bin/env python3
"""Exact Hessian split audit for the balanced Witting packet layer.

This audit refines the packet tritangent-support bridge to the full local
Hessian decomposition.

Starting from the 27 balanced Witting packets:
1. The 36 shell triangles project to exactly the 12 affine lines of AG(2,3).
2. Each affine line supports exactly 3 packet triangles, partitioning the 9
   packet positions above that line.
3. Those 12 lines split into 4 direction classes of 3 parallel lines, and
   each direction class supports exactly 9 packet triangles.
4. Every balanced packet lies on exactly one affine lift in each direction
   class, together with its unique fiber triple.

So the Witting communication layer reconstructs the full exact local Hessian
split:

    45 = 9 fibers + 36 affine lifts = 9 + 12 x 3.
"""

from __future__ import annotations

from collections import Counter, defaultdict
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

from scripts.e6_hessian_tritangents import _all_ag23_lines, _u_line_direction  # noqa: E402
from scripts.w33_witting_packet_heisenberg_chart_audit import (  # noqa: E402
    _build_balanced_packet_rows,
    _build_balanced_shell_graph,
    _local_h27_shell_graph,
)


Triple = tuple[int, int, int]
ULine = tuple[tuple[int, int], tuple[int, int], tuple[int, int]]
Direction = tuple[int, int]


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
    by_fiber: dict[tuple[int, int], list[int]] = defaultdict(list)
    for node_index, row in enumerate(rows):
        by_fiber[tuple(row["fiber_xy"])].append(node_index)
    return {_norm_triple(nodes) for nodes in by_fiber.values()}


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


@lru_cache(maxsize=1)
def analyze() -> dict[str, Any]:
    rows = _build_balanced_packet_rows()
    shell = _build_balanced_shell_graph(rows)
    shell_triangles = _triangle_cliques(shell)
    fibers = _fiber_triples(rows)

    isomorphic, mapping, local_xyz = _fiber_preserving_mapping(rows, shell)

    line_to_triangles: dict[ULine, list[Triple]] = defaultdict(list)
    line_to_xyz: dict[ULine, list[tuple[tuple[int, int, int], ...]]] = defaultdict(list)
    node_to_directions: dict[int, list[Direction]] = defaultdict(list)

    for triangle in sorted(shell_triangles):
        xyz = tuple(sorted(local_xyz[mapping[node]] for node in triangle))
        u_line = tuple(sorted({(x, y) for x, y, _z in xyz}))
        direction = _u_line_direction(u_line)
        line_to_triangles[u_line].append(triangle)
        line_to_xyz[u_line].append(xyz)
        for node in triangle:
            node_to_directions[node].append(direction)

    ag23_lines = set(_all_ag23_lines())
    lifted_lines = set(line_to_triangles)

    line_multiplicities = Counter(len(triangles) for triangles in line_to_triangles.values())
    line_partition_failures = []
    for u_line, xyz_triples in line_to_xyz.items():
        covered = {point for tri in xyz_triples for point in tri}
        expected = {(u[0], u[1], z) for u in u_line for z in (0, 1, 2)}
        if covered != expected:
            line_partition_failures.append(
                {
                    "u_line": [list(u) for u in u_line],
                    "covered_size": len(covered),
                    "expected_size": len(expected),
                }
            )

    direction_to_lines: dict[Direction, list[ULine]] = defaultdict(list)
    direction_to_triangle_count = Counter()
    for u_line in sorted(line_to_triangles):
        direction = _u_line_direction(u_line)
        direction_to_lines[direction].append(u_line)
        direction_to_triangle_count[direction] += len(line_to_triangles[u_line])

    per_node_direction_sets = Counter(tuple(sorted(set(directions))) for directions in node_to_directions.values())
    per_node_direction_multisets = Counter(
        tuple(sorted(Counter(directions).items())) for directions in node_to_directions.values()
    )
    affine_incidence = Counter(node for triangle in shell_triangles for node in triangle)
    fiber_incidence = Counter(node for triangle in fibers for node in triangle)

    theorem = {
        "the_36_packet_shell_triangles_project_to_exactly_the_12_affine_lines_of_ag23": (
            isomorphic is True
            and len(shell_triangles) == 36
            and lifted_lines == ag23_lines
            and len(lifted_lines) == 12
        ),
        "each_affine_line_supports_exactly_3_packet_triangles_partitioning_its_9_points": (
            line_multiplicities == Counter({3: 12})
            and not line_partition_failures
        ),
        "the_12_affine_lines_split_into_4_direction_classes_of_3_lines_each": (
            len(direction_to_lines) == 4
            and Counter(len(lines) for lines in direction_to_lines.values()) == Counter({3: 4})
            and direction_to_triangle_count == Counter({direction: 9 for direction in direction_to_lines})
        ),
        "each_balanced_packet_lies_on_exactly_one_affine_lift_in_each_direction_plus_its_unique_fiber": (
            Counter(affine_incidence.values()) == Counter({4: 27})
            and Counter(fiber_incidence.values()) == Counter({1: 27})
            and per_node_direction_sets == Counter({((0, 1), (1, 0), (1, 1), (1, 2)): 27})
            and per_node_direction_multisets
            == Counter({(((0, 1), 1), ((1, 0), 1), ((1, 1), 1), ((1, 2), 1)): 27})
        ),
        "the_balanced_packet_layer_realizes_the_full_hessian_split_9_plus_12_times_3": (
            len(fibers) == 9
            and len(shell_triangles) == 36
            and len(fibers | shell_triangles) == 45
        ),
    }
    theorem["the_witting_packet_layer_reconstructs_the_exact_local_hessian_split"] = all(
        theorem.values()
    )

    return {
        "status": "ok",
        "affine_line_dictionary": {
            "affine_packet_triangle_count": len(shell_triangles),
            "ag23_line_count": len(ag23_lines),
            "packet_projected_lines_equal_ag23_lines": lifted_lines == ag23_lines,
            "packet_lifts_per_line_distribution": dict(line_multiplicities),
            "line_partition_failures": line_partition_failures[:10],
            "sample_u_lines": [[list(point) for point in u_line] for u_line in sorted(line_to_triangles)[:6]],
        },
        "direction_dictionary": {
            "direction_count": len(direction_to_lines),
            "lines_per_direction_distribution": dict(Counter(len(lines) for lines in direction_to_lines.values())),
            "triangles_per_direction": {str(direction): int(count) for direction, count in sorted(direction_to_triangle_count.items())},
            "direction_classes": {
                str(direction): [[[x, y] for (x, y) in u_line] for u_line in sorted(lines)]
                for direction, lines in sorted(direction_to_lines.items())
            },
        },
        "packet_incidence_dictionary": {
            "affine_incidence_distribution": dict(Counter(affine_incidence.values())),
            "fiber_incidence_distribution": dict(Counter(fiber_incidence.values())),
            "direction_set_distribution": {str(key): count for key, count in per_node_direction_sets.items()},
            "direction_multiset_distribution": {str(key): count for key, count in per_node_direction_multisets.items()},
        },
        "hessian_split_dictionary": {
            "fiber_triple_count": len(fibers),
            "affine_triple_count": len(shell_triangles),
            "support_total": len(fibers | shell_triangles),
            "sample_line_lifts": {
                str([[x, y] for (x, y) in u_line]): [
                    [list(point) for point in xyz] for xyz in sorted(line_to_xyz[u_line])
                ]
                for u_line in sorted(line_to_xyz)[:4]
            },
        },
        "packet_hessian_split_theorem": theorem,
        "bridge_verdict": (
            "The Witting packet layer now matches the full local Hessian split, not just the "
            "raw 45-support count. The 36 packet-shell triangles project to the exact 12 affine "
            "lines of AG(2,3), each line has exactly 3 packet lifts partitioning its 9 points, "
            "the 12 lines split into 4 direction classes of 3, and every balanced packet lies on "
            "exactly one affine lift in each direction plus its unique fiber. So the communication "
            "layer reconstructs the exact local 9 + 12 x 3 decomposition."
        ),
    }


def main() -> int:
    timer = time.perf_counter()
    payload = analyze()
    output_dir = ROOT / "checks"
    output_dir.mkdir(exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"PART_CXXXI_witting_packet_hessian_split_audit_{timestamp}.json"
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("W33 Witting packet Hessian-split audit")
    for key, value in payload["packet_hessian_split_theorem"].items():
        print(f"  [{'PASS' if value else 'FAIL'}] {key}")
    print(f"  Wrote: {output_path}")
    print(f"  Runtime: {time.perf_counter() - timer:.3f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
