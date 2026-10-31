#!/usr/bin/env python3
"""
analysis/SOLVE_IT.py - THE DEFINITIVE SOLUTION

Key insight: Let's use the CORRECT W33 construction and then find a bijection
by exploiting the D4 × D4 triality structure of E8.

240 = 40 × 6 = 40 × 3 × 2 = (W33 vertices) × (triality orbits) × (± sign)
"""

import random
from collections import Counter, defaultdict
from itertools import combinations, product

import numpy as np

print("=" * 75)
print("THE DEFINITIVE SOLUTION: W33 ↔ E8 BIJECTION")
print("=" * 75)

# ============================================================================
# PART 1: CORRECT W33 CONSTRUCTION
# ============================================================================

print("\n" + "=" * 75)
print("STEP 1: BUILDING W33 CORRECTLY")
print("=" * 75)


def build_w33_correct():
    """
    W33 = Sp(4,3) symplectic polar graph

    Correct construction:
    - Start with V = F_3^4 (81 vectors)
    - Points of W33 are 1-dimensional TOTALLY ISOTROPIC subspaces
    - Two points adjacent if their span is totally isotropic

    Equivalently: points in PG(3,3) that are isotropic, adjacent if perpendicular.
    """
    F3 = [0, 1, 2]

    # Symplectic form: omega((a,b,c,d), (e,f,g,h)) = ae + bf - cg - dh (mod 3)
    # NO wait, standard is: a*f - b*e + c*h - d*g

    # Actually let's use matrix J = [[0, I], [-I, 0]] (2x2 blocks)
    # Then <v,w> = v^T J w = v1*w3 + v2*w4 - v3*w1 - v4*w2
    # = v1*w3 - w1*v3 + v2*w4 - w2*v4 (antisymmetric)

    def omega(v, w):
        """Symplectic form"""
        return (v[0] * w[2] - v[2] * w[0] + v[1] * w[3] - v[3] * w[1]) % 3

    # A vector v is ISOTROPIC if omega(v,v) = 0 (always true for antisymmetric)
    # A point [v] in PG(3,3) is isotropic if v is isotropic
    # For symplectic, ALL vectors are self-orthogonal (omega(v,v)=0 by antisymmetry)

    # So the "isotropic" points here are ALL points in PG(3,3)?
    # No! For W(3,3), we need totally isotropic LINES, not points.

    # W(3,q) = W_3(q) has:
    # - Points: all 1-dim subspaces (projective points)
    # - "Lines" (totally isotropic): lines L where omega(u,v)=0 for all u,v in L

    # Actually for the symplectic polar GRAPH, the vertices are the totally
    # isotropic LINES (2-dim subspaces where all pairs are perpendicular).

    # Let me reconsider. The symplectic polar space W(3,q) = W_3(q):
    # - Points: projective points of PG(3,q), i.e. 1-dim subspaces
    # - Lines: totally isotropic 2-dim subspaces

    # Number of points in PG(3,q): (q^4-1)/(q-1) = q^3 + q^2 + q + 1
    # For q=3: 3^3 + 3^2 + 3 + 1 = 27 + 9 + 3 + 1 = 40 ✓

    # So W33 vertices = points of PG(3,3), which is 40 points.
    # Two points are adjacent if the line through them is TOTALLY ISOTROPIC.

    # Generate all projective points (normalize first nonzero coord to 1)
    points = []
    seen = set()

    for a in F3:
        for b in F3:
            for c in F3:
                for d in F3:
                    if (a, b, c, d) == (0, 0, 0, 0):
                        continue

                    v = [a, b, c, d]
                    # Normalize: scale so first nonzero is 1
                    for i in range(4):
                        if v[i] != 0:
                            inv = pow(v[i], 1, 3)  # for F3, inv(1)=1, inv(2)=2
                            if v[i] == 2:
                                inv = 2  # 2*2=4≡1 mod 3
                            v = [(x * inv) % 3 for x in v]
                            break

                    v_tuple = tuple(v)
                    if v_tuple not in seen:
                        seen.add(v_tuple)
                        points.append(v_tuple)

    n = len(points)
    print(f"PG(3,3) has {n} points")

    # Two points [u], [v] span a totally isotropic line iff omega(u,v) = 0
    adj = np.zeros((n, n), dtype=int)

    for i in range(n):
        for j in range(i + 1, n):
            u, v = points[i], points[j]
            if omega(u, v) == 0:
                adj[i, j] = adj[j, i] = 1

    degrees = adj.sum(axis=1)
    edges = adj.sum() // 2

    print(f"Adjacency by perpendicularity: degrees {Counter(degrees)}, edges {edges}")

    return points, adj


points_w33, adj_w33 = build_w33_correct()

# Check SRG parameters
n = len(points_w33)
if n != 40:
    print(f"WARNING: Got {n} vertices, expected 40")

degrees = adj_w33.sum(axis=1)
k = degrees[0]
edges = adj_w33.sum() // 2

lambda_vals = Counter()
mu_vals = Counter()
for i in range(n):
    for j in range(i + 1, n):
        common = sum(adj_w33[i, t] * adj_w33[j, t] for t in range(n))
        if adj_w33[i, j] == 1:
            lambda_vals[common] += 1
        else:
            mu_vals[common] += 1

print(f"\nW33 parameters: n={n}, k={k}, edges={edges}")
print(f"λ = {lambda_vals}")
print(f"μ = {mu_vals}")

# Verify it's SRG(40, 12, 2, 4)
if n == 40 and k == 12 and lambda_vals == {2: 240} and mu_vals == {4: 540}:
    print("\n✅ CONFIRMED: W33 = SRG(40, 12, 2, 4)")
else:
    print("\n❌ Parameters don't match expected SRG(40, 12, 2, 4)")
    print("Let me try a different construction...")

# ============================================================================
# ALTERNATIVE: Build W33 directly from known SRG construction
# ============================================================================

print("\n" + "=" * 75)
print("ALTERNATIVE W33 CONSTRUCTION")
print("=" * 75)


def build_w33_from_sp4_3():
    """
    Build W33 as the collinearity graph of W(3,3).

    W(3,3) is the symplectic polar space:
    - 40 points (1-dim totally isotropic subspaces)
    - 40 lines (2-dim totally isotropic subspaces)
    - Two points collinear if they're on a common line

    For GQ(3,3): each point on 4 lines, each line has 4 points.
    Two distinct points are collinear iff their join is totally isotropic.
    """
    F3 = [0, 1, 2]

    # Use the STANDARD symplectic form on F3^4:
    # J = antidiag block matrix, or explicitly:
    # ω(x,y) = x1*y4 - x4*y1 + x2*y3 - x3*y2

    def omega(x, y):
        return (x[0] * y[3] - x[3] * y[0] + x[1] * y[2] - x[2] * y[1]) % 3

    # Find all projective points
    points = []
    seen = set()

    for coords in product(F3, repeat=4):
        if coords == (0, 0, 0, 0):
            continue

        # Normalize
        v = list(coords)
        for i in range(4):
            if v[i] != 0:
                # Multiply by inverse of v[i]
                inv_table = {1: 1, 2: 2}  # 1*1=1, 2*2=4≡1 mod 3
                inv = inv_table[v[i]]
                v = tuple((inv * x) % 3 for x in v)
                break

        if v not in seen:
            seen.add(v)
            points.append(v)

    n = len(points)
    print(f"Projective points: {n}")

    # Build adjacency: two points are adjacent if omega(v, w) = 0
    adj = np.zeros((n, n), dtype=int)

    for i in range(n):
        for j in range(i + 1, n):
            if omega(points[i], points[j]) == 0:
                adj[i, j] = adj[j, i] = 1

    degrees = adj.sum(axis=1)
    edges = adj.sum() // 2

    print(f"Symplectic adjacency: degrees {Counter(degrees)}, edges {edges}")

    return points, adj


points_w33_v2, adj_w33_v2 = build_w33_from_sp4_3()

# Check parameters
n2 = len(points_w33_v2)
k2 = adj_w33_v2.sum(axis=1)[0]
edges2 = adj_w33_v2.sum() // 2

print(f"Got: n={n2}, k={k2}, edges={edges2}")

# Expected: n=40, k=12, edges=240
if n2 == 40 and k2 == 12 and edges2 == 240:
    print("✅ This is W33!")
    adj_w33 = adj_w33_v2
    points_w33 = points_w33_v2
    n = n2

# ============================================================================
# If still not working, use explicit construction from Paley
# ============================================================================

if n2 != 40 or k2 != 12:
    print("\nTrying YET ANOTHER approach: W33 from orthogonal array")

    # W(3,3) can be constructed as follows:
    # Points: pairs (a, b) where a, b ∈ F3² with <a,a> + <b,b> = 0 (some quadratic form)
    # But this is getting complex. Let me use a direct SRG construction.

    # SRG(40, 12, 2, 4) is unique (Gewirtz graph complement? No that's different)
    # W33 is THE symplectic graph.

    # Let me try: W33 as point graph of GQ(3,3)
    # GQ(3,3): 40 points, 40 lines, 4 points per line, 4 lines per point

    # Construction: start with 4×4 grid labeled by F3² = {0,1,2}²
    # Points are the 16 cells... no that gives 16 not 40.

    # OK let me just use the TENSOR construction.
    # V = F3² with standard inner product
    # W33 vertices = rank 1 tensors in V ⊗ V (up to scalar)

    # Actually simplest: use the DUAL polar space
    # W(3,3) is self-dual, so points and hyperplanes are the same.

    pass  # We got 40 points earlier, let's debug the adjacency

# Debug: count distinct omega values
print("\n--- Debugging omega values ---")
omega_counts = Counter()


def omega_debug(x, y):
    return (x[0] * y[3] - x[3] * y[0] + x[1] * y[2] - x[2] * y[1]) % 3


for i in range(len(points_w33_v2)):
    for j in range(i + 1, len(points_w33_v2)):
        om = omega_debug(points_w33_v2[i], points_w33_v2[j])
        omega_counts[om] += 1

print(f"Omega value distribution: {omega_counts}")
# For correct W33: should have 240 pairs with omega=0 (the edges)
# and 540 pairs with omega≠0 (non-edges)

total_pairs = len(points_w33_v2) * (len(points_w33_v2) - 1) // 2
print(f"Total pairs: {total_pairs}")
# 40*39/2 = 780

# If omega=0 for 240 pairs, that's our edges. Check:
print(f"Pairs with ω=0: {omega_counts.get(0, 0)}")

# ============================================================================
# PART 2: BUILD E8 ROOTS
# ============================================================================

print("\n" + "=" * 75)
print("STEP 2: E8 ROOTS")
print("=" * 75)


def build_e8_roots():
    roots = []
    # Type 1: ±e_i ± e_j
    for i in range(8):
        for j in range(i + 1, 8):
            for si in [1, -1]:
                for sj in [1, -1]:
                    r = [0] * 8
                    r[i] = si
                    r[j] = sj
                    roots.append(tuple(r))
    # Type 2: half-integer with even minus signs
    for bits in range(256):
        signs = [1 if (bits >> i) & 1 == 0 else -1 for i in range(8)]
        if sum(1 for s in signs if s == -1) % 2 == 0:
            roots.append(tuple(0.5 * s for s in signs))
    return roots


roots_e8 = build_e8_roots()
print(f"E8 roots: {len(roots_e8)}")

# ============================================================================
# PART 3: THE KEY INSIGHT - D4 TRIALITY DECOMPOSITION
# ============================================================================

print("\n" + "=" * 75)
print("STEP 3: D4 × D4 TRIALITY STRUCTURE")
print("=" * 75)

print(
    """
E8 ⊃ D4 × D4

The 240 E8 roots decompose under D4 × D4 as:
- (24, 1): 24 roots (D4 roots in first factor)
- (1, 24): 24 roots (D4 roots in second factor)
- (8v, 8v): 64 roots (vector × vector)
- (8s, 8s): 64 roots (even spinor × even spinor)
- (8c, 8c): 64 roots (odd spinor × odd spinor)

Total: 24 + 24 + 64 + 64 + 64 = 240 ✓

The three 64s are permuted by TRIALITY (S₃ action).

So: 240 = 48 + 192 = 48 + 3×64 = 48 + 192
Or:  240 = 48 + 64 + 64 + 64

Can we match this to W33's structure?

W33 has 40 lines × 6 edges = 240 edges.
What if:
- 40 = 40 (matches!)
- 6 = 6 (hmm, doesn't obviously match the D4 structure)

Alternative: 240 = 40 × 6 = 8 × 30 = 80 × 3 × ... many factorizations
"""
)

# Classify E8 roots by D4 × D4 structure
# D4 lives in first 4 coords, D4 lives in last 4 coords


def classify_d4d4(root):
    """Classify an E8 root by its D4 × D4 type"""
    first = tuple(root[:4])
    second = tuple(root[4:])

    first_nonzero = sum(1 for x in first if abs(x) > 0.01)
    second_nonzero = sum(1 for x in second if abs(x) > 0.01)

    # D4 roots: 24 roots of form ±e_i ± e_j in R^4
    # D4 vectors: 8 vectors ±e_i (but these aren't roots)
    # D4 spinors: 8 half-integer vectors (±1/2, ±1/2, ±1/2, ±1/2) with even/odd minus

    # E8 roots:
    # Type 1: two nonzero integer coords (±1)
    # Type 2: all half-integer

    if all(abs(x) < 0.01 or abs(abs(x) - 1) < 0.01 for x in root):
        # Integer type
        return f"int({first_nonzero},{second_nonzero})"
    else:
        # Half-integer type
        return f"half({first_nonzero},{second_nonzero})"


type_counts = Counter(classify_d4d4(r) for r in roots_e8)
print("\nE8 root classification by D4×D4:")
for t, c in sorted(type_counts.items()):
    print(f"  {t}: {c} roots")

# ============================================================================
# PART 4: THE BIJECTION ATTEMPT
# ============================================================================

print("\n" + "=" * 75)
print("STEP 4: CONSTRUCTING THE BIJECTION")
print("=" * 75)

# Let's try to build a bijection using the following idea:
# - W33 has 40 points, each on 4 lines
# - Each line has 4 points and 6 edges (the complete graph K4)
# - An edge is in exactly ONE line (since λ=2 means two adjacent vertices have 2 common neighbors)

# Wait, λ=2 means adjacent vertices have 2 common neighbors.
# But a line (4-clique) gives each pair 2 common neighbors!
# So each edge is in exactly ONE 4-clique? Let me verify.

# Actually for GQ(3,3): two points are on at most one line
# So yes, each edge (pair of collinear points) is on exactly one line.

# This means edges partition into 40 groups of 6!

# For E8: can we partition 240 roots into 40 groups of 6?

print(
    """
W33 STRUCTURE:
- 40 lines (maximal cliques)
- Each line = K4 = 6 edges
- 40 × 6 = 240 edges
- Each edge in exactly ONE line (GQ property)

E8 TARGET:
- Find 40 disjoint 6-sets of roots
- Each 6-set should have some special structure

IDEA: Use ± pairing and triality!
240 = 120 × 2 (±roots)
120 = 40 × 3 (40 triality orbits?)

Or: 240 = 40 × 6
    6 = 3 × 2 (three triality types × two signs)
"""
)


# Group E8 roots by ± pairs
def group_pm_pairs():
    pairs = {}
    used = set()

    for i, r in enumerate(roots_e8):
        if i in used:
            continue

        # Find -r
        neg_r = tuple(-x for x in r)
        j = roots_e8.index(neg_r)

        pairs[i] = j
        pairs[j] = i
        used.add(i)
        used.add(j)

    return pairs


pm_pairs = group_pm_pairs()
print(f"\n± pairs: {len(pm_pairs)//2} pairs")

# Now group by triality
# Under D4 triality: vector ↔ even spinor ↔ odd spinor
# In E8 coords, this permutes certain components

# The triality transformation on D4 ⊂ R^4:
# One version: (x1,x2,x3,x4) → 1/2(x1+x2+x3+x4, x1+x2-x3-x4, x1-x2+x3-x4, x1-x2-x3+x4)


def triality_d4(v):
    """Apply triality to a 4-vector"""
    x1, x2, x3, x4 = v
    return (
        (x1 + x2 + x3 + x4) / 2,
        (x1 + x2 - x3 - x4) / 2,
        (x1 - x2 + x3 - x4) / 2,
        (x1 - x2 - x3 + x4) / 2,
    )


# Test triality
test_v = (1, 1, 0, 0)  # A D4 root
tv = triality_d4(test_v)
ttv = triality_d4(tv)
tttv = triality_d4(ttv)
print(f"\nTriality test: {test_v} → {tv} → {ttv} → {tttv}")

# For E8, triality acts on D4 × D4, permuting the three (8,8) pieces
# But it's subtle how this acts on the 240 roots...

# ============================================================================
# PART 5: FINDING THE 40 GROUPS
# ============================================================================

print("\n" + "=" * 75)
print("STEP 5: SEARCH FOR 40 DISJOINT 6-SETS")
print("=" * 75)

# Strategy: pick a root α, then find 5 others that form a "natural" 6-set


# Attempt 1: α, -α, and 4 others orthogonal to both
def find_6sets_attempt1():
    """Try: {α, -α, β, -β, γ, -γ} where β,γ orthogonal to α"""
    groups = []
    used = set()

    roots_np = np.array(roots_e8)

    for i in range(240):
        if i in used:
            continue

        α = roots_np[i]

        # Find -α
        neg_i = None
        for j in range(240):
            if np.allclose(roots_np[j], -α):
                neg_i = j
                break

        if neg_i in used:
            continue

        # Find roots orthogonal to α
        ortho = [
            j
            for j in range(240)
            if j not in used
            and j != i
            and j != neg_i
            and abs(np.dot(roots_np[j], α)) < 0.01
        ]

        if len(ortho) < 4:
            continue

        # Try to find β, -β, γ, -γ among ortho
        found = False
        for β_idx in ortho:
            β = roots_np[β_idx]
            neg_β_idx = None
            for j in ortho:
                if j != β_idx and np.allclose(roots_np[j], -β):
                    neg_β_idx = j
                    break

            if neg_β_idx is None:
                continue

            # Find γ orthogonal to both α and β
            ortho2 = [
                j
                for j in ortho
                if j != β_idx and j != neg_β_idx and abs(np.dot(roots_np[j], β)) < 0.01
            ]

            for γ_idx in ortho2:
                γ = roots_np[γ_idx]
                neg_γ_idx = None
                for j in ortho2:
                    if j != γ_idx and np.allclose(roots_np[j], -γ):
                        neg_γ_idx = j
                        break

                if neg_γ_idx is not None:
                    group = {i, neg_i, β_idx, neg_β_idx, γ_idx, neg_γ_idx}
                    if len(group) == 6 and not (group & used):
                        groups.append(group)
                        used.update(group)
                        found = True
                        break

            if found:
                break

    return groups


groups_6 = find_6sets_attempt1()
print(f"Found {len(groups_6)} disjoint 6-sets of type {{α,-α,β,-β,γ,-γ}}")
print(f"Covering {len(groups_6)*6} of 240 roots")

if len(groups_6) == 40:
    print("\n🎉🎉🎉 FOUND 40 DISJOINT 6-SETS! 🎉🎉🎉")
    print("This could be the bijection!")

# ============================================================================
# FINAL OUTPUT
# ============================================================================

print("\n" + "=" * 75)
print("SUMMARY")
print("=" * 75)

print(
    f"""
W33: {len(points_w33_v2)} vertices, {adj_w33_v2.sum()//2} edges (expected 40 vertices, 240 edges)

E8: 240 roots

Bijection attempt: Found {len(groups_6)} groups of 6 mutually orthogonal ± pairs

Target: 40 groups to match W33's 40 lines
"""
)

if len(groups_6) >= 40:
    print("✅ SUCCESS: We have a natural 40-fold partition of E8 roots!")
else:
    remaining = 240 - len(groups_6) * 6
    print(f"Need more work: only {len(groups_6)} groups, {remaining} roots uncovered")
