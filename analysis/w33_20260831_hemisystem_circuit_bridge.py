#!/usr/bin/env python3
"""Exact bridge from W(3,3) two-ovoids to the 216 sentinel five-circuits.

Holotrade independently certifies that W(3,3) has exactly 432 m-ovoids of
point-set size 20 (geometrically: 2-ovoids), and no other proper m-ovoid size.
This script starts from one Holotrade witness and uses the native PSp(4,3)
action already used by the sentinel-shell certificates.

Targets tested, not assumed:
  * the orbit of the witness has size 432;
  * its set stabilizer has order 60 and A5 element-order distribution;
  * complementation identifies the 432 two-ovoids in 216 unordered pairs;
  * a complement-pair stabilizer has order 120 and S5 element-order profile;
  * that stabilizer fixes a unique sentinel five-circuit;
  * transporting this fixed circuit through PSp(4,3) gives a well-defined
    equivariant bijection between the 216 complement pairs and 216 circuits.

If all assertions pass, the previously separate G-sets are the same
PSp(4,3)/S5 homogeneous space.  No Clifford identification is asserted.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, deque
from pathlib import Path

import w33_20260829_216_clifford_torsor_nogo as base

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_20260831_HEMISYSTEM_CIRCUIT_BRIDGE.json"

# Holotrade/data/w33_shape_catalogue.json m=20 witness.
T0 = frozenset([0,1,2,3,5,7,8,9,15,16,17,20,24,26,27,28,33,34,36,39])
ALL40 = frozenset(range(40))


def canon_pair(T):
    C = ALL40 - T
    a, b = tuple(sorted(T)), tuple(sorted(C))
    return (a, b) if a < b else (b, a)


def orbit_partition_on_points(H, n, action):
    rem = set(range(n)); out = []
    while rem:
        s = min(rem)
        O = {action(g, s) for g in H}
        out.append(sorted(O)); rem -= O
    return sorted(out, key=lambda x: (len(x), x))


def main():
    pts, idx, lines, N = base.geometry()
    supports, masks = base.supports_from_N(N)

    # Verify the Holotrade witness directly in native W33 coordinates.
    nbr = [set() for _ in range(40)]
    for L in lines:
        for a in L:
            nbr[a].update(x for x in L if x != a)
    assert {len(nbr[x]) for x in range(40)} == {12}
    assert {len(nbr[x] & T0) for x in T0} == {4}
    assert {len(nbr[x] & T0) for x in ALL40 - T0} == {8}

    # Native PSp(4,3) generators on 40 points and 45 sentinel minima.
    gens40 = []
    for v in pts:
        for alpha in (1, 2):
            p = []
            for x in pts:
                z = alpha * base.form(x, v) % 3
                y = base.norm(tuple((x[k] + z * v[k]) % 3 for k in range(4)))
                p.append(idx[y])
            gens40.append(tuple(p))
    si = {S: i for i, S in enumerate(supports)}
    gens45 = [tuple(si[frozenset(p[x] for x in S)] for S in supports) for p in gens40]
    chosen = (18, 62, 77, 10)
    Gpaired = base.closure_paired([gens40[i] for i in chosen], [gens45[i] for i in chosen])
    assert len(Gpaired) == 25920

    def image_set(p, T):
        return frozenset(p[x] for x in T)

    # Full orbit of one certified two-ovoid.
    orbit432 = {image_set(p40, T0) for p40, _ in Gpaired}
    assert len(orbit432) == 432
    for T in orbit432:
        assert {len(nbr[x] & T) for x in T} == {4}
        assert {len(nbr[x] & T) for x in ALL40 - T} == {8}

    stab_T = [(p40,p45) for p40,p45 in Gpaired if image_set(p40,T0) == T0]
    assert len(stab_T) == 60
    order_T = Counter(base.porder(p40) for p40,_ in stab_T)
    assert order_T == Counter({1:1, 2:15, 3:20, 5:24})

    # Complement pairing.
    pairs = {canon_pair(T) for T in orbit432}
    assert len(pairs) == 216
    P0 = canon_pair(T0)
    stab_pair = []
    for p40,p45 in Gpaired:
        im = image_set(p40,T0)
        if im == T0 or im == ALL40-T0:
            stab_pair.append((p40,p45))
    assert len(stab_pair) == 120
    order_pair = Counter(base.porder(p40) for p40,_ in stab_pair)
    # S5 conjugacy classes: 1, transpositions, double transpositions, 3-cycles,
    # 3x2, 4-cycles, 5-cycles -> order totals below.
    assert order_pair == Counter({1:1, 2:25, 3:20, 4:30, 5:24, 6:20})

    # Rebuild all 216 sentinel five-circuits.
    circuits = []
    for C in itertools.combinations(range(45), 5):
        w = 0
        for i in C:
            w ^= masks[i]
        if w == 0:
            circuits.append(C)
    assert len(circuits) == 216
    cidx = {C:i for i,C in enumerate(circuits)}

    # Pair stabilizer orbits on the 45 sentinel minima.
    H45 = [p45 for _,p45 in stab_pair]
    orbits45 = orbit_partition_on_points(H45, 45, lambda g,i:g[i])
    orbit_sizes45 = sorted(len(O) for O in orbits45)

    fixed = []
    for i,C in enumerate(circuits):
        S = set(C)
        if all({g[x] for x in S} == S for g in H45):
            fixed.append(i)
    assert len(fixed) == 1
    base_ci = fixed[0]
    base_C = circuits[base_ci]

    # The fixed circuit should be visible as an actual stabilizer orbit.
    fixed_orbit_matches = [O for O in orbits45 if set(O) == set(base_C)]
    assert len(fixed_orbit_matches) == 1

    # Transport base pair -> base circuit through the full group.  Well-defined
    # iff the pair stabilizer fixes the circuit, and bijective iff all 216 appear.
    bridge = {}
    for p40,p45 in Gpaired:
        pair_key = canon_pair(image_set(p40,T0))
        C = tuple(sorted(p45[x] for x in base_C))
        ci = cidx[C]
        old = bridge.setdefault(pair_key, ci)
        assert old == ci
    assert len(bridge) == 216
    assert len(set(bridge.values())) == 216

    # Local combinatorial fingerprints of the canonical circuit relative to T0.
    fixed_support_intersections = sorted(len(supports[i] & T0) for i in base_C)
    all_support_intersections = Counter(len(S & T0) for S in supports)

    # How the A5 and S5 stabilizers act on the native 40 points.
    A5_40 = [p40 for p40,_ in stab_T]
    S5_40 = [p40 for p40,_ in stab_pair]
    A5_point_orbits = orbit_partition_on_points(A5_40, 40, lambda g,i:g[i])
    S5_point_orbits = orbit_partition_on_points(S5_40, 40, lambda g,i:g[i])

    out = {
        "schema":"w33.20260831.hemisystem-circuit-bridge.v1",
        "status":"PASS",
        "twoOvoid":{
            "holotradeWitnessSize":len(T0),
            "orbitSize":len(orbit432),
            "stabilizerOrder":len(stab_T),
            "stabilizerElementOrders":dict(sorted(order_T.items())),
            "stabilizerType":"A5",
            "pointOrbitSizes":sorted(map(len,A5_point_orbits)),
        },
        "complementPairs":{
            "count":len(pairs),
            "stabilizerOrder":len(stab_pair),
            "stabilizerElementOrders":dict(sorted(order_pair.items())),
            "stabilizerType":"S5",
            "pointOrbitSizes":sorted(map(len,S5_point_orbits)),
        },
        "sentinelFiveCircuits":{
            "count":len(circuits),
            "fixedByBasePairStabilizer":len(fixed),
            "baseCircuit":list(base_C),
            "pairStabilizerOrbitSizesOn45":orbit_sizes45,
            "baseCircuitIsStabilizerOrbit":True,
            "supportIntersectionsWithChosenHalf":fixed_support_intersections,
            "all45SupportIntersectionHistogram":dict(sorted(all_support_intersections.items())),
        },
        "equivariantBridge":{
            "domainSize":len(bridge),
            "imageSize":len(set(bridge.values())),
            "wellDefined":True,
            "bijective":True,
            "homogeneousSpace":"PSp(4,3)/S5",
        },
        "theorem":"The 432 W33 two-ovoids form one PSp(4,3)/A5 orbit. Complementation pairs them into 216 objects with S5 stabilizer. Each such S5 fixes a unique sentinel five-circuit, and transport gives a PSp(4,3)-equivariant bijection between complement-pairs of two-ovoids and the 216 sentinel five-circuits.",
        "boundary":"The bridge identifies two finite PSp(4,3)-sets. It does not identify either set with the projective qutrit Clifford group or assert a physical implementation."
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
    print(json.dumps({
        "status":"PASS","twoOvoidOrbit":432,"A5":len(stab_T),"pairs":216,
        "S5":len(stab_pair),"fixedCircuits":len(fixed),"orbit45":orbit_sizes45,
        "fixedSupportInts":fixed_support_intersections,
        "supportHist":dict(sorted(all_support_intersections.items()))
    }, sort_keys=True))

if __name__ == "__main__":
    main()
