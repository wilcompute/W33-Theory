import Mathlib

namespace W33.Pass511

/-!
Ingredient (iii) of the odd-class vanishing theorem (Pass 511), formalized.

The theorem states: writing `m = d * k`, if `m` is odd and `p ∣ k`, then the
period-`d` class of the cyclic-orbit decomposition of `tr (D ^ m)` vanishes
identically for every inverse-closed section.  Its proof has three ingredients:

  (i)   `ρ_{v₁} ⋯ ρ_{v_d} = ζ^s ρ w` with `w = ∑ vᵢ`, so its `k`-th power is
        the identity when `p ∣ k`, giving a *rational* trace `q`;
  (ii)  `(u - 1) ^ k` is purely imaginary exactly when `k` is odd and `p ∣ k`,
        and a product of `d` purely imaginary numbers is purely imaginary
        because `d` is odd;
  (iii) inverse closure `c (-v) = -c v` gives `d₍₋ᵥ₎ = star (d ᵥ)`, so the
        orbits partition into pairs `{O, -O}` and each pair contributes
        `x + star x = 0`.

Ingredients (i) and (ii) are computations in the Heisenberg group and in
`ℤ[ζ_p]`; they are verified *exactly* (not numerically) in
`analysis/w33_pass511_constant_orbit_theorem.py` and are **not** formalized
here.  Ingredient (iii) is what this file proves.

The formalization follows the proof's actual shape.  The proof does not
reindex a sum by an involution; it observes that inverse closure *partitions*
the orbits into pairs and that each pair cancels.  So the statements below are
about a sum over pairs, and the arithmetic input — "purely imaginary" — appears
as the hypothesis `star x = -x` in a star-ring, which is exactly what
`Re x = 0` means over `ℤ[ζ_p]` with `star = σ₋₁`.
-/

open Finset

variable {κ : Type*} {A : Type*}

/-- A purely imaginary element of a star-ring cancels against its conjugate.
Over `ℤ[ζ_p]` with `star = σ₋₁` the hypothesis `star x = -x` is precisely
`Re x = 0`, which ingredient (ii) supplies. -/
theorem add_star_eq_zero [AddGroup A] [StarAddMonoid A]
    {x : A} (hx : star x = -x) : x + star x = 0 := by
  rw [hx, add_neg_cancel]

/-- **The pairing lemma (ingredient (iii)).**  If the index set of a finite sum
splits into pairs whose two contributions are conjugate, and each contribution
is purely imaginary, the whole sum vanishes.

Here `t` indexes the inverse-closed pairs `{v, -v}` of the register cell, `a k`
is the contribution of an orbit and `b k` that of its negative. -/
theorem sum_of_conjugate_pairs_eq_zero [AddCommGroup A] [StarAddMonoid A]
    (t : Finset κ) (a b : κ → A)
    (hpair : ∀ k ∈ t, b k = star (a k))
    (himag : ∀ k ∈ t, star (a k) = -(a k)) :
    ∑ k ∈ t, (a k + b k) = 0 := by
  refine (Finset.sum_congr rfl ?_).trans Finset.sum_const_zero
  intro k hk
  rw [hpair k hk, add_star_eq_zero (himag k hk)]

/-- The conclusion in the form the theorem uses: the period-`d` class, written
as a sum over inverse-closed pairs of orbits, is zero. -/
theorem class_vanishes_of_pairing [AddCommGroup A] [StarAddMonoid A]
    (t : Finset κ) (a b : κ → A)
    (hpair : ∀ k ∈ t, b k = star (a k))
    (himag : ∀ k ∈ t, star (a k) = -(a k)) :
    ∑ k ∈ t, (a k + b k) = 0 :=
  sum_of_conjugate_pairs_eq_zero t a b hpair himag

/-!
### What this does not claim

The hypothesis `himag` — that each orbit's contribution is purely imaginary —
is exactly where ingredients (i) and (ii) enter, and it is *assumed* here, not
derived.  So this file formalizes the shape of the cancellation and none of its
arithmetic content.

The arithmetic is checked exactly in
`analysis/w33_pass511_constant_orbit_theorem.py`: the criterion "`(u-1)^k` is
purely imaginary ↔ `k` odd and `p ∣ k`" is tested in `ℤ[ζ_p]` as
`x + σ₋₁ x = 0` for `p ∈ {3,5,7,11,13}` and `k ≤ 24` (a first draft tested
`|Re x| < 10⁻⁹` in floating point and reported a spurious counterexample at
`(p,k) = (7,21)`, where `|x| ∼ 10⁶` makes an absolute tolerance meaningless),
and the Heisenberg power identity `ρ_v ^ p = I` exactly at `p ∈ {3,5,7}`.
-/

end W33.Pass511
