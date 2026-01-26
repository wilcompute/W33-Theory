#!/usr/bin/env python3
"""Analyze trace-map images of Witting rays under GF(4) scalars.

We take the 40 Witting rays (projective points in GF(4)^4), compute
trace images of scalar multiples by {1, ω, ω^2}, and analyze:
  - per-ray image set sizes
  - PG(3,2) point coverage
  - W33 line (size-4 clique) image unions

Outputs:
- artifacts/witting_pg32_ray_trace.json
- artifacts/witting_pg32_ray_trace.md
"""
from __future__ import annotations

import json
from itertools import combinations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "witting_pg32_ray_trace.json"
OUT_MD = ROOT / "artifacts" / "witting_pg32_ray_trace.md"

# GF(4) arithmetic: 0,1,ω,ω^2 encoded as 0,1,2,3
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
    pts = []
    for v in product([0, 1], repeat=4):
        if v == (0, 0, 0, 0):
            continue
        pts.append(v)
    return pts

def main():
    base_states = [normalize_projective(s) for s in build_base_states()]
    base_states = list(dict.fromkeys(base_states))
    if len(base_states) != 40:
        raise SystemExit(f"Expected 40 projective states, got {len(base_states)}")

    # W33 graph
    n = len(base_states)
    adj = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if hermitian(base_states[i], base_states[j]) == 0:
                adj[i][j] = 1
                adj[j][i] = 1

    # compute W33 lines (4-cliques)
    lines = []
    for combo in combinations(range(n), 4):
        ok = True
        for a, b in combinations(combo, 2):
            if adj[a][b] == 0:
                ok = False
                break
        if ok:
            lines.append(combo)

    # trace images for scalars 1, ω, ω^2
    scalars = [1, omega, omega2]
    ray_images = []
    for s in base_states:
        imgs = set()
        for c in scalars:
            scaled = tuple(gf4_mul(c, x) for x in s)
            p = trace_map(scaled)
            if p != (0, 0, 0, 0):
                imgs.add(p)
        ray_images.append(sorted(imgs))

    # PG(3,2) coverage
    pg_points = build_pg32_points()
    pg_cover = {p: [] for p in pg_points}
    for idx, imgs in enumerate(ray_images):
        for p in imgs:
            pg_cover[p].append(idx)

    ray_image_sizes = [len(imgs) for imgs in ray_images]
    pg_point_cover_sizes = [len(v) for v in pg_cover.values()]

    # line image unions
    line_image_sizes = []
    for line in lines:
        union = set()
        for idx in line:
            union.update(ray_images[idx])
        line_image_sizes.append(len(union))

    summary = {
        "ray_count": n,
        "w33_line_count": len(lines),
        "ray_image_sizes": {
            "min": min(ray_image_sizes),
            "max": max(ray_image_sizes),
            "counts": {str(k): ray_image_sizes.count(k) for k in sorted(set(ray_image_sizes))},
        },
        "pg_point_cover_sizes": {
            "min": min(pg_point_cover_sizes),
            "max": max(pg_point_cover_sizes),
            "counts": {str(k): pg_point_cover_sizes.count(k) for k in sorted(set(pg_point_cover_sizes))},
        },
        "line_image_union_sizes": {
            "min": min(line_image_sizes) if line_image_sizes else 0,
            "max": max(line_image_sizes) if line_image_sizes else 0,
            "counts": {str(k): line_image_sizes.count(k) for k in sorted(set(line_image_sizes))},
        },
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    lines_md = []
    lines_md.append("# Witting Ray Trace-Map Analysis")
    lines_md.append("")
    lines_md.append(f"- rays: {summary['ray_count']}")
    lines_md.append(f"- W33 lines (4-cliques): {summary['w33_line_count']}")
    lines_md.append("")
    lines_md.append("## Ray image sizes (per ray)")
    lines_md.append(f"- min: {summary['ray_image_sizes']['min']}")
    lines_md.append(f"- max: {summary['ray_image_sizes']['max']}")
    lines_md.append(f"- counts: {summary['ray_image_sizes']['counts']}")
    lines_md.append("")
    lines_md.append("## PG(3,2) point cover sizes (rays per point)")
    lines_md.append(f"- min: {summary['pg_point_cover_sizes']['min']}")
    lines_md.append(f"- max: {summary['pg_point_cover_sizes']['max']}")
    lines_md.append(f"- counts: {summary['pg_point_cover_sizes']['counts']}")
    lines_md.append("")
    lines_md.append("## W33 line image union sizes")
    lines_md.append(f"- min: {summary['line_image_union_sizes']['min']}")
    lines_md.append(f"- max: {summary['line_image_union_sizes']['max']}")
    lines_md.append(f"- counts: {summary['line_image_union_sizes']['counts']}")

    OUT_MD.write_text("\n".join(lines_md) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")

if __name__ == "__main__":
    main()
