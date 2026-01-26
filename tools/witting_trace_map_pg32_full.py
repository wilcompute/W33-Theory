#!/usr/bin/env python3
"""Full Witting 240-vertex trace map GF(4)->GF(2) per Marcelis §8.

We generate the 240 vertices using the given coordinate patterns with ω^λ
and ± signs (counted as distinct vertices before trace). We then apply the
trace map Tr(x)=x+x^2 coordinatewise.

Outputs:
- artifacts/witting_trace_map_pg32_full.json
- artifacts/witting_trace_map_pg32_full.md
"""
from __future__ import annotations

import json
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "witting_trace_map_pg32_full.json"
OUT_MD = ROOT / "artifacts" / "witting_trace_map_pg32_full.md"

# GF(4) representation: 0,1,2,3 correspond to 0,1,ω,ω^2
# with ω^2 = ω + 1, and Tr(x)=x+x^2

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

def trace_map(state):
    return tuple(gf4_trace(x) for x in state)

def build_vertices():
    vertices = []
    # Type A: ±(0, ω^λ, -ω^μ, ω^ν) and permutations of zero position
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
                vertices.append(v)  # sign doesn't affect GF(4) value, but counts multiplicity
    # Type B: (±i√3 ω^λ, 0, 0, 0) etc -> treated as single nonzero coordinate ω^λ
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
    images = [trace_map(v) for v in vertices]

    counts = {}
    for v in images:
        counts[v] = counts.get(v, 0) + 1

    summary = {
        "vertex_count": len(vertices),
        "unique_trace_points": len(counts),
        "trace_values": {x: gf4_trace(x) for x in [0, 1, omega, omega2]},
        "counts": {str(k): v for k, v in counts.items()},
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    lines = []
    lines.append("# Witting Trace-Map Test (Full 240 vertices)")
    lines.append("")
    lines.append(f"- vertices: {summary['vertex_count']}")
    lines.append(f"- unique trace points: {summary['unique_trace_points']}")
    lines.append(f"- trace values: {summary['trace_values']}")
    lines.append("")
    lines.append("## Point multiplicities")
    for k, v in sorted(summary["counts"].items(), key=lambda kv: -kv[1]):
        lines.append(f"- {k}: {v}")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")

if __name__ == "__main__":
    main()
