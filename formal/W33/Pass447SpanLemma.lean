import Mathlib

namespace W33.Pass447

/-!
The heart of cover-law lemma L1 (repository witness P394), formalized
generically: for a central elation, `z·x − x` is a nonzero multiple of `p₀`,
so the span of `{x, z·x}` equals the span of `{x, p₀}`. Stripped of the
geometry, this is: `span {x, x + c • p} = span {x, p}` for `c ≠ 0`. The
remaining geometric steps of L1 (perp monotonicity and the rim/bulk count)
are the named formalization boundary.
-/

variable {K : Type*} [Field K] {V : Type*} [AddCommGroup V] [Module K V]

theorem span_pair_shift (c : K) (hc : c ≠ 0) (x p : V) :
    Submodule.span K {x, x + c • p} = Submodule.span K {x, p} := by
  apply le_antisymm
  · rw [Submodule.span_le]
    rintro v (rfl | rfl)
    · exact Submodule.subset_span (Or.inl rfl)
    · exact Submodule.add_mem _
        (Submodule.subset_span (Or.inl rfl))
        (Submodule.smul_mem _ c (Submodule.subset_span (Or.inr rfl)))
  · rw [Submodule.span_le]
    rintro v (rfl | rfl)
    · exact Submodule.subset_span (Or.inl rfl)
    · have hx : x ∈ Submodule.span K {x, x + c • p} :=
        Submodule.subset_span (Or.inl rfl)
      have hxc : x + c • p ∈ Submodule.span K {x, x + c • p} :=
        Submodule.subset_span (Or.inr rfl)
      have hcp : c • p ∈ Submodule.span K {x, x + c • p} := by
        have := Submodule.sub_mem _ hxc hx
        simpa using this
      have : c⁻¹ • (c • p) ∈ Submodule.span K {x, x + c • p} :=
        Submodule.smul_mem _ c⁻¹ hcp
      simpa [smul_smul, inv_mul_cancel₀ hc] using this

end W33.Pass447
