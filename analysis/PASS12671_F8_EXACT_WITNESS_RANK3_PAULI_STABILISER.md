# Pass 12671: an exact six-qubit state attaining c₈ = (47 − 32 cos(2π/9))/9 — the F₈ regulus minimum lives in a three-qubit Pauli code space

Claude track. Follows Pass 12669. **Not a theory of everything.** The upper bound is now exact; optimality (the lower bound) is still numerical.

## Summary

For the nine F₈-regulus MUBs of C⁶⁴, Pass 12669 identified c₈ = 64·min F = (47 − 32 cos(2π/9))/9 numerically (45 digits) but found no exact witness: the minimiser it had sat in a positive-dimensional family whose Pauli expectations were not algebraic. This pass finds a canonical point of that family and proves the upper bound exactly.

> **Theorem (exact, computer-verified).** There is a pure six-qubit state ρ, with all Pauli expectations in Q(cos 2π/9, √3), such that 64·F(ρ) = (47 − 32 cos(2π/9))/9. Hence c₈ ≤ (47 − 32 cos(2π/9))/9 exactly.
>
> **Numerical.** This is the minimum (Passes 12658–12669; 45-digit agreement). The best exact lower bound remains 2.0818 (PPT dual).

The previous best exact upper bound was the other track's rational witness 2.49850865922, 1.3×10⁻⁸ above.

## 1. The order-9 idea fails, informatively (`w33_f8_order9_reduction.py`)

The constant's 2π/9 suggested the order-9 elements of SL(2,8), which cycle the nine regulus lines. In the CZ model every g ∈ GL(2,8) acts as a pure index permutation x ↦ xg of C⁶⁴.
- All 3,528 elements of GL(2,8) preserve F (checked on random states).
- No ζ₉-eigenspace of an order-9 element attains c₈. The eigenspace minima are **37/3** (j = 0, dim 8) and **47/9** (j ≠ 0, dim 7).
- 47/9 is c₈ with the cosine term removed. This is noted, not explained.
- The same holds for every cyclic class of GL(2,8) (orders 2, 3, 7, 9, 14, 21, 63; 37 classes, all eigenvalues). The best restricted value is 2.7756 (order 3).
- So the minimum breaks every linear symmetry, even every involution. The 2π/9 does not come from a symmetry of the state.

## 2. The symmetry is a Pauli stabiliser (`w33_f8_pauli_stabiliser_ladder.py`)

Pass 12660 (`w33_f8_minimiser_structure.py`) found that the numerical minimiser has a Pauli stabiliser of order 4 whose non-identity elements are all uncovered. That is the starting point here.

| stabiliser rank | code space dim | groups tested | attaining c₈ |
|---|---|---|---|
| 2 (S of Pass 12660) | 16 | 1 (40 random starts) | 40/40 starts |
| 3 (S + one coset of S in S^⊥, both signs) | 8 | 510 | **56** (28 cosets × 2 signs; all uncovered) |
| 4 | 4 | 756 (from 3 rank-3 parents) | 0 |

Within S^⊥/S (256 cosets), the covered-weight histogram is {0: 156, 1: 63, 2: 36}. Other rank-3 values are 2.74109 (126), 3 (326) and 7 (2). The rank-4 search started from only three of the 56 parents, so it is not exhaustive.

## 3. On the rank-3 code space the minimiser is rigid and algebraic (`w33_f8_rank3_stabiliser_exact.py`)

Let T = ⟨−iP(12,53), P(53,33), P(1,6)⟩, with Paulis written as (P(u,v)ψ)[x] = (−1)^{v·(x⊕u)} ψ[x⊕u].
- Restricted to the +1 eigenspace of T (C⁸), all 20 double-precision starts reach c₈.
- Newton's method in mpmath (16 real parameters) converges quadratically: gradient 2×10⁻⁹ → 4×10⁻¹⁷ → 9×10⁻³² → 7×10⁻⁵². The value agrees with the closed form to 3×10⁻⁵⁰.
- The Hessian null space has dimension 2 (global phase and scale). **The minimiser is isolated.** Five independent minimisers had identical expectation multisets.

All 512 non-zero squared Pauli expectations are identified at 50 digits, with γ = 2cos(2π/9):

| level × 81 | count |
|---|---|
| (5 − 2γ²)² = 25 − 4γ − 8γ² | 72 |
| 3 (i.e. 1/27) | 72 |
| (1 − 2γ)² | 72 |
| 11 − 4γ = 3·((7 − 4γ − 2γ²)/3)² | 72 |
| 19 − 4γ² | 72 |
| 3 + 4γ + 4γ² | 72 |
| (3 + 2γ − 2γ²)² = 1 + 8γ + 4γ² | 72 |
| 81 (the stabiliser T) | 8 |

The square roots lie in Q(γ) or √3·Q(γ). The purity sum closes exactly: 8 + 72·63/81 = 64.

## 4. The exact witness (`w33_f8_exact_witness.py`)

1. Each Hermitian Pauli expectation r_P = ⟨i^{|u∧v|} X^u Z^v⟩ is identified in Q(γ, √3) with basis [1, γ, γ², √3, √3γ, √3γ²], and the residual below 10⁻⁴⁰ is asserted.
2. ρ := (1/64) Σ r_P P̂ is built over K = Q(γ, √3, i) in exact integer arithmetic, with 12 rational coordinates and a common denominator.
3. The checks, with **no floating point**:
   - ρ† = ρ, tr ρ = 1 and ρ² = ρ, so ρ is a pure state;
   - each of the nine basis distributions p_{t,k} = (U_t ρ U_tᵀ)_{kk}, using the exact CZ-model basis unitaries, gives 64·(Σp² − 9/64) = **47/9 − (16/9)γ**, exactly the closed form.

Floating point was used only to *find* the coefficients. The runtime is about 8 s.

**The covered side, explicitly.** 63 covered Paulis are non-zero (7 per basis, as in Pass 12660):
- 27 at ±√3/9;
- 18 at ±(1 − 2γ)/9;
- 9 at ±(5 − 2γ²)/9;
- 9 at ±√3(7 − 4γ − 2γ²)/27.

Summing their squares gives

  c₈ = 27·(1/27) + 18·(1−2γ)²/81 + 9·(5−2γ²)²/81 + 9·(11−4γ)/81 = (47 − 16γ)/9.

## What this does and does not establish

- **Exact:** the upper bound c₈ ≤ (47 − 32 cos 2π/9)/9, and the witness's field Q(cos 2π/9, √3, i) ⊂ Q(ζ₃₆).
- **Numerical:** that this is the global minimum. A matching lower bound would need, for example, an SOS or dual certificate at this value. The degree-6 SOS reached only 0.0452 even at q = 4 (Pass 12660), so this is open.
- **Not derived:** why the minimum family contains a rank-3 code-space point, and why the field is Q(cos 2π/9). The norm-one torus of F₆₄ has order 9 (Pass 12669), but no mechanism links it to T.
- **Corollary (via Pass 12659's quotient lemma, as in Pass 12669):** the two five-qubit quotient 9-sets have exact upper bound (47 − 32 cos 2π/9)/288 *if* the quotient map carries this witness; this was not checked separately here.

## Prior art and ownership

- The order-4 stabiliser S and the "7 covered non-zero per basis" pattern are Pass 12660 (Claude track, e5c85d51e).
- The closed form is Pass 12669 (Claude track).
- The rational witness 2.49850865922 and the PPT dual bound 2.0818 are the other track's.
- Searched origin/master for the closed form, `2.4985086`, "rank-3 stabiliser" and "exact witness": no prior exact witness found.
- The paper (papers/strongly_unextendible_pauli_mubs.tex, Proposition (iii)) is updated.
