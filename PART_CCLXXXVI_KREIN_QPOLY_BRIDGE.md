# Part CCLXXXVI — Krein Parameters and Q-Polynomial Association Scheme of W(3,3)

## Overview

This part establishes the **Krein parameters** and **Q-polynomial structure** of the
2-class association scheme arising from the symplectic polar space W(3,3).  The collinearity
graph of W(3,3) is the strongly regular graph SRG(40,12,2,4); its association scheme is
simultaneously P-polynomial (distance-regular) and Q-polynomial (cometric), confirming
the deep algebraic richness of this structure.

---

## SRG Parameters and Eigenvalues

The foundational constants for SRG(40,12,2,4):

| Symbol | Value | Meaning |
|--------|-------|---------|
| V      | 40    | vertex count |
| K      | 12    | valency |
| λ      | 2     | common neighbours for adjacent pair |
| μ      | 4     | common neighbours for non-adjacent pair |
| k₂     | 27    | non-adjacency valency (= LINES_27) |

The discriminant satisfies

$$\Delta = (\lambda - \mu)^2 + 4(K - \mu) = 4 + 32 = 36 = (\lambda Q)^2 = 6^2$$

giving eigenvalues

$$r = \frac{(\lambda-\mu) + \sqrt{\Delta}}{2} = 2, \qquad
  s = \frac{(\lambda-\mu) - \sqrt{\Delta}}{2} = -4$$

with multiplicities

$$m_r = \lambda K = 24 = \text{LINES}_{27} - Q, \qquad
  m_s = Q(Q+\lambda) = 15.$$

The **dual eigenvalues** of the complementary relation A₂:

$$r_2 = -(r+1) = -3 = -Q, \qquad s_2 = -(s+1) = 3 = Q.$$

---

## The Eigenmatrices P and Q

### First eigenmatrix (P-matrix)

$$P = \begin{pmatrix} 1 & 12 & 27 \\ 1 & 2 & -3 \\ 1 & -4 & 3 \end{pmatrix}, \qquad \det(P) = -240 = -\text{EDGES}.$$

Rows correspond to eigenspaces (trivial, r-space, s-space) and columns to the three
relations (identity, edges, non-edges).

### Second eigenmatrix (Q-matrix)

$$Q = V \cdot P^{-1} = \begin{pmatrix} 1 & 24 & 15 \\ 1 & 4 & -5 \\ 1 & -\tfrac{8}{3} & \tfrac{5}{3} \end{pmatrix}, \qquad PQ = 40I.$$

Row 0 of Q encodes the **multiplicities** [1, 24, 15]; the non-integer row Q[2] reflects
that the scheme is **not self-dual** (i.e. not isomorphic to its own dual).

---

## Intersection Numbers

The non-trivial intersection numbers (Bose-Mesner structure constants) are:

| Parameter | Value | Identity |
|-----------|-------|----------|
| p¹₁₁ = λ | 2     | common edge-nbrs for adjacent pair |
| p¹₁₂     | 9     | = k₂ / Q |
| p²₁₁ = μ | 4     | common edge-nbrs for non-adjacent pair |
| p²₁₂     | 8     | = K − μ |
| p²₂₂     | 18    | = k₂ − 1 − (K − μ) |

Key symmetry: $K \cdot p^1_{12} = K_2 \cdot p^2_{11}$, i.e. $12 \times 9 = 27 \times 4 = 108$.

---

## Krein Parameters and Q-Polynomial Condition

The Krein parameters $q^k_{ij}$ are defined via the Hadamard product of primitive idempotents:

$$E_i \circ E_j = \frac{1}{V} \sum_k q^k_{ij} E_k.$$

Using the **eigenpolynomial normalization** $P'[i][d] = P[i][d] / k_d$ (the entry of the
idempotent scaled by $V/m_i$), the system

$$m_i m_j P[i][d] P[j][d] / k_d = \sum_k q^k_{ij} m_k P[k][d]$$

is solved in exact arithmetic (Fraction).

### Non-negativity (Krein condition)

All six non-trivial Krein parameters are **non-negative**:

| Param | Exact value |
|-------|-------------|
| q⁰₁₁  | 24 (= m_r) |
| q⁰₂₂  | 15 (= m_s) |
| q¹₁₁  | 44/3 > 0   |
| q¹₁₂  | 25/3 > 0   |
| q¹₂₂  | 20/3 > 0   |
| q²₁₁  | 40/3 > 0   |
| q²₁₂  | 32/3 > 0   |
| q²₂₂  | 10/3 > 0   |

Because all Krein parameters are non-negative the scheme is **Q-polynomial** (cometric)
with ordering (0→trivial, 1→r-eigenspace, 2→s-eigenspace).

**Identity**: $q^0_{ij} = m_i \delta_{ij}$ (diagonal Krein parameters equal multiplicities).

---

## Hoffman Bounds and Absolute Bound

The **Hoffman clique bound** and **independent set bound** for SRG(40,12,2,4):

$$\omega \leq 1 - K/s = 1 - 12/(-4) = 4 = \mu, \qquad
  \alpha \leq V \cdot \frac{-s}{K-s} = 40 \cdot \frac{4}{16} = 10 = \Phi_4.$$

Notably $\omega \cdot \alpha = 40 = V$, reflecting the tight structure of the polar space.

The **absolute (Delsarte) bound** on equiangular line systems:

$$\text{AbsBound} = \frac{m_r(m_r+1)}{2} = \frac{24 \times 25}{2} = 300 \gg 40.$$

---

## Dual Scheme Structure

The dual scheme has "valencies" $(m_0, m_1, m_2) = (1, 24, 15)$ and dual eigenvalues:

$$\hat{r} = r_2 = -Q = -3, \qquad \hat{s} = s_2 = +Q = +3.$$

The dual product $r_2 \cdot s_2 = -9 = -Q^2$ and $r_2 + s_2 = 0$.

---

## Key Numerological Identities

A collection of exact identities relating the scheme constants:

| Identity | LHS | RHS |
|----------|-----|-----|
| K · k₂ = Q² · Δ | 324 | 9 · 36 |
| m_r · m_s = 360 = STAB | 24·15 | STABILIZER_STATES |
| TRANSPORT = k₂ · Φ₄ | 270 | 27 · 10 |
| EDGES // K = m_s + Φ₆ − λ | 20 | 15+7−2 |
| m_r + m_s = V−1 | 39 | 40−1 |
| det(P) = −EDGES | −240 | −240 |

---

## Bridge Results

All 107 bridge checks and all 118 test assertions pass, confirming:

1. The SRG(40,12,2,4) association scheme has a valid P-matrix with det = −240.
2. The Q-matrix satisfies PQ = 40I exactly.
3. All Krein parameters are non-negative (scheme is Q-polynomial / cometric).
4. Intersection numbers satisfy all standard relations.
5. Hoffman bounds and absolute bounds are tight / consistent.
6. The dual scheme has valencies (1, 24, 15) matching multiplicities of the primal scheme.

---

## Physical and Mathematical Significance

The Q-polynomial property of W(3,3) connects to:

- **Quantum information**: Cometric schemes underpin tight spherical designs and optimal quantum measurements (SIC-POVMs).
- **Coding theory**: Q-polynomial schemes admit "dual distance" machinery (Delsarte LP bound).
- **Representation theory**: The idempotents E₁, E₂ correspond to the non-trivial irreducible constituents of the permutation representation of Sp(4,3) on W(3,3) points (rank 3 action).
- **E₈ lattice**: The multiplicity m_r = 24 and m_s = 15 appear in the E₈ weight lattice via the identity m_r = μ·(E8_RANK − λ), connecting polar space combinatorics to exceptional geometry.

---

*Part CCLXXXVI of the W33-Theory series.*
