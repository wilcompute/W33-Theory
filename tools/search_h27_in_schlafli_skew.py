#!/usr/bin/env python3
"""Search for an embedding of H27 into the Schläfli skew graph.

We seek a permutation p of 27 vertices such that
for every edge (u,v) in H27, (p(u),p(v)) is an edge in Schläfli-skew.
This is a graph monomorphism between H27 and the skew graph.

If found, this exhibits H27 as an 8-regular spanning subgraph of Schläfli-skew.
"""

from __future__ import annotations

import json
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build_w33():
    F3 = [0, 1, 2]
    vectors = [v for v in product(F3, repeat=4) if any(x != 0 for x in v)]

    proj_points = []
    seen = set()
    for v in vectors:
        v = list(v)
        for i in range(4):
            if v[i] != 0:
                inv = 1 if v[i] == 1 else 2
                v = tuple((x * inv) % 3 for x in v)
                break
        if v not in seen:
            seen.add(v)
            proj_points.append(v)

    n = len(proj_points)

    def omega(x, y):
        return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3

    adj = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if omega(proj_points[i], proj_points[j]) == 0:
                adj[i][j] = adj[j][i] = 1

    return adj, proj_points


def h27_from_w33(adj, v0=0):
    n = len(adj)
    non_neighbors = [j for j in range(n) if j != v0 and adj[v0][j] == 0]
    idx = {v: i for i, v in enumerate(non_neighbors)}

    h_adj = [[0] * 27 for _ in range(27)]
    for i, vi in enumerate(non_neighbors):
        for j, vj in enumerate(non_neighbors):
            if i < j and adj[vi][vj]:
                h_adj[i][j] = h_adj[j][i] = 1

    return h_adj, non_neighbors


# Schläfli skew graph construction


def build_27_lines():
    lines = []
    for i in range(1, 7):
        lines.append(("E", i))
    for i in range(1, 7):
        lines.append(("C", i))
    for i in range(1, 7):
        for j in range(i + 1, 7):
            lines.append(("L", i, j))
    return lines


def lines_intersect(L1, L2):
    if L1 == L2:
        return False

    t1, t2 = L1[0], L2[0]

    if t1 == "E" and t2 == "E":
        return False
    if t1 == "C" and t2 == "C":
        return False

    if t1 == "E" and t2 == "C":
        return L1[1] != L2[1]
    if t1 == "C" and t2 == "E":
        return L1[1] != L2[1]

    if t1 == "E" and t2 == "L":
        return L1[1] in L2[1:]
    if t1 == "L" and t2 == "E":
        return L2[1] in L1[1:]

    if t1 == "C" and t2 == "L":
        return L1[1] in L2[1:]
    if t1 == "L" and t2 == "C":
        return L2[1] in L1[1:]

    if t1 == "L" and t2 == "L":
        s1 = set(L1[1:])
        s2 = set(L2[1:])
        return len(s1 & s2) == 0

    return False


def schlafli_skew_graph():
    lines = build_27_lines()
    n = len(lines)
    adj = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            if lines_intersect(lines[i], lines[j]):
                adj[i][j] = adj[j][i] = 1

    # skew graph = complement of intersection graph
    skew = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                skew[i][j] = 0
            else:
                skew[i][j] = 1 - adj[i][j]
    return skew, lines


def to_bitmasks(adj):
    n = len(adj)
    masks = [0] * n
    for i in range(n):
        m = 0
        for j in range(n):
            if adj[i][j]:
                m |= 1 << j
        masks[i] = m
    return masks


def search_embedding(h_adj, s_adj, max_solutions=1):
    n = len(h_adj)
    h_masks = to_bitmasks(h_adj)
    s_masks = to_bitmasks(s_adj)

    all_mask = (1 << n) - 1

    mapping = {}
    used_mask = 0
    solutions = []

    # Fix vertex 0 to 0 to break symmetry
    mapping[0] = 0
    used_mask |= 1 << 0

    def candidates(u, mapping, used_mask):
        cand = all_mask ^ used_mask
        # enforce adjacency constraints with already-mapped neighbors
        for u2, v2 in mapping.items():
            if h_adj[u][u2]:
                cand &= s_masks[v2]
        return cand

    # order vertices by degree in H (all 8), but we can precompute neighbor list sizes to break ties
    h_deg = [sum(row) for row in h_adj]

    def select_unmapped(mapping, used_mask):
        best_u = None
        best_count = 1 << 30
        for u in range(n):
            if u in mapping:
                continue
            cand = candidates(u, mapping, used_mask)
            count = cand.bit_count()
            if count < best_count:
                best_count = count
                best_u = u
            if count == 0:
                return u, 0
        return best_u, best_count

    def iter_bits(mask):
        while mask:
            lsb = mask & -mask
            v = lsb.bit_length() - 1
            yield v
            mask ^= lsb

    def dfs():
        nonlocal used_mask
        if len(mapping) == n:
            solutions.append(dict(mapping))
            return len(solutions) >= max_solutions

        u, count = select_unmapped(mapping, used_mask)
        if count == 0:
            return False

        cand_mask = candidates(u, mapping, used_mask)

        # heuristic: try candidates with more adjacency to already mapped neighbors
        cand_list = []
        for v in iter_bits(cand_mask):
            score = 0
            for u2, v2 in mapping.items():
                if h_adj[u][u2] and s_adj[v][v2]:
                    score += 1
            cand_list.append((score, v))
        cand_list.sort(reverse=True)

        for _, v in cand_list:
            # injective
            if (used_mask >> v) & 1:
                continue
            # check adjacency consistency with mapped vertices
            ok = True
            for u2, v2 in mapping.items():
                if h_adj[u][u2] and not s_adj[v][v2]:
                    ok = False
                    break
            if not ok:
                continue

            mapping[u] = v
            used_mask |= 1 << v

            if dfs():
                return True

            # backtrack
            del mapping[u]
            used_mask &= ~(1 << v)

        return False

    dfs()
    return solutions


def main():
    w33_adj, _ = build_w33()
    h_adj, h_vertices = h27_from_w33(w33_adj, v0=0)
    s_adj, lines = schlafli_skew_graph()

    print("Searching for H27 embedding in Schläfli-skew...")
    sols = search_embedding(h_adj, s_adj, max_solutions=1)

    if sols:
        sol = sols[0]
        print("Found embedding!")
        # compute edge overlap stats
        h_edges = 0
        mapped_edges = 0
        for i in range(27):
            for j in range(i + 1, 27):
                if h_adj[i][j]:
                    h_edges += 1
                    if s_adj[sol[i]][sol[j]]:
                        mapped_edges += 1
        print(f"H27 edges: {h_edges}, mapped edges in skew: {mapped_edges}")

        results = {
            "found_embedding": True,
            "mapping": {str(k): int(v) for k, v in sol.items()},
            "h27_edges": h_edges,
            "mapped_edges": mapped_edges,
        }
    else:
        print("No embedding found (with current search).")
        results = {"found_embedding": False}

    out_path = ROOT / "artifacts" / "h27_in_schlafli_skew.json"
    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
