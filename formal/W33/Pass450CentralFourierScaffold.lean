import Mathlib

open scoped BigOperators

namespace W33.Pass450

/-- Finite-group convolution in the convention used by the Heisenberg witnesses. -/
def convolution {G R : Type*} [Fintype G] [Group G] [CommRing R]
    (f g : G → R) (x : G) : R :=
  ∑ y : G, f y * g (y⁻¹ * x)

/-- A multiplicative character vector is an eigenvector of every convolution
operator. The representation-theoretic work in the W33 papers is exactly the
construction and conductor classification of the relevant characters. -/
theorem convolution_character_eigenvector
    {G R : Type*} [Fintype G] [Group G] [CommRing R]
    (f χ : G → R)
    (hχ : ∀ y x : G, χ (y⁻¹ * x) = χ y⁻¹ * χ x)
    (x : G) :
    convolution f χ x = (∑ y : G, f y * χ y⁻¹) * χ x := by
  simp [convolution, hχ, mul_assoc, Finset.sum_mul]

/-- The scalar cancellation step behind finite-character orthogonality. -/
theorem twisted_fixed_scalar_is_zero
    {K : Type*} [Field K]
    (s u : K) (hu : u ≠ 1) (hfixed : s = u * s) : s = 0 := by
  -- `rw [hfixed]` rewrites `s` into `u * s` on BOTH sides, which does not close
  -- the goal.  Expand the product and fold `u * s` back to `s` instead.
  have hzero : (1 - u) * s = 0 := by
    rw [sub_mul, one_mul, ← hfixed, sub_self]
  rcases mul_eq_zero.mp hzero with hleft | hright
  · exfalso
    apply hu
    exact (sub_eq_zero.mp hleft).symm
  · exact hright

/-- The conductor multiplicities used in Pass 440 have the correct total active
rank at each depth. -/
theorem conductor_active_rank_identity (characters t : ℤ) :
    characters * t * (t + 1) + characters * t * (t - 1) =
      2 * characters * t^2 := by
  ring

/-- Pairing the plus and minus Fourier blocks leaves the residual rank used by
integral Smith gluing. -/
theorem conductor_residual_rank_identity (characters t : ℤ) :
    characters * t * (t + 1) - characters * t * (t - 1) =
      2 * characters * t := by
  ring

/-- Length-three Hjelmslev eigenlevels match the three conductor magnitudes. -/
theorem length_three_conductor_magnitudes (q : ℤ) :
    (q^5, q^4, q^3) = (q^(2 * 3 - 1), q^(2 * 3 - 2), q^(2 * 3 - 3)) := by
  norm_num

end W33.Pass450
