import W33.Pass1106CliffordFirewallCarrier
import Mathlib.Tactic

/-!
# Pass 1110: A₂ carrier, central-phase, and second-vendor closure

Compact kernel-checked consequences extending Passes 1103–1106.  The large E₈
permutation action and Qontrol protocol trace remain executable external
certificates; only their exact arithmetic consequences are frozen here.
-/
namespace W33.Pass1110

def classSizes : List Int :=
  [1,45,270,80,240,480,540,3240,5184,720,1440,1440,2160,5760,4320,
   36,540,540,1620,1440,1440,4320,6480,5184,4320]

def chi81Plus : List Int :=
  [81,9,-3,0,0,0,-3,-1,1,0,0,0,0,0,0,-9,3,-3,1,0,0,0,-1,1,0]

def chi81Minus : List Int :=
  [81,9,-3,0,0,0,-3,-1,1,0,0,0,0,0,0,9,-3,3,-1,0,0,0,1,-1,0]

/-- Fixed-point character of the 2240 unordered A₂ root triples α+β+γ=0. -/
def a2TripleCharacter : List Int :=
  [2240,32,160,26,242,8,32,12,20,2,32,2,10,2,2,672,40,8,80,42,6,4,8,2,8]

def weightedDot : List Int → List Int → List Int → Int
  | s :: ss, x :: xs, y :: ys => s*x*y + weightedDot ss xs ys
  | _, _, _ => 0

/-- The A₂-triple carrier contains no 81₊. -/
theorem a2Triple_no_81Plus :
    weightedDot classSizes chi81Plus a2TripleCharacter = 0 := by
  norm_num [weightedDot, classSizes, chi81Plus, a2TripleCharacter]

/-- The A₂-triple carrier contains exactly three copies of 81₋. -/
theorem a2Triple_three_81Minus :
    weightedDot classSizes chi81Minus a2TripleCharacter = 3 * 51840 := by
  norm_num [weightedDot, classSizes, chi81Minus, a2TripleCharacter]

/-- The all-45 cubic central-phase histogram is 0^25,1^10,2^10. -/
def centralPhaseHistogram : List Nat := [25,10,10]

theorem centralPhase_total : centralPhaseHistogram.sum = 45 := by
  norm_num [centralPhaseHistogram]

theorem centralPhase_nonzero_total : (centralPhaseHistogram.drop 1).sum = 20 := by
  norm_num [centralPhaseHistogram]

/-- The nine signed firewall fibers split 2 positive and 7 negative. -/
def firewallFiberSignCounts : List Nat := [2,7]

theorem firewallFiber_sign_total : firewallFiberSignCounts.sum = 9 := by
  norm_num [firewallFiberSignCounts]

/-- The second vendor schedule has 40 limits, 160 routes, and 40 telemetry queries. -/
def qontrolScheduleCounts : List Nat := [40,160,40]

theorem qontrol_schedule_total : qontrolScheduleCounts.sum = 240 := by
  norm_num [qontrolScheduleCounts]

theorem a2_beats_pair_minimum : 2240 < 3360 := by norm_num

theorem first_tested_plus_stays_orthogonal_pairs : 3360 < 15120 := by norm_num

end W33.Pass1110
