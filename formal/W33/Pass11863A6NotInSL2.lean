import Mathlib

namespace W33.Pass11863

/-!
Pass 11863: the finite-group step of the family no-go (Pass 11854).

A finite Lorentz group commuting with the grand-unified `SU(5)` and an exact family `SU(3)` inside `E₈` would have to
lie in `U(2)`; since `A₆` is perfect its image lies in `SU(2) ⊂ SL(2, ℂ)`.  Here:

* **Involution lemma.**  In `SL(2, ℂ)` the only solutions of `g² = 1` are `g = ±1`.  (Entrywise: `(a + d)² = 4`, so
  `b = c = 0` and `a = d = ±1`.)
* **No faithful image.**  `A₆` contains two distinct involutions, `(0 1)(2 3)` and `(0 1)(2 4)`.  An injective
  homomorphism `A₆ → SL(2, ℂ)` would send both to `-1`, a contradiction.  Hence `A₆` (and with it the spinorial Lorentz
  group, which contains `A₆`-preimages of these involutions of order 4 squaring to the centre) has no faithful image in
  `SL(2, ℂ)`.
-/

open Matrix

theorem sl2_involution (g : Matrix (Fin 2) (Fin 2) ℂ) (h2 : g * g = 1) (hd : g.det = 1) :
    g = 1 ∨ g = -1 := by
  have e00 := congrFun (congrFun h2 0) 0
  have e01 := congrFun (congrFun h2 0) 1
  have e10 := congrFun (congrFun h2 1) 0
  have e11 := congrFun (congrFun h2 1) 1
  simp [Matrix.mul_apply, Fin.sum_univ_two] at e00 e01 e10 e11
  rw [Matrix.det_fin_two] at hd
  have hs : (g 0 0 + g 1 1) ^ 2 = 4 := by linear_combination e00 + e11 + 2 * hd
  have hs0 : g 0 0 + g 1 1 ≠ 0 := by
    intro h
    rw [h] at hs
    norm_num at hs
  have hb : g 0 1 = 0 := by
    have hm : g 0 1 * (g 0 0 + g 1 1) = 0 := by linear_combination e01
    rcases mul_eq_zero.mp hm with h | h
    · exact h
    · exact absurd h hs0
  have hc : g 1 0 = 0 := by
    have hm : g 1 0 * (g 0 0 + g 1 1) = 0 := by linear_combination e10
    rcases mul_eq_zero.mp hm with h | h
    · exact h
    · exact absurd h hs0
  have had : g 0 0 = g 1 1 := by
    have hsq : (g 0 0 - g 1 1) ^ 2 = 0 := by linear_combination e00 + e11 - 2 * hd - 4 * g 1 0 * hb
    exact sub_eq_zero.mp ((pow_eq_zero_iff two_ne_zero).mp hsq)
  have ha : (g 0 0 - 1) * (g 0 0 + 1) = 0 := by linear_combination e00 - g 1 0 * hb
  rcases mul_eq_zero.mp ha with h | h
  · left
    ext i j
    fin_cases i <;> fin_cases j <;> simp [hb, hc] <;>
      first | linear_combination h | linear_combination h - had
  · right
    ext i j
    fin_cases i <;> fin_cases j <;> simp [hb, hc] <;>
      first | linear_combination h | linear_combination h - had

/-- Two distinct involutions of `A₆`. -/
def s1 : alternatingGroup (Fin 6) :=
  ⟨Equiv.swap 0 1 * Equiv.swap 2 3, Equiv.Perm.mem_alternatingGroup.mpr (by simp [Equiv.Perm.sign_swap'])⟩
def s2 : alternatingGroup (Fin 6) :=
  ⟨Equiv.swap 0 1 * Equiv.swap 2 4, Equiv.Perm.mem_alternatingGroup.mpr (by simp [Equiv.Perm.sign_swap'])⟩

theorem s1_ne_s2 : s1 ≠ s2 := by decide
theorem s1_ne_one : s1 ≠ 1 := by decide
theorem s2_ne_one : s2 ≠ 1 := by decide
theorem s1_sq : s1 * s1 = 1 := by decide
theorem s2_sq : s2 * s2 = 1 := by decide

/-- `A₆` has no faithful image in `SL(2, ℂ)`. -/
theorem no_injective_hom :
    ¬ ∃ f : alternatingGroup (Fin 6) →* Matrix.SpecialLinearGroup (Fin 2) ℂ, Function.Injective f := by
  rintro ⟨f, hf⟩
  have key : ∀ s : alternatingGroup (Fin 6), s * s = 1 → s ≠ 1 →
      ((f s : Matrix.SpecialLinearGroup (Fin 2) ℂ) : Matrix (Fin 2) (Fin 2) ℂ) = -1 := by
    intro s hs hne
    have hsq : ((f s : Matrix.SpecialLinearGroup (Fin 2) ℂ) : Matrix (Fin 2) (Fin 2) ℂ) *
        ((f s : Matrix.SpecialLinearGroup (Fin 2) ℂ) : Matrix (Fin 2) (Fin 2) ℂ) = 1 := by
      rw [← Matrix.SpecialLinearGroup.coe_mul, ← map_mul, hs, map_one, Matrix.SpecialLinearGroup.coe_one]
    rcases sl2_involution _ hsq (f s).2 with h | h
    · exfalso
      apply hne
      apply hf
      rw [map_one]
      exact Subtype.ext (by rw [h, Matrix.SpecialLinearGroup.coe_one])
    · exact h
  have e1 := key s1 s1_sq s1_ne_one
  have e2 := key s2 s2_sq s2_ne_one
  exact s1_ne_s2 (hf (Subtype.ext (e1.trans e2.symm)))

end W33.Pass11863
