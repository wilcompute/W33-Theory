#!/usr/bin/env python3
"""Build the exact PSp(4,3) pair geometry between 216 five- and 540 six-circuits.

The sentinel binary matroid has one 216-orbit of five-circuits and one 540-orbit
of six-circuits.  This audit acts on all 216*540 ordered cross-pairs and computes
the orbital refinement.  There are 17 PSp(4,3)-orbitals.

The maximal-overlap relation |C5 intersect C6|=3 is especially rigid: it is a
(216,540)-biregular relation of degrees (20,8), split into two equal orbitals of
size 2160.  For a fixed six-circuit, its induced 3K2 matching makes the eight
maximal-overlap five-circuits the eight vertices of a binary cube: each chooses
one endpoint from each matching edge.  The faithful S4 quotient of the order-48
six-circuit stabilizer splits that cube into the even and odd parity tetrahedra
4+4.  The names even/odd depend on endpoint orientation; the unordered 4+4
partition is intrinsic.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, deque
from pathlib import Path

import w33_20260829_216_clifford_torsor_nogo as base
from w33_20260830_sentinel_six_circuit_orbit import six_circuits

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_20260830_C5_C6_COHERENT_INCIDENCE.json"


def main():
    pts, idx, _lines, N = base.geometry()
    supports, masks = base.supports_from_N(N)

    c5 = []
    for C in itertools.combinations(range(45), 5):
        w = 0
        for i in C:
            w ^= masks[i]
        if w == 0:
            c5.append(C)
    assert len(c5) == 216
    c6 = six_circuits(masks)
    assert len(c6) == 540
    i5 = {C: i for i, C in enumerate(c5)}
    i6 = {C: i for i, C in enumerate(c6)}

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
    gg = [gens45[i] for i in chosen]
    G = base.closure(gg, 45)
    assert len(G) == 25920

    act5 = [tuple(i5[tuple(sorted(g[x] for x in C))] for C in c5) for g in gg]
    act6 = [tuple(i6[tuple(sorted(g[x] for x in C))] for C in c6) for g in gg]

    # Full cross-pair orbital decomposition.
    seen = set(); orbitals = []
    for a in range(216):
        for b in range(540):
            seed = a * 540 + b
            if seed in seen:
                continue
            O = {seed}; seen.add(seed); Q = deque([seed])
            while Q:
                z = Q.popleft(); x, y = divmod(z, 540)
                for p5, p6 in zip(act5, act6):
                    nz = p5[x] * 540 + p6[y]
                    if nz not in seen:
                        seen.add(nz); O.add(nz); Q.append(nz)
            orbitals.append(O)
    assert len(seen) == 216 * 540
    sizes = sorted(len(O) for O in orbitals)
    assert sizes == [
        1080, 2160, 2160, 2160, 3240, 4320, 4320,
        6480, 6480, 6480, 6480, 6480,
        12960, 12960, 12960, 12960, 12960,
    ]

    orbital_rows = []
    for O in orbitals:
        seed = next(iter(O)); a, b = divmod(seed, 540)
        t = len(set(c5[a]) & set(c6[b]))
        orbital_rows.append({
            "size": len(O),
            "intersection": t,
            "fiveCircuitSubdegree": len(O) // 216,
            "sixCircuitSubdegree": len(O) // 540,
        })
    orbital_rows.sort(key=lambda r: (r["intersection"], r["size"], r["fiveCircuitSubdegree"]))

    by_intersection = Counter()
    orbital_count_by_intersection = Counter()
    for O in orbitals:
        seed = next(iter(O)); a, b = divmod(seed, 540)
        t = len(set(c5[a]) & set(c6[b]))
        by_intersection[t] += len(O)
        orbital_count_by_intersection[t] += 1
    assert dict(sorted(by_intersection.items())) == {0: 54000, 1: 51840, 2: 6480, 3: 4320}
    assert dict(sorted(orbital_count_by_intersection.items())) == {0: 8, 1: 6, 2: 1, 3: 2}

    # Maximal-overlap incidence is biregular: degrees 20 from C5 and 8 from C6.
    t3 = [O for O in orbitals if len(set(c5[next(iter(O)) // 540]) & set(c6[next(iter(O)) % 540])) == 3]
    assert sorted(len(O) for O in t3) == [2160, 2160]
    assert 4320 // 216 == 20 and 4320 // 540 == 8
    assert 2160 // 216 == 10 and 2160 // 540 == 4

    # Native GQ(4,2) graph on the 45 minimum supports.
    adj = [[False] * 45 for _ in range(45)]
    for i, j in itertools.combinations(range(45), 2):
        if not (supports[i] & supports[j]):
            adj[i][j] = adj[j][i] = True

    C6 = tuple(c6[0]); C6set = set(C6)
    matching = sorted(
        tuple(sorted((i, j)))
        for i, j in itertools.combinations(C6, 2)
        if adj[i][j]
    )
    assert len(matching) == 3
    deg = Counter(x for e in matching for x in e)
    assert set(deg.values()) == {1}

    neighbours = [i for i, C in enumerate(c5) if len(set(C) & C6set) == 3]
    assert len(neighbours) == 8
    patterns = {}
    for i in neighbours:
        T = set(c5[i]) & C6set
        bits = []
        for a, b in matching:
            assert (a in T) + (b in T) == 1
            bits.append(0 if a in T else 1)
        patterns[i] = tuple(bits)
    assert set(patterns.values()) == set(itertools.product((0, 1), repeat=3))

    Stab6 = [g for g in G if {g[x] for x in C6set} == C6set]
    assert len(Stab6) == 48
    npos = {x: i for i, x in enumerate(neighbours)}
    restrictions = {
        tuple(npos[i5[tuple(sorted(g[x] for x in c5[n]))]] for n in neighbours)
        for g in Stab6
    }
    assert len(restrictions) == 24
    assert Counter(base.porder(r) for r in restrictions) == Counter({1: 1, 2: 9, 3: 8, 4: 6})
    kernel = [
        g for g in Stab6
        if all(i5[tuple(sorted(g[x] for x in c5[n]))] == n for n in neighbours)
    ]
    assert len(kernel) == 2

    rem = set(neighbours); local_orbits = []
    while rem:
        s = min(rem)
        O = {
            i5[tuple(sorted(g[x] for x in c5[s]))]
            for g in Stab6
        }
        rem -= O; local_orbits.append(sorted(O))
    assert sorted(len(O) for O in local_orbits) == [4, 4]
    parity_sets = []
    for O in local_orbits:
        pars = {sum(patterns[i]) % 2 for i in O}
        assert len(pars) == 1
        parity_sets.append(next(iter(pars)))
    assert sorted(parity_sets) == [0, 1]

    out = {
        "schema": "w33.20260830.c5-c6-coherent-incidence.v1",
        "status": "PASS",
        "ambientGroup": {"name": "PSp(4,3)", "order": 25920},
        "objects": {"fiveCircuits": 216, "sixCircuits": 540, "crossPairs": 116640},
        "coherentPairGeometry": {
            "orbitals": 17,
            "orbitalSizes": sizes,
            "fiveCircuitSubdegrees": sorted(len(O) // 216 for O in orbitals),
            "intersectionPairCounts": {str(k): v for k, v in sorted(by_intersection.items())},
            "orbitalCountsByIntersection": {str(k): v for k, v in sorted(orbital_count_by_intersection.items())},
            "orbitalsDetail": orbital_rows,
        },
        "maximalOverlapIncidence": {
            "intersection": 3,
            "pairs": 4320,
            "degreeAtFiveCircuit": 20,
            "degreeAtSixCircuit": 8,
            "PSpOrbitalSplit": [2160, 2160],
            "degreePerOrbitalAtFiveCircuit": 10,
            "degreePerOrbitalAtSixCircuit": 4,
            "localSixCircuitGraph": "3K2",
            "localEightNeighbours": "all 2^3 choices of one endpoint from each matching edge",
            "sixCircuitStabilizer": "C2 x S4 of order 48",
            "faithfulActionOnEightNeighbours": "S4 of order 24",
            "faithfulOrderSpectrum": {"1": 1, "2": 9, "3": 8, "4": 6},
            "kernelOnEightNeighbours": "C2",
            "localOrbitSizes": [4, 4],
            "cubeReading": "the two local S4 orbits are the even- and odd-parity tetrahedra in the 3-cube; swapping an endpoint convention exchanges the labels but preserves the unordered 4+4 partition",
        },
        "theorem": "The 216x540 circuit cross-action has 17 PSp orbitals. Its maximal-overlap relation is a two-colour (20,8)-biregular incidence geometry whose local eight-neighbour fibre is the cube split by S4 into two parity tetrahedra 4+4.",
        "boundary": "This is an intrinsic sentinel-matroid/PSp incidence geometry. Its 4+4 cube parity resembles other project chirality splittings, but no identification with a separate Holotrade or photonic chirality variable is asserted without an equivariant map.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status":"PASS","orbitals":17,"intersectionCounts":dict(sorted(by_intersection.items())),"maximalDegrees":[20,8],"localSplit":[4,4]}, sort_keys=True))


if __name__ == "__main__":
    main()
