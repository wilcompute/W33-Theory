import Mathlib.Tactic

/-!
# The even-`q` incidence rank law (arithmetic layer)

This file formalizes the ARITHMETIC of the even-`q` rank law established
computationally in Passes 256/261/265/270/275.  It does not define `W(3,q)`, an
incidence matrix, or an `F₂` rank: the geometric content is a separate,
machine-verified statement (see `analysis/w33_pass256_even_q_closed_form.py` and
`data/w33_pass256_even_q_closed_form.json`).  What IS formalized here is the
closed-form recurrence and the Cayley–Hamilton fact that forces its
inhomogeneous term.

The geometric statement, for context: `rank₂ W(3,2^t) = Tr(Bᵗ) + 1` with
`B = !![4,2; 2,5]`, whose characteristic polynomial is `X² - 9X + 16`.

Proof scripts use `decide`/`norm_num`/`omega`; a real `lake build` is still
required before calling any of this kernel-checked.
-/

namespace W33.RankLaw

/-- The even-`q` rank sequence, indexed by the Frobenius degree `t`.
`a 1 = 10` (the doily), `a 2 = 50`, and thereafter the inhomogeneous
Sastry–Sin recurrence `a (t+1) = 9 * a t - 16 * a (t-1) + 8`. -/
def a : ℕ → ℤ
  | 0 => 2      -- Tr(B⁰) + 1 = 2 + 1 - 1; unused, fixes the recursion
  | 1 => 10
  | 2 => 50
  | (n + 3) => 9 * a (n + 2) - 16 * a (n + 1) + 8

/-- The committed anchors: `q = 2, 4, 8, 16, 32`. -/
theorem a_one : a 1 = 10 := by rfl
theorem a_two : a 2 = 50 := by rfl
theorem a_three : a 3 = 298 := by decide
theorem a_four : a 4 = 1890 := by decide
theorem a_five : a 5 = 12250 := by decide

/-- The trace of `Bᵗ` is the rank minus the trivial (all-ones) module `⟨j⟩`
(Pass 270).  Here it is the shifted sequence. -/
def tr (t : ℕ) : ℤ := a t - 1

theorem tr_one : tr 1 = 9 := by rfl
theorem tr_two : tr 2 = 49 := by rfl
theorem tr_three : tr 3 = 297 := by decide

/-- **The key lemma (Pass 261).**  For any `2×2` matrix with trace `p` and
determinant `q`, Cayley–Hamilton gives `Tr(Bᵗ⁺¹) = p·Tr(Bᵗ) - q·Tr(Bᵗ⁻¹)`.  If a
sequence is `Tr(Bᵗ) + c`, then it satisfies the recurrence with the
INHOMOGENEOUS constant `c * (1 - p + q)`.  In particular the recurrence is
homogeneous iff `c = 0`. -/
theorem shifted_recurrence (p q c T Tm : ℤ) :
    (p * T - q * Tm) + c = p * (T + c) - q * (Tm + c) + c * (1 - p + q) := by
  ring

/-- **The `+8` is forced.**  With `c = 1` (the trivial module `⟨j⟩` lies in the
incidence code, Pass 270), `Tr B = 9` and `det B = 16`, the inhomogeneous
constant is exactly `8`.  This is why Pass 250's homogeneous test could never
have succeeded. -/
theorem constant_is_eight : (1 : ℤ) * (1 - 9 + 16) = 8 := by norm_num

/-- The characteristic polynomial's coefficients are doily data (Pass 275):
`Tr B = rank₂ W(3,2) - 1 = 9`. -/
theorem trace_from_doily_rank : (10 : ℤ) - 1 = 9 := by norm_num

/-- `det B = 16` is forced by the first two ranks: `Tr(B²) = Tr(B)² - 2·det B`
gives `det B = (81 - 49)/2 = 16` (Pass 265). -/
theorem det_forced : (9 ^ 2 - 49 : ℤ) / 2 = 16 := by norm_num

/-- The discriminant of `X² - 9X + 16` is `17` — the quadratic irrationality of
the even tower (Pass 256). -/
theorem discriminant_seventeen : (9 ^ 2 - 4 * 16 : ℤ) = 17 := by norm_num

end W33.RankLaw
