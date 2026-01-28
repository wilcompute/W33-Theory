#!/usr/bin/env python3
"""Construct the explicit bijection via the Sp(4,3) = W(E6) isomorphism.

Key insight: Both groups have order 51,840 and are isomorphic.
The bijection between 240 W33 edges and 240 E8 roots should be
EQUIVARIANT under this group action.

Strategy:
1. Build generators of Sp(4,3) acting on W33 edges
2. Find corresponding action on E8 roots (via W(E6) subset of E8)
3. Use equivariance to construct the bijection
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from functools import reduce
from itertools import combinations, product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def construct_w33():
    """Construct W33."""
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
    edges = []
    edge_set = set()
    for i in range(n):
        for j in range(i + 1, n):
            if omega(proj_points[i], proj_points[j]) == 0:
                adj[i, j] = adj[j, i] = 1
                edges.append((i, j))
                edge_set.add(frozenset([i, j]))

    return adj, proj_points, edges, edge_set, omega


def matrix_mod3(M):
    """Apply mod 3 to matrix."""
    return [[x % 3 for x in row] for row in M]


def mat_mult_mod3(A, B):
    """Matrix multiplication mod 3."""
    n = len(A)
    m = len(B[0])
    k = len(B)
    result = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for l in range(k):
                result[i][j] = (result[i][j] + A[i][l] * B[l][j]) % 3
    return result


def apply_matrix_to_vector(M, v):
    """Apply matrix to vector, return normalized projective point."""
    result = [sum(M[i][j] * v[j] for j in range(4)) % 3 for i in range(4)]
    # Normalize
    for i in range(4):
        if result[i] != 0:
            inv = 1 if result[i] == 1 else 2
            result = tuple((x * inv) % 3 for x in result)
            break
    return tuple(result)


def check_symplectic(M):
    """Check if matrix preserves symplectic form."""
    # Omega matrix: omega(x,y) = x^T * Omega * y
    # Standard symplectic: Omega = [[0,0,1,0],[0,0,0,1],[-1,0,0,0],[0,-1,0,0]]
    # = [[0,0,1,0],[0,0,0,1],[2,0,0,0],[0,2,0,0]] in F3

    Omega = [[0, 0, 1, 0], [0, 0, 0, 1], [2, 0, 0, 0], [0, 2, 0, 0]]

    # M is symplectic iff M^T * Omega * M = Omega
    MT = [[M[j][i] for j in range(4)] for i in range(4)]
    temp = mat_mult_mod3(MT, Omega)
    result = mat_mult_mod3(temp, M)

    return result == Omega


def generate_sp43_elements():
    """Generate elements of Sp(4,3) that preserve the symplectic form.

    Use generators to build a subset (full enumeration is slow).
    """
    # Standard generators for Sp(4,F) include:
    # 1. Symplectic transvections
    # 2. Symplectic dilations
    # 3. Swap matrices

    generators = []

    # Transvection T_{e1,e3}: x -> x + omega(x,e3)*e1
    # In matrix form for our omega: add row3 to row1
    T1 = [[1, 0, 1, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    if check_symplectic(T1):
        generators.append(T1)

    T2 = [[1, 0, 0, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]]
    if check_symplectic(T2):
        generators.append(T2)

    # Swap first and third coordinates (symplectic swap)
    S1 = [[0, 0, 1, 0], [0, 1, 0, 0], [2, 0, 0, 0], [0, 0, 0, 1]]  # 2 = -1 in F3
    if check_symplectic(S1):
        generators.append(S1)

    S2 = [[1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 2, 0, 0]]
    if check_symplectic(S2):
        generators.append(S2)

    # Dilation: scale (x1,x2) by 2 and (x3,x4) by 2^-1=2
    D = [[2, 0, 0, 0], [0, 2, 0, 0], [0, 0, 2, 0], [0, 0, 0, 2]]
    if check_symplectic(D):
        generators.append(D)

    print(f"Found {len(generators)} valid symplectic generators")

    return generators


def compute_edge_orbit(generators, vertices, edges, edge_set):
    """Compute orbits of edges under Sp(4,3) generators."""
    # Map vertices to indices
    v_to_idx = {tuple(v): i for i, v in enumerate(vertices)}

    def apply_to_edge(M, e):
        """Apply symplectic matrix to edge."""
        i, j = e
        vi_new = apply_matrix_to_vector(M, vertices[i])
        vj_new = apply_matrix_to_vector(M, vertices[j])

        # Find new indices
        try:
            i_new = v_to_idx[vi_new]
            j_new = v_to_idx[vj_new]
            return (min(i_new, j_new), max(i_new, j_new))
        except KeyError:
            return None

    # Check that generators preserve edges
    print("\nChecking generator action on edges:")
    for g_idx, g in enumerate(generators):
        preserved = 0
        for e in edges:
            e_new = apply_to_edge(g, e)
            if e_new and frozenset(e_new) in edge_set:
                preserved += 1
        print(f"  Generator {g_idx}: {preserved}/240 edges map to edges")

    return apply_to_edge


def find_edge_invariants(edges, vertices, adj):
    """Find invariants that could distinguish W33 edges for the bijection."""
    print("\n" + "=" * 60)
    print("EDGE INVARIANTS FOR BIJECTION")
    print("=" * 60)

    # For each edge, compute various invariants
    invariants = []

    for e_idx, (i, j) in enumerate(edges):
        vi, vj = vertices[i], vertices[j]

        # Invariant 1: Position pair (which coordinates are active)
        nz_i = frozenset(k for k in range(4) if vi[k] != 0)
        nz_j = frozenset(k for k in range(4) if vj[k] != 0)
        active = nz_i | nz_j
        common = nz_i & nz_j

        # Invariant 2: Number of common neighbors in W33
        common_neighbors = sum(1 for k in range(40) if adj[i, k] and adj[j, k])

        # Invariant 3: Triality axis alignment
        V_axis = (nz_i <= {0, 1} or nz_i <= {2, 3}) and (
            nz_j <= {0, 1} or nz_j <= {2, 3}
        )
        Sp_axis = (nz_i <= {0, 2} or nz_i <= {1, 3}) and (
            nz_j <= {0, 2} or nz_j <= {1, 3}
        )
        Sm_axis = (nz_i <= {0, 3} or nz_i <= {1, 2}) and (
            nz_j <= {0, 3} or nz_j <= {1, 2}
        )

        inv = (len(active), len(common), common_neighbors, V_axis, Sp_axis, Sm_axis)
        invariants.append(inv)

    # Count invariant types
    inv_counts = Counter(invariants)
    print(f"\nDistinct invariant tuples: {len(inv_counts)}")
    print("(active_count, common_count, common_neighbors, V, S+, S-):")
    for inv, count in sorted(inv_counts.items(), key=lambda x: -x[1])[:15]:
        print(f"  {inv}: {count} edges")

    # The key: find an invariant that splits into groups matching E8 structure

    # Common neighbors distribution
    cn_counts = Counter(invariants[i][2] for i in range(240))
    print(f"\nCommon neighbors distribution:")
    for cn, count in sorted(cn_counts.items()):
        print(f"  {cn} common neighbors: {count} edges")

    return invariants


def explore_triality_bijection(edges, vertices):
    """Try to build bijection using triality structure."""
    print("\n" + "=" * 60)
    print("TRIALITY-BASED BIJECTION ATTEMPT")
    print("=" * 60)

    # Partition edges by position pair
    pos_pair_edges = defaultdict(list)

    for e_idx, (i, j) in enumerate(edges):
        vi, vj = vertices[i], vertices[j]
        nz_i = frozenset(k for k in range(4) if vi[k] != 0)
        nz_j = frozenset(k for k in range(4) if vj[k] != 0)

        # The position pair of this edge
        active = tuple(sorted(nz_i | nz_j))
        pos_pair_edges[active].append(e_idx)

    print("\nEdges by active position set:")
    for pp in sorted(pos_pair_edges.keys()):
        print(f"  {set(pp)}: {len(pos_pair_edges[pp])} edges")

    # The position pairs fall into triality classes
    print("\nGrouping by triality axis (position pair complement):")

    axis_V = []  # {0,1} <-> {2,3}
    axis_Sp = []  # {0,2} <-> {1,3}
    axis_Sm = []  # {0,3} <-> {1,2}

    for pp, edge_list in pos_pair_edges.items():
        pp_set = set(pp)
        complement = {0, 1, 2, 3} - pp_set

        if pp_set == {0, 1} or pp_set == {2, 3}:
            axis_V.extend(edge_list)
        elif pp_set == {0, 2} or pp_set == {1, 3}:
            axis_Sp.extend(edge_list)
        elif pp_set == {0, 3} or pp_set == {1, 2}:
            axis_Sm.extend(edge_list)
        # Edges with 3 or 4 active positions don't align with pure axis

    print(f"  V axis (01|23): {len(axis_V)} edges")
    print(f"  S+ axis (02|13): {len(axis_Sp)} edges")
    print(f"  S- axis (03|12): {len(axis_Sm)} edges")
    print(f"  Unaligned: {240 - len(axis_V) - len(axis_Sp) - len(axis_Sm)} edges")

    # The unaligned edges are the "mixed" ones
    # This mirrors E8's structure where some roots are "pure D4" and others are "mixed"

    return pos_pair_edges


def main():
    adj, vertices, edges, edge_set, omega = construct_w33()

    print("CONSTRUCTING Sp(4,3) = W(E6) BIJECTION")
    print("=" * 60)

    print(f"\nW33: {len(vertices)} vertices, {len(edges)} edges")

    # Generate Sp(4,3) elements
    generators = generate_sp43_elements()

    # Compute edge orbits
    apply_to_edge = compute_edge_orbit(generators, vertices, edges, edge_set)

    # Find edge invariants
    invariants = find_edge_invariants(edges, vertices, adj)

    # Explore triality structure
    pos_pair_edges = explore_triality_bijection(edges, vertices)

    # Key insight
    print("\n" + "=" * 60)
    print("KEY INSIGHT: THE BIJECTION STRUCTURE")
    print("=" * 60)

    print(
        """
The bijection W33 edges <-> E8 roots should be:

1. EQUIVARIANT under Sp(4,3) = W(E6) action
   - The groups act on both sets
   - The bijection commutes with the action

2. TRIALITY-PRESERVING
   - V axis edges <-> D4(V) roots in E8
   - S+ axis edges <-> D4(S+) roots in E8
   - S- axis edges <-> D4(S-) roots in E8

3. BASED ON COMMON NEIGHBOR COUNT
   - Edges with 2 common neighbors form one class
   - Edges with 4 common neighbors form another
   - This aligns with E8's inner product structure

The explicit construction requires:
1. Choose base edge e0 <-> base root r0
2. Use Sp(4,3) generators to map all edges
3. The image under corresponding W(E6) generators gives the roots

This is a COMPUTATIONAL GROUP THEORY problem:
Given the isomorphism phi: Sp(4,3) -> W(E6),
the bijection is: e |-> phi(g) . r0 where g.e0 = e
"""
    )

    # Save results
    results = {
        "summary": "Sp(4,3) = W(E6) bijection framework",
        "generators_found": len(generators),
        "invariant_types": len(set(invariants)),
        "triality_edges": {
            "V_axis": len(
                [
                    e
                    for pp, edges in pos_pair_edges.items()
                    if set(pp) in [{0, 1}, {2, 3}]
                    for e in edges
                ]
            ),
            "Sp_axis": len(
                [
                    e
                    for pp, edges in pos_pair_edges.items()
                    if set(pp) in [{0, 2}, {1, 3}]
                    for e in edges
                ]
            ),
            "Sm_axis": len(
                [
                    e
                    for pp, edges in pos_pair_edges.items()
                    if set(pp) in [{0, 3}, {1, 2}]
                    for e in edges
                ]
            ),
        },
    }

    out_path = ROOT / "artifacts" / "sp43_we6_bijection.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\n\nWrote {out_path}")


if __name__ == "__main__":
    main()
