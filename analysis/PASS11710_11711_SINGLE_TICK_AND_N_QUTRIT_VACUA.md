# Passes 11710–11711 — a single natural Standard-Model tick, and the chirality vacua for every number of qutrits

Producer: `analysis/w33_pass11710_11711_single_tick_and_n_qutrit_vacua.py`
Certificate: `data/w33_pass11710_11711_single_tick_and_n_qutrit_vacua.json`
Regression: `tests/test_w33_pass11706_11712.py`

## 11710 — one tick with exactly SM-shaped symmetry

**The gate.** Let R = ζ₂₇^{x³} = diag(1, ζ₂₇, ζ₂₇⁸). It is the fourth-level qutrit gate with R³ = T.

**The scan.** The family (Rᶜ¹ ⊗ Rᶜ²)·CZᵉ has 6,561 gates, each with 3 determinant-one lifts.
* Exactly **648** elements leave su(3) ⊕ su(2) ⊕ u(1)⁵ unbroken.
* All 648 have E₈ order **27**. Pass 11701's Kac bound requires order ≥ 16, and 27 is the first qutrit-tower order above it.
* 108 of the 648 are unentangled.

**The simplest is R² ⊗ R⁻¹** (lift 1), with its swap and its inverse: a pair of opposite-handed fourth-level phase gates, one on each qutrit, with exponent ratio −2.

## 11711 — THEOREM (every n): S4 ≤ (9/8)·3^{n−1}, with equality exactly on the Lagrangian stabiliser states with a nontrivial character

**Statement.** On n qutrits, with S4 = Σ_{v≠0}(Im⟨D_v⟩)⁴:
* S4 ≤ (9/8)·3^{n−1};
* equality holds exactly on the stabiliser states of Lagrangian subspaces with a nontrivial character;
* there are ∏ᵢ(3ⁱ + 1)·(3ⁿ − 1) such states: **8, 320, 29,120** for n = 1, 2, 3.

**Proof.** This is Pass 11698's argument.
1. S = (3/2)Σ_P(p₁ − p₂)² = (d/2)(1 − ⟨Π⟩²) (Pass 11697). Hence Σ_P(p₁ − p₂)² ≤ 3^{n−1}.
2. S4 = (9/8)Σ(p₁ − p₂)⁴, and x⁴ ≤ x² on [−1, 1]. Hence the bound.
3. Equality needs 3^{n−1} pairwise-commuting ω^{±1}-eigen-Paulis. Their span W is isotropic, of dimension k ≤ n, and ψ is a joint eigenvector of W with character χ.
4. The points of W with χ ≠ 1 number 3^{k−1}, so k = n: W is Lagrangian.
5. Conversely, such states have exactly 3^{n−1} chirality points and zero expectation elsewhere.

**Check.** Random-start maximisation reaches the bound in every run: n = 1 (100/100), n = 2 (40/40), n = 3 (20/20).

**Reading.** The quartic chirality potential condenses on a maximal commuting set of Paulis, together with a sign, for any number of qutrits. For n = 2 this is the W(3,3) flag picture of Pass 11698.
