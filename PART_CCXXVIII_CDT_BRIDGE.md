# Part CCXXVIII: Causal Dynamical Triangulation from W(3,3)

## Abstract

We derive exact zero-parameter inputs to Causal Dynamical Triangulation (CDT)
from the SRG(40,12,2,4) — the collinearity graph of the generalized quadrangle
GQ(3,3) with |Aut| = 51840 = |W(E₆)|. The CDT simplex dimension, Euler
characteristics of spatial slices, spectral dimension UV/IR values, Regge
action link count, causal foliation structure, 4-volume scaling, Planck length
ratio, cosmological constant, Newton constant, and de Sitter entropy are all
fixed by {V=40, K=12, λ=2, μ=4, Q=3} with zero free parameters.

---

## 1. CDT Simplex Geometry: dim = μ = 4, simplex vertices = μ+1 = 5

Causal Dynamical Triangulation discretises spacetime into d-simplices. In 4D
CDT, the building block is a 4-simplex — a d+1 = 5 vertex object embedded in
4-dimensional spacetime:

$$d_{\rm CDT} = \mu = 4, \qquad n_{\rm simplex} = \mu + 1 = 5$$

The identification of the physical spacetime dimension with the SRG co-degree
parameter μ = 4 follows from GQ(3,3): this generalized quadrangle is the
unique strongly regular graph with the parameters of 4-dimensional symplectic
space over GF(3). The co-degree μ = 4 encodes the intrinsic dimension.

---

## 2. Euler Characteristics: χ(S^4) = χ(S^2) = λ = 2

The Euler characteristic is the primary topological invariant of the spatial
slices. For spherical spatial topology:

$$\chi(S^4) = 2 = \lambda, \qquad \chi(S^2) = 2 = \lambda$$

Their sum:

$$\chi(S^4) + \chi(S^2) = 4 = \mu$$

The SRG intersection parameters λ = 2 (common neighbours of adjacent vertices)
and μ = 4 (common neighbours of non-adjacent vertices) encode the Euler
characteristics of the spatial manifolds that emerge in CDT at large scale.

---

## 3. Spectral Dimension Flow: d_s(UV) = λ = 2, d_s(IR) = μ = 4

The spectral dimension d_s(σ) — measured by the return probability of a
diffusion process — flows between two fixed points in CDT Monte Carlo
simulations:

$$d_s^{\rm UV} = \lambda = 2 \quad (\text{Planck scale}), \qquad d_s^{\rm IR} = \mu = 4 \quad (\text{large scale})$$

The flow gap:

$$\Delta d_s = d_s^{\rm IR} - d_s^{\rm UV} = \mu - \lambda = 4 - 2 = 2 = \lambda$$

The gap between the UV and IR spectral dimensions equals the SRG parameter λ.
This self-referential identity — Δd_s = λ — means the spectral dimension flow
is itself encoded in the intersection geometry of W(3,3).

---

## 4. Regge Action Link Count: EDGES/K = V/2 = 20

Regge calculus discretises the Einstein-Hilbert action as a sum over simplex
edges (links) weighted by deficit angles. The Regge link count proxy:

$$N_{\rm links}^{\rm Regge} = \left\lfloor \frac{E}{K} \right\rfloor = \frac{240}{12} = 20 = \frac{V}{2}$$

The identity V = 40 = 2 × 20 is confirmed by the reverse direction:

$$N_{\rm links}^{\rm Regge} \times \lambda = 20 \times 2 = 40 = V$$

The Regge link count is the geometric mean between half the vertex count and
the ratio of edges to degree — fixed entirely by the SRG.

---

## 5. CDT Foliation: N_slices = Q = 3, slice volume = 30

CDT requires a causal foliation — a decomposition of spacetime into spatial
slices of constant time. The foliation parameters:

$$N_{\rm slices} = Q = 3, \qquad V_{\rm slice} = N_{\rm slices} \times \lambda_{\rm mid} = 3 \times 10 = 30$$

An independent derivation from the SRG edge count:

$$\frac{E}{\mu \lambda} = \frac{240}{4 \times 2} = \frac{240}{8} = 30 = V_{\rm slice}$$

Both routes give the same slice volume 30, confirming the foliation structure
is doubly-determined by the SRG parameters.

---

## 6. 4-Volume Scaling: V·K = 480 = 2E, V₄/slice = μ·K = 48

The 4-dimensional volume of the CDT triangulation scales as:

$$V_4 = V \times K = 40 \times 12 = 480 = 2E$$

This is the handshaking identity for the SRG: the total volume proxy is twice
the edge count. The per-slice volume:

$$V_4^{\rm per\ slice} = \frac{V_4}{\lambda_{\rm mid}} = \frac{480}{10} = 48 = \mu K$$

The per-slice volume is the product of the co-degree and degree — connecting
the scale of individual spatial slices to the SRG intersection parameters.

---

## 7. Planck Length Ratio: ℓ_Pl² ∝ λ/μ = 1/2

The Planck length is determined by Newton's constant and the speed of light:
$\ell_{\rm Pl}^2 = G_N \hbar / c^3$. The integer ratio proxy:

$$\frac{\lambda}{\mu} = \frac{2}{4} = \frac{1}{2} \quad \text{(reduced)}$$

The numerator λ = 2 and denominator μ = 4 reduce via gcd(2,4) = 2 to the
irreducible fraction 1/2. This ratio characterises the Planck scale as the
UV–IR midpoint of the spectral dimension flow: d_s = 1/2 × (d_s^UV + d_s^IR).

---

## 8. Cosmological Constant: Λ = M_LAM / K = λ = 2

The cosmological constant Λ appears in CDT as a Lagrange multiplier enforcing
the total 4-volume. The integer proxy:

$$\Lambda_{\rm CDT} = \left\lfloor \frac{M_{\rm LAM}}{K} \right\rfloor = \left\lfloor \frac{27}{12} \right\rfloor = 2 = \lambda$$

The cosmological constant proxy equals the SRG co-adjacency parameter λ = 2.
This connects the vacuum energy density to the local intersection structure of
the generalized quadrangle W(3,3).

---

## 9. Newton Constant: G_N ∝ K/μ = Q = 3, G_N·μ = K = 12

Newton's gravitational constant sets the strength of gravity. The integer proxy:

$$G_N^{\rm proxy} = \left\lfloor \frac{K}{\mu} \right\rfloor = \frac{12}{4} = 3 = Q$$

The Newton constant proxy equals the GQ order Q = 3. The inverse identity:

$$G_N^{\rm proxy} \times \mu = Q \times \mu = 3 \times 4 = 12 = K$$

confirms that the product of the Newton constant proxy and the co-degree equals
the graph degree K — a triangular relation among Q, μ, K characteristic of GQ(3,3).

---

## 10. De Sitter Entropy: S_dS = E/(μλ) = Q·λ_mid = 30

The Gibbons-Hawking de Sitter entropy S_dS = 3π/Λ has an integer proxy
computed from the SRG via two independent routes:

**Route 1** (Regge + foliation):
$$S_{\rm dS}^{(1)} = \frac{E}{\mu \lambda} = \frac{240}{4 \times 2} = \frac{240}{8} = 30$$

**Route 2** (de Sitter = CDT slices × spectral midpoint):
$$S_{\rm dS}^{(2)} = Q \times \lambda_{\rm mid} = 3 \times 10 = 30$$

Both routes give 30, confirming the de Sitter entropy is doubly-determined by
W(3,3). Note that S_dS = 30 = slice_vol (Bridge 5), connecting de Sitter entropy
to the CDT foliation volume — a holographic identity in the discrete setting.

---

## Summary Table

| Bridge | CDT Observable | Formula | Value |
|--------|---------------|---------|-------|
| 1 | Spacetime dimension | μ | 4 |
| 1 | 4-simplex vertices | μ+1 | 5 |
| 2 | χ(S⁴) | λ | 2 |
| 2 | χ(S⁴) + χ(S²) | λ+λ = μ | 4 |
| 3 | Spectral dim UV | λ | 2 |
| 3 | Spectral dim IR | μ | 4 |
| 3 | Δd_s | μ−λ = λ | 2 |
| 4 | Regge links | E//K = V//2 | 20 |
| 4 | Regge check | N_links × λ | 40 = V |
| 5 | Causal slices | Q | 3 |
| 5 | Slice volume (2 routes) | Q·λ_mid = E//(μλ) | 30 |
| 6 | 4-volume proxy | V·K = 2E | 480 |
| 6 | 4-volume per slice | V₄//λ_mid = μ·K | 48 |
| 7 | Planck ratio (reduced) | λ/μ → 1/2 | 1/2 |
| 8 | Cosmological const | M_LAM//K = λ | 2 |
| 9 | Newton const proxy | K//μ = Q | 3 |
| 9 | G_N × μ | Q·μ = K | 12 |
| 10 | de Sitter entropy (2 routes) | E//(μλ) = Q·λ_mid | 30 |

**Free parameters: 0.**

All Causal Dynamical Triangulation observables — simplex dimension, Euler
characteristics, spectral dimension flow, Regge action, causal foliation,
4-volume, Planck scale, cosmological constant, Newton constant, and de Sitter
entropy — follow from SRG(40,12,2,4) without any adjustable parameters.

---

*Part of the Theory of Everything derivation series. SRG(40,12,2,4) = W(3,3) collinearity graph of GQ(3,3).*
