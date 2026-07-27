import W33.Pass465CoverLawL2L4Q3
import Mathlib.Data.Fintype.Card
import Mathlib.Tactic.Ring

namespace W33.Pass477

/-!
# Uniform projective-chart cardinality over finite fields

A normalized representative in projective 3-space is partitioned by the first
nonzero coordinate. Relative to the fixed symplectic point used by the cover
chart, the opposite/bulk chart has three free coordinates and the rim is a
projective plane. The types below encode those normal forms directly.
-/

variable (K : Type*) [Field K] [Fintype K]

abbrev q : ℕ := Fintype.card K
abbrev BulkRep := (K × K) × K
abbrev LineRep := Sum K PUnit
abbrev RimRep := Sum (K × K) (Sum K PUnit)
abbrev PG3Rep := Sum (BulkRep K) (RimRep K)

omit [Field K] in
theorem card_bulk : Fintype.card (BulkRep K) = (q K)^3 := by
  simp [BulkRep, q, pow_succ, Nat.mul_assoc]

omit [Field K] in
theorem card_projective_line : Fintype.card (LineRep K) = q K + 1 := by
  simp [LineRep, q]

omit [Field K] in
theorem card_rim : Fintype.card (RimRep K) = (q K)^2 + q K + 1 := by
  simp [RimRep, q, pow_two]
  ring

omit [Field K] in
theorem card_pg3 : Fintype.card (PG3Rep K) = (q K + 1) * ((q K)^2 + 1) := by
  simp [PG3Rep, BulkRep, RimRep, q, pow_two]
  ring

omit [Field K] in
theorem card_bulk_rim_split :
    Fintype.card (PG3Rep K) = (q K)^3 + ((q K)^2 + q K + 1) := by
  simp [PG3Rep, BulkRep, RimRep, q, pow_succ, Nat.mul_assoc]
  ring

def bulkFiberEquiv : BulkRep K ≃ (K × K) × K := Equiv.refl _

omit [Field K] in
theorem card_fiber_base : Fintype.card (K × K) = (q K)^2 := by
  simp [q, pow_two]

omit [Field K] in
theorem card_each_fiber : Fintype.card K = q K := rfl

omit [Field K] in
theorem card_bulk_as_fibers :
    Fintype.card (BulkRep K) = Fintype.card (K × K) * Fintype.card K := by
  simp [BulkRep]

omit [Field K] in
theorem cover_shell_total_uniform :
    1 + ((q K : ℤ)^2 - 1) + ((q K : ℤ)^2 - 1) * ((q K : ℤ) - 1) +
      ((q K : ℤ) - 1) = (q K : ℤ)^3 := by
  exact W33.Pass465.cover_shell_total (q K)

end W33.Pass477
