#!/usr/bin/env python3
"""Exhaustive search for double-sixes by checking all 6-sets S and finding T via bipartite matching.

This is heavier but should find all solutions if they exist. Uses meet adjacency semantics.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from itertools import combinations

from tools.compute_double_sixes import (build_schlafli_adjacency,
                                        compute_we6_orbits, construct_e8_roots)

# Simple DFS-based bipartite matching for small sizes


def bipartite_matching(adj_map, n_left, n_right):
    # adj_map: dict left_idx -> iterable of right_idx
    match_r = {}

    def dfs(u, seen):
        for v in adj_map.get(u, []):
            if v in seen:
                continue
            seen.add(v)
            if v not in match_r or dfs(match_r[v], seen):
                match_r[v] = u
                return True
        return False

    match_count = 0
    for u in range(n_left):
        if dfs(u, set()):
            match_count += 1
    return match_count == n_left, match_r


def find_double_sixes_exhaustive():
    roots = construct_e8_roots()
    we6 = compute_we6_orbits(roots)
    orb = [o for o in we6 if len(o) == 27][0]
    adj_meet, ip_counts, adj_ip = build_schlafli_adjacency(roots, orb)

    n = 27
    solutions = []
    total_checked = 0
    # Consider candidate S types: skew-independent sets and meet-cliques
    # skew-independent sets (pairwise gram == 0)
    orbit_roots = construct_e8_roots()[orb]
    gram = orbit_roots @ orbit_roots.T

    def find_skew_indep_sets():
        skew_adj = [[False] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if abs(gram[i, j] - 0.0) < 1e-6:
                    skew_adj[i][j] = skew_adj[j][i] = True
        return list(combinations(range(n), 6)) if False else None

    # Build candidates explicitly for two strategies
    skew_candidates = []
    # brute-force combinations but prune quickly using skew condition
    for S in combinations(range(n), 6):
        ok = True
        for i in range(6):
            for j in range(i + 1, 6):
                if abs(gram[S[i], S[j]] - 0.0) > 1e-6:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            skew_candidates.append(S)

    # meet-clique candidates
    clique_candidates = []
    for S in combinations(range(n), 6):
        ok = True
        for i in range(6):
            for j in range(i + 1, 6):
                if not adj_meet[S[i], S[j]]:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            clique_candidates.append(S)

    total_checked = 0
    # Try both candidate types
    for candidates in (skew_candidates, clique_candidates):
        for S in candidates:
            total_checked += 1
            S_set = set(S)
            # build allowed candidates for each position i using meet adjacency logic
            allowed = {i: set() for i in range(6)}
            S_list = list(S)
            for i in range(6):
                si = S_list[i]
                others = [S_list[j] for j in range(6) if j != i]
                for v in range(n):
                    if v in S_set:
                        continue
                    # in meet graph, partner must be non-adjacent to s_i (skew) and adjacent to all other s_j
                    if adj_meet[si, v]:
                        continue
                    if all(adj_meet[sj, v] for sj in others):
                        allowed[i].add(v)
            if any(len(allowed[i]) == 0 for i in range(6)):
                continue
            ok, match_r = bipartite_matching(allowed, 6, n)
            if ok:
                T_list = []
                for v, u in match_r.items():
                    if u is not None:
                        T_list.append((u, v))
                T = tuple(sorted([v for (_, v) in T_list]))
                solutions.append((tuple(sorted(S)), T))
    return solutions


if __name__ == "__main__":
    sols = find_double_sixes_exhaustive()
    print("found", len(sols), "double-six pairs")
    if sols:
        print(sols[:5])
    Path("artifacts").mkdir(exist_ok=True)
    Path("artifacts/double_sixes_exhaustive.json").write_text(str(sols))
    print("Wrote artifacts/double_sixes_exhaustive.json")
