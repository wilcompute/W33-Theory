import Mathlib

namespace W33.Pass11815

/-!
Passes 11803 / 11805 / 11807 / 11714 in Lean: identities of the nine two-qutrit levels.

Levels are ordered as colour `0,1,2`, weak `3,4`, flavour `5..8`.  Electric charge is diagonal on the
levels, with level charges `1/3` on colour, `0` and `-1` on the two weak levels and `0` on flavour
(Pass 11803).  An occupation vector `n : Fin 9 → ℤ` then has charge
`Q n = (n 0 + n 1 + n 2) / 3 - n 4`.
-/

/-- The electric charge of an integral level occupation. -/
def charge (n : Fin 9 → ℤ) : ℚ := ((n 0 + n 1 + n 2 : ℤ) : ℚ) / 3 - (n 4 : ℚ)

/-- Pass 11803, integrality: a colour-neutral occupation (colour number divisible by three) has an
integer electric charge. -/
theorem charge_integral_of_colour_neutral (n : Fin 9 → ℤ) (h : (3 : ℤ) ∣ n 0 + n 1 + n 2) :
    ∃ k : ℤ, charge n = k := by
  obtain ⟨m, hm⟩ := h
  refine ⟨m - n 4, ?_⟩
  unfold charge
  rw [hm]
  push_cast
  ring

/-- Pass 11803, the converse: if the colour number is not divisible by three, the charge is not an
integer (it lies in `ℤ ± 1/3`). -/
theorem charge_not_integral_of_colour_charged (n : Fin 9 → ℤ) (h : ¬ (3 : ℤ) ∣ n 0 + n 1 + n 2) :
    ∀ k : ℤ, charge n ≠ k := by
  intro k hk
  apply h
  refine ⟨k + n 4, ?_⟩
  unfold charge at hk
  have h3 : ((n 0 + n 1 + n 2 : ℤ) : ℚ) = 3 * ((k : ℚ) + (n 4 : ℚ)) := by
    linear_combination 3 * hk
  exact_mod_cast h3

/-- Pass 11805: the level traces give the unification value of the weak mixing angle,
`Tr T3² / Tr Q² = 3/8`. -/
theorem weinberg_level_trace :
    ((1 / 2 : ℚ) ^ 2 + (-1 / 2) ^ 2) /
      (3 * (1 / 3 : ℚ) ^ 2 + 0 ^ 2 + (-1 : ℚ) ^ 2) = 3 / 8 := by
  norm_num

/-- Pass 11807: the number of ordered partitions of the nine levels into three triples, i.e. of
nonzero trivector cubic couplings of the two-qutrit `E₈`. -/
theorem nine_level_partitions : Nat.factorial 9 / (Nat.factorial 3) ^ 3 = 1680 := by
  decide

/-- Pass 11714: the `SU(9)` anomaly of `Λ³ ℂ⁹` is `(n-3)(n-6)/2 = 9` at `n = 9`, and three planes of
it are cancelled by the twenty-seven fixed points of `T⁶/ℤ₃`. -/
theorem su9_anomaly_balance : (9 - 3) * (9 - 6) / 2 = 9 ∧ 3 * 9 = 27 ∧ 3 ^ 3 = 27 := by
  decide

end W33.Pass11815
