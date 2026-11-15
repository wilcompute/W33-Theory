# Pass 12674: degree 8 closes the F₈ code-space gap — certified 64F ≥ 2.498508646 on the T code space; global minimisers sit on two families of four-qubit code spaces; the other track's PPT bound equals degree-6 SOS

Claude track. Follows Pass 12673. **Not a theory of everything.** Global optimality of c₈ is still not proved.

## 0. Correction to Pass 12673

The other track's bound 2.0818 (PPT dual, `2026-11-14_regulus_ppt_dual.md`) holds on the **16-dimensional common four-qubit code space** of S, not on all of C⁶⁴. Pass 12673 compared it with the global degree-6 value 0.760 as if both were global; that sentence is corrected in place. The 0.760 global bound and the code-space bounds measure different things.

## 1. One tool for all code spaces (`w33_f8_codespace_effective_sos.py`)

For an isotropic uncovered Pauli group T of rank r, the code-space objective is

  c(ψ) = Σ_{(x,z)≠0} n(x,z)⟨E_{x,z}⟩²/|ψ|⁴

over ψ ∈ C^{2^{6−r}}, where (x,z) are standard symplectic coordinates of T^⊥/T and n counts covered Paulis per coset.

The SOS for this objective is reduced by the (6 − r)-qubit Pauli group:
- Gram matrices are block-diagonal by Z-character;
- X-shifts relate the blocks (odd degree) or are Fourier-diagonalised inside them (even degree);
- variables live on shift-orbits of monomial pairs, and coefficient matching is sparse.

Validation:
- the effective-model minimum is c₈ for every code space tested;
- **T at degree 6 gives 2.4966772814**, against Pass 12672's 2.4966772779 from independent code (4 s instead of 49 min);
- **S at degree 6 gives 2.0818298**, against the other track's PPT-dual value 2.081828, so their one-versus-two-copy PPT relaxation is numerically the degree-6 SOS bound.

| code space | dim | degree 6 | degree 8 |
|---|---|---|---|
| T (rank 3, Pass 12671) | 8 | 2.4966773 | **2.4985086841** (≥ c₈ within the 4×10⁻⁸ solver tolerance) |
| S type A (Pass 12660's, weights {1: 63, 2: 36}) | 16 | 2.0818298 (= other track's PPT dual) | too large without more symmetry |
| S type B (weights {1: 99, 2: 18}, §3) | 16 | **2.4728769** | too large |

## 2. Exact: 64F ≥ 2.498508646 on the T code space (`w33_f8_codespace_effective_certify.py`)

All target coefficients are integers in the effective model. The certificate is built as follows:
1. SCS at fixed C maximises the PSD margin (192 Fourier blocks of at most 72 real dimensions).
2. Round to denominator 2⁴⁰.
3. **Exact projection.** Each variable enters one class and its conjugate, so each conjugate-class pair gives one real and one imaginary equation, solved in closed form. All 1,800 coefficient equations then hold exactly.
4. **Exact PSD proof** of every block: Y − δI = LLᵀ + E, with dyadic L, exact E and ‖E‖_F < δ.

| C | gap to c₈ | margin | certified |
|---|---|---|---|
| 2.4985 | 8.6×10⁻⁶ | 8.9×10⁻⁶ | yes |
| 2.498508 | 6.5×10⁻⁷ | 6.7×10⁻⁷ | yes |
| 2.4985086 | 4.7×10⁻⁸ | 4.8×10⁻⁸ | yes |
| 2.49850864 | 6.7×10⁻⁹ | 6.9×10⁻⁹ | yes |
| **2.498508646** | **6.9×10⁻¹⁰** | 6.9×10⁻¹⁰ | **yes** |

> **Theorem (exact certificate).** On the 8-dimensional code space of T, 64F ≥ 1249254323/500000000 = 2.498508646. With the exact witness (Pass 12671), the minimum on this code space is c₈ = (47 − 32cos 2π/9)/9 to nine digits, certified on both sides.

The margin equals the gap throughout, so degree 8 is exactly tight. An exact certificate at c₈ itself, with coefficients in Q(cos 2π/9), is the natural next step.

## 3. Where global minimisers live (`w33_f8_global_minimiser_stabilisers.py`)

From 150 random starts in C⁶⁴, 16 runs reach c₈; the others stop at local minima between 2.6848 and 2.785. Every one of the 16 has a Pauli stabiliser of **order exactly 4 with no covered element**. They fall into **two types**, told apart by the covered-weight histogram of the cosets of S′ in S′^⊥:
- **type A (9 of 16):** {0: 156, 1: 63, 2: 36}, Pass 12660's S;
- **type B (7 of 16):** {0: 138, 1: 99, 2: 18}, an inequivalent family, not previously recorded.

> **Numerical reduction.** All global minimisers found lie on 16-dimensional code spaces of uncovered order-4 Pauli groups, of two types. A proof of c₈ along this route would need two things: (i) a proof that every minimiser has such a stabiliser, and (ii) a bound c₈ on both types of 16-dimensional code space. For (ii), degree 6 gives 2.0818 (type A) and 2.4729 (type B), and degree 8 on 16 dimensions needs further symmetry reduction (about 2×10⁶ pair variables with Pauli symmetry alone).

## 4. q = 32 level identification: not done

Identifying 12.489620768 needs about 40 digits, because the candidate field Q(cos 2π/33) has degree 10. At 14 digits, pslq over Q(cos 2π/11) and Q(cos 2π/33) gives only relations that are not significant. A 40-digit refinement needs a high-precision basis of a 16-dimensional eigenspace of a dense 1,024 × 1,024 Clifford, which was not attempted. This stays open.

## Prior art and ownership

- The PPT-dual bound 2.0818 on the common code is the other track's (`toe_20261114_regulus_ppt_dual.py`). Its numerical equality with degree-6 SOS is computed here.
- The code-space structure is Passes 12671–12673. Type-A stabilisers are Pass 12660's.
- The certification method follows Pass 12673 / Pass 12660 (Peyrl–Parrilo-style rounding with exact projection).

## Standalone write-up

A self-contained summary for readers outside the repository (problem, closed form, status table with proved/numerical/open tags, the torus mechanism, the q = 2^k family, and what a proof still needs) is published as a private artifact: https://claude.ai/artifact/ENEQzx4bBuCS1urzExp7o7
