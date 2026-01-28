#!/usr/bin/env python3
"""Lift the canonical Z3 phase to the full W33 edge->E8 root map.

For each W33 edge, compute endpoint phases from F3^4 coordinate x4.
Using the explicit edge->root map and W(E6) orbit labels, summarize phase
pair distributions per orbit type (72, 27_i, 1_i).
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build_w33():
    F3 = [0, 1, 2]
    vectors = [v for v in product(F3, repeat=4) if any(x != 0 for x in v)]

    proj_points = []
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
            proj_points.append(v)

    n = len(proj_points)

    def omega(x, y):
        return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3

    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if omega(proj_points[i], proj_points[j]) == 0:
                edges.append((i, j))

    return proj_points, edges


def main():
    # Load mappings
    edge_map = json.loads(
        (ROOT / "artifacts" / "explicit_bijection_decomposition.json").read_text()
    )
    edge_to_root_idx = {int(k): v for k, v in edge_map["edge_to_root_index"].items()}
    root_coords = [tuple(r) for r in edge_map["root_coords"]]

    we6 = json.loads((ROOT / "artifacts" / "we6_orbit_labels.json").read_text())
    root_to_orbit = {eval(k): v for k, v in we6["mapping"].items()}

    # W33 vertices and phases
    points, edges = build_w33()
    edge_to_idx = {tuple(sorted(e)): i for i, e in enumerate(edges)}
    v_phase = {i: points[i][3] % 3 for i in range(len(points))}

    # Accumulators
    per_orbit = defaultdict(lambda: Counter())
    per_orbit_sum = defaultdict(lambda: Counter())
    per_orbit_diff = defaultdict(lambda: Counter())

    type_counts = Counter()

    for e in edges:
        eidx = edge_to_idx[tuple(sorted(e))]
        ridx = edge_to_root_idx[eidx]
        r = root_coords[ridx]
        info = root_to_orbit.get(r)
        if info is None:
            # try scaled? (some coords may be lists)
            info = root_to_orbit.get(tuple(int(x) for x in r))
        if info is None:
            continue
        orbit_id = info["orbit_id"]
        orbit_size = info["orbit_size"]
        orbit_key = f"{orbit_size}_{orbit_id}"

        a, b = v_phase[e[0]], v_phase[e[1]]
        pair = tuple(sorted((a, b)))
        per_orbit[orbit_key][pair] += 1
        per_orbit_sum[orbit_key][(a + b) % 3] += 1
        per_orbit_diff[orbit_key][(a - b) % 3] += 1
        type_counts[orbit_size] += 1

    # summarize by orbit size
    size_summary = defaultdict(lambda: Counter())
    size_sum = defaultdict(lambda: Counter())
    size_diff = defaultdict(lambda: Counter())

    for k, cnt in per_orbit.items():
        size = int(k.split("_")[0])
        size_summary[size] += cnt
        size_sum[size] += per_orbit_sum[k]
        size_diff[size] += per_orbit_diff[k]

    # stringify tuple keys for JSON
    def stringify_counter(cnt):
        return {str(k): v for k, v in cnt.items()}

    results = {
        "type_counts": dict(type_counts),
        "per_orbit_pairs": {k: stringify_counter(v) for k, v in per_orbit.items()},
        "per_orbit_sum": {k: stringify_counter(v) for k, v in per_orbit_sum.items()},
        "per_orbit_diff": {k: stringify_counter(v) for k, v in per_orbit_diff.items()},
        "size_summary_pairs": {
            str(k): stringify_counter(v) for k, v in size_summary.items()
        },
        "size_summary_sum": {str(k): stringify_counter(v) for k, v in size_sum.items()},
        "size_summary_diff": {
            str(k): stringify_counter(v) for k, v in size_diff.items()
        },
    }

    out_path = ROOT / "artifacts" / "su3_phase_edge_lift.json"
    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(results["type_counts"])
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
