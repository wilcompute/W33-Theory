#!/usr/bin/env python3
"""Compute support-size distribution (nonzero coordinates) per pattern class."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build_points():
    F3 = [0, 1, 2]
    vectors = [v for v in product(F3, repeat=4) if any(x != 0 for x in v)]
    points = []
    seen = set()
    for v in vectors:
        v = list(v)
        for i in range(4):
            if v[i] != 0:
                inv = 1 if v[i] == 1 else 2
                v = tuple((x * inv) % 3 for x in v)
                break
        if v not in seen:
            seen.add(v)
            points.append(v)
    return points


def pattern_class_by_vertex(points):
    inter = json.loads((ROOT / "artifacts" / "we6_coxeter6_intersection.json").read_text())
    orbit_map = json.loads((ROOT / "artifacts" / "e8_orbit_to_f3_point.json").read_text())
    mapping = orbit_map["mapping"]

    patterns = [tuple(row) for row in inter["matrix"]]
    pat_ids = {}
    for row in patterns:
        if row not in pat_ids:
            pat_ids[row] = len(pat_ids)

    orbit_class = {i: pat_ids[patterns[i]] for i in range(40)}
    point_to_orbit = {tuple(v): int(k) for k, v in mapping.items()}

    class_by_vertex = []
    for p in points:
        oid = point_to_orbit[p]
        class_by_vertex.append(orbit_class[oid])
    return class_by_vertex


def main():
    points = build_points()
    class_by_vertex = pattern_class_by_vertex(points)

    support = defaultdict(Counter)
    for p, c in zip(points, class_by_vertex):
        s = sum(1 for x in p if x != 0)
        support[c][s] += 1

    out = {str(c): dict(cnt) for c, cnt in support.items()}
    (ROOT / "artifacts" / "pattern_class_support_sizes.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )
    print(out)
    print("Wrote artifacts/pattern_class_support_sizes.json")


if __name__ == "__main__":
    main()
