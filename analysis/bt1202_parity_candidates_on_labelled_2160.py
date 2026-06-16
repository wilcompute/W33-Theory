#!/usr/bin/env python3
"""BT1202 -- parity candidates on the labelled 2160 codec.

With actual 720-edge labels attached, there are two natural binary candidates:
  * half-fiber parity z2_half = floor(h/24), living on C2160 rows;
  * local S3 matching parity on each actual packet-transport edge, already known
    from the Witting packet transport complement audit.

The test is honest: half-fiber parity is NOT a function of the 720 edge alone
(each edge has both sheets across the three C3 rows), while local S3 parity IS an
edge-level binary label and has distribution 366+354 over the 720 actual edges.
Therefore raw edge voltage, if it is an edge-level voltage, can only be compared
to the actual S3 sign candidate or to a chosen half-fiber section, not to the
unsectioned half-fiber parity.
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
for p in (ROOT, ROOT / "scripts"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from scripts.w33_witting_packet_quotient_geometry_audit import _build_leaf_list, _packet_lines, _line_graph
from scripts.w33_witting_packet_transport_complement_audit import _leaf_packet_lines


def parity(perm):
    return sum(1 for i in range(3) for j in range(i + 1, 3) if perm[i] > perm[j]) % 2


def actual_720_s3_parities():
    leaves = _build_leaf_list()
    leaf_graph = nx.Graph(); leaf_graph.add_nodes_from(range(len(leaves)))
    for a, b in combinations(range(len(leaves)), 2):
        if len(set(leaves[a][2]) & set(leaves[b][2])) == 1:
            leaf_graph.add_edge(a, b)
    transport = nx.complement(leaf_graph)
    packet_lines = _packet_lines(leaves)
    line_graph = _line_graph(packet_lines)
    memberships = _leaf_packet_lines(packet_lines, len(leaves))
    out = []
    for edge_id, (a, b) in enumerate(sorted(transport.edges())):
        perm = []
        for packet_line in memberships[a]:
            matches = [idx for idx, other in enumerate(memberships[b]) if line_graph.has_edge(packet_line, other)]
            perm.append(matches[0])
        out.append({"edge720_id": edge_id, "edge": [a, b], "perm": tuple(perm), "s3_sign": parity(tuple(perm))})
    return out


def main():
    s3_edges = actual_720_s3_parities()
    s3_dist = Counter(edge["s3_sign"] for edge in s3_edges)

    half_by_edge = defaultdict(set)
    half_by_edge_c3 = defaultdict(set)
    for t in range(45):
        for h in range(48):
            edge720 = 16 * t + (h % 16)
            c3 = h // 16
            z2_half = h // 24
            half_by_edge[edge720].add(z2_half)
            half_by_edge_c3[(edge720, c3)].add(z2_half)

    ambiguous_edges = sum(1 for values in half_by_edge.values() if values == {0, 1})
    section_tests = {}
    for c3 in (0, 1, 2):
        section_values = {edge: next(iter(half_by_edge_c3[(edge, c3)])) for edge in range(720)}
        dist = Counter(section_values.values())
        section_tests[str(c3)] = {"half_parity_dist": dict(sorted(dist.items())), "matches_s3_sign_distribution": dict(sorted(dist.items())) == dict(sorted(s3_dist.items()))}

    payload = {
        "bt": 1202,
        "title": "parity candidates on the labelled 2160 carrier",
        "actual_720_s3_sign_distribution": dict(sorted(s3_dist.items())),
        "half_fiber_parity_edge_level": {
            "ambiguous_edges": ambiguous_edges,
            "is_edge_function_without_section": ambiguous_edges == 0,
        },
        "half_fiber_sections_by_c3": section_tests,
        "verdict": "raw edge Z2 cannot equal unsectioned half-fiber parity; actual local S3 sign is the viable edge-level binary candidate",
        "checks": {
            "s3_edges720": len(s3_edges) == 720,
            "s3_sign_distribution_expected": dict(sorted(s3_dist.items())) == {0: 366, 1: 354},
            "half_parity_not_edge_function": ambiguous_edges == 720,
            "c3_sections_are_edge_functions": all(len(v) == 1 for v in half_by_edge_c3.values()),
        },
    }
    payload["checks"]["all_checks_pass"] = all(payload["checks"].values())
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
