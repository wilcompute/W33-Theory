#!/usr/bin/env python3
"""
BT693 — Unique local K33 chart enumerator.

Continuation of BT690.

We enumerate every corrected local K_{3,3} chart in W(3,3):
  center point P + unordered pair of the four GQ lines through P.

Each chart contributes 9 W33 nonedges, one for every cross-pair between the
chosen two punctured lines.

Result:
  * 40 centers
  * C(4,2)=6 charts per center
  * 240 centered charts
  * all 240 chart edge-sets are distinct
  * W33 has 540 nonedges
  * each nonedge lies in exactly 4 centered charts (= mu)
  * two distinct charts intersect in either 0 or 1 nonedge
  * each chart meets 27 other charts in exactly one nonedge and 212 in none
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
    assert len(pts) == 40
    assert len(lines) == 40
    assert all(sum(row) == 12 for row in adj)
    assert all(len(through[p]) == 4 for p in range(40))
    return adj, lines, through


def chart_edge_set(p, li, lj, lines):
    A = tuple(sorted(set(lines[li]) - {p}))
    B = tuple(sorted(set(lines[lj]) - {p}))
    return frozenset(tuple(sorted((x,y))) for x in A for y in B)


def main() -> None:
    adj, lines, through = build()
    charts = []
    for p in range(40):
        for li, lj in combinations(through[p], 2):
            charts.append((p, li, lj, chart_edge_set(p, li, lj, lines)))

    chart_sets = [c[-1] for c in charts]
    unique_sets = set(chart_sets)
    assert len(charts) == 240
    assert len(unique_sets) == 240
    assert all(len(s) == 9 for s in unique_sets)

    nonedges = {tuple(sorted((i,j))) for i,j in combinations(range(40),2) if not adj[i][j]}
    assert len(nonedges) == 540

    incidence = Counter()
    for s in chart_sets:
        for e in s:
            incidence[e] += 1
    assert set(incidence.keys()) == nonedges
    assert Counter(incidence.values()) == Counter({4: 540})

    intersections = Counter()
    for a,b in combinations(range(len(chart_sets)),2):
        intersections[len(chart_sets[a] & chart_sets[b])] += 1
    assert set(intersections.keys()) == {0,1}

    per_chart = Counter()
    for a in range(len(chart_sets)):
        per_chart.update(len(chart_sets[a] & chart_sets[b]) for b in range(len(chart_sets)) if b != a)
    normalized = {k: v // len(chart_sets) for k,v in per_chart.items()}
    assert normalized == {0: 212, 1: 27}

    print("BT693 unique local K33 chart enumerator: PASS")
    print("centered_charts=240")
    print("unique_edge_set_charts=240")
    print("w33_nonedges=540")
    print("nonedge_chart_multiplicity=4=mu")
    print("chart_intersections={0:%d,1:%d}" % (intersections[0], intersections[1]))
    print("per_chart_intersections={0:212,1:27}")
    print("identity=240*9=2160=4*540")


if __name__ == "__main__":
    main()
