import W33.OddQRank
import Mathlib.Tactic

/-!
# Arithmetic block assembly for the odd-q Levi formulas

This module kernel-checks the polynomial identities obtained *after* the
trivial and nontrivial block ranks have been supplied by geometry.  It does
not define a finite-field Fourier transform, an incidence matrix, or a rank,
and therefore does not prove those geometric block ranks.

The earlier `TrivialBlock` and `NontrivialBlock` structures contained only
reflexive equalities, while the global theorems ignored their certificate
argument.  They have been removed so the formal surface states its actual
scope directly: divisibility, arithmetic assembly, and the q=3 numerals.
-/

namespace W33.FourierBlocks

/-- Oddness makes the proposed nontrivial point-block numerator divisible by
two.  This proves integrality, not that the quotient is a matrix rank. -/
theorem pointBlockIntegral (q : ℤ) (hq : Odd q) :
    2 ∣ q * (q - 1) := by
  rcases hq with ⟨k, rfl⟩
  refine ⟨(2*k + 1) * k, ?_⟩
  ring

/-- Oddness makes the proposed nontrivial incidence-block numerator
divisible by two. -/
theorem incidenceBlockIntegral (q : ℤ) (hq : Odd q) :
    2 ∣ q * (q + 1) := by
  rcases hq with ⟨k, rfl⟩
  refine ⟨(2*k + 1) * (k + 1), ?_⟩
  ring

/-- Arithmetic assembly identity for the proposed point-block dimensions. -/
theorem globalPointRankArithmetic (q : ℤ) :
    2 * (q^2 + 1) + (q - 1) * q * (q - 1) = q * (q^2 + 1) + 2 := by
  exact W33.OddQRank.point_block_assembly q

/-- Arithmetic assembly identity for the proposed incidence-block dimensions. -/
theorem globalIncidenceRankArithmetic (q : ℤ) :
    2 * (q^2 + q + 1) + (q - 1) * q * (q + 1) = q * (q + 1)^2 + 2 := by
  exact W33.OddQRank.incidence_block_assembly q

/-- Arithmetic assembly identity for the proposed line-block dimensions. -/
theorem globalLineRankArithmetic (q : ℤ) :
    (q + 1) + (q - 1) * q = q^2 + 1 := by
  exact W33.OddQRank.line_block_assembly q

/-- Collect the arithmetic identities used by the Jordan calculation. -/
theorem arithmeticClosure (q : ℤ) : W33.OddQRank.ArithmeticCertificate q :=
  W33.OddQRank.arithmeticCertificate q

/-- Numerical evaluation of the three proposed formulas at q=3. -/
theorem q3ArithmeticValues :
    ((3 * (3 + 1)^2 + 2) / 2 : ℤ) = 25 ∧
    ((3 * (3^2 + 1) + 2) / 2 : ℤ) = 16 ∧
    (3^2 + 1 : ℤ) = 10 := by
  norm_num

/-- Numerical evaluation of the proposed q=3 Jordan multiplicities. -/
theorem q3JordanArithmetic :
    ((3^3 + 2*3^2 + 3 - 4) / 2 : ℤ) = 22 ∧
    (3 * (3 - 1)^2 / 2 : ℤ) = 6 ∧
    2*4 + 22*3 + 6 = 80 := by
  norm_num

end W33.FourierBlocks
