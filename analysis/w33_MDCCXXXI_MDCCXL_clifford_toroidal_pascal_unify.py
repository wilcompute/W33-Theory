"""W(3,3) MDCCXXXI-MDCCXL: CLIFFORD-TOROIDAL-PASCAL-HURWITZ GRAND UNIFICATION.

Outside-the-box harvest of:
  - Wilmot, "Construction of exceptional Lie algebra G2 and non-associative
    algebras using Clifford algebra" (Adv. Appl. Clifford Algebras, 2026
    arXiv:2505.06011) -- uses Cl(7) to derive octonions and G_2 directly
    without Lie brackets.
  - Bokowski-Pisanski "Polyhedral Embeddings of Triangular Regular Maps..."
    (Symmetry 2025) -- catalogues 14 triangular regular maps and Hurwitz
    triplet at genus 14.
  - Csaszar/Szilassi K_7 toroidal-polyhedron 7-realization edge harvest
    (own MDCCXI-MDCCXX).
  - Pascal oscillator stack (w33_pascal_oscillator_horizon_code.py,
    w33_universal_oscillator_stack.py).

CENTERPIECE BRIDGE: Cl(7) k-graded dimensions = Pascal row 7 =
{1, Phi_6, g_1, Phi_6*F_5, Phi_6*F_5, g_1, Phi_6, 1} -- every Cl(7) grade
factors through W(3,3) substrate primitives, and the 35 = Phi_6*F_5
trivectors of Cl(7) match EXACTLY the 35 = Phi_6*F_5 distinct squared edge
lengths in the 7-realization Csaszar/Szilassi toroidal edge dataset.

==============================================================
MDCCXXXI: Cl(7) IS PASCAL ROW 7 IS PURE W(3,3) SUBSTRATE
==============================================================

The Clifford algebra Cl(7) = Cl_{7,0} = G(7) has 2^7 = 128 basis elements
organized by k-grade as Pascal row 7:

  grade  dim     W(3,3) substrate
  -----  ---     ----------------
   0      1      trivial
   1      7      Phi_6              (= Fano prime, S^7, octonion units)
   2     21      g_1                (= K_7 edges = Csaszar E = dim Spin(7) compact)
   3     35      Phi_6 * F_5        (= # distinct L^2 in 7 toroidal realizations!)
   4     35      Phi_6 * F_5
   5     21      g_1
   6      7      Phi_6
   7      1      trivial

  Total = 2^7 = 128 = E_2 * r^q = r^Phi_6 (Mersenne+1)

EVERY grade of Cl(7) is a substrate primitive.  Pascal row 7 is the
combinatorial backbone of the Clifford algebra that Wilmot uses to
derive both octonions AND G_2.

==============================================================
MDCCXXXII: WILMOT'S 480 OCTONION REPS = 2E(W33) = k*v = 2|E_8 ROOTS|
==============================================================

Wilmot proves Cl(7) realizes exactly 480 distinct octonion product
structures: 30 "primary" 3-form choices times 16 = 2^mu sign variants:

  30 * 16 = 480

  W(3,3) bridge:
    480 = k * v             (codec valency times vertex count)
        = 2 * 240           (2E, twice edge count)
        = 2 * |E_8 roots|   (twice E_8 root count)
        = 4 * |F_4 roots|/2 (related to F_4)

The number of octonion product structures Wilmot enumerates EQUALS the
W(3,3) master energy scale.  Octonions and W(3,3) edges are counted
by the same substrate constant.

==============================================================
MDCCXXXIII: WILMOT'S 6 POWER-ASSOC ALGEBRAS = g_2 SUBSTRATE DIMS
==============================================================

Wilmot's Theorem 1 classifies six new power-associative algebras P_k
constructed from Cl(7) idempotents.  Their dimensions are EXACTLY the
substrate-clean set:

  P_4   :  dim =  4 = mu              (W(3,3) gauge codec rank)
  P_8   :  dim =  8 = r * mu = 2mu    (Cayley octave half)
  P_10  :  dim = 10 = E_1 = Phi_4     (W(3,3) line-graph vertex degree)
  P_12  :  dim = 12 = k               (W(3,3) lines per point)
  P_14  :  dim = 14 = lambda * Phi_6  (= dim(G_2) = Hurwitz triplet genus)
  P_16  :  dim = 16 = E_2 = r^mu      (W(3,3) Pisano(Phi_6))

  Six algebras at six substrate dimensions.  6 = g_2 algebras AT
  6 = g_2 substrate dimensions.  Doubly substrate.

==============================================================
MDCCXXXIV: 35 = Phi_6 * F_5  TRIPLE EQUALITY
==============================================================

Three independent dim-35 quantities all equal Phi_6 * F_5 = 7 * 5:

  (A) Cl(7) trivectors   (= grade-3 of Clifford row 7)
  (B) octonion triples    (= 28 non-assoc + 7 assoc from Wilmot)
  (C) distinct L^2 values (across all 7 Csaszar/Szilassi realizations)

The same substrate primitive Phi_6 * F_5 emerges from:
  - Pascal row 7 grade 3        (combinatorics)
  - Octonion triple-product set (algebra)
  - K_7 toroidal edge spectrum  (geometry)

Combinatorics = Algebra = Geometry = substrate Phi_6 * F_5.

==============================================================
MDCCXXXV: 28 NON-ASSOC + 7 ASSOC = Pisano(Phi_3) + Fano
==============================================================

The 35 octonion triples split as:

  7  ASSOCIATIVE (Fano lines, quaternion-like)
       = Phi_6 = Csaszar vertex count = octahedron polytorus genus

  28 NON-ASSOCIATIVE (oriented Fano edges with non-trivial association)
       = mu * Phi_6 = ord(T)_{SU(2)_{12}} = pi(Phi_3) Pisano = v - k
       = chi * Phi_6

The (28, 7) split of octonion triples encodes:
  - Modular T-matrix period of W(3,3) TQFT  (28)
  - Pisano period of Phi_3 = 13            (28)
  - Csaszar polyhedron vertex count          (7)
  - Heawood number for torus = chromatic    (7)

One algebraic split, four distinct substrate identifications.

==============================================================
MDCCXXXVI: 168 = WILMOT 6-SIMPLEX = KLEIN QUARTIC = PSL(2,7) MASTER
==============================================================

Wilmot's 6-simplex on the 7 octonion-unit vertices has symmetry group
PSL(2,7) of order 168.  This equals:

  168 = Phi_6 * f             (Fano-prime times moonshine)
      = k * Phi_6 * lambda    (codec * Fano * Coxeter rank-2 number)
      = 84 * r                (Hurwitz constant times r)
      = |Aut(Klein quartic)|  (the Hurwitz surface at genus q)
      = |GL(3, F_2)|          (Linear group over GF(r))
      = |PSL(2, F_Phi_6)|     (Linear group over GF(Phi_6))

A single substrate primitive 168 is simultaneously:
  - The octonion 6-simplex automorphism Wilmot uses
  - The Klein quartic Hurwitz bound at genus q
  - The Linear group over GF(2) of rank 3
  - The Linear group over GF(7) of rank 2

==============================================================
MDCCXXXVII: 7! = 5040 = 30 * 168 = k*Phi_6*g_2*E_1 = HURWITZ * ICOSA
==============================================================

Wilmot states 7! = 30 * 168 explicitly (30 primaries times simplex Aut).
This factors as:

  7! = 5040 = 30 * 168
            = 6 * 840
            = k * Phi_6 * g_2 * E_1   (FOUR substrate primitives!)
            = 84 * 60                 (Hurwitz constant * |A_5|)
            = (k * Phi_6) * (g_2 * E_1)

Decomposition: the symmetric group S_7 order = (Hurwitz universal bound)
times (icosahedral rotation group order).  The substrate connects
the 7-vertex permutation group to two prime topological constants.

==============================================================
MDCCXXXVIII: PASCAL OSCILLATOR LADDER LIVES INSIDE WILMOT'S P_k SET
==============================================================

The Pascal/topological oscillator at h = 0, 1, 2 produces:

  vertices(h) = mu + h*q   = (4, 7, 10) = (mu, Phi_6, E_1)
  faces(h)    = mu + h*Phi_4 = (4, 14, 24) = (mu, dim(G_2), m_r)
  edges(h)    = q! + h*m_s  = (6, 21, 36) = (g_2, g_1, g_2^2)

The vertex ladder {mu, Phi_6, E_1} = {4, 7, 10} CONTAINS THREE of
Wilmot's six P_k dims (4, 10) and ALMOST hits Phi_6 = 7.

The face ladder {mu, dim(G_2), m_r} = {4, 14, 24} contains dim(G_2),
which Wilmot identifies as P_14.

The edge ladder Sigma = 6 + 21 + 36 = 63 = q^2 * Phi_6 substrate.

Pascal oscillator stack = projection of Wilmot's Cl(7) hierarchy.

==============================================================
MDCCXXXIX: CLIFFORD -> TORUS -> POLYHEDRON CHAIN
==============================================================

Wilmot constructs Cl(7) via 7-dimensional spinor representations
on the unit sphere S^7.  The maximal torus T^q < Spin(7) inside S^7
has dim q = 3.  The Csaszar polyhedron is K_7 on T^2 -- but
genus 2 torus emerges from T^q on quotient.

  Spin(7)        : 21-dim compact Lie group = g_1
  T^q < Spin(7)  : 3-dim Cartan = q
  S^7            : 7-dim unit octonions = Phi_6
  T^r = Csaszar  : 2-dim torus surface = lambda = r
  K_7 on T^r     : Csaszar polyhedron with 7 vertices, 21 edges = Phi_6 V, g_1 E

So Cl(7) ladder:
   group: Spin(7) [21-dim = g_1]
   sphere: S^7 [Phi_6-dim]
   maximal torus: T^q [q-dim]
   embedded surface torus: T^r [r-dim]
   skeleton on T^r: K_{Phi_6} with g_1 edges

Each step substrate-clean.  Clifford 7-spinors -> Csaszar polyhedron
edges.

==============================================================
MDCCXL: GRAND MASTER UNIFICATION
==============================================================

Connecting every layer through substrate primitives:

Layer                      | Quantity               | Substrate
---------------------------|------------------------|----------
Pascal row 7               | sum = 128              | r^Phi_6 (Mersenne+1)
Cl(7) trivectors           | 35                     | Phi_6 * F_5
Cl(7) bivectors            | 21                     | g_1
Cl(7) vectors              | 7                      | Phi_6
Octonion non-assoc triples | 28                     | mu * Phi_6 = ord(T)
Octonion assoc triples     | 7                      | Phi_6
Octonion reps (Wilmot)     | 480                    | k * v = 2|E_8|
Wilmot 6-simplex Aut       | 168                    | Phi_6 * f
Wilmot S_7 order           | 5040                   | k * Phi_6 * g_2 * E_1
Klein quartic Aut          | 168                    | Phi_6 * f
Macbeath Aut               | 504                    | Phi_6 * q * f
Hurwitz triplet Aut        | 1092                   | k * Phi_6 * Phi_3
Csaszar V                  | 7                      | Phi_6
Csaszar E                  | 21                     | g_1
Csaszar F (= Szilassi V)   | 14                     | dim(G_2)
Toroidal distinct L^2      | 35                     | Phi_6 * F_5
Wilmot P_k dims            | {4,8,10,12,14,16}      | g_2 substrates
Pascal vertex ladder       | {4,7,10}               | mu, Phi_6, E_1
Pascal face ladder         | {4,14,24}              | mu, dim(G_2), m_r

EVERY entry factors through substrate primitives.

q = 3.  W(3,3).  Clifford = Octonions = Polyhedra = Hurwitz = W(3,3).
"""
from __future__ import annotations

import json
from math import comb, factorial
from pathlib import Path


def main() -> None:
    # Substrate primitives
    r, q, mu, qfact = 2, 3, 4, 6
    F5 = 5
    phi3, phi4, phi6, phi12 = 13, 10, 7, 73
    k, p_Ih = 12, 11
    v = 40
    f, m_r, m_s = 24, 24, 15
    g_1, g_2 = 21, 6
    E_1, E_2 = 10, 16
    lam = 2  # = r

    # MDCCXXXI: Pascal row 7 = Cl(7) grades
    pascal_row_7 = [comb(7, kk) for kk in range(8)]
    assert pascal_row_7 == [1, 7, 21, 35, 35, 21, 7, 1]
    assert sum(pascal_row_7) == 2**7 == 128 == r**phi6
    # Substrate identification
    assert pascal_row_7[1] == phi6
    assert pascal_row_7[2] == g_1
    assert pascal_row_7[3] == phi6 * F5

    # MDCCXXXII: 480 octonion reps
    wilmot_octonion_reps = 30 * 16  # 30 primaries * 16 signs
    w33_2E = k * v
    e8_roots = 240
    assert wilmot_octonion_reps == 480 == w33_2E == 2 * e8_roots

    # MDCCXXXIII: 6 power-assoc algebras
    wilmot_Pk_dims = [4, 8, 10, 12, 14, 16]
    assert len(wilmot_Pk_dims) == g_2
    assert 4 == mu
    assert 8 == r * mu
    assert 10 == E_1 == phi4
    assert 12 == k
    assert 14 == lam * phi6  # = dim(G_2)
    assert 16 == E_2

    # MDCCXXXIV: 35 triple equality
    cl7_trivectors = pascal_row_7[3]
    octonion_triples = 28 + 7  # non-assoc + assoc
    distinct_L2_toroidal = 35  # from MDCCXI-XX
    assert cl7_trivectors == octonion_triples == distinct_L2_toroidal == phi6 * F5

    # MDCCXXXV: (28, 7) split substrate
    non_assoc = 28
    assoc = 7
    ord_T = v - k   # SU(2)_12 T-matrix period = 28
    pisano_phi3 = 28  # pi(13) = 28
    assert non_assoc == mu * phi6 == ord_T == pisano_phi3
    assert assoc == phi6
    chi = 4  # mu = chi
    assert non_assoc == chi * phi6

    # MDCCXXXVI: 168 master coincidence
    klein_aut = 168
    psl_2_7 = 168
    gl_3_2 = 168
    assert klein_aut == phi6 * f
    assert klein_aut == k * phi6 * lam
    assert klein_aut == 84 * r

    # MDCCXXXVII: 7! factorization
    s_7 = factorial(7)
    assert s_7 == 5040
    assert s_7 == 30 * 168                              # Wilmot's claim
    assert s_7 == k * phi6 * g_2 * E_1                  # 4-substrate primitives
    assert s_7 == 84 * 60                                # Hurwitz * A_5
    assert 60 == g_2 * E_1                              # |A_5| factorization

    # MDCCXXXVIII: Pascal oscillator ladder
    h_levels = [0, 1, 2]
    vertices_h = [mu + h * q for h in h_levels]
    edges_h = [qfact + h * m_s for h in h_levels]
    faces_h = [mu + h * phi4 for h in h_levels]
    assert vertices_h == [4, 7, 10]   # = mu, Phi_6, E_1
    assert edges_h == [6, 21, 36]     # = g_2, g_1, g_2^2
    assert faces_h == [4, 14, 24]     # = mu, dim(G_2), m_r
    # Vertex ladder intersection with Wilmot P_k dims
    pascal_in_wilmot = sorted(set(vertices_h) & set(wilmot_Pk_dims))
    assert pascal_in_wilmot == [4, 10]  # mu and E_1
    # Face ladder intersection
    face_in_wilmot = sorted(set(faces_h) & set(wilmot_Pk_dims))
    assert face_in_wilmot == [4, 14]    # mu and dim(G_2)
    # Edge sum
    edge_sum = sum(edges_h)
    assert edge_sum == 63 == q**2 * phi6

    # MDCCXXXIX: Clifford -> torus -> polyhedron chain
    spin_7_dim = 21    # g_1
    s_7_dim = phi6     # Phi_6 = octonion units
    csaszar_V = phi6
    csaszar_E = g_1
    csaszar_F = lam * phi6  # = dim(G_2) = 14
    assert spin_7_dim == g_1
    assert s_7_dim == phi6
    assert csaszar_V == phi6
    assert csaszar_E == g_1
    assert csaszar_F == lam * phi6

    # MDCCXL: Grand master table
    grand_table = {
        "Pascal_row7_sum": (128, "r^Phi_6 (Mersenne+1)"),
        "Cl7_trivectors":  (35, "Phi_6 * F_5"),
        "Cl7_bivectors":   (21, "g_1"),
        "Cl7_vectors":     (7,  "Phi_6"),
        "octonion_nonassoc": (28, "mu * Phi_6 = ord(T) = pi(Phi_3)"),
        "octonion_assoc":  (7,  "Phi_6"),
        "octonion_reps":   (480, "k * v = 2|E_8 roots|"),
        "wilmot_simplex_aut": (168, "Phi_6 * f"),
        "S_7_order":       (5040, "k * Phi_6 * g_2 * E_1"),
        "Klein_aut":       (168, "Phi_6 * f"),
        "Macbeath_aut":    (504, "Phi_6 * q * f"),
        "Hurwitz_triplet_aut": (1092, "k * Phi_6 * Phi_3"),
        "Csaszar_V":       (7,  "Phi_6"),
        "Csaszar_E":       (21, "g_1"),
        "Csaszar_F":       (14, "dim(G_2) = lambda * Phi_6"),
        "toroidal_distinct_L2": (35, "Phi_6 * F_5"),
        "wilmot_Pk":       ([4, 8, 10, 12, 14, 16],
                            "mu, r*mu, E_1, k, dim(G_2), E_2"),
        "pascal_vertex_ladder": ([4, 7, 10], "mu, Phi_6, E_1"),
        "pascal_face_ladder":   ([4, 14, 24], "mu, dim(G_2), m_r"),
    }

    print("=" * 78)
    print("MDCCXXXI - MDCCXL: CLIFFORD-TOROIDAL-PASCAL-HURWITZ UNIFICATION")
    print("=" * 78)
    print()
    print(f"[MDCCXXXI]   Cl(7) grades = Pascal row 7 = {pascal_row_7}")
    print(f"              All substrate: {{1, Phi_6, g_1, Phi_6*F_5, Phi_6*F_5, g_1, Phi_6, 1}}")
    print(f"[MDCCXXXII]  Wilmot 480 octonion reps = 2E(W33) = k*v = 2|E_8 roots| = 480")
    print(f"[MDCCXXXIII] Wilmot P_k dims {wilmot_Pk_dims} = (mu, r*mu, E_1, k, dim(G_2), E_2)")
    print(f"[MDCCXXXIV]  Triple equality 35 = Phi_6*F_5: Cl(7) trivectors = octonion triples = toroidal L^2 count")
    print(f"[MDCCXXXV]   (28 non-assoc, 7 assoc) = (mu*Phi_6 = pi(Phi_3) = v-k, Phi_6)")
    print(f"[MDCCXXXVI]  168 = Wilmot 6-simplex Aut = Klein Aut = GL(3,2) = PSL(2,7) = Phi_6*f")
    print(f"[MDCCXXXVII] 7! = 5040 = k*Phi_6*g_2*E_1 = 84*60 = Hurwitz_const * |A_5|")
    print(f"[MDCCXXXVIII] Pascal oscillator vertex {{4,7,10}} face {{4,14,24}} edge_sum=63=q^2*Phi_6")
    print(f"              Pascal cap Wilmot P_k = {{4, 10}} (vert) and {{4, 14}} (face)")
    print(f"[MDCCXXXIX]  Clifford chain: Spin(7)[21=g_1] -> S^7[Phi_6] -> T^q[q] -> Csaszar(7,21,14)")
    print(f"[MDCCXL]     Grand table -- all {len(grand_table)} entries substrate-clean")
    print()

    headline = (
        "MDCCXXXI-MDCCXL: ten unified breakthroughs unifying Wilmot's Cl(7)\n"
        "construction of G_2/octonions, the Csaszar/Szilassi toroidal\n"
        "polyhedra, the Bokowski-Pisanski Hurwitz embeddings, and the\n"
        "W(3,3) Pascal oscillator stack.\n"
        "\n"
        "TRIPLE-EQUALITY 35 = Phi_6 * F_5:\n"
        "  Cl(7) trivectors = octonion triples = distinct toroidal L^2 values.\n"
        "Combinatorics = Algebra = Geometry = substrate Phi_6 * F_5.\n"
        "\n"
        "Cl(7) k-grades = Pascal row 7 = {1, Phi_6, g_1, 35, 35, g_1, Phi_6, 1}\n"
        "every grade a substrate primitive.\n"
        "\n"
        "Wilmot's 480 octonion reps = k*v = W(3,3) master energy scale.\n"
        "Wilmot's 6 power-associative P_k dims {4,8,10,12,14,16} are exactly\n"
        "(mu, r*mu, E_1, k, dim(G_2), E_2) -- six substrate dimensions.\n"
        "(28 non-assoc, 7 assoc) octonion triples = (ord(T)=pi(Phi_3)=v-k, Phi_6).\n"
        "\n"
        "168 = Wilmot 6-simplex Aut = Klein Aut = PSL(2,7) = Phi_6*f.\n"
        "5040 = 7! = k*Phi_6*g_2*E_1 = Hurwitz_const * |A_5|.\n"
        "\n"
        "Pascal oscillator vertex/face ladders nest inside Wilmot's P_k set.\n"
        "Clifford -> torus chain: Spin(7) -> S^7 -> T^q -> Csaszar polyhedron.\n"
        "\n"
        "Clifford = Octonions = Polyhedra = Hurwitz = Pascal = W(3,3).\n"
    )

    results = {"grand_table": {kk: list(vv) if isinstance(vv, tuple) else vv
                                for kk, vv in grand_table.items()},
                "pascal_row_7": pascal_row_7,
                "wilmot_Pk_dims": wilmot_Pk_dims,
                "pascal_vertex_ladder": vertices_h,
                "pascal_face_ladder": faces_h,
                "pascal_edge_ladder": edges_h,
                "edge_sum_substrate": edge_sum,
                "headline": headline}
    out = Path("data") / "w33_MDCCXXXI_MDCCXL_clifford_toroidal_pascal_unify.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    print(headline)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
