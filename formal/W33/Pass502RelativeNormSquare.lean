import Mathlib

namespace W33.Pass502

open scoped BigOperators

variable {ι R : Type*} [Fintype ι] [CommRing R] [StarRing R]

/-- If every selected embedding value is fixed by the involution, multiplying
it with its conjugate partner gives the square of the half-orbit product.  This
is the finite-product core of
`N_{K/ℚ}(x) = N_{K⁺/ℚ}(x)^2` for `x ∈ K⁺`. -/
theorem pairedStarProduct_eq_sq (f : ι → R)
    (hfixed : ∀ i, star (f i) = f i) :
    (∏ i, f i * star (f i)) = (∏ i, f i) ^ 2 := by
  simp_rw [hfixed]
  rw [Finset.prod_mul_distrib]
  simp [pow_two]

/-- The same statement in an integral domain, matching the cyclotomic use. -/
theorem pairedStarProduct_eq_sq_domain
    {K : Type*} [Fintype ι] [CommRing K] [NoZeroDivisors K] [StarRing K]
    (f : ι → K) (hfixed : ∀ i, star (f i) = f i) :
    (∏ i, f i * star (f i)) = (∏ i, f i) ^ 2 :=
  pairedStarProduct_eq_sq f hfixed

end W33.Pass502
