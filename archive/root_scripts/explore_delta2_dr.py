"""Check if Δ₂(v) is distance-regular with intersection array {8,6,1; 1,3,8}."""
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

# Check all 40 Δ₂ for distance-regularity
print("Checking distance-regularity of all 40 second subconstituents...")

all_dr = True
all_arrays = set()
all_dist_distributions = Counter()

for v in range(n):
    nbrs = set(j for j in range(n) if A[v,j]==1)
    non_nbrs = [j for j in range(n) if j != v and j not in nbrs]
    S = np.zeros((27,27), dtype=int)
    for i, u in enumerate(non_nbrs):
        for jj, w in enumerate(non_nbrs):
            if A[u,w] == 1: S[i,jj] = 1
    
    # Check intersection numbers from each vertex
    is_dr = True
    int_nums = {}  # (i, j) -> count of neighbors at dist j from source that are neighbors of vertex at dist i
    
    for src in range(27):
        d = bfs_dist(S, src)
        max_d = max(d)
        
        dd = Counter(d)
        all_dist_distributions[tuple(sorted(dd.items()))] += 1
        
        for w in range(27):
            if w == src: continue
            dw = d[w]
            # Count neighbors of w at each distance from src
            for nb in range(27):
                if S[w,nb] != 1: continue
                dnb = d[nb]
                key = (dw, dnb)
                if key not in int_nums:
                    int_nums[key] = set()
                # count how many neighbors of w are at distance dnb from src
            
    # More direct: compute intersection numbers b_i, c_i, a_i
    for src in range(27):
        d = bfs_dist(S, src)
        for w in range(27):
            if w == src: continue
            dw = d[w]
            nbrs_w = [j for j in range(27) if S[w,j]==1]
            ci = sum(1 for j in nbrs_w if d[j] == dw - 1) if dw > 0 else 0
            ai = sum(1 for j in nbrs_w if d[j] == dw)
            bi = sum(1 for j in nbrs_w if d[j] == dw + 1)
            
            key = f"c{dw}"
            if key not in int_nums: int_nums[key] = set()
            int_nums[key].add(ci)
            
            key = f"a{dw}"
            if key not in int_nums: int_nums[key] = set()
            int_nums[key].add(ai)
            
            key = f"b{dw}"
            if key not in int_nums: int_nums[key] = set()
            int_nums[key].add(bi)
    
    # Check if all constant
    for key, vals in int_nums.items():
        if len(vals) > 1:
            is_dr = False
    
    if is_dr:
        arr = []
        max_d_val = max(int(k[1:]) for k in int_nums.keys())
        for i in range(max_d_val + 1):
            b = int_nums.get(f"b{i}", {0}).pop() if f"b{i}" in int_nums else 0
            c = int_nums.get(f"c{i}", {0}).pop() if f"c{i}" in int_nums else 0
            a = int_nums.get(f"a{i}", {0}).pop() if f"a{i}" in int_nums else 0
            arr.append((b, c, a))
        arr_str = str(arr)
        all_arrays.add(arr_str)
    else:
        all_dr = False
    
    if v == 0:
        print(f"\nΔ₂(0) intersection numbers:")
        for key in sorted(int_nums.keys()):
            print(f"  {key} = {int_nums[key]}")
        print(f"  Distance-regular: {is_dr}")

print(f"\nAll 40 Δ₂ distance-regular: {all_dr}")
if all_arrays:
    print(f"Intersection arrays found: {all_arrays}")

print(f"\nDistance distributions (from any vertex within any Δ₂):")
for dd, cnt in sorted(all_dist_distributions.items()):
    print(f"  {dict(dd)} x {cnt}")

# Also check: are the two distance-3 vertices adjacent to each other?
print("\nDistance-3 pair adjacency check:")
v = 0
nbrs = set(j for j in range(n) if A[v,j]==1)
non_nbrs = [j for j in range(n) if j != v and j not in nbrs]
S = np.zeros((27,27), dtype=int)
for i, u in enumerate(non_nbrs):
    for jj, w in enumerate(non_nbrs):
        if A[u,w] == 1: S[i,jj] = 1

for src in range(27):
    d = bfs_dist(S, src)
    d3_verts = [j for j in range(27) if d[j] == 3]
    if len(d3_verts) == 2:
        adj = S[d3_verts[0], d3_verts[1]]
        print(f"  From {src}: d3 pair {d3_verts}, adjacent={adj}")
    if src >= 4: break  # just a few samples
