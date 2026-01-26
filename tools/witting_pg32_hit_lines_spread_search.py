#!/usr/bin/env python3
"""Search for spreads / partial spreads inside the 16 hit PG(3,2) lines.

We look for sets of 5 pairwise-disjoint hit lines (a full spread would cover 15 points),
and for sets of 5 lines covering 14 points (missing one point).

Outputs:
- artifacts/witting_pg32_hit_lines_spread_search.json
- artifacts/witting_pg32_hit_lines_spread_search.md
"""
from __future__ import annotations

import json
from itertools import combinations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "witting_pg32_hit_lines_spread_search.json"
OUT_MD = ROOT / "artifacts" / "witting_pg32_hit_lines_spread_search.md"

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

    hit_lines = []
    for im in ray_images:
        if len(im) == 3 and tuple(im) in pg_line_set:
            hit_lines.append(tuple(im))
    hit_lines = sorted(set(hit_lines))

    full_spreads = 0
    partial_spreads = 0
    for combo in combinations(range(len(hit_lines)), 5):
        lines = [hit_lines[i] for i in combo]
        # disjoint?
        pts = []
        ok = True
        for line in lines:
            for p in line:
                if p in pts:
                    ok = False
                    break
                pts.append(p)
            if not ok:
                break
        if not ok:
            continue
        if len(pts) == 15:
            full_spreads += 1
        elif len(pts) == 14:
            partial_spreads += 1

    summary = {
        "hit_line_count": len(hit_lines),
        "full_spreads": full_spreads,
        "partial_spreads_14pts": partial_spreads,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    lines = []
    lines.append("# Hit-Line Spread Search (PG(3,2))")
    lines.append("")
    lines.append(f"- hit lines: {summary['hit_line_count']}")
    lines.append(f"- full spreads (cover 15 pts): {summary['full_spreads']}")
    lines.append(f"- partial spreads (cover 14 pts): {summary['partial_spreads_14pts']}")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")

if __name__ == "__main__":
    main()
