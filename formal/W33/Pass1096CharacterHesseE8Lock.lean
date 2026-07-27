import W33.Pass1091FrameOrbitalIntertwiner
import Mathlib.Tactic

/-!
# Pass 1096: character, Hessian-fiber, and E8 obstruction locks

The large permutation and intertwiner tensors remain external exact certificates.
This module freezes their compact character-theoretic consequences in ATLAS class
order for `U4(2):2`.
-/
namespace W33.Pass1096

def classSizes : List Int :=
  [1,45,270,80,240,480,540,3240,5184,720,1440,1440,2160,5760,4320,
   36,540,540,1620,1440,1440,4320,6480,5184,4320]

def chi81Plus : List Int :=
  [81,9,-3,0,0,0,-3,-1,1,0,0,0,0,0,0,-9,3,-3,1,0,0,0,-1,1,0]

def chi81Minus : List Int :=
  [81,9,-3,0,0,0,-3,-1,1,0,0,0,0,0,0,9,-3,3,-1,0,0,0,1,-1,0]

def outerSign : List Int :=
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]

def e8RootCharacter : List Int :=
  [240,24,60,6,72,12,24,14,20,6,24,6,12,6,6,126,26,12,40,30,6,8,12,6,12]

def e8RootLineCharacter : List Int :=
  [120,24,32,3,36,6,12,8,10,3,12,6,8,3,3,64,16,12,20,16,4,4,6,4,6]

def weightedTriple : List Int → List Int → List Int → Int
  | s :: ss, x :: xs, y :: ys => s*x*y + weightedTriple ss xs ys
  | _, _, _ => 0

theorem minus_is_sign_twist :
    List.zipWith (fun a b : Int => a*b) outerSign chi81Plus = chi81Minus := by
  decide

theorem no_81Plus_in_E8_roots :
    weightedTriple classSizes chi81Plus e8RootCharacter = 0 := by decide

theorem no_81Minus_in_E8_roots :
    weightedTriple classSizes chi81Minus e8RootCharacter = 0 := by decide

theorem no_81Plus_in_E8_root_lines :
    weightedTriple classSizes chi81Plus e8RootLineCharacter = 0 := by decide

theorem no_81Minus_in_E8_root_lines :
    weightedTriple classSizes chi81Minus e8RootLineCharacter = 0 := by decide

theorem inner_frame_dimension :
    1 + 3*15 + 2*20 + 2*24 + 2*30 + 2*30 + 60 + 64 + 2*81 = 540 := by norm_num

theorem inner_rank_from_multiplicities :
    1^2 + 3^2 + 2^2 + 2^2 + 2^2 + 2^2 + 1^2 + 1^2 + 2^2 = 32 := by norm_num

theorem outer_frame_dimension :
    1 + 2*15 + 15 + 2*20 + 2*24 + 60 + 2*60 + 64 + 81 + 81 = 540 := by norm_num

theorem outer_rank_from_multiplicities :
    1^2 + 2^2 + 1^2 + 2^2 + 2^2 + 1^2 + 2^2 + 1^2 + 1^2 + 1^2 = 22 := by norm_num

theorem steinberg_induction_dimension : 81 + 81 = 2*81 := by norm_num

def steinbergPlusHash : String := "1455f33e219d8464a7fac74ca693f31dfa1cf01548c205c7fa246a4802132213"
def steinbergMinusHash : String := "66476d71e75e52b3e06c3ed4b5594e63a095681d14cd3847d88f334fe225b052"

theorem hashes_are_distinct : steinbergPlusHash ≠ steinbergMinusHash := by decide

end W33.Pass1096
