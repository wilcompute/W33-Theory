#!/usr/bin/env python3
"""Exact cross-frontier bridge: depth-3 reguli -> uniquely completed E8 D4 spreads.

Dependencies already certified in this repository:
  * Pass7163--7170: 240 E8 roots -> 40 W33 six-root fibres; the 45
    weight-8/tritangent supports are 45 orthogonal D4+D4 packets; the 27
    GQ(4,2) lines are five-packs partitioning all 240 roots into ten D4s.
  * Holotrade commit 4952a3b3b3061af796edb86bce316c2f92475d10 independently
    proves objectwise that its 270 depth-3 all-isotropic reguli are exactly the
    270 support-disjoint pairs of those same 45 polar-pair/tritangent supports.

New theorem certified here:
  Every one of the 270 disjoint packet pairs lies in exactly one of the 27
  five-packs.  Thus every depth-3 obstruction regulus selects 96 E8 roots
  (four selected D4s, grouped as two orthogonal D4+D4 packets) and has a unique
  completion by six more selected D4s / 144 roots to a ten-D4 partition of the
  full 240-root E8 shell.

This is finite combinatorics only.  It does not claim a physical obstruction is
removed, nor does it assign dynamics to E8.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

from w33_pass7163_7170_e8_hexagonal_lift import e8_fibers, gf2_basis, dot

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_W33_20260901_REGULUS_E8_COMPLETION_BRIDGE.json"


def minimum_supports(base_adj):
    rows = [sum(1 << j for j in base_adj[i]) for i in range(40)]
    basis = gf2_basis(rows)
    assert len(basis) == 16
    words = []
    for mask in range(1 << 16):
        x = 0
        for i, b in enumerate(basis):
            if (mask >> i) & 1:
                x ^= b
        if x.bit_count() == 8:
            words.append(frozenset(i for i in range(40) if (x >> i) & 1))
    assert len(words) == 45 and len(set(words)) == 45
    return sorted(words, key=lambda s: tuple(sorted(s)))


def packet_halves(support, base_adj, fibres):
    halves = []
    for H in itertools.combinations(sorted(support), 4):
        if all(v not in base_adj[u] for u, v in itertools.combinations(H, 2)):
            halves.append(tuple(H))
    halves = sorted(set(halves))
    assert len(halves) == 2
    assert set(halves[0]).isdisjoint(halves[1])
    assert set(halves[0]) | set(halves[1]) == set(support)
    root_halves = [frozenset(u for f in H for u in fibres[f]) for H in halves]
    assert all(len(R) == 24 for R in root_halves)
    return halves, root_halves


def build_certificate():
    roots, fibres, _phase, _radj, base_adj, _zero, _twelve, _diffhist = e8_fibers()
    supports = minimum_supports(base_adj)

    intersection_hist = Counter()
    edges = set()
    for i, j in itertools.combinations(range(45), 2):
        k = len(supports[i] & supports[j])
        intersection_hist[k] += 1
        if k == 0:
            edges.add(frozenset((i, j)))
    assert intersection_hist == Counter({2: 720, 0: 270})

    nbr = [set() for _ in range(45)]
    for e in edges:
        a, b = tuple(e)
        nbr[a].add(b)
        nbr[b].add(a)
    assert {len(N) for N in nbr} == {12}

    # The 27 GQ(4,2) lines are exactly the 5-cliques in support disjointness.
    fivepacks = []
    for C in itertools.combinations(range(45), 5):
        if all(b in nbr[a] for a, b in itertools.combinations(C, 2)):
            fivepacks.append(tuple(C))
    assert len(fivepacks) == 27
    assert all(set().union(*(supports[i] for i in C)) == set(range(40)) for C in fivepacks)

    packet_data = []
    selected_d4 = set()
    for S in supports:
        halves, root_halves = packet_halves(S, base_adj, fibres)
        A, B = root_halves
        assert all(dot(roots[u], roots[v]) == 0 for u in A for v in B)
        selected_d4.update(root_halves)
        packet_data.append((halves, root_halves, A | B))
    assert len(selected_d4) == 90
    assert all(len(P[2]) == 48 for P in packet_data)

    # Every five-pack is a literal partition of the E8 root shell into ten D4s.
    for C in fivepacks:
        packets = [packet_data[i][2] for i in C]
        d4s = [H for i in C for H in packet_data[i][1]]
        assert sum(map(len, packets)) == 240
        assert len(set().union(*packets)) == 240
        assert sum(map(len, d4s)) == 240
        assert len(set().union(*d4s)) == 240

    edge_to_line = {}
    for e in edges:
        hits = [k for k, C in enumerate(fivepacks) if set(e) <= set(C)]
        assert len(hits) == 1
        edge_to_line[e] = hits[0]
    line_edge_load = Counter(edge_to_line.values())
    assert set(line_edge_load.values()) == {10}
    packet_line_load = Counter(i for C in fivepacks for i in C)
    assert set(packet_line_load.values()) == {3}

    # Each obstruction edge therefore exposes 96 roots and uniquely determines
    # the complementary 144-root completion inside its unique five-pack.
    completion_sizes = Counter()
    cross_d4_rank8 = 0
    for e, li in edge_to_line.items():
        a, b = tuple(e)
        exposed = packet_data[a][2] | packet_data[b][2]
        assert len(exposed) == 96
        C = fivepacks[li]
        completion = set().union(*(packet_data[i][2] for i in C if i not in e))
        assert len(completion) == 144 and exposed.isdisjoint(completion)
        assert exposed | completion == set(range(240))
        completion_sizes[len(completion)] += 1

        # Across the two D4+D4 packets, every cross choice spans rank 8.
        # This is the root-space shadow of the previously certified unimodular
        # E8 chart relation; integer index-one is not re-proved here.
        for A in packet_data[a][1]:
            for B in packet_data[b][1]:
                rows = [roots[u] for u in A | B]
                # exact Gaussian elimination over Q using Fraction-free integer arithmetic
                M = [list(r) for r in rows]
                rank = 0
                for col in range(8):
                    pivot = next((r for r in range(rank, len(M)) if M[r][col]), None)
                    if pivot is None:
                        continue
                    M[rank], M[pivot] = M[pivot], M[rank]
                    pv = M[rank][col]
                    for r in range(rank + 1, len(M)):
                        if M[r][col]:
                            a0, b0 = M[r][col], pv
                            M[r] = [b0 * M[r][c] - a0 * M[rank][c] for c in range(8)]
                    rank += 1
                assert rank == 8
                cross_d4_rank8 += 1
    assert completion_sizes == Counter({144: 270})
    assert cross_d4_rank8 == 270 * 4

    return {
        "schema": "w33.20260901.regulus-e8-completion-bridge.v1",
        "status": "PASS",
        "w33": {
            "points": 40,
            "polarPairPackets": 45,
            "packetSupportSize": 8,
            "supportPairIntersections": {str(k): v for k, v in sorted(intersection_hist.items())},
            "disjointnessDegree": 12,
            "disjointEdges": len(edges),
            "fivepackLines": len(fivepacks),
            "packetsPerFivepack": 5,
            "fivepacksPerPacket": 3,
            "disjointEdgesPerFivepack": 10,
            "edgeUniqueCompletion": True,
        },
        "e8": {
            "roots": 240,
            "selectedD4Subsystems": len(selected_d4),
            "rootsPerD4": 24,
            "orthogonalD4Pairs": 45,
            "rootsPerPacket": 48,
            "d4PerSpread": 10,
            "packetsPerSpread": 5,
            "eachSpreadPartitionsAllRoots": True,
            "obstructionPairRoots": 96,
            "uniqueCompletionAddsRoots": 144,
            "crossPacketD4PairsRank8Checked": cross_d4_rank8,
        },
        "crossRepo": {
            "holotradeCommit": "4952a3b3b3061af796edb86bce316c2f92475d10",
            "holotradeObjectwiseFact": "the 270 depth-3 all-isotropic reguli equal the 270 support-disjoint polar-pair pairs",
            "newComposition": "each depth-3 obstruction regulus determines exactly one of the 27 E8 ten-D4 root partitions",
        },
        "theorem": "The depth-3 regulus obstruction is an E8 completion address: its two disjoint D4+D4 packets expose 96 roots and uniquely complete by 144 roots to one ten-D4 partition of the 240-root shell.",
        "boundary": "Exact finite-combinatorial composition of certified objects. It is not a physical obstruction-removal theorem and assigns no dynamics to E8.",
    }


def main():
    out = build_certificate()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out, sort_keys=True))


if __name__ == "__main__":
    main()
