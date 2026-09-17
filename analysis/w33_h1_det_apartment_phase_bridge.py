#!/usr/bin/env python3
"""W33 apartment -> projective basis -> determinant phase bridge.

Pass 4474 distinguishes the 1620 induced W33 quadrangles/apartments from the
120 line-internal simple four-cycles.  The new determinant/Tutte theorem says
that det((VV^T)J) is the rank-four matroid basis count modulo 3.

This file welds the two structures directly:

  every one of the 1620 induced W33 C4 apartments is a projective basis of
  F3^4, hence det((VV^T)J)=1.

Equivalently, for a cyclic apartment p1-p2-p3-p4-p1, adjacent symplectic
products vanish while the two diagonal products a=<p1,p3>, b=<p2,p4> are
nonzero.  The 4x4 alternating Gram determinant is (ab)^2=1 in F3, so the four
points are a basis.  The candidate central-character phase is therefore
uniform: omega^r on every apartment.

The script also constructs the 40 generalized-quadrangle lines and verifies
that each induced point C4 lifts uniquely to an alternating point-line Levi
8-cycle, giving the same 1620 apartments.

Scope: exact finite geometry only.  This does not certify a VOA/OPE coupling or
a physical apartment-addressed phase gate.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_h1_det_apartment_phase_bridge.json"
P = 3
J = np.array(
    [[0, 1, 0, 0], [-1, 0, 0, 0], [0, 0, 0, 1], [0, 0, -1, 0]],
    dtype=np.int64,
) % P


def canon(v):
    v = np.asarray(v, dtype=np.int64) % P
    i = next(i for i, x in enumerate(v) if x)
    return tuple((v * pow(int(v[i]), -1, P)) % P)


def om(a, b):
    return int(np.asarray(a, dtype=np.int64) @ J @ np.asarray(b, dtype=np.int64) % P)


POINTS = sorted(
    {canon(v) for v in itertools.product(range(P), repeat=4) if any(v)}
)
assert len(POINTS) == 40


def det_mod3(A):
    A = np.asarray(A, dtype=np.int64).copy() % P
    n = A.shape[0]
    d = 1
    for c in range(n):
        q = next((r for r in range(c, n) if A[r, c]), None)
        if q is None:
            return 0
        if q != c:
            A[[c, q]] = A[[q, c]]
            d = -d
        a = int(A[c, c])
        d = d * a % P
        ia = pow(a, -1, P)
        for r in range(c + 1, n):
            if A[r, c]:
                A[r] = (A[r] - A[r, c] * ia * A[c]) % P
    return d % P


def main(write=True):
    # W33 point graph.
    A = np.zeros((40, 40), dtype=np.int64)
    for i, a in enumerate(POINTS):
        for j, b in enumerate(POINTS):
            if i != j and om(a, b) == 0:
                A[i, j] = 1
    assert set(A.sum(axis=1)) == {12}
    assert int(A.sum() // 2) == 240

    # Build the 40 isotropic GQ lines and the unique edge -> line map.
    lines = set()
    edge_line_set = {}
    for i, j in itertools.combinations(range(40), 2):
        if not A[i, j]:
            continue
        a = np.asarray(POINTS[i])
        b = np.asarray(POINTS[j])
        line = frozenset(
            canon(x * a + y * b)
            for x in range(P)
            for y in range(P)
            if x or y
        )
        assert len(line) == 4
        lines.add(line)
        edge_line_set[(i, j)] = line
    lines = sorted(lines, key=lambda z: sorted(z))
    line_index = {z: i for i, z in enumerate(lines)}
    assert len(lines) == 40
    assert len(edge_line_set) == 240

    apartments = []
    diagonal_products = []
    levi_packets = set()

    for I in itertools.combinations(range(40), 4):
        sub = A[np.ix_(I, I)]
        # Induced C4: four edges and every vertex degree two.
        if int(sub.sum() // 2) != 4 or not np.all(sub.sum(axis=1) == 2):
            continue

        # Find one cyclic ordering by walking the induced 2-regular graph.
        start = I[0]
        nbr = [x for x in I if x != start and A[start, x]]
        p1, p2 = start, nbr[0]
        prev, cur = p1, p2
        cyc = [p1, p2]
        while len(cyc) < 4:
            nxt = [x for x in I if x != prev and A[cur, x] and x not in cyc]
            assert len(nxt) == 1
            cyc.append(nxt[0])
            prev, cur = cur, nxt[0]
        assert A[cyc[-1], cyc[0]]

        V = np.asarray([POINTS[i] for i in cyc], dtype=np.int64).T % P
        assert det_mod3(V) != 0
        S = V @ V.T % P
        X = S @ J % P
        assert det_mod3(X) == 1

        # Direct apartment Gram proof: only opposite products are nonzero.
        a = om(POINTS[cyc[0]], POINTS[cyc[2]])
        b = om(POINTS[cyc[1]], POINTS[cyc[3]])
        assert a in (1, 2) and b in (1, 2)
        G = V.T @ J @ V % P
        assert det_mod3(G) == (a * a * b * b) % P == 1
        diagonal_products.append((a, b))

        # Unique Levi lift: the four adjacent point edges determine four GQ lines.
        edges = [
            tuple(sorted((cyc[t], cyc[(t + 1) % 4])))
            for t in range(4)
        ]
        ls = tuple(line_index[edge_line_set[e]] for e in edges)
        assert len(set(ls)) == 4
        incidences = tuple(
            sorted((cyc[t], ls[t]) for t in range(4))
            + sorted((cyc[(t + 1) % 4], ls[t]) for t in range(4))
        )
        levi_packets.add(incidences)
        apartments.append(tuple(sorted(I)))

    assert len(apartments) == 1620
    assert len(set(apartments)) == 1620
    assert len(levi_packets) == 1620

    diag_profile = {}
    for a, b in diagonal_products:
        diag_profile[f"{a},{b}"] = diag_profile.get(f"{a},{b}", 0) + 1

    out = {
        "schema": "w33.h1_det_apartment_phase_bridge.v1",
        "status": "PASS",
        "headline": (
            "All 1620 induced W33 quadrangles/apartments are projective bases "
            "of F3^4 and therefore have det((VV^T)J)=1. Each lifts uniquely "
            "to one point-line Levi 8-cycle, so the determinant/Tutte phase "
            "candidate is uniform on the complete apartment set."
        ),
        "W33": {
            "points": 40,
            "lines": 40,
            "point_graph_edges": 240,
            "induced_C4_apartments": len(apartments),
            "levi_8cycle_lifts": len(levi_packets),
        },
        "direct_proof": {
            "cyclic_order": "p1-p2-p3-p4-p1",
            "adjacent_pairing": "<p_i,p_{i+1}>=0",
            "opposite_pairings": "a=<p1,p3>, b=<p2,p4> are both nonzero",
            "gram_determinant": "det(V^T J V)=(a b)^2=1 in F3",
            "consequence": "V is a projective basis and det((VV^T)J)=det(V)^2 det(J)=1",
        },
        "opposite_pairing_profile": diag_profile,
        "candidate_phase": {
            "central_character_r1": "omega",
            "central_character_r2": "omega^2",
            "uniform_on_all_apartments": True,
        },
        "relation_to_pass4474": (
            "Uses only induced C4 quadrangles/apartments. The separate 120 "
            "simple C4s lying inside geometric K4 lines are excluded."
        ),
        "boundary": (
            "This is an exact finite bridge between the determinant invariant "
            "and the W33/Levi apartment geometry. It does not show that a VOA "
            "OPE or physical controller implements the apartment phase."
        ),
        "checks": {
            "W33_SRG_degree12": True,
            "40_GQ_lines": True,
            "1620_induced_apartments": True,
            "every_apartment_projective_basis": True,
            "every_apartment_det1": True,
            "unique_Levi_8cycle_lift": True,
        },
    }
    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    main(True)
