#!/usr/bin/env python3
"""Compute automorphism group of the 6x6 Gram matrix for Coxeter-6 orbits."""

from __future__ import annotations

import json
from itertools import permutations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def cartan_e8():
    return [
        [2, -1, 0, 0, 0, 0, 0, 0],
        [-1, 2, -1, 0, 0, 0, 0, 0],
        [0, -1, 2, -1, 0, 0, 0, -1],
        [0, 0, -1, 2, -1, 0, 0, 0],
        [0, 0, 0, -1, 2, -1, 0, 0],
        [0, 0, 0, 0, -1, 2, -1, 0],
        [0, 0, 0, 0, 0, -1, 2, 0],
        [0, 0, -1, 0, 0, 0, 0, 2],
    ]


def ip_e8(r, s, C):
    return sum(r[i] * C[i][j] * s[j] for i in range(8) for j in range(8))


def gram(orbit, C):
    m = [[0] * 6 for _ in range(6)]
    for i in range(6):
        for j in range(6):
            m[i][j] = ip_e8(orbit[i], orbit[j], C)
    return m


def is_aut(perm, G):
    # check if G[i][j] == G[p[i]][p[j]]
    for i in range(6):
        for j in range(6):
            if G[i][j] != G[perm[i]][perm[j]]:
                return False
    return True


def main():
    data = json.loads((ROOT / "artifacts" / "e8_coxeter6_orbits.json").read_text())
    orbits = data["orbits"]
    C = cartan_e8()

    sizes = []
    for o_idx, orb in enumerate(orbits):
        G = gram(orb, C)
        auts = []
        for perm in permutations(range(6)):
            if is_aut(perm, G):
                auts.append(perm)
        sizes.append(len(auts))

    out = {
        "orbit_aut_sizes": sizes,
        "unique_sizes": sorted(set(sizes)),
        "count_by_size": {str(s): sizes.count(s) for s in set(sizes)},
    }
    out_path = ROOT / "artifacts" / "orbit_gram_auts.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(out)
    print("Wrote", out_path)


if __name__ == "__main__":
    main()
