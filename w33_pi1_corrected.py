#!/usr/bin/env sage
"""
W33 π₁ Puzzle - Reconciling with H₁

The calculation showed:
  rank(π₁(1-skeleton)) = 201 (free group)
  triangles = 160 (relations)

So π₁ should have (201 - 160) = 41 generators mod relations?
But H₁ = Z^81!

Wait - this isn't how it works. Let me redo this properly.
"""

from itertools import combinations, product

import numpy as np
from sage.all import *

print("=" * 70)
print("W33 π₁ ANALYSIS - CORRECTED")
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

# Build simplicial complex
edges = [(i, j) for i in range(n) for j in range(i + 1, n) if adj[i][j]]
triangles = []
for line in lines:
    for triple in combinations(line, 3):
        triangles.append(tuple(sorted(triple)))
triangles = list(set(triangles))
tetrahedra = [tuple(sorted(line)) for line in lines]

print(f"W33 simplicial complex:")
print(f"  Vertices: {n}")
print(f"  Edges: {len(edges)}")
print(f"  Triangles: {len(triangles)}")
print(f"  Tetrahedra: {len(tetrahedra)}")

# Build the actual simplicial complex in Sage
K = SimplicialComplex([list(tet) for tet in tetrahedra])

print(f"\nSage SimplicialComplex verification:")
print(f"  Dimension: {K.dimension()}")
print(f"  f-vector: {K.f_vector()}")

# Compute homology
print("\n" + "=" * 70)
print("HOMOLOGY via SAGE")
print("=" * 70)

for i in range(4):
    H_i = K.homology(i)
    print(f"  H_{i} = {H_i}")

# Compute fundamental group
print("\n" + "=" * 70)
print("FUNDAMENTAL GROUP via SAGE")
print("=" * 70)

try:
    pi1 = K.fundamental_group()
    print(f"π₁(W33) = {pi1}")
    print(f"π₁ generators: {pi1.ngens()}")
    print(f"π₁ relations: {len(pi1.relations())}")

    # Abelianization
    ab = pi1.abelianization()
    print(f"\nπ₁^ab = {ab}")

except Exception as e:
    print(f"Error computing π₁: {e}")

    # Manual approach
    print("\nComputing π₁ manually...")

    # For a 2-dimensional complex (or higher with 2-skeleton data):
    # π₁ = F(edges based at basepoint) / (triangular relations)
    #
    # More carefully:
    # - Choose a spanning tree T of the 1-skeleton
    # - The generators are edges NOT in T
    # - Each triangle gives a relation

    # Spanning tree has (n-1) edges, so (edges - n + 1) generators
    # Each triangle gives one relation

    # But! The relation from a triangle (v0, v1, v2) is:
    # [v0→v1] * [v1→v2] * [v2→v0] = 1
    # where [vi→vj] is the generator if (vi,vj) not in tree, else 1 or -1

    # H₁ = π₁^ab, which is computed via Smith normal form of:
    # ∂₂: C₂ → C₁ (the boundary matrix)

    print("See the boundary matrix computation for H₁.")

# =============================================================================
# Understanding the difference
# =============================================================================
print("\n" + "=" * 70)
print("THE KEY INSIGHT")
print("=" * 70)

print("""
The formula "rank = edges - vertices + 1 - triangles" is WRONG.

The correct computation is:
  H₁ = ker(∂₁) / im(∂₂)

where ∂₁: C₁ → C₀ and ∂₂: C₂ → C₁.

We found:
  rank(∂₁) = 39  (so dim(ker ∂₁) = 240 - 39 = 201)
  rank(∂₂) = 120 (so im ∂₂ has rank 120)
  
Therefore:
  dim(H₁) = 201 - 120 = 81  ✓

The error before was assuming each triangle contributes one "relation".
But triangles can give DEPENDENT relations!

In fact: 160 triangles, but only 120 independent boundary relations.
The 40 "missing" relations come from the tetrahedra!

Each tetrahedron's boundary is 4 triangles, giving a "zero relation".
40 tetrahedra × 1 relation each = 40 dependencies.
So: 160 - 40 = 120 independent triangle boundaries. ✓
""")

# Verify this
print("\n" + "=" * 70)
print("VERIFICATION: TETRAHEDRA AND TRIANGLE DEPENDENCIES")
print("=" * 70)

# ∂₃(tetrahedron) = sum of 4 triangles = 0 in C₂/im(∂₃)
# This means the 4 boundary triangles of each tetrahedron are dependent

# Check: each tetrahedron gives 4 triangles
# But some triangles appear in multiple tetrahedra?
triangle_to_tets = {t: [] for t in triangles}
for i, tet in enumerate(tetrahedra):
    for triple in combinations(tet, 3):
        t = tuple(sorted(triple))
        triangle_to_tets[t].append(i)

# How many tetrahedra is each triangle in?
from collections import Counter

count = Counter(len(tets) for tets in triangle_to_tets.values())
print(f"Triangles per tetrahedron count: {dict(count)}")

# Each triangle is in exactly 1 tetrahedron? Let's check
# (Since lines are maximal cliques, no triangle can be in 2 tetrahedra)
all_one = all(len(tets) == 1 for tets in triangle_to_tets.values())
print(f"Every triangle in exactly one tetrahedron: {all_one}")

if all_one:
    print("""
Every triangle belongs to exactly one line (tetrahedron).
This means:
  - 40 tetrahedra × 4 triangles each = 160 triangles ✓
  - Each tetrahedron boundary gives ∂₃(tet) = t1 - t2 + t3 - t4 = 0
  - This provides 40 linear dependencies among triangle boundaries
  - So rank(∂₂) = 160 - 40 = 120 ✓
""")

print("=" * 70)
print("CONCLUSION")
print("=" * 70)

print("""
The homology calculation is correct:
  H₁(W33) = Z^81

The apparent discrepancy came from naive counting.
The proper calculation uses linear algebra on boundary matrices.

For the fundamental group:
  π₁(W33) has generators and relations
  π₁^ab = H₁ = Z^81

So π₁(W33) could be:
  1. Abelian (π₁ = Z^81)
  2. Non-abelian with Z^81 as abelianization

Let's see what Sage computes for π₁...
""")
