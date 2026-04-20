#!/usr/bin/env python3
"""
Neighborhood and induced subgraph structure
"""

import numpy as np
import itertools
from collections import defaultdict, Counter

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

print("=" * 70)
print(" NEIGHBORHOOD STRUCTURE AND INDUCED SUBGRAPHS")
print("=" * 70)

# For each vertex, analyze its neighborhood as an induced subgraph
print(f"\n[1] Neighborhood Properties (for vertex 0)")
v = 0
neighbors = sorted(list(adj[v]))
k = len(neighbors)

print(f"    Neighbors of vertex {v}: {neighbors}")
print(f"    Neighborhood size: |N(v)| = {k}")

# Count edges in the neighborhood (induced subgraph)
edges_in_neighborhood = 0
for i in range(k):
    for j in range(i+1, k):
        if neighbors[j] in adj[neighbors[i]]:
            edges_in_neighborhood += 1

print(f"    Edges in induced N(v): {edges_in_neighborhood}")
print(f"    N(v) parameter: k_N = {edges_in_neighborhood} edges in {k}-vertex subgraph")

# For SRG with parameters λ, the number of edges in N(v) is k(λ)/2 = 12*2/2 = 12
# But let me verify this properly
print(f"\n    From SRG theory: neighbors of v share 2 common edges")
print(f"    Each neighbor u of v has exactly λ = 2 edges to other neighbors of v")
print(f"    Total edge endpoints: k*λ = {k}*2 = {2*k}")
print(f"    Total edges: k*λ/2 = {k*2//2} = {edges_in_neighborhood}")

# Check connectivity of neighborhood
from collections import deque

def is_connected(vertices, adj_dict):
    if not vertices:
        return True
    visited = {vertices[0]}
    queue = deque([vertices[0]])
    while queue:
        u = queue.popleft()
        for v in adj_dict[u]:
            if v in vertices and v not in visited:
                visited.add(v)
                queue.append(v)
    return len(visited) == len(vertices)

neighbors_connected = is_connected(neighbors, adj)
print(f"    N(v) is connected: {neighbors_connected}")

# Analyze all neighborhoods (sample)
print(f"\n[2] Neighborhood Edge Patterns (sampling vertices)")
edge_counts = []
for sample_v in range(min(10, n)):
    neighbors_sv = list(adj[sample_v])
    edges_sv = 0
    for i in range(len(neighbors_sv)):
        for j in range(i+1, len(neighbors_sv)):
            if neighbors_sv[j] in adj[neighbors_sv[i]]:
                edges_sv += 1
    edge_counts.append(edges_sv)

print(f"    Sample of {len(edge_counts)} vertices:")
print(f"    Edge counts in neighborhoods: {edge_counts}")
print(f"    All same: {len(set(edge_counts)) == 1} (expected for vertex-transitive)")

# Non-neighbors
print(f"\n[3] Non-Neighborhood (Distance-2 Neighborhood)")
v = 0
neighbors = set(adj[v])
non_neighbors = [u for u in range(n) if u != v and u not in neighbors]

print(f"    Non-neighbors of vertex {v}: {len(non_neighbors)} vertices")
print(f"    Expected: n - 1 - k = {n - 1 - k}")

# Edges in non-neighbor induced subgraph
edges_in_nonneighbors = 0
for i in range(len(non_neighbors)):
    for j in range(i+1, len(non_neighbors)):
        if non_neighbors[j] in adj[non_neighbors[i]]:
            edges_in_nonneighbors += 1

print(f"    Edges in induced non-neighbors: {edges_in_nonneighbors}")
print(f"    Non-neighbor subgraph: {len(non_neighbors)}-vertex, {edges_in_nonneighbors}-edge")

# Density analysis
print(f"\n[4] Subgraph Density Analysis")
print(f"    N(v) (neighborhood): {k} vertices, {edges_in_neighborhood} edges")
if edges_in_neighborhood > 0:
    density_N = 2 * edges_in_neighborhood / (k * (k-1))
    print(f"      Density: {density_N:.3f}")

print(f"    Non-N(v) (complement of neighborhood): {len(non_neighbors)} vertices, {edges_in_nonneighbors} edges")
if edges_in_nonneighbors > 0:
    density_nonN = 2 * edges_in_nonneighbors / (len(non_neighbors) * (len(non_neighbors)-1))
    print(f"      Density: {density_nonN:.3f}")

# Spectrum of neighborhood
print(f"\n[5] Spectrum of Neighborhood Induced Subgraph")
neighbors_v = sorted(list(adj[v]))
n_N = len(neighbors_v)
A_N = np.zeros((n_N, n_N), dtype=int)
for i in range(n_N):
    for j in range(n_N):
        if neighbors_v[j] in adj[neighbors_v[i]]:
            A_N[i,j] = 1

eigvals_N = np.linalg.eigvalsh(A_N)
eigvals_N_sorted = sorted(eigvals_N, reverse=True)
eigvals_rounded = [round(x, 1) for x in eigvals_N_sorted]
eig_counts = Counter(eigvals_rounded)

print(f"    Neighborhood spectrum: {dict(sorted(eig_counts.items(), reverse=True))}")

# Regularity of neighborhood
degrees_N = [np.sum(A_N[i]) for i in range(n_N)]
print(f"    Neighborhood vertex degrees: {set(degrees_N)}")
print(f"    Regular: {len(set(degrees_N)) == 1}")
if len(set(degrees_N)) == 1:
    print(f"      Regularity: {degrees_N[0]}-regular")
    print(f"      For SRG, N(v) has λ = 2 edges per vertex to other neighbors")

# Clique in neighborhood
max_clique_N = 0
for mask in range(1 << n_N):
    clique_vertices = [neighbors_v[i] for i in range(n_N) if mask & (1 << i)]
    if len(clique_vertices) > max_clique_N:
        # Check if it's a clique
        is_clique = True
        for i in range(len(clique_vertices)):
            for j in range(i+1, len(clique_vertices)):
                if clique_vertices[j] not in adj[clique_vertices[i]]:
                    is_clique = False
                    break
            if not is_clique:
                break
        if is_clique:
            max_clique_N = len(clique_vertices)

print(f"\n[6] Clique and Independence in Neighborhoods")
print(f"    Max clique in N(v): {max_clique_N} (if 3, then N(v) contains triangles)")

# Independence in neighborhood
max_indep_N = 0
for mask in range(1 << min(n_N, 14)):  # Limit for computational reasons
    indep_vertices = [neighbors_v[i] for i in range(min(n_N, 14)) if mask & (1 << i)]
    if len(indep_vertices) > max_indep_N:
        is_indep = True
        for i in range(len(indep_vertices)):
            for j in range(i+1, len(indep_vertices)):
                if indep_vertices[j] in adj[indep_vertices[i]]:
                    is_indep = False
                    break
            if not is_indep:
                break
        if is_indep:
            max_indep_N = len(indep_vertices)

print(f"    Max independence in N(v): >= {max_indep_N}")

print("\n" + "=" * 70)
print(" SUMMARY: NEIGHBORHOOD STRUCTURE")
print("=" * 70)
print(f"  • Neighborhood size: k = 12")
print(f"  • Edges in neighborhood: k·λ/2 = 12·2/2 = {edges_in_neighborhood}")
print(f"  • Neighborhood connected: {neighbors_connected}")
print(f"  • Non-neighborhood vertices: 27")
print(f"  • Neighborhood induced subgraph is {degrees_N[0] if len(set(degrees_N)) == 1 else 'irregular'}-regular")
print(f"  • Each vertex in N(v) connects to {degrees_N[0]} other neighbors of v")
print()
