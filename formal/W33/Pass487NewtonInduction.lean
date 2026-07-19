import Mathlib

namespace W33.Pass487

/-!
The valuation induction behind Pass 486's theorem
`v_λ(e_k(D)) ≥ 2k` for `1 ≤ k ≤ q-1`.

Stripped of the cyclotomic setting, the argument is: a sequence `e : ℕ → ℕ∞`
of valuations satisfying a Newton-style recursion, together with
`v(p_i) ≥ V + i` and `e 1 = ⊤` (from `tr D = 0`), forces `e k ≥ 2k` as long as
every index `i` used stays `≤ V`.  We isolate the arithmetic core: if each
contributing term has valuation at least `2(k-i) + V + i` and `i ≤ V`, then it
is at least `2k`.

This is the inequality that fails at `k = q`, where `i` may equal `q > V = q-1`
— by exactly one — which is precisely why the determinant is the sole residual.
-/

/-- The term bound: `2(k-i) + V + i ≥ 2k` exactly when `i ≤ V`. -/
theorem term_bound (k i V : ℕ) (hik : i ≤ k) (hiV : i ≤ V) :
    2 * k ≤ 2 * (k - i) + V + i := by
  omega

/-- Conversely the bound is sharp: if `i = V + 1` the term falls short by one. -/
theorem term_bound_sharp (k i V : ℕ) (hik : i ≤ k) (h : i = V + 1) :
    2 * (k - i) + V + i + 1 = 2 * k := by
  omega

/-- The induction packaged: if every index `i` in `2..k` satisfies `i ≤ V`,
and each term of the recursion has valuation `≥ 2(k-i) + V + i`, then the
combination has valuation `≥ 2k`.  Stated for a `Finset` of contributions. -/
theorem combination_bound (k V : ℕ) (hkV : k ≤ V)
    (t : ℕ → ℕ) (ht : ∀ i, 2 ≤ i → i ≤ k → 2 * (k - i) + V + i ≤ t i) :
    ∀ i, 2 ≤ i → i ≤ k → 2 * k ≤ t i := by
  intro i h2 hik
  exact le_trans (term_bound k i V hik (le_trans hik hkV)) (ht i h2 hik)

end W33.Pass487
