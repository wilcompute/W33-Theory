# Part CCCXLIV: Three-Idempotent GUT Projector Decomposition

## Overview

The Bose-Mesner algebra of any strongly-regular graph has dimension equal to
the number of distinct adjacency eigenvalues.  For W(3,3) — with eigenvalues
k=12, r=2, s=−4 — this algebra is **3-dimensional**, spanned by {I, A, J},
and its three **primitive idempotents** E_0, E_1, E_2 project onto the
corresponding eigenspaces.

This part derives the exact rational coefficients of E_0, E_1, E_2 in the
basis {I, A, J} and shows that their **eigenspace ranks** encode the
SU(5) Grand Unified Theory spectrum exactly — with no fitting.

---

## The Three Primitive Idempotents

From the completeness and spectral reconstruction equations:

```
E_0 + E_1 + E_2 = I           (resolution of identity)
k·E_0 + r·E_1 + s·E_2 = A    (adjacency reconstruction)
```

with E_0 = J/V (trivial projector onto the all-ones eigenvector), solving
gives:

| Idempotent | I-coeff | A-coeff | J-coeff |
|---|---|---|---|
| E_0 | 0 | 0 | 1/40 |
| E_1 | 2/3 | +1/6 | −1/15 |
| E_2 | 1/3 | −1/6 | +1/24 |

All entries are exact rationals.  Derivation uses k=12, r=2, s=−4, V=40.

---

## Rank Formula via Trace

Using Tr(I)=V, Tr(A)=0 (zero diagonal), Tr(J)=V:

```
rank(E_i) = Tr(E_i) = V · (I-coeff + J-coeff)
```

| Idempotent | rank | Algebraic source |
|---|---|---|
| E_0 | 1 | trivial eigenspace |
| E_1 | 24 | MULT_R: multiplicity of r=2 |
| E_2 | 15 | MULT_S: multiplicity of s=−4 |
| **Sum** | **40 = V** | completeness |

---

## SU(5) GUT Encoding

The ranks 24 and 15 are the exact dimensions of the two fundamental
representations of SU(5) that partition the Standard Model spectrum:

| W(3,3) object | Rank | SU(5) interpretation |
|---|---|---|
| E_1 (R-sector projector) | **24** | Adjoint of SU(5): 8 gluons + 3 W/Z + 1 γ + 12 X/Y leptoquarks |
| E_2 (S-sector projector) | **15** | Matter per generation: 5̄ (3 d̄c + νe + e−) + 10 (antisymmetric tensor) |

Additional exact identities:

```
rank(E_2) = GUT_DIM − K  =  27 − 12  =  15
GENERATIONS × rank(E_2)  =  3 × 15   =  45   (total SM Weyl fermions in SU(5))
SU5_ADJ  =  SU5_DIM² − 1  =  5² − 1  =  24
```

The identity rank(E_2) = GUT_DIM − K = 27 − 12 connects:
- **GUT_DIM = 27**: dimension of the E_6 fundamental representation
- **K = 12**: degree of the W(3,3) strongly-regular graph
- **15**: SU(5) matter content per generation

---

## Completeness Identities

The coefficient arrays satisfy exact cancellation across all three idempotents:

| Basis component | Sum over {E_0, E_1, E_2} | Required |
|---|---|---|
| I-coefficient | 0 + 2/3 + 1/3 = **1** | = 1 (identity) |
| A-coefficient | 0 + 1/6 − 1/6 = **0** | = 0 (no A in I) |
| J-coefficient | 1/40 − 1/15 + 1/24 = **0** | = 0 (no J in I) |

The J-coefficient cancellation is non-trivial: 3/120 − 8/120 + 5/120 = 0.

**A-antisymmetry**: E_1 and E_2 carry equal and opposite A-coefficients (±1/6).
They are mirror images under A → −A — a spectral sector duality.

---

## Eigenspace Projection Table

| Projector | On K-eigenspace | On R-eigenspace | On S-eigenspace |
|---|---|---|---|
| E_0 | 1 | 0 | 0 |
| E_1 | 0 | 1 | 0 |
| E_2 | 0 | 0 | 1 |

Each row sums to 1 (completeness); columns sum to 1 (each eigenspace fully covered).
The adjacency reconstruction k·E_0 + r·E_1 + s·E_2 = A verifies on all three
eigenspaces: 12·1=12, 2·1=2, (−4)·1=−4.

---

## 27-Check Verification Summary

| Group | Checks | Description |
|---|---|---|
| 1 | 7 | Exact rational idempotent coefficients in basis {I, A, J} |
| 2 | 5 | Rank formulas via trace: 1, 24, 15, completeness, ratio 8/5 |
| 3 | 5 | Eigenspace projection values (each E_i = δ-function on its eigenspace) |
| 4 | 5 | GUT encoding: SU5_ADJ=24, matter=15, GUT_DIM−K=15, 3×15=45, 5²−1=24 |
| 5 | 5 | Completeness: I-sum=1, A-sum=0, J-sum=0, non-trivial span, antisymmetry |
| **Total** | **27/27** | **PASS** |

---

## Key Discoveries

1. The W(3,3) Bose-Mesner algebra has exactly 3 primitive idempotents with ranks 1, 24, 15.
2. rank(E_1) = 24 = SU(5) adjoint dimension: the W(3,3) R-sector IS the SU(5) gauge sector.
3. rank(E_2) = 15 = SU(5) matter per generation (5̄+10): the W(3,3) S-sector IS the SU(5) matter sector.
4. rank(E_2) = GUT_DIM − K = 27 − 12 = 15: E_6 fundamental rep minus W(3,3) degree.
5. Three SM generations × 15 = 45 total SU(5) Weyl fermions, encoded in spectral rank.
6. Coefficient completeness: I-sum=1, A-sum=0, J-sum=0 — exact rational cancellation.
7. A-antisymmetry: E_1 and E_2 are related by A → −A (spectral sector duality).

---

## Architecture Position

```
CCCXLII  →  anchor-free response identities (one-sector)
CCCXLIII →  eigenvalue-graded two-sector response (R + S sectors)
CCCXLIV  →  three-idempotent GUT projector decomposition (ranks 1, 24, 15 = SU(5))
```

The three-idempotent picture completes the spectral decomposition:
where CCCXLIII showed the **metric** coupling between the two non-trivial sectors,
CCCXLIV reveals that the **algebraic rank** of each sector's projector is a
fundamental GUT constant — the W(3,3) graph encodes the SU(5) gauge and matter
content as spectral multiplicity.
