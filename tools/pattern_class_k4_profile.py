#!/usr/bin/env python3
"""Analyze how W(E6) pattern classes distribute across K4 components.

Outputs:
- artifacts/pattern_class_k4_profile.json
"""
from __future__ import annotations

import csv
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


def load_lines():
    path = ROOT / "data/_workbench/02_geometry/W33_line_phase_map.csv"
    lines = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pts = tuple(map(int, str(row['point_ids']).split()))
            lines.append(pts)
    return lines


def pattern_class_by_vertex():
    inter = json.loads((ROOT / "artifacts" / "we6_coxeter6_intersection.json").read_text())
    orbit_map = json.loads((ROOT / "artifacts" / "e8_orbit_to_f3_point.json").read_text())
    mapping = orbit_map["mapping"]

    # pattern rows for orbits
    patterns = [tuple(row) for row in inter["matrix"]]
    pat_ids = {}
    for row in patterns:
        if row not in pat_ids:
            pat_ids[row] = len(pat_ids)

    orbit_class = {i: pat_ids[patterns[i]] for i in range(40)}
    point_to_orbit = {tuple(v): int(k) for k, v in mapping.items()}

    points = build_points()
    class_by_vertex = []
    for p in points:
        oid = point_to_orbit[p]
        class_by_vertex.append(orbit_class[oid])
    return class_by_vertex


def compute_k4_components():
    points = build_points()
    lines = load_lines()

    col = defaultdict(set)
    for L in lines:
        for p in L:
            col[p].update(L)
            col[p].discard(p)

    noncol = defaultdict(set)
    for p in range(40):
        for q in range(40):
            if p != q and q not in col[p]:
                noncol[p].add(q)

    k4_list = []
    for a in range(40):
        for b in noncol[a]:
            if b <= a:
                continue
            for c in noncol[a] & noncol[b]:
                if c <= b:
                    continue
                for d in noncol[a] & noncol[b] & noncol[c]:
                    if d <= c:
                        continue
                    common = col[a] & col[b] & col[c] & col[d]
                    if len(common) == 4:
                        k4_list.append(((a,b,c,d), tuple(sorted(common))))
    return k4_list


def main():
    class_by_vertex = pattern_class_by_vertex()
    k4_list = compute_k4_components()

    outer_class_multisets = Counter()
    center_class_multisets = Counter()
    outer_class_counts = Counter()
    center_class_counts = Counter()

    for outer, center in k4_list:
        o_classes = tuple(sorted([class_by_vertex[v] for v in outer]))
        c_classes = tuple(sorted([class_by_vertex[v] for v in center]))
        outer_class_multisets[o_classes] += 1
        center_class_multisets[c_classes] += 1
        for v in outer:
            outer_class_counts[class_by_vertex[v]] += 1
        for v in center:
            center_class_counts[class_by_vertex[v]] += 1

    out = {
        "k4_count": len(k4_list),
        "outer_class_multisets": {str(k): v for k, v in outer_class_multisets.items()},
        "center_class_multisets": {str(k): v for k, v in center_class_multisets.items()},
        "outer_class_counts": dict(outer_class_counts),
        "center_class_counts": dict(center_class_counts),
    }

    (ROOT / "artifacts" / "pattern_class_k4_profile.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )
    print("Wrote artifacts/pattern_class_k4_profile.json")


if __name__ == "__main__":
    main()
