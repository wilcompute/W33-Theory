import Mathlib

namespace W33.Pass515

/-!
The rank of the sieve system (Pass 515), formalized — with no arithmetic input.

The sieve theorem (Pass 514) gives one relation per `t ∈ T`:
`∑_{d ∣ t} d • S d = 0`.  Pass 515 observes that relation `t` involves exactly
the `S d` with `d ∣ t`, and that `S t` occurs in relation `t` and in no relation
indexed by a *proper* divisor of `t`.  Ordering the relations along any linear
extension of divisibility therefore presents the system as a triangular matrix
whose diagonal entries are the nonzero integers `t`, so its rank is the number
of relations and

    pinned(m) = |T|,   free(m) = τ(m) - |T| .

All of that except the triangularity is divisor bookkeeping.  The triangularity
step is what this file proves, and unlike the other modules of this arc it
assumes **no hypotheses about the Heisenberg group or about `ℤ[ζ_e]`** — it is a
statement about matrices over a field and stands entirely on its own.
-/

open Matrix

variable {n : ℕ} {K : Type*} [Field K]

/-- A lower-triangular matrix with nonzero diagonal has nonzero determinant. -/
theorem det_ne_zero_of_lowerTriangular
    (M : Matrix (Fin n) (Fin n) K)
    (htri : ∀ i j, i < j → M i j = 0)
    (hdiag : ∀ i, M i i ≠ 0) :
    M.det ≠ 0 := by
  rw [Matrix.det_of_lowerTriangular M htri]
  exact Finset.prod_ne_zero_iff.mpr fun i _ => hdiag i

/-- Hence such a matrix has full rank: the sieve system's rank is the number of
its relations.  (`Matrix.rank_eq_finrank_of_det_ne_zero` is spelled here via
invertibility, which is the form mathlib exposes.) -/
theorem isUnit_det_of_lowerTriangular
    (M : Matrix (Fin n) (Fin n) K)
    (htri : ∀ i j, i < j → M i j = 0)
    (hdiag : ∀ i, M i i ≠ 0) :
    IsUnit M.det :=
  (isUnit_iff_ne_zero).mpr (det_ne_zero_of_lowerTriangular M htri hdiag)

/-- The sieve system's square block, made concrete: `A t d = d` when `d ∣ t` and
`0` otherwise, restricted to the relation indices.  Written abstractly here as
"the diagonal entries are nonzero and everything strictly above vanishes", which
is exactly what divisibility supplies once the indices are listed in a linear
extension. -/
theorem sieve_block_isUnit
    (A : Matrix (Fin n) (Fin n) K)
    (hzero : ∀ i j, i < j → A i j = 0)
    (hne : ∀ i, A i i ≠ 0) :
    IsUnit A.det :=
  isUnit_det_of_lowerTriangular A hzero hne

/-!
### Scope

This is the whole of the rank argument that is not divisor counting.  The
remaining steps — that relation `t` involves exactly the `S d` with `d ∣ t`,
that the diagonal entry is `t ≠ 0`, and that
`|T| = #{u ∣ m : u odd, e ∣ u}` — are arithmetic identities about divisors,
checked exactly in `analysis/w33_pass515_sieve_rank.py` against the rank of the
actual matrix over `ℚ` for `e ∈ {3,5,7,9,25,27}` and `m ≤ 60`.

Note what is *not* claimed: nothing here says the sieve relations are the only
ones.  That the nullity of the measured system equals `|T|` is a separate,
purely empirical finding of Pass 516, scoped to linear relations with constant
rational coefficients over sampled sections.
-/

end W33.Pass515
