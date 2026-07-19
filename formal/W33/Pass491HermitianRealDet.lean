import Mathlib

namespace W33.Pass491

/-!
The real-subring lemma of Pass 491.

`D = B_t(c) - F` is Hermitian, and complex conjugation is the Galois element
`σ_{-1}`.  Applying a ring automorphism entrywise commutes with taking the
determinant, and on a Hermitian matrix conjugation is transposition — so
`σ_{-1}(det D) = det (Dᵀ) = det D`, i.e. `det D` is fixed by conjugation and
lies in the maximal real subring.

Two consequences used in the paper: `v_λ(det D)` is always even (the ramified
prime has index 2 over the real subring), and `det D` is rational exactly when
`p = 3`.  We formalize the algebraic core — a `star`-invariance statement for
determinants of self-adjoint matrices — which is what makes both work.
-/

open Matrix

variable {n : Type*} [Fintype n] [DecidableEq n]
variable {R : Type*} [CommRing R] [StarRing R]

/-- Entrywise star of a matrix, then determinant, equals star of the
determinant: `star` is a ring homomorphism `R →+* Rᵐᵒᵖ`-free here because `R`
is commutative, so it commutes with `det`. -/
theorem det_conjTranspose_eq_star_det (M : Matrix n n R) :
    (Mᴴ).det = star M.det := by
  rw [Matrix.conjTranspose, Matrix.det_transpose_eq_det_map]
  · simp [Matrix.det_map]
  all_goals simp

/-- **The lemma.** If `M` is self-adjoint (Hermitian) then its determinant is
fixed by `star`, hence lies in the real subring. -/
theorem star_det_eq_det_of_isHermitian {M : Matrix n n R}
    (h : M.IsHermitian) : star M.det = M.det := by
  have : (Mᴴ).det = M.det := by rw [h.eq]
  rw [← det_conjTranspose_eq_star_det, this]

/-- Restated as membership in the fixed subring of `star`. -/
theorem det_mem_star_fixed {M : Matrix n n R} (h : M.IsHermitian) :
    M.det ∈ {x : R | star x = x} :=
  star_det_eq_det_of_isHermitian h

end W33.Pass491
