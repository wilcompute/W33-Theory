# Part CCCXLV: Krein Coupling Constants — Dual Algebra Structure of W(3,3)

## Overview

The Bose-Mesner algebra of W(3,3) is closed under **two** products:
1. **Ordinary matrix multiplication** — structure constants are the intersection
   numbers p_{ij}^l.
2. **Entry-wise (Hadamard) product** — structure constants are the
   **Krein parameters** q[i][j][l].

In the idempotent basis {E_0, E_1, E_2} the Hadamard product decomposes as:

```
E_i o E_j  =  (1/V) * sum_l  q[i][j][l]  E_l
```

Part CCCXLV computes all 27 entries of the Krein tensor q[i][j][l] exactly
(as Fractions), verifies the Krein condition (all >= 0), and identifies how
the non-trivial structure constants encode the SU(5) GUT physics established
in Part CCCXLIV.

---

## Setup: Association Scheme of W(3,3)

W(3,3) carries a **2-class association scheme** with three relations:
- A_0 = I (identity)
- A_1 = A (adjacency matrix, degree k=12)
- A_2 = J - I - A (complement, degree l=27)

Eigenspace structure (from the P-matrix):

| Eigenspace | Symbol | Multiplicity | Eigenvalue of A | Eigenvalue of A_2 |
| --- | --- | --- | --- | --- |
| Trivial | E_0 | 1 | 12 | 27 |
| R-sector | E_1 | 24 | 2 | -3 |
| S-sector | E_2 | 15 | -4 | 3 |

---

## Dual Linear System for Krein Parameters

The (x,y) entry of E_j depends only on the relation class of the pair (x,y).
Setting up entry-wise products in each of the three relation classes gives a
3x3 linear system:

```
sum_l  q[i][j][l] * m_l * P[s][l]  =  m_i * m_j * P[s][i] * P[s][j] / k_s
```

for s in {0, 1, 2}, where k_s are the valencies {1, 12, 27}.  Solving this
system with exact Fraction arithmetic yields all 27 Krein parameters.

---

## Complete Krein Tensor

### E_0-coupled parameters (trivial sector acts as identity)

Since E_0 = J/V, we have E_0 o E_j = (1/V) * E_j, giving q[0][j][l] = delta_{jl}:

| q[0][j][l] | l=0 | l=1 | l=2 |
| --- | --- | --- | --- |
| j=0 | **1** | 0 | 0 |
| j=1 | 0 | **1** | 0 |
| j=2 | 0 | 0 | **1** |

### Non-trivial sector parameters

| | l=0 | l=1 | l=2 |
| --- | --- | --- | --- |
| q[1][1][l] | **24** | 44/3 | 40/3 |
| q[1][2][l] | **0** | 25/3 | 32/3 |
| q[2][2][l] | **15** | 20/3 | 10/3 |

All non-trivial (i,j >= 1) parameters have denominator 3.

---

## Key Physical Identities

### Trivial-output self-couplings

```
q[1][1][0] = 24 = MULT_R = SU5_ADJ
q[2][2][0] = 15 = MULT_S = SU5_MATTER_PER_GEN
q[1][2][0] = 0   (gauge x matter has no scalar/trivial output)
```

The R-sector self-coupling saturates exactly at the SU(5) adjoint dimension 24,
and the S-sector self-coupling at the matter dimension 15.  The vanishing of
q[1][2][0] is a "charge neutrality" condition: the Hadamard product of the
gauge and matter projectors has no trivial component.

### Eigenvalue ratio in the dual algebra

```
q[2][2][1] / q[2][2][2]  =  |S_EIG| / R_EIG  =  4 / 2  =  2
```

The SRG eigenvalue ratio |s|/r appears as a coupling ratio in the dual
(Hadamard) algebra — the matter sector's output is split 2:1 between the
R and S sectors, weighted exactly by the original eigenvalue ratio.

### Sector-sum identities

```
q[1][1][1] + q[1][1][2]  =  V - K        =  28   (gauge self-coupling sum)
q[2][2][1] + q[2][2][2]  =  K - R_EIG   =  10   (matter self-coupling sum)
q[1][2][1] + q[1][2][2]  =  (V - R_EIG)/2  =  19   (cross-coupling sum)
```

Remarkably, the cross-coupling sum is the **arithmetic mean** of the gauge
and matter sector sums.  This reflects the structure:

```
19  =  (28 + 10) / 2
```

### Output ratio

```
q[1][1][2] / q[2][2][2]  =  V / (K - R_EIG)  =  40 / 10  =  4
```

---

## Sum Rules (Conservation Laws)

For all (i,j):

```
sum_l  q[i][j][l] * m_l  =  m_i * m_j
```

| (i,j) | Sum | Value |
| --- | --- | --- |
| (1,1) | m_1^2 | 576 |
| (1,2) | m_1 * m_2 | 360 |
| (2,2) | m_2^2 | 225 |

---

## 27-Check Verification Summary

| Group | Checks | Description |
| --- | --- | --- |
| 1 | 5 | E_0 trivial coupling: q[0][j][l] = delta_{jl} |
| 2 | 6 | Trivial-output self-couplings: q[ii][0] = m_i, cross = 0, SU(5) labels |
| 3 | 6 | Exact rational Krein values: 44/3, 40/3, 25/3, 32/3, 20/3, 10/3 |
| 4 | 5 | Krein condition (>= 0), symmetry q[ij]=q[ji], sum rules |
| 5 | 5 | Physical ratio identities: eigenvalue ratio, sector sums, output ratio |
| **Total** | **27/27** | **PASS** |

---

## Key Discoveries

1. q[1][1][0] = 24 = SU5_ADJ: the gauge-sector self-coupling in the dual algebra
   equals the SU(5) adjoint dimension, as established in Part CCCXLIV.
2. q[2][2][0] = 15 = SU5_MATTER: the matter-sector self-coupling equals the
   per-generation matter content.
3. q[1][2][0] = 0: gauge-matter Hadamard coupling has no trivial output —
   a "charge neutrality" condition from the dual algebra structure.
4. q[2][2][1]/q[2][2][2] = |s|/r = 2: the original SRG eigenvalue ratio encodes
   a coupling ratio in the dual algebra.
5. Sector sums follow V-K, K-r, and their arithmetic mean (V-r)/2 — a
   clean AP structure.
6. All non-trivial Krein parameters have denominator 3, arising from the
   interaction of valencies k=12 and l=27 in the dual linear system.
7. The Krein condition (all q >= 0) is satisfied — W(3,3) passes the absolute
   bound constraint in the dual algebra.

---

## Architecture Position

```
CCCXLIII  -->  two-sector response: coupling ratio SECTOR_SCALE_RATIO = (|s|/r)^2 = 4
CCCXLIV   -->  primitive idempotents: ranks 1, 24, 15 = SU(5) GUT spectrum
CCCXLV    -->  Krein parameters: dual algebra structure constants encoding same physics
```

Part CCCXLIV showed that the **ranks** of the primitive idempotents encode
the SU(5) GUT spectrum.  Part CCCXLV shows that the **Hadamard product** of
those same idempotents — the dual algebra — encodes the same spectrum in its
trivial-output coupling constants, and further reveals the eigenvalue ratio
|s|/r = 2 as a genuine feature of the dual algebra's structure constants.
