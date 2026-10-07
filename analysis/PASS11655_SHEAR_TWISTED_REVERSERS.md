# Pass 11655 — shear-twisted reversers are a conjugacy problem: one Y per class disposes of all of them

Producer: `analysis/w33_pass11655_shear_twisted_reversers.py`
Certificate: `data/w33_pass11655_shear_twisted_reversers.json`
Regression: `tests/test_w33_pass11655_11662.py`

**What was open.** In Pass 11647 the union law was proved except for one case: k ≠ 0 solutions outside the eigenvector
cells, where cubing does not remove the shear. At n = 3 that is 108 solutions in 6 same-line orbits. They had to be
dominated one by one, and no short word in A, M and transvections worked.

## Lemma C (every n)

**Statement.** Suppose Y ∈ Sp satisfies three conditions:
* Y fixes z₁;
* Y fixes K₀ = ker(M − I) ∩ z₁^⊥ pointwise;
* YMY⁻¹ = s^k M.

Then **for every** k-solution A, the product A′ = AY is a k = 0 solution with N_{A′} = N_A.

*Proof.*
1. A⁻¹sA = s⁻¹, so A⁻¹M⁻¹A = s^k M. Hence A′MA′⁻¹ = M⁻¹ exactly when YMY⁻¹ = s^k M.
2. A′z₁ = Az₁ = −z₁.
3. A preserves K₀ and Y fixes it, so A′⁻¹w = A⁻¹w on K₀ and therefore N_{A′} = N_A.
4. Lemma A of Pass 11647 then applies to A′. ∎

**The point.** A single Y(M, k), independent of the solution, disposes of all k-solutions of a class at once.

## Certificate

| cell | (M, k) pairs with a symplectic Y | k ≠ 0 solutions for which AY is a k = 0 solution with N(AY) = N(A) |
|---|---|---|
| n = 3, same line, other | **8 / 8** | **72 / 72** |
| n = 3, same line, M²z₁ = −z₁ | **4 / 4** | **36 / 36** |
| n = 3, Mz₁ = −z₁ | 34 / 34 | 6 300 / 6 300 |
| n = 3, Mz₁ = z₁ | 28 / 34 | 5 436 (all solutions of those pairs) |
| n = 2, Mz₁ = −z₁ | 336 / 336 | 3 888 / 3 888 |
| n = 2, Mz₁ = z₁ | 288 / 336 | 2 592 (all solutions of those pairs) |

* Every Y found works for every solution, as Lemma C predicts.
* **All 108 same-line solutions are disposed of by 12 Y's.**
* The eigenvector-cell pairs without a symplectic Y are covered by Lemma B (Pass 11647).
* **Why the earlier ansatz failed.** A symmetric shear along ℓ = ⟨z₁, Mz₁⟩ would need kE₁₁ ∈ Im(φ − 1) on Sym²(ℓ). That
  fails everywhere, so Y is never a pure shear along the line.

## Status of the union law

> **For every class at n = 2 and every orbit at n = 3 within the enumeration caps, the reversible frames are exactly the
> union of ((I − A⁻¹)K₀)^⊥ over the semisimple reversers A.**

Every step is now a lemma with a uniform proof (A, B, C) except the *existence* of Y in the same-line cells. That is
certified for the 12 cases that occur and is open in general.
