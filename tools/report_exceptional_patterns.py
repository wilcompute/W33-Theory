#!/usr/bin/env python3
"""Report Coxeter‑6 orbits that intersect W(E6) size‑1 roots (exceptional patterns)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    inter = json.loads(
        (ROOT / "artifacts" / "we6_coxeter6_intersection.json").read_text()
    )
    orbit_map = json.loads(
        (ROOT / "artifacts" / "e8_orbit_to_f3_point.json").read_text()
    )
    mapping = orbit_map["mapping"]

    matrix = inter["matrix"]
    # size-1 orbits are columns 7..12 (after 72 + 6x27)
    # We flag any row with a 1 in these columns.
    exceptional = []
    for i, row in enumerate(matrix):
        if any(row[j] == 1 for j in range(7, 13)):
            exceptional.append((i, row))

    print(f"Exceptional Coxeter‑6 orbits (involving size‑1 roots): {len(exceptional)}")
    for i, row in exceptional:
        point = mapping[str(i)]
        print(f"  orbit {i}: row={row}  point={point}")

    # Build adjacency among exceptional points in W33
    points = [
        tuple(item[2]) if len(item) > 2 else tuple(mapping[str(item[0])]) for item in []
    ]  # placeholder
    pts = [tuple(mapping[str(i)]) for i, _ in exceptional]

    def omega(p, q):
        return (p[0] * q[2] - p[2] * q[0] + p[1] * q[3] - p[3] * q[1]) % 3

    adj_pairs = []
    for a in range(len(pts)):
        for b in range(a + 1, len(pts)):
            adj_pairs.append(
                {
                    "pair": [pts[a], pts[b]],
                    "omega": omega(pts[a], pts[b]),
                    "adjacent": omega(pts[a], pts[b]) == 0,
                }
            )

    out = {
        "exceptional_orbits": [
            {"orbit": i, "row": row, "point": mapping[str(i)]} for i, row in exceptional
        ],
        "adjacency_pairs": adj_pairs,
    }
    (ROOT / "artifacts" / "exceptional_we6_patterns.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )
    print("Wrote artifacts/exceptional_we6_patterns.json")


if __name__ == "__main__":
    main()
