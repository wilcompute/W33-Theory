# Part MCLIV: Bose-Mesner Algebra Recurrence for W(3,3)

## Overview

Every power A^n of the adjacency matrix of W(3,3) = SRG(40, 12, 2, 4) lies in
the three-dimensional Bose-Mesner algebra spanned by {I, A, J}. The recurrence
coefficients a_n, b_n, c_n satisfy an exact linear recurrence with rational
coefficients determined solely by the SRG parameters.

## Parameters and Algebra Basis

SRG parameters: (v, k, λ, μ) = (40, 12, 2, 4), eigenvalues r=2, s=−4.

Bose-Mesner decomposition: A^n = a_n · I + b_n · A + c_n · J

Recurrence constants: α = k − μ = 8, β = λ − μ = −2.

## Theorem MCLIV.1 — Fundamental SRG Identity (n=2)

$$A^2 = 8I - 2A + 4J$$

Explicitly: (A²)_{ii} = k = 12 ≡ k (diagonal), (A²)_{ij} = λ = 2 for adjacent, μ = 4 for non-adjacent.
This reads: a_2 = 8, b_2 = −2, c_2 = 4.

## Theorem MCLIV.2 — Linear Recurrence System

The coefficients satisfy:

$$a_{n+1} = \alpha \cdot b_n = 8 b_n$$
$$b_{n+1} = a_n + \beta \cdot b_n = a_n - 2 b_n$$
$$c_{n+1} = \mu \cdot b_n + k \cdot c_n = 4 b_n + 12 c_n$$

Initial conditions: (a_0, b_0, c_0) = (1, 0, 0); (a_1, b_1, c_1) = (0, 1, 0).

## Theorem MCLIV.3 — First Six BM Coordinates

| n | a_n | b_n | c_n |
|---|-----|-----|-----|
| 0 | 1 | 0 | 0 |
| 1 | 0 | 1 | 0 |
| 2 | 8 | −2 | 4 |
| 3 | −16 | 12 | 40 |
| 4 | 96 | −40 | 528 |
| 5 | −320 | 176 | 6176 |

## Theorem MCLIV.4 — Closed Form for b_n

The b_n coefficient has the closed form:

$$b_n = \frac{r^n - s^n}{r - s} = \frac{2^n - (-4)^n}{6}$$

This is the "Fibonacci-like" formula for the SRG eigenvalue pair (r, s) = (2, −4).

Explicit: b_0 = 0, b_1 = 1, b_2 = −2, b_3 = 12, b_4 = −40, b_5 = 176.

## Theorem MCLIV.5 — a_n From b_n

$$a_n = \alpha \cdot b_{n-1} = 8 \cdot b_{n-1} = \frac{8(2^{n-1} - (-4)^{n-1})}{6} = \frac{4(2^{n-1} - (-4)^{n-1})}{3}$$

## Theorem MCLIV.6 — Minimal Polynomial Identity

$$A^3 = 10 A^2 + 32 A - 96 I$$

Equivalently, the minimal polynomial of A divides x³ − 10x² − 32x + 96 = (x−12)(x−2)(x+4).
Verified: a_3·I + b_3·A + c_3·J = −16I + 12A + 40J
and 10·(8I − 2A + 4J) + 32·(0·I + 1·A + 0·J) − 96·I
= 80I − 20A + 40J + 32A − 96I
= −16I + 12A + 40J ✓

## Theorem MCLIV.7 — Normalized Traces

$$B_2 = \frac{\text{tr}(A^2)}{v} = \frac{a_2 \cdot v + 0 + c_2 \cdot v^2}{v} / \text{(via eigenvalue formula)} = k = 12$$

Exact: tr(A^n) = a_n · v + k · b_n · v/k · 0 + ... → trace from spectral formula = k^n + m_r · r^n + m_s · s^n.

| n | B_n = tr(A^n)/v | Value | Interpretation |
|---|-----------------|-------|----------------|
| 2 | k | 12 | degree |
| 3 | λ·k | 24 | λ × degree |

## Connection to Prior Parts

| Bridge | Equation |
|--------|----------|
| To MCLIII (Ihara Zeta) | tr(A^3) = 960 = 6 × triangle_count = 6 × 160 |
| To MCXLVII (CTQW) | A^n amplitudes from same b_n recurrence |
| To MCLV (Laplacian Zeta) | Laplacian = kI − A, BM coordinates of (kI−A)^n follow |

## Physical Interpretation

The Bose-Mesner algebra recurrence for A^n is the exact nonlinear dynamics engine
for W(3,3): it shows that all matrix powers remain within the three-dimensional
algebra {I, A, J}. The closed form b_n = (2^n − (−4)^n)/6 encodes the
alternating oscillation between the two non-trivial eigenvalues r=2 and s=−4.
The ratio |s/r| = 2 gives a "2:1 eigenvalue amplitude ratio" analogous to a
discrete harmonic oscillator with eigenfrequency ratio 2.
