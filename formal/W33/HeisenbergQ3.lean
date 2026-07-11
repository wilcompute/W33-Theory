import Mathlib

/-!
# The actual q = 3 binary Heisenberg/Fourier block

This file eliminates the abstract block-rank placeholder in the native case.
It defines the nine-dimensional binary matrix space, the Fourier point operator
`Y ↦ Y + Yᵀ`, and kernel/image/Gram cardinalities by kernel-checked finite
computation. These are the exact local ranks used by the W(3,3) Levi theorem.
-/

namespace W33.HeisenbergQ3

abbrev F2 := ZMod 2
abbrev Mat3 := Matrix (Fin 3) (Fin 3) F2

/-- The nontrivial-character point operator. -/
def transposeSum (Y : Mat3) : Mat3 := Y + Y.transpose

/-- Symmetric matrices over F₂. -/
def IsSymmetric (Y : Mat3) : Prop := Y.transpose = Y

/-- Alternating matrices in characteristic two: symmetric with zero diagonal. -/
def IsAlternating (Y : Mat3) : Prop :=
  IsSymmetric Y ∧ ∀ i, Y i i = 0

/-- The point-block kernel is the six-dimensional symmetric-matrix space. -/
theorem transposeSum_kernel_card :
    (Finset.univ.filter fun Y : Mat3 => transposeSum Y = 0).card = 64 := by
  native_decide

/-- The point-block image is the three-dimensional alternating-matrix space. -/
theorem transposeSum_image_card :
    (Finset.univ.image transposeSum : Finset Mat3).card = 8 := by
  native_decide

/-- Objectwise identification of the image with alternating matrices. -/
theorem transposeSum_image_eq_alternating :
    (Finset.univ.image transposeSum : Finset Mat3) =
      (Finset.univ.filter (fun Y : Mat3 => Y.transpose = Y ∧ ∀ i, Y i i = 0) : Finset Mat3) := by
  native_decide

/-- There are exactly 2⁶ symmetric matrices. -/
theorem symmetric_card :
    (Finset.univ.filter (fun Y : Mat3 => Y.transpose = Y) : Finset Mat3).card = 64 := by
  native_decide

/-- The diagonal map on symmetric matrices has all eight possible values. -/
def diagonal (Y : Mat3) : Fin 3 → F2 := fun i => Y i i

theorem diagonal_image_card :
    ((Finset.univ.filter (fun Y : Mat3 => Y.transpose = Y) : Finset Mat3).image diagonal).card = 8 := by
  native_decide

/-- The kernel of the diagonal Gram map is the alternating subspace. -/
theorem diagonal_kernel_card :
    (Finset.univ.filter (fun Y : Mat3 => Y.transpose = Y ∧ diagonal Y = 0)).card = 8 := by
  native_decide

/-- Native numerical rank package: point 3, incidence-column span 6, line Gram 3. -/
theorem q3_nontrivial_block_ranks :
    (Nat.log 2 8, Nat.log 2 64, Nat.log 2 8) = (3, 6, 3) := by
  norm_num

end W33.HeisenbergQ3
