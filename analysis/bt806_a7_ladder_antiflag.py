#!/usr/bin/env python3
"""
BT806 - The A7 ladder: the Csaszar census is the F21-orbit structure of
        PG(3,2), and the two Steiner systems are an ANTI-FLAG.

GAP witness (gap_a7_pg32.g / gap_f21_pg32.g, recorded in JSON):
  * A7 < GL(4,2) = A8 is TRANSITIVE on the 15 points, 35 lines, and 15
    planes of PG(3,2) (both conjugacy classes), with line stabilizer of
    order 72 = |triple stabilizer in A7| - so the classical equivariant
    bijection {triples of 7} <-> {lines of PG(3,2)} exists.
  * N_GL(4,2)(P7) = F21 = C7:C3 (the multiplier C3 = QR set {1,2,4}).

PYTHON VERIFICATION (explicit matrices, no GAP needed):
  Build P7 = <Singer(F8) + fixed line> and F21 = <P7, Frobenius> inside
  GL(4,2) and compute all orbit structures:

    points:  [1, 7, 7]      vacuum point + two heptads
    lines:   [7, 7, 21]     STAR + PLANE + generic
    planes:  [1, 7, 7]      polar plane + two 7-orbits

  THE ANTI-FLAG THEOREM: the two 7-line orbits are
    (a) the 7 lines through the fixed point p0 (the STAR), and
    (b) the 7 lines inside the fixed plane pi0 (a Fano PG(2,2)),
  with p0 NOT on pi0 - a non-incident (point, plane) pair, the anti-flag.
  Under the A7 bijection these are the two Z7-invariant Steiner triple
  systems = the Csaszar faces (BT804/805).  Hence:

    Csaszar faces (14) = star(p0) u lines(pi0)   [the anti-flag]
    Csaszar edges (21) = the generic line orbit

  and the (e,f) = (21,14) census of the torus is literally the F21-orbit
  partition of PG(3,2)'s lines.  The point census 15 = 1 + 7 + 7 is the
  q=2 vacuum decomposition (the W(3,3) analogue is 40 = 1 + 12 + 27).
"""
from __future__ import annotations

from collections import Counter
from itertools import combinations
import json


def mat_mul(A, B):
    n = len(A)
    return tuple(tuple(
        (sum(A[i][k] & B[k][j] for k in range(n)) & 1)
        for j in range(n)) for i in range(n))


def mat_vec(A, v):
    n = len(A)
    return tuple((sum(A[i][k] & v[k] for k in range(n)) & 1)
                 for i in range(n))


def main():
    # Singer cycle on F8 = F2[a]/(a^3+a+1), companion matrix of x^3+x+1,
    # extended by a fixed 1-dim summand.
    C = ((0, 0, 1), (1, 0, 1), (0, 1, 0))   # multiplication by a
    # Frobenius x -> x^2 on basis {1, a, a^2}: 1->1, a->a^2, a^2->a^2+a
    F = ((1, 0, 0), (0, 0, 1), (0, 1, 1))

    def extend(M3):
        return tuple(tuple(list(row) + [0]) for row in M3) + ((0, 0, 0, 1),)

    g = extend(C)
    f = extend(F)

    # orders
    def order(M):
        I = tuple(tuple(1 if i == j else 0 for j in range(4))
                  for i in range(4))
        k, X = 1, M
        while X != I:
            X = mat_mul(X, M)
            k += 1
        return k

    assert order(g) == 7 and order(f) == 3
    # f normalizes <g>: f g f^-1 = g^2
    f2 = mat_mul(f, f)
    finv = mat_mul(f2, f2 @ () if False else f2)  # f^3 = I so f^-1 = f^2
    finv = f2
    conj = mat_mul(mat_mul(f, g), finv)
    g2 = mat_mul(g, g)
    assert conj == g2
    print("T1 P7 = <Singer>, F21 = <Singer, Frobenius>: f g f^-1 = g^2  OK")

    # group elements of F21
    elems = set()
    frontier = [tuple(tuple(1 if i == j else 0 for j in range(4))
                      for i in range(4))]
    elems.add(frontier[0])
    while frontier:
        nxt = []
        for X in frontier:
            for Y in (g, f):
                Z = mat_mul(X, Y)
                if Z not in elems:
                    elems.add(Z)
                    nxt.append(Z)
        frontier = nxt
    assert len(elems) == 21
    print(f"T1 |F21| = {len(elems)}  OK")

    pts = [v for v in
           [tuple(int(b) for b in format(i, '04b')) for i in range(1, 16)]]

    def orbits(objs, act):
        rem = set(objs)
        sizes = []
        reps = []
        while rem:
            x = next(iter(rem))
            orb = {x}
            frontier = [x]
            while frontier:
                nxt = []
                for y in frontier:
                    for M in (g, f):
                        z = act(M, y)
                        if z not in orb:
                            orb.add(z)
                            nxt.append(z)
                frontier = nxt
            sizes.append(len(orb))
            reps.append((x, orb))
            rem -= orb
        return sorted(sizes), reps

    psizes, preps = orbits(pts, mat_vec)
    print(f"T2 point orbits: {psizes}  (vacuum + two heptads)")
    assert psizes == [1, 7, 7]
    p0 = next(x for x, orb in preps if len(orb) == 1)
    print(f"T2 vacuum point p0 = {p0}")

    def xor(a, b):
        return tuple(x ^ y for x, y in zip(a, b))

    lines = set()
    for a, b in combinations(pts, 2):
        lines.add(frozenset((a, b, xor(a, b))))
    assert len(lines) == 35

    def act_line(M, L):
        return frozenset(mat_vec(M, v) for v in L)

    lsizes, lreps = orbits(lines, act_line)
    print(f"T3 line orbits: {lsizes}  (the Csaszar census 7+7+21!)")
    assert lsizes == [7, 7, 21]

    planes = set()
    for fvec in pts:
        pl = frozenset(v for v in pts
                       if sum(x & y for x, y in zip(v, fvec)) % 2 == 0)
        planes.add(pl)
    assert len(planes) == 15

    def act_plane(M, P):
        return frozenset(mat_vec(M, v) for v in P)

    plsizes, plreps = orbits(planes, act_plane)
    print(f"T4 plane orbits: {plsizes}")
    assert plsizes == [1, 7, 7]
    pi0 = next(x for x, orb in plreps if len(orb) == 1)
    print(f"T4 fixed plane pi0 = 7 points, p0 on pi0: {p0 in pi0}")
    assert p0 not in pi0   # ANTI-FLAG

    # identify the two 7-line orbits
    star = {L for L in lines if p0 in L}
    inplane = {L for L in lines if L <= pi0}
    assert len(star) == 7 and len(inplane) == 7
    for x, orb in lreps:
        if len(orb) == 7:
            which = "STAR(p0)" if orb == star else (
                "LINES(pi0)" if orb == inplane else "???")
            print(f"T5 7-line orbit identified: {which}")
            assert which != "???"
    print("T5 ANTI-FLAG THEOREM: the two 7-orbits are the star of the")
    print("   vacuum point and the line set of the polar Fano plane;")
    print("   p0 not on pi0.  Csaszar faces = star + plane (anti-flag),")
    print("   Csaszar edges = the 21 generic lines.")

    out = {
        "theorem": "BT806 A7 ladder + anti-flag",
        "gap_witness": {
            "A7_transitive": {"points": 15, "lines": 35, "planes": 15},
            "A7_line_stabilizer": 72,
            "normalizer": "C7:C3 order 21",
        },
        "f21_orbits": {
            "points": psizes, "lines": lsizes, "planes": plsizes,
        },
        "antiflag": True,
        "csaszar_dictionary": {
            "faces_14": "star(p0) u lines(pi0)",
            "edges_21": "generic line orbit",
            "vertices_7": "heptad point orbit",
        },
        "vacuum_decomposition_q2": "15 = 1 + 7 + 7 (cf. q=3: 40 = 1+12+27)",
    }
    with open("data/bt806_a7_ladder_antiflag.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt806_a7_ladder_antiflag.json")


if __name__ == "__main__":
    main()
