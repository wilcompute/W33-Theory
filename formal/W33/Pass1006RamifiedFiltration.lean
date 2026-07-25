import Mathlib

namespace W33.Pass1006

/-!
# The ramified gluing filtration, combinatorial core

Pass 1002 recovers the ramified `p`-primary gluing of a projector-congruence
stack `S` from the growth of `ker (S mod p^j)`.  Writing `a₁,…,a_r` for the
`p`-adic valuations of the Smith invariants of `S`, and `ν = v_p(M)` for the
conductor exponent, the chain is

* `κ j = log_p |ker (S mod p^j)| = ∑ i, min aᵢ j`,
* `Δ j = κ j - κ (j-1) = #{i | aᵢ ≥ j}`,
* the multiplicity of `ℤ/p^e` in the gluing is `#{i | aᵢ = ν - e}`,
* which equals `Δ (ν-e) - Δ (ν-e+1)`.

Only the first step mentions `p`, and there only as the residue characteristic,
via `ker (p^a : ℤ/p^j) ≅ ℤ/p^(min a j)`.  Steps two and four are pure counting on
a multiset of naturals and hold for every prime.  That is why the theorem —
certified at `p = 2` in Pass 1002, and verified at odd ramified primes up to
`ν = 6` in Passes 1005/1006 — is uniform in `p`.

This file formalizes those two counting steps.  Tail predicates are written as
`j < x` rather than `j + 1 ≤ x`, which is the form `simp` normalizes to, so that
the induction hypothesis and the goal share syntactically equal atoms.
-/

open Multiset

/-- `κ`, the total kernel exponent at level `j`: `∑ᵢ min aᵢ j`. -/
def kappa (a : Multiset ℕ) (j : ℕ) : ℕ := (a.map (fun x => min x j)).sum

/-- **Step two.** One level of kernel growth counts exactly the Smith invariants
of valuation greater than `j`:  `κ (j+1) = κ j + #{i | aᵢ > j}`. -/
theorem kappa_succ (a : Multiset ℕ) (j : ℕ) :
    kappa a (j + 1) = kappa a j + a.countP (fun x => j < x) := by
  classical
  induction a using Multiset.induction with
  | empty => simp [kappa]
  | cons x s ih =>
      simp only [kappa, Multiset.map_cons, Multiset.sum_cons,
        Multiset.countP_cons] at *
      by_cases h : j < x
      · rw [min_eq_right h, min_eq_right (Nat.le_of_lt_succ (Nat.lt_succ_of_lt h))]
        simp only [h, if_true, decide_true]
        omega
      · have hx : x ≤ j := by omega
        rw [min_eq_left (Nat.le_succ_of_le hx), min_eq_left hx]
        simp only [h, if_false, decide_false]
        omega

/-- The subtractive form used downstream: `Δ (j+1) = #{i | aᵢ > j}`. -/
theorem delta_eq (a : Multiset ℕ) (j : ℕ) :
    kappa a (j + 1) - kappa a j = a.countP (fun x => j < x) := by
  rw [kappa_succ]; omega

/-- **Step four.** Tail counts telescope: `#{i | aᵢ ≥ k} = #{i | aᵢ = k} + #{i | aᵢ > k}`.
This is what converts kernel-growth increments into gluing multiplicities. -/
theorem countP_eq_add (a : Multiset ℕ) (k : ℕ) :
    a.countP (fun x => k ≤ x)
      = a.countP (fun x => x = k) + a.countP (fun x => k < x) := by
  classical
  induction a using Multiset.induction with
  | empty => simp
  | cons x s ih =>
      simp only [Multiset.countP_cons] at *
      by_cases h : x = k
      · subst h
        simp only [le_refl, if_true, decide_true, lt_irrefl, if_false,
          decide_false]
        omega
      · by_cases h2 : k ≤ x
        · have h3 : k < x := lt_of_le_of_ne h2 (Ne.symm h)
          simp only [h, h2, h3, if_true, if_false, decide_true, decide_false]
          omega
        · have h3 : ¬ k < x := by omega
          simp only [h, h2, h3, if_false, decide_false]
          omega

/-- The multiplicity form: `#{i | aᵢ = k} = #{i | aᵢ ≥ k} - #{i | aᵢ > k}`. -/
theorem countP_exact (a : Multiset ℕ) (k : ℕ) :
    a.countP (fun x => x = k)
      = a.countP (fun x => k ≤ x) - a.countP (fun x => k < x) := by
  rw [countP_eq_add a k]; omega

/-!
## Step one: where the prime actually enters

The remaining link is `ker (p^a : ZMod (p^j)) ≅ ZMod (p^(min a j))`, which is the
only place the residue characteristic is used.  Its arithmetic core is the
statement that gcd on prime powers is `min` on exponents: the kernel of
multiplication by `c` on `ZMod n` has cardinality `gcd c n`, and specialising
`c = p^a`, `n = p^j` gives `p^(min a j)` — exactly the summand appearing in
`kappa j = ∑ᵢ min aᵢ j`.

That exponent arithmetic is proved below.  Note it holds for every `p`, prime or
not: primality is not what makes the filtration work, only the fact that the
modulus is a power of a single element.
-/

/-- **Step one, arithmetic core.** `gcd (p^a) (p^j) = p ^ min a j`.  Combined with
`|ker (c · _ : ZMod n)| = gcd c n`, this is the `p^(min aᵢ j)` factor whose
logarithm is the summand of `κ`. -/
theorem gcd_pow_pow (p a j : ℕ) : Nat.gcd (p ^ a) (p ^ j) = p ^ min a j := by
  rcases Nat.le_total a j with h | h
  · rw [min_eq_left h, Nat.gcd_eq_left (pow_dvd_pow p h)]
  · rw [min_eq_right h, Nat.gcd_eq_right (pow_dvd_pow p h)]

/-- The `κ` summand in closed form: the kernel exponent contributed by a Smith
invariant of valuation `a` at level `j` is `min a j`, for every `p`. -/
theorem kernel_exponent (p a j : ℕ) (hp : 1 < p) :
    Nat.log p (Nat.gcd (p ^ a) (p ^ j)) = min a j := by
  rw [gcd_pow_pow, Nat.log_pow hp]

end W33.Pass1006
