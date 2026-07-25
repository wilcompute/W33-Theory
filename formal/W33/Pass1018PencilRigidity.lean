/-
Pass 1018, formalised: the two pencil thresholds of `W(q,q)` never meet its
spectrum, for any integer `q ≥ 2`.

`W(q,q)` is strongly regular with

  n = (q+1)(q²+1),  k = q(q+1),  restricted eigenvalues  r = q-1,  s = -q-1.

Pass 1017's criterion says the gluing of `α A + β J + γ I` moves exactly when
`k + βn/α` lands on the spectrum.  The two members that matter are
complementation, with threshold `k - n`, and the Seidel matrix, with threshold
`k - n/2`.  Rigidity is then four non-collisions:

  k - n   ≠ r,   k - n   ≠ s,   k - n/2 ≠ r,   k - n/2 ≠ s.

The Seidel threshold is a half-integer in general, so we clear the denominator
once and work with `2k - n` against `2r` and `2s`; over `ℤ` that is an
equivalence, and it keeps every statement below in the integers.

Closed forms (`complThreshold_eq`, `twiceSeidelThreshold_eq`):

  k - n    = -(q³ + 1),
  2k - n   = -(q-1)²(q+1).
-/
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

namespace W33.Pass1018

variable {q : ℤ}

/-- Vertex count of `W(q,q)`. -/
def n (q : ℤ) : ℤ := (q + 1) * (q ^ 2 + 1)

/-- Valency of `W(q,q)`. -/
def k (q : ℤ) : ℤ := q * (q + 1)

/-- The positive restricted eigenvalue. -/
def r (q : ℤ) : ℤ := q - 1

/-- The negative restricted eigenvalue. -/
def s (q : ℤ) : ℤ := -q - 1

/-- Complementation threshold, `k - n`. -/
def complThreshold (q : ℤ) : ℤ := k q - n q

/-- Twice the Seidel threshold, `2k - n`.  Doubling clears the `n/2`. -/
def twiceSeidelThreshold (q : ℤ) : ℤ := 2 * k q - n q

lemma complThreshold_eq (q : ℤ) : complThreshold q = -(q ^ 3 + 1) := by
  unfold complThreshold n k; ring

lemma twiceSeidelThreshold_eq (q : ℤ) :
    twiceSeidelThreshold q = -((q - 1) ^ 2 * (q + 1)) := by
  unfold twiceSeidelThreshold n k; ring

/-- **Non-collision 1.**  `k - n = r` would force `q(q²+1) = 0`. -/
theorem compl_ne_r (hq : 2 ≤ q) : complThreshold q ≠ r q := by
  rw [complThreshold_eq]
  unfold r
  intro h
  nlinarith [sq_nonneg q, sq_nonneg (q - 1)]

/-- **Non-collision 2.**  `k - n = s` would force `q³ = q`. -/
theorem compl_ne_s (hq : 2 ≤ q) : complThreshold q ≠ s q := by
  rw [complThreshold_eq]
  unfold s
  intro h
  nlinarith [sq_nonneg q, sq_nonneg (q - 1)]

/-- **Non-collision 3.**  `2k - n = 2r` would force `(q-1)(q²+1) = 0`. -/
theorem seidel_ne_r (hq : 2 ≤ q) : twiceSeidelThreshold q ≠ 2 * r q := by
  rw [twiceSeidelThreshold_eq]
  unfold r
  intro h
  nlinarith [sq_nonneg q, sq_nonneg (q - 1)]

/-- **Non-collision 4.**  `2k - n = 2s` would force `(q-1)² = 2`. -/
theorem seidel_ne_s (hq : 2 ≤ q) : twiceSeidelThreshold q ≠ 2 * s q := by
  rw [twiceSeidelThreshold_eq]
  unfold s
  intro h
  rcases eq_or_lt_of_le hq with h2 | h3
  · rw [← h2] at h; norm_num at h
  · nlinarith [sq_nonneg (q - 1), sq_nonneg (q - 3)]

/-- **Pencil rigidity of `W(q,q)`.**  For every integer `q ≥ 2` neither the
complementation threshold nor the Seidel threshold is a restricted eigenvalue,
so by the Pass 1017 criterion the gluing is constant along both directions of
the pencil.  This is the formal content of Pass 1018. -/
theorem pencil_rigid (hq : 2 ≤ q) :
    complThreshold q ≠ r q ∧ complThreshold q ≠ s q ∧
    twiceSeidelThreshold q ≠ 2 * r q ∧ twiceSeidelThreshold q ≠ 2 * s q :=
  ⟨compl_ne_r hq, compl_ne_s hq, seidel_ne_r hq, seidel_ne_s hq⟩

/-- The `q = 3` specialisation, matching the numbers used in the paper and in
`data/w33_pass1018_pencil_rigidity_and_the_wqq_family.json`: the thresholds are
`-28` and `-8` against the spectrum `{12, 2, -4}`. -/
example : complThreshold 3 = -28 ∧ twiceSeidelThreshold 3 = -16 ∧
    n 3 = 40 ∧ k 3 = 12 ∧ r 3 = 2 ∧ s 3 = -4 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩ <;> decide

end W33.Pass1018
