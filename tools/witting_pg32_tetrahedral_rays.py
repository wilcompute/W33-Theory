#!/usr/bin/env python3
"""List the rays whose trace images are the tetrahedral (2,2,2) lines."""

from __future__ import annotations

import json
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "witting_pg32_tetrahedral_rays.json"
OUT_MD = ROOT / "artifacts" / "witting_pg32_tetrahedral_rays.md"


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


def weight(t):
    return sum(t)


def main():
    base_states = [normalize_projective(s) for s in build_base_states()]
    base_states = list(dict.fromkeys(base_states))
    if len(base_states) != 40:
        raise SystemExit(f"Expected 40 projective states, got {len(base_states)}")

    scalars = [1, omega, omega2]
    records = []
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
                records.append({"index": idx, "state": s, "line": imgs})

    # group by line
    line_map = {}
    for rec in records:
        line = tuple(rec["line"])
        line_map.setdefault(line, []).append(rec["index"])

    results = {
        "tetrahedral_rays": records,
        "line_to_rays": {str(k): v for k, v in line_map.items()},
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(results, indent=2), encoding="utf-8")

    lines = []
    lines.append("# Tetrahedral Rays (line pattern (2,2,2))")
    lines.append("")
    lines.append(f"- ray count: {len(records)}")
    lines.append(f"- distinct lines: {len(line_map)}")
    lines.append("")
    for line, rays in line_map.items():
        lines.append(f"- line {line}: rays {rays}")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
