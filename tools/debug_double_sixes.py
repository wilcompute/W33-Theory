#!/usr/bin/env python3
"""Debug helper for compute_double_sixes independent set search."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.compute_double_sixes import (build_schlafli_adjacency,
                                        compute_we6_orbits, construct_e8_roots,
                                        find_independent_sets_of_size_k)

roots = construct_e8_roots()
we6_orbits = compute_we6_orbits(roots)
orbit27 = [o for o in we6_orbits if len(o) == 27][0]
adj, ip_counts, adj_ip = build_schlafli_adjacency(roots, orbit27)
print("adj_ip", adj_ip)
print(
    "ip_counts (sample):",
    {k: ip_counts[k] for k in sorted(list(ip_counts.keys()))[:10]},
)
print("valency", set(adj.sum(axis=1)))
# For each vertex, count non-neighbors
n = adj.shape[0]
for v in range(n):
    non_neighbors = [u for u in range(n) if u != v and not adj[v, u]]
    print(f"vertex {v}: non-neighbors {len(non_neighbors)}")

print("Searching independent sets of size 6...")
ind = find_independent_sets_of_size_k(adj, 6)
print("Found", len(ind))
if ind:
    print(ind[:5])

# Try greedy heuristic for a single independent set
sel = []
for v in range(n):
    if all(not adj[v, u] for u in sel):
        sel.append(v)
    if len(sel) == 6:
        break
print("Greedy selection", sel, "len", len(sel))
