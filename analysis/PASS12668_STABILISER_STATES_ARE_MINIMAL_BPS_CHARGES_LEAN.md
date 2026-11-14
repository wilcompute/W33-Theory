# Pass 12668: the 1,080 three-qubit stabiliser states fibre 6-to-1 over the 180 minimal integral BPS charges, each fibre a logical qubit; Lean formalisation of the attractor majorisation inequalities

Claude track. Follows Pass 12667. **Not a theory of everything.**

## 1. Stabiliser states and minimal charges (`w33_stabiliser_states_minimal_charges.py`)

In the Pauli realisation of the E6(6) cubic (Passes 12655–12656), a state ψ has charge Z_v = ⟨ψ|P_v|ψ⟩ over the 27 Paulis commuting with J = (Y⊗I⊗I)K.

| quantity | result |
|---|---|
| three-qubit stabiliser states | 1,080 |
| distinct charges | 180 |
| integral charges with entries in {0, ±1}, support a tritangent triad, N = +1 (Pass 12655 table) | 180 |
| image = that set | **yes** |
| fibre sizes | **6** for all 180 |
| span of each fibre | dimension 2, equal to the quaternionic line span{ψ, Jψ}, for all 180 |
| overlaps inside a fibre | three orthogonal pairs and twelve overlaps 1/2, for all 180 |

So the six states in a fibre are the six stabiliser states of a single qubit (eigenstates of its three logical Paulis) living on the line span{ψ, Jψ}.

**Reading** (5D dictionary of Passes 12665–12667). The smallest integral 1/8-BPS charges, N = 1 with |Z|² = 3, are exactly the stabiliser states up to a logical-qubit degree of freedom. Each minimal black-hole charge "is" a logical qubit, and its six stabiliser states are indistinguishable by the charge.

**Literature.** Lévay, Saniga, Vrana and Pracna label the split Cayley hexagon of order two and the E7 and E6 entropy formulas with three-qubit operators (arXiv:0808.3849, 0903.0541). The fibration statement here was not found in the sources searched; novelty unverified.

## 2. Lean formalisation (`formal/W33/Pass12667AttractorMajorisation.lean`)

The endpoint majorisation of Pass 12667 (proved first, along the whole flow, by the other track, 8e73be5b5) reduces to three real inequalities, now machine-checked with Mathlib. For a ≥ b ≥ c > 0 and g > 0 with g³ = abc:

- `max_ge_geomean`: g ≤ a;
- `sum_ge_three_geomean`: 3g ≤ a + b + c (AM-GM via 27abc ≤ (a+b+c)³ and monotonicity of t³);
- `attractor_majorisation`: 3g ≤ a + b + c ∧ 2g ≤ 2a ∧ g ≤ a + b − c.

Compiled with `lake env lean` against the repository's Mathlib (v4.32.0-rc1): exit code 0, no errors, no `sorry`; two `push_neg` deprecation warnings and one unused-variable warning. The module is not added to `W33.lean`'s import list, so `lake build` does not depend on it.

## 3. Experimental context (web)

- Photonic MUB experiments exist: a non-extendable triple in d = 6 (arXiv:1304.4081); inequivalent MUBs in d = 4 (PRL 132, 080202 (2024), arXiv:2311.06539); entropic uncertainty relations in d = 3–5 with frequency bins (arXiv:2507.05025).
- Certainty relations (upper bounds on entropy sums) are studied theoretically (e.g. arXiv:2002.00004), and are trivial for extendible MUB sets.
- No experiment on a strongly unextendible Pauli MUB set, or a test of a proved certainty bound in d = 16, was found. The four-qubit five-circuit test of Pass 12664 (pure states only, as corrected by the other track) would be a cheap first.

## 4. Shannon capacity: low-symmetry classes (`w33_shannon_long_lowsym.py`)

Longer CP-SAT runs in the cyclic classes where the earlier solver bound was loose. See the addendum; the order-4 class closed at an optimum of 56.
