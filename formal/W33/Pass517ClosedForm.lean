import Mathlib

namespace W33.Pass517

/-!
The step that turns the closed form into the sieve (Pass 517), formalized.

Pass 517 proves that, whenever `e ∣ (m / d)`,

    d * S d = q * ∑ c ∈ d.divisors, μ (d / c) * Ps (m / c) ^ c ,

and then derives the sieve theorem by summing over `d ∣ t` and exchanging the
order of summation:

    ∑_{d ∣ t} d * S d
      = q * ∑_{c ∣ t} Ps (m / c) ^ c * (∑_{c ∣ d ∣ t} μ (d / c))
      = q * Ps (m / t) ^ t ,

the inner sum being `1` at `c = t` and `0` otherwise.

Two things happen there.  The *arithmetic* input is the Möbius collapse
`∑_{c ∣ d ∣ t} μ (d/c) = if c = t then 1 else 0`; the *structural* step is the
exchange of summation order.  This file proves the second and takes the first
as an explicit hypothesis, in the same style as the other modules of this arc —
the arithmetic content is checked exactly by the Python witnesses, and what is
formalized is the manipulation that carries it.
-/

open Finset

variable {R : Type*} [CommRing R]

/-- **The order exchange.**  If each `f d` is a `∑ c ∈ inner d, w d c • g c`,
then summing over `d ∈ outer` regroups as a sum over `c` weighted by the
column sums of `w`.  Stated over an arbitrary index pair so that no divisor
theory is needed. -/
theorem sum_exchange
    {ι κ : Type*} [DecidableEq κ]
    (outer : Finset ι) (inner : Finset κ)
    (w : ι → κ → R) (g : κ → R) :
    ∑ d ∈ outer, ∑ c ∈ inner, w d c * g c
      = ∑ c ∈ inner, (∑ d ∈ outer, w d c) * g c := by
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl ?_
  intro c _
  rw [Finset.sum_mul]

/-- **The sieve, from the closed form.**  With `hcollapse` supplying the
Möbius fact — the column sums of `w` are the indicator of `c = top` — the
regrouped sum collapses to a single term. -/
theorem sieve_of_closed_form
    {ι κ : Type*} [DecidableEq κ]
    (outer : Finset ι) (inner : Finset κ) (top : κ)
    (w : ι → κ → R) (g : κ → R)
    (htop : top ∈ inner)
    (hcollapse : ∀ c ∈ inner, (∑ d ∈ outer, w d c) = if c = top then 1 else 0) :
    ∑ d ∈ outer, ∑ c ∈ inner, w d c * g c = g top := by
  rw [sum_exchange outer inner w g]
  rw [Finset.sum_congr rfl
    (fun c hc => by rw [hcollapse c hc])]
  simp [Finset.sum_ite_eq' inner top g, htop]

/-!
### Scope

`hcollapse` is the arithmetic half — over the divisor lattice it is
`∑_{c ∣ d ∣ t} μ (d/c) = [c = t]`, the defining property of the Möbius
function — and it is assumed here rather than derived.  The closed form itself,
`d * S d = q ∑_{c ∣ d} μ(d/c) Ps(m/c)^c`, is proved in Pass 517 and verified
against honest enumeration of the orbits on 34 cells before anything relied on
it.

What this file contributes is the regrouping: that summing a divisor-indexed
family and exchanging the order produces column sums against which the Möbius
fact can be applied at all.  Together with `Pass514Sieve.lean` (the fibrewise
step behind the closed form) and `Pass515TriangularRank.lean` (the rank of the
resulting system, with no hypotheses at all), the three modules cover the
non-arithmetic content of Passes 514–517.
-/

end W33.Pass517
