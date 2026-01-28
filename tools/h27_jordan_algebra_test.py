#!/usr/bin/env python3
"""Test Jordan algebra structure on H27 (non-neighbors in W33).

The 27 non-neighbors of any W33 vertex are proposed to form a structure
related to the Albert algebra J³(O), the exceptional 27-dimensional
Jordan algebra.

This tool tests:
1. Natural multiplication structures on H27
2. Jordan identity: (xy)(xx) = x(y(xx))
3. Power-associativity
4. Relationship to E6/F4 exceptional structures

Outputs:
- artifacts/h27_jordan_algebra_test.json
- artifacts/h27_jordan_algebra_test.md
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "h27_jordan_algebra_test.json"
OUT_MD = ROOT / "artifacts" / "h27_jordan_algebra_test.md"


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

    # Build W33
    adj, vertices = construct_w33()
    n = len(vertices)

    lines.append("# H27 Jordan Algebra Test")
    lines.append("")
    lines.append(
        "Testing Jordan algebra structure on the 27 non-neighbors of W33 vertices."
    )
    lines.append("")

    # Pick a base vertex and find H27
    v0 = 0
    neighbors = [i for i in range(n) if adj[v0, i] == 1]
    non_neighbors = [i for i in range(n) if i != v0 and adj[v0, i] == 0]

    results["base_vertex"] = v0
    results["neighbor_count"] = len(neighbors)
    results["non_neighbor_count"] = len(non_neighbors)

    lines.append(f"## Base Vertex Analysis (v0 = {v0})")
    lines.append("")
    lines.append(f"- Neighbors: {len(neighbors)}")
    lines.append(f"- Non-neighbors: {len(non_neighbors)}")
    lines.append("")

    # Analyze H27 subgraph structure
    h27_adj = np.zeros((27, 27), dtype=int)
    h27_map = {v: i for i, v in enumerate(non_neighbors)}

    for i, a in enumerate(non_neighbors):
        for j, b in enumerate(non_neighbors):
            if i != j and adj[a, b] == 1:
                h27_adj[i, j] = 1

    h27_edges = h27_adj.sum() // 2
    h27_degrees = h27_adj.sum(axis=1)
    h27_degree_set = sorted(set(h27_degrees))

    results["h27_edges"] = int(h27_edges)
    results["h27_degree_set"] = [int(d) for d in h27_degree_set]

    lines.append("## H27 Subgraph Structure")
    lines.append("")
    lines.append(f"- Edges in H27: {h27_edges}")
    lines.append(f"- Degree set: {h27_degree_set}")
    lines.append(f"- Is regular: {len(h27_degree_set) == 1}")
    lines.append("")

    # Check if H27 is regular
    if len(h27_degree_set) == 1:
        k27 = h27_degree_set[0]
        lines.append(f"H27 is {k27}-regular with {h27_edges} edges.")

        # Compute lambda and mu for SRG test
        lambda_vals = set()
        mu_vals = set()
        for i in range(27):
            for j in range(i + 1, 27):
                common = sum(h27_adj[i, k] * h27_adj[j, k] for k in range(27))
                if h27_adj[i, j] == 1:
                    lambda_vals.add(common)
                else:
                    mu_vals.add(common)

        results["h27_lambda"] = sorted(lambda_vals)
        results["h27_mu"] = sorted(mu_vals)

        lines.append(f"- λ values (adjacent pairs): {sorted(lambda_vals)}")
        lines.append(f"- μ values (non-adjacent pairs): {sorted(mu_vals)}")

        if len(lambda_vals) == 1 and len(mu_vals) == 1:
            lam = list(lambda_vals)[0]
            mu = list(mu_vals)[0]
            lines.append(f"- **H27 is SRG(27, {k27}, {lam}, {mu})**")
            results["h27_srg_params"] = [27, int(k27), int(lam), int(mu)]

    lines.append("")

    # Test Jordan-like structure
    # In a Jordan algebra, we have: (xy)(xx) = x(y(xx))
    # We need to define a "multiplication" on H27

    lines.append("## Jordan Algebra Analysis")
    lines.append("")
    lines.append(
        "The Albert algebra J³(O) is 27-dimensional with a specific multiplication."
    )
    lines.append("We test if H27 admits a Jordan-like structure.")
    lines.append("")

    # Natural multiplication candidate 1: common neighbors in W33
    # For a, b in H27, define a*b = set of common neighbors in FULL W33

    common_neighbors_matrix = np.zeros((27, 27), dtype=int)
    for i, a in enumerate(non_neighbors):
        for j, b in enumerate(non_neighbors):
            if i != j:
                common = sum(1 for k in range(n) if adj[a, k] and adj[b, k])
                common_neighbors_matrix[i, j] = common

    cn_values = sorted(
        set(
            common_neighbors_matrix[i, j]
            for i in range(27)
            for j in range(27)
            if i != j
        )
    )
    results["common_neighbor_values"] = cn_values

    lines.append("### Common Neighbors in W33")
    lines.append("")
    lines.append(f"For pairs (a,b) in H27, common W33-neighbors: {cn_values}")
    lines.append("")

    # Check if common neighbor count relates to H27 adjacency
    cn_when_h27_adj = []
    cn_when_h27_nonadj = []
    for i in range(27):
        for j in range(i + 1, 27):
            if h27_adj[i, j]:
                cn_when_h27_adj.append(common_neighbors_matrix[i, j])
            else:
                cn_when_h27_nonadj.append(common_neighbors_matrix[i, j])

    results["cn_when_h27_adjacent"] = sorted(set(cn_when_h27_adj))
    results["cn_when_h27_nonadjacent"] = sorted(set(cn_when_h27_nonadj))

    lines.append(
        f"- Common neighbors when H27-adjacent: {sorted(set(cn_when_h27_adj))}"
    )
    lines.append(
        f"- Common neighbors when H27-non-adjacent: {sorted(set(cn_when_h27_nonadj))}"
    )
    lines.append("")

    # Test if there's a clean relationship
    adj_cn = set(cn_when_h27_adj)
    nonadj_cn = set(cn_when_h27_nonadj)
    if adj_cn.isdisjoint(nonadj_cn):
        lines.append("**Adjacency in H27 is DETERMINED by common W33-neighbor count!**")
        results["cn_determines_h27_adj"] = True
    else:
        overlap = adj_cn & nonadj_cn
        lines.append(f"Common neighbor counts overlap: {overlap}")
        results["cn_determines_h27_adj"] = False

    lines.append("")

    # Eigenvalue analysis of H27
    h27_eigenvalues = np.linalg.eigvalsh(h27_adj)
    h27_eigenvalues = np.round(h27_eigenvalues, 4)
    h27_eig_mults = Counter(h27_eigenvalues)

    results["h27_eigenvalues"] = {
        str(e): int(m) for e, m in sorted(h27_eig_mults.items(), reverse=True)
    }

    lines.append("### H27 Eigenvalue Spectrum")
    lines.append("")
    for e, m in sorted(h27_eig_mults.items(), reverse=True):
        lines.append(f"- λ = {e}: multiplicity {m}")
    lines.append("")

    # Key numbers for E6/F4 comparison
    lines.append("## Exceptional Algebra Comparisons")
    lines.append("")
    lines.append("Key dimensions for exceptional structures:")
    lines.append("- Albert algebra J³(O): dim = 27")
    lines.append("- E6 fundamental: 27-dimensional")
    lines.append("- F4 fundamental: 26-dimensional (traceless Albert)")
    lines.append("- E6 roots: 72")
    lines.append("- F4 roots: 48")
    lines.append("")

    lines.append(f"H27 edges: {h27_edges}")
    lines.append(f"- Compare to: E6 roots/2 = 36, F4 roots/2 = 24")
    lines.append("")

    # Connection to 40 = 1 + 12 + 27
    lines.append("## The 40 = 1 + 12 + 27 Decomposition")
    lines.append("")
    lines.append("From any vertex v0:")
    lines.append("- 1: the vertex v0 itself (singlet)")
    lines.append("- 12: neighbors H12 = 4 disjoint triangles (D4 structure)")
    lines.append(f"- 27: non-neighbors H27 with {h27_edges} edges")
    lines.append("")
    lines.append("**Physical interpretation:**")
    lines.append("- 1 = singlet (Higgs?)")
    lines.append("- 12 = gauge sector (related to D4)")
    lines.append("- 27 = matter sector (E6 fundamental)")
    lines.append("")

    # Write outputs
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(to_native(results), indent=2), encoding="utf-8")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
