# Pass 12664: the type B certainty relation as a four-qubit experiment: five circuits of at most three CZ gates

Claude track. Follows Pass 12663. **Not a theory of everything.**

## 1. The five measurements are short circuits (`w33_typeB_hardware_circuits.py`)

For the F₄ regulus set, write each ququart as two qubits via the F₂-basis {1, ω} of F₄. Then:
- the F₄-Fourier transform is H⊗H (up to relabelling outcomes);
- CZ_t = (−1)^{Tr(t·x₁x₂)} is a product of two-qubit CZ gates between (a₀, a₁) and (b₀, b₁), along the bipartite graph with biadjacency M_t[i][j] = Tr(t·b_i·b_j).

| measurement | t | CZ gates (then H on all four qubits, then read out) | count |
|---|---|---|---|
| A | 0 | none | 0 |
| B | 1 | a₀–b₁, a₁–b₀, a₁–b₁ | 3 |
| C | ω | a₀–b₀, a₀–b₁, a₁–b₀ | 3 |
| D | ω² | a₀–b₀, a₁–b₁ | 2 |
| E | ∞ | none, no Hadamards (computational basis) | 0 |

**Checks.**
- The circuits are built from H and CZ matrices on a 16-dimensional state vector, with no finite-field code. F computed from them equals the CZ-model F for 20 random states to 9×10⁻¹⁶.
- Minimising F through the circuit unitaries alone gives 0.0625000 = 1/16, an independent re-derivation of the numerical optimum.

## 2. The statement to test

For every four-qubit state, the total collision probability over the five settings,

Σ over settings of Σ over outcomes of p²,

is **at least 5/16 + 11/250 = 0.3565** (proved exactly, Pass 12663). Numerically it is at least 5/16 + 1/16 = 0.375, attained by stabiliser states. A maximally mixed state gives 5/16 = 0.3125.

**Noise.** Under global depolarisation ρ ↦ λρ + (1−λ)I/16, every p − 1/16 scales by λ, so the excess over 5/16 scales by λ²:

| λ | floor, numerical | floor, proved |
|---|---|---|
| 1.00 | 0.0625 | 0.0440 |
| 0.95 | 0.0564 | 0.0397 |
| 0.90 | 0.0506 | 0.0356 |
| 0.80 | 0.0400 | 0.0282 |
| 0.70 | 0.0306 | 0.0216 |

So hardware noise lowers the total and can fake a violation. A meaningful test needs an independent estimate of λ: for example a separate fidelity benchmark, or the same five circuits run on a reference state whose total is known (the basis state |0000⟩ has total 1.25 when noiseless, i.e. excess 15/16 over 5/16, which shrinks by λ²).

**Shots.** The plug-in estimate of Σp² from N shots is biased upward by about (1 − Σp²)/N per setting. Keeping the total bias under a tenth of 1/16 needs about 750 shots per circuit. This is a rough guide, not a full error analysis.

## 3. Ownership correction for Pass 12663

The parity theorem of Pass 12663 was proved first by the other track, in a stronger every-coset form (`analysis/2026-11-14_regulus_stabilizer_variation.md`, 0b8e11c16). An ownership note was added to the Pass 12663 file. The same commit also gives an exact descending curve from the F₈ weight-3 stabiliser (a saddle), and its neighbours prove fourth-order stability of the F₃₂ weight-11 state (fd78b3194) and an integer-certified lower bound 2.0818 for the F₈ problem on the common four-qubit code (c04b00587).

## 4. Public page

The playable page "Five Measurements" (claude.ai artifact, private to the user) now lists the five circuits, the proved and observed floors, and the noise caveat.
