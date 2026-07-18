import Mathlib

open Matrix

namespace W33.Pass441

/-- The integral two-by-two block left after central Fourier pairing. -/
def pairedBlock (q : ℤ) : Matrix (Fin 2) (Fin 2) ℤ :=
  !![q * (q + 1), 1; 0, q * (q - 1)]

/-- An explicit integral row-operation witness. It is its own inverse. -/
def leftWitness (q : ℤ) : Matrix (Fin 2) (Fin 2) ℤ :=
  !![1, 0; q * (q - 1), -1]

/-- An explicit integral column-operation witness. -/
def rightWitness (q : ℤ) : Matrix (Fin 2) (Fin 2) ℤ :=
  !![0, 1; 1, -(q * (q + 1))]

/-- The explicit inverse of `rightWitness`. -/
def rightInverse (q : ℤ) : Matrix (Fin 2) (Fin 2) ℤ :=
  !![q * (q + 1), 1; 1, 0]

/-- The claimed Smith diagonal of the paired block. -/
def smithDiagonal (q : ℤ) : Matrix (Fin 2) (Fin 2) ℤ :=
  !![1, 0; 0, q^2 * (q^2 - 1)]

theorem leftWitness_involutive (q : ℤ) :
    leftWitness q * leftWitness q = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, leftWitness] <;> ring

theorem rightWitness_rightInverse (q : ℤ) :
    rightWitness q * rightInverse q = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, rightWitness, rightInverse] <;> ring

theorem rightInverse_rightWitness (q : ℤ) :
    rightInverse q * rightWitness q = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, rightWitness, rightInverse] <;> ring

/-- Constructive integral equivalence of the paired block to its Smith diagonal. -/
theorem pairedBlock_reduction (q : ℤ) :
    leftWitness q * pairedBlock q * rightWitness q = smithDiagonal q := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, pairedBlock, leftWitness, rightWitness,
      smithDiagonal] <;> ring

/-- Polynomial factorization underlying the nontrivial Smith divisor. -/
theorem paired_divisor_factorization (q : ℤ) :
    (q * (q + 1)) * (q * (q - 1)) = q^2 * (q^2 - 1) := by
  ring

/-- The spectral multiplicity difference is the residual Smith multiplicity. -/
theorem spectral_residual_identity (q : ℤ) :
    q * (q^2 - 1) - q * (q - 1)^2 = 2 * q * (q - 1) := by
  ring

/-- At one conductor stratum, plus and minus multiplicity numerators exhaust the active block. -/
theorem conductor_sum_identity (characters t : ℤ) :
    characters * t * (t + 1) + characters * t * (t - 1) =
      2 * characters * t^2 := by
  ring

/-- At one conductor stratum, their difference is the residual rank. -/
theorem conductor_difference_identity (characters t : ℤ) :
    characters * t * (t + 1) - characters * t * (t - 1) =
      2 * characters * t := by
  ring

/-- The valuation bookkeeping identity behind low plus glued prime-primary layers. -/
theorem valuation_pairing_polynomial_identity
    (mMinus residual a b : ℤ) :
    (mMinus + residual) * a + mMinus * b =
      residual * a + mMinus * (a + b) := by
  ring

end W33.Pass441
