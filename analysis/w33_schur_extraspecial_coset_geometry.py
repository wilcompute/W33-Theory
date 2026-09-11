#!/usr/bin/env python3
"""Realize the Schur (24_4,32_3) configuration as an extraspecial coset geometry.

Start from the internally reconstructed F4 root-parity group H_576 that the
companion certificates identify with both the W33 minimum-vector stabilizer and
the Schur half-stabilizer W(D4):C3.  Its characteristic second derived subgroup
is E = 2_+^{1+4}, order 32.

Exact result:
  * E acts regularly on the 32 zero-sum D4 root triples;
  * its action on the 24 roots has three orbits of size 8;
  * after choosing a base triple as identity, the unique line from each orbit
    through the base triple pulls back to a V4 subgroup V_i < E;
  * all 24 lines are exactly the left cosets of V_1,V_2,V_3;
  * V_i cap V_j = 1 for i != j;
  * modulo Z(E), their images are the three totally-singular 2-spaces in one
    ruling of Q^+(3,2), partitioning all nine nonzero singular vectors.

Thus the Schur incidence configuration is a rank-three coset geometry of the
same extraspecial-plus phase group appearing in the W33/Latin/Clifford lane.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_schur_quartic_d4_triality_bridge import (  # noqa: E402
    f4_roots, schur_incidence, restrict_perm, wd4_group,
)
from w33_threeway_576_provenance_closure import (  # noqa: E402
    compose, derived_subgroup, porder, quotient_E_coords, wf4_and_kernels,
)

OUT = ROOT / "data" / "w33_schur_extraspecial_coset_geometry.json"


def build_result():
    roots = f4_roots()
    d4, triples = schur_incidence(roots)
    ridx = {r: i for i, r in enumerate(d4)}
    tsets = tuple(frozenset(ridx[r] for r in T) for T in triples)
    tidx = {T: i for i, T in enumerate(tsets)}
    root_global = {r: i for i, r in enumerate(roots)}

    _wf4, longk, shortk, rotk, _auto = wf4_and_kernels()
    WD4 = wd4_group(roots)
    kernels = [K for K in (longk, shortk, rotk) if WD4 <= K]
    assert len(kernels) == 1
    H = kernels[0]
    H1 = derived_subgroup(H, 48)
    E = derived_subgroup(H1, 48)
    assert len(H) == 576 and len(H1) == 96 and len(E) == 32
    assert Counter(porder(g) for g in E) == {1: 1, 2: 19, 4: 12}

    def root_perm(g):
        return restrict_perm(roots, d4, g)

    def triple_perm(g):
        rp = root_perm(g)
        return tuple(tidx[frozenset(rp[i] for i in T)] for T in tsets)

    Eroot = {g: root_perm(g) for g in E}
    Etriple = {g: triple_perm(g) for g in E}
    Hroot = {g: root_perm(g) for g in H}

    # E acts faithfully and regularly on the 32 triple points.
    assert len(set(Etriple.values())) == 32
    orbit0 = {p[0] for p in Etriple.values()}
    assert len(orbit0) == 32
    point_to_elem = {}
    for g, p in Etriple.items():
        j = p[0]
        assert j not in point_to_elem
        point_to_elem[j] = g
    assert len(point_to_elem) == 32

    # Incidence subsets: line/root i corresponds to four triple points.
    line_points = tuple(
        frozenset(j for j, T in enumerate(triples) if r in T)
        for r in d4
    )
    assert {len(S) for S in line_points} == {4}

    # E has three 8-line orbits.
    unseen = set(range(24)); families = []
    while unseen:
        i = min(unseen)
        O = {p[i] for p in Eroot.values()}
        families.append(frozenset(O)); unseen -= O
    assert sorted(map(len, families)) == [8, 8, 8]
    families = tuple(sorted(families, key=lambda x: min(x)))

    # The unique line from each family through base triple 0 pulls back to V4.
    V = []
    base_lines = []
    line_elem_sets = tuple(
        frozenset(point_to_elem[j] for j in S) for S in line_points
    )
    identity = tuple(range(48))
    for F in families:
        through = [i for i in F if 0 in line_points[i]]
        assert len(through) == 1
        i = through[0]; base_lines.append(i)
        subgroup = set(line_elem_sets[i])
        assert len(subgroup) == 4 and identity in subgroup
        assert all(compose(a, b) in subgroup for a in subgroup for b in subgroup)
        assert Counter(porder(g) for g in subgroup) == {1: 1, 2: 3}
        V.append(frozenset(subgroup))
    assert all(len(V[i] & V[j]) == 1 for i in range(3) for j in range(i + 1, 3))

    # Every line in family i is exactly a left coset of V_i.
    for F, Vi in zip(families, V):
        cosets = {frozenset(compose(g, h) for h in Vi) for g in E}
        actual = {line_elem_sets[i] for i in F}
        assert len(cosets) == 8 and cosets == actual

    # Quotient E/Z(E): the three V4s become the three lines of one ruling.
    Q = quotient_E_coords(E, 48)
    def qcoord(g):
        return Q["coord"][Q["ci"][g]]
    planes = [frozenset(qcoord(g) for g in Vi) for Vi in V]
    assert all(len(P) == 4 and 0 in P for P in planes)
    assert all(all(Q["q"][x] == 0 for x in P) for P in planes)
    assert all(len(planes[i] & planes[j]) == 1 for i in range(3) for j in range(i + 1, 3))
    singular_nonzero = {x for x in range(1, 16) if Q["q"][x] == 0}
    union_nonzero = set().union(*(set(P) - {0} for P in planes))
    assert len(singular_nonzero) == 9 and union_nonzero == singular_nonzero

    # Full H action permutes the three E-families as S3; kernel/E has order 3.
    family_index = {F: i for i, F in enumerate(families)}
    fam_perms = set(); fam_kernel = []
    for g, p in Hroot.items():
        image = []
        for F in families:
            imageF = frozenset(p[i] for i in F)
            image.append(family_index[imageF])
        fp = tuple(image); fam_perms.add(fp)
        if fp == (0, 1, 2): fam_kernel.append(g)
    assert len(fam_perms) == 6
    assert len(fam_kernel) == 96
    assert len(fam_kernel) // len(E) == 3

    checks = {
        "E_is_extraspecial_plus_order32": len(E) == 32 and Counter(porder(g) for g in E) == {1: 1, 2: 19, 4: 12},
        "E_regular_on_32_triples": len(orbit0) == 32,
        "E_line_orbits_8_8_8": sorted(map(len, families)) == [8, 8, 8],
        "three_base_stabilizers_are_V4": all(Counter(porder(g) for g in Vi) == {1: 1, 2: 3} for Vi in V),
        "V4s_pairwise_intersect_trivially": all(len(V[i] & V[j]) == 1 for i in range(3) for j in range(i + 1, 3)),
        "all_24_lines_are_left_cosets": True,
        "quotient_planes_totally_singular": all(all(Q["q"][x] == 0 for x in P) for P in planes),
        "three_planes_partition_9_singular_points": union_nonzero == singular_nonzero,
        "family_action_is_S3": len(fam_perms) == 6,
        "family_kernel_over_E_is_C3_order": len(fam_kernel) // len(E) == 3,
    }

    return {
        "schema": "w33.schur-extraspecial-coset-geometry.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "point_torsor": {
            "group": "E = 2_+^{1+4}",
            "order": 32,
            "triple_points": 32,
            "action": "regular",
        },
        "line_cosets": {
            "families": [8, 8, 8],
            "base_line_indices": base_lines,
            "subgroup_types": ["V4", "V4", "V4"],
            "pairwise_intersection_orders": [len(V[0] & V[1]), len(V[0] & V[2]), len(V[1] & V[2])],
            "all_lines": "left cosets of V1,V2,V3",
        },
        "quadratic_quotient": {
            "space": "E/Z(E) ~= F2^4 with plus quadratic form",
            "V_images": [sorted(P) for P in planes],
            "singular_nonzero_count": len(singular_nonzero),
            "interpretation": "the three V_i/Z-intersection images are the three generator lines of one ruling of Q^+(3,2)",
        },
        "outer_action": {
            "family_permutation_group_order": len(fam_perms),
            "family_kernel_order": len(fam_kernel),
            "family_kernel_mod_E_order": len(fam_kernel) // len(E),
            "reading": "H/E ~= S3 x C3: the S3 triality factor permutes the three ruling families; a C3 remains in the family kernel.",
        },
        "theorem": (
            "The Schur (24_4,32_3) root configuration is exactly the rank-three coset geometry of the W33 extraspecial-plus phase kernel E: its points are the E-torsor and its lines are the 24 left cosets of three V4 subgroups whose images form one ruling of Q^+(3,2)."
        ),
        "boundary": (
            "The algebraic identification with actual Schur-quartic lines still uses the external D4-root model. The coset/torsor theorem itself is recomputed entirely from the finite root incidence and group action."
        ),
        "checks": checks,
    }


def main():
    r = build_result()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(r, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": r["status"], "points": r["point_torsor"]["triple_points"], "line_families": r["line_cosets"]["families"], "family_group": r["outer_action"]["family_permutation_group_order"]}, sort_keys=True))
    return 0 if r["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
