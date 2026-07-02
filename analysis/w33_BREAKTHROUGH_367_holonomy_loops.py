#!/usr/bin/env python3
"""BT367 Extension: Identify the Holonomy Cycles.

Builds the skew-line graph G of W(3,3), finds a cycle basis,
and measures the S3 holonomy of each cycle.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict, deque
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_357_minimal_logical_orbit_stabilizers import (
    build_w33,
    generate_projective_symplectic_group,
)
from analysis.w33_BREAKTHROUGH_360_selector_zmin_sheet_design import (
    selector_failure_edge_supports,
    sheet_orbit,
)
from analysis.w33_BREAKTHROUGH_361_selector_qutrit_phase_bundle import sheet_anchor_line


def compose(p1: tuple[int, ...], p2: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(p2[p1[i]] for i in range(3))


def inverse(p: tuple[int, ...]) -> tuple[int, ...]:
    inv = [0, 0, 0]
    for i, v in enumerate(p):
        inv[v] = i
    return tuple(inv)


def find_path(tree: dict[int, int], start: int, end: int) -> list[int]:
    """Finds path in a spanning tree represented as parent pointers."""

    def get_ancestors(node):
        path = []
        curr = node
        while curr is not None:
            path.append(curr)
            curr = tree.get(curr)
        return path

    path_start = get_ancestors(start)
    path_end = get_ancestors(end)

    # Find lowest common ancestor
    lca = None
    path_end_set = set(path_end)
    for node in path_start:
        if node in path_end_set:
            lca = node
            break

    # Path is start -> lca -> end
    res = []
    for node in path_start:
        res.append(node)
        if node == lca:
            break

    full_end_path = []
    for node in path_end:
        if node == lca:
            break
        full_end_path.append(node)

    return res + full_end_path[::-1]


def main():
    # 1. Build sigma (1-cocycle)
    points, edges, edge_index, lines, _ = build_w33()
    group = generate_projective_symplectic_group(points)
    base_sheet = frozenset(selector_failure_edge_supports(edges, edge_index))
    sheets = sheet_orbit(group, base_sheet, edges, edge_index)
    anchor_by_sheet = [sheet_anchor_line(sheet, edges, lines) for sheet in sheets]
    fibers = defaultdict(list)
    for s_idx, l_idx in enumerate(anchor_by_sheet):
        fibers[l_idx].append(s_idx)

    intersections = [
        [len(sheets[l] & sheets[r]) for r in range(120)] for l in range(120)
    ]

    sigma = {}
    graph = defaultdict(list)  # skew-line graph
    all_edges = []

    line_indices = sorted(fibers.keys())
    for i in range(len(line_indices)):
        for j in range(i + 1, len(line_indices)):
            u, v = line_indices[i], line_indices[j]
            if set(lines[u]) & set(lines[v]):
                continue  # not skew

            left_fiber = sorted(fibers[u])
            right_fiber = sorted(fibers[v])
            mapping = {}
            for l_ord, l_sheet in enumerate(left_fiber):
                for r_ord, r_sheet in enumerate(right_fiber):
                    if intersections[l_sheet][r_sheet] == 4:
                        mapping[l_ord] = r_ord

            perm = tuple(mapping[k] for k in range(3))
            sigma[(u, v)] = perm
            sigma[(v, u)] = inverse(perm)
            graph[u].append(v)
            graph[v].append(u)
            all_edges.append((u, v))

    # 2. Build spanning tree T
    tree_parents = {line_indices[0]: None}
    queue = deque([line_indices[0]])
    tree_edges = set()

    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if v not in tree_parents:
                tree_parents[v] = u
                tree_edges.add(tuple(sorted((u, v))))
                queue.append(v)

    # 3. Find cycle basis and compute holonomy
    back_edges = [e for e in all_edges if tuple(sorted(e)) not in tree_edges]

    id_perm = (0, 1, 2)
    twisted_cycles = []

    for u, v in back_edges:
        # Cycle is u -> v -> path_in_tree(v, u)
        path = find_path(tree_parents, v, u)
        # Holonomy: sigma(u,v) * sigma(v, path[0]) * ... * sigma(path[-2], u)
        h = sigma[(u, v)]
        curr = v
        for next_node in path[1:]:
            h = compose(h, sigma[(curr, next_node)])
            curr = next_node

        if h != id_perm:
            twisted_cycles.append({"edge": [u, v], "path": path, "holonomy": list(h)})

    from collections import Counter

    holonomy_types = Counter([tuple(c["holonomy"]) for c in twisted_cycles])

    results = {
        "total_back_edges": len(back_edges),
        "twisted_cycles_in_basis": len(twisted_cycles),
        "total_cycles_in_basis": len(back_edges),
        "holonomy_distribution": {str(k): v for k, v in holonomy_types.items()},
        "sample_twisted_cycle": twisted_cycles[0] if twisted_cycles else None,
    }

    OUT = ROOT / "data" / "w33_BREAKTHROUGH_367_holonomy_loops.json"
    OUT.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
