#!/usr/bin/env python3
"""Passes 4721--4724: support-12 thickening triangles resolve the old 270-class frontier.

This verifier starts from the already certified W33 apartment model of Passes
4495/4703--4704 and proves four exact statements.

4721.  The graph on the 1620 support-12 corner-star thickenings, with adjacency
       meaning disjoint line support, is 540 disjoint triangles.

4722.  Each triangle leaves four W33 lines uncovered.  The 540 complements
       collapse 2-to-1 onto 270 four-line sets.  Those 270 sets are exactly the
       fixed-line sets of the 270 inner involutions of PSp(4,3) that fix four
       lines.  The remaining 45 inner involutions fix sixteen lines.  This
       corrects Pass 1830: its reported 2880 orbit applied a point permutation
       group to a set of line indices, so that orbit computation was not an
       action on the object being classified.

4723.  For a representative four-line residue R and its unique inner
       involution g, there are eight outer square roots h in PGSp(4,3) with
       h^2=g.  Exactly two fix four lines; they are h and h^{-1}.  The PSp
       stabilizer of either thickening triangle over R equals the PSp
       centralizer of either four-fixing square root, of order 48.  Hence the
       540 triangle G-set and the 540 four-fixing outer-order-four conjugacy
       G-set are PSp-equivariantly isomorphic, with two choices related by
       inversion.  Both are 2-covers of the same 270 involution residue orbit.
       The full PGSp stabilizers are distinct order-96 extensions sharing the
       same inner order-48 subgroup, so no untwisted PGSp identification is
       claimed.

4724.  The 270 residues form an exact incidence factorization on the forty W33
       lines.  Every line lies in 27 residues; every skew line-pair lies in
       exactly three; intersecting line-pairs lie in none.  If B is the 40x270
       incidence matrix and A_* the line-intersection graph, then

           B B^T = 27 I + 3 (J - I - A_*).

       Thus spec(BB^T)=108^1 + 18^24 + 36^15 over R, while the binary row span
       of the 270 residue masks has rank 30.  No representation name is inferred
       from the modular rank alone.

The script deliberately imports the established W33 constructor/group helpers
rather than maintaining a second geometry implementation.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict, deque
from pathlib import Path

import numpy as np

from w33_pass4495_4502_distance_prism_reconstruction import (
    J3,
    build_line_perm,
    compose_perm,
    geometry,
    perm_group,
    transvection3,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_W33_PASS4721_4724_SUPPORT12_INVOLUTION_SQUARE_ROOT_COVER.json"


def gf2_rank(masks):
    piv = {}
    for x in masks:
        y = int(x)
        while y:
            p = y.bit_length() - 1
            if p in piv:
                y ^= piv[p]
            else:
                piv[p] = y
                break
    return len(piv)


def thickening(apartment, lines):
    corners = set()
    for i, j in itertools.combinations(apartment, 2):
        z = lines[i] & lines[j]
        if z:
            corners |= z
    assert len(corners) == 4
    out = frozenset(i for i, line in enumerate(lines) if line & corners)
    assert len(out) == 12
    return out


def permute_mask(mask, perm):
    out = 0
    for i in range(40):
        if (mask >> i) & 1:
            out |= 1 << perm[i]
    return out


def inverse_perm(p):
    q = [0] * len(p)
    for i, j in enumerate(p):
        q[j] = i
    return tuple(q)


def fixed_mask(p):
    return sum(1 << i for i in range(40) if p[i] == i)


def conjugate(a, x):
    return compose_perm(compose_perm(a, x), inverse_perm(a))


def act_triangle(triangle, p):
    return frozenset(permute_mask(mask, p) for mask in triangle)


def build_groups(pts, pidx, lines):
    trans = [build_line_perm(transvection3(v), pts, pidx, lines) for v in pts]
    selected = []
    inner = {tuple(range(40))}
    for p in trans:
        trial = perm_group(selected + [p])
        if len(trial) > len(inner):
            selected.append(p)
            inner = trial
        if len(inner) == 25920:
            break
    assert len(inner) == 25920

    outer_matrix = np.diag([1, 2, 1, 2]) % 3
    assert np.array_equal((outer_matrix.T @ J3 @ outer_matrix) % 3, (2 * J3) % 3)
    outer = build_line_perm(outer_matrix, pts, pidx, lines)
    full = perm_group(selected + [outer])
    assert len(full) == 51840
    return selected, inner, full


def main() -> int:
    pts, pidx, lines, astar, apartments, _apmasks, _H = geometry()
    assert len(lines) == 40 and len(apartments) == 1620

    # Pass 4721: disjointness graph of the exact support-12 minimum shell.
    thickenings = [thickening(ap, lines) for ap in apartments]
    assert len(set(thickenings)) == 1620
    tmasks = [sum(1 << i for i in t) for t in thickenings]
    tindex = {m: i for i, m in enumerate(tmasks)}

    nbr = [[] for _ in range(1620)]
    for i in range(1620):
        for j in range(i + 1, 1620):
            if tmasks[i] & tmasks[j] == 0:
                nbr[i].append(j)
                nbr[j].append(i)
    assert Counter(map(len, nbr)) == Counter({2: 1620})

    seen = set()
    components = []
    for seed in range(1620):
        if seed in seen:
            continue
        q = deque([seed])
        seen.add(seed)
        comp = set([seed])
        while q:
            u = q.popleft()
            for v in nbr[u]:
                if v not in seen:
                    seen.add(v)
                    comp.add(v)
                    q.append(v)
        components.append(tuple(sorted(comp)))
    assert len(components) == 540
    assert Counter(map(len, components)) == Counter({3: 540})
    for comp in components:
        assert all(b in nbr[a] for a, b in itertools.combinations(comp, 2))

    all40 = (1 << 40) - 1
    residues = []
    for comp in components:
        union = 0
        for i in comp:
            union |= tmasks[i]
        assert union.bit_count() == 36
        r = all40 ^ union
        ridx = [i for i in range(40) if (r >> i) & 1]
        assert len(ridx) == 4
        assert all(astar[i, j] == 0 for i, j in itertools.combinations(ridx, 2))
        residues.append(r)
    rc = Counter(residues)
    assert len(rc) == 270 and Counter(rc.values()) == Counter({2: 270})

    # Pass 4722: identify the 270 residues with the four-fixed-line involutions.
    _gens, inner, full = build_groups(pts, pidx, lines)
    ident = tuple(range(40))
    involutions = [p for p in inner if p != ident and compose_perm(p, p) == ident]
    assert len(involutions) == 315
    fixed_census = Counter(fixed_mask(p).bit_count() for p in involutions)
    assert fixed_census == Counter({4: 270, 16: 45})

    four_fixed = {}
    for p in involutions:
        f = fixed_mask(p)
        if f.bit_count() == 4:
            assert f not in four_fixed
            four_fixed[f] = p
    assert len(four_fixed) == 270
    assert set(four_fixed) == set(rc)

    # The residue orbit/stabilizer gives the corrected orbit size directly on lines.
    r0 = next(iter(rc))
    residue_orbit = {permute_mask(r0, p) for p in inner}
    residue_stab = {p for p in inner if permute_mask(r0, p) == r0}
    assert residue_orbit == set(rc)
    assert len(residue_stab) == 96
    g = four_fixed[r0]
    assert sum(1 for p in involutions if fixed_mask(p) == r0) == 1

    # Pass 4723: the two square-root sheets and the triangle G-set.
    roots = [p for p in full if p not in inner and compose_perm(p, p) == g]
    assert len(roots) == 8
    roots4 = [p for p in roots if fixed_mask(p).bit_count() == 4]
    assert len(roots4) == 2
    h = roots4[0]
    assert set(roots4) == {h, inverse_perm(h)}
    assert all(compose_perm(compose_perm(x, x), compose_perm(x, x)) == ident for x in roots)

    comp_ids = [i for i, r in enumerate(residues) if r == r0]
    assert len(comp_ids) == 2
    tri0 = frozenset(tmasks[i] for i in components[comp_ids[0]])
    tri1 = frozenset(tmasks[i] for i in components[comp_ids[1]])
    assert act_triangle(tri0, h) == tri1 and act_triangle(tri1, h) == tri0

    tri_stab = {p for p in inner if act_triangle(tri0, p) == tri0}
    h_cent = {p for p in inner if compose_perm(p, h) == compose_perm(h, p)}
    assert len(tri_stab) == len(h_cent) == 48
    assert tri_stab == h_cent

    tri_orbit = {act_triangle(tri0, p) for p in inner}
    h_orbit = {conjugate(p, h) for p in inner}
    assert len(tri_orbit) == 540
    assert len(h_orbit) == 540
    assert Counter(fixed_mask(x).bit_count() for x in h_orbit) == Counter({4: 540})
    assert len({fixed_mask(x) for x in h_orbit}) == 270
    assert Counter(fixed_mask(x) for x in h_orbit) == Counter({r: 2 for r in rc})

    # Full PGSp extensions exist but are not the same subgroup: this is the
    # explicit outer-twist boundary for the otherwise canonical inner G-set map.
    tri_stab_full = {p for p in full if act_triangle(tri0, p) == tri0}
    h_cent_full = {p for p in full if compose_perm(p, h) == compose_perm(h, p)}
    assert len(tri_stab_full) == len(h_cent_full) == 96
    assert tri_stab_full != h_cent_full
    assert tri_stab_full & h_cent_full == tri_stab

    # Pass 4724: exact 40 x 270 incidence factorization.
    blocks = sorted(rc)
    B = np.zeros((40, 270), dtype=np.int64)
    for j, r in enumerate(blocks):
        for i in range(40):
            if (r >> i) & 1:
                B[i, j] = 1
    assert set(B.sum(axis=0).tolist()) == {4}
    assert set(B.sum(axis=1).tolist()) == {27}

    pair_counts = Counter()
    for r in blocks:
        ids = [i for i in range(40) if (r >> i) & 1]
        for a, b in itertools.combinations(ids, 2):
            pair_counts[(a, b)] += 1
    skew_pairs = {(a, b) for a, b in itertools.combinations(range(40), 2) if not astar[a, b]}
    meeting_pairs = {(a, b) for a, b in itertools.combinations(range(40), 2) if astar[a, b]}
    assert len(skew_pairs) == 540 and len(meeting_pairs) == 240
    assert set(pair_counts) == skew_pairs
    assert Counter(pair_counts.values()) == Counter({3: 540})

    acomp = np.ones((40, 40), dtype=np.int64) - np.eye(40, dtype=np.int64) - astar.astype(np.int64)
    gram = B @ B.T
    assert np.array_equal(gram, 27 * np.eye(40, dtype=np.int64) + 3 * acomp)
    assert gf2_rank(blocks) == 30

    # A useful character datum: each 270-class involution fixes 24 support-12
    # thickenings and therefore eight of the 540 disjointness triangles.
    fixed_thickenings = [m for m in tmasks if permute_mask(m, g) == m]
    fixed_triangles = [tr for tr in tri_orbit if act_triangle(tr, g) == tr]
    assert len(fixed_thickenings) == 24
    assert len(fixed_triangles) == 8

    out = {
        "passes": [4721, 4722, 4723, 4724],
        "4721_support12_disjointness": {
            "vertices": 1620,
            "degree": 2,
            "components": 540,
            "component_graph": "K3",
            "triangle_union_lines": 36,
            "residual_lines": 4,
            "distinct_residues": 270,
            "triangles_per_residue": 2,
        },
        "4722_involution_resolution": {
            "PSp_order": 25920,
            "inner_involutions_total": 315,
            "fixed_line_census": {"4": 270, "16": 45},
            "residues_equal_four_fixed_line_sets": True,
            "unique_involution_per_residue": True,
            "residue_stabilizer_order_PSp": 96,
            "old_pass1830_erratum": "Its 2880 orbit used a permutation group on W33 point positions on a set of W33 line indices.  Under the induced line action the four-line residues form the correct 270-orbit.",
        },
        "4723_square_root_double_cover": {
            "PGSp_order": 51840,
            "outer_square_roots_per_representative_involution": 8,
            "four_fixed_line_square_roots": 2,
            "four_fixed_roots_are_inverse_pair": True,
            "triangle_orbit_PSp": 540,
            "outer_order4_orbit_PSp": 540,
            "triangle_stabilizer_order_PSp": 48,
            "root_centralizer_order_PSp": 48,
            "inner_stabilizers_equal": True,
            "two_covers_share_base": "270 four-line involution residues",
            "full_PGSp_triangle_stabilizer": 96,
            "full_PGSp_root_centralizer": 96,
            "full_extensions_equal": False,
            "full_extensions_intersection_order": 48,
            "equivariance_boundary": "Canonical as a PSp(4,3)-G-set after choosing one of the two inverse root sheets.  The full PGSp(4,3) extensions differ by the outer twist; no untwisted PGSp identification is claimed.",
        },
        "4724_residual_incidence": {
            "blocks": 270,
            "block_size": 4,
            "replication_per_line": 27,
            "skew_line_pairs": 540,
            "residues_per_skew_pair": 3,
            "residues_per_meeting_pair": 0,
            "gram_identity": "B B^T = 27 I + 3 (J-I-A_*)",
            "real_gram_spectrum": {"108": 1, "18": 24, "36": 15},
            "real_rank": 40,
            "binary_residue_span_rank": 30,
            "involution_fixed_support12_thickenings": 24,
            "involution_fixed_disjointness_triangles": 8,
        },
        "theorem": "The 1620 support-12 apartment thickenings carry a canonical 2-regular disjointness relation whose 540 K3 components and the 540 four-fixed-line outer order-four elements are isomorphic PSp(4,3)-sets. Both are two-fold covers of the 270 four-line fixed sets of the inner involution class, resolving the old unnamed-270 frontier. The 270 residues additionally factor the complement of the W33 line graph by B B^T = 27I + 3(J-I-A_*).",
        "boundary": "Exact finite geometry/group/code theorem.  The correction is to an action-domain error in Pass 1830.  Cardinalities alone are not used: fixed sets, stabilizers, centralizers, square maps, orbits, and the incidence Gram identity are all checked explicitly.  No physical interpretation is inferred.",
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
