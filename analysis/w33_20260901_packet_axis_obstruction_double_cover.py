#!/usr/bin/env python3
"""Classify the packet/local-axis 1080 G-set against the obstruction carrier.

There are two independent transitive degree-1080 PSp(4,3) carriers:

  O = 27 completion charts x 40 W33 lines,
  A = {(P,a): P one of the 45 K4,4/D4+D4 packets and a one of the
       three local pencil-octahedron axes at one of the eight points of P},
      |A|=45*8*3=1080.

The first execution of this file falsified the naive direct identification:
the order-24 stabilizer of a packet-axis flag fixes no point of O.  This version
keeps that no-go and tests the stronger exceptional-automorphism hypothesis.
The nonsquare symplectic similitude

    s = diag(1,2,1,2)

normalizes PSp(4,3) inside PGSp(4,3) and induces the nontrivial outer
automorphism.  We twist A by g -> s g s^{-1} and test objectwise whether O is
isomorphic to that outer-twisted action.

Independently, the already-proved 2160 packet/K3,3 = BT796 D12 shell has an
order-12 flag stabilizer.  We test whether it lies in an order-24 packet-axis
stabilizer on the natural sheet, and separately after the outer twist.  Any
index-two inclusion is propagated over all 25,920 group elements and checked
to give a genuine 2-to-1 equivariant cover.

Pass123 independently identifies the 120 local W33 axes with the 120 antipodal
E8 root lines.  A positive outer-twist result therefore supplies an E8-axis
address for the OUTER-TWISTED obstruction action, not a silent inner
identification.  A further coordinate check is still required to prove that a
selected axis lies inside the corresponding packet's particular D4+D4 root
subsystem.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, deque
from pathlib import Path

import w33_20260901_packet48_bt796_crossid as shell
import w33_20260901_obstruction_wedderburn_steinberg_projectors as obs

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_20260901_PACKET_AXIS_OBSTRUCTION_DOUBLE_COVER.json"


def comp(p, q):
    return tuple(p[q[i]] for i in range(len(q)))


def paired_closure(A, B, n, m):
    I = (tuple(range(n)), tuple(range(m)))
    G = {I}
    Q = deque([I])
    while Q:
        a, b = Q.popleft()
        for ga, gb in zip(A, B):
            z = (comp(ga, a), comp(gb, b))
            if z not in G:
                G.add(z)
                Q.append(z)
    assert len(G) == 25920
    return list(G)


def matchings4(vals):
    a, b, c, d = sorted(vals)
    return (
        tuple(sorted(((a, b), (c, d)))),
        tuple(sorted(((a, c), (b, d)))),
        tuple(sorted(((a, d), (b, c)))),
    )


def norm3(v):
    i = next(k for k, x in enumerate(v) if x % 3)
    z = pow(v[i] % 3, -1, 3)
    return tuple((z * x) % 3 for x in v)


def main():
    D = shell.build()
    pts, wlines, supports = D["pts"], D["wlines"], D["supports"]
    g40, g45 = D["g40"], D["g45"]
    pidx = {v: i for i, v in enumerate(pts)}
    li = {frozenset(L): i for i, L in enumerate(wlines)}
    sidx = {frozenset(S): i for i, S in enumerate(supports)}

    point_lines = [[] for _ in range(40)]
    for ell, L in enumerate(wlines):
        for p in L:
            point_lines[p].append(ell)
    assert {len(x) for x in point_lines} == {4}

    axes = []
    for p in range(40):
        for M in matchings4(point_lines[p]):
            axes.append((p, M))
    assert len(axes) == 120 and len(set(axes)) == 120
    aidx = {a: i for i, a in enumerate(axes)}

    def line_perm(p40):
        return tuple(li[frozenset(p40[x] for x in L)] for L in wlines)

    def packet_perm(p40):
        return tuple(sidx[frozenset(p40[x] for x in S)] for S in supports)

    def axis_perm(p40):
        lp = line_perm(p40)
        out = []
        for p, M in axes:
            MM = tuple(sorted(tuple(sorted((lp[a], lp[b]))) for a, b in M))
            out.append(aidx[(p40[p], MM)])
        return tuple(out)

    flags = []
    for packet, S in enumerate(supports):
        for a, (p, _M) in enumerate(axes):
            if p in S:
                flags.append((packet, a))
    assert len(flags) == 1080 and len(set(flags)) == 1080
    fidx = {x: i for i, x in enumerate(flags)}

    def flag_perm(p40):
        pp = packet_perm(p40)
        pa = axis_perm(p40)
        return tuple(fidx[(pp[p], pa[a])] for p, a in flags)

    flag_gens = [flag_perm(p40) for p40 in g40]
    # Cross-check against the packet generators already frozen by the shell.
    assert all(packet_perm(p40) == p45 for p40, p45 in zip(g40, g45))

    src_gens, charts, lines2 = obs.build_action()
    assert lines2 == wlines

    # Natural inner comparison: this is intentionally allowed to fail.
    Ginner = paired_closure(src_gens, flag_gens, 1080, 1080)
    base_flag = 0
    assert len({gf[base_flag] for _gs, gf in Ginner}) == 1080
    H24inner = [(gs, gf) for gs, gf in Ginner if gf[base_flag] == base_flag]
    assert len(H24inner) == 24
    fixed_inner = [x for x in range(1080)
                   if all(gs[x] == x for gs, _gf in H24inner)]

    # Explicit nonsquare similitude s=diag(1,2,1,2).  Projectively s^2=1.
    sout = tuple(
        pidx[norm3((v[0], 2 * v[1], v[2], 2 * v[3]))]
        for v in pts
    )
    assert comp(sout, sout) == tuple(range(40))
    outer_g40 = [comp(sout, comp(g, sout)) for g in g40]
    # The conjugates remain in the inner group; closure order below is a check.
    outer_flag_gens = [flag_perm(g) for g in outer_g40]
    Gouter = paired_closure(src_gens, outer_flag_gens, 1080, 1080)
    H24outer = [(gs, gf) for gs, gf in Gouter if gf[base_flag] == base_flag]
    assert len(H24outer) == 24
    fixed_outer = [x for x in range(1080)
                   if all(gs[x] == x for gs, _gf in H24outer)]

    outer_bijection = None
    if fixed_outer:
        source_base = fixed_outer[0]
        phi = {}
        for gs, gf in Gouter:
            x = gf[base_flag]
            y = gs[source_base]
            if x in phi:
                assert phi[x] == y
            else:
                phi[x] = y
        assert len(phi) == 1080 and len(set(phi.values())) == 1080
        outer_bijection = [phi[i] for i in range(1080)]
        for gs, gf in zip(src_gens, outer_flag_gens):
            assert all(outer_bijection[gf[x]] == gs[outer_bijection[x]]
                       for x in range(1080))

    # Reconstruct the order-12 stabilizer of the packet/K3,3 base flag used in
    # the already-proved 2160 shell cross-identification.
    K33 = D["K33"]
    kidx = {K: i for i, K in enumerate(K33)}
    def actK(pc, K):
        return kidx[frozenset(pc[x] for x in K)]
    nbp, nbk = D["newbase"]
    H12triples = [z for z in D["G"]
                  if z[1][nbp] == nbp and actK(z[2], K33[nbk]) == nbk]
    assert len(H12triples) == 12

    def act_flag_p40(p40, flag_index):
        fp = flag_perm(p40)
        return fp[flag_index]

    fixed_by_H12_natural = [i for i in range(1080)
                            if all(act_flag_p40(z[0], i) == i
                                   for z in H12triples)]
    # Outer-twist the CHILD subgroup by conjugating its PSp elements.
    H12_outer_p40 = [comp(sout, comp(z[0], sout)) for z in H12triples]
    fixed_by_H12_outer = [i for i in range(1080)
                          if all(act_flag_p40(g, i) == i
                                 for g in H12_outer_p40)]

    nf = D["nf"]
    nfi = {x: i for i, x in enumerate(nf)}

    def cover_for_parent(parent_base, twist_child=False):
        cover = {}
        for z in D["G"]:
            p40, p45, p27 = z
            child = (p45[nbp], actK(p27, K33[nbk]))
            ci = nfi[child]
            pg = comp(sout, comp(p40, sout)) if twist_child else p40
            par = act_flag_p40(pg, parent_base)
            if ci in cover:
                if cover[ci] != par:
                    return None
            else:
                cover[ci] = par
        if len(cover) != 2160:
            return None
        fibres = Counter(cover.values())
        if len(fibres) != 1080 or set(fibres.values()) != {2}:
            return None
        same_packet = sum(nf[ci][0] == flags[par][0]
                          for ci, par in cover.items())
        return {
            "mapDefinedOn": 2160,
            "parentImageSize": 1080,
            "fibreSizeHistogram": {"2": 1080},
            "samePacketCount": same_packet,
        }

    natural_cover = (cover_for_parent(fixed_by_H12_natural[0], False)
                     if fixed_by_H12_natural else None)
    outer_cover = (cover_for_parent(fixed_by_H12_outer[0], True)
                   if fixed_by_H12_outer else None)

    out = {
        "schema": "w33.20260901.packet-axis-obstruction-outer-classification.v2",
        "status": "PASS",
        "groupOrder": 25920,
        "outerAutomorphism": {
            "similitude": "diag(1,2,1,2)",
            "projectivePermutationOrder": 2,
            "meaning": "nontrivial PGSp(4,3)/PSp(4,3) outer automorphism",
        },
        "packetAxisCarrier": {
            "degree": 1080,
            "factorization": "45 packets * 8 packet points * 3 local axes",
            "stabilizerOrder": 24,
            "pass123AxisReading": "120 local axes = 120 antipodal E8 root lines",
        },
        "innerComparisonToObstruction": {
            "fixedObstructionPointsOfPacketAxisStabilizer": fixed_inner,
            "isomorphic": bool(fixed_inner),
        },
        "outerTwistedComparisonToObstruction": {
            "fixedObstructionPointsOfTwistedPacketAxisStabilizer": fixed_outer,
            "isomorphic": bool(fixed_outer),
            "explicitEquivariantBijectionVerified": outer_bijection is not None,
            "bijection": outer_bijection,
        },
        "bt796D12Shell": {
            "degree": 2160,
            "childStabilizerOrder": 12,
            "naturalPacketAxisParentsFixed": len(fixed_by_H12_natural),
            "outerTwistedPacketAxisParentsFixed": len(fixed_by_H12_outer),
            "naturalTwoCover": natural_cover,
            "outerTwistedTwoCover": outer_cover,
        },
        "theorem": (
            "The natural packet/local-axis degree-1080 PSp action is NOT silently "
            "identified with the chartxline obstruction action unless the inner fixed "
            "set above is nonempty.  Conjugation by the explicit nonsquare similitude "
            "tests the unique outer sheet objectwise; a nonempty outer fixed set plus "
            "the verified bijection proves that the two degree-1080 actions differ by "
            "the nontrivial outer automorphism.  The recorded D12-shell cover fields "
            "independently decide on which sheet, if either, the 2160 carrier admits an "
            "index-two packet-axis quotient."
        ),
        "e8Boundary": (
            "Pass123 makes the local-axis coordinate an intrinsic E8 antipodal-axis "
            "label.  Even if the outer-twist isomorphism passes, a separate common-root "
            "coordinate computation is required before saying that the axis lies inside "
            "the packet's selected D4+D4 subsystem."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": "PASS",
        "innerFixed": len(fixed_inner),
        "outerFixed": len(fixed_outer),
        "outerIso": outer_bijection is not None,
        "naturalH12Parents": len(fixed_by_H12_natural),
        "outerH12Parents": len(fixed_by_H12_outer),
        "naturalCover": natural_cover is not None,
        "outerCover": outer_cover is not None,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
