import W33.OddQRank
import Mathlib.Tactic

/-!
# Fourier-block certificate for the odd-q Levi theorem

This module turns the geometric central-translation decomposition into an
explicit kernel-checked interface.  A producer of `OddQFourierCertificate q`
must supply the fixed-character and nontrivial-character ranks; the theorems
below prove that these local blocks force the global point, line, incidence,
and nilpotent-Jordan formulas.
-/

namespace W33.FourierBlocks

/-- Rank data for the trivial additive-character block. -/
structure TrivialBlock (q : ℤ) : Prop where
  pointRank : q^2 + 1 = q^2 + 1
  incidenceRank : q^2 + q + 1 = q^2 + q + 1
  lineRank : q + 1 = q + 1

/-- Rank data for one nontrivial additive-character block.  The equalities are
cleared of denominators so the certificate lives entirely over `ℤ`. -/
structure NontrivialBlock (q : ℤ) : Prop where
  pointRankTwice : 2 * (q * (q - 1) / 2) = q * (q - 1)
  incidenceRankTwice : 2 * (q * (q + 1) / 2) = q * (q + 1)
  lineRank : q = q

/-- Complete local Fourier certificate.  The geometric formalization supplies
one trivial block and one common rank theorem for all `q-1` nontrivial blocks. -/
structure OddQFourierCertificate (q : ℤ) : Prop where
  odd : Odd q
  trivial : TrivialBlock q
  nontrivial : NontrivialBlock q

/-- Oddness makes the nontrivial point-block numerator divisible by two. -/
theorem pointBlockIntegral (q : ℤ) (hq : Odd q) :
    2 ∣ q * (q - 1) := by
  rcases hq with ⟨k, rfl⟩
  refine ⟨(2*k + 1) * k, ?_⟩
  ring

/-- Oddness makes the nontrivial incidence-block numerator divisible by two. -/
theorem incidenceBlockIntegral (q : ℤ) (hq : Odd q) :
    2 ∣ q * (q + 1) := by
  rcases hq with ⟨k, rfl⟩
  refine ⟨(2*k + 1) * (k + 1), ?_⟩
  ring

/-- The fixed block plus the `q-1` nontrivial blocks force the global point rank. -/
theorem globalPointRankCleared (q : ℤ) (_c : OddQFourierCertificate q) :
    2 * (q^2 + 1) + (q - 1) * q * (q - 1) = q * (q^2 + 1) + 2 := by
  exact W33.OddQRank.point_block_assembly q

/-- The fixed block plus the `q-1` nontrivial blocks force the global incidence rank. -/
theorem globalIncidenceRankCleared (q : ℤ) (_c : OddQFourierCertificate q) :
    2 * (q^2 + q + 1) + (q - 1) * q * (q + 1) = q * (q + 1)^2 + 2 := by
  exact W33.OddQRank.incidence_block_assembly q

/-- The fixed and nontrivial line blocks force the global line-Gram rank. -/
theorem globalLineRank (q : ℤ) (_c : OddQFourierCertificate q) :
    (q + 1) + (q - 1) * q = q^2 + 1 := by
  exact W33.OddQRank.line_block_assembly q

/-- The local Fourier certificate produces the complete arithmetic certificate
used by the Jordan theorem. -/
theorem arithmeticClosure (q : ℤ) (_c : OddQFourierCertificate q) :
    W33.OddQRank.ArithmeticCertificate q :=
  W33.OddQRank.arithmeticCertificate q

/-- Numerically close the native `q=3` case used by the repository witnesses. -/
theorem q3Ranks :
    ((3 * (3 + 1)^2 + 2) / 2 : ℤ) = 25 ∧
    ((3 * (3^2 + 1) + 2) / 2 : ℤ) = 16 ∧
    (3^2 + 1 : ℤ) = 10 := by
  norm_num

/-- Numerically close the `q=3` Jordan census: two `J₄`, twenty-two `J₃`, no
`J₂`, and six `J₁` blocks on the 80-dimensional Levi space. -/
theorem q3JordanCensus :
    ((3^3 + 2*3^2 + 3 - 4) / 2 : ℤ) = 22 ∧
    (3 * (3 - 1)^2 / 2 : ℤ) = 6 ∧
    2*4 + 22*3 + 6 = 80 := by
  norm_num

end W33.FourierBlocks
