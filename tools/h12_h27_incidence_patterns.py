#!/usr/bin/env python3
"""Analyze H12-H27 incidence patterns relative to the 4-triangle decomposition.

For a base vertex v0:
- H12 = neighbors (12 vertices) split into 4 disjoint triangles
- H27 = non-neighbors (27 vertices)

We measure how each H27 vertex connects into the 4 triangles and whether
the pattern distribution is uniform across base vertices.

Outputs:
- artifacts/h12_h27_incidence_patterns.json
- artifacts/h12_h27_incidence_patterns.md
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "h12_h27_incidence_patterns.json"
OUT_MD = ROOT / "artifacts" / "h12_h27_incidence_patterns.md"


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

    triangles = sorted(triangles)
    return triangles


def to_native(obj):
    """Convert numpy types to native Python types for JSON."""
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


def main():
    results = {}
    lines = []

    adj, _ = construct_w33()
    n = adj.shape[0]

    lines.append("# H12–H27 Incidence Patterns")
    lines.append("")
    lines.append("For each base vertex v0, H12 (neighbors) splits into 4 triangles.")
    lines.append("We count how each H27 vertex attaches to these triangles.")
    lines.append("")

    per_base_patterns = []
    per_base_sorted_patterns = []
    per_base_h27_deg_to_h12 = []
    per_base_tri_counts = []

    for v0 in range(n):
        triangles = find_h12_triangles(adj, v0)
        neighbors = [i for i in range(n) if adj[v0, i] == 1]
        nonneighbors = [i for i in range(n) if i != v0 and adj[v0, i] == 0]

        # sanity checks
        if len(triangles) != 4 or any(len(t) != 3 for t in triangles):
            continue

        # map vertex -> triangle index
        tri_index = {}
        for idx, tri in enumerate(triangles):
            for v in tri:
                tri_index[v] = idx

        pattern_counts = Counter()
        pattern_counts_sorted = Counter()
        h27_deg_to_h12 = []

        for u in nonneighbors:
            counts = []
            for tri in triangles:
                counts.append(sum(adj[u, v] for v in tri))
            counts_tuple = tuple(counts)
            pattern_counts[counts_tuple] += 1
            pattern_counts_sorted[tuple(sorted(counts, reverse=True))] += 1
            h27_deg_to_h12.append(sum(counts))

        per_base_patterns.append(pattern_counts)
        per_base_sorted_patterns.append(pattern_counts_sorted)
        per_base_h27_deg_to_h12.append(h27_deg_to_h12)

        # per-triangle local distribution
        tri_local = []
        for tri in triangles:
            local_counts = Counter()
            for u in nonneighbors:
                local_counts[sum(adj[u, v] for v in tri)] += 1
            tri_local.append(dict(sorted(local_counts.items())))
        per_base_tri_counts.append(tri_local)

    # Check uniformity across bases
    base_pattern_sets = {tuple(sorted(c.items())) for c in per_base_sorted_patterns}
    base_uniform = len(base_pattern_sets) == 1

    results["bases_checked"] = n
    results["pattern_distribution_uniform"] = base_uniform
    if per_base_sorted_patterns:
        results["pattern_distribution_example"] = dict(per_base_sorted_patterns[0])
    if per_base_patterns:
        results["pattern_distribution_ordered_example"] = dict(per_base_patterns[0])

    # H27 degree-to-H12 statistics
    flat_deg = [d for lst in per_base_h27_deg_to_h12 for d in lst]
    results["h27_degree_to_h12_min"] = int(min(flat_deg)) if flat_deg else None
    results["h27_degree_to_h12_max"] = int(max(flat_deg)) if flat_deg else None
    results["h27_degree_to_h12_hist"] = dict(Counter(flat_deg))

    lines.append("## Pattern Distribution (triangle-order independent)")
    lines.append("")
    lines.append(f"- Uniform across bases: {base_uniform}")
    if per_base_sorted_patterns:
        lines.append("- Example distribution (sorted counts):")
        for k, v in sorted(per_base_sorted_patterns[0].items()):
            key = tuple(int(x) for x in k)
            lines.append(f"  - {key}: {int(v)}")
    lines.append("")

    lines.append("## Pattern Distribution (ordered by triangle index)")
    lines.append("")
    if per_base_patterns:
        for k, v in sorted(per_base_patterns[0].items()):
            key = tuple(int(x) for x in k)
            lines.append(f"- {key}: {int(v)}")
    lines.append("")

    lines.append("## H27 Degree into H12")
    lines.append("")
    lines.append(f"- min: {results['h27_degree_to_h12_min']}")
    lines.append(f"- max: {results['h27_degree_to_h12_max']}")
    lines.append("- histogram:")
    for k, v in sorted(results["h27_degree_to_h12_hist"].items()):
        lines.append(f"  - {int(k)}: {int(v)}")
    lines.append("")

    lines.append("## Per-Triangle Attachment Counts (example base)")
    lines.append("")
    if per_base_tri_counts:
        for idx, local in enumerate(per_base_tri_counts[0]):
            clean = {int(k): int(v) for k, v in local.items()}
            lines.append(f"- Triangle {idx}: {clean}")
    lines.append("")

    OUT_JSON.write_text(json.dumps(to_native(results), indent=2))
    OUT_MD.write_text("\n".join(lines) + "\n")

    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
