import W33.Pass575CyclotomicDVRKernel
import Mathlib.Tactic

/-!
# Pass 1063: the signed E8 lift obstruction

Pass 1055 reduced the failure of an internal signed lift to four equations over
`F₂`. Adding the equations cancels every gauge variable and leaves `0 = 1`.
This file formalizes that certificate and also imports the actual Pass 575
module as a build lock, so the full umbrella build verifies both obligations.
-/

namespace W33.Pass1063

/-- The four-row certificate proves that no assignment of the six displayed
sign variables can satisfy the signed-lift equations. -/
theorem signedLiftFourRowObstruction
    (s0 s1 s48 s49 s50 s60 : ZMod 2)
    (h1 : s0 + s1 + s49 + s50 = 0)
    (h2 : s0 + s1 + s48 + s50 = 0)
    (h3 : s0 + s49 + s50 + s60 = 1)
    (h4 : s0 + s48 + s50 + s60 = 0) :
    False := by
  -- The certificate is sound: summing the four rows cancels every variable
  -- (each occurs an even number of times) and leaves 0 = 1.  But that
  -- cancellation IS the characteristic-two fact, and `linear_combination`
  -- discharges its residue with `ring`, which normalizes numerals without
  -- knowing 2 = 0 in `ZMod 2` -- so it was left with `4*s0 + 2*s1 + ... = 0`
  -- and failed.  Over six two-valued variables the statement is 64 cases, so
  -- decide it.
  revert h1 h2 h3 h4
  revert s0 s1 s48 s49 s50 s60
  decide

/-- Compilation of this definition is a regression lock on the actual imported
Pass 575 kernel certificate, not on the detached proposal file under `lean/`. -/
theorem pass575BuildLock : W33.Pass575.OrderLocalCertificate :=
  W33.Pass575.orderLocalCertificate

end W33.Pass1063
