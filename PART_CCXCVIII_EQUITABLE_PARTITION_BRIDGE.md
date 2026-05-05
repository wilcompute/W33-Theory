# Part CCXCVIII: Equitable Partitions and Quotient Matrices in W(3,3)

## Overview

An **equitable (regular) partition** of V(G) into cells C_1, …, C_s assigns to
each pair (i, j) a constant b_{ij} = number of neighbours in C_j from any vertex
in C_i. The s × s matrix B = (b_{ij}) is the *quotient matrix*; its eigenvalues
form a subset of the adjacency eigenvalues of G.

For W(3,3) we construct two natural equitable partitions whose quotient eigenvalues
expose all three spectral values {K, R_EIG, S_EIG} = {12, 2, −4}.

---

## 1. Distance Partition (3 Cells)

Fix a vertex v. Partition V into:

| Cell | Description | Size |
| --- | --- | --- |
| C_0 | {v} | 1 |
| C_1 | N(v) — neighbours of v | 12 = K |
| C_2 | V \ ({v} ∪ N(v)) | 27 = K2 |

The quotient matrix is:

$$B_3 = \begin{pmatrix} 0 & 12 & 0 \\ 1 & 2 & 9 \\ 0 & 4 & 8 \end{pmatrix}$$

Row sums all equal K = 12 (k-regularity ✓).

### Quotient derivation

- **C_0 row:** all K = 12 neighbours in C_1.
- **C_1 row:** 1 back to v (C_0), LAM = 2 common neighbours with v in C_1, K − 1 − LAM = 9 to C_2.
- **C_2 row:** 0 to C_0, MU = 4 shared with v in C_1, K − MU = 8 in C_2.

### Eigenvalues of B_3

Characteristic polynomial (from trace = 0 + 2 + 8 = 10 = K + R + S):

$$-\lambda^3 + 10\lambda^2 + 32\lambda - 96 = 0$$

Roots: **{12, 2, −4} = {K, R_EIG, S_EIG}** — all three SRG eigenvalues appear.

---

## 2. Independent-Set Partition (2 Cells)

Partition V into:

| Cell | Description | Size |
| --- | --- | --- |
| C_0 | Maximum independent set I | 10 = α |
| C_1 | V \ I | 30 |

Quotient matrix:

$$B_2 = \begin{pmatrix} 0 & 12 \\ 4 & 8 \end{pmatrix}$$

- b_{01} = K = 12 (C_0 is independent, all edges to C_1).
- b_{10} = (α × K) / |C_1| = 120 / 30 = 4 = **MU = EW_GAUGE_4**.
- b_{11} = K − b_{10} = 12 − 4 = 8 = K − MU.

### Eigenvalues of B_2

$$\text{char poly: } \lambda^2 - 8\lambda - 48 = 0$$

Discriminant: 8² + 4 × 48 = 64 + 192 = **256 = 16² = EW_GAUGE_4⁴**.

$$\lambda = \frac{8 \pm 16}{2} \in \{12,\; -4\} = \{K,\; S\_EIG\}$$

R_EIG drops out — only the "outer" eigenvalues {K, S} survive.

---

## 3. Key Arithmetic Identities

| Quantity | Formula | Value |
| --- | --- | --- |
| Cross edges | α × K | 120 = EDGES / 2 |
| b₁₀ | 120 / 30 | 4 = MU = EW_GAUGE_4 |
| Discriminant √ | 16 | = EW_GAUGE_4² |
| B_3 trace | 0 + 2 + 8 | 10 = K + R + S |

The cross-edge count 120 = EDGES / 2 shows the maximum independent set touches
exactly half of all edges in W(3,3).

---

## 4. Summary Table

| Partition | Cells | Quotient eigenvalues |
| --- | --- | --- |
| Distance from v | {v}, N(v), rest | {12, 2, −4} = full spectrum |
| Indep-set vs rest | I_{10}, V\I | {12, −4} ⊂ spectrum |
| Checks pass | — | 27/27 ✓ |

---

## 5. Connections to Earlier Parts

- **Part CCXCVI** — b_{10} = MU = 4 matches the Hoffman denominator EW_GAUGE_4.
- **Part CCXCVII** — interlacing: all quotient eigenvalues ∈ [S_EIG, K] = [−4, 12] ✓.
- **Part CCXCV** — Seidel matrix: distance partition 3-cell quotient encodes the
  SRG parameter triple (K, λ, μ) = (12, 2, 4) directly.
- **Part CCXCVI** — α = 10 and the 2-cell partition eigenvalues {K, S_EIG} mirror
  the Hoffman 2-eigenvalue calculation.
