#!/usr/bin/env python3
"""Relate tetrahedral rays to W33 lines via Hermitian orthogonality."""
from __future__ import annotations

import json
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "witting_w33_line_tetrahedron_analysis.json"
OUT_MD = ROOT / "artifacts" / "witting_w33_line_tetrahedron_analysis.md"

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

def weight(t):
    return sum(t)

def main():
    base_states = [normalize_projective(s) for s in build_base_states()]
    base_states = list(dict.fromkeys(base_states))
    if len(base_states) != 40:
        raise SystemExit(f"Expected 40 projective states, got {len(base_states)}")

    # adjacency
    n = len(base_states)
    adj = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if hermitian(base_states[i], base_states[j]) == 0:
                adj[i][j] = adj[j][i] = True

    # compute W33 lines as {i,j} plus common neighbors (size 2)
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

    # tetrahedral rays (pattern (2,2,2))
    scalars = [1, omega, omega2]
    tetra_rays = []
    for idx, s in enumerate(base_states):
        imgs = set()
        for c in scalars:
            scaled = tuple(gf4_mul(c, x) for x in s)
            p = trace_map(scaled)
            if p != (0, 0, 0, 0):
                imgs.add(p)
        imgs = tuple(sorted(imgs))
        if len(imgs) == 3:
            wpat = tuple(sorted(weight(p) for p in imgs))
            if wpat == (2, 2, 2):
                tetra_rays.append(idx)
    tetra_set = set(tetra_rays)

    # distribution of tetra rays per W33 line
    tetra_counts = {}
    for line in lines:
        count = sum(1 for v in line if v in tetra_set)
        tetra_counts[count] = tetra_counts.get(count, 0) + 1

    # per-ray line counts
    lines_by_ray = {i: 0 for i in range(n)}
    for line in lines:
        for v in line:
            lines_by_ray[v] += 1
    tetra_line_counts = {i: lines_by_ray[i] for i in tetra_rays}

    # induced subgraph on tetra rays
    tetra_edges = []
    for i in tetra_rays:
        for j in tetra_rays:
            if i < j and adj[i][j]:
                tetra_edges.append((i, j))

    results = {
        "line_count": len(lines),
        "expected_lines": 40,
        "tetra_rays": tetra_rays,
        "tetra_ray_count": len(tetra_rays),
        "tetra_edges": tetra_edges,
        "tetra_edge_count": len(tetra_edges),
        "tetra_counts_per_line": tetra_counts,
        "tetra_ray_line_counts": tetra_line_counts,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(results, indent=2), encoding="utf-8")

    lines_out = []
    lines_out.append("# Tetrahedral Rays vs W33 Lines")
    lines_out.append("")
    lines_out.append(f"- W33 lines found: {results['line_count']}")
    lines_out.append(f"- tetra rays: {results['tetra_ray_count']} -> {results['tetra_rays']}")
    lines_out.append(f"- tetra edges (induced): {results['tetra_edge_count']}")
    lines_out.append(f"- tetra counts per line: {results['tetra_counts_per_line']}")
    lines_out.append(f"- tetra ray line counts: {results['tetra_ray_line_counts']}")

    OUT_MD.write_text("\n".join(lines_out) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")

if __name__ == "__main__":
    main()
