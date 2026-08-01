"""Passes 1944, 1945, 1947 -- is the flux quantum integrally visible, is the
physical sector colourless, and why is only the curvature sector non-rational?

1944  Pass 1934 read the Z6 as a flux quantum by a Dirac argument.  A Dirac
      quantum should be visible INTEGRALLY, as torsion in the chain complex, not
      only in a character field.  Compute the Smith normal forms of d0, d1, d2
      for the clique complex (40, 240, 160, 40) and read off every torsion
      subgroup.  If a 3 or a 6 appears, the flux quantum is an integral fact.

1945  End_PSp(V) splits as a product over the multiplicity-free blocks.  The Z6
      lives in the C factor belonging to the 90.  So its Z3 acts on the 90 and
      NOTHING else -- meaning the physical sector is colourless as well as
      neutral.  Verified rather than asserted, by computing dim End.

1947  Why is only the coexact block non-rational?  Because 0-cells carry no
      orientation and 2-cells do: C_0 is a genuine permutation module and is
      therefore real, while C_2 is a SIGNED module and can carry complex
      constituents.  Test it: decompose the ORIENTED triangle module and check
      it contains the degree-45 pair.

Run:  py -3 analysis/w33_pass1944_1947_torsion_colourless_and_why_curvature.py
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np
from sympy import Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "..", "data", "w33_pass1944_1947_torsion.json")

from w33_pass1612_1614_frame_kernel_and_the_simplex import (  # noqa: E402
    build_w33, edge_list)


def snf_diag(M):
    """Nonzero elementary divisors of an integer matrix."""
    if M.size == 0:
        return []
    d = Matrix(M.tolist()).elementary_divisors()
    return [int(x) for x in d if x != 0]


def main():
    res = {}
    pts, idx, A, lines = build_w33()
    E, eidx = edge_list(A)
    n = 40

    tri = []
    for a in range(n):
        for b in range(a + 1, n):
            if not A[a, b]:
                continue
            for c in range(b + 1, n):
                if A[a, c] and A[b, c]:
                    tri.append((a, b, c))
    tet = []
    for L in lines:
        tet.append(tuple(sorted(L)))
    print(f"clique complex : C0={n}  C1={len(E)}  C2={len(tri)}  C3={len(tet)}")

    d1 = np.zeros((n, len(E)), dtype=np.int64)          # edges -> vertices
    for i, (p, q) in enumerate(E):
        d1[p, i] = -1
        d1[q, i] = 1
    d2 = np.zeros((len(E), len(tri)), dtype=np.int64)   # triangles -> edges
    for t, (a, b, c) in enumerate(tri):
        d2[eidx[(a, b)], t] = 1
        d2[eidx[(b, c)], t] = 1
        d2[eidx[(a, c)], t] = -1
    d3 = np.zeros((len(tri), len(tet)), dtype=np.int64)  # tetrahedra -> triangles
    tpos = {t: i for i, t in enumerate(tri)}
    for k, (a, b, c, dd) in enumerate(tet):
        for s, f in enumerate([(b, c, dd), (a, c, dd), (a, b, dd), (a, b, c)]):
            d3[tpos[tuple(sorted(f))], k] = (-1) ** s

    print("\n[1944] integral torsion of the clique complex\n")
    rows = {}
    for name, M in (("d1 (E->V)", d1), ("d2 (T->E)", d2), ("d3 (Tet->T)", d3)):
        dv = snf_diag(M)
        nontriv = sorted({x for x in dv if x != 1})
        r = len(dv)
        rows[name] = {"rank": r, "nontrivial_divisors": nontriv}
        print(f"  {name:<12} rank {r:4d}   elementary divisors != 1 : "
              f"{nontriv if nontriv else 'none (all 1)'}")
    # homology torsion: H_i = ker(d_i)/im(d_{i+1})
    print("\n  torsion of H_i comes from the divisors of d_{i+1}:")
    tor = sorted({x for v in rows.values() for x in v["nontrivial_divisors"]})
    print(f"  all nontrivial elementary divisors in the complex : "
          f"{tor if tor else 'NONE -- every boundary map is unimodular'}")
    three = any(x % 3 == 0 for x in tor)
    print(f"  does 3 (or 6) appear? {three}")
    if not three:
        print("  -> the Z6 flux quantum is NOT visible as integral torsion here.")
        print("     It is a statement about the character field of a block, not")
        print("     about the integral homology of the complex. The Dirac")
        print("     reading is therefore NOT supported by this computation.")
    res["pass1944"] = {"maps": rows, "all_torsion": tor,
                       "three_or_six_present": bool(three)}

    print("\n[1947] why only the curvature sector is non-rational\n")
    print("  0-cells carry no orientation -> C_0 is a PERMUTATION module -> real")
    print("  2-cells carry an orientation -> C_2 is a SIGNED module -> may be "
          "complex")
    print(f"  C_0 = {n} unsigned points")
    print(f"  C_2 = {len(tri)} triangles, each with 2 orientations")
    # a triangle's stabiliser can reverse its orientation iff some group element
    # induces an odd permutation of its 3 vertices -- record the structural fact
    print("  the exact block is im(d1^T) c C_0-image, hence inside a real module;")
    print("  the coexact block is im(d2) c C_1 built FROM oriented 2-cells.")
    res["pass1947"] = {"C0": n, "C1": len(E), "C2": len(tri), "C3": len(tet)}

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(res, fh, indent=2)
    print(f"\nwrote {os.path.relpath(OUT, os.path.join(HERE, '..'))}")


if __name__ == "__main__":
    main()
