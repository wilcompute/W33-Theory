"""Check if Δ₂(v) is distance-regular."""
import itertools, numpy as np
from collections import Counter, deque

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

def bfs_dist(adj, start):
    nn = adj.shape[0]
    dist = [-1]*nn
    dist[start] = 0
    q = deque([start])
    while q:
        c = q.popleft()
        for j in range(nn):
            if adj[c,j]==1 and dist[j]==-1:
                dist[j] = dist[c]+1
                q.append(j)
    return dist

def check_dr(S):
    """Check if graph S is distance-regular, return intersection array or None."""
    nn = S.shape[0]
    # Collect intersection numbers
    b_vals = {}  # i -> set of b_i values seen
    c_vals = {}
    a_vals = {}
    
    for src in range(nn):
        d = bfs_dist(S, src)
        max_d = max(d)
        for w in range(nn):
            if w == src: continue
            dw = d[w]
            nbrs_w = [j for j in range(nn) if S[w,j]==1]
            ci = sum(1 for j in nbrs_w if d[j] == dw - 1) if dw > 0 else 0
            ai = sum(1 for j in nbrs_w if d[j] == dw)
            bi = sum(1 for j in nbrs_w if d[j] == dw + 1)
            
            b_vals.setdefault(dw, set()).add(bi)
            c_vals.setdefault(dw, set()).add(ci)
            a_vals.setdefault(dw, set()).add(ai)
    
    is_dr = all(len(v)==1 for v in b_vals.values()) and \
            all(len(v)==1 for v in c_vals.values()) and \
            all(len(v)==1 for v in a_vals.values())
    
    if is_dr:
        max_d = max(b_vals.keys())
        b_arr = [b_vals.get(i, {0}).copy().pop() for i in range(max_d+1)]
        c_arr = [c_vals.get(i, {0}).copy().pop() for i in range(max_d+1)]
        a_arr = [a_vals.get(i, {0}).copy().pop() for i in range(max_d+1)]
        return b_arr, c_arr, a_arr
    else:
        # Show what varies
        for i in sorted(set(b_vals)|set(c_vals)|set(a_vals)):
            if i in b_vals and len(b_vals[i])>1: print(f"  b_{i} varies: {b_vals[i]}")
            if i in c_vals and len(c_vals[i])>1: print(f"  c_{i} varies: {c_vals[i]}")
            if i in a_vals and len(a_vals[i])>1: print(f"  a_{i} varies: {a_vals[i]}")
        return None

# Check Δ₂(0)
print("=== Checking Δ₂(0) ===")
v = 0
nbrs = set(j for j in range(n) if A[v,j]==1)
non_nbrs = [j for j in range(n) if j != v and j not in nbrs]
S = np.zeros((27,27), dtype=int)
for i, u in enumerate(non_nbrs):
    for jj, w in enumerate(non_nbrs):
        if A[u,w] == 1: S[i,jj] = 1

result = check_dr(S)
if result:
    b, c, a = result
    print(f"  Distance-regular!")
    print(f"  b = {b}")
    print(f"  c = {c}")
    print(f"  a = {a}")
    # Standard notation: intersection array {b₀,...,b_{d-1}; c₁,...,c_d}
    d = max(i for i in range(len(b)) if b[i] > 0) + 1 if any(bi > 0 for bi in b) else 0
    print(f"  Diameter = {d}")
    b_part = b[:d]
    c_part = c[1:d+1]
    print(f"  Intersection array: {{{', '.join(map(str,b_part))}; {', '.join(map(str,c_part))}}}")
else:
    print("  NOT distance-regular")

# Check all 40
print("\n=== Checking all 40 Δ₂ ===")
all_dr = True
for v in range(n):
    nbrs = set(j for j in range(n) if A[v,j]==1)
    non_nbrs = [j for j in range(n) if j != v and j not in nbrs]
    S2 = np.zeros((27,27), dtype=int)
    for i, u in enumerate(non_nbrs):
        for jj, w in enumerate(non_nbrs):
            if A[u,w] == 1: S2[i,jj] = 1
    result = check_dr(S2)
    if result is None:
        all_dr = False
        print(f"  Δ₂({v}) is NOT DR")
        break

print(f"All 40 Δ₂ distance-regular: {all_dr}")

# Distance-3 pair adjacency
print("\n=== Distance-3 pairs ===")
v = 0
nbrs = set(j for j in range(n) if A[v,j]==1)
non_nbrs = [j for j in range(n) if j != v and j not in nbrs]
S = np.zeros((27,27), dtype=int)
for i, u in enumerate(non_nbrs):
    for jj, w in enumerate(non_nbrs):
        if A[u,w] == 1: S[i,jj] = 1

antipodal_classes = []
for src in range(27):
    d = bfs_dist(S, src)
    d3 = [j for j in range(27) if d[j] == 3]
    antipodal_classes.append(frozenset([src] + d3))
    if src < 5:
        adj = S[d3[0], d3[1]] if len(d3)==2 else "?"
        print(f"  From {src}: dist-3 = {d3}, mutual adj = {adj}")

unique_classes = set(antipodal_classes)
print(f"\n  Antipodal classes (dist-3 triples): {len(unique_classes)}")
for cl in sorted(unique_classes, key=lambda x: min(x)):
    print(f"    {sorted(cl)}")
