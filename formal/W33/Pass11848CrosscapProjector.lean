import Mathlib

namespace W33.Pass11848

/-!
Pass 11848: two algebraic facts behind the crosscap holography of Passes 11839 and 11847.

* **Crosscap symmetry.** A time reversal `T = U K` (`U` unitary, `K` complex conjugation) has `T² = U * conj U`.  Its
  crosscap form `B(ψ, φ) = ⟨T ψ, φ⟩ = ψᵀ Uᴴ φ` has matrix `Uᴴ`.  If `T² = ε` then `(Uᴴ)ᵀ = ε • Uᴴ`: the form is symmetric
  for `ε = 1` (Rac, bosonic) and antisymmetric for `ε = -1` (Di, Kramers).
* **The bulk propagator is a projector.**  For the orthogonality graph `A` of the 36 Kramers reversals, an
  `SRG(36, 15, 6, 6)` (so `A² = 9 + 6 J`, `A J = J A = 15 J`, `J² = 36 J`), the crosscap two-point matrix
  `G = 6 + 2 A - J` satisfies `G² = 12 G`: `G / 12` is the projector onto the bulk `15`.
-/

open Matrix

/-- Crosscap symmetry: `T² = ε` forces `Bᵀ = ε B` for the crosscap matrix `B = Uᴴ`. -/
theorem crosscap_symm {n : Type*} [Fintype n] [DecidableEq n] (U : Matrix n n ℂ) (ε : ℂ)
    (hU : U * Uᴴ = 1) (hT : U * U.map star = ε • (1 : Matrix n n ℂ)) :
    (Uᴴ)ᵀ = ε • Uᴴ := by
  have h1 : Uᴴ * U = 1 := mul_eq_one_comm.mp hU
  have hbar : U.map star = ε • Uᴴ := by
    calc U.map star = (Uᴴ * U) * U.map star := by rw [h1, Matrix.one_mul]
      _ = Uᴴ * (U * U.map star) := by rw [Matrix.mul_assoc]
      _ = Uᴴ * (ε • (1 : Matrix n n ℂ)) := by rw [hT]
      _ = ε • Uᴴ := by rw [Matrix.mul_smul, Matrix.mul_one]
  have key : (Uᴴ)ᵀ = U.map star := by
    ext i j
    simp [Matrix.conjTranspose_apply]
  rw [key, hbar]

/-- Bosonic sector: `T² = 1` gives a symmetric crosscap form. -/
theorem crosscap_symmetric {n : Type*} [Fintype n] [DecidableEq n] (U : Matrix n n ℂ)
    (hU : U * Uᴴ = 1) (hT : U * U.map star = 1) : (Uᴴ)ᵀ = Uᴴ := by
  have := crosscap_symm U 1 hU (by rw [hT, one_smul])
  rwa [one_smul] at this

/-- Kramers sector: `T² = -1` gives an antisymmetric crosscap form. -/
theorem crosscap_antisymmetric {n : Type*} [Fintype n] [DecidableEq n] (U : Matrix n n ℂ)
    (hU : U * Uᴴ = 1) (hT : U * U.map star = -1) : (Uᴴ)ᵀ = -Uᴴ := by
  have := crosscap_symm U (-1) hU (by rw [hT, neg_one_smul])
  rwa [neg_one_smul] at this

/-- The crosscap two-point matrix `G = 6 + 2A - J` of an `SRG(36,15,6,6)` satisfies `G² = 12 G`. -/
theorem bulk_projector {n : Type*} [Fintype n] [DecidableEq n] (A J : Matrix n n ℤ)
    (hAA : A * A = 9 • (1 : Matrix n n ℤ) + 6 • J) (hAJ : A * J = 15 • J) (hJA : J * A = 15 • J)
    (hJJ : J * J = 36 • J) :
    (6 • (1 : Matrix n n ℤ) + 2 • A - J) * (6 • (1 : Matrix n n ℤ) + 2 • A - J) =
      12 • (6 • (1 : Matrix n n ℤ) + 2 • A - J) := by
  have e : (6 • (1 : Matrix n n ℤ) + 2 • A - J) * (6 • (1 : Matrix n n ℤ) + 2 • A - J) =
      36 • (1 : Matrix n n ℤ) + 24 • A - 12 • J + 4 • (A * A) - 2 • (A * J) - 2 • (J * A) + J * J := by
    simp only [add_mul, mul_add, sub_mul, mul_sub, smul_mul_assoc, mul_smul_comm, Matrix.one_mul,
      Matrix.mul_one]
    abel
  rw [e, hAA, hAJ, hJA, hJJ]
  simp only [smul_add, smul_sub, smul_smul]
  abel

/-- The SRG(36,15,6,6) relation behind `hAA`: `k I + λ A + μ (J - I - A) = 9 I + 6 J` for `k = 15, λ = μ = 6`. -/
theorem srg_square_coefficients : (15 : ℤ) - 6 = 9 ∧ (6 : ℤ) - 6 = 0 ∧ 12 * 3 = 36 := by decide

end W33.Pass11848
