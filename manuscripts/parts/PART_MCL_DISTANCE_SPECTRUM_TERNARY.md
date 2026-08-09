# Part MCL: Distance-2 Spectrum and Ternary Eigenvalue Identity

## Overview

For the symplectic generalized quadrangle W(3,3) = SRG(40, 12, 2, 4) = GQ(q,q) with q = 3,
the distance-2 adjacency matrix **A₂ = J − I − A** carries a ternary eigenvalue structure
that ties the Bose-Mesner algebra, Frobenius norms, and the parameter q together exactly.

---

## Parameters

| Symbol | Value |
|--------|-------|
| q | 3 |
| v | 40 |
| k | 12 |
| r (2nd eigenvalue) | 2 |
| s (3rd eigenvalue) | −4 |
| m_r | 24 |
| m_s | 15 |

---

## Theorem MCL.1 — Closed-Form Multiplicities for GQ(q,q)

For the collinearity graph of GQ(q,q):

$$m_r = \frac{q(q+1)^2}{2}, \qquad m_s = \frac{q(q^2+1)}{2}$$

For W(3,3): m_r = 3 · 16 / 2 = **24**, m_s = 3 · 10 / 2 = **15**.

**Corollary — Multiplicity Gap Identity:**

$$m_r - m_s = q^2$$

*Proof:*

$$m_r - m_s = \frac{q(q+1)^2 - q(q^2+1)}{2} = \frac{q[(q+1)^2 - (q^2+1)]}{2}
= \frac{q \cdot 2q}{2} = q^2 \qquad \square$$

For W(3,3): 24 − 15 = **9 = q²** ✓

---

## Theorem MCL.2 — Ternary Eigenvalue Spectrum of A₂

The distance-2 matrix A₂ = J − I − A has eigenvalues:

| Eigenspace | Eigenvalue of A | Eigenvalue of A₂ |
|------------|-----------------|------------------|
| Principal (dim 1) | k = 12 | v − 1 − k = 27 |
| r-eigenspace (dim 24) | r = q − 1 = 2 | **−q = −3** |
| s-eigenspace (dim 15) | s = −(q+1) = −4 | **+q = +3** |

*Proof:* On nonprincipal eigenspaces, J has eigenvalue 0. Therefore:
$$\lambda_j(A_2) = 0 - 1 - \lambda_j(A)$$

- r-eigenspace: −1 − r = −1 − (q−1) = **−q** ✓  
- s-eigenspace: −1 − s = −1 + (q+1) = **+q** ✓

The nonprincipal spectrum of A₂ is **{−q, +q}** — purely ternary (±q). □

---

## Theorem MCL.3 — The B-Matrix and trace(B) = 0

Define **B = A₂/q = (J − I − A)/q**. Then B has eigenvalues:

$$\lambda(B) \in \{q^2,\; -1,\; +1\}$$

with multiplicities 1, m_r = 24, m_s = 15 respectively.

**Trace identity:**

$$\text{tr}(B) = q^2 \cdot 1 + (-1) \cdot m_r + (+1) \cdot m_s = q^2 - q^2 = \mathbf{0}$$

using m_r − m_s = q² (Theorem MCL.1). □

---

## Theorem MCL.4 — Frobenius Norm Identities

$$\|A\|_F^2 = k \cdot v = 2|E| = 480$$

$$\|A_2\|_F^2 = q^3 \cdot v = 1080$$

*Proof (A₂):*
$$\|A_2\|_F^2 = (v-1-k)^2 + q^2(m_r + m_s) = 27^2 + 9 \cdot 39 = 729 + 351 = 1080 = q^3 v \qquad \square$$

**Ratio identity:**

$$\frac{\|A_2\|_F^2}{\|A\|_F^2} = \frac{q^3 v}{kv} = \frac{q^3}{k} = \frac{q^2}{q+1} = \frac{9}{4}$$

using k = q(q+1). □

---

## Theorem MCL.5 — BM-Algebra Square Identity

$$A_2^2 = q^2 I + 2q^2 J$$

*Proof:* The eigenvalues of A₂² are:
- Principal (dim 1): 27² = 729 = q²(1 + 2v) = 9 · 81 ✓
- Nonprincipal: (−q)² = q² = 9; q² = q² = 9 ✓

Since A₂² has eigenvalue q² on all nonprincipal spaces and q²(1+2v) on the principal space:
$$A_2^2 = q^2 I + (q^4 - q^2) P_\text{principal} = q^2 I + 2q^2 J$$

where P_principal = J/v and (q⁴ − q²)/v = (81−9)/40 = 72/40 = 9/5...

Actually: q²(1+2v)·(J/v) has principal eigenvalue q²(1+2v)/v·v = q²(1+2v). Check: 9·81 = 729 ✓  
And q²I + 2q²J: eigenvalue on principal = q² + 2q²v = q²(1+2v) = 9·81 = 729 ✓  
On nonprincipal: q² + 0 = q² ✓ □

**Corollary:**

$$B^2 - I = 2J$$

where B = A₂/q. This means (B−I)(B+I) = 2J, and B acts as a "quasi-involution" on the nonprincipal eigenspaces.

---

## Theorem MCL.6 — Spectral Annihilators

$$(\,A_2 + q\,I)\text{ kills the }r\text{-eigenspace.}$$
$$(\,A_2 - q\,I)\text{ kills the }s\text{-eigenspace.}$$

*Proof:*
- On r-eigenspace: A₂ has eigenvalue −q, so (A₂ + qI)|_r = 0 ✓  
- On s-eigenspace: A₂ has eigenvalue +q, so (A₂ − qI)|_s = 0 ✓ □

---

## Master Identity Table

| Identity | LHS | RHS | Verified |
|----------|-----|-----|----------|
| Multiplicity gap | m_r − m_s | q² = 9 | ✓ |
| Sum of multiplicities | m_r + m_s | v−1 = 39 | ✓ |
| Ternary spectrum | λ(A₂) on nonprincipal | ±q = ±3 | ✓ |
| trace(B) = 0 | q² − m_r + m_s | 0 | ✓ |
| Frobenius norm A | ‖A‖² | kv = 480 | ✓ |
| Frobenius norm A₂ | ‖A₂‖² | q³v = 1080 | ✓ |
| Frobenius ratio | ‖A₂‖²/‖A‖² | q²/(q+1) = 9/4 | ✓ |
| BM-algebra square | A₂² | q²I + 2q²J | ✓ |
| B-square | B² − I | 2J | ✓ |
| Annihilator r | (A₂+qI) on r-eigen | 0 | ✓ |
| Annihilator s | (A₂−qI) on s-eigen | 0 | ✓ |

**All 11 identities verified by exact arithmetic.**

---

## Physical Interpretation

| Mathematical fact | Physical reading |
|------------------|-----------------|
| m_r − m_s = q² = 9 | Multiplicity gap = dim(compact space) = (3D)² |
| m_r = 24 = |SL(2,3)| | r-eigenspace dimension matches binary tetrahedral group |
| m_r + m_s = 39 = v−1 | Both nonprincipal eigenspaces account for all non-trivial d.o.f. |
| B² − I = 2J | Distance-2 normalised matrix is a "spectral square root" of 2J |
| ‖A₂‖²/‖A‖² = 9/4 | A₂ carries q² more "spectral energy per vertex" than A |
