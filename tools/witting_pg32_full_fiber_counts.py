#!/usr/bin/env python3
"""Analyze multiplicities inside PG(3,2) fibers for full 240 Witting vertices.

We build the 240 Witting vertices in GF(4)^4 (with ± counted as distinct),
apply the trace map to PG(3,2), and then compute per-fiber:
  - total multiplicity (should be 16)
  - number of distinct GF(4)^4 vectors (phase-quotiented)

Outputs:
- artifacts/witting_pg32_full_fiber_counts.json
- artifacts/witting_pg32_full_fiber_counts.md
"""

from __future__ import annotations

import json
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "witting_pg32_full_fiber_counts.json"
OUT_MD = ROOT / "artifacts" / "witting_pg32_full_fiber_counts.md"


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


omega = 2
omega2 = 3
omega_powers = [1, omega, omega2]


def trace_map(v):
    return tuple(gf4_trace(x) for x in v)


def build_vertices():
    vertices = []
    # Type A
    for lam, mu, nu in product(range(3), repeat=3):
        w_l = omega_powers[lam]
        w_m = omega_powers[mu]
        w_n = omega_powers[nu]
        base = [
            (0, w_l, w_m, w_n),
            (w_l, 0, w_m, w_n),
            (w_l, w_m, 0, w_n),
            (w_l, w_m, w_n, 0),
        ]
        for v in base:
            for s in [1, -1]:
                vertices.append(v)
    # Type B
    for lam in range(3):
        w_l = omega_powers[lam]
        for pos in range(4):
            v = [0, 0, 0, 0]
            v[pos] = w_l
            for s in [1, -1]:
                vertices.append(tuple(v))
    return vertices


def main():
    vertices = build_vertices()
    fibers = {}
    for v in vertices:
        p = trace_map(v)
        fibers.setdefault(p, []).append(v)

    fiber_stats = {}
    for p, verts in fibers.items():
        unique = {v for v in verts}
        fiber_stats[str(p)] = {
            "total": len(verts),
            "unique_vectors": len(unique),
        }

    summary = {
        "vertex_count": len(vertices),
        "fiber_count": len(fibers),
        "fiber_stats": fiber_stats,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    lines = []
    lines.append("# Witting 240-Vertex Fiber Multiplicity Analysis")
    lines.append("")
    lines.append(f"- vertices: {summary['vertex_count']}")
    lines.append(f"- fibers: {summary['fiber_count']}")
    lines.append("")
    for p, stats in sorted(fiber_stats.items()):
        lines.append(f"- {p}: total={stats['total']} unique={stats['unique_vectors']}")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
