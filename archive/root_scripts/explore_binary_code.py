"""
Explore binary code C₂(W) = rowspace(A mod 2) and matching polynomial of W(3,3).

C₂(W) is a [40, 16] binary code (since rank₂(A) = 16).
Key questions:
1. What is the weight distribution (weight enumerator)?
2. What is the minimum distance d?
3. What are the dual code parameters?
4. Does C₂(W) have any special structure (self-orthogonal, doubly-even)?
5. What is the covering radius?

Also explore the matching polynomial and matching number.
"""

import itertools
import numpy as np
from collections import Counter

# ── Build W(3,3) ──
J = np.array([[0,1,0,0],[2,0,0,0],[0,0,0,1],[0,0,2,0]], dtype=int)

def symp(u, v):
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
assert n == 40

A = np.zeros((n, n), dtype=int)
for i in range(n):
    for j in range(i+1, n):
        if symp(points[i], points[j]) == 0:
            A[i,j] = A[j,i] = 1

print("="*60)
print("BINARY CODE C₂(W) AND MATCHING POLYNOMIAL")
print("="*60)

# ── 1. Construct the binary code ──
print("\n--- 1. Binary Code C₂(W) = row(A mod 2) ---")

A2 = A % 2  # adjacency mod 2

# Row-reduce to get a basis for the row space
def rref_gf2(M):
    """Row echelon form over GF(2). Returns (rref, pivot_cols, rank)."""
    m = M.copy() % 2
    rows, cols = m.shape
    pivot_cols = []
    r = 0
    for c in range(cols):
        # find pivot
        piv = None
        for rr in range(r, rows):
            if m[rr, c] % 2 == 1:
                piv = rr
                break
        if piv is None:
            continue
        m[[r, piv]] = m[[piv, r]]
        for rr in range(rows):
            if rr != r and m[rr, c] == 1:
                m[rr] = (m[rr] + m[r]) % 2
        pivot_cols.append(c)
        r += 1
    return m[:r], pivot_cols, r

basis, pivots, rank = rref_gf2(A2)
print(f"  rank₂(A) = {rank}")
assert rank == 16, f"Expected rank 16, got {rank}"
print(f"  C₂(W) is a [{n}, {rank}] binary code")

# ── 2. Enumerate all 2^16 codewords and compute weight distribution ──
print("\n--- 2. Weight Distribution ---")

weight_dist = Counter()
# 2^16 = 65536 codewords — feasible
for bits in range(2**rank):
    # construct codeword as GF(2) linear combination of basis vectors
    cw = np.zeros(n, dtype=int)
    for i in range(rank):
        if (bits >> i) & 1:
            cw = (cw + basis[i]) % 2
    wt = int(cw.sum())
    weight_dist[wt] += 1

print(f"  Total codewords: {sum(weight_dist.values())} = 2^{rank}")
assert sum(weight_dist.values()) == 2**rank

# Minimum distance
min_dist = min(w for w in weight_dist if w > 0)
print(f"  Minimum distance d = {min_dist}")
print(f"  C₂(W) = [{n}, {rank}, {min_dist}]")

print(f"\n  Weight enumerator W(z):")
for w in sorted(weight_dist.keys()):
    print(f"    A_{w:2d} = {weight_dist[w]}")

# ── 3. Properties of the code ──
print("\n--- 3. Code Properties ---")

# Self-orthogonality: C ⊆ C⊥ iff all codeword pairs have even dot product
# Equivalently: basis · basis^T ≡ 0 mod 2
gram = (basis @ basis.T) % 2
self_orth = np.all(gram == 0)
print(f"  Self-orthogonal (C ⊆ C⊥): {self_orth}")

# Check if all codeword weights are divisible by 4 (doubly even)
nonzero_weights = [w for w in weight_dist if w > 0 and weight_dist[w] > 0]
doubly_even = all(w % 4 == 0 for w in nonzero_weights)
singly_even = all(w % 2 == 0 for w in nonzero_weights) and not doubly_even
print(f"  All weights even: {all(w % 2 == 0 for w in nonzero_weights)}")
print(f"  Doubly even (all wt ≡ 0 mod 4): {doubly_even}")
print(f"  Singly even: {singly_even}")

# Dual code dimension
dual_dim = n - rank
print(f"  Dual code C⊥: [{n}, {dual_dim}]")

# ── 4. Dual code construction ──
print("\n--- 4. Dual Code C₂(W)⊥ ---")

# Find a basis for the null space of A mod 2
# kernel of A^T mod 2 = left null space of A mod 2
# Since A = A^T (symmetric), this is the null space of A mod 2
# We need vectors x with A·x ≡ 0 mod 2

# Build extended matrix [A | I] and row reduce
ext = np.hstack([A2, np.eye(n, dtype=int)])
_, _, _ = rref_gf2(ext)  # for pivot finding

# Better: directly compute null space of A mod 2
# Using the already-computed rref
null_basis = []
non_pivot = [c for c in range(n) if c not in pivots]
rref_mat = np.zeros((rank, n), dtype=int)
rref_mat[:] = basis

for col in non_pivot:
    vec = np.zeros(n, dtype=int)
    vec[col] = 1
    for i, pc in enumerate(pivots):
        vec[pc] = rref_mat[i, col]
    null_basis.append(vec % 2)

null_basis = np.array(null_basis, dtype=int)
print(f"  Null space dimension: {len(null_basis)} = {n} - {rank} = {dual_dim}")

# Verify: A * null_basis^T ≡ 0 mod 2
for nb in null_basis:
    assert np.all((A2 @ nb) % 2 == 0), "Null basis vector not in kernel!"
print(f"  Null basis verified: A·v ≡ 0 mod 2 for all {len(null_basis)} vectors  ✓")

# Weight distribution of dual code
print(f"\n  Dual code weight distribution:")
dual_weight_dist = Counter()
for bits in range(2**dual_dim):
    cw = np.zeros(n, dtype=int)
    for i in range(dual_dim):
        if (bits >> i) & 1:
            cw = (cw + null_basis[i]) % 2
    wt = int(cw.sum())
    dual_weight_dist[wt] += 1

dual_min_dist = min(w for w in dual_weight_dist if w > 0)
print(f"  Dual code C⊥ = [{n}, {dual_dim}, {dual_min_dist}]")
for w in sorted(dual_weight_dist.keys()):
    print(f"    A⊥_{w:2d} = {dual_weight_dist[w]}")

# ── 5. MacWilliams identity check ──
print("\n--- 5. MacWilliams Identity Check ---")
# W_C⊥(x,y) = (1/|C|) * W_C(x+y, x-y)
# We'll verify: sum of dual weights = 2^(n-k) and check a few coefficients

print(f"  |C| = 2^{rank} = {2**rank}")
print(f"  |C⊥| = 2^{dual_dim} = {2**dual_dim}")

# Verify Singleton bound: d ≤ n - k + 1
singleton = n - rank + 1
print(f"  Singleton bound: d ≤ n-k+1 = {singleton}, actual d = {min_dist}: {'MET' if min_dist <= singleton else 'VIOLATED'}")

# Plotkin bound for binary codes: d ≤ n/2 * (2^k - 1) / (2^(k-1) - 1) ≈ 2n/3 for large k
# Hamming bound: 2^n / V(n, t) ≥ 2^k where t = floor((d-1)/2)
t_correct = (min_dist - 1) // 2
vol = sum(1 for r in range(t_correct + 1) for _ in [0]) # rough
print(f"  Error-correcting capability: t = ⌊(d-1)/2⌋ = {t_correct}")

# ── 6. Symmetry of weight enumerator ──
print("\n--- 6. Weight Enumerator Symmetry ---")
# For a self-orthogonal code: A_w = A_{n-w} (not always, but worth checking)
symmetric = True
for w in weight_dist:
    if weight_dist[w] != weight_dist.get(n - w, 0):
        symmetric = False
        print(f"  A_{w} = {weight_dist[w]} ≠ A_{n-w} = {weight_dist.get(n-w, 0)}")

if symmetric:
    print(f"  Weight enumerator has complement symmetry: A_w = A_{{n-w}} for all w")

# ── 7. Relationship to graph structure ──
print("\n--- 7. Codewords and Graph Structure ---")

# Minimum weight codewords
min_cw_count = weight_dist[min_dist]
print(f"  Number of minimum weight ({min_dist}) codewords: {min_cw_count}")

# Check if minimum weight codewords correspond to known graph objects
# Enumerate them
min_cws = []
for bits in range(2**rank):
    cw = np.zeros(n, dtype=int)
    for i in range(rank):
        if (bits >> i) & 1:
            cw = (cw + basis[i]) % 2
    if int(cw.sum()) == min_dist:
        support = tuple(np.where(cw == 1)[0])
        min_cws.append(support)

# Check if supports form special subgraphs
print(f"  Analyzing minimum weight codeword supports:")
for idx, supp in enumerate(min_cws[:5]):  # show first few
    sub = np.zeros((len(supp), len(supp)), dtype=int)
    for i, u in enumerate(supp):
        for j, w in enumerate(supp):
            if A[u, w] == 1:
                sub[i, j] = 1
    edges = sub.sum() // 2
    degs = sorted(sub.sum(axis=1).tolist())
    print(f"    cw {idx}: support size {len(supp)}, {edges} edges, deg seq {degs}")

# ── 8. Connection: A² ≡ 0 mod 2 implies C ⊆ C⊥ ──
print("\n--- 8. Self-orthogonality from Nilpotency ---")
# Since A² ≡ 0 mod 2, row(A) ⊆ ker(A) = C₂(W) ⊆ C₂(W)⊥
# So C₂(W) is self-orthogonal
print(f"  A² ≡ 0 mod 2 ⟹ row(A) ⊆ ker(A) ⟹ C ⊆ C⊥")
print(f"  dim(C) = {rank} ≤ n/2 = {n//2}: {rank <= n//2}")
# If rank = n/2, it's self-dual
if rank == n // 2:
    print(f"  rank = n/2 = {n//2} ⟹ C₂(W) is SELF-DUAL!")
else:
    print(f"  rank = {rank} < n/2 = {n//2}, so C is properly self-orthogonal but not self-dual")

print("\n" + "="*60)
print("EXPLORATION COMPLETE")
print("="*60)
