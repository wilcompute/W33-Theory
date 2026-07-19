import Mathlib

namespace W33.Pass484

/-!
The cancellation driving the sharp determinant law of Pass 484.

In the expansion of `Q = ∑_{v,w} d v * d w * ψ(-ω v w)` modulo `λ⁴`, the term
that survives pairs the **symmetric** coefficient `d v * d w` against the
**antisymmetric** symplectic form `ω v w`.  Such a sum equals its own negative,
so twice it vanishes; in `ℤ[ζ_p]` with `p` odd, `2` is not a zero divisor, so
the sum itself vanishes.  This is the reason `Q ≡ 0` and hence the reason the
first two orders of the determinant expansion cancel.
-/

variable {ι : Type*} [Fintype ι] {R : Type*} [CommRing R]

/-- Relabelling the two summation indices rewrites the weight as its
transpose, because the coefficient `c v * c w` is symmetric. -/
theorem sum_swap_transpose (c : ι → R) (g : ι → ι → R) :
    ∑ v : ι, ∑ w : ι, c v * c w * g v w
      = ∑ v : ι, ∑ w : ι, c v * c w * g w v := by
  rw [Finset.sum_comm]
  exact Finset.sum_congr rfl fun _ _ =>
    Finset.sum_congr rfl fun _ _ => by ring

/-- For an antisymmetric weight the doubly-indexed sum is annihilated by `2`. -/
theorem two_mul_sum_eq_zero (c : ι → R) (g : ι → ι → R)
    (hg : ∀ v w, g w v = -g v w) :
    2 * ∑ v : ι, ∑ w : ι, c v * c w * g v w = 0 := by
  have hsum :
      (∑ v : ι, ∑ w : ι, c v * c w * g v w)
        + (∑ v : ι, ∑ w : ι, c v * c w * g v w) = 0 := by
    nth_rewrite 2 [sum_swap_transpose c g]
    rw [← Finset.sum_add_distrib]
    refine Finset.sum_eq_zero fun v _ => ?_
    rw [← Finset.sum_add_distrib]
    refine Finset.sum_eq_zero fun w _ => ?_
    rw [hg v w]
    ring
  rw [two_mul]
  exact hsum

/-- If `R` has no zero divisors and `2 ≠ 0` — for instance `ℤ[ζ_p]` with `p`
odd — the sum vanishes outright. -/
theorem sum_symm_antisymm_eq_zero [NoZeroDivisors R] (h2 : (2 : R) ≠ 0)
    (c : ι → R) (g : ι → ι → R) (hg : ∀ v w, g w v = -g v w) :
    ∑ v : ι, ∑ w : ι, c v * c w * g v w = 0 := by
  rcases mul_eq_zero.mp (two_mul_sum_eq_zero c g hg) with h | h
  · exact absurd h h2
  · exact h

end W33.Pass484
