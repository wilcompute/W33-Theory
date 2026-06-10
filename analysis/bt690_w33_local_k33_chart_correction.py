#!/usr/bin/env python3
"""
BT690 — W33 local K33 chart correction theorem.

This uses BT689 as a hint but repairs the first count.

BT689's useful idea: W(3,3) should locally generate K_{3,3} charts.
Correction: for a point P in W(3,3), the projective perp-set P^perp has
13 points, not 9.  It is the pencil of the four GQ lines through P:

    |P^perp| = 1 + 4*3 = 13.

The actual canonical K_{3,3} chart comes from choosing two of the four
punctured lines through P.  Each punctured line has 3 points; the cross
non-collinearity relation between two such lines is K_{3,3}.  Equivalently,
this is a virtual AG(2,3) coordinate chart

    (L_i \ {P}) x (L_j \ {P})

with 9 coordinate-pair points / K33 edges.

Strong global count:
  * 40 points P
  * C(4,2)=6 line-pairs through each P
  * 9 cross-pairs per chart
  * total centered chart incidences = 40*6*9 = 2160
  * W33 has 540 nonedges
  * every nonedge is resolved by exactly mu=4 common centers

Hence 2160 = 4*540.
"""
from __future__ import annotations

from itertools import combinations
from collections import defaultdict

MOD = 3


def inv3(a: int) -> int:
    a %= 3
    if a == 1:
        return 1
    if a == 2:
        return 2
    raise ZeroDivisionError


def canon(v):
    v = tuple(x % 3 for x in v)
    for x in v:
        if x:
            c = inv3(x)
            return tuple((c*y) % 3 for y in v)
    raise ValueError("zero vector")


def projective_points():
    pts = set()
    for a in range(3):
        for b in range(3):
            for c in range(3):
                for d in range(3):
                    if (a,b,c,d) != (0,0,0,0):
                        pts.add(canon((a,b,c,d)))
    return sorted(pts)


def symp(x, y):
    return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3


def build_graph():
    pts = projective_points()
    adj = [[False]*40 for _ in range(40)]
    for i, j in combinations(range(40), 2):
        if symp(pts[i], pts[j]) == 0:
            adj[i][j] = adj[j][i] = True
    assert len(pts) == 40
    assert all(sum(row) == 12 for row in adj)
    return pts, adj


def build_lines(adj):
    lines = []
    for quad in combinations(range(40), 4):
        if all(adj[i][j] for i, j in combinations(quad, 2)):
            lines.append(tuple(quad))
    assert len(lines) == 40
    through = defaultdict(list)
    for idx, line in enumerate(lines):
        for p in line:
            through[p].append(idx)
    assert all(len(through[p]) == 4 for p in range(40))
    return lines, through


def main() -> None:
    pts, adj = build_graph()
    lines, through = build_lines(adj)

    nonedges = {tuple(sorted((i,j))) for i,j in combinations(range(40),2) if not adj[i][j]}
    assert len(nonedges) == 540

    total_charts = 0
    total_chart_edges = 0
    nonedge_center_count = defaultdict(int)
    chart_sizes = []

    for p in range(40):
        perp = {p} | {q for q in range(40) if adj[p][q]}
        assert len(perp) == 13
        punctured_lines = []
        for li in through[p]:
            punctured = tuple(x for x in lines[li] if x != p)
            assert len(punctured) == 3
            punctured_lines.append(punctured)
        for a, b in combinations(range(4), 2):
            A = punctured_lines[a]
            B = punctured_lines[b]
            # Distinct lines through P have complete bipartite non-collinearity.
            for x in A:
                for y in B:
                    assert not adj[x][y]
                    nonedge_center_count[tuple(sorted((x,y)))] += 1
            total_charts += 1
            total_chart_edges += 9
            chart_sizes.append((len(A), len(B), len(A)*len(B)))

    assert total_charts == 40*6 == 240
    assert total_chart_edges == 40*6*9 == 2160
    assert set(nonedge_center_count.keys()) == nonedges
    assert set(nonedge_center_count.values()) == {4}
    assert total_chart_edges == 4 * len(nonedges)

    print("BT690 W33 local K33 chart correction: PASS")
    print("perp_set_size=13 not 9")
    print("lines_through_each_point=4")
    print("punctured_line_size=3")
    print("k33_charts_per_point=C(4,2)=6")
    print("centered_k33_charts=240")
    print("chart_edges_total=2160")
    print("w33_nonedges=540")
    print("each_nonedge_resolved_by_centers=4=mu")
    print("corrected_chain=W33 point -> perp pencil of 4 punctured lines -> pair of directions -> K33 virtual affine chart")


if __name__ == "__main__":
    main()
