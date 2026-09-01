#!/usr/bin/env python3
"""Exact W33 <-> GQ(2,4) <-> E8 chart atlas.

This composes two previously separate exact dictionaries instead of matching
counts:

  * W33-Theory: the 45 minimum weight-8 W33 supports are the selected
    orthogonal D4+D4 packets in the 240-root E8 shell; their 27 disjoint
    fivepacks are ten-D4 partitions of all 240 roots.
  * Holotrade 7eef505 (2026-09-01): those same 45 polar-pair supports are the
    induced K(4,4) octets of W(3,3), and the 27 fivepacks are K(4,4)-factors
    of all 40 W33 vertices.

The result is objectwise.  A single 27x45 incidence matrix simultaneously means

  point of GQ(2,4)  incident with  line of GQ(2,4),
  cubic line        incident with  tritangent plane,
  K(4,4)-factor     contains       K(4,4) octet,
  ten-D4 E8 chart   contains       orthogonal D4+D4 packet.

No physical interpretation is inferred from the shared finite carrier.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

import networkx as nx
import numpy as np

from w33_pass7163_7170_e8_hexagonal_lift import e8_fibers
from w33_20260901_regulus_e8_completion_bridge import minimum_supports, packet_halves
from w33_pass4992_4999_common import build_base
from w33_pass7225_7232_spread_code_doily_puncture import coordinate_isomorphism

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_W33_20260901_GQ24_K44_E8_ATLAS.json"


def rankp(A, p):
    A = np.asarray(A, dtype=np.int64).copy() % p
    m, n = A.shape
    r = 0
    for c in range(n):
        z = next((i for i in range(r, m) if A[i, c]), None)
        if z is None:
            continue
        A[[r, z]] = A[[z, r]]
        A[r] = A[r] * pow(int(A[r, c]), -1, p) % p
        for i in range(m):
            if i != r and A[i, c]:
                A[i] = (A[i] - A[i, c] * A[r]) % p
        r += 1
        if r == m:
            break
    return r


def srg_parameters(adj):
    v = len(adj)
    ks = {len(N) for N in adj}
    assert len(ks) == 1
    k = next(iter(ks))
    lam, mu = set(), set()
    for a, b in itertools.combinations(range(v), 2):
        c = len(adj[a] & adj[b])
        (lam if b in adj[a] else mu).add(c)
    assert len(lam) == len(mu) == 1
    return (v, k, next(iter(lam)), next(iter(mu)))


def main():
    roots, fibres, _phase, _radj, base_adj, _zero, _twelve, _diffhist = e8_fibers()
    assert len(roots) == 240 and len(fibres) == 40
    supports = minimum_supports(base_adj)
    assert len(supports) == 45

    # One packet, three exact meanings.  packet_halves supplies the two
    # independent four-sets whose 6-root fibres are the two 24-root D4 blocks.
    packet_d4 = []
    k44_bipartitions = []
    for S in supports:
        halves, root_halves = packet_halves(S, base_adj, fibres)
        A, B = map(set, halves)
        assert len(A) == len(B) == 4 and A.isdisjoint(B) and A | B == set(S)
        assert all(v not in base_adj[u] for H in (A, B)
                   for u, v in itertools.combinations(sorted(H), 2))
        assert all(v in base_adj[u] for u in A for v in B)
        # Hence the W33 subgraph induced by the support is literally K(4,4).
        degs = []
        for u in S:
            degs.append(len(base_adj[u] & set(S)))
        assert degs == [4] * 8
        k44_bipartitions.append((tuple(sorted(A)), tuple(sorted(B))))
        assert len(root_halves) == 2 and all(len(H) == 24 for H in root_halves)
        packet_d4.append(tuple(root_halves))
    assert len(set(k44_bipartitions)) == 45

    # Packet disjointness is the GQ(4,2) point graph.  Its maximal K5s are the
    # 27 GQ(4,2) lines / GQ(2,4) points / completion charts.
    padj = [set() for _ in range(45)]
    for a, b in itertools.combinations(range(45), 2):
        if supports[a].isdisjoint(supports[b]):
            padj[a].add(b)
            padj[b].add(a)
    assert srg_parameters(padj) == (45, 12, 3, 3)

    P = nx.Graph()
    P.add_nodes_from(range(45))
    P.add_edges_from((a, b) for a in range(45) for b in padj[a] if a < b)
    fivepacks = sorted(
        (tuple(sorted(C)) for C in nx.find_cliques(P) if len(C) == 5),
        key=lambda C: C,
    )
    assert len(fivepacks) == 27 and len(set(fivepacks)) == 27

    chart_blocks = []
    for C in fivepacks:
        octet_union = set().union(*(set(supports[p]) for p in C))
        assert len(octet_union) == 40
        assert sum(len(supports[p]) for p in C) == 40
        assert all(supports[a].isdisjoint(supports[b])
                   for a, b in itertools.combinations(C, 2))

        d4s = frozenset(H for p in C for H in packet_d4[p])
        assert len(d4s) == 10
        assert all(len(H) == 24 for H in d4s)
        assert sum(map(len, d4s)) == 240
        assert len(set().union(*d4s)) == 240
        chart_blocks.append(d4s)
    assert len(set(chart_blocks)) == 27

    # The common incidence matrix I is simultaneously the GQ(2,4), cubic,
    # K44-factor, and E8-chart incidence matrix.
    I = np.zeros((27, 45), dtype=int)
    for c, C in enumerate(fivepacks):
        I[c, list(C)] = 1
    assert set(I.sum(axis=1)) == {5}
    assert set(I.sum(axis=0)) == {3}

    cadj = [set() for _ in range(27)]
    shared = Counter()
    for a, b in itertools.combinations(range(27), 2):
        n = int(I[a] @ I[b])
        shared[n] += 1
        assert n in (0, 1)
        if n == 1:
            cadj[a].add(b)
            cadj[b].add(a)
    assert shared == Counter({0: 216, 1: 135})
    assert srg_parameters(cadj) == (27, 10, 1, 5)

    A27 = np.zeros((27, 27), dtype=int)
    for a in range(27):
        for b in cadj[a]:
            A27[a, b] = 1
    A45 = np.zeros((45, 45), dtype=int)
    for a in range(45):
        for b in padj[a]:
            A45[a, b] = 1
    assert np.array_equal(I @ I.T, 5 * np.eye(27, dtype=int) + A27)
    assert np.array_equal(I.T @ I, 3 * np.eye(45, dtype=int) + A45)

    ranks = {str(p): rankp(I, p) for p in (2, 3, 5, 7)}
    assert ranks["2"] == 21 and ranks["3"] == 21
    assert np.linalg.matrix_rank(I.astype(float)) == 21

    # Existing cubic-surface coordinate dictionary: packet supports ->
    # tritangents.  This proves that the same I is the old 27x45 R incidence
    # after explicit row/column permutations, not merely an isospectral copy.
    cubic = build_base()
    T = cubic["tritangents"]
    packet_to_tri = coordinate_isomorphism(supports, T)
    chart_to_line = []
    for C in fivepacks:
        common = set(range(27))
        for p in C:
            common &= set(T[packet_to_tri[p]])
        assert len(common) == 1
        chart_to_line.append(next(iter(common)))
    assert sorted(chart_to_line) == list(range(27))

    R = np.zeros((27, 45), dtype=int)
    for t, tri in enumerate(T):
        R[list(tri), t] = 1
    Icubic = np.zeros((27, 45), dtype=int)
    for c in range(27):
        line = chart_to_line[c]
        for p in fivepacks[c]:
            Icubic[line, packet_to_tri[p]] = 1
    assert np.array_equal(Icubic, R)

    out = {
        "schema": "w33.20260901.gq24-k44-e8-atlas.v1",
        "status": "PASS",
        "dependencies": {
            "W33": [
                "Pass7163-7170 E8 40x6 fibre/D4 dictionary",
                "2026-09-01 selected 45 D4+D4 packets and 27 ten-D4 charts",
                "2026-09-01 D4 prism packet<->tritangent/chart<->cubic-line coordinate map",
            ],
            "Holotrade": "7eef50506498051cdde24363d5e839fd0fa7c493: 27 K(4,4)-factors of W(3,3)",
        },
        "packetObjects45": {
            "count": 45,
            "w33Meaning": "induced K(4,4) octet on one weight-8 support",
            "e8Meaning": "48-root orthogonal D4+D4 packet, 24+24 roots",
            "cubicMeaning": "tritangent plane",
            "gq24Meaning": "line of GQ(2,4)",
            "eachOccursInCharts": 3,
        },
        "chartObjects27": {
            "count": 27,
            "w33Meaning": "K(4,4)-factor: five disjoint octets partition all 40 W33 vertices",
            "e8Meaning": "ten-D4 chart: the corresponding ten 24-root D4 blocks partition all 240 E8 roots",
            "cubicMeaning": "cubic-surface line coordinate",
            "gq24Meaning": "point of GQ(2,4)",
            "packetsPerChart": 5,
        },
        "commonIncidence": {
            "shape": [27, 45],
            "rowWeight": 5,
            "columnWeight": 3,
            "rankQ": 21,
            "rankMod2": ranks["2"],
            "rankMod3": ranks["3"],
            "rankMod5": ranks["5"],
            "rankMod7": ranks["7"],
            "IItranspose": "5 I_27 + A_GQ(2,4)",
            "ItransposeI": "3 I_45 + A_GQ(4,2)",
            "equalsCubicLineTritangentIncidenceAfterExplicitCoordinatePermutations": True,
        },
        "chartPointGraph": {
            "parameters": [27, 10, 1, 5],
            "sharedPacketHistogram": {str(k): v for k, v in sorted(shared.items())},
            "collinearity": "two charts/GQ(2,4) points are collinear iff they share exactly one K44/D4+D4 packet",
        },
        "theorem": (
            "One explicit 27x45 incidence atlas simultaneously realizes GQ(2,4), the cubic 27-line/45-tritangent configuration, "
            "the 27 K(4,4)-factorizations of W(3,3), and the 27 selected ten-D4 partitions of the same 240-root E8 shell. "
            "Each of its 45 line coordinates is literally one W33 K(4,4) weight-8 octet and the corresponding 48-root orthogonal D4+D4 packet."
        ),
        "boundary": (
            "The W33 octet/D4 and cubic incidence ingredients pre-existed; Holotrade 7eef505 supplied the K(4,4)-factor reading. "
            "The new result is their objectwise composition into one atlas. No physical dynamics, spacetime identification, or tau_2 improvement follows from this finite incidence theorem."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": "PASS",
        "packets": 45,
        "charts": 27,
        "K44Factors": 27,
        "E8TenD4Partitions": 27,
        "incidenceRank": ranks,
        "cubicIncidenceSame": True,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
