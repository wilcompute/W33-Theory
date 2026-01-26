#!/usr/bin/env python3
"""Analyze hit lines in PG(3,2) via Plücker (Klein quadric) coordinates.

We map each PG(3,2) line to a 6-bit Plücker vector (p01,p02,p03,p12,p13,p23).
Then we test whether the 16 hit lines from Witting ray images correspond to:
  - a linear hyperplane section in PG(5,2)
  - a quadratic form in Plücker coordinates (degree ≤ 2 over F2)

Outputs:
- artifacts/witting_pg32_line_space_plucker.json
- artifacts/witting_pg32_line_space_plucker.md
"""
from __future__ import annotations

import json
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "witting_pg32_line_space_plucker.json"
OUT_MD = ROOT / "artifacts" / "witting_pg32_line_space_plucker.md"

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

def tuple_to_bits(t):
    return (t[0] << 3) | (t[1] << 2) | (t[2] << 1) | t[3]

def bits_to_vec(x: int):
    return [(x >> 3) & 1, (x >> 2) & 1, (x >> 1) & 1, x & 1]

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

def plucker(line):
    # line given by two independent vectors in F2^4
    a, b, _ = line
    av = bits_to_vec(a)
    bv = bits_to_vec(b)
    # p_ij = a_i b_j + a_j b_i
    coords = [
        (av[0] & bv[1]) ^ (av[1] & bv[0]),  # 01
        (av[0] & bv[2]) ^ (av[2] & bv[0]),  # 02
        (av[0] & bv[3]) ^ (av[3] & bv[0]),  # 03
        (av[1] & bv[2]) ^ (av[2] & bv[1]),  # 12
        (av[1] & bv[3]) ^ (av[3] & bv[1]),  # 13
        (av[2] & bv[3]) ^ (av[3] & bv[2]),  # 23
    ]
    val = 0
    for bit in coords:
        val = (val << 1) | bit
    return val  # 6-bit int

def parity(x: int) -> int:
    return bin(x).count("1") & 1

def main():
    # build hit lines (Witting ray images)
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

    # Plücker coordinates for all lines
    line_plucker = {line: plucker(line) for line in pg_lines}
    plucker_hit = {line_plucker[line] for line in hit_lines}

    # Linear hyperplane search: w·p = 0 or 1
    best_lin = {"match": False, "w": None, "polarity": None, "overlap": -1, "jaccard": -1.0, "selected": None}
    exact_linear = []
    hit_mask = 0
    line_list = pg_lines
    for idx, line in enumerate(line_list):
        if line in hit_line_set:
            hit_mask |= (1 << idx)

    for w in range(1, 64):
        mask0 = 0
        mask1 = 0
        for idx, line in enumerate(line_list):
            p = line_plucker[line]
            val = parity(w & p)
            if val == 0:
                mask0 |= (1 << idx)
            else:
                mask1 |= (1 << idx)

        for polarity, mask in [("0", mask0), ("1", mask1)]:
            if mask == hit_mask:
                exact_linear.append({"w": w, "polarity": polarity})
            overlap = (mask & hit_mask).bit_count()
            union = (mask | hit_mask).bit_count()
            jaccard = overlap / union if union else 0.0
            if overlap > best_lin["overlap"] or (overlap == best_lin["overlap"] and jaccard > best_lin["jaccard"]):
                best_lin = {
                    "match": False,
                    "w": w,
                    "polarity": polarity,
                    "overlap": overlap,
                    "jaccard": jaccard,
                    "selected": mask.bit_count(),
                }

    # Quadratic form search on Plücker coordinates
    # monomials: 1, x_i (6), x_i x_j (15) -> 22 terms
    monomials = []
    # constant term
    monomials.append([1] * len(line_list))
    # linear terms
    for i in range(6):
        monomials.append([((line_plucker[line] >> (5 - i)) & 1) for line in line_list])
    # quadratic terms
    for i in range(6):
        for j in range(i + 1, 6):
            monomials.append([
                (((line_plucker[line] >> (5 - i)) & 1) & ((line_plucker[line] >> (5 - j)) & 1))
                for line in line_list
            ])

    # convert monomials to bitmasks
    mono_masks = []
    for mon in monomials:
        mask = 0
        for idx, val in enumerate(mon):
            if val:
                mask |= (1 << idx)
        mono_masks.append(mask)

    best_quad = {"overlap": -1, "jaccard": -1.0, "selected": None, "coeffs": None}
    exact_quad = 0
    total_forms = 1 << len(mono_masks)
    for coeff in range(total_forms):
        mask = 0
        c = coeff
        mi = 0
        while c:
            if c & 1:
                mask ^= mono_masks[mi]
            c >>= 1
            mi += 1
        if mask == hit_mask:
            exact_quad += 1
        overlap = (mask & hit_mask).bit_count()
        union = (mask | hit_mask).bit_count()
        jaccard = overlap / union if union else 0.0
        if overlap > best_quad["overlap"] or (overlap == best_quad["overlap"] and jaccard > best_quad["jaccard"]):
            best_quad = {
                "overlap": overlap,
                "jaccard": jaccard,
                "selected": mask.bit_count(),
                "coeffs": coeff,
            }

    results = {
        "line_count": len(pg_lines),
        "hit_lines": len(hit_lines),
        "plucker_unique": len(set(line_plucker.values())),
        "linear_exact_matches": len(exact_linear),
        "linear_best": best_lin,
        "quadratic_forms_tested": total_forms,
        "quadratic_exact_matches": exact_quad,
        "quadratic_best": best_quad,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(results, indent=2), encoding="utf-8")

    lines = []
    lines.append("# PG(3,2) Line Space (Plücker) Analysis")
    lines.append("")
    lines.append(f"- total lines: {results['line_count']}")
    lines.append(f"- hit lines: {results['hit_lines']}")
    lines.append(f"- unique Plücker points: {results['plucker_unique']}")
    lines.append(f"- linear exact matches: {results['linear_exact_matches']}")
    lines.append(f"- linear best overlap: {results['linear_best']['overlap']} (selected={results['linear_best']['selected']}, Jaccard={results['linear_best']['jaccard']:.3f})")
    lines.append(f"- quadratic forms tested: {results['quadratic_forms_tested']}")
    lines.append(f"- quadratic exact matches: {results['quadratic_exact_matches']}")
    lines.append(f"- quadratic best overlap: {results['quadratic_best']['overlap']} (selected={results['quadratic_best']['selected']}, Jaccard={results['quadratic_best']['jaccard']:.3f})")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")

if __name__ == "__main__":
    main()
