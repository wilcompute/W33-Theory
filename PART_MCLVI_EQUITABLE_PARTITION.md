# Part MCLVI: Equitable Partition and Quotient Matrix for W(3,3)

## Overview

W(3,3) = SRG(40, 12, 2, 4) carries multiple equitable partitions inherited from
its GQ(3,3) structure. The quotient matrices of these partitions have eigenvalues
exactly matching subsets of the SRG spectrum {12, 2, −4}, with perfect (sharp)
interlacing. This provides a powerful link between the combinatorial geometry of
the generalized quadrangle and spectral graph theory.

## Definitions

A partition of V into cells C_0, ..., C_t is **equitable** if for every pair
(i, j) the number of neighbours in C_j from any vertex in C_i is constant
(depends only on i, j, not on the vertex). The **quotient matrix** B is the
t×t matrix with B[i][j] = (common edges from C_i to C_j per C_i-vertex).

**Interlacing Theorem:** If B is the quotient matrix of an equitable partition
of A, then the eigenvalues of B interlace those of A.

**Perfect Interlacing:** If every eigenvalue of B is also an eigenvalue of A
(with the same multiplicity counting), then the partition is an equitable
partition of a "completely regular" graph.

## Theorem MCLVI.1 — 3-Cell Equitable Partition

Fix vertex x. Cells: C_0 = {x} (size 1), C_1 = N(x) (size k=12), C_2 = V \ N[x] (size v−k−1=27).

Quotient matrix:

$$B_3 = \begin{pmatrix} 0 & 12 & 0 \\ 1 & 2 & 9 \\ 0 & 4 & 8 \end{pmatrix}$$

Row sums all equal k = 12 (regularity check ✓).

Equitability checks:
- C_0 ↔ C_1: n_0 · B[0][1] = 1·12 = 12 = 12·1 = n_1 · B[1][0] ✓
- C_1 ↔ C_2: n_1 · B[1][2] = 12·9 = 108 = 27·4 = n_2 · B[2][1] ✓

## Theorem MCLVI.2 — Characteristic Polynomial of B3

$$\det(B_3 - xI) = -(x-12)(x-2)(x+4) = -(x^3 - 10x^2 - 32x + 96)$$

Coefficients:
- tr(B_3) = 0 + 2 + 8 = **10** = k + r + s
- sum of 2×2 principal minors = **−32**
- det(B_3) = **−96** = k · r · s = 12 · 2 · (−4)

**The characteristic polynomial of B_3 equals the minimal polynomial of A.**
This is the hallmark of a distance-regular graph.

## Theorem MCLVI.3 — Eigenvalues and Eigenvectors of B3

| Eigenvalue | Eigenvector |
|-----------|-------------|
| k = 12 | (1, 1, 1) — Perron eigenvector |
| r = 2 | (−18, −3, 2) |
| s = −4 | (−9, 3, −1) |

Each eigenvalue of B_3 is an exact eigenvalue of A — **perfect interlacing**.

## Theorem MCLVI.4 — 2-Cell GQ Spread Partition

A line L (a clique of 4 vertices in GQ(3,3)) gives a 2-cell partition:
C_0 = L (size 4), C_1 = V \ L (size 36).

In GQ(3,3): each vertex off a line is collinear with **exactly 1** vertex on that line
(the unique perp-collinearity property of GQ(q,q)). So:

$$B_2 = \begin{pmatrix} 3 & 9 \\ 1 & 11 \end{pmatrix}$$

Equitability: 4 · 9 = 36 = 36 · 1 ✓

Characteristic polynomial: x² − 14x + 24 = (x−12)(x−2).

**The 2-cell spread partition captures eigenvalues {k, r} = {12, 2} only, missing s = −4.**
The eigenvalue s = −4 requires at least 3 cells to appear in a quotient.

## Theorem MCLVI.5 — Trace Identities for Quotient Matrix

Let T_n = tr(B_3^n) = k^n + r^n + s^n.

| n | T_n | Formula |
|---|-----|---------|
| 1 | 10 | 12 + 2 − 4 = 10 |
| 2 | 164 | 144 + 4 + 16 = 164 |
| 3 | 1672 | 1728 + 8 − 64 = 1672 |
| 4 | 21008 | 20736 + 16 + 256 = 21008 |

Note T_1 = 10 = k·δ = k·(spectral gap) from MCLII.

## Theorem MCLVI.6 — Interlacing is Sharp (Completely Regular)

Since the eigenvalues of B_3 are exactly {12, 2, −4} = Spec(A), the interlacing
of Theorem is tight: W(3,3) is **completely regular** (a strengthened form of
distance-regular).

Every equitable partition with a quotient whose eigenvalues are all SRG eigenvalues
is a "perfect partition" in the sense of Delsarte.

## Connection Table

| Bridge | Identity |
|--------|----------|
| MCLIII Ihara | char poly (x−12)(x−2)(x+4) = minimal poly of A |
| MCLIV BM algebra | B_3 row sums = k; B_3 eigenvecs encode BM projectors |
| MCLII spectral gap | T_1 = 10 = k·δ |
| GQ(3,3) geometry | 2-cell spread gives exactly eigenvalues {k,r} |
| Delsarte theory | All SRG equitable partitions have quotient eigenvalues in {k,r,s} |

## Physical Interpretation

The 3-cell equitable partition {x, N(x), rest} is the exact adjacency shell
structure of W(3,3) as a GQ. The quotient matrix B_3 is the "radial" or
"shell" dynamics operator: it tells you how probability mass (or field amplitude)
flows between distance shells around a fixed vertex.

The fact that B_3 has the same spectrum as A means there is no information loss
in reducing the full 40×40 dynamics to a 3-state Markov chain — the shell
structure fully captures the spectral data of the GQ.
