#!/usr/bin/env python3
"""Analyze hit lines by Hamming-weight classes and the 6-point subgeometry."""

from __future__ import annotations

import json
from itertools import combinations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "witting_pg32_weight_orbit_analysis.json"
OUT_MD = ROOT / "artifacts" / "witting_pg32_weight_orbit_analysis.md"


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


def tuple_to_bits(t):
    return (t[0] << 3) | (t[1] << 2) | (t[2] << 1) | t[3]


def build_pg32_points():
    return [v for v in range(1, 16)]


def build_pg32_lines(points):
    lines = set()
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            p = points[i]
            q = points[j]
            r = p ^ q
            line = tuple(sorted([p, q, r]))
            lines.add(line)
    return sorted(lines)


def weight(x: int) -> int:
    return bin(x).count("1")


def main():
    base_states = [normalize_projective(s) for s in build_base_states()]
    base_states = list(dict.fromkeys(base_states))
    if len(base_states) != 40:
        raise SystemExit(f"Expected 40 projective states, got {len(base_states)}")

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

    hit_lines = []
    for im in ray_images:
        if len(im) != 3:
            continue
        line_bits = tuple(sorted(tuple_to_bits(p) for p in im))
        if line_bits in pg_line_set:
            hit_lines.append(line_bits)
    hit_lines = sorted(set(hit_lines))
    hit_line_set = set(hit_lines)

    # Point weight classes
    weight_classes = {}
    for p in pg_points:
        weight_classes.setdefault(weight(p), []).append(p)

    # Line weight patterns
    def line_pattern(line):
        return tuple(sorted(weight(p) for p in line))

    pattern_all = {}
    pattern_hit = {}
    for line in pg_lines:
        pat = line_pattern(line)
        pattern_all[pat] = pattern_all.get(pat, 0) + 1
        if line in hit_line_set:
            pattern_hit[pat] = pattern_hit.get(pat, 0) + 1

    # 6-point (weight-2) subgeometry
    wt2_points = set(weight_classes.get(2, []))
    wt2_lines = [line for line in pg_lines if set(line).issubset(wt2_points)]
    wt2_incidence = {p: 0 for p in wt2_points}
    for line in wt2_lines:
        for p in line:
            wt2_incidence[p] += 1

    # intersection pattern among wt2 lines
    wt2_line_sets = [set(line) for line in wt2_lines]
    wt2_intersections = []
    for i, j in combinations(range(len(wt2_line_sets)), 2):
        wt2_intersections.append(len(wt2_line_sets[i] & wt2_line_sets[j]))

    results = {
        "weight_classes": {str(k): sorted(v) for k, v in weight_classes.items()},
        "pattern_all": {str(k): v for k, v in sorted(pattern_all.items())},
        "pattern_hit": {str(k): v for k, v in sorted(pattern_hit.items())},
        "wt2_points": sorted(wt2_points),
        "wt2_line_count": len(wt2_lines),
        "wt2_lines": wt2_lines,
        "wt2_point_degrees": {str(p): wt2_incidence[p] for p in sorted(wt2_incidence)},
        "wt2_line_intersection_counts": {
            "min": min(wt2_intersections) if wt2_intersections else None,
            "max": max(wt2_intersections) if wt2_intersections else None,
            "all": wt2_intersections,
        },
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(results, indent=2), encoding="utf-8")

    lines = []
    lines.append("# Weight-Class Analysis (PG(3,2) Hit Lines)")
    lines.append("")
    lines.append(
        f"- weight classes: { {k: len(v) for k, v in weight_classes.items()} }"
    )
    lines.append(f"- hit-line patterns: {results['pattern_hit']}")
    lines.append(f"- all-line patterns: {results['pattern_all']}")
    lines.append("")
    lines.append("## Weight-2 Subgeometry (6 points)")
    lines.append(f"- points: {sorted(wt2_points)}")
    lines.append(f"- lines on weight-2 points: {len(wt2_lines)}")
    lines.append(f"- point degrees on those lines: {results['wt2_point_degrees']}")
    lines.append(
        f"- line intersections (pairwise): min={results['wt2_line_intersection_counts']['min']} max={results['wt2_line_intersection_counts']['max']}"
    )

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
