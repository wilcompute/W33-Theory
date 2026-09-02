#!/usr/bin/env python3
"""Exact packet/local-axis realization of the 1080 obstruction G-set.

Two independently available carriers have degree 1080:

  O = 27 completion charts x 40 W33 lines (the obstruction carrier),
  A = {(P,a): P one of the 45 K4,4/D4+D4 packets and a one of the
       three local pencil-octahedron axes at one of the eight W33 points of P}.

The second count is 45*8*3 = 1080.  This script does not identify them by
cardinality.  It builds both under the same four deterministic PSp(4,3)
generators, computes the exact stabilizer of one packet-axis flag, finds an
obstruction point fixed by that same subgroup, and propagates the base match
under all 25,920 group elements.

It then places the already-proved 2160 packet/K3,3 = BT796 D12 shell over the
packet-axis carrier.  If its order-12 flag stabilizer fixes a packet-axis flag,
then the latter has stabilizer order 24 and the subgroup inclusion gives the
canonical transitive G-map G/H12 -> G/H24.  The script verifies the propagated
map is 2-to-1 on every fibre.  Since H12 has index two in H24 it is normal in
H24 and H24/H12=C2 is the deck group of this finite G-set cover.

Boundary: Pass123 identifies the 120 local W33 axes with the 120 antipodal E8
root lines, while the 45 packets independently have a D4+D4 E8 reading.  The
finite G-set theorem below therefore gives packet + intrinsic-E8-axis labels,
but it does NOT assert without a separate coordinate check that the selected
axis is literally one of the 24 root axes internal to that packet's particular
D4+D4 coordinate subsystem.
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


def main():
    D = shell.build()
    pts, wlines, supports = D["pts"], D["wlines"], D["supports"]
    g40, g45 = D["g40"], D["g45"]
    li = {frozenset(L): i for i, L in enumerate(wlines)}

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
    assert len(flags) == 45 * 8 * 3 == 1080 and len(set(flags)) == 1080
    fidx = {x: i for i, x in enumerate(flags)}

    flag_gens = []
    for p40, p45 in zip(g40, g45):
        pa = axis_perm(p40)
        flag_gens.append(tuple(fidx[(p45[p], pa[a])] for p, a in flags))

    src_gens, charts, lines2 = obs.build_action()
    assert lines2 == wlines
    Gpair = paired_closure(src_gens, flag_gens, 1080, 1080)

    base_flag = 0
    flag_orbit = {gf[base_flag] for _gs, gf in Gpair}
    assert len(flag_orbit) == 1080
    H24pair = [(gs, gf) for gs, gf in Gpair if gf[base_flag] == base_flag]
    assert len(H24pair) == 24

    fixed_source = [x for x in range(1080) if all(gs[x] == x for gs, _gf in H24pair)]
    assert fixed_source
    source_base = fixed_source[0]
    Hsrc = [(gs, gf) for gs, gf in Gpair if gs[source_base] == source_base]
    assert len(Hsrc) == 24
    assert {gf for _gs, gf in Hsrc} == {gf for _gs, gf in H24pair}

    equiv = {}
    for gs, gf in Gpair:
        x = gf[base_flag]
        y = gs[source_base]
        if x in equiv:
            assert equiv[x] == y
        else:
            equiv[x] = y
    assert len(equiv) == 1080 and len(set(equiv.values())) == 1080

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

    # Evaluate those same p40 elements on packet-axis flags.
    def act_flag_triple(z, flag_index):
        p40, p45, _p27 = z
        pa = axis_perm(p40)
        p, a = flags[flag_index]
        return fidx[(p45[p], pa[a])]

    fixed_by_H12 = [i for i in range(1080)
                    if all(act_flag_triple(z, i) == i for z in H12triples)]
    assert fixed_by_H12
    parent_base = fixed_by_H12[0]
    H24triples = [z for z in D["G"] if act_flag_triple(z, parent_base) == parent_base]
    assert len(H24triples) == 24
    H12p40 = {z[0] for z in H12triples}
    H24p40 = {z[0] for z in H24triples}
    assert H12p40 <= H24p40 and len(H24p40 - H12p40) == 12

    # Propagate G/H12 -> G/H24 and prove all 1080 fibres have size two.
    nf = D["nf"]
    nfi = {x: i for i, x in enumerate(nf)}
    cover = {}
    for z in D["G"]:
        p40, p45, p27 = z
        child = (p45[nbp], actK(p27, K33[nbk]))
        ci = nfi[child]
        par = act_flag_triple(z, parent_base)
        if ci in cover:
            assert cover[ci] == par
        else:
            cover[ci] = par
    assert len(cover) == 2160
    fibres = Counter(cover.values())
    assert len(fibres) == 1080 and set(fibres.values()) == {2}

    # The parent packet coordinate is an exact invariant of this selected
    # cover only if the subgroup-selected parent has the same packet as child.
    same_packet = 0
    for ci, par in cover.items():
        child_packet = nf[ci][0]
        parent_packet = flags[par][0]
        same_packet += (child_packet == parent_packet)

    out = {
        "schema": "w33.20260901.packet-axis-obstruction-double-cover.v1",
        "status": "PASS",
        "groupOrder": 25920,
        "packetAxisCarrier": {
            "packets": 45,
            "pointsPerPacket": 8,
            "localAxesPerPoint": 3,
            "degree": 1080,
            "transitive": True,
            "stabilizerOrder": 24,
        },
        "obstructionCarrier": {
            "degree": 1080,
            "stabilizerOrder": 24,
            "fixedPointsOfPacketAxisBaseStabilizer": fixed_source,
            "explicitEquivariantBijectionVerified": True,
        },
        "bt796Packet48Cover": {
            "degree": 2160,
            "childStabilizerOrder": 12,
            "packetAxisParentsFixedByChildStabilizer": len(fixed_by_H12),
            "parentStabilizerOrder": 24,
            "H12ContainedInH24": True,
            "index": 2,
            "quotient": "C2",
            "propagatedMapDefinedOn": 2160,
            "parentImageSize": 1080,
            "fibreSizeHistogram": {"2": 1080},
            "childParentSamePacketCount": same_packet,
        },
        "theorem": (
            "The transitive 1080-object packet/local-axis carrier is isomorphic as a "
            "PSp(4,3)-set to the 27x40 obstruction carrier.  Moreover the already "
            "identified 2160 packet/K3,3 = BT796 D12 shell admits an explicit "
            "PSp-equivariant two-to-one map onto this carrier: its order-12 base "
            "stabilizer is contained with index two in the order-24 packet-axis "
            "stabilizer.  Hence H12 is normal in H24 and H24/H12 is C2, giving the "
            "finite cover its deck involution."
        ),
        "e8Boundary": (
            "Pass123 independently identifies each of the 120 local W33 axes with an "
            "antipodal E8 root line.  The present theorem therefore equips each "
            "obstruction coordinate with packet plus intrinsic-E8-axis data.  It does "
            "not yet prove that this axis belongs to the packet's particular D4+D4 "
            "root subsystem in a common signed-root coordinate gauge."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": "PASS",
        "fixedSource": len(fixed_source),
        "H12FixedParents": len(fixed_by_H12),
        "coverFibres": dict(Counter(fibres.values())),
        "samePacket": same_packet,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
