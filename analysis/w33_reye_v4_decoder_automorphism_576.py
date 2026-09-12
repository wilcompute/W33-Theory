#!/usr/bin/env python3
"""Resolve the 576-symmetry of the D4/Reye sector as an affine V4 decoder group.

The hidden-radical decoder identifies the Reye point set with three copies of
R=F2^2 and the 16 blocks with R^2:

    A_r, B_s, C_t,       t=r+s,
    T(r,s)={A_r,B_s,C_{r+s}}.

This certificate exhibits all 576 typed incidence automorphisms explicitly as

    (R x R) semidirect ( GL(2,2) x S3 ).

The normal R^2 translates the two independent hidden radical offsets; GL(2,2)
acts simultaneously on every radical coordinate; S3 permutes the three point
roles A,B,C.  Since |R^2|=16, |GL(2,2)|=6 and |S3|=6, the group has order 576.
An independent colored-Levi-graph enumeration also gives exactly 576, so the
constructed affine decoder group is the full typed automorphism group.  This
supplies an explicit structural model for the repo's prior identification
Aut(Reye)=W(F4)/{+-I}.
"""
from __future__ import annotations

from itertools import combinations, permutations, product
import json
from pathlib import Path
import sys

import networkx as nx
from networkx.algorithms import isomorphism as iso

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_reye_hidden_radical_v4_decoder import build_result as build_decoder  # noqa: E402

OUT = ROOT / "data" / "w33_reye_v4_decoder_automorphism_576.json"

ROLES = (0, 1, 2)  # A,B,C
R = tuple(range(4))  # two-bit radical indices; group law is xor
POINTS = tuple((role, r) for role in ROLES for r in R)
BLOCKS = tuple((r, s) for r in R for s in R)


def block_points(block):
    r, s = block
    return frozenset(((0, r), (1, s), (2, r ^ s)))


def bitpair(x):
    return (x & 1, (x >> 1) & 1)


def from_bitpair(v):
    return int(v[0]) | (int(v[1]) << 1)


def mat_apply(M, x):
    u, v = bitpair(x)
    return from_bitpair(((M[0][0]*u + M[0][1]*v) & 1,
                         (M[1][0]*u + M[1][1]*v) & 1))


def gl22():
    mats = []
    for a,b,c,d in product((0,1), repeat=4):
        if ((a*d) ^ (b*c)) == 1:
            M = ((a,b),(c,d))
            image = tuple(mat_apply(M, x) for x in R)
            assert len(set(image)) == 4
            mats.append(M)
    assert len(mats) == 6
    return tuple(mats)


GL = gl22()
S3 = tuple(permutations(ROLES))


def translate_point(p, a, b):
    role, x = p
    shifts = (a, b, a ^ b)
    return role, x ^ shifts[role]


def linear_point(p, M):
    role, x = p
    return role, mat_apply(M, x)


def role_point(p, sigma):
    role, x = p
    return sigma[role], x


def compose_action(p, a, b, M, sigma):
    # translation, then linear relabelling, then role permutation
    return role_point(linear_point(translate_point(p, a, b), M), sigma)


def point_perm(a, b, M, sigma):
    image = tuple(compose_action(p, a, b, M, sigma) for p in POINTS)
    assert len(set(image)) == len(POINTS)
    return image


def image_block(B, perm_map):
    return frozenset(perm_map[p] for p in block_points(B))


def build_levi():
    G = nx.Graph()
    for p in POINTS:
        G.add_node(("P", p), kind="point")
    for B in BLOCKS:
        G.add_node(("B", B), kind="block")
        for p in block_points(B):
            G.add_edge(("P", p), ("B", B))
    return G


def build_result():
    decoder = build_decoder()
    assert decoder["status"] == "PASS"

    canonical_blocks = {block_points(B) for B in BLOCKS}
    assert len(canonical_blocks) == 16

    # Explicit affine decoder automorphisms.
    actions = {}
    for a, b, M, sigma in product(R, R, GL, S3):
        P = point_perm(a, b, M, sigma)
        pmap = dict(zip(POINTS, P))
        images = {image_block(B, pmap) for B in BLOCKS}
        assert images == canonical_blocks
        actions[P] = (a, b, M, sigma)
    assert len(actions) == 16 * 6 * 6 == 576

    # Translation subgroup N ~= R^2, acting regularly on the 16 blocks.
    I = ((1,0),(0,1))
    ident_sigma = (0,1,2)
    translations = {point_perm(a,b,I,ident_sigma) for a,b in BLOCKS}
    assert len(translations) == 16
    base_block = block_points((0,0))
    translated_base = set()
    for a,b in BLOCKS:
        pmap = dict(zip(POINTS, point_perm(a,b,I,ident_sigma)))
        translated_base.add(image_block((0,0), pmap))
    assert translated_base == canonical_blocks

    # Complement H = GL(2,2) x S3.  The two factors commute and intersect trivially.
    linear = {point_perm(0,0,M,ident_sigma) for M in GL}
    role = {point_perm(0,0,I,sigma) for sigma in S3}
    complement = {point_perm(0,0,M,sigma) for M,sigma in product(GL,S3)}
    assert len(linear) == 6 and len(role) == 6 and len(complement) == 36
    assert linear & role == {point_perm(0,0,I,ident_sigma)}

    # Verify commuting factors pointwise.
    for M, sigma, p in product(GL, S3, POINTS):
        left = role_point(linear_point(p, M), sigma)
        right = linear_point(role_point(p, sigma), M)
        assert left == right

    # N is normal under both complement factors: conjugation sends the shift
    # triple (a,b,a+b) to another shift triple of the same form.
    shift_triples = {(a,b,a^b) for a,b in BLOCKS}
    for a,b,M,sigma in product(R,R,GL,S3):
        shifts = (a,b,a^b)
        # linear relabelling
        gshifts = tuple(mat_apply(M,x) for x in shifts)
        assert gshifts[2] == (gshifts[0] ^ gshifts[1])
        # role permutation
        permuted = [None,None,None]
        for old_role in ROLES:
            permuted[sigma[old_role]] = shifts[old_role]
        pshifts = tuple(permuted)
        assert pshifts in shift_triples

    # Independent typed Levi-graph automorphism enumeration.
    G = build_levi()
    nm = iso.categorical_node_match("kind", None)
    full_aut = sum(1 for _ in iso.GraphMatcher(G, G, node_match=nm).isomorphisms_iter())
    assert full_aut == 576

    # Structural quotient data.
    assert len(actions) // len(translations) == 36
    assert len(actions) == len(translations) * len(complement)

    checks = {
        "explicit_affine_actions_are_576": len(actions) == 576,
        "every_explicit_action_preserves_Reye_incidence": True,
        "translation_subgroup_is_R2_order16": len(translations) == 16,
        "translations_are_regular_on_16_blocks": translated_base == canonical_blocks,
        "GL22_factor_has_order6": len(linear) == 6,
        "role_S3_factor_has_order6": len(role) == 6,
        "complement_is_GL22_times_S3_order36": len(complement) == 36,
        "GL22_and_role_S3_commute": True,
        "translation_shift_family_is_normal_under_complement": True,
        "independent_typed_Levi_automorphism_count_is_576": full_aut == 576,
        "explicit_group_exhausts_full_typed_automorphism_group": len(actions) == full_aut,
    }

    return {
        "schema": "w33.reye-v4-decoder-automorphism-576.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "orders": {
            "R": 4,
            "R_x_R_translation_kernel": len(translations),
            "GL_2_2": len(linear),
            "role_S3": len(role),
            "complement": len(complement),
            "full_typed_automorphism_group": full_aut,
        },
        "structure": {
            "normal_kernel": "R^2 ~= C2^4",
            "complement": "GL(2,2) x S3 ~= S3 x S3",
            "semidirect_product": "C2^4 : (S3 x S3)",
            "order_factorization": "576 = 16 * 6 * 6",
            "translation_action": "(a,b): (A_r,B_s,C_t) -> (A_{r+a},B_{s+b},C_{t+a+b})",
            "linear_action": "g in GL(2,2) acts simultaneously on r,s,t",
            "role_action": "sigma in S3 permutes A,B,C; r+s+t=0 is symmetric",
        },
        "identification": {
            "repo_prior": "full colored Reye automorphism group = W(F4)/{+-I}, order 576",
            "new_explicit_model": "W(F4)/{+-I} ~= C2^4 : (S3 x S3) in the hidden-radical decoder coordinates",
            "literature_alignment": "Nurowski arXiv:2609.10751 gives projective stabilizer order 576 for either Schur 24-line component; this certificate supplies the internal affine V4 decoder model of the same Reye/D4 symmetry order.",
        },
        "theorem": (
            "The full typed automorphism group of the E8-selected D4/Reye incidence geometry is exactly the affine autotopism group of its hidden V4 radical decoder: (R x R) semidirect (GL(2,2) x S3), of order 16*6*6=576. The normal C2^4 acts regularly on the 16 Reye blocks."
        ),
        "claim_boundary": (
            "Exact finite incidence/group theorem. Equality of the order-576 projective Schur-component stabilizer with this abstract Reye automorphism model is structurally aligned with the cited paper, but this certificate does not construct Nurowski's projective matrices objectwise."
        ),
        "checks": checks,
    }


def main():
    r = build_result()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(r, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": r["status"],
        "group": r["structure"]["semidirect_product"],
        "order": r["orders"]["full_typed_automorphism_group"],
        "kernel": r["orders"]["R_x_R_translation_kernel"],
        "complement": r["orders"]["complement"],
    }, sort_keys=True))
    return 0 if r["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
