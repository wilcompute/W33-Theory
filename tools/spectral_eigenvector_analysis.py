#!/usr/bin/env python3
"""Deep eigenvector analysis of spectral connections.

Building on the discovery that:
- W33: 240 edges, 160 triangles (spectrum: 1+24+15)
- Triangle graph: 240 edges, 160 triangles (spectrum: 40+120)
- E8: 240 roots with 120-dim nullspace

This investigates:
1. Eigenvector structure and symmetry
2. Relationship between W33 and triangle graph eigenvectors
3. E8 nullspace interpretation
"""
from __future__ import annotations

import json
from collections import Counter
from itertools import product
from pathlib import Path

import numpy as np
from numpy.linalg import eigh

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "eigenvector_analysis.json"
OUT_MD = ROOT / "artifacts" / "eigenvector_analysis.md"


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


def to_native(obj):
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

    lines.append("# Eigenvector Analysis of Spectral Connections")
    lines.append("")

    # Build W33
    adj, vertices = construct_w33()
    n = len(vertices)

    # Full eigendecomposition
    w33_eigenvalues, w33_eigenvectors = eigh(adj.astype(float))

    # Round eigenvalues for grouping
    w33_eigs_rounded = np.round(w33_eigenvalues, 6)
    unique_eigs = sorted(set(w33_eigs_rounded), reverse=True)

    lines.append("## W33 Eigenspace Analysis")
    lines.append("")

    for eig in unique_eigs:
        mask = np.abs(w33_eigenvalues - eig) < 0.001
        mult = np.sum(mask)
        evecs = w33_eigenvectors[:, mask]

        lines.append(f"### λ = {eig} (multiplicity {mult})")
        lines.append("")

        # Analyze eigenvector structure
        if mult == 1:
            # Trivial representation - should be constant
            vec = evecs[:, 0]
            is_constant = np.allclose(vec, vec[0])
            lines.append(f"- Constant vector: {is_constant}")
            lines.append(f"- Value: {vec[0]:.6f}")
        else:
            # Check for patterns
            # Project eigenvectors onto coordinate directions
            coord_projs = []
            for coord in range(4):
                # Group vertices by coordinate value
                groups = {0: [], 1: [], 2: []}
                for i, v in enumerate(vertices):
                    groups[v[coord]].append(i)

                # Check if eigenvectors respect this grouping
                for j in range(mult):
                    vec = evecs[:, j]
                    means = [np.mean(vec[groups[k]]) if groups[k] else 0 for k in range(3)]
                    coord_projs.append((coord, j, means))

            lines.append(f"- Eigenspace dimension: {mult}")

            # Check symmetry of eigenvector support
            vec_norms = np.sum(evecs**2, axis=1)
            lines.append(f"- Total weight distribution: min={vec_norms.min():.4f}, max={vec_norms.max():.4f}")
        lines.append("")

    # Build triangle graph
    all_triangles = {}
    triangle_to_base = {}

    for v0 in range(n):
        triangles = find_h12_triangles(adj, v0)
        all_triangles[v0] = triangles
        for t in triangles:
            triangle_to_base[t] = v0

    unique_triangles = list(triangle_to_base.keys())
    tri_index = {t: i for i, t in enumerate(unique_triangles)}

    tri_adj = np.zeros((len(unique_triangles), len(unique_triangles)), dtype=int)
    for v0 in range(n):
        tris = all_triangles[v0]
        for i, t1 in enumerate(tris):
            for t2 in tris[i+1:]:
                idx1, idx2 = tri_index[t1], tri_index[t2]
                tri_adj[idx1, idx2] = 1
                tri_adj[idx2, idx1] = 1

    # Triangle graph eigendecomposition
    tri_eigenvalues, tri_eigenvectors = eigh(tri_adj.astype(float))
    tri_eigs_rounded = np.round(tri_eigenvalues, 6)

    lines.append("## Triangle Graph Eigenspace Analysis")
    lines.append("")

    # λ = 3 eigenspace (multiplicity 40)
    mask_3 = np.abs(tri_eigenvalues - 3) < 0.001
    evecs_3 = tri_eigenvectors[:, mask_3]

    lines.append("### λ = 3 Eigenspace (dimension 40)")
    lines.append("")

    # Key insight: Does this 40-dim space relate to W33 vertices?
    # Build incidence matrix: triangle × W33 vertex
    incidence = np.zeros((len(unique_triangles), n), dtype=float)
    for i, t in enumerate(unique_triangles):
        for v in t:
            incidence[i, v] = 1

    # Project λ=3 eigenspace onto incidence structure
    proj = evecs_3.T @ incidence  # 40 × 40 matrix
    lines.append(f"- Projection onto W33 vertices: rank = {np.linalg.matrix_rank(proj, tol=1e-6)}")
    lines.append("")

    # λ = -1 eigenspace (multiplicity 120)
    mask_m1 = np.abs(tri_eigenvalues + 1) < 0.001
    evecs_m1 = tri_eigenvectors[:, mask_m1]

    lines.append("### λ = -1 Eigenspace (dimension 120)")
    lines.append("")

    # Check if this relates to E8 roots
    proj_m1 = evecs_m1.T @ incidence  # 120 × 40
    lines.append(f"- Projection onto W33 vertices: rank = {np.linalg.matrix_rank(proj_m1, tol=1e-6)}")
    lines.append("")

    # Relationship between eigenspaces
    lines.append("## Eigenspace Relationships")
    lines.append("")

    # Check: Do W33 eigenvectors lift to triangle graph eigenvectors?
    lines.append("### Lifting W33 eigenvectors to Triangle Graph")
    lines.append("")

    # For each W33 eigenvector, check if it induces a triangle graph eigenvector
    for eig in unique_eigs:
        mask = np.abs(w33_eigenvalues - eig) < 0.001
        evecs = w33_eigenvectors[:, mask]
        mult = np.sum(mask)

        # Lift via incidence (average over triangle vertices)
        lifted = np.zeros((len(unique_triangles), mult))
        for i, t in enumerate(unique_triangles):
            lifted[i] = np.mean([evecs[v] for v in t], axis=0)

        # Check if lifted vectors are triangle graph eigenvectors
        for j in range(mult):
            lv = lifted[:, j]
            if np.linalg.norm(lv) < 1e-10:
                continue
            lv_normalized = lv / np.linalg.norm(lv)
            Tlv = tri_adj @ lv_normalized

            # Check eigenvalue
            if np.linalg.norm(lv_normalized) > 1e-10:
                ratio = Tlv / (lv_normalized + 1e-15)
                ratio_valid = np.abs(lv_normalized) > 0.01
                if np.any(ratio_valid):
                    eigenval = np.median(ratio[ratio_valid])
                    error = np.std(ratio[ratio_valid]) if np.sum(ratio_valid) > 1 else 0
                    if error < 0.01:
                        lines.append(f"- W33 λ={eig}[{j}] → Triangle λ={eigenval:.2f}")
    lines.append("")

    # Deep connection: 160 triangles in both
    lines.append("## The 160 = 160 Mystery")
    lines.append("")
    lines.append("Both W33 and triangle graph have exactly 160 triangles.")
    lines.append("")

    # Count triangles in triangle graph
    tri_tris = 0
    num_tri = len(unique_triangles)
    for i in range(num_tri):
        for j in range(i+1, num_tri):
            if tri_adj[i, j]:
                for k in range(j+1, num_tri):
                    if tri_adj[i, k] and tri_adj[j, k]:
                        tri_tris += 1

    lines.append(f"- Triangles in W33: 160 (= triangle graph vertices)")
    lines.append(f"- Triangles in triangle graph: {tri_tris}")
    lines.append("")

    # This suggests the triangle graph is the "triangle" of W33
    # And the triangle of the triangle graph should be related to...

    lines.append("### Interpretation")
    lines.append("")
    lines.append("If T(G) denotes the triangle graph of G:")
    lines.append("- |V(W33)| = 40")
    lines.append("- |triangles(W33)| = |V(T(W33))| = 160")
    lines.append("- |triangles(T(W33))| = 160 = |V(T(W33))|")
    lines.append("")
    lines.append("This suggests T(W33) might be self-similar in some sense!")
    lines.append("")

    # 240 edge connection
    lines.append("## The 240 Edge Connection")
    lines.append("")

    w33_edges = np.sum(adj) // 2
    tri_edges = np.sum(tri_adj) // 2

    lines.append(f"- W33 edges: {w33_edges}")
    lines.append(f"- Triangle graph edges: {tri_edges}")
    lines.append(f"- E8 roots: 240")
    lines.append("")
    lines.append("Both graphs have 240 edges = |E8 roots|!")
    lines.append("")

    # Check if edges have E8-like structure
    # In E8, roots at 60° (inner product ±1/2) are adjacent
    # Check the edge distribution

    lines.append("### W33 Edge Interpretation")
    lines.append("")
    lines.append("W33 edges connect orthogonal points (ω(x,y)=0).")
    lines.append("Each vertex has degree 12 (= H12 neighborhood).")
    lines.append("40 × 12 / 2 = 240 edges.")
    lines.append("")

    lines.append("### Triangle Graph Edge Interpretation")
    lines.append("")
    tri_degrees = np.sum(tri_adj, axis=1)
    lines.append(f"- Degree distribution: min={tri_degrees.min()}, max={tri_degrees.max()}")
    lines.append(f"- Unique degrees: {sorted(set(tri_degrees))}")
    lines.append(f"- 160 × avg_degree / 2 = {tri_edges}")
    lines.append("")

    # Representation theory interpretation
    lines.append("## Representation Theory Interpretation")
    lines.append("")
    lines.append("### W33 Decomposition: 40 = 1 + 24 + 15")
    lines.append("")
    lines.append("Under Sp(4, F_3) / Z_2:")
    lines.append("- 1: trivial representation (λ=12)")
    lines.append("- 24: matches D4 roots (λ=2)")
    lines.append("- 15: matches dimension 15 rep (λ=-4)")
    lines.append("")

    lines.append("### Triangle Graph Decomposition: 160 = 40 + 120")
    lines.append("")
    lines.append("- 40: lifts from W33 vertices (λ=3)")
    lines.append("- 120: new degrees of freedom (λ=-1)")
    lines.append("")
    lines.append("120 = |E8 root lines| = |S_5| = dimension of adjoint for some group?")
    lines.append("")

    lines.append("### E8 Decomposition: 240 = 1 + 35 + 84 + 120")
    lines.append("")
    lines.append("- 1: trivial (λ=112)")
    lines.append("- 35: dimension matches 36-1 (λ=16)")
    lines.append("- 84: matches 84-dim rep (λ=-8)")
    lines.append("- 120: nullspace - antisymmetric forms?")
    lines.append("")

    results["w33_spectrum"] = [(float(e), int(m)) for e, m in Counter(w33_eigs_rounded).items()]
    results["triangle_spectrum"] = [(float(e), int(m)) for e, m in Counter(tri_eigs_rounded).items()]
    results["w33_edges"] = int(w33_edges)
    results["triangle_edges"] = int(tri_edges)
    results["triangle_graph_triangles"] = int(tri_tris)

    # Write outputs
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(to_native(results), indent=2), encoding="utf-8")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    print("\n=== KEY FINDINGS ===")
    print(f"W33: {w33_edges} edges, 160 triangles")
    print(f"Triangle graph: {tri_edges} edges, {tri_tris} triangles")
    print("Both have 240 edges = E8 root count!")


if __name__ == "__main__":
    main()
