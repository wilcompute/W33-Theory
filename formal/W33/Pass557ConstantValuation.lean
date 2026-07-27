import Mathlib

/-!
# Pass 557: constant-family valuation control

This file formalizes the finite residue-control layer used by the exact
q = 5 constant-section valuation theorem. The cyclotomic Hensel/LTE input is
kept as an explicit hypothesis: this module does not pretend that local-field
analysis has already been reconstructed inside Lean.
-/

namespace W33.Pass557

/-- The base correction attached to an odd exponent modulo 20. Residues 5 and
15 carry an additional `4 * v₅(m)` term in the analytic theorem; this function
records the residue-only part. -/
def constantOddBase (m : Nat) : Nat :=
  match m % 20 with
  | 1  => 6
  | 3  => 2
  | 5  => 4
  | 7  => 2
  | 9  => 4
  | 11 => 2
  | 13 => 4
  | 15 => 2
  | 17 => 4
  | 19 => 2
  | _  => 0

/-- One complete odd residue period. -/
theorem constantOddBase_period :
    [constantOddBase 1, constantOddBase 3, constantOddBase 5,
     constantOddBase 7, constantOddBase 9, constantOddBase 11,
     constantOddBase 13, constantOddBase 15, constantOddBase 17,
     constantOddBase 19]
      = [6, 2, 4, 2, 4, 2, 4, 2, 4, 2] := by
  native_decide

/-- The lookup depends only on the residue modulo 20. -/
theorem constantOddBase_mod (m : Nat) :
    constantOddBase (m % 20) = constantOddBase m := by
  simp [constantOddBase]

/-- Interface for the local-field part of the constant-family theorem. -/
structure ConstantValuationCertificate where
  delta : Nat → Nat
  fiveValuation : Nat → Nat
  evenFour : ∀ m, 4 ∣ m → delta m = 0
  twiceOdd : ∀ r, Odd r → delta (2 * r) = 2 + 4 * fiveValuation r
  oddResidue : ∀ m, Odd m →
    delta m = constantOddBase m +
      (if m % 20 = 5 ∨ m % 20 = 15 then 4 * fiveValuation m else 0)

/-- Once the Hensel/LTE certificate is supplied, the all-exponent odd formula
is available without any hidden assumptions. -/
theorem constant_odd_formula
    (h : ConstantValuationCertificate) (m : Nat) (hm : Odd m) :
    h.delta m = constantOddBase m +
      (if m % 20 = 5 ∨ m % 20 = 15 then 4 * h.fiveValuation m else 0) :=
  h.oddResidue m hm

/-- The even-multiple-of-four branch is isolated explicitly. -/
theorem constant_four_divides_formula
    (h : ConstantValuationCertificate) (m : Nat) (hm : 4 ∣ m) :
    h.delta m = 0 := h.evenFour m hm

end W33.Pass557
