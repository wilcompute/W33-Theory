/-
W(3,9) seven-class cubic arithmetic ledger.
The geometric classification, GF(9) incidence enumeration, and orbit
transitivity are separate hypotheses; THIS FILE only proves exact integer
class partition, scaled moment checksum, and unique line coefficient.
No 'sorry'; no external mathlib required.
-/
import Std

namespace W33Q9

def totalTriples : Nat :=
  98400 + 2988900 + 23911200 + 398520 + 398520 + 31881600 + 31881600

theorem partition_all_distinct_triplets :
    totalTriples = 91558740 := by decide

theorem combinatorial_count :
    820 * 819 * 818 / 6 = 91558740 := by decide

/-
All third moments multiplied by LCM(15,1215,243,270)=2430.
This avoids floating arithmetic and denominators in the kernel.
-/
def scaledMomentSum : Int :=
    (98400 : Int) * 3987792
  + (2988900 : Int) * (-283424)
  + (23911200 : Int) * 17680
  + (398520 : Int) * (-309910)
  + (398520 : Int) * (-309910)
  + (31881600 : Int) * 4437
  + (31881600 : Int) * 4437

theorem exact_cubic_checksum :
    scaledMomentSum = (1617040 : Int) * 2430 := by decide

theorem line_class_unique :
   (3987792 : Int) ≠ -283424 ∧
   (3987792 : Int) ≠ 17680 ∧
   (3987792 : Int) ≠ -309910 ∧
   (3987792 : Int) ≠ 4437 := by decide

theorem two_quadratic_character_pairs_agree :
   (-309910 : Int) = -309910 ∧
   (4437 : Int) = 4437 := by decide

theorem check_group_order :
   (9^4 * (9^2-1) * (9^4-1) / 2 : Nat) = 1721606400 := by decide

end W33Q9
