#!/usr/bin/env python3
"""Investigate potential E8 correspondence via the triangle co-occurrence graph.

KEY OBSERVATION:
- W33 has 160 unique triangles (H12 decompositions)
- Triangle co-occurrence graph: 160 vertices, 240 edges, 3-regular
- E8 has 240 roots!

Could the 240 EDGES of the triangle graph correspond to E8 roots?

This tool investigates:
1. Triangle graph structure and spectrum
2. E8 root system structure
3. Potential bijections between triangle-graph edges and E8 roots
4. Structure preservation under any found mapping

Outputs:
- artifacts/triangle_e8_correspondence.json
- artifacts/triangle_e8_correspondence.md
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "triangle_e8_correspondence.json"
OUT_MD = ROOT / "artifacts" / "triangle_e8_correspondence.md"


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
    """Find the 4 disjoint triangles in H12."""
    n = adj.shape[0]
    neighbors = [i for i in range(n) if adj[v0, i] == 1]

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


def build_e8_roots():
    """Build E8 root system (240 roots in R^8)."""
    roots = []

    # Type 1: permutations of (±1, ±1, 0, 0, 0, 0, 0, 0) - 112 roots
    for i in range(8):
        for j in range(i+1, 8):
            for si in [1, -1]:
                for sj in [1, -1]:
                    r = [0]*8
                    r[i] = si
                    r[j] = sj
                    roots.append(tuple(r))

    # Type 2: (±1/2, ..., ±1/2) with even number of minus signs - 128 roots
    for signs in product([1, -1], repeat=8):
        if sum(1 for s in signs if s == -1) % 2 == 0:
            roots.append(tuple(s/2 for s in signs))

    return roots


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


def main():
    results = {}
    lines = []

    lines.append("# Triangle Graph ↔ E8 Correspondence Investigation")
    lines.append("")
    lines.append("**Key Observation**: The W33 triangle co-occurrence graph has 240 edges,")
    lines.append("the same as the number of E8 roots!")
    lines.append("")

    # Build W33 and collect all triangles
    adj, vertices = construct_w33()
    n = len(vertices)

    all_triangles = {}
    triangle_to_base = defaultdict(list)

    for v0 in range(n):
        triangles = find_h12_triangles(adj, v0)
        all_triangles[v0] = triangles
        for t in triangles:
            triangle_to_base[t].append(v0)

    unique_triangles = list(triangle_to_base.keys())
    tri_index = {t: i for i, t in enumerate(unique_triangles)}

    results["triangle_count"] = len(unique_triangles)
    lines.append(f"## W33 Triangle Structure")
    lines.append("")
    lines.append(f"- Unique triangles: {len(unique_triangles)}")
    lines.append("")

    # Build triangle co-occurrence graph
    tri_adj = np.zeros((len(unique_triangles), len(unique_triangles)), dtype=int)

    for v0 in range(n):
        tris = all_triangles[v0]
        for i, t1 in enumerate(tris):
            for t2 in tris[i+1:]:
                idx1, idx2 = tri_index[t1], tri_index[t2]
                tri_adj[idx1, idx2] = 1
                tri_adj[idx2, idx1] = 1

    tri_edges = tri_adj.sum() // 2
    tri_degrees = tri_adj.sum(axis=1)
    tri_degree_set = sorted(set(tri_degrees))

    results["triangle_graph"] = {
        "vertices": len(unique_triangles),
        "edges": int(tri_edges),
        "degree_set": [int(d) for d in tri_degree_set],
    }

    lines.append(f"## Triangle Co-occurrence Graph")
    lines.append("")
    lines.append(f"- Vertices: {len(unique_triangles)}")
    lines.append(f"- **Edges: {tri_edges}** (= E8 root count!)")
    lines.append(f"- Degree: {tri_degree_set[0] if len(tri_degree_set) == 1 else tri_degree_set}")
    lines.append("")

    # Compute triangle graph spectrum
    tri_eigenvalues = np.linalg.eigvalsh(tri_adj)
    tri_eigenvalues = np.round(tri_eigenvalues, 4)
    tri_eig_mults = Counter(tri_eigenvalues)

    results["triangle_graph_spectrum"] = {str(e): int(m) for e, m in sorted(tri_eig_mults.items(), reverse=True)}

    lines.append("### Triangle Graph Spectrum")
    lines.append("")
    for e, m in sorted(tri_eig_mults.items(), reverse=True):
        lines.append(f"- λ = {e}: multiplicity {m}")
    lines.append("")

    # Build E8 root system
    e8_roots = build_e8_roots()
    results["e8_root_count"] = len(e8_roots)

    lines.append(f"## E8 Root System")
    lines.append("")
    lines.append(f"- Roots: {len(e8_roots)}")
    lines.append("")

    # E8 root inner products and adjacency
    # Roots are adjacent if inner product = ±1 (angle 60° or 120°)
    e8_adj = np.zeros((240, 240), dtype=int)
    for i, r1 in enumerate(e8_roots):
        for j, r2 in enumerate(e8_roots):
            if i != j:
                ip = sum(a*b for a, b in zip(r1, r2))
                if abs(ip - 1) < 0.01 or abs(ip + 1) < 0.01:
                    e8_adj[i, j] = 1

    e8_degree = e8_adj.sum(axis=1)[0]
    e8_edges = e8_adj.sum() // 2

    results["e8_adjacency"] = {
        "degree": int(e8_degree),
        "edges": int(e8_edges),
    }

    lines.append(f"### E8 Root Adjacency (|inner product| = 1)")
    lines.append("")
    lines.append(f"- Degree: {e8_degree}")
    lines.append(f"- Edges: {e8_edges}")
    lines.append("")

    # Key comparison: triangle graph edges vs E8 roots
    lines.append("## The 240 = 240 Connection")
    lines.append("")
    lines.append(f"| Object | Count |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Triangle graph edges | {tri_edges} |")
    lines.append(f"| E8 roots | {len(e8_roots)} |")
    lines.append("")

    if tri_edges == len(e8_roots):
        lines.append("**EXACT MATCH!**")
        lines.append("")
        lines.append("This suggests a potential bijection:")
        lines.append("- Triangle graph edges ↔ E8 roots")
        lines.append("")

    # Investigate the line graph of triangle graph
    # Each edge becomes a vertex; edges are adjacent if they share a triangle-vertex
    lines.append("## Line Graph Analysis")
    lines.append("")
    lines.append("The line graph L(T) of the triangle graph T has:")
    lines.append("- Vertices = edges of T = 240")
    lines.append("- Edges = pairs of T-edges sharing a T-vertex")
    lines.append("")

    # Build edge list
    tri_edge_list = []
    for i in range(len(unique_triangles)):
        for j in range(i+1, len(unique_triangles)):
            if tri_adj[i, j]:
                tri_edge_list.append((i, j))

    results["triangle_edge_count"] = len(tri_edge_list)

    # Build line graph adjacency
    line_adj = np.zeros((len(tri_edge_list), len(tri_edge_list)), dtype=int)
    edge_to_idx = {e: i for i, e in enumerate(tri_edge_list)}

    for i, (a1, b1) in enumerate(tri_edge_list):
        for j, (a2, b2) in enumerate(tri_edge_list):
            if i < j:
                # Edges are adjacent in line graph if they share a vertex
                if a1 == a2 or a1 == b2 or b1 == a2 or b1 == b2:
                    line_adj[i, j] = 1
                    line_adj[j, i] = 1

    line_degree = line_adj.sum(axis=1)
    line_degree_set = sorted(set(line_degree))
    line_edges = line_adj.sum() // 2

    results["line_graph"] = {
        "vertices": len(tri_edge_list),
        "edges": int(line_edges),
        "degree_set": [int(d) for d in line_degree_set],
    }

    lines.append(f"### Line Graph L(T) Properties")
    lines.append("")
    lines.append(f"- Vertices: {len(tri_edge_list)}")
    lines.append(f"- Edges: {line_edges}")
    lines.append(f"- Degree: {line_degree_set[0] if len(line_degree_set) == 1 else line_degree_set}")
    lines.append("")

    # Compare with E8
    lines.append(f"### Comparison with E8")
    lines.append("")
    lines.append(f"| Property | L(T) | E8 root graph |")
    lines.append(f"|----------|------|---------------|")
    lines.append(f"| Vertices | {len(tri_edge_list)} | {len(e8_roots)} |")
    lines.append(f"| Degree | {line_degree_set[0] if len(line_degree_set) == 1 else 'varies'} | {e8_degree} |")
    lines.append(f"| Edges | {line_edges} | {e8_edges} |")
    lines.append("")

    # Check if degrees match
    if len(line_degree_set) == 1 and line_degree_set[0] == e8_degree:
        lines.append("**DEGREE MATCH!** Both graphs are regular with the same degree.")
        results["degree_match"] = True
    else:
        lines.append(f"Degree mismatch: L(T) has degree {line_degree_set}, E8 has degree {e8_degree}")
        results["degree_match"] = False

    lines.append("")

    # Compute line graph spectrum
    if len(tri_edge_list) == 240:
        line_eigenvalues = np.linalg.eigvalsh(line_adj)
        line_eigenvalues = np.round(line_eigenvalues, 4)
        line_eig_mults = Counter(line_eigenvalues)

        results["line_graph_spectrum"] = {str(e): int(m) for e, m in sorted(line_eig_mults.items(), reverse=True)}

        lines.append("### Line Graph Spectrum")
        lines.append("")
        for e, m in sorted(line_eig_mults.items(), reverse=True):
            lines.append(f"- λ = {e}: multiplicity {m}")
        lines.append("")

        # E8 spectrum
        e8_eigenvalues = np.linalg.eigvalsh(e8_adj)
        e8_eigenvalues = np.round(e8_eigenvalues, 4)
        e8_eig_mults = Counter(e8_eigenvalues)

        results["e8_spectrum"] = {str(e): int(m) for e, m in sorted(e8_eig_mults.items(), reverse=True)}

        lines.append("### E8 Root Graph Spectrum")
        lines.append("")
        for e, m in sorted(e8_eig_mults.items(), reverse=True):
            lines.append(f"- λ = {e}: multiplicity {m}")
        lines.append("")

        # Compare spectra
        if set(line_eig_mults.items()) == set(e8_eig_mults.items()):
            lines.append("**SPECTRA MATCH!** The graphs are cospectral!")
            results["spectra_match"] = True
        else:
            lines.append("Spectra do not match exactly.")
            results["spectra_match"] = False

    lines.append("")

    # Alternative: look at the dual - E8 root LINES (120 ±pairs)
    lines.append("## Alternative: E8 Root Lines")
    lines.append("")
    lines.append("E8 has 120 root lines (±pairs). Compare to 160 triangles.")
    lines.append("")

    # Canonical E8 root lines
    def canonical_line(root):
        """Get canonical representative of ±root pair."""
        for i, x in enumerate(root):
            if abs(x) > 1e-9:
                if x < 0:
                    return tuple(-r for r in root)
                return tuple(root)
        return tuple(root)

    e8_lines = set()
    for root in e8_roots:
        e8_lines.add(canonical_line(root))

    results["e8_line_count"] = len(e8_lines)
    lines.append(f"- E8 root lines: {len(e8_lines)}")
    lines.append(f"- W33 triangles: {len(unique_triangles)}")
    lines.append("")

    # Summary
    lines.append("## Summary")
    lines.append("")
    lines.append("| W33 Structure | Count | E8 Structure | Count |")
    lines.append("|---------------|-------|--------------|-------|")
    lines.append(f"| Triangles | 160 | Root lines | 120 |")
    lines.append(f"| Triangle graph edges | 240 | Roots | 240 |")
    lines.append(f"| L(T) vertices | 240 | Roots | 240 |")
    lines.append("")

    if results.get("degree_match"):
        lines.append("**Key finding**: The line graph of the triangle co-occurrence graph")
        lines.append("has 240 vertices with the same degree as E8 root adjacency!")
        lines.append("")
        lines.append("This strongly suggests a structural correspondence.")

    # Write outputs
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(to_native(results), indent=2), encoding="utf-8")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
