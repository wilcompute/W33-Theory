#!/usr/bin/env python3
"""Investigate E8 correspondence via D4×D4 decomposition.

KEY INSIGHT: E8 contains D4×D4 structure
- E8 has maximal subgroup Spin(8)×Spin(8)/Z2
- D4 has 24 roots and triality automorphism
- W33 eigenvalue 2 has multiplicity 24 (= D4 root count)
- W33 H12 = 4 triangles (4-fold structure matches D4)

This tool investigates:
1. D4 root system structure
2. D4×D4 inside E8
3. How the 240 triangle-graph edges might map to E8 via D4×D4
4. The significance of shared nullspace dimension 120

Outputs:
- artifacts/d4_d4_e8_decomposition.json
- artifacts/d4_d4_e8_decomposition.md
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "d4_d4_e8_decomposition.json"
OUT_MD = ROOT / "artifacts" / "d4_d4_e8_decomposition.md"


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


def build_d4_roots():
    """Build D4 root system (24 roots in R^4).

    D4 roots: all permutations of (±1, ±1, 0, 0)
    """
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


def root_inner_product(r1, r2):
    """Compute inner product of two roots."""
    return sum(a*b for a, b in zip(r1, r2))


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

    lines.append("# D4×D4 Decomposition Approach to E8 Correspondence")
    lines.append("")

    # Build systems
    d4_roots = build_d4_roots()
    e8_roots = build_e8_roots()
    adj, vertices = construct_w33()
    n = len(vertices)

    lines.append("## Root System Comparison")
    lines.append("")
    lines.append("| System | Roots | Dimension |")
    lines.append("|--------|-------|-----------|")
    lines.append(f"| D4 | {len(d4_roots)} | 4 |")
    lines.append(f"| E8 | {len(e8_roots)} | 8 |")
    lines.append(f"| D4×D4 | {len(d4_roots)**2} = 576 | 8 |")
    lines.append("")

    results["d4_root_count"] = len(d4_roots)
    results["e8_root_count"] = len(e8_roots)
    results["d4xd4_pairs"] = len(d4_roots)**2

    # D4 adjacency structure
    d4_adj = np.zeros((24, 24), dtype=int)
    for i, r1 in enumerate(d4_roots):
        for j, r2 in enumerate(d4_roots):
            if i != j:
                ip = root_inner_product(r1, r2)
                if abs(ip) == 1:
                    d4_adj[i, j] = 1

    d4_degree = d4_adj.sum(axis=1)[0]
    d4_edges = d4_adj.sum() // 2

    lines.append("### D4 Root Adjacency (|inner product| = 1)")
    lines.append("")
    lines.append(f"- Degree: {d4_degree}")
    lines.append(f"- Edges: {d4_edges}")
    lines.append("")

    results["d4_adjacency"] = {"degree": int(d4_degree), "edges": int(d4_edges)}

    # E8 = D8 ∪ half-spinor-weight lattice
    # Split E8 into D8 (type 1) and spinor (type 2)
    type1_roots = [r for r in e8_roots if sum(abs(x) == 1 for x in r) == 2]
    type2_roots = [r for r in e8_roots if all(abs(x) == 0.5 for x in r)]

    lines.append("### E8 Root Types")
    lines.append("")
    lines.append(f"- Type 1 (D8 roots): {len(type1_roots)}")
    lines.append(f"- Type 2 (half-spinor): {len(type2_roots)}")
    lines.append(f"- Total: {len(type1_roots) + len(type2_roots)}")
    lines.append("")

    results["e8_type1_count"] = len(type1_roots)
    results["e8_type2_count"] = len(type2_roots)

    # Key ratio: 112/128 vs W33 structure
    lines.append("### Key Number Comparisons")
    lines.append("")
    lines.append("| E8 Structure | Count | W33 Structure | Count |")
    lines.append("|--------------|-------|---------------|-------|")
    lines.append(f"| Type 1 roots | 112 | ? | - |")
    lines.append(f"| Type 2 roots | 128 | ? | - |")
    lines.append(f"| Total roots | 240 | Triangle graph edges | 240 |")
    lines.append(f"| Root lines (±pairs) | 120 | Line graph nullspace | 120 |")
    lines.append("")

    # Analyze the 240 triangle edges more deeply
    # Collect all triangles
    all_triangles = {}
    triangle_to_base = defaultdict(list)

    for v0 in range(n):
        triangles = find_h12_triangles(adj, v0)
        all_triangles[v0] = triangles
        for t in triangles:
            triangle_to_base[t].append(v0)

    unique_triangles = list(triangle_to_base.keys())
    tri_index = {t: i for i, t in enumerate(unique_triangles)}

    # Build triangle edge list with labels
    tri_edges = []
    for v0 in range(n):
        tris = all_triangles[v0]
        for i, t1 in enumerate(tris):
            for j, t2 in enumerate(tris):
                if i < j:
                    idx1, idx2 = tri_index[t1], tri_index[t2]
                    tri_edges.append({
                        "base": v0,
                        "tri1_idx": idx1,
                        "tri2_idx": idx2,
                        "tri1": t1,
                        "tri2": t2,
                        "position_pair": (i, j)  # Which triangles in the H12
                    })

    lines.append("## Triangle Graph Edge Structure")
    lines.append("")
    lines.append(f"- Total edges: {len(tri_edges)}")
    lines.append("")

    # Analyze position pairs (which of the 4 triangles connect)
    position_dist = Counter(e["position_pair"] for e in tri_edges)
    lines.append("### Edge Distribution by Position Pair")
    lines.append("")
    for pair, count in sorted(position_dist.items()):
        lines.append(f"- Triangles {pair}: {count} edges")
    lines.append("")

    results["position_pair_distribution"] = {str(k): v for k, v in position_dist.items()}

    # Each position pair gives 40 edges (one per base vertex)
    # 6 pairs × 40 = 240
    lines.append(f"Total: 6 position pairs × 40 bases = 240 edges ✓")
    lines.append("")

    # Now consider: can we split 240 into 112 + 128?
    lines.append("## Splitting 240 = 112 + 128?")
    lines.append("")
    lines.append("E8 splits as 112 (type 1) + 128 (type 2).")
    lines.append("Can the 240 triangle edges be similarly partitioned?")
    lines.append("")

    # Try various splits
    # Option 1: By position pair (6 groups of 40)
    lines.append("### Option 1: By position pair")
    lines.append("- 6 groups of 40 each")
    lines.append("- No obvious 112+128 split")
    lines.append("")

    # Option 2: By base vertex properties
    # W33 vertices have different positions in the symplectic structure
    lines.append("### Option 2: By base vertex type")
    lines.append("")

    # Check if bases can be split into two types
    # Use the symplectic form to classify vertices
    # A vertex v is "isotropic" if it's in its own perpendicular
    # In projective terms, all points are isotropic in symplectic geometry
    # Try classifying by coordinate structure
    coord_types = defaultdict(list)
    for i, v in enumerate(vertices):
        # Type: number of non-zero coordinates
        t = sum(1 for x in v if x != 0)
        coord_types[t].append(i)

    lines.append("W33 vertices by coordinate structure (# non-zero coords):")
    for t, verts in sorted(coord_types.items()):
        lines.append(f"- {t} non-zero: {len(verts)} vertices")
    lines.append("")

    results["vertex_coord_types"] = {str(k): len(v) for k, v in coord_types.items()}

    # 16 + 24 = 40 (if split into 1-coord and 2+ coords)
    # But we need 14 + 26 or similar for 112+128 = 240 with 6 edges each
    # Actually: we need something that gives 112 = some_count × 6 edges
    # 112 / 6 ≈ 18.67 - doesn't work
    # So the split probably isn't by base vertex

    # Option 3: By triangle pair structure
    lines.append("### Option 3: By triangle intersection pattern")
    lines.append("")

    # Check how triangles from different position pairs relate
    # Do triangles (0,1) vs (2,3) have different properties?

    # First, let's understand the 4 triangles better
    # For a fixed base, are the 4 triangles distinguishable?
    v0 = 0
    base_tris = all_triangles[v0]

    lines.append(f"For base vertex {v0}, the 4 triangles are:")
    for i, t in enumerate(base_tris):
        # Count edges to H27 (non-neighbors of v0)
        non_neighbors = [j for j in range(n) if adj[v0, j] == 0 and j != v0]
        edges_to_h27 = sum(1 for a in t for b in non_neighbors if adj[a, b])
        lines.append(f"  T{i}: {t} - edges to H27: {edges_to_h27}")
    lines.append("")

    # Check if triangles have consistent labeling across all bases
    # i.e., is there a canonical way to label 4 triangles as (T0, T1, T2, T3)?

    lines.append("## D4 Triality and 4-Triangle Labeling")
    lines.append("")
    lines.append("D4 has triality: its 3 fundamental 8-dim representations")
    lines.append("(vector, spinor+, spinor-) are permuted by an order-3 automorphism.")
    lines.append("")
    lines.append("Question: Do the 4 triangles of H12 correspond to D4 nodes?")
    lines.append("")
    lines.append("D4 Dynkin diagram:")
    lines.append("```")
    lines.append("    T1")
    lines.append("    |")
    lines.append("T0--T2--T3")
    lines.append("```")
    lines.append("Or equivalently (star shape):")
    lines.append("```")
    lines.append("  T1")
    lines.append("  |")
    lines.append("  T0")
    lines.append(" / \\")
    lines.append("T2  T3")
    lines.append("```")
    lines.append("")

    # Key insight: 24 D4 roots = W33 eigenvalue-2 multiplicity
    lines.append("### Connection to W33 Spectrum")
    lines.append("")
    lines.append("W33 eigenvalue structure:")
    lines.append("- λ = 12: multiplicity 1")
    lines.append("- λ = 2: multiplicity **24** (= D4 root count!)")
    lines.append("- λ = -4: multiplicity 15")
    lines.append("")
    lines.append("The 24 eigenvectors with eigenvalue 2 may correspond to D4 roots!")
    lines.append("")

    # Compute W33 spectrum to confirm
    eigenvalues = np.linalg.eigvalsh(adj)
    eigenvalues = np.round(eigenvalues, 4)
    eig_mults = Counter(eigenvalues)

    lines.append("Confirmed W33 spectrum:")
    for e, m in sorted(eig_mults.items(), reverse=True):
        lines.append(f"- λ = {e}: multiplicity {m}")
    lines.append("")

    results["w33_spectrum"] = {str(float(e)): int(m) for e, m in eig_mults.items()}

    # The eigenvectors with eigenvalue 2 form a 24-dim space
    # This space might have D4 structure

    lines.append("## Alternative: 120 and the Nullspace")
    lines.append("")
    lines.append("Both the triangle line graph L(T) and E8 root graph have")
    lines.append("eigenvalue 0 with multiplicity 120.")
    lines.append("")
    lines.append("120 = E8 root lines (±pairs)")
    lines.append("120 = 240/2")
    lines.append("")
    lines.append("This shared dimension might indicate a deeper connection")
    lines.append("at the level of root LINES rather than individual roots.")
    lines.append("")

    # E8 root lines: each root r has -r, forming 120 lines
    # Triangle graph edges: is there a natural involution?
    lines.append("### Involution on Triangle Edges")
    lines.append("")
    lines.append("Is there a natural pairing of the 240 triangle edges into 120 pairs?")
    lines.append("")

    # One natural involution: swap the two triangles in each edge
    # But this doesn't give a new edge - the edge is unordered
    # Another idea: for edge (T_i, T_j) at base v0, is there a "dual" edge?

    # Check if position pairs have natural duals
    # (0,1) ↔ (2,3), (0,2) ↔ (1,3), (0,3) ↔ (1,2)
    lines.append("Position pair complement structure:")
    lines.append("- (0,1) ↔ (2,3): both have 40 edges")
    lines.append("- (0,2) ↔ (1,3): both have 40 edges")
    lines.append("- (0,3) ↔ (1,2): both have 40 edges")
    lines.append("")
    lines.append("This gives 3 pairs of position pairs, total 120 + 120 = 240.")
    lines.append("Could map to 120 E8 root lines!")
    lines.append("")

    results["position_pair_duality"] = {
        "(0,1)↔(2,3)": 80,
        "(0,2)↔(1,3)": 80,
        "(0,3)↔(1,2)": 80
    }

    # Summary
    lines.append("## Summary and Hypothesis")
    lines.append("")
    lines.append("### Structural Parallels")
    lines.append("")
    lines.append("| W33 | Count | E8 | Count |")
    lines.append("|-----|-------|-----|-------|")
    lines.append("| Vertices | 40 | ? | - |")
    lines.append("| H12 triangles | 4 per vertex | D4 nodes | 4 |")
    lines.append("| Total triangles | 160 | ? | - |")
    lines.append("| Triangle edges | 240 | Roots | 240 |")
    lines.append("| Eigenvalue-2 mult | 24 | D4 roots | 24 |")
    lines.append("| Position pair groups | 6 × 40 | ? | - |")
    lines.append("| Nullspace dim (L(T)) | 120 | Root lines | 120 |")
    lines.append("")

    lines.append("### Hypothesis")
    lines.append("")
    lines.append("The correspondence might be:")
    lines.append("")
    lines.append("1. **D4 level**: 24 W33 eigenvectors (λ=2) ↔ 24 D4 roots")
    lines.append("")
    lines.append("2. **E8 level**: 240 triangle edges ↔ 240 E8 roots")
    lines.append("   - Not via graph isomorphism (different degrees)")
    lines.append("   - Possibly via shared combinatorial structure")
    lines.append("")
    lines.append("3. **Line level**: 120 position-pair orbits ↔ 120 E8 root lines")
    lines.append("   - Each base vertex contributes 6 edges")
    lines.append("   - 40 bases × 6 = 240")
    lines.append("   - Position pairs naturally group into 3 complementary pairs")
    lines.append("")

    lines.append("### Open Questions")
    lines.append("")
    lines.append("1. Can we explicitly construct a bijection 240 edges ↔ 240 E8 roots?")
    lines.append("2. What structure is preserved under such a bijection?")
    lines.append("3. How does the D4 triality act on the 4 triangles?")
    lines.append("4. Is the 112+128 split reflected in the triangle edges?")
    lines.append("")

    # Write outputs
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(to_native(results), indent=2), encoding="utf-8")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
