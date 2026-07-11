import Mathlib

/-!
# A q = 3 binary symmetric-matrix block

This file defines the nine-dimensional binary matrix space, the transpose-sum
operator `Y ↦ Y + Yᵀ`, and several kernel/image cardinalities by kernel-checked
finite computation.  It does not define the 40 by 40 W(3,3) incidence matrix or
a Fourier transform connecting these matrices to it.  Consequently these are
exact matrix-space facts, not a formal proof of the W(3,3) Levi rank theorem.
-/

namespace W33.HeisenbergQ3

abbrev F2 := ZMod 2
abbrev Mat3 := Matrix (Fin 3) (Fin 3) F2

/-- The transpose-sum operator on 3 by 3 binary matrices. -/
def transposeSum (Y : Mat3) : Mat3 := Y + Y.transpose

/-- Symmetric matrices over F₂. -/
def IsSymmetric (Y : Mat3) : Prop := Y.transpose = Y

/-- Alternating matrices in characteristic two: symmetric with zero diagonal. -/
def IsAlternating (Y : Mat3) : Prop :=
  IsSymmetric Y ∧ ∀ i, Y i i = 0

/-- The transpose-sum kernel has 64 elements. -/
theorem transposeSum_kernel_card :
    (Finset.univ.filter fun Y : Mat3 => transposeSum Y = 0).card = 64 := by
  native_decide

/-- The transpose-sum image has eight elements. -/
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

/-- Package the three finite cardinality results without rebranding them as
incidence or Fourier ranks. -/
theorem q3_matrix_cardinality_package :
    (Finset.univ.image transposeSum : Finset Mat3).card = 8 ∧
    (Finset.univ.filter fun Y : Mat3 => transposeSum Y = 0).card = 64 ∧
    ((Finset.univ.filter (fun Y : Mat3 => Y.transpose = Y) : Finset Mat3).image diagonal).card = 8 := by
  exact ⟨transposeSum_image_card, transposeSum_kernel_card, diagonal_image_card⟩

end W33.HeisenbergQ3
