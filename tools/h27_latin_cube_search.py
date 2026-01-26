#!/usr/bin/env python3
"""Search for a Latin-cube model of H27 via H12 triangle labels.

We label each of the 4 H12 triangles with symbols {0,1,2}. Each H27 vertex
then becomes a 4-tuple in F3^4. We check whether, for some labeling,
one coordinate is a function of the other three (a 3×3×3 Latin cube).

Outputs:
- artifacts/h27_latin_cube_search.json
- artifacts/h27_latin_cube_search.md
"""
from __future__ import annotations

import json
from collections import Counter
from itertools import permutations, product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "h27_latin_cube_search.json"
OUT_MD = ROOT / "artifacts" / "h27_latin_cube_search.md"


def construct_w33():
    """Construct W33 from F_3^4 symplectic geometry."""
    F3 = [0, 1, 2]
    vectors = [v for v in product(F3, repeat=4) if any(x != 0 for x in v)]

    proj_points = []
    seen = set()
    for v in vectors:
        v = list(v)
        for i in range(4):
            if v[i] != 0:
                inv = 1 if v[i] == 1 else 2
                v = tuple((x * inv) % 3 for x in v)
                break
        if v not in seen:
            seen.add(v)
            proj_points.append(v)

    n = len(proj_points)

    def omega(x, y):
        return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3

    adj = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(i+1, n):
            if omega(proj_points[i], proj_points[j]) == 0:
                adj[i, j] = adj[j, i] = 1

    return adj, proj_points


def find_h12_triangles(adj, v0):
    """Return the 4 disjoint triangles inside H12 (neighbors of v0)."""
    n = adj.shape[0]
    neighbors = [i for i in range(n) if adj[v0, i] == 1]

    visited = set()
    triangles = []
    for start in neighbors:
        if start in visited:
            continue
        stack = [start]
        comp = []
        while stack:
            v = stack.pop()
            if v in visited:
                continue
            visited.add(v)
            comp.append(v)
            for u in neighbors:
                if u not in visited and adj[v, u]:
                    stack.append(u)
        triangles.append(tuple(sorted(comp)))

    return sorted(triangles)


def main():
    adj, _ = construct_w33()
    n = adj.shape[0]
    perm_list = list(permutations([0, 1, 2]))

    results = {}
    lines = []

    lines.append("# H27 Latin-Cube Search")
    lines.append("")
    lines.append("Checks if H27 can be modeled as a 3×3×3 Latin cube (one coordinate")
    lines.append("is a function of the other three) under triangle labelings.")
    lines.append("")

    bases_with_solution = 0
    base_summaries = []
    coord_counts = Counter()

    for v0 in range(n):
        triangles = find_h12_triangles(adj, v0)
        if len(triangles) != 4:
            continue
        tri_index = []
        for tri in triangles:
            tri_index.append({v: i for i, v in enumerate(tri)})

        nonneighbors = [i for i in range(n) if i != v0 and adj[v0, i] == 0]
        idx_tuples = []
        for u in nonneighbors:
            tup = []
            for t in range(4):
                found = None
                for v in triangles[t]:
                    if adj[u, v]:
                        found = tri_index[t][v]
                        break
                if found is None:
                    found = -1
                tup.append(found)
            idx_tuples.append(tuple(tup))

        found = False
        example = None
        solutions = 0

        for p0 in perm_list:
            for p1 in perm_list:
                for p2 in perm_list:
                    for p3 in perm_list:
                        labels = []
                        for tup in idx_tuples:
                            if -1 in tup:
                                labels = None
                                break
                            labels.append((p0[tup[0]], p1[tup[1]], p2[tup[2]], p3[tup[3]]))
                        if labels is None:
                            continue
                        label_set = set(labels)
                        if len(label_set) != 27:
                            continue
                        # Check each coordinate as dependent
                        for dep in range(4):
                            proj = set()
                            for x in labels:
                                proj.add(tuple(x[i] for i in range(4) if i != dep))
                            if len(proj) == 27:
                                solutions += 1
                                coord_counts[dep] += 1
                                if not found:
                                    found = True
                                    example = {
                                        "labeling": (p0, p1, p2, p3),
                                        "dependent_coord": dep,
                                    }
                        # small speedup: skip more checks if found and we only want one

        if found:
            bases_with_solution += 1
        base_summaries.append({
            "base": v0,
            "solutions": solutions,
            "example": example,
        })

    results["bases_checked"] = n
    results["bases_with_solution"] = bases_with_solution
    results["dependent_coord_counts"] = dict(coord_counts)

    lines.append(f"- Bases checked: {n}")
    lines.append(f"- Bases with at least one Latin-cube labeling: {bases_with_solution}")
    lines.append("")

    if coord_counts:
        lines.append("## Dependent-coordinate counts (across all solutions)")
        for dep, cnt in sorted(coord_counts.items()):
            lines.append(f"- coord {dep}: {cnt}")
        lines.append("")

    if base_summaries:
        lines.append("## Example base summaries (first 5)")
        for info in base_summaries[:5]:
            lines.append(
                f"- v{info['base']}: solutions={info['solutions']}, example={info['example']}"
            )

    OUT_JSON.write_text(json.dumps(results, indent=2))
    OUT_MD.write_text("\n".join(lines) + "\n")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
