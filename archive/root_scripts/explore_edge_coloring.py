#!/usr/bin/env python3
"""
Perfect matchings via maximum matching algorithm (Edmond's blossom-like approach)
"""

import numpy as np
import itertools
from collections import defaultdict

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

def max_matching_bfs(adj, n):
    """Find maximum matching using augmenting path approach"""
    matching = set()
    matched = set()
    
    improved = True
    while improved:
        improved = False
        # Try to find an augmenting path using BFS
        unmatched = set(range(n)) - matched
        
        for start in unmatched:
            if start in matched:
                continue
            # BFS to find augmenting path
            queue = [start]
            parent = {start: None}
            found_aug = False
            
            while queue and not found_aug:
                u = queue.pop(0)
                for v in adj[u]:
                    if v not in parent:
                        parent[v] = u
                        if v not in matched:
                            # Found augmenting path: reconstruct and flip
                            path = []
                            curr = v
                            while curr is not None:
                                prev = parent[curr]
                                if prev is not None:
                                    path.append((min(prev, curr), max(prev, curr)))
                                curr = prev
                            
                            # Flip matching status on path
                            for edge in path:
                                if edge in matching:
                                    matching.discard(edge)
                                    matched.discard(edge[0])
                                    matched.discard(edge[1])
                                else:
                                    matching.add(edge)
                                    matched.add(edge[0])
                                    matched.add(edge[1])
                            found_aug = True
                            improved = True
                            break
                        else:
                            # Continue through matched vertex
                            queue.append(v)
    
    return matching

print("=" * 70)
print(" EDGE COLORING AND MATCHING DECOMPOSITION: W(3,3)")
print("=" * 70)

print(f"\n[1] Maximum Matching via Augmenting Paths")
max_m = max_matching_bfs(adj, n)
print(f"    Maximum matching size: {len(max_m)}")
print(f"    Expected for even n: n/2 = {n/2}")
print(f"    Covers: {2*len(max_m)} vertices out of {n}")
print(f"    Unmatched: {n - 2*len(max_m)} vertices")

# Decompose edges using maximum matchings
print(f"\n[2] Iterative Edge Decomposition")
matchings = []
current_adj = {i: set(adj[i]) for i in range(n)}

for iter_num in range(1, k+2):  # Try k+1 matchings (Vizing upper bound)
    matching = max_matching_bfs(current_adj, n)
    
    if not matching:
        print(f"    Matching #{iter_num}: EMPTY (complete decomposition achieved)")
        break
    
    matchings.append(matching)
    
    # Remove edges
    for u, v in matching:
        current_adj[u].discard(v)
        current_adj[v].discard(u)
    
    uncovered = sum(len(current_adj[i]) for i in range(n)) // 2
    print(f"    Matching #{iter_num}: size {len(matching)}, remaining edges: {uncovered}")

print(f"\n[3] Decomposition Summary")
total_edges = sum(len(m) for m in matchings)
print(f"    Matchings found: {len(matchings)}")
print(f"    Total edges covered: {total_edges}")
print(f"    Expected edges: {E}")
print(f"    Perfect decomposition: {total_edges == E}")

if total_edges == E:
    print(f"\n[4] Edge Chromatic Number")
    if len(matchings) <= k:
        print(f"    All matchings fit in {len(matchings)} <= k = {k}")
        print(f"    χ'(W(3,3)) = {len(matchings)} (CLASS 1)")
    else:
        print(f"    Need {len(matchings)} matchings > k = {k}")
        print(f"    χ'(W(3,3)) = {len(matchings)} (CLASS 2)")

# Check regularity of each matching
print(f"\n[5] Matching Coverage and Regularity")
if matchings:
    sizes = [len(m) for m in matchings]
    print(f"    Matching sizes: {sizes}")
    all_perfect = all(size == n//2 for size in sizes)
    print(f"    All perfect (size {n//2}): {all_perfect}")
    if all_perfect:
        print(f"    ✓ All {len(matchings)} matchings are perfect matchings")

# Verify decomposition property
print(f"\n[6] Verification: Edge Partition Property")
all_edges_in_matchings = set()
for m_idx, matching in enumerate(matchings):
    for u, v in matching:
        all_edges_in_matchings.add((min(u,v), max(u,v)))

# Construct all edges from adjacency
all_actual_edges = set()
for u in range(n):
    for v in adj[u]:
        if u < v:
            all_actual_edges.add((u,v))

if all_edges_in_matchings == all_actual_edges:
    print(f"    ✓ Perfect partition: every edge in exactly one matching")
else:
    missing = all_actual_edges - all_edges_in_matchings
    extra = all_edges_in_matchings - all_actual_edges
    print(f"    Missing edges: {len(missing)}")
    print(f"    Extra edges: {len(extra)}")

# Summary stats
print(f"\n[7] Edge Color Distribution (if perfect decomposition)")
if total_edges == E:
    deg_by_color = defaultdict(int)
    for m_idx, matching in enumerate(matchings):
        for u, v in matching:
            deg_by_color[m_idx] += 1
    
    print(f"    Color class sizes (# edges): {sorted(deg_by_color.values())}")
    
    # Check if each vertex has exactly one incident edge per color
    vertex_color_degree = defaultdict(lambda: defaultdict(int))
    for m_idx, matching in enumerate(matchings):
        for u, v in matching:
            vertex_color_degree[u][m_idx] += 1
            vertex_color_degree[v][m_idx] += 1
    
    all_one = all(
        all(deg == 1 for deg in color_degs.values())
        for v_idx, color_degs in vertex_color_degree.items()
    )
    print(f"    Each vertex incident to exactly 1 edge per color: {all_one}")

print("\n" + "=" * 70)
print(" SUMMARY: EDGE COLORING")
print("=" * 70)
if total_edges == E:
    print(f"  • Perfect edge decomposition: {len(matchings)} matchings")
    if len(matchings) == k:
        print(f"  • Edge chromatic number χ'(W) = {k}")
        print(f"  • W(3,3) is CLASS 1 k-edge-colorable")
    else:
        print(f"  • Edge chromatic number χ'(W) = {len(matchings)}")
        if len(matchings) == k + 1:
            print(f"  • W(3,3) is CLASS 2 (requires k+1 colors)")
else:
    print(f"  • Incomplete decomposition: {total_edges}/{E} edges covered")
print()
