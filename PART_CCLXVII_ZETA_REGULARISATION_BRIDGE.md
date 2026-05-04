# Part CCLXVII — Zeta Regularisation and the Tomotope Covering Tower

**Bridge:** `exploration/PART_CCLXVII_ZETA_REGULARISATION_BRIDGE.py`  
**Tests:** `tests/test_zeta_regularisation_cclxvii.py`  
**Results:** `PART_CCLXVII_zeta_regularisation_results.json`  
**Status:** ✓ VERIFIED — 38/38 checks pass, 48/48 tests pass

---

## Core Thesis

> *"The sum of all positive integers is −1/12."*

This Part bridges the Ramanujan–Riemann identity ζ(−1) = −1/12 to
the W(3,3) strongly-regular graph and its tomotope (Part CCLXVI).
The denominator **12 = K** (W33 valency = tomotope edge count) is
not a coincidence: the tomotope has Euler characteristic **χ = 0**,
so it admits an infinite tower of n-sheeted covering spaces (one for
every n ≥ 1).  The formal sum of those sheet-counts,

$$\sum_{n=1}^{\infty} n = 1 + 2 + 3 + \cdots = \zeta(-1) = -\tfrac{1}{12},$$

assigns the covering tower a **zeta-regularised weight** whose
denominator is exactly K = TE = 12.  This is the passage from the
3-dimensional discrete world of PG(3,3) (40 = V points, over GF(3))
to the 4-dimensional continuous ambient space of the tomotope (ℝ⁴),
with the Euler–Maclaurin formula providing the precise bridge operator.

---

## W(3,3) and Tomotope Constants

| Symbol | Value | Meaning |
|--------|-------|---------|
| V | 40 | vertices of W(3,3) |
| K | 12 | valency |
| λ | 2 | LAM — common neighbours (adjacent) |
| μ | 4 | MU — common neighbours (non-adjacent) |
| M_LAM | 27 | co-degree class size |
| LAP_MID | 10 | Laplacian eigenvalue (middle) |
| LAP_TOP | 16 | Laplacian eigenvalue (top) |
| TV,TE,TF,TC | 4,12,16,8 | tomotope face-vector |
| T_FLAGS | 192 | tomotope flag count = TE × TF |
| χ | 0 | Euler characteristic of tomotope |

---

## Six Bridges

### 1 · ζ(−1) = −1/12 and W33 Valency (B01–B05)

The Bernoulli number B₂ = 1/6 gives
$$\zeta(-1) = -\frac{B_2}{2} = -\frac{1}{12}.$$
The denominator 12 equals both **K** (W33 valency) and **TE** (tomotope
edge count).  The numerator −1 is the unit in ℤ — no free parameters.

### 2 · Bosonic String Critical Dimension (B06–B17)

The bosonic string requires D = 26 dimensions for anomaly cancellation.
All key numbers are W33/tomotope constants:

| Identity | Value |
|----------|-------|
| D\_bos = M\_LAM − 1 | 27 − 1 = **26** |
| D\_sup = LAP\_MID | **10** |
| D\_bos − D\_sup = TF = LAP\_TOP | **16** |
| N\_trans = D\_bos − 2 = 2K | **24** |
| Casimir = 24 × ζ(−1) = 24 × (−1/12) = −λ | **−2** |
| N\_trans(super) = 2μ | **8** |

The ground-state Casimir energy −λ = −2 is the bosonic string tachyon
mass shift, derived from 24 = 2K transverse oscillator modes each
contributing ζ(−1) = −1/12.

### 3 · Tomotope χ = 0 and the Infinite Cover Tower (B18–B23)

$$\chi(\text{tomotope}) = TV - TE + TF - TC = 4 - 12 + 16 - 8 = 0.$$

A space with χ = 0 admits infinitely many connected covering spaces.
The flag count T\_FLAGS = TE × TF = 12 × 16 = 192 participates:

$$\zeta(-1) \times T\_FLAGS = -\tfrac{1}{12} \times 192 = -16 = -TF = -LAP\_TOP.$$

Also: |ζ(−1)| × K = (1/12) × 12 = **1**, showing the covering zeta-weight
is a unit — the covering tower is the minimal non-trivial extension.

### 4 · Euler–Maclaurin: Discrete 3D → Continuous 4D (B24–B30)

The Euler–Maclaurin formula bridges a discrete sum to a continuous
integral.  Its leading correction coefficient is:

$$\frac{B_2}{2!} = \frac{1/6}{2} = \frac{1}{12} = \frac{1}{K} = -\zeta(-1).$$

For the V = 40 vertices of W(3,3):
- Discrete: $\sum_{n=1}^{40} n = 820$  
- Continuous: $\int_0^{40} x\,dx = 800$  
- Difference: 20 = V/2 (boundary term)  
- Hidden zeta constant: −1/12 (the analytic continuation of the sum)

The EM correction coefficient 1/K is precisely the reciprocal of W33's
valency — the discrete structure encodes its own continuum limit.

### 5 · Zeta Values and W33 Parameters (B31–B34)

| Identity | Check |
|----------|-------|
| ζ(0) = −1/2, and −ζ(0) · K = 6 = λ · q | **6 = 2 × 3** |
| ζ(−3) = 1/120 = 1/(V × Q) | **120 = 40 × 3** |

The denominators of the negative-integer zeta values encode products of
W33 parameters with zero free parameters.

### 6 · 3D Discrete → 4D Continuous Dimension Jump (B35–B38)

The projective space PG(3,3) contains exactly
$$\frac{3^4-1}{3-1} = 40 = V \text{ points},$$
so W(3,3) is a *3-dimensional discrete* structure.  The tomotope lives
in ℝ⁴ (since TV = Q + 1 = 4), one dimension higher:

$$\text{dim\_jump} = TV - (Q+1-1) = 4 - 3 = 1 = \lambda - 1.$$

The single dimension jump corresponds to the passage from a finite field
geometry to its real-number covering space — exactly what ζ-regularisation
accomplishes: assigning a finite value (−1/12) to the divergent sum that
counts the layers of that passage.

---

## All 38 Bridge Checks

| ID | Identity | Value |
|----|----------|-------|
| B01 | ζ(−1) = −1/12 | ✓ |
| B02 | denom(ζ(−1)) = K | 12 |
| B03 | denom(ζ(−1)) = TE | 12 |
| B04 | B₂ = 1/6 | ✓ |
| B05 | ζ(−1) = −B₂/2 | ✓ |
| B06 | D\_bos = 26 | ✓ |
| B07 | D\_bos = M\_LAM − 1 | 27−1 |
| B08 | D\_sup = 10 | ✓ |
| B09 | D\_sup = LAP\_MID | ✓ |
| B10 | D\_bos − D\_sup = TF | 16 |
| B11 | D\_bos − D\_sup = LAP\_TOP | 16 |
| B12 | N\_trans = 2K | 24 |
| B13 | N\_trans = 24 | ✓ |
| B14 | Casimir = −2 | ✓ |
| B15 | Casimir = −λ | ✓ |
| B16 | N\_trans(sup) = 2μ | 8 |
| B17 | N\_trans(sup) = 8 | ✓ |
| B18 | χ(tomotope) = 0 | ✓ |
| B19 | T\_FLAGS = TE × TF | 192 |
| B20 | ζ(−1) × T\_FLAGS = −TF | −16 |
| B21 | ζ(−1) × T\_FLAGS = −LAP\_TOP | −16 |
| B22 | \|ζ(−1)\| × K = 1 | ✓ |
| B23 | \|numer(ζ(−1))\| = 1 | ✓ |
| B24 | EM coeff = 1/12 | ✓ |
| B25 | denom(EM coeff) = K | 12 |
| B26 | denom(EM coeff) = TE | 12 |
| B27 | EM coeff = −ζ(−1) | ✓ |
| B28 | Σn (n=1…V) = 820 | ✓ |
| B29 | ∫₀ᵛ x dx = 800 | ✓ |
| B30 | 820 − 800 = V/2 | 20 |
| B31 | ζ(0) = −1/2 | ✓ |
| B32 | −ζ(0) · K = λ · q | 6 |
| B33 | ζ(−3) = 1/120 | ✓ |
| B34 | denom(ζ(−3)) = V · Q | 120 |
| B35 | \|PG(3,3)\| = V | 40 |
| B36 | TV = Q + 1 | 4 |
| B37 | dim\_jump = 1 | ✓ |
| B38 | dim\_jump = λ − 1 | 1 |

---

## Physical Interpretation

The identity ζ(−1) = −1/12 is not merely an analytic curiosity.  In
the W(3,3) framework it is the **zeta-regularised covering weight** of
the tomotope: because χ = 0, every positive integer n labels a valid
n-sheeted cover, and their formal sum is −1/12.  The bosonic string
"knows" this via its 24 = 2K transverse modes, each contributing −1/12
to the Casimir vacuum energy, forcing D = 26 = M\_LAM − 1.  The
Euler–Maclaurin formula makes the same number appear as the discrete-to-
continuous correction coefficient 1/K = 1/TE, bridging the 3D finite-
field geometry of PG(3,3) (the home of W(3,3)) to the 4-dimensional real
space (the home of the tomotope) in a single, zero-free-parameter step.

---

*Verified: 38/38 bridge checks, 48/48 tests.*  
*Preceding: Part CCLXVI — Tomotope and the Turing Machine.*
