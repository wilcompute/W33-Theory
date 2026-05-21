# Part MCLVII: Normalized Laplacian and Cheeger Constant for W(3,3)

## Overview

We compute the normalized Laplacian L̂ = I − A/k for the W(3,3) strongly regular graph
SRG(40, 12, 2, 4) and derive a collection of exact spectral identities, Cheeger expansion
bounds, Kemeny transport constant, and a von Neumann entropy analysis.

## Graph Parameters

- v = 40, k = 12, λ = 2, μ = 4
- Adjacency eigenvalues: k = 12 (mult 1), r = 2 (mult 24), s = −4 (mult 15)

## Normalized Laplacian Eigenvalues

For a k-regular graph, L̂ = I − A/k has eigenvalues μᵢ = 1 − λᵢ/k:

| Eigenvalue | Value | Multiplicity |
|-----------|-------|-------------|
| μ₀ = 1 − k/k | 0 | 1 |
| μᵣ = 1 − r/k | 5/6 | 24 |
| μₛ = 1 − s/k | 4/3 | 15 |

**Trace identity:** tr(L̂) = v − tr(A)/k = 40 − 0 = **40 = v**
(because tr(A) = k + m_r·r + m_s·s = 12 + 48 − 60 = 0 for the SRG).

## Theorem MCLVII.1 — Ramanujan-type bound

All non-zero eigenvalues of L̂ lie in (0, 2):

- μᵣ = 5/6 < 2 ✓
- μₛ = 4/3 < 2 ✓

This is the normalized Laplacian analog of the Ramanujan condition and follows from
s > −k (equivalently, μₛ = 1 − s/k < 2).

## Theorem MCLVII.2 — Equal Aggregate Energy (NOVEL)

$$m_r \cdot \mu_r = 24 \cdot \frac{5}{6} = 20 = 15 \cdot \frac{4}{3} = m_s \cdot \mu_s$$

The two non-trivial eigenspaces contribute **identical total weight** (20 each) to the
normalized Laplacian spectrum. This is the exact normalized-Laplacian analog of the
unnormalized Laplacian equal-energy identity from MCLV.

## Cheeger Constant Bounds

The discrete Cheeger inequality gives:

$$\frac{\mu_r}{2} \leq h(G) \leq \sqrt{2\mu_r}$$

For W(3,3):

$$\frac{5}{12} \leq h(G) \leq \sqrt{\frac{5}{3}} \approx 1.291$$

The lower bound 5/12 is the spectral expander bound: any vertex cut must remove at
least 5/12 of the edges crossing from one side.

## Spectral Moments

$$M_n = \sum_i m_i \, \mu_i^n = m_r \mu_r^n + m_s \mu_s^n$$

| n | Mₙ (exact) | Decimal |
|---|-----------|---------|
| 0 | 40 | 40.000 |
| 1 | 40 | 40.000 |
| 2 | 130/3 | 43.333 |
| 3 | 445/9 | 49.444 |
| 4 | 3185/54 | 58.981 |
| 5 | 23605/324 | 72.855 |

Note M₀ = M₁ = 40 = v — a consequence of equal aggregate energy.

## Theorem MCLVII.3 — Kemeny Constant from L̂ (Bridge to MCXLIX)

$$K = \sum_{i \neq 0} \frac{m_i}{\mu_i} = \frac{m_r}{\mu_r} + \frac{m_s}{\mu_s} = \frac{24}{5/6} + \frac{15}{4/3} = \frac{144}{5} + \frac{45}{4} = \frac{801}{20}$$

This exactly reproduces the Kemeny constant K = 801/20 computed in MCXLIX via the
random walk approach, providing an independent verification.

## Theorem MCLVII.4 — Von Neumann Entropy (Equal Split)

Treating ρ = L̂/tr(L̂) = L̂/v as a density matrix, the aggregate eigenvalue weights are:

$$p_r^{(\text{agg})} = \frac{m_r \cdot \mu_r}{\text{tr}(L̂)} = \frac{20}{40} = \frac{1}{2}$$
$$p_s^{(\text{agg})} = \frac{m_s \cdot \mu_s}{\text{tr}(L̂)} = \frac{20}{40} = \frac{1}{2}$$

The two non-trivial eigenspaces are **exactly equally weighted** in the thermal state, a
precise quantum-information signature of the equal-energy identity.

Per-eigenvalue density weights: p_i_r = 1/48, p_i_s = 1/30.

Von Neumann entropy: S ≈ 3.636 nats.

## Novel Identity Summary

| Identity | Value |
|---------|-------|
| Spectral gap μ₁(L̂) | 5/6 |
| Equal aggregate energy | m_r·μ_r = m_s·μ_s = 20 |
| von Neumann equal split | p_r = p_s = 1/2 |
| Kemeny from L̂ | 801/20 (matches MCXLIX) |
| Cheeger lower bound | 5/12 |
| Sum of μ² | 130/3 |
| μ_r · μ_s | 10/9 |

## Cross-Part Connections

- **MCLV:** Unnormalized Laplacian equal-energy: m_r(k−r) = m_s(k−s) = 240. Ratio: 240/20 = k = 12.
- **MCXLIX:** Kemeny K = 801/20 recovered independently.
- **MCLII:** Spectral gap of random walk matrix P = A/k is δ = r/k = 1/6; gap of L̂ = 1 − (1−1/6) = 1/6 → μ_r = 5/6. Bridge: μ_r = 1 − (largest non-trivial eigenvalue of P).

## Verification

- 20 identities verified by exact `Fraction` arithmetic
- 27 pytest tests, all passing
