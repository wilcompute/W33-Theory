import Mathlib

/-!
# Pass 570: residue map for the fifth-cyclotomic integral order

This module continues the native `AdjoinRoot` construction from Pass 565.  It
constructs the canonical reduction map to `ZMod 5`, proves that the distinguished
uniformizer maps to zero, proves surjectivity, and records the resulting kernel
ideal together with its principal uniformizer containment.

The completed local field and equality of the kernel with the principal ideal
`(lambdaBar)` are intentionally not asserted here; that final step requires the
local unit theorem and completion machinery.
-/

namespace W33.Pass570

open Polynomial

noncomputable section

/-- The shifted fifth cyclotomic polynomial for `lambda = 1 - zeta`. -/
def shiftedPhiFive : ℤ[X] :=
  X ^ 4 - C 5 * X ^ 3 + C 10 * X ^ 2 - C 10 * X + C 5

/-- The native integral fifth-cyclotomic order. -/
abbrev CyclotomicFiveOrder := AdjoinRoot shiftedPhiFive

/-- The distinguished class of the cyclotomic uniformizer. -/
def lambdaBar : CyclotomicFiveOrder := AdjoinRoot.root shiftedPhiFive

/-- The shifted polynomial is monic. -/
theorem shiftedPhiFive_monic : shiftedPhiFive.Monic := by
  -- `simp` does not compute a leading coefficient; `monicity!` is the tactic for
  -- exactly this shape (Mathlib.Tactic.ComputeDegree).
  unfold shiftedPhiFive
  monicity!

/-- Evaluating the shifted polynomial at zero modulo five vanishes. -/
theorem shiftedPhiFive_zero_mod_five :
    Polynomial.eval₂ (Int.castRingHom (ZMod 5)) 0 shiftedPhiFive = 0 := by
  -- `eval₂ f 0 p = f (p.coeff 0)`, and the constant term is 5, which is 0 mod 5.
  rw [Polynomial.eval₂_at_zero]
  simp [shiftedPhiFive]
  -- whatever survives is the numeric fact (5 : ZMod 5) = 0
  all_goals decide

/-- Canonical residue map, sending the uniformizer to zero. -/
def residueMap : CyclotomicFiveOrder →+* ZMod 5 :=
  AdjoinRoot.lift (Int.castRingHom (ZMod 5)) 0 shiftedPhiFive_zero_mod_five

@[simp]
theorem residueMap_lambda : residueMap lambdaBar = 0 := by
  simp [residueMap, lambdaBar]

@[simp]
theorem residueMap_integer (n : ℤ) :
    residueMap (AdjoinRoot.of shiftedPhiFive n) = (n : ZMod 5) := by
  simp [residueMap]

/-- The residue map is onto `F_5`. -/
theorem residueMap_surjective : Function.Surjective residueMap := by
  intro y
  refine ⟨AdjoinRoot.of shiftedPhiFive (y.val : ℤ), ?_⟩
  simpa [residueMap] using (ZMod.natCast_zmod_val y)

/-- The exact residue-kernel ideal. -/
def residueIdeal : Ideal CyclotomicFiveOrder := RingHom.ker residueMap

/-- The uniformizer lies in the residue kernel. -/
theorem lambda_mem_residueIdeal : lambdaBar ∈ residueIdeal := by
  change residueMap lambdaBar = 0
  exact residueMap_lambda

/-- Five lies in the residue kernel. -/
theorem five_mem_residueIdeal :
    AdjoinRoot.of shiftedPhiFive 5 ∈ residueIdeal := by
  change residueMap (AdjoinRoot.of shiftedPhiFive 5) = 0
  -- `lift` must be pushed through `of` FIRST; without `lift_of` the goal is an
  -- unreduced `lift ... 5` and `decide` gets stuck on its Decidable instance.
  simp only [residueMap, AdjoinRoot.lift_of]
  decide

/-- The principal uniformizer ideal is contained in the residue kernel. -/
theorem lambda_span_le_residueIdeal :
    Ideal.span ({lambdaBar} : Set CyclotomicFiveOrder) ≤ residueIdeal := by
  rw [Ideal.span_le]
  intro x hx
  rcases hx with rfl
  exact lambda_mem_residueIdeal

/-- Presentation-level description of the remaining local-field obligation. -/
structure CompletionObligations where
  kernel_is_uniformizer_span : residueIdeal = Ideal.span ({lambdaBar} : Set CyclotomicFiveOrder)
  completion_is_field : Prop
  completion_is_complete : Prop
  totally_ramified_degree_four : Prop

end

end W33.Pass570
