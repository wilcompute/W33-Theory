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
  · subst j
    simp [uniformCoverIncidence, Matrix.mul_apply]
  · simp [uniformCoverIncidence, Matrix.mul_apply, h]

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
