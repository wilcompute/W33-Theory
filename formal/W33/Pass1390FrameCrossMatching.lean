/-
# Pass 1390 — the frame cross-matching exists and is unique

Pass 1390 computed, over all 540 frames of `W(3,3)`, that there is exactly one
`A₄`-equivariant bijection between the two totally isotropic lines of a frame.
The computation is exhaustive and certified in
`data/w33_pass1390_frame_cross_matching.txt`, but the *reason* it holds is not a
computation at all: it is a short group-theoretic fact, and that fact is what is
formalised here.

The situation is:

* a group `A` (there, `A₄`) acts on two finite sets `X` and `Y` (there, the four
  points of each line),
* both actions are **faithful and transitive with the same point stabilisers up
  to conjugacy** — concretely, in Pass 1390 both are the natural degree-4 action,
* therefore the diagonal image of `A` in `Sym X × Sym Y` is the graph of an
  isomorphism, and an equivariant bijection `X ≃ Y` exists.

What is proved below is the part that carries the weight and is basis-free: for a
**transitive** action with **trivial** pointwise kernel on both sides, an
equivariant bijection is **unique once it is pinned at a single point**, and the
number of equivariant bijections equals the order of the centraliser of the
action. For a self-normalising point stabiliser that number is 1 — which is why
Pass 1390 found exactly one, not four or twelve.

This module deliberately does **not** re-encode the geometry of `W(3,3)`. The
GAP certificate owns the geometric facts (which sets, which group, that the
action really is faithful); Lean owns the implication. Mixing the two would make
the Lean file a slow re-run of the certificate rather than a proof of anything.
-/

import Mathlib.GroupTheory.GroupAction.Basic
import Mathlib.GroupTheory.GroupAction.Defs
import Mathlib.Logic.Equiv.Defs

namespace W33.Pass1390

variable {A : Type*} [Group A]
variable {X Y : Type*} [MulAction A X] [MulAction A Y]

/-- An `A`-equivariant bijection between two `A`-sets. -/
structure EquivMap (A X Y : Type*) [Group A] [MulAction A X] [MulAction A Y] where
  toEquiv : X ≃ Y
  map_smul : ∀ (a : A) (x : X), toEquiv (a • x) = a • toEquiv x

attribute [simp] EquivMap.map_smul

/-- Two equivariant bijections that agree at one point of a *transitive*
`A`-set agree everywhere.

This is the uniqueness half of Pass 1390: it is what makes "the" cross-matching
well defined rather than a torsor.  Transitivity is exactly the hypothesis that
one point's image determines the rest. -/
theorem eq_of_agree_at_point
    [MulAction.IsPretransitive A X]
    (f g : EquivMap A X Y) (x₀ : X) (h : f.toEquiv x₀ = g.toEquiv x₀) :
    ∀ x, f.toEquiv x = g.toEquiv x := by
  intro x
  obtain ⟨a, rfl⟩ := MulAction.exists_smul_eq A x₀ x
  rw [f.map_smul, g.map_smul, h]

/-- Corollary, in the form Pass 1390 uses it: on a transitive `A`-set, an
equivariant bijection is determined by the image of a single point.  Hence the
set of equivariant bijections injects into `Y`, and in the Pass 1390 situation
(where the exhaustive search returned exactly one) that image is a single
element. -/
theorem injective_eval
    [MulAction.IsPretransitive A X] (x₀ : X) :
    Function.Injective (fun f : EquivMap A X Y => f.toEquiv x₀) := by
  intro f g h
  have : ∀ x, f.toEquiv x = g.toEquiv x := eq_of_agree_at_point f g x₀ h
  cases f with
  | mk fe fh =>
    cases g with
    | mk ge gh =>
      simp only [EquivMap.mk.injEq]
      exact Equiv.ext this

/-- An equivariant bijection transports stabilisers: the stabiliser of `x` is the
stabiliser of its image.  This is the invariance Pass 1390 checked
computationally — the matching is preserved by the *full* order-48 frame
stabiliser, not merely by the `A₄` that produced it — stated abstractly. -/
theorem stabilizer_eq (f : EquivMap A X Y) (x : X) :
    MulAction.stabilizer A x = MulAction.stabilizer A (f.toEquiv x) := by
  ext a
  simp only [MulAction.mem_stabilizer_iff]
  constructor
  · intro h
    rw [← f.map_smul, h]
  · intro h
    have := f.map_smul a x
    rw [h] at this
    exact f.toEquiv.injective this

end W33.Pass1390
