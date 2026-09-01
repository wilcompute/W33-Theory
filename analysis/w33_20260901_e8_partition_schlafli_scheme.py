#!/usr/bin/env python3
"""Exact Schlaefli incidence scheme on the 27 selected E8 ten-D4 partitions.

Builds only from the certified W33/E8 fibre model.  The 45 minimum weight-8
supports are the selected orthogonal D4+D4 packets.  Their 27 five-cliques are
partitions of the 240 roots into ten selected D4 subsystems.

New chart-level statement:
  * any two of the 27 partitions share either 0 or 2 D4 blocks;
  * adjacency = sharing 2 D4 blocks gives SRG(27,10,1,5);
  * its complement is the Schlaefli graph SRG(27,16,10,8);
  * the 45 packet blocks are exactly the 45 triangles of the adjacency graph.

Thus the cubic-surface 27-line / 45-tritangent incidence is reconstructed
inside the selected E8 partition catalogue: lines -> ten-D4 partitions,
tritangent planes -> common D4+D4 packet blocks.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

from w33_pass7163_7170_e8_hexagonal_lift import e8_fibers, gf2_basis
from w33_20260901_regulus_e8_completion_bridge import minimum_supports, packet_halves

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_W33_20260901_E8_PARTITION_SCHLAFLI_SCHEME.json"


def common_neighbor_parameter(adj, u, v):
    return len(adj[u] & adj[v])


def main():
    roots, fibres, _phase, _radj, base_adj, _zero, _twelve, _diffhist = e8_fibers()
    supports = minimum_supports(base_adj)

    # Packet-disjointness graph and its 27 GQ(4,2) lines / five-packs.
    p_adj = [set() for _ in range(45)]
    for i, j in itertools.combinations(range(45), 2):
        if supports[i].isdisjoint(supports[j]):
            p_adj[i].add(j)
            p_adj[j].add(i)
    assert {len(x) for x in p_adj} == {12}

    fivepacks = []
    for C in itertools.combinations(range(45), 5):
        if all(b in p_adj[a] for a, b in itertools.combinations(C, 2)):
            fivepacks.append(tuple(C))
    assert len(fivepacks) == 27

    # Realize each packet as its two selected 24-root D4 blocks.
    packet_d4 = []
    for S in supports:
        _halves, root_halves = packet_halves(S, base_adj, fibres)
        packet_d4.append(tuple(root_halves))

    # Each chart is a partition of all 240 roots into ten selected D4 blocks.
    charts = []
    for C in fivepacks:
        blocks = frozenset(H for p in C for H in packet_d4[p])
        assert len(blocks) == 10
        assert sum(len(H) for H in blocks) == 240
        assert len(set().union(*blocks)) == 240
        charts.append(blocks)
    assert len(set(charts)) == 27

    # Pairwise partition-block overlap.
    overlap_hist = Counter()
    chart_adj = [set() for _ in range(27)]
    for i, j in itertools.combinations(range(27), 2):
        common = len(charts[i] & charts[j])
        overlap_hist[common] += 1
        assert common in (0, 2)
        if common == 2:
            chart_adj[i].add(j)
            chart_adj[j].add(i)
    assert overlap_hist == Counter({0: 216, 2: 135})
    assert {len(N) for N in chart_adj} == {10}

    # SRG(27,10,1,5).
    lam = set()
    mu = set()
    for i, j in itertools.combinations(range(27), 2):
        c = common_neighbor_parameter(chart_adj, i, j)
        (lam if j in chart_adj[i] else mu).add(c)
    assert lam == {1}
    assert mu == {5}

    # Each packet occurs in exactly three charts.  Those three charts form one
    # triangle, and every triangle comes from exactly one packet.
    packet_to_charts = []
    packet_triangles = set()
    for p in range(45):
        hits = tuple(i for i, C in enumerate(fivepacks) if p in C)
        assert len(hits) == 3
        assert all(b in chart_adj[a] for a, b in itertools.combinations(hits, 2))
        packet_to_charts.append(hits)
        packet_triangles.add(frozenset(hits))
    assert len(packet_triangles) == 45

    graph_triangles = set()
    for T in itertools.combinations(range(27), 3):
        if all(b in chart_adj[a] for a, b in itertools.combinations(T, 2)):
            graph_triangles.add(frozenset(T))
    assert graph_triangles == packet_triangles

    # Each adjacent chart pair shares exactly one packet, hence exactly its two
    # D4 blocks.  This proves the packet/triangle incidence, not just counts.
    edge_packet_unique = True
    for i in range(27):
        for j in chart_adj[i]:
            if i >= j:
                continue
            common_packets = set(fivepacks[i]) & set(fivepacks[j])
            assert len(common_packets) == 1
            p = next(iter(common_packets))
            assert charts[i] & charts[j] == frozenset(packet_d4[p])

    out = {
        "schema": "w33.20260901.e8-partition-schlafli-scheme.v1",
        "status": "PASS",
        "partitions": 27,
        "d4BlocksPerPartition": 10,
        "rootsPerPartition": 240,
        "allPartitionsCoverSameRootShell": True,
        "pairwiseSharedD4BlockHistogram": {str(k): v for k, v in sorted(overlap_hist.items())},
        "partitionOverlapGraph": {
            "v": 27,
            "k": 10,
            "lambda": 1,
            "mu": 5,
            "name": "cubic-surface 27-line intersection graph",
            "complement": "Schlaefli graph SRG(27,16,10,8)"
        },
        "packetTriangles": {
            "packets": 45,
            "chartsPerPacket": 3,
            "graphTriangles": len(graph_triangles),
            "allTrianglesArePackets": True,
            "packetMeaning": "one shared 48-root orthogonal D4+D4 block"
        },
        "objectwise": {
            "adjacentPartitionPairSharesOnePacket": edge_packet_unique,
            "sharedD4BlocksWhenAdjacent": 2,
            "sharedD4BlocksWhenNonadjacent": 0
        },
        "theorem": "The 27 selected ten-D4 partitions of the E8 root shell carry the cubic-surface SRG(27,10,1,5); the 45 selected D4+D4 packets are exactly its 45 triangles/tritangent incidences.",
        "boundary": "All 27 objects partition the same 240 roots. The overlap invariant is common D4 partition blocks, not intersection of their underlying root sets."
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out, sort_keys=True))


if __name__ == "__main__":
    main()
