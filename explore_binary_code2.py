"""
Focused exploration of C₂(W) = [40, 16, 8] binary code.
Skip brute-force dual enumeration; use MacWilliams transform instead.
"""
import itertools
import numpy as np
from collections import Counter
from fractions import Fraction

# ── Build W(3,3) ──
J = np.array([[0,1,0,0],[2,0,0,0],[0,0,0,1],[0,0,2,0]], dtype=int)
def symp(u, v): return int(np.dot(u, np.dot(J, v))) % 3

points = []
for combo in itertools.product(range(3), repeat=4):
    if any(x != 0 for x in combo):
        v = np.array(combo, dtype=int)
        for i in range(4):
            if v[i] != 0:
                if v[i] == 1: points.append(v.copy())
                break
n = len(points); assert n == 40
A = np.zeros((n, n), dtype=int)
for i in range(n):
    for j in range(i+1, n):
        if symp(points[i], points[j]) == 0: A[i,j] = A[j,i] = 1

# ── Row-reduce A mod 2 ──
A2 = A % 2
def rref_gf2(M):
    m = M.copy() % 2; rows, cols = m.shape; pivot_cols = []; r = 0
    for c in range(cols):
        piv = None
        for rr in range(r, rows):
            if m[rr, c] == 1: piv = rr; break
        if piv is None: continue
        m[[r, piv]] = m[[piv, r]]
        for rr in range(rows):
            if rr != r and m[rr, c] == 1: m[rr] = (m[rr] + m[r]) % 2
        pivot_cols.append(c); r += 1
    return m[:r], pivot_cols, r

basis, pivots, rank = rref_gf2(A2)
assert rank == 16
print(f"C₂(W) = [{n}, {rank}] binary code")

# ── Weight distribution (2^16 = 65536 is fast) ──
weight_dist = Counter()
for bits in range(2**rank):
    cw = np.zeros(n, dtype=int)
    for i in range(rank):
        if (bits >> i) & 1: cw = (cw + basis[i]) % 2
    weight_dist[int(cw.sum())] += 1

print(f"\nWeight enumerator of C₂(W) = [{n}, {rank}, {min(w for w in weight_dist if w > 0)}]:")
A_w = {}
for w in sorted(weight_dist.keys()):
    A_w[w] = weight_dist[w]
    print(f"  A_{w:2d} = {weight_dist[w]}")

# Verify complement symmetry: A_w = A_{n-w}
print(f"\nComplement symmetry A_w = A_{{n-w}}:")
sym = all(A_w.get(w, 0) == A_w.get(n - w, 0) for w in range(n+1))
print(f"  Holds: {sym}")
print(f"  (because 𝟏 ∈ C: A·𝟏 = k·𝟏 ≡ 0 mod 2, so row(A) contains 𝟏)")

# Verify doubly even
de = all(w % 4 == 0 for w in A_w if A_w[w] > 0 and w > 0)
print(f"\nDoubly even: {de}")

# Self-orthogonal
gram = (basis @ basis.T) % 2
so = np.all(gram == 0)
print(f"Self-orthogonal (C ⊆ C⊥): {so}")

# ── MacWilliams transform ──
print(f"\n--- MacWilliams Transform → Dual Weight Distribution ---")
# For binary code C of length n, dimension k:
# B_j = (1/|C|) * sum_{i=0}^{n} A_i * K_j(i)
# where K_j(i) = sum_{s=0}^{j} (-1)^s C(i,s) C(n-i, j-s) is Krawtchouk polynomial
from math import comb

def krawtchouk(j, i, nn):
    """Krawtchouk polynomial K_j(i; n) over binary field."""
    return sum((-1)**s * comb(i, s) * comb(nn - i, j - s) 
               for s in range(j+1) if s <= i and j-s <= nn-i)

card_C = 2**rank
B_w = {}
for j in range(n+1):
    val = Fraction(0)
    for i in A_w:
        val += Fraction(A_w[i]) * Fraction(krawtchouk(j, i, n))
    val = val / Fraction(card_C)
    if val != 0:
        B_w[j] = int(val)

print(f"C⊥ = [{n}, {n - rank}] dual code weight distribution:")
dual_min = min(w for w in B_w if w > 0)
print(f"C⊥ = [{n}, {n - rank}, {dual_min}]")
for w in sorted(B_w.keys()):
    print(f"  B_{w:2d} = {B_w[w]}")

# Verify total
print(f"\n  Total dual codewords: {sum(B_w.values())} = 2^{n - rank} = {2**(n-rank)}")

# ── Analyze the 45 minimum weight codewords ──
print(f"\n--- Minimum Weight ({min(w for w in A_w if w > 0)}) Codewords ---")

min_d = min(w for w in A_w if w > 0)
min_cws = []
for bits in range(2**rank):
    cw = np.zeros(n, dtype=int)
    for i in range(rank):
        if (bits >> i) & 1: cw = (cw + basis[i]) % 2
    if int(cw.sum()) == min_d:
        min_cws.append(tuple(np.where(cw == 1)[0]))

print(f"  Count: {len(min_cws)}")

# Check subgraph structure of each support
edge_counts = Counter()
for supp in min_cws:
    edges = 0
    for i, u in enumerate(supp):
        for w in supp[i+1:]:
            if A[u, w] == 1: edges += 1
    edge_counts[edges] += 1
print(f"  Edge counts in support subgraphs: {dict(edge_counts)}")

# Check if supports are related to spreads or other structures
# Each support has 8 vertices. Are they independent sets? unions of lines?
for idx, supp in enumerate(min_cws[:3]):
    sub = np.zeros((len(supp), len(supp)), dtype=int)
    for i, u in enumerate(supp):
        for j, w in enumerate(supp):
            if A[u, w] == 1: sub[i, j] = 1
    degs = sub.sum(axis=1)
    print(f"  cw {idx}: support = {supp}, degrees in induced subgraph: {degs.tolist()}")

# 45 = C(10,2) — could these be pairs of lines from a spread?
# Each spread has 10 lines. Symmetric difference of 2 disjoint 4-cliques = 8 vertices.
# Let's check if the supports are symmetric differences of line pairs

# Find all 4-cliques
cliques4 = []
for i in range(n):
    for j in range(i+1, n):
        if A[i,j] == 1:
            for c in range(j+1, n):
                if A[i,c] == 1 and A[j,c] == 1:
                    for d in range(c+1, n):
                        if A[i,d] == 1 and A[j,d] == 1 and A[c,d] == 1:
                            cliques4.append(frozenset([i,j,c,d]))

print(f"\n  Total 4-cliques (lines): {len(cliques4)}")

# Check: is each min-wt support a union of 2 disjoint lines?
union_count = 0
for supp in min_cws:
    s = set(supp)
    found = False
    for i, l1 in enumerate(cliques4):
        if l1.issubset(s):
            rem = s - l1
            if frozenset(rem) in cliques4:
                union_count += 1
                found = True
                break
    if not found:
        # Not a union of 2 disjoint lines
        pass

print(f"  Supports that are unions of 2 disjoint lines: {union_count}/{len(min_cws)}")

# ── Numerology ──
print(f"\n--- Numerological Connections ---")
print(f"  d = {min_d} = k - |s| = 12 - 4 = rank(E₈)")
print(f"  A₈ = 45 = C(10,2) = C(q²+1, 2)")
print(f"  A₁₂ = 1120 = 2·8·70 = 2·rank(E₈)·C(8,4)")
print(f"  A₂₀ = 32064")
print(f"  |C| = 2^16 = 2^(k+|s|)")
print(f"  |C⊥| = 2^24 = 2^(f_r) where f_r = 24")
print(f"  Dual dim = f_r = 24 (multiplicity of eigenvalue r=2)")

# Check: A₈ = 45 connections
# 45 = |W(E₆)|/|PSp(4,3)| * something?
# 45 = 3(q²+1)(q²)/2 for q=3: 3*10*9/2 = 135 no
# 45 = (n-k)(n-k-1)/... = 27*26/... no
# 45 = C(10,2) where 10 = q²+1 = Hoffman bound
print(f"  45 = C(10,2): 10 = q²+1 = Hoffman bound for independence")

# ── Summary of doubly-even self-orthogonal code ──
print(f"\n=== SUMMARY ===")
print(f"C₂(W) = [{n}, {rank}, {min_d}] doubly-even self-orthogonal binary code")
print(f"  dim = rank₂(A) = {rank} = k + |s|")
print(f"  d_min = {min_d} = k - |s| = rank(E₈)")
print(f"  Self-orth: A² ≡ 0 mod 2 ⟹ C ⊆ C⊥")
print(f"  Doubly even: all weights ≡ 0 mod 4")
print(f"  Complement symmetric: A_w = A_{{n-w}} (since 𝟏 ∈ C)")
print(f"  C⊥ = [{n}, {n-rank}, {dual_min}]")
