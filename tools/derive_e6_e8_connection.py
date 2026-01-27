#!/usr/bin/env python3
"""Derive the explicit W33 -> E6 -> E8 connection.

Creative exploration to find the structural map.

Key insight: Sp(4,3) = W(E6) both have order 51,840.
This isomorphism should map W33 structures to E6 structures.

E8 decomposes under E6 x SU(3) as:
  248 = (78,1) + (1,8) + (27,3) + (27bar,3bar)

For roots (240):
  240 = 72 + 6 + 81 + 81
      = E6_roots + SU3_roots + 27x3 + 27bar x 3bar

Note: 81 = 3^4 = |F3^4| - our flux configurations!

Strategy:
1. Map F3^4 points to E6 weight space
2. Use the symplectic structure to get edge relations
3. Show this extends to E8 roots
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import product, combinations
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


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
        """Symplectic form on F3^4."""
        return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3

    adj = np.zeros((n, n), dtype=int)
    edges = []
    for i in range(n):
        for j in range(i+1, n):
            if omega(proj_points[i], proj_points[j]) == 0:
                adj[i, j] = adj[j, i] = 1
                edges.append((i, j))

    return adj, proj_points, edges, omega


def build_e6_roots():
    """Build E6 root system (72 roots in R^6).

    E6 roots in the standard basis can be written as:
    - +-e_i +- e_j for i,j in {1..5} (40 roots)
    - +-1/2 * (e_1 +- e_2 +- e_3 +- e_4 +- e_5 +- sqrt(3)*e_6)
      with odd number of minus signs among e_1..e_5 (32 roots)

    Total: 40 + 32 = 72 roots
    """
    roots = []

    # Type 1: +-e_i +- e_j for 1 <= i < j <= 5 (in R^6, using coords 0-4)
    for i in range(5):
        for j in range(i+1, 5):
            for si in [1, -1]:
                for sj in [1, -1]:
                    r = [0]*6
                    r[i] = si
                    r[j] = sj
                    roots.append(tuple(r))

    # Type 2: half-integer with sqrt(3) in 6th coordinate
    sqrt3 = np.sqrt(3)
    for signs in product([1, -1], repeat=5):
        # Odd number of minus signs among first 5
        if sum(1 for s in signs if s == -1) % 2 == 1:
            for s6 in [1, -1]:
                r = [s/2 for s in signs] + [s6 * sqrt3 / 2]
                roots.append(tuple(r))

    return np.array(roots, dtype=float)


def build_e8_roots():
    """Build E8 root system (240 roots in R^8)."""
    roots = []
    for i in range(8):
        for j in range(i+1, 8):
            for si in [1, -1]:
                for sj in [1, -1]:
                    r = [0]*8
                    r[i] = si
                    r[j] = sj
                    roots.append(tuple(r))
    for signs in product([1, -1], repeat=8):
        if sum(1 for s in signs if s == -1) % 2 == 0:
            roots.append(tuple(s/2 for s in signs))
    return np.array(roots, dtype=float)


def f3_to_complex(x):
    """Map F3 element to cube root of unity.

    0 -> 1
    1 -> omega = e^(2pi i/3)
    2 -> omega^2
    """
    omega = np.exp(2j * np.pi / 3)
    return omega ** x


def map_f3_4_to_c4(v):
    """Map F3^4 vector to C^4 using cube roots of unity."""
    return np.array([f3_to_complex(x) for x in v])


def map_f3_4_to_r8(v):
    """Map F3^4 vector to R^8 via C^4 realification."""
    c4 = map_f3_4_to_c4(v)
    r8 = np.zeros(8)
    for i in range(4):
        r8[2*i] = c4[i].real
        r8[2*i+1] = c4[i].imag
    return r8


def explore_f3_to_e6_map(vertices):
    """Explore mappings from F3^4 to E6 weight space."""
    print("\n" + "=" * 60)
    print("EXPLORING F3^4 -> E6 MAPPING")
    print("=" * 60)

    # Map each W33 vertex to R^8 via cube roots
    r8_images = [map_f3_4_to_r8(v) for v in vertices]

    print(f"\n40 W33 vertices mapped to R^8:")

    # Check norms
    norms = [np.linalg.norm(r) for r in r8_images]
    print(f"  Norms: {set(round(n, 4) for n in norms)}")

    # Check inner products
    ip_counts = Counter()
    for i in range(40):
        for j in range(i+1, 40):
            ip = round(np.dot(r8_images[i], r8_images[j]), 4)
            ip_counts[ip] += 1

    print(f"\n  Inner product distribution:")
    for ip, count in sorted(ip_counts.items()):
        print(f"    {ip}: {count} pairs")

    return r8_images


def explore_edge_encoding(edges, vertices):
    """Encode W33 edges as R^8 vectors and compare to E8."""
    print("\n" + "=" * 60)
    print("ENCODING W33 EDGES AS R^8 VECTORS")
    print("=" * 60)

    # For each edge (i,j), create an encoding
    # Idea: Use the tensor product or sum/difference of vertex images

    r8_verts = [map_f3_4_to_r8(v) for v in vertices]

    # Encoding 1: Normalized sum
    edge_sums = []
    for i, j in edges:
        s = r8_verts[i] + r8_verts[j]
        if np.linalg.norm(s) > 0.001:
            s = s / np.linalg.norm(s)
        edge_sums.append(s)

    print(f"\nEdge encoding via normalized sum:")

    # Check inner products
    ip_counts = Counter()
    for k in range(len(edge_sums)):
        for l in range(k+1, len(edge_sums)):
            ip = round(np.dot(edge_sums[k], edge_sums[l]), 4)
            ip_counts[ip] += 1

    print(f"  Inner product distribution ({len(ip_counts)} distinct values):")
    for ip, count in sorted(ip_counts.items())[:10]:
        print(f"    {ip}: {count} pairs")
    if len(ip_counts) > 10:
        print(f"    ... and {len(ip_counts) - 10} more values")

    # Encoding 2: Difference
    edge_diffs = []
    for i, j in edges:
        d = r8_verts[i] - r8_verts[j]
        if np.linalg.norm(d) > 0.001:
            d = d / np.linalg.norm(d)
        edge_diffs.append(d)

    print(f"\nEdge encoding via normalized difference:")

    ip_counts2 = Counter()
    for k in range(len(edge_diffs)):
        for l in range(k+1, len(edge_diffs)):
            ip = round(np.dot(edge_diffs[k], edge_diffs[l]), 4)
            ip_counts2[ip] += 1

    print(f"  Inner product distribution ({len(ip_counts2)} distinct values):")
    for ip, count in sorted(ip_counts2.items())[:10]:
        print(f"    {ip}: {count} pairs")

    return edge_sums, edge_diffs


def explore_81_structure(vertices, omega_func):
    """Explore the 81 = 3^4 structure and its relation to E8.

    Under E6 x SU(3) subset of E8:
      240 = 72 + 6 + 81 + 81

    The 81 comes from 27 x 3 (E6 fundamental tensored with SU(3) triplet).
    Our F3^4 has exactly 81 elements!
    """
    print("\n" + "=" * 60)
    print("THE 81 = 3^4 STRUCTURE")
    print("=" * 60)

    # All 81 elements of F3^4
    F3 = [0, 1, 2]
    all_81 = list(product(F3, repeat=4))

    print(f"\n|F3^4| = {len(all_81)} = 81 = 3^4")
    print(f"  = 27 x 3 (E6 fundamental x SU(3) triplet)")

    # The 40 projective points come from 80 non-zero vectors (paired by scaling)
    # Plus the zero vector
    # 81 = 1 + 80 = 1 + 40*2

    print(f"\n81 = 1 (zero) + 80 (non-zero)")
    print(f"80 non-zero vectors -> 40 projective points (mod F3*)")

    # Can we see the 27 x 3 structure?
    # Idea: The 81 elements split into orbits under some action

    # Check orbit structure under the symplectic group action
    # (This is computationally intensive, so we'll just analyze the structure)

    print(f"\nSymplectic form decomposes F3^4 into:")
    print(f"  - Isotropic vectors: those with omega(v,v)=0 (all, since omega is alternating)")
    print(f"  - Pairs (v,w) with omega(v,w)=0 give W33 edges")

    # The 27 might come from fixing one coordinate
    # Let's check: fixing x_0 = 1 gives 27 vectors
    fixed_x0 = [v for v in all_81 if v[0] == 1]
    print(f"\n  Vectors with x_0=1: {len(fixed_x0)} = 27")

    # These 27 vectors, modulo scaling by F3*, give how many projective points?
    proj_from_27 = set()
    for v in fixed_x0:
        # Normalize
        v = list(v)
        for i in range(4):
            if v[i] != 0:
                inv = 1 if v[i] == 1 else 2
                v = tuple((x * inv) % 3 for x in v)
                break
        proj_from_27.add(v)

    print(f"  -> {len(proj_from_27)} projective points")

    # This is interesting! Let's see the structure
    print(f"\n  The 27 vectors with x_0=1 project to {len(proj_from_27)} points")
    print(f"  because some are related by F3* scaling")

    return all_81


def derive_240_decomposition():
    """Derive how 240 decomposes under E6 x SU(3)."""
    print("\n" + "=" * 60)
    print("E8 DECOMPOSITION UNDER E6 x SU(3)")
    print("=" * 60)

    print("""
The E8 root system decomposes under E6 x SU(3) as:

  240 E8 roots = 72 (E6 roots)
               + 6  (SU(3) roots)
               + 81 (27 x 3)
               + 81 (27bar x 3bar)

Key observations:
  - 72 E6 roots live in R^6
  - 6 SU(3) roots live in R^2 (the remaining directions)
  - 81 = 27 x 3: E6 fundamental (27-dim) tensored with SU(3) triplet
  - 81 = 27bar x 3bar: conjugate representations

Our W33 structure:
  - 40 points in PG(3,3)
  - 240 edges
  - 81 = |F3^4| flux configurations

The connection:
  - The 81 in E8 decomposition = 81 elements of F3^4
  - The 40 projective points = quotient of 80 non-zero vectors by F3*
  - The 240 edges encode symplectic orthogonality
""")

    # Build the explicit count
    print("\nNumerical verification:")
    print(f"  E6 roots: 72")
    print(f"  SU(3) roots: 6")
    print(f"  27 x 3: 81")
    print(f"  27bar x 3bar: 81")
    print(f"  Total: 72 + 6 + 81 + 81 = {72 + 6 + 81 + 81}")


def explore_triality_in_e6(vertices, edges, omega_func):
    """Look for D4 triality structure in E6 decomposition."""
    print("\n" + "=" * 60)
    print("D4 TRIALITY IN E6 STRUCTURE")
    print("=" * 60)

    print("""
E6 contains D5, and D5 contains D4.
D4 has triality: its three 8-dim representations (V, S+, S-) are permuted.

In W33, we found triality via position pair complements:
  V:  (0,1) <-> (2,3)
  S+: (0,2) <-> (1,3)
  S-: (0,3) <-> (1,2)

This matches the symplectic form structure!
The symplectic form pairs coordinates: (0,2) and (1,3).

Let's verify: omega(x,y) = x0*y2 - x2*y0 + x1*y3 - x3*y1
  - Coordinates 0,2 are paired
  - Coordinates 1,3 are paired

The three triality axes correspond to:
  - Splitting R^4 = R^2 + R^2 in three different ways
  - Each splitting gives a D2 x D2 = SO(4) structure
  - The three splittings are permuted by S3 (triality)
""")

    # Verify the symplectic pairing
    print("\nSymplectic coordinate pairings:")
    print("  omega(x,y) = x0*y2 - x2*y0 + x1*y3 - x3*y1")
    print("  Pairs: {0,2} and {1,3}")
    print("  This is the S+ triality axis!")

    # Count edges by their position structure
    axis_V = 0  # Both endpoints have support in {0,1} or {2,3}
    axis_Sp = 0  # Both endpoints have support in {0,2} or {1,3}
    axis_Sm = 0  # Both endpoints have support in {0,3} or {1,2}

    for i, j in edges:
        v1, v2 = vertices[i], vertices[j]
        supp1 = frozenset(k for k in range(4) if v1[k] != 0)
        supp2 = frozenset(k for k in range(4) if v2[k] != 0)

        # Check alignment with triality axes
        V_sets = [frozenset({0,1}), frozenset({2,3})]
        Sp_sets = [frozenset({0,2}), frozenset({1,3})]
        Sm_sets = [frozenset({0,3}), frozenset({1,2})]

        if supp1 in V_sets and supp2 in V_sets:
            axis_V += 1
        if supp1 in Sp_sets and supp2 in Sp_sets:
            axis_Sp += 1
        if supp1 in Sm_sets and supp2 in Sm_sets:
            axis_Sm += 1

    print(f"\nEdges aligned with triality axes:")
    print(f"  V (01|23): {axis_V}")
    print(f"  S+ (02|13): {axis_Sp}")
    print(f"  S- (03|12): {axis_Sm}")


def search_for_bijection(vertices, edges):
    """Search for an explicit bijection to E8 roots."""
    print("\n" + "=" * 60)
    print("SEARCHING FOR EXPLICIT BIJECTION")
    print("=" * 60)

    # Build E8 roots
    e8_roots = build_e8_roots()

    print(f"\nE8 roots: {len(e8_roots)}")
    print(f"W33 edges: {len(edges)}")

    # The key insight: We need a map that respects the 120-line structure
    # on both sides.

    # W33: 240 edges pair into 120 via position-complement
    # E8: 240 roots pair into 120 via antipodal (-r for each r)

    # Let's look at the structure more carefully
    #
    # Idea: Each W33 edge (v1, v2) where omega(v1, v2) = 0
    # can be mapped to an E8 root based on the coordinates of v1, v2

    # Attempt: Map based on the difference v1 - v2 in F3^4
    # then lift to R^8 via cube roots

    print("\nAttempt: Map edge (v1,v2) to R^8 via:")
    print("  r = (v1 - v2) mapped through cube roots")

    edge_r8 = []
    for v1_idx, v2_idx in edges:
        v1 = np.array(vertices[v1_idx])
        v2 = np.array(vertices[v2_idx])
        diff = tuple((v1 - v2) % 3)  # Difference in F3
        r8 = map_f3_4_to_r8(diff)
        edge_r8.append(r8)

    # Check if these form a root-like system
    norms = [np.linalg.norm(r) for r in edge_r8]
    unique_norms = set(round(n, 4) for n in norms)
    print(f"\n  Norms of edge images: {unique_norms}")

    if len(unique_norms) == 1:
        # Normalize and check inner products
        edge_r8_norm = [r / np.linalg.norm(r) if np.linalg.norm(r) > 0.01 else r
                        for r in edge_r8]

        ip_counts = Counter()
        for k in range(len(edge_r8_norm)):
            for l in range(k+1, len(edge_r8_norm)):
                ip = round(np.dot(edge_r8_norm[k], edge_r8_norm[l]), 4)
                ip_counts[ip] += 1

        print(f"  Inner products (normalized):")
        for ip, count in sorted(ip_counts.items()):
            print(f"    {ip}: {count}")

    # Compare to E8 inner products
    e8_norm = e8_roots / np.linalg.norm(e8_roots[0])
    e8_ip_counts = Counter()
    for k in range(len(e8_norm)):
        for l in range(k+1, len(e8_norm)):
            ip = round(np.dot(e8_norm[k], e8_norm[l]), 4)
            e8_ip_counts[ip] += 1

    print(f"\n  E8 inner products (normalized):")
    for ip, count in sorted(e8_ip_counts.items()):
        print(f"    {ip}: {count}")


def main():
    adj, vertices, edges, omega = construct_w33()
    n = len(vertices)

    print("DERIVING THE W33 -> E6 -> E8 CONNECTION")
    print("=" * 60)
    print(f"\nW33: {n} vertices, {len(edges)} edges")
    print(f"E6: 72 roots, Weyl group W(E6) of order 51,840")
    print(f"E8: 240 roots")
    print(f"Key: |Sp(4,3)| = |W(E6)| = 51,840 = |Aut(W33)|")

    # Explore the mappings
    r8_images = explore_f3_to_e6_map(vertices)
    edge_sums, edge_diffs = explore_edge_encoding(edges, vertices)
    all_81 = explore_81_structure(vertices, omega)
    derive_240_decomposition()
    explore_triality_in_e6(vertices, edges, omega)
    search_for_bijection(vertices, edges)

    # Save results
    results = {
        "summary": "W33-E6-E8 connection derivation",
        "key_numbers": {
            "w33_vertices": 40,
            "w33_edges": 240,
            "e6_roots": 72,
            "e8_roots": 240,
            "f3_4_elements": 81,
            "automorphism_order": 51840,
        },
        "e8_decomposition": {
            "e6_roots": 72,
            "su3_roots": 6,
            "27_x_3": 81,
            "27bar_x_3bar": 81,
            "total": 240,
        }
    }

    out_path = ROOT / "artifacts" / "derive_e6_e8_connection.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(results, indent=2), encoding='utf-8')
    print(f"\n\nWrote {out_path}")


if __name__ == "__main__":
    main()
