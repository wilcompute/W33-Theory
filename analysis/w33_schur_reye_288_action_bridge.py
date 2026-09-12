#!/usr/bin/env python3
"""Resolve the Schur-half -> Reye symmetry map at the correct order 288.

This is a corrective action-level theorem.  The Schur (24_4,32_3) half has an
order-576 stabilizer H=W(D4):C3 on the 24 signed D4 roots.  Its central
antipodal involution r->-r acts trivially after the Reye quotient, so H does
*not* become the full order-576 Reye automorphism group.  The induced action has
order 288.

We build the 12 root-pairs and 16 opposite-triple blocks, enumerate the exact
576 Schur root actions, quotient them, and then find a typed incidence
isomorphism to the repo's V4-decoder Reye model.  Under that explicit map all
288 induced Schur permutations land inside the 576-element affine decoder
Aut(Reye)=C2^4:(S3xS3), as an index-two subgroup.  The kernel upstairs is
exactly {1, antipode}.

This distinguishes two different 576 objects which had been too easy to blur:
  * Schur half stabilizer / W33 minimum stabilizer: 2_+^{1+4}:(S3xC3), center 2;
  * full typed Reye automorphism group: C2^4:(S3xS3), center trivial.
Their correct bridge is the Schur central quotient of order 288, not an
isomorphism of the two 576 groups.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
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

from w33_schur_quartic_d4_triality_bridge import (  # noqa: E402
    f4_roots, wd4_group, schur_incidence, restrict_perm,
)
from w33_threeway_576_provenance_closure import wf4_and_kernels  # noqa: E402
from w33_reye_v4_decoder_automorphism_576 import (  # noqa: E402
    POINTS, BLOCKS, R, GL, S3, block_points, point_perm,
)

OUT = ROOT / "data" / "w33_schur_reye_288_action_bridge.json"


def neg(r):
    return tuple(-x for x in r)


def pcompose(g, h):
    return tuple(g[h[i]] for i in range(len(h)))


def pinverse(g):
    out = [0] * len(g)
    for i, j in enumerate(g):
        out[j] = i
    return tuple(out)


def porder(g):
    e = tuple(range(len(g)))
    x = e
    for n in range(1, 65):
        x = pcompose(g, x)
        if x == e:
            return n
    raise AssertionError("order bound")


def generated_group(gens, n):
    e = tuple(range(n))
    pool = list(gens) + [pinverse(g) for g in gens]
    seen = {e}; stack = [e]
    while stack:
        x = stack.pop()
        for g in pool:
            y = pcompose(g, x)
            if y not in seen:
                seen.add(y); stack.append(y)
    return seen


def parity(p):
    return sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p))) & 1


def gl_nonzero_perm(M):
    nz = (1, 2, 3)
    pos = {x:i for i,x in enumerate(nz)}
    # local copy of decoder bit convention
    def bitpair(x): return (x & 1, (x >> 1) & 1)
    def frompair(v): return int(v[0]) | (int(v[1]) << 1)
    def apply(x):
        u,v = bitpair(x)
        return frompair(((M[0][0]*u+M[0][1]*v)&1, (M[1][0]*u+M[1][1]*v)&1))
    return tuple(pos[apply(x)] for x in nz)


def build_result():
    roots = f4_roots()
    WD4 = wd4_group(roots)
    d4, triples = schur_incidence(roots)
    _wf4, longk, shortk, rotk, _auto = wf4_and_kernels()
    candidates = [K for K in (longk, shortk, rotk) if WD4 <= K]
    assert len(candidates) == 1
    H = candidates[0]
    assert len(H) == 576

    # Faithful 24-root action.
    action24 = {restrict_perm(roots, d4, g) for g in H}
    assert len(action24) == 576
    di = {r:i for i,r in enumerate(d4)}

    # Twelve antipodal root pairs.
    pair_keys = tuple(sorted({min(r, neg(r)) for r in d4}))
    assert len(pair_keys) == 12
    pair_index = {p:i for i,p in enumerate(pair_keys)}
    root_to_pair = {r: pair_index[min(r, neg(r))] for r in d4}

    # Sixteen Reye blocks: an opposite zero-sum triple pair has the same three
    # antipodal root pairs, so each block is represented by that 3-subset.
    reye_blocks = tuple(sorted({frozenset(root_to_pair[r] for r in T) for T in triples}, key=lambda B: tuple(sorted(B))))
    assert len(reye_blocks) == 16 and all(len(B) == 3 for B in reye_blocks)
    block_index = {B:i for i,B in enumerate(reye_blocks)}

    # Induced Schur quotient action on the 12 root pairs and 16 blocks.
    induced12 = set()
    kernel24 = []
    for p in action24:
        q = [None] * 12
        for r in d4:
            i = root_to_pair[r]
            j = root_to_pair[d4[p[di[r]]]]
            if q[i] is None: q[i] = j
            else: assert q[i] == j
        q = tuple(q)
        induced12.add(q)
        if q == tuple(range(12)):
            kernel24.append(p)
    assert len(induced12) == 288
    assert len(kernel24) == 2

    # The nontrivial kernel element is exactly antipodal on all 24 roots.
    antipode = tuple(di[neg(r)] for r in d4)
    assert antipode in kernel24 and tuple(range(24)) in kernel24

    # Build Schur quotient typed incidence graph.
    Gs = nx.Graph()
    for i in range(12): Gs.add_node(("P",i), kind="point")
    for j,B in enumerate(reye_blocks):
        Gs.add_node(("B",j), kind="block")
        for i in B: Gs.add_edge(("P",i),("B",j))
    assert Gs.number_of_edges() == 48

    # Decoder Reye graph.
    Gd = nx.Graph()
    for p in POINTS: Gd.add_node(("P",p), kind="point")
    for B in BLOCKS:
        Gd.add_node(("B",B), kind="block")
        for p in block_points(B): Gd.add_edge(("P",p),("B",B))
    nm = iso.categorical_node_match("kind", None)
    GM = iso.GraphMatcher(Gs, Gd, node_match=nm)
    mapping = next(GM.isomorphisms_iter())

    # Point-level conjugator Schur pair index -> decoder point index.
    dpi = {p:i for i,p in enumerate(POINTS)}
    f = tuple(dpi[mapping[("P",i)][1]] for i in range(12))
    assert len(set(f)) == 12
    finv = [None]*12
    for i,j in enumerate(f): finv[j]=i

    schur_in_decoder = set()
    for q in induced12:
        out = [None]*12
        for j in range(12):
            i = finv[j]
            out[j] = f[q[i]]
        schur_in_decoder.add(tuple(out))
    assert len(schur_in_decoder) == 288

    # Full affine decoder action on its 12 points, with parameter provenance.
    decoder_actions = {}
    for a,b,M,sigma in itertools.product(R,R,GL,S3):
        labels = point_perm(a,b,M,sigma)
        perm = tuple(dpi[x] for x in labels)
        decoder_actions[perm] = (a,b,M,sigma)
    assert len(decoder_actions) == 576
    assert schur_in_decoder < set(decoder_actions)

    # Determine the index-two parity character in this explicit gauge.
    patterns = Counter()
    for perm in schur_in_decoder:
        a,b,M,sigma = decoder_actions[perm]
        patterns[(parity(gl_nonzero_perm(M)), parity(sigma))] += 1
    present = set(patterns)
    if present == {(0,0),(1,0)}:
        parity_rule = "decoder-role S3 even"
        quotient_structure = "C2^4 : (S3 x C3)"
    elif present == {(0,0),(0,1)}:
        parity_rule = "GL(2,2) S3 even"
        quotient_structure = "C2^4 : (C3 x S3)"
    elif present == {(0,0),(1,1)}:
        parity_rule = "matched parity in the two S3 factors"
        quotient_structure = "C2^4 : ((C3 x C3) : C2)"
    else:
        parity_rule = f"conjugate index-two subgroup with parity support {sorted(present)}"
        quotient_structure = "index-two subgroup of C2^4:(S3 x S3)"

    # Permutation invariants of the 288 image.
    order_hist = dict(sorted(Counter(porder(g) for g in schur_in_decoder).items()))
    center = [g for g in schur_in_decoder if all(pcompose(g,h)==pcompose(h,g) for h in schur_in_decoder)]
    comms = set()
    for g in schur_in_decoder:
        gi=pinverse(g)
        for h in schur_in_decoder:
            hi=pinverse(h)
            comms.add(pcompose(pcompose(pcompose(gi,hi),g),h))
    derived = generated_group(comms,12)

    # Distinguish the two order-576 parents using independent repo invariants.
    w33 = json.loads((ROOT / "data" / "PART_W33_20260828_MINIMUM_STABILIZER_576_STRUCTURE.json").read_text(encoding="utf-8"))
    assert w33["status"] == "PASS"
    assert w33["minimumLineStabilizer"]["order"] == 576 if "minimumLineStabilizer" in w33 else True
    decoder = json.loads((ROOT / "data" / "w33_reye_v4_decoder_automorphism_576.json").read_text(encoding="utf-8"))
    assert decoder["status"] == "PASS"
    assert decoder["orders"]["full_typed_automorphism_group"] == 576

    checks = {
        "Schur_signed_root_stabilizer_order576": len(action24) == 576,
        "antipodal_kernel_exactly_order2": len(kernel24) == 2 and antipode in kernel24,
        "Schur_induced_Reye_action_order288": len(induced12) == 288,
        "typed_Schur_quotient_is_Reye": nx.is_isomorphic(Gs,Gd,node_match=nm),
        "explicit_conjugated_Schur_action_is_subset_of_full_decoder_group": schur_in_decoder < set(decoder_actions),
        "decoder_full_group_order576": len(decoder_actions) == 576,
        "Schur_Reye_image_has_index2_in_decoder_group": len(decoder_actions)//len(schur_in_decoder) == 2,
        "two_576_groups_are_not_identified_by_Reye_quotient": len(action24) == len(decoder_actions) == 576 and len(schur_in_decoder) == 288,
    }

    return {
        "schema": "w33.schur-reye-288-action-bridge.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "orders": {
            "Schur_half_signed_root_stabilizer": 576,
            "antipodal_kernel": len(kernel24),
            "Schur_induced_Reye_group": len(schur_in_decoder),
            "full_typed_Reye_automorphism_group": len(decoder_actions),
            "index": len(decoder_actions)//len(schur_in_decoder),
        },
        "induced_288": {
            "parity_support_counts": {str(k):v for k,v in sorted(patterns.items())},
            "parity_rule_in_chosen_incidence_isomorphism": parity_rule,
            "affine_structure_reading": quotient_structure,
            "element_order_census": order_hist,
            "center_order": len(center),
            "derived_order": len(derived),
        },
        "correction": (
            "The Schur component stabilizer of order 576 is NOT the full typed Reye automorphism group of order 576. Its antipodal central involution dies in the Reye projection, leaving an order-288 image which embeds with index two in Aut(Reye). Equal order of the two parent groups was a count trap."
        ),
        "theorem": (
            "The D4-root antipodal quotient gives an exact sequence 1 -> C2 -> H_Schur(576) -> B_Reye(288) -> 1, and an explicit typed-incidence conjugator embeds B_Reye as an index-two subgroup of the affine V4 decoder Aut(Reye)=C2^4:(S3xS3)."
        ),
        "claim_boundary": (
            "Exact finite permutation/action theorem. It corrects a previous overidentification of two order-576 groups. It does not construct Nurowski's P3 projective matrices; it uses the D4 root action imported from Hohn and the exact incidence quotient."
        ),
        "checks": checks,
    }


def main():
    r=build_result(); OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":r["status"],"orders":r["orders"],"parity":r["induced_288"]["parity_rule_in_chosen_incidence_isomorphism"]},sort_keys=True))
    return 0 if r["status"]=="PASS" else 1

if __name__=="__main__":
    raise SystemExit(main())
