# Passes 11697–11698 — the chirality order parameter is Weil parity in disguise, and its quartic condenses on a W(3,3) flag

Producer: `analysis/w33_pass11697_11698_chirality_vacuum.py`
Certificate: `data/w33_pass11697_11698_chirality_vacuum.json`
Regression: `tests/test_w33_pass11697_11703.py`

**Question (from Pass 11693, target 2).** Pass 11689 named Im⟨P⟩ as the lowest C × T-odd order parameter for matter chirality. Pass 11649's potential was unbounded (Codex 11663 intake). Is there a *bounded* potential that condenses Im⟨P⟩, and what does its vacuum select?

## 11697 — THEOREM (every n): S = (d/2)(1 − ⟨Π⟩²)

**Setting.**
* n qutrits, d = 3ⁿ.
* Symmetric Weyl operators D_v = τ^{x·z}XˣZᶻ with τ = ω².
* Π, the Pauli inversion |x⟩ ↦ |−x⟩. This is the Weil parity: +1 on the even sector, −1 on the odd sector.

For every unit state ψ,

  **S(ψ) := Σ_{v≠0} (Im⟨D_v⟩)² = (d/2)·(1 − ⟨Π⟩²).**

**Proof.**
1. Write a_v = ⟨D_v⟩. Since a_{−v} = conj(a_v), we get S = ½Σ|a_v|² − ½ Re Σ a_v².
2. For a pure state, Σ_{v≠0}|a_v|² = d − 1.
3. Π D_v Π = D_{−v} = D_v^†, and Σ_v D_v ⊗ D_v^† = d·SWAP. Together these give Σ_v D_v ⊗ D_v = d·(I⊗Π)·SWAP·(I⊗Π), hence Σ_v a_v² = d⟨Π⟩².

Checks:
* the operator identity holds to 3·10⁻¹⁴ (n = 1, 2);
* the formula holds to 10⁻¹⁴ on random states (n = 1, 2, 3).

**Consequences.**
* **The quadratic functional cannot select anything.** It is maximal (d/2) on every state with equal weight in the even and odd Weil sectors, a huge degenerate set. This explains the earlier numerical maximiser with spread, unremarkable Pauli expectations.
* **Boundedness.** S ≤ (d/2)|ψ|⁴, so λ(|ψ|² − 1)² − μS is bounded below iff λ ≥ (d/2)μ. The bound 8|ψ|⁴ quoted during this round was not sharp.
* **Rewording.** The total chirality intensity is fixed by the C-type parity ⟨Π⟩ of Pass 11689's ε.

## 11698 — THEOREM (two qutrits): the quartic selects a flag and a chirality

Let S4 := Σ_{v≠0} (Im⟨D_v⟩)⁴.

**Claim.** S4 ≤ 27/8. Equality holds **exactly** on the 320 stabiliser states of a Lagrangian line with a nontrivial character.

**Proof.**
1. For a projective point P with eigen-weights p₀, p₁, p₂ (eigenvalues 1, ω, ω²), Im⟨D_v⟩ = ±(√3/2)(p₁ − p₂) for both v in P.
2. Hence S = (3/2)Σ_P(p₁ − p₂)² and S4 = (9/8)Σ_P(p₁ − p₂)⁴.
3. By 11697, S ≤ 9/2, so Σ_P(p₁ − p₂)² ≤ 3. Since x⁴ ≤ x² on [−1, 1], S4 ≤ 27/8.
4. Equality forces every |p₁ − p₂| into {0, 1}, with exactly three points at 1. So ψ is an ω- or ω²-eigenvector of three pairwise-commuting Paulis.
5. W(3,3) is a generalised quadrangle and has **no triangles**, so the three points are collinear. The state is the stabiliser state of that line L, with a character that is trivial only at the fourth point p of L.

**Checks.**
* Census over all 360 line-stabiliser states: 320 at 27/8 and 40 (trivial character) at 0.
* 400 BFGS starts all reach 3.3749999999999867.
* The maximiser has ⟨Π⟩ = −2·10⁻⁸.

**The vacuum.** With λ, μ > 0, the bounded potential

  V = λ(|ψ|² − 1)² + μ((27/8)|ψ|⁸ − S4) ≥ 0

has exactly these 320 vacua, i.e. 160 flags (p ∈ L) × 2 conjugate characters. Each vacuum selects:
* **a W(3,3) line L**, whose centraliser is SU(3)⁴ (trinification-type; Pass 11687);
* **a distinguished point p ∈ L**, where ⟨D_p⟩ is real;
* **a sign of Im⟨D_q⟩** at the other three points q of L, i.e. a matter chirality for the three E₆ × SU(3)_q shells (Pass 11689).

The two characters are exchanged by Π (the C-like ε). The potential is C- and T-even, so the choice is **spontaneous**.

## Scope

* **Claimed:** two exact theorems about these functionals and potentials.
* **Not claimed:**
  * that nature minimises V;
  * which flag is chosen;
  * that the selected sign is the observed (left-handed) one, since the two vacua are degenerate by construction.

The vacuum is a *stabiliser* state. This is the opposite of the magic needed for SM-shaped ticks (Passes 11692, 11701), so the vacuum and the clock carry different resources.

## Prior art

* Pauli/Weyl sums Σ D_v ⊗ D_v^† = d·SWAP: standard (unitary-design and stabiliser-entropy literature).
* The stabiliser Rényi entropy uses Σ|a_v|⁴, not the Im-only sums used here.
* No identity S = (d/2)(1 − ⟨Π⟩²) was found by result-grep in `analysis/*.md`, `RESULTS_INDEX.md` or the paper.
