#!/usr/bin/env python3
"""
BT713 — Selector Sheet Rank Filter Theorem.

This continues BT696/BT699/BT705/BT708.  BT696 found that each centered
local K_{3,3} rectangle has 24 valid center-gauge presentations lifting to
Levi 8-cycles.  BT699 split the 24 presentations as 8 square-orientation
masks times 3 residual channel choices.

BT713 tests those 24 candidate one-cycle-per-rectangle selector sheets against
the actual Levi Hodge target: the signed cycle space of the W(3,3) point-line
Levi graph.  The criterion is simple and executable: the signed incidence rows
selected by a sheet must span rank 81, the first Betti number of the Levi graph.

Result:
  * 19 of 24 selector sheets span the full Levi H_1 rank 81;
  * 1 selector sheet has rank 76;
  * 4 selector sheets have rank 70;
  * at the mask level, 7 of 8 masks span rank 81 when all three residual
    channels are retained;
  * the unique mask-level defect is mask 1001, with rank 76.

Interpretation: the 24->3->1 selector architecture is not purely cosmetic.
The Levi-Hodge rank test filters out algebraically defective selector sheets.
A tomotope/Fano hinge selector must land in a rank-81 sheet (or, at minimum,
in a rank-81 mask bundle) to carry the full protected E4/H1 sector.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations, product
import json
import networkx as nx

P = 1_000_003


def inv3(a: int) -> int:
    a %= 3
    if a == 1:
        return 1
    if a == 2:
        return 2
    raise ZeroDivisionError


def canon(v):
    for x in v:
        if x % 3:
            c = inv3(x)
            return tuple((c * y) % 3 for y in v)
    raise ValueError("zero vector")


def points():
    return sorted({
        canon((a, b, c, d))
        for a in range(3) for b in range(3) for c in range(3) for d in range(3)
        if (a, b, c, d) != (0, 0, 0, 0)
    })


def symp(x, y) -> int:
    return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3


def build():
    pts = points()
    adj = [[False] * 40 for _ in range(40)]
    G = nx.Graph()
    G.add_nodes_from(range(40))
    for i, j in combinations(range(40), 2):
        if symp(pts[i], pts[j]) == 0:
            adj[i][j] = adj[j][i] = True
            G.add_edge(i, j)

    assert G.number_of_nodes() == 40
    assert G.number_of_edges() == 240
    assert set(dict(G.degree()).values()) == {12}

    lines = [tuple(q) for q in combinations(range(40), 4)
             if all(adj[i][j] for i, j in combinations(q, 2))]
    assert len(lines) == 40

    through = defaultdict(list)
    edge_line = {}
    for li, line in enumerate(lines):
        for p in line:
            through[p].append(li)
        for a, b in combinations(line, 2):
            edge_line[tuple(sorted((a, b)))] = li
    assert all(len(through[p]) == 4 for p in range(40))

    centers = {}
    for x, y in combinations(range(40), 2):
        if not adj[x][y]:
            cs = tuple(sorted(c for c in range(40) if adj[x][c] and adj[y][c]))
            assert len(cs) == 4
            centers[tuple(sorted((x, y)))] = cs

    flags = sorted((p, li) for li, line in enumerate(lines) for p in line)
    flag_index = {f: i for i, f in enumerate(flags)}
    assert len(flags) == 160

    L = nx.Graph()
    L.add_nodes_from(("p", p) for p in range(40))
    L.add_nodes_from(("l", li) for li in range(40))
    L.add_edges_from((("p", p), ("l", li)) for p, li in flags)
    assert L.number_of_nodes() == 80
    assert L.number_of_edges() == 160
    assert nx.is_connected(L)
    beta1 = L.number_of_edges() - L.number_of_nodes() + 1
    assert beta1 == 81

    return adj, lines, through, edge_line, centers, flag_index


def path_edges(x, y, c, edge_line):
    lxc = edge_line[tuple(sorted((x, c)))]
    lcy = edge_line[tuple(sorted((c, y)))]
    return [(x, lxc), (c, lxc), (c, lcy), (y, lcy)]


def xor_path_edges(paths):
    cnt = Counter()
    for path in paths:
        for e in path:
            cnt[e] ^= 1
    return frozenset(e for e, v in cnt.items() if v)


def is_simple_levi_8_cycle(edge_set) -> bool:
    if len(edge_set) != 8:
        return False
    deg = Counter()
    graph = defaultdict(list)
    for p, li in edge_set:
        a = ("p", p)
        b = ("l", li)
        deg[a] += 1
        deg[b] += 1
        graph[a].append(b)
        graph[b].append(a)
    if len(deg) != 8 or any(d != 2 for d in deg.values()):
        return False
    start = next(iter(deg))
    seen = {start}
    stack = [start]
    while stack:
        u = stack.pop()
        for v in graph[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return len(seen) == 8


def oriented_sparse_row(edge_set, flag_index):
    """Return sorted (column, sign) pairs for one oriented Levi 8-cycle."""
    graph = defaultdict(list)
    edge_for = {}
    for p, li in edge_set:
        a = ("p", p)
        b = ("l", li)
        graph[a].append(b)
        graph[b].append(a)
        edge_for[frozenset((a, b))] = (p, li)
    for u in graph:
        graph[u].sort()
    start = min(graph)
    prev = None
    cur = start
    nxt = graph[start][0]
    row = {}
    for _ in range(8):
        flag = edge_for[frozenset((cur, nxt))]
        sign = 1 if cur[0] == "p" and nxt[0] == "l" else -1
        row[flag_index[flag]] = sign
        prev, cur = cur, nxt
        if cur == start:
            break
        nxt = next(x for x in graph[cur] if x != prev)
    assert len(row) == 8
    return tuple(sorted(row.items()))


def gf_rank_sparse(rows, ncols=160, p=P) -> int:
    """Sparse Gaussian elimination over a large prime field."""
    pivots = {}
    for row in rows:
        r = {c: v % p for c, v in row if v % p}
        while r:
            c = min(r)
            if c not in pivots:
                inv = pow(r[c], p - 2, p)
                pivots[c] = {k: (v * inv) % p for k, v in r.items()}
                break
            factor = r[c]
            for k, v in pivots[c].items():
                nv = (r.get(k, 0) - factor * v) % p
                if nv:
                    r[k] = nv
                elif k in r:
                    del r[k]
    return len(pivots)


def main() -> None:
    adj, lines, through, edge_line, centers, flag_index = build()
    masks = [
        (1,1,1,0), (1,1,0,1), (1,0,1,1), (0,1,1,1),
        (1,1,0,0), (1,0,0,1), (0,1,1,0), (0,0,1,1),
    ]
    sheet_rows = {(m, r): [] for m in masks for r in range(3)}
    unique_cycles = Counter()
    rectangles = 0

    for c in range(40):
        for li, lj in combinations(through[c], 2):
            A = tuple(sorted(set(lines[li]) - {c}))
            B = tuple(sorted(set(lines[lj]) - {c}))
            for aa in combinations(A, 2):
                for bb in combinations(B, 2):
                    # Cyclic edge order inherited from BT699.
                    rect_edges = [tuple(sorted(e)) for e in [
                        (aa[0], bb[0]),
                        (aa[1], bb[0]),
                        (aa[1], bb[1]),
                        (aa[0], bb[1]),
                    ]]
                    assert all(not adj[x][y] for x, y in rect_edges)
                    per_mask = defaultdict(list)
                    for gauges in product(*(centers[e] for e in rect_edges)):
                        paths = [path_edges(x, y, g, edge_line)
                                 for (x, y), g in zip(rect_edges, gauges)]
                        cycle = xor_path_edges(paths)
                        if is_simple_levi_8_cycle(cycle):
                            mask = tuple(1 if g == c else 0 for g in gauges)
                            row = oriented_sparse_row(cycle, flag_index)
                            per_mask[mask].append((tuple(sorted(cycle)), row, cycle))
                            unique_cycles[cycle] += 1
                    assert set(per_mask) == set(masks)
                    for mask in masks:
                        vals = sorted(per_mask[mask], key=lambda t: t[0])
                        assert len(vals) == 3
                        for residual_index, (_, row, _) in enumerate(vals):
                            sheet_rows[(mask, residual_index)].append(row)
                    rectangles += 1

    assert rectangles == 2160
    assert len(unique_cycles) == 1620
    assert Counter(unique_cycles.values()) == Counter({32: 1620})

    sheet_ranks = {}
    for key, rows in sheet_rows.items():
        assert len(rows) == 2160
        sheet_ranks[key] = gf_rank_sparse(rows)

    mask_bundle_ranks = {}
    for mask in masks:
        rows = []
        for r in range(3):
            rows.extend(sheet_rows[(mask, r)])
        mask_bundle_ranks[mask] = gf_rank_sparse(rows)

    all_rows = []
    for rows in sheet_rows.values():
        all_rows.extend(rows)
    all_rank = gf_rank_sparse(all_rows)

    full_sheets = sum(1 for r in sheet_ranks.values() if r == 81)
    result = {
        "theorem": "BT713 Selector Sheet Rank Filter Theorem",
        "w33_vertices": 40,
        "w33_edges": 240,
        "levi_vertices": 80,
        "levi_flag_edges": 160,
        "levi_beta1": 81,
        "centered_k33_rectangles": rectangles,
        "valid_lifts_per_rectangle": 24,
        "unique_levi_8_cycles": len(unique_cycles),
        "cycle_presentation_multiplicity": 32,
        "selector_sheets": 24,
        "rank_distribution": dict(Counter(sheet_ranks.values())),
        "full_rank_sheets": full_sheets,
        "defective_sheets": 24 - full_sheets,
        "sheet_ranks": {"".join(map(str, m)) + f"_r{r}": rank for (m, r), rank in sheet_ranks.items()},
        "mask_bundle_ranks": {"".join(map(str, m)): rank for m, rank in mask_bundle_ranks.items()},
        "all_sheet_union_rank": all_rank,
        "interpretation": "Hodge rank filters the 24 candidate 24->3->1 selector sheets; full physical selectors must land in rank-81 sheets or rank-81 mask bundles.",
    }

    assert result["rank_distribution"] == {81: 19, 76: 1, 70: 4}
    assert result["full_rank_sheets"] == 19
    assert mask_bundle_ranks[(1,0,0,1)] == 76
    assert sum(1 for r in mask_bundle_ranks.values() if r == 81) == 7
    assert all_rank == 81

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
