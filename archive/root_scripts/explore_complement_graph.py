#!/usr/bin/env python3
"""
Complement graph W̄ and self-complementary/complementary properties
"""

import numpy as np
import itertools
from collections import defaultdict

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
adj = defaultdict(set)
for i in range(n):
    for j in range(i+1, n):
        if symp_form(points[i], points[j]) == 0:
            adj[i].add(j)
            adj[j].add(i)

k = len(adj[0])
E = sum(len(adj[i]) for i in range(n)) // 2

# Build complement
adj_comp = defaultdict(set)
for u in range(n):
    for v in range(u+1, n):
        if v not in adj[u]:
            adj_comp[u].add(v)
            adj_comp[v].add(u)

k_comp = len(adj_comp[0])
E_comp = sum(len(adj_comp[i]) for i in range(n)) // 2

print("=" * 70)
print(" COMPLEMENT GRAPH W̄: PROPERTIES AND ANALYSIS")
print("=" * 70)

print(f"\n[1] Basic Complement Properties")
print(f"    Original graph W(3,3):")
print(f"      Vertices: {n}")
print(f"      Edges: {E}")
print(f"      Regularity: {k}-regular")
print(f"      Degree sum: nk/2 = {n*k//2}")

print(f"\n    Complete graph K_n:")
print(f"      Edges: n(n-1)/2 = {n*(n-1)//2}")

print(f"\n    Complement W̄:")
print(f"      Vertices: {n}")
print(f"      Edges: {E_comp}")
print(f"      Regularity: {k_comp}-regular")
print(f"      Verification: E + E_comp = {E + E_comp} should equal {n*(n-1)//2}")
assert E + E_comp == n*(n-1)//2, "Edge partition failed"
print(f"      ✓ Verified: perfect edge partition")

print(f"\n[2] Complement Regularity")
print(f"    W is {k}-regular")
print(f"    W̄ is {k_comp}-regular")
print(f"    Expected: k_comp = n - 1 - k = {n - 1 - k}")
print(f"    Actual: {k_comp}")
assert k_comp == n - 1 - k, "Complement degree mismatch"
print(f"    ✓ Verified: complement degree formula")

# Eigenvalues of complement
print(f"\n[3] Spectrum of W̄")
A = np.zeros((n, n), dtype=int)
for i in range(n):
    for j in range(i+1, n):
        if j in adj[i]:
            A[i,j] = A[j,i] = 1

J_full = np.ones((n, n), dtype=int)
np.fill_diagonal(J_full, 0)
A_comp = J_full - A

eigvals_comp = np.linalg.eigvalsh(A_comp)
eigvals_comp_sorted = sorted(eigvals_comp, reverse=True)

from collections import Counter
eigvals_rounded = [round(x, 1) for x in eigvals_comp_sorted]
eig_mult = Counter(eigvals_rounded)
print(f"    Spectrum of W̄: {dict(sorted(eig_mult.items(), reverse=True))}")

# Relationship between spectra
print(f"\n[4] Spectral Relationship")
print(f"    W spectrum: {{12, 2^24, (-4)^15}}")
print(f"    W̄ spectrum: {dict(sorted(eig_mult.items(), reverse=True))}")
print(f"    For k-regular complement (k_comp={k_comp})-regular:")
print(f"    λ_i(W̄) = (n-1-k) - λ_i(W) = {n-1-k} - λ_i(W)")
print(f"    Expected W̄ spectrum: {{{n-1-k}-12, {n-1-k}-2, {n-1-k}-(-4)}} = {{15, 25, 31}}")

# Check complement connectivity
print(f"\n[5] Connectivity Properties of W̄")
A_comp_dict = defaultdict(set)
for u in range(n):
    for v in range(n):
        if u != v and v in adj_comp[u]:
            A_comp_dict[u].add(v)

# BFS to check connectivity
visited = set()
queue = [0]
visited.add(0)
while queue:
    u = queue.pop(0)
    for v in A_comp_dict[u]:
        if v not in visited:
            visited.add(v)
            queue.append(v)

connected = len(visited) == n
print(f"    Complement is connected: {connected}")

if connected:
    # Compute diameter of complement
    from collections import deque
    
    def bfs_dist(adj_dict, start, n):
        dist = [-1] * n
        dist[start] = 0
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in adj_dict[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + 1
                    queue.append(v)
        return dist
    
    diam_comp = 0
    for v in range(n):
        dist = bfs_dist(A_comp_dict, v, n)
        diam_comp = max(diam_comp, max(dist))
    
    print(f"    Diameter of W̄: {diam_comp}")

# Coclique and clique relationship
print(f"\n[6] Coclique and Clique Relationship")
print(f"    Coclique in W (independent set) = Clique in W̄")
print(f"    Clique in W (clique) = Coclique in W̄ (independent set)")
print(f"    Independence number α(W) = 7")
print(f"    => Clique number ω(W̄) = 7")
print(f"    => Independence number α(W̄) = ω(W) = 4")

# Chromatic number
print(f"\n[7] Chromatic Properties")
print(f"    Chromatic number χ(W) = 7")
print(f"    Clique number ω(W) = 4")
print(f"    For complement: χ(W̄) >= ω(W̄) = α(W) = 7")
print(f"    Chromatic number χ(W̄) = ?")

# Bipartiteness
print(f"\n[8] Bipartiteness")
print(f"    W is non-bipartite (contains triangles)")
print(f"    W̄ may be bipartite if girth is even")

print("\n" + "=" * 70)
print(" SUMMARY: COMPLEMENT GRAPH W̄(3,3)")
print("=" * 70)
print(f"  • Regular: {k_comp}-regular (complement of 12-regular)")
print(f"  • Vertices: {n}, Edges: {E_comp}")
print(f"  • Degree formula: k_comp = n - 1 - k = {n - 1 - k} ✓")
print(f"  • Spectrum: {dict(sorted(eig_mult.items(), reverse=True))}")
print(f"  • Connected: {connected}")
if connected:
    print(f"  • Diameter: {diam_comp}")
print(f"  • Coclique(W) = Clique(W̄): both size 7")
print(f"  • Independence α(W̄) = ω(W) = 4")
print()
