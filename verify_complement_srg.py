#!/usr/bin/env python3
"""
Verify that W̄ is also strongly regular
"""

import numpy as np
import itertools
from collections import defaultdict, Counter

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

# Build complement
adj_comp = defaultdict(set)
for u in range(n):
    for v in range(u+1, n):
        if v not in adj[u]:
            adj_comp[u].add(v)
            adj_comp[v].add(u)

print("=" * 70)
print(" COMPLEMENT GRAPH SRG PARAMETERS")
print("=" * 70)

print(f"\n[1] Original W(3,3) = SRG(40, 12, 2, 4)")
print(f"    Parameters: (n, k, λ, μ) = (40, 12, 2, 4)")

print(f"\n[2] Computing W̄ SRG Parameters")
print(f"    Basic parameters:")
n = len(points)
k_comp = len(adj_comp[0])
print(f"    n = {n}")
print(f"    k̄ = {k_comp}")

# For each pair of vertices, count common neighbors
lambda_pairs = []  # Common neighbors in W̄ for adjacent pairs in W̄
mu_pairs = []      # Common neighbors in W̄ for non-adjacent pairs in W̄

for u in range(n):
    for v in range(u+1, n):
        common_neighbors = len(adj_comp[u] & adj_comp[v])
        
        if v in adj_comp[u]:  # Adjacent in W̄
            lambda_pairs.append(common_neighbors)
        else:  # Non-adjacent in W̄
            mu_pairs.append(common_neighbors)

# Check for consistency
lambda_counts = Counter(lambda_pairs)
mu_counts = Counter(mu_pairs)

print(f"\n    λ̄ (common neighbors for adjacent pairs in W̄):")
print(f"      Distribution: {dict(lambda_counts)}")
if len(lambda_counts) == 1:
    lambda_bar = list(lambda_counts.keys())[0]
    print(f"      λ̄ = {lambda_bar} (uniform)")
else:
    lambda_bar = None
    print(f"      NOT uniform (irregular)")

print(f"\n    μ̄ (common neighbors for non-adjacent pairs in W̄):")
print(f"      Distribution: {dict(mu_counts)}")
if len(mu_counts) == 1:
    mu_bar = list(mu_counts.keys())[0]
    print(f"      μ̄ = {mu_bar} (uniform)")
else:
    mu_bar = None
    print(f"      NOT uniform (irregular)")

if lambda_bar is not None and mu_bar is not None:
    print(f"\n    ✓ W̄ is strongly regular: SRG(40, {k_comp}, {lambda_bar}, {mu_bar})")
    
    # Verify SRG constraint
    print(f"\n[3] SRG Constraint Verification")
    print(f"    For SRG(n,k,λ,μ): k(k-λ-1) = μ(n-k-1)")
    lhs = k_comp * (k_comp - lambda_bar - 1)
    rhs = mu_bar * (n - k_comp - 1)
    print(f"    LHS: {k_comp}({k_comp}-{lambda_bar}-1) = {k_comp}({k_comp-lambda_bar-1}) = {lhs}")
    print(f"    RHS: {mu_bar}({n}-{k_comp}-1) = {mu_bar}({n-k_comp-1}) = {rhs}")
    print(f"    Equal: {lhs == rhs} {'✓' if lhs == rhs else '✗'}")
    
    # Theory: for complement of SRG(n,k,λ,μ):
    print(f"\n[4] Complementarity Theory")
    print(f"    Original W: SRG(n, k, λ, μ) = SRG(40, 12, 2, 4)")
    print(f"    Complement W̄: SRG(n, n-k-1, μ-μ, λ) ???")
    print(f"    Wait, that's not quite right. Let me derive correctly...")
    print(f"\n    For adjacent pairs u,v in W̄ (non-adjacent in W):")
    print(f"      Common neighbors in W̄ = all neighbors of u in W̄ that are also neighbors of v in W̄")
    print(f"      = (non-neighbors of u in W) ∩ (non-neighbors of v in W)")
    print(f"      = {n} - |neighbors of u in W| - |neighbors of v in W| + |common neighbors of u,v in W|")
    print(f"      = {n} - {k_comp + k_comp} + {4} = {n - 2*12 + 4}")
    
    print(f"\n    For non-adjacent pairs u,v in W̄ (adjacent in W):")
    print(f"      Common neighbors in W̄ = (non-neighbors of u in W) ∩ (non-neighbors of v in W)")
    print(f"      = {n} - |neighbors of u in W| - |neighbors of v in W| + |common neighbors of u,v in W|")
    print(f"      = {n} - {k_comp + k_comp} + {2} = {n - 2*12 + 2}")
    
    print(f"\n    Formula check:")
    print(f"    λ̄ = n - 2k - (μ - 1) for non-adjacent in W: {n} - 2*{k_comp} - ({mu_bar}-1) = {n - 2*k_comp - (mu_bar-1)}")
    print(f"    μ̄ = n - 2k - (λ - 1) for adjacent in W: {n} - 2*{k_comp} - ({lambda_bar}-1) = {n - 2*k_comp - (lambda_bar-1)}")
    
else:
    print(f"\n    W̄ is NOT strongly regular")

print("\n" + "=" * 70)
print(" SUMMARY: COMPLEMENT STRONGLY REGULAR")
print("=" * 70)
if lambda_bar is not None and mu_bar is not None:
    print(f"  ✓ W̄(3,3) = SRG({n}, {k_comp}, {lambda_bar}, {mu_bar})")
    print(f"  ✓ Complement of SRG(40,12,2,4) is SRG(40,27,{lambda_bar},{mu_bar})")
    print(f"  • Both W and W̄ are strongly regular")
    print(f"  • Together they partition K_40 (complete graph on 40 vertices)")
print()
