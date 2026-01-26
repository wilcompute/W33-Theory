#!/usr/bin/env python3
"""Test the Witting->PG(3,2) trace-map construction described by Marcelis.

We model GF(4) with elements {0,1,ω,ω^2} where ω^2=ω+1 and Tr(x)=x+x^2 in GF(4).
We build the 40 base states and apply the trace map coordinatewise to GF(2)^4.

Outputs:
- artifacts/witting_trace_map_pg32.json
- artifacts/witting_trace_map_pg32.md
"""
from __future__ import annotations

import json
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "witting_trace_map_pg32.json"
OUT_MD = ROOT / "artifacts" / "witting_trace_map_pg32.md"

# GF(4) representation: 0,1,2,3 correspond to 0,1,ω,ω^2
# with ω^2 = ω + 1, and ω^3 = 1.

def gf4_add(a: int, b: int) -> int:
    # addition in GF(2)[x]/(x^2+x+1), encoded in bits
    # map 0->00, 1->01, ω->10, ω^2->11
    return a ^ b

def gf4_mul(a: int, b: int) -> int:
    if a == 0 or b == 0:
        return 0
    # map to polynomial bits
    a0, a1 = a & 1, (a >> 1) & 1
    b0, b1 = b & 1, (b >> 1) & 1
    # multiply (a0 + a1*x)(b0 + b1*x) = c0 + c1*x + c2*x^2
    c0 = a0 * b0
    c1 = a0 * b1 + a1 * b0
    c2 = a1 * b1
    # reduce x^2 = x + 1 in GF(2)
    c0 = (c0 + c2) % 2
    c1 = (c1 + c2) % 2
    return (c1 << 1) | c0

def gf4_square(a: int) -> int:
    return gf4_mul(a, a)

def gf4_trace(a: int) -> int:
    # Tr(x)=x+x^2 in GF(4) -> element of GF(2): 0 or 1
    return gf4_add(a, gf4_square(a)) & 1

# powers of ω
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

    # 36 other states (signs collapse in char 2)
    for mu, nu in product(range(3), repeat=2):
        w_mu = omega_powers[mu]
        w_nu = omega_powers[nu]
        states.append((0, 1, w_mu, w_nu))
        states.append((1, 0, w_mu, w_nu))
        states.append((1, w_mu, 0, w_nu))
        states.append((1, w_mu, w_nu, 0))
    return states

def trace_map(state):
    return tuple(gf4_trace(x) for x in state)

def normalize_projective(v):
    # normalize nonzero vector in GF(2)^4 to projective point
    if all(x == 0 for x in v):
        return None
    return v

def main():
    states = build_base_states()
    images = [trace_map(s) for s in states]

    counts = {}
    for v in images:
        p = normalize_projective(v)
        if p is None:
            continue
        counts[p] = counts.get(p, 0) + 1

    summary = {
        "base_state_count": len(states),
        "unique_projective_points": len(counts),
        "counts": {str(k): v for k, v in counts.items()},
        "trace_values": {x: gf4_trace(x) for x in [0, 1, omega, omega2]},
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    lines = []
    lines.append("# Witting Trace-Map Test (GF(4) -> GF(2))")
    lines.append("")
    lines.append(f"- base states: {summary['base_state_count']}")
    lines.append(f"- unique projective points: {summary['unique_projective_points']}")
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
