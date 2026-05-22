#!/usr/bin/env python3
"""Decode the 1,3,9,27 X-overlap scheme as flag geometry of W(3,3).

The previous minimal-support theorem identified projective X_min supports with
flags (p,L), where L is a totally isotropic K4 line and p in L.  This script
proves that the unsigned overlap values in U U^T are not mysterious spectral
numbers: they are determined exactly by the relative position of two flags.

For ordered distinct flags f=(p,L), g=(q,M):

  overlap 27: same point or same line;
  overlap  9: one cross-incidence, p in M or q in L, but not same line;
  overlap  3: lines meet away from both flagged points, or L,M skew while p,q
              are collinear;
  overlap  1: L,M skew and p,q are noncollinear.

Per fixed flag this gives 6,18,54,81 neighbours respectively, matching the
projective 3-adic scheme 27^6, 9^18, 3^54, 1^81.
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
    adjacency = [[False] * len(points) for _ in points]
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
    flags = [(p, li) for li, L in enumerate(lines) for p in L]
    return points, edges, adjacency, lines, flags


def classify_pair(flag_a, flag_b, lines, adjacency):
    p, li = flag_a
    q, mj = flag_b
    if flag_a == flag_b:
        return "same_flag"
    L = set(lines[li])
    M = set(lines[mj])
    if p == q:
        return "same_point"
    if li == mj:
        return "same_line"
    if q in L and p not in M:
        return "q_on_L_cross_incidence"
    if p in M and q not in L:
        return "p_on_M_cross_incidence"
    if L & M:
        return "lines_meet_elsewhere"
    if adjacency[p][q]:
        return "skew_lines_flag_points_collinear"
    return "skew_lines_flag_points_noncollinear"


def predicted_overlap(relation: str) -> int:
    if relation in {"same_point", "same_line"}:
        return 27
    if relation in {"q_on_L_cross_incidence", "p_on_M_cross_incidence"}:
        return 9
    if relation in {"lines_meet_elsewhere", "skew_lines_flag_points_collinear"}:
        return 3
    if relation == "skew_lines_flag_points_noncollinear":
        return 1
    raise ValueError(relation)


def main() -> int:
    points, edges, adjacency, lines, flags = build_geometry()
    relation_counts_ordered = Counter()
    overlap_counts_ordered = Counter()
    per_flag_overlap = defaultdict(Counter)
    relation_to_overlap = defaultdict(Counter)

    for i, f in enumerate(flags):
        for j, g in enumerate(flags):
            if i == j:
                continue
            rel = classify_pair(f, g, lines, adjacency)
            ov = predicted_overlap(rel)
            relation_counts_ordered[rel] += 1
            overlap_counts_ordered[ov] += 1
            per_flag_overlap[i][ov] += 1
            relation_to_overlap[rel][ov] += 1

    per_flag_patterns = Counter(tuple(sorted(c.items())) for c in per_flag_overlap.values())
    expected_per_flag = ((1, 81), (3, 54), (9, 18), (27, 6))
    checks = {
        "point_line_flag_count": len(points) == 40 and len(lines) == 40 and len(flags) == 160,
        "ordered_relation_total": sum(relation_counts_ordered.values()) == 160*159,
        "overlap_distribution_ordered": overlap_counts_ordered == Counter({1: 12960, 3: 8640, 9: 2880, 27: 960}),
        "per_flag_pattern": per_flag_patterns == Counter({expected_per_flag: 160}),
        "relations_single_overlap_value": all(len(c) == 1 for c in relation_to_overlap.values()),
    }

    payload = {
        "theorem_name": "W33 Flag Overlap Association Theorem",
        "summary": {
            "points": len(points),
            "lines": len(lines),
            "flags": len(flags),
            "per_flag_overlap_pattern": dict(expected_per_flag),
            "all_checks_passed": all(checks.values()),
        },
        "relation_counts_ordered": dict(relation_counts_ordered),
        "relation_to_overlap_ordered": {k: dict(v) for k, v in relation_to_overlap.items()},
        "overlap_counts_ordered": dict(overlap_counts_ordered),
        "overlap_counts_unordered": {str(k): v//2 for k, v in sorted(overlap_counts_ordered.items())},
        "per_flag_patterns": {str(k): v for k, v in per_flag_patterns.items()},
        "checks": checks,
        "interpretation": "The 3-adic overlap value is a flag-distance invariant on the point-line flags of the generalized quadrangle W(3,3).",
    }
    root = Path(__file__).resolve().parents[1]
    out = root / "data" / "w33_flag_overlap_scheme.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    return 0 if payload["summary"]["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
