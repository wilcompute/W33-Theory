#!/usr/bin/env python3
"""Exhaustively search alternating bilinear forms on F2^4 vs hit lines.

We enumerate all 4x4 alternating matrices over GF(2) (zero diagonal, symmetric),
keep the nondegenerate ones, and compare their isotropic lines to the 16 hit
lines from the Witting ray trace map.

Outputs:
- artifacts/witting_pg32_alternating_form_search.json
- artifacts/witting_pg32_alternating_form_search.md
"""
from __future__ import annotations

import json
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "witting_pg32_alternating_form_search.json"
OUT_MD = ROOT / "artifacts" / "witting_pg32_alternating_form_search.md"

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

def parity(x: int) -> int:
    return bin(x).count("1") & 1

def bilinear(A, x, y):
    # A is 4x4 list of bits, x,y are 4-bit ints
    xb = [(x >> (3 - i)) & 1 for i in range(4)]
    yb = [(y >> (3 - i)) & 1 for i in range(4)]
    s = 0
    for i in range(4):
        for j in range(4):
            s ^= (A[i][j] & xb[i] & yb[j])
    return s

def det_mod2(M):
    M = [row[:] for row in M]
    n = 4
    rank = 0
    col = 0
    for r in range(n):
        while col < n and all(M[i][col] == 0 for i in range(r, n)):
            col += 1
        if col == n:
            break
        pivot = None
        for i in range(r, n):
            if M[i][col] == 1:
                pivot = i
                break
        if pivot is None:
            continue
        if pivot != r:
            M[r], M[pivot] = M[pivot], M[r]
        for i in range(r + 1, n):
            if M[i][col] == 1:
                M[i] = [(a ^ b) for a, b in zip(M[i], M[r])]
        rank += 1
        col += 1
    return 1 if rank == n else 0

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

    forms = []
    hit_hist = {}
    best_hit = -1
    best_forms = []
    exact_forms = []

    # enumerate alternating matrices (symmetric with zero diagonal)
    coeffs = list(range(2))
    for a01, a02, a03, a12, a13, a23 in product(coeffs, repeat=6):
        A = [
            [0, a01, a02, a03],
            [a01, 0, a12, a13],
            [a02, a12, 0, a23],
            [a03, a13, a23, 0],
        ]
        if det_mod2(A) == 0:
            continue

        iso_lines = []
        for line in pg_lines:
            p, q, r = line
            if bilinear(A, p, q) == 0 and bilinear(A, p, r) == 0 and bilinear(A, q, r) == 0:
                iso_lines.append(line)
        iso_set = set(iso_lines)

        hit_count = len(iso_set & hit_line_set)
        hit_hist[hit_count] = hit_hist.get(hit_count, 0) + 1
        if hit_count > best_hit:
            best_hit = hit_count
            best_forms = [(A, len(iso_lines))]
        elif hit_count == best_hit:
            best_forms.append((A, len(iso_lines)))

        if hit_count == len(hit_line_set) and len(iso_lines) == len(hit_line_set):
            exact_forms.append(A)

    results = {
        "hit_lines": len(hit_line_set),
        "nondegenerate_forms": sum(hit_hist.values()),
        "best_hit_count": best_hit,
        "hit_count_histogram": dict(sorted(hit_hist.items())),
        "best_form_count": len(best_forms),
        "exact_match_forms": len(exact_forms),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(results, indent=2), encoding="utf-8")

    lines = []
    lines.append("# Alternating Form Search (PG(3,2) vs Hit Lines)")
    lines.append("")
    lines.append(f"- hit lines: {results['hit_lines']}")
    lines.append(f"- nondegenerate alternating forms checked: {results['nondegenerate_forms']}")
    lines.append(f"- best hit count: {results['best_hit_count']}")
    lines.append(f"- exact-match forms (16/16 with 16 isotropic lines): {results['exact_match_forms']}")
    lines.append(f"- hit count histogram: {results['hit_count_histogram']}")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")

if __name__ == "__main__":
    main()
