#!/usr/bin/env python3
"""Analyze W33 lines vs tetrahedral rays and PG(3,2) trace images."""
from __future__ import annotations

import json
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "witting_w33_line_trace_tetra_analysis.json"
OUT_MD = ROOT / "artifacts" / "witting_w33_line_trace_tetra_analysis.md"

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

def weight(p):
    return sum(p)

def main():
    base_states = [normalize_projective(s) for s in build_base_states()]
    base_states = list(dict.fromkeys(base_states))
    if len(base_states) != 40:
        raise SystemExit(f"Expected 40 projective states, got {len(base_states)}")

    # adjacency and W33 lines
    n = len(base_states)
    adj = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if hermitian(base_states[i], base_states[j]) == 0:
                adj[i][j] = adj[j][i] = True

    lines = set()
    for i in range(n):
        for j in range(i + 1, n):
            if not adj[i][j]:
                continue
            common = [k for k in range(n) if adj[i][k] and adj[j][k]]
            if len(common) == 2:
                line = tuple(sorted([i, j, common[0], common[1]]))
                lines.add(line)
    lines = sorted(lines)

    # ray trace images
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

    # tetra rays and tetra PG lines
    tetra_rays = []
    ray_to_pgline = {}
    for idx, imgs in enumerate(ray_images):
        if len(imgs) == 3:
            wpat = tuple(sorted(weight(p) for p in imgs))
            if wpat == (2, 2, 2):
                tetra_rays.append(idx)
                ray_to_pgline[idx] = tuple(sorted(imgs))
    tetra_set = set(tetra_rays)
    tetra_pg_lines = sorted(set(ray_to_pgline.values()))

    # analyze W33 lines
    stats = {
        "total_lines": len(lines),
        "tetra_pg_lines": tetra_pg_lines,
        "tetra_ray_lines": [],
        "distributions": {
            "tetra_count": {},
            "union_size": {},
            "union_size_by_tetra": {},
            "tetra_line_count": {},
            "same_tetra_line": {},
        },
    }

    for line in lines:
        tetra_in = [v for v in line if v in tetra_set]
        tetra_count = len(tetra_in)
        union = set()
        for v in line:
            union.update(ray_images[v])
        union = tuple(sorted(union))
        union_size = len(union)

        tetra_lines_here = sorted(set(ray_to_pgline[v] for v in tetra_in))
        tetra_line_count = len(tetra_lines_here)
        same_line = (tetra_line_count == 1 and tetra_count == 2)

        stats["distributions"]["tetra_count"][str(tetra_count)] = stats["distributions"]["tetra_count"].get(str(tetra_count), 0) + 1
        stats["distributions"]["union_size"][str(union_size)] = stats["distributions"]["union_size"].get(str(union_size), 0) + 1
        stats["distributions"]["union_size_by_tetra"].setdefault(str(tetra_count), {}).setdefault(str(union_size), 0)
        stats["distributions"]["union_size_by_tetra"][str(tetra_count)][str(union_size)] += 1
        stats["distributions"]["tetra_line_count"][str(tetra_line_count)] = stats["distributions"]["tetra_line_count"].get(str(tetra_line_count), 0) + 1
        stats["distributions"]["same_tetra_line"][str(same_line)] = stats["distributions"]["same_tetra_line"].get(str(same_line), 0) + 1

        if tetra_count == 2:
            stats["tetra_ray_lines"].append({
                "line": line,
                "tetra_rays": tetra_in,
                "tetra_pg_lines": tetra_lines_here,
                "union_size": union_size,
                "union": union,
            })

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(stats, indent=2), encoding="utf-8")

    lines_out = []
    lines_out.append("# W33 Line ↔ Tetra Ray Trace Analysis")
    lines_out.append("")
    lines_out.append(f"- total W33 lines: {stats['total_lines']}")
    lines_out.append(f"- tetra PG lines: {stats['tetra_pg_lines']}")
    lines_out.append(f"- tetra_count distribution: {stats['distributions']['tetra_count']}")
    lines_out.append(f"- union size distribution: {stats['distributions']['union_size']}")
    lines_out.append(f"- union size by tetra count: {stats['distributions']['union_size_by_tetra']}")
    lines_out.append(f"- tetra_line_count distribution: {stats['distributions']['tetra_line_count']}")
    lines_out.append(f"- same tetra line? {stats['distributions']['same_tetra_line']}")

    OUT_MD.write_text("\n".join(lines_out) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")

if __name__ == "__main__":
    main()
