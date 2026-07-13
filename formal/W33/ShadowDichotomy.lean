import Mathlib.Tactic

/-!
# The odd-`q` shadow formulas (arithmetic layer)

This file formalizes only the arithmetic formulas suggested by the
odd-`q` `W(3,q)` calculations.  It does not define `W(3,q)`, a permutation
module, a filtration, or a quadratic form.  The polynomial layer dimensions
reconstruct `v = (q+1)(q²+1)`, and the coefficient-parity predicate defined
below is equivalent to `q ≡ 3 (mod 4)`.  The geometric/module interpretation
is a separate GAP-certified statement at `q = 3,5,7`.

Arithmetic companion to
`analysis/w33_pass202_shadow_dichotomy_arithmetic.py` and structurally
proof scripts are written with `ring`, `omega`, and `decide`; a real
`lake build` is still required before calling them kernel-checked.
-/

namespace W33.ShadowDichotomy

/-- Twice the two-generation code-layer dimension `2·d(q)`, kept as a
polynomial to avoid integer division. -/
def twoLayerD (q : ℤ) : ℤ := (q - 1) * (q ^ 2 + q + 2)

/-- The central quadratic-shadow dimension `q² - 1`. -/
def shadowDim (q : ℤ) : ℤ := q ^ 2 - 1

/-- Twice the Sastry–Sin binary incidence rank `2·rank₂ M`. -/
def twoIncidenceRank (q : ℤ) : ℤ := q * (q + 1) ^ 2 + 2

/-- The seven uniserial layers `1, d, 1, q²-1, 1, d, 1` sum to the point
count `v = (q+1)(q²+1)`.  Stated with the doubled code layer, so the whole
identity is a polynomial identity over `ℤ`:
`4 + 2·d(q) + (q²-1) = (q+1)(q²+1)`. -/
theorem layer_sum_eq_v (q : ℤ) :
    (4 : ℤ) + twoLayerD q + shadowDim q = (q + 1) * (q ^ 2 + 1) := by
  simp only [twoLayerD, shadowDim]
  ring

/-- The doubled incidence rank unfolds to `q(q+1)² + 2` (Sastry–Sin). -/
theorem two_incidence_rank_def (q : ℤ) :
    twoIncidenceRank q = q * (q + 1) ^ 2 + 2 := rfl

/-- The coefficient-parity condition predicted to govern nondegeneracy.
This definition itself contains no quadratic space. -/
def nondegenerate (q : ℕ) : Prop :=
  (q ^ 2 - 1) / 2 % 2 = 0 ∧ (q + 1) / 2 % 2 = 0

/-- For odd `q ≥ 3`, the coefficient-parity predicate is equivalent to
`q ≡ 3 (mod 4)`.  (The first conjunct is automatic; the arithmetic
dichotomy is carried by the second.) -/
theorem nondegenerate_iff (q : ℕ) (hq : q % 2 = 1) (h3 : 3 ≤ q) :
    nondegenerate q ↔ q % 4 = 3 := by
  obtain ⟨k, rfl⟩ : ∃ k, q = 2 * k + 3 := ⟨(q - 3) / 2, by omega⟩
  unfold nondegenerate
  have hsq : (2 * k + 3) ^ 2 = 4 * k ^ 2 + 12 * k + 9 := by ring
  rw [hsq]
  omega

/-- Values of the dimension polynomial at three residue-class examples;
this does not construct the corresponding modules. -/
example : shadowDim 3 = 8 ∧ shadowDim 7 = 48 ∧ shadowDim 11 = 120 := by
  refine ⟨?_, ?_, ?_⟩ <;> decide

end W33.ShadowDichotomy
