#!/usr/bin/env python3
"""Compute invariants for the 14-point/16-line configuration hit by Witting rays.

Build the incidence bipartite graph between the 14 covered PG(3,2) points
and the 16 hit lines, then compute degree sequences and eigenvalues.

Outputs:
- artifacts/witting_pg32_config_invariants.json
- artifacts/witting_pg32_config_invariants.md
"""
from __future__ import annotations

import json
from itertools import combinations, product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "witting_pg32_config_invariants.json"
OUT_MD = ROOT / "artifacts" / "witting_pg32_config_invariants.md"

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
    covered_points = sorted(set(p for line in hit_lines for p in line))

    # incidence matrix: points x lines
    P = len(covered_points)
    L = len(hit_lines)
    idx_point = {p: i for i, p in enumerate(covered_points)}
    M = np.zeros((P, L), dtype=int)
    for j, line in enumerate(hit_lines):
        for p in line:
            if p in idx_point:
                M[idx_point[p], j] = 1

    point_degrees = M.sum(axis=1).tolist()
    line_degrees = M.sum(axis=0).tolist()

    # bipartite adjacency eigenvalues
    A = np.zeros((P + L, P + L), dtype=int)
    A[:P, P:] = M
    A[P:, :P] = M.T
    eigs = np.linalg.eigvals(A)
    eigs = np.round(eigs.real, 6)
    # count eigenvalues
    vals = {}
    for v in eigs:
        vals[str(v)] = vals.get(str(v), 0) + 1

    summary = {
        "covered_points": len(covered_points),
        "hit_lines": len(hit_lines),
        "point_degree_counts": {str(k): point_degrees.count(k) for k in sorted(set(point_degrees))},
        "line_degree_counts": {str(k): line_degrees.count(k) for k in sorted(set(line_degrees))},
        "bipartite_spectrum_counts": vals,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    lines = []
    lines.append("# 14-Point / 16-Line Configuration Invariants")
    lines.append("")
    lines.append(f"- points: {summary['covered_points']}")
    lines.append(f"- lines: {summary['hit_lines']}")
    lines.append(f"- point degrees: {summary['point_degree_counts']}")
    lines.append(f"- line degrees: {summary['line_degree_counts']}")
    lines.append("## Bipartite adjacency spectrum (rounded)")
    for k, v in summary["bipartite_spectrum_counts"].items():
        lines.append(f"- {k}: {v}")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")

if __name__ == "__main__":
    main()
