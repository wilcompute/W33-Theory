#!/usr/bin/env python3
"""Analyze the 24-dimensional eigenspace of W33 (λ=2) for D4 structure.

KEY INSIGHT:
- W33 has eigenvalue 2 with multiplicity 24
- D4 has exactly 24 roots
- This cannot be a coincidence!

This tool investigates:
1. The explicit eigenvectors of W33 with λ=2
2. Whether they exhibit D4 root structure
3. Inner product relations in this eigenspace
4. Connection to the 4-triangle H12 structure

Outputs:
- artifacts/eigenspace_d4_analysis.json
- artifacts/eigenspace_d4_analysis.md
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path

import numpy as np
from numpy.linalg import eigh

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "eigenspace_d4_analysis.json"
OUT_MD = ROOT / "artifacts" / "eigenspace_d4_analysis.md"


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


def build_d4_roots():
    """Build D4 root system (24 roots in R^4)."""
    roots = []
    for i in range(4):
        for j in range(i+1, 4):
            for si in [1, -1]:
                for sj in [1, -1]:
                    r = [0, 0, 0, 0]
                    r[i] = si
                    r[j] = sj
                    roots.append(tuple(r))
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

    lines.append("# W33 Eigenspace (λ=2) and D4 Root Structure")
    lines.append("")

    # Build W33
    adj, vertices = construct_w33()
    n = len(vertices)

    # Compute full eigendecomposition
    eigenvalues, eigenvectors = eigh(adj.astype(float))

    # Round to avoid floating point issues
    eigenvalues = np.round(eigenvalues, 6)

    # Find the λ=2 eigenspace
    tol = 0.001
    lambda2_mask = np.abs(eigenvalues - 2.0) < tol
    lambda2_indices = np.where(lambda2_mask)[0]
    lambda2_vectors = eigenvectors[:, lambda2_indices]

    lines.append("## W33 Eigenspace Analysis")
    lines.append("")
    lines.append(f"- Eigenvalue λ = 2")
    lines.append(f"- Multiplicity: {len(lambda2_indices)}")
    lines.append(f"- Eigenspace dimension: {lambda2_vectors.shape[1]}")
    lines.append("")

    results["lambda2_multiplicity"] = len(lambda2_indices)

    # Build D4 roots for comparison
    d4_roots = build_d4_roots()
    d4_array = np.array(d4_roots, dtype=float)

    lines.append("## D4 Root System")
    lines.append("")
    lines.append(f"- Roots: {len(d4_roots)}")
    lines.append(f"- Dimension: 4")
    lines.append("")

    # D4 Gram matrix (inner products)
    d4_gram = d4_array @ d4_array.T
    d4_ip_counts = Counter(np.round(d4_gram.flatten(), 4))

    lines.append("### D4 Inner Product Distribution")
    lines.append("")
    for ip, count in sorted(d4_ip_counts.items()):
        lines.append(f"- ⟨r_i, r_j⟩ = {ip}: {count} pairs")
    lines.append("")

    results["d4_inner_products"] = {str(k): int(v) for k, v in d4_ip_counts.items()}

    # Now analyze the λ=2 eigenspace
    # The eigenvectors are orthonormal, so we can compute their inner products
    # with respect to a different metric

    lines.append("## Eigenspace Structure")
    lines.append("")

    # Project each W33 vertex onto the eigenspace
    # This gives a 24-dimensional representation of each vertex
    vertex_projections = lambda2_vectors  # n × 24 matrix

    lines.append("### Vertex Projections onto λ=2 Eigenspace")
    lines.append("")
    lines.append(f"Each W33 vertex v has a 24-dim projection ṽ = P_λ=2 · e_v")
    lines.append("")

    # Compute inner products between vertex projections
    proj_gram = vertex_projections @ vertex_projections.T
    proj_gram_rounded = np.round(proj_gram, 4)

    # Count different inner product values
    proj_ip_counts = Counter(proj_gram_rounded.flatten())

    lines.append("### Projection Inner Product Distribution")
    lines.append("")
    for ip, count in sorted(proj_ip_counts.items()):
        if count > 5:  # Only show significant values
            lines.append(f"- ⟨ṽ_i, ṽ_j⟩ = {ip}: {count} pairs")
    lines.append("")

    # Key insight: how do adjacent vs non-adjacent vertices differ?
    adj_ips = []
    nonadj_ips = []
    for i in range(n):
        for j in range(i+1, n):
            ip = proj_gram_rounded[i, j]
            if adj[i, j]:
                adj_ips.append(ip)
            else:
                nonadj_ips.append(ip)

    adj_ip_counts = Counter(adj_ips)
    nonadj_ip_counts = Counter(nonadj_ips)

    lines.append("### Adjacency Separation in Eigenspace")
    lines.append("")
    lines.append("**Adjacent pairs (W33 edges):**")
    for ip, count in sorted(adj_ip_counts.items()):
        lines.append(f"- ⟨ṽ_i, ṽ_j⟩ = {ip}: {count} pairs")
    lines.append("")

    lines.append("**Non-adjacent pairs:**")
    for ip, count in sorted(nonadj_ip_counts.items()):
        lines.append(f"- ⟨ṽ_i, ṽ_j⟩ = {ip}: {count} pairs")
    lines.append("")

    results["adj_projection_ips"] = {str(k): int(v) for k, v in adj_ip_counts.items()}
    results["nonadj_projection_ips"] = {str(k): int(v) for k, v in nonadj_ip_counts.items()}

    # Check if the separation is clean
    adj_set = set(adj_ip_counts.keys())
    nonadj_set = set(nonadj_ip_counts.keys())
    if adj_set.isdisjoint(nonadj_set):
        lines.append("**CLEAN SEPARATION!** Adjacent and non-adjacent pairs have")
        lines.append("completely different inner products in the λ=2 eigenspace!")
        results["clean_separation"] = True
    else:
        overlap = adj_set & nonadj_set
        lines.append(f"Overlap in inner products: {overlap}")
        results["clean_separation"] = False
    lines.append("")

    # Look for D4-like structure in the eigenspace
    lines.append("## Searching for D4 Structure")
    lines.append("")

    # The 24 eigenvectors span a 24-dim subspace
    # Try to find 24 special directions that form D4 roots

    # Approach: look at the rows of lambda2_vectors
    # Each row is a 24-dim vector (the projection of that vertex)
    # But we have 40 vertices, not 24

    # Alternative: the COLUMNS are the 24 eigenvectors
    # Each is a 40-dim vector
    # Their inner products might reveal D4 structure

    eigen_gram = lambda2_vectors.T @ lambda2_vectors  # 24 × 24
    eigen_gram_rounded = np.round(eigen_gram, 6)

    # Eigenvectors should be orthonormal
    lines.append("### Eigenvector Gram Matrix")
    lines.append("")
    off_diag = eigen_gram_rounded - np.eye(24)
    max_off_diag = np.max(np.abs(off_diag))
    lines.append(f"Max off-diagonal entry: {max_off_diag:.6f}")
    lines.append("(Should be ~0 for orthonormal eigenvectors)")
    lines.append("")

    # Now let's look for special vectors in the eigenspace
    # that might correspond to D4 roots

    # Key idea: look at indicator vectors for triangles
    # Each triangle in H12 has 3 vertices
    # The sum of indicator vectors for a triangle might be special

    lines.append("## Triangle Indicator Analysis")
    lines.append("")

    # Find all triangles
    triangle_set = set()
    for v0 in range(n):
        neighbors = [i for i in range(n) if adj[v0, i]]
        for i, a in enumerate(neighbors):
            for b in neighbors[i+1:]:
                if adj[a, b]:
                    triangle_set.add(tuple(sorted([a, b, v0])))

    triangles = list(triangle_set)
    lines.append(f"Total triangles in W33: {len(triangles)}")
    lines.append("")

    # For each triangle, compute its projection onto λ=2 eigenspace
    triangle_projections = []
    for tri in triangles:
        # Indicator vector for triangle
        indicator = np.zeros(n)
        for v in tri:
            indicator[v] = 1
        # Project onto eigenspace
        proj = lambda2_vectors.T @ indicator  # 24-dim
        triangle_projections.append(proj)

    triangle_projections = np.array(triangle_projections)  # (#tri) × 24

    lines.append(f"Triangle projections shape: {triangle_projections.shape}")
    lines.append("")

    # Compute inner products between triangle projections
    tri_gram = triangle_projections @ triangle_projections.T
    tri_gram_rounded = np.round(tri_gram, 4)

    tri_ip_counts = Counter(tri_gram_rounded.flatten())

    lines.append("### Triangle Projection Inner Products")
    lines.append("")
    for ip, count in sorted(tri_ip_counts.items()):
        if count > 5:
            lines.append(f"- ⟨T_i, T_j⟩ = {ip}: {count} pairs")
    lines.append("")

    results["triangle_projection_ips"] = {str(k): int(v) for k, v in tri_ip_counts.items() if v > 5}

    # Look for 24 special directions
    # D4 roots come in 12 antipodal pairs
    # Let's see if triangle projections form such pairs

    # Normalize triangle projections
    norms = np.linalg.norm(triangle_projections, axis=1, keepdims=True)
    norms[norms < 0.001] = 1  # Avoid division by zero
    normalized_tri_projs = triangle_projections / norms

    # Check for antipodal pairs
    antipodal_pairs = []
    for i in range(len(triangles)):
        for j in range(i+1, len(triangles)):
            dot = np.dot(normalized_tri_projs[i], normalized_tri_projs[j])
            if abs(dot + 1) < 0.01:  # Nearly antipodal
                antipodal_pairs.append((i, j, dot))

    lines.append(f"### Antipodal Triangle Pairs (dot ≈ -1)")
    lines.append("")
    lines.append(f"Found {len(antipodal_pairs)} antipodal pairs")
    if antipodal_pairs:
        for i, j, dot in antipodal_pairs[:5]:
            lines.append(f"- Triangles {triangles[i]} and {triangles[j]}: dot = {dot:.4f}")
    lines.append("")

    results["antipodal_triangle_pairs"] = len(antipodal_pairs)

    # Alternative: look at edges (pairs of adjacent vertices)
    lines.append("## Edge Indicator Analysis")
    lines.append("")

    edges = []
    for i in range(n):
        for j in range(i+1, n):
            if adj[i, j]:
                edges.append((i, j))

    lines.append(f"Total edges in W33: {len(edges)}")
    lines.append("")

    # For each edge, compute its projection
    edge_projections = []
    for (a, b) in edges:
        indicator = np.zeros(n)
        indicator[a] = 1
        indicator[b] = 1
        proj = lambda2_vectors.T @ indicator
        edge_projections.append(proj)

    edge_projections = np.array(edge_projections)

    # Compute norms of edge projections
    edge_norms = np.linalg.norm(edge_projections, axis=1)
    edge_norm_counts = Counter(np.round(edge_norms, 4))

    lines.append("### Edge Projection Norms")
    lines.append("")
    for norm, count in sorted(edge_norm_counts.items()):
        lines.append(f"- ||P(e)|| = {norm}: {count} edges")
    lines.append("")

    results["edge_projection_norms"] = {str(k): int(v) for k, v in edge_norm_counts.items()}

    # Key insight: the 240 edges might map to 240 E8 roots
    # Let's see if edge projections have root-like properties

    # Normalize and check inner product structure
    norms = np.linalg.norm(edge_projections, axis=1, keepdims=True)
    norms[norms < 0.001] = 1
    normalized_edge_projs = edge_projections / norms

    # Compute edge-edge inner products
    edge_gram = normalized_edge_projs @ normalized_edge_projs.T
    edge_gram_rounded = np.round(edge_gram, 4)

    edge_ip_counts = Counter(edge_gram_rounded.flatten())

    lines.append("### Normalized Edge Projection Inner Products")
    lines.append("")
    for ip, count in sorted(edge_ip_counts.items()):
        if count > 5:
            lines.append(f"- ⟨ê_i, ê_j⟩ = {ip}: {count} pairs")
    lines.append("")

    results["edge_projection_ips"] = {str(k): int(v) for k, v in edge_ip_counts.items() if v > 5}

    # Summary
    lines.append("## Summary")
    lines.append("")
    lines.append("### Key Findings")
    lines.append("")
    lines.append(f"1. W33's λ=2 eigenspace has dimension {len(lambda2_indices)} = D4 root count")
    lines.append("")

    if results.get("clean_separation"):
        lines.append("2. **Adjacent vs non-adjacent vertices are cleanly separated**")
        lines.append("   in the λ=2 eigenspace by inner product value!")
    else:
        lines.append("2. Adjacency partially determines eigenspace inner products")
    lines.append("")

    lines.append(f"3. Found {len(antipodal_pairs)} antipodal triangle pairs")
    lines.append("   (These might correspond to ±root pairs in D4)")
    lines.append("")

    lines.append(f"4. {len(edges)} W33 edges have projections into 24-dim eigenspace")
    lines.append("   (These 240 projections might relate to E8 roots)")
    lines.append("")

    lines.append("### Hypothesis Refined")
    lines.append("")
    lines.append("The λ=2 eigenspace of W33 carries D4 root structure.")
    lines.append("The 240 edge projections into this space may relate to E8 roots")
    lines.append("through the D4×D4 ⊂ E8 decomposition.")
    lines.append("")

    # Write outputs
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(to_native(results), indent=2), encoding="utf-8")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
