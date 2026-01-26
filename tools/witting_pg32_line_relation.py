#!/usr/bin/env python3
"""Analyze relations between W33 lines and PG(3,2) lines via trace images.

We map each Witting ray to a set of PG(3,2) points using scalars {1, ω, ω^2}.
For each W33 line (4-clique of rays), we take the union of its PG images.
We then compare with each PG(3,2) line (3 points).

Outputs:
- artifacts/witting_pg32_line_relation.json
- artifacts/witting_pg32_line_relation.md
"""
from __future__ import annotations

import json
from itertools import combinations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "witting_pg32_line_relation.json"
OUT_MD = ROOT / "artifacts" / "witting_pg32_line_relation.md"

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
    pts = []
    for v in product([0, 1], repeat=4):
        if v == (0, 0, 0, 0):
            continue
        pts.append(v)
    return pts

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
    if len(base_states) != 40:
        raise SystemExit(f"Expected 40 projective states, got {len(base_states)}")

    # W33 adjacency and lines (4-cliques)
    n = len(base_states)
    adj = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if hermitian(base_states[i], base_states[j]) == 0:
                adj[i][j] = 1
                adj[j][i] = 1
    w33_lines = []
    for combo in combinations(range(n), 4):
        ok = True
        for a, b in combinations(combo, 2):
            if adj[a][b] == 0:
                ok = False
                break
        if ok:
            w33_lines.append(combo)

    # trace images for scalars
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

    # analyze W33 line unions vs PG lines
    line_union_sizes = []
    pg_line_cover_counts = {str(line): 0 for line in pg_lines}
    exact_match = 0
    contained_line_counts = []

    for line in w33_lines:
        union = set()
        for idx in line:
            union.update(images[idx])
        line_union_sizes.append(len(union))
        # count coverage of each PG line
        for pg_line in pg_lines:
            if set(pg_line).issubset(union):
                pg_line_cover_counts[str(pg_line)] += 1
        contained = sum(1 for pg_line in pg_lines if set(pg_line).issubset(union))
        contained_line_counts.append(contained)
        if len(union) == 3 and any(set(pg_line) == union for pg_line in pg_lines):
            exact_match += 1

    summary = {
        "w33_line_count": len(w33_lines),
        "pg_line_count": len(pg_lines),
        "line_union_size_counts": {str(k): line_union_sizes.count(k) for k in sorted(set(line_union_sizes))},
        "pg_line_cover_stats": {
            "min": min(pg_line_cover_counts.values()) if pg_line_cover_counts else 0,
            "max": max(pg_line_cover_counts.values()) if pg_line_cover_counts else 0,
        },
        "pg_lines_contained_per_w33_line": {
            "min": min(contained_line_counts) if contained_line_counts else 0,
            "max": max(contained_line_counts) if contained_line_counts else 0,
            "counts": {str(k): contained_line_counts.count(k) for k in sorted(set(contained_line_counts))},
        },
        "exact_pg_line_matches": exact_match,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    lines = []
    lines.append("# W33 Lines vs PG(3,2) Lines (Trace Images)")
    lines.append("")
    lines.append(f"- W33 lines: {summary['w33_line_count']}")
    lines.append(f"- PG(3,2) lines: {summary['pg_line_count']}")
    lines.append("")
    lines.append("## W33 line union sizes (PG points)")
    lines.append(f"- counts: {summary['line_union_size_counts']}")
    lines.append("")
    lines.append("## PG line coverage by W33 line unions")
    lines.append(f"- min cover count: {summary['pg_line_cover_stats']['min']}")
    lines.append(f"- max cover count: {summary['pg_line_cover_stats']['max']}")
    lines.append(f"- exact PG line matches: {summary['exact_pg_line_matches']}")
    lines.append("")
    lines.append("## PG lines contained per W33 line")
    lines.append(f"- counts: {summary['pg_lines_contained_per_w33_line']['counts']}")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")

if __name__ == "__main__":
    main()
