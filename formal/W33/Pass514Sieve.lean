import Mathlib

namespace W33.Pass514

/-!
The combinatorial core of the sieve theorem (Pass 514), formalized.

The sieve theorem states: with `e` the order of the generating character and
`t ∣ m` such that `m / t` is odd and `e ∣ (m / t)`,

    ∑_{d ∣ t} d • S d = q * (∑_{v ≠ 0} d_v ^ (m / t)) ^ t = 0 .

Its proof has two halves.

*The arithmetic half* shows that for `d ∣ t` a period-`d` representative has
`M ^ (m / d) = I`, so its orbit contributes `q * ∏ᵢ d_{wᵢ} ^ (m / d)`, and that
the bracket vanishes because `m / t` is odd and `e ∣ (m / t)`.  Both are
computations in the Heisenberg group and in `ℤ[ζ_e]`; they are verified exactly
in `analysis/w33_pass511_constant_orbit_theorem.py` and
`analysis/w33_pass514_sieve_theorem.py`, and are **not** formalized here.

*The combinatorial half* is the step "summing over `d ∣ t` sweeps every
`t`-tuple exactly once, each period-`d` orbit contributing `d` times".  That is
a statement about fibres: the summand is constant on cyclic orbits, so the sum
over all `t`-tuples equals the sum over orbits of (orbit size) • (value at a
representative).  That is what this file proves, in the generality the argument
uses — an arbitrary map `g` playing the role of "which orbit", with no group
theory required.
-/

open Finset

variable {α β M : Type*} [DecidableEq β] [AddCommMonoid M]

/-- **The fiberwise step.**  If `f` is constant on the fibres of `g` — say
`f x = v (g x)` — then summing `f` over `s` is the same as summing, over the
fibre labels, the fibre's cardinality times its common value.

This is exactly the sieve's bookkeeping: `s` is the set of `t`-tuples, `g x` is
the cyclic orbit of `x`, `v` is the orbit's value, and the fibre of a period-`d`
orbit has `d` elements — so the right-hand side is `∑_{d ∣ t} d • S d`. -/
theorem sum_eq_sum_fibres
    (s : Finset α) (t : Finset β) (g : α → β) (v : β → M) (f : α → M)
    (hmaps : ∀ x ∈ s, g x ∈ t)
    (hconst : ∀ x ∈ s, f x = v (g x)) :
    ∑ x ∈ s, f x = ∑ y ∈ t, (s.filter fun x => g x = y).card • v y := by
  rw [← Finset.sum_fiberwise_of_maps_to hmaps f]
  refine Finset.sum_congr rfl ?_
  intro y _
  have : ∀ x ∈ s.filter fun x => g x = y, f x = v y := by
    intro x hx
    obtain ⟨hxs, hxy⟩ := Finset.mem_filter.mp hx
    rw [hconst x hxs, hxy]
  rw [Finset.sum_congr rfl this, Finset.sum_const]

/-- The sieve's conclusion, given both halves as hypotheses: if the fibre sum
is the `t`-th power of the vanishing bracket, the whole sum is zero.

`hpow` is the arithmetic half — that the total over all `t`-tuples factors as
`q * P ^ t` — and `hP` is the odd-class vanishing of the bracket. -/
theorem sieve_sum_eq_zero
    (s : Finset α) (t : Finset β) (g : α → β) (v : β → M) (f : α → M)
    {R : Type*} [CommRing R] (q P : R) (toR : M → R)
    (hmaps : ∀ x ∈ s, g x ∈ t)
    (hconst : ∀ x ∈ s, f x = v (g x))
    (hpow : toR (∑ x ∈ s, f x) = q * P ^ (t.card))
    (hP : P = 0) (ht : t.Nonempty) :
    toR (∑ y ∈ t, (s.filter fun x => g x = y).card • v y) = 0 := by
  rw [← sum_eq_sum_fibres s t g v f hmaps hconst, hpow, hP]
  rw [zero_pow ht.card_pos.ne', mul_zero]

/-!
### What this does not claim

`hpow` and `hP` are assumed, not derived: they are the arithmetic half of the
proof, and formalizing them would need the Heisenberg cocycle and the
cyclotomic criterion `(u-1)^n` purely imaginary ↔ `n` odd and `e ∣ n`.  Both are
checked exactly (in `ℤ[ζ_e]`, not in floating point) by the Python witnesses:
the shortcut `value = q ∏ d_{wᵢ} ^ (m/d)` against the honest matrix computation
on 15616 orbits, and the criterion for `e ∈ {3,5,7,9,11,13,25,27}`.

What is formalized is the bookkeeping that turns "sum over orbits, weighted by
orbit size" into "sum over all tuples" — the step that makes the sieve a
statement about `∑_{d ∣ t} d • S d` rather than about orbits one at a time.
-/

end W33.Pass514
