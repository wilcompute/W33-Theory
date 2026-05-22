#!/usr/bin/env python3
"""Decode the Z-side 0,1,2,3,4 distribution as quadrangle flag incidence.

After the support-geometry theorem:
  X_min = flags (p,L) of W(3,3)
  Z_min = ordinary quadrangles Q

A quadrangle Q has four cycle edges.  Each edge lies on a unique isotropic line,
and each endpoint gives one point-line flag.  Therefore Q naturally determines
an 8-element incident-flag set F(Q).

This script verifies:
  overlap_Z(Q,Q') = |F(Q) cap F(Q')|.
For every fixed Q, the distribution over the other 1619 quadrangles is:
  0^1187, 1^288, 2^96, 3^32, 4^16.

It also refines these counts by vertex/edge/diagonal intersection signatures.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path

P = 3
Vec = tuple[int, int, int, int]


def canonical(v) -> Vec:
    vv = tuple(int(x) % P for x in v)
    if vv == (0, 0, 0, 0):
        raise ValueError("zero vector")
    for x in vv:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % P for y in vv)  # type: ignore[return-value]
    raise AssertionError


def omega(u: Vec, v: Vec) -> int:
    return (u[0]*v[2] - u[2]*v[0] + u[1]*v[3] - u[3]*v[1]) % P


def build_geometry():
    points = []
    seen = set()
    for raw in product(range(P), repeat=4):
        if raw == (0, 0, 0, 0):
            continue
        c = canonical(raw)
        if c not in seen:
            seen.add(c)
            points.append(c)
    point_index = {p: i for i, p in enumerate(points)}
    edges = [(i, j) for i, j in combinations(range(len(points)), 2) if omega(points[i], points[j]) == 0]
    edge_index = {e: k for k, e in enumerate(edges)}
    adjacency = [[False]*len(points) for _ in points]
    for i, j in edges:
        adjacency[i][j] = adjacency[j][i] = True
    lines = set()
    for i, j in edges:
        u, v = points[i], points[j]
        line = set()
        for a, b in product(range(P), repeat=2):
            if a == 0 and b == 0:
                continue
            line.add(point_index[canonical((a*u[t] + b*v[t] for t in range(4)))])
        lines.add(tuple(sorted(line)))
    lines = sorted(lines)
    edge_to_line = {}
    for li, L in enumerate(lines):
        for e in combinations(L, 2):
            edge_to_line[tuple(sorted(e))] = li
    return points, edges, edge_index, adjacency, lines, edge_to_line


def quadrangles(points, edges, edge_index, adjacency):
    quads = {}
    for a, b in combinations(range(len(points)), 2):
        if adjacency[a][b]:
            continue
        common = [x for x in range(len(points)) if adjacency[a][x] and adjacency[b][x]]
        for c, d in combinations(common, 2):
            cycle_edges = tuple(sorted(tuple(sorted(e)) for e in ((a, c), (c, b), (b, d), (d, a))))
            key = cycle_edges
            if key in quads:
                continue
            verts = tuple(sorted((a, b, c, d)))
            graph_edges = tuple(sorted(tuple(sorted((u, v))) for u, v in combinations(verts, 2) if adjacency[u][v]))
            diagonals = tuple(sorted(tuple(sorted((u, v))) for u, v in combinations(verts, 2) if not adjacency[u][v]))
            quads[key] = {"vertices": verts, "graph_edges": graph_edges, "diagonals": diagonals, "cycle_edges": cycle_edges}
    return list(quads.values())


def incident_flags(q, edge_to_line):
    flags = set()
    for u, v in q["cycle_edges"]:
        li = edge_to_line[tuple(sorted((u, v)))]
        flags.add((u, li))
        flags.add((v, li))
    return frozenset(flags)


def signature(q, r):
    return (
        len(set(q["vertices"]) & set(r["vertices"])),
        len(set(q["cycle_edges"]) & set(r["cycle_edges"])),
        len(set(q["diagonals"]) & set(r["diagonals"])),
    )


def main() -> int:
    points, edges, edge_index, adjacency, lines, edge_to_line = build_geometry()
    quads = quadrangles(points, edges, edge_index, adjacency)
    flag_sets = [incident_flags(q, edge_to_line) for q in quads]
    overlap_counts_ordered = Counter()
    per_quad_patterns = Counter()
    signature_by_overlap = defaultdict(Counter)

    for i, q in enumerate(quads):
        row = Counter()
        for j, r in enumerate(quads):
            if i == j:
                continue
            ov = len(flag_sets[i] & flag_sets[j])
            row[ov] += 1
            overlap_counts_ordered[ov] += 1
            signature_by_overlap[ov][signature(q, r)] += 1
        per_quad_patterns[tuple(sorted(row.items()))] += 1

    expected = ((0, 1187), (1, 288), (2, 96), (3, 32), (4, 16))
    checks = {
        "w33_geometry": len(points) == 40 and len(edges) == 240 and len(lines) == 40,
        "quadrangle_count": len(quads) == 1620,
        "each_quadrangle_has_8_incident_flags": Counter(len(s) for s in flag_sets) == Counter({8: 1620}),
        "per_quad_pattern": per_quad_patterns == Counter({expected: 1620}),
        "ordered_overlap_distribution": overlap_counts_ordered == Counter({0: 1922940, 1: 466560, 2: 155520, 3: 51840, 4: 25920}),
    }
    payload = {
        "theorem_name": "W33 Quadrangle Dual Visibility Theorem",
        "summary": {
            "points": len(points),
            "lines": len(lines),
            "edges": len(edges),
            "quadrangles": len(quads),
            "incident_flags_per_quadrangle": 8,
            "per_quadrangle_overlap_pattern": dict(expected),
            "all_checks_passed": all(checks.values()),
        },
        "overlap_counts_ordered": dict(overlap_counts_ordered),
        "overlap_counts_unordered": {str(k): v//2 for k, v in sorted(overlap_counts_ordered.items())},
        "signature_by_overlap_ordered": {
            str(k): {str(sig): int(c) for sig, c in sorted(v.items())}
            for k, v in sorted(signature_by_overlap.items())
        },
        "checks": checks,
        "interpretation": "The Z-side distribution is the intersection distribution of 8-flag boundary sets of ordinary quadrangles.",
    }
    root = Path(__file__).resolve().parents[1]
    out = root / "data" / "w33_quadrangle_dual_visibility_scheme.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    return 0 if payload["summary"]["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
