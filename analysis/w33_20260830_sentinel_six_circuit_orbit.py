#!/usr/bin/env python3
"""Resolve the PSp(4,3) action on the 540 sentinel six-circuit shell.

The preceding triple-shell audit produced 540 six-circuits among the 45
minimum words of the [40,15,8]_2 sentinel code.  This script proves that these
540 circuits form one PSp(4,3)-orbit and identifies the exact order-48 circuit
stabilizer.
"""
from __future__ import annotations

import itertools
import json
import math
from collections import Counter, defaultdict, deque
from pathlib import Path

from w33_20260829_216_clifford_torsor_nogo import (
    closure, compose, form, geometry, norm, porder, supports_from_N,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_20260830_SENTINEL_SIX_CIRCUIT_ORBIT.json"


def six_circuits(masks):
    reps = defaultdict(list)
    for T in itertools.combinations(range(45), 3):
        w = masks[T[0]] ^ masks[T[1]] ^ masks[T[2]]
        reps[w].append(T)
    out = set()
    for Ts in reps.values():
        for U, V in itertools.combinations(Ts, 2):
            if set(U).isdisjoint(V):
                out.add(tuple(sorted(U + V)))
    assert len(out) == 540
    return sorted(out)


def closure_local(gens, n, limit=None):
    e = tuple(range(n)); H = {e}; Q = deque([e])
    while Q:
        a = Q.popleft()
        for g in gens:
            h = compose(g, a)
            if h not in H:
                H.add(h); Q.append(h)
                if limit is not None and len(H) > limit:
                    raise AssertionError("subgroup exceeded limit")
    return H


def main():
    pts, idx, _lines, N = geometry()
    supports, masks = supports_from_N(N)
    circuits = six_circuits(masks)
    cidx = {C: i for i, C in enumerate(circuits)}

    # Same deterministic native transvection generators used by the preceding
    # order-216 audit; their closure is PSp(4,3) of order 25920.
    gens40 = []
    for v in pts:
        for alpha in (1, 2):
            p = []
            for x in pts:
                z = alpha * form(x, v) % 3
                y = norm(tuple((x[k] + z * v[k]) % 3 for k in range(4)))
                p.append(idx[y])
            gens40.append(tuple(p))
    si = {S: i for i, S in enumerate(supports)}
    gens45 = [
        tuple(si[frozenset(p[x] for x in S)] for S in supports)
        for p in gens40
    ]
    chosen = (18, 62, 77, 10)
    gg = [gens45[i] for i in chosen]
    G = closure(gg, 45)
    assert len(G) == 25920

    def image(C, g):
        return tuple(sorted(g[x] for x in C))

    # Generator orbit already exhausts the 540-shell.
    O = {0}; Q = deque([0])
    while Q:
        i = Q.popleft()
        for g in gg:
            j = cidx[image(circuits[i], g)]
            if j not in O:
                O.add(j); Q.append(j)
    assert len(O) == 540

    C = circuits[0]; Cset = set(C)
    stab = {g for g in G if {g[x] for x in C} == Cset}
    assert len(stab) == 48
    assert 25920 // len(stab) == 540

    # The six GQ points induce 3K2.  The stabilizer is not the full 48-element
    # automorphism group of that matching on these six labels: a central C2
    # fixes all six circuit points, leaving an order-24 faithful quotient.
    edges = [
        (i, j) for i, j in itertools.combinations(C, 2)
        if not (supports[i] & supports[j])
    ]
    assert len(edges) == 3
    deg = Counter(x for e in edges for x in e)
    assert set(deg.values()) == {1}

    pos = {x: i for i, x in enumerate(C)}
    restrictions = {
        tuple(pos[g[x]] for x in C)
        for g in stab
    }
    assert len(restrictions) == 24
    qorders = Counter(porder(r) for r in restrictions)
    assert qorders == Counter({1: 1, 2: 9, 3: 8, 4: 6})

    e45 = tuple(range(45))
    kernel = {
        g for g in stab if all(g[x] == x for x in C)
    }
    assert len(kernel) == 2
    z = next(g for g in kernel if g != e45)
    assert porder(z) == 2
    assert all(compose(z, g) == compose(g, z) for g in stab)

    # Exhibit a complement of order 24, proving the central extension splits.
    # Its order spectrum is exactly S4, and its restriction is faithful.
    by_order = defaultdict(list)
    for g in stab:
        by_order[porder(g)].append(g)
    complement = None
    for a in by_order[4]:
        for b in by_order[3]:
            H = closure_local([a, b], 45, 48)
            if len(H) != 24 or z in H:
                continue
            rr = {tuple(pos[g[x]] for x in C) for g in H}
            if len(rr) == 24:
                complement = H
                break
        if complement is not None:
            break
    assert complement is not None
    assert Counter(porder(g) for g in complement) == Counter({1:1, 2:9, 3:8, 4:6})
    assert len({compose(k, h) for k in kernel for h in complement}) == 48

    full_orders = Counter(porder(g) for g in stab)
    assert full_orders == Counter({1:1, 2:19, 3:8, 4:12, 6:8})

    out = {
        "schema": "w33.20260830.sentinel-six-circuit-orbit.v1",
        "status": "PASS",
        "ambientGroup": {"name":"PSp(4,3)", "order":25920},
        "sixCircuitShell": {
            "size": 540,
            "orbitSizes": [540],
            "transitive": True,
            "inducedGQGraph": "3K2",
        },
        "stabilizer": {
            "order": 48,
            "isomorphism": "C2 x S4",
            "centralKernelOnSixCircuitPoints": "C2",
            "faithfulSixPointQuotient": "S4",
            "quotientOrderSpectrum": {str(k):v for k,v in sorted(qorders.items())},
            "fullOrderSpectrum": {str(k):v for k,v in sorted(full_orders.items())},
            "splitComplementOrder": 24,
            "geometricReading": "S4 acts on the six edges of a tetrahedron and preserves the three opposite-edge pairs; the extra central C2 fixes all six circuit labels but acts nontrivially on the remaining 45-point shell.",
        },
        "theorem": "The 540 sentinel six-circuits are the homogeneous space PSp(4,3)/(C2 x S4).",
        "boundary": "The exact order-48 stabilizer is established internally. No identification with other project order-48 or 540-object constructions is asserted without an explicit equivariant map.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status":"PASS","orbit":540,"stabilizer":48,"stabilizerType":"C2 x S4"}))


if __name__ == "__main__":
    main()
