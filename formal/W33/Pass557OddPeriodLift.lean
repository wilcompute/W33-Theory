import Mathlib

/-!
# Pass 557: odd-switch period lifting

The exact companion-matrix computation gives period
`312 * 5^ceil((k-1)/2)` at precision `π^k`. On natural-number precision
indices this is represented by the two-step recurrence below.
-/

namespace W33.Pass557

/-- Period of the odd-switch trace automaton at `π`-adic precision `k`.
The unused value at precision zero is fixed to 312 so the two-step recurrence
has no exceptional case. -/
def oddPeriod : Nat → Nat
  | 0 => 312
  | 1 => 312
  | k + 2 => 5 * oddPeriod k

/-- Each two additional `π`-adic digits multiply the period by five. -/
theorem oddPeriod_step (k : Nat) :
    oddPeriod (k + 2) = 5 * oddPeriod k := by
  rfl

/-- The first seven precision periods used by the executable certificate. -/
theorem oddPeriod_first_seven :
    [oddPeriod 1, oddPeriod 2, oddPeriod 3, oddPeriod 4,
     oddPeriod 5, oddPeriod 6, oddPeriod 7]
      = [312, 1560, 1560, 7800, 7800, 39000, 39000] := by
  decide

/-- The recurrence is equivalent to the closed natural-number exponent form
on the checked precision range. This finite theorem is deliberately separate
from the local-field order-lifting hypothesis. -/
theorem oddPeriod_closed_first_seven :
    ∀ k ∈ Finset.Icc 1 7, oddPeriod k = 312 * 5 ^ (k / 2) := by
  decide

/-- Explicit interface for the companion-matrix order theorem. -/
structure OddPeriodLiftCertificate where
  matrixOrder : Nat → Nat
  orderLaw : ∀ k, 1 ≤ k → matrixOrder k = oddPeriod k
  valuationAtLift : Nat → Nat
  liftLaw : ∀ j, valuationAtLift j = 2 * j + 1

/-- The all-precision automaton period follows directly from the certified
matrix-order law. -/
theorem odd_switch_period
    (h : OddPeriodLiftCertificate) (k : Nat) (hk : 1 ≤ k) :
    h.matrixOrder k = oddPeriod k := h.orderLaw k hk

/-- The observed lift valuations are odd and advance by two. -/
theorem odd_switch_lift_valuation
    (h : OddPeriodLiftCertificate) (j : Nat) :
    h.valuationAtLift j = 2 * j + 1 := h.liftLaw j

end W33.Pass557
