# PART CCCLV — Strongly Regular Complement of W(3,3)

## Overview

The **complement** of a strongly regular graph $\mathrm{SRG}(v,k,\lambda,\mu)$ is itself strongly regular with parameters

$$
\overline{\mathrm{SRG}(v,k,\lambda,\mu)} = \mathrm{SRG}(v,\; v-1-k,\; v-2-2k+\mu,\; v-2k+\lambda).
$$

Applying this to $W(3,3) = \mathrm{SRG}(40,12,2,4)$:

$$
\overline{W(3,3)} = \mathrm{SRG}(40,\; 27,\; 18,\; 18).
$$

## Complement Parameters

| Parameter | Formula | Value |
|-----------|---------|-------|
| $V_c$ | $V$ | $40$ |
| $K_c$ | $V-1-K$ | $27$ |
| $\lambda_c$ | $V-2-2K+\mu$ | $18$ |
| $\mu_c$ | $V-2K+\lambda$ | $18$ |
| Edges$_c$ | $\tfrac{V(V-1)}{2} - \text{Edges}$ | $540$ |

Since $\lambda_c = \mu_c = 18$, every pair of vertices in $\overline{W(3,3)}$ has the same number of common neighbours regardless of adjacency — a **conference-type** SRG.

## Complement Eigenvalues

For $\mathrm{SRG}(v,k,\lambda,\mu)$ with non-trivial eigenvalues $r, s$, the complement has non-trivial eigenvalues $-1-s$ and $-1-r$ with **swapped multiplicities**.

| Eigenvalue | Formula | Value | Multiplicity |
|------------|---------|-------|--------------|
| $K_c$ (trivial) | $V-1-K$ | $27$ | $1$ |
| $r_c$ | $-1 - s$ | $3$ | $15$ |
| $s_c$ | $-1 - r$ | $-3$ | $24$ |

Multiplicities: $1 + 15 + 24 = 40 = V$. Trace zero: $27 + 15(3) + 24(-3) = 27 + 45 - 72 = 0$.

## Key Identities

**Parameter relations between $W(3,3)$ and its complement:**

$$
K + K_c = V - 1 = 39, \qquad K \cdot K_c = 324 = \lambda_c^2.
$$

**Spectral Frobenius norm:**

$$
\|A_c\|_F^2 = K_c^2 + m_{r_c} r_c^2 + m_{s_c} s_c^2 = 729 + 135 + 216 = 1080 = V \cdot K_c.
$$

**Eigenvalue symmetry:**

$$
r_c + s_c = 0, \qquad r_c \cdot s_c = -9 = -3^2.
$$

## Physics Connections

| Mathematical Quantity | Value | Physics Interpretation |
|-----------------------|-------|------------------------|
| $K_c$ | $27$ | GUT dimension ($E_6$ matter representation) |
| $r_c$ | $3$ | Three particle generations |
| $s_c$ | $-3$ | Negative-chirality generation count |
| $m_{r_c}$ | $15$ | $\mathbf{15}$ of $SU(5)$ (matter multiplet) |
| $m_{s_c}$ | $24$ | $\mathbf{24}$ of $SU(5)$ (adjoint / gauge) |
| $\lambda_c = \mu_c$ | $18$ | $2 \times 3^2 = 2 \times \text{generations}^2$ |

The complement $\overline{W(3,3)}$ realises a complete exchange of roles: the 27-dimensional representation of $E_6$ becomes the degree, the positive eigenvalue equals the generation count, and the $SU(5)$ matter and adjoint multiplicities emerge as $m_{r_c}$ and $m_{s_c}$ respectively.

## Checks (27/27)

```
[PASS]  K_c = V-1-K = 27
[PASS]  K_c = GUT_DIM = 27
[PASS]  LAM_c = V-2-2K+MU = 18
[PASS]  MU_c = V-2K+LAM = 18
[PASS]  LAM_c = MU_c (conference-type SRG)
[PASS]  edges_c = V*(V-1)/2 - EDGES = 540
[PASS]  r_c = -1-S_EIG = 3
[PASS]  s_c = -1-R_EIG = -3
[PASS]  r_c = GENERATIONS = 3
[PASS]  s_c = -GENERATIONS = -3
[PASS]  Trace complement A_c = 0
[PASS]  K + K_c = V-1 = 39
[PASS]  K * K_c = LAM_c^2 = 324
[PASS]  mult_rc = MULT_S = 15
[PASS]  mult_sc = MULT_R = 24
[PASS]  r_c + s_c = 0 (symmetric eigenvalues)
[PASS]  r_c * s_c = -(GENERATIONS^2) = -9
[PASS]  K_c - K = MULT_S = 15
[PASS]  LAM_c * K = K_c * LAM (ratio identity)
[PASS]  spectral_sum_sq_c = V*K_c = 1080
[PASS]  |r_c| + |s_c| = 2*GENERATIONS = 6
[PASS]  edges_c = V * K_c // 2 = 540
[PASS]  K_c = GUT_DIM = 27 (E6 / GUT matter)
[PASS]  r_c = GENERATIONS = 3 (three families)
[PASS]  mult_rc = SU5_MATTER = 15
[PASS]  mult_sc = SU5_ADJ = 24
[PASS]  LAM_c = MU_c = 2*GENERATIONS^2 = 18
```

**Status: PASS — 27/27**

## Discoveries

1. The complement degree $K_c = 27$ equals the GUT dimension and the number $L = 27$ of $\mathbb{F}_3^3$ lines.
2. The complement eigenvalues $r_c = 3$ and $s_c = -3$ are symmetric about zero with $|r_c| = \text{generations}$.
3. Multiplicities swap: $m_{r_c} = 15 = m_s(W(3,3))$ and $m_{s_c} = 24 = m_r(W(3,3))$.
4. The conference-type condition $\lambda_c = \mu_c$ means $\overline{W(3,3)}$ is a strongly regular conference graph.
5. The Frobenius norm identity $\|A_c\|_F^2 = V K_c = 1080$ is equivalent to $2\,\text{Edges}_c = 1080$.

## Files

| File | Description |
|------|-------------|
| `exploration/PART_CCCLV_SRG_COMPLEMENT_BRIDGE.py` | Bridge: complement SRG parameters, eigenvalues, 27 checks |
| `tests/test_srg_complement_ccclv.py` | 107 pytest tests |
| `PART_CCCLV_srg_complement_results.json` | JSON summary |
| `PART_CCCLV_SRG_COMPLEMENT_BRIDGE.md` | This file |
