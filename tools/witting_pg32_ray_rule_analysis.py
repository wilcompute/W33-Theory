#!/usr/bin/env python3
"""Search for a GF(4) ray-level rule that yields the (1,2,3) vs (2,2,2) patterns.

We compute the trace-map image for each Witting ray and classify:
  - size 1 (single point)
  - size 3 (PG line) with weight pattern (1,2,3) or (2,2,2)

Then we group rays by simple GF(4) invariants (zero-count, value counts, etc.)
to see which invariant uniquely predicts the pattern.

Outputs:
- artifacts/witting_pg32_ray_rule_analysis.json
- artifacts/witting_pg32_ray_rule_analysis.md
"""

from __future__ import annotations

import json
from collections import defaultdict
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "witting_pg32_ray_rule_analysis.json"
OUT_MD = ROOT / "artifacts" / "witting_pg32_ray_rule_analysis.md"


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

    ray_records = []
    pattern_groups = defaultdict(list)
    invariant_groups = defaultdict(lambda: defaultdict(int))

    for idx, s in enumerate(base_states):
        imgs = set()
        for c in scalars:
            scaled = tuple(gf4_mul(c, x) for x in s)
            p = trace_map(scaled)
            if p != (0, 0, 0, 0):
                imgs.add(p)
        imgs = tuple(sorted(imgs))
        img_size = len(imgs)

        if img_size == 1:
            pattern = f"point_w{weight(imgs[0])}"
        else:
            wpat = tuple(sorted(weight(p) for p in imgs))
            pattern = f"line_{wpat}"

        # simple invariants on s
        counts = {v: s.count(v) for v in [0, 1, 2, 3]}
        inv_key = (
            counts[0],  # zeros
            counts[1],  # ones
            counts[2],  # omega
            counts[3],  # omega^2
        )
        support = 4 - counts[0]
        inv_key2 = (support, counts[1], counts[2], counts[3])
        inv_key3 = (support, counts[1], counts[2] + counts[3])  # omega/omega2 merged

        ray_records.append(
            {
                "index": idx,
                "state": s,
                "pattern": pattern,
                "counts": counts,
                "support": support,
                "img_size": img_size,
                "imgs": imgs,
            }
        )

        pattern_groups[pattern].append(idx)
        invariant_groups["zeros"].setdefault(inv_key, 0)
        invariant_groups["zeros"][inv_key] += 1
        invariant_groups["support_split"].setdefault(inv_key2, 0)
        invariant_groups["support_split"][inv_key2] += 1
        invariant_groups["support_merged"].setdefault(inv_key3, 0)
        invariant_groups["support_merged"][inv_key3] += 1

    # For each invariant, check which patterns appear
    inv_pattern_map = defaultdict(lambda: defaultdict(set))
    for rec in ray_records:
        counts = rec["counts"]
        inv_key = (counts[0], counts[1], counts[2], counts[3])
        inv_key2 = (rec["support"], counts[1], counts[2], counts[3])
        inv_key3 = (rec["support"], counts[1], counts[2] + counts[3])
        inv_pattern_map["zeros"][inv_key].add(rec["pattern"])
        inv_pattern_map["support_split"][inv_key2].add(rec["pattern"])
        inv_pattern_map["support_merged"][inv_key3].add(rec["pattern"])

    results = {
        "pattern_counts": {k: len(v) for k, v in pattern_groups.items()},
        "patterns": {k: v for k, v in pattern_groups.items()},
        "invariant_pattern_map": {
            key: {str(k): sorted(list(v)) for k, v in mapping.items()}
            for key, mapping in inv_pattern_map.items()
        },
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(results, indent=2), encoding="utf-8")

    lines = []
    lines.append("# Ray Rule Analysis (GF(4) invariants → trace-image patterns)")
    lines.append("")
    lines.append(f"- pattern counts: {results['pattern_counts']}")
    lines.append("")
    lines.append("## Invariant → pattern map (zeros counts)")
    for inv, pats in results["invariant_pattern_map"]["zeros"].items():
        lines.append(f"- {inv}: {pats}")

    lines.append("")
    lines.append("## Invariant → pattern map (support, exact counts)")
    for inv, pats in results["invariant_pattern_map"]["support_split"].items():
        lines.append(f"- {inv}: {pats}")

    lines.append("")
    lines.append("## Invariant → pattern map (support, omega merged)")
    for inv, pats in results["invariant_pattern_map"]["support_merged"].items():
        lines.append(f"- {inv}: {pats}")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
