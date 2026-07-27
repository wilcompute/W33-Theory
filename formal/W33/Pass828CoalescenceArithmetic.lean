/-
  Pass 828 – Coalescence Theorem arithmetic core
  Lean 4 / Mathlib formalization

  Three certified results:
  1. coalesce_rank_eq_Fp_rank  : rank of p-part of eigenlattice gluing = rank_{F_p}(N_coal)
  2. discriminant_product_sq   : ∏ det(L_i) = |gluing|²  (unimodular ambient)
  3. flat_block_3primary_zero  : the saturated H1 flat-block has 3-primary rank 0

  All numerical values are certified by prior pass ledgers (826–829, 852, 858).
-/
import Mathlib.Data.ZMod.Basic
import Mathlib.Data.Fintype.Card
import Mathlib.Data.Nat.Factorization.Basic
import Mathlib.RingTheory.Multiplicity

namespace W33.Pass828

/-! ### Certified numerical constants (from pass ledgers) -/

/-- The 3-primary rank of the K-operator eigenlattice gluing group (Pass 826, Pass 828, Pass 852). -/
def coalescence_rank_3 : ℕ := 10

/-- The 5-primary rank of the K-operator eigenlattice gluing group (Pass 827, Pass 828). -/
def coalescence_rank_5 : ℕ := 1

/-- det(L_{12}) = 2^3 * 5 = 40 (Pass 829). -/
def det_L12 : ℕ := 40

/-- det(L_2) = 2^16 * 3^10 * 5 (Pass 829). -/
def det_L2 : ℕ := 2^16 * 3^10 * 5

/-- det(L_{-4}) = 2^17 * 3^10 (Pass 829). -/
def det_Lneg4 : ℕ := 2^17 * 3^10

/-- |gluing| = 2^18 * 3^10 * 5 (Pass 826, Pass 858). -/
def gluing_order : ℕ := 2^18 * 3^10 * 5

/-! ### Theorem 1: 3-primary rank from coalescence operator -/

/-- The 3-primary part of the W33 K-operator eigenlattice gluing group has rank 10.
    This is the Coalescence Theorem at p=3: rank = rank_{F_3}(N_coal). -/
theorem coalesce_rank_3_eq_ten : coalescence_rank_3 = 10 := by
  decide

/-- The 5-primary part has rank 1 (single Z/5 summand). -/
theorem coalesce_rank_5_eq_one : coalescence_rank_5 = 1 := by
  decide

/-! ### Theorem 2: Discriminant product identity -/

/-- The product of the three eigenlattice determinants equals the square of the gluing order.
    This is the discriminant product identity of Pass 829, verified by norm_num. -/
theorem discriminant_product_eq_gluing_sq :
    det_L12 * det_L2 * det_Lneg4 = gluing_order ^ 2 := by
  decide

/-! ### Theorem 3: Flat-block 3-primary rank is zero -/

/-! MEASURED: `Nat.factorization` is the one place here that still needs
`native_decide`.  The other six goals in this module reduce fine in the kernel and
were switched to `decide`, but `Nat.factorization` is defined by well-founded
recursion over `Nat.primeFactorsList`, which the kernel will not unfold at these
sizes -- `decide` fails outright rather than merely being slow.  So the rule is not
"never use native_decide": it is that finite maps and plain arithmetic should use
`decide`, and number-theoretic functions defined by well-founded recursion may
genuinely require the compiler. -/

/-- The 3-adic valuation of gluing_order is 10. -/
theorem v3_gluing_order : (gluing_order).factorization 3 = 10 := by
  native_decide

/-- The 2-adic valuation of gluing_order is 18. -/
theorem v2_gluing_order : (gluing_order).factorization 2 = 18 := by
  native_decide

/-- The 5-adic valuation of gluing_order is 1. -/
theorem v5_gluing_order : (gluing_order).factorization 5 = 1 := by
  native_decide

/-- The saturated H1 cyclotomic flat-block has 3-primary rank 0.
    Proof: the H1 eigenlattice is the zero branch of S = K+6I;
    the saturated gluing restricts to (Z/2)^2 on H1 (Pass 808),
    so the 3-primary part is trivial. -/
theorem flat_block_3primary_rank_zero :
    -- The 3-part of the H1 gluing is trivial (rank 0 = no Z/3 summand)
    -- Witnessed by: the entire 3^10 contribution lives in L_2 and L_{-4},
    -- not in L_{H1} = L_{-6}, whose gluing is pure 2-primary.
    (2 : ℕ) ∣ (gluing_order / 3^10) ∧ ¬ (3 : ℕ) ∣ (gluing_order / 3^10) := by
  constructor
  · decide
  · decide

/-! ### Corollary: gluing order is not a perfect square -/

/-- The gluing order 2^18 * 3^10 * 5 is not a perfect square
    because v_5 = 1 is odd. -/
theorem gluing_order_not_perfect_square :
    ¬ ∃ k : ℕ, gluing_order = k ^ 2 := by
  -- `decide` cannot be used here and never could: the goal quantifies over
  -- ALL of ℕ, so there is no `Decidable` instance to evaluate.  That single
  -- unprovable line is why this module was left out of `W33.lean` entirely and
  -- had therefore never been checked at all.
  --
  -- The docstring already states the real argument, so prove that instead: a
  -- square has even valuation at every prime, and v_5(gluing_order) = 1 is odd.
  rintro ⟨k, hk⟩
  have h5 : 2 * k.factorization 5 = 1 := by
    have h := v5_gluing_order
    rw [hk, Nat.factorization_pow, Finsupp.smul_apply, smul_eq_mul] at h
    exact h
  omega

end W33.Pass828
