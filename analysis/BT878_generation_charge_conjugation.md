# BT878 — Generation Charge-Conjugation: N(⟨R⟩)/C(R) = Z₂ Inverts the Grade

**Status: PROVEN (machine-verified, `analysis/bt878_generation_charge_conjugation.py`, data `data/bt878_generation_charge_conjugation.json`)**

The last piece of the discrete flavor/parity picture. R is the generation
symmetry (long-root transvection, BT874), C(R) the gauge group (BT876,
order 648). The normalizer-mod-centralizer N(⟨R⟩)/C(R) ≤ Aut(Z₃) = Z₂ asks
whether the substrate can invert the generation grade.

## The theorems

- **T1:** in W(E₆) = PGSp(4,3), |C(R)| = 648 and |N(⟨R⟩)| = 1296, so
  **N/C = Z₂**: there exists C with C R C⁻¹ = R⁻¹ = R². A generation
  charge-conjugation exists.
- **T2:** on the 27-matter shell, C R C⁻¹ = R⁻¹ means C **fixes grade-0 and
  swaps grade-1 ↔ grade-2** — the two off-diagonal generations. C is exactly
  generation charge-conjugation, inverting the Z₃ generation grade.
- **T3:** the discrete flavor/parity structure inside W(E₆) is now complete:

| symmetry | element | role |
| --- | --- | --- |
| generation Z₃ | R (long-root transvection) | the three generations (BT874) |
| generation C (Z₂) | N(⟨R⟩)/C(R) | inverts the grade, swaps gens 1↔2 (this) |
| matter chirality Z₂ | polar-pair involution | left/right matter (BT869) |
| gauge parity Z₂ | W/Q duality (A₄→S₄) | gauge handedness (BT877) |
| gauge group | C(R) = Stab(p₀) | SU(3)×SU(2)×U(1) = 1⊕3⊕8 (BT876) |

## Reading

The substrate carries the full discrete data of the Standard-Model flavor
sector as group theory inside W(E₆): a generation Z₃ (R), its charge
conjugation Z₂ (C, the CP-like grade inversion that exchanges the two
non-trivial generations), a matter chirality Z₂ (the polar-pair involution),
and a gauge parity Z₂ (the duality). C is the discrete shadow of CP — it
conjugates the generation grading exactly as the single-photon paper's CPT
theorem conjugates the temporal Bell qutrit (ω ↦ ω̄). The "why three
generations + their conjugation + chirality + parity" of the SM flavor sector
is the normalizer geometry of one long-root transvection.

## Open

- C combined with the matter chirality and gauge parity: does
  C × chirality × parity generate a Klein-type discrete group acting as
  full CPT on the matter register?
- The CP phase (CKM δ): C inverts the grade, but the CP-violating phase
  should be the failure of C to be realized by a real (grade-preserving-up-
  to-phase) element — measure the obstruction.
