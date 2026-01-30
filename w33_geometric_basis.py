#!/usr/bin/env sage
"""
W33 - GEOMETRIC BASIS FOR H₁ AND π₁

We know π₁(W33) = F₈₁ and H₁ = Z^81 = Steinberg.
Can we find an explicit geometric basis for these 81 generators?

The key: Find 81 independent "cycles" in W33 with geometric meaning.
"""

from itertools import combinations, product

import numpy as np
from sage.all import *

print("=" * 70)
print("GEOMETRIC BASIS FOR H₁(W33)")
print("=" * 70)


# Build the symplectic polar space W(3,3)
def symplectic_form(x, y):
    return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3


def normalize(v):
    for i in range(4):
        if v[i] != 0:
            inv = pow(v[i], -1, 3)
            return tuple((inv * x) % 3 for x in v)
    return None


proj_points = set()
for v in product(range(3), repeat=4):
    if v != (0, 0, 0, 0):
        nv = normalize(v)
        if nv:
            proj_points.add(nv)

proj_points = sorted(proj_points)
n = len(proj_points)

# Adjacency
adj = [[False] * n for _ in range(n)]
for i, p1 in enumerate(proj_points):
    for j, p2 in enumerate(proj_points):
        if i < j and symplectic_form(p1, p2) == 0:
            adj[i][j] = adj[j][i] = True

# Find lines
lines_set = set()
for i in range(n):
    for j in range(i + 1, n):
        if adj[i][j]:
            common = [
                k for k in range(n) if k != i and k != j and adj[i][k] and adj[j][k]
            ]
            for k, l in combinations(common, 2):
                if adj[k][l]:
                    lines_set.add(tuple(sorted([i, j, k, l])))

lines = sorted(lines_set)

# Build graph
G = Graph({i: [j for j in range(n) if adj[i][j]] for i in range(n)})

print(f"W33: {n} points, {len(lines)} lines")
print(f"Graph: {G.num_verts()} vertices, {G.num_edges()} edges")

# =============================================================================
# SPANNING TREE AND FUNDAMENTAL CYCLES
# =============================================================================
print("\n" + "=" * 70)
print("SPANNING TREE ANALYSIS")
print("=" * 70)

# Get a spanning tree
T = G.min_spanning_tree()
T_edges = set((min(e[0], e[1]), max(e[0], e[1])) for e in T)
print(f"Spanning tree has {len(T)} edges (expected: {n-1})")

# Non-tree edges give fundamental cycles
all_edges = set((min(e[0], e[1]), max(e[0], e[1])) for e in G.edges(labels=False))
non_tree_edges = all_edges - T_edges
print(f"Non-tree edges: {len(non_tree_edges)}")
print(f"These give {len(non_tree_edges)} fundamental cycles")

# But wait - we have 240 edges, 39 in tree, so 201 non-tree edges
# But π₁ = F₈₁, so the 160 triangles reduce this to 81
# Let's verify: 201 - 120 (from independent triangle relations) = 81 ✓

print("\n" + "=" * 70)
print("UNDERSTANDING THE 81 GENERATORS")
print("=" * 70)

# The 81 generators of π₁ come from:
# - Start with 201 fundamental cycles (non-tree edges)
# - The 160 triangles give relations
# - But triangles give only 120 independent relations (rank of ∂₂)
# - So 201 - 120 = 81 independent cycles remain

# Question: Which 81 cycles form a basis?

# One approach: use Smith Normal Form to find the kernel of ∂₂

# Build edge index
edges = sorted(all_edges)
edge_idx = {e: i for i, e in enumerate(edges)}

# Build triangle index
triangles = []
for line in lines:
    for triple in combinations(line, 3):
        triangles.append(tuple(sorted(triple)))
triangles = list(set(triangles))
triangle_idx = {t: i for i, t in enumerate(triangles)}

print(f"Edges: {len(edges)}")
print(f"Triangles: {len(triangles)}")

# Build ∂₂: triangles → edges
d2 = matrix(ZZ, len(edges), len(triangles), sparse=True)
for j, (v0, v1, v2) in enumerate(triangles):
    e01 = (min(v0, v1), max(v0, v1))
    e02 = (min(v0, v2), max(v0, v2))
    e12 = (min(v1, v2), max(v1, v2))
    d2[edge_idx[e12], j] = 1
    d2[edge_idx[e02], j] = -1
    d2[edge_idx[e01], j] = 1

print(f"∂₂ matrix: {d2.nrows()} × {d2.ncols()}")
print(f"rank(∂₂) = {d2.rank()}")

# Kernel of ∂₁ (cycles)
# Build ∂₁: edges → vertices
d1 = matrix(ZZ, n, len(edges), sparse=True)
for j, (v0, v1) in enumerate(edges):
    d1[v0, j] = -1
    d1[v1, j] = 1

print(f"∂₁ matrix: {d1.nrows()} × {d1.ncols()}")
print(f"rank(∂₁) = {d1.rank()}")

# H₁ = ker(∂₁) / im(∂₂)
# dim(ker ∂₁) = 240 - 39 = 201
# dim(im ∂₂) = 120
# dim(H₁) = 201 - 120 = 81 ✓

# =============================================================================
# FIND A GEOMETRIC BASIS
# =============================================================================
print("\n" + "=" * 70)
print("FINDING A GEOMETRIC BASIS FOR H₁")
print("=" * 70)

# Approach: Find cycles that are "minimal" in some sense
# One natural choice: induced 4-cycles!

# An induced 4-cycle is: v1 ~ v2 ~ v3 ~ v4 ~ v1, with v1 ≁ v3, v2 ≁ v4
# We found 3240 of these earlier

induced_4cycles = []
for v1 in range(n):
    neighbors_v1 = set(j for j in range(n) if adj[v1][j])
    non_neighbors_v1 = set(j for j in range(n) if j != v1 and not adj[v1][j])

    for v3 in non_neighbors_v1:
        if v3 <= v1:
            continue
        neighbors_v3 = set(j for j in range(n) if adj[v3][j])
        common = neighbors_v1 & neighbors_v3

        for v2 in common:
            for v4 in common:
                if v4 <= v2:
                    continue
                if not adj[v2][v4]:
                    induced_4cycles.append((v1, v2, v3, v4))

print(f"Induced 4-cycles: {len(induced_4cycles)}")


# Convert to cycle vectors (in edge space)
def cycle_to_vector(cycle):
    """Convert a cycle (v1, v2, v3, v4) to a vector in edge space."""
    v1, v2, v3, v4 = cycle
    vec = [0] * len(edges)
    # Edges: v1-v2, v2-v3, v3-v4, v4-v1
    e1 = (min(v1, v2), max(v1, v2))
    e2 = (min(v2, v3), max(v2, v3))
    e3 = (min(v3, v4), max(v3, v4))
    e4 = (min(v4, v1), max(v4, v1))
    vec[edge_idx[e1]] = 1
    vec[edge_idx[e2]] = 1
    vec[edge_idx[e3]] = 1
    vec[edge_idx[e4]] = 1
    return vector(ZZ, vec)


# Check if 4-cycles span H₁
print("\nChecking if induced 4-cycles generate H₁...")

# Build matrix of 4-cycle vectors
M_4cycles = matrix(ZZ, [cycle_to_vector(c) for c in induced_4cycles[:500]])  # Sample
print(f"Sample matrix: {M_4cycles.nrows()} × {M_4cycles.ncols()}")

# This is in the edge space. We need to work modulo im(∂₂)
# Actually, let's just check the rank

# The 4-cycles should be in ker(∂₁) (they're actual cycles)
# Check: d1 * (4-cycle vector) should be 0
sample_cycle = induced_4cycles[0]
v = cycle_to_vector(sample_cycle)
boundary = d1 * v
print(f"Sample 4-cycle boundary: {list(boundary)[:10]}... sum = {sum(boundary)}")
print(f"Is it a cycle (∂=0)? {boundary == 0}")

# Find rank of 4-cycles modulo triangle boundaries
# This is tricky - let's use a different approach

print("\n" + "=" * 70)
print("GEOMETRIC INTERPRETATION: APARTMENTS")
print("=" * 70)

print("""
In building theory, an APARTMENT is a "thin" sub-building.
For Sp(4,3), an apartment corresponds to:
  - A non-degenerate 2-dimensional symplectic subspace of GF(3)⁴
  - This gives a "grid" structure

Let's find the apartments in W33!
""")

# An apartment in W(3,q) is determined by a symplectic basis
# A symplectic basis of GF(3)⁴ is (e1, e2, f1, f2) with:
#   ⟨e1, f1⟩ = 1, ⟨e2, f2⟩ = 1, all other pairings = 0

# The apartment contains:
# - 4 points: [e1], [e2], [f1], [f2] and their linear combinations that are isotropic
# Actually wait, for Sp(4), the apartment is more complex...

# For rank 2 buildings (like Sp(4)), an apartment is an 8-gon (octagon)
# It consists of 4 points and 4 lines in alternating sequence

# Let me find an apartment explicitly
print("\nFinding an apartment (8-cycle in incidence graph)...")

# The incidence graph: vertices = points ∪ lines, edges = incidences
# An apartment is an 8-cycle in this graph

# Build incidence graph
inc_graph = Graph()
for i in range(n):
    inc_graph.add_vertex(("P", i))
for j in range(len(lines)):
    inc_graph.add_vertex(("L", j))
for j, line in enumerate(lines):
    for p in line:
        inc_graph.add_edge(("P", p), ("L", j))

print(
    f"Incidence graph: {inc_graph.num_verts()} vertices, {inc_graph.num_edges()} edges"
)

# Find 8-cycles
# An 8-cycle alternates: P-L-P-L-P-L-P-L
# Starting from a point p0, go to a line L0, then to a different point p1 on L0, etc.


def find_apartment(start_point):
    """Find an apartment starting from a given point."""
    p0 = start_point
    for L0 in [j for j, line in enumerate(lines) if p0 in line]:
        points_on_L0 = list(lines[L0])
        for p1 in points_on_L0:
            if p1 == p0:
                continue
            for L1 in [j for j, line in enumerate(lines) if p1 in line and j != L0]:
                points_on_L1 = list(lines[L1])
                for p2 in points_on_L1:
                    if p2 == p1:
                        continue
                    for L2 in [
                        j for j, line in enumerate(lines) if p2 in line and j != L1
                    ]:
                        points_on_L2 = list(lines[L2])
                        for p3 in points_on_L2:
                            if p3 == p2:
                                continue
                            # Check if p3 and p0 share a line L3 != L2, L0
                            for L3 in [
                                j
                                for j, line in enumerate(lines)
                                if p3 in line and p0 in line
                            ]:
                                if L3 != L2 and L3 != L0:
                                    # Found an apartment!
                                    return [(p0, L0, p1, L1, p2, L2, p3, L3)]
    return None


apt = find_apartment(0)
if apt:
    p0, L0, p1, L1, p2, L2, p3, L3 = apt[0]
    print(f"\nFound apartment:")
    print(f"  Points: {p0}, {p1}, {p2}, {p3}")
    print(f"  Lines:  {L0}, {L1}, {L2}, {L3}")
    print(f"  Lines as point sets: {lines[L0]}, {lines[L1]}, {lines[L2]}, {lines[L3]}")

# Count apartments
apartment_count = 0
apartments = []
seen = set()
for p0 in range(n):
    apt = find_apartment(p0)
    if apt:
        # Normalize apartment (sort by min point)
        pts = tuple(sorted([apt[0][0], apt[0][2], apt[0][4], apt[0][6]]))
        lns = tuple(sorted([apt[0][1], apt[0][3], apt[0][5], apt[0][7]]))
        key = (pts, lns)
        if key not in seen:
            seen.add(key)
            apartments.append(apt[0])
            apartment_count += 1

print(f"\nTotal apartments found: {apartment_count}")

# Actually, for Sp(4,3) there should be exactly (q+1)³ × something apartments
# Let me count more systematically...

print("\n" + "=" * 70)
print("APARTMENT STRUCTURE")
print("=" * 70)

# Each apartment is an octagon with 4 points and 4 lines
# The 4 points form an "opposite pair" structure

if apartments:
    apt = apartments[0]
    p0, L0, p1, L1, p2, L2, p3, L3 = apt
    print(f"\nFirst apartment in detail:")
    print(f"  Point {p0}: {proj_points[p0]}")
    print(f"  Point {p1}: {proj_points[p1]}")
    print(f"  Point {p2}: {proj_points[p2]}")
    print(f"  Point {p3}: {proj_points[p3]}")

    # Check: are opposite points (p0, p2) and (p1, p3) non-collinear?
    print(f"\n  p0 ~ p2? {adj[p0][p2]} (should be False - opposite)")
    print(f"  p1 ~ p3? {adj[p1][p3]} (should be False - opposite)")

    # The 4 lines form a "frame"
    print(f"\n  Line L0 = {lines[L0]}")
    print(f"  Line L1 = {lines[L1]}")
    print(f"  Line L2 = {lines[L2]}")
    print(f"  Line L3 = {lines[L3]}")
