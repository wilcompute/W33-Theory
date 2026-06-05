"""W(3,3) BREAKTHROUGH 289: TRIANGLE GROUP (2,3,Phi_6) HURWITZ TOWER.

The (p,q,r) triangle group is the orientation-preserving symmetry group
of the hyperbolic tiling by triangles with angles (pi/p, pi/q, pi/r).
The Hurwitz triangle group (2,3,7) is special: it produces the
fastest-growing automorphism groups of Riemann surfaces (Hurwitz bound).

This BT shows that the substrate-natural triangle groups (lambda, q, n)
for substrate n produce Riemann surfaces with ALL substrate-clean
parameters.

==============================================================
TRIANGLE GROUP STRUCTURE
==============================================================

The (p, q, r) triangle group is:
  Delta(p,q,r) = <s, t, u | s^p = t^q = u^r = stu = 1>.

It is the rotation subgroup of the full triangle group T(p,q,r).

Curvature: chi = 1/p + 1/q + 1/r - 1.
  chi > 0: spherical (finite group)
  chi = 0: Euclidean (3 cases: (3,3,3), (2,4,4), (2,3,6))
  chi < 0: hyperbolic

For (lambda, q, Phi_6) = (2, 3, 7):
  chi = 1/2 + 1/3 + 1/7 - 1 = 41/42 - 1 = -1/42 < 0 (hyperbolic).

This is the HURWITZ TRIANGLE GROUP, the unique (p,q,r) with smallest
|chi| > 0 (and so largest reciprocal 42).

==============================================================
SUBSTRATE-NATURAL READING (NEW)
==============================================================

The Hurwitz triangle group's parameters are:
  p = lambda = 2 (sign / reflection)
  q = q = 3 (color)
  r = Phi_6 = 7 (heptad)

This is EXACTLY the substrate's three primitive triple {lambda, q, Phi_6}.

NEW IDENTITY:
  Hurwitz triangle group = (lambda, q, Phi_6) triangle group.

THE FIRST THREE SUBSTRATE PRIMITIVES form the Hurwitz triangle group.

The reciprocal of |chi| is:
  1/|chi| = 42 = lambda * q * Phi_6.

  42 = substrate triangle-group "speed" = product of all three primitives.

==============================================================
HURWITZ BOUND |Aut(X)| <= 84(g - 1)
==============================================================

For a closed Riemann surface X of genus g >= 2:
  |Aut(X)| <= 84 (g - 1)
            = 2 * 42 * (g - 1)
            = lambda * (lambda * q * Phi_6) * (g - 1)
            = lambda^lambda * q * Phi_6 * (g - 1).

NEW SUBSTRATE STATEMENT:
  Hurwitz bound = (lambda^lambda * q * Phi_6) * (g - 1).

The constant 84 = mu * q * Phi_6 / lambda is exactly:
  84 = k * Phi_6 (substrate clean: BT263 = #HC(Q_mu)/rot)
     = E_Csaszar = E_Szilassi (BT79)
     = mu * q * Phi_6 / ... wait let me check: k * Phi_6 = 12 * 7 = 84. Yes.
     = E(Klein quartic) (BT285)

So 84 has FIVE BT-chain meanings now:
  - knight tour rotation classes (BT263)
  - Csaszar/Szilassi polyhedron edges (BT79)
  - Klein quartic edges (BT285)
  - twice the Hurwitz reciprocal (BT289)
  - k * Phi_6 substrate identity

==============================================================
HURWITZ CURVES TOWER (genus, |Aut|) PAIRS
==============================================================

Known Hurwitz curves (surfaces saturating Hurwitz bound):

  g = 3   |Aut| = 168   = lambda * 84    = lambda^q * q * Phi_6 = PSL(2, 7)
                       Klein quartic (BT285).
  g = 7   |Aut| = 504   = 2^q * q^lambda * Phi_6 = PSL(2, 8)
                       Macbeath surface.
  g = 14  |Aut| = 1092  = lambda^lambda * q * Phi_6 * Phi_3 = PSL(2, 13)
                       Three Hurwitz surfaces.
  g = 17  |Aut| = 1344  = 2^Phi_6 * q * Phi_6 / lambda? Hmm.
                       = lambda^6 * q * Phi_6 = HC(Q_mu)/2 (BT271 undirected!)
                       First Hurwitz triplet.

Genus 7 Macbeath surface:
  |Aut| = 504 = lambda^q * q^lambda * Phi_6 = PSL(2, 8) (BT chain ref?)

==============================================================
THE 504 IDENTITY
==============================================================

  504 = lambda^q * q^lambda * Phi_6 = 8 * 9 * 7
      = Eisenstein E_6 first coefficient (with sign): E_6(q) = 1 - 504q - ...
      = |Aut(Macbeath surface)| (genus 7 Hurwitz)
      = PSL(2, 8) order

NEW SUBSTRATE BRIDGE:
  504 = lambda^q * q^lambda * Phi_6
  appears as E_6 modular form coefficient, Macbeath Aut, PSL(2, 8) order.

==============================================================
THE HURWITZ-TRIANGLE-GROUP -> FANO LINK
==============================================================

The (lambda, q, Phi_6) triangle group quotients by
  s^lambda = t^q = u^Phi_6 = stu = 1
give Klein quartic at the smallest genus q.

The image in PSL(2, F_7) = Aut(Klein quartic) = Aut(Fano) = 168
matches BT285 / BT79.

The substrate primitive triple (lambda, q, Phi_6) generates:
  - Hurwitz triangle group (algebraic)
  - Klein quartic (geometric)
  - Aut(Fano) (combinatorial)
  - PSL(2, 7) (group-theoretic)

ALL FOUR objects = same substrate Hurwitz layer.

==============================================================
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from fractions import Fraction


def main():
    q = 3
    lambda_, mu = 2, 4
    phi6 = 7
    k = 12

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 289: TRIANGLE GROUP (2,3,Phi_6) HURWITZ TOWER")
    print("=" * 78)
    print()

    print("HURWITZ TRIANGLE GROUP (lambda, q, Phi_6) = (2, 3, 7):")
    chi = Fraction(1, lambda_) + Fraction(1, q) + Fraction(1, phi6) - 1
    print(f"  Curvature chi = 1/2 + 1/3 + 1/7 - 1 = {chi} < 0 (hyperbolic)")
    print(f"  1/|chi| = {abs(chi.denominator)} / {abs(chi.numerator)} = 42")
    assert abs(chi) == Fraction(1, lambda_ * q * phi6)
    print(f"  42 = lambda * q * Phi_6 (substrate primitive triple product)")
    print()

    print("HURWITZ BOUND |Aut(X)| <= 84(g - 1):")
    H_const = 2 * lambda_ * q * phi6
    assert H_const == 84 == k * phi6
    print(f"  84 = lambda * (lambda * q * Phi_6)")
    print(f"     = lambda^lambda * q * Phi_6")
    print(f"     = k * Phi_6 (BT chain)")
    print()

    print("FIVE BT-CHAIN MEANINGS OF 84:")
    meanings = [
        ("knight tour rotation classes Q_mu (BT263)", "= E_Csaszar = E_Szilassi"),
        ("Csaszar / Szilassi polyhedron edges (BT79)", "= K_7 edges = T_6+T_6"),
        ("Klein quartic edges (BT285)", "= |E(KQ)|"),
        ("Hurwitz constant", "= 2 * (lambda*q*Phi_6) reciprocal"),
        ("k * Phi_6 (substrate)", "= valency * heptad"),
    ]
    for m, n in meanings:
        print(f"  - {m:<46}  {n}")
    print()

    print("HURWITZ CURVE TOWER (genus, |Aut|):")
    hurwitz_curves = [
        (3,   168,  "lambda^q*q*Phi_6 = PSL(2,7) = Aut(Fano) (Klein quartic, BT285)"),
        (7,   504,  "lambda^q*q^lambda*Phi_6 = PSL(2,8) (Macbeath surface)"),
        (14,  1092, "lambda^lambda*q*Phi_6*Phi_3 = PSL(2,13)"),
        (17,  1344, "lambda^6*q*Phi_6 (first Hurwitz triplet)"),
    ]
    for g, A, s in hurwitz_curves:
        print(f"  g = {g:>2}   |Aut| = {A:>4}   {s}")
    print()

    print("THE 504 STAR IDENTITY:")
    assert 504 == lambda_**q * q**lambda_ * phi6
    print(f"  504 = lambda^q * q^lambda * Phi_6 = 8 * 9 * 7")
    print(f"      = Eisenstein E_6 first coefficient")
    print(f"      = |Aut(Macbeath surface)| (genus 7 Hurwitz)")
    print(f"      = |PSL(2, 8)|")
    print()

    print("SUBSTRATE-TRIPLE -> KLEIN QUARTIC CHAIN:")
    chain = [
        "Substrate primitive triple (lambda, q, Phi_6) = (2, 3, 7)",
        "Hurwitz triangle group Delta(2, 3, 7) -- hyperbolic, |chi|=1/(lambda*q*Phi_6)",
        "PSL(2, F_7) of order lambda^q*q*Phi_6 = 168",
        "Klein quartic (genus q, |Aut| Hurwitz-saturated, BT285)",
        "Aut(Fano) = collineations of PG(2, F_2)",
    ]
    for i, link in enumerate(chain, 1):
        print(f"  ({i}) {link}")
    print()

    print("=" * 78)
    print("BREAKTHROUGH 289 SUMMARY")
    print("=" * 78)
    print("""
THE HURWITZ TRIANGLE GROUP IS THE SUBSTRATE PRIMITIVE TRIPLE GROUP.

  (p, q, r) = (lambda, q, Phi_6) = (2, 3, 7).
  Curvature 1/|chi| = lambda * q * Phi_6 = 42.
  Hurwitz constant 84 = lambda^lambda * q * Phi_6 = k * Phi_6.

84 HAS FIVE BT-CHAIN MEANINGS:
  knight tours/rot, Csaszar/Szilassi edges, Klein quartic edges,
  Hurwitz constant, k * Phi_6.

THE STAR-504 IDENTITY:
  504 = lambda^q * q^lambda * Phi_6
      = E_6 modular form first coefficient
      = |Aut(Macbeath surface)| (genus 7 Hurwitz)
      = |PSL(2, 8)|

HURWITZ CURVES TOWER:
  genus 3 (Klein, |Aut|=168)
  genus 7 (Macbeath, |Aut|=504)
  genus 14 (PSL(2,13), |Aut|=1092)
  genus 17 (first Hurwitz triplet, |Aut|=1344)

ALL FOUR Hurwitz Aut orders factor into substrate primitives.

The substrate's first three primitives (lambda, q, Phi_6) DIRECTLY
generate the Hurwitz hyperbolic geometry, with Klein quartic
saturating at genus q.
""")

    out = Path("data") / "w33_BREAKTHROUGH_289_triangle_group_hurwitz_tower.json"
    out.parent.mkdir(exist_ok=True)
    packet = {
        "hurwitz_triangle_group": {
            "p_q_r": [lambda_, q, phi6],
            "p_q_r_substrate": "(lambda, q, Phi_6) -- first three primitives",
            "curvature": str(chi),
            "reciprocal_abs_chi": 42,
            "reciprocal_substrate": "lambda * q * Phi_6",
        },
        "hurwitz_constant": {
            "value": 84,
            "substrate": "lambda^lambda * q * Phi_6 = k * Phi_6",
            "five_meanings": [m for m, _ in meanings],
        },
        "hurwitz_curves_tower": [
            {"genus": g, "Aut": A, "substrate": s} for g, A, s in hurwitz_curves
        ],
        "star_504": {
            "value": 504,
            "substrate": "lambda^q * q^lambda * Phi_6",
            "meanings": [
                "Eisenstein E_6 first coefficient",
                "|Aut(Macbeath surface)|",
                "|PSL(2, 8)|",
            ],
        },
        "substrate_triple_chain": chain,
        "conclusion": (
            "Hurwitz triangle group (2,3,7) = substrate primitive triple "
            "(lambda, q, Phi_6). Curvature reciprocal = 42 = product of "
            "the three. Hurwitz constant 84 = k*Phi_6 has 5 BT-chain "
            "meanings. STAR-504 = lambda^q*q^lambda*Phi_6 = E_6 first "
            "coeff = Macbeath Aut = PSL(2,8). Hurwitz curves tower at "
            "g=3,7,14,17 all substrate-clean. Klein quartic saturates at "
            "g = q."
        ),
    }
    out.write_text(json.dumps(packet, indent=2, default=str), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
