#!/usr/bin/env python3
"""Classify every triple of minimum W33 sentinel words.

The 45 weight-eight minima are the points of the sentinel-shell GQ(4,2).
This audit classifies all C(45,3)=14,190 triple XORs by induced GQ edges and
triple support intersection.  It also extracts the dependency geometry hidden
in collisions of triple sums: the known 216 five-circuits and a new shell of
540 six-circuits, each inducing a perfect matching on its six GQ points.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

from w33_20260829_sentinel_shell_matroid import geometry, supports_from_N

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_20260829_SENTINEL_TRIPLE_SHELL.json"


def main():
    _, _, N = geometry()
    supports, masks = supports_from_N(N)

    # The 720 distance-12 pair sums are unique and form the complete weight-12
    # shell from the preceding theorem.
    pair12 = {}
    for i, j in itertools.combinations(range(45), 2):
        w = masks[i] ^ masks[j]
        if w.bit_count() == 12:
            assert w not in pair12
            pair12[w] = (i, j)
    assert len(pair12) == 720

    strata = Counter()
    reps = defaultdict(list)
    for T in itertools.combinations(range(45), 3):
        edge_count = sum(
            1 for i, j in itertools.combinations(T, 2)
            if not (supports[i] & supports[j])
        )
        triple_intersection = len(supports[T[0]] & supports[T[1]] & supports[T[2]])
        w = masks[T[0]] ^ masks[T[1]] ^ masks[T[2]]
        strata[(edge_count, triple_intersection, w.bit_count())] += 1
        reps[w].append(T)

    expected = Counter({
        (0, 0, 12): 2160,
        (0, 1, 16): 2880,
        (0, 2, 20): 240,
        (1, 0, 16): 6480,
        (2, 0, 20): 2160,
        (3, 0, 24): 270,
    })
    assert strata == expected
    assert sum(strata.values()) == 14190

    distinct_by_weight = Counter(w.bit_count() for w in reps)
    assert distinct_by_weight == Counter({12:720, 16:6120, 20:2400, 24:270})
    multiplicities = Counter((w.bit_count(), len(Ts)) for w, Ts in reps.items())
    assert multiplicities == Counter({
        (12,3):720,
        (16,2):3240,
        (16,1):2880,
        (20,1):2400,
        (24,1):270,
    })

    # Every weight-12 triple equals the unique weight-12 pair sum.  The triple
    # and pair are disjoint and their five-word union is a 5-circuit.  Each
    # 5-circuit occurs through its ten complementary 3+2 decompositions.
    five_counts = Counter()
    for w, Ts in reps.items():
        if w.bit_count() != 12:
            continue
        assert w in pair12 and len(Ts) == 3
        P = pair12[w]
        for T in Ts:
            assert set(P).isdisjoint(T)
            C = tuple(sorted(P + T))
            z = 0
            for i in C: z ^= masks[i]
            assert z == 0 and len(C) == 5
            five_counts[C] += 1
    assert len(five_counts) == 216
    assert set(five_counts.values()) == {10}

    # Equal XORs of disjoint triples are exactly 6-circuits.  Each six-circuit
    # has ten complementary 3+3 partitions; geometrically its six GQ points
    # induce three disjoint edges, i.e. a perfect matching.
    six_counts = Counter()
    collision_weights = Counter()
    for w, Ts in reps.items():
        for U, V in itertools.combinations(Ts, 2):
            if not set(U).isdisjoint(V):
                continue
            C = tuple(sorted(U + V))
            z = 0
            for i in C: z ^= masks[i]
            assert z == 0 and len(C) == 6
            six_counts[C] += 1
            collision_weights[w.bit_count()] += 1
    assert len(six_counts) == 540
    assert set(six_counts.values()) == {10}
    assert collision_weights == Counter({16:3240, 12:2160})

    for C in six_counts:
        deg = {i:0 for i in C}
        edges = 0
        for i, j in itertools.combinations(C, 2):
            if not (supports[i] & supports[j]):
                deg[i] += 1; deg[j] += 1; edges += 1
        assert edges == 3
        assert set(deg.values()) == {1}

    out = {
        "schema": "w33.20260829.sentinel-triple-shell.v1",
        "status": "PASS",
        "tripleCount": 14190,
        "strata": [
            {"GQEdges":e,"tripleSupportIntersection":t,"xorWeight":w,"triples":n}
            for (e,t,w),n in sorted(expected.items())
        ],
        "distinctTripleSumsByWeight": {str(k):v for k,v in sorted(distinct_by_weight.items())},
        "representationMultiplicities": [
            {"xorWeight":w,"tripleRepresentations":m,"words":n}
            for (w,m),n in sorted(multiplicities.items())
        ],
        "fiveCircuitRecovery": {
            "circuits":216,
            "decompositionsPerCircuit":10,
            "theorem":"each weight-12 triple sum equals the unique complementary noncollinear pair sum; their union is a five-circuit"
        },
        "sixCircuitShell": {
            "circuits":540,
            "threePlusThreePartitionsPerCircuit":10,
            "GQInducedGraph":"3K2 (a perfect matching)",
            "collisionPartitionsByXorWeight":{"12":2160,"16":3240}
        },
        "boundary":"The count 540 is an exact new dependency shell of this binary matroid; no identification with other project 540-sets is asserted without an equivariant map."
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status":"PASS","triples":14190,"fiveCircuits":216,"sixCircuits":540,"sixCircuitGraph":"3K2"}))


if __name__ == "__main__":
    main()
