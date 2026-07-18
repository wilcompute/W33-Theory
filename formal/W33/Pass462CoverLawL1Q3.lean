import W33.Pass457PerpMonotonicity
import Mathlib.Data.Matrix.Notation

namespace W33.Pass462

/-!
The abstract span/perp core of cover-law L1 was proved in Passes 447 and 457.
This module closes L1 objectwise at q=3: it defines canonical projective
representatives in F_3^4, the symplectic form, the fixed point p0, the central
elation orbit map, and verifies the exact four-rim/zero-bulk common-neighbor
statement by finite kernel-checked computation.
-/

abbrev F3 := ZMod 3
abbrev V4 := Fin 4 → F3

def symp (x y : V4) : F3 :=
  x 0 * y 2 - x 2 * y 0 + x 1 * y 3 - x 3 * y 1

def p0 : V4 := ![0, 0, 0, 1]

/-- Unique normalized representative of a point of PG(3,3): the first nonzero
coordinate is one. -/
def Canonical (v : V4) : Prop :=
  v 0 = 1 ∨
  (v 0 = 0 ∧ v 1 = 1) ∨
  (v 0 = 0 ∧ v 1 = 0 ∧ v 2 = 1) ∨
  (v 0 = 0 ∧ v 1 = 0 ∧ v 2 = 0 ∧ v 3 = 1)

def points : Finset V4 := Finset.univ.filter Canonical

def Opposite (x : V4) : Prop := Canonical x ∧ symp p0 x ≠ 0

def Rim (x : V4) : Prop := Canonical x ∧ symp p0 x = 0

/-- The vector representative of the central-elation translate used in Pass 394.
Only the last projective coordinate changes, so canonical representatives stay
canonical on the opposite chart. -/
def zact (t : F3) (x : V4) : V4 :=
  fun i => x i + t * symp x p0 * p0 i

def Common (x y w : V4) : Prop :=
  Canonical w ∧ w ≠ x ∧ w ≠ y ∧ symp w x = 0 ∧ symp w y = 0

def commonSet (x : V4) (t : F3) : Finset V4 :=
  points.filter fun w => Common x (zact t x) w

def commonBulkSet (x : V4) (t : F3) : Finset V4 :=
  points.filter fun w => Common x (zact t x) w ∧ symp p0 w ≠ 0

/-- The general linear-algebraic implication used by L1, restated as the bridge
from the projective computation to Pass 457. -/
theorem abstract_l1_axis
    {K : Type*} [Field K] {V : Type*} [AddCommGroup V] [Module K V]
    (B : LinearMap.BilinForm K V) (c : K) (hc : c ≠ 0) (x p : V) :
    B.orthogonal (Submodule.span K {x, x + c • p}) ≤
      B.orthogonal (Submodule.span K {p}) :=
  W33.Pass457.shifted_pair_orthogonal_le_axis B c hc x p

/-- Every common neighbor of two distinct members of a central-elation fiber is
in the rim p0^perp. -/
theorem q3_L1_all_common_in_rim :
    ∀ x : V4, Opposite x → ∀ t : F3, t ≠ 0 → ∀ w : V4,
      Common x (zact t x) w → symp p0 w = 0 := by
  native_decide

/-- The perpendicular line contains exactly q+1=4 projective common neighbors. -/
theorem q3_L1_common_card_four :
    ∀ x : V4, Opposite x → ∀ t : F3, t ≠ 0 →
      (commonSet x t).card = 4 := by
  native_decide

/-- None of those common neighbors lies in the opposite/bulk chart. -/
theorem q3_L1_bulk_common_card_zero :
    ∀ x : V4, Opposite x → ∀ t : F3, t ≠ 0 →
      (commonBulkSet x t).card = 0 := by
  native_decide

/-- End-to-end q=3 package for cover-law lemma L1. -/
theorem q3_cover_law_L1 :
    (∀ x : V4, Opposite x → ∀ t : F3, t ≠ 0 → ∀ w : V4,
      Common x (zact t x) w → Rim w) ∧
    (∀ x : V4, Opposite x → ∀ t : F3, t ≠ 0 →
      (commonSet x t).card = 4) ∧
    (∀ x : V4, Opposite x → ∀ t : F3, t ≠ 0 →
      (commonBulkSet x t).card = 0) := by
  constructor
  · intro x hx t ht w hw
    exact ⟨hw.1, q3_L1_all_common_in_rim x hx t ht w hw⟩
  · exact ⟨q3_L1_common_card_four, q3_L1_bulk_common_card_zero⟩

end W33.Pass462
