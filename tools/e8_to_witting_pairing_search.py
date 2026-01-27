#!/usr/bin/env python3
"""Search for a pairing of R^8 coordinates into C^4 that yields 40 rays (6 roots per ray).

Idea:
- Take E8 roots in R^8.
- Pair coordinates into 4 complex coordinates.
- Identify rays in C^4 (complex scalar multiples).
- Look for pairings where roots cluster into 40 rays of size 6.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import combinations
from collections import Counter, defaultdict


def e8_roots():
    roots = []
    # Type 1: +-e_i +- e_j
    for i in range(8):
        for j in range(i + 1, 8):
            for si in (1, -1):
                for sj in (1, -1):
                    r = [Fraction(0)] * 8
                    r[i] = Fraction(si)
                    r[j] = Fraction(sj)
                    roots.append(tuple(r))
    # Type 2: half-integers with even number of minus signs
    for bits in range(256):
        signs = [1 if (bits >> k) & 1 else -1 for k in range(8)]
        if sum(1 for s in signs if s == -1) % 2 == 0:
            roots.append(tuple(Fraction(s, 2) for s in signs))
    return roots


def pairings_of_8():
    # Generate all perfect matchings of 8 items: 105 total.
    # Represent pairing as list of 4 pairs (a,b).
    items = list(range(8))

    def rec(remaining):
        if not remaining:
            return [[]]
        a = remaining[0]
        result = []
        for i in range(1, len(remaining)):
            b = remaining[i]
            rest = remaining[1:i] + remaining[i + 1 :]
            for tail in rec(rest):
                result.append([(a, b)] + tail)
        return result

    return rec(items)


def complex_mul(a, b, c, d):
    # (a+ib)*(c+id) = (ac-bd) + i(ad+bc)
    return (a * c - b * d, a * d + b * c)


def complex_inv(a, b):
    # 1/(a+ib) = (a-ib)/(a^2+b^2)
    denom = a * a + b * b
    return (a / denom, -b / denom)


def canonical_ray(vec):
    # vec is list of 4 complex entries (a,b) with a,b Fractions.
    # Normalize by first nonzero component to make it 1+0i.
    for (a, b) in vec:
        if a != 0 or b != 0:
            inv = complex_inv(a, b)
            normed = [complex_mul(x[0], x[1], inv[0], inv[1]) for x in vec]
            # canonical: if first nonzero component has negative real part, flip sign
            fa, fb = normed[0]
            # If the first component is -1,0 (can happen), flip sign
            if fa < 0:
                normed = [(-x[0], -x[1]) for x in normed]
            return tuple(normed)
    raise ValueError("Zero vector")


def ray_stats_for_pairing(pairing, roots):
    # pairing: list of 4 pairs
    rays = defaultdict(list)
    for idx, r in enumerate(roots):
        vec = []
        for (a, b) in pairing:
            vec.append((r[a], r[b]))
        key = canonical_ray(vec)
        rays[key].append(idx)
    sizes = Counter(len(v) for v in rays.values())
    return len(rays), sizes


def main():
    roots = e8_roots()
    pairings = pairings_of_8()
    print(f"Total roots: {len(roots)}")
    print(f"Total pairings: {len(pairings)}")

    candidates = []
    for i, pairing in enumerate(pairings):
        n_rays, sizes = ray_stats_for_pairing(pairing, roots)
        # We want 40 rays, each of size 6
        if n_rays == 40 and sizes == Counter({6: 40}):
            candidates.append(pairing)
            print(f"Found candidate pairing: {pairing}")
        if i % 10 == 0:
            print(f"Checked {i}/{len(pairings)} pairings... current rays={n_rays}, sizes={dict(sizes)}")

    print("\nCandidates:")
    for p in candidates:
        print(p)


if __name__ == "__main__":
    main()
