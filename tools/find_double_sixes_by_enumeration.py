#!/usr/bin/env python3
"""Brute force: for each skew-independent 6-set S, iterate all 6-subsets T from remaining vertices and
check whether the complement of the S-T meet adjacency is a perfect matching (i.e., K6,6 minus matching).
Writes artifacts/double_sixes_enumeration.json with found pairs.
"""
import json
import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np

from tools.compute_double_sixes import (build_schlafli_adjacency,
                                        compute_we6_orbits, construct_e8_roots,
                                        find_independent_sets_of_size_k)

ROOT = Path(__file__).resolve().parents[1]

roots = construct_e8_roots()
we6 = compute_we6_orbits(roots)
orb = [o for o in we6 if len(o) == 27][0]
adj_meet, ip_counts, adj_ip = build_schlafli_adjacency(roots, orb)
orbit_roots = roots[orb]
gram = orbit_roots @ orbit_roots.T

# build skew adjacency
n = 27
skew_adj = np.zeros((n, n), dtype=bool)
for i in range(n):
    for j in range(i + 1, n):
        if abs(gram[i, j]) < 1e-6:
            skew_adj[i, j] = skew_adj[j, i] = True

skew_indep = find_independent_sets_of_size_k(skew_adj, 6)
print("skew independent sets:", len(skew_indep))

solutions = []
for S in skew_indep:
    S_set = set(S)
    rest = [v for v in range(n) if v not in S_set]
    # iterate T subsets
    for T in combinations(rest, 6):
        T_set = set(T)
        # check T is skew independent
        ok = True
        for a, b in combinations(T, 2):
            if not skew_adj[a, b]:
                ok = False
                break
        if not ok:
            continue
        # build complement of meet adjacency matrix between S and T
        M = np.zeros((6, 6), dtype=int)
        for i, s in enumerate(S):
            for j, t in enumerate(T):
                if not adj_meet[s, t]:
                    M[i, j] = 1
        # M must be permutation matrix: exactly one 1 per row and col
        if not np.all(M.sum(axis=1) == 1):
            continue
        if not np.all(M.sum(axis=0) == 1):
            continue
        # verify it's a permutation matrix (binary and each row/col has one 1)
        if np.count_nonzero(M) != 6:
            continue
        # Found a double-six
        solutions.append((tuple(sorted(S)), tuple(sorted(T))))
    if solutions:
        break

out = ROOT / "artifacts" / "double_sixes_enumeration.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps({"solutions": solutions}, indent=2))
print("Found", len(solutions), "solutions; wrote", out)
