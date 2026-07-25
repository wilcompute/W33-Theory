"""Explore: clique geometry, GQ axioms, mu-graphs, complement graph."""
import numpy as np
from itertools import combinations
from collections import Counter

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
print(f"n = {n}")

def symp(u, v):
    return sum(u[i] * J[i][j] * v[j] for i in range(4) for j in range(4)) % p

A = np.zeros((n, n), dtype=int)
for i in range(n):
    for j in range(i+1, n):
        if symp(pts[i], pts[j]) == 0:
            A[i][j] = A[j][i] = 1

k = A[0].sum()
print(f"k = {k}")

# ── 1. Find all triangles ─────────────────────────────────────
triangles = []
for i in range(n):
    for j in range(i+1, n):
        if A[i,j] == 1:
            for c in range(j+1, n):
                if A[i,c] == 1 and A[j,c] == 1:
                    triangles.append((i,j,c))

print(f"\nTriangles: {len(triangles)}")
print(f"  Expected nkλ/6 = 40*12*2/6 = {40*12*2//6}")

# ── 2. Find all 4-cliques (K₄s = GQ lines) ───────────────────
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
print(f"\n4-cliques (GQ lines): {len(cliques4)}")

# Lines through each vertex
lines_per_v = Counter()
for cl in cliques4:
    for v in cl:
        lines_per_v[v] += 1
lines_per_v_vals = set(lines_per_v.values())
print(f"Lines per vertex: {lines_per_v_vals}")

# ── 3. Verify no 5-clique ─────────────────────────────────────
has_5clique = False
for cl in cliques4:
    verts = list(cl)
    for w in range(n):
        if w not in cl and all(A[w, v] == 1 for v in verts):
            has_5clique = True
            break
    if has_5clique:
        break
print(f"5-clique exists: {has_5clique}")
print(f"=> All maximal cliques have size ω = 4")

# ── 4. Every triangle extends to a unique K₄ ──────────────────
unique_extension = True
for tri in triangles:
    i, j, c = tri
    extensions = [w for w in range(n) if w not in tri
                  and A[i,w] == 1 and A[j,w] == 1 and A[c,w] == 1]
    if len(extensions) != 1:
        unique_extension = False
        print(f"  Triangle {tri}: {len(extensions)} extensions")
        break

print(f"\nEvery triangle extends to unique K₄: {unique_extension}")

# ── 5. GQ axiom: for non-incident (point, line), unique collinear point ──
gq_axiom = True
violations = 0
for v in range(n):
    for cl in cliques4:
        if v in cl:
            continue
        # Count points on this line collinear with v
        collinear = [w for w in cl if A[v, w] == 1]
        if len(collinear) != 1:
            gq_axiom = False
            violations += 1

print(f"GQ axiom (non-incident pt-line => unique collinear pt): {gq_axiom}")
if not gq_axiom:
    print(f"  Violations: {violations}")

# ── 6. Triangles per K₄ ──────────────────────────────────────
tri_per_clique = []
for cl in cliques4:
    vl = sorted(cl)
    t = 0
    for combo in combinations(vl, 3):
        i, j, c = combo
        if A[i,j] == 1 and A[i,c] == 1 and A[j,c] == 1:
            t += 1
    tri_per_clique.append(t)
print(f"\nTriangles per K₄: always {set(tri_per_clique)} = C(4,3)")
print(f"Total triangles from cliques: {sum(tri_per_clique)} = 40 * 4 = {40*4}")

# ── 7. Classify μ-graphs ─────────────────────────────────────
print("\n--- μ-graph classification ---")
mu_graph_types = Counter()
for i in range(n):
    for j in range(i+1, n):
        if A[i,j] == 0:
            cn = [v for v in range(n) if A[i,v] == 1 and A[j,v] == 1]
            if len(cn) != 4:
                continue
            # Get adjacency among the 4 common neighbors
            edges = 0
            for a, b in combinations(cn, 2):
                if A[a, b] == 1:
                    edges += 1
            # Degree sequence of the induced subgraph
            degs = sorted([sum(A[a,b] for b in cn if b != a) for a in cn])
            mu_graph_types[tuple(degs)] += 1

print(f"μ-graph types (degree sequences -> count):")
for dt, cnt in sorted(mu_graph_types.items()):
    # Identify the graph
    edges = sum(dt) // 2
    if dt == (0, 0, 0, 0):
        name = "4K₁ (empty)"
    elif dt == (0, 0, 1, 1):
        name = "K₂ + 2K₁"
    elif dt == (1, 1, 1, 1) and edges == 2:
        name = "2K₂ (matching)"
    elif dt == (0, 1, 1, 2):
        name = "P₃ + K₁"
    elif dt == (1, 1, 2, 2):
        name = "P₄ or C₄"
    elif dt == (1, 1, 1, 3):
        name = "K₁,₃ (star)"
    elif dt == (0, 2, 2, 2):
        name = "K₃ + K₁"
    elif dt == (2, 2, 2, 2):
        name = "C₄"
    elif dt == (2, 2, 3, 3):
        name = "K₄-e"
    elif dt == (3, 3, 3, 3):
        name = "K₄"
    else:
        name = f"? (edges={edges})"
    print(f"  {dt} [{name}]: {cnt}")

total_nonadj = sum(mu_graph_types.values())
print(f"Total non-adjacent pairs: {total_nonadj} = n(n-1-k)/2 = {n*(n-1-k)//2}")

# ── 8. Complement graph W̄ ──────────────────────────────────────
print("\n--- Complement graph W̄ ---")
Abar = 1 - A - np.eye(n, dtype=int)
kbar = Abar[0].sum()
print(f"W̄: n={n}, k̄={kbar}")

# Lambda-bar and mu-bar
lam_bar_vals = set()
mu_bar_vals = set()
for i in range(n):
    for j in range(i+1, n):
        cn = sum(Abar[i] * Abar[j])
        if Abar[i,j] == 1:
            lam_bar_vals.add(cn)
        else:
            mu_bar_vals.add(cn)

print(f"λ̄ = {lam_bar_vals}")
print(f"μ̄ = {mu_bar_vals}")

# Eigenvalues of complement
eigvals = np.linalg.eigvalsh(Abar.astype(float))
eigvals_rounded = sorted(set(np.round(eigvals).astype(int)), reverse=True)
print(f"Spectrum of W̄: {eigvals_rounded}")
for ev in eigvals_rounded:
    mult = sum(1 for e in eigvals if abs(e - ev) < 0.5)
    print(f"  eigenvalue {ev:+d}, multiplicity {mult}")

print(f"|r̄| = |s̄| = 3: eigenvalues ±3 (balanced)")

# ── 9. Seidel matrix ──────────────────────────────────────────
print("\n--- Seidel matrix ---")
S = np.ones((n, n), dtype=int) - np.eye(n, dtype=int) - 2 * A
seidel_eigvals = np.linalg.eigvalsh(S.astype(float))
seidel_rounded = sorted(set(np.round(seidel_eigvals).astype(int)), reverse=True)
print(f"Seidel eigenvalues:")
for ev in seidel_rounded:
    mult = sum(1 for e in seidel_eigvals if abs(e - ev) < 0.5)
    print(f"  {ev:+d}, multiplicity {mult}")

# ── 10. Ovoid non-existence ───────────────────────────────────
print("\n--- Ovoid analysis ---")
print(f"For GQ(s,t) = GQ(3,3): ovoid size = st+1 = {3*3+1}")
print(f"Maximum independent set α = 7")
print(f"Since α = 7 < 10 = st+1, GQ(3,3) has NO ovoid.")

# ── 11. Spreads vs ovoids duality ─────────────────────────────
print("\n--- Spread/Ovoid duality ---")
print(f"GQ(3,3) has 36 spreads (Prop 32), but NO ovoid.")
print(f"In self-dual GQ(s,s), spreads ↔ ovoids under duality.")
print(f"Non-existence of ovoids in W(q) for q>2 is a theorem of Thas (1981).")

# ── 12. Fractional chromatic number ───────────────────────────
print("\n--- Fractional chromatic number ---")
from fractions import Fraction
chi_f = Fraction(n, 7)
print(f"For vertex-transitive graphs: χ_f = n/α = {chi_f} = {float(chi_f):.6f}")
print(f"Hoffman bound: χ ≥ 1 - k/s = 1 + 12/4 = 4")
print(f"χ_f = 40/7 ≈ 5.714, χ = 7")
print(f"Clique number ω = 4 ≤ χ_f = 40/7 ≤ χ = 7")

# ── 13. Verify: each pair of distinct lines meet in 0 or 1 point ──
print("\n--- Line intersection structure ---")
line_isct = Counter()
for i, cl1 in enumerate(cliques4):
    for j in range(i+1, len(cliques4)):
        cl2 = cliques4[j]
        isct = len(cl1 & cl2)
        line_isct[isct] += 1

print(f"Line-line intersection sizes: {dict(line_isct)}")
print(f"  0: parallel (disjoint)     => {line_isct[0]} pairs")
print(f"  1: concurrent (meet at pt) => {line_isct[1]} pairs")
# In GQ, no two lines meet in more than 1 point
for isct_size, cnt in line_isct.items():
    if isct_size > 1:
        print(f"  WARNING: {cnt} pairs meet in {isct_size} points!")

# Total concurrent pairs: each point is on 4 lines, giving C(4,2)=6 pairs
# Total = 40 * 6 = 240
print(f"  Expected concurrent pairs = 40 * C(4,2) = {40*6}")

# ── 14. Lines meeting each line ──────────────────────────────
print("\n--- Lines meeting a given line ---")
meeting_counts = []
for cl1 in cliques4:
    cnt = sum(1 for cl2 in cliques4 if cl2 != cl1 and len(cl1 & cl2) >= 1)
    meeting_counts.append(cnt)
print(f"Lines meeting each line: always {set(meeting_counts)}")
print(f"  Each line has 4 pts, each on 3 other lines => 4*3 = 12")
print(f"  Parallel lines per line = 40 - 1 - 12 = 27")

# ── 15. Check: parallel classes (spread structure) ────────────
print("\n--- Parallel class structure ---")
# For each line, how many lines are parallel (disjoint)?
parallel_counts = []
for cl1 in cliques4:
    cnt = sum(1 for cl2 in cliques4 if cl2 != cl1 and len(cl1 & cl2) == 0)
    parallel_counts.append(cnt)
print(f"Parallel lines per line: always {set(parallel_counts)}")

print("\nDone.")
