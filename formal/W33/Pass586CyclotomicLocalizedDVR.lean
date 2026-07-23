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
open W33.Pass570 W33.Pass575 W33.Pass581
noncomputable section

theorem uniformizerIdeal_isMaximal : uniformizerIdeal.IsMaximal := by
  rw [Ideal.Quotient.maximal_ideal_iff_isField_quotient]
  exact RingEquiv.isField residueQuotientEquiv

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
  have hroot := AdjoinRoot.eval₂_root shiftedPhiFive
  have hquartic :
      lambdaBar ^ 4 = AdjoinRoot.of shiftedPhiFive 5 *
          (lambdaBar ^ 3 - 2 * lambdaBar ^ 2 + 2 * lambdaBar - 1) := by
    have h0 : lambdaBar ^ 4 - 5 * lambdaBar ^ 3 + 10 * lambdaBar ^ 2 -
            10 * lambdaBar + 5 = 0 := by
      simpa [shiftedPhiFive, lambdaBar] using hroot
    linear_combination h0
  simpa [localLambda, unitFactor] using
    congrArg (algebraMap CyclotomicFiveOrder LocalCyclotomicFiveOrder) hquartic

theorem unitFactor_residue_nonzero :
    unitFactor ∉ IsLocalRing.maximalIdeal LocalCyclotomicFiveOrder := by
  rw [← local_maximalIdeal_eq]
  intro h
  have hcomap : lambdaBar ^ 3 - 2 * lambdaBar ^ 2 + 2 * lambdaBar - 1 ∈
        uniformizerIdeal := by
    exact (Localization.AtPrime.to_map_mem_maximal_iff
      LocalCyclotomicFiveOrder uniformizerIdeal
      (lambdaBar ^ 3 - 2 * lambdaBar ^ 2 + 2 * lambdaBar - 1)).mp h
  have hr := congrArg residueMap
    (show lambdaBar ^ 3 - 2 * lambdaBar ^ 2 + 2 * lambdaBar - 1 ∈
      uniformizerIdeal from hcomap)
  simp [uniformizerIdeal, residueMap_lambda] at hr

theorem unitFactor_isUnit : IsUnit unitFactor := by
  exact (IsLocalRing.not_isUnit_iff_mem_maximalIdeal unitFactor).not.mp
    unitFactor_residue_nonzero

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
