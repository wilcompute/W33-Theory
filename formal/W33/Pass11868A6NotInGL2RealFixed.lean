import Mathlib

namespace W33.Pass11868

/-!
Pass 11868: closing the finite steps of the family no-go and of the chirality firewall.

* **No faithful image of `A₆` in `GL(2, ℂ)`** (hence none in `U(2)`), without assuming perfectness: the involutions
  `(0 1)(2 3) = ⁅(0 1)(0 2), (0 1)(0 3)⁆` and `(0 1)(2 4) = ⁅(0 1)(0 2), (0 1)(0 4)⁆` are commutators, so their images
  have determinant `1`, hence lie in `SL(2, ℂ)`, where the only involution is `-1` (Pass 11863).  An injective
  homomorphism would identify the two.
* **Real-structure lemma** (behind "no automorphism of `E₈` is chiral", Pass 11859): if `g` commutes with an antilinear
  map `v ↦ J (conj v)`, then the fixed space of `g` is preserved by it.
-/

open Matrix

/-- The `SL(2, ℂ)` involution lemma (as in Pass 11863, repeated so this module is self-contained). -/
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


def w (a b c d : Fin 6) : Equiv.Perm (Fin 6) := Equiv.swap a b * Equiv.swap c d

theorem w_mem (a b c d : Fin 6) (h1 : a ≠ b) (h2 : c ≠ d) : w a b c d ∈ alternatingGroup (Fin 6) := by
  rw [Equiv.Perm.mem_alternatingGroup, w, Equiv.Perm.sign_mul, Equiv.Perm.sign_swap h1, Equiv.Perm.sign_swap h2]
  decide

def a0 : alternatingGroup (Fin 6) := ⟨w 0 1 0 2, w_mem _ _ _ _ (by decide) (by decide)⟩
def b3 : alternatingGroup (Fin 6) := ⟨w 0 1 0 3, w_mem _ _ _ _ (by decide) (by decide)⟩
def b4 : alternatingGroup (Fin 6) := ⟨w 0 1 0 4, w_mem _ _ _ _ (by decide) (by decide)⟩

theorem s1_commutator : s1 = a0 * b3 * a0⁻¹ * b3⁻¹ := by decide
theorem s2_commutator : s2 = a0 * b4 * a0⁻¹ * b4⁻¹ := by decide

/-- A homomorphism to a commutative group kills commutators. -/
theorem comm_kills {G H : Type*} [Group G] [CommGroup H] (D : G →* H) (a b : G) : D (a * b * a⁻¹ * b⁻¹) = 1 := by
  rw [map_mul, map_mul, map_mul, map_inv, map_inv, mul_right_comm (D a) (D b) (D a)⁻¹, mul_inv_cancel, one_mul,
    mul_inv_cancel]

/-- `A₆` has no faithful image in `GL(2, ℂ)` (in particular none in `U(2)`). -/
theorem no_injective_hom_GL2 :
    ¬ ∃ f : alternatingGroup (Fin 6) →* GL (Fin 2) ℂ, Function.Injective f := by
  rintro ⟨f, hf⟩
  have key : ∀ s x y : alternatingGroup (Fin 6), s = x * y * x⁻¹ * y⁻¹ → s * s = 1 → s ≠ 1 →
      ((f s : GL (Fin 2) ℂ) : Matrix (Fin 2) (Fin 2) ℂ) = -1 := by
    intro s x y hc hs hne
    have hdet : ((f s : GL (Fin 2) ℂ) : Matrix (Fin 2) (Fin 2) ℂ).det = 1 := by
      have h1 : (Matrix.GeneralLinearGroup.det.comp f) s = 1 := by rw [hc]; exact comm_kills _ x y
      have h2 := congrArg Units.val h1
      simpa [Matrix.GeneralLinearGroup.val_det_apply] using h2
    have hsq : ((f s : GL (Fin 2) ℂ) : Matrix (Fin 2) (Fin 2) ℂ) * ((f s : GL (Fin 2) ℂ) : Matrix (Fin 2) (Fin 2) ℂ) = 1 := by
      rw [← Units.val_mul, ← map_mul, hs, map_one, Units.val_one]
    rcases sl2_involution _ hsq hdet with h | h
    · exfalso
      apply hne
      apply hf
      rw [map_one]
      exact Units.ext (by rw [h, Units.val_one])
    · exact h
  have e1 := key _ _ _ s1_commutator s1_sq s1_ne_one
  have e2 := key _ _ _ s2_commutator s2_sq s2_ne_one
  exact s1_ne_s2 (hf (Units.ext (e1.trans e2.symm)))

/-- Real-structure lemma: if `g J = J ḡ` then `g` preserves `J (conj v)` whenever it fixes `v`. -/
theorem real_structure_fixed {n : Type*} [Fintype n] [DecidableEq n] (g J : Matrix n n ℂ)
    (hgJ : g * J = J * g.map star) (v : n → ℂ) (hv : g.mulVec v = v) :
    g.mulVec (J.mulVec (star v)) = J.mulVec (star v) := by
  have hconj : (g.map star).mulVec (star v) = star (g.mulVec v) := by
    ext i
    simp [Matrix.mulVec, dotProduct, star_sum]
  rw [Matrix.mulVec_mulVec, hgJ, ← Matrix.mulVec_mulVec, hconj, hv]

end W33.Pass11868
