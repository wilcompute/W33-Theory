# PART CCCXLIX — First Eigenmatrix P and Dual Eigenmatrix Q of W(3,3)

## Overview

The strongly regular graph W(3,3) admits a 3-class symmetric association scheme.
Its spectral structure is completely encoded in two 3×3 matrices — the **first
eigenmatrix** P and the **dual eigenmatrix** Q — which satisfy the exact
orthogonality identity P·Q = V·I₃.  This part verifies all entries of P and Q
with exact rational arithmetic and connects the numerical values directly to
Standard Model constants.

---

## Association Scheme Parameters

| Symbol | Value | Meaning |
|--------|-------|---------|
| V | 40 | number of vertices |
| k₀=1, k₁=12, k₂=27 | — | valencies of relations A₀, A₁, A₂ |
| m₀=1, m₁=24, m₂=15 | — | multiplicities of idempotents E₀, E₁, E₂ |
| r = 2 | R_EIG | non-trivial eigenvalue #1 |
| s = −4 | S_EIG | non-trivial eigenvalue #2 |

---

## First Eigenmatrix P

Entry P[s][j] is the eigenvalue of the adjacency operator A_s on the eigenspace E_j.

$$
P = \begin{pmatrix}
1 & 1 & 1 \\
12 & 2 & -4 \\
27 & -3 & 3
\end{pmatrix}
$$

Row s=0 is the valency row: P[0][j]=1 for all j (trivial eigenspace E₀ is
constant-1 on every relation).  Row s=1 carries the SRG eigenvalues k=12, r=2,
s=−4.  Row s=2 follows from the complementary relation: k₂=27=GUT_DIM.

### Trace of P

$$
\operatorname{tr}(P) = 1 + 2 + 3 = 6 = 2 \times \text{GENERATIONS}
$$

The trace splits as 1 (trivial) + r (= 2) + (−s−1) (= 3), summing to exactly
twice the number of Standard Model generations.

### Determinant of P

$$
\det(P) = -240 = -2 \times 120 = -(\text{number of edges in } W(3,3))
$$

The absolute value is 240 = V·K/2, the edge count.  Dividing by the multiplicity
MULT_R = 24 gives:

$$
\frac{|\det(P)|}{\text{MULT\_R}} = \frac{240}{24} = 10 = \alpha_{\text{project}}
$$

where α = 10 is the fine-structure project constant encoding electroweak unification.

---

## Dual Eigenmatrix Q

The dual eigenmatrix Q is defined by the relation

$$
Q[j][s] = \frac{m_j}{k_s} \, P[s][j]
$$

Explicitly:

$$
Q = \begin{pmatrix}
1 & 1 & 1 \\
24 & 4 & -\tfrac{8}{3} \\
15 & -5 & \tfrac{5}{3}
\end{pmatrix}
$$

### Column 0 of Q — Multiplicities

| Entry | Value | Interpretation |
|-------|-------|---------------|
| Q[0][0] | 1 | trivial multiplicity |
| Q[1][0] | 24 | MULT_R = 24 = SU(5) adjoint dimension |
| Q[2][0] | 15 | MULT_S = 15 = SU(5) matter representation per generation |

The multiplicity column directly encodes the SU(5) GUT representations.

### Diagonal of Q — Spectral Weights

$$
Q[1][1] = \frac{\text{MULT\_R} \cdot r}{K} = \frac{24 \times 2}{12} = 4
$$

$$
Q[2][2] = \frac{\text{MULT\_S} \times 3}{L} = \frac{15 \times 3}{27} = \frac{5}{3}
$$

---

## Orthogonality Identity

The fundamental duality relation is:

$$
P \cdot Q = V \cdot I_3 = 40 \cdot I_3
$$

Verified entry-by-entry with exact Fraction arithmetic:

| Position | Value |
|----------|-------|
| (PQ)[i][i] | 40 |
| (PQ)[i][j], i≠j | 0 |

This identity underpins the entire spectral theory: P and Q are mutual
"inverses" up to the scalar V, confirming that the two eigenmatrices form a
dual pair in the sense of Delsarte.

---

## Physics Bridge

| Mathematical Quantity | Value | Standard Model Counterpart |
|-----------------------|-------|---------------------------|
| k₂ = L | 27 | GUT dimension (E₆ fundamental rep) |
| Q[1][0] = MULT_R | 24 | SU(5) adjoint representation dim |
| Q[2][0] = MULT_S | 15 | SU(5) matter rep per generation |
| \|det(P)\| / MULT_R | 10 | fine-structure project constant α |
| tr(P) | 6 | 2 × number of quark/lepton generations |
| m₁ + m₂ | 39 | V − 1 = spectral degrees of freedom |

---

## Verification Summary

All 27 checks pass under exact rational arithmetic using `fractions.Fraction`:

- 7 P-matrix entry checks (P[s][j] values and weighted row sums)
- 7 Q-matrix entry checks (Q[j][s] values including Q[0][1]=1, Q[2][2]=5/3)
- 5 orthogonality checks (diagonal = 40, off-diagonal = 0)
- 5 determinant and trace checks
- 3 consistency checks (K+L=V−1, tr(P)=2·gen, |det|/MULT_R=ALPHA)

```
status: PASS, checks_pass: 27, checks_total: 27
```
