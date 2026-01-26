#!/usr/bin/env python3
"""Analyze the configuration from hit lines augmented by the 7 lines through the missing point.

Outputs:
- artifacts/witting_pg32_augmented_lines_analysis.json
- artifacts/witting_pg32_augmented_lines_analysis.md
"""
from __future__ import annotations

import json
from itertools import combinations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "witting_pg32_augmented_lines_analysis.json"
OUT_MD = ROOT / "artifacts" / "witting_pg32_augmented_lines_analysis.md"

# GF(4) arithmetic
def gf4_add(a: int, b: int) -> int:
    return a ^ b

def gf4_mul(a: int, b: int) -> int:
    if a == 0 or b == 0:
        return 0
    a0, a1 = a & 1, (a >> 1) & 1
    b0, b1 = b & 1, (b >> 1) & 1
    c0 = a0 * b0
    c1 = a0 * b1 + a1 * b0
    c2 = a1 * b1
    c0 = (c0 + c2) % 2
    c1 = (c1 + c2) % 2
    return (c1 << 1) | c0

def gf4_square(a: int) -> int:
    return gf4_mul(a, a)

def gf4_trace(a: int) -> int:
    return gf4_add(a, gf4_square(a)) & 1

def gf4_inv(a: int) -> int:
    if a == 0:
        raise ZeroDivisionError
    for b in [1, 2, 3]:
        if gf4_mul(a, b) == 1:
            return b
    raise ZeroDivisionError

omega = 2
omega2 = 3
omega_powers = [1, omega, omega2]

def build_base_states():
    states = []
    for i in range(4):
        v = [0, 0, 0, 0]
        v[i] = 1
        states.append(tuple(v))
    for mu, nu in product(range(3), repeat=2):
        w_mu = omega_powers[mu]
        w_nu = omega_powers[nu]
        states.append((0, 1, w_mu, w_nu))
        states.append((1, 0, w_mu, w_nu))
        states.append((1, w_mu, 0, w_nu))
        states.append((1, w_mu, w_nu, 0))
    return states

def normalize_projective(v):
    for x in v:
        if x != 0:
            inv = gf4_inv(x)
            return tuple(gf4_mul(inv, xi) for xi in v)
    return None

def trace_map(v):
    return tuple(gf4_trace(x) for x in v)

def build_pg32_points():
    return [v for v in product([0, 1], repeat=4) if v != (0, 0, 0, 0)]

def build_pg32_lines(points):
    lines = set()
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            p = points[i]
            q = points[j]
            r = tuple((pi ^ qi) for pi, qi in zip(p, q))
            line = tuple(sorted([p, q, r]))
            lines.add(line)
    return sorted(lines)

def main():
    base_states = [normalize_projective(s) for s in build_base_states()]
    base_states = list(dict.fromkeys(base_states))
    scalars = [1, omega, omega2]
    ray_images = []
    for s in base_states:
        imgs = set()
        for c in scalars:
            scaled = tuple(gf4_mul(c, x) for x in s)
            p = trace_map(scaled)
            if p != (0, 0, 0, 0):
                imgs.add(p)
        ray_images.append(tuple(sorted(imgs)))

    pg_points = build_pg32_points()
    pg_lines = build_pg32_lines(pg_points)
    pg_line_set = {tuple(sorted(line)) for line in pg_lines}

    hit_lines = sorted(set(tuple(im) for im in ray_images if len(im) == 3 and tuple(im) in pg_line_set))

    # missing point
    covered = set(p for line in hit_lines for p in line)
    missing = [p for p in pg_points if p not in covered]
    missing_pt = missing[0] if missing else None

    # lines through missing point
    lines_through_missing = []
    if missing_pt is not None:
        for line in pg_lines:
            if missing_pt in line:
                lines_through_missing.append(line)

    augmented = sorted(set(hit_lines + lines_through_missing))

    # incidence stats
    point_cover = {p: 0 for p in pg_points}
    for line in augmented:
        for p in line:
            point_cover[p] += 1

    # line intersection degrees (adjacent if intersect)
    n = len(augmented)
    adj_deg = [0] * n
    for i, j in combinations(range(n), 2):
        if len(set(augmented[i]) & set(augmented[j])) == 1:
            adj_deg[i] += 1
            adj_deg[j] += 1

    summary = {
        "hit_lines": len(hit_lines),
        "missing_point": missing_pt,
        "lines_through_missing": len(lines_through_missing),
        "augmented_lines": len(augmented),
        "point_cover_counts": {str(k): list(point_cover.values()).count(k) for k in sorted(set(point_cover.values()))},
        "line_intersection_degree_set": sorted(set(adj_deg)),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    lines = []
    lines.append("# Augmented Hit-Line Configuration (add lines through missing point)")
    lines.append("")
    lines.append(f"- hit lines: {summary['hit_lines']}")
    lines.append(f"- missing point: {summary['missing_point']}")
    lines.append(f"- lines through missing: {summary['lines_through_missing']}")
    lines.append(f"- augmented lines: {summary['augmented_lines']}")
    lines.append(f"- point cover counts: {summary['point_cover_counts']}")
    lines.append(f"- line intersection degree set: {summary['line_intersection_degree_set']}")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")

if __name__ == "__main__":
    main()
