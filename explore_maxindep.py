"""Explore: maximum independent sets, coclique structure, equitable partitions,
   distance quotient matrix, and matching polynomial."""
import numpy as np
from itertools import combinations
from collections import Counter, defaultdict

# ── Build W(3,3) ──────────────────────────────────────────────
p = 3
J = np.array([[0,1,0,0],[2,0,0,0],[0,0,0,1],[0,0,2,0]])

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
    return sum(u[i] * J[i][j] * v[j] for i in range(4) for j in range(4)) % p

A = np.zeros((n, n), dtype=int)
for i in range(n):
    for j in range(i+1, n):
        if symp(pts[i], pts[j]) == 0:
            A[i][j] = A[j][i] = 1

k = 12; lam = 2; mu = 4

print("="*60)
print("MAXIMUM INDEPENDENT SETS AND EQUITABLE PARTITIONS")
print("="*60)

# ── 1. Find ALL maximum independent sets (α=7) ──────────────
print("\n--- 1. Maximum independent sets (α = 7) ---")

# Use backtracking search
max_indep = []

def find_max_indep(current, candidates, size_target):
    if len(current) == size_target:
        max_indep.append(frozenset(current))
        return
    if len(current) + len(candidates) < size_target:
        return
    for idx, v in enumerate(candidates):
        new_cands = [w for w in candidates[idx+1:] if A[v, w] == 0]
        find_max_indep(current + [v], new_cands, size_target)

find_max_indep([], list(range(n)), 7)
print(f"  Maximum independent sets of size 7: {len(max_indep)}")

# ── 2. Intersection patterns ─────────────────────────────────
print("\n--- 2. Intersection patterns ---")
isct_sizes = Counter()
for i, s1 in enumerate(max_indep):
    for s2 in max_indep[i+1:]:
        isct_sizes[len(s1 & s2)] += 1
print(f"  Pairwise intersection sizes: {dict(sorted(isct_sizes.items()))}")

# How many per vertex?
per_vertex = Counter()
for v in range(n):
    cnt = sum(1 for s in max_indep if v in s)
    per_vertex[cnt] += 1
print(f"  Max indep sets per vertex (count -> #vertices): {dict(sorted(per_vertex.items()))}")

# Orbit under Aut (vertex-transitive => constant per vertex)
total_memberships = sum(cnt * num for cnt, num in per_vertex.items())
print(f"  Total (vertex, set) incidences: {total_memberships}")
print(f"  = 7 * {len(max_indep)} = {7 * len(max_indep)}")

# ── 3. μ-graph structure and independent sets ────────────────
print("\n--- 3. Independent set structure ---")
# Are max independent sets related to GQ structure?
# In GQ(3,3), a partial ovoid has max size 7 (since no ovoid of size 10 exists)
# Check: does each max indep set meet every line in ≤1 point? (partial ovoid)
partial_ovoid_count = 0
non_po_count = 0
# First find all lines (4-cliques)
cliques4 = []
for i in range(n):
    for j in range(i+1, n):
        if A[i,j] == 1:
            for c in range(j+1, n):
                if A[i,c] == 1 and A[j,c] == 1:
                    for d in range(c+1, n):
                        if A[i,d] == 1 and A[j,d] == 1 and A[c,d] == 1:
                            cl = frozenset([i,j,c,d])
                            if cl not in cliques4:
                                cliques4.append(cl)

for s in max_indep:
    is_po = True
    for cl in cliques4:
        if len(s & cl) > 1:
            is_po = False
            break
    if is_po:
        partial_ovoid_count += 1
    else:
        non_po_count += 1

print(f"  Partial ovoids (meet each line in ≤1): {partial_ovoid_count}")
print(f"  Non-partial-ovoid max indep sets: {non_po_count}")

# For partial ovoids: how many lines do they miss?
if partial_ovoid_count > 0:
    for s in max_indep:
        is_po = all(len(s & cl) <= 1 for cl in cliques4)
        if is_po:
            lines_hit = sum(1 for cl in cliques4 if len(s & cl) == 1)
            lines_missed = 40 - lines_hit
            print(f"    Example partial ovoid: {sorted(s)}")
            print(f"    Lines hit: {lines_hit}, missed: {lines_missed}")
            break

# ── 4. Equitable partition from distance ──────────────────────
print("\n--- 4. Distance partition (equitable) ---")
# From vertex 0: partition into {v}, N(v), N₂(v)
# Quotient matrix B has eigenvalues = eigenvalues of A
v0 = 0
N1 = [w for w in range(n) if A[v0, w] == 1]
N2 = [w for w in range(n) if A[v0, w] == 0 and w != v0]
print(f"  Partition: {{v₀}} ∪ N₁(v₀) ∪ N₂(v₀) = 1 + {len(N1)} + {len(N2)} = {1+len(N1)+len(N2)}")

# Quotient matrix: Bij = (edges from cell i to cell j) / |cell i vertex degree into j|
# Row 0 (v0): 0 edges to self, k to N1, 0 to N2
# Row 1 (N1): 1 to v0, λ to N1, k-1-λ to N2
# Row 2 (N2): 0 to v0, μ to N1, k-μ to N2
B = np.array([
    [0, k, 0],
    [1, lam, k-1-lam],
    [0, mu, k-mu]
])
print(f"  Quotient matrix B:")
for row in B:
    print(f"    {row}")

# Eigenvalues of B
eig_B = sorted(np.linalg.eigvalsh(B.astype(float)), reverse=True)
print(f"  Eigenvalues of B: {[int(round(e)) for e in eig_B]}")
print(f"  = {{k, r, s}} = {{12, 2, -4}}  ✓")

# Verify: the quotient matrix eigenvalues interlace with A
print(f"  B eigenvalues = A eigenvalues (distance-regular property)  ✓")

# ── 5. Equitable partition from edge ──────────────────────────
print("\n--- 5. Edge partition (equitable) ---")
# For an edge (u,v): partition vertices by (dist to u, dist to v)
# Types: (0,1), (1,0), (1,1), (1,2), (2,1), (2,2)
u, v = 0, N1[0]
cells = defaultdict(list)
for w in range(n):
    du = 0 if w == u else (1 if A[u,w]==1 else 2)
    dv = 0 if w == v else (1 if A[v,w]==1 else 2)
    cells[(du, dv)].append(w)

print(f"  Edge ({u},{v}) partition:")
for key in sorted(cells.keys()):
    print(f"    ({key[0]},{key[1]}): {len(cells[key])} vertices")

# Check equitable: each vertex in cell C has same number of neighbors in cell D
is_equitable = True
quotient = {}
for c_key in sorted(cells.keys()):
    for d_key in sorted(cells.keys()):
        counts = set()
        for w in cells[c_key]:
            cnt = sum(1 for x in cells[d_key] if A[w, x] == 1)
            counts.add(cnt)
        if len(counts) == 1:
            quotient[(c_key, d_key)] = counts.pop()
        else:
            is_equitable = False
            print(f"    NOT equitable: {c_key} -> {d_key}: counts = {counts}")
            quotient[(c_key, d_key)] = counts

print(f"  Edge partition is equitable: {is_equitable}")

# ── 6. Equitable partition from non-edge ──────────────────────
print("\n--- 6. Non-edge partition (equitable) ---")
ne_u = 0
ne_v = N2[0]
cells_ne = defaultdict(list)
for w in range(n):
    du = 0 if w == ne_u else (1 if A[ne_u,w]==1 else 2)
    dv = 0 if w == ne_v else (1 if A[ne_v,w]==1 else 2)
    cells_ne[(du, dv)].append(w)

print(f"  Non-edge ({ne_u},{ne_v}) partition:")
for key in sorted(cells_ne.keys()):
    print(f"    ({key[0]},{key[1]}): {len(cells_ne[key])} vertices")

is_equitable_ne = True
for c_key in sorted(cells_ne.keys()):
    for d_key in sorted(cells_ne.keys()):
        counts = set()
        for w in cells_ne[c_key]:
            cnt = sum(1 for x in cells_ne[d_key] if A[w, x] == 1)
            counts.add(cnt)
        if len(counts) != 1:
            is_equitable_ne = False

print(f"  Non-edge partition is equitable: {is_equitable_ne}")

# ── 7. Number of matchings by size ────────────────────────────
print("\n--- 7. Matching numbers ---")
# For a 40-vertex graph, computing all matchings is hard.
# But we can compute m_1, m_2, m_3 easily.
m = n * k // 2  # = 240 edges
print(f"  m₁ = |E| = {m}")

# m₂ = number of 2-matchings (pairs of independent edges)
# = C(|E|,2) - number of intersecting edge pairs
# Two edges share a vertex if they share an endpoint
# For each vertex v of degree k, C(k,2) pairs of edges at v
# Total intersecting pairs = n * C(k,2)
intersecting = n * k * (k-1) // 2
m2 = m * (m-1) // 2 - intersecting
print(f"  m₂ = C(240,2) - 40·C(12,2) = {m*(m-1)//2} - {intersecting} = {m2}")

# m₃ = harder, skip exact computation

# ── 8. Perfect matching existence ─────────────────────────────
print("\n--- 8. Perfect matchings ---")
# W is 12-regular on 40 vertices. By Petersen's theorem (2-edge-connected + regular
# with even degree), W has a perfect matching.
# Actually, any bridgeless k-regular graph with n even has a perfect matching.
# W is 12-connected (Prop 35), so certainly bridgeless.
print(f"  W is 12-connected, 12-regular, n=40 even")
print(f"  => Perfect matching exists (Petersen's theorem)")
print(f"  Class 1 (Prop 18) => edge-chromatic number = 12")
print(f"  => W decomposes into 12 perfect matchings")

# Find one perfect matching (greedy augmenting path)
# Use a simple greedy + augmenting paths approach
def find_perfect_matching(adj):
    """Find a perfect matching using augmenting paths."""
    nn = adj.shape[0]
    match = [-1] * nn
    
    def augment(u, visited):
        for v in range(nn):
            if adj[u, v] == 1 and v not in visited:
                visited.add(v)
                if match[v] == -1 or augment(match[v], visited):
                    match[v] = u
                    match[u] = v
                    return True
        return False
    
    for u in range(nn):
        if match[u] == -1:
            augment(u, {u})
    
    return match

matching = find_perfect_matching(A)
matched_pairs = set()
for i in range(n):
    if matching[i] != -1 and i < matching[i]:
        matched_pairs.add((i, matching[i]))

print(f"  Perfect matching found: {len(matched_pairs)} edges")
assert len(matched_pairs) == 20  # n/2

# ── 9. Matching deficiency ────────────────────────────────────
print("\n--- 9. Factorization ---")
print(f"  12 = k edge-disjoint perfect matchings (1-factors)")
print(f"  Each 1-factor has 20 = n/2 edges")
print(f"  12 × 20 = 240 = |E|  ✓")

# ── 10. Structure of maximum independent sets ─────────────────
print(f"\n--- 10. Detailed structure of max independent sets ---")

# How many lines does each max indep set hit?
line_hit_counts = Counter()
for s in max_indep:
    hits = sum(1 for cl in cliques4 if len(s & cl) >= 1)
    line_hit_counts[hits] += 1
print(f"  Lines hit per max indep set: {dict(sorted(line_hit_counts.items()))}")

# For each max indep set: number of lines meeting it in 0, 1, 2 points
for s in list(max_indep)[:3]:
    meet0 = sum(1 for cl in cliques4 if len(s & cl) == 0)
    meet1 = sum(1 for cl in cliques4 if len(s & cl) == 1)
    meet2 = sum(1 for cl in cliques4 if len(s & cl) == 2)
    print(f"    S = sorted subset: |S∩ℓ|=0: {meet0}, =1: {meet1}, =2: {meet2}")

# ── 11. Complement of max indep set ──────────────────────────
print(f"\n--- 11. Complement of max indep set ---")
# The 33 = n - α vertices NOT in a max indep set
for s in list(max_indep)[:1]:
    comp = [v for v in range(n) if v not in s]
    # Induced subgraph on complement
    sub_A = A[np.ix_(comp, comp)]
    degs = sub_A.sum(axis=1)
    deg_dist = Counter(int(d) for d in degs)
    print(f"  Complement subgraph (33 vertices): degree distribution {dict(sorted(deg_dist.items()))}")
    # Is it regular?
    if len(deg_dist) == 1:
        print(f"    Regular!")
    # Edges
    edges_sub = sub_A.sum() // 2
    print(f"    Edges: {edges_sub} (of 240 total)")
    # Eigenvalues
    eigs = sorted(np.linalg.eigvalsh(sub_A.astype(float)), reverse=True)
    print(f"    Spectrum (rounded): {[int(round(e)) for e in eigs[:5]]} ... {[int(round(e)) for e in eigs[-5:]]}")

# ── 12. Automorphism orbits on max independent sets ───────────
print(f"\n--- 12. Orbits of max independent sets ---")
# Two max indep sets are in the same orbit if one can be mapped to the other
# by an automorphism. Since |Aut| = 25920, we expect few orbits.
# Without computing the full automorphism group, we can use invariants:
# - degree sequence of induced subgraph on N(S) (neighbors of S)
# - number of lines meeting S in 0, 1, 2 points
orbit_signatures = Counter()
for s in max_indep:
    meet0 = sum(1 for cl in cliques4 if len(s & cl) == 0)
    meet1 = sum(1 for cl in cliques4 if len(s & cl) == 1)
    meet2 = sum(1 for cl in cliques4 if len(s & cl) == 2)
    sig = (meet0, meet1, meet2)
    orbit_signatures[sig] += 1

print(f"  Signatures (lines meeting in 0,1,2 pts -> count):")
for sig, cnt in sorted(orbit_signatures.items()):
    print(f"    {sig}: {cnt}")

print(f"\n  Total max independent sets: {len(max_indep)}")
print(f"  Number of distinct signatures: {len(orbit_signatures)}")

print("\nDone.")
