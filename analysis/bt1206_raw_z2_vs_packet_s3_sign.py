#!/usr/bin/env python3
"""BT1206 -- raw/canonical Z2 voltage versus packet local S3 sign.

Align the Witting-packet 720-edge transport graph with the reconstructed
center-quad transport graph by an explicit graph isomorphism.  Then compare the
raw and canonical center-quad Z2 voltages with the actual local S3 matching sign
on the packet edge.  This is the first edgewise contingency test on the 720-edge
carrier.  The chosen graph isomorphism is recorded as a labelled comparison; a
future canonical labelling can test isomorphism-independence.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
for p in (ROOT, ROOT / "scripts", ROOT / "exploration", ROOT / "pillars"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from exploration.w33_center_quad_transport_bridge import quotient_edge_voltage_data, reconstructed_quotient_graph
from scripts.w33_witting_packet_quotient_geometry_audit import _build_leaf_list, _packet_lines, _line_graph
from scripts.w33_witting_packet_transport_complement_audit import _leaf_packet_lines


def perm_parity(perm):
    return sum(1 for i in range(3) for j in range(i + 1, 3) if perm[i] > perm[j]) % 2


def packet_transport_with_s3():
    leaves = _build_leaf_list()
    leaf_graph = nx.Graph(); leaf_graph.add_nodes_from(range(len(leaves)))
    for a, b in combinations(range(len(leaves)), 2):
        if len(set(leaves[a][2]) & set(leaves[b][2])) == 1:
            leaf_graph.add_edge(a, b)
    transport = nx.complement(leaf_graph)
    packet_lines = _packet_lines(leaves)
    line_graph = _line_graph(packet_lines)
    memberships = _leaf_packet_lines(packet_lines, len(leaves))
    edge_sign = {}
    edge_perm = {}
    for a, b in sorted(transport.edges()):
        perm = []
        for packet_line in memberships[a]:
            matches = [idx for idx, other in enumerate(memberships[b]) if line_graph.has_edge(packet_line, other)]
            perm.append(matches[0])
        perm = tuple(perm)
        edge_sign[tuple(sorted((a, b)))] = perm_parity(perm)
        edge_perm[tuple(sorted((a, b)))] = "".join(map(str, perm))
    return transport, edge_sign, edge_perm


def main():
    packet_graph, s3_sign, s3_perm = packet_transport_with_s3()
    center_graph, raw_lookup = reconstructed_quotient_graph()
    voltage_edges, _gauge = quotient_edge_voltage_data()
    canonical_lookup = {tuple(sorted((e.u, e.v))): e.canonical_z2 for e in voltage_edges}

    matcher = nx.algorithms.isomorphism.GraphMatcher(packet_graph, center_graph)
    mapping = next(matcher.isomorphisms_iter())  # packet node -> center-quad node

    raw_vs_s3 = Counter()
    canonical_vs_s3 = Counter()
    perm_by_raw = Counter()
    examples = []
    for edge in sorted(packet_graph.edges()):
        pe = tuple(sorted(edge))
        ce = tuple(sorted((mapping[edge[0]], mapping[edge[1]])))
        raw = raw_lookup[ce]
        canonical = canonical_lookup[ce]
        sign = s3_sign[pe]
        raw_vs_s3[(raw, sign)] += 1
        canonical_vs_s3[(canonical, sign)] += 1
        perm_by_raw[(raw, s3_perm[pe])] += 1
        if len(examples) < 8:
            examples.append({"packet_edge": list(pe), "center_edge": list(ce), "raw_z2": raw, "canonical_z2": canonical, "s3_perm": s3_perm[pe], "s3_sign": sign})

    payload = {
        "bt": 1206,
        "title": "raw Z2 voltage versus packet local S3 sign",
        "comparison_scope": "one explicit packet-transport -> center-quad graph isomorphism",
        "edge_count": packet_graph.number_of_edges(),
        "raw_vs_s3_sign": {str(k): v for k, v in sorted(raw_vs_s3.items())},
        "canonical_vs_s3_sign": {str(k): v for k, v in sorted(canonical_vs_s3.items())},
        "raw_distribution": dict(sorted(Counter(k[0] for k in raw_vs_s3.elements()).items())),
        "s3_sign_distribution": dict(sorted(Counter(k[1] for k in raw_vs_s3.elements()).items())),
        "all_six_s3_permutations_present": len({k[1] for k in perm_by_raw}) == 6,
        "example_edges": examples,
        "verdict": "edgewise table computed under an explicit isomorphism; equality is not assumed and isomorphism-dependence remains a next test",
        "checks": {
            "edge_count_720": packet_graph.number_of_edges() == 720,
            "raw_vs_s3_sums_720": sum(raw_vs_s3.values()) == 720,
            "canonical_vs_s3_sums_720": sum(canonical_vs_s3.values()) == 720,
            "s3_distribution_expected": dict(sorted(Counter(k[1] for k in raw_vs_s3.elements()).items())) == {0: 366, 1: 354},
        },
    }
    payload["checks"]["all_checks_pass"] = all(payload["checks"].values())
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
