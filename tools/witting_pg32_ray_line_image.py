#!/usr/bin/env python3
"""Analyze whether Witting ray trace images are PG(3,2) lines / isotropic lines.

We compute the trace images of each Witting ray under scalars {1, ω, ω^2}.
For size-3 images, we check:
  - whether the 3 points form a PG(3,2) line
  - whether that line is isotropic for a standard symplectic form (W(3,2))

Outputs:
- artifacts/witting_pg32_ray_line_image.json
- artifacts/witting_pg32_ray_line_image.md
"""

from __future__ import annotations

import json
from itertools import combinations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "witting_pg32_ray_line_image.json"
OUT_MD = ROOT / "artifacts" / "witting_pg32_ray_line_image.md"


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


def symplectic_dot(p, q):
    # standard symplectic form on F2^4: x1*y3 + x2*y4 + x3*y1 + x4*y2
    return (p[0] & q[2]) ^ (p[1] & q[3]) ^ (p[2] & q[0]) ^ (p[3] & q[1])


def is_isotropic_line(line):
    a, b, c = line
    return (
        symplectic_dot(a, b) == 0
        and symplectic_dot(a, c) == 0
        and symplectic_dot(b, c) == 0
    )


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
    isotropic_lines = {
        tuple(sorted(line)) for line in pg_lines if is_isotropic_line(line)
    }

    stats = {
        "ray_count": len(ray_images),
        "ray_image_sizes": {
            str(k): sum(1 for im in ray_images if len(im) == k)
            for k in sorted({len(im) for im in ray_images})
        },
        "line_images": 0,
        "isotropic_line_images": 0,
        "distinct_line_images": 0,
        "distinct_isotropic_line_images": 0,
    }

    line_images = []
    iso_images = []
    for im in ray_images:
        if len(im) == 3 and tuple(im) in pg_line_set:
            line_images.append(tuple(im))
            if tuple(im) in isotropic_lines:
                iso_images.append(tuple(im))

    stats["line_images"] = len(line_images)
    stats["isotropic_line_images"] = len(iso_images)
    stats["distinct_line_images"] = len(set(line_images))
    stats["distinct_isotropic_line_images"] = len(set(iso_images))

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(stats, indent=2), encoding="utf-8")

    lines = []
    lines.append("# Witting Ray → PG(3,2) Line Image Analysis")
    lines.append("")
    lines.append(f"- rays: {stats['ray_count']}")
    lines.append(f"- image size counts: {stats['ray_image_sizes']}")
    lines.append(f"- rays mapping to PG lines: {stats['line_images']}")
    lines.append(f"- distinct PG lines hit: {stats['distinct_line_images']}")
    lines.append(f"- rays mapping to isotropic lines: {stats['isotropic_line_images']}")
    lines.append(
        f"- distinct isotropic lines hit: {stats['distinct_isotropic_line_images']}"
    )

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
