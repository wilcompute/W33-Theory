#!/usr/bin/env python3
"""Search for a PG(3,2) symplectic polarity maximizing isotropic hit lines.

We apply random GL(4,2) changes of basis to PG points, then evaluate how many
of the 16 hit lines become isotropic with respect to the standard symplectic form.

Outputs:
- artifacts/witting_pg32_polarity_search.json
- artifacts/witting_pg32_polarity_search.md
"""
from __future__ import annotations

import json
import os
import random
from itertools import combinations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "witting_pg32_polarity_search.json"
OUT_MD = ROOT / "artifacts" / "witting_pg32_polarity_search.md"

TRIALS = int(os.environ.get("W33_POLARITY_TRIALS", "2000"))
SEED = int(os.environ.get("W33_POLARITY_SEED", "12345"))

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

def build_pg32_points():
    return [v for v in product([0, 1], repeat=4) if v != (0, 0, 0, 0)]

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

def symplectic_dot(p, q):
    # standard symplectic form
    return (p[0] & q[2]) ^ (p[1] & q[3]) ^ (p[2] & q[0]) ^ (p[3] & q[1])

def is_isotropic_line(line):
    a, b, c = line
    return symplectic_dot(a, b) == 0 and symplectic_dot(a, c) == 0 and symplectic_dot(b, c) == 0

def random_gl4(rng):
    # random invertible 4x4 over F2
    while True:
        M = [[rng.randint(0, 1) for _ in range(4)] for _ in range(4)]
        # compute determinant mod 2
        det = 0
        for perm in [(0,1,2,3),(0,1,3,2),(0,2,1,3),(0,2,3,1),(0,3,1,2),(0,3,2,1),
                     (1,0,2,3),(1,0,3,2),(1,2,0,3),(1,2,3,0),(1,3,0,2),(1,3,2,0),
                     (2,0,1,3),(2,0,3,1),(2,1,0,3),(2,1,3,0),(2,3,0,1),(2,3,1,0),
                     (3,0,1,2),(3,0,2,1),(3,1,0,2),(3,1,2,0),(3,2,0,1),(3,2,1,0)]:
            prod = 1
            for i in range(4):
                prod &= M[i][perm[i]]
            det ^= prod
        if det == 1:
            return M

def apply_mat(M, v):
    return tuple(sum(M[i][j] * v[j] for j in range(4)) % 2 for i in range(4))

def main():
    base_states = [normalize_projective(s) for s in build_base_states()]
    base_states = list(dict.fromkeys(base_states))
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
    hit_lines = sorted(set(tuple(im) for im in ray_images if len(im) == 3 and tuple(im) in pg_line_set))

    rng = random.Random(SEED)
    best = {"iso_count": -1, "matrix": None}
    iso_counts = []
    for _ in range(TRIALS):
        M = random_gl4(rng)
        count = 0
        for line in hit_lines:
            line_t = tuple(sorted(apply_mat(M, p) for p in line))
            if is_isotropic_line(line_t):
                count += 1
        iso_counts.append(count)
        if count > best["iso_count"]:
            best = {"iso_count": count, "matrix": M}

    summary = {
        "hit_line_count": len(hit_lines),
        "trials": TRIALS,
        "best_isotropic_count": best["iso_count"],
        "best_matrix": best["matrix"],
        "iso_count_hist": {str(k): iso_counts.count(k) for k in sorted(set(iso_counts))},
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    lines = []
    lines.append("# PG(3,2) Polarity Search (Hit Lines)")
    lines.append("")
    lines.append(f"- hit lines: {summary['hit_line_count']}")
    lines.append(f"- trials: {summary['trials']}")
    lines.append(f"- best isotropic count: {summary['best_isotropic_count']}")
    lines.append(f"- isotropic count histogram: {summary['iso_count_hist']}")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")

if __name__ == "__main__":
    main()
