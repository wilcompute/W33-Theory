#!/usr/bin/env python3
"""Exact binary extension theorem linking W33 adjacency and sentinel codes.

The 45 Hermitian eight-supports generate the historical [40,15,8]_2 sentinel.
The W33 adjacency rows generate a rank-16 binary code.  This audit proves the
rank gap is exactly one geometric character: parity on any W33 line.

In particular, if C_A is the row code of the 40x40 W33 adjacency matrix and
C_S is the sentinel code, then

    C_S = span{N(u)+N(v)} = {x in C_A : |x cap L| = 0 mod 2}

for every W33 line L.  Every neighborhood N(v) has odd intersection with every
line, so all 40 neighborhoods lie in the same nonzero coset C_A/C_S.
"""
from __future__ import annotations

import json
from pathlib import Path

from w33_20260829_pg34_polarity_sentinel import geometry, trade_incidence, gf2_basis, in_span

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_20260829_ADJACENCY_SENTINEL_EXTENSION.json"


def mask(bits):
    return sum((x & 1) << i for i, x in enumerate(bits))


def same_span(xs, ys):
    bx, by = gf2_basis(xs), gf2_basis(ys)
    return all(in_span(x, by) for x in bx) and all(in_span(y, bx) for y in by)


def main():
    N, A = geometry()
    B, _ = trade_incidence(N)

    adjacency = [mask(row) for row in A]
    sentinel = [sum((B[i][j] & 1) << i for i in range(40)) for j in range(45)]
    line_masks = [mask(row) for row in N]

    BA = gf2_basis(adjacency)
    BS = gf2_basis(sentinel)
    assert len(BA) == 16
    assert len(BS) == 15
    assert all(in_span(w, BA) for w in sentinel)

    # All neighborhood differences generate exactly the sentinel code.
    differences = [adjacency[i] ^ adjacency[0] for i in range(1, 40)]
    assert len(gf2_basis(differences)) == 15
    assert same_span(differences, sentinel)

    # Generalized-quadrangle geometry supplies the missing character.  A
    # vertex on a line sees the other three line points; a vertex off the line
    # sees the unique collinear point on that line.  Either way the parity is 1.
    for lm in line_masks:
        assert all((a & lm).bit_count() % 2 == 1 for a in adjacency)
        assert all((s & lm).bit_count() % 2 == 0 for s in sentinel)

    # Hence every line defines the same nonzero functional on C_A, with kernel
    # C_S.  Equivalently all line indicators differ by vectors in C_A^perp.
    for l0 in line_masks[1:]:
        d = l0 ^ line_masks[0]
        assert all((d & a).bit_count() % 2 == 0 for a in adjacency)

    # No adjacency row lies in C_S, but any two differ by a sentinel word.
    assert all(not in_span(a, BS) for a in adjacency)
    assert all(in_span(adjacency[i] ^ adjacency[j], BS)
               for i in range(40) for j in range(i))

    out = {
        "schema": "w33.20260829.adjacency-sentinel-extension.v1",
        "status": "PASS",
        "adjacencyCode": {"length": 40, "dimension": 16},
        "sentinelCode": {"parameters": "[40,15,8]_2", "dimension": 15},
        "inclusion": "C_S is a codimension-one subcode of C_A",
        "generatorTheorem": "C_S = span_F2{N(u)+N(v): u,v in W33}",
        "quotient": "C_A/C_S = C2; every one of the 40 neighborhoods represents its unique nonzero coset",
        "geometricCharacter": {
            "definition": "chi_L(x)=|supp(x) intersect L| mod 2",
            "independentOfLineOnCA": True,
            "neighborhoodValue": 1,
            "sentinelValue": 0,
            "kernelOnAdjacencyCode": "C_S",
            "reason": "a vertex sees 3 points of L when it lies on L and the unique collinear point of L otherwise"
        },
        "interpretation": "The missing binary dimension is universal W33 line parity, not an unexplained extra generator."
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status":"PASS","rankAdjacency":16,"rankSentinel":15,"quotient":"C2","character":"line parity"}))


if __name__ == "__main__":
    main()
