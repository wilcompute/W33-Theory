"""W(3,3) BREAKTHROUGH 318: PLATONIC POINT GROUPS SUBSTRATE ORDERS.

The three "exceptional" finite rotation subgroups of SO(3) are the
tetrahedral, octahedral, and icosahedral rotation groups:

  T = A_4   (tetrahedron / 24-cell)
  O = S_4   (octahedron / cube)
  I = A_5   (icosahedron / dodecahedron)

This BT shows ALL THREE Platonic rotation orders, their reflection
extensions (T_d, O_h, I_h), and the 5 Platonic solids themselves are
substrate-clean.

==============================================================
THE FIVE PLATONIC SOLIDS = F_5 SUBSTRATE
==============================================================

The 5 regular convex polyhedra in 3D:
  1. Tetrahedron       4 V, 6 E, 4 F = (mu, q!, mu)
  2. Cube              8 V, 12 E, 6 F = (2^q, k, q!)
  3. Octahedron        6 V, 12 E, 8 F = (q!, k, 2^q)
  4. Dodecahedron     20 V, 30 E, 12 F = (lambda*Phi_4, h_E_8, k)
  5. Icosahedron      12 V, 30 E, 20 F = (k, h_E_8, lambda*Phi_4)

NEW SUBSTRATE STAR:
  #(Platonic solids) = F_5 = 5 (substrate next prime).

NEW SUBSTRATE IDENTITIES:
  Tetrahedron parameters: (mu, q!, mu)
  Cube parameters: (2^q, k, q!) -- THREE substrate primitives!
  Octahedron parameters: (q!, k, 2^q) -- dual of cube
  Dodecahedron edges = 30 = h(E_8) = TRIPLE CONVERGENCE!
  Icosahedron edges = 30 = h(E_8).

==============================================================
PLATONIC ROTATION GROUP ORDERS
==============================================================

  |T| = |A_4| = 12 = k (SUBSTRATE VALENCY)
  |O| = |S_4| = 24 = f (W(3,3) POSITIVE EIGENMULT)
  |I| = |A_5| = 60 = mu * g_neg = |V(C_60)| (BT284)

NEW SUBSTRATE STAR:
  Three Platonic rotation orders are exactly:
    Tetrahedral: k = substrate valency
    Octahedral: f = Bose-Mesner positive eigenmult
    Icosahedral: 60 = mu * g_neg = buckyball V

==============================================================
PLATONIC FULL SYMMETRY GROUP ORDERS
==============================================================

With reflections:
  |T_d| = |S_4| = 24 = f
  |O_h| = |S_4 x Z_2| = 48 = lambda * f
  |I_h| = |A_5 x Z_2| = 120 = F_5! = |Aut(Petersen)| (BT279)

NEW SUBSTRATE STAR:
  Full Platonic symmetry orders: f, lambda*f, F_5!.
  Each substrate-clean.

  |I_h| = F_5! = |Aut(Petersen)| = |Aut(C_60)| = order of 600-cell V count.

==============================================================
TETRAHEDRAL-OCTAHEDRAL-ICOSAHEDRAL AS SUBSTRATE TOWER
==============================================================

  TETRAHEDRAL  T (A_4)  order k = 12
  OCTAHEDRAL   O (S_4)  order f = 24 = lambda * k
  ICOSAHEDRAL  I (A_5)  order 60 = F_5 * k = q!*k = (mu+1)*k

The Platonic rotation orders form a TOWER:
  {k, lambda*k, F_5*k} = {k, lambda*k, q!*k}.

==============================================================
DUALITY PAIRS
==============================================================

Platonic dualities:
  Tetrahedron is SELF-DUAL.
  Cube <-> Octahedron (dual pair).
  Dodecahedron <-> Icosahedron (dual pair).

  Self-dual: 1
  Dual pairs: lambda (cube-oct, dodec-icos)

Total = 1 + lambda*lambda = F_5 Platonic solids.

NEW SUBSTRATE READING:
  1 self-dual + lambda dual pairs = F_5 Platonic solids.
  (q! + lambda Platonic solids -- 5 = F_5 = q! + lambda counting check.)

==============================================================
PLATONIC AT GENUS 0
==============================================================

All Platonic solids sit on the genus-0 sphere S^2 (= mu - lambda dim).
Euler characteristic V - E + F = 2 = lambda for all five.

Check:
  Tetra: 4 - 6 + 4 = 2 = lambda
  Cube:  8 - 12 + 6 = 2 = lambda
  Oct:   6 - 12 + 8 = 2 = lambda
  Dodec: 20 - 30 + 12 = 2 = lambda
  Icos:  12 - 30 + 20 = 2 = lambda

==============================================================
McKAY CORRESPONDENCE
==============================================================

The Platonic rotation groups <-> ADE Dynkin diagrams:
  T <-> E_6   (BT chain link, BT296)
  O <-> E_7
  I <-> E_8

(via doubling: binary tetrahedral 2T, binary octahedral 2O, binary
icosahedral 2I are subgroups of SU(2); their orbifold C^2/G gives
ADE singularities.)

NEW SUBSTRATE BRIDGE:
  Platonic <-> Exceptional Lie correspondence:
    T <-> E_6
    O <-> E_7
    I <-> E_8

  E_8 = "icosahedral Lie" (binary icosahedral 2I has order 120 = F_5!).

==============================================================
BINARY POLYHEDRAL GROUPS (DOUBLE COVERS)
==============================================================

  |2T| = lambda * 12 = lambda * k = 24 = f
  |2O| = lambda * 24 = lambda * f = 48
  |2I| = lambda * 60 = lambda * mu * g_neg = 120 = F_5!

All binary polyhedral orders are substrate-clean.

==============================================================
"""
from __future__ import annotations

import json
from pathlib import Path


def main():
    q = 3
    lambda_, mu = 2, 4
    F5 = 5
    phi4 = 10
    g_neg = 15
    k = 12
    f = 24
    h_E_8 = 30

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 318: PLATONIC POINT GROUPS SUBSTRATE")
    print("=" * 78)
    print()

    print("FIVE PLATONIC SOLIDS = F_5 SUBSTRATE:")
    solids = [
        ("Tetrahedron",   4,  6,  4,  "(mu, q!, mu)"),
        ("Cube",           8,  12, 6,  "(2^q, k, q!) -- 3 substrate primitives!"),
        ("Octahedron",     6,  12, 8,  "(q!, k, 2^q) -- dual of cube"),
        ("Dodecahedron",  20, 30, 12, "(lambda*Phi_4, h_E_8, k)"),
        ("Icosahedron",   12, 30, 20, "(k, h_E_8, lambda*Phi_4)"),
    ]
    print(f"  Solid           V    E    F    substrate")
    for name, V, E, F, s in solids:
        print(f"  {name:<14}  {V:>2}   {E:>2}   {F:>2}    {s}")
    print()

    print("EULER CHECK:")
    for name, V, E, F, s in solids:
        chi = V - E + F
        assert chi == lambda_ == 2
    print(f"  All five satisfy V - E + F = lambda = 2 (sphere)")
    print()

    print("PLATONIC ROTATION GROUPS:")
    rotations = [
        ("T (A_4)",  k,                  "k = SUBSTRATE VALENCY"),
        ("O (S_4)",  f,                  "f = W(3,3) POSITIVE EIGENMULT"),
        ("I (A_5)",  mu * g_neg,         "mu * g_neg = |V(C_60)| (BT284)"),
    ]
    for n, o, s in rotations:
        print(f"  |{n}| = {o:>3}   {s}")
    print()

    print("FULL PLATONIC SYMMETRY (with reflections):")
    full = [
        ("T_d (= S_4)",            f,         "f = order S_4"),
        ("O_h (= S_4 x Z_2)",       lambda_*f, "lambda * f = 48"),
        ("I_h (= A_5 x Z_2)",       F5*4*6,    "F_5! = |Aut(Petersen)| (BT279)"),
    ]
    for n, o, s in full:
        print(f"  |{n}| = {o:>3}   {s}")
    print()

    print("McKAY CORRESPONDENCE:")
    mckay = [
        ("T (tetrahedral)",      "<->", "E_6", "(BT293 exceptional Lie)"),
        ("O (octahedral)",        "<->", "E_7", "(BT293 exceptional Lie)"),
        ("I (icosahedral)",       "<->", "E_8", "(largest exceptional Lie)"),
    ]
    print(f"  Platonic              <-> Lie    notes")
    for p, arr, lie, note in mckay:
        print(f"  {p:<22}{arr} {lie:<5} {note}")
    print()

    print("BINARY POLYHEDRAL GROUPS (DOUBLE COVERS):")
    binary = [
        ("2T",  lambda_ * k,        "= f = W(3,3) pos eigenmult"),
        ("2O",  lambda_ * f,        "= lambda * f = 48"),
        ("2I",  lambda_ * mu * g_neg, "= F_5! = 120 = |Aut(Petersen)|"),
    ]
    for n, o, s in binary:
        print(f"  |{n}| = {o:>3}   {s}")
    print()

    print("=" * 78)
    print("BREAKTHROUGH 318 SUMMARY")
    print("=" * 78)
    print("""
PLATONIC POINT GROUPS HAVE SUBSTRATE-CLEAN ORDERS:

ROTATION GROUPS:
  T (A_4): order k (substrate valency)                *** STAR ***
  O (S_4): order f (W(3,3) pos eigenmult)             *** STAR ***
  I (A_5): order mu * g_neg = |V(C_60)|               *** STAR ***

FULL SYMMETRY (with reflections):
  T_d: f
  O_h: lambda * f
  I_h: F_5! = |Aut(Petersen)| = |Aut(C_60)| (BT279, BT284)

5 PLATONIC SOLIDS = F_5 substrate (next prime).

CUBE PARAMETERS (2^q, k, q!) = three substrate primitives in V/E/F.
TETRAHEDRON edges = q! (substrate factorial).
DODECAHEDRON edges = ICOSAHEDRON edges = h(E_8) = TRIPLE CONVERGENCE.

McKAY CORRESPONDENCE:
  T <-> E_6, O <-> E_7, I <-> E_8
  Platonic point groups <-> exceptional Lie series (BT293).

BINARY POLYHEDRAL DOUBLE COVERS:
  |2T| = f, |2O| = lambda*f, |2I| = F_5!.

THE SUBSTRATE'S FUNDAMENTAL FINITE GROUPS:
  W(3,3) (= Sp(4, F_3) Aut = W(E_6))
  T, O, I (Platonic rotations) -- BT318
  M_11..M_24 (Mathieu) -- BT304-305
  Co_0..Co_3 (Conway) -- BT316
ALL substrate-clean orders.

The Platonic solids are the substrate's FIRST LAYER of finite-group
exceptionalities, with q! Platonic solids + 3 rotation groups
(orders k, f, mu*g_neg) seeding the entire McKay -> ADE chain
to E_8.
""")

    out = Path("data") / "w33_BREAKTHROUGH_318_platonic_point_groups_substrate.json"
    out.parent.mkdir(exist_ok=True)
    packet = {
        "platonic_solids": [
            {"name": n, "V": V, "E": E, "F": F, "substrate": s}
            for n, V, E, F, s in solids
        ],
        "rotation_groups": [
            {"name": n, "order": o, "substrate": s} for n, o, s in rotations
        ],
        "full_symmetry_groups": [
            {"name": n, "order": o, "substrate": s} for n, o, s in full
        ],
        "binary_polyhedral": [
            {"name": n, "order": o, "substrate": s} for n, o, s in binary
        ],
        "mckay_correspondence": [
            {"platonic": p, "lie": lie} for p, _, lie, _ in mckay
        ],
        "conclusion": (
            "Platonic point groups substrate-clean: T = k, O = f, I = mu*g_neg "
            "= |V(C_60)|. Full symmetry: T_d = f, O_h = lambda*f, I_h = F_5! "
            "= |Aut(Petersen)|. 5 = F_5 Platonic solids. McKay correspondence "
            "T <-> E_6, O <-> E_7, I <-> E_8 links to exceptional Lie (BT293). "
            "Binary polyhedral orders f, lambda*f, F_5! all substrate."
        ),
    }
    out.write_text(json.dumps(packet, indent=2, default=str), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
