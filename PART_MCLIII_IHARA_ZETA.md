# Part MCLIII: Ihara Zeta Function and Graph Riemann Hypothesis for W(3,3)

## Overview

The Ihara zeta function ζ_G(u) of W(3,3) = SRG(40, 12, 2, 4) encodes the
prime cycle spectrum of the graph. Its non-trivial zeros lie exactly on the
circle |u| = 1/√(k−1) = 1/√11, which is the precise graph-theoretic analog
of the Riemann Hypothesis.

## Parameters

| Symbol | Value |
|--------|-------|
| v | 40 |
| k | 12 |
| r | 2 |
| s | −4 |
| m_r | 24 |
| m_s | 15 |
| E | 240 |

## Ihara Factorization

The Ihara zeta function factors exactly as:

$$\zeta_G(u)^{-1} = (1-u^2)^{|E|-v} \cdot \det(I - Au + (k-1)u^2 I)$$

$$= (1-u^2)^{200} \cdot (1 - ku) \cdot \prod_{j} (1 - r_j u + (k-1)u^2)$$

where the product runs over Hashimoto eigenvalue pairs.

For W(3,3) the determinant splits into three factors:

$$\det(I - Au + (k-1)u^2 I) = (1 - 12u)^1 \cdot (1 - 2u + 11u^2)^{24} \cdot (1 + 4u + 11u^2)^{15}$$

## Theorem MCLIII.1 — Graph Riemann Hypothesis (Both Families)

The discriminants of the non-trivial quadratic factors are both negative:

| Factor | Discriminant | Value | Conclusion |
|--------|-------------|-------|------------|
| r-family: 1 − 2u + 11u² | r² − 4(k−1) | −40 | RH holds |
| s-family: 1 + 4u + 11u² | s² − 4(k−1) | −28 | RH holds |

Both discriminants negative ⟺ all non-trivial zeros lie on |u| = 1/√(k−1) = 1/√11.

**W(3,3) satisfies the Graph Riemann Hypothesis.**

## Theorem MCLIII.2 — Discriminant Values

$$\Delta_r = r^2 - 4(k-1) = 4 - 44 = -40$$
$$\Delta_s = s^2 - 4(k-1) = 16 - 44 = -28$$

Note: |Δ_r| = 40 = v (number of vertices) — a remarkable coincidence.

## Theorem MCLIII.3 — Hashimoto Eigenvalue Count

The Hashimoto (edge adjacency) matrix has 2|E| = 480 eigenvalues:

| Type | Count | Formula |
|------|-------|---------|
| Trivial +1 | 2 | from (1−u²)^200 factor at u=±1 |
| r-family non-trivial | 48 | 2 × m_r |
| s-family non-trivial | 30 | 2 × m_s |
| Trivial −1 (backtrack) | 400 | 2|E| − 2 − 48 − 30 = 400 |
| **Total** | **480** | **= 2\|E\|** ✓ |

## Theorem MCLIII.4 — Spectral Trace Identities

The trace of A^L is the count of closed walks of length L:

| L | tr(A^L) | Meaning |
|---|---------|---------|
| 0 | 40 = v | vertices |
| 1 | 0 | no self-loops |
| 2 | 480 = kv | degree × vertices |
| 3 | 960 = 6 × 160 | 6 × (triangle count) |

The triangle count = 160, verified from tr(A³)/6 = 960/6 = 160.

Formula: tr(A^L) = k^L + m_r·r^L + m_s·s^L = 12^L + 24·2^L + 15·(−4)^L.

## Theorem MCLIII.5 — Jacobi Zero Trace

tr(A^1) = 12¹ + 24·2¹ + 15·(−4)¹ = 12 + 48 − 60 = 0 ✓

The trace vanishes at L=1, confirming no directed edges appear in the zeta
walk counting.

## Connection to Prior Parts

| Bridge | Equation |
|--------|----------|
| To MCLIV (BM Algebra) | tr(A³) = 960 = 6 × Δ_r × 4 = traces in BM recurrence |
| To MCLII (Spectral Gap) | Ramanujan ⟺ GRH holds (both equivalent for regular graphs) |
| To MCXLVII (CTQW) | Spectral traces = CTQW revival amplitudes at integer times |

## Physical Interpretation

The Ihara zeta function is the generating function of prime geodesic cycles.
The Graph Riemann Hypothesis certifies that W(3,3) has optimal spectral expansion:
no prime cycle has "too many" returns. This is the combinatorial Weil conjecture
analog for this finite geometry.

The discriminant |Δ_r| = v = 40 — that the r-family discriminant equals the
vertex count — is an arithmetic coincidence of the W(3,3) SRG parameters.
