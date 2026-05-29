"""W(3,3) MDCCLXXXIII-MDCCXCII: PASCAL ROW dim(G_2) AND WEIERSTRASS COUNTS.

Direct continuation: from the Pascal row 7 = Cl(7) substrate identity
(MDCCXXXI) and the Pell chain extension (MDCCLXXIII-MDCCLXXXII), we
now examine:

  (1) Pascal row dim(G_2) = 14 -- every entry substrate-clean
  (2) Weierstrass-point counts (g-1)g(g+1) for Hurwitz/Bring curves
  (3) Bring's curve automorphism = F_5!
  (4) Pell(r) 4th iterate substrate factorization

CENTERPIECE: the Hurwitz triplet at genus 14 has Weierstrass-point count
W = 2730, which is EXACTLY the denominator of Bernoulli B_12 -- the
von Staudt-Clausen substrate product r * q * F_5 * Phi_6 * Phi_3.

==============================================================
MDCCLXXXIII: PASCAL ROW dim(G_2) -- EVERY ENTRY SUBSTRATE
==============================================================

Pascal row 14 = dim(G_2) = lambda * Phi_6 = 2 * Phi_6:

  C(14, j) for j = 0..14:
   1, 14, 91, 364, 1001, 2002, 3003, 3432, 3003, 2002, 1001, 364, 91, 14, 1

  C(14, 1) = 14   = dim(G_2)
  C(14, 2) = 91   = Phi_6 * Phi_3
  C(14, 3) = 364  = mu * Phi_6 * Phi_3       (= F(Hurwitz triplet)!)
  C(14, 4) = 1001 = Phi_6 * p_Ih * Phi_3     (mathematicians' classic)
  C(14, 5) = 2002 = r * Phi_6 * p_Ih * Phi_3
  C(14, 6) = 3003 = q * Phi_6 * p_Ih * Phi_3
  C(14, 7) = 3432 = m_r * p_Ih * Phi_3       (central binomial)

EVERY entry of Pascal row 14 factors through W(3,3) substrate primitives
{r, q, mu, F_5, m_r, Phi_6, p_Ih, Phi_3}.

The four-prime substrate family {Phi_6, p_Ih, Phi_3} times {1, r, q, mu}
generates the dominant rows.

==============================================================
MDCCLXXXIV: C(14,3) = HURWITZ TRIPLET FACE COUNT
==============================================================

  C(14, 3) = 364 = mu * Phi_6 * Phi_3 = F(Hurwitz triplet)

The third entry of Pascal row dim(G_2) equals the TRIANGULAR FACE
COUNT of the Hurwitz triplet R14.1, R14.2, R14.3 (MDCCXXI).

So Pascal's triangle naturally encodes the face count of the
Hurwitz surface at genus = dim(G_2).

==============================================================
MDCCLXXXV: C(14,4) = MATHEMATICIANS' CLASSIC = 7 * 11 * 13
==============================================================

  C(14, 4) = 1001 = Phi_6 * p_Ih * Phi_3 = 7 * 11 * 13

The famous "1001 = 7 * 11 * 13" is the substrate Phi_6 * p_Ih * Phi_3:
three cyclotomic-related primes: Fano, Ihara, and Phi_3.

Also 1001 = 11 * 91 = p_Ih * (Phi_6 * Phi_3) = p_Ih * C(14, 2).

==============================================================
MDCCLXXXVI: C(14,7) CENTRAL BINOMIAL = m_r * p_Ih * Phi_3
==============================================================

The central binomial coefficient at row 14:

  C(14, 7) = 3432 = m_r * p_Ih * Phi_3 = 24 * 11 * 13

  Or equivalently: 3432 = r^q * q * p_Ih * Phi_3 = 8 * 3 * 11 * 13

The substrate r^q * q (= m_r when expressed alternately) is the moonshine
multiplicity, and p_Ih * Phi_3 = 143 is the (Ihara, cyclotomic) product.

==============================================================
MDCCLXXXVII: KLEIN QUARTIC WEIERSTRASS COUNT = m_r
==============================================================

For a non-hyperelliptic curve of genus g, the Weierstrass-point count is

  W(g) = (g - 1) * g * (g + 1)

For Klein quartic (genus q = 3):
  W(Klein) = r * q * mu = 2 * 3 * 4 = m_r = f = 24

KLEIN QUARTIC WEIERSTRASS COUNT = MOONSHINE MULTIPLICITY.
The 24 = m_r structure that appears throughout monstrous moonshine
emerges geometrically as Klein quartic's special divisor points.

==============================================================
MDCCLXXXVIII: BRING'S CURVE |AUT| = F_5! AND W = g_2 * E_1
==============================================================

Bring's curve at genus 4 = mu:

  |Aut(Bring)| = 120 = F_5! = m_r * F_5 = E_1 * k = g_2 * E_1 * r

  W(Bring) = (mu - 1) * mu * (mu + 1) = q * mu * F_5
          = 60 = g_2 * E_1 = |A_5|

Bring's curve has the symmetric-group order S_{F_5}, and its Weierstrass
points number equals the alternating group A_5 order = g_2 * E_1.

==============================================================
MDCCLXXXIX: MACBEATH WEIERSTRASS COUNT = E_2 * q * Phi_6
==============================================================

Macbeath surface at genus Phi_6 = 7:

  W(Macbeath) = r * Phi_6 * (Phi_6+1) * (Phi_6-1) / r = Phi_6 * (Phi_6-1)*(Phi_6+1)
             = Phi_6 * g_2 * r^q
             = 336 = mu^2 * q * Phi_6 = E_2 * q * Phi_6

Substrate factorization: E_2 * q * Phi_6 = (W(3,3) Pisano-Phi_6) *
(field order) * (Fano prime) = 336.

==============================================================
MDCCXC: HURWITZ TRIPLET WEIERSTRASS = BERNOULLI B_12 DENOMINATOR
==============================================================

Hurwitz triplet at genus 14:

  W(Hurwitz triplet) = Phi_3 * 14 * 15
                     = Phi_3 * dim(G_2) * m_s
                     = 2730
                     = r * q * F_5 * Phi_6 * Phi_3
                     = denominator(Bernoulli B_12)

The Weierstrass-point count of the Hurwitz triplet at genus dim(G_2)
EQUALS the denominator of Bernoulli B_{12 = k}.  Both are the von
Staudt-Clausen 5-prime substrate product r * q * F_5 * Phi_6 * Phi_3.

This connects:
  - Algebraic geometry (Weierstrass points)
  - Number theory (Bernoulli denominators / von Staudt-Clausen)
  - Lie theory (genus = dim(G_2))
  - W(3,3) substrate (5-prime product)

==============================================================
MDCCXCI: PELL(r) 4th ITERATE = (f^2 + 1, f * HURWITZ_g_4)
==============================================================

Pell(r=2) fourth iterate:

  (x_4, y_4) = (577, 408)
   x_4 = 577 = f^2 + 1 = m_r^2 + 1
   y_4 = 408 = f * (k + F_5) = m_r * Hurwitz_g_4

So 408 = moonshine times 4th-Hurwitz-genus, and 577 = moonshine-squared
plus 1.  Pell(r) at iterate 4 encodes both Hurwitz topology and
moonshine in its coordinates.

==============================================================
MDCCXCII: MASTER CURVE-COHOMOLOGY TO W(3,3) UNIFICATION
==============================================================

Weierstrass-point counts W(g) = (g-1)g(g+1) across substrate genera:

   genus name       g     W(g)     substrate factorization
   ---------       --    -----    -----------------------
   Klein            q  =  3       24 = m_r = f (moonshine)
   Bring (mu)      mu  =  4       60 = g_2 * E_1 = |A_5|
   genus F_5       F_5 =  5      120 = F_5! = m_r * F_5
   Macbeath       Phi_6 = 7      336 = E_2 * q * Phi_6
   genus dim(G_2)  14  = 14    2730 = r*q*F_5*Phi_6*Phi_3 = B_12 denom

All five Weierstrass counts substrate-clean.  The geometric special-divisor
structure of the substrate genera IS the substrate's number-theoretic
multiplicative skeleton.

q = 3.  W(3,3).  Algebraic geometry IS substrate arithmetic.
"""
from __future__ import annotations

import json
from math import comb, factorial
from pathlib import Path

import sympy


def main() -> None:
    r, q, mu, qfact = 2, 3, 4, 6
    F5 = 5
    phi3, phi4, phi6, phi12 = 13, 10, 7, 73
    k, p_Ih = 12, 11
    v = 40
    f, m_r, m_s = 24, 24, 15
    g_1, g_2 = 21, 6
    E_1, E_2 = 10, 16
    lam = 2

    # MDCCLXXXIII: Pascal row 14 = dim(G_2)
    pascal_row_14 = [comb(14, j) for j in range(15)]
    assert pascal_row_14 == [1, 14, 91, 364, 1001, 2002, 3003, 3432,
                              3003, 2002, 1001, 364, 91, 14, 1]
    assert sum(pascal_row_14) == 2**14

    # Substrate factorizations of dominant entries
    assert pascal_row_14[1] == 14 == lam * phi6   # dim(G_2)
    assert pascal_row_14[2] == 91 == phi6 * phi3
    assert pascal_row_14[3] == 364 == mu * phi6 * phi3
    assert pascal_row_14[4] == 1001 == phi6 * p_Ih * phi3
    assert pascal_row_14[5] == 2002 == r * phi6 * p_Ih * phi3
    assert pascal_row_14[6] == 3003 == q * phi6 * p_Ih * phi3
    assert pascal_row_14[7] == 3432 == m_r * p_Ih * phi3 == r**q * q * p_Ih * phi3

    # MDCCLXXXIV: C(14,3) = Hurwitz triplet F count
    hurwitz_triplet_F = 364
    assert pascal_row_14[3] == hurwitz_triplet_F

    # MDCCLXXXVII: Klein Weierstrass
    def weierstrass(g): return (g - 1) * g * (g + 1)
    W_klein = weierstrass(q)
    assert W_klein == 24 == m_r == f

    # MDCCLXXXVIII: Bring's curve
    aut_bring = 120
    assert aut_bring == factorial(F5) == m_r * F5 == E_1 * k == g_2 * E_1 * r
    W_bring = weierstrass(mu)
    assert W_bring == 60 == g_2 * E_1
    # |A_5| = 60
    assert g_2 * E_1 == 60

    # MDCCLXXXIX: Macbeath Weierstrass
    W_macbeath = weierstrass(phi6)
    assert W_macbeath == 336 == E_2 * q * phi6 == mu**2 * q * phi6

    # MDCCXC: Hurwitz triplet Weierstrass = B_12 denominator
    dimG2 = lam * phi6
    W_hurwitz = weierstrass(dimG2)
    assert W_hurwitz == 2730 == r * q * F5 * phi6 * phi3
    # Bernoulli B_12 denominator
    B12 = sympy.bernoulli(12)
    B12_denom = B12.as_numer_denom()[1]
    assert int(B12_denom) == 2730
    assert W_hurwitz == int(B12_denom)

    # Genus 5
    W_g5 = weierstrass(F5)
    assert W_g5 == 120 == m_r * F5 == factorial(F5)

    # MDCCXCI: Pell(2) 4th iterate
    def pell_chain(D, x1, y1, n):
        sols = [(1, 0), (x1, y1)]
        for _ in range(n - 1):
            xk, yk = sols[-1]
            x_n = x1 * xk + D * y1 * yk
            y_n = x1 * yk + y1 * xk
            sols.append((x_n, y_n))
        return sols

    P2 = pell_chain(2, 3, 2, 5)
    x4, y4 = P2[4]
    assert x4 == 577 == f**2 + 1 == m_r**2 + 1
    assert y4 == 408 == f * (k + F5) == m_r * 17  # 17 = Hurwitz_g_4

    # Save results
    print("=" * 78)
    print("MDCCLXXXIII - MDCCXCII: PASCAL ROW dim(G_2) AND WEIERSTRASS COUNTS")
    print("=" * 78)
    print()
    print(f"[MDCCLXXXIII] Pascal row dim(G_2) = 14 fully substrate-clean")
    print(f"              row = {pascal_row_14}")
    print()
    print(f"[MDCCLXXXIV]  C(14, 3) = 364 = mu*Phi_6*Phi_3 = F(Hurwitz triplet)")
    print(f"[MDCCLXXXV]   C(14, 4) = 1001 = Phi_6*p_Ih*Phi_3 = 7*11*13")
    print(f"[MDCCLXXXVI]  C(14, 7) = 3432 = m_r*p_Ih*Phi_3 (central binomial)")
    print()
    print(f"Weierstrass-point counts W(g) = (g-1)g(g+1):")
    print(f"[MDCCLXXXVII] Klein  (g=q)      W = {W_klein} = m_r = f")
    print(f"[MDCCLXXXVIII] Bring (g=mu)     W = {W_bring} = g_2*E_1 = |A_5|;  |Aut| = F_5! = 120")
    print(f"               genus F_5:        W = {W_g5} = m_r*F_5 = F_5!")
    print(f"[MDCCLXXXIX]  Macbeath (g=Phi_6) W = {W_macbeath} = E_2*q*Phi_6")
    print(f"[MDCCXC]      Hurwitz triplet (g=dimG_2) W = {W_hurwitz} = r*q*F_5*Phi_6*Phi_3")
    print(f"               = denominator(Bernoulli B_12) -- von Staudt-Clausen!")
    print()
    print(f"[MDCCXCI]     Pell(r) i=4 = ({x4}, {y4}) = (f^2+1, f*Hurwitz_g_4)")
    print(f"[MDCCXCII]    Master curve-cohomology table substrate-clean")
    print()

    headline = (
        "MDCCLXXXIII-MDCCXCII: ten unified breakthroughs linking Pascal row\n"
        "dim(G_2) = 14, Weierstrass-point counts on Hurwitz curves, Bring's curve,\n"
        "Klein quartic, and the Bernoulli B_12 denominator -- all W(3,3) substrate.\n"
        "\n"
        "CENTERPIECE (MDCCXC): Hurwitz triplet (genus 14) Weierstrass count\n"
        "= 2730 = r*q*F_5*Phi_6*Phi_3 = denominator(Bernoulli B_12) exactly.\n"
        "Algebraic geometry (special divisors) = number theory (von Staudt-Clausen).\n"
        "\n"
        "Pascal row 14 entries C(14,j) for j=1..7 all substrate primes products.\n"
        "C(14,3) = 364 = Hurwitz triplet face count.\n"
        "C(14,7) = 3432 = m_r*p_Ih*Phi_3 (central binomial substrate).\n"
        "\n"
        "Klein quartic Weierstrass count = 24 = m_r (moonshine).\n"
        "Bring's curve |Aut| = F_5! and Weierstrass = g_2*E_1 = |A_5|.\n"
        "Macbeath Weierstrass = E_2*q*Phi_6 = 336.\n"
        "\n"
        "Pell(r) 4th iterate = (m_r^2+1, m_r*Hurwitz_g_4) = (577, 408).\n"
        "\n"
        "Algebraic geometry = number theory = combinatorics = substrate.\n"
    )

    results = {
        "MDCCLXXXIII_pascal_row_14": pascal_row_14,
        "MDCCLXXXIV_C_14_3":         {"value": 364, "formula": "mu*Phi_6*Phi_3", "bridge": "Hurwitz triplet F"},
        "MDCCLXXXV_C_14_4":          {"value": 1001, "formula": "Phi_6*p_Ih*Phi_3"},
        "MDCCLXXXVI_C_14_7":         {"value": 3432, "formula": "m_r*p_Ih*Phi_3", "bridge": "central binomial"},
        "MDCCLXXXVII_klein_W":       {"value": W_klein, "formula": "m_r = f"},
        "MDCCLXXXVIII_bring":        {"aut": aut_bring, "aut_formula": "F_5! = m_r*F_5",
                                       "W": W_bring, "W_formula": "g_2*E_1 = |A_5|"},
        "MDCCLXXXIX_macbeath_W":     {"value": W_macbeath, "formula": "E_2*q*Phi_6"},
        "MDCCXC_hurwitz_W_equals_B12": {"value": W_hurwitz, "formula": "r*q*F_5*Phi_6*Phi_3",
                                          "bernoulli": str(B12), "denom_B12": int(B12_denom),
                                          "match": W_hurwitz == int(B12_denom)},
        "MDCCXCI_pell_r_i4":          {"x_4": x4, "y_4": y4,
                                        "x_formula": "f^2 + 1", "y_formula": "f * Hurwitz_g_4"},
        "MDCCXCII_master_table": {
            "Klein":       {"g": q,   "W": W_klein,   "Wsub": "m_r"},
            "Bring":       {"g": mu,  "W": W_bring,   "Wsub": "g_2*E_1"},
            "Genus_F5":    {"g": F5,  "W": W_g5,      "Wsub": "F_5! = m_r*F_5"},
            "Macbeath":    {"g": phi6, "W": W_macbeath, "Wsub": "E_2*q*Phi_6"},
            "Hurwitz_triplet": {"g": dimG2, "W": W_hurwitz, "Wsub": "r*q*F_5*Phi_6*Phi_3"},
        },
        "headline": headline,
    }
    out = Path("data") / "w33_MDCCLXXXIII_MDCCXCII_pascal14_weierstrass.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    print(headline)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
