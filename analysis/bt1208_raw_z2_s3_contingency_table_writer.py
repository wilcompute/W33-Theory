#!/usr/bin/env python3
"""BT1208 -- write the raw/canonical Z2 vs packet-local S3 sign table.

This is the executable version of the table requested after BT1206.  It aligns
the Witting-packet transport graph with the reconstructed center-quad transport
graph by a deterministic NetworkX isomorphism, then writes the actual 2x2 tables
for

    raw Z2 voltage       vs local S3 matching sign
    canonical Z2 voltage vs local S3 matching sign

to data/PART_BT1208_RAW_Z2_S3_CONTINGENCY_TABLE_results.json.

Important boundary: the table is isomorphism-labelled.  BT1209 samples other
isomorphisms to test whether the table is invariant under this alignment choice.
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

OUT = ROOT / "data" / "PART_BT1208_RAW_Z2_S3_CONTINGENCY_TABLE_results.json"


def _parity(perm: tuple[int, int, int]) -> int:
    return sum(1 for i in range(3) for j in range(i + 1, 3) if perm[i] > perm[j]) % 2


def packet_transport_with_s3() -> tuple[nx.Graph, dict[tuple[int, int], int], dict[tuple[int, int], str]]:
    leaves = _build_leaf_list()
    leaf_graph = nx.Graph(); leaf_graph.add_nodes_from(range(len(leaves)))
    for a, b in combinations(range(len(leaves)), 2):
        if len(set(leaves[a][2]) & set(leaves[b][2])) == 1:
            leaf_graph.add_edge(a, b)
    transport = nx.complement(leaf_graph)
    packet_lines = _packet_lines(leaves)
    line_graph = _line_graph(packet_lines)
    memberships = _leaf_packet_lines(packet_lines, len(leaves))
    edge_sign: dict[tuple[int, int], int] = {}
    edge_perm: dict[tuple[int, int], str] = {}
    for a, b in sorted(transport.edges()):
        perm = []
        for packet_line in memberships[a]:
            matches = [idx for idx, other in enumerate(memberships[b]) if line_graph.has_edge(packet_line, other)]
            if len(matches) != 1:
                raise AssertionError((a, b, packet_line, matches))
            perm.append(matches[0])
        perm_t = tuple(perm)
        edge_sign[tuple(sorted((a, b)))] = _parity(perm_t)
        edge_perm[tuple(sorted((a, b)))] = "".join(map(str, perm_t))
    return transport, edge_sign, edge_perm


def contingency_for_mapping(mapping: dict[int, int]) -> dict:
    packet_graph, s3_sign, s3_perm = packet_transport_with_s3()
    center_graph, raw_lookup = reconstructed_quotient_graph()
    canonical_lookup = {tuple(sorted((e.u, e.v))): e.canonical_z2 for e in quotient_edge_voltage_data()[0]}
    raw_vs_s3: Counter[tuple[int, int]] = Counter()
    canonical_vs_s3: Counter[tuple[int, int]] = Counter()
    raw_vs_perm: Counter[tuple[int, str]] = Counter()
    examples = []
    for a, b in sorted(packet_graph.edges()):
        pe = tuple(sorted((a, b)))
        ce = tuple(sorted((mapping[a], mapping[b])))
        if not center_graph.has_edge(*ce):
            raise AssertionError((pe, ce))
        raw = raw_lookup[ce]
        canonical = canonical_lookup[ce]
        sign = s3_sign[pe]
        perm = s3_perm[pe]
        raw_vs_s3[(raw, sign)] += 1
        canonical_vs_s3[(canonical, sign)] += 1
        raw_vs_perm[(raw, perm)] += 1
        if len(examples) < 12:
            examples.append({"packet_edge": list(pe), "center_edge": list(ce), "raw_z2": raw, "canonical_z2": canonical, "s3_perm": perm, "s3_sign": sign})
    return {
        "raw_vs_s3_sign": {f"{a},{b}": c for (a, b), c in sorted(raw_vs_s3.items())},
        "canonical_vs_s3_sign": {f"{a},{b}": c for (a, b), c in sorted(canonical_vs_s3.items())},
        "raw_vs_s3_perm": {f"{a},{p}": c for (a, p), c in sorted(raw_vs_perm.items())},
        "examples": examples,
    }


def main() -> int:
    packet_graph, _s3_sign, _s3_perm = packet_transport_with_s3()
    center_graph, _raw_lookup = reconstructed_quotient_graph()
    mapping = next(nx.algorithms.isomorphism.GraphMatcher(packet_graph, center_graph).isomorphisms_iter())
    table = contingency_for_mapping(mapping)
    payload = {
        "bt": 1208,
        "title": "raw/canonical Z2 voltage versus packet-local S3 sign contingency table",
        "alignment": "first deterministic NetworkX packet-transport -> center-quad graph isomorphism",
        "edge_count": packet_graph.number_of_edges(),
        **table,
        "status": "actual table written by executing this script; BT1209 tests isomorphism dependence",
        "checks": {
            "edge_count_720": packet_graph.number_of_edges() == center_graph.number_of_edges() == 720,
            "raw_table_sums_720": sum(table["raw_vs_s3_sign"].values()) == 720,
            "canonical_table_sums_720": sum(table["canonical_vs_s3_sign"].values()) == 720,
        },
    }
    payload["checks"]["all_checks_pass"] = all(payload["checks"].values())
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
