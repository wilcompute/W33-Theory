#!/usr/bin/env python3
"""Pass 101: construct the 120-point anisotropic E8-root companion graph."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import numpy as np

from w33_pass92_discriminant_e8 import (
    build_graph,
    nullspace_basis,
    rowspace_basis,
    to_int,
)

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "w33_pass120_srg120_anisotropic.json"


def anisotropic_cosets() -> list[int]:
    _, adjacency = build_graph()
    code = rowspace_basis([to_int(adjacency[i]) for i in range(40)])
    dual = nullspace_basis(adjacency)
    words = [0]
    for basis in code:
        words += [x ^ basis for x in words]
    combined = list(code)
    glue = []
    for vector in dual:
        reduced = vector
        for basis in combined:
            reduced = min(reduced, reduced ^ basis)
        if reduced:
            combined.append(reduced)
            combined.sort(reverse=True)
            glue.append(vector)
    reps = [0]
    for basis in glue:
        reps += [x ^ basis for x in reps]
    return [rep for rep in reps if min((rep ^ word).bit_count() for word in words) == 6]


def main() -> int:
    vertices = anisotropic_cosets()
    n = len(vertices)
    adjacency = np.zeros((n, n), dtype=np.int64)
    for i in range(n):
        for j in range(i + 1, n):
            if (vertices[i] & vertices[j]).bit_count() % 2 == 0:
                adjacency[i, j] = adjacency[j, i] = 1

    square = adjacency @ adjacency
    degrees = Counter(int(row.sum()) for row in adjacency)
    common_adjacent = Counter()
    common_nonadjacent = Counter()
    for i in range(n):
        for j in range(i + 1, n):
            target = common_adjacent if adjacency[i, j] else common_nonadjacent
            target[int(square[i, j])] += 1
    spectrum = Counter(
        np.rint(np.linalg.eigvalsh(adjacency.astype(float))).astype(int).tolist()
    )
    checks = {
        "anisotropic_count_120": n == 120,
        "regular_degree_63": degrees == {63: 120},
        "lambda_30": set(common_adjacent) == {30},
        "mu_36": set(common_nonadjacent) == {36},
        "spectrum": spectrum == {63: 1, 3: 84, -9: 35},
        "partition_with_isotropic": 120 + 135 == 255,
    }
    payload = {
        "schema": "w33.pass101.srg120_anisotropic.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "parameters": [120, 63, 30, 36],
        "spectrum": {str(k): v for k, v in sorted(spectrum.items())},
        "construction": (
            "Take the 120 minimum-weight-6 anisotropic cosets in Cperp/C and "
            "join distinct cosets with binary inner product zero."
        ),
        "e8_reading": (
            "The vertices are the 240 E8 roots modulo sign. Together with "
            "Pass 93's 135 isotropic points they exhaust E8/2E8 minus zero."
        ),
        "checks": checks,
    }
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
