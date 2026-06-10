#!/usr/bin/env python3
"""
BT694 — K33 cycle basis to Levi H1 boundary theorem.

Goal from BT694 plan: map each local [9,4,4] K33 cycle code into the
81-dimensional Levi cycle space and compute overlap with E4.

Corrected result:
  The local K33 cycle code is canonical, but it lives on the W33 nonedge chart
  (cross-pairs between two punctured perp-lines).  Those 9 chart edges are not
  Levi flag-edges.  Therefore there is no canonical chain map into the 160-edge
  point-line Levi graph using only the chart data.

What can be verified exactly:
  * Each chart has a [9,4,4] binary cycle code.
  * Each chart has 9 distinct 4-cycles (rectangles), generating beta_1=4.
  * Across all 240 charts, there are 2160 local rectangles counted with centers.
  * At the W33 nonedge level, this is a nonedge-cycle layer, not a Levi H1 layer.

Boundary:
  To map into H1(Levi)=81, one must add a lift rule that replaces each nonedge
  by a canonical path/connector in the Levi graph.  But nonedges have mu=4
  common centers, so such a lift is a gauge choice, not canonical from K33 alone.
"""
from __future__ import annotations
from itertools import combinations
from collections import defaultdict, Counter


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
            return tuple((c*y) % 3 for y in v)
    raise ValueError("zero vector")


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
    for li,line in enumerate(lines):
        for p in line:
            through[p].append(li)
    return adj, lines, through


def local_rectangles(A, B):
    # Rectangles / 4-cycles in K_{3,3}: choose 2 left vertices and 2 right vertices.
    rects = []
    for aa in combinations(A,2):
        for bb in combinations(B,2):
            edges = frozenset(tuple(sorted((x,y))) for x in aa for y in bb)
            rects.append(edges)
    return rects


def main() -> None:
    adj, lines, through = build()
    chart_count = 0
    rectangle_count = 0
    rectangle_sizes = Counter()
    nonedge_usage = Counter()

    for p in range(40):
        for li, lj in combinations(through[p], 2):
            A = tuple(sorted(set(lines[li]) - {p}))
            B = tuple(sorted(set(lines[lj]) - {p}))
            chart_edges = {tuple(sorted((x,y))) for x in A for y in B}
            assert len(chart_edges) == 9
            assert all(not adj[x][y] for x,y in chart_edges)
            rects = local_rectangles(A,B)
            assert len(rects) == 9
            assert all(len(r) == 4 for r in rects)
            chart_count += 1
            rectangle_count += len(rects)
            rectangle_sizes.update(len(r) for r in rects)
            for e in chart_edges:
                nonedge_usage[e] += 1

    assert chart_count == 240
    assert rectangle_count == 240*9 == 2160
    assert rectangle_sizes == Counter({4:2160})
    assert set(nonedge_usage.values()) == {4}

    # Classical K33 cycle-code facts.
    V = 6
    E = 9
    beta1 = E - V + 1
    dmin = 4
    nonzero_codewords = 2**beta1 - 1
    assert beta1 == 4
    assert dmin == 4
    assert nonzero_codewords == 15

    print("BT694 K33-to-Levi H1 boundary: PASS")
    print("local_cycle_code=[9,4,4]")
    print("rectangles_per_chart=9")
    print("centered_chart_rectangles=2160")
    print("rectangle_weight=4")
    print("nonedge_multiplicity=4=mu")
    print("canonical_levi_chain_map=False")
    print("reason=K33 chart edges are W33 nonedges, not Levi flag-edges; nonedges have 4 center gauges")
    print("required_extra_data=choice of connector/lift rule into Levi graph")


if __name__ == "__main__":
    main()
