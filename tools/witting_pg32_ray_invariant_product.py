#!/usr/bin/env python3
"""Check simple GF(4) invariants (product/sum) vs ray image patterns."""

from __future__ import annotations

import json
from collections import defaultdict
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "witting_pg32_ray_invariant_product.json"
OUT_MD = ROOT / "artifacts" / "witting_pg32_ray_invariant_product.md"


# GF(4) arithmetic (0,1,ω,ω^2 -> 0,1,2,3)
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
    pattern_counts = defaultdict(int)
    product_counts = defaultdict(lambda: defaultdict(int))
    sum_counts = defaultdict(lambda: defaultdict(int))

    for s in base_states:
        imgs = set()
        for c in scalars:
            scaled = tuple(gf4_mul(c, x) for x in s)
            p = trace_map(scaled)
            if p != (0, 0, 0, 0):
                imgs.add(p)
        imgs = tuple(sorted(imgs))
        if len(imgs) == 1:
            pattern = f"point_w{weight(imgs[0])}"
        else:
            wpat = tuple(sorted(weight(p) for p in imgs))
            pattern = f"line_{wpat}"

        nonzeros = [x for x in s if x != 0]
        prod = 1
        for x in nonzeros:
            prod = gf4_mul(prod, x)
        total = 0
        for x in nonzeros:
            total = gf4_add(total, x)

        pattern_counts[pattern] += 1
        product_counts[pattern][prod] += 1
        sum_counts[pattern][total] += 1

    results = {
        "pattern_counts": dict(pattern_counts),
        "product_counts": {k: dict(v) for k, v in product_counts.items()},
        "sum_counts": {k: dict(v) for k, v in sum_counts.items()},
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(results, indent=2), encoding="utf-8")

    lines = []
    lines.append("# GF(4) Invariant Check (product/sum of nonzeros)")
    lines.append("")
    lines.append(f"- pattern counts: {results['pattern_counts']}")
    lines.append("")
    lines.append("## product of nonzeros by pattern")
    for pat, counts in results["product_counts"].items():
        lines.append(f"- {pat}: {counts}")
    lines.append("")
    lines.append("## sum of nonzeros by pattern")
    for pat, counts in results["sum_counts"].items():
        lines.append(f"- {pat}: {counts}")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
