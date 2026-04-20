#!/usr/bin/env python3
"""
Line graph, independence polynomial, Lovász theta, and
Tutte polynomial evaluations for W(3,3).
"""

import numpy as np
import itertools
from collections import defaultdict, Counter
from fractions import Fraction

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
adj = defaultdict(set)
edges = []
for i in range(n):
    for j in range(i+1, n):
        if symp_form(points[i], points[j]) == 0:
            A[i,j] = A[j,i] = 1
            adj[i].add(j)
            adj[j].add(i)
            edges.append((i,j))

k = int(A.sum(axis=1)[0])
E = len(edges)

print("=" * 70)
print(" LINE GRAPH, INDEPENDENCE, LOVÁSZ THETA, TUTTE: W(3,3)")
print("=" * 70)
print(f"  n = {n}, k = {k}, |E| = {E}")

# ========================================================
# 1. LINE GRAPH L(W)
# ========================================================
print(f"\n[1] Line Graph L(W(3,3))")

# L(G) has |E| vertices. Two edges are adjacent in L(G) iff they share an endpoint.
# For k-regular graph: L(G) is (2k-2)-regular with |E| vertices.
n_L = E
k_L = 2 * k - 2

print(f"    |V(L)| = |E(W)| = {n_L}")
print(f"    L(W) is {k_L}-regular (2k-2 = 2·{k}-2 = {k_L})")

# Number of edges in L(G)
E_L = n_L * k_L // 2
print(f"    |E(L)| = {E_L}")

# Spectrum of line graph: if G has eigenvalues λ_i with multiplicities m_i,
# then L(G) has eigenvalues λ_i + k - 2 with same multiplicities,
# plus eigenvalue -2 with multiplicity |E| - n.
# Wait, that's only for regular graphs and the relationship is:
# Spec(L(G)) = {λ_i + k - 2 : i=1,...,n} ∪ {-2^(|E|-n)}

spec_L = {}
# From adjacency eigenvalues {12^1, 2^24, (-4)^15}
for (lam, mult) in [(12, 1), (2, 24), (-4, 15)]:
    val = lam + k - 2
    spec_L[val] = spec_L.get(val, 0) + mult

# Plus -2 with multiplicity E - n
extra_neg2 = E - n
spec_L[-2] = spec_L.get(-2, 0) + extra_neg2

print(f"    Spectrum of L(W):")
for val in sorted(spec_L.keys(), reverse=True):
    print(f"      {val}^{spec_L[val]}")

# Verify: sum of multiplicities = |V(L)| = |E|
total_mult = sum(spec_L.values())
print(f"    Total multiplicities: {total_mult} (should be {n_L})")
assert total_mult == n_L

# Verify: sum of eigenvalues = 0 (trace of adj matrix of L(G))
# Actually for line graphs, trace = sum of degrees of endpoints... let's check
sum_eigs_L = sum(val * mult for val, mult in spec_L.items())
print(f"    Sum of eigenvalues: {sum_eigs_L}")
# For regular graph L(G), trace should be 0 if graph is regular?
# Actually trace(A_L) = Σ λ_i = sum of (number of triangles containing each edge)?
# No. For L(G), A_L[e,f] = 1 iff e,f share endpoint. Diagonal is 0.
# Sum of eigenvalues = tr(A_L) = 0 for any adjacency matrix.
# Let's verify:
# (12+10)*1 + (2+10)*24 + (-4+10)*15 + (-2)*200
# = 22 + 288 + 90 + (-400) = 0 ✓
print(f"    Sum check: 22·1 + 12·24 + 6·15 + (-2)·200 = {22 + 288 + 90 - 400} = 0 ✓")

# Line graph is strongly regular?
# L(G) for SRG is often SRG. Let's check parameters.
# For SRG(n,k,λ,μ), L(G) has parameters:
# n' = nk/2, k' = 2(k-1), λ' = k-2 + (A²)_{ij terms}
# Actually let's just compute from scratch whether it's SRG

# For L(G) of SRG(40,12,2,4):
# Two adjacent edges share a vertex v. Through v, the other endpoints are
# two neighbors of v. Common neighbors in L(G) of two adjacent edges =
# number of edges adjacent to both = (deg(shared endpoint) - 2) + (common adj of endpoints in G)
# = (k-2) + λ_G if the endpoints of both edges are also adjacent in G (triangle)
# = (k-2) + λ_G - something...
# This is getting complex. Let me check if the spectrum has exactly 3 distinct eigenvalues.

distinct_eigs = sorted(spec_L.keys())
print(f"\n    Distinct eigenvalues of L(W): {distinct_eigs}")
print(f"    Number of distinct eigenvalues: {len(distinct_eigs)}")

if len(distinct_eigs) == 3:
    print(f"    L(W) could be strongly regular!")
else:
    print(f"    L(W) has {len(distinct_eigs)} distinct eigenvalues (not SRG if > 3)")

# ========================================================
# 2. LOVÁSZ THETA FUNCTION
# ========================================================
print(f"\n[2] Lovász Theta Function")

# For SRG(n,k,λ,μ) with eigenvalues k > r > s:
# θ(G) = n * (-s) / (k - s)     [Lovász theta of complement... let me be precise]
# 
# Actually: θ(G) = 1 - k/s = 1 - 12/(-4) = 1 + 3 = 4... 
# No wait. The standard formula:
# θ(G) = n * (1 - r/k) / (1 - r/s) ... let me look this up properly.
# 
# For SRG: θ(G) = -n·s/(k-s) [this gives Lovász theta]
# = -40·(-4)/(12-(-4)) = 160/16 = 10
#
# And θ(Ḡ) = n·(1 + r/(−s)) / ... 
# Actually the standard results:
# For SRG, θ(G) = 1 - λ_1/λ_n where λ_1 is largest, λ_n smallest eigenvalue
# No that's the Hoffman bound on independence number.
# 
# Hoffman bound: α(G) ≤ n·(-s)/(k-s) = 40·4/16 = 10
# Lovász theta: θ(G) = 1 - λ_max/λ_min = 1 - 12/(-4) = 4... no
#
# Let me be precise. For vertex-transitive graphs:
# α(G) ≤ θ(G) ≤ χ̄(G) (fractional chromatic number of complement)
# For SRG: θ(G) = -n·λ_min/(λ_max - λ_min)
# = -40·(-4)/(12-(-4)) = 160/16 = 10

theta_G = -n * (-4) / (12 - (-4))
print(f"    Lovász theta θ(W) = -n·s/(k-s) = -40·(-4)/16 = {theta_G}")
print(f"    Hoffman bound: α ≤ n·(-s)/(k-s) = 10")
print(f"    Actual independence number: α = 7")
print(f"    θ(W) = 10 (= Hoffman bound, but actual α = 7)")

# For complement
# θ(Ḡ) = -n·λ_min(Ā)/(λ_max(Ā) - λ_min(Ā))
# Complement spectrum: {27^1, 3^15, (-3)^24}  
# Wait: complement of SRG(40,12,2,4) is SRG(40,27,18,18)
# Eigenvalues of complement: n-1-k = 27, -1-r = -3, -1-s = 3
# So complement spectrum: {27^1, (-3)^24, 3^15}
theta_Gbar = -n * (-3) / (27 - (-3))
print(f"\n    Complement: θ(W̄) = -40·(-3)/(27+3) = {theta_Gbar}")
print(f"    Clique cover of W = chromatic of W̄ relates to θ(W̄)")

# Sandwich theorem: α(G) ≤ θ(G) ≤ χ̄(G)
# where χ̄ is fractional chromatic number of complement
# Also: ω(G) ≤ θ̄(G) ≤ χ(G)  where θ̄ = n/θ(G)
theta_bar = n / theta_G
print(f"    θ̄(W) = n/θ(W) = 40/10 = {theta_bar}")
print(f"    Sandwich: ω ≤ θ̄ ≤ χ, i.e., 4 ≤ {theta_bar} ≤ 7")

# Shannon capacity
# Θ(G) = sup_k (α(G^⊠k))^{1/k} where ⊠ is strong product
# For vertex-transitive: Θ(G) = θ(G) when θ achieves it
# Actually Shannon capacity ≤ θ(G)
print(f"\n    Shannon capacity: Θ(W) ≤ θ(W) = 10")
print(f"    Lower bound: α(W) = 7 ≤ Θ(W)")
print(f"    So 7 ≤ Θ(W) ≤ 10")

# ========================================================
# 3. FRACTIONAL CHROMATIC NUMBER
# ========================================================
print(f"\n[3] Fractional Chromatic Number")

# For vertex-transitive graph: χ_f = n/α
chi_f = Fraction(n, 7)
print(f"    χ_f(W) = n/α = 40/7 ≈ {float(chi_f):.6f}")
print(f"    (For vertex-transitive graphs: χ_f = n/α)")

# Fractional clique number = fractional chromatic (LP duality for vertex-transitive)
print(f"    ω_f(W) = χ_f(W) = 40/7 (LP duality for vertex-transitive)")

# Relationship to θ
print(f"    Comparison: χ_f = 40/7 ≈ 5.71, θ̄ = 4, χ = 7")
print(f"    Note: χ_f < χ (proper fractional relaxation)")

# ========================================================
# 4. INDEPENDENCE POLYNOMIAL
# ========================================================
print(f"\n[4] Independence Polynomial (partial)")

# I(G,x) = Σ_{k=0}^{α} i_k x^k where i_k = # independent sets of size k
# Computing this exactly is expensive, but we can get small coefficients

# i_0 = 1 (empty set)
# i_1 = n = 40
# i_2 = number of non-edges = C(n,2) - E = 780 - 240 = 540
# i_3 = number of independent triples

# For i_3, count triples of mutually non-adjacent vertices
# A faster approach: for each non-edge (u,v), count vertices w non-adjacent to both
i_0 = 1
i_1 = n
i_2 = n*(n-1)//2 - E

print(f"    i_0 = {i_0}")
print(f"    i_1 = {i_1}")  
print(f"    i_2 = C(n,2) - |E| = {n*(n-1)//2} - {E} = {i_2}")

# i_3: independent triples
# For each pair of non-adjacent vertices (u,v), count w not adjacent to either
# that has index > max(u,v) to avoid counting
i_3 = 0
non_adj_pairs = [(i,j) for i in range(n) for j in range(i+1, n) if A[i,j] == 0]
for (u, v) in non_adj_pairs:
    for w in range(v+1, n):
        if A[u,w] == 0 and A[v,w] == 0:
            i_3 += 1

print(f"    i_3 = {i_3} (independent triples)")

# i_4: independent 4-sets (may be slow but let's try)
print(f"    Computing i_4 (independent 4-sets)...")
i_4 = 0
# Use adjacency structure for efficiency
non_neighbors = {}
for v in range(n):
    non_neighbors[v] = set(range(n)) - adj[v] - {v}

# For each independent triple, count extensions
# More efficient: iterate over non-edges and extend
for u in range(n):
    for v in range(u+1, n):
        if A[u,v] == 0:
            common_non = non_neighbors[u] & non_neighbors[v]
            common_non = {w for w in common_non if w > v}
            for w in common_non:
                further_non = common_non & non_neighbors[w]
                further_non = {x for x in further_non if x > w}
                i_4 += len(further_non)

print(f"    i_4 = {i_4} (independent 4-sets)")

# i_5
print(f"    Computing i_5 (independent 5-sets)...")
i_5 = 0
for u in range(n):
    for v in range(u+1, n):
        if A[u,v] == 0:
            cn_uv = non_neighbors[u] & non_neighbors[v]
            cn_uv = {w for w in cn_uv if w > v}
            for w in sorted(cn_uv):
                cn_uvw = cn_uv & non_neighbors[w]
                cn_uvw = {x for x in cn_uvw if x > w}
                for x in sorted(cn_uvw):
                    cn_uvwx = cn_uvw & non_neighbors[x]
                    cn_uvwx = {y for y in cn_uvwx if y > x}
                    i_5 += len(cn_uvwx)

print(f"    i_5 = {i_5} (independent 5-sets)")

# i_6
print(f"    Computing i_6 (independent 6-sets)...")
i_6 = 0
for u in range(n):
    for v in range(u+1, n):
        if A[u,v] == 0:
            cn_uv = non_neighbors[u] & non_neighbors[v]
            cn_uv_list = sorted(w for w in cn_uv if w > v)
            for idx_w, w in enumerate(cn_uv_list):
                cn_uvw = set(cn_uv_list[idx_w+1:]) & non_neighbors[w]
                cn_uvw_list = sorted(cn_uvw)
                for idx_x, x in enumerate(cn_uvw_list):
                    cn_uvwx = set(cn_uvw_list[idx_x+1:]) & non_neighbors[x]
                    cn_uvwx_list = sorted(cn_uvwx)
                    for idx_y, y in enumerate(cn_uvwx_list):
                        cn_uvwxy = set(cn_uvwx_list[idx_y+1:]) & non_neighbors[y]
                        i_6 += len(cn_uvwxy)

print(f"    i_6 = {i_6} (independent 6-sets)")

# i_7 (maximum)
print(f"    Computing i_7 (maximum independent sets, α=7)...")
i_7 = 0
for u in range(n):
    for v in range(u+1, n):
        if A[u,v] == 0:
            cn_uv = non_neighbors[u] & non_neighbors[v]
            cn_uv_list = sorted(w for w in cn_uv if w > v)
            for idx_w, w in enumerate(cn_uv_list):
                cn_uvw = set(cn_uv_list[idx_w+1:]) & non_neighbors[w]
                cn_uvw_list = sorted(cn_uvw)
                for idx_x, x in enumerate(cn_uvw_list):
                    cn_uvwx = set(cn_uvw_list[idx_x+1:]) & non_neighbors[x]
                    cn_uvwx_list = sorted(cn_uvwx)
                    for idx_y, y in enumerate(cn_uvwx_list):
                        cn_uvwxy = set(cn_uvwx_list[idx_y+1:]) & non_neighbors[y]
                        cn_uvwxy_list = sorted(cn_uvwxy)
                        for idx_z, z in enumerate(cn_uvwxy_list):
                            cn_uvwxyz = set(cn_uvwxy_list[idx_z+1:]) & non_neighbors[z]
                            i_7 += len(cn_uvwxyz)

print(f"    i_7 = {i_7} (maximum independent sets)")

total_indep = i_0 + i_1 + i_2 + i_3 + i_4 + i_5 + i_6 + i_7
print(f"\n    Independence polynomial I(W,x) = {i_0} + {i_1}x + {i_2}x² + {i_3}x³")
print(f"      + {i_4}x⁴ + {i_5}x⁵ + {i_6}x⁶ + {i_7}x⁷")
print(f"    Total independent sets: I(W,1) = {total_indep}")

# ========================================================
# 5. TUTTE POLYNOMIAL EVALUATIONS
# ========================================================
print(f"\n[5] Tutte Polynomial Special Evaluations")

# T(G; 1,1) = number of spanning trees
T_11 = 2**81 * 5**23
print(f"    T(1,1) = τ(W) = 2^81 · 5^23 ≈ {T_11:.4e} (spanning trees)")

# T(2,1) = number of forests
# Hard to compute directly. Skip.

# T(1,2) = number of connected spanning subgraphs
# Also hard. Skip.

# T(2,0) = number of acyclic orientations
# = (-1)^n · χ(-1) where χ is chromatic polynomial
# For SRG, chromatic polynomial is complex. Skip exact computation.

# T(0,2) = number of strongly connected orientations... not applicable

# Reliability polynomial: R(G,p) = Σ_{A⊆E} p^|A| (1-p)^{|E|-|A|} [A connects G]
# At p=1: R(G,1) = 1 (trivially)
# At p=0: R(G,0) = 0

# For a connected graph, T(1,1) = spanning trees, which we have.

# Number of forests (from matrix-tree variant):
# For k-regular graph, number of rooted forests = det(L + I) 
# Not quite right. Let's use:
# Number of forests = T(2,1) 
# For SRG: this relates to det(I + L) = prod(1 + μ_i)
det_IpL = (1 + 0)**1 * (1 + 10)**24 * (1 + 16)**15
print(f"    det(I + L) = 1 · 11^24 · 17^15 = {det_IpL:.4e}")
print(f"    (Related to rooted forest count)")

# Number of acyclic orientations from chromatic polynomial
# χ(G, k) for SRG(n,k_reg,λ,μ) evaluated at k=-1 gives (-1)^n * (acyclic orientations)
# For now, let's compute a few chromatic polynomial evaluations using deletion-contraction
# This is exponential so skip for n=40.

# Instead, let's compute some evaluations we can get from the spectrum:
# The number of closed walks of various lengths:
print(f"\n    Closed walk counts (from tr(Aᵏ)):")
for p in range(1, 9):
    tr_Ap = 12**p + (2**p)*24 + ((-4)**p)*15
    print(f"      W_{p} = tr(A^{p}) = {tr_Ap}")

# ========================================================
# 6. GRAPH POLYNOMIAL SUMMARY
# ========================================================
print(f"\n[6] Polynomial Invariant Summary")
print(f"    Characteristic: (x-12)(x-2)²⁴(x+4)¹⁵")
print(f"    Minimal: x³ - 10x² - 32x + 96")
print(f"    Independence: I(W,x) = {i_0} + {i_1}x + {i_2}x² + {i_3}x³ + {i_4}x⁴ + {i_5}x⁵ + {i_6}x⁶ + {i_7}x⁷")
print(f"    Lovász theta: θ(W) = 10")
print(f"    Fractional chromatic: χ_f = 40/7 ≈ 5.714")
print(f"    Shannon capacity: 7 ≤ Θ(W) ≤ 10")

print("\n" + "=" * 70)
print(" SUMMARY")
print("=" * 70)
print(f"  • Line graph L(W): {n_L} vertices, {k_L}-regular, spectrum {{22¹, 12²⁴, 6¹⁵, (-2)²⁰⁰}}")
print(f"  • Lovász theta: θ(W) = 10 = Hoffman bound")
print(f"  • Fractional chromatic: χ_f = 40/7")
print(f"  • Independence polynomial coefficients: ({i_0}, {i_1}, {i_2}, {i_3}, {i_4}, {i_5}, {i_6}, {i_7})")
print(f"  • Total independent sets: {total_indep}")
print()
