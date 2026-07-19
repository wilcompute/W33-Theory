import W33.Pass462CoverLawL1Q3

namespace W33.Pass465

/-!
# Cover-law L2--L4 at q = 3, plus the uniform parameter arithmetic

Pass 462 closed L1 objectwise for the explicit symplectic model of PG(3,3).
This file keeps that model and verifies the remaining local counts by finite,
kernel-checked computation.  The final section formalizes the intersection-array
and shell arithmetic uniformly over an indeterminate q.  It does not claim that
the finite-field incidence/cardinality lemmas have been proved for every odd
prime power; that geometric uniformization remains the named boundary.
-/

open W33.Pass462

abbrev F3 := W33.Pass462.F3
abbrev V4 := W33.Pass462.V4

/-- Two opposite-chart points lie in the same central-elation fiber. -/
def SameFiber (x y : V4) : Prop := ∃ t : F3, y = zact t x

/-- Common neighbors split by the fixed rim/bulk chart. -/
def pairCommonRimSet (x y : V4) : Finset V4 :=
  points.filter fun w => Common x y w ∧ symp p0 w = 0

def pairCommonBulkSet (x y : V4) : Finset V4 :=
  points.filter fun w => Common x y w ∧ symp p0 w ≠ 0

/-- Bulk neighbors in the induced antipodal cover. -/
def bulkNeighborSet (x : V4) : Finset V4 :=
  points.filter fun w => Opposite w ∧ w ≠ x ∧ symp x w = 0

/-- A length-two path staying inside the bulk chart. -/
def BulkDistanceTwo (x y : V4) : Prop :=
  ∃ u : V4, Opposite u ∧ u ≠ x ∧ u ≠ y ∧ symp x u = 0 ∧ symp u y = 0

/-- The three members of one central-elation fiber. -/
def fiberSet (x : V4) : Finset V4 :=
  points.filter fun y => SameFiber x y

/-- L2 at q=3: a cross-fiber non-collinear pair has one rim and three bulk
common neighbors. -/
theorem q3_L2_common_split_one_three :
    ∀ x y : V4, Opposite x → Opposite y → x ≠ y →
      symp x y ≠ 0 → ¬ SameFiber x y →
      (pairCommonRimSet x y).card = 1 ∧
      (pairCommonBulkSet x y).card = 3 := by
  native_decide

/-- L3 at q=3: a collinear bulk pair has one rim and one bulk common neighbor,
so the induced bulk parameter is lambda=q-2=1. -/
theorem q3_L3_collinear_split_one_one :
    ∀ x y : V4, Opposite x → Opposite y → x ≠ y →
      symp x y = 0 →
      (pairCommonRimSet x y).card = 1 ∧
      (pairCommonBulkSet x y).card = 1 := by
  native_decide

/-- Every q=3 central-elation fiber has q=3 points and is independent in the
bulk collinearity graph. -/
theorem q3_fiber_card_three_independent :
    ∀ x : V4, Opposite x →
      (fiberSet x).card = 3 ∧
      ∀ y ∈ fiberSet x, ∀ z ∈ fiberSet x, y ≠ z → symp y z ≠ 0 := by
  native_decide

/-- L4 at q=3: a nontrivial fiber mate has exactly q^2-1=8 bulk neighbors;
every one is nonadjacent to the original point, lies outside its fiber, and is
at bulk distance two from it. -/
theorem q3_L4_c3_eight_a3_zero :
    ∀ x : V4, Opposite x → ∀ t : F3, t ≠ 0 →
      (bulkNeighborSet (zact t x)).card = 8 ∧
      ∀ w ∈ bulkNeighborSet (zact t x),
        symp x w ≠ 0 ∧ ¬ SameFiber x w ∧ BulkDistanceTwo x w := by
  native_decide

/-- End-to-end q=3 package extending Pass 462 from L1 through L4. -/
theorem q3_cover_law_L1_L4 :
    (∀ x : V4, Opposite x → ∀ t : F3, t ≠ 0 →
      (commonSet x t).card = 4 ∧ (commonBulkSet x t).card = 0) ∧
    (∀ x y : V4, Opposite x → Opposite y → x ≠ y →
      symp x y ≠ 0 → ¬ SameFiber x y →
      (pairCommonRimSet x y).card = 1 ∧ (pairCommonBulkSet x y).card = 3) ∧
    (∀ x y : V4, Opposite x → Opposite y → x ≠ y →
      symp x y = 0 →
      (pairCommonRimSet x y).card = 1 ∧ (pairCommonBulkSet x y).card = 1) ∧
    (∀ x : V4, Opposite x → ∀ t : F3, t ≠ 0 →
      (bulkNeighborSet (zact t x)).card = 8) := by
  exact ⟨
    fun x hx t ht => ⟨q3_L1_common_card_four x hx t ht,
      q3_L1_bulk_common_card_zero x hx t ht⟩,
    q3_L2_common_split_one_three,
    q3_L3_collinear_split_one_one,
    fun x hx t ht => (q3_L4_c3_eight_a3_zero x hx t ht).1
  ⟩

/-! ## Uniform symbolic intersection-array arithmetic -/

/-- The cover-law identity b1=(q^2-1)-1-(q-2)=q(q-1). -/
theorem cover_b1_identity (q : ℤ) :
    (q^2 - 1) - 1 - (q - 2) = q * (q - 1) := by
  ring

/-- Edge-balance recurrences for shell sizes
1, q^2-1, (q^2-1)(q-1), q-1. -/
theorem cover_shell_recurrences (q : ℤ) :
    ((q^2 - 1) * 1 = 1 * (q^2 - 1)) ∧
    (((q^2 - 1) * (q - 1)) * q = (q^2 - 1) * (q * (q - 1))) ∧
    ((q - 1) * (q^2 - 1) = ((q^2 - 1) * (q - 1)) * 1) := by
  constructor
  · ring
  constructor <;> ring

/-- The four distance shells sum to q^3 vertices. -/
theorem cover_shell_total (q : ℤ) :
    1 + (q^2 - 1) + (q^2 - 1) * (q - 1) + (q - 1) = q^3 := by
  ring

/-- Symbolic intersection array recorded by L1--L4. -/
def coverIntersectionArray (q : ℤ) : (ℤ × ℤ × ℤ) × (ℤ × ℤ × ℤ) :=
  ((q^2 - 1, q * (q - 1), 1), (1, q, q^2 - 1))

end W33.Pass465
