#!/usr/bin/env python3
"""Analyze W33 line unions vs PG(3,2) planes and ovoids.

We build PG(3,2) planes (15 planes, each 7 points) and test whether
W33 line trace-image unions contain planes or form ovoids (5-point sets
with no line).

Outputs:
- artifacts/witting_pg32_plane_relation.json
- artifacts/witting_pg32_plane_relation.md
"""
from __future__ import annotations

import json
from itertools import combinations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "witting_pg32_plane_relation.json"
OUT_MD = ROOT / "artifacts" / "witting_pg32_plane_relation.md"

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

def hermitian(u, v):
    s = 0
    for a, b in zip(u, v):
        s = gf4_add(s, gf4_mul(a, gf4_square(b)))
    return s

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

def build_pg32_planes(points):
    # planes correspond to 3D subspaces of F2^4; each plane has 7 nonzero vectors
    planes = set()
    for a, b, c in combinations(points, 3):
        # check if a,b,c are independent
        mat = [a, b, c]
        # compute span
        span = set()
        for x, y, z in product([0, 1], repeat=3):
            if x == y == z == 0:
                continue
            v = tuple((x * ai) ^ (y * bi) ^ (z * ci) for ai, bi, ci in zip(a, b, c))
            if v != (0, 0, 0, 0):
                span.add(v)
        if len(span) == 7:
            planes.add(tuple(sorted(span)))
    return sorted(planes)

def is_ovoid(points_set, lines):
    # no line fully contained
    for line in lines:
        if set(line).issubset(points_set):
            return False
    return True

def main():
    base_states = [normalize_projective(s) for s in build_base_states()]
    base_states = list(dict.fromkeys(base_states))
    if len(base_states) != 40:
        raise SystemExit(f"Expected 40 projective states, got {len(base_states)}")

    # W33 adjacency and lines
    n = len(base_states)
    adj = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if hermitian(base_states[i], base_states[j]) == 0:
                adj[i][j] = 1
                adj[j][i] = 1
    w33_lines = []
    for combo in combinations(range(n), 4):
        if all(adj[a][b] for a, b in combinations(combo, 2)):
            w33_lines.append(combo)

    # trace images
    scalars = [1, omega, omega2]
    images = []
    for s in base_states:
        imgs = set()
        for c in scalars:
            scaled = tuple(gf4_mul(c, x) for x in s)
            p = trace_map(scaled)
            if p != (0, 0, 0, 0):
                imgs.add(p)
        images.append(imgs)

    pg_points = build_pg32_points()
    pg_lines = build_pg32_lines(pg_points)
    pg_planes = build_pg32_planes(pg_points)

    plane_contained_counts = []
    ovoid_count = 0
    for line in w33_lines:
        union = set()
        for idx in line:
            union.update(images[idx])
        # planes contained
        contained = sum(1 for plane in pg_planes if set(plane).issubset(union))
        plane_contained_counts.append(contained)
        # ovoid check if size 5
        if len(union) == 5 and is_ovoid(union, pg_lines):
            ovoid_count += 1

    summary = {
        "w33_line_count": len(w33_lines),
        "pg_plane_count": len(pg_planes),
        "plane_contained_counts": {
            "min": min(plane_contained_counts),
            "max": max(plane_contained_counts),
            "counts": {str(k): plane_contained_counts.count(k) for k in sorted(set(plane_contained_counts))},
        },
        "ovoid_like_unions": ovoid_count,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    lines = []
    lines.append("# W33 Line Unions vs PG(3,2) Planes/Ovoids")
    lines.append("")
    lines.append(f"- W33 lines: {summary['w33_line_count']}")
    lines.append(f"- PG(3,2) planes: {summary['pg_plane_count']}")
    lines.append("")
    lines.append("## Planes contained per W33 line union")
    lines.append(f"- counts: {summary['plane_contained_counts']['counts']}")
    lines.append("")
    lines.append(f"- ovoid-like unions (size 5, no line): {summary['ovoid_like_unions']}")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")

if __name__ == "__main__":
    main()
