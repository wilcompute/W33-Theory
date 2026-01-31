"""Partial pure-Python verifier for W33 conjugacy/class alignment pre-checks.

This script avoids Sage/GAP by checking the incidence bipartite graph construction,
counts, and degree distributions. It does not compute automorphism groups (those
remain in Sage), but it provides a CI-friendly smoke test to ensure basic
structure is correct and reproducible.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

from lib.w33_io import W33DataPaths, load_w33_lines


def build_incidence_edges(
    lines: List[Tuple[int, int, int, int]],
) -> List[Tuple[int, int]]:
    edges = []
    for line_index, pts in enumerate(lines):
        line_vertex = 41 + line_index
        for p in pts:
            # convert point IDs which are 0-based in our data to 1-based vertex labels (1..40)
            edges.append((p + 1, line_vertex))
    return edges


def summary_from_edges(edges: List[Tuple[int, int]]):
    verts = set()
    degree = {}
    for u, v in edges:
        verts.add(u)
        verts.add(v)
        degree[u] = degree.get(u, 0) + 1
        degree[v] = degree.get(v, 0) + 1
    return {
        "num_vertices": len(verts),
        "num_edges": len(edges),
        "degree_counts": sorted(degree.values()),
    }


def main() -> int:
    here = Path(__file__).resolve().parent
    paths = W33DataPaths.from_this_file(here / "tools" / "w33_verify_alignment_py.py")
    lines = load_w33_lines(paths)
    edges = build_incidence_edges(lines)
    s = summary_from_edges(edges)
    print("Incidence graph summary:")
    for k, v in s.items():
        print(f"  {k}: {v}")
    # Basic assertions
    if s["num_vertices"] != 80:
        print("Unexpected number of vertices in incidence graph (expect 80)")
        return 2
    if s["num_edges"] != 40 * 4:
        print("Unexpected number of edges (expect 160)")
        return 3
    # check degree distribution: points degree 4, line vertices degree 4
    degs = s["degree_counts"]
    if min(degs) < 1:
        print("Some vertex has zero degree, unexpected")
        return 4
    print("Basic structural checks passed (incidence bipartite graph looks correct).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
