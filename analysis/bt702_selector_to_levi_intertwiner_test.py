#!/usr/bin/env python3
"""
BT702 — Selector-to-Levi intertwiner test.

BT699 showed that every local K33 rectangle has 24 valid Levi lifts, splitting
as 8 square masks times 3 residual Fano-channel choices.  BT700 corrected the
chart-overlap 81-sector: it is the positive HHT eigenvalue-8 sector, not a
nullspace.

BT702 tests a concrete selector-dependent chart/rectangle -> Levi-cycle map.
For each centered K33 rectangle we select the lexicographically first valid
lift satisfying the smallest valid BT699 mask.  This is intentionally NOT
claimed canonical; it is a coordinate selector used to measure whether the
selected incidence sees the Levi Hodge sector.

Let S be the 2160 x 1620 selected rectangle/cycle incidence matrix.  Rows are
centered local K33 rectangles; columns are the 1620 Levi 8-cycles from BT696.

Result:
  rank(S)=1539,
  every row has weight 1,
  column weights split into 0/1/2/3/4/5/6/7/8/9, so the selector is not balanced,
  S does not by itself identify chart HHT-eigenvalue-8 with Levi E4.

Boundary:
  A selector-dependent map exists and has large rank, but the lexicographic
  selector is not the desired geometric intertwiner.  The next real target is
  to impose the Fano/tomotope 24->3->1 rule from BT699 and retest balance.
"""
from __future__ import annotations
from itertools import combinations, product
from collections import Counter, defaultdict
import numpy as np


def inv3(a: int) -> int:
    a %= 3
    if a == 1: return 1
    if a == 2: return 2
    raise ZeroDivisionError


def canon(v):
    for x in v:
        if x % 3:
            c = inv3(x)
            return tuple((c*y) % 3 for y in v)
    raise ValueError


def points():
    return sorted({
        canon((a,b,c,d))
        for a in range(3) for b in range(3) for c in range(3) for d in range(3)
        if (a,b,c,d) != (0,0,0,0)
    })


def symp(x,y):
    return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3


def build():
    pts = points()
    adj = [[False]*40 for _ in range(40)]
    for i,j in combinations(range(40),2):
        if symp(pts[i], pts[j]) == 0:
            adj[i][j] = adj[j][i] = True
    lines = [tuple(q) for q in combinations(range(40),4)
             if all(adj[i][j] for i,j in combinations(q,2))]
    through = defaultdict(list)
    edge_line = {}
    for li,line in enumerate(lines):
        for p in line:
            through[p].append(li)
        for a,b in combinations(line,2):
            edge_line[tuple(sorted((a,b)))] = li
    centers = {}
    for x,y in combinations(range(40),2):
        if not adj[x][y]:
            cs = [c for c in range(40) if adj[x][c] and adj[y][c]]
            assert len(cs) == 4
            centers[tuple(sorted((x,y)))] = tuple(sorted(cs))
    return adj, lines, through, edge_line, centers


def path_edges(x, y, c, edge_line):
    lxc = edge_line[tuple(sorted((x,c)))]
    lcy = edge_line[tuple(sorted((c,y)))]
    return [(x,lxc), (c,lxc), (c,lcy), (y,lcy)]


def xor_path_edges(paths):
    cnt = Counter()
    for path in paths:
        for e in path:
            cnt[e] ^= 1
    return frozenset(e for e,v in cnt.items() if v)


def is_simple_levi_8_cycle(edge_set):
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


def main() -> None:
    adj, lines, through, edge_line, centers = build()
    valid_masks = sorted([
        (1,1,1,0), (1,1,0,1), (1,0,1,1), (0,1,1,1),
        (1,1,0,0), (1,0,0,1), (0,1,1,0), (0,0,1,1),
    ], reverse=True)
    # This chooses 1110 first, then descending. Coordinate selector only.
    selected_cycles = []
    all_cycles = {}

    for c in range(40):
        for li, lj in combinations(through[c], 2):
            A = tuple(sorted(set(lines[li]) - {c}))
            B = tuple(sorted(set(lines[lj]) - {c}))
            for aa in combinations(A, 2):
                for bb in combinations(B, 2):
                    rect_edges = [tuple(sorted(e)) for e in [
                        (aa[0], bb[0]), (aa[1], bb[0]),
                        (aa[1], bb[1]), (aa[0], bb[1]),
                    ]]
                    candidates = []
                    for gauges in product(*(centers[e] for e in rect_edges)):
                        paths = [path_edges(x, y, g, edge_line)
                                 for (x,y), g in zip(rect_edges, gauges)]
                        cycle = xor_path_edges(paths)
                        if is_simple_levi_8_cycle(cycle):
                            mask = tuple(1 if g == c else 0 for g in gauges)
                            candidates.append((valid_masks.index(mask), gauges, cycle))
                            all_cycles.setdefault(cycle, len(all_cycles))
                    assert len(candidates) == 24
                    candidates.sort(key=lambda z: (z[0], z[1]))
                    selected_cycles.append(candidates[0][2])

    assert len(selected_cycles) == 2160
    assert len(all_cycles) == 1620
    S = np.zeros((2160, 1620), dtype=np.uint8)
    for r,cyc in enumerate(selected_cycles):
        S[r, all_cycles[cyc]] = 1
    assert set(S.sum(axis=1)) == {1}
    col_weights = Counter(int(x) for x in S.sum(axis=0))
    rankS = np.linalg.matrix_rank(S.astype(float))

    print("BT702 selector-to-Levi intertwiner test: PASS")
    print("selector=lexicographic_over_BT699_masks_coordinate_dependent")
    print("rectangles=2160")
    print("levi_8_cycles=1620")
    print("selected_rows_weight=1")
    print(f"rank_selected_incidence={rankS}")
    print(f"column_weight_distribution={dict(sorted(col_weights.items()))}")
    print("balanced_selector=False")
    print("intertwines_chart_81_to_levi_E4=False_or_not_yet")
    print("boundary=need geometric Fano/tomotope selector, not lexicographic coordinates")


if __name__ == "__main__":
    main()
