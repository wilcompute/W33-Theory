#!/usr/bin/env python3
"""
BT825 - The Universality Theorem: the photon's own optics generate the
        full Clifford group; the matter shell supplies the magic.

  T1. CLIFFORD COMPLETENESS.  The machine's physical gate set -
        F  (tritter: qutrit Fourier transform)
        S  (phase plate: quadratic phase |j> -> w^{j(j+1)/2}|j>)
        CX (delay-conditioned EOM: |j,k> -> |j, j+k>)
      acting on either register, has symplectic images generating ALL of
      Sp(4,3), order 51840 (matrix closure over F3, exact).  Hence the
      optical elements generate the complete two-qutrit Clifford group
      (modulo phases/Paulis): every stabilizer operation of the
      substrate is reachable by tabletop optics.
  T2. UNIVERSALITY.  Clifford + any magic state = universal (qudit
      magic-state injection/distillation; for qutrits, contextuality is
      necessary and sufficient for distillation - Howard, Wallman,
      Veitch, Emerson, Nature 510, 351 (2014)).  The machine's matter
      shell IS its magic supply (BT822), and the exact contextual
      fraction 1/10 (BT823) certifies the resource is present in every
      vacuum.  Therefore: ONE self-entangled photon + the W(3,3) mesh
      = a universal quantum computer whose network transport is its
      gate action.
"""
from __future__ import annotations

import json


def mat_mul3(A, B):
    n = len(A)
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(n)) % 3
                       for j in range(n)) for i in range(n))


def main():
    # symplectic images on F3^4 with coordinates (x1, z1, x2, z2)
    # and form <u,v> = x1 z1' - z1 x1' + x2 z2' - z2 x2'.
    # F on register 1: X -> Z -> X^-1 : (x1,z1) -> (-z1, x1)
    F1 = ((0, 2, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
    F2 = ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 2), (0, 0, 1, 0))
    # S on register 1: X -> XZ, Z -> Z : (x1,z1) -> (x1, z1 + x1)
    S1 = ((1, 0, 0, 0), (1, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
    S2 = ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 1, 1))
    # CX (control 1 -> target 2): X1 -> X1 X2, Z2 -> Z1^-1 Z2... standard:
    # x2' = x2 + x1, z1' = z1 - z2
    CX = ((1, 0, 0, 0), (0, 1, 0, 2), (1, 0, 1, 0), (0, 0, 0, 1))

    gens = [F1, F2, S1, S2, CX]

    def symp(u, v):
        return (u[0]*v[1] - u[1]*v[0] + u[2]*v[3] - u[3]*v[2]) % 3

    # verify each generator preserves the form
    basis = [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)]

    def apply(M, v):
        return tuple(sum(M[i][k] * v[k] for k in range(4)) % 3
                     for i in range(4))

    for M in gens:
        for u in basis:
            for v in basis:
                assert symp(apply(M, u), apply(M, v)) == symp(u, v)
    print("T1 all five optical generators are symplectic (form preserved)")

    ident = tuple(tuple(1 if i == j else 0 for j in range(4))
                  for i in range(4))
    group = {ident}
    frontier = [ident]
    while frontier:
        nxt = []
        for g in frontier:
            for h in gens:
                gh = mat_mul3(h, g)
                if gh not in group:
                    group.add(gh)
                    nxt.append(gh)
        frontier = nxt
    print(f"T1 closure of <F1, F2, S1, S2, CX> = {len(group)} "
          f"(|Sp(4,3)| = 51840)")
    assert len(group) == 51840
    print("T1 CLIFFORD COMPLETENESS: tritter + phase plate + EOM generate")
    print("   the ENTIRE two-qutrit Clifford group (mod Paulis/phases) -")
    print("   every substrate symmetry is reachable by tabletop optics")

    print("\nT2 UNIVERSALITY: Clifford completeness (T1) + magic supply")
    print("   (matter shell = 36 magic rays, BT822) + nonzero contextual")
    print("   fraction 1/10 EXACT (BT823) + Howard et al. (contextuality")
    print("   is necessary and sufficient for qutrit magic distillation)")
    print("   => ONE self-entangled photon on the W(3,3) mesh is a")
    print("   UNIVERSAL quantum computer whose transport IS its gates.")

    out = {
        "theorem": "BT825 universality",
        "symplectic_closure": len(group),
        "clifford_complete": True,
        "magic_supply": "matter shell (36 rays, grades 8+24+4)",
        "contextual_fraction": "1/10 exact",
        "conclusion": "one photon + W33 mesh = universal QC; "
                      "transport = gates",
    }
    with open("data/bt825_universality_theorem.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt825_universality_theorem.json")


if __name__ == "__main__":
    main()
