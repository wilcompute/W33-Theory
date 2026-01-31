#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from itertools import combinations, permutations

import numpy as np

from tools.compute_double_sixes import (build_schlafli_adjacency,
                                        compute_we6_orbits, construct_e8_roots)

roots = construct_e8_roots()
we6 = compute_we6_orbits(roots)
orb = [o for o in we6 if len(o) == 27][0]
adj, ip_counts, adj_ip = build_schlafli_adjacency(roots, orb)
# adj here is 'meet' graph (ip==1.0)
# Find all 6-cliques in adj (cliques meaning all pairwise adj True)
cliques6 = []
for comb in combinations(range(27), 6):
    ok = True
    for i in range(6):
        for j in range(i + 1, 6):
            if not adj[comb[i], comb[j]]:
                ok = False
                break
        if not ok:
            break
    if ok:
        cliques6.append(comb)
print("cliques6 count", len(cliques6))
# Try pairings S,T where S and T are cliques but s_i adjacent to t_j iff i != j
double_sixes = []
for S in cliques6:
    S_list = list(S)
    candidates = [c for c in cliques6 if set(c) & set(S) == set()]
    for T in candidates:
        # Try to find pairing T_list such that for each i, T_list[i] is non-adjacent to S_list[i], and adjacent to others
        # Try permutations of T
        for perm in permutations(T):
            ok = True
            for i in range(6):
                si = S_list[i]
                ti = perm[i]
                if adj[si, ti]:  # should be non-adjacent to partner
                    ok = False
                    break
                for j in range(6):
                    if j == i:
                        continue
                    if not adj[si, perm[j]]:  # should be adjacent to other T members
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                double_sixes.append((S, tuple(sorted(perm)), perm))
                break
    if double_sixes:
        break
print("double_sixes found", len(double_sixes))
if double_sixes:
    print(double_sixes[0])
