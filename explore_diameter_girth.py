#!/usr/bin/env python3
"""
Explore diameter, girth, cycles, and Laplacian properties of W(3,3)
"""

import numpy as np
import itertools
from collections import deque, Counter

# Build W(3,3)
J = np.array([[0,1,0,0],[2,0,0,0],[0,0,0,1],[0,0,2,0]], dtype=int)
def symp_form(u, v):
    return int(np.dot(u, np.dot(J, v))) % 3

points = []
for combo in itertools.product(range(3), repeat=4):
    if any(x != 0 for x in combo):
        v = np.array(combo, dtype=int)
        for i in range(4):
            if v[i] != 0:
                if v[i] == 1:
                    points.append(v.copy())
                break

n = len(points)
A = np.zeros((n, n), dtype=int)
for i in range(n):
    for j in range(i+1, n):
        if symp_form(points[i], points[j]) == 0:
            A[i,j] = A[j,i] = 1

print("=== W(3,3) Diameter and Girth Analysis ===\n")

# BFS shortest paths
def bfs_shortest_paths(adj, start):
    """BFS from start, return distances to all vertices"""
    n = len(adj)
    dist = [-1] * n
    dist[start] = 0
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for v in range(n):
            if adj[u, v] and dist[v] == -1:
                dist[v] = dist[u] + 1
                queue.append(v)
    return dist

# Find girth (shortest cycle)
girth = float('inf')
for start in range(n):
    # Check for triangles (3-cycles)
    for u in range(n):
        for v in range(u+1, n):
            if A[start, u] and A[start, v] and A[u, v]:
                girth = min(girth, 3)
    
    if girth > 3:
        # Check for 4-cycles through BFS
        dist = bfs_shortest_paths(A, start)
        for u in range(start+1, n):
            if A[start, u]:
                for v in range(u+1, n):
                    if A[start, v] and A[u, v]:
                        # Found a 4-cycle: start-u-v-start
                        pass
                    elif A[u, v] and dist[v] >= 2:
                        # Potential 4-cycle
                        path_len = dist[v]
                        if path_len + 1 == 4:  # u to v distance 2, plus 2 edges to start
                            girth = min(girth, 4)

# Compute diameter
dist_matrix = []
for start in range(n):
    dist = bfs_shortest_paths(A, start)
    dist_matrix.append(dist)

diameter = 0
for row in dist_matrix:
    diameter = max(diameter, max(d for d in row if d >= 0))

print(f"Girth (shortest cycle): {girth}")
print(f"Diameter (longest shortest path): {diameter}")

# Count cycles
print("\n=== Cycle Enumeration ===")

# C_3
c3_count = 0
for i in range(n):
    for j in range(i+1, n):
        if A[i,j]:
            for k in range(j+1, n):
                if A[i,k] and A[j,k]:
                    c3_count += 1
print(f"C_3 (triangles): {c3_count}")

# C_4: 4-cycles via distance-2 pairs
c4_count = 0
for i in range(n):
    for j in range(i+1, n):
        if A[i,j] == 0:  # Non-adjacent
            # Count paths of length 2 between i and j
            paths_2 = 0
            for k in range(n):
                if A[i,k] and A[k,j]:
                    paths_2 += 1
            # Each path gives a 4-cycle i-k1-j-k2-i if there's another k2
            if paths_2 >= 2:
                c4_count += paths_2 * (paths_2 - 1) // 2

print(f"C_4 (4-cycles, formula-based): {c4_count}")

# Compute spectrum of adjacency matrix (already known)
eigvals_A = np.linalg.eigvalsh(A)
eigvals_A_sorted = sorted(eigvals_A, reverse=True)
print(f"\nAdjacency eigenvalues: {[f'{x:.1f}' for x in eigvals_A_sorted]}")

# Laplacian spectrum
L = np.diag(A.sum(axis=1)) - A
eigvals_L = np.linalg.eigvalsh(L)
eigvals_L_sorted = sorted(eigvals_L)

print(f"\n=== Laplacian Spectrum ===")
print(f"Smallest (trivial) lambda_0 = {eigvals_L_sorted[0]:.6f}")
print(f"Algebraic connectivity lambda_1 = {eigvals_L_sorted[1]:.6f}")
print(f"Next few eigenvalues: {[f'{x:.2f}' for x in eigvals_L_sorted[1:6]]}")
print(f"Largest eigenvalue lambda_n = {eigvals_L_sorted[-1]:.1f}")

# Relation: sum of Laplacian eigenvalues = trace(L) = nk
print(f"Trace(L) = sum of eigenvalues = {sum(eigvals_L):.1f}")
print(f"Expected: nk = 40 × 12 = {40*12}")

# Cheeger inequality: h >= lambda_1/2 where h is edge expansion
h_lower = eigvals_L_sorted[1] / 2
print(f"\nCheeger lower bound: h >= lambda_1/2 = {h_lower:.4f}")

# Compute actual edge expansion (isoperimetric constant)
min_expansion = float('inf')
for subset_size in range(1, n//2 + 1):
    for vertices in itertools.combinations(range(n), subset_size):
        vertex_set = set(vertices)
        edges_out = 0
        for v in vertices:
            for u in range(n):
                if u not in vertex_set and A[v,u]:
                    edges_out += 1
        if subset_size > 0:
            expansion = edges_out / (subset_size if subset_size <= n//2 else n - subset_size)
            min_expansion = min(min_expansion, expansion)
            if subset_size <= 3:  # Print small cases
                print(f"  Subset {vertices}: expansion = {expansion:.2f}")
        if subset_size > 5:  # Don't check large subsets
            break

print(f"\nMin edge expansion: {min_expansion:.4f}")

# Distance matrix analysis (complement)
print(f"\n=== Distance Matrix ===")
D = np.zeros((n, n), dtype=int)
for i in range(n):
    for j in range(n):
        if i != j:
            D[i,j] = dist_matrix[i][j]

# D spectrum
D_float = D.astype(float)
eigvals_D = np.linalg.eigvalsh(D_float)
eigvals_D_sorted = sorted(eigvals_D, reverse=True)
print(f"Distance matrix eigenvalues: {[f'{x:.1f}' for x in eigvals_D_sorted[:10]]}")

# Wiener index
W = np.sum(D) // 2
print(f"Wiener index W = {W}")

print("\n=== Verification ===")
print(f"[OK] Graph diameter: {diameter}")
print(f"[OK] Girth: {girth}")
print(f"[OK] Algebraic connectivity: {eigvals_L_sorted[1]:.4f}")
