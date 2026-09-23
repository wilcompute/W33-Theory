#!/usr/bin/env python3
"""Maximal symmetry that an address->operator compiler can preserve.

For K = H27_address x C3_external, the regular address module and the landed
operator matter81 module have equal restricted characters on L <= K exactly
when L intersects D=[K,K]=Z(H27)x{0} trivially.

This script exhausts the subgroup geometry and proves:
  * maximal compiler-safe subgroups have order 9;
  * exactly 36 such C3^2 subgroups exist;
  * they split 12+12+12 under the fixed-center 216-element Heisenberg
    automorphism group;
  * in the fixed physical lift gauge, their H27 intersections are dual to the
    12 affine Hesse lines of AG(2,3);
  * incidence between the 36 maximal safe planes and the 36 noncentral C3
    subgroups is four disjoint Pappus configurations.

Scope: finite representation/control theorem only. It does not identify these
36 planes with the classical 36 GQ(2,2) hyperplanes/double-sixes.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_maximal_compiler_symmetry_pappus.json"
F = range(3)
H = tuple(itertools.product(F, repeat=3))
ID = (0, 0, 0)
ZC = (0, 0, 1)
ZGEN = (1, 0, 0)
XGEN = (0, 1, 0)
KID = (ID, 0)

SELECTED_LIFT_PHASE = {
    (0, 1): 1,  # omega X
    (1, 0): 1,  # omega Z
    (1, 1): 0,  # Z X
    (1, 2): 2,  # omega^2 Z X^2
}
DIRECTIONS = tuple(sorted(SELECTED_LIFT_PHASE))


def hmul(g, h):
    a, b, c = g
    A, B, C = h
    return ((a + A) % 3, (b + B) % 3, (c + C - b * A) % 3)


def hinv(g):
    for h in H:
        if hmul(g, h) == ID and hmul(h, g) == ID:
            return h
    raise AssertionError(g)


def hpow(g, n):
    r = ID
    for _ in range(n):
        r = hmul(r, g)
    return r


def hcomm(g, h):
    return hmul(hmul(hmul(g, h), hinv(g)), hinv(h))


K = tuple((g, p) for g in H for p in F)


def kmul(x, y):
    return (hmul(x[0], y[0]), (x[1] + y[1]) % 3)


def kpow(x, n):
    r = KID
    for _ in range(n):
        r = kmul(r, x)
    return r


def subgroup_generated(gens):
    gens = tuple(gens)
    S = {KID}
    frontier = [KID]
    while frontier:
        a = frontier.pop()
        for b in gens + tuple(S):
            for c in (kmul(a, b), kmul(b, a)):
                if c not in S:
                    S.add(c)
                    frontier.append(c)
    return frozenset(S)


D = frozenset(((0, 0, c), 0) for c in F)
ZK = frozenset(((0, 0, c), p) for c in F for p in F)
HSLICE = frozenset((g, 0) for g in H)


def operator_character(x):
    (a, b, c), p = x
    if a == 0 and b == 0 and p == 0:
        return (81, c % 3)
    return (0, 0)


def regular_character(x):
    return (81, 0) if x == KID else (0, 0)


def normalized_direction(a, b):
    if a:
        inv = 1 if a == 1 else 2
    else:
        inv = 1 if b == 1 else 2
    return ((a * inv) % 3, (b * inv) % 3)


def canonical_h_cyclic_label(C):
    for a, b, c in C:
        if (a, b, c) == ID or (a, b) == (0, 0):
            continue
        d = normalized_direction(a, b)
        if (a, b) == d:
            return d, c
    raise AssertionError(C)


def center_beta(R):
    hit = [x for x in R if x[1] == 1]
    assert len(hit) == 1
    return hit[0][0][2]


def symp(d, v):
    return (d[0] * v[1] - d[1] * v[0]) % 3


V = tuple(itertools.product(F, repeat=2))


def hesse_line(d, c):
    level = (c - SELECTED_LIFT_PHASE[d]) % 3
    return frozenset(v for v in V if symp(d, v) == level)


def gen_h(u, v):
    S = {ID}
    frontier = [ID]
    while frontier:
        a = frontier.pop()
        for b in (u, v):
            for c in (hmul(a, b), hmul(b, a)):
                if c not in S:
                    S.add(c)
                    frontier.append(c)
    return S


def phi(uv, g):
    u, v = uv
    a, b, c = g
    r = ID
    for base, n in ((u, a), (v, b), (ZC, c)):
        r = hmul(r, hpow(base, n))
    return r


def action_on_subgroup(uv, S):
    return frozenset((phi(uv, g), p) for g, p in S)


def direction_of_noncentral_k_c3(C):
    dirs = {
        normalized_direction(a, b)
        for (a, b, _c), _p in C
        if (a, b) != (0, 0)
    }
    assert len(dirs) == 1
    return next(iter(dirs))


def main(write=True):
    assert len(H) == 27 and len(K) == 81
    assert hcomm(ZGEN, XGEN) == ZC
    assert len(D) == 3 and len(ZK) == 9

    c3subs = {
        frozenset((KID, x, kpow(x, 2)))
        for x in K
        if x != KID
    }
    assert len(c3subs) == 40
    safe_c3 = [S for S in c3subs if S & D == {KID}]
    assert len(safe_c3) == 39

    order9 = set()
    for x in K:
        for y in K:
            S = subgroup_generated((x, y))
            if len(S) == 9:
                order9.add(S)
    safe9 = [S for S in order9 if S & D == {KID}]
    unsafe9 = [S for S in order9 if D <= S]
    assert (len(order9), len(safe9), len(unsafe9)) == (49, 36, 13)

    functionals = []
    for u in itertools.product(F, repeat=3):
        if u == (0, 0, 0):
            continue
        first = next(i for i, x in enumerate(u) if x)
        inv = 1 if u[first] == 1 else 2
        n = tuple((inv * x) % 3 for x in u)
        if n not in functionals:
            functionals.append(n)
    assert len(functionals) == 13

    def abelianized(x):
        (a, b, _c), p = x
        return (a, b, p)

    order27 = []
    for f in functionals:
        S = frozenset(
            x
            for x in K
            if sum(fi * xi for fi, xi in zip(f, abelianized(x))) % 3 == 0
        )
        order27.append(S)
    assert len(set(order27)) == 13
    assert all(len(S) == 27 and D <= S for S in order27)

    assert all(
        all(operator_character(x) == regular_character(x) for x in L)
        for L in safe9
    )
    assert all(
        any(operator_character(x) != regular_character(x) for x in L)
        for L in unsafe9
    )

    plane_label = {}
    for L in safe9:
        CH = frozenset(g for g, p in (L & HSLICE))
        assert len(CH) == 3
        d, c = canonical_h_cyclic_label(CH)
        R = L & ZK
        assert len(R) == 3 and R != D
        beta = center_beta(R)
        plane_label[L] = (d, c, beta)
    assert len(set(plane_label.values())) == 36
    assert Counter(beta for _d, _c, beta in plane_label.values()) == {
        0: 12,
        1: 12,
        2: 12,
    }

    hesse_lines = {hesse_line(d, c) for d, c, _beta in plane_label.values()}
    all_hesse_lines = {
        frozenset(v for v in V if symp(d, v) == level)
        for d in DIRECTIONS
        for level in F
    }
    assert hesse_lines == all_hesse_lines and len(hesse_lines) == 12

    profile = Counter()
    safe9_list = list(safe9)
    for i, A in enumerate(safe9_list):
        da, ca, ba = plane_label[A]
        LA = hesse_line(da, ca)
        for B in safe9_list[i + 1 :]:
            db, cb, bb = plane_label[B]
            LB = hesse_line(db, cb)
            parallel = LA == LB or len(LA & LB) == 0
            profile[(ba == bb, parallel, len(A & B))] += 1
            if ba == bb:
                assert len(A & B) == 3
            else:
                assert (len(A & B) == 3) == parallel
    assert profile == Counter(
        {
            (False, False, 1): 324,
            (True, False, 3): 162,
            (False, True, 3): 108,
            (True, True, 3): 36,
        }
    )

    aut_pairs = [
        (u, v)
        for u in H
        for v in H
        if hcomm(u, v) == ZC and len(gen_h(u, v)) == 27
    ]
    assert len(aut_pairs) == 216
    assert all(
        phi(uv, hmul(g, h)) == hmul(phi(uv, g), phi(uv, h))
        for uv in aut_pairs
        for g in H
        for h in H
    )

    safe9_set = set(safe9)
    unseen = set(safe9)
    orbits = []
    while unseen:
        seed = next(iter(unseen))
        orb = {action_on_subgroup(uv, seed) for uv in aut_pairs}
        assert orb <= safe9_set
        orbits.append(orb)
        unseen -= orb
    assert sorted(map(len, orbits)) == [12, 12, 12]

    noncentral_c3 = [S for S in c3subs if not S <= ZK]
    assert len(noncentral_c3) == 36
    G = nx.Graph()
    for i, C in enumerate(noncentral_c3):
        G.add_node(("P", i), side=0, direction=direction_of_noncentral_k_c3(C))
    for j, L in enumerate(safe9):
        G.add_node(("L", j), side=1, direction=plane_label[L][0])
    for i, C in enumerate(noncentral_c3):
        for j, L in enumerate(safe9):
            if C <= L:
                G.add_edge(("P", i), ("L", j))
    assert G.number_of_nodes() == 72 and G.number_of_edges() == 108
    assert Counter(dict(G.degree()).values()) == {3: 72}
    components = list(nx.connected_components(G))
    assert sorted(map(len, components)) == [18, 18, 18, 18]
    pappus = nx.pappus_graph()
    assert all(nx.is_isomorphic(G.subgraph(component), pappus) for component in components)
    assert {
        frozenset(G.nodes[n]["direction"] for n in component)
        for component in components
    } == {frozenset((d,)) for d in DIRECTIONS}

    overlap = nx.Graph()
    overlap.add_nodes_from(range(36))
    for i, A in enumerate(safe9_list):
        for j in range(i + 1, 36):
            if len(A & safe9_list[j]) == 3:
                overlap.add_edge(i, j)
    assert Counter(dict(overlap.degree()).values()) == {17: 36}

    out = {
        "schema": "w33.maximal_compiler_symmetry_pappus.v1",
        "status": "PASS_MAXIMAL_COMPILER_SYMMETRY_IS_36_ORDER9_PLANES_WITH_FOUR_PAPPUS_COMPONENTS",
        "headline": (
            "The full K=H27_address x C3 scheduler cannot act equivariantly on the "
            "landed operator carrier, but the maximal symmetry that can survive an "
            "invertible compiler is exact: order 9. There are exactly 36 maximal "
            "compiler-safe C3^2 planes. In the fixed Clifford gauge they are three "
            "sheets over the 12 affine Hesse lines, and their incidence with the 36 "
            "noncentral C3 subgroups is four disjoint Pappus configurations."
        ),
        "group": {
            "K_order": 81,
            "K_structure": "H27 x C3_external",
            "derived_subgroup_order": 3,
            "derived_subgroup": "Z(H27) x {0}",
            "center_order": 9,
            "abelianization": "F3^3",
        },
        "restriction_criterion": {
            "statement": (
                "address and operator 81-dimensional characters restrict identically "
                "to L iff L intersects [K,K] trivially"
            ),
            "operator_character_support": "only [K,K]; values 81*omega^c",
            "regular_character_support": "identity only",
            "maximal_safe_subgroup_order": 9,
        },
        "subgroup_census": {
            "order3_total": 40,
            "order3_safe": 39,
            "order3_unsafe": 1,
            "order9_total": 49,
            "order9_safe": 36,
            "order9_containing_derived": 13,
            "order27_maximal_total": 13,
            "order27_safe": 0,
        },
        "safe_plane_geometry": {
            "count": 36,
            "structure": "C3^2",
            "label_factorization": (
                "4 projective H27 directions x 3 central lift phases x "
                "3 complementary center slopes"
            ),
            "center_sheet_sizes": [12, 12, 12],
            "fixed_center_automorphism_group_order": 216,
            "fixed_center_automorphism_orbit_sizes": [12, 12, 12],
            "compiler_plane_order3_intersection_graph_degree": 17,
            "pair_profile": {
                "different_sheet_meeting_hesse_lines_intersection1": 324,
                "same_sheet_meeting_hesse_lines_intersection3": 162,
                "different_sheet_parallel_hesse_lines_intersection3": 108,
                "same_sheet_parallel_hesse_lines_intersection3": 36,
            },
        },
        "hesse_duality": {
            "affine_plane": "AG(2,3)",
            "hesse_line_count": 12,
            "parallel_classes": 4,
            "lines_per_parallel_class": 3,
            "selected_lift_phase_by_direction": {
                str(k): v for k, v in sorted(SELECTED_LIFT_PHASE.items())
            },
            "line_formula": "<d,v>_symp = c - c0(d)",
            "all_12_lines_recovered": True,
            "interpretation": (
                "the 12 noncentral H27 cyclic lifts are symplectic-dual to the "
                "12 affine Hesse lines in the fixed physical lift gauge"
            ),
        },
        "pappus_controller": {
            "noncentral_C3_points": 36,
            "maximal_safe_planes": 36,
            "incidence_edges": 108,
            "point_degree": 3,
            "plane_degree": 3,
            "connected_components": 4,
            "component_sizes": [18, 18, 18, 18],
            "all_components_isomorphic_to_Pappus_graph": True,
            "coordinate_law": (
                "for a fixed H27 direction, noncentral C3 labels (c,p) lie on "
                "safe-plane blocks c=alpha+beta*p; this is AG(2,3) with one "
                "parallel class removed"
            ),
        },
        "ownership_and_firewalls": {
            "prior_repo_pappus": (
                "scripts/w33_witting_packet_foliation_incidence_audit.py already owns "
                "a different Pappus occurrence from pairwise affine-foliation leaf incidence"
            ),
            "prior_repo_hesse36": (
                "docs/PAYNE_HESSE_PACKET_DICTIONARY.md already owns the ordinary 36 "
                "as 12 x 3 phase-decorated Hesse-line lifts"
            ),
            "classical_doily36": (
                "GQ(2,4) has 36 GQ(2,2) hyperplanes in published prior art; "
                "no identification is made"
            ),
            "double_six_firewall": (
                "the natural compiler-plane order-3-intersection graph is 17-regular, "
                "not the repo's E6/double-six SRG(36,20,10,12), so the repeated "
                "count 36 is not an incidence identification"
            ),
        },
        "consequence": (
            "The missing address-to-operator compiler should be searched as a "
            "symmetry-changing transform whose largest exact common control group is "
            "C3^2. The 36 maximal choices are organized by a three-sheet Hesse/Pappus "
            "controller rather than by the full H27 x C3 scheduler."
        ),
        "boundary": (
            "Exact finite group/character/incidence theorem. It does not select one "
            "of the 36 safe planes physically, identify them with GQ(2,2) hyperplanes, "
            "or prove a Standard Model vacuum, continuum limit, or hardware realization."
        ),
        "checks": {
            "character_restriction_iff_derived_avoided_on_maximal_candidates": True,
            "maximal_safe_order_is_9": True,
            "exactly_36_maximal_safe_planes": True,
            "three_12_orbits_under_fixed_center_216": True,
            "twelve_hesse_lines_recovered": True,
            "safe_plane_intersection_law_checked_all_630_pairs": True,
            "four_pappus_components": True,
            "doily_double_six_count_collision_firewalled": True,
        },
    }
    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n")
    return out


if __name__ == "__main__":
    print(json.dumps(main(True), indent=2))
