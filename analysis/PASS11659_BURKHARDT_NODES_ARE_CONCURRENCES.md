# Pass 11659 — the 45 Burkhardt nodes are the 45 two-qutrit determinants, and every factorisation frame obeys a monogamy sum rule

Producer: `analysis/w33_pass11659_burkhardt_nodes_are_concurrences.py`
Certificate: `data/w33_pass11659_burkhardt_nodes_are_concurrences.json`
Regression: `tests/test_w33_pass11655_11662.py`

## Nodes are determinants

The unit root n_F of the reflection of a tensor factorisation F is a Burkhardt node (Pass 11657). For the standard
factorisation, with the root's phase fixed,

> **⟨n_F, u(ψ)⟩ = det(ψ_F)**, where ψ_F is the 3×3 coefficient matrix.

* **Exact.** The ratio is 1.000 with spread 5·10⁻¹⁵ over 300 random states.
* **All 45 factorisations.** The other factorisations follow by Clifford covariance.
* **What det is.** det(ψ_F) is the SL(3) × SL(3)-invariant cubic, and its modulus^{2/3} is Gour's **G-concurrence** of
  two qutrits.

**Consequences.**
* **Products.** The node of F annihilates every F-product state (max 3·10⁻¹⁷ over 500).
* **Maximal entanglement.** |det_F|² ≤ 1/27, with equality exactly at maximal F-entanglement, i.e. Schmidt coefficients
  (1/3, 1/3, 1/3).
* **Relations.** The **45 determinants of the 45 factorisations span only a 5-dimensional space** (rank 5), so they
  satisfy **40 linear relations**. The Burkhardt/Coble space is the span of the qutrit concurrences.

## The monogamy sum rule

**Frames are orthonormal bases.** Five mutually orthogonal nodes are a line of GQ(4,2). There are exactly **27** such
frames, Pass 11177's complete factorisation frames, and each is an orthonormal basis of the Hesse space. Hence, for
**every** frame and every two-qutrit state,

> **Σ_{F ∈ frame} |det_F ψ|² = |u(ψ)|² = (M₃ − 2)/6 ≤ 1/9.**

* Here M₃ is the stabiliser third moment (Gross–Nezami–Walter; Pass 11651).
* Checked on all 27 frames × 200 states, maximum error 1.3·10⁻¹⁵.
* The bound 1/9 is attained exactly on stabiliser states.

**A monogamy relation for qutrit concurrence.**
* At most 3 of the 5 factorisations of a frame can be maximally entangled at once. Since 3/27 = 1/9, three maximal
  determinants saturate the rule, and this is achieved (1/27, constrained optimisation).
* Four factorisations of one frame reach at most ≈ 0.01563 each, numerically, well below the sum-rule bound of 1/36.

## A tested non-result

Two factorisations can be simultaneously maximally entangled (both |det|² = 1/27), whether their nodes are orthogonal
or overlap 1/4.
* An unconverged Nelder–Mead run first suggested a gap for orthogonal pairs.
* A constrained SLSQP optimiser converges to 1/27 in both cases.
* Per the repo's lesson on solver hit rates, the earlier gap is withdrawn.

## Reading

**One identification.** The two-qutrit Hesse space is the span of the determinants of the 45 tensor factorisations.
* The nodes of the Burkhardt quartic are those determinants, i.e. the qutrit G-concurrences.
* The 27 lines of GQ(4,2), i.e. the 27 lines of the cubic surface of the W(E₆) dictionary, are orthonormal frames of
  concurrences.
* Their squared moduli sum to the stabiliser third moment.

**What it unifies.**
* Pass 11177's "perfect gates move a factorisation to a collinear one" (= orthogonal nodes, Pass 11657).
* The Gross–Nezami–Walter stabiliser moment.
* Gour's concurrence.

**Scope.**
* The node = determinant identity and the sum rule are exact to machine precision.
* The 3-of-5 and 4-of-5 statements come from a converged constrained optimisation.

**Prior art.** Gour's G-concurrence (2005), Gross–Nezami–Walter (2017), the classical Burkhardt configuration, and the
Holotrade/Pass 11177 factorisation dictionary.
