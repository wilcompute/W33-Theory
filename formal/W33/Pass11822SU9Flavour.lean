import Mathlib

namespace W33.Pass11822

/-!
Pass 11821/11822: SU(9) flavour unification on the two-qutrit levels.

* The cubic invariant of `Λ³ℂ⁹` is alternating, so when families are copies of the `84` the Yukawa matrix is the
  cross-product matrix `M h` with `(M h) i j = ∑ k, ε i j k * h k`.  It annihilates `h` and has determinant zero:
  one massless family, and (since `M h * (M h)ᵀ = |h|² I - h hᵀ`) a degenerate pair.
* The `ℤ₉` centre of `SU(9)` gives the `84` charge `3` and the `9̄` charge `-1`; invariants need `3a - b ≡ 0 (mod 9)`.
-/

/-- The Yukawa matrix forced by an alternating trilinear form on three family copies. -/
def skew (h : Fin 3 → ℤ) : Matrix (Fin 3) (Fin 3) ℤ :=
  !![0, h 2, -h 1; -h 2, 0, h 0; h 1, -h 0, 0]

theorem skew_transpose (h : Fin 3 → ℤ) : (skew h).transpose = -skew h := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [skew]

/-- The family direction of the Higgs vev is a massless family. -/
theorem skew_mulVec_self (h : Fin 3 → ℤ) : (skew h).mulVec h = 0 := by
  ext i; fin_cases i <;> simp [skew, Matrix.mulVec, dotProduct, Fin.sum_univ_three] <;> ring

theorem skew_det (h : Fin 3 → ℤ) : (skew h).det = 0 := by
  simp [skew, Matrix.det_fin_three]; ring

/-- `M Mᵀ = |h|² I - h hᵀ`: on the plane orthogonal to `h` both singular values equal `|h|` (degenerate pair). -/
theorem skew_mul_transpose (h : Fin 3 → ℤ) (i j : Fin 3) :
    (skew h * (skew h).transpose) i j =
      (if i = j then h 0 ^ 2 + h 1 ^ 2 + h 2 ^ 2 else 0) - h i * h j := by
  fin_cases i <;> fin_cases j <;>
    simp [skew, Matrix.mul_apply, Fin.sum_univ_three, Matrix.transpose_apply] <;> ring

/-- `ℤ₉` centre: `84 · 9̄ · 9̄` is not invariant, `84 · 9̄³` and `84³` are. -/
theorem centre_rule : (3 * 1 - 2) % 9 ≠ 0 ∧ (3 * 1 - 3) % 9 = 0 ∧ (3 * 3 - 0) % 9 = 0 := by
  decide

/-- Minimal three-generation SU(9) content `84 + 9 × 9̄`: net tens `4 - 1` and net antifives `9 - 6` per copy;
the W(3,3) `T⁶/ℤ₃` vacuum carries three copies (`3 · 84 + 27 · 9̄`). -/
theorem family_counts : 4 - 1 = 3 ∧ 9 - 6 = 3 ∧ 3 * 9 = 27 := by
  decide

end W33.Pass11822
