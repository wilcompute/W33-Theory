#!/usr/bin/env python3
"""Resolve the three order-3 Clifford species on the 72 central circuit fibres.

The central cover audit gives 216 sentinel five-circuits -> 72 free C3 deck
fibres, with Q=K/Z ~= ASL(2,3) acting faithfully in two 36-orbits.  The local
lift audit and affine quotient audit split the 40 cyclic order-three subgroups
of Q into conjugacy classes 4+12+24, with the unique 24-class lifting to C9.

This script computes their action on the actual 72 circuit fibres and proves a
sharper stabilizer theorem:
  * the 4 translation C3s fix 9 fibres in Q/S3 and none in Q/C6;
  * the 12 fixed-line unipotent C3s fix 3 fibres in Q/C6 and none in Q/S3;
  * the 24 nonsplit C9 directions are fixed-point-free on both 36-orbits.
Thus the nonsplit obstruction is exactly the order-three species avoiding both
point-stabilizer geometries.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

import w33_20260829_216_clifford_torsor_nogo as base

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_20260830_CLIFFORD_C3_FIBRE_STABILIZER_GEOMETRY.json"
AFFINE = ROOT / "data/PART_W33_20260830_CLIFFORD_C3_ORDER3_ORBITS.json"


def cycle_shape_subset(p, subset):
    subset = set(subset); seen = set(); out = Counter()
    for i in sorted(subset):
        if i in seen:
            continue
        j = i; n = 0
        while j not in seen:
            assert j in subset
            seen.add(j); n += 1; j = p[j]
        out[n] += 1
    return {str(k): v for k, v in sorted(out.items())}


def orbit_partition(G, n):
    rem = set(range(n)); out = []
    while rem:
        s = min(rem); O = {g[s] for g in G}
        out.append(sorted(O)); rem -= O
    return sorted(out, key=lambda O: (-len(O), O))


def main():
    pts, idx, _lines, N = base.geometry()
    supports, masks = base.supports_from_N(N)

    circuits = []
    for C in itertools.combinations(range(45), 5):
        w = 0
        for i in C:
            w ^= masks[i]
        if w == 0:
            circuits.append(C)
    assert len(circuits) == 216
    cidx = {C: i for i, C in enumerate(circuits)}

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

    K = {p45 for p40, p45 in Gpaired if p40[0] == 0}
    assert len(K) == 648

    def act_circuit(i, g):
        return cidx[tuple(sorted(g[x] for x in circuits[i]))]

    kgens = base.deterministic_generators(K, 45)
    Z = [z for z in K if all(base.compose(z, g) == base.compose(g, z) for g in kgens)]
    assert len(Z) == 3
    e45 = tuple(range(45))
    z = next(x for x in Z if x != e45)

    zperm = tuple(act_circuit(i, z) for i in range(216))
    zfibres = []; seen = set()
    for i in range(216):
        if i in seen:
            continue
        O = []; j = i
        while j not in seen:
            seen.add(j); O.append(j); j = zperm[j]
        zfibres.append(tuple(sorted(O)))
    assert len(zfibres) == 72 and {len(O) for O in zfibres} == {3}
    fibre_of = {x: i for i, O in enumerate(zfibres) for x in O}

    def qperm(g):
        return tuple(fibre_of[act_circuit(O[0], g)] for O in zfibres)

    Q = {qperm(g) for g in K}
    assert len(Q) == 216
    lifts = defaultdict(list)
    for g in K:
        lifts[qperm(g)].append(g)
    assert len(lifts) == 216 and {len(v) for v in lifts.values()} == {3}

    q_orbits = orbit_partition(Q, 72)
    assert [len(O) for O in q_orbits] == [36, 36]
    fibre_orbits = {}
    for O in q_orbits:
        vals = set()
        for fi in O:
            C = circuits[zfibres[fi][0]]
            vals.add(sum(0 in supports[j] for j in C))
        assert len(vals) == 1
        r = next(iter(vals)); assert r in (0, 2)
        fibre_orbits[r] = O
    assert set(fibre_orbits) == {0, 2}

    e72 = tuple(range(72))
    order3_subgroups = {
        frozenset((e72, q, base.compose(q, q)))
        for q in Q if base.porder(q) == 3
    }
    assert len(order3_subgroups) == 40
    subs = list(order3_subgroups); sidx = {H: i for i, H in enumerate(subs)}
    qinv = {q: base.invperm(q) for q in Q}

    def conj(x, q):
        return base.compose(base.compose(x, q), qinv[x])

    rem = set(range(40)); suborbits = []
    while rem:
        i = min(rem); H = subs[i]
        O = {
            sidx[frozenset(conj(x, q) for q in H)]
            for x in Q
        }
        rem -= O; suborbits.append(sorted(O))
    assert sorted(len(O) for O in suborbits) == [4, 12, 24]

    affine = json.loads(AFFINE.read_text())
    assert affine["status"] == "PASS"
    affine_by_size = {
        row["subgroups"]: row
        for row in affine["cyclicOrder3Subgroups"]["orbits"]
    }
    assert set(affine_by_size) == {4, 12, 24}

    rows = []
    for O in sorted(suborbits, key=len):
        H = subs[O[0]]
        q = next(x for x in H if x != e72)
        lift_orders = sorted(base.porder(x) for x in lifts[q])
        restriction = "nonsplit C9" if lift_orders == [9, 9, 9] else "split C3 x C3"
        r0 = fibre_orbits[0]; r2 = fibre_orbits[2]
        fixed0 = sum(q[x] == x for x in r0)
        fixed2 = sum(q[x] == x for x in r2)
        row = {
            "subgroupConjugacyOrbitSize": len(O),
            "affineType": affine_by_size[len(O)]["affineType"],
            "extensionRestriction": restriction,
            "liftOrdersOfGeneratorCoset": lift_orders,
            "cycleShape72": cycle_shape_subset(q, range(72)),
            "cycleShapeOnS3Orbit36": cycle_shape_subset(q, r0),
            "cycleShapeOnC6Orbit36": cycle_shape_subset(q, r2),
            "fixedFibresInS3Orbit": fixed0,
            "fixedFibresInC6Orbit": fixed2,
            "conjugateS3StabilizersContainingSubgroup": fixed0,
            "conjugateC6StabilizersContainingSubgroup": fixed2,
        }
        rows.append(row)

    assert rows == [
        {
            "subgroupConjugacyOrbitSize": 4,
            "affineType": "pure-translation",
            "extensionRestriction": "split C3 x C3",
            "liftOrdersOfGeneratorCoset": [3, 3, 3],
            "cycleShape72": {"1": 9, "3": 21},
            "cycleShapeOnS3Orbit36": {"1": 9, "3": 9},
            "cycleShapeOnC6Orbit36": {"3": 12},
            "fixedFibresInS3Orbit": 9,
            "fixedFibresInC6Orbit": 0,
            "conjugateS3StabilizersContainingSubgroup": 9,
            "conjugateC6StabilizersContainingSubgroup": 0,
        },
        {
            "subgroupConjugacyOrbitSize": 12,
            "affineType": "unipotent-with-affine-fixed-line",
            "extensionRestriction": "split C3 x C3",
            "liftOrdersOfGeneratorCoset": [3, 3, 3],
            "cycleShape72": {"1": 3, "3": 23},
            "cycleShapeOnS3Orbit36": {"3": 12},
            "cycleShapeOnC6Orbit36": {"1": 3, "3": 11},
            "fixedFibresInS3Orbit": 0,
            "fixedFibresInC6Orbit": 3,
            "conjugateS3StabilizersContainingSubgroup": 0,
            "conjugateC6StabilizersContainingSubgroup": 3,
        },
        {
            "subgroupConjugacyOrbitSize": 24,
            "affineType": "fixed-point-free-nontranslation-unipotent",
            "extensionRestriction": "nonsplit C9",
            "liftOrdersOfGeneratorCoset": [9, 9, 9],
            "cycleShape72": {"3": 24},
            "cycleShapeOnS3Orbit36": {"3": 12},
            "cycleShapeOnC6Orbit36": {"3": 12},
            "fixedFibresInS3Orbit": 0,
            "fixedFibresInC6Orbit": 0,
            "conjugateS3StabilizersContainingSubgroup": 0,
            "conjugateC6StabilizersContainingSubgroup": 0,
        },
    ]

    # Incidence double counts sharpen the stabilizer statement.  Every S3
    # fibre stabilizer contains one translation-class C3, every C6 stabilizer
    # contains one fixed-line-class C3, and no fibre stabilizer contains an
    # obstruction-class C3.
    assert 4 * rows[0]["fixedFibresInS3Orbit"] == 36
    assert 12 * rows[1]["fixedFibresInC6Orbit"] == 36

    out = {
        "schema": "w33.20260830.clifford-c3-fibre-stabilizer-geometry.v1",
        "status": "PASS",
        "cover": {"circuitStates": 216, "centralC3Fibres": 72, "quotientOrder": 216},
        "fibreOrbits": [
            {"supportsThroughDistinguishedW33Point": 0, "size": 36, "pointStabilizer": "S3"},
            {"supportsThroughDistinguishedW33Point": 2, "size": 36, "pointStabilizer": "C6"},
        ],
        "order3Species": rows,
        "stabilizerIncidenceTheorem": {
            "S3Fibres": "each of the 36 S3-stabilized fibres contains the unique C3 from the 4-subgroup translation class",
            "C6Fibres": "each of the 36 C6-stabilized fibres contains the unique C3 from the 12-subgroup fixed-line unipotent class",
            "C9Obstruction": "the 24 nonsplit order-three directions fix no circuit fibre and lie in neither point-stabilizer species",
        },
        "theorem": "The nonsplit 24-class is exactly the order-three Clifford species that is fixed-point-free on both 36-fibre orbits; the two split species are detected separately by the S3 and C6 stabilizer geometries.",
        "boundary": "Exact in the 72-fibre permutation representation of the projective one-qutrit Clifford quotient. No physical qutrit/OAM coordinate identification is asserted without an explicit intertwiner.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status":"PASS","species":[4,12,24],"fixedS3":[9,0,0],"fixedC6":[0,3,0],"nonsplit":"24-class"}, sort_keys=True))


if __name__ == "__main__":
    main()
