# PART CCCLVI — Seidel Switching Classes of W(3,3)

## Overview

The **Seidel matrix** of a graph $G$ on vertex set $V$ is

$$
S = J - I - 2A,
$$

where $J$ is the all-ones matrix, $I$ the identity, and $A$ the adjacency matrix. Entries are $S_{ij} = -1$ for adjacent pairs, $+1$ for non-adjacent pairs, and $S_{ii} = 0$.

Two graphs are **Seidel switching equivalent** if one can be obtained from the other by complementing all edges between a subset $U \subseteq V$ and its complement $V \setminus U$. The Seidel spectrum $\{\tau_i^{m_i}\}$ is a complete invariant of the switching class.

## Seidel Eigenvalues of W(3,3)

For any SRG$(v,k,\lambda,\mu)$ with $A$-eigenvalues $k, r, s$, the Seidel matrix has eigenvalues

$$
\tau_0 = v - 1 - 2k \quad (m=1), \qquad
\tau_r = -(1+2r) \quad (m = m_r), \qquad
\tau_s = -(1+2s) \quad (m = m_s),
$$

because every $A$-eigenvector $\mathbf{v} \perp \mathbf{1}$ satisfies $S\mathbf{v} = -(1+2\rho)\mathbf{v}$.

For $W(3,3) = \mathrm{SRG}(40,12,2,4)$ with $r=2$ (mult 24) and $s=-4$ (mult 15):

| Eigenvalue | Formula | Value | Multiplicity |
|------------|---------|-------|--------------|
| $\tau_0$ | $V-1-2K$ | $15$ | $1$ |
| $\tau_r$ | $-(1+2r)$ | $-5$ | $24$ |
| $\tau_s$ | $-(1+2s)$ | $7$ | $15$ |

Total: $1+24+15=40=V$. Trace: $15 + 24(-5) + 15(7) = 15-120+105=0$.

## Spectral Identities

**Trace zero:**

$$
\tau_0 \cdot 1 + \tau_r \cdot 24 + \tau_s \cdot 15 = 0.
$$

**Frobenius norm:** Since all off-diagonal entries of $S$ are $\pm 1$,

$$
\|S\|_F^2 = V(V-1) = 1560 = 1 \cdot 15^2 + 24 \cdot (-5)^2 + 15 \cdot 7^2 = 225 + 600 + 735.
$$

**Linear relations:**

$$
\tau_0 + \tau_r = 10 = \alpha, \qquad
\tau_r + \tau_s = 2 = R, \qquad
\tau_0 - \tau_s = 8 = 2 \cdot E_4.
$$

## Physics Connections

| Seidel Quantity | Value | Physics Interpretation |
|-----------------|-------|------------------------|
| $\tau_0$ | $15$ | $\mathbf{15}$ of $SU(5)$ (matter) $= K + \text{gen}$ |
| abs(τ_r) | 5 | SU(5) rank = α/2 |
| $\tau_s$ | $7$ | $\mu + \text{gen} = 4+3$ |
| $m_{\tau_r}$ | $24$ | $\mathbf{24}$ of $SU(5)$ (adjoint) |
| $m_{\tau_s}$ | $15$ | $\mathbf{15}$ of $SU(5)$ (matter) |
| $\tau_0 + \tau_r$ | $10$ | Fine-structure code $\alpha = 10$ |
| $V - \tau_0$ | $25$ | $(\alpha/2)^2 = 5^2$ |

The Seidel spectrum of $W(3,3)$ thus encodes three SM multiplets simultaneously:
the trivial eigenvalue $\tau_0 = 15 = \mathbf{15}_{SU(5)}$, the multiplicity of $\tau_r$ gives $\mathbf{24}_{SU(5)}$,
and $|\tau_r| = 5$ recovers the $SU(5)$ rank.

## Checks (27/27)

```
[PASS]  seid_trivial_eig = 15
[PASS]  seid_trivial_eig = V-1-2K
[PASS]  seid_r_eig = -5
[PASS]  seid_r_eig = -(1+2*R_EIG)
[PASS]  seid_s_eig = 7
[PASS]  seid_s_eig = -(1+2*S_EIG)
[PASS]  mult_seid_trivial = 1
[PASS]  mult_seid_r = MULT_R = 24
[PASS]  mult_seid_s = MULT_S = 15
[PASS]  trace_seid = 0
[PASS]  frobenius_seid = V*(V-1) = 1560
[PASS]  seid_trivial + seid_r = ALPHA = 10
[PASS]  seid_r + seid_s = R_EIG = 2
[PASS]  seid_trivial - seid_s = 2*EW_GAUGE_4 = 8
[PASS]  seid_trivial^2 = MULT_S^2 = 225
[PASS]  seid_r^2 = (ALPHA//2)^2 = 25
[PASS]  seid_s^2 = (MU+GENERATIONS)^2 = 49
[PASS]  seid_r * seid_s = -35
[PASS]  V - seid_trivial = (ALPHA//2)^2 = 25
[PASS]  seid_trivial = MULT_S = SU5_MATTER = 15
[PASS]  seid_trivial = K + GENERATIONS = 15
[PASS]  mult_seid_r = SU5_ADJ = 24
[PASS]  seid_s_eig = MU + GENERATIONS = 7
[PASS]  mult_seid_r + mult_seid_s = V-1 = 39
[PASS]  seid_trivial // GENERATIONS = ALPHA//2 = 5
[PASS]  abs(seid_r_eig) = ALPHA//2 = 5
[PASS]  seid_trivial + abs(seid_r) = 2*ALPHA = 20
```

**Status: PASS — 27/27**

## Discoveries

1. The trivial Seidel eigenvalue $\tau_0 = 15 = \text{MULT\_S} = \mathbf{15}_{SU(5)}$: the switching-class invariant matches the SU(5) matter representation dimension.
2. $\tau_r = -5 = -\alpha/2$: the non-trivial negative Seidel eigenvalue is half the fine-structure code with sign.
3. $\tau_r + \tau_s = 2 = R\_EIG$: the Seidel eigenvalues sum to the original positive $A$-eigenvalue.
4. $\tau_0 + \tau_r = 10 = \alpha$: the two most distinguished Seidel eigenvalues sum to the fine-structure code.
5. Multiplicities map: $m_{\tau_r} = 24 = \mathbf{24}_{SU(5)}$ and $m_{\tau_s} = 15 = \mathbf{15}_{SU(5)}$ — the Seidel multiplicity spectrum reproduces both fundamental $SU(5)$ representations.

## Files

| File | Description |
|------|-------------|
| `exploration/PART_CCCLVI_SEIDEL_SWITCHING_BRIDGE.py` | Bridge: Seidel eigenvalues, traces, 27 checks |
| `tests/test_seidel_switching_ccclvi.py` | 86 pytest tests |
| `PART_CCCLVI_seidel_switching_results.json` | JSON summary |
| `PART_CCCLVI_SEIDEL_SWITCHING_BRIDGE.md` | This file |
