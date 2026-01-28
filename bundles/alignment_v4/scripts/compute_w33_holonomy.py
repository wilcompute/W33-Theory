#!/usr/bin/env python3
"""Compute W33 triad center counts + Z12 holonomy from ray overlaps.

Inputs (relative to repo root):
- data/_workbench/02_geometry/W33_line_phase_map.csv
- data/_toe/w33_orthonormal_phase_solution_20260110/W33_point_rays_C4_complex.csv

Outputs written next to this script if run standalone.
"""

from __future__ import annotations

import cmath
import itertools
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
W33_LINES = ROOT / "data/_workbench/02_geometry/W33_line_phase_map.csv"
W33_RAYS = (
    ROOT
    / "data/_toe/w33_orthonormal_phase_solution_20260110/W33_point_rays_C4_complex.csv"
)


def sym_to_int(ch: str) -> int:
    if ch == "a":
        return 10
    if ch == "b":
        return 11
    return int(ch)


def main() -> None:
    df = pd.read_csv(W33_LINES)
    df["pts"] = df["point_ids"].astype(str).apply(lambda s: [int(x) for x in s.split()])
    lines = [tuple(sorted(pts)) for pts in df["pts"]]

    points = sorted(set(p for pts in lines for p in pts))
    col = {p: set() for p in points}
    for pts in lines:
        for a, b in itertools.combinations(pts, 2):
            col[a].add(b)
            col[b].add(a)

    noncol = {p: set(points) - {p} - col[p] for p in points}

    triads = []
    for a in range(40):
        for b in [x for x in noncol[a] if x > a]:
            for c in [x for x in noncol[a].intersection(noncol[b]) if x > b]:
                triads.append((a, b, c))

    def centers(t):
        a, b, c = t
        return col[a].intersection(col[b]).intersection(col[c])

    center_hist = Counter(len(centers(t)) for t in triads)
    special = [t for t in triads if len(centers(t)) == 4]

    rays = pd.read_csv(W33_RAYS).sort_values("point_id")
    V = np.vstack(
        [
            rays[f"v{i}"]
            .apply(lambda s: complex(str(s).replace(" ", "").replace("+-", "-")))
            .to_numpy()
            for i in range(4)
        ]
    ).T

    def inner(a, b):
        return np.vdot(V[a], V[b])

    roots = [cmath.exp(1j * math.pi / 6 * k) for k in range(12)]

    def quantize(z):
        u = z / abs(z)
        d = [abs(u - r) for r in roots]
        k = int(np.argmin(d))
        return k

    edge_k = {}
    for a in range(40):
        for b in noncol[a]:
            edge_k[(a, b)] = quantize(inner(a, b))

    hol_hist = Counter()
    hol_by_center = Counter()
    for a, b, c in triads:
        h = (edge_k[(a, b)] + edge_k[(b, c)] + edge_k[(c, a)]) % 12
        cc = len(centers((a, b, c)))
        hol_hist[h] += 1
        hol_by_center[(cc, h)] += 1

    out = {
        "num_noncollinear_triads": len(triads),
        "center_hist": {str(k): v for k, v in center_hist.items()},
        "num_four_center_triads": len(special),
        "holonomy_hist_mod12": {str(k): v for k, v in hol_hist.items()},
        "holonomy_by_center_count": {
            f"{cc},{h}": v for (cc, h), v in hol_by_center.items()
        },
    }
    from utils.json_safe import dumps

    print(dumps(out, indent=2))


if __name__ == "__main__":
    main()
