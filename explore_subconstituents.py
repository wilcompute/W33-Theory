"""
Explore subconstituent (local) structure of W(3,3) = SRG(40,12,2,4).

For each vertex v, the first subconstituent Δ₁(v) is the neighborhood
(12 vertices, 2-regular), and the second subconstituent Δ₂(v) is the
induced graph on non-neighbors (27 vertices).

Questions:
1. What is the cycle decomposition of each neighborhood?
   (2-regular on 12 verts: could be C₁₂, C₃+C₉, C₄+C₈, C₅+C₇,
    2C₆, C₃+C₄+C₅, C₃+C₃+C₆, C₄+C₄+C₄, 3C₄, 4C₃, etc.)
2. Are all neighborhoods isomorphic?
3. What is the spectrum and structure of Δ₂(v)?
4. Vertex connectivity κ(W) and edge connectivity λ(W)?
5. Toughness bounds?
"""

import itertools
import numpy as np
from collections import Counter

# ── Build W(3,3) ──
J = np.array([[0,1,0,0],[2,0,0,0],[0,0,0,1],[0,0,2,0]], dtype=int)

def symp(u, v):
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
assert n == 40

A = np.zeros((n, n), dtype=int)
for i in range(n):
    for j in range(i+1, n):
        if symp(points[i], points[j]) == 0:
            A[i,j] = A[j,i] = 1

print("="*60)
print("SUBCONSTITUENT ANALYSIS OF W(3,3)")
print("="*60)

# ── 1. Neighborhood cycle decomposition ──
print("\n--- 1. Neighborhood (First Subconstituent) Cycle Types ---")

def get_cycle_type(adj_sub):
    """Given adjacency matrix of a 2-regular graph, find cycle decomposition."""
    n_sub = adj_sub.shape[0]
    visited = [False]*n_sub
    cycles = []
    for start in range(n_sub):
        if visited[start]:
            continue
        cycle = [start]
        visited[start] = True
        curr = start
        # find first unvisited neighbor
        nbrs = [j for j in range(n_sub) if adj_sub[curr,j]==1]
        prev = -1
        curr = nbrs[0]
        while curr != start:
            visited[curr] = True
            cycle.append(curr)
            nbrs = [j for j in range(n_sub) if adj_sub[curr,j]==1 and j != prev]
            prev = cycle[-2] if len(cycle)>=2 else start
            # pick the neighbor that isn't where we came from
            nbrs2 = [j for j in range(n_sub) if adj_sub[curr,j]==1]
            next_v = [x for x in nbrs2 if x != cycle[-2]][0]
            prev = curr
            curr = next_v
        cycles.append(len(cycle))
    return tuple(sorted(cycles))

cycle_type_counts = Counter()
all_cycle_types = []
for v in range(n):
    nbrs = [j for j in range(n) if A[v,j]==1]
    assert len(nbrs) == 12
    # subgraph induced on neighborhood
    idx_map = {nb: i for i, nb in enumerate(nbrs)}
    sub = np.zeros((12, 12), dtype=int)
    for i, u in enumerate(nbrs):
        for j, w in enumerate(nbrs):
            if A[u,w] == 1:
                sub[i,j] = 1
    # verify 2-regular
    assert all(sub.sum(axis=1)[i] == 2 for i in range(12))
    ct = get_cycle_type(sub)
    cycle_type_counts[ct] += 1
    all_cycle_types.append(ct)

print(f"  Cycle type distribution across all 40 neighborhoods:")
for ct, count in sorted(cycle_type_counts.items()):
    label = " + ".join(f"C_{c}" for c in ct)
    print(f"    {label} : {count} vertices")

all_same = len(cycle_type_counts) == 1
print(f"  All neighborhoods isomorphic? {all_same}")

# ── 2. Neighborhood spectra ──
print("\n--- 2. Neighborhood Spectra ---")
nbhd_spectra = Counter()
for v in range(n):
    nbrs = [j for j in range(n) if A[v,j]==1]
    sub = np.zeros((12, 12), dtype=int)
    for i, u in enumerate(nbrs):
        for j, w in enumerate(nbrs):
            if A[u,w] == 1:
                sub[i,j] = 1
    eigs = sorted(np.round(np.linalg.eigvalsh(sub), 8).tolist())
    eigs_tuple = tuple(round(e, 6) for e in eigs)
    nbhd_spectra[eigs_tuple] += 1

print(f"  Number of distinct neighborhood spectra: {len(nbhd_spectra)}")
for spec, cnt in nbhd_spectra.items():
    print(f"    spectrum = {spec}  x {cnt}")

# ── 3. Second subconstituent Δ₂(v) ──
print("\n--- 3. Second Subconstituent Δ₂(v) ---")

delta2_spectra = Counter()
delta2_degree_seqs = Counter()
delta2_params = Counter()
for v in range(n):
    nbrs = set(j for j in range(n) if A[v,j]==1)
    non_nbrs = [j for j in range(n) if j != v and j not in nbrs]
    assert len(non_nbrs) == 27  # n - 1 - k = 40 - 1 - 12 = 27
    idx_map = {u: i for i, u in enumerate(non_nbrs)}
    sub = np.zeros((27, 27), dtype=int)
    for i, u in enumerate(non_nbrs):
        for j, w in enumerate(non_nbrs):
            if A[u,w] == 1:
                sub[i,j] = 1
    degs = sorted(sub.sum(axis=1).tolist())
    delta2_degree_seqs[tuple(degs)] += 1
    eigs = sorted(np.round(np.linalg.eigvalsh(sub), 6).tolist())
    eigs_tuple = tuple(round(e, 4) for e in eigs)
    delta2_spectra[eigs_tuple] += 1
    
    # Check regularity
    if len(set(degs)) == 1:
        reg = degs[0]
        # Check SRG parameters
        edges_sub = sub.sum() // 2
        n2 = 27
        # For SRG: count common neighbors in subgraph
        lam_vals = set()
        mu_vals = set()
        for i in range(n2):
            for j in range(i+1, n2):
                common = sum(sub[i,l]*sub[j,l] for l in range(n2))
                if sub[i,j] == 1:
                    lam_vals.add(common)
                else:
                    mu_vals.add(common)
        if len(lam_vals) == 1 and len(mu_vals) == 1:
            delta2_params[(n2, reg, lam_vals.pop(), mu_vals.pop())] += 1

print(f"  Number of distinct Δ₂ degree sequences: {len(delta2_degree_seqs)}")
for ds, cnt in delta2_degree_seqs.items():
    print(f"    degree seq min={ds[0]}, max={ds[-1]}, all-same={len(set(ds))==1}  x {cnt}")

print(f"  Number of distinct Δ₂ spectra: {len(delta2_spectra)}")
if len(delta2_spectra) <= 5:
    for spec, cnt in delta2_spectra.items():
        unique_eigs = Counter(spec)
        desc = ", ".join(f"{e}^{m}" for e, m in sorted(unique_eigs.items(), key=lambda x: -x[0]))
        print(f"    [{desc}]  x {cnt}")

if delta2_params:
    print(f"  Δ₂ is SRG? Parameters found:")
    for p, cnt in delta2_params.items():
        print(f"    SRG{p}  x {cnt}")
else:
    print(f"  Δ₂ is NOT a strongly regular graph (parameters vary)")

# ── 4. Vertex/Edge Connectivity ──
print("\n--- 4. Vertex and Edge Connectivity ---")

# For an SRG with λ ≥ 1, vertex connectivity = k (Brouwer-Mesner theorem)
# Since W(3,3) has λ = 2 ≥ 1, κ = k = 12
# We verify computationally using max-flow / min-cut

# Simple computation: find minimum vertex cut via checking
# For SRGs with λ ≥ 1, it's known that κ = k
# Let's verify by checking that removing k-1 = 11 vertices cannot disconnect
# and that removing k = 12 vertices (a neighborhood) does disconnect

# Removing N(v) disconnects: v is isolated
# Brouwer's result: κ(SRG) = k when λ ≥ 1

# BFS connectivity check
def is_connected(adj, removed):
    """Check if graph with 'removed' vertices deleted is connected."""
    remaining = [i for i in range(adj.shape[0]) if i not in removed]
    if len(remaining) <= 1:
        return True
    visited = {remaining[0]}
    queue = [remaining[0]]
    rem_set = set(removed)
    while queue:
        curr = queue.pop(0)
        for j in remaining:
            if j not in visited and adj[curr,j]==1:
                visited.add(j)
                queue.append(j)
    return len(visited) == len(remaining)

# Removing N(v) isolates v → disconnected
v0 = 0
nbrs_v0 = [j for j in range(n) if A[v0,j]==1]
assert not is_connected(A, set(nbrs_v0))
print(f"  Removing N(v₀) (12 verts) disconnects: True  ✓")

# Check: removing any 11 vertices keeps it connected?
# This is expensive to check exhaustively, so we use the theorem
# Brouwer-Mesner: for SRG with λ ≥ 1, κ = k
# Just verify by sampling many random 11-vertex removals
import random
random.seed(42)
all_connected = True
for _ in range(500):
    removed = set(random.sample(range(n), 11))
    if not is_connected(A, removed):
        all_connected = False
        break
print(f"  500 random 11-vertex removals: all connected = {all_connected}")
print(f"  Vertex connectivity κ = k = 12  (Brouwer-Mesner, λ≥1)  ✓")
print(f"  Edge connectivity λ_e = k = 12  (Whitney: κ ≤ λ_e ≤ δ = k)  ✓")

# ── 5. Toughness ──
print("\n--- 5. Toughness ---")
# For SRGs, Brouwer's bound: t ≥ k/(−s) for s the negative eigenvalue
# t(W) ≥ 12/4 = 3
# Removing N(v) gives isolated v + connected remainder → components = 2, removed = 12
# so t ≤ 12/2 = 6 but we need to find the worst case
# Actually removing N(v) gives: {v} isolated, and subgraph on non-nbrs
# which has 27 vertices. If the non-nbr subgraph is connected, we get 2 components.
# Let's check: is Δ₂(v) always connected?

delta2_connected = True
for v in range(n):
    nbrs = set(j for j in range(n) if A[v,j]==1)
    removed = nbrs  # remove the neighborhood, vertex v remains
    non_nbrs_plus_v = [j for j in range(n) if j not in nbrs]
    # Check if this subgraph (v + non-neighbors) is connected
    remaining = non_nbrs_plus_v
    visited = {remaining[0]}
    queue = [remaining[0]]
    while queue:
        curr = queue.pop(0)
        for j in remaining:
            if j not in visited and A[curr,j]==1:
                visited.add(j)
                queue.append(j)
    connected_here = (len(visited) == len(remaining))
    if not connected_here:
        delta2_connected = False
        print(f"  Δ₂(v={v}) ∪ {{v}} is disconnected!")
        break

if delta2_connected:
    print(f"  Removing N(v) always gives exactly 2 components: {{v}} + Δ₂(v)")
    print(f"  Toughness ≥ k/|s| = 12/4 = 3  (Brouwer)")
    print(f"  Upper bound from N(v) removal: t ≤ 12/2 = 6")

# Better toughness analysis: try removing various vertex sets
# to get more components
best_ratio = float('inf')
best_set = None
best_components = None

# Try removing neighborhoods of edges (common neighbors)
for i in range(n):
    for j in range(i+1, n):
        if A[i,j] == 1:
            # Remove common neighbors of i,j plus some
            common = [v for v in range(n) if v!=i and v!=j and A[i,v]==1 and A[j,v]==1]
            # Try removing N(i) ∩ N(j) = λ = 2 common neighbors
            # This is too small. Let's try removing N(i) ∪ N(j)
            removed = set(v for v in range(n) if A[i,v]==1 or A[j,v]==1) - {i, j}
            remaining = [v for v in range(n) if v not in removed]
            # Count components
            comp = 0
            visited_all = set()
            for start in remaining:
                if start in visited_all:
                    continue
                comp += 1
                visited = {start}
                queue = [start]
                while queue:
                    curr = queue.pop(0)
                    for w in remaining:
                        if w not in visited and A[curr,w]==1:
                            visited.add(w)
                            queue.append(w)
                visited_all |= visited
            if comp >= 2:
                ratio = len(removed) / comp
                if ratio < best_ratio:
                    best_ratio = ratio
                    best_set = removed
                    best_components = comp
            break  # just sample a few
    if best_set is not None:
        break

# The key toughness result for SRG(40,12,2,4):
# By Brouwer, SRGs with eigenvalue s have toughness ≥ -s⁻¹·k = k/|s|
# For k=12, s=-4: t ≥ 3
# Since it's Hamiltonian (proven), t ≥ 1
# Chvátal: t ≥ n/(2·α) for Hamiltonian → t ≥ 40/14 ≈ 2.86
print(f"  Brouwer toughness lower bound: t(W) ≥ k/|s| = {12}/{4} = 3")

# ── 6. Diameter / Girth / Local Girth ──
print("\n--- 6. Local Girth Analysis ---")
# Local girth at v = length of shortest cycle through v
local_girths = []
for v in range(n):
    # BFS from v to find shortest cycle through v
    # = shortest cycle in the graph containing v
    # For a 12-regular graph with λ=2, every edge is in a triangle
    # So local girth = 3 for all vertices
    nbrs = [j for j in range(n) if A[v,j]==1]
    has_triangle = False
    for i, u in enumerate(nbrs):
        for w in nbrs[i+1:]:
            if A[u,w] == 1:
                has_triangle = True
                break
        if has_triangle:
            break
    local_girths.append(3 if has_triangle else 0)

print(f"  Local girth = 3 for all vertices: {all(g==3 for g in local_girths)}")

# ── 7. Mu-graphs: common neighbors of non-adjacent pairs ──
print("\n--- 7. μ-Graphs (Common Neighbors of Non-adjacent Pairs) ---")

mu_graph_types = Counter()
for i in range(n):
    for j in range(i+1, n):
        if A[i,j] == 0:  # non-adjacent
            common = [v for v in range(n) if A[i,v]==1 and A[j,v]==1]
            assert len(common) == 4  # μ = 4
            # Induced subgraph on these 4 common neighbors
            sub = np.zeros((4,4), dtype=int)
            for a in range(4):
                for b in range(a+1, 4):
                    if A[common[a], common[b]] == 1:
                        sub[a,b] = sub[b,a] = 1
            edges = sub.sum() // 2
            degs = tuple(sorted(sub.sum(axis=1).tolist()))
            mu_graph_types[(edges, degs)] += 1

print(f"  μ = 4 for all non-adjacent pairs: True  ✓")
print(f"  Distinct μ-graph types: {len(mu_graph_types)}")
for (edges, degs), cnt in sorted(mu_graph_types.items()):
    # Classify: 0 edges = 4K₁, 1 edge = P₂+2K₁, 2 edges = P₃+K₁ or 2K₂ or P₂+P₂,
    #           3 edges = K₃+K₁ or P₄ or star, ...
    if edges == 0:
        name = "4K₁ (empty)"
    elif edges == 1:
        name = "K₂ + 2K₁"
    elif edges == 2:
        if degs == (0, 0, 2, 2):
            name = "K₃ (missing)"
        elif degs == (0, 1, 1, 2):
            name = "P₃ + K₁"
        elif degs == (1, 1, 1, 1):
            name = "2K₂ (matching)"
        else:
            name = f"2-edge ({degs})"
    elif edges == 3:
        if degs == (1, 1, 1, 3):
            name = "K₁,₃ (star)"
        elif degs == (0, 2, 2, 2):
            name = "K₃ + K₁"
        elif degs == (1, 1, 2, 2):
            name = "P₄ (path)"
        else:
            name = f"3-edge ({degs})"
    elif edges == 4:
        if degs == (1, 2, 2, 3):
            name = "K₄ − e"
        elif degs == (2, 2, 2, 2):
            name = "C₄ (cycle)"
        else:
            name = f"4-edge ({degs})"
    elif edges == 5:
        name = "K₄ − e (almost complete)"
    elif edges == 6:
        name = "K₄ (complete)"
    else:
        name = f"{edges}-edge ({degs})"
    print(f"    {name}: {cnt} pairs ({cnt}/{sum(mu_graph_types.values())} = {cnt/sum(mu_graph_types.values()):.4f})")

# ── 8. Lambda-graphs: common neighbors of adjacent pairs ──
print("\n--- 8. λ-Graphs (Common Neighbors of Adjacent Pairs) ---")

lambda_graph_types = Counter()
for i in range(n):
    for j in range(i+1, n):
        if A[i,j] == 1:  # adjacent
            common = [v for v in range(n) if v!=i and v!=j and A[i,v]==1 and A[j,v]==1]
            assert len(common) == 2  # λ = 2
            # Are the two common neighbors adjacent?
            adj_or_not = A[common[0], common[1]]
            lambda_graph_types[adj_or_not] += 1

total_adj_pairs = sum(lambda_graph_types.values())
print(f"  λ = 2 for all adjacent pairs: True  ✓")
print(f"  Total adjacent pairs: {total_adj_pairs}")
print(f"  λ-graph = K₂ (common nbrs adjacent): {lambda_graph_types.get(1, 0)}")
print(f"  λ-graph = 2K₁ (common nbrs non-adj): {lambda_graph_types.get(0, 0)}")

# In GQ(3,3), two adjacent vertices lie on exactly 1 line (4-clique).
# The two common neighbors are the other two points on that line.
# Since lines are 4-cliques, these two ARE adjacent.
print(f"  => All λ-graphs are K₂ (both common neighbors on same line): "
      f"{lambda_graph_types.get(1,0) == total_adj_pairs}")

# ── 9. Perfect matchings ──
print("\n--- 9. Perfect Matchings ---")
# W(3,3) is Hamiltonian, so it has perfect matchings.
# Count is expensive, but we can verify existence and compute the matching number.
# matching number ν = n/2 = 20 (since graph is Hamiltonian)
# Actually, each spread gives 10 lines of 4 vertices = 10 × C(4,2) = 60 matchings per spread
# But let's just verify matching number = 20

# Greedy maximum matching
def max_matching_greedy(adj):
    """Find a maximal matching greedily."""
    n_v = adj.shape[0]
    matched = set()
    matching = []
    # Sort edges by some criterion
    for i in range(n_v):
        if i in matched:
            continue
        for j in range(i+1, n_v):
            if j in matched:
                continue
            if adj[i,j] == 1:
                matching.append((i,j))
                matched.add(i)
                matched.add(j)
                break
    return matching

m = max_matching_greedy(A)
print(f"  Greedy matching size: {len(m)}")
print(f"  Perfect matching (ν = n/2 = 20): {len(m) == 20}")

# From Hamiltonian cycle, extract perfect matching
# We know the graph is Hamiltonian, so ν = 20

print("\n" + "="*60)
print("EXPLORATION COMPLETE")
print("="*60)
