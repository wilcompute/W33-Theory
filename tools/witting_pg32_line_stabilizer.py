#!/usr/bin/env python3
"""Compute the GL(4,2) stabilizer of the 16 hit lines in PG(3,2).

We rebuild the Witting ray trace images (GF(4)->GF(2)) to recover the
16 distinct PG(3,2) lines hit by rays, then enumerate GL(4,2) and find
the subgroup that preserves this line set.

Outputs:
- artifacts/witting_pg32_line_stabilizer.json
- artifacts/witting_pg32_line_stabilizer.md
"""

from __future__ import annotations

import json
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "witting_pg32_line_stabilizer.json"
OUT_MD = ROOT / "artifacts" / "witting_pg32_line_stabilizer.md"


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


def bits_to_tuple(x):
    return ((x >> 3) & 1, (x >> 2) & 1, (x >> 1) & 1, x & 1)


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


def apply_matrix(rows, v):
    # rows are 4-bit ints; v is 4-bit int
    out = 0
    for i, row in enumerate(rows):
        bit = parity(row & v)
        out |= bit << (3 - i)
    return out


def span(basis):
    s = {0}
    for v in basis:
        s |= {x ^ v for x in list(s)}
    return s


def enumerate_gl4():
    vecs = [i for i in range(1, 16)]
    mats = []
    for r1 in vecs:
        span1 = span([r1])
        for r2 in vecs:
            if r2 in span1:
                continue
            span2 = span([r1, r2])
            for r3 in vecs:
                if r3 in span2:
                    continue
                span3 = span([r1, r2, r3])
                for r4 in vecs:
                    if r4 in span3:
                        continue
                    mats.append((r1, r2, r3, r4))
    return mats


def main():
    # Rebuild Witting ray images and hit lines
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
    hit_line_set = {tuple(sorted(line)) for line in hit_lines}
    covered_points = sorted(set(p for line in hit_lines for p in line))

    # GL(4,2) stabilizer
    stabilizer = []
    for rows in enumerate_gl4():
        ok = True
        for line in hit_lines:
            img = tuple(sorted(apply_matrix(rows, v) for v in line))
            if img not in hit_line_set:
                ok = False
                break
        if ok:
            stabilizer.append(rows)

    # Orbits on points/lines
    def orbit_of_point(p):
        return {apply_matrix(rows, p) for rows in stabilizer}

    def orbit_of_line(line):
        return {
            tuple(sorted(apply_matrix(rows, v) for v in line)) for rows in stabilizer
        }

    point_orbits = []
    seen_points = set()
    for p in covered_points:
        if p in seen_points:
            continue
        orb = orbit_of_point(p)
        seen_points |= orb
        point_orbits.append(sorted(orb))

    line_orbits = []
    seen_lines = set()
    for line in hit_lines:
        if line in seen_lines:
            continue
        orb = orbit_of_line(line)
        seen_lines |= orb
        line_orbits.append(sorted(orb))

    missing_point = 15  # 1111
    fixes_missing = all(
        apply_matrix(rows, missing_point) == missing_point for rows in stabilizer
    )

    results = {
        "stabilizer_order": len(stabilizer),
        "covered_points": len(covered_points),
        "hit_lines": len(hit_lines),
        "missing_point": missing_point,
        "fixes_missing_point": fixes_missing,
        "point_orbit_sizes": sorted([len(o) for o in point_orbits]),
        "line_orbit_sizes": sorted([len(o) for o in line_orbits]),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(results, indent=2), encoding="utf-8")

    lines = []
    lines.append("# GL(4,2) Stabilizer of Hit Lines")
    lines.append("")
    lines.append(f"- hit lines: {results['hit_lines']}")
    lines.append(
        f"- covered points: {results['covered_points']} (missing point: {missing_point:04b})"
    )
    lines.append(f"- stabilizer order: {results['stabilizer_order']}")
    lines.append(f"- fixes missing point: {results['fixes_missing_point']}")
    lines.append(f"- point orbit sizes: {results['point_orbit_sizes']}")
    lines.append(f"- line orbit sizes: {results['line_orbit_sizes']}")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
