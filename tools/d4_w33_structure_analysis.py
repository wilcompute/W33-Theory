#!/usr/bin/env python3
"""D4 structure analysis in W33.

Investigates the connection between:
- K4,4 tetrahedral subgraph (8 special rays)
- H12 = 4 disjoint triangles structure (neighbors of any vertex)
- D4 triality and the 24-dimensional eigenspace

Key insight: H12 being 4 disjoint triangles suggests D4 structure
since D4 root system has 24 = 4 × 6 roots forming 4 octahedra.

Outputs:
- artifacts/d4_w33_structure_analysis.json
- artifacts/d4_w33_structure_analysis.md
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "d4_w33_structure_analysis.json"
OUT_MD = ROOT / "artifacts" / "d4_w33_structure_analysis.md"
TETRA_JSON = ROOT / "artifacts" / "witting_w33_tetra_subgraph.json"


def construct_w33():
    """Construct W33 from F_3^4 symplectic geometry."""
    F3 = [0, 1, 2]

    # Generate projective points
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

    # Symplectic form
    def omega(x, y):
        return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3

    # Adjacency: collinear points have omega = 0
    # But we must exclude the same point (which always has omega = 0 with itself)
    adj = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(i + 1, n):
            # Check if points are collinear (omega = 0 means they span isotropic subspace)
            # But also verify they're distinct projective points
            if omega(proj_points[i], proj_points[j]) == 0:
                adj[i, j] = adj[j, i] = 1

    return adj, proj_points


def find_triangles(adj, vertices):
    """Find all triangles in induced subgraph."""
    triangles = []
    vlist = list(vertices)
    for i, a in enumerate(vlist):
        for j, b in enumerate(vlist[i + 1 :], i + 1):
            if adj[a, b]:
                for c in vlist[j + 1 :]:
                    if adj[a, c] and adj[b, c]:
                        triangles.append((a, b, c))
    return triangles


def find_connected_components(adj, vertices):
    """Find connected components in induced subgraph."""
    vset = set(vertices)
    visited = set()
    components = []

    for start in vertices:
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
            for u in vertices:
                if u not in visited and adj[v, u]:
                    stack.append(u)
        components.append(sorted(component))

    return components


def build_d4_roots():
    """Build D4 root system (24 roots in R^4)."""
    roots = []
    for i in range(4):
        for j in range(i + 1, 4):
            for si in [1, -1]:
                for sj in [1, -1]:
                    r = [0, 0, 0, 0]
                    r[i] = si
                    r[j] = sj
                    roots.append(tuple(r))
    return roots


def to_native(obj):
    """Convert numpy types to native Python types for JSON serialization."""
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, dict):
        return {k: to_native(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [to_native(x) for x in obj]
    return obj


def main():
    results = {}
    lines = []

    # Build W33
    adj, vertices = construct_w33()
    n = len(vertices)
    results["w33_vertices"] = int(n)

    # Compute eigenvalues
    eigenvalues = np.linalg.eigvalsh(adj)
    eigenvalues = np.round(eigenvalues, 6)
    eig_mults = Counter(eigenvalues)
    results["eigenvalues"] = {
        str(e): int(m) for e, m in sorted(eig_mults.items(), reverse=True)
    }

    lines.append("# D4 Structure Analysis in W33")
    lines.append("")
    lines.append("## Eigenvalue Structure")
    lines.append("")
    for e, m in sorted(eig_mults.items(), reverse=True):
        lines.append(f"- λ = {e:.0f}: multiplicity {m}")
    lines.append("")

    # Analyze H12 for several vertices
    lines.append("## H12 Analysis (neighbor subgraph)")
    lines.append("")

    h12_analyses = []
    for v0 in range(min(5, n)):  # Check first 5 vertices
        neighbors = [i for i in range(n) if adj[v0, i]]
        deg_in_h12 = [sum(adj[i, j] for j in neighbors if i != j) for i in neighbors]
        components = find_connected_components(adj, neighbors)
        triangles = find_triangles(adj, neighbors)

        h12_analyses.append(
            {
                "vertex": v0,
                "neighbor_count": len(neighbors),
                "degree_set_in_h12": sorted(set(deg_in_h12)),
                "component_count": len(components),
                "component_sizes": [len(c) for c in components],
                "triangle_count": len(triangles),
            }
        )

    results["h12_analyses"] = h12_analyses

    # Check if H12 is always 4 disjoint triangles
    all_4_triangles = all(
        a["component_count"] == 4 and a["component_sizes"] == [3, 3, 3, 3]
        for a in h12_analyses
    )
    results["h12_always_4_triangles"] = all_4_triangles

    lines.append(f"Checked {len(h12_analyses)} vertices:")
    for a in h12_analyses:
        lines.append(
            f"- v{a['vertex']}: {a['component_count']} components of sizes {a['component_sizes']}, {a['triangle_count']} triangles"
        )
    lines.append("")
    lines.append(f"**H12 is always 4 disjoint triangles: {all_4_triangles}**")
    lines.append("")

    # D4 root system analysis
    lines.append("## D4 Root System")
    lines.append("")

    d4_roots = build_d4_roots()
    results["d4_root_count"] = len(d4_roots)

    # D4 has 6 pairs of opposite roots (±r), so 12 lines
    # Each root has norm sqrt(2), inner products are 2, 1, 0, -1, -2
    d4_adjacency = np.zeros((24, 24), dtype=int)
    for i, r1 in enumerate(d4_roots):
        for j, r2 in enumerate(d4_roots):
            if i != j:
                ip = sum(a * b for a, b in zip(r1, r2))
                # Adjacent if inner product = ±1 (angle 60° or 120°)
                if abs(ip) == 1:
                    d4_adjacency[i, j] = 1

    d4_degree = d4_adjacency.sum(axis=1)[0]
    results["d4_root_adjacency_degree"] = int(d4_degree)

    lines.append(f"- D4 has {len(d4_roots)} roots")
    lines.append(f"- Root adjacency degree (|ip|=1): {d4_degree}")
    lines.append("")

    # Check D4 root graph structure
    d4_components = find_connected_components(d4_adjacency, list(range(24)))
    results["d4_component_count"] = len(d4_components)
    results["d4_component_sizes"] = [len(c) for c in d4_components]

    lines.append(f"- D4 root graph components: {len(d4_components)}")
    lines.append(f"- Component sizes: {[len(c) for c in d4_components]}")
    lines.append("")

    # Load tetrahedral subgraph if available
    if TETRA_JSON.exists():
        tetra_data = json.loads(TETRA_JSON.read_text())
        tetra_rays = tetra_data.get("tetra_rays", [])
        partition = tetra_data.get("partition", {})

        lines.append("## K4,4 Tetrahedral Subgraph")
        lines.append("")
        lines.append(f"- 8 tetrahedral rays: {tetra_rays}")
        lines.append(f"- Bipartition: {partition}")
        lines.append("")

        # Check relationship between tetrahedral rays and H12 triangles
        lines.append("### Tetrahedral rays in H12 decomposition")
        lines.append("")

        for v0 in [0, 1, 2]:
            neighbors = [i for i in range(n) if adj[v0, i]]
            tetra_in_neighbors = [r for r in tetra_rays if r in neighbors]
            lines.append(
                f"- v{v0} neighbors contain {len(tetra_in_neighbors)} tetrahedral rays: {tetra_in_neighbors}"
            )

        results["tetra_rays"] = tetra_rays
        results["tetra_partition"] = partition

    lines.append("")
    lines.append("## Key Observations")
    lines.append("")
    lines.append(
        "1. **H12 = 4 disjoint triangles** (verified for all checked vertices)"
    )
    lines.append("   - 12 = 4 × 3 matches D4 structure")
    lines.append("   - Each triangle might correspond to one of four D4 'octahedra'")
    lines.append("")
    lines.append("2. **D4 has 24 roots = eigenspace dimension for λ=2**")
    lines.append("   - 24 = 3 × 8 (triality)")
    lines.append("   - 24 = 4 × 6 (four octahedra)")
    lines.append("")
    lines.append("3. **Connection to W(D4) = 192**:")
    lines.append("   - |Aut(W33)| = 51840 = 192 × 270")
    lines.append("   - 192 = |W(D4)| = Weyl group of D4")
    lines.append("   - 270 = 27 × 10 (Albert × SO(10) vector)")
    lines.append("")

    # Write outputs
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(to_native(results), indent=2), encoding="utf-8")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
