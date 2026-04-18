#!/usr/bin/env python3
"""Simple triangle counting in W(3,3) to verify tr(A^3) = 6*C3."""

import numpy as np

# Build the 40-vertex SRG using the working method from SPECTRAL_VERIFICATION
n_full = 0
vertices = []
for c0 in range(3):
    for c1 in range(3):
        for c2 in range(3):
            for c3 in range(3):
                if (c0, c1, c2, c3) != (0, 0, 0, 0):
                    vertices.append((c0, c1, c2, c3))
                    n_full += 1

def form(v, w):
    return (v[0]*w[1] - v[1]*w[0] + v[2]*w[3] - v[3]*w[2]) % 3

A_full = np.zeros((80, 80), dtype=int)
for i in range(80):
    for j in range(i+1, 80):
        if form(vertices[i], vertices[j]) == 1:
            A_full[i, j] = 1
            A_full[j, i] = 1

# Project to 40 vertices
A = A_full[:40, :40]

print("Graph: 40 vertices, {} edges".format(int(np.sum(A)//2)))

# Count triangles
print("Counting triangles...")
c3 = 0
for i in range(40):
    for j in range(i+1, 40):
        if A[i, j]:
            for k in range(j+1, 40):
                if A[j, k] and A[k, i]:
                    c3 += 1

print(f"C3 (triangles): {c3}")

# Verify spectral trace
A_float = A.astype(float)
tr3 = int(np.trace(np.linalg.matrix_power(A_float, 3)))
print(f"tr(A^3) = {tr3}")
print(f"6*C3 = {6*c3}")
print(f"Match: {tr3 == 6*c3}")
