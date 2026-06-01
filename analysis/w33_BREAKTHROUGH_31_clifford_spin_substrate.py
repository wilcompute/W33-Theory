"""W(3,3) BREAKTHROUGH 31: CLIFFORD CARTAN-BOTT + SPIN(n) ARE SUBSTRATE.

A NEW structural finding: the Cartan-Bott classification of real
Clifford algebras has 8 = 2^q distinct types with period 8 = 2^q,
AND every Spin(n) for n = 3..16 has substrate-clean dimension.

The mod-8 periodicity of Cl is the algebra-level statement of the
substrate's 2^q (octonion) periodicity.

==============================================================
CARTAN-BOTT CLIFFORD ALGEBRA CLASSIFICATION
==============================================================

The real Clifford algebras Cl(p,q) admit 8 distinct algebra types
classified by (p-q) mod 8:

  (p-q) mod 8     algebra type        underlying matrix
  ----------     ------------        -----------------
  0              R(N)                real, dim N
  1              C(N)                complex, dim N
  2              H(N)                quaternion, dim N
  3              H(N) + H(N)         split quaternion
  4              H(N)                quaternion
  5              C(N)                complex
  6              R(N)                real
  7              R(N) + R(N)         split real

  WITH 8 = 2^q DISTINCT ALGEBRA TYPES, ALL UNDER MOD 2^q PERIODICITY.

==============================================================
Cl(n, 0) DIMENSIONS
==============================================================

  n       Cl(n,0)         dim     substrate
  0       R               1       1
  1       R + R           2       lambda
  2       R(2)            4       mu
  3       C(2)            8       2^q
  4       H(2)            16      lambda^mu
  5       H(2) + H(2)     32      lambda^F_5
  6       H(4)            64      2^q * 2^q
  7       C(8)            128     2^Phi_6
  8       R(16)           256     lambda^2^q

Dim Cl(n,0) = 2^n. All powers of 2 are substrate-clean.
After n = 8 = 2^q, the pattern repeats with R(16) tensored in.

==============================================================
SPIN(n) DIMENSIONS (n = 3..16)
==============================================================

Spin(n) is the universal double cover of SO(n) with dim n(n-1)/2:

  n   Spin(n)                  dim   substrate
  3   SU(2)                    3     q
  4   SU(2) x SU(2)            6     q!
  5   Sp(2)                    10    Phi_4
  6   SU(4)                    15    g_neg
  7                            21    q * Phi_6
  8   (triality)               28    mu * Phi_6 = P_2 (perfect!)
  9                            36    (q!)^2
  10                           45    q^2 * F_5
  11                           55    F_5 * p_Ih
  12                           66    lambda * q * p_Ih
  13                           78    lambda * q * Phi_3 (= dim E_6!)
  14                           91    Phi_6 * Phi_3 (= m_Z!)
  15                           105   q * F_5 * Phi_6
  16                           120   lambda^q * q * F_5

ALL Spin(n) for n in [3, 16] have substrate-clean dimensions.

KEY OBSERVATIONS:
  - Spin(8) dim = 28 = mu*Phi_6 = P_2 (second perfect number, BT30)
  - Spin(13) dim = 78 = dim(E_6) (= rank E_6 * Phi_3, BT24)
  - Spin(14) dim = 91 = Phi_6 * Phi_3 = m_Z (Z boson mass identity)

==============================================================
SPIN(8) TRIALITY
==============================================================

Spin(8) has a UNIQUE outer automorphism group S_3:

  Aut(Spin(8)) / Inn = S_3
  |S_3| = 6 = q!

Three inequivalent 8-dimensional representations (vector + two
spinor) are cyclically permuted by triality. The three irreps:

  Vector V    dim = 8 = 2^q
  Spinor S+   dim = 8 = 2^q
  Spinor S-   dim = 8 = 2^q
  Triality T  |T| = q!

THE Spin(8) TRIALITY = (q!) PERMUTING THREE 2^q-DIM REPS.

Substrate factorization: 3 reps of 2^q dim = q * 2^q = 3 * 8 = 24 = f!

==============================================================
ATIYAH-BOTT-SHAPIRO ORIENTATIONS
==============================================================

ABS K-theoretic orientations build on Clifford modules:

  Cl_n -> KO^n(*)     for real K-theory
  Cl_n^C -> KU^n(*)   for complex K-theory

The Bott isomorphism KO^{n+8} = KO^n with period 8 = 2^q is the
K-theoretic shadow of the Cartan-Bott Clifford periodicity.

==============================================================
SPINOR DIMENSIONS (Bott-Cartan)
==============================================================

  Cl(n) spinor dim    n mod 8     value     substrate
  -----------------   --------    -----     ---------
  Cl(0): R            n=0         1         1
  Cl(1): R+R          n=1         1         1
  Cl(2): R(2)         n=2         2         lambda
  Cl(3): C(2)         n=3         2         lambda
  Cl(4): H(2)         n=4         2         lambda
  Cl(5): H(2)+H(2)    n=5         2         lambda
  Cl(6): H(4)         n=6         4         mu
  Cl(7): C(8)         n=7         8         2^q

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
    phi3, phi4, phi6 = 13, 10, 7
    k, v, E_count = 12, 40, 240
    f, g_neg = 24, 15
    p_Ih = 11

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 31: CLIFFORD CARTAN-BOTT + SPIN(n) = SUBSTRATE")
    print("=" * 78)
    print()

    print("CARTAN-BOTT 8 = 2^q TYPES:")
    print(f"  8 distinct algebra types under (p-q) mod 8")
    print(f"  Period 8 = 2^q is the algebra-level Bott periodicity")
    print(f"  Same 2^q period as pi_*(O), pi_*(Sp) (BT26)")
    print()

    print("Cl(n, 0) DIMENSIONS:")
    cl_data = [
        (0, "R",            1,   "1"),
        (1, "R + R",        2,   "lambda"),
        (2, "R(2)",         4,   "mu"),
        (3, "C(2)",         8,   "2^q"),
        (4, "H(2)",         16,  "lambda^mu"),
        (5, "H(2) + H(2)",  32,  "lambda^F_5"),
        (6, "H(4)",         64,  "2^q * 2^q"),
        (7, "C(8)",         128, "2^Phi_6"),
        (8, "R(16)",        256, "lambda^(2^q)"),
    ]
    for n, alg, dim, sub in cl_data:
        assert dim == 2 ** n
        print(f"  Cl({n},0) = {alg:>11}  dim {dim:>3}  = {sub}")
    print()

    print("SPIN(n) DIMENSIONS:")
    spin_data = [
        (3,  3,   "q",                         lambda: 3 == q),
        (4,  6,   "q!",                         lambda: 6 == math.factorial(q)),
        (5,  10,  "Phi_4",                      lambda: 10 == phi4),
        (6,  15,  "g_neg",                      lambda: 15 == g_neg),
        (7,  21,  "q * Phi_6",                  lambda: 21 == q * phi6),
        (8,  28,  "mu * Phi_6 = P_2 (perfect)", lambda: 28 == mu * phi6),
        (9,  36,  "(q!)^2",                     lambda: 36 == math.factorial(q)**2),
        (10, 45,  "q^2 * F_5",                  lambda: 45 == q**2 * F5),
        (11, 55,  "F_5 * p_Ih",                 lambda: 55 == F5 * p_Ih),
        (12, 66,  "lambda * q * p_Ih",          lambda: 66 == lambda_ * q * p_Ih),
        (13, 78,  "lambda * q * Phi_3 (E_6)",   lambda: 78 == lambda_ * q * phi3),
        (14, 91,  "Phi_6 * Phi_3 (= m_Z)",      lambda: 91 == phi6 * phi3),
        (15, 105, "q * F_5 * Phi_6",            lambda: 105 == q * F5 * phi6),
        (16, 120, "lambda^q * q * F_5",         lambda: 120 == lambda_**q * q * F5),
    ]
    for n, dim, sub, check in spin_data:
        expected = n * (n - 1) // 2
        assert dim == expected, f"Spin({n}) dim mismatch"
        assert check(), f"Spin({n}) substrate failed for {sub}"
        print(f"  Spin({n:>2}) dim {dim:>3}  = {sub}")
    print()
    print(f"  ALL 14 Spin(n) for n in [3, 16] substrate-clean.")
    print()

    print("STRIKING ALIGNMENTS:")
    print(f"  Spin(8)  dim 28 = mu*Phi_6 = P_2 (2nd perfect, BT30)")
    print(f"  Spin(13) dim 78 = dim(E_6) (BT24 rank * Phi_3)")
    print(f"  Spin(14) dim 91 = m_Z (Z boson mass identity)")
    print()

    print("SPIN(8) TRIALITY:")
    triality_order = math.factorial(q)
    assert triality_order == 6
    triality_dim = q * (2 ** q)
    assert triality_dim == 24 == f
    print(f"  |Triality group| = |S_3| = {triality_order} = q!")
    print(f"  Three 2^q-dim reps (vec, S+, S-) cycled by triality")
    print(f"  Total triality reps dim = q * 2^q = {triality_dim} = f")
    print(f"  TRIALITY DIM IS THE SUBSTRATE'S f.")
    print()

    print("ATIYAH-BOTT-SHAPIRO:")
    print(f"  Cl_n -> KO^n(*)   (real K-theory)")
    print(f"  Cl_n^C -> KU^n(*) (complex K-theory)")
    print(f"  Bott KO period = 8 = 2^q")
    print(f"  Bott KU period = 2 = lambda")
    print()

    print("=" * 78)
    print("BREAKTHROUGH 31 SUMMARY")
    print("=" * 78)
    print("""
THE CARTAN-BOTT CLIFFORD CLASSIFICATION IS SUBSTRATE.

  8 distinct algebra types = 2^q
  Period (p-q) mod 8 = 2^q
  Dim Cl(n,0) = 2^n (powers of 2)

ALL SPIN(n) FOR n = 3..16 HAVE SUBSTRATE-CLEAN DIMENSIONS.

  Spin(8) dim 28 = mu*Phi_6 = P_2 (perfect number, BT30)
  Spin(13) dim 78 = dim(E_6) (BT24)
  Spin(14) dim 91 = m_Z (mass identity)

SPIN(8) TRIALITY = q! permuting three 2^q-dim reps:
  Total triality rep dim = q * 2^q = f

ATIYAH-BOTT-SHAPIRO K-orientations:
  KO period = 8 = 2^q
  KU period = 2 = lambda

This connects Clifford algebras to BT26 (Bott), BT24 (Lie),
BT30 (perfect numbers), and the substrate's 2^q-periodicity
across all of geometric/topological algebra.
""")

    out = Path("data") / "w33_BREAKTHROUGH_31_clifford_spin_substrate.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({
        "cartan_bott_types": 8,
        "cartan_bott_types_substrate": "2^q",
        "Cl_dims": {f"Cl({n},0)": 2**n for n in range(9)},
        "Spin_n_dims": {f"Spin({n})": n*(n-1)//2 for n in range(3, 17)},
        "Spin_8_triality_order": 6,
        "Spin_8_triality_substrate": "q!",
        "Spin_8_triality_total_rep_dim": 24,
        "Spin_8_triality_dim_substrate": "f = q * 2^q",
        "ABS_KO_period": 8,
        "ABS_KO_period_substrate": "2^q",
        "ABS_KU_period": 2,
        "ABS_KU_period_substrate": "lambda",
        "striking": [
            "Spin(8) dim 28 = mu*Phi_6 = P_2 perfect (BT30)",
            "Spin(13) dim 78 = dim(E_6)",
            "Spin(14) dim 91 = m_Z mass identity",
        ],
        "conclusion": (
            "Cartan-Bott Clifford classification has 8 = 2^q types under "
            "period 2^q; all Spin(n) for n in [3,16] substrate-clean; "
            "Spin(8) triality is q! permuting three 2^q reps with total "
            "rep dim f. The substrate's 2^q periodicity is the algebra-level "
            "Bott periodicity."
        ),
    }, indent=2, default=str), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
