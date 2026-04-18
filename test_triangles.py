#!/usr/bin/env python3
"""Triangle counting in W(3,3) to verify tr(A^3) = 6*C3 = 960."""

import itertools
import numpy as np

# Build the correct 40-vertex projective symplectic graph W(3,3)
# Points: PG(3,3) = vectors in GF(3)^4 with first nonzero coordinate == 1
J = np.array([[0,1,0,0],[2,0,0,0],[0,0,0,1],[0,0,2,0]], dtype=int)

def symp_form(u, v):
    return int(np.dot(u, np.dot(J, v))) % 3

points = []
for combo in itertools.product(range(3), repeat=4):
    if any(x != 0 for x in combo):
        v = list(combo)
        for i in range(4):
            if v[i] != 0:
                if v[i] == 1:
                    points.append(v)
                break

n = len(points)
A = np.zeros((n, n), dtype=int)
for i in range(n):
    for j in range(i+1, n):
        if symp_form(points[i], points[j]) == 0:
            A[i,j] = A[j,i] = 1

degs = A.sum(axis=1)
print(f"Graph: n={n}, degree={degs.min()},{degs.max()}, edges={A.sum()//2}")

# Count triangles
print("Counting triangles...")
c3 = 0
for i in range(n):
    for j in range(i+1, n):
        if A[i, j]:
            for k in range(j+1, n):
                if A[j, k] and A[k, i]:
                    c3 += 1

print(f"C3 (triangles): {c3}")

# Verify spectral trace
tr3 = int(np.trace(np.linalg.matrix_power(A.astype(float), 3)))
print(f"tr(A^3) = {tr3}")
print(f"6*C3 = {6*c3}")
print(f"Match: {tr3 == 6*c3}")

# Cross-check from eigenvalues
k_val, f_r, r_val, f_s, s_val = 12, 24, 2, 15, -4
tr3_eig = 1*k_val**3 + f_r*r_val**3 + f_s*s_val**3
print(f"tr(A^3) from eigenvalues = {tr3_eig}")
assert c3 == 160, f"Expected C3=160, got {c3}"
assert tr3 == 960, f"Expected tr(A^3)=960, got {tr3}"
assert tr3 == 6*c3
print("All assertions passed: C3=160, tr(A^3)=960  ✓")

