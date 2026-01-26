#!/usr/bin/env python3
"""Search simple quadratic-form rules that select the 16 hit lines.

We enumerate all quadratic forms Q on F2^4 (6 cross terms, 4 linear, 1 constant),
classify lines by the count of ones of Q on their 3 points, and test whether
any subset of counts {0,1,2,3} reproduces the 16 hit lines.

Outputs:
- artifacts/witting_pg32_quadratic_rule_search.json
- artifacts/witting_pg32_quadratic_rule_search.md
"""
from __future__ import annotations

import json
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "witting_pg32_quadratic_rule_search.json"
OUT_MD = ROOT / "artifacts" / "witting_pg32_quadratic_rule_search.md"

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

def tuple_to_bits(t):
    return (t[0] << 3) | (t[1] << 2) | (t[2] << 1) | t[3]

def build_pg32_points():
    return [v for v in range(1, 16)]

def build_pg32_lines(points):
    lines = set()
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            p = points[i]
            q = points[j]
            r = p ^ q
            line = tuple(sorted([p, q, r]))
            lines.add(line)
    return sorted(lines)

def q_eval(coeffs, x):
    # coeffs: 6 cross, 4 linear, 1 constant
    (a01, a02, a03, a12, a13, a23, b0, b1, b2, b3, c) = coeffs
    x0 = (x >> 3) & 1
    x1 = (x >> 2) & 1
    x2 = (x >> 1) & 1
    x3 = x & 1
    val = 0
    val ^= a01 & x0 & x1
    val ^= a02 & x0 & x2
    val ^= a03 & x0 & x3
    val ^= a12 & x1 & x2
    val ^= a13 & x1 & x3
    val ^= a23 & x2 & x3
    val ^= b0 & x0
    val ^= b1 & x1
    val ^= b2 & x2
    val ^= b3 & x3
    val ^= c
    return val

def main():
    # Build hit lines
    base_states = [normalize_projective(s) for s in build_base_states()]
    base_states = list(dict.fromkeys(base_states))
    if len(base_states) != 40:
        raise SystemExit(f"Expected 40 projective states, got {len(base_states)}")

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

    hit_lines = []
    for im in ray_images:
        if len(im) != 3:
            continue
        line_bits = tuple(sorted(tuple_to_bits(p) for p in im))
        if line_bits in pg_line_set:
            hit_lines.append(line_bits)
    hit_lines = sorted(set(hit_lines))
    hit_line_set = set(hit_lines)

    best_overlap = -1
    best_jaccard = -1.0
    best_records = []
    exact_records = []

    counts = [0, 1, 2, 3]
    subsets = []
    for mask in range(1, 1 << 4):
        subset = {counts[i] for i in range(4) if (mask >> i) & 1}
        subsets.append(subset)

    for coeffs in product([0, 1], repeat=11):
        line_counts = {}
        for line in pg_lines:
            p, q, r = line
            cnt = q_eval(coeffs, p) + q_eval(coeffs, q) + q_eval(coeffs, r)
            line_counts[line] = cnt

        for subset in subsets:
            selected = {line for line, cnt in line_counts.items() if cnt in subset}
            if selected == hit_line_set:
                exact_records.append({"subset": sorted(subset), "coeffs": coeffs})
                continue
            overlap = len(selected & hit_line_set)
            union = len(selected | hit_line_set)
            jaccard = overlap / union if union else 0.0
            if overlap > best_overlap or (overlap == best_overlap and jaccard > best_jaccard):
                best_overlap = overlap
                best_jaccard = jaccard
                best_records = [{"subset": sorted(subset), "coeffs": coeffs, "overlap": overlap, "jaccard": jaccard, "selected": len(selected)}]
            elif overlap == best_overlap and abs(jaccard - best_jaccard) < 1e-9:
                if len(best_records) < 5:
                    best_records.append({"subset": sorted(subset), "coeffs": coeffs, "overlap": overlap, "jaccard": jaccard, "selected": len(selected)})

    results = {
        "hit_lines": len(hit_line_set),
        "quadratic_forms": 2 ** 11,
        "exact_rule_matches": len(exact_records),
        "best_overlap": best_overlap,
        "best_jaccard": best_jaccard,
        "best_examples": best_records,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(results, indent=2), encoding="utf-8")

    lines = []
    lines.append("# Quadratic Rule Search (Line Selection by Q-values)")
    lines.append("")
    lines.append(f"- hit lines: {results['hit_lines']}")
    lines.append(f"- quadratic forms tested: {results['quadratic_forms']}")
    lines.append(f"- exact matches: {results['exact_rule_matches']}")
    lines.append(f"- best overlap: {results['best_overlap']} (Jaccard {results['best_jaccard']:.3f})")
    if results["best_examples"]:
        ex = results["best_examples"][0]
        lines.append(f"- example best subset: {ex['subset']} with selected={ex['selected']}")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")

if __name__ == "__main__":
    main()
