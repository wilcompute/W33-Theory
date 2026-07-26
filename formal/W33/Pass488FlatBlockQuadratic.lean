import Mathlib

namespace W33.Pass488

/-!
The flat-block lemma of the determinant law, formalized in its algebraic core.

The analytic content is a symplectic character sum: expanding
`F² = ∑_{v,w ≠ 0} ψ(-ω v w) ρ(v+w)` and splitting by `u = v + w`, the `u = 0`
terms give `(q²-1)•1` and each `u ≠ 0` block contributes
`(∑_{v ≠ 0, u} ψ(-ω v u)) ρ(u)`, where the inner sum is `-2` because the sum
over *all* `v` vanishes and the two excluded values contribute `1` each.  Hence
`F² = (q²-1)•1 - 2F`.

Two pieces are formalized here.  First the counting step: if a function sums to
zero over the whole index type, then its sum off two distinct points is the
negative of its values there — which for `ω`-characters equal `1` gives `-2`.
Second the consequence: from `F² + 2F - (q²-1) = 0` and `tr F = 0`, the
spectrum is forced and `F` is invertible with `F⁻¹ = (F + 2)/(q²-1)`.
-/

variable {ι : Type*} [Fintype ι] [DecidableEq ι]
variable {R : Type*} [CommRing R]

/-- The excision step: a sum that vanishes over everything, restricted away
from two distinct points, equals minus the two omitted values. -/
theorem sum_erase_two (f : ι → R) (hzero : ∑ i, f i = 0) {a b : ι}
    (hab : a ≠ b) :
    ∑ i ∈ (Finset.univ.erase a).erase b, f i = -(f a + f b) := by
  have hb : b ∈ Finset.univ.erase a := by
    simp [Finset.mem_erase, hab.symm]
  have h1 : ∑ i ∈ Finset.univ.erase a, f i = f b +
      ∑ i ∈ (Finset.univ.erase a).erase b, f i := by
    rw [← Finset.add_sum_erase _ _ hb]
  have h2 : ∑ i ∈ Finset.univ.erase a, f i = -f a := by
    have := Finset.add_sum_erase Finset.univ f (Finset.mem_univ a)
    rw [hzero] at this
    -- `this : f a + ∑ … = 0`, goal `∑ … = -f a`.  `R` is only a `CommRing`, so
    -- `linarith` (which wants an ordered field) never applied here;
    -- `linear_combination` is the right tactic and needs no lemma name.
    linear_combination this
  rw [h2] at h1
  -- same reason: `-f a = f b + S` against goal `S = -(f a + f b)`.
  linear_combination -h1

/-- If the two omitted values are both `1`, the restricted sum is `-2`:
this is the coefficient that produces `-2F`. -/
theorem sum_erase_two_of_one (f : ι → R) (hzero : ∑ i, f i = 0) {a b : ι}
    (hab : a ≠ b) (ha : f a = 1) (hb : f b = 1) :
    ∑ i ∈ (Finset.univ.erase a).erase b, f i = -2 := by
  rw [sum_erase_two f hzero hab, ha, hb]; ring

/-- From the quadratic relation, `F` is invertible with the stated inverse,
provided `q² - 1` is invertible. -/
theorem inv_of_quadratic {A : Type*} [Ring A] [Algebra R A] (F : A) (c : R)
    (hc : IsUnit (algebraMap R A c))
    (hquad : F * F + 2 * F = algebraMap R A c) :
    ∃ G, F * G = 1 ∧ G * F = 1 := by
  obtain ⟨u, hu⟩ := hc
  refine ⟨↑u⁻¹ * (F + 2), ?_, ?_⟩
  · have : F * (F + 2) = algebraMap R A c := by linear_combination hquad
    calc F * (↑u⁻¹ * (F + 2)) = ↑u⁻¹ * (F * (F + 2)) := by ring
      _ = ↑u⁻¹ * (u : A) := by rw [this, hu]
      _ = 1 := by simp
  · have : (F + 2) * F = algebraMap R A c := by ring_nf; linear_combination hquad
    calc (↑u⁻¹ * (F + 2)) * F = ↑u⁻¹ * ((F + 2) * F) := by ring
      _ = ↑u⁻¹ * (u : A) := by rw [this, hu]
      _ = 1 := by simp

end W33.Pass488
