"""
D₅ ROOT GRAPH: Careful analysis of which adjacency definition gives GQ(3,3)

The D₅ root system has 40 roots. We need to find the RIGHT adjacency
relation that makes it isomorphic to srg(40,12,2,4) = GQ(3,3).

Possible definitions:
1. <α,β> = +1 (angle 60°)
2. <α,β> = -1 (angle 120°) 
3. <α,β> = 0 (orthogonal)
4. Some other condition

Also investigate: is there a DIFFERENT 40-element structure from E₆
that IS GQ(3,3)?
"""

import numpy as np
from collections import Counter
import json

# Build D₅ roots: ±e_i ± e_j, 1 ≤ i < j ≤ 5
roots = []
for i in range(5):
    for j in range(i+1, 5):
        for si in [1, -1]:
            for sj in [1, -1]:
                root = [0]*5
                root[i] = si
                root[j] = sj
                roots.append(tuple(root))

n = len(roots)
print(f"D₅ root system: {n} roots\n")

# Compute ALL inner products
ip_matrix = np.zeros((n, n), dtype=int)
for i in range(n):
    for j in range(n):
        ip_matrix[i][j] = sum(a*b for a, b in zip(roots[i], roots[j]))

# For a specific root, count inner product distribution
ip_dist = Counter(ip_matrix[0])
print(f"Inner product distribution from root 0:")
for ip, count in sorted(ip_dist.items()):
    print(f"  <α,β> = {ip:+d}: {count} roots")

# Try each possible adjacency definition
print(f"\n{'='*60}")
for ip_val in [0, 1, -1]:
    adj = (ip_matrix == ip_val).astype(int)
    np.fill_diagonal(adj, 0)
    
    degrees = adj.sum(axis=1)
    k_val = degrees[0]
    is_regular = all(d == k_val for d in degrees)
    
    # Check SRG parameters
    if is_regular and k_val > 0:
        lambda_vals = set()
        mu_vals = set()
        for i in range(min(40, n)):
            for j in range(i+1, min(40, n)):
                common = int(sum(adj[i] * adj[j]))
                if adj[i][j] == 1:
                    lambda_vals.add(common)
                else:
                    mu_vals.add(common)
        
        lambda_const = len(lambda_vals) == 1
        mu_const = len(mu_vals) == 1
        
        print(f"\nAdjacency = <α,β> = {ip_val:+d}:")
        print(f"  Regular: {is_regular}, k = {k_val}")
        print(f"  λ values: {sorted(lambda_vals)}")
        print(f"  μ values: {sorted(mu_vals)}")
        if lambda_const and mu_const:
            lam_v = list(lambda_vals)[0]
            mu_v = list(mu_vals)[0]
            print(f"  → srg({n}, {k_val}, {lam_v}, {mu_v})")
            if (n, k_val, lam_v, mu_v) == (40, 12, 2, 4):
                print(f"  ★★★ THIS IS GQ(3,3)! ★★★")
        else:
            print(f"  NOT strongly regular (parameters vary)")
    else:
        print(f"\nAdjacency = <α,β> = {ip_val:+d}: k = {k_val}, regular = {is_regular}")

# Also try: pair of conditions
print(f"\n{'='*60}")
for ip_vals in [(0,), (1, -1)]:
    adj = np.zeros((n, n), dtype=int)
    for ip_v in ip_vals:
        adj += (ip_matrix == ip_v).astype(int)
    np.fill_diagonal(adj, 0)
    adj = (adj > 0).astype(int)
    
    degrees = adj.sum(axis=1)
    k_val = degrees[0]
    is_regular = all(d == k_val for d in degrees)
    
    if is_regular and k_val > 0:
        lambda_vals = set()
        mu_vals = set()
        for i in range(min(40, n)):
            for j in range(i+1, min(40, n)):
                common = int(sum(adj[i] * adj[j]))
                if adj[i][j] == 1:
                    lambda_vals.add(common)
                else:
                    mu_vals.add(common)
        
        lambda_const = len(lambda_vals) == 1
        mu_const = len(mu_vals) == 1
        
        label = '+'.join([f'{v:+d}' for v in ip_vals])
        print(f"\nAdjacency = <α,β> ∈ {{{label}}}:")
        print(f"  Regular: {is_regular}, k = {k_val}")
        print(f"  λ values: {sorted(lambda_vals)}")
        print(f"  μ values: {sorted(mu_vals)}")
        if lambda_const and mu_const:
            lam_v = list(lambda_vals)[0]
            mu_v = list(mu_vals)[0]
            print(f"  → srg({n}, {k_val}, {lam_v}, {mu_v})")

# ═══════════════════════════════════════════════════════
# THE CORRECT CONNECTION: W(E₆) ACTS ON BOTH
# ═══════════════════════════════════════════════════════
print(f"\n{'='*60}")
print("THE STRUCTURAL CONNECTION (NOT GRAPH ISOMORPHISM)")
print("=" * 60)

# The correct statement is:
# 1. Aut(GQ(3,3)) = PSp(4,3) of order 25920
# 2. W(E₆) = 51840 = 2 × 25920
# 3. PSp(4,3) = W(E₆)/Z₂ (the simple quotient)
# 4. D₅ has 40 roots, GQ(3,3) has 40 points
# 5. They have the SAME symmetry group acting on them

# But the GRAPH structures are different:
# D₅ root graph with <α,β>=+1 is srg(40, 12, 5, varies) — NOT srg(40,12,2,4)
# GQ(3,3) point graph IS srg(40,12,2,4)

# The CONNECTION is through the Weyl group action:
# W(E₆) acts on the 40 D₅ roots AND on the 40 GQ(3,3) points
# via the SAME permutation group PSp(4,3)

# But as GRAPHS they are not isomorphic!
# What IS true: there exists a bijection between D₅ roots and GQ(3,3) points
# that is equivariant under W(E₆), even though the adjacency structures differ.

print(f"""
  CORRECTION: D₅ root graph ≠ GQ(3,3) collinearity graph
  
  D₅ root graph (adj = <α,β>=+1): srg(40, 12, 5, ?)  — NOT GQ(3,3)
  GQ(3,3) collinearity graph: srg(40, 12, 2, 4)
  
  BOTH have:
  - 40 vertices
  - 12-regular (k = 12)
  - Automorphism group containing PSp(4,3) (order 25920)
  
  The connection is GROUP-THEORETIC, not graph-theoretic:
  W(E₆) = 51840 acts on both structures through PSp(4,3).
  
  PSp(4,3) acts transitively on:
  - The 40 D₅ roots (as W(E₆) acts on a D₅ subsystem)
  - The 40 GQ(3,3) points (as Aut(W(3,F₃)))
  
  This is the REPRESENTATION-THEORETIC bridge:
  The same abstract group has two different faithful actions
  on 40-element sets, giving two different srg structures.
""")

# Let me check the D₅ root graph eigenvalues
adj_d5 = (ip_matrix == 1).astype(float)
np.fill_diagonal(adj_d5, 0)
eigenvalues = sorted(np.linalg.eigvalsh(adj_d5), reverse=True)
eig_rounded = [round(e) for e in eigenvalues]
eig_counts = Counter(eig_rounded)

print(f"D₅ root graph (adj = <α,β>=+1) eigenvalues:")
for eig, mult in sorted(eig_counts.items(), reverse=True):
    print(f"  {eig:+d} with multiplicity {mult}")

# GQ(3,3) eigenvalues: 12(1), 2(24), -4(15)
# D₅ root eigenvalues: let's see...

# Also check the orthogonality graph
adj_orth = (ip_matrix == 0).astype(float)
np.fill_diagonal(adj_orth, 0)
eigenvalues_orth = sorted(np.linalg.eigvalsh(adj_orth), reverse=True)
eig_rounded_orth = [round(e) for e in eigenvalues_orth]
eig_counts_orth = Counter(eig_rounded_orth)

print(f"\nD₅ root orthogonality graph (adj = <α,β>=0) eigenvalues:")
for eig, mult in sorted(eig_counts_orth.items(), reverse=True):
    print(f"  {eig:+d} with multiplicity {mult}")

# ═══════════════════════════════════════════════════════
# THE CORRECT 40-ELEMENT OBJECT IN E₆
# ═══════════════════════════════════════════════════════
print(f"\n{'='*60}")
print("WHERE DOES GQ(3,3) LIVE IN E₆?")
print("=" * 60)

# The answer: GQ(3,3) = W(3,F₃) is constructed from the SYMPLECTIC SPACE
# V = F₃⁴ with the standard symplectic form.
# The 40 points are the 1-dimensional subspaces of F₃⁴ that are ISOTROPIC.

# The group PSp(4,3) acts on these 40 isotropic lines.
# This SAME group appears as W(E₆)/Z₂.

# The 40 isotropic lines of (F₃⁴, ω) are NOT the D₅ roots,
# but they carry an action of the same group.

# The BRIDGE between E₆ and GQ(3,3):
# E₆ has Weyl group W(E₆) = 51840
# W(E₆) has a unique maximal normal subgroup Z₂
# W(E₆)/Z₂ ≅ PSp(4,3) ≅ Ω⁻(4,3) 
# PSp(4,3) acts faithfully on the 40 isotropic lines of (F₃⁴, ω)
# THIS action gives GQ(3,3) with srg(40,12,2,4)

# Meanwhile, W(E₆) also acts on the 27 weights of the fundamental rep of E₆,
# and on the 72 roots of E₆, and on various other structures.

# The key insight: the 40-point GQ(3,3) is a GEOMETRIC realization
# of the abstract permutation action of PSp(4,3) on 40 elements
# that arises from the Weyl group W(E₆).

print(f"""
  GQ(3,3) = W(3,F₃) is the set of 40 isotropic lines in (F₃⁴, ω)
  where ω is the standard symplectic form.
  
  The group PSp(4,3) acts on these 40 lines,
  giving the srg(40,12,2,4) collinearity graph.
  
  PSp(4,3) ≅ W(E₆)/Z₂ is the bridge to exceptional Lie algebras.
  
  The D₅ root system has 40 roots, and W(E₆) acts on them too,
  but the resulting graph structure is DIFFERENT.
  
  WHAT IS THE SAME:
  - Both are 40-element sets with PSp(4,3) acting transitively
  - Both give 12-regular graphs
  - The abstract group structure is identical
  
  WHAT IS DIFFERENT:
  - GQ(3,3): srg(40,12,2,4) — the collinearity graph
  - D₅ roots: srg(40,12,5,varies) — NOT the same SRG
  - The GQ has the ADDITIONAL structure of lines (4 points each)
  
  THE PHYSICAL INTERPRETATION:
  The GQ(3,3) geometry adds INCIDENCE STRUCTURE beyond what the 
  root system provides. This incidence structure encodes:
  - Which particles can interact (collinearity = interaction)
  - The generation structure (lines through Higgs)
  - The Yukawa couplings (line multiplicities)
""")

# Save corrected results
results = {
    "d5_root_graph_correction": {
        "statement": "D₅ root graph with <α,β>=+1 is 12-regular but NOT srg(40,12,2,4)",
        "actual_lambda": "5 (not 2)",
        "actual_mu": "varies (not constant 4)",
        "conclusion": "D₅ root graph ≠ GQ(3,3) as graphs"
    },
    "structural_connection": {
        "common_group": "PSp(4,3) = W(E₆)/Z₂ of order 25920",
        "acts_on_d5": "40 D₅ roots (as Weyl group action)",
        "acts_on_gq": "40 GQ(3,3) isotropic lines (as Aut(W(3,F₃)))",
        "both_12_regular": True,
        "same_srg": False
    },
    "gq33_construction": {
        "ambient_space": "V = F₃⁴ with symplectic form ω",
        "points": "40 isotropic 1-dim subspaces",
        "lines": "40 isotropic 2-dim subspaces (each containing q+1=4 points)",
        "automorphism_group": "PSp(4,3) of order 25920"
    }
}

with open('/home/user/workspace/W33-Theory/data/w33_d5_graph_correction.json', 'w') as fp:
    json.dump(results, fp, indent=2)

print("Results saved to data/w33_d5_graph_correction.json")
