#!/usr/bin/env python3
"""BT772 — PG(3,2)-labeled 15-sector basis theorem.

BT771 identified the null 15-sector as the image of

    H_15 = 8I - 4A_W33 + J.

This verifier puts canonical PG(3,2) labels on a basis of that sector.
Each W33 point is reduced coordinatewise mod 2, giving one of the 15
nonzero vectors of F_2^4, i.e. one point of PG(3,2).  The script chooses
one W33 representative over each PG(3,2) point and proves that the 15
corresponding columns of H_15 form a basis of the null sector.

Boundary: the PG(3,2) labels are a canonical coordinate-label frame from
F_3^4 -> F_2^4 reduction, not a claim that the full Sp(4,3) action factors
through GL(4,2).
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

import networkx as nx
import numpy as np

from bt766_intrinsic_k44_octet_quotient import build_w33
from bt770_octet_nonedge_packet_abi import make_packets

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT772_PG32_LABELED_15_SECTOR_summary.json"


def bit_add(a, b):
    return tuple((x ^ y) for x, y in zip(a, b))


def pg32_points():
    return sorted(v for v in itertools.product([0, 1], repeat=4) if any(v))


def pg32_lines(points):
    point_set = set(points)
    lines = set()
    for a, b in itertools.combinations(points, 2):
        c = bit_add(a, b)
        if c in point_set and c != a and c != b:
            lines.add(tuple(sorted((a, b, c))))
    return sorted(lines)


def main():
    pts, lines, idx, G, point_lines = build_w33()
    A = nx.to_numpy_array(G, nodelist=range(40), dtype=int)
    H = 8 * np.eye(40, dtype=int) - 4 * A + np.ones((40, 40), dtype=int)

    # Octet incidence matrix from BT770 packets.
    packets = make_packets(G)
    M = np.zeros((40, len(packets)), dtype=int)
    for j, packet in enumerate(packets):
        for p in packet["octet"]:
            M[p, j] = 1

    labels = [tuple(x % 2 for x in p) for p in pts]
    label_classes = defaultdict(list)
    for pid, lab in enumerate(labels):
        label_classes[lab].append(pid)

    pg_points = pg32_points()
    pg_lines = pg32_lines(pg_points)

    selected = None
    for choice in itertools.product(*[label_classes[p] for p in pg_points]):
        C = H[:, choice]
        if np.linalg.matrix_rank(C) == 15:
            selected = tuple(choice)
            break
    assert selected is not None
    C = H[:, selected]

    line_count_by_point = Counter()
    pair_count = Counter()
    for L in pg_lines:
        for p in L:
            line_count_by_point[p] += 1
        for a, b in itertools.combinations(L, 2):
            pair_count[tuple(sorted((a, b)))] += 1

    checks = {
        "PG32_has_15_points": len(pg_points) == 15,
        "PG32_has_35_lines": len(pg_lines) == 35,
        "PG32_each_line_3_each_point_7_each_pair_1": all(len(L) == 3 for L in pg_lines)
        and Counter(line_count_by_point.values()) == Counter({7: 15})
        and Counter(pair_count.values()) == Counter({1: 105}),
        "mod2_reduction_hits_all_15_labels": set(label_classes) == set(pg_points),
        "one_representative_per_label": len(selected) == 15 and len({labels[p] for p in selected}) == 15,
        "selected_columns_rank_15": int(np.linalg.matrix_rank(C)) == 15,
        "selected_columns_are_H15_eigenvectors": np.array_equal(H @ C, 24 * C),
        "selected_columns_are_octet_null": np.array_equal(M.T @ C, np.zeros((45, 15), dtype=int)),
        "selected_columns_span_H15_image": int(np.linalg.matrix_rank(np.concatenate([H, C], axis=1))) == 15,
    }

    result = {
        "theorem": "BT772 PG(3,2)-Labeled 15-Sector Basis Theorem",
        "pg32": {
            "points": len(pg_points),
            "lines": len(pg_lines),
            "line_size": 3,
            "lines_per_point": 7,
            "pairs_per_line_closure": 1,
        },
        "labeling": {
            "method": "coordinatewise reduction F_3^4 -> F_2^4 followed by one full-rank representative per nonzero F_2^4 label",
            "label_class_size_distribution": {str(k): int(v) for k, v in sorted(Counter(len(label_classes[p]) for p in pg_points).items())},
            "selected_w33_point_ids": list(selected),
            "selected_pg32_labels": [list(labels[p]) for p in selected],
        },
        "sector": {
            "basis_columns": 15,
            "rank": int(np.linalg.matrix_rank(C)),
            "eigenvalue_under_H15": 24,
            "octet_matrix_condition": "M_octet^T C = 0",
        },
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "boundary": "PG(3,2) supplies canonical labels for an exact 15-column basis of the H15 image. Full group-action equivariance remains a separate target."
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
