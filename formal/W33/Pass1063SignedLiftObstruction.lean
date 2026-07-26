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
  have impossible : (0 : ZMod 2) = 1 := by
    linear_combination h1 + h2 + h3 + h4
  exact zero_ne_one impossible

/-- Compilation of this definition is a regression lock on the actual imported
Pass 575 kernel certificate, not on the detached proposal file under `lean/`. -/
def pass575BuildLock : W33.Pass575.OrderLocalCertificate :=
  W33.Pass575.orderLocalCertificate

end W33.Pass1063
