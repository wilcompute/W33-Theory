#!/usr/bin/env python3
"""
BT700 — Chart-overlap idempotent extraction, corrected.

BT697 built the 240-vertex graph Gamma_K on local K33 charts, with adjacency
when two charts share one W33 nonedge.  Its spectrum contains (-1)^81.
BT700 identifies the exact incidence mechanism behind that 81-sector.

Let H be the 240 x 540 chart/nonedge incidence matrix:
    H[C,e] = 1 iff local chart C contains nonedge e.

Then:
    H H^T = 9 I + A_Gamma.

Corrected interpretation:
  The (-1)-eigenspace of A_Gamma is the 8-eigenspace of H H^T, not the
  zero-eigenspace.  The zero eigenspace of H H^T has dimension 35, coming from
  the (-9)-eigenspace of A_Gamma.  Thus the 81-dimensional chart sector is a
  real positive-energy incidence sector, not a left-nullspace.

Result:
    rank(H)=205,
    dim ker(H^T)=240-205=35,
    spec(HH^T)=36^1, 18^24, 12^75, 8^81, 6^24, 0^35.

Boundary:
    This is a real 81-sector in the local K33 chart-overlap layer. It is not
    automatically the Levi Hodge idempotent E4; a lift selector/intertwiner is
    required to compare it with the 160-flag Levi sector.
"""
from __future__ import annotations
from itertools import combinations
from collections import defaultdict, Counter
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


def build_charts_and_nonedges():
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
    nonedges = [tuple(sorted((i,j))) for i,j in combinations(range(40),2) if not adj[i][j]]
    nonedge_index = {e:i for i,e in enumerate(nonedges)}
    charts = []
    for p in range(40):
        for li, lj in combinations(through[p], 2):
            A = tuple(sorted(set(lines[li]) - {p}))
            B = tuple(sorted(set(lines[lj]) - {p}))
            charts.append(frozenset(tuple(sorted((x,y))) for x in A for y in B))
    assert len(charts) == 240
    assert len(set(charts)) == 240
    assert len(nonedges) == 540
    return charts, nonedges, nonedge_index


def main() -> None:
    charts, nonedges, nonedge_index = build_charts_and_nonedges()
    H = np.zeros((len(charts), len(nonedges)), dtype=int)
    for i,ch in enumerate(charts):
        for e in ch:
            H[i, nonedge_index[e]] = 1
    assert set(H.sum(axis=1)) == {9}
    assert set(H.sum(axis=0)) == {4}

    G = H @ H.T
    A = G - 9*np.eye(240, dtype=int)
    assert set(A.diagonal()) == {0}
    assert set(A.sum(axis=1)) == {27}
    assert int(A.sum()//2) == 3240
    assert set(A[np.triu_indices(240,1)]) <= {0,1}

    rankH = np.linalg.matrix_rank(H)
    assert rankH == 205
    assert 240-rankH == 35

    eval_A = Counter(round(float(x), 8) for x in np.linalg.eigvalsh(A))
    expected_A = Counter({27.0:1, 9.0:24, 3.0:75, -1.0:81, -3.0:24, -9.0:35})
    assert eval_A == expected_A

    eval_G = Counter(round(float(x), 8) for x in np.linalg.eigvalsh(G))
    expected_G = Counter({36.0:1, 18.0:24, 12.0:75, 8.0:81, 6.0:24, 0.0:35})
    assert eval_G == expected_G

    print("BT700 chart-overlap idempotent extraction, corrected: PASS")
    print("charts=240")
    print("nonedges=540")
    print("row_weight=9")
    print("column_weight=4")
    print("identity=HHT=9I+A_Gamma")
    print("rank_H=205")
    print("left_nullity=35")
    print("chart_81_sector=A_Gamma eigenvalue -1 = HHT eigenvalue 8")
    print("chart_spectrum_A=27^1,9^24,3^75,-1^81,-3^24,-9^35")
    print("chart_incidence_spectrum_HHT=36^1,18^24,12^75,8^81,6^24,0^35")
    print("boundary=chart 81-sector is not automatically Levi E4 without a lift selector")


if __name__ == "__main__":
    main()
