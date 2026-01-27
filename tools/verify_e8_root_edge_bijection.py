#!/usr/bin/env python3
"""Verify the root->edge mapping against W33 edges.

Exit non-zero if any check fails.
"""
from __future__ import annotations

import json
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build_w33_edges():
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

    def omega(x, y):
        return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3

    edges = set()
    for i in range(len(proj_points)):
        for j in range(i + 1, len(proj_points)):
            if omega(proj_points[i], proj_points[j]) == 0:
                edges.add((i, j))
    return edges


def main():
    src = ROOT / "artifacts_archive" / "e8_root_to_w33_edge.json"
    if not src.exists():
        raise SystemExit("Missing artifacts_archive/e8_root_to_w33_edge.json")

    data = json.loads(src.read_text(encoding="utf-8"))
    root_to_edge = data.get("root_to_edge", {})
    if len(root_to_edge) != 240:
        raise SystemExit(f"Expected 240 roots, got {len(root_to_edge)}")

    edges = set()
    for edge in root_to_edge.values():
        if not isinstance(edge, list) or len(edge) != 2:
            raise SystemExit(f"Invalid edge entry: {edge}")
        a, b = edge
        if a == b:
            raise SystemExit(f"Self-edge: {edge}")
        edges.add(tuple(sorted((a, b))))

    if len(edges) != 240:
        raise SystemExit(f"Expected 240 edges, got {len(edges)}")

    w33_edges = build_w33_edges()
    if edges != w33_edges:
        missing = w33_edges - edges
        extra = edges - w33_edges
        raise SystemExit(f"Edge mismatch: missing {len(missing)}, extra {len(extra)}")

    print("OK: root->edge mapping matches W33 edges")


if __name__ == "__main__":
    main()
