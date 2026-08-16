#!/usr/bin/env python3
"""Pass5596 addendum: realize the Latin/Relye 576 group on F4 short-root pairs.

Build the 48 F4 roots in integer-scaled coordinates, generate W(F4) from four
simple-root reflections, quotient its action by antipodes on the 24 short roots,
and compare the resulting degree-12 permutation group with the independently
constructed Klein-V4 Latin autoparatopy group.
"""
from __future__ import annotations

import itertools
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_W33_PASS5596_F4_ROOTPAIR_LATIN_ACTION.json"


def compose(a, b):
    return tuple(a[b[i]] for i in range(len(a)))


def inverse_perm(a):
    out = [0] * len(a)
    for i, j in enumerate(a):
        out[j] = i
    return tuple(out)


def f4_roots():
    roots = []
    for i in range(4):
        for j in range(i + 1, 4):
            for si in (-2, 2):
                for sj in (-2, 2):
                    v = [0] * 4
                    v[i], v[j] = si, sj
                    roots.append(tuple(v))
    for i in range(4):
        for s in (-2, 2):
            v = [0] * 4
            v[i] = s
            roots.append(tuple(v))
    roots.extend(itertools.product((-1, 1), repeat=4))
    roots = sorted(set(tuple(x) for x in roots))
    assert len(roots) == 48
    assert sum(sum(x*x for x in r) == 4 for r in roots) == 24
    assert sum(sum(x*x for x in r) == 8 for r in roots) == 24
    return roots


def reflect(v, a):
    dot = sum(x*y for x, y in zip(v, a))
    aa = sum(x*x for x in a)
    c = Fraction(2 * dot, aa)
    w = tuple(Fraction(x) - c * Fraction(y) for x, y in zip(v, a))
    assert all(z.denominator == 1 for z in w)
    return tuple(int(z) for z in w)


def generate_group(gens, degree):
    identity = tuple(range(degree))
    group = {identity}
    frontier = [identity]
    while frontier:
        x = frontier.pop()
        for s in gens:
            y = compose(s, x)
            if y not in group:
                group.add(y)
                frontier.append(y)
    return group


def orbital_data(group, n=12):
    seen = set()
    orbits = []
    for i in range(n):
        for j in range(n):
            if (i, j) in seen:
                continue
            orb = {(g[i], g[j]) for g in group}
            seen |= orb
            orbits.append(orb)
    sizes = sorted(len(o) for o in orbits)
    small = next(o for o in orbits if len(o) == 36)
    adj = [set() for _ in range(n)]
    for i, j in small:
        if i != j:
            adj[i].add(j)
    comps = []
    done = set()
    for i in range(n):
        if i in done:
            continue
        c = {i}
        stack = [i]
        done.add(i)
        while stack:
            x = stack.pop()
            for y in adj[x]:
                if y not in done:
                    done.add(y)
                    c.add(y)
                    stack.append(y)
        comps.append(sorted(c))
    return sizes, sorted(comps)


def latin_group():
    gl = []
    for p in itertools.permutations(range(4)):
        if p[0] != 0:
            continue
        if all(p[x ^ y] == (p[x] ^ p[y]) for x in range(4) for y in range(4)):
            gl.append(p)
    group = set()
    for pi in itertools.permutations(range(3)):
        for A in gl:
            for t0 in range(4):
                for t1 in range(4):
                    ts = (t0, t1, t0 ^ t1)
                    p = [0] * 12
                    for part in range(3):
                        for x in range(4):
                            p[4 * part + x] = 4 * pi[part] + (A[x] ^ ts[part])
                    group.add(tuple(p))
    assert len(group) == 576
    return group


def find_block_conjugator(source, target, source_gens):
    _, sb = orbital_data(source)
    _, tb = orbital_data(target)
    checked = 0
    for bp in itertools.permutations(range(3)):
        dest = [tb[bp[i]] for i in range(3)]
        for m0 in itertools.permutations(dest[0]):
            for m1 in itertools.permutations(dest[1]):
                for m2 in itertools.permutations(dest[2]):
                    checked += 1
                    phi = [None] * 12
                    for src, dst in zip(sb[0], m0): phi[src] = dst
                    for src, dst in zip(sb[1], m1): phi[src] = dst
                    for src, dst in zip(sb[2], m2): phi[src] = dst
                    phi = tuple(phi)
                    iphi = inverse_perm(phi)
                    if all(compose(compose(phi, g), iphi) in target for g in source_gens):
                        return phi, checked
    raise AssertionError("no block-respecting conjugator")


def main():
    roots = f4_roots()
    ri = {r: i for i, r in enumerate(roots)}
    simple = [
        (0, 2, -2, 0),
        (0, 0, 2, -2),
        (0, 0, 0, 2),
        (1, -1, -1, -1),
    ]
    root_gens = [tuple(ri[reflect(r, a)] for r in roots) for a in simple]
    WF4 = generate_group(root_gens, 48)
    assert len(WF4) == 1152

    short = [r for r in roots if sum(x*x for x in r) == 4]
    neg = lambda v: tuple(-x for x in v)
    pairs = sorted({min(r, neg(r)) for r in short})
    pi = {p: i for i, p in enumerate(pairs)}

    def induced(g):
        out = []
        for p in pairs:
            img = roots[g[ri[p]]]
            out.append(pi[min(img, neg(img))])
        return tuple(out)

    pair_gens = [induced(g) for g in root_gens]
    pair_group = {induced(g) for g in WF4}
    assert len(pair_group) == 576

    latin = latin_group()
    os_f4, blocks_f4 = orbital_data(pair_group)
    os_lat, blocks_lat = orbital_data(latin)
    assert os_f4 == os_lat == [12, 36, 96]
    assert [len(c) for c in blocks_f4] == [4, 4, 4]
    assert [len(c) for c in blocks_lat] == [4, 4, 4]

    phi, checked = find_block_conjugator(pair_group, latin, pair_gens)
    iphi = inverse_perm(phi)
    conjugated = {compose(compose(phi, g), iphi) for g in pair_group}
    assert conjugated == latin

    out = {
        "pass": 5596,
        "status": "F4_SHORT_ROOTPAIR_ACTION_CONJUGATE_TO_LATIN12",
        "F4_roots": 48,
        "F4_short_roots": 24,
        "F4_short_antipodal_pairs": 12,
        "WF4_order": len(WF4),
        "antipodal_pair_image_order": len(pair_group),
        "antipodal_kernel_order": len(WF4) // len(pair_group),
        "latin12_order": len(latin),
        "orbital_sizes": os_f4,
        "small_orbital_components_F4_indices": blocks_f4,
        "small_orbital_components_Latin_indices": blocks_lat,
        "conjugating_permutation_F4pair_to_Latin": list(phi),
        "block_maps_checked_before_witness": checked,
        "theorem": "W(F4)/{+-1} on the 12 antipodal short-root pairs is permutation-conjugate in S12 to the Klein-V4 Latin autoparatopy action; by Pass5596 the latter is also the Reye row action.",
        "cover_boundary": "Pass5468 identifies the 13-cover setwise stabilizer with W(F4) and its 13-point image with W(F4)/{+-1}. The separate GAP Pass5596 action test decides whether its specific moving 12-orbit is this same conjugacy class.",
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    print(f"wrote {OUT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
