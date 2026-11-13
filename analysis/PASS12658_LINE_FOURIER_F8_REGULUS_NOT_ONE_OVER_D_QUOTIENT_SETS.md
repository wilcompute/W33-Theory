# Pass 12658: F is a sum of line-Fourier 4-norms on AG(2,q); the F₈ regulus and its five-qubit quotients have min F = 2.4985/d, not 1/d; degree-6 SOS gives F ≥ 0.0452 for type B

Claude track. Follows Pass 12657. **Not a theory of everything.**

## 1. Line-Fourier form (`w33_regulus_f8_and_quotient.py`)

For the F_q regulus set (Pass 12657), let A(x₁, x₂) be the amplitudes and B the row-wise F_q-Fourier transform of A. Then

> **F + (q+1)/q² = Σ over the q(q+1) affine lines ℓ of AG(2,q) of ‖𝔉_ℓ(B|_ℓ)‖₄⁴**,

where 𝔉_ℓ is the additive Fourier transform on the line. Residuals: 9×10⁻¹⁶, 0, 2×10⁻¹⁶ for q = 2, 4, 8.

- All q + 1 bases are on the same footing: lines of slope t give basis B_t, and vertical lines give the computational basis.
- Each term is ≥ ‖B|_ℓ‖⁴/q. Summing gives exactly the trivial bound F ≥ 0, with equality iff |B| is constant and every line restriction has a flat Fourier transform.
- So strong unextendibility of the regulus set is the statement that **no unimodular function on AG(2,q) is "bent" on every line**, with a quantitative gap.

For q = 4 this is equivalent to the pairing identity of Pass 12657, and in real form: with u_p ∈ R² the 16 planar vectors (B_p as real pairs), F = Σ|u_p|⁴ − 1/16 + Σ_{ℓ,π}(u_a·u_b + u_c·u_d)². That is a quadratic form in the Gram matrix of 16 vectors in the plane; without the rank-2 constraint its minimum is the trivial one.

## 2. The F₈ regulus is not a 1/d set (`w33_regulus_minF_gradient.py`)

Analytic-gradient minimisation in the CZ model (gradient check 10⁻⁶; controls q = 2 → 1/4 and q = 4 → 1/16 on 30 and 200 starts, every start reaching the minimum):

| q | d | min F | F·d | starts |
|---|---|---|---|---|
| 2 | 4 | 0.25 | 1.000000 | 30 |
| 4 | 16 | 0.0625 | 1.000000 | 200 |
| 8 | 64 | 0.039039197604501 | **2.498508646688** | 300 |

- At q = 8 the lowest six values agree to 15 digits; the next level is 2.685/64.
- **The F₈ regulus has min F ≈ 2.4985/64, about 2.5 times the stabiliser-type value 1/64**, and the optimum is not a multiple of 1/64, so it is not attained at a stabiliser state.
- The constant is unidentified: no polynomial of degree ≤ 4 with coefficients ≤ 200 and no relation with cos(2πj/7) was found at the 14 available digits.
- This corrects an expectation carried since Pass 12651: "every 2^⌈n/2⌉+1 set tested has min F = 1/d" was a statement about the sets found by search. The six-qubit set of Pass 12651 (1/64) and the F₈ regulus (2.4985/64) are inequivalent 9-sets (Pass 12657) with different constants.

## 3. Five-qubit quotients of the F₈ regulus (same script; `w33_five_qubit_quotient_sets_minF.py`)

Kantor's Lemma 6.1, executed: for a point p with Tr Q(p) = 1 (an antisymmetric Pauli), project the nine Lagrangians to p⊥/⟨p⟩ ≅ W(9,2).
- **All 6 sampled p give a maximal partial spread of size 9** (0 extendible T among 13,888). Control: Q₀-singular uncovered p do not even give disjoint images.
- Two spectral types of uncovered graph appear: both 368-regular with 16²³³ and (−16)²⁴⁸, then either two eigenvalues of multiplicity 27 or ±8 with multiplicity 17. Each has only **one** simple eigenvalue.
- The Pass 12650 set has 16²²⁵, (−16)²⁴⁸ and **271** simple eigenvalues. So there are **at least three inequivalent five-qubit 9-sets**.
- **min F** (40 starts each, analytic gradient):

| five-qubit 9-set | min F | F·32 |
|---|---|---|
| Pass 12650 (search) | 0.03125 | 1.0000 |
| regulus quotient, type 27 | 0.078078395209 | **2.498508646688** |
| regulus quotient, type 17 | 0.078078395209 | **2.498508646688** |

- The quotients inherit **the same constant** as the F₈ regulus to 13 digits. This is the reverse of the type B lift (Pass 12648), and is numerical: no proof of F_quotient·32 = F_regulus·64 was written.
- So the smallest five-qubit unextendible sets differ in strength by a factor 2.5. The strongest known has min F ≈ 0.0781.

## 4. Degree-6 SOS for type B (`w33_typeB_degree6_sos.py`)

Port of the three-qubit Pauli-reduced SOS (Pass 12647) to d = 16: Gram blocks 51 and 136.
- Control (two bases only, true minimum 0): δ = −2×10⁻⁸.
- **Type B: δ = 0.045156** (SCS, optimal, eps 10⁻⁷).
- So F ≥ 0.0452 for the F₄ regulus at degree 6, against the true 0.0625. This is a floating-point SDP value, not an exactly rounded certificate.
- It improves the Lovász bound (ϑ = 14.609 gives 0.0244) but does not close. At three qubits degree 6 was essentially tight; here it is not.

## Open

- The constant 2.498508646688 (closed form; why the quotient preserves it).
- A proof of 1/16 for type B: decomposable level gives 0, degree 6 gives 0.0452.
- Is 2.4985/32 the largest min F among five-qubit 9-sets?

## 5. Shannon codes with larger symmetry: nothing new (`w33_shannon_group_codes.py`)

80 runs over random two-generator diagonal subgroups of order ≤ 240 (with and without a conjugation twist), each solved to optimality:
- best sizes by group order: 49 (order 9), 48 (order 18), 16 (orders 24, 48, 72), ≤ 1 for the rest sampled (6, 8, 60, 80, 81);
- nothing beats the Z₅ code of size 60.

This is a small, weak sample: the groups sampled did not include dihedral groups of order 10 or 20. Θ(W(3,3)) stays in [√60, 10].

## 6. Paper

`papers/strongly_unextendible_pauli_mubs.tex` gains Proposition "regulus sets": the explicit construction, the line-Fourier and AG(2,4) identities, the type B identification, the degree-6 value 0.0452, and the q = 8 constant with its five-qubit quotients. The sentence that minimal sets have min F = 1/d is now restricted to the sets found by search.
