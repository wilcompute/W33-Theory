#!/usr/bin/env python3
"""
BT871 - Where the Z3 actually lives: an honest correction to the
        "Berry phase = topological invariant" reading.

W33_FOR_EVERYONE.tex claims a particle crossing a triangle picks up a
Z3 Berry phase 2pi/3; four triangles meet at each vertex
(4.(2pi/3) = 2pi/3 since 4 = 1 mod 3), global 40.(2pi/3) = 2pi/3
(40 = 1 mod 3) -- read there as "a global Z3 topological invariant,
the structural origin of the Z3 centre of SU(3)".

Tested rigorously, the cohomological reading is REFUTED and corrected:

  T1  (confirmed) every vertex lies on exactly 4 lines; its 12
      neighbours partition into 4 disjoint triangles (q+1 lines,
      lambda=2).
  T2  (homology, confirmed) over F3: H0 = 1, H1 = 81 (Steinberg),
      H2 = 40.
  T2' (REFUTATION) the uniform Berry 2-cochain omega (value 1 on every
      triangle) is a COBOUNDARY: it pairs to 0 with every
      tetrahedron-boundary 2-cycle (the alternating face sum
      1-1+1-1 = 0), and delta^1 f = omega is solvable over F3.  So
      [omega] = 0 in H^2(;F3): the uniform Berry phase is exact, NOT a
      topological obstruction.  The per-vertex "4 = 1 mod 3" and
      global "40 = 1 mod 3" are genuine arithmetic but they are
      Euler/vertex-count data mod 3, not an H^2 class.
  T3  (correct placement) the physical Z3 - generation and the SU(3)
      centre - is the ORDER-3 GROUP ACTION on the Steinberg register
      H1 (BT863: chi_St vanishes on 3-singular classes, forcing the
      27+27+27 split), not a Berry 2-cocycle.  The Z3 is a
      representation-theoretic eigengrading, which is why it is exact
      as a cochain yet physically real as a symmetry.
"""
from __future__ import annotations

from collections import Counter
from itertools import combinations, product
import json

import numpy as np


def canon(v):
    for x in v:
        if x % 3:
            c = 1 if x % 3 == 1 else 2
            return tuple((c * y) % 3 for y in v)
    raise ValueError


def rank_mod3(rows):
    A = [list(map(lambda z: z % 3, r)) for r in rows]
    if not A:
        return 0
    nr, nc = len(A), len(A[0])
    r = 0
    for c in range(nc):
        piv = next((i for i in range(r, nr) if A[i][c] % 3), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        inv = 1 if A[r][c] % 3 == 1 else 2
        A[r] = [(inv*x) % 3 for x in A[r]]
        for i in range(nr):
            if i != r and A[i][c] % 3:
                f = A[i][c]
                A[i] = [(A[i][j]-f*A[r][j]) % 3 for j in range(nc)]
        r += 1
        if r == nr:
            break
    return r


def main():
    pts = sorted({canon(v) for v in product(range(3), repeat=4) if any(v)})
    n = 40
    pt_index = {p: i for i, p in enumerate(pts)}

    def symp(x, y):
        return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3

    adj = [[False]*n for _ in range(n)]
    for i, j in combinations(range(n), 2):
        if symp(pts[i], pts[j]) == 0:
            adj[i][j] = adj[j][i] = True
    lines = [frozenset(q) for q in combinations(range(n), 4)
             if all(adj[i][j] for i, j in combinations(q, 2))]
    assert len(lines) == 40

    # T1: each vertex on exactly 4 lines; neighbours = 4 triangles
    lines_through = [[l for l in lines if i in l] for i in range(n)]
    assert all(len(lt) == 4 for lt in lines_through)
    for i in range(n):
        nbrs = set()
        for l in lines_through[i]:
            tri = l - {i}
            assert len(tri) == 3
            assert all(adj[a][b] for a, b in combinations(tri, 2))
            nbrs |= tri
        assert len(nbrs) == 12   # 4 disjoint triangles partition the 12
    print("T1 every vertex on exactly 4 lines; 12 neighbours = "
          "4 disjoint triangles (q+1 lines, lambda=2)")

    edges = sorted({tuple(sorted((i, j))) for i, j in
                    combinations(range(n), 2) if adj[i][j]})
    eidx = {e: i for i, e in enumerate(edges)}
    tris = sorted({tuple(sorted(t)) for l in lines
                   for t in combinations(sorted(l), 3)})
    assert len(edges) == 240 and len(tris) == 160

    # boundary d1: C2(tris) -> C1(edges)
    d1 = [[0]*160 for _ in range(240)]
    for j, (x, y, z) in enumerate(tris):
        d1[eidx[(y, z)]][j] = 1
        d1[eidx[(x, z)]][j] = -1 % 3
        d1[eidx[(x, y)]][j] = 1
    # d0: C1 -> C0
    d0 = [[0]*240 for _ in range(40)]
    for i, (a, b) in enumerate(edges):
        d0[b][i] = 1
        d0[a][i] = -1 % 3

    r0 = rank_mod3(d0)
    r1 = rank_mod3([[d1[e][t] for e in range(240)] for t in range(160)])
    H0 = 40 - r0
    H1 = (240 - r0) - r1
    H2 = 160 - r1
    print(f"T2 over F3: H0 = {H0}, H1 = {H1} (Steinberg), H2 = {H2}")
    assert (H0, H1, H2) == (1, 81, 40)

    # Berry cochain omega = all-ones on triangles; [omega] in H2 nonzero
    # iff omega is NOT a coboundary, i.e. omega . z != 0 for some
    # 2-cycle z in ker(d1).  Equivalent: pair omega with each line's
    # tetrahedron-boundary 2-cycle.
    # tetra boundary cycle of a line: the 4 triangles with signs that
    # make d1 . z = 0.
    def tetra_cycle(l):
        v4 = sorted(l)
        z = [0]*160
        # standard 3-simplex boundary signs: face opposite vertex k has
        # sign (-1)^k
        for k in range(4):
            face = tuple(x for idx, x in enumerate(v4) if idx != k)
            z[tris.index(face)] = ((-1)**k) % 3
        return z

    # verify these are cycles and pair with omega
    omega = [1]*160
    pairings = Counter()
    cycles = []
    for l in lines:
        z = tetra_cycle(l)
        # check d1 . z == 0 mod 3
        for e in range(240):
            s = sum(d1[e][t]*z[t] for t in range(160)) % 3
            assert s == 0
        cycles.append(z)
        pairings[sum(omega[t]*z[t] for t in range(160)) % 3] += 1
    print(f"T2' omega paired with the 40 tetrahedron 2-cycles: "
          f"{dict(pairings)}")
    nonzero = any(k != 0 for k in pairings)
    # independent confirmation: solve delta^1 f = omega over F3 (rank test)
    d1T = [[d1[e][t] for e in range(240)] for t in range(160)]
    base_rank = rank_mod3(d1T)
    aug_rank = rank_mod3([row + [omega[t]] for t, row in enumerate(d1T)])
    exact = (base_rank == aug_rank)
    print(f"T2' delta^1 f = omega solvable over F3 (omega exact): {exact} "
          f"(rank {base_rank} -> {aug_rank})")
    print(f"T2' => [omega] = 0 in H^2(;F3): the uniform Berry phase is a "
          f"COBOUNDARY, not a topological invariant (claim corrected)")
    assert not nonzero and exact

    # per-vertex and global holonomy mod 3 -- genuine, but Euler-data
    per_vertex = 4 % 3
    glob = 40 % 3
    print(f"T3 per-vertex 4 mod 3 = {per_vertex}, global 40 mod 3 = {glob}:")
    print("   real arithmetic, but a vertex/Euler-count mod 3 statement,")
    print("   not an H^2 class.  The physical Z3 (generation = SU(3)")
    print("   centre) is the ORDER-3 ACTION on Steinberg H1 (BT863):")
    print("   a representation eigengrading - exact as a cochain, real")
    print("   as a symmetry.")
    assert per_vertex == 1 and glob == 1

    out = {
        "theorem": "BT871 where the Z3 lives (Berry-phase correction)",
        "F3_betti": [H0, H1, H2],
        "omega_pairings": {str(k): v for k, v in pairings.items()},
        "uniform_berry_cochain_exact": bool(exact),
        "berry_class_nonzero": bool(nonzero),
        "per_vertex_mod3": per_vertex, "global_mod3": glob,
        "correction": "uniform Berry phase is a coboundary; the physical "
                      "Z3 is the order-3 action on Steinberg H1 (BT863)",
    }
    with open("data/bt871_berry_phase_qcd_center.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt871_berry_phase_qcd_center.json")


if __name__ == "__main__":
    main()
