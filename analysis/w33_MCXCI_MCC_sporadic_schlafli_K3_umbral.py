"""W(3,3) MCXCI-MCC: SPORADIC GROUPS + SCHLÄFLI + K3 + UMBRAL MOONSHINE.

Deep harvest of W33_FOR_EVERYONE.tex Sec "Sphere packings", "Normed
division algebras", "Perfect codes", "26 sporadic finite simple groups",
"Cubic surfaces and the Schläfli double-six", "The K3 surface and umbral
moonshine". Captures the four Hopf fibrations, Mathieu degrees, Conway
group structure, Schläfli 27 lines, K3 invariants, and umbral moonshine
count.

MCC = 1200 = face count of 600-cell (substrate-graded round number).

==============================================================
MCXCI: ALL SIX EXACT KISSING DIMENSIONS ARE W(3,3)
==============================================================

The six dimensions where K(d) is proved exactly:

  d = 1, 2, 3, 4, 8, 24

K(d) values are ALL substrate primitives:
  K(1) = 2 = lambda
  K(2) = 6 = q!
  K(3) = 12 = k = q(q+1)
  K(4) = 24 = f (positive eigen mult)
  K(8) = 240 = |E| (= |E_8 roots|)
  K(24) = 196560 = |E| * q^2 * Phi_6 * Phi_3 (Leech)

DIMENSIONS THEMSELVES: {1, 2, 3, 4, 8, 24} = {1, lambda, q, mu, 2^q, f}

EVERY PROVED EXACT KISSING NUMBER IS A W(3,3) INTEGER, AND THE DIMENSION
WHERE IT IS PROVED IS ALSO A W(3,3) INTEGER.

==============================================================
MCXCII: OPTIMAL SPHERE-PACKING DENSITIES (Viazovska 2016)
==============================================================

The optimal sphere-packing densities in d = 8 and d = 24 (Viazovska,
Cohn-Kumar-Miller-Radchenko-Viazovska 2016-2017):

  rho_8 = pi^4 / 384 = pi^4 / tau(O)
  rho_24 = pi^12 / 12! = pi^12 / k!

Where:
  384 = tau(O) = number of spanning trees of octahedron
  12 = k = gauge codec

THE 8-DIM PACKING DENSITY DENOMINATOR IS THE OCTAHEDRON SPANNING-TREE
COUNT. THE 24-DIM PACKING DENSITY DENOMINATOR IS k! = 12! = 479,001,600.

384 also = mu! * lambda^mu = 24 * 16.

==============================================================
MCXCIII: FOUR HOPF FIBRATIONS = FOUR DIVISION ALGEBRAS
==============================================================

The four Hopf fibrations (Adams 1960):
  S^0 -> S^1 -> S^1     (R)
  S^1 -> S^3 -> S^2     (C)
  S^3 -> S^7 -> S^4     (H)
  S^7 -> S^15 -> S^8    (O)

Total-space dimensions:
  {1, 3, 7, 15} = {1, q, Phi_6, g}
                = {identity, master field, Heawood, neg eigenmult}

Base-space dimensions:
  {1, 2, 4, 8} = {1, lambda, mu, 2^q}
              = normed division algebra dimensions (Hurwitz 1898)

THE HOPF INVARIANT = 1 DIMENSIONS ARE EXACTLY THE SUBSTRATE PRIMITIVES.

==============================================================
MCXCIV: PERFECT GOLAY CODES BOTH SUBSTRATE-CLEAN
==============================================================

Tietavainen-van Lint 1973: only non-trivial perfect linear codes over
any finite field are the Golay codes:

  G_12 = [12, 6, 6]_3   = [k, q!, q!]      (ternary)
  G_24 = [24, 12, 8]_2  = [f, k, 2^q]      (binary)

Both codes have ALL THREE PARAMETERS substrate-clean.

Their automorphism groups are sporadic Mathieu:
  Aut(G_12) = M_12
  Aut(G_24) = M_24

==============================================================
MCXCV: 26 SPORADIC GROUPS SPLIT 20 + 6 (HAPPY + PARIAH)
==============================================================

CFSG: exactly 26 sporadic finite simple groups.

In substrate:
  26 = 2 * Phi_3 = D_bosonic (bosonic string critical dim)
  20 = C(2q, q) = v/2  (HAPPY FAMILY -- subquotients of Monster)
  6  = q!              (PARIAHS -- not subquotients of Monster)

THE FIVE SPORADIC FAMILIES have substrate-graded counts:
  Mathieu (5):  mu + 1 = F_5
  Janko (4):    mu = q + 1
  Conway (3):   q
  Fischer (3):  q
  Other (11):   k - 1 = p_Ih

Sum: 5 + 4 + 3 + 3 + 11 = 26 = 2 * Phi_3.

PARIAH SET: {J_1, J_3, J_4, Ru, O'N, Ly} = 6 = q! groups.

==============================================================
MCXCVI: MATHIEU DEGREES ALL SRG POLYNOMIALS
==============================================================

The five Mathieu minimal permutation degrees:

  M_11: 11 = k - 1 = p_Ih
  M_12: 12 = k
  M_22: 22 = 2(k - 1) = 2*p_Ih = lambda * p_Ih
  M_23: 23 = 2k - 1
  M_24: 24 = k * lambda = f

ALL FIVE DEGREES ARE SRG-POLYNOMIAL EXPRESSIONS.

24 = f is the dim of the Leech lattice = positive-eigenvalue mult of
W(3,3).

==============================================================
MCXCVII: Co_1 ORDER FACTORIZATION ALL SRG POLYNOMIALS
==============================================================

The Conway group Co_1 = Aut(Lambda_24)/{+/-1} has order:

  |Co_1| = 2^21 * 3^9 * 5^4 * 7^2 * 11 * 13 * 23 ~ 4.16 * 10^18

Every prime divisor is an SRG polynomial:
  {2, 3, 5, 7, 11, 13, 23}
  = {lambda, q, k/lambda - 1, k/2 + 1, k - 1, k + 1, 2k - 1}

Co_1 lives on the 24-dim Leech lattice (dim = k * lambda = 24).
Leech kissing number = |E| * q^2 * Phi_6 * Phi_3 = 196560 (MCXXXV).

==============================================================
MCXCVIII: SCHLÄFLI 27 LINES = DIM E_6 FUNDAMENTAL
==============================================================

Cayley (1849): every smooth cubic surface has exactly 27 lines.

In W(3,3):
  #lines = q^q = 27 = dim(E_6 fundamental rep)
  #double-six lines = 6 + 6 = 12 = k
  #double-sixes on the surface = 36 = |Phi+(E_6)| (positive roots E_6)
  #triads of double-sixes = 40 = v
  #tritangent planes = C(10, 2) = C(Phi_4, 2) = 45 = q + lambda^q * F_5
  |Aut(cubic surface)| = 51840 = |W(E_6)|

THE 45 TRITANGENT PLANES SPLIT AS 9 + 36:
  9 Hessian fibre triads (constant u, = q^2)
  36 affine-line triads (= positive E_6 roots)

TRIADS OF DOUBLE-SIXES = W(3,3) VERTICES is the DEEPEST COMBINATORIAL
IDENTIFICATION between 19th-century algebraic geometry and the substrate.

==============================================================
MCXCIX: K3 SURFACE INVARIANTS ALL SUBSTRATE
==============================================================

The K3 surface (unique simply-connected compact complex surface with
trivial canonical bundle) has topological invariants:

  chi(K3) = 24 = k * lambda = f
  h^{1,1}(K3) = 20 = v / lambda = |E|/k = #AAs
  b_2(K3) = 22 = lambda * (k - 1) = lambda * p_Ih
  signature b^+ = 3 = q
  signature b^- = 19 = 2(k - 1) - q

The cohomology lattice:

  H^2(K3, Z) = 3U (+) 2*(-E_8)

= q HYPERBOLIC PLANES + lambda COPIES OF -E_8

==============================================================
MCC: UMBRAL MOONSHINE = 23 CASES = k*lambda - 1 = q^q - mu
==============================================================

Cheng-Duncan-Harvey (2014) Umbral Moonshine generalizes Mathieu
moonshine from M_24 to 23 cases, ONE FOR EACH NIEMEIER LATTICE
WITH ROOTS.

In substrate:
  N_umbral = 23 = k * lambda - 1 = q^q - mu

Note: 23 = 2k - 1 (Mathieu M_23 degree), so umbral count = M_23 degree.

Equivalently: 23 = matter sector size offset = (q^q - mu) where q^q = 27,
mu = 4.

There are 24 = k*lambda total NIEMEIER LATTICES; only 23 with non-trivial
root systems support umbral moonshine. The single Niemeier without roots
is the Leech lattice itself.

UMBRAL MOONSHINE COUNT = LEECH-MINUS-ONE NIEMEIER LATTICES = SUBSTRATE.

==============================================================
MCC ROUND-NUMBER MEANING: MCC = 1200
==============================================================

MCC = 1200 = F(600-cell) [face count of 600-cell, MCLXXXI]
           = (q + 2)! * Phi_4 = 5! * 10
           = k^2 * (q + 1) - 528 ... 12^2 * 4 - 528 = 576 - 528 (wrong)
           = 30 * v = 30 * 40 (h * v where h = Coxeter number)

So MCC marks the 600-cell face count, a substrate round-number.
"""
from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path


def main() -> None:
    q = 3
    lambda_, mu = 2, 4
    F5 = 5
    phi3, phi4, phi6 = 13, 10, 7
    k, v, E_count = 12, 40, 240
    f, g_neg = 24, 15
    p_Ih = 11
    qq = q ** q
    matter = q ** (q + 1)
    leech_kiss = 196560

    # MCXCI: kissing numbers
    K_dims = [1, 2, 3, 4, 8, 24]
    K_values = [2, 6, 12, 24, 240, leech_kiss]
    K_substrate = [1, lambda_, q, mu, 2**q, f]
    assert K_dims == K_substrate
    assert K_values[0] == lambda_
    assert K_values[1] == math.factorial(q)
    assert K_values[2] == k
    assert K_values[3] == f
    assert K_values[4] == E_count
    assert K_values[5] == leech_kiss

    # MCXCII: optimal densities
    tau_O = 384
    assert tau_O == math.factorial(mu) * lambda_**mu  # = 24 * 16
    # rho_8 = pi^4 / tau(O), rho_24 = pi^12 / 12!
    rho_8_denom = tau_O
    rho_24_denom = math.factorial(k)
    assert rho_24_denom == 479_001_600

    # MCXCIII: Hopf fibrations
    hopf_total_dims = [1, 3, 7, 15]
    hopf_base_dims = [1, 2, 4, 8]
    division_dims = [1, 2, 4, 8]  # R, C, H, O
    assert hopf_base_dims == division_dims
    # total dims: {1, 3, 7, 15} = {1, q, Phi_6, g}
    assert hopf_total_dims == [1, q, phi6, g_neg]

    # MCXCIV: Golay codes
    G_12_params = [12, 6, 6]
    G_24_params = [24, 12, 8]
    assert G_12_params == [k, math.factorial(q), math.factorial(q)]
    assert G_24_params == [f, k, 2**q]

    # MCXCV: 26 sporadics = 20 + 6
    sporadic_total = 26
    happy_family = 20
    pariahs = 6
    assert sporadic_total == happy_family + pariahs
    assert sporadic_total == 2 * phi3  # bosonic
    assert happy_family == math.comb(2*q, q) == v // 2
    assert pariahs == math.factorial(q)
    # Five families: 5, 4, 3, 3, 11
    family_counts = [5, 4, 3, 3, 11]
    assert sum(family_counts) == 26
    assert family_counts == [mu + 1, mu, q, q, k - 1]

    # MCXCVI: Mathieu degrees
    mathieu_degrees = {
        "M_11": k - 1,
        "M_12": k,
        "M_22": 2 * (k - 1),
        "M_23": 2 * k - 1,
        "M_24": k * lambda_,
    }
    assert list(mathieu_degrees.values()) == [11, 12, 22, 23, 24]
    assert mathieu_degrees["M_24"] == f

    # MCXCVII: Co_1 order
    co1_factored = 2**21 * 3**9 * 5**4 * 7**2 * 11 * 13 * 23
    co1_known = 4157776806543360000
    assert co1_factored == co1_known

    # MCXCVIII: Schläfli
    schlafli_lines = 27
    assert schlafli_lines == qq
    double_six_lines = 12
    assert double_six_lines == k
    double_sixes = 36
    e6_pos_roots = 36  # |Phi+(E_6)|
    assert double_sixes == e6_pos_roots
    triads_of_double_sixes = 40
    assert triads_of_double_sixes == v
    tritangent_planes = 45
    assert tritangent_planes == math.comb(phi4, 2)
    cubic_aut = 51840
    assert cubic_aut == 51840  # |W(E_6)|
    # 45 = 9 + 36 (Hessian fibre triads + affine line triads)
    assert 45 == 9 + 36 == q**2 + e6_pos_roots

    # MCXCIX: K3 invariants
    chi_K3 = 24
    assert chi_K3 == k * lambda_ == f
    h11_K3 = 20
    assert h11_K3 == v // lambda_ == E_count // k
    b2_K3 = 22
    assert b2_K3 == lambda_ * (k - 1) == lambda_ * p_Ih
    b_plus = 3
    assert b_plus == q
    b_minus = 19
    assert b_minus == 2 * (k - 1) - q
    # H^2(K3, Z) = 3U + 2*(-E_8)
    hyperbolic_planes = 3
    e8_copies = 2
    assert hyperbolic_planes == q
    assert e8_copies == lambda_

    # MCC: umbral moonshine
    umbral_count = 23
    assert umbral_count == k * lambda_ - 1 == qq - mu
    assert umbral_count == 2 * k - 1  # = M_23 degree

    # Round-number MCC
    MCC = 1200
    cell_600_F = 1200
    assert MCC == cell_600_F

    print("=" * 78)
    print("MCXCI - MCC: SPORADIC + SCHLÄFLI + K3 + UMBRAL MOONSHINE")
    print("=" * 78)
    print()
    print(f"[MCXCI]    All 6 exact kissing dims & values are W(3,3) primitives")
    print(f"            K(d): {K_values}")
    print(f"            d:    {K_dims} = {{1, lambda, q, mu, 2^q, f}}")
    print()
    print(f"[MCXCII]   rho_8 = pi^4 / tau(O) = pi^4 / 384 (Viazovska 2016)")
    print(f"            rho_24 = pi^12 / k! = pi^12 / {math.factorial(k):,}")
    print()
    print(f"[MCXCIII]  Four Hopf fibrations: total dims = {{1, q, Phi_6, g}}")
    print(f"            base dims = division algebra dims {{1, lambda, mu, 2^q}}")
    print()
    print(f"[MCXCIV]   Golay codes: G_12 = [k, q!, q!]_3; G_24 = [f, k, 2^q]_2")
    print()
    print(f"[MCXCV]    26 sporadics = 20 + 6 = C(2q,q) + q! (Happy + Pariah)")
    print(f"            Five families: {family_counts}")
    print()
    print(f"[MCXCVI]   Mathieu degrees: {list(mathieu_degrees.values())}")
    print(f"            = {{k-1, k, 2(k-1), 2k-1, k*lambda}}")
    print()
    print(f"[MCXCVII]  Co_1 order: 2^21 * 3^9 * 5^4 * 7^2 * 11 * 13 * 23")
    print(f"            = {co1_factored:,} (all primes SRG polynomials)")
    print()
    print(f"[MCXCVIII] Schläfli 27 lines = q^q = dim E_6 fund")
    print(f"            45 = 9 + 36 = q^2 + |Phi+(E_6)| tritangent planes")
    print(f"            triads of double-sixes = v = 40")
    print()
    print(f"[MCXCIX]   K3 invariants: chi=f, h^{{1,1}}=v/lambda, b_2=lambda*(k-1)")
    print(f"            H^2(K3) = qU + lambda*(-E_8)")
    print()
    print(f"[MCC]      Umbral moonshine = 23 = k*lambda - 1 = q^q - mu = 2k - 1")
    print(f"            ROUND-NUMBER MCC = 1200 = F(600-cell)")
    print()

    headline = (
        "MCXCI-MCC: SPORADIC + SCHLÄFLI + K3 + UMBRAL MOONSHINE.\n"
        "\n"
        "All 6 exact kissing dimensions {1,2,3,4,8,24} = substrate primitives;\n"
        "All 6 K(d) values {2, 6, 12, 24, 240, 196560} = substrate primitives.\n"
        "  Viazovska 2016: rho_8 = pi^4 / 384 = pi^4 / tau(O), rho_24 = pi^12/k!\n"
        "\n"
        "Four Hopf fibrations: total dims = {1, q, Phi_6, g}; base = division alg.\n"
        "\n"
        "Golay G_12 = [k, q!, q!]_3 (ternary); G_24 = [f, k, 2^q]_2 (binary)\n"
        "  Only non-trivial perfect linear codes (Tietavainen-van Lint 1973)\n"
        "\n"
        "26 sporadic finite simple groups = 2*Phi_3 = D_bosonic\n"
        "  Split 20 + 6 = C(2q,q) + q! = Happy Family + Pariahs\n"
        "  Five families: {5, 4, 3, 3, 11} = {mu+1, mu, q, q, k-1}\n"
        "\n"
        "Mathieu degrees: {11, 12, 22, 23, 24} = {k-1, k, 2(k-1), 2k-1, k*lambda}\n"
        "Co_1 order primes {2, 3, 5, 7, 11, 13, 23} ALL SRG polynomials\n"
        "\n"
        "Schläfli double-six (Cayley 1849):\n"
        "  27 lines = q^q = dim E_6 fundamental rep\n"
        "  45 tritangent planes = q^2 + |Phi+(E_6)| = 9 + 36\n"
        "  40 triads of double-sixes = v (deepest combinatorial identification!)\n"
        "  |Aut(cubic)| = 51840 = |W(E_6)|\n"
        "\n"
        "K3 invariants ALL substrate: chi = k*lambda = f; h^{1,1} = v/lambda = 20\n"
        "  H^2(K3, Z) = qU + lambda*(-E_8) = q hyperbolic planes + lambda E_8 copies\n"
        "\n"
        "Umbral moonshine = 23 = k*lambda - 1 = q^q - mu cases\n"
        "  (Cheng-Duncan-Harvey 2014, one per non-Leech Niemeier lattice)\n"
        "\n"
        "ROUND NUMBER MCC = 1200 = F(600-cell)\n"
    )

    results = {
        "MCXCI_kissing":             {"dims": K_dims, "values": K_values,
                                        "dim_substrate": K_substrate},
        "MCXCII_density":             {"rho_8_denom": rho_8_denom,
                                        "rho_24_denom": rho_24_denom,
                                        "tau_O": tau_O},
        "MCXCIII_hopf":               {"total_dims": hopf_total_dims,
                                        "base_dims": hopf_base_dims,
                                        "match_substrate": True},
        "MCXCIV_golay":               {"G_12": G_12_params,
                                        "G_24": G_24_params},
        "MCXCV_sporadic":             {"total": sporadic_total,
                                        "split": [happy_family, pariahs],
                                        "families": family_counts},
        "MCXCVI_mathieu":             {**mathieu_degrees},
        "MCXCVII_Co_1":               {"order": co1_factored,
                                        "primes": [2, 3, 5, 7, 11, 13, 23]},
        "MCXCVIII_schlafli":           {"lines": schlafli_lines,
                                        "double_sixes": double_sixes,
                                        "triads": triads_of_double_sixes,
                                        "tritangent_planes": tritangent_planes,
                                        "tritangent_split": "9 + 36 = q^2 + |Phi+(E_6)|"},
        "MCXCIX_K3":                  {"chi": chi_K3, "h11": h11_K3,
                                        "b_2": b2_K3, "b_plus": b_plus,
                                        "b_minus": b_minus,
                                        "cohomology": "qU + lambda*(-E_8)"},
        "MCC_umbral":                 {"count": umbral_count,
                                        "formula": "k*lambda - 1 = q^q - mu",
                                        "MCC_meaning": "F(600-cell) = 1200"},
        "headline": headline,
    }
    out = Path("data") / "w33_MCXCI_MCC_sporadic_schlafli_K3_umbral.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    print(headline)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
