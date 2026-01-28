#!/usr/bin/env python3
"""Investigate D4 triality action on W33's 4-triangle H12 structure.

Key observations:
- H12 (neighbors of any vertex) = 4 disjoint triangles
- D4 has triality: three 8-dimensional representations permuted by order-3 automorphism
- 12 = 4 × 3 suggests the 4 triangles might be related to D4 structure

This tool investigates:
1. How the 4 triangles are related across different base vertices
2. Whether there's a consistent labeling related to D4/triality
3. The structure of the "triangle graph" (4 triangles as vertices)

Outputs:
- artifacts/d4_triality_action.json
- artifacts/d4_triality_action.md
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import combinations, permutations, product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "d4_triality_action.json"
OUT_MD = ROOT / "artifacts" / "d4_triality_action.md"


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
        return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3

    adj = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(i + 1, n):
            if omega(proj_points[i], proj_points[j]) == 0:
                adj[i, j] = adj[j, i] = 1

    return adj, proj_points


def find_h12_triangles(adj, v0):
    """Find the 4 disjoint triangles in H12 (neighbors of v0)."""
    n = adj.shape[0]
    neighbors = [i for i in range(n) if adj[v0, i] == 1]

    # Find connected components (each should be a triangle)
    visited = set()
    triangles = []

    for start in neighbors:
        if start in visited:
            continue
        component = []
        stack = [start]
        while stack:
            v = stack.pop()
            if v in visited:
                continue
            visited.add(v)
            component.append(v)
            for u in neighbors:
                if u not in visited and adj[v, u]:
                    stack.append(u)
        triangles.append(tuple(sorted(component)))

    return triangles


def to_native(obj):
    """Convert numpy types to native Python types."""
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, dict):
        return {str(k): to_native(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [to_native(x) for x in obj]
    return obj


def connected_components(adj):
    """Return connected components for an adjacency matrix."""
    n = adj.shape[0]
    seen = set()
    components = []
    for start in range(n):
        if start in seen:
            continue
        stack = [start]
        comp = []
        while stack:
            v = stack.pop()
            if v in seen:
                continue
            seen.add(v)
            comp.append(v)
            neighbors = np.nonzero(adj[v])[0]
            for u in neighbors:
                if u not in seen:
                    stack.append(u)
        components.append(comp)
    return components


def main():
    results = {}
    lines = []

    # Build W33
    adj, vertices = construct_w33()
    n = len(vertices)

    lines.append("# D4 Triality Action on W33's 4-Triangle Structure")
    lines.append("")

    # Collect all H12 triangles for all vertices
    all_triangles = {}
    triangle_to_base = defaultdict(list)  # Which base vertices have this triangle

    for v0 in range(n):
        triangles = find_h12_triangles(adj, v0)
        all_triangles[v0] = triangles
        for t in triangles:
            triangle_to_base[t].append(v0)

    # Count unique triangles
    unique_triangles = list(triangle_to_base.keys())
    results["unique_triangle_count"] = len(unique_triangles)
    results["total_h12_decompositions"] = n

    lines.append("## Triangle Statistics")
    lines.append("")
    lines.append(f"- W33 vertices: {n}")
    lines.append(
        f"- Unique triangles across all H12 decompositions: {len(unique_triangles)}"
    )
    lines.append("")

    # How many base vertices share each triangle?
    base_counts = Counter(len(v) for v in triangle_to_base.values())
    results["bases_per_triangle_distribution"] = dict(base_counts)

    lines.append("### Triangles shared by base vertices")
    lines.append("")
    for count, freq in sorted(base_counts.items()):
        lines.append(f"- {freq} triangles appear in {count} H12 decompositions")
    lines.append("")

    # Analyze the "triangle adjacency" structure
    # Two triangles are "adjacent" if they share a common base vertex
    lines.append("## Triangle Adjacency Graph")
    lines.append("")

    tri_adj = np.zeros((len(unique_triangles), len(unique_triangles)), dtype=int)
    tri_index = {t: i for i, t in enumerate(unique_triangles)}

    for v0 in range(n):
        tris = all_triangles[v0]
        for i, t1 in enumerate(tris):
            for t2 in tris[i + 1 :]:
                idx1, idx2 = tri_index[t1], tri_index[t2]
                tri_adj[idx1, idx2] = 1
                tri_adj[idx2, idx1] = 1

    tri_edges = tri_adj.sum() // 2
    tri_degrees = tri_adj.sum(axis=1)
    tri_degree_set = sorted(set(tri_degrees))

    results["triangle_graph_vertices"] = len(unique_triangles)
    results["triangle_graph_edges"] = int(tri_edges)
    results["triangle_graph_degree_set"] = [int(d) for d in tri_degree_set]

    lines.append(f"- Vertices (unique triangles): {len(unique_triangles)}")
    lines.append(f"- Edges (co-occurrence in H12): {tri_edges}")
    lines.append(f"- Degree set: {tri_degree_set}")
    lines.append("")

    # Connected components in triangle graph
    components = connected_components(tri_adj)
    comp_sizes = sorted(len(c) for c in components)
    results["triangle_graph_component_sizes"] = comp_sizes

    # Check if each component is a K4
    k4_flags = []
    for comp in components:
        if len(comp) != 4:
            k4_flags.append(False)
            continue
        sub = tri_adj[np.ix_(comp, comp)]
        edges = sub.sum() // 2
        k4_flags.append(edges == 6)

    results["triangle_graph_all_k4"] = bool(components) and all(k4_flags)
    results["triangle_graph_component_count"] = len(components)

    lines.append("### Triangle Graph Components")
    lines.append("")
    lines.append(f"- Component sizes: {comp_sizes}")
    lines.append(f"- All components are K4: {results['triangle_graph_all_k4']}")
    lines.append("")

    # Analyze intersection patterns between H12 decompositions
    lines.append("## H12 Intersection Patterns")
    lines.append("")

    # For adjacent vertices, how do their H12 decompositions relate?
    intersection_sizes = []
    for i in range(n):
        for j in range(i + 1, n):
            if adj[i, j]:  # adjacent vertices
                tris_i = set(all_triangles[i])
                tris_j = set(all_triangles[j])
                intersection_sizes.append(len(tris_i & tris_j))

    intersection_dist = Counter(intersection_sizes)
    results["adjacent_h12_intersection_distribution"] = dict(intersection_dist)

    lines.append(
        "For W33-adjacent vertices (i, j), how many H12 triangles do they share?"
    )
    lines.append("")
    for size, count in sorted(intersection_dist.items()):
        lines.append(f"- {count} adjacent pairs share {size} triangles")
    lines.append("")

    # For non-adjacent vertices
    nonadj_intersection_sizes = []
    for i in range(n):
        for j in range(i + 1, n):
            if not adj[i, j]:  # non-adjacent vertices
                tris_i = set(all_triangles[i])
                tris_j = set(all_triangles[j])
                nonadj_intersection_sizes.append(len(tris_i & tris_j))

    nonadj_intersection_dist = Counter(nonadj_intersection_sizes)
    results["nonadjacent_h12_intersection_distribution"] = dict(
        nonadj_intersection_dist
    )

    lines.append(
        "For W33-non-adjacent vertices (i, j), how many H12 triangles do they share?"
    )
    lines.append("")
    for size, count in sorted(nonadj_intersection_dist.items()):
        lines.append(f"- {count} non-adjacent pairs share {size} triangles")
    lines.append("")

    # Analyze triangle structure more deeply
    # Each triangle is 3 W33 vertices - what's their W33 structure?
    lines.append("## Triangle Vertex Analysis")
    lines.append("")

    # Sample a few triangles
    sample_triangles = unique_triangles[:5]
    for tri in sample_triangles:
        a, b, c = tri
        # Count common neighbors in W33
        cn_ab = sum(1 for k in range(n) if adj[a, k] and adj[b, k])
        cn_bc = sum(1 for k in range(n) if adj[b, k] and adj[c, k])
        cn_ac = sum(1 for k in range(n) if adj[a, k] and adj[c, k])
        # All three mutual
        cn_abc = sum(1 for k in range(n) if adj[a, k] and adj[b, k] and adj[c, k])

        lines.append(f"Triangle {tri}:")
        lines.append(
            f"  - Common neighbors: ab={cn_ab}, bc={cn_bc}, ac={cn_ac}, abc={cn_abc}"
        )

    lines.append("")

    # Key insight: relationship to D4 structure
    lines.append("## D4 Connection")
    lines.append("")
    lines.append("The 4-triangle decomposition of H12 suggests D4 structure:")
    lines.append("")
    lines.append("- D4 Dynkin diagram has 4-fold symmetry (3 legs from center)")
    lines.append("- D4 has 24 roots = 4 × 6 (4 groups of 6)")
    lines.append("- W33 eigenvalue 2 has multiplicity 24")
    lines.append("- Each H12 decomposition gives 4 triangles × 3 vertices = 12")
    lines.append("")

    # Check if the 4 triangles form any pattern
    lines.append("### Inter-triangle W33 adjacencies")
    lines.append("")

    v0 = 0
    tris = all_triangles[v0]
    lines.append(f"For v0 = {v0}, H12 triangles: {tris}")
    lines.append("")

    # Build inter-triangle adjacency matrix
    inter_tri_adj = np.zeros((4, 4), dtype=int)
    for i, t1 in enumerate(tris):
        for j, t2 in enumerate(tris):
            if i != j:
                # Count edges between triangles
                edges = sum(1 for a in t1 for b in t2 if adj[a, b])
                inter_tri_adj[i, j] = edges

    lines.append("Inter-triangle edge counts (within H12, should be 0 since disjoint):")
    for i in range(4):
        row = [str(inter_tri_adj[i, j]) for j in range(4)]
        lines.append(f"  T{i}: [{', '.join(row)}]")
    lines.append("")

    # Check edges between triangle vertices and base vertex
    lines.append("Each triangle vertex is adjacent to base vertex v0 by definition.")
    lines.append("")

    # What about edges between triangles in the full W33 (not just H12)?
    # This is the same as inter_tri_adj since H12 is induced subgraph
    lines.append("In the full W33, are vertices from different triangles connected?")
    full_inter = np.zeros((4, 4), dtype=int)
    for i, t1 in enumerate(tris):
        for j, t2 in enumerate(tris):
            if i < j:
                edges = sum(1 for a in t1 for b in t2 if adj[a, b])
                full_inter[i, j] = edges
                full_inter[j, i] = edges

    for i in range(4):
        row = [str(full_inter[i, j]) for j in range(4)]
        lines.append(f"  T{i}: [{', '.join(row)}]")

    results["sample_inter_triangle_adj"] = full_inter.tolist()
    lines.append("")

    total_inter = full_inter.sum() // 2
    lines.append(f"Total inter-triangle edges: {total_inter}")
    lines.append("")

    # Write outputs
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(to_native(results), indent=2), encoding="utf-8")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
