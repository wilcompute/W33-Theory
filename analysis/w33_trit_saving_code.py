#!/usr/bin/env python3
"""
Trit-saving IS the code: every closed triangle saves a trit (a CSS Z-check), and the
trits NO triangle can save are the H1 = 81 logical qutrits of the [[240,81,4]]_3
Steinberg code. Closing a loop and encoding a qutrit are the same act.

The Klee-Irwin trit-saving picture (w33_genus_ladder_clock.py): closing the third
edge of a triangle fixes one q=3 trit. On W(3,3) the simplicial chain complex over
F3 is
    C0 (40 vertices)  <--d1--  C1 (240 edges)  <--d2--  C2 (160 triangles),
with d1 d2 = 0. A triangle that closes is a 2-cell whose boundary is a saved
trit -- exactly a weight-3 CSS Z-stabilizer (the trichromatic Yukawa face). The
vertex coboundary gives the X-stabilizers. The logical qutrits are the 1-cycles
that NO triangle bounds:
    H1 = ker(d1)/im(d2),   dim H1 = (240 - rank d1) - rank d2 = (240-39) - 120 = 81.
So H1 = 81 = q^4 is the trits that cannot be saved by closing any triangle -- the
protected logical register of the [[240,81,4]]_3 code (check ranks 39 and 120,
distance d_Z = 4 = mu). Trit-saving (triangle closure) = the CSS checks; the
unsaved trits = the logical information. Geometry = code.

Verifies d1 d2 = 0, rank d1 = 39, rank d2 = 120, and H1 = 81 over F3.
"""
from __future__ import annotations

import itertools
import json

F = 3


def sform(u, v):
    return (u[0] * v[2] - u[2] * v[0] + u[1] * v[3] - u[3] * v[1]) % F


def projective_points():
    pts, seen = [], set()
    for vec in itertools.product(range(F), repeat=4):
        if vec == (0, 0, 0, 0):
            continue
        for i in range(4):
            if vec[i] != 0:
                inv = pow(vec[i], F - 2, F)
                rep = tuple((inv * x) % F for x in vec)
                break
        if rep not in seen:
            seen.add(rep)
            pts.append(rep)
    return pts


def rank_mod3(M):
    M = [row[:] for row in M]
    rows, cols = len(M), len(M[0]) if M else 0
    r = 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if M[i][c] % F), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = pow(M[r][c], F - 2, F)
        M[r] = [(x * inv) % F for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c] % F:
                fac = M[i][c]
                M[i] = [(a - fac * b) % F for a, b in zip(M[i], M[r])]
        r += 1
    return r


def main():
    out = {}
    pts = projective_points()
    n = len(pts)
    idx = {p: i for i, p in enumerate(pts)}
    # edges (collinear pairs) and triangles (mutually collinear triples)
    edges = [
        (i, j)
        for i, j in itertools.combinations(range(n), 2)
        if sform(pts[i], pts[j]) == 0
    ]
    eidx = {e: m for m, e in enumerate(edges)}
    adj = {i: set() for i in range(n)}
    for i, j in edges:
        adj[i].add(j)
        adj[j].add(i)
    tris = [
        t
        for t in itertools.combinations(range(n), 3)
        if t[1] in adj[t[0]] and t[2] in adj[t[0]] and t[2] in adj[t[1]]
    ]
    print(
        f"[chain complex over F3]  C0={n} vertices, C1={len(edges)} edges, "
        f"C2={len(tris)} triangles"
    )
    assert n == 40 and len(edges) == 240 and len(tris) == 160

    # d1: edges -> vertices (40 x 240) ; d2: triangles -> edges (240 x 160)
    d1 = [[0] * len(edges) for _ in range(n)]
    for m, (i, j) in enumerate(edges):
        d1[i][m] = 1
        d1[j][m] = F - 1  # -1
    d2 = [[0] * len(tris) for _ in range(len(edges))]
    for t, (a, b, c) in enumerate(tris):
        for (x, y), sgn in [((a, b), 1), ((a, c), F - 1), ((b, c), 1)]:
            e = (x, y) if (x, y) in eidx else (y, x)
            d2[eidx[e]][t] = sgn

    # d1 d2 = 0
    prod = [
        [
            sum(d1[i][m] * d2[m][t] for m in range(len(edges))) % F
            for t in range(len(tris))
        ]
        for i in range(n)
    ]
    d1d2_zero = all(all(x == 0 for x in row) for row in prod)
    print(f"  d1 d2 = 0 (dd=0): {d1d2_zero}")
    assert d1d2_zero

    r1 = rank_mod3(d1)
    r2 = rank_mod3([[d2[m][t] for t in range(len(tris))] for m in range(len(edges))])
    H1 = (len(edges) - r1) - r2
    print(
        f"\n[ranks / homology]  rank d1 = {r1} (vertex/X-checks), "
        f"rank d2 = {r2} (triangle/Z-checks)"
    )
    print(f"  H1 = (240 - {r1}) - {r2} = {H1} = q^4 = the logical register")
    assert r1 == 39 and r2 == 120 and H1 == 81
    out["rank_d1"] = r1
    out["rank_d2"] = r2
    out["H1"] = H1

    print(f"\n[trit-saving = CSS code]")
    print(
        f"  each closed triangle (160 of them) SAVES a trit = a weight-3 Z-stabilizer"
    )
    print(f"  (rank {r2}); the vertex coboundary gives the X-stabilizers (rank {r1});")
    print(f"  the trits NO triangle can save = H1 = 81 = the logical qutrits of the")
    print(f"  [[240,81,4]]_3 Steinberg code (distance d_Z = 4 = mu).")
    out["code"] = "[[240,81,4]]_3"

    print("\nRESULT: trit-saving and error correction are the same geometry. On the")
    print("  W(3,3) chain complex (40 vertices, 240 edges, 160 triangles, dd=0), each")
    print("  triangle that closes saves one q=3 trit -- a weight-3 CSS Z-check (the")
    print("  trichromatic Yukawa face); the vertices give the X-checks. The 1-cycles")
    print("  that no triangle bounds are H1 = 81 = q^4, the protected logical register")
    print("  of the [[240,81,4]]_3 code. So closing a loop (Klee-Irwin trit-saving)")
    print("  and encoding a logical qutrit are one and the same act: the triangulation")
    print(
        "  IS the code, and the 81 unsaved trits are the matter the machine protects."
    )

    out["summary"] = (
        "trit-saving = the code: W(3,3) chain complex (40,240,160), "
        "dd=0; closing a triangle saves a trit = weight-3 CSS Z-check "
        "(rank 120), vertices = X-checks (rank 39); H1 = (240-39)-120 = "
        "81 = q^4 = the trits no triangle saves = the logical register "
        "of [[240,81,4]]_3 (d_Z=4=mu). Closing a loop = encoding a "
        "qutrit; the triangulation IS the code."
    )
    out["sources"] = [
        "Klee-Irwin trit-saving / cycle clock; W(3,3) clique complex "
        "CSS code [[240,81,4]]_3 (check ranks 39,120); simplicial "
        "homology over F3; w33_genus_ladder_clock.py"
    ]
    with open("data/w33_trit_saving_code.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_trit_saving_code.json")


if __name__ == "__main__":
    main()
