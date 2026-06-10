#!/usr/bin/env python3
"""
BT697 — Chart-intersection graph theorem.

Build the graph Gamma_K on the 240 corrected local K33 charts from BT693.
Two chart vertices are adjacent iff the corresponding 9-nonedge sets share
one W33 nonedge.

Result:
  * 240 vertices
  * 27-regular
  * 3240 edges
  * not strongly regular: nonadjacent common-neighbor counts are 0,4,6
  * adjacent common-neighbor count is always 2
  * diameter 4 with shell profile 1,27,144,67,1
  * adjacency spectrum:
       27^1, 9^24, 3^75, (-1)^81, (-3)^24, (-9)^35

This is the exact chart-overlap geometry behind the 240 local K33 charts.
"""
from __future__ import annotations
from itertools import combinations
from collections import defaultdict, Counter, deque
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


def build_charts():
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
    charts = []
    for p in range(40):
        for li, lj in combinations(through[p], 2):
            A = tuple(sorted(set(lines[li]) - {p}))
            B = tuple(sorted(set(lines[lj]) - {p}))
            charts.append(frozenset(tuple(sorted((x,y))) for x in A for y in B))
    assert len(charts) == 240
    assert len(set(charts)) == 240
    return charts


def bfs(A, s):
    n = len(A)
    dist = [-1]*n
    dist[s] = 0
    q = deque([s])
    while q:
        u = q.popleft()
        for v in np.nonzero(A[u])[0]:
            if dist[v] < 0:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


def main() -> None:
    charts = build_charts()
    n = len(charts)
    A = np.zeros((n,n), dtype=int)
    for i,j in combinations(range(n),2):
        if charts[i] & charts[j]:
            A[i,j] = A[j,i] = 1

    degrees = A.sum(axis=1)
    assert set(degrees) == {27}
    assert int(A.sum()//2) == 3240

    adj_common = Counter()
    non_common = Counter()
    for i,j in combinations(range(n),2):
        cn = int(A[i] @ A[j])
        if A[i,j]:
            adj_common[cn] += 1
        else:
            non_common[cn] += 1
    assert adj_common == Counter({2:3240})
    assert non_common == Counter({4:12960, 0:8160, 6:4320})

    shell_profiles = Counter()
    diam = 0
    for i in range(n):
        d = bfs(A, i)
        diam = max(diam, max(d))
        shell_profiles[tuple(Counter(d).get(k,0) for k in range(max(d)+1))] += 1
    assert diam == 4
    assert shell_profiles == Counter({(1,27,144,67,1):240})

    vals = np.linalg.eigvalsh(A)
    spec = Counter(round(float(x), 8) for x in vals)
    expected = Counter({27.0:1, 9.0:24, 3.0:75, -1.0:81, -3.0:24, -9.0:35})
    assert spec == expected, spec

    print("BT697 chart-intersection graph theorem: PASS")
    print("vertices=240")
    print("degree=27")
    print("edges=3240")
    print("adjacent_common_neighbors=2")
    print("nonadjacent_common_neighbors={0:8160,4:12960,6:4320}")
    print("strongly_regular=False")
    print("diameter=4")
    print("shell_profile=1,27,144,67,1")
    print("spectrum=27^1,9^24,3^75,-1^81,-3^24,-9^35")


if __name__ == "__main__":
    main()
