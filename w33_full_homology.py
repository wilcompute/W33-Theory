#!/usr/bin/env sage
"""
W33 Higher Homology Analysis

We know H_1(W33) = 81-dimensional Steinberg representation.
What about H_0, H_2, H_3?

Euler characteristic: χ = V - E + F - T = 40 - 240 + 160 - 40 = -80
χ = b_0 - b_1 + b_2 - b_3 = 1 - 81 + b_2 - b_3 = -80
So: b_2 - b_3 = -80 + 81 - 1 = 0

Either b_2 = b_3 = 0, or they're equal and nonzero.
Let's compute them!
"""

import json
from itertools import combinations

import numpy as np
from scipy.sparse import csr_matrix, lil_matrix
from scipy.sparse.linalg import svds

print("=" * 70)
print("W33 COMPLETE HOMOLOGY ANALYSIS")
print("=" * 70)

# Load W33 data - reconstruct from the incidence H1 file
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(script_dir, "data", "w33_sage_incidence_h1.json")

with open(data_file, "r") as f:
    data = json.load(f)

# Extract the lines from the first generator's structure
# We need to reconstruct the incidence from the JSON
# The file has generators with point and line permutations

# Actually, let's construct the symplectic polar space directly
# since we now know that's what W33 is

# Build GF(3)^4 symplectic geometry
from itertools import product


# Symplectic form: <x,y> = x1*y3 - x3*y1 + x2*y4 - x4*y2
def symplectic_form(x, y):
    return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3


# Get all projective points of PG(3,3)
# A projective point is a 1-dimensional subspace, represented by
# the lexicographically smallest nonzero representative
def normalize(v):
    """Normalize to projective representative."""
    for i in range(4):
        if v[i] != 0:
            inv = pow(v[i], -1, 3)  # multiplicative inverse mod 3
            return tuple((inv * x) % 3 for x in v)
    return None


proj_points = set()
for v in product(range(3), repeat=4):
    if v != (0, 0, 0, 0):
        nv = normalize(v)
        if nv:
            proj_points.add(nv)

proj_points = sorted(proj_points)
point_to_idx = {p: i for i, p in enumerate(proj_points)}
n_points = len(proj_points)

print(f"Projective points in PG(3,3): {n_points}")

# Build adjacency: two points are collinear if orthogonal under symplectic form
adj = [[False] * n_points for _ in range(n_points)]
for i, p1 in enumerate(proj_points):
    for j, p2 in enumerate(proj_points):
        if i < j:
            if symplectic_form(p1, p2) == 0:
                adj[i][j] = True
                adj[j][i] = True

# Count neighbors per point
degrees = [sum(row) for row in adj]
print(
    f"Degree distribution: min={min(degrees)}, max={max(degrees)}, avg={sum(degrees)/len(degrees):.1f}"
)

# Find lines (totally isotropic 2-spaces = sets of 4 mutually orthogonal points)
# A line is a maximal clique in the collinearity graph
lines = []
for i in range(n_points):
    for j in range(i + 1, n_points):
        if adj[i][j]:
            # Find all points collinear with both i and j
            common = [
                k
                for k in range(n_points)
                if k != i and k != j and adj[i][k] and adj[j][k]
            ]
            # Check which form a 4-clique
            for k in common:
                for l in common:
                    if l > k and adj[k][l]:
                        line = tuple(sorted([i, j, k, l]))
                        if line not in lines:
                            # Verify it's a maximal clique
                            is_clique = all(
                                adj[a][b] or a == b for a in line for b in line
                            )
                            if is_clique:
                                lines.append(line)

lines = list(set(lines))
print(f"Lines (totally isotropic 2-spaces): {len(lines)}")

# Set up for homology computation
points = list(range(n_points))
n = n_points

# Build simplicial complex
# 0-simplices: points (vertices)
# 1-simplices: collinear pairs (edges)
# 2-simplices: collinear triples (triangles)
# 3-simplices: lines (each line = 4 mutually collinear points)

# Point graph adjacency
n = len(points)
adj = [[False] * n for _ in range(n)]
for line in lines:
    for i in range(4):
        for j in range(i + 1, 4):
            adj[line[i]][line[j]] = True
            adj[line[j]][line[i]] = True

# Generate simplices
vertices = list(range(n))
edges = []
for i in range(n):
    for j in range(i + 1, n):
        if adj[i][j]:
            edges.append((i, j))

triangles = []
for line in lines:
    for triple in combinations(line, 3):
        triangles.append(tuple(sorted(triple)))
triangles = list(set(triangles))

tetrahedra = [tuple(sorted(line)) for line in lines]

print(f"\nSimplex counts:")
print(f"  0-simplices (vertices):   {len(vertices)}")
print(f"  1-simplices (edges):      {len(edges)}")
print(f"  2-simplices (triangles):  {len(triangles)}")
print(f"  3-simplices (tetrahedra): {len(tetrahedra)}")

chi = len(vertices) - len(edges) + len(triangles) - len(tetrahedra)
print(f"\nEuler characteristic: χ = {chi}")

# Build boundary matrices
print("\n" + "=" * 70)
print("COMPUTING BOUNDARY MATRICES")
print("=" * 70)

# Index the simplices
v_idx = {v: i for i, v in enumerate(vertices)}
e_idx = {e: i for i, e in enumerate(edges)}
t_idx = {t: i for i, t in enumerate(triangles)}
tet_idx = {tet: i for i, tet in enumerate(tetrahedra)}

# ∂_1: edges → vertices
print(f"\n∂_1: C_1 → C_0, matrix {len(vertices)} × {len(edges)}")
d1 = np.zeros((len(vertices), len(edges)), dtype=np.float64)
for j, (v0, v1) in enumerate(edges):
    d1[v0, j] = -1
    d1[v1, j] = 1

# ∂_2: triangles → edges
print(f"∂_2: C_2 → C_1, matrix {len(edges)} × {len(triangles)}")
d2 = np.zeros((len(edges), len(triangles)), dtype=np.float64)
for j, (v0, v1, v2) in enumerate(triangles):
    # Boundary: (v1,v2) - (v0,v2) + (v0,v1)
    e01 = (min(v0, v1), max(v0, v1))
    e02 = (min(v0, v2), max(v0, v2))
    e12 = (min(v1, v2), max(v1, v2))
    d2[e_idx[e12], j] = 1  # (v1,v2) with sign +1
    d2[e_idx[e02], j] = -1  # (v0,v2) with sign -1
    d2[e_idx[e01], j] = 1  # (v0,v1) with sign +1

# ∂_3: tetrahedra → triangles
print(f"∂_3: C_3 → C_2, matrix {len(triangles)} × {len(tetrahedra)}")
d3 = np.zeros((len(triangles), len(tetrahedra)), dtype=np.float64)
for j, (v0, v1, v2, v3) in enumerate(tetrahedra):
    # Boundary: (v1,v2,v3) - (v0,v2,v3) + (v0,v1,v3) - (v0,v1,v2)
    t123 = tuple(sorted([v1, v2, v3]))
    t023 = tuple(sorted([v0, v2, v3]))
    t013 = tuple(sorted([v0, v1, v3]))
    t012 = tuple(sorted([v0, v1, v2]))
    d3[t_idx[t123], j] = 1
    d3[t_idx[t023], j] = -1
    d3[t_idx[t013], j] = 1
    d3[t_idx[t012], j] = -1

# Verify ∂∂ = 0
print("\nVerifying ∂∂ = 0:")
print(f"  ||∂_1 ∂_2|| = {np.linalg.norm(d1 @ d2):.2e}")
print(f"  ||∂_2 ∂_3|| = {np.linalg.norm(d2 @ d3):.2e}")

print("\n" + "=" * 70)
print("COMPUTING HOMOLOGY GROUPS")
print("=" * 70)

# H_0 = ker(∂_0) / im(∂_1) = Z^n / im(∂_1)
# rank H_0 = n - rank(∂_1)
rank_d1 = np.linalg.matrix_rank(d1)
b0 = len(vertices) - rank_d1
print(f"\nb_0 = {len(vertices)} - rank(∂_1) = {len(vertices)} - {rank_d1} = {b0}")

# H_1 = ker(∂_1) / im(∂_2)
# rank H_1 = dim(ker ∂_1) - rank(∂_2) = (n_edges - rank ∂_1) - rank ∂_2
rank_d2 = np.linalg.matrix_rank(d2)
dim_ker_d1 = len(edges) - rank_d1
b1 = dim_ker_d1 - rank_d2
print(f"b_1 = dim(ker ∂_1) - rank(∂_2) = ({len(edges)} - {rank_d1}) - {rank_d2} = {b1}")

# H_2 = ker(∂_2) / im(∂_3)
rank_d3 = np.linalg.matrix_rank(d3)
dim_ker_d2 = len(triangles) - rank_d2
b2 = dim_ker_d2 - rank_d3
print(
    f"b_2 = dim(ker ∂_2) - rank(∂_3) = ({len(triangles)} - {rank_d2}) - {rank_d3} = {b2}"
)

# H_3 = ker(∂_3)
dim_ker_d3 = len(tetrahedra) - rank_d3
b3 = dim_ker_d3
print(f"b_3 = dim(ker ∂_3) = {len(tetrahedra)} - {rank_d3} = {b3}")

print("\n" + "=" * 70)
print("BETTI NUMBERS")
print("=" * 70)
print(f"""
  b_0 = {b0}   (connected components)
  b_1 = {b1}  (1-cycles)
  b_2 = {b2}   (2-cycles / voids)
  b_3 = {b3}   (3-cycles)

  χ = b_0 - b_1 + b_2 - b_3 = {b0} - {b1} + {b2} - {b3} = {b0 - b1 + b2 - b3}
  Expected χ = {chi}
  Match: {b0 - b1 + b2 - b3 == chi}
""")

# Analysis
print("=" * 70)
print("INTERPRETATION")
print("=" * 70)

if b2 == 0 and b3 == 0:
    print("""
W33 has:
  • H_0 = Z    (connected)
  • H_1 = Z^81 (the Steinberg representation!)
  • H_2 = 0    (no 2-dimensional "voids")
  • H_3 = 0    (no 3-dimensional "cavities")

This means W33 is homologically 1-dimensional:
  - All interesting topology is in H_1
  - The 40 tetrahedra are boundaries (they "fill in" all potential H_2, H_3)
  
This is consistent with W33 being the clique complex of a graph.
Clique complexes are often "aspherical" in higher dimensions.
""")

    print("The ENTIRE homological content of W33 is the Steinberg representation!")

elif b2 > 0:
    print(f"\nSurprise! H_2 has rank {b2}. This needs investigation.")
elif b3 > 0:
    print(f"\nSurprise! H_3 has rank {b3}. This needs investigation.")

print("\n" + "=" * 70)
print("BOUNDARY MATRIX RANKS SUMMARY")
print("=" * 70)
print(f"""
  C_0 ←∂₁― C_1 ←∂₂― C_2 ←∂₃― C_3
  {len(vertices):3d} ←――― {len(edges):3d} ←――― {len(triangles):3d} ←――― {len(tetrahedra):3d}
  
  rank(∂_1) = {rank_d1}
  rank(∂_2) = {rank_d2}
  rank(∂_3) = {rank_d3}
""")
