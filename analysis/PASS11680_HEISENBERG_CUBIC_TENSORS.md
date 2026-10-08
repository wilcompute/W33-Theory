# Pass 11680 — the Pauli-invariant cubic tensors of n qutrits are a conjugate copy of the Hilbert space, and their permutation symmetry is the Weil parity

Producer: `analysis/w33_pass11680_heisenberg_cubic_tensors.py`
Certificate: `data/w33_pass11680_heisenberg_cubic_tensors.json`
Regression: `tests/test_w33_pass11680_11686.py`

## Theorem (every n)

**Setup.** Let V = C^{3ⁿ}, with the n-qutrit Pauli group acting on V^{⊗3} by P ⊗ P ⊗ P.

**Dimension.** The centre acts trivially and every non-identity Pauli is traceless, so

  dim (V^{⊗3})^{Pauli} = 3^{3n}/3^{2n} = 3ⁿ.

**The invariants** are exactly

  **T_u = Σ_a |a⟩ ⊗ |a + u⟩ ⊗ |a − u⟩,  u ∈ F₃ⁿ.**

Z-invariance forces the three labels to sum to 0, and X-invariance forces the translation sum.

**How permutations act.**
* A 3-cycle of the tensor factors fixes every T_u.
* A transposition sends T_u ↦ T_{−u}.

Hence:

| part | spanned by | dimension | Weil half |
|---|---|---|---|
| Sym³ | T_u + T_{−u} | (3ⁿ + 1)/2 | **even** |
| Λ³ | T_u − T_{−u} | (3ⁿ − 1)/2 | **odd** |
| mixed | — | **0** | — |

**Parity is permutation symmetry.** The transposition sign of a Pauli-invariant cubic tensor *is* the Weil parity u ↦ −u, the central element −1 of Sp(2n, 3).

**The Clifford action** on the 3ⁿ invariants is the complex conjugate of the Weil representation. At n = 1 and 2, 40/40 random Clifford words match the conjugate even and odd blocks.

## The three cases checked

| n | Sym³ (even) | Λ³ (odd) | meaning |
|---|---|---|---|
| 1 | 2 | 1 | the Hesse doublet of Pass 11641 plus the determinant ψ₀ ∧ ψ₁ ∧ ψ₂ |
| 2 | 5 | 4 | the **Burkhardt space** of Passes 11651/11657/11659 plus the **E₈ Cartan** of Pass 11681 |
| 3 | 14 | 13 | — |

**The n = 2 odd basis.** It consists of the four sums over the parallel classes of lines of AG(2,3):

  h_u = Σ_{lines ℓ ∥ u} e_{ℓ₁} ∧ e_{ℓ₂} ∧ e_{ℓ₃}.

These are the classical **Vinberg–Elashvili Cartan subspace** of Λ³C⁹, whose little Weyl group is the Witting group G₃₂.

## Reading

**One space, two exceptional sides.** Three copies of a two-qutrit system, averaged over the Pauli group, give back one copy of the (conjugated) two-qutrit space.
* **Bosonic (symmetric) triples** carry the even half: the Burkhardt/Coble geometry (G₃₃; factorisations, concurrences, Pass 11659).
* **Fermionic (antisymmetric) triples** carry the odd half: the Witting/E₈ geometry (Pass 11681).

**Codex's vanishing explained.** It also accounts for Pass 11663's finding that the symmetric cubic vanishes on the odd sector.

**Prior art.**
* Classical: Λ³C⁹ as Vinberg's θ-representation of the A₈-grading of E₈ (Vinberg–Elashvili 1978), and the Hesse configuration's 12 lines.
* Gruson–Sam–Weyman connect Λ³C⁹ to Coble cubics and abelian surfaces.
* New here: the all-n statement in Pauli language, the identification of the transposition sign with Weil parity, and the placing of Burkhardt (Sym³) and Witting (Λ³) side by side as the two halves of one 9-dimensional space.
