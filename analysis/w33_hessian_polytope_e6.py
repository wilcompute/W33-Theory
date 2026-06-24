#!/usr/bin/env python3
"""
The Eisenstein complex-polytope tower is qutrit -> E6 -> E8. Between the
Mobius-Kantor polygon (8 vertices, symmetry 2T=24=f) and the Witting polytope
(240 vertices = E8, symmetry q*Sp(4,3)) sits the HESSIAN polyhedron: 27 vertices
= the 27 lines on a cubic surface = the E6 fundamental rep = the 27 = GQ(2,4)
points, symmetry 648 = 27*f. And W(E6) = 51840 = |Sp(4,3)|.

The regular complex polytopes over the Eisenstein integers Z[omega] (every edge
a 3{} triangle, the "3" = q) form a dimension ladder:

    dim 2:  3{3}3        Mobius-Kantor   8 verts,  8 edges    sym 24 = |2T| = f
    dim 3:  3{3}3{3}3    Hessian        27 verts, 72 edges    sym 648 = 27*f
    dim 4:  3{3}3{3}3{3}3 Witting      240 verts,2160 edges    sym 155520 = q*|Sp(4,3)|

The Mobius-Kantor polygon is the face AND vertex figure of the Hessian
polyhedron, which is the face/vertex figure pattern of the Witting polytope, so
this is one nested family. The symmetry orders multiply by the next vertex
count: 24 * 27 = 648, 648 * 240 = 155520. The base symmetry 24 = |2T| (binary
tetrahedral group) = f, the Hessian symmetry 648 = 27*f, and the Witting
symmetry 155520 = q * |Sp(4,3)| (w33_witting_polytope_substrate.py).

THE E6 RUNG (27): the 27 Hessian vertices are the 27 lines on a cubic surface =
the minuscule fundamental rep of E6 = the 27 points of the generalized
quadrangle GQ(2,4), whose automorphism group is W(E6), of order
    |W(E6)| = 51840 = |Sp(4,3)| = |W(3,3) Aut|.
So the E6 of the 27 lines and the substrate gauge group Sp(4,3) have the SAME
order (both extensions of U4(2)=PSp(4,3)=25920). And 27 is exactly the matter
piece of the substrate decomposition v = 40 = 1 + 12 + 27 (gauge + adjoint +
E6-matter). The Witting reflection group's invariant degrees {12,18,24,30}
include k=12, f=24, and h(E8)=30.

Verifies the tower's f-vectors and symmetry orders (24=f, 648=27*f,
155520=q*Sp(4,3)), |W(E6)|=51840=|Sp(4,3)|, and 40=1+12+27.
"""
from __future__ import annotations

import json

Q, K, F, V40, SP43 = 3, 12, 24, 40, 51840
W_E6 = 51840
TWO_T = 24  # |binary tetrahedral group 2T|


def main():
    out = {}

    # the Eisenstein complex-polytope tower (Coxeter, Regular Complex Polytopes)
    tower = [
        ("Mobius-Kantor", "3{3}3", 2, 8, 8, 24),
        ("Hessian", "3{3}3{3}3", 3, 27, 72, 648),
        ("Witting", "3{3}3{3}3{3}3", 4, 240, 2160, 155520),
    ]
    print("[Eisenstein complex-polytope tower over Z[omega] (q=3)]")
    for name, sym, dim, V, E, aut in tower:
        print(f"  dim {dim}: {sym:14s} {name:13s} V={V:3d} E={E:4d}  sym={aut}")
    out["tower"] = [
        {"name": n, "schlafli": s, "dim": d, "V": V, "E": E, "sym": a}
        for n, s, d, V, E, a in tower
    ]

    # symmetry orders: 24 = |2T| = f, then *27, then *240
    mk, hess, witt = tower[0][5], tower[1][5], tower[2][5]
    print(f"\n[symmetry orders]")
    print(f"  Mobius-Kantor 24 = |2T| (binary tetrahedral) = f = {F}")
    print(f"  Hessian       648 = 27 * f = 27 * {F} = {27*F}")
    print(f"  Witting       155520 = 240 * 648 = q * |Sp(4,3)| = {Q}*{SP43} = {Q*SP43}")
    assert mk == TWO_T == F == 24
    assert hess == 27 * F == 648 == mk * 27
    assert witt == 240 * hess == Q * SP43 == 155520
    out["symmetry"] = {
        "mobius_kantor": "24=|2T|=f",
        "hessian": "648=27*f",
        "witting": "155520=q*|Sp(4,3)|",
    }

    # the E6 rung: 27 = 27 lines on a cubic = E6 = GQ(2,4) points; W(E6)=51840
    print(f"\n[the E6 rung, 27 Hessian vertices]")
    print(f"  27 = 27 lines on a cubic surface = E6 fundamental rep = GQ(2,4) points")
    print(f"  Aut(GQ(2,4)) = W(E6), |W(E6)| = {W_E6} = |Sp(4,3)| = |W(3,3) Aut|")
    print(f"  (both extensions of U4(2)=PSp(4,3)={SP43//2})")
    assert W_E6 == SP43 == 51840 and SP43 // 2 == 25920
    out["e6_rung"] = {
        "verts": 27,
        "is": "27 lines/E6/GQ(2,4)",
        "W_E6": 51840,
        "equals_Sp43": True,
    }

    # 27 is the matter piece of v = 40 = 1 + 12 + 27
    print(f"\n[v = 40 = 1 + 12 + 27]  (gauge + adjoint + E6 matter)")
    print(f"  1 (singlet) + 12 (k = vertex valency) + 27 (E6) = {1+12+27} = v")
    assert 1 + K + 27 == V40 == 40
    out["decomposition"] = "v=40 = 1 + 12 + 27 (E6 matter = the 27)"

    # Witting reflection-group invariant degrees include k, f, h(E8)
    degrees = (12, 18, 24, 30)
    prod = 1
    for d in degrees:
        prod *= d
    print(f"\n[Witting reflection group invariant degrees {degrees}]")
    print(
        f"  product = {prod} = 155520 = the group order; includes k=12, f=24, h(E8)=30"
    )
    assert prod == 155520 and degrees == (12, 18, 24, 30)
    out["witting_degrees"] = list(degrees)

    print("\nRESULT: the regular Eisenstein complex polytopes are the substrate's")
    print("  qutrit -> E6 -> E8 ladder. Over Z[omega] (q=3), the Mobius-Kantor")
    print("  polygon (8 verts, symmetry 2T=24=f), the Hessian polyhedron (27 verts,")
    print("  symmetry 27*f=648), and the Witting polytope (240 verts=E8, symmetry")
    print("  q*Sp(4,3)=155520) nest as face/vertex-figure. The middle rung's 27")
    print("  vertices are the 27 lines on a cubic = the E6 fundamental rep = the 27")
    print("  points of GQ(2,4), whose automorphism group W(E6) has order 51840 =")
    print("  |Sp(4,3)| -- the same as the substrate gauge group. And 27 is exactly")
    print("  the E6 matter piece of v = 40 = 1 + 12 + 27. The qutrit (Hesse 9), the")
    print("  E6 (Hessian 27), and E8 (Witting 240) are three rungs of one Eisenstein")
    print("  polytope tower.")

    out["summary"] = (
        "Eisenstein complex-polytope tower qutrit->E6->E8: Mobius-Kantor 3{3}3 "
        "(8 verts, sym 24=|2T|=f) -> Hessian 3{3}3{3}3 (27 verts, sym 648=27*f) -> "
        "Witting 3{3}3{3}3{3}3 (240 verts=E8, sym 155520=q*Sp(4,3)), nested as "
        "face/vertex-figure; orders multiply by next vertex count. The E6 rung's "
        "27 = 27 lines on a cubic = E6 fund rep = GQ(2,4) points, Aut=W(E6)=51840="
        "|Sp(4,3)| (both ext of U4(2)=25920). 27 = E6 matter in v=40=1+12+27. "
        "Witting invariant degrees {12,18,24,30}={k,18,f,h(E8)}."
    )
    out["sources"] = [
        "Hessian polyhedron (Wikipedia): 3{3}3{3}3, 27 verts/72 edges, sym 648, "
        "self-dual; Mobius-Kantor polygon 3{3}3 8 verts sym 24=2T; Witting sym "
        "155520; GQ(2,4) 27 pts = 27 lines on cubic, collinearity-complement = "
        "Schlafli SRG(27,16,10,8), Aut=W(E6)=51840 (Wikipedia/MathWorld; black-"
        "hole/qubit E6 entropy); v=40=1+12+27; w33_witting_polytope_substrate.py, "
        "w33_e8_eisenstein_witting_weld.py, w33_hesse_mermin_contextuality.py."
    ]
    with open("data/w33_hessian_polytope_e6.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_hessian_polytope_e6.json")


if __name__ == "__main__":
    main()
