import Mathlib

namespace W33.Pass446

/-!
The arithmetic skeleton of the antipodal cover law (repository witness P394)
and the nesting tower law (P430), as checked ring identities. The incidence
geometry itself (the perp-of-span lemmas) is a named formalization boundary,
exactly as the central Fourier decomposition is for Pass 441.
-/

/-- Distance shells of the cover sum to the bulk: 1 + (q²-1) + (q-1)(q²-1) + (q-1) = q³. -/
theorem shell_sum (q : ℤ) :
    1 + (q ^ 2 - 1) + (q - 1) * (q ^ 2 - 1) + (q - 1) = q ^ 3 := by
  ring

/-- The b₁ entry of the intersection array: (q²-1) - 1 - (q-2) = q(q-1). -/
theorem b1_identity (q : ℤ) :
    (q ^ 2 - 1) - 1 - (q - 2) = q * (q - 1) := by
  ring

/-- Second-shell size from the array: k·b₁/c₂ with c₂ = q gives (q-1)(q²-1). -/
theorem second_shell (q : ℤ) :
    (q ^ 2 - 1) * (q * (q - 1)) = q * ((q - 1) * (q ^ 2 - 1)) := by
  ring

/-- Trace-pinned multiplicities: a(q-1) = b(q+1) for a = q(q²-1)/2, b = q(q-1)²/2,
    cleared of denominators. -/
theorem multiplicity_pairing (q : ℤ) :
    q * (q ^ 2 - 1) * (q - 1) = q * (q - 1) ^ 2 * (q + 1) := by
  ring

/-- The multiplicity difference: a - b = q(q-1), cleared of denominators:
    q(q²-1) - q(q-1)² = 2q(q-1). -/
theorem multiplicity_difference (q : ℤ) :
    q * (q ^ 2 - 1) - q * (q - 1) ^ 2 = 2 * (q * (q - 1)) := by
  ring

/-- Dimension count: a + b = q²(q-1), cleared of denominators. -/
theorem multiplicity_total (q : ℤ) :
    q * (q ^ 2 - 1) + q * (q - 1) ^ 2 = 2 * (q ^ 2 * (q - 1)) := by
  ring

/-- Nested SRG degree: (q²-1) + (q-1) = (q-1)(q+2). -/
theorem nested_degree (q : ℤ) :
    (q ^ 2 - 1) + (q - 1) = (q - 1) * (q + 2) := by
  ring

/-- Nested SRG μ from the eigenvalues r = q-2, s = -(q+2): μ = k + rs = q+2. -/
theorem nested_mu (q : ℤ) :
    (q - 1) * (q + 2) + (q - 2) * (-(q + 2)) = q + 2 := by
  ring

/-- Nested SRG λ = μ + r + s = q-2. -/
theorem nested_lambda (q : ℤ) :
    (q + 2) + (q - 2) + (-(q + 2)) = q - 2 := by
  ring

/-- The abelian-PDS obstruction bookkeeping (P433): k - r = q² and s - r = -2q. -/
theorem pds_bookkeeping (q : ℤ) :
    (q - 1) * (q + 2) - (q - 2) = q ^ 2 ∧ (-(q + 2)) - (q - 2) = -(2 * q) := by
  constructor <;> ring

/-- SRG feasibility: k(k-λ-1) = (v-k-1)μ, cleared: both sides equal q(q+2)(q²-q-... -/
theorem srg_feasibility (q : ℤ) :
    (q - 1) * (q + 2) * ((q - 1) * (q + 2) - (q - 2) - 1) =
    (q ^ 3 - (q - 1) * (q + 2) - 1) * (q + 2) := by
  ring

end W33.Pass446
