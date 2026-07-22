import Mathlib

/-!
# Pass 560: the fifth-cyclotomic uniformizer identity

This module moves one layer below the certificate interfaces of Pass 557.  It
formalizes the exact algebraic identity obtained by translating the fifth
cyclotomic polynomial by `lambda = 1 - zeta`, and derives the ramification
factorization `lambda^4 = 5 * unitFactor`.
-/

namespace W33.Pass560

section CyclotomicIdentity

variable {R : Type*} [CommRing R]

/-- The fifth cyclotomic polynomial evaluated at an element. -/
def phiFive (z : R) : R := z ^ 4 + z ^ 3 + z ^ 2 + z + 1

/-- The factor multiplying five after the shift `lambda = 1 - z`. -/
def unitFactor (lambda : R) : R :=
  lambda ^ 3 - 2 * lambda ^ 2 + 2 * lambda - 1

/-- Exact translation of `Phi_5(z)` to the uniformizer coordinate. -/
theorem phiFive_shift_identity (z : R) :
    (1 - z) ^ 4 - 5 * unitFactor (1 - z) = phiFive z := by
  simp [phiFive, unitFactor]
  ring

/-- A fifth root satisfying `Phi_5(z)=0` obeys the exact ramification identity. -/
theorem lambda_pow_four_eq_five_mul
    (z : R) (hz : phiFive z = 0) :
    (1 - z) ^ 4 = 5 * unitFactor (1 - z) := by
  have h := phiFive_shift_identity z
  rw [hz] at h
  exact sub_eq_zero.mp h

/-- The residual factor is congruent to `-1` modulo `lambda`. -/
theorem unitFactor_add_one_factorization (lambda : R) :
    unitFactor lambda + 1 = lambda * (lambda ^ 2 - 2 * lambda + 2) := by
  simp [unitFactor]
  ring

/-- The shifted polynomial itself has coefficients `1,-5,10,-10,5`. -/
theorem shifted_coefficient_identity (lambda : R) :
    lambda ^ 4 - 5 * lambda ^ 3 + 10 * lambda ^ 2 - 10 * lambda + 5 =
      lambda ^ 4 - 5 * unitFactor lambda := by
  simp [unitFactor]
  ring

end CyclotomicIdentity

section ValuationTransport

variable {R : Type*} [CommRing R]

/-- Minimal additive-valuation interface needed to transport the exact
cyclotomic factorization.  Unlike Pass 557, the ramification equation itself is
now proved in this file; only the standard valuation laws and unit status are
fields. -/
structure CyclotomicFiveValuationModel where
  zeta : R
  cyclotomic : phiFive zeta = 0
  val : R → Nat
  val_pow : ∀ x n, val (x ^ n) = n * val x
  val_mul : ∀ x y, val (x * y) = val x + val y
  val_five : val (5 : R) = 4
  unitFactor_value : val (unitFactor (1 - zeta)) = 0

/-- Total ramification at five forces `v(1-zeta)=1`. -/
theorem uniformizer_value_one (h : CyclotomicFiveValuationModel (R := R)) :
    h.val (1 - h.zeta) = 1 := by
  have heq := congrArg h.val (lambda_pow_four_eq_five_mul h.zeta h.cyclotomic)
  rw [h.val_pow, h.val_mul, h.val_five, h.unitFactor_value] at heq
  omega

/-- Every positive power of the cyclotomic uniformizer has the expected value. -/
theorem uniformizer_power_value
    (h : CyclotomicFiveValuationModel (R := R)) (n : Nat) :
    h.val ((1 - h.zeta) ^ n) = n := by
  rw [h.val_pow, uniformizer_value_one h, Nat.mul_one]

end ValuationTransport

end W33.Pass560
