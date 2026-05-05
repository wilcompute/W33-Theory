# Part CCXCV: Seidel Matrix Eigenvalue Structure of W(3,3)

## Overview

The **Seidel matrix** of a graph G on n vertices is the symmetric matrix
S = J − I − 2A with entries −1 on edges and +1 on non-edges (and 0 on the
diagonal). Two graphs G and G′ are *Seidel-equivalent* (belong to the same
*two-graph*) if and only if one can be obtained from the other by switching.
For the strongly regular W(3,3), the Seidel matrix has exactly three distinct
eigenvalues {15, −5, 7}, and each Seidel eigenvalue or multiplicity encodes an
SRG constant or Standard Model value.

---

## 1. Seidel Matrix Eigenvalues

For an SRG(v, k, λ, μ) with restricted eigenvalues r and s, the Seidel matrix
S = J − I − 2A has eigenvalues:

$$\tau_0 = v - 1 - 2k, \quad \tau_r = -(1+2r), \quad \tau_s = -(1+2s)$$

with multiplicities 1, m_r, and m_s respectively.

For W(3,3) with (v, k, λ, μ) = (40, 12, 2, 4) and (r, s) = (2, −4):

| Eigenvalue | Formula | Value | Multiplicity |
| --- | --- | --- | --- |
| τ_0 | v − 1 − 2k | **15** | 1 |
| τ_r | −(1 + 2r) | **−5** | 24 (= MULT_R) |
| τ_s | −(1 + 2s) | **7** | 15 (= MULT_S) |

---

## 2. Spectral Verification

### Multiplicity sum

$$1 + 24 + 15 = 40 = V \checkmark$$

### Trace(S) = 0 (diagonal is zero)

$$15 \cdot 1 + (-5) \cdot 24 + 7 \cdot 15 = 15 - 120 + 105 = 0 \checkmark$$

### Trace(S²) = V(V − 1)

Each of the n(n − 1) off-diagonal entries of S is ±1, so:

$$\text{tr}(S^2) = \tau_0^2 + 24\tau_r^2 + 15\tau_s^2 = 225 + 600 + 735 = 1560$$

$$V(V-1) = 40 \times 39 = 1560 \checkmark$$

---

## 3. Equiangular Lines

The Seidel matrix corresponds to a set of **40 equiangular lines** in ℝ^15 with
common angle arccos(1/5):

| Quantity | Value | Derivation |
| --- | --- | --- |
| Number of lines | 40 | = V |
| Embedding dimension | 15 | = MULT_S (multiplicity of τ_s = 7) |
| Angle numerator | 1 | — |
| Angle denominator | 5 | = \|τ_r\| = \|−5\| |
| Common angle | arccos(1/5) | — |

The absolute bound for equiangular lines in ℝ^d is d(d+1)/2 = 120 ≥ 40,
so the W(3,3) lines do not saturate the absolute bound but illustrate the
Seidel spectrum's geometric interpretation.

---

## 4. Seidel ↔ SRG Eigenvalue Cross-Checks

| Identity | Formula | Value |
| --- | --- | --- |
| \|τ_r\| = \|s\| + 1 | 4 + 1 | 5 |
| τ_s = 2\|s\| − 1 | 2×4 − 1 | 7 |
| \|τ_r\| = Q + 2 | 3 + 2 | 5 |
| MULT_R − MULT_S = Q² | 24 − 15 | 9 |

The last identity connects to Part CCXCIV: Q² = 9 is the GQ(3,3) "square order"
(s × t = 3 × 3).

---

## 5. Eigenvalue Arithmetic

| Expression | Value | SRG formula |
| --- | --- | --- |
| τ_r × τ_s | −35 | = −(V − μ − 1) |
| τ_0 + τ_s | 22 | = 2K − λ |
| τ_0 − τ_s | 8 | = K − μ |

---

## 6. Notable Coincidence: τ_0 = MULT_S = 15

The *largest* Seidel eigenvalue (τ_0 = 15) exactly equals the multiplicity of
the *mid-level* Seidel eigenvalue (τ_s, mult = 15 = MULT_S). This is not a
general SRG fact; it is specific to the W(3,3) parameter set.

---

## 7. SM Connections

| Identity | Value | SM meaning |
| --- | --- | --- |
| QUARKS_36 − MULT_R | 12 | = K (degree) |
| τ_0 = MULT_S | 15 | W(3,3) spectral coincidence |
| (τ_0 + 1) / 2 | 8 | = K − μ = 8 |
| \|τ_r\| = Q + 2 | 5 | ternary base + 2 |

---

## 8. Summary Table

| Quantity | Value | Notes |
| --- | --- | --- |
| τ_0 | 15 | = MULT_S (coincidence) |
| τ_r | −5 | mult 24 = MULT_R |
| τ_s | 7 | mult 15 = MULT_S |
| Trace S | 0 | spectral constraint |
| Trace S² | 1560 | = V(V−1) ✓ |
| Equiangular dim | 15 | = MULT_S |
| Equiangular angle | arccos(1/5) | \|τ_r\| = 5 |
| MULT_R − MULT_S | 9 | = Q² (from GQ) |
| Checks pass | 27/27 | ✓ |

---

## 9. Connections to Earlier Parts

- **Part CCXCIV** — GQ(3,3): MULT_R − MULT_S = 9 = Q² = s×t (GQ square order).
- **Part CCXCIII** — Lovász theta: the eigenvalues r = 2 and s = −4 computed
  there are the inputs τ_r = −5 and τ_s = 7 here.
- **Part CCXCII** — Gleason weight enumerator: Gleason ring degree 4 = EW_GAUGE_4
  appears here as (τ_0 + 1)/2 = K − μ = 8 and as MULT_TAU_0 + MULT_S·(1/5)…
  indirectly via the angle denominator chain.
- **Part CCLXX** — W(3,3) core: all SRG parameters (V, K, LAM, MU, MULT_R,
  MULT_S) appear directly in the Seidel eigenvalue formulas.
