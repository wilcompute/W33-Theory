import W33.Pass447SpanLemma
import Mathlib.LinearAlgebra.BilinearForm.Orthogonal

namespace W33.Pass457

variable {K : Type*} [Field K] {V : Type*} [AddCommGroup V] [Module K V]

/-- The axis line belongs to the two-generator plane. -/
theorem singleton_span_le_pair_span (x p : V) :
    Submodule.span K {p} ≤ Submodule.span K {x, p} := by
  rw [Submodule.span_le]
  intro v hv
  have hvp : v = p := by simpa using hv
  subst v
  exact Submodule.subset_span (Or.inr rfl)

/-- Orthogonal complement reverses inclusion. This is the exact perp step named
as the boundary after Pass 447. -/
theorem pair_orthogonal_le_axis
    (B : LinearMap.BilinForm K V) (x p : V) :
    B.orthogonal (Submodule.span K {x, p}) ≤
      B.orthogonal (Submodule.span K {p}) :=
  B.orthogonal_le (singleton_span_le_pair_span x p)

/-- Combining Pass 447's shifted-span identity with perp antitonicity closes the
linear-algebraic core of cover-law lemma L1. -/
theorem shifted_pair_orthogonal_le_axis
    (B : LinearMap.BilinForm K V) (c : K) (hc : c ≠ 0) (x p : V) :
    B.orthogonal (Submodule.span K {x, x + c • p}) ≤
      B.orthogonal (Submodule.span K {p}) := by
  rw [W33.Pass447.span_pair_shift c hc x p]
  exact pair_orthogonal_le_axis B x p

end W33.Pass457
