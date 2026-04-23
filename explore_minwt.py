"""Quick check: what are the 45 minimum weight supports? 4-regular on 8 verts with 16 edges."""
import itertools, numpy as np
from collections import Counter

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
n = len(points)
A = np.zeros((n, n), dtype=int)
for i in range(n):
    for j in range(i+1, n):
        if symp(points[i], points[j]) == 0: A[i,j] = A[j,i] = 1

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

# Enumerate minimum weight codewords
min_cws = []
for bits in range(2**rank):
    cw = np.zeros(n, dtype=int)
    for i in range(rank):
        if (bits >> i) & 1: cw = (cw + basis[i]) % 2
    if int(cw.sum()) == 8:
        min_cws.append(tuple(int(x) for x in np.where(cw == 1)[0]))

print(f"45 minimum weight (8) codewords")

# Check: are supports K_{4,4}? (complete bipartite on 4+4)
# K_{4,4} has 4*4 = 16 edges and is 4-regular on 8 vertices
for idx, supp in enumerate(min_cws):
    sub = np.zeros((8, 8), dtype=int)
    for i, u in enumerate(supp):
        for j, w in enumerate(supp):
            if A[u, w] == 1: sub[i, j] = 1
    # Check bipartiteness
    color = [-1]*8
    color[0] = 0
    queue = [0]
    bipartite = True
    while queue:
        v = queue.pop(0)
        for w in range(8):
            if sub[v, w] == 1:
                if color[w] == -1:
                    color[w] = 1 - color[v]
                    queue.append(w)
                elif color[w] == color[v]:
                    bipartite = False
    
    # Check complement: are the non-edges forming K₄ + K₄?
    comp = np.zeros((8, 8), dtype=int)
    for i in range(8):
        for j in range(i+1, 8):
            if sub[i,j] == 0: comp[i,j] = comp[j,i] = 1
    comp_edges = comp.sum() // 2
    # K₄+K₄ has 2*C(4,2) = 12 edges
    
    if idx < 3:
        part0 = [i for i in range(8) if color[i]==0]
        part1 = [i for i in range(8) if color[i]==1]
        print(f"  cw {idx}: bipartite={bipartite}, partition {len(part0)}+{len(part1)}, "
              f"complement edges={comp_edges}")

# Count bipartite vs not
bip_count = 0
for supp in min_cws:
    sub = np.zeros((8, 8), dtype=int)
    for i, u in enumerate(supp):
        for j, w in enumerate(supp):
            if A[u, w] == 1: sub[i, j] = 1
    color = [-1]*8; color[0] = 0; queue = [0]; bipartite = True
    while queue:
        v = queue.pop(0)
        for w in range(8):
            if sub[v, w] == 1:
                if color[w] == -1: color[w] = 1 - color[v]; queue.append(w)
                elif color[w] == color[v]: bipartite = False
    if bipartite: bip_count += 1

print(f"\nBipartite (K₄,₄) supports: {bip_count}/45")

# Check: are these related to ovoids (independent sets of size 10)?
# Actually, 45 = C(10,2). Does each minimum weight codeword correspond to
# a pair from some set of 10 objects?

# Check if the 45 supports arise as symmetric differences of pairs of lines from spreads
# Find spreads
cliques4 = []
for i in range(n):
    for j in range(i+1, n):
        if A[i,j] == 1:
            for c in range(j+1, n):
                if A[i,c] == 1 and A[j,c] == 1:
                    for d in range(c+1, n):
                        if A[i,d] == 1 and A[j,d] == 1 and A[c,d] == 1:
                            cliques4.append(frozenset([i,j,c,d]))

line_sets = [set(cl) for cl in cliques4]
spreads = []
def find_spreads(chosen, covered, start):
    if len(covered) == n:
        spreads.append(tuple(sorted(chosen)))
        return
    for idx in range(start, 40):
        if line_sets[idx].isdisjoint(covered):
            find_spreads(chosen + [idx], covered | line_sets[idx], idx + 1)
find_spreads([], set(), 0)

print(f"\nSpreads: {len(spreads)}")

# For each spread, compute symmetric differences of pairs of lines (char vectors mod 2)
spread_symdiffs = set()
for sp in spreads:
    for i, li in enumerate(sp):
        for j in range(i+1, len(sp)):
            lj = sp[j]
            symdiff = frozenset(line_sets[li] ^ line_sets[lj])
            spread_symdiffs.add(symdiff)

min_cw_supports = set(frozenset(s) for s in min_cws)
overlap = min_cw_supports & spread_symdiffs
print(f"Symmetric diffs of spread line pairs: {len(spread_symdiffs)}")
print(f"Min-weight supports that are spread line-pair symdiffs: {len(overlap)}/{len(min_cws)}")

# Each line pair gives |L1 △ L2| = |L1| + |L2| - 2|L1∩L2| = 4+4-0 = 8 (disjoint lines)
# But the union of 2 disjoint lines is not the same as symmetric difference when lines are disjoint
# Union = symdiff for disjoint sets. So these ARE unions of 2 disjoint lines.
# But we checked earlier: 0/45 are unions of 2 lines.

# Wait — the check was "supports that are unions of 2 disjoint GQ lines" = 0.
# But the characteristic vector of the UNION of 2 disjoint lines mod 2 equals the XOR,
# which is only a codeword if both row(line1) and row(line2) are in rowspace(A mod 2).
# The rows of A are NOT the characteristic vectors of lines!
# Rows of A are adjacency rows (indicator of neighbors), NOT line indicators.

# Let's check: what is the intersection of each support with each line?
print(f"\nIntersection sizes of min-wt supports with GQ lines:")
int_sizes = Counter()
for supp in min_cws:
    ss = frozenset(supp)
    for l in cliques4:
        int_sizes[len(ss & l)] += 1
int_dist = {k: v // len(min_cws) for k, v in sorted(int_sizes.items())}
print(f"  Per codeword (avg over 45): {int_dist}")
print(f"  i.e., each min-wt cw intersects each of 40 lines in 0 or 2 points")

# So each min-weight support is a set of 8 vertices that hits each GQ line in 0 or 2 vertices!
# This means it's a "hyperoval" or "hyperbolic line" in the GQ geometry.
# Specifically: a set S with |S ∩ ℓ| ∈ {0, 2} for every line ℓ is called an "even set"
# or "dual hyperoval" or "m-ovoid" (here 2-ovoid: meeting each line in exactly 0 or 2 points).

# How many lines does each support intersect?
lines_per_cw = []
for supp in min_cws:
    ss = frozenset(supp)
    hits = sum(1 for l in cliques4 if len(ss & l) == 2)
    lines_per_cw.append(hits)
print(f"  Lines meeting each support in 2: {Counter(lines_per_cw)}")
# Should be: each vertex on 4 lines, each pair in support adjacent hits C(2,2)=1 line (for edges)
# Total: 16 edges → 16 lines hit in exactly 2... but there are 40 lines total
# Actually each edge is on exactly 1 line, so 16 edges → 16 lines met in 2 pts
# and 40-16 = 24 lines met in 0 pts
