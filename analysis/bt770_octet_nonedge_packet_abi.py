#!/usr/bin/env python3
"""BT770 — Octet nonedge packet ABI theorem.

BT769 identifies the 45 intrinsic octets with the old center-quad quotient
objects.  This file turns that into a deterministic packet ABI.

Each packet consists of two noncollinear K4 halves A and B.  The W33 graph
restricted to A union B is K_{4,4}: 16 crossing collinearity edges plus 12
internal nonedges.  Across the 45 packets, the 12 internal nonedges partition
all 540 W33 nonedges exactly once.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

import networkx as nx

from bt766_intrinsic_k44_octet_quotient import build_w33
from bt769_center_quad_octet_identification import find_center_quad_components

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT770_OCTET_NONEDGE_PACKET_ABI_summary.json"
PACKET_OUT = ROOT / "data" / "generated_octet_packets" / "bt770_octet_packet_abi.json"


def make_packets(G):
    components = find_center_quad_components(G)
    outer_to_center = {c["outer"]: c["center"] for c in components}
    pairs = sorted({tuple(sorted((c["outer"], c["center"]))) for c in components})
    packets = []
    for pid, (A, B) in enumerate(pairs):
        A = tuple(A)
        B = tuple(B)
        octet = tuple(sorted(set(A) | set(B)))
        crossing_edges = []
        for a in A:
            for b in B:
                assert G.has_edge(a, b)
                crossing_edges.append(tuple(sorted((a, b))))
        internal_nonedges = []
        for half in (A, B):
            for e in itertools.combinations(half, 2):
                assert not G.has_edge(*e)
                internal_nonedges.append(tuple(sorted(e)))
        packet = {
            "packet_id": pid,
            "half_a": list(A),
            "half_b": list(B),
            "octet": list(octet),
            "stored_nonedges": [list(e) for e in sorted(internal_nonedges)],
            "transport_edges": [list(e) for e in sorted(crossing_edges)],
            "arity": {
                "points": 8,
                "stored_nonedges": 12,
                "transport_edges": 16,
                "internal_pairs": 28,
            },
        }
        packets.append(packet)
    return packets


def srg_params(H):
    degs = Counter(dict(H.degree()).values())
    lambdas = Counter()
    mus = Counter()
    for i, j in itertools.combinations(H.nodes(), 2):
        cn = len(set(H.neighbors(i)) & set(H.neighbors(j)))
        if H.has_edge(i, j):
            lambdas[cn] += 1
        else:
            mus[cn] += 1
    return degs, lambdas, mus


def main():
    pts, lines, idx, G, point_lines = build_w33()
    packets = make_packets(G)

    all_nonedges = {tuple(sorted((a, b))) for a, b in itertools.combinations(range(40), 2) if not G.has_edge(a, b)}
    all_edges = {tuple(sorted(e)) for e in G.edges()}
    stored = [tuple(e) for p in packets for e in p["stored_nonedges"]]
    transport = [tuple(e) for p in packets for e in p["transport_edges"]]

    point_packet_count = Counter(q for p in packets for q in p["octet"])
    edge_packet_count = Counter(transport)
    nonedge_packet_count = Counter(stored)

    packet_graph = nx.Graph()
    packet_graph.add_nodes_from(range(len(packets)))
    for i, j in itertools.combinations(range(len(packets)), 2):
        inter = len(set(packets[i]["octet"]) & set(packets[j]["octet"]))
        if inter == 2:
            packet_graph.add_edge(i, j)
    packet_comp = nx.complement(packet_graph)
    degs, lam, mu = srg_params(packet_graph)
    cdegs, clam, cmu = srg_params(packet_comp)

    abi = {
        "bt770_schema_version": "1.0",
        "packet_count": len(packets),
        "packet_type": "intrinsic_W33_K44_octet_nonedge_packet",
        "packet_contract": {
            "points_per_packet": 8,
            "stored_nonedges_per_packet": 12,
            "transport_edges_per_packet": 16,
            "stored_nonedge_partition_total": 540,
            "transport_edge_cover_multiplicity": 3,
            "point_cover_multiplicity": 9,
        },
        "packets": packets,
    }
    payload = json.dumps(abi, indent=2, sort_keys=True) + "\n"
    sha = hashlib.sha256(payload.encode()).hexdigest()

    checks = {
        "packet_count_45": len(packets) == 45,
        "each_packet_8_12_16": all(len(p["octet"]) == 8 and len(p["stored_nonedges"]) == 12 and len(p["transport_edges"]) == 16 for p in packets),
        "stored_nonedges_partition_540": len(stored) == 540 and set(stored) == all_nonedges and Counter(stored) == Counter({e: 1 for e in all_nonedges}),
        "transport_edges_cover_240_each_3": set(transport) == all_edges and Counter(edge_packet_count.values()) == Counter({3: 240}),
        "point_cover_40_each_9": Counter(point_packet_count.values()) == Counter({9: 40}),
        "packet_intersection_graph_SRG_45_32_22_24": packet_graph.number_of_edges() == 720 and degs == Counter({32: 45}) and lam == Counter({22: 720}) and mu == Counter({24: 270}),
        "packet_disjointness_complement_SRG_45_12_3_3": packet_comp.number_of_edges() == 270 and cdegs == Counter({12: 45}) and clam == Counter({3: 270}) and cmu == Counter({3: 720}),
    }

    summary = {
        "theorem": "BT770 Octet Nonedge Packet ABI Theorem",
        "abi_payload": str(PACKET_OUT.relative_to(ROOT)),
        "abi_sha256": sha,
        "summary": {
            "packet_count": len(packets),
            "points_per_packet": 8,
            "stored_nonedges_per_packet": 12,
            "transport_edges_per_packet": 16,
            "stored_nonedge_total": len(stored),
            "unique_stored_nonedges": len(set(stored)),
            "unique_transport_edges": len(set(transport)),
            "point_cover_distribution": {str(k): int(v) for k, v in sorted(Counter(point_packet_count.values()).items())},
            "edge_cover_distribution": {str(k): int(v) for k, v in sorted(Counter(edge_packet_count.values()).items())},
            "nonedge_cover_distribution": {str(k): int(v) for k, v in sorted(Counter(nonedge_packet_count.values()).items())},
        },
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "boundary": "This defines a deterministic packet ABI for W33 nonedges using the 45 intrinsic K4,4 octets. It is an ABI/export layer, not a claim about the missing root-torsor-to-Q(4,3) transport table."
    }

    PACKET_OUT.parent.mkdir(parents=True, exist_ok=True)
    PACKET_OUT.write_text(payload)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    if not summary["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
