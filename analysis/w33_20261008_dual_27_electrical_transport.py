#!/usr/bin/env python3
"""Exact electrical transport separating the two cospectral W33 27-state carriers.

Complements the pre-existing 2026-09-24 point/line cospectral firewall.
All matrix checks use integer arithmetic; resistances use fractions.Fraction.
No numerical eigensolver or floating point enters the certificate.
"""
from __future__ import annotations
import itertools
import json
from collections import Counter, deque
from fractions import Fraction
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "w33_20261008_dual_27_electrical_transport.json"
I27 = np.eye(27, dtype=np.int64)
J27 = np.ones((27, 27), dtype=np.int64)


def normalize(v):
    a = next(x for x in v if x)
    return tuple(x * (1 if a == 1 else 2) % 3 for x in v)


def pairing(x, y):
    return (x[0]*y[2] + x[1]*y[3] - x[2]*y[0] - x[3]*y[1]) % 3


def build_graphs():
    points = sorted({normalize(v) for v in itertools.product(range(3), repeat=4) if any(v)})
    assert len(points) == 40
    anchor = points[0]
    far = [p for p in points if p != anchor and pairing(anchor, p) != 0]
    sym = list(itertools.product(range(3), repeat=3))
    assert len(far) == len(sym) == 27
    point = np.zeros((27,27), dtype=np.int64)
    history = np.zeros_like(point)
    for i in range(27):
        for j in range(i+1,27):
            point[i,j] = point[j,i] = (pairing(far[i],far[j]) == 0)
            d = tuple((sym[i][k]-sym[j][k]) % 3 for k in range(3))
            history[i,j] = history[j,i] = ((d[0]*d[2]-d[1]*d[1]) % 3 == 0)
    return {"point_far_H27":point, "line_transverse_null":history}


def bfs_distances(a, start):
    dist = {start:0}
    todo = deque([start])
    while todo:
        u = todo.popleft()
        for v in range(27):
            if a[u,v] and v not in dist:
                dist[v] = dist[u]+1
                todo.append(v)
    assert len(dist) == 27
    return dist


def audit(a):
    assert a.shape == (27,27) and np.array_equal(a,a.T)
    assert np.array_equal(np.diag(a),np.zeros(27,dtype=np.int64))
    assert np.array_equal(a.sum(axis=1),8*np.ones(27,dtype=np.int64))
    assert int(a.sum()//2) == 108
    a2,a3 = a@a, a@a@a
    assert [int(np.trace(x)) for x in (a,a2,a3)] == [0,216,216]
    assert np.array_equal((a-8*I27)@(a-2*I27)@(a+I27)@(a+4*I27),np.zeros_like(a))
    # Eigenvalues 8^1,2^12,(-1)^8,(-4)^6 follow from the
    # simple-root annihilator together with the first four trace moments.
    L = 8*I27-a
    Q = 13*(L@L@L) - 315*(L@L) + 2070*L
    # L^+ = Q / 23328 is the exact Moore-Penrose inverse:
    # its four spectral values are 0, 1/6, 1/9, 1/12.
    assert np.array_equal(L@Q,23328*I27-864*J27)
    assert np.array_equal(Q@L,23328*I27-864*J27)
    assert np.array_equal(Q.sum(axis=0),np.zeros(27,dtype=np.int64))
    assert set(int(x) for x in Q.diagonal()) == {2928}
    pairs = Counter()
    resistance = Counter()
    distances = Counter()
    for i in range(27):
        di = bfs_distances(a,i)
        for j in range(i+1,27):
            d = di[j]
            r = Fraction(int(Q[i,i]+Q[j,j]-2*Q[i,j]),23328)
            pairs[(d,str(r))] += 1
            resistance[str(r)] += 1
            distances[d] += 1
    kirchhoff = sum(Fraction(k)*n for k,n in resistance.items())
    assert kirchhoff == Fraction(183,2)
    return {
        "vertices":27, "edges":108, "triangles":36,
        "spectrum":{"8":1,"2":12,"-1":8,"-4":6},
        "distance_histogram":{str(k):v for k,v in sorted(distances.items())},
        "distance_resistance_pairs":{f"{d}|{r}":n for (d,r),n in sorted(pairs.items())},
        "resistance_histogram":dict(sorted(resistance.items())),
        "kirchhoff_index":str(kirchhoff),
        "laplacian_pseudoinverse_polynomial":"L*(13*L^2-315*L+2070)/23328",
        "pseudoinverse_diagonal":"61/486",
    }


def compute():
    records = {name:audit(a) for name,a in build_graphs().items()}
    point=records["point_far_H27"]
    line=records["line_transverse_null"]
    assert point["distance_resistance_pairs"] == {
        "1|13/54":108, "2|29/108":216, "3|5/18":27
    }
    assert line["distance_resistance_pairs"] == {
        "1|13/54":108, "2|22/81":162, "2|43/162":81
    }
    assert point["spectrum"] == line["spectrum"]
    assert point["kirchhoff_index"] == line["kirchhoff_index"] == "183/2"
    return {
        "status":"PASS_EXACT_POINT_LINE_ELECTRICAL_TRANSPORT_DEFECT",
        "prior_art":"analysis/w33_20260924_history_pointline_cospectral_firewall.py",
        "claim":"Cospectral nonisomorphic 27-state pair has equal global resistance but unequal exact pairwise resistance and distance-resistance profiles.",
        "graphs":records,
        "boundaries":["Existing repo already establishes cospectrality and nonisomorphism.",
                      "Unit-edge electrical networks are mathematical probes, not calibrated physical propagation or spacetime."],
    }


def main():
    payload=compute()
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(payload,indent=2,sort_keys=True))


if __name__ == "__main__":
    main()
