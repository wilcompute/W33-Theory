# Pass 12669: the nine-basis F₈ regulus constant is (47 − 32 cos(2π/9))/9; Haemers matrices of rank 10 for W(3,3), none of rank 9

Claude track. Follows Pass 12668. **Not a theory of everything.**

## 1. A closed form for the non-stabiliser certainty constant (`w33_f8_constant_high_precision.py`)

The F₈ regulus set is nine mutually unbiased bases of C⁶⁴ (six qubits); Passes 12657–12661 cover it. Its constant c₈ = 64·min F was known numerically: 2.498508646688 (Passes 12658–12662), with exact bounds 2.0818 (PPT dual, other track, common code) and a rational witness 2.4985086592 (other track).

**High precision.** Newton's method in mpmath (60 digits) on the Riemannian gradient, with a pseudo-inverse Hessian since the minimum is degenerate along symmetry orbits, started from the saved minimiser. The gradient norm went 5.9×10⁻⁹ → 1.5×10⁻¹⁴ → 1.3×10⁻²⁷ → 1.7×10⁻⁵⁴ (quadratic convergence):

c₈ = 2.49850864668807809705815946469185182600592904…

**Integer relation.** `mpmath.findpoly` (degree ≤ 12, coefficients ≤ 10⁷) returns, at degree 3,

**243 c³ − 3807 c² + 17577 c − 23941 = 0**, with residual 4.6×10⁻⁴².

- The discriminant is 2²⁴·3¹², a perfect square, so the cubic is cyclic (Galois group Z/3).
- With c = (y + 47)/9 it becomes y³ − 768y − 4096 = 0, and y = 32 cos θ turns this into cos 3θ = 1/2. Its three roots are therefore

  **c ∈ {(47 + 32 cos(2π/9 + 2πk/3))/9}**, and **c₈ = (47 − 32 cos(2π/9))/9** (the smallest; the others are 4.6048… and 8.5634…).

> **Identification.** For the nine F₈-regulus MUBs in dimension 64, min F = (47 − 32 cos(2π/9))/576 ≈ 0.0390392, and by the quotient lemma (Pass 12659) and the numerical equality of Pass 12658 the two five-qubit quotient 9-sets have min F = (47 − 32 cos(2π/9))/288.

**Status.** A numerical identification at 45 digits, not a proof. A random cubic relation with coefficients up to 2.4×10⁴ matching 45 digits has probability around 10⁻²⁷.
- It is consistent with every exact bound in the repository: 2.0818 ≤ c₈ (PPT dual) ≤ 2.49850865922 (rational witness) and < 3 (exhaustive stabiliser minimum).
- A proof would need an exact minimiser over Q(ζ₉) and a matching lower bound.

**Why 2π/9.** q + 1 = 9 is the number of bases, and the norm-one torus of F₆₄ (the kernel of the norm F₆₄* → F₈*) is cyclic of order 9. The appearance of the real subfield of Q(ζ₉) is suggestive; no mechanism is derived here. The same field Q(cos 2π/9) appears in earlier repository work on two-qutrit fidelity levels (Pass 11253) and magic (Pass 11149), in different problems.

**Comparison.** For q = 2, 4, 16 the constant is the stabiliser value 1, which is rational. At q = 8 the optimum is a non-stabiliser state whose value lies in the real cyclotomic field of the order-9 torus.

## 2. Shannon capacity: subgroup-invariant Haemers matrices (`w33_haemers_invariant_search.py`)

Haemers' bound Θ ≤ rank(M), for M with nonzero diagonal and zeros on non-adjacent pairs, was searched over matrices invariant under subgroups H of Aut(W(3,3)):
- exhaustive over F₂ when H has at most 18 free orbital coefficients, annealing over F₃ otherwise;
- 29 subgroups (orders 20 to about 6,000) over two seeds;
- control: the 27-line meeting graph gives rank 7, matching Haemers' classical example.

| best rank | subgroup order | free orbitals | field |
|---|---|---|---|
| **10** | 120 | 7 | F₂ (exhaustive) |
| **10** | 720 | 4 | F₂ (exhaustive) |
| 11 | 576 | 7 | F₃ |

- Rank-10 Haemers matrices exist, improving the fully symmetric A + cI value of 11 and **tying the Lovász bound ϑ = 10**.
- **No rank-9 matrix was found**, so Θ(W(3,3)) < 10 is not established. The interval remains √60 ≤ Θ ≤ 10.
- The search covers only these subgroups, so this is evidence, not a proof that the Haemers bound equals 10.

The long low-symmetry code searches (Pass 12668 §4) ended at 58 (order 2 and order 3 classes) and 56 (order 4, optimal), so √60 stands.
