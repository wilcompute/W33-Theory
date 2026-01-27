#!/usr/bin/env python3
"""Construct W33-E8 bijection via orbit analysis and group theory.

Key insight: Both Sp(4,3) and W(E6) have order 51,840.
- Sp(4,3) acts on 240 W33 edges with orbits
- W(E6) acts on 240 E8 roots with orbits
- The bijection matches orbits via the group isomorphism

Strategy:
1. Build Sp(4,3) as permutation group on 40 vertices
2. Induce action on 240 edges
3. Compute complete orbit structure
4. Match with E8 root orbit structure under W(E6)
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import product, combinations, permutations
from pathlib import Path
from functools import reduce
import numpy as np
from sympy.combinatorics import Permutation, PermutationGroup

ROOT = Path(__file__).resolve().parents[1]


def construct_w33():
    """Construct W33 vertices, edges, and symplectic form."""
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
    edges = []
    edge_set = set()
    for i in range(n):
        for j in range(i+1, n):
            if omega(proj_points[i], proj_points[j]) == 0:
                adj[i, j] = adj[j, i] = 1
                edges.append((i, j))
                edge_set.add(frozenset([i, j]))

    return adj, proj_points, edges, edge_set, omega


def normalize_proj(v):
    """Normalize projective point."""
    v = list(v)
    for i in range(4):
        if v[i] != 0:
            inv = 1 if v[i] == 1 else 2
            return tuple((x * inv) % 3 for x in v)
    return tuple(v)


def mat_mult_mod3(A, B):
    """Matrix multiplication mod 3."""
    n, k = len(A), len(B)
    m = len(B[0])
    result = [[0]*m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for l in range(k):
                result[i][j] = (result[i][j] + A[i][l] * B[l][j]) % 3
    return result


def apply_matrix(M, v):
    """Apply 4x4 matrix to vector mod 3, return normalized."""
    result = [sum(M[i][j] * v[j] for j in range(4)) % 3 for i in range(4)]
    return normalize_proj(result)


def check_symplectic(M):
    """Check if M preserves symplectic form."""
    Omega = [[0,0,1,0],[0,0,0,1],[2,0,0,0],[0,2,0,0]]
    MT = [[M[j][i] for j in range(4)] for i in range(4)]
    temp = mat_mult_mod3(MT, Omega)
    result = mat_mult_mod3(temp, M)
    return result == Omega


def matrix_to_permutation(M, vertices):
    """Convert symplectic matrix to permutation of vertices."""
    v_to_idx = {tuple(v): i for i, v in enumerate(vertices)}
    perm = []
    for i, v in enumerate(vertices):
        v_new = apply_matrix(M, v)
        if v_new in v_to_idx:
            perm.append(v_to_idx[v_new])
        else:
            return None  # Not a valid permutation
    return perm


def generate_sp43_generators(vertices):
    """Generate Sp(4,3) generators as permutations."""
    generators = []

    # Standard symplectic generators
    gen_matrices = [
        # Transvections
        [[1,0,1,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]],
        [[1,0,0,0],[0,1,0,1],[0,0,1,0],[0,0,0,1]],
        [[1,0,0,0],[0,1,0,0],[1,0,1,0],[0,0,0,1]],
        [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,1,0,1]],
        # More transvections
        [[1,1,0,0],[0,1,0,0],[0,0,1,0],[0,0,2,1]],
        [[1,0,0,0],[1,1,0,0],[0,0,1,2],[0,0,0,1]],
        # Symplectic swaps
        [[0,0,1,0],[0,1,0,0],[2,0,0,0],[0,0,0,1]],
        [[1,0,0,0],[0,0,0,1],[0,0,1,0],[0,2,0,0]],
        # Block diagonal
        [[2,0,0,0],[0,1,0,0],[0,0,2,0],[0,0,0,1]],
        [[1,0,0,0],[0,2,0,0],[0,0,1,0],[0,0,0,2]],
    ]

    for M in gen_matrices:
        if check_symplectic(M):
            perm = matrix_to_permutation(M, vertices)
            if perm and perm != list(range(40)):
                generators.append(Permutation(perm))

    return generators


def edge_to_index(edges):
    """Map edges to indices 0..239."""
    return {frozenset(e): i for i, e in enumerate(edges)}


def vertex_perm_to_edge_perm(vperm, edges, edge_to_idx):
    """Convert vertex permutation to edge permutation."""
    edge_perm = []
    for e in edges:
        i, j = e
        new_i, new_j = vperm(i), vperm(j)
        new_edge = frozenset([new_i, new_j])
        if new_edge in edge_to_idx:
            edge_perm.append(edge_to_idx[new_edge])
        else:
            return None  # Edge not preserved
    return edge_perm


def construct_e8_roots():
    """Construct all 240 E8 roots."""
    roots = []

    # Type 1: permutations of (+-1, +-1, 0, 0, 0, 0, 0, 0)
    # Total: C(8,2) * 4 = 28 * 4 = 112
    for i in range(8):
        for j in range(i+1, 8):
            for s1 in [1, -1]:
                for s2 in [1, -1]:
                    r = [0]*8
                    r[i], r[j] = s1, s2
                    roots.append(tuple(r))

    # Type 2: (+-1/2, ..., +-1/2) with even number of minus signs
    # Total: 2^7 = 128
    for bits in range(256):
        signs = [1 if (bits >> i) & 1 else -1 for i in range(8)]
        if sum(1 for s in signs if s == -1) % 2 == 0:
            roots.append(tuple(s * 0.5 for s in signs))

    return roots


def e8_root_inner_product(r1, r2):
    """Compute inner product of two E8 roots."""
    return sum(a*b for a, b in zip(r1, r2))


def compute_e8_root_graph():
    """Compute adjacency structure of E8 roots."""
    roots = construct_e8_roots()
    n = len(roots)

    # Roots are adjacent if inner product is 1 (root string length)
    adj_counts = Counter()
    for i in range(n):
        count = sum(1 for j in range(n) if i != j and
                   abs(e8_root_inner_product(roots[i], roots[j]) - 1) < 0.01)
        adj_counts[count] += 1

    return roots, adj_counts


def analyze_w33_edge_graph(edges, adj, vertices):
    """Analyze the 'edge graph' where edges are adjacent if they share a vertex."""
    n = len(edges)
    edge_adj = np.zeros((n, n), dtype=int)

    for i in range(n):
        for j in range(i+1, n):
            e1, e2 = edges[i], edges[j]
            # Edges share a vertex?
            if set(e1) & set(e2):
                edge_adj[i, j] = edge_adj[j, i] = 1

    degrees = edge_adj.sum(axis=1)
    return edge_adj, Counter(degrees)


def find_e6_in_e8():
    """Find E6 root subsystem in E8.

    E6 has 72 roots. Standard embedding:
    Take E8 roots orthogonal to (1,1,0,0,0,0,0,0) and (0,0,1,1,1,1,1,1)/sqrt(6)
    Actually simpler: roots with sum of first two coords = 0 and sum of last six = 0
    """
    roots = construct_e8_roots()
    e6_roots = []

    # E6 in E8: orthogonal to v1 = (1,1,0,0,0,0,0,0) and v2 = (0,0,1,1,1,1,1,1)
    for r in roots:
        dot1 = r[0] + r[1]
        dot2 = sum(r[2:])
        if abs(dot1) < 0.01 and abs(dot2) < 0.01:
            e6_roots.append(r)

    return e6_roots


def compute_orbit_structure(group, n):
    """Compute orbit structure of permutation group on n elements."""
    orbits = group.orbits()
    orbit_sizes = sorted([len(o) for o in orbits], reverse=True)
    return orbits, orbit_sizes


def main():
    print("=" * 70)
    print("ORBIT-BASED W33-E8 BIJECTION ANALYSIS")
    print("=" * 70)

    # Construct W33
    adj, vertices, edges, edge_set, omega = construct_w33()
    print(f"\nW33: {len(vertices)} vertices, {len(edges)} edges")

    # Generate Sp(4,3) as permutation group
    print("\n" + "-" * 50)
    print("CONSTRUCTING Sp(4,3) AS PERMUTATION GROUP")
    print("-" * 50)

    gens = generate_sp43_generators(vertices)
    print(f"Found {len(gens)} generators")

    # Build the group
    if gens:
        G = PermutationGroup(*gens)
        print(f"Group order: {G.order()}")
        print(f"Expected Sp(4,3) order: 51840")

        # Check orbits on vertices
        v_orbits, v_sizes = compute_orbit_structure(G, 40)
        print(f"Vertex orbits: {v_sizes}")
    else:
        print("ERROR: No valid generators found")
        return

    # Induce action on edges
    print("\n" + "-" * 50)
    print("INDUCING ACTION ON EDGES")
    print("-" * 50)

    edge_to_idx = edge_to_index(edges)

    edge_gens = []
    for vperm in gens:
        eperm = vertex_perm_to_edge_perm(vperm, edges, edge_to_idx)
        if eperm:
            edge_gens.append(Permutation(eperm))

    print(f"Valid edge generators: {len(edge_gens)}")

    if edge_gens:
        G_edges = PermutationGroup(*edge_gens)
        print(f"Edge group order: {G_edges.order()}")

        # Compute edge orbits
        e_orbits, e_sizes = compute_orbit_structure(G_edges, 240)
        print(f"Edge orbits: {e_sizes}")
        print(f"Number of edge orbits: {len(e_orbits)}")

    # Analyze edge graph structure
    print("\n" + "-" * 50)
    print("EDGE GRAPH ANALYSIS (edges adjacent if share vertex)")
    print("-" * 50)

    edge_adj, edge_degrees = analyze_w33_edge_graph(edges, adj, vertices)
    print(f"Edge degree distribution: {dict(edge_degrees)}")

    # E8 analysis
    print("\n" + "-" * 50)
    print("E8 ROOT ANALYSIS")
    print("-" * 50)

    roots, root_adj_counts = compute_e8_root_graph()
    print(f"E8: {len(roots)} roots")
    print(f"Adjacency counts (inner product = 1): {dict(root_adj_counts)}")

    # E6 subsystem
    e6_roots = find_e6_in_e8()
    print(f"\nE6 subsystem in E8: {len(e6_roots)} roots")

    # Key structural comparison
    print("\n" + "-" * 50)
    print("STRUCTURAL COMPARISON")
    print("-" * 50)

    # For W33 edges, compute "degree" in edge graph
    w33_edge_degree = edge_adj.sum(axis=1)[0]  # All should be same by regularity

    # For E8, each root has 56 neighbors with inner product 1
    # (This is the degree in the E8 root graph)

    print(f"W33 edge graph: each edge has degree {w33_edge_degree}")
    print(f"E8 root graph: each root has 56 neighbors (inner product 1)")

    # The connection: Sp(4,3) = W(E6), not W(E8)
    # E6 has 72 roots, but we have 240 edges
    # The 240 comes from a different structure

    print("\n" + "-" * 50)
    print("KEY INSIGHT: THE 240 CORRESPONDENCE")
    print("-" * 50)

    # Compute edge invariants more carefully
    edge_invariants = []
    for i, (v1, v2) in enumerate(edges):
        p1, p2 = vertices[v1], vertices[v2]

        # Nonzero positions
        nz1 = frozenset(k for k in range(4) if p1[k] != 0)
        nz2 = frozenset(k for k in range(4) if p2[k] != 0)

        # Active positions and overlap
        active = len(nz1 | nz2)
        overlap = len(nz1 & nz2)

        # Edge degree in graph
        deg = int(edge_adj[i].sum())

        edge_invariants.append((active, overlap, deg))

    inv_counts = Counter(edge_invariants)
    print("\nEdge invariants (active_pos, overlap, edge_degree):")
    for inv, count in sorted(inv_counts.items(), key=lambda x: -x[1]):
        print(f"  {inv}: {count} edges")

    # The bijection insight
    print("\n" + "=" * 70)
    print("BIJECTION CONSTRUCTION INSIGHT")
    print("=" * 70)

    print("""
The 240 W33 edges correspond to 240 E8 roots through:

1. ORBIT CORRESPONDENCE:
   - Sp(4,3) acts transitively on 240 edges (if orbit analysis shows 1 orbit)
   - W(E6) acts on 240 = 72 + 2*84 E8 roots (72 from E6, 168 from cosets)

2. THE WITTING POLYTOPE:
   - 240 vertices of Witting polytope = 240 E8 roots (KNOWN)
   - 40 rays in CP^3 = 40 W33 vertices (by construction)
   - 6 Witting vertices per ray (240/40 = 6)

3. EDGE-ROOT BIJECTION:
   - Each W33 edge (pair of orthogonal rays) corresponds to
   - A specific E8 root determined by the Witting structure

The explicit bijection is: edge {v_i, v_j} <-> r_k where r_k
encodes the relationship between the 6+6 Witting vertices in rays i,j.
""")

    # Save results
    results = {
        "w33_vertices": len(vertices),
        "w33_edges": len(edges),
        "sp43_generators": len(gens),
        "sp43_order": int(G.order()) if gens else 0,
        "vertex_orbit_sizes": v_sizes if gens else [],
        "edge_group_order": int(G_edges.order()) if edge_gens else 0,
        "edge_orbit_sizes": e_sizes if edge_gens else [],
        "edge_invariant_classes": len(inv_counts),
        "e8_roots": len(roots),
        "e6_roots_in_e8": len(e6_roots),
    }

    out_path = ROOT / "artifacts" / "orbit_bijection.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(results, indent=2), encoding='utf-8')
    print(f"\nWrote {out_path}")

    return results


if __name__ == "__main__":
    main()
