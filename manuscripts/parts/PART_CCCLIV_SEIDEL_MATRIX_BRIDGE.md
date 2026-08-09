# PART CCCLIV — Seidel Matrix and Two-Graphs of W(3,3)

## Overview

Every graph $G$ on $V$ vertices determines a **Seidel matrix**

$$S = J - I - 2A$$

whose entries are $S_{ii}=0$, $S_{ij}=-1$ if $i\sim j$, and $S_{ij}=+1$ if $i\not\sim j$.
Two graphs related by a sequence of *Seidel switchings* share the same two-graph,
making $S$ the natural invariant for the switching-equivalence class.

Applied to $W(3,3)$, the strongly regular graph $\mathrm{SRG}(40,12,2,4)$,
the Seidel matrix encodes both the graph structure and surprising arithmetic
connections to the Standard Model gauge group $\mathrm{SU}(5)$.

---

## SRG Parameters

| Parameter | Symbol | Value |
|-----------|--------|-------|
| Vertices  | $V$    | 40    |
| Degree    | $K$    | 12    |
| $\lambda$ | LAM    | 2     |
| $\mu$     | MU     | 4     |
| Edges     | —      | 240   |
| $\mathrm{mult}(r)$ | MULT\_R | 24 |
| $\mathrm{mult}(s)$ | MULT\_S | 15 |

---

## Seidel Matrix Entries

| Position | Value |
|----------|-------|
| Diagonal $S_{ii}$ | $0$ |
| Adjacent $S_{ij}$, $i\sim j$ | $-1$ |
| Non-adjacent $S_{ij}$, $i\not\sim j$ | $+1$ |

Each row contains exactly $K=12$ entries equal to $-1$ and $V-1-K=27$ entries equal to $+1$.
The Frobenius norm satisfies $\|S\|_F^2 = V(V-1) = 1560$.

---

## Seidel Eigenvalues

The adjacency matrix $A$ of $W(3,3)$ has eigenvalues $k=12$ (mult 1), $r=2$ (mult 24), $s=-4$ (mult 15).
Since $S = J-I-2A$, the action on each eigenspace of $A$ gives:

$$\sigma_{\mathrm{trivial}} = V - 1 - 2K = \mathbf{15}, \quad \text{(multiplicity 1)}$$

$$\sigma_r = -1 - 2r = \mathbf{-5}, \quad \text{(multiplicity 24)}$$

$$\sigma_s = -1 - 2s = \mathbf{+7}, \quad \text{(multiplicity 15)}$$

**Trace check:** $1\cdot15 + 24\cdot(-5) + 15\cdot7 = 15 - 120 + 105 = 0$ ✓

**Spectral sum of squares** (= $\|S\|_F^2$):
$$15^2 + 24\cdot(-5)^2 + 15\cdot7^2 = 225 + 600 + 735 = 1560 = V(V-1)$$

---

## $S^2$ Entries

Because $S$ is a $\{0,\pm1\}$-matrix, $S^2$ can be computed combinatorially.

| Position | Value | SRG interpretation |
|----------|-------|--------------------|
| Diagonal $(S^2)_{ii}$ | $V-1 = 39$ | row of unit-square entries |
| Adjacent $(S^2)_{ij}$, $i\sim j$ | $\lambda = 2$ | |
| Non-adjacent $(S^2)_{ij}$, $i\not\sim j$ | $\lambda+\mu = 6$ | |

**Derivation for adjacent pair** ($i\sim j$):
$$\sum_{k\ne i,j}(1-2A_{ik})(1-2A_{jk}) = (V-2) - 4(K-1) + 4\lambda = 38 - 44 + 8 = 2 = \lambda.$$

**Derivation for non-adjacent pair**:
$$\sum_{k\ne i,j}(1-2A_{ik})(1-2A_{jk}) = (V-2) - 4K + 4\mu = 38 - 48 + 16 = 6 = \lambda+\mu.$$

The eigenvalues of $S^2$ are the squares of those of $S$: $225$, $25$, $49$.

---

## Key Arithmetic Relations

The Seidel eigenvalues satisfy four elegant identities involving the SRG parameters:

| Identity | LHS | RHS |
|----------|-----|-----|
| $\sigma_r + \sigma_s$ | $-5+7=2$ | $\lambda = 2$ |
| $\lvert\sigma_r\rvert+\lvert\sigma_s\rvert$ | $5+7=12$ | $K = 12$ |
| $\sigma_r\sigma_s + \mathrm{mult}(r) + \mathrm{mult}(s)$ | $-35+39=4$ | $\mu = 4$ |
| $\sigma_s - \sigma_r$ | $7-(-5)=12$ | $K = 12$ |

The trivial Seidel eigenvalue coincides with the SU(5) matter dimension:
$$\sigma_{\mathrm{trivial}} = 15 = \mathrm{MULT\_S} = \dim(\mathbf{15}_{\mathrm{SU}(5)}).$$

---

## Two-Graph Structure

The **two-graph** $\mathcal{T}$ on $V=40$ vertices associated with $S$ consists of all
triples $\{i,j,k\}$ for which $S_{ij}S_{jk}S_{ki}=-1$ (an odd number of edges among them).
Because $W(3,3)$ is strongly regular, $\mathcal{T}$ is a **regular two-graph**: every pair
of vertices lies in a constant number of triples.

The regularity is confirmed by the fact that $S$ has exactly two non-trivial eigenvalues
($-5$ and $+7$), which is the characterisation of regular two-graphs due to Seidel.

Counting entries:
- Number of $-1$ entries in $S$: $2\times240 = 480$ (one per ordered edge direction)
- Number of $+1$ entries: $V(V-1)-480 = 1560-480 = 1080$

---

## Physics Connections

| Observation | Value | Physics |
|-------------|-------|---------|
| $\mathrm{mult}(\sigma_r) = \mathrm{MULT\_R}$ | 24 | $\mathrm{SU}(5)$ adjoint $\mathbf{24}$ |
| $\mathrm{mult}(\sigma_s) = \mathrm{MULT\_S}$ | 15 | $\mathrm{SU}(5)$ matter $\overline{\mathbf{15}}$ |
| $\sigma_{\mathrm{trivial}}$ | 15 | Equals $\mathrm{SU}(5)$ matter dimension |
| $\lvert\sigma_r\rvert$ | 5 | $= \alpha_\mathrm{proxy}/2 = 10/2$ |
| $\sigma_s$ | 7 | $= N_{\mathrm{gen}} + N_{\mathrm{EW}} = 3+4$ |
| $\sigma_r^2$ | 25 | $= \mathrm{MULT\_R}+1 = 25$ |

The fact that $|\sigma_r|+|\sigma_s| = K$ (vertex degree) and
$\sigma_r+\sigma_s = \lambda$ (triangle parameter) ties the
Seidel spectrum directly to the graph's combinatorial parameters.

---

## Verification

All 27 checks pass (`checks_pass = 27 / 27`, `status = PASS`).

| Group | Checks | Topic |
|-------|--------|-------|
| 1 | 6 | Seidel matrix entry values |
| 2 | 5 | Seidel eigenvalues and trace |
| 3 | 5 | $S^2$ combinatorial entries |
| 4 | 6 | Seidel–SRG arithmetic relations |
| 5 | 5 | Physics connections |

91 unit tests pass (`tests/test_seidel_matrix_cccliv.py`).
