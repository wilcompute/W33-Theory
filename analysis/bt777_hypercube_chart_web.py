#!/usr/bin/env python3
"""
BT777 - The hypercube chart layer of W(3,3) and the 540-cube web.

Holonet context (papers/dahn_asi_toe/witting_holonet.md, idea 9): hypercube
networks should be absorbed as local transport charts inside the Witting
fabric.  BT773-BT776 supply the exact mathematics: W(3,3) natively contains
540 copies of the 3-hypercube Q3 - one per skew line pair (l, l'), vertices
= the 8 points, edges = non-collinear cross-pairs, antipode = the unique
collinear cross partner.  BT777 builds the full chart layer and the
inter-chart fabric:

  T1. Transversal structure: every skew pair has exactly 4 common
      transversals (GQ axiom); count their pairwise disjointness - each
      disjoint transversal pair is the AXIS OF ANOTHER CUBE (BT776), so
      this is the cube-web out-degree.
  T2. The cube web: graph on the 540 skew pairs, t ~ t' iff axis(t') is a
      disjoint pair of transversals of t.  Symmetry, regularity,
      connectivity, diameter, full spectrum, SRG test.
  T3. Hypercube addressing: each cube is K_{4,4} minus the collinear
      perfect matching (crown graph) = Q3; construct an explicit F2^3
      Gray-code addressing per cube (XOR routing = e-cube routing valid);
      the 12 edges split into 3 dimension matchings.
  T4. Holonet counts: cubes through a point = 4 x 27 = 108 (gauge lines x
      skew partners); chart-slots 540 x 8 = 4320 = 108 x 40;每 cube edge
      anchored by mu = 4 lifts (BT776).
"""
from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations
import json

import numpy as np
import networkx as nx


def inv3(a):
    a %= 3
    if a in (1, 2):
        return a
    raise ZeroDivisionError


def canon(v):
    for x in v:
        if x % 3:
            c = inv3(x)
            return tuple((c * y) % 3 for y in v)
    raise ValueError


def points():
    return sorted({
        canon((a, b, c, d))
        for a in range(3) for b in range(3) for c in range(3) for d in range(3)
        if (a, b, c, d) != (0, 0, 0, 0)
    })


def symp(x, y):
    return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3


def main():
    pts = points()
    n = 40
    adj = [[False]*n for _ in range(n)]
    for i, j in combinations(range(n), 2):
        if symp(pts[i], pts[j]) == 0:
            adj[i][j] = adj[j][i] = True
    lines = [frozenset(q) for q in combinations(range(n), 4)
             if all(adj[i][j] for i, j in combinations(q, 2))]
    assert len(lines) == 40
    line_sets = [set(l) for l in lines]

    # skew pairs
    skew = []
    for i, j in combinations(range(40), 2):
        if not (line_sets[i] & line_sets[j]):
            # skew iff disjoint AND no point of one collinear-line... in a GQ
            # two lines either meet or are disjoint; disjoint = skew here?
            # GQ lines: disjoint lines are "non-concurrent". Use disjoint.
            skew.append((i, j))
    print(f"T1 disjoint (skew) line pairs: {len(skew)} (expect 540)")
    assert len(skew) == 540
    skew_index = {frozenset(p): k for k, p in enumerate(skew)}

    # transversals of a skew pair: lines meeting both
    def transversals(i, j):
        return [k for k in range(40)
                if k != i and k != j
                and line_sets[k] & line_sets[i]
                and line_sets[k] & line_sets[j]]

    tcounts = Counter()
    web_edges = set()
    disjoint_pair_counts = Counter()
    for (i, j) in skew:
        tv = transversals(i, j)
        tcounts[len(tv)] += 1
        dis = 0
        for a, b in combinations(tv, 2):
            if not (line_sets[a] & line_sets[b]):
                dis += 1
                other = frozenset((a, b))
                if other in skew_index:
                    web_edges.add(frozenset((skew_index[frozenset((i, j))],
                                             skew_index[other])))
        disjoint_pair_counts[dis] += 1
    print(f"T1 transversal counts per skew pair: {dict(tcounts)}")
    print(f"T1 disjoint transversal-pairs per skew pair: "
          f"{dict(disjoint_pair_counts)}")

    # T2: the cube web
    W = nx.Graph()
    W.add_nodes_from(range(540))
    for e in web_edges:
        a, b = tuple(e)
        W.add_edge(a, b)
    degs = Counter(dict(W.degree()).values())
    print(f"T2 cube web: 540 nodes, {W.number_of_edges()} edges, "
          f"degrees {dict(degs)}")
    conn = nx.is_connected(W)
    diam = nx.diameter(W) if conn else None
    print(f"T2 connected: {conn}, diameter: {diam}")
    A = nx.to_numpy_array(W)
    ev = np.linalg.eigvalsh(A)
    spec = Counter(round(float(x), 6) for x in ev)
    print(f"T2 spectrum: {dict(sorted(spec.items(), reverse=True))}")
    # SRG test
    k0 = next(iter(degs))
    is_reg = len(degs) == 1
    srg = None
    if is_reg:
        A2 = A @ A
        lam = set()
        mu = set()
        for x in range(540):
            for y in range(x+1, 540):
                if A[x, y]:
                    lam.add(int(A2[x, y]))
                else:
                    mu.add(int(A2[x, y]))
        if len(lam) == 1 and len(mu) == 1:
            srg = (540, k0, lam.pop(), mu.pop())
    print(f"T2 SRG parameters: {srg}")

    # T3: hypercube addressing of one cube chart
    i, j = skew[0]
    L1 = sorted(line_sets[i])
    L2 = sorted(line_sets[j])
    cube = nx.Graph()
    cube.add_nodes_from(L1 + L2)
    antipode = {}
    for a in L1:
        for b in L2:
            if adj[a][b]:
                antipode[a] = b
                antipode[b] = a
            else:
                cube.add_edge(a, b)
    assert nx.is_isomorphic(cube, nx.cubical_graph())
    # F2^3 addressing via explicit isomorphism onto the 3-hypercube
    H3 = nx.hypercube_graph(3)   # nodes are F2^3 tuples
    gm = nx.algorithms.isomorphism.GraphMatcher(cube, H3)
    assert gm.is_isomorphic()
    addr = dict(gm.mapping)
    ok_addr = (len(addr) == 8 and
               all(sum(x ^ y for x, y in zip(addr[u], addr[v])) == 1
                   for u, v in cube.edges()))
    anti_ok = all(tuple(1 - x for x in addr[v]) == addr[antipode[v]]
                  for v in addr)
    print(f"T3 F2^3 Gray addressing valid (edges = unit XOR): {ok_addr}")
    print(f"T3 antipode = bitwise complement = collinear partner: {anti_ok}")
    dims = Counter()
    for u, v in cube.edges():
        d = [k for k in range(3) if addr[u][k] != addr[v][k]][0]
        dims[d] += 1
    print(f"T3 dimension matchings: {dict(dims)} (3 x 4 edges)")

    # T4: holonet counts
    cubes_through_pt = Counter()
    for (i2, j2) in skew:
        for p in line_sets[i2] | line_sets[j2]:
            cubes_through_pt[p] += 1
    cset = set(cubes_through_pt.values())
    print(f"T4 cubes through each point: {cset} (expect {{108 = 4 x 27}})")
    print(f"T4 chart slots 540 x 8 = {540*8} = 108 x 40 = {108*40}")

    out = {
        "theorem": "BT777 hypercube chart layer + cube web",
        "skew_pairs": len(skew),
        "transversals_per_pair": dict(tcounts),
        "disjoint_transversal_pairs": dict(disjoint_pair_counts),
        "web_edges": W.number_of_edges(),
        "web_degrees": {str(k): v for k, v in degs.items()},
        "web_connected": bool(conn),
        "web_diameter": diam,
        "web_spectrum": {str(k): v for k, v in sorted(spec.items(),
                                                      reverse=True)},
        "web_srg": srg,
        "gray_addressing_valid": bool(ok_addr),
        "antipode_is_complement": bool(anti_ok),
        "cubes_through_point": sorted(cset),
    }
    with open("data/bt777_hypercube_chart_web.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote data/bt777_hypercube_chart_web.json")


if __name__ == "__main__":
    main()
