#!/usr/bin/env python3
"""Analyze the GF(4)->GF(2) trace map fibers and their W33 incidence.

We build the 40 base Witting rays in GF(4)^4, define a Hermitian form,
construct the W33 orthogonality graph, then map points to PG(3,2) via trace.

We analyze:
  - fiber sizes for PG(3,2) points
  - induced subgraphs on fibers and on PG(3,2) lines (3-point unions)

Outputs:
- artifacts/witting_pg32_fiber_analysis.json
- artifacts/witting_pg32_fiber_analysis.md
"""
from __future__ import annotations

import json
from itertools import combinations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "witting_pg32_fiber_analysis.json"
OUT_MD = ROOT / "artifacts" / "witting_pg32_fiber_analysis.md"

# GF(4): 0,1,ω,ω^2 encoded as 0,1,2,3 with ω^2=ω+1
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
    # brute force
    for b in [1, 2, 3]:
        if gf4_mul(a, b) == 1:
            return b
    raise ZeroDivisionError

omega = 2
omega2 = 3
omega_powers = [1, omega, omega2]

def build_base_states():
    states = []
    # 4 basis states
    for i in range(4):
        v = [0, 0, 0, 0]
        v[i] = 1
        states.append(tuple(v))
    # 36 other states
    for mu, nu in product(range(3), repeat=2):
        w_mu = omega_powers[mu]
        w_nu = omega_powers[nu]
        states.append((0, 1, w_mu, w_nu))
        states.append((1, 0, w_mu, w_nu))
        states.append((1, w_mu, 0, w_nu))
        states.append((1, w_mu, w_nu, 0))
    return states

def normalize_projective(v):
    # multiply so first nonzero coordinate = 1
    for x in v:
        if x != 0:
            inv = gf4_inv(x)
            return tuple(gf4_mul(inv, xi) for xi in v)
    return None

def hermitian(u, v):
    # sum u_i * v_i^2
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

def build_pg32_lines(points):
    # each line: {p, q, p+q} in GF(2)^4
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
    if len(base_states) != 40:
        raise SystemExit(f"Expected 40 projective states, got {len(base_states)}")

    # build W33 graph from hermitian orthogonality
    n = len(base_states)
    adj = [[0] * n for _ in range(n)]
    edge_count = 0
    for i in range(n):
        for j in range(i + 1, n):
            if hermitian(base_states[i], base_states[j]) == 0:
                adj[i][j] = 1
                adj[j][i] = 1
                edge_count += 1
    degrees = [sum(row) for row in adj]

    # trace map fibers to PG(3,2)
    pg_points = build_pg32_points()
    pg_lines = build_pg32_lines(pg_points)
    fiber = {}
    for idx, s in enumerate(base_states):
        p = trace_map(s)
        if p == (0, 0, 0, 0):
            # skip zero vector (projective replacement)
            continue
        fiber.setdefault(p, []).append(idx)

    fiber_sizes = [len(v) for v in fiber.values()]

    # analyze line fibers
    line_stats = []
    for line in pg_lines:
        idxs = []
        for p in line:
            idxs.extend(fiber.get(p, []))
        idxs = sorted(set(idxs))
        if not idxs:
            continue
        # induced edges
        e = 0
        for i, j in combinations(idxs, 2):
            if adj[i][j]:
                e += 1
        line_stats.append({
            "size": len(idxs),
            "edges": e,
        })

    summary = {
        "w33_vertices": n,
        "w33_edges": edge_count,
        "degree_set": sorted(set(degrees)),
        "pg32_point_count": len(pg_points),
        "pg32_line_count": len(pg_lines),
        "fiber_sizes": {
            "min": min(fiber_sizes) if fiber_sizes else 0,
            "max": max(fiber_sizes) if fiber_sizes else 0,
            "counts": {str(k): fiber_sizes.count(k) for k in sorted(set(fiber_sizes))},
        },
        "line_fiber_sizes": {
            "min": min(ls["size"] for ls in line_stats) if line_stats else 0,
            "max": max(ls["size"] for ls in line_stats) if line_stats else 0,
        },
        "line_edge_counts": {
            "min": min(ls["edges"] for ls in line_stats) if line_stats else 0,
            "max": max(ls["edges"] for ls in line_stats) if line_stats else 0,
        },
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    lines = []
    lines.append("# Witting → PG(3,2) Fiber Analysis")
    lines.append("")
    lines.append(f"- W33 vertices: {summary['w33_vertices']}")
    lines.append(f"- W33 edges: {summary['w33_edges']}")
    lines.append(f"- W33 degree set: {summary['degree_set']}")
    lines.append(f"- PG(3,2) points: {summary['pg32_point_count']}")
    lines.append(f"- PG(3,2) lines: {summary['pg32_line_count']}")
    lines.append("")
    lines.append("## Fiber sizes (PG points)")
    lines.append(f"- min: {summary['fiber_sizes']['min']}")
    lines.append(f"- max: {summary['fiber_sizes']['max']}")
    lines.append(f"- counts: {summary['fiber_sizes']['counts']}")
    lines.append("")
    lines.append("## Line fiber stats")
    lines.append(f"- size min/max: {summary['line_fiber_sizes']['min']} / {summary['line_fiber_sizes']['max']}")
    lines.append(f"- edge min/max: {summary['line_edge_counts']['min']} / {summary['line_edge_counts']['max']}")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")

if __name__ == "__main__":
    main()
