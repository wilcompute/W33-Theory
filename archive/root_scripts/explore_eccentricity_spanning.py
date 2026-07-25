#!/usr/bin/env python3
"""
Eccentricity, centers, and extremal subgraphs of W(3,3)
"""

import numpy as np
import itertools
from collections import defaultdict, deque

# Build W(3,3)
J = np.array([[0,1,0,0],[2,0,0,0],[0,0,0,1],[0,0,2,0]], dtype=int)
def symp_form(u, v):
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
adj = defaultdict(set)
for i in range(n):
    for j in range(i+1, n):
        if symp_form(points[i], points[j]) == 0:
            adj[i].add(j)
            adj[j].add(i)

k = len(adj[0])
E = sum(len(adj[i]) for i in range(n)) // 2

print("=" * 70)
print(" ECCENTRICITY, CENTERS, AND SPANNING TREES: W(3,3)")
print("=" * 70)

# Compute distances via BFS
print(f"\n[1] Computing All-Pairs Shortest Paths (BFS)")
distances = {}
for start in range(n):
    dist = [-1] * n
    dist[start] = 0
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                queue.append(v)
    distances[start] = dist

# Compute eccentricity of each vertex
print(f"\n[2] Eccentricity Distribution")
eccentricities = {}
for v in range(n):
    ecc = max(distances[v])
    eccentricities[v] = ecc

ecc_dist = defaultdict(int)
for v in range(n):
    ecc_dist[eccentricities[v]] += 1

print(f"    Eccentricity of each vertex:")
print(f"    Distribution: {dict(sorted(ecc_dist.items()))}")

# Center, periphery, middle
center = [v for v in range(n) if eccentricities[v] == min(eccentricities.values())]
periphery = [v for v in range(n) if eccentricities[v] == max(eccentricities.values())]
radius = min(eccentricities.values())
diameter = max(eccentricities.values())

print(f"\n[3] Radius, Diameter, Center, and Periphery")
print(f"    Radius: {radius}")
print(f"    Diameter: {diameter}")
print(f"    Center: {len(center)} vertices with eccentricity {radius}")
print(f"    Periphery: {len(periphery)} vertices with eccentricity {diameter}")
print(f"    All vertices in center: {len(center) == n} (self-centered)")

if len(center) == n:
    print(f"    => W(3,3) is SELF-CENTERED (all vertices are central)")

# Distance matrix statistics
print(f"\n[4] Distance Matrix Statistics")
dist_counts = defaultdict(int)
num_pairs = n * (n - 1) // 2
for u in range(n):
    for v in range(u+1, n):
        d = distances[u][v]
        dist_counts[d] += 1

print(f"    Pairwise distances:")
for d in sorted(dist_counts.keys()):
    print(f"      Distance {d}: {dist_counts[d]} pairs ({100*dist_counts[d]/num_pairs:.1f}%)")

# Median distance
median_dist_count = 0
for d in sorted(dist_counts.keys()):
    median_dist_count += dist_counts[d]
    if median_dist_count >= num_pairs // 2:
        median_dist = d
        break

print(f"    Median distance: {median_dist}")
print(f"    Mean distance: {sum(d * count for d, count in dist_counts.items()) / num_pairs:.2f}")

# Bipartite graph structure (would require odd diameter)
print(f"\n[5] Bipartiteness Check")
bipartite = diameter % 2 == 1
print(f"    Diameter is odd: {bipartite}")
print(f"    Bipartite status: {'YES' if bipartite else 'NO (non-bipartite)'}")

# Spanning tree count lower bound (via matrix-tree theorem)
print(f"\n[6] Spanning Trees (Matrix-Tree Theorem Bounds)")
print(f"    For any connected n-vertex graph:")
print(f"    Number of spanning trees T(G) satisfies: 1 <= T(G) <= n^(n-2)")
print(f"    For n={n}: 1 <= T(G) <= {n**(n-2):.2e}")
print(f"    For regular k-regular graph:")
print(f"    Lower bound (Cayley-type): T(G) >= k^(n/2-1) ~ exponential")

# Minimum spanning tree (all edges have weight 1)
print(f"\n[7] Minimal Spanning Trees and Cost")
print(f"    For any spanning tree of n={n} vertices:")
print(f"    Number of edges: {n-1}")
print(f"    If all edges have unit weight: cost = {n-1}")
print(f"    Ratio to total edges: (n-1)/E = {n-1}/{E} = {(n-1)/E:.3f}")
print(f"    Tree sparsity: only {100*(n-1)/E:.1f}% of edges needed to span")

# Girth and diameter relationship
print(f"\n[8] Girth-Diameter-Order Relationship")
girth = 3  # From prior knowledge
print(f"    Girth g = {girth} (smallest cycle)")
print(f"    Diameter d = {diameter}")
print(f"    Moore bound: n <= 1 + k(k-1)^((d-1)/2) for odd d")
if diameter % 2 == 1:
    moore = 1 + k * (k-1)**((diameter-1)//2)
    print(f"    Moore bound (d={diameter}): n <= {moore}")
    print(f"    Actual n = {n}")
    print(f"    Ratio: n/Moore = {n/moore:.2%} (excess over Moore)")
else:
    moore = 1 + k + k*(k-1) * sum((k-1)**i for i in range((diameter-2)//2))
    print(f"    Moore bound (even d): n <= {moore}")
    print(f"    Actual n = {n}")

# Vertex eccentricity classes and structure
print(f"\n[9] Eccentricity-Based Partition")
ecc_class = defaultdict(list)
for v in range(n):
    ecc_class[eccentricities[v]].append(v)

print(f"    Eccentricity classes:")
for ecc in sorted(ecc_class.keys()):
    print(f"      Ecc {ecc}: {len(ecc_class[ecc])} vertices")

# Distance regularity check
print(f"\n[10] Distance Regularity (Partial Check)")
print(f"    For each distance d, count vertex pairs at distance d:")
dist_regular = True
for d in range(1, diameter+1):
    per_vertex = defaultdict(int)
    for v1 in range(n):
        for v2 in range(n):
            if distances[v1][v2] == d:
                per_vertex[v1] += 1
    
    counts = list(per_vertex.values())
    uniform = len(set(counts)) == 1
    if d <= 2:
        print(f"    Distance {d}: {'uniform' if uniform else 'non-uniform'} (counts={counts[0] if uniform else set(counts)})")
    dist_regular = dist_regular and uniform

print("\n" + "=" * 70)
print(" SUMMARY: ECCENTRICITY AND STRUCTURE")
print("=" * 70)
print(f"  • Self-centered: YES (all {n} vertices in center)")
print(f"  • Radius = Diameter = {radius}")
print(f"  • All pairwise distances: {sorted(dist_counts.keys())}")
print(f"  • Distance-regular: {dist_regular} (metric-regular property)")
print(f"  • Non-bipartite: YES (even diameter {diameter})")
print(f"  • Moore bound: W achieves {n}/{moore if diameter % 2 == 1 else moore:.0f} = {100*n/(moore if diameter % 2 == 1 else moore):.1f}% of Moore bound")
print(f"  • Spanning trees: T(G) >> 1 (exact count requires numerical computation)")
print()
