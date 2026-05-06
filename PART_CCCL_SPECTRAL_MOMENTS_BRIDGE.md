# PART CCCL — Spectral Moments and Walk Counting in W(3,3)

## Overview

The **spectral moments** $\mu_\ell = \operatorname{tr}(A^\ell)$ count the total
number of closed walks of length $\ell$ in the graph, summed over all starting
vertices.  For any strongly regular graph they factor exactly in terms of the
three distinct eigenvalues and their multiplicities:

$$\mu_\ell = m_0 \cdot k^\ell + m_r \cdot r^\ell + m_s \cdot s^\ell$$

For W(3,3) with $(k, r, s) = (12, 2, -4)$ and multiplicities $(m_0, m_r, m_s) = (1, 24, 15)$:

$$\mu_\ell = 1 \cdot 12^\ell + 24 \cdot 2^\ell + 15 \cdot (-4)^\ell$$

All calculations are exact (integer / rational arithmetic, no floating point).

---

## Spectral Moment Table

| $\ell$ | Formula contribution | $\mu_\ell$ | Combinatorial meaning |
|--------|----------------------|-----------|----------------------|
| 0 | $1 + 24 + 15$ | **40** | $= V$ (trace of identity) |
| 1 | $12 + 48 - 60$ | **0** | $= 0$ (A is traceless) |
| 2 | $144 + 96 + 240$ | **480** | $= V \cdot K = 2 \cdot \text{EDGES}$ |
| 3 | $1728 + 192 - 960$ | **960** | $= V \cdot K \cdot \lambda$ |
| 4 | $20736 + 384 + 3840$ | **24960** | 4th-order walk sum |

---

## Key Identities

### Triangle Count

Each triangle contributes exactly 6 closed walks of length 3 (3 starting
vertices × 2 directions).  Therefore:

$$T = \frac{\mu_3}{6} = \frac{960}{6} = 160 = \frac{V \cdot K \cdot \lambda}{6}$$

### Walk Normalization

Dividing by $V$ gives closed walks **per vertex**:

$$\frac{\mu_2}{V} = K = 12, \qquad \frac{\mu_3}{V} = K \lambda = 24$$

The second quantity equals the **SU(5) adjoint dimension** and $m_r = \text{MULT\_R}$.

### Fourth-Moment Ratio

$$\frac{\mu_4}{\mu_2} = \frac{24960}{480} = 52 = V + K$$

This structural identity encodes the interplay between the graph's size and
regularity.

---

## The Number 24 — A Universal Convergence

The multiplicity $m_r = 24$ is not an accident.  The same count arises from
multiple independent mathematical sources:

| Source | Reason for 24 |
|--------|---------------|
| **K4 flags** | $4 \text{ faces} \times 3 \text{ edges/face} \times 2 \text{ verts/edge} = 24$ |
| $\|\operatorname{Aut}(K_4)\| = \|S_4\|$ | $4! = 24$ |
| Toroidal map $\{3,6\}_{2,2}$ | Exactly 24 triangular faces |
| Two toroidal $K_n$ | $K_5$ and $K_6$ share $K_4$'s complete-graph extremal-adjacency property and both embed on the torus ($\gamma = 1$ from genus formula $\lceil(n-3)(n-4)/12\rceil$) |
| **Mathieu group M24** | Acts on **24** points |
| **Mathieu group M12** | Acts on **12 = K** points; $24 = 2K$ |
| **SU(5) adjoint** | 24 gauge bosons in SU(5) GUT |
| $\text{EDGES}/\alpha$ | $240 / 10 = 24$ |
| $\mu_3 / V$ | $960 / 40 = 24$ |

The two toroidal complete graphs K5 and K6 are the smallest cases where
$\lceil(n-3)(n-4)/12\rceil = 1$, making them the toroidal analogues of planar
K4.  Both inherit K4's property of being *extremally adjacent* (complete graphs)
while living on the next surface up.

---

## Physics Bridge

| Identity | Value | Meaning |
|----------|-------|---------|
| $\mu_3 / V$ | 24 | SU(5) adjoint, $m_r$, M24 points |
| $\text{EDGES}/\alpha$ | 24 | $240/10 = 24$ |
| $\mu_2 / \mu_0$ | 12 | Total gauge bosons $K$ |
| $\mu_4 / \mu_2$ | 52 | $V + K$ structural constant |
| $T = 160$ | $4 \alpha \cdot 4$ | Triangle count |
| $m_s = 15$ | $= \mathbf{15}$ of SU(5) | Matter representation per generation |

---

## Verification

All 27 checks pass (`status: PASS, checks_pass: 27, checks_total: 27`).

Groups:
1. **(5 checks)** Moments $\mu_0$ through $\mu_4$
2. **(5 checks)** Normalized moments and per-vertex walk counts
3. **(5 checks)** Triangle and walk identities
4. **(6 checks)** Physics connections (SU5, EDGES/ALPHA, Mathieu)
5. **(6 checks)** Generating function ratios and K4 flags

---

## Files

| File | Description |
|------|-------------|
| `exploration/PART_CCCL_SPECTRAL_MOMENTS_BRIDGE.py` | Bridge with verify_all() |
| `tests/test_spectral_moments_cccl.py` | 70 tests, all pass |
| `PART_CCCL_spectral_moments_results.json` | JSON summary |
| `PART_CCCL_SPECTRAL_MOMENTS_BRIDGE.md` | This file |
