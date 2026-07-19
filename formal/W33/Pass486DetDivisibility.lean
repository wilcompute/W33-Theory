import Mathlib

namespace W33.Pass486

/-!
The two steps that make the unified determinant law unconditional off the
primes (Pass 485).

Every entry of the section difference `D` is a `ℤ[ζ_p]`-combination of the
`d_v`, each divisible by `λ`.  A determinant is a signed sum of products of
`n` entries, one from each row, so `λ ∣ every entry` gives `λ ^ n ∣ det`.
With `n = q` this yields `v_λ(det D) ≥ q`; and since `q = p ^ f` satisfies
`q ≥ v_λ(q) + 4 = f (p-1) + 4` for every `f ≥ 2`, the top-term hypothesis is
discharged at every prime power that is not prime.

To avoid truncated subtraction the arithmetic lemma is stated with `a = p - 1`.
-/

open Finset Matrix

variable {n : Type*} [Fintype n] [DecidableEq n]
variable {R : Type*} [CommRing R]

/-- If `lam` divides every entry of `M`, then `lam ^ card n` divides `det M`. -/
theorem pow_card_dvd_det (lam : R) (M : Matrix n n R)
    (h : ∀ i j, lam ∣ M i j) :
    lam ^ (Fintype.card n) ∣ M.det := by
  rw [Matrix.det_apply']
  refine Finset.dvd_sum fun σ _ => ?_
  refine Dvd.dvd.mul_left ?_ _
  have hall : ∀ i ∈ (Finset.univ : Finset n), lam ∣ M (σ i) i :=
    fun i _ => h _ _
  have : ∏ _i : n, lam ∣ ∏ i : n, M (σ i) i :=
    Finset.prod_dvd_prod_of_dvd _ _ hall
  simpa [Finset.prod_const, Finset.card_univ] using this

/-- `f * a + 4 ≤ (a+1) ^ f` for `a ≥ 2` and `f ≥ 2`.  With `a = p - 1` this is
`f (p-1) + 4 ≤ p ^ f`, the inequality behind "unconditional for `f ≥ 2`". -/
theorem mul_add_four_le_pow (a : ℕ) (ha : 2 ≤ a) :
    ∀ f : ℕ, 2 ≤ f → f * a + 4 ≤ (a + 1) ^ f := by
  intro f hf
  induction f, hf using Nat.le_induction with
  | base =>
      have : (a + 1) ^ 2 = a * a + 2 * a + 1 := by ring
      nlinarith
  | succ k hk ih =>
      have hpos : 1 ≤ (a + 1) ^ k := Nat.one_le_pow _ _ (by omega)
      have hstep : (a + 1) ^ (k + 1) = (a + 1) * (a + 1) ^ k := by ring
      nlinarith

end W33.Pass486
