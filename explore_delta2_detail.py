"""Quick check: Δ₂ parameter distribution and connectivity."""
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

# Check Δ₂ for vertex 0
v = 0
nbrs = set(j for j in range(n) if A[v,j]==1)
non_nbrs = [j for j in range(n) if j != v and j not in nbrs]
idx = {u: i for i, u in enumerate(non_nbrs)}
S = np.zeros((27, 27), dtype=int)
for i, u in enumerate(non_nbrs):
    for j, w in enumerate(non_nbrs):
        if A[u,w] == 1: S[i,j] = 1

# Connectivity of Δ₂ alone (without v)
visited = {0}
queue = [0]
while queue:
    c = queue.pop(0)
    for j in range(27):
        if j not in visited and S[c,j] == 1:
            visited.add(j); queue.append(j)
print(f"Δ₂(0) connected: {len(visited) == 27}")
print(f"Δ₂(0) component size: {len(visited)}")

# λ, μ within Δ₂
lam_vals = Counter()
mu_vals = Counter()
for i in range(27):
    for j in range(i+1, 27):
        common = sum(S[i,l]*S[j,l] for l in range(27))
        if S[i,j] == 1:
            lam_vals[common] += 1
        else:
            mu_vals[common] += 1

print(f"\nWithin Δ₂(0):")
print(f"  λ values (adj pairs): {dict(lam_vals)}")
print(f"  μ values (non-adj pairs): {dict(mu_vals)}")
print(f"  Edges in Δ₂: {S.sum()//2}")

# Check diameter of Δ₂
from collections import deque
def bfs_dist(adj, start):
    dist = [-1]*adj.shape[0]
    dist[start] = 0
    q = deque([start])
    while q:
        c = q.popleft()
        for j in range(adj.shape[0]):
            if adj[c,j]==1 and dist[j]==-1:
                dist[j] = dist[c]+1
                q.append(j)
    return dist

dists = bfs_dist(S, 0)
print(f"  Diameter of Δ₂: {max(dists)}")
dist_counts = Counter(dists)
print(f"  Distance distribution from v₀: {dict(sorted(dist_counts.items()))}")

# Verify for all 40 vertices: Δ₂ always connected, always diameter 2?
all_connected = True
all_diam2 = True
for v in range(n):
    nbrs = set(j for j in range(n) if A[v,j]==1)
    non_nbrs = [j for j in range(n) if j != v and j not in nbrs]
    S2 = np.zeros((27,27), dtype=int)
    for i, u in enumerate(non_nbrs):
        for j, w in enumerate(non_nbrs):
            if A[u,w] == 1: S2[i,j] = 1
    vis = {0}; q = [0]
    while q:
        c = q.pop(0)
        for j in range(27):
            if j not in vis and S2[c,j]==1:
                vis.add(j); q.append(j)
    if len(vis) != 27: all_connected = False
    d = bfs_dist(S2, 0)
    if max(d) != 2: all_diam2 = False

print(f"\nAll 40 Δ₂ connected: {all_connected}")
print(f"All 40 Δ₂ diameter 2: {all_diam2}")
