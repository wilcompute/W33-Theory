import Mathlib

namespace W33.Pass12667

/-!
Pass 12667 (attractor flows of the E6(6) cubic in the three-qubit Pauli realisation).

In a diagonal frame a charge with positive cubic invariant has quaternionic spectrum
`(a+b+c, a-b-c, b-a-c, c-a-b)` with `a ≥ b ≥ c > 0` and cubic `N = a*b*c`.  The attractor endpoint
has spectrum `g*(3,-1,-1,-1)` with `g^3 = a*b*c`.  Majorisation of the endpoint by the start reduces to
three inequalities on the leading partial sums:

* `a + b + c ≥ 3 g`  (AM-GM),
* `2 a ≥ 2 g`        (the largest entry is at least the geometric mean),
* `a + b - c ≥ g`    (since `b ≥ c`).

The other track proved the stronger statement along the whole flow (commit 8e73be5b5); this file
formalises only the endpoint inequalities.
-/

/-- The largest of three positive reals is at least their geometric mean `g` (`g^3 = a*b*c`). -/
theorem max_ge_geomean {a b c g : ℝ} (hab : b ≤ a) (hbc : c ≤ b) (hc : 0 < c) (hg : 0 < g)
    (hprod : g ^ 3 = a * b * c) : g ≤ a := by
  by_contra h
  push_neg at h
  have hb : 0 < b := lt_of_lt_of_le hc hbc
  have ha : 0 < a := lt_of_lt_of_le hb hab
  have h1 : a * b * c ≤ a * a * a := by
    have : b * c ≤ a * a := by nlinarith
    nlinarith
  have h2 : a * a * a < g * g * g := by
    have hag : a * a < g * g := by nlinarith
    nlinarith
  nlinarith [h1, h2, hprod]

/-- AM-GM for three positive reals in the form needed: `a + b + c ≥ 3 g` when `g^3 = a*b*c`. -/
theorem sum_ge_three_geomean {a b c g : ℝ} (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) (hg : 0 < g)
    (hprod : g ^ 3 = a * b * c) : 3 * g ≤ a + b + c := by
  -- Schur-free route: (a+b+c)^3 ≥ 27 abc, then take cube roots via monotonicity of t ↦ t^3.
  have hcube : 27 * (a * b * c) ≤ (a + b + c) ^ 3 := by
    nlinarith [sq_nonneg (a - b), sq_nonneg (b - c), sq_nonneg (a - c), mul_pos ha hb, mul_pos hb hc,
      mul_pos ha hc, sq_nonneg (a + b - 2 * c), sq_nonneg (a + c - 2 * b), sq_nonneg (b + c - 2 * a)]
  have hs : 0 < a + b + c := by linarith
  by_contra h
  push_neg at h
  have : (a + b + c) ^ 3 < (3 * g) ^ 3 := by
    exact pow_lt_pow_left₀ h hs.le (by norm_num)
  nlinarith [this, hcube, hprod]

/-- The three leading partial-sum inequalities of the majorisation. -/
theorem attractor_majorisation {a b c g : ℝ} (hab : b ≤ a) (hbc : c ≤ b) (hc : 0 < c) (hg : 0 < g)
    (hprod : g ^ 3 = a * b * c) :
    3 * g ≤ a + b + c ∧ 2 * g ≤ 2 * a ∧ g ≤ a + b - c := by
  have hb : 0 < b := lt_of_lt_of_le hc hbc
  have ha : 0 < a := lt_of_lt_of_le hb hab
  have hmax := max_ge_geomean hab hbc hc hg hprod
  refine ⟨sum_ge_three_geomean ha hb hc hg hprod, by linarith, by linarith⟩

end W33.Pass12667
