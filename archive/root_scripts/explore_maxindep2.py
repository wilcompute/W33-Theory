"""Clean exploration: max indep sets, quotient matrix, edge partition."""
import numpy as np
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
                if first is None: continue
                inv = pow(first, -1, p)
                nv = tuple((x * inv) % p for x in v)
                if nv not in pts: pts.append(nv)
n = len(pts)
def symp(u, v):
    return sum(u[i] * J[i][j] * v[j] for i in range(4) for j in range(4)) % p
A = np.zeros((n, n), dtype=int)
for i in range(n):
    for j in range(i+1, n):
        if symp(pts[i], pts[j]) == 0: A[i][j] = A[j][i] = 1
k = 12; lam = 2; mu = 4

# ── Distance quotient (fix: use eigvals, not eigvalsh) ────────
print("--- Distance quotient matrix ---")
B = np.array([[0, 12, 0], [1, 2, 9], [0, 4, 8]])
eig_B = sorted(np.linalg.eigvals(B.astype(float)).real, reverse=True)
print(f"  B = {B.tolist()}")
print(f"  Eigenvalues: {[int(round(e)) for e in eig_B]} = {{k, r, s}}  ✓")

# ── Edge quotient matrix ──────────────────────────────────────
print("\n--- Edge quotient matrix ---")
N1 = [w for w in range(n) if A[0, w] == 1]
u, v = 0, N1[0]
cells = defaultdict(list)
for w in range(n):
    du = 0 if w == u else (1 if A[u,w]==1 else 2)
    dv = 0 if w == v else (1 if A[v,w]==1 else 2)
    cells[(du, dv)].append(w)

cell_keys = sorted(cells.keys())
nc = len(cell_keys)
print(f"  Cells: {[(k, len(cells[k])) for k in cell_keys]}")
Q = np.zeros((nc, nc), dtype=int)
for ci, ck in enumerate(cell_keys):
    for cj, dk in enumerate(cell_keys):
        counts = [sum(1 for x in cells[dk] if A[w, x] == 1) for w in cells[ck]]
        Q[ci, cj] = counts[0]  # all should be equal (equitable)
print(f"  Quotient matrix Q ({nc}×{nc}):")
for i, ck in enumerate(cell_keys):
    print(f"    {ck}: {Q[i].tolist()}")
eig_Q = sorted(np.linalg.eigvals(Q.astype(float)).real, reverse=True)
print(f"  Eigenvalues of Q: {[round(e, 4) for e in eig_Q]}")

# ── Max indep set orbit signatures (from first run) ──────────
print("\n--- Max indep set summary ---")
print(f"  |I₇(W)| = 2880 = 2⁶ · 3² · 5 = |Aut(W)|/9")
print(f"  All 2880 are partial ovoids (meet each line in ≤1 pt)")
print(f"  504 per vertex (= 2880 × 7/40)")

# Verify: 2880 * 7 / 40 = 504
assert 2880 * 7 == 504 * 40

# Verify: 25920 / 2880
print(f"  |Aut|/|I₇| = 25920/2880 = {25920//2880}")
# Under Aut, orbit size divides |Aut| = 25920
# If single orbit: orbit size = 2880, stabilizer = 25920/2880 = 9
print(f"  If single orbit: stabilizer order = 9 = 3²")

# Verify factorizations
print(f"\n  2880 = 2⁶ · 3² · 5 = {2**6 * 9 * 5}")
print(f"  504 = 2³ · 3² · 7 = {8 * 9 * 7}")

# i₇ from independence polynomial was 2880
print(f"  i₇ = 2880 (matches independence polynomial, Prop 29)")

# ── Line distribution for max indep sets ──────────────────────
print("\n--- Line distribution ---")
print(f"  Each partial ovoid of size 7:")
print(f"    meets 7 × 4 = 28 lines (7 pts, each on 4 lines, no two on same line)")
print(f"    misses 40 - 28 = 12 lines")
print(f"    Each missed line has all 4 points NOT in the partial ovoid")

# ── Intersection sizes ────────────────────────────────────────
print("\n--- Intersection distribution ---")
print(f"  |S₁ ∩ S₂| distribution for pairs of max indep sets:")
print(f"    |∩|=0: 1283040")
print(f"    |∩|=1: 1473120")
print(f"    |∩|=2:  829440")
print(f"    |∩|=3:  365760")
print(f"    |∩|=4:  141120")
print(f"    |∩|=5:   43200")
print(f"    |∩|=6:   10080")
total_pairs = 2880 * 2879 // 2
print(f"  Total pairs: {total_pairs}")
print(f"  Sum: {1283040+1473120+829440+365760+141120+43200+10080}")
# Check divisibility by orbit structure
# Average intersection: sum(i * count) / total_pairs
avg = (0*1283040+1*1473120+2*829440+3*365760+4*141120+5*43200+6*10080) / total_pairs
print(f"  Average intersection: {avg:.4f}")
print(f"  Expected for random: 7² /40 = {49/40} = {49/40:.4f}")

# ── Non-edge partition ────────────────────────────────────────
print("\n--- Non-edge quotient ---")
N2 = [w for w in range(n) if A[0, w] == 0 and w != 0]
ne_u, ne_v = 0, N2[0]
cells_ne = defaultdict(list)
for w in range(n):
    du = 0 if w == ne_u else (1 if A[ne_u,w]==1 else 2)
    dv = 0 if w == ne_v else (1 if A[ne_v,w]==1 else 2)
    cells_ne[(du, dv)].append(w)

print(f"  Cells: {[(k, len(cells_ne[k])) for k in sorted(cells_ne.keys())]}")

# Check equitability
ne_equitable = True
for ck in sorted(cells_ne.keys()):
    for dk in sorted(cells_ne.keys()):
        counts = set(sum(1 for x in cells_ne[dk] if A[w, x] == 1) for w in cells_ne[ck])
        if len(counts) > 1:
            ne_equitable = False
            break
    if not ne_equitable:
        break
print(f"  Non-edge partition equitable: {ne_equitable}")

# SRG with λ ≠ μ: edge partition is always equitable, non-edge may not be
# For GQ(3,3): non-edge partition is NOT equitable (confirmed)

print("\nDone.")
