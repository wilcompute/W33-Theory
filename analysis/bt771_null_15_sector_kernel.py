#!/usr/bin/env python3
"""BT771 — Null 15-sector kernel theorem.

BT767 proved that the 40-by-45 point/octet incidence matrix M keeps the
1+24 W33 point sector and has zero response on the 15-dimensional
(-4)-eigenspace.  This verifier identifies that sector as an explicit
integer kernel:

    H_15 = 8 I - 4 A_W33 + J.

H_15 has entries 9 on the diagonal, -3 on W33 edges, and +1 on W33
nonedges.  It satisfies H_15^2 = 24 H_15, has rank 15, and obeys

    H_15 M = 0.

After normalization H_15/9 is the Gram matrix of 40 unit vectors in R^15,
with inner products -1/3 on adjacent W33 points and +1/9 on nonadjacent W33
points.
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

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT771_NULL_15_SECTOR_KERNEL_summary.json"


def cdict(counter):
    return {str(k): int(v) for k, v in sorted(counter.items())}


def main():
    pts, lines, idx, G, point_lines = build_w33()
    packets = make_packets(G)

    A = nx.to_numpy_array(G, nodelist=range(40), dtype=int)
    I = np.eye(40, dtype=int)
    J = np.ones((40, 40), dtype=int)
    H = 8 * I - 4 * A + J

    M = np.zeros((40, len(packets)), dtype=int)
    for j, p in enumerate(packets):
        for q in p["octet"]:
            M[q, j] = 1

    eig_H = Counter(int(round(x)) for x in np.linalg.eigvalsh(H))
    eig_A = Counter(int(round(x)) for x in np.linalg.eigvalsh(A))
    adj_values = Counter()
    nonadj_values = Counter()
    for i, j in itertools.combinations(range(40), 2):
        if G.has_edge(i, j):
            adj_values[int(H[i, j])] += 1
        else:
            nonadj_values[int(H[i, j])] += 1

    checks = {
        "W33_spectrum_12_2_minus4": eig_A == Counter({-4: 15, 2: 24, 12: 1}),
        "H_entries_9_minus3_plus1": Counter(int(H[i, i]) for i in range(40)) == Counter({9: 40})
        and adj_values == Counter({-3: 240})
        and nonadj_values == Counter({1: 540}),
        "H_squared_24H": np.array_equal(H @ H, 24 * H),
        "rank_15": int(np.linalg.matrix_rank(H)) == 15,
        "spectrum_24_rank15_zero25": eig_H == Counter({0: 25, 24: 15}),
        "octet_matrix_HM_zero": np.array_equal(H @ M, np.zeros((40, 45), dtype=int)),
        "octet_matrix_MtH_zero": np.array_equal(M.T @ H, np.zeros((45, 40), dtype=int)),
        "all_ones_zero": np.array_equal(H @ np.ones((40, 1), dtype=int), np.zeros((40, 1), dtype=int)),
    }

    result = {
        "theorem": "BT771 Null 15-Sector Kernel Theorem",
        "kernel": {
            "formula": "H_15 = 8I - 4A_W33 + J",
            "entries": {"diagonal": 9, "W33_adjacent": -3, "W33_nonadjacent": 1},
            "rank": int(np.linalg.matrix_rank(H)),
            "minimal_idempotent": "E_15 = H_15/24",
            "projector_identity": "H_15^2 = 24 H_15",
            "octet_condition": "H_15 M_octet = 0",
        },
        "spectra": {
            "A_W33": cdict(eig_A),
            "H_15": cdict(eig_H),
        },
        "tight_frame": {
            "vectors": 40,
            "dimension": 15,
            "Gram": "H_15/9",
            "frame_bound": "40/15=8/3",
            "inner_products": {"diagonal": "1", "W33_adjacent": "-1/3", "W33_nonadjacent": "1/9"},
        },
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "boundary": "This identifies the 15-sector as a W33 point-space tight frame and octet-sum null kernel. It does not yet add PG(3,2) labels to the 15 basis directions."
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
