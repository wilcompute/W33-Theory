#!/usr/bin/env python3
"""Pass 4588 -- apartment/half-spinor comparison and exact selector obstruction.

This pass starts from the W33-derived O+(8,2) quotient of Passes 4579/4587.
Every W33 apartment determines a totally singular line by its two opposite
line-pair differences.  The image is a distinguished 270-line orbit.  The six
apartment lifts over one selected singular line are then compared equivariantly
with the six maximal totally singular generators containing that line.

The comparison is deliberately a G-set test, not a count match.  It yields an
exact obstruction to identifying those two six-sets.  The same computation also
finds three honest copies of the 36-spread W33 G-set inside one half-spinor
family.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict, deque
from itertools import combinations
from pathlib import Path

import numpy as np

from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import (
    build_geometry, build_line_perm, transvection_matrix,
)
from w33_pass4587_w33_derived_d4_triality import rank_basis_int, span

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_PASS4588_APARTMENT_TRIALITY_OBSTRUCTION.json"


def compose(p, q):
    return tuple(p[q[i]] for i in range(len(p)))


def perm_group(gens, n=40):
    I = tuple(range(n))
    seen = {I}
    Q = deque([I])
    while Q:
        g = Q.popleft()
        for h in gens:
            z = compose(h, g)
            if z not in seen:
                seen.add(z)
                Q.append(z)
    return seen


def pmask(mask, p):
    y = 0
    for i in range(len(p)):
        if (mask >> i) & 1:
            y |= 1 << p[i]
    return y


def main() -> int:
    pts, pidx, lines, lidx, _, Astar, _, apartments, _ = build_geometry()
    Astar = np.asarray(Astar, dtype=np.uint8)
    n = 40
    j = (1 << n) - 1

    cols = []
    for c in range(n):
        m = 0
        for r in np.flatnonzero(Astar[:, c]):
            m |= 1 << int(r)
        cols.append(m)
    edges = [(i, k) for i in range(n) for k in range(i + 1, n) if Astar[i, k]]
    B9 = rank_basis_int([cols[i] ^ cols[k] for i, k in edges])
    V9 = set(span(B9))
    assert len(B9) == 9 and len(V9) == 512 and j in V9
    reps = {min(x, x ^ j) for x in V9}

    def rep(x):
        return min(int(x), int(x) ^ j)

    def q(x):
        return (rep(x).bit_count() // 4) & 1

    def polar(x, y):
        return q(x) ^ q(y) ^ q(rep(x) ^ rep(y))

    singular = sorted(x for x in reps if x and q(x) == 0)
    assert len(singular) == 135

    # All maximal totally singular 4-spaces, as in Pass 4587.
    levels = {0: {frozenset((0,))}}
    for d in range(4):
        nxt = set()
        for S in levels[d]:
            for v in singular:
                if v in S or any(polar(v, u) for u in S):
                    continue
                T = frozenset(set(S) | {rep(u ^ v) for u in S})
                if len(T) == (1 << (d + 1)) and all(q(u) == 0 for u in T):
                    nxt.add(T)
        levels[d + 1] = nxt
    generators = sorted(levels[4], key=lambda S: tuple(sorted(S)))
    assert len(generators) == 270

    G0 = generators[0]
    idim = lambda X, Y: (len(X & Y)).bit_length() - 1
    fam_a = [G for G in generators if idim(G0, G) % 2 == 0]
    fam_b = [G for G in generators if idim(G0, G) % 2 == 1]
    assert (len(fam_a), len(fam_b)) == (135, 135)

    # Apartment -> singular line.  The two nonedges of the C4 give singular
    # vectors s,t and the apartment fiber is s+t.
    def apartment_fiber(ap):
        x = 0
        for i in ap:
            x ^= cols[int(i)]
        return rep(x)

    def apartment_singular_line(ap):
        opp = [(a, b) for a, b in combinations(ap, 2) if not Astar[a, b]]
        assert len(opp) == 2
        s = rep(cols[opp[0][0]] ^ cols[opp[0][1]])
        t = rep(cols[opp[1][0]] ^ cols[opp[1][1]])
        x = apartment_fiber(ap)
        assert q(s) == q(t) == q(x) == 0 and rep(s ^ t) == x
        return tuple(sorted((s, t, x)))

    line_fiber = defaultdict(list)
    flag_fiber = Counter()
    for ap in apartments:
        L = apartment_singular_line(ap)
        x = apartment_fiber(ap)
        assert x in L
        line_fiber[L].append(tuple(map(int, ap)))
        flag_fiber[(L, x)] += 1

    assert len(line_fiber) == 270
    assert Counter(map(len, line_fiber.values())) == Counter({6: 270})
    assert len(flag_fiber) == 810 and Counter(flag_fiber.values()) == Counter({2: 810})
    selected_lines = sorted(line_fiber)
    point_degrees = Counter(x for L in selected_lines for x in L)
    assert Counter(point_degrees.values()) == Counter({6: 135})

    # Build PSp(4,3) on W33 lines.
    cand = [build_line_perm(transvection_matrix(v), pts, pidx, lines, lidx) for v in pts]
    gens = []
    G = {tuple(range(40))}
    for g in cand:
        if g in G:
            continue
        gens.append(g)
        G = perm_group(gens)
        if len(G) == 25920:
            break
    assert len(G) == 25920

    def act_v(x, g):
        return rep(pmask(rep(x), g))

    def act_sline(L, g):
        return tuple(sorted(act_v(x, g) for x in L))

    selected_set = set(selected_lines)
    L0 = selected_lines[0]
    assert {act_sline(L0, g) for g in G} == selected_set
    H = [g for g in G if act_sline(L0, g) == L0]
    assert len(H) == 96

    six_apartments = sorted(line_fiber[L0])
    six_generators = [X for X in generators if set(L0).issubset(X)]
    assert len(six_apartments) == len(six_generators) == 6
    ap_idx = {ap: i for i, ap in enumerate(six_apartments)}
    gen_idx = {X: i for i, X in enumerate(six_generators)}

    def act_ap(ap, g):
        return tuple(sorted(g[i] for i in ap))

    def act_gen(X, g):
        return frozenset(act_v(x, g) for x in X)

    ap_perms = []
    gen_perms = []
    fixed_profile = Counter()
    for g in H:
        pa = tuple(ap_idx[act_ap(ap, g)] for ap in six_apartments)
        pg = tuple(gen_idx[act_gen(X, g)] for X in six_generators)
        ap_perms.append(pa)
        gen_perms.append(pg)
        fixed_profile[(sum(pa[i] == i for i in range(6)), sum(pg[i] == i for i in range(6)))] += 1

    ap_image = set(ap_perms)
    gen_image = set(gen_perms)
    ident6 = tuple(range(6))
    ap_kernel = {g for g, p in zip(H, ap_perms) if p == ident6}
    gen_kernel = {g for g, p in zip(H, gen_perms) if p == ident6}
    assert len(ap_image) == len(gen_image) == 12
    assert len(ap_kernel) == len(gen_kernel) == 8 and ap_kernel == gen_kernel
    assert len({p[0] for p in ap_image}) == 6  # apartment action is transitive

    # The generator action is not transitive, hence no H-equivariant bijection
    # between the two six-sets.  The character mismatch makes the obstruction
    # stronger than a labelling-dependent orbit statement.
    rem = set(range(6))
    gen_orbit_sizes = []
    while rem:
        a = min(rem)
        O = {p[a] for p in gen_image}
        gen_orbit_sizes.append(len(O))
        rem -= O
    assert sorted(gen_orbit_sizes) == [1, 2, 3]
    assert fixed_profile == Counter({(0, 4): 32, (2, 2): 24, (0, 1): 16, (0, 3): 16, (6, 6): 8})

    # Global PSp orbit structure on the 270 maximal singular generators.
    remaining = set(generators)
    generator_orbits = []
    while remaining:
        X = next(iter(remaining))
        O = {act_gen(X, g) for g in G}
        generator_orbits.append(O)
        remaining -= O
    assert sorted(map(len, generator_orbits)) == [27, 36, 36, 36, 135]

    # Enumerate all 36 W33 spreads and test the G-set identification rather
    # than naming the degree-36 orbits by cardinality.
    lines_by_point = defaultdict(list)
    for li, L in enumerate(lines):
        for p in L:
            lines_by_point[p].append(li)
    spreads = set()

    def backtrack_spread(chosen, used):
        if len(chosen) == 10:
            if len(used) == 40:
                spreads.add(tuple(sorted(chosen)))
            return
        p = next((x for x in range(40) if x not in used), None)
        if p is None:
            return
        for li in lines_by_point[p]:
            L = set(lines[li])
            if used.isdisjoint(L):
                backtrack_spread(chosen + [li], used | L)

    backtrack_spread([], set())
    spreads = sorted(spreads)
    assert len(spreads) == 36

    def act_spread(S, g):
        return tuple(sorted(g[i] for i in S))

    spread_set = set(spreads)
    assert {act_spread(spreads[0], g) for g in G} == spread_set

    degree36_certificates = []
    for O in generator_orbits:
        if len(O) != 36:
            continue
        X = next(iter(O))
        SX = [g for g in G if act_gen(X, g) == X]
        assert len(SX) == 720
        fixed_spreads = [S for S in spreads if all(act_spread(S, g) == S for g in SX)]
        assert len(fixed_spreads) == 1
        degree36_certificates.append({"generator_stabilizer_order": 720, "fixed_spreads": 1})
    assert len(degree36_certificates) == 3

    # The selected 270-line orbit distinguishes the two half-spinor families.
    # Every member of the transitive 135-orbit contains six selected lines;
    # the other family decomposes as 27+36+36+36.
    selected_subspace_counts = Counter(
        sum(set(L).issubset(X) for L in selected_lines) for X in generators
    )
    assert selected_subspace_counts == Counter({6: 135, 0: 72, 15: 36, 10: 27})

    out = {
        "pass": 4588,
        "apartment_to_singular_line": {
            "apartments": 1620,
            "selected_singular_lines": 270,
            "apartments_per_selected_line": 6,
            "selected_line_points": 3,
            "selected_lines_through_each_singular_point": 6,
            "apartment_lifts_per_point_line_flag": 2,
            "selected_line_stabilizer_order": 96,
        },
        "local_selector_test": {
            "apartment_lifts": 6,
            "maximal_singular_generators_containing_line": 6,
            "common_kernel_order": 8,
            "both_image_orders": 12,
            "apartment_action": "transitive degree 6",
            "generator_action_orbits": [1, 2, 3],
            "fixed_point_pair_profile": {"(0,4)": 32, "(2,2)": 24, "(0,1)": 16, "(0,3)": 16, "(6,6)": 8},
            "equivariant_bijection": false,
            "obstruction": "The two six-point H-sets have different permutation characters; equal cardinality and equal image order do not make them the same G-set.",
        },
        "half_spinor_PSp_orbits": [27, 36, 36, 36, 135],
        "spread_bridge": {
            "W33_spreads": 36,
            "degree36_half_spinor_orbits": 3,
            "certificate": "For each degree-36 orbit, a representative stabilizer has order 720 and fixes exactly one W33 spread, so its stabilizer equals a spread stabilizer and the transitive G-sets are isomorphic.",
        },
        "selected_line_counts_inside_maximal_generators": {"6": 135, "0": 72, "15": 36, "10": 27},
        "theorem": "Apartments form a 2-fold cover of the flags of a distinguished 135_6-270_3 singular-line geometry.  Its six apartment lifts over a selected line are not equivariantly the six half-spinor generators through that line.  Globally, however, one half-spinor family contains three genuine PSp(4,3)-equivariant copies of the 36-spread carrier.",
        "boundary": "The degree-27 orbit is intentionally left unnamed here; a matching cardinality is not a G-set identification.  No physical spinor interpretation is asserted.",
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
