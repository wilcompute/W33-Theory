import Mathlib.Tactic

/-!
# Arithmetic identities behind the proposed odd-q binary Levi ranks

This file formalizes only the arithmetic closure used after a geometric
central-translation block calculation: polynomial identities, parity of the
half-integral expressions for odd `q`, and consistency of the proposed Jordan
multiplicities.  No incidence matrix, finite field, Fourier decomposition, or
matrix rank is defined here, so the geometric rank theorem remains an external
input rather than a Lean theorem in this module.
-/

namespace W33.OddQRank

/-- Polynomial identity corresponding to the proposed point-block assembly. -/
theorem point_block_assembly (q : ℤ) :
    2 * (q^2 + 1) + (q - 1) * q * (q - 1) = q * (q^2 + 1) + 2 := by
  ring

/-- Polynomial identity corresponding to the proposed incidence-block assembly. -/
theorem incidence_block_assembly (q : ℤ) :
    2 * (q^2 + q + 1) + (q - 1) * q * (q + 1) =
      q * (q + 1)^2 + 2 := by
  ring

/-- Polynomial identity corresponding to the proposed line-block assembly. -/
theorem line_block_assembly (q : ℤ) :
    (q + 1) + (q - 1) * q = q^2 + 1 := by
  ring

/-- The numerator of the `J₃` multiplicity is even for odd `q`. -/
theorem j3_numerator_even (q : ℤ) (hq : Odd q) :
    Even (q^3 + 2*q^2 + q - 4) := by
  rcases hq with ⟨k, hk⟩
  rw [hk]
  refine ⟨4*k^3 + 10*k^2 + 8*k, ?_⟩
  ring

/-- The numerator of the `J₁` multiplicity is even for odd `q`. -/
theorem j1_numerator_even (q : ℤ) (hq : Odd q) :
    Even (q * (q - 1)^2) := by
  rcases hq with ⟨k, hk⟩
  rw [hk]
  refine ⟨4*k^3 + 2*k^2, ?_⟩
  ring

/-- The incidence-rank numerator is even for odd `q`. -/
theorem incidence_numerator_even (q : ℤ) (hq : Odd q) :
    Even (q * (q + 1)^2 + 2) := by
  rcases hq with ⟨k, hk⟩
  rw [hk]
  refine ⟨4*k^3 + 10*k^2 + 8*k + 3, ?_⟩
  ring

/-- The point-rank numerator is even for odd `q`. -/
theorem point_numerator_even (q : ℤ) (hq : Odd q) :
    Even (q * (q^2 + 1) + 2) := by
  rcases hq with ⟨k, hk⟩
  rw [hk]
  refine ⟨4*k^3 + 6*k^2 + 4*k + 2, ?_⟩
  ring

/-- With `b₄=2`, `b₃=(q³+2q²+q-4)/2`, and `b₂=0`, the rank of the
nilpotent operator is the proved incidence-rank formula. The identity is
written without division. -/
theorem jordan_rank_one_assembly (q : ℤ) :
    (q^3 + 2*q^2 + q - 4) + 3*2 = q * (q + 1)^2 + 2 := by
  ring

/-- The rank of the square agrees with `b₃+2b₄`; again the equality is
cleared of denominators. -/
theorem jordan_rank_two_assembly (q : ℤ) :
    (q^3 + 2*q^2 + q - 4) + 2*(2*2) =
      q * (q^2 + 1) + 2*q^2 + 4 := by
  ring

/-- The total dimension is recovered from `b₁+3b₃+4b₄`, with all halves
cleared. -/
theorem jordan_dimension_assembly (q : ℤ) :
    q * (q - 1)^2 + 3*(q^3 + 2*q^2 + q - 4) + 2*(4*2) =
      4 * (q + 1) * (q^2 + 1) := by
  ring

/-- A compact proposition collecting exactly the arithmetic consequences used
by the odd-prime-power Jordan theorem. -/
structure ArithmeticCertificate (q : ℤ) : Prop where
  pointRank : 2 * (q^2 + 1) + (q - 1) * q * (q - 1) = q * (q^2 + 1) + 2
  incidenceRank : 2 * (q^2 + q + 1) + (q - 1) * q * (q + 1) = q * (q + 1)^2 + 2
  lineRank : (q + 1) + (q - 1) * q = q^2 + 1
  rankOne : (q^3 + 2*q^2 + q - 4) + 3*2 = q * (q + 1)^2 + 2
  rankTwo : (q^3 + 2*q^2 + q - 4) + 2*(2*2) = q * (q^2 + 1) + 2*q^2 + 4
  dimension : q * (q - 1)^2 + 3*(q^3 + 2*q^2 + q - 4) + 2*(4*2) =
    4 * (q + 1) * (q^2 + 1)

/-- The arithmetic certificate is constructible for every integer `q`; oddness
is needed only to interpret the cleared numerators as integral multiplicities. -/
theorem arithmeticCertificate (q : ℤ) : ArithmeticCertificate q where
  pointRank := point_block_assembly q
  incidenceRank := incidence_block_assembly q
  lineRank := line_block_assembly q
  rankOne := jordan_rank_one_assembly q
  rankTwo := jordan_rank_two_assembly q
  dimension := jordan_dimension_assembly q

end W33.OddQRank
