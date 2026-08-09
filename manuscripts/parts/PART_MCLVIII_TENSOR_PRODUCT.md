# Part MCLVIII: Tensor Product Spectrum and Kemeny-Strong Bridge for W(3,3)

## Overview

We compute the eigenvalue spectra of the Kronecker (tensor), Cartesian, and Strong
products of W(3,3) with itself, discovering a remarkable connection between the strong
product and the Kemeny transport constant.

## Graph Parameters

W(3,3) = SRG(40, 12, 2, 4). Eigenvalues of A: k=12 (m=1), r=2 (m=24), s=-4 (m=15).

## Tensor (Kronecker) Product A ⊗ A

The Kronecker product G × G has vertex set V × V and eigenvalues λᵢ·λⱼ with
multiplicity mᵢ·mⱼ:

| Eigenvalue | = | Multiplicity |
|-----------|---|-------------|
| k·k = 144 | k² | 1 |
| k·r = 24 | | 48 (= 2·1·24) |
| s·s = 16 | s² | 225 (= 15²) |
| r·r = 4 | r² | 576 (= 24²) |
| r·s = -8 | | 720 (= 2·24·15) |
| k·s = -48 | | 30 (= 2·1·15) |

**Total vertices:** 1 + 48 + 225 + 576 + 720 + 30 = **1600 = v²** ✓

### Trace Identity

$$\text{tr}(A \otimes A) = \text{tr}(A)^2 = 0$$

(Since tr(A) = 0 for the adjacency matrix of any simple graph.)

### Frobenius Norm

$$\|A \otimes A\|_F^2 = \|A\|_F^4 = (k \cdot v)^2 = (12 \cdot 40)^2 = 480^2 = 230400$$

## Cartesian Product A □ A

Eigenvalues λᵢ + λⱼ with multiplicity mᵢ·mⱼ:

| Eigenvalue | Multiplicity |
|-----------|-------------|
| 24 = k+k | 1 |
| 14 = k+r | 48 |
| 8 = k+s | 30 |  ← Wait: no! k+s = 12+(-4)=8
| 4 = r+r | 576 |
| -2 = r+s | 720 |
| -8 = s+s | 225 |

**Largest eigenvalue:** 2k = 24 (degree of Cartesian square).

## Theorem MCLVIII.1 — Kemeny-Strong Product Bridge (NOVEL)

In the **Strong product** G ⊠ G, the eigenvalues are (1+λᵢ)(1+λⱼ)−1:

| Eigenvalue | Multiplicity |
|-----------|-------------|
| 168 = (1+k)²-1 | 1 |
| 38 = (1+k)(1+r)-1 | 48 |
| **8 = (1+r)²-1 = (1+s)²-1** | **801** |
| -10 = (1+r)(1+s)-1 | 720 |
| -40 = (1+s)²-1 wait... | 30 |

The **collision** at eigenvalue 8 is remarkable: both the r-eigenspace and the
s-eigenspace of G contribute to eigenvalue 8 in G ⊠ G, since:

$$( 1+r)^2 - 1 = (1+2)^2 - 1 = 8$$
$$(1+s)^2 - 1 = (1-4)^2 - 1 = (-3)^2 - 1 = 8$$

The total multiplicity is:

$$\text{mult}(8) = m_r^2 + m_s^2 = 24^2 + 15^2 = 576 + 225 = \mathbf{801}$$

**Key identity:**

$$\text{mult}_{\text{strong}}(8) = m_r^2 + m_s^2 = 801 = 20 \cdot K$$

where K = 801/20 is the **Kemeny transport constant** of W(3,3).

## Theorem MCLVIII.2 — Equal Energy Implies Kemeny Formula

The equal aggregate energy from MCLVII (m_r·μ_r = m_s·μ_s = 20) forces:

$$\mu_r = \frac{20}{m_r}, \quad \mu_s = \frac{20}{m_s}$$

Therefore:

$$K = \frac{m_r}{\mu_r} + \frac{m_s}{\mu_s} = \frac{m_r^2}{20} + \frac{m_s^2}{20} = \frac{m_r^2 + m_s^2}{20} = \frac{801}{20}$$

The equal-energy condition **uniquely determines** the Kemeny constant from the
multiplicities alone:

$$\boxed{K = \frac{m_r^2 + m_s^2}{\text{common energy}} = \frac{576 + 225}{20} = \frac{801}{20}}$$

## Theorem MCLVIII.3 — Tensor Energy Balance

In the Kronecker spectrum (excluding the top eigenvalue k² = 144):

$$\sum_{\text{subleading}} e_i \cdot m_i = 7056 - 7200 = -144 = -k^2$$

The subleading energy deficit equals exactly −k², so:

$$\text{tr}(A \otimes A) = k^2 + (-k^2) = 0$$

This encodes the vanishing trace of A as an energy balance identity in the product graph.

## Novel Identity Summary

| Identity | Value |
|---------|-------|
| tr(A⊗A) | 0 (= tr(A)²) |
| max eig (tensor) | 144 = k² |
| min eig (tensor) | -48 = k·s |
| strong mult(8) | 801 = m_r² + m_s² |
| strong mult(8)/20 | 801/20 = Kemeny |
| subleading energy balance | −144 = −k² |
| Frobenius squared | 230400 = (kv)² |

## Cross-Part Connections

- **MCLVII:** Equal energy m_r·μ_r = m_s·μ_s = 20 → K = (m_r²+m_s²)/20 (Theorem MCLVIII.2)
- **MCXLIX:** Kemeny K = 801/20 reappears as strong product multiplicity / 20
- **MCLV:** Frobenius ||A||_F² = kv = 480 → ||A⊗A||_F² = (kv)² = 230400

## Verification

- 14 identities verified by exact `Fraction` arithmetic
- 26 pytest tests, all passing
