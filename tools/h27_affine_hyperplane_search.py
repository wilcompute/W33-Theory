#!/usr/bin/env python3
"""Search for an affine F3^4 hyperplane model for H27 via H12 triangle labels.

Setup for each base vertex v0:
- H12 splits into 4 triangles T0..T3 (each of size 3).
- Each H27 vertex is adjacent to exactly one vertex in each Ti.

We label the 3 vertices of each triangle with {0,1,2} (permutation),
then each H27 vertex yields a 4-tuple in F3^4. We check whether the 27
tuples form an affine hyperplane (codimension 1), i.e., a solution set
to a linear equation a·x = c over F3.

Outputs:
- artifacts/h27_affine_hyperplane_search.json
- artifacts/h27_affine_hyperplane_search.md
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import permutations, product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "h27_affine_hyperplane_search.json"
OUT_MD = ROOT / "artifacts" / "h27_affine_hyperplane_search.md"


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


def row_reduce_mod3(mat):
    """Row-reduce a matrix over F3 and return rank and reduced matrix."""
    m = [list(row) for row in mat]
    n_rows = len(m)
    n_cols = len(m[0]) if n_rows else 0
    rank = 0
    col = 0
    while rank < n_rows and col < n_cols:
        pivot = None
        for r in range(rank, n_rows):
            if m[r][col] % 3 != 0:
                pivot = r
                break
        if pivot is None:
            col += 1
            continue
        m[rank], m[pivot] = m[pivot], m[rank]
        inv = 1 if m[rank][col] == 1 else 2  # inverse in F3
        m[rank] = [(inv * x) % 3 for x in m[rank]]
        for r in range(n_rows):
            if r == rank:
                continue
            factor = m[r][col] % 3
            if factor != 0:
                m[r] = [(m[r][c] - factor * m[rank][c]) % 3 for c in range(n_cols)]
        rank += 1
        col += 1
    return rank, m


def nullspace_vector_mod3(mat):
    """Return a nonzero vector in the nullspace of mat over F3 (if exists)."""
    # Solve mat * v = 0, where mat is r x 4, and we expect 1-dim nullspace.
    r = len(mat)
    if r == 0:
        return [1, 0, 0, 0]
    rank, rref = row_reduce_mod3(mat)
    n_cols = len(rref[0])
    pivots = []
    for i in range(rank):
        pivot_col = None
        for j in range(n_cols):
            if rref[i][j] == 1:
                pivot_col = j
                break
        if pivot_col is not None:
            pivots.append(pivot_col)
    free_cols = [c for c in range(n_cols) if c not in pivots]
    if not free_cols:
        return None
    free = free_cols[0]
    v = [0] * n_cols
    v[free] = 1
    for i in range(rank):
        pivot_col = pivots[i]
        v[pivot_col] = (-rref[i][free]) % 3
    return v


def normalize_alpha(alpha):
    """Normalize alpha by scaling so first nonzero is 1."""
    for a in alpha:
        if a % 3 != 0:
            if a % 3 == 1:
                return tuple(a % 3 for a in alpha)
            return tuple((2 * x) % 3 for x in alpha)
    return tuple(alpha)


def main():
    adj, _ = construct_w33()
    n = adj.shape[0]

    lines = []
    results = {}

    lines.append("# H27 as an Affine Hyperplane in F3^4")
    lines.append("")
    lines.append("Searches for labelings of H12 triangles so the 27 H27 vertices")
    lines.append("form an affine hyperplane a·x = c in F3^4.")
    lines.append("")

    perm_list = list(permutations([0, 1, 2]))
    total_labelings = len(perm_list) ** 4

    base_summaries = []
    alpha_counts = Counter()
    base_has_solution = 0

    for v0 in range(n):
        triangles = find_h12_triangles(adj, v0)
        if len(triangles) != 4:
            continue
        # Map each triangle vertex to index 0..2
        tri_index = []
        for tri in triangles:
            tri_index.append({v: i for i, v in enumerate(tri)})

        nonneighbors = [i for i in range(n) if i != v0 and adj[v0, i] == 0]

        # For each H27 vertex, record index tuple (i0,i1,i2,i3)
        idx_tuples = []
        for u in nonneighbors:
            tup = []
            for t in range(4):
                # find which vertex in triangle is adjacent to u
                found = None
                for v in triangles[t]:
                    if adj[u, v]:
                        found = tri_index[t][v]
                        break
                if found is None:
                    found = -1
                tup.append(found)
            idx_tuples.append(tuple(tup))

        # search labelings
        found = False
        example = None
        example_alpha = None
        example_c = None
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
                        # check affine hyperplane
                        base = labels[0]
                        diffs = []
                        for x in labels[1:]:
                            diffs.append([(x[i] - base[i]) % 3 for i in range(4)])
                        rank, _ = row_reduce_mod3(diffs)
                        if rank != 3:
                            continue
                        alpha = nullspace_vector_mod3(diffs)
                        if alpha is None or all(a == 0 for a in alpha):
                            continue
                        alpha = normalize_alpha(alpha)
                        c = sum(alpha[i] * base[i] for i in range(4)) % 3
                        solutions += 1
                        alpha_counts[(alpha, c)] += 1
                        if not found:
                            found = True
                            example = (p0, p1, p2, p3)
                            example_alpha = alpha
                            example_c = c
            # small optimization: early exit if we only want one example
            # (commented to allow full counting per base)
            # if found:
            #     break

        if found:
            base_has_solution += 1
        base_summaries.append({
            "base": v0,
            "solutions": solutions,
            "example_alpha": example_alpha,
            "example_c": example_c,
        })

    results["bases_checked"] = n
    results["labelings_per_base"] = total_labelings
    results["bases_with_solution"] = base_has_solution
    results["alpha_c_counts"] = {str(k): int(v) for k, v in alpha_counts.items()}

    lines.append(f"- Bases checked: {n}")
    lines.append(f"- Labelings per base: {total_labelings}")
    lines.append(f"- Bases with at least one affine-hyperplane labeling: {base_has_solution}")
    lines.append("")

    if alpha_counts:
        lines.append("## Alpha·x = c occurrences (normalized)")
        for (alpha, c), cnt in alpha_counts.most_common(10):
            lines.append(f"- alpha={alpha}, c={c}: {cnt}")
        lines.append("")

    if base_summaries:
        lines.append("## Example base solutions (first 5 bases)")
        for info in base_summaries[:5]:
            lines.append(
                f"- v{info['base']}: solutions={info['solutions']}, "
                f"alpha={info['example_alpha']}, c={info['example_c']}"
            )

    OUT_JSON.write_text(json.dumps(results, indent=2))
    OUT_MD.write_text("\n".join(lines) + "\n")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
