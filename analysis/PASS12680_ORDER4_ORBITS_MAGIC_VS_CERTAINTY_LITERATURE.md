# Pass 12680: 893,088 uncovered order-4 groups in 17 orbits, the minimisers in exactly two; magic does not select c₈; literature placement

Claude track. Follows Pass 12679. **Not a theory of everything.**

## 1. Orbit classification of uncovered order-4 groups (`w33_f8_order4_orbit_classification.py`)

All uncovered isotropic order-4 Pauli groups {0, a, b, a + b} of the F₈ regulus were enumerated: **893,088** of them. They fall into **17 orbits** under H = (SL(2,8) × SL(2,8)) ⋊ Frobenius, the regulus symmetries m ↦ g·m·hᵀ (union-find under 9 generators; Paulis act trivially on subgroups).

| type (coset weights) | orbits (sizes) |
|---|---|
| A {1: 63, 2: 36} | 1 (1,512) |
| B {1: 99, 2: 18} | 5 (84,672 ×3, 42,336 ×2) |
| C {1: 54, 2: 27, 3: 9} | 2 (42,336; 14,112) |
| {1: 107, 2: 14} | 2 (108,864; 54,432) |
| {1: 135} (every coset weight ≤ 1) | 2 (1,512; 504) |
| five further types | 1 each |

**Where the minimisers sit.** All 16 census minimisers of Pass 12674 have stabilisers in exactly **two** orbits: the unique type-A orbit (9 minimisers) and **one** of the five type-B orbits, of size 42,336 (7 minimisers). The other 15 orbits, including the four other type-B orbits and both type-C orbits, contain none. The 48 minimisers of the 600-start census (24 A, 24 B) were not re-assigned to orbits here.

> **Sharpened reduction claim (numerical).** Every global minimiser found is stabilised by a group in orbit A (1,512 groups) or in one specific type-B orbit (42,336 groups). The coset-weight type alone does not single out the orbit.

## 2. Magic versus certainty across the torus eigenstates (`w33_f8_torus_eigenstate_magic.py`)

The logical stabiliser fidelity of all 512 torus Clifford eigenstates (64 lifts × 8), by eigenvalue index r:

| r | c(ψ_r) (Pass 12673) | logical stabiliser fidelity |
|---|---|---|
| ±4 | c₈ = 2.4985 (minimum) | **0.509929113 = (3 + √3)·cos²(π/18)/9** |
| ±1 | 4.6048 | **0.509929113** |
| ±2 | 8.5634 | **0.509929113** |
| ±3 | 37/3 | 0.490562612 |

- The three primitive pairs, which carry the three Galois-conjugate certainty values, have **identical** stabiliser fidelity. Only the non-primitive pair differs.
- So the closed form of Pass 12679 belongs to the whole primitive Galois family, not to the minimum. **Certainty and magic are independent here**: the minimiser is neither the most nor the least magic state in its family.

## 3. Literature placement (web search, 2026-11-16)

- **Three qubits and E₇.** W(E₇)/Z₂ ≅ Sp(6,2) as the three-qubit symplectic group, with the 28 bitangents and Steiner complexes, is established: Cerchiai–van Geemen, "From qubits to E7" ([arXiv:1003.4255](https://arxiv.org/abs/1003.4255)). It has been used for black-hole entropy, the "magic three-qubit Veldkamp line" ([Lévay–Planat–Saniga, arXiv:1704.01598](https://arxiv.org/pdf/1704.01598)).
- **Witting configuration.** 40 rays in C⁴, symmetry group 2·U₄(2) ≅ 2·PSp(4,3), with MUB-related structure ([arXiv:2208.13644](https://arxiv.org/pdf/2208.13644), [arXiv:2503.18431](https://arxiv.org/pdf/2503.18431)). The corpus already identifies the Witting configuration with W(3,3).
- **No source found** treats the F₈ regulus certainty constant, its E₆(a₁) eigenstates, the bitangent selection (Pass 12678) or the stabiliser fidelity above. The chain E₇ → bitangent → E₆ → E₆(a₁) → c₈ sits inside known finite geometry, and its F₈-specific content appears to be new as far as these searches go.

## 4. Not done

- **Exact c₈ certificate.** Scoped in Pass 12679; needs compiled number-field arithmetic.
- **Degree 8 on type-B code spaces.** About 2×10⁶ pair variables with Pauli symmetry alone, and the type-B minimiser set is a positive-dimensional family, so the face is not finite.
- **Exact Galois test at q = 16.** Not attempted.
