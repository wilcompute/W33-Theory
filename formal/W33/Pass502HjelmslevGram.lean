import Mathlib

namespace W33.Pass502

open Matrix
open scoped BigOperators

variable {p : ℕ} {β : Type*} [Fintype β] [DecidableEq β]

/-- Incidence matrix of the canonical uniform `p`-sheeted cover
`Fin p × β → β`.  This is the abstract combinatorial core of the reduction
`P¹(Z/pⁿ) → P¹(Z/pⁿ⁻¹)`. -/
def uniformCoverIncidence (p : ℕ) (β : Type*)
    [Fintype β] [DecidableEq β] : Matrix β (Fin p × β) ℤ :=
  fun i x => if x.2 = i then 1 else 0

/-- The Gram matrix of a uniform `p`-sheeted incidence map is `p I`. -/
theorem uniformCover_gram_apply (i j : β) :
    (uniformCoverIncidence p β * (uniformCoverIncidence p β)ᵀ) i j =
      if i = j then (p : ℤ) else 0 := by
  classical
  by_cases h : i = j
  · -- Diagonal: the sum runs over `Fin p × β`; split it as an iterated sum so the
    -- inner `β`-sum collapses by `Finset.sum_ite_eq'`, leaving `∑ _ : Fin p, 1 = p`.
    subst j
    simp [uniformCoverIncidence, Matrix.mul_apply, Matrix.transpose_apply,
      Fintype.sum_prod_type, mul_ite, Finset.sum_ite_eq']
  · rw [if_neg h, Matrix.mul_apply]
    apply Finset.sum_eq_zero
    intro x _
    by_cases hx : x.2 = i
    · have hxj : ¬ (x.2 = j) := by rw [hx]; exact h
      simp only [uniformCoverIncidence, Matrix.transpose_apply,
        if_pos hx, if_neg hxj, mul_zero]
    · simp [uniformCoverIncidence, Matrix.transpose_apply, hx]

/-- Matrix form of the Hjelmslev reduction Gram identity. -/
theorem uniformCover_gram :
    uniformCoverIncidence p β * (uniformCoverIncidence p β)ᵀ =
      (p : ℤ) • (1 : Matrix β β ℤ) := by
  ext i j
  rw [uniformCover_gram_apply]
  by_cases h : i = j
  · subst j
    simp
  · simp [h]

end W33.Pass502
