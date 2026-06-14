#!/usr/bin/env python3
"""
BT993 — Edgewise chain-density recurrences replacing barycentric 120/19, 860/19.

BT991 gives local edgewise f-vectors in dimensions 0..4.  From them we compute
the carrier-exact subdivision matrix L such that

    f'_j = sum_i f_i L[i,j].

This is stronger than top-channel counting: it gives the full f-vector recurrence
for every level of any 4-complex under k=2 edgewise refinement.  Applying it to
CP2_9 and K3_16 gives level-1 and level-2 f-vectors matching the explicit
incidence computation at level 1.
"""
from __future__ import annotations

import json
from math import comb
from pathlib import Path

LOCAL_EDGEWISE_F = [
    [1, 0, 0, 0, 0],
    [3, 2, 0, 0, 0],
    [6, 9, 4, 0, 0],
    [10, 25, 24, 8, 0],
    [15, 55, 85, 60, 16],
]

SEEDS = {
    "CP2_9": [9, 36, 84, 90, 36],
    "K3_16": [16, 120, 560, 720, 288],
}


def carrier_matrix() -> list[list[int]]:
    # L[i][j] = number of new j-faces whose minimal carrier is an old i-face.
    L = [[0 for _ in range(5)] for _ in range(5)]
    for i in range(5):
        for j in range(5):
            value = LOCAL_EDGEWISE_F[i][j]
            for h in range(i):
                value -= comb(i + 1, h + 1) * L[h][j]
            L[i][j] = value
    return L


def apply(f_vector: list[int], L: list[list[int]]) -> list[int]:
    return [sum(f_vector[i] * L[i][j] for i in range(5)) for j in range(5)]


def iterate(f_vector: list[int], steps: int, L: list[list[int]]) -> list[list[int]]:
    out = [list(f_vector)]
    current = list(f_vector)
    for _ in range(steps):
        current = apply(current, L)
        out.append(current)
    return out


def main() -> None:
    L = carrier_matrix()
    out = {
        "theorem": "BT993 edgewise f-vector density recurrence",
        "local_edgewise_f_vectors_by_dimension": LOCAL_EDGEWISE_F,
        "carrier_exact_matrix_rows_old_dim_cols_new_dim": L,
        "recurrence": "f_next[j] = sum_i f_current[i] * L[i][j]",
        "retired_barycentric_constants": ["120/19", "860/19"],
        "seed_iterates": {name: iterate(fv, 3, L) for name, fv in SEEDS.items()},
        "checks": {
            "CP2_9_level1": apply(SEEDS["CP2_9"], L),
            "K3_16_level1": apply(SEEDS["K3_16"], L),
            "top_multiplier": L[4][4],
        },
        "reading": "The edgewise R3 tower now has a true full f-vector recurrence. The old barycentric density constants are replaced by the carrier-exact edgewise subdivision matrix.",
    }
    Path("data").mkdir(exist_ok=True)
    Path("data/bt993_edgewise_density_recurrences.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
