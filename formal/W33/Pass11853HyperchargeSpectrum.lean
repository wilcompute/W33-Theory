import Mathlib

namespace W33.Pass11853

/-!
Pass 11853: the Georgi–Glashow hypercharge spectrum on `E₈ = (24,1) + (1,24) + (10,5) + (10̄,5̄) + (5̄,10) + (5,10̄)`.

Pass 11845 found numerically that the direction separating the faithful Lorentz commutant `su(5)` from the
torus-extension commutant `su(3) ⊕ su(2)` has, on all of `E₈`, the ad-spectrum
`0³⁶ (±1/6)³⁰ (±1/3)³⁰ (±1/2)²⁰ (±2/3)¹⁵ (±5/6)⁶ (±1)⁵`.  Here that spectrum is derived from the hypercharge of the
`5` (three colours `-1/3`, two isospins `1/2`), in units of `1/6`:
* the `24` carries the differences `yᵢ - yⱼ` (one zero removed);
* the GUT `10 = Λ²5` carries the pair sums, with Lorentz multiplicity `5`;
* the GUT `5̄` carries `-yᵢ`, with Lorentz multiplicity `10`;
* the Lorentz-side `24` is hypercharge-neutral.
-/

/-- `6Y` on the GUT `5`. -/
def y5 : List ℤ := [-2, -2, -2, 3, 3]

/-- `6Y` on the adjoint `24`: all differences, one zero removed. -/
def adj24 : List ℤ := (y5.flatMap fun a => y5.map fun b => a - b).erase 0

/-- `6Y` on the GUT `10 = Λ²5`. -/
def w10 : List ℤ := (y5.sublistsLen 2).map List.sum

/-- `n` copies of a list. -/
def rep (n : ℕ) (l : List ℤ) : List ℤ := (List.replicate n l).flatten

/-- `6Y` on all `248` directions of `E₈`. -/
def spec248 : List ℤ :=
  adj24 ++ List.replicate 24 0 ++ rep 5 w10 ++ rep 5 (w10.map Neg.neg) ++ rep 10 (y5.map Neg.neg) ++ rep 10 y5

set_option maxRecDepth 100000 in
theorem w10_is_Q_uc_ec : w10.count 1 = 6 ∧ w10.count (-4) = 3 ∧ w10.count 6 = 1 := by decide

set_option maxRecDepth 100000 in
theorem spec_length : spec248.length = 248 := by decide

set_option maxRecDepth 100000 in
/-- The Georgi–Glashow spectrum, in sixths: `0³⁶ (±1)³⁰ (±2)³⁰ (±3)²⁰ (±4)¹⁵ (±5)⁶ (±6)⁵`. -/
theorem spec_counts :
    spec248.count 0 = 36 ∧
    spec248.count 1 = 30 ∧ spec248.count (-1) = 30 ∧
    spec248.count 2 = 30 ∧ spec248.count (-2) = 30 ∧
    spec248.count 3 = 20 ∧ spec248.count (-3) = 20 ∧
    spec248.count 4 = 15 ∧ spec248.count (-4) = 15 ∧
    spec248.count 5 = 6 ∧ spec248.count (-5) = 6 ∧
    spec248.count 6 = 5 ∧ spec248.count (-6) = 5 := by
  decide

set_option maxRecDepth 100000 in
/-- Hypercharge is traceless on `E₈` (it lies in a semisimple algebra). -/
theorem spec_traceless : spec248.sum = 0 := by decide

end W33.Pass11853
