"""W(3,3) BREAKTHROUGH 306: CATALAN NUMBERS SUBSTRATE TOWER.

The Catalan numbers C_n = C(2n, n) / (n + 1) appear in many enumeration
contexts: balanced parentheses, binary trees, polygon triangulations,
lattice paths.

This BT shows that evaluating C_n at substrate-natural n gives integers
that are BT-chain objects: Hurwitz reciprocal, Witt design block count,
Heawood vertex count.

==============================================================
CATALAN TOWER AT SUBSTRATE n
==============================================================

  C_0 = 1
  C_1 = 1
  C_2 = 2 = lambda
  C_3 = 5 = F_5
  C_4 = 14 = lambda * Phi_6 = |V(Heawood)|       (BT267!)
  C_5 = 42 = lambda * q * Phi_6 = HURWITZ RECIP. (BT289!)
  C_6 = 132 = mu * q * p_Ih = |blocks S(5,6,12)| (BT304!)
  C_7 = 429 = q * Phi_6 * lambda^q + q = q * Phi_6 * 11 - ... actually 429 = 3*11*13 = q * p_Ih * Phi_3 (substrate clean!)
  C_8 = 1430 = lambda * F_5 * 11 * 13 = lambda * F_5 * p_Ih * Phi_3

==============================================================
THE STAR IDENTITIES
==============================================================

(1) C_mu = lambda * Phi_6 = |V(Heawood)| (BT267)
    Catalan at spacetime = Heawood vertex count.

(2) C_F_5 = lambda * q * Phi_6 = HURWITZ RECIPROCAL = 42 (BT289)
    Catalan at next-prime = Hurwitz triangle group constant.

(3) C_q! = mu * q * p_Ih = |blocks of Witt design S(5, 6, 12)| (BT304)
    Catalan at substrate factorial = Witt-12 block count.

(4) C_Phi_6 = q * p_Ih * Phi_3 = 429
    Catalan at heptad = q * p_Ih * Phi_3 (substrate-clean!)

THREE CONSECUTIVE substrate-index Catalan numbers (C_mu, C_F_5, C_q!)
hit three BT-chain objects (Heawood, Hurwitz, Witt-12).

==============================================================
SUBSTRATE CATALAN INDEX MAP
==============================================================

  n       C_n     substrate factorisation       BT chain link
  ----------------------------------------------------------------
  lambda  lambda  trivial
  q       F_5     F_5
  mu      14      lambda * Phi_6                 |V(Heawood)|
  F_5     42      lambda * q * Phi_6              Hurwitz reciprocal
  q!      132     mu * q * p_Ih                   Witt-12 blocks
  Phi_6   429     q * p_Ih * Phi_3                substrate clean

The Catalan sequence "rolls over" the substrate primitives, hitting
substrate-clean integers at every substrate index.

==============================================================
CATALAN AS TRIANGULATION COUNT
==============================================================

C_n = number of triangulations of an (n + 2)-gon by non-crossing diagonals.

  C_mu = triangulations of (mu + 2)-gon = 6-gon = q!-gon
       = lambda * Phi_6 = 14

  C_F_5 = triangulations of (F_5 + 2)-gon = 7-gon = Phi_6-gon
        = lambda * q * Phi_6 = 42

NEW SUBSTRATE READING:
  Catalan-counted triangulations of (F_5+2)-gon (= Phi_6-gon!)
  give the Hurwitz reciprocal 42.

  Triangulations of HEPTAGON = Hurwitz constant.

==============================================================
CATALAN AS BALANCED PARENTHESES
==============================================================

C_n = number of valid balanced parentheses sequences of length 2n.

  C_q = F_5 (5 balanced (...) sequences of length 6)
  C_mu = 14 = |V(Heawood)| (14 sequences of length 8)
  C_F_5 = 42 (42 sequences of length 10)

Each Catalan number at substrate n counts a substrate-clean number of
balanced expressions.

==============================================================
GENERATING FUNCTION
==============================================================

  C(x) = (1 - sqrt(1 - 4x)) / (2x)
  C(x) = sum_(n >= 0) C_n x^n
  C(x) satisfies x * C(x)^2 - C(x) + 1 = 0.

At substrate value x = 1/mu (since 4x = 1):
  C(1/mu) = (1 - 0) / (lambda / mu) = mu / lambda = 2.
  The series diverges; mu = 4 is the convergence boundary.

NEW SUBSTRATE READING:
  Catalan generating function radius of convergence = 1/mu (= 1/4).
  Substrate spacetime IS the Catalan convergence boundary.

==============================================================
"""
from __future__ import annotations

import json
import math
from pathlib import Path


def main():
    q = 3
    lambda_, mu = 2, 4
    F5 = 5
    phi3 = 13
    phi6 = 7
    p_Ih = 11

    def catalan(n):
        return math.comb(2 * n, n) // (n + 1)

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 306: CATALAN NUMBERS SUBSTRATE TOWER")
    print("=" * 78)
    print()

    rows = [
        (lambda_, "lambda", catalan(lambda_), "lambda",                "trivial"),
        (q,        "q",      catalan(q),       "F_5",                   "F_5"),
        (mu,       "mu",     catalan(mu),      "lambda * Phi_6 = 14",   "|V(Heawood)| (BT267)"),
        (F5,       "F_5",    catalan(F5),      "lambda * q * Phi_6",     "HURWITZ RECIPROCAL (BT289)"),
        (6,        "q!",     catalan(6),       "mu * q * p_Ih",         "|blocks S(5,6,12)| (BT304)"),
        (phi6,     "Phi_6",  catalan(phi6),    "q * p_Ih * Phi_3",       "substrate clean"),
    ]

    print("CATALAN TOWER AT SUBSTRATE n:")
    print(f"  n           C_n    substrate factor             BT chain link")
    for n, name, c, sub, link in rows:
        print(f"  {n}({name:<6}) {c:>4}   {sub:<26}   {link}")
    print()

    print("STAR IDENTITIES:")
    assert catalan(mu) == lambda_ * phi6 == 14
    assert catalan(F5) == lambda_ * q * phi6 == 42
    assert catalan(6) == 132 == mu * q * p_Ih
    assert catalan(phi6) == q * p_Ih * phi3 == 429
    print(f"  C_mu = lambda * Phi_6 = 14 = |V(Heawood)| (BT267)")
    print(f"  C_F_5 = lambda * q * Phi_6 = 42 = HURWITZ RECIPROCAL (BT289)")
    print(f"  C_q! = mu * q * p_Ih = 132 = |blocks S(5,6,12)| (BT304)")
    print(f"  C_Phi_6 = q * p_Ih * Phi_3 = 429")
    print()

    print("TRIANGULATION READING (C_n = triangulations of (n+2)-gon):")
    print(f"  C_mu triangulates 6-gon (q!-gon); count = 14")
    print(f"  C_F_5 triangulates 7-gon (Phi_6-gon); count = 42 = Hurwitz reciprocal")
    print(f"  C_q! triangulates 8-gon (2^q-gon); count = 132 = Witt-12 blocks")
    print()

    print("GENERATING-FUNCTION RADIUS OF CONVERGENCE:")
    print(f"  C(x) converges for |x| < 1/mu = 1/4.")
    print(f"  Substrate spacetime mu IS the Catalan-series convergence")
    print(f"  boundary.")
    print()

    print("=" * 78)
    print("BREAKTHROUGH 306 SUMMARY")
    print("=" * 78)
    print("""
CATALAN NUMBERS AT SUBSTRATE INDICES HIT BT-CHAIN OBJECTS:

  C_mu  = 14 = |V(Heawood)|                       (BT267)
  C_F_5 = 42 = Hurwitz triangle reciprocal         (BT289)
  C_q!  = 132 = |blocks of Witt design S(5,6,12)| (BT304)
  C_Phi_6 = 429 = q * p_Ih * Phi_3

The Catalan number sequence "rolls over" the substrate primitives,
landing on substrate-clean BT-chain integers at every substrate index
from C_lambda up through C_Phi_6.

GENERATING FUNCTION RADIUS = 1/mu:
  Catalan series converges for |x| < 1/mu.
  Substrate spacetime = Catalan convergence boundary.

TRIANGULATION COUNTS at substrate-natural polygon sizes are
substrate-clean: 14 triangulations of q!-gon, 42 of Phi_6-gon,
132 of 2^q-gon, 429 of (Phi_6+2)-gon.

This connects:
  - combinatorial enumeration (Catalan numbers, triangulations)
  - Heawood graph (BT267)
  - Hurwitz triangle group (BT289)
  - Witt designs / Mathieu groups (BT304)

into one classical integer sequence at substrate-natural indices.
""")

    out = Path("data") / "w33_BREAKTHROUGH_306_catalan_substrate_tower.json"
    out.parent.mkdir(exist_ok=True)
    packet = {
        "catalan_tower": [
            {"n": n, "name": nm, "C_n": c, "substrate": sub, "link": link}
            for n, nm, c, sub, link in rows
        ],
        "star_identities": [
            "C_mu = lambda * Phi_6 = |V(Heawood)|",
            "C_F_5 = lambda * q * Phi_6 = Hurwitz reciprocal",
            "C_q! = mu * q * p_Ih = |blocks S(5,6,12)|",
            "C_Phi_6 = q * p_Ih * Phi_3 = 429",
        ],
        "generating_function_radius": "1/mu = 1/4",
        "conclusion": (
            "Catalan numbers at substrate-natural indices land on BT-chain "
            "objects: C_mu = |V(Heawood)|, C_F_5 = Hurwitz reciprocal, "
            "C_q! = Witt-12 block count. Catalan series radius of "
            "convergence = 1/mu (substrate spacetime). Triangulations of "
            "substrate-sized polygons give substrate-clean counts."
        ),
    }
    out.write_text(json.dumps(packet, indent=2, default=str), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
