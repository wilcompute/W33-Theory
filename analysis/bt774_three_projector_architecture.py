#!/usr/bin/env python3
"""BT774 — Three-projector architecture verifier.

This integrates BT767, BT771, and BT773.

Point space split:
    40 = (1 + 24) + 15

The 1+24 carrier is the image of the point/octet incidence matrix M.  The
15-sector is the image of H_15 = 8I - 4A_W33 + J, and M^T H_15 = 0.

Chart space split:
    the 240 centered local K_{3,3} chart graph has an 81-dimensional
    (-1)-eigenspace.  The packet/chart incidence matrix N annihilates this
    sector, separating chart memory from packet routing.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

import networkx as nx
import numpy as np

from bt766_intrinsic_k44_octet_quotient import build_w33
from bt770_octet_nonedge_packet_abi import make_packets
from bt773_octet_packet_selector_bus import build_chart_system

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT774_THREE_PROJECTOR_ARCHITECTURE_summary.json"


def cdict(counter):
    return {str(k): int(v) for k, v in sorted(counter.items())}


def spectrum_counter(M):
    vals = np.linalg.eigvalsh(np.array(M, dtype=float))
    return cdict(Counter(int(round(x)) for x in vals))


def main():
    pts, lines, idx, G, point_lines = build_w33()
    A = nx.to_numpy_array(G, nodelist=range(40), dtype=int)
    I40 = np.eye(40, dtype=int)
    J40 = np.ones((40, 40), dtype=int)

    packets = make_packets(G)
    M = np.zeros((40, 45), dtype=int)
    for j, packet in enumerate(packets):
        for p in packet["octet"]:
            M[p, j] = 1
    MMt = M @ M.T
    H15 = 8 * I40 - 4 * A + J40

    nonedges, nonedge_to_id, line_pair_to_id, charts, chart_nonedges, chart_key_to_id = build_chart_system(G, lines, idx, point_lines)

    # Chart graph: adjacent when two centered local K3,3 charts share exactly one W33 nonedge.
    chart_graph = nx.Graph()
    chart_graph.add_nodes_from(range(len(charts)))
    chart_sets = [set(x) for x in chart_nonedges]
    for i, j in itertools.combinations(range(len(charts)), 2):
        if len(chart_sets[i] & chart_sets[j]) == 1:
            chart_graph.add_edge(i, j)
    B = nx.to_numpy_array(chart_graph, nodelist=range(240), dtype=int)
    I240 = np.eye(240, dtype=object)
    Bobj = B.astype(object)

    # Integer spectral numerator for the chart -1 eigenspace.
    L81 = I240.copy()
    for lam in [27, 9, 3, -3, -9]:
        L81 = L81 @ (Bobj - lam * I240)
    chart_idempotent_scale = -17920

    # Chart/packet incidence N: N[c,p]=1 when chart c contains a stored nonedge of packet p.
    edge_to_packet = {}
    for p in packets:
        pid = p["packet_id"]
        for e in p["stored_nonedges"]:
            edge_to_packet[tuple(e)] = pid
    N = np.zeros((240, 45), dtype=int)
    for ci, nes in enumerate(chart_nonedges):
        for eid in nes:
            N[ci, edge_to_packet[nonedges[eid]]] = 1

    eig_A = Counter(int(round(x)) for x in np.linalg.eigvalsh(A))
    eig_B = Counter(int(round(x)) for x in np.linalg.eigvalsh(B))
    eig_H15 = Counter(int(round(x)) for x in np.linalg.eigvalsh(H15))
    eig_MMt = Counter(int(round(x)) for x in np.linalg.eigvalsh(MMt))

    L81_float = np.array(L81, dtype=float)
    rank_L81 = int(np.linalg.matrix_rank(L81_float))
    L81N = np.array(L81 @ N.astype(object), dtype=object)

    checks = {
        "point_space_W33_spectrum_1_24_15": eig_A == Counter({12: 1, 2: 24, -4: 15}),
        "octet_carrier_rank_25": int(np.linalg.matrix_rank(MMt)) == 25 and eig_MMt == Counter({72: 1, 12: 24, 0: 15}),
        "null_15_rank_15": int(np.linalg.matrix_rank(H15)) == 15 and eig_H15 == Counter({24: 15, 0: 25}),
        "point_projectors_orthogonal": np.array_equal(MMt @ H15, np.zeros((40, 40), dtype=int))
        and np.array_equal(H15 @ MMt, np.zeros((40, 40), dtype=int)),
        "point_ranks_sum_to_40": int(np.linalg.matrix_rank(MMt)) + int(np.linalg.matrix_rank(H15)) == 40,
        "chart_graph_spectrum_has_minus1_81": eig_B == Counter({27: 1, 9: 24, 3: 75, -1: 81, -3: 24, -9: 35}),
        "chart_81_projector_rank_81": rank_L81 == 81,
        "chart_81_projector_scaled_idempotent": np.array_equal(np.array(L81 @ L81, dtype=object), chart_idempotent_scale * L81),
        "chart_packet_incidence_shape_240_45": list(N.shape) == [240, 45],
        "chart_packet_incidence_2160_ones": int(N.sum()) == 2160,
        "chart_81_sector_annihilates_packet_incidence": np.array_equal(L81N, np.zeros((240, 45), dtype=object)),
    }

    result = {
        "theorem": "BT774 Three-Projector Architecture Verifier",
        "point_space": {
            "split": "40 = (1+24) + 15",
            "octet_carrier": {
                "matrix": "M_octet M_octet^T",
                "rank": int(np.linalg.matrix_rank(MMt)),
                "spectrum": cdict(eig_MMt),
            },
            "null_15": {
                "matrix": "H_15 = 8I - 4A_W33 + J",
                "rank": int(np.linalg.matrix_rank(H15)),
                "spectrum": cdict(eig_H15),
            },
            "orthogonality": "(M M^T) H_15 = H_15 (M M^T) = 0",
        },
        "chart_space": {
            "chart_count": len(charts),
            "chart_graph_spectrum": cdict(eig_B),
            "memory_sector": "-1 eigenspace",
            "memory_dimension": rank_L81,
            "projector_numerator": "prod_{lambda != -1}(B_chart - lambda I)",
            "scaled_idempotent": "L_81^2 = -17920 L_81",
            "packet_incidence": "N_chart_packet",
            "packet_incidence_ones": int(N.sum()),
            "annihilation": "L_81 N_chart_packet = 0",
        },
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "boundary": "This proves the integrated linear-algebra architecture: point octet carrier, point 15-null sector, and chart 81-memory sector. It does not yet construct the full 51840 root-torsor transport table."
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
