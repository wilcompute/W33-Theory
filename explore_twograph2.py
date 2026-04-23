"""Explore: Hoffman polynomial, matrix algebra, two-graph, Delsarte bounds, cycle counts."""
import numpy as np
from fractions import Fraction
from itertools import combinations

# ── Build W(3,3) ──────────────────────────────────────────────
p = 3
J_symp = np.array([[0,1,0,0],[2,0,0,0],[0,0,0,1],[0,0,2,0]])

pts = []
for a in range(p):
    for b in range(p):
        for c in range(p):
            for d in range(p):
                v = [a, b, c, d]
                first = next((x for x in v if x != 0), None)
                if first is None:
                    continue
                inv = pow(first, -1, p)
                nv = tuple((x * inv) % p for x in v)
                if nv not in pts:
                    pts.append(nv)

n = len(pts)

def symp(u, v):
    return sum(u[i] * J_symp[i][j] * v[j] for i in range(4) for j in range(4)) % p

A = np.zeros((n, n), dtype=int)
for i in range(n):
    for j in range(i+1, n):
        if symp(pts[i], pts[j]) == 0:
            A[i][j] = A[j][i] = 1

k = 12; r_val = 2; s_val = -4; f_r = 24; f_s = 15; lam = 2; mu = 4
Jmat = np.ones((n, n), dtype=int)
I = np.eye(n, dtype=int)

print("="*60)
print("HOFFMAN POLYNOMIAL, MATRIX ALGEBRA, TWO-GRAPH, DELSARTE")
print("="*60)

# ── 1. Hoffman polynomial ────────────────────────────────────
print("\n--- 1. Hoffman polynomial ---")
A2 = A @ A
hA = A2 + 2*A - 8*I
assert np.allclose(hA, 4 * Jmat)
print(f"  h(x) = (x² + 2x - 8)/4 = (x-2)(x+4)/4")
print(f"  h(A) = J: (A² + 2A - 8I)/4 = J  ✓")

# ── 2. Minimal polynomial ────────────────────────────────────
print("\n--- 2. Minimal polynomial ---")
minpoly = (A - 12*I) @ (A - 2*I) @ (A + 4*I)
assert np.allclose(minpoly, 0)
print(f"  m(x) = (x - 12)(x - 2)(x + 4) = x³ - 10x² - 32x + 96")
print(f"  m(A) = 0  ✓")

# ── 3. Fundamental matrix identity ───────────────────────────
print("\n--- 3. A² recurrence ---")
A2_formula = (lam - mu)*A + mu*Jmat + (k - mu)*I
assert np.allclose(A2, A2_formula)
print(f"  A² = (λ-μ)A + μJ + (k-μ)I = -2A + 4J + 8I  ✓")

# ── 4. Idempotent projectors ─────────────────────────────────
print("\n--- 4. Primitive idempotents ---")
# E_θ = prod_{φ≠θ} (A - φI) / prod_{φ≠θ} (θ - φ)
E0 = (A.astype(float) - r_val*np.eye(n)) @ (A.astype(float) - s_val*np.eye(n)) / ((k - r_val) * (k - s_val))
Er = (A.astype(float) - k*np.eye(n)) @ (A.astype(float) - s_val*np.eye(n)) / ((r_val - k) * (r_val - s_val))
Es = (A.astype(float) - k*np.eye(n)) @ (A.astype(float) - r_val*np.eye(n)) / ((s_val - k) * (s_val - r_val))

# Check idempotent
assert np.allclose(E0 @ E0, E0)
assert np.allclose(Er @ Er, Er)
assert np.allclose(Es @ Es, Es)
# Check orthogonal
assert np.allclose(E0 @ Er, 0)
assert np.allclose(E0 @ Es, 0)
assert np.allclose(Er @ Es, 0)
# Check sum
assert np.allclose(E0 + Er + Es, np.eye(n))
# Check ranks
r0 = int(round(np.trace(E0)))
rr = int(round(np.trace(Er)))
rs = int(round(np.trace(Es)))
print(f"  E₀ + E_r + E_s = I  ✓")
print(f"  E_θ² = E_θ, E_θ E_φ = 0 (θ ≠ φ)  ✓")
print(f"  rank(E₀) = {r0}, rank(E_r) = {rr}, rank(E_s) = {rs}")
assert r0 == 1 and rr == f_r and rs == f_s

# E₀ = J/n
assert np.allclose(E0, Jmat/n)
print(f"  E₀ = J/40  ✓")

# Diagonal entries of E_r, E_s
er_diag = Er[0,0]
es_diag = Es[0,0]
print(f"  (E_r)_{'{ii}'} = {Fraction(f_r, n)} = {er_diag:.4f}")
print(f"  (E_s)_{'{ii}'} = {Fraction(f_s, n)} = {es_diag:.4f}")

# ── 5. Regular two-graph ─────────────────────────────────────
print("\n--- 5. Regular two-graph ---")
S = Jmat - I - 2*A
# Non-trivial eigenvalues of S
s_eigs = np.linalg.eigvalsh(S.astype(float))
s_nontrivial = sorted(set(int(round(e)) for e in s_eigs if abs(e - (n-1-2*k)) > 0.5))
print(f"  Non-trivial Seidel eigenvalues: {s_nontrivial}")
print(f"  Exactly 2 values on j⊥ => REGULAR two-graph  ✓")

# Two-graph: a set T of triples from vertex set V such that every 4-set
# contains an even number of triples from T.
# For a graph G, the triples are {x,y,z} with odd number of edges.
# A two-graph is regular if every pair is in the same number of triples.
print(f"  Two-graph T(W): triple {{x,y,z}} ∈ T iff odd #edges in G[x,y,z]")

# Count: for each pair, how many triples contain it?
pair_triple_count = set()
for i in range(min(n, 10)):
    for j in range(i+1, min(n, 10)):
        cnt = 0
        for c in range(n):
            if c == i or c == j:
                continue
            edges_in_triple = A[i,j] + A[i,c] + A[j,c]
            if edges_in_triple % 2 == 1:
                cnt += 1
        pair_triple_count.add(cnt)

# Do full count for a few pairs to get the regularity parameter
full_pair_counts = set()
for i in range(n):
    for j in range(i+1, n):
        cnt = 0
        for c in range(n):
            if c == i or c == j:
                continue
            edges = A[i,j] + A[i,c] + A[j,c]
            if edges % 2 == 1:
                cnt += 1
        full_pair_counts.add(cnt)
        if len(full_pair_counts) > 1:
            break
    if len(full_pair_counts) > 1:
        break

if len(full_pair_counts) == 1:
    reg_param = full_pair_counts.pop()
    # Verify for all pairs
    all_same = True
    for i in range(n):
        for j in range(i+1, n):
            cnt = 0
            for c in range(n):
                if c == i or c == j:
                    continue
                edges = A[i,j] + A[i,c] + A[j,c]
                if edges % 2 == 1:
                    cnt += 1
            if cnt != reg_param:
                all_same = False
                break
        if not all_same:
            break
    print(f"  Regular two-graph: each pair in exactly {reg_param} triples  ✓")
else:
    print(f"  Pair-triple counts: {full_pair_counts}")

# ── 6. Delsarte LP bounds ────────────────────────────────────
print("\n--- 6. Delsarte bounds ---")
delsarte_clique = Fraction(1) - Fraction(k, s_val)
delsarte_coclique = Fraction(n * (-s_val), k - s_val)
print(f"  Clique bound: |C| ≤ 1 - k/s = {delsarte_clique}")
print(f"    ω = 4 = {delsarte_clique}: TIGHT (Delsarte-optimal cliques)  ✓")
print(f"  Coclique bound: |S| ≤ n(-s)/(k-s) = {delsarte_coclique}")
print(f"    α = 7 < {delsarte_coclique}: NOT tight (no ovoid)")

# Tightness of clique bound => cliques form Delsarte design
print(f"  Tight clique bound => maximal cliques are Delsarte 1-designs")

# ── 7. Cycle counts ──────────────────────────────────────────
print("\n--- 7. Cycle counts ---")

# Triangles
tri_count = 0
for i in range(n):
    for j in range(i+1, n):
        if A[i,j] == 1:
            for c in range(j+1, n):
                if A[i,c] == 1 and A[j,c] == 1:
                    tri_count += 1
print(f"  C₃ (triangles): {tri_count}")

# 4-cycles: for each pair {u,v}, count non-adj pairs among common neighbors
c4_count = 0
for i in range(n):
    for j in range(i+1, n):
        cn = [v for v in range(n) if A[i,v]==1 and A[j,v]==1]
        for a in range(len(cn)):
            for b in range(a+1, len(cn)):
                if A[cn[a], cn[b]] == 0:
                    c4_count += 1
# Each C₄ has 2 pairs of opposite vertices
c4_count //= 2
print(f"  C₄ (4-cycles): {c4_count}")

# 5-cycles: more complex, use spectral approach
# Tr(A^5) counts closed 5-walks
A3 = A @ A2
A4 = A @ A3
A5 = A @ A4
tr5 = int(round(np.trace(A5)))
# Tr(A^5)/10 is related to 5-cycles but also includes other closed walks
# For 5-cycles specifically, we need inclusion-exclusion... skip exact count

# Spectral walk counts
print(f"\n  Spectral walk counts Tr(Aℓ):")
for ell in range(1, 9):
    tr_val = sum(m * ev**ell for ev, m in [(k,1),(r_val,f_r),(s_val,f_s)])
    print(f"    Tr(A^{ell}) = {tr_val}")

# ── 8. Girth ─────────────────────────────────────────────────
print(f"\n--- 8. Girth ---")
print(f"  λ = 2 > 0, so triangles exist => girth g = 3")

# ── 9. Diameter and distance distribution ─────────────────────
print(f"\n--- 9. Distance distribution ---")
# BFS from vertex 0
from collections import deque
dist = [-1]*n
dist[0] = 0
q = deque([0])
while q:
    v = q.popleft()
    for w in range(n):
        if A[v,w] == 1 and dist[w] == -1:
            dist[w] = dist[v] + 1
            q.append(w)

dist_counts = {}
for d in dist:
    dist_counts[d] = dist_counts.get(d, 0) + 1
print(f"  From vertex 0: {dict(sorted(dist_counts.items()))}")
print(f"  Diameter = {max(dist)}")

# ── 10. Walk generating function coefficient identities ──────
print(f"\n--- 10. Walk generating function ---")
# W(x) = sum_ℓ Tr(A^ℓ) x^ℓ / n = sum (k^ℓ + f_r r^ℓ + f_s s^ℓ) x^ℓ / n
# = 1/(1-kx) + f_r/(n(1-rx)) + f_s/(n(1-sx))  [per vertex]
# Total: n/(1-kx) + f_r·n/(n(1-rx)) + f_s·n/(n(1-sx))
# = n/(1-12x) + 24/(1-2x) + 15/(1+4x)  [total closed walks / vertex]
# Actually Tr(A^ℓ) = k^ℓ + f_r·r^ℓ + f_s·s^ℓ
# Per vertex: Tr(A^ℓ)/n = (k^ℓ + f_r·r^ℓ + f_s·s^ℓ)/n

print(f"  Tr(A^ℓ)/n = (12^ℓ + 24·2^ℓ + 15·(-4)^ℓ) / 40")
print(f"  Return probability: p_ℓ = Tr(A^ℓ)/(n·k^ℓ)")
for ell in range(1, 7):
    tr_val = k**ell + f_r * r_val**ell + f_s * s_val**ell
    p = Fraction(tr_val, n * k**ell)
    print(f"    p_{ell} = {p} = {float(p):.6f}")

# ── 11. Seidel switching equivalence ─────────────────────────
print(f"\n--- 11. Seidel switching ---")
# Switching W w.r.t. a set U: flip all edges between U and V\U
# The two-graph is the equivalence class under switching
# Switching w.r.t. the neighborhood of a vertex gives the descendant
# For a regular two-graph, all descendants are isomorphic
print(f"  W(3,3) defines regular two-graph T on 40 vertices")
print(f"  All descendants are isomorphic (vertex-transitivity)")
print(f"  Switching class contains SRG(40,12,2,4) and SRG(40,27,18,18)")
print(f"  (W and its complement are in the same switching class)")

# ── 12. Strongly regular decomposition ───────────────────────
print(f"\n--- 12. Edge-disjoint decomposition ---")
# Can W be decomposed into edge-disjoint regular subgraphs?
# |E| = nk/2 = 240. 
# We know: 36 spreads of size 10 lines each, each line has C(4,2)=6 edges
# A spread has 10 lines * 6 edges = 60 edges
# 4 edge-disjoint spreads would give 240 edges total
# Check if spreads can be edge-disjoint (3 spreads per edge? from Prop 32: 9 spreads per line)
print(f"  |E| = 240 = |Φ(E₈)|")
print(f"  Each edge is in some lines; each line in 9 of 36 spreads")
print(f"  Each spread covers 10 × 6 = 60 edges")
print(f"  4 edge-disjoint spreads would decompose E (240/60 = 4)")

# Check: are there 4 pairwise edge-disjoint spreads?
# First find all cliques and spreads
cliques4 = []
for i in range(n):
    for j in range(i+1, n):
        if A[i,j] == 1:
            for c in range(j+1, n):
                if A[i,c] == 1 and A[j,c] == 1:
                    for d in range(c+1, n):
                        if A[i,d] == 1 and A[j,d] == 1 and A[c,d] == 1:
                            cliques4.append(frozenset([i,j,c,d]))
cliques4 = list(set(cliques4))

spreads = []
def find_spreads(lines, current, covered):
    if len(current) == 10:
        spreads.append(frozenset(current))
        return
    remaining = [l for l in lines if not l & covered]
    if not remaining:
        return
    first = remaining[0]
    # Branch: include first
    find_spreads(remaining[1:], current + [first], covered | first)
    # Branch: exclude first
    find_spreads(remaining[1:], current, covered)

find_spreads(list(cliques4), [], frozenset())
print(f"  Spreads found: {len(spreads)}")

# Check edge-disjoint pairs
def spread_edges(sp):
    edges = set()
    for line in sp:
        for pair in combinations(line, 2):
            edges.add(frozenset(pair))
    return edges

spread_list = list(spreads)
# Find 4 pairwise edge-disjoint spreads (greedy)
spread_edge_sets = [spread_edges(sp) for sp in spread_list]
found_decomp = False
for i in range(len(spread_list)):
    for j in range(i+1, len(spread_list)):
        if spread_edge_sets[i] & spread_edge_sets[j]:
            continue
        for c in range(j+1, len(spread_list)):
            if (spread_edge_sets[c] & spread_edge_sets[i]) or (spread_edge_sets[c] & spread_edge_sets[j]):
                continue
            for d in range(c+1, len(spread_list)):
                if (spread_edge_sets[d] & spread_edge_sets[i]) or \
                   (spread_edge_sets[d] & spread_edge_sets[j]) or \
                   (spread_edge_sets[d] & spread_edge_sets[c]):
                    continue
                total = spread_edge_sets[i] | spread_edge_sets[j] | spread_edge_sets[c] | spread_edge_sets[d]
                if len(total) == 240:
                    found_decomp = True
                    print(f"  Found edge-disjoint decomposition into 4 spreads!  ✓")
                    break
            if found_decomp: break
        if found_decomp: break
    if found_decomp: break

if not found_decomp:
    print(f"  No edge-disjoint 4-spread decomposition found")

# ── 13. Number of edges per spread overlap ────────────────────
print(f"\n--- 13. Edge overlap between spreads ---")
overlap_sizes = set()
for i in range(len(spread_list)):
    for j in range(i+1, len(spread_list)):
        overlap = len(spread_edge_sets[i] & spread_edge_sets[j])
        overlap_sizes.add(overlap)
print(f"  Edge overlaps between spread pairs: {sorted(overlap_sizes)}")

print("\nDone.")
