#!/usr/bin/env sage
"""
W33's point graph is SRG(40, 12, 2, 4).
This is a FAMOUS graph! Let's identify it.

SRG(40, 12, 2, 4) is the symplectic graph from the 
dual polar space of Sp(4,3)!
"""

from sage.all import *
import numpy as np

print("=== Identifying SRG(40, 12, 2, 4) ===")
print()

# SRG(40, 12, 2, 4) properties
v, k, lam, mu = 40, 12, 2, 4

print(f"Parameters: v={v}, k={k}, λ={lam}, μ={mu}")
print()

# Check the eigenvalue multiplicities
# For SRG, the multiplicities are:
# f = k(s+1)(k-s) / ((k-r)(s-r))
# g = k(r+1)(k-r) / ((k-s)(r-s))
# where r, s are the non-trivial eigenvalues

r, s = 2, -4
f = k * (s + 1) * (k - s) / ((k - r) * (s - r))
g = k * (r + 1) * (k - r) / ((k - s) * (r - s))

print(f"Eigenvalue r = {r}, multiplicity f = {f}")
print(f"Eigenvalue s = {s}, multiplicity g = {g}")
print(f"Check: 1 + f + g = {1 + f + g} (should be {v})")
print()

# This SRG is known as:
print("=== Known Realizations ===")
print()
print("SRG(40, 12, 2, 4) is realized by:")
print()
print("1. SYMPLECTIC GRAPH Sp(4,3)")
print("   - Vertices: 40 points of PG(3, 3) (projective 3-space over GF(3))")
print("   - Edges: pairs of points orthogonal w.r.t. symplectic form")
print("   - Automorphism group: PSp(4, 3)")
print()
print("2. DUAL POLAR GRAPH of W(3)")
print("   - W(3) is the symplectic polar space")
print("   - Vertices: maximal totally isotropic subspaces (lines)")
print()
print("3. COMPLEMENT of the TRIANGULAR GRAPH T(10)")
print("   - Wait, T(10) has 45 vertices, not 40...")
print()

# Let's verify: the symplectic graph
print("=== Constructing Symplectic Graph Sp(4,3) ===")
print()

# PG(3, 3) has (3^4 - 1)/(3 - 1) = 40 points! ✓
print("PG(3, 3) (projective 3-space over GF(3)):")
print(f"  Number of points: (3^4 - 1)/(3 - 1) = {(3**4 - 1)//(3 - 1)}")
print()

# In PG(3, q), a symplectic form makes pairs of points "orthogonal"
# The symplectic graph connects orthogonal pairs

# Let's construct it
F = GF(3)
V = VectorSpace(F, 4)

# Symplectic form: [x, y] = x1*y3 - x3*y1 + x2*y4 - x4*y2
def symplectic_form(x, y):
    return x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]

# Get projective points (equivalence classes of non-zero vectors)
points = []
seen = set()
for v in V:
    if v == V.zero():
        continue
    # Normalize: first non-zero coordinate is 1
    v_list = list(v)
    for i, c in enumerate(v_list):
        if c != 0:
            v_normalized = tuple(F(x) / c for x in v_list)
            break
    if v_normalized not in seen:
        seen.add(v_normalized)
        points.append(v_normalized)

print(f"Projective points in PG(3, 3): {len(points)}")

# Build symplectic graph
adj = [[0]*40 for _ in range(40)]
for i in range(40):
    for j in range(i+1, 40):
        p1, p2 = points[i], points[j]
        # Convert to vectors
        v1 = V(list(p1))
        v2 = V(list(p2))
        if symplectic_form(v1, v2) == F(0):
            adj[i][j] = adj[j][i] = 1

# Compute degree
degrees = [sum(adj[i]) for i in range(40)]
print(f"Symplectic graph degrees: {set(degrees)}")
print()

# Check if it's SRG(40, 12, 2, 4)
if set(degrees) == {12}:
    print("Degree = 12 ✓")
    
    # Check λ and μ
    lambda_test = []
    mu_test = []
    for i in range(40):
        for j in range(i+1, 40):
            common = sum(1 for k in range(40) if adj[i][k] and adj[j][k])
            if adj[i][j]:
                lambda_test.append(common)
            else:
                mu_test.append(common)
    
    print(f"λ values: {set(lambda_test)}")
    print(f"μ values: {set(mu_test)}")
    
    if set(lambda_test) == {2} and set(mu_test) == {4}:
        print()
        print("★ Symplectic graph Sp(4,3) IS SRG(40, 12, 2, 4)! ★")

print()
print("=== The Key Connection ===")
print()
print("W33 is a 2-(40, 4, 1) design whose point graph is")
print("isomorphic to the symplectic graph of PG(3, 3)!")
print()
print("The 40 'lines' of W33 correspond to the 40 'totally isotropic")  
print("lines' in the symplectic geometry of PG(3, 3).")
print()
print("This makes W33 the SYMPLECTIC POLAR SPACE W(3,3)!")
print("Also known as the generalized quadrangle GQ(3,3)'s")
print("point-hyperplane incidence structure.")
