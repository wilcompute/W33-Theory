# Pass 12663: every fibre of Q on a Lagrangian is even (proved); F ≥ 11/250 for type B with an exact certificate

Claude track. Follows Pass 12662. **Not a theory of everything.**

## 1. Parity theorem (`w33_lagrangian_quadric_parity.py`)

Let q = 2^k, Q = x₁z₁ + x₂z₂ on F_q⁴ with polar form B, ω = Tr∘B, and M a Lagrangian (an F₂-subspace of dimension 2k with ω|_M = 0).

> **Theorem.** For every y ∈ F_q the number of v ∈ M with Q(v) = y is even. In particular the number of covered Paulis in a stabiliser group, |M ∩ {Q = 0}| − 1, is odd.

**Proof.**
- Modulo 2, n_y = Σ_{v∈M} (1 + (Q(v) + y)^{q−1}) = Σ_j y^{q−1−j}·Σ_{v∈M} Q(v)^j, since every binomial coefficient C(q−1, j) is odd.
- In F₂-coordinates x on M, Q(v(x))^{2^m} = Σ_i x_i·Q(e_i)^{2^m} + Σ_{i<j} x_i x_j·B_ij^{2^m}, of degree at most 2. So Q^j has degree at most 2·wt(j), where wt is the binary weight.
- The sum over F₂^{2k} of a polynomial of degree below 2k is 0. Only j = q − 1 (weight k) can contribute, through its coefficient of x₁⋯x_{2k}.
- That coefficient is a sum over perfect matchings {e₁, …, e_k} of the Moore determinants det[B_{e_a}^{2^m}]. A Moore determinant vanishes when its arguments are F₂-dependent, and the k values B_e lie in ker Tr, which has dimension k − 1. ∎

**Checks.**
- No odd fibre in 200 to 4,000 sampled Lagrangians for each of q = 2, 4, 8, 16, 32.
- Moore determinants of k random elements of ker Tr are 0; for a basis of F_q the determinant is non-zero.
- Control: non-isotropic 2k-dimensional subspaces do have odd fibres (about half the samples; all of them at q = 2).

This explains why "exactly two covered points" was empty in Pass 12661, and it uses the Lagrangian condition exactly once.

## 2. Exact certificate: F ≥ (11/250)·|v|⁴ for the F₄ regulus (`w33_typeB_exact_certificate.py`)

**Structure.** The coefficient equations of the Pauli-reduced degree-6 SOS split the 51² + 136² = 21,097 Gram entries into **2,601 disjoint groups**, each constrained only through the sum of its entries. Every group's 16 rows carry identical right-hand sides. All of this is verified in the script.

**Construction.**
1. Round the interior solution (Pass 12660) to Gaussian rationals with denominator 2⁴⁰, Hermitian.
2. For each group, add (exact deficit)/(group size) to every entry; the largest correction is 3.6×10⁻¹³.
3. The right-hand side is exact: 256·c_F is an integer vector and δ = 11/250.

**Verified exactly.**
- All 41,616 coefficient equations hold, real and imaginary parts, in Fraction arithmetic.
- Both Gram matrices are exactly Hermitian.
- **Positive definiteness in integer arithmetic.** With R ≈ L⁻¹ (floating Cholesky inverse rounded to denominator 2³⁰), every absolute row sum of R·G·R* − I is below 1: the largest is 3.8×10⁻⁹ for the 51-block and 2.1×10⁻⁸ for the 136-block. So R·G·R* is strictly diagonally dominant, hence G is positive definite.

**Independent end-to-end check** (`tests/test_w33_pass12663.py`): at random v ∈ C¹⁶, F(v)·|v|² − (11/250)·|v|⁶ computed directly from the 80 basis vectors equals the SOS expression built from the stored exact Gram matrices, to relative 10⁻⁹. This validates the bookkeeping that the exact equations rest on.

> **Theorem (computer-assisted, exact).** For the F₄ regulus set of five MUBs in dimension 16 and every v ∈ C¹⁶, F(v) ≥ (11/250)·|v|⁴. Equivalently Σ_t IC_t ≥ 5/16 + 11/250: a certainty relation with collision-entropy deficit at least 0.950 bits.

- The true minimum is 1/16 = 0.0625 numerically; the degree-6 optimum is 0.0452.
- "Type B" (Pass 12648) is identified with this set by two invariants, not by an explicit symplectic map; the theorem is stated for the regulus set.
- The certificate hash and the Gram matrices (as exact fractions) are in `data/w33_typeB_exact_certificate.json` and `…_gram.npz`.

## 3. q = 128 (`w33_regulus_stabiliser_q128.py`)

Annealing over Lagrangians of F₂²⁸ against the prediction (q+1)/3 = 43: see addendum.

## Not attempted

- Closed form of 2.498509 through the 16-dimensional code space.
- Why odd k forbids a one-point Lagrangian. The parity theorem uses all the mod-2 information; the (q+1)/3 pattern needs something else.

## Addendum: q = 128

Three annealing seeds over Lagrangians of F₂²⁸ (fourteen qubits, 129 regulus bases), 1,500 s and about 4.6 million steps each:

| seed | best covered count | last improvement at step |
|---|---|---|
| 0 | 47 | 827,400 |
| 1 | 49 | 3,106,968 |
| 2 | 51 | 172,216 |

- The prediction (q+1)/3 = 43 was **not reached**, and nothing below 43 was seen. So this gives only the upper bound m*(128) ≤ 47; it neither confirms nor refutes the conjecture.
- The runs were still improving slowly, so 47 is not evidence that the minimum is above 43.
- **Parity theorem check:** every one of the 13.8 million Lagrangians visited had an odd covered count.
