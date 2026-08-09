# PART CCCXLVII — Intersection Numbers as Primal Propagators of W(3,3)

## Overview

The Bose-Mesner algebra of the W(3,3) strongly regular graph carries **two** product
structures with complementary physical meanings:

| Product | Structure constants | Part |
|---------|---------------------|------|
| Hadamard (entry-wise) | Krein parameters q[i][j][l] | CCCXLV |
| Ordinary matrix | **Intersection numbers p[i][j][l]** | **CCCXLVII** |

This part computes all 27 non-redundant intersection numbers of W(3,3) exactly via
integer arithmetic and shows they encode the same Standard Model / SU(5) spectrum
seen in the eigenvalue and Krein analyses — from an entirely different algebraic angle.

---

## Setup: Three Relation Classes

W(3,3) is a (40, 12, 2, 4)-SRG with three adjacency matrices:

```
A_0 = I          (identity / self relation)      valency k_0 = 1
A_1 = adj        (adjacency matrix)              valency k_1 = K = 12
A_2 = J-I-A_1    (complement adjacency)          valency k_2 = L = 27
```

The intersection numbers are defined by the ordinary matrix products:

```
A_i · A_j  =  Σ_l  p[i][j][l]  A_l
```

Combinatorially, p[i][j][l] counts the number of vertices z such that (x,z) ∈ R_i
and (z,y) ∈ R_j, for any fixed pair (x,y) ∈ R_l.

---

## Derivation

### A_1² (adjacency self-product)

The SRG defining recurrence reads directly as:

```
A_1² = K·A_0 + λ·A_1 + μ·A_2
     = 12·I  + 2·A_1 + 4·A_2
```

So: **p[1][1][0] = 12,  p[1][1][1] = 2,  p[1][1][2] = 4**

### A_1·A_2 (adjacency × complement)

Using A_1·J = K·J and J = A_0+A_1+A_2:

```
A_1·A_2 = K·J − A_1 − A_1²
         = 0·A_0 + (K−λ−1)·A_1 + (K−μ)·A_2
         = 0·A_0 + 9·A_1 + 8·A_2
```

So: **p[1][2][0] = 0,  p[1][2][1] = 9,  p[1][2][2] = 8**

### A_2² (complement self-product)

Using A_2·J = L·J:

```
A_2² = L·J − A_2 − A_1·A_2
      = 27·A_0 + 18·A_1 + 18·A_2
```

So: **p[2][2][0] = 27,  p[2][2][1] = 18,  p[2][2][2] = 18**

---

## Full Intersection Table

| i | j | l=0 | l=1 | l=2 |
|---|---|-----|-----|-----|
| 0 | 0 | 1   | 0   | 0   |
| 0 | 1 | 0   | 1   | 0   |
| 0 | 2 | 0   | 0   | 1   |
| 1 | 1 | **12** | **2** | **4** |
| 1 | 2 | 0   | **9** | **8** |
| 2 | 2 | **27** | **18** | **18** |

---

## Physical Identities

### 1. Triangle Count = R Eigenvalue
```
p[1][1][1]  =  λ  =  2  =  R_EIG
```
The number of common neighbors of an adjacent pair equals the positive
non-trivial eigenvalue of W(3,3). The local triangle structure is eigen-locked.

### 2. Quad Count = |S Eigenvalue| = EW Gauge Count
```
p[1][1][2]  =  μ  =  4  =  ABS_S  =  EW_GAUGE_4
```
The number of common non-neighbors of an adjacent pair is simultaneously:
- The absolute value of the negative eigenvalue |s| = 4
- The number of electroweak gauge bosons (W⁺, W⁻, Z, γ)

### 3. Gluon Octet from Adjacency-Complement Cross Product
```
p[1][2][2]  =  K − μ  =  12 − 4  =  8  =  GLUON_COUNT
```
The "propagation" from adjacency to complement encodes the SU(3)_C gluon
octet — the 8 gauge bosons of strong QCD.

### 4. GUT Dimension from Complement Valency
```
p[2][2][0]  =  L  =  27  =  GUT_DIM
```
The complement self-product diagonal entry equals the E₆ fundamental
representation dimension, identical to the complement valency.

### 5. Conference-Type Complement
```
p[2][2][1]  =  p[2][2][2]  =  18  =  6 × GENERATIONS
```
The complement of W(3,3) is itself a (40, 27, 18, 18)-SRG — a
**conference-type** graph (λ_c = μ_c = 18). The equal triangle/quad
counts decompose as 6 per generation × 3 generations.

### 6. Adjacency Degree = Half SU(5) Adjoint
```
p[1][1][0]  =  K  =  12  =  SU5_ADJ / 2  =  24 / 2
```

### 7. Eigenvalue Ratio from Triangle/Quad Ratio
```
p[1][1][1] / p[1][1][2]  =  2/4  =  R_EIG / ABS_S  =  1/2
```

---

## Valency Conservation Laws

The row-sum identity sum_l p[i][j][l]·k_l = k_i·k_j holds exactly:

| i,j | Formula | Value |
|-----|---------|-------|
| 1,1 | 12·1 + 2·12 + 4·27 | **144** = 12² |
| 1,2 | 0·1 + 9·12 + 8·27 | **324** = 12·27 |
| 2,2 | 27·1 + 18·12 + 18·27 | **729** = 27² |

---

## Primal vs Dual Structure Constants

Together, CCCXLV (Krein parameters) and CCCXLVII (intersection numbers) give
the complete Bose-Mesner algebra of W(3,3):

| Constant | Primal p[i][j][l] | Dual q[i][j][l] |
|----------|-------------------|-----------------|
| Dimension entry | p[1][1][0] = 12 | q[1][1][0] = 24 = SU5_ADJ |
| SM gauge | p[1][1][2] = 4 = EW | q[2][2][0] = 15 = SU5_MATTER |
| QCD | p[1][2][2] = 8 = gluons | — |
| GUT | p[2][2][0] = 27 = GUT_DIM | — |

---

## Verification

All 27 checks pass:

- **Group 1** (5): Identity relation A₀ acts as multiplicative identity
- **Group 2** (6): Adjacency self-product p[1][1][l] values and physics identities
- **Group 3** (5): Cross product p[1][2][l] including gluon octet
- **Group 4** (5): Complement self-product p[2][2][l] including GUT dim and conference property
- **Group 5** (6): Valency conservation, symmetry, ratio identities

**status: PASS — 27/27**

---

*Part CCCXLVII of the Theory of Everything sequence.*
*Bridge: `exploration/PART_CCCXLVII_INTERSECTION_NUMBERS_BRIDGE.py`*
*Tests: `tests/test_intersection_numbers_cccxlvii.py` (94 tests)*
