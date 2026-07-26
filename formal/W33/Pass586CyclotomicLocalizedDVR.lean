import W33.Pass581CyclotomicCompletion
import Mathlib.RingTheory.Localization.AtPrime.Basic
import Mathlib.RingTheory.AdicCompletion.LocalRing
import Mathlib.RingTheory.DiscreteValuationRing.TFAE

/-!
# Pass 586: localize the fifth-cyclotomic order before completion

The integral order is not itself local: it has primes above rational primes other
than five. The correct local object is the localization at the principal
uniformizer ideal. This file defines that localization and its maximal-ideal
completion, records the residue-field equivalence, and isolates the remaining
Noetherian-domain input needed for the generic DVR theorem.
-/
namespace W33.Pass586
open Polynomial W33.Pass570 W33.Pass575 W33.Pass581
noncomputable section

theorem uniformizerIdeal_isMaximal : uniformizerIdeal.IsMaximal := by
  -- `RingEquiv.isField` no longer exists; the surviving form is
  -- `MulEquiv.isField (hB : IsField B) (e : A ≃* B)`, and `ZMod 5` is a field
  -- only in the presence of `Fact (Nat.Prime 5)`.
  haveI : Fact (Nat.Prime 5) := ⟨by norm_num⟩
  rw [Ideal.Quotient.maximal_ideal_iff_isField_quotient]
  exact MulEquiv.isField (Field.toIsField (ZMod 5)) residueQuotientEquiv.toMulEquiv

local instance : uniformizerIdeal.IsMaximal := uniformizerIdeal_isMaximal
local instance : uniformizerIdeal.IsPrime := uniformizerIdeal_isMaximal.isPrime
abbrev LocalCyclotomicFiveOrder := Localization.AtPrime uniformizerIdeal

theorem local_maximalIdeal_eq :
    IsLocalRing.maximalIdeal LocalCyclotomicFiveOrder =
      Ideal.map (algebraMap CyclotomicFiveOrder LocalCyclotomicFiveOrder)
        uniformizerIdeal := by
  symm
  exact Localization.AtPrime.map_eq_maximalIdeal

noncomputable def localResidueEquiv :
    CyclotomicFiveOrder ⧸ uniformizerIdeal ≃+*
      LocalCyclotomicFiveOrder ⧸ IsLocalRing.maximalIdeal LocalCyclotomicFiveOrder :=
  IsLocalization.AtPrime.equivQuotMaximalIdeal uniformizerIdeal LocalCyclotomicFiveOrder

abbrev CompletedLocalCyclotomicFiveOrder :=
  AdicCompletion (IsLocalRing.maximalIdeal LocalCyclotomicFiveOrder)
    LocalCyclotomicFiveOrder

noncomputable def localLambda : LocalCyclotomicFiveOrder :=
  algebraMap CyclotomicFiveOrder LocalCyclotomicFiveOrder lambdaBar
noncomputable def completedLocalLambda : CompletedLocalCyclotomicFiveOrder :=
  algebraMap LocalCyclotomicFiveOrder CompletedLocalCyclotomicFiveOrder localLambda
noncomputable def unitFactor : LocalCyclotomicFiveOrder :=
  algebraMap CyclotomicFiveOrder LocalCyclotomicFiveOrder
    (lambdaBar ^ 3 - 2 * lambdaBar ^ 2 + 2 * lambdaBar - 1)

theorem local_ramification_relation :
    localLambda ^ 4 =
      algebraMap CyclotomicFiveOrder LocalCyclotomicFiveOrder
          (AdjoinRoot.of shiftedPhiFive 5) * unitFactor := by
  have hquartic :
      lambdaBar ^ 4 = AdjoinRoot.of shiftedPhiFive 5 *
          (lambdaBar ^ 3 - 2 * lambdaBar ^ 2 + 2 * lambdaBar - 1) := by
    -- Second copy of the Pass 575 defect: going via `eval₂_root` + `simpa`
    -- stalls with an unevaluated `eval₂` atom.  Take `mk f f = 0` instead, with
    -- the argument unfolded and the subscript folded.
    have h0 : lambdaBar ^ 4 - 5 * lambdaBar ^ 3 + 10 * lambdaBar ^ 2 -
            10 * lambdaBar + 5 = 0 := by
      have h : (AdjoinRoot.mk shiftedPhiFive)
          (X ^ 4 - C 5 * X ^ 3 + C 10 * X ^ 2 - C 10 * X + C 5) = 0 :=
        AdjoinRoot.mk_self
      simp only [map_add, map_sub, map_mul, map_pow, map_ofNat,
        AdjoinRoot.mk_X] at h
      simp only [lambdaBar]
      linear_combination h
    -- `AdjoinRoot.of _ 5` is an atom to `ring` until it is reduced to the numeral.
    have hof : (AdjoinRoot.of shiftedPhiFive) 5 = (5 : CyclotomicFiveOrder) := by simp
    rw [hof]
    linear_combination h0
  simpa [localLambda, unitFactor] using
    congrArg (algebraMap CyclotomicFiveOrder LocalCyclotomicFiveOrder) hquartic

theorem unitFactor_residue_nonzero :
    unitFactor ∉ IsLocalRing.maximalIdeal LocalCyclotomicFiveOrder := by
  -- was `rw [← local_maximalIdeal_eq]`, which searches for `Ideal.map ...` in a
  -- goal that already says `maximalIdeal`.  No rewrite is needed at all.
  intro h
  -- the lemma lives in `IsLocalization.AtPrime`, not `Localization.AtPrime`
  have hcomap : lambdaBar ^ 3 - 2 * lambdaBar ^ 2 + 2 * lambdaBar - 1 ∈
        uniformizerIdeal :=
    (IsLocalization.AtPrime.to_map_mem_maximal_iff
      LocalCyclotomicFiveOrder uniformizerIdeal
      (lambdaBar ^ 3 - 2 * lambdaBar ^ 2 + 2 * lambdaBar - 1)).mp h
  -- The old proof applied `congrArg residueMap` to `hcomap`, which is a
  -- MEMBERSHIP proof and not an equation -- hence the type mismatch.  Turn the
  -- membership into the equation it implies first, then push the residue map
  -- through it: the residue kills lambdaBar, so the right side is 0 while the
  -- left is -1 in ZMod 5.
  rw [uniformizerIdeal, Ideal.mem_span_singleton] at hcomap
  obtain ⟨c, hc⟩ := hcomap
  have hr := congrArg residueMap hc
  simp [residueMap_lambda] at hr
  -- simp lands on `hr : (1 : ZMod 5) = 0` but does not discharge it
  exact absurd hr (by decide)

theorem unitFactor_isUnit : IsUnit unitFactor := by
  -- `IsLocalRing.not_isUnit_iff_mem_maximalIdeal` is gone; the surviving lemma is
  -- `IsLocalRing.mem_maximalIdeal x : x ∈ maximalIdeal R ↔ x ∈ nonunits R`.
  have h := unitFactor_residue_nonzero
  rw [IsLocalRing.mem_maximalIdeal, mem_nonunits_iff, not_not] at h
  exact h

structure LocalDVRBoundary where
  order_is_domain : Prop
  local_order_is_noetherian : Prop
  maximal_ideal_is_generated_by_localLambda : Prop
  completion_is_dvr : Prop
  normalized_value_lambda : Prop
  ramification_index_four : Prop
  residue_degree_one : Prop
end
end W33.Pass586
