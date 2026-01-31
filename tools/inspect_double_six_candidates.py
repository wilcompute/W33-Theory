#!/usr/bin/env python3
"""Inspect partner-candidate structure for skew-independent 6-sets (double-six halves).

Prints the first few S halves and, for each s_i in S, the candidate t vertices that are
skew to s_i and meet all other s_j. Also prints inner-products to aid diagnosis.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np

from tools.compute_double_sixes import (build_schlafli_adjacency,
                                        compute_we6_orbits, construct_e8_roots,
                                        find_independent_sets_of_size_k)

roots = construct_e8_roots()
we6 = compute_we6_orbits(roots)
orb = [o for o in we6 if len(o) == 27][0]
adj_meet, ip_counts, adj_ip = build_schlafli_adjacency(roots, orb)
orbit_roots = roots[orb]
gram = orbit_roots @ orbit_roots.T

# Build skew adjacency
n = len(orbit_roots)
skew_adj = np.zeros((n, n), dtype=bool)
for i in range(n):
    for j in range(i + 1, n):
        if abs(gram[i, j]) < 1e-6:
            skew_adj[i, j] = skew_adj[j, i] = True

skew_indep = find_independent_sets_of_size_k(skew_adj, 6)
print("Found skew independent sets:", len(skew_indep))

for idx, S in enumerate(skew_indep[:6]):
    print("\nS idx", idx, "S", S)
    S_list = list(S)
    # For each S, for each v not in S compute:
    #  - skew_to_index: index i such that gram[v, S[i]] == 0 (if any)
    #  - meet_count: how many of the S elements v meets (adj_meet True)
    # This will show whether any v is skew to exactly one s_i and meets the other five.
    for i in range(6):
        si = S_list[i]
        others = [S_list[j] for j in range(6) if j != i]
        cands = []
        stats = []
        for v in range(n):
            if v in S_list:
                continue
            meets = sum(1 for s in S_list if adj_meet[v, s])
            is_skew_to_si = abs(gram[v, si]) < 1e-6
            stats.append((v, meets, is_skew_to_si))
            if is_skew_to_si and meets == 5:
                cands.append(v)
        print(f"  i={i} s={si} candidates={len(cands)} -> {cands[:12]}")
        # Show histogram of meet counts
        hist = {}
        for _, meets, _ in stats:
            hist[meets] = hist.get(meets, 0) + 1
        print("    meet_count_hist:", dict(sorted(hist.items())))
        # Show any vertices skew to si and their meet counts (up to 20)
        skew_vs = [(v, m) for v, m, skew in stats if skew]
        print("    skew examples (v,meet_count):", skew_vs[:20])

print("\nDone")
