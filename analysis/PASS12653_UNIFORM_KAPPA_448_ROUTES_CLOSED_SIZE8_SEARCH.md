# Pass 12653: κ ≤ 3 holds uniformly on all 448 six-Pauli supports; three proof routes to exact 1/d closed with controls; the five-qubit 9-set is not a lift; an exhaustive size-8 search

Claude track. Follows Pass 12652. **Not a theory of everything.**

## 1. κ ≤ 3 on all 448 supports (`w33_kappa_448_supports.py`) — cross-track

The parallel assistant reported (2026-11-13; pasted into this session, its script is not in this repository):
- 448 six-element subsets of two-qubit Pauli labels have 15 pairwise differences equal to all of F₂⁴ \ {0};
- these form three affine-symplectic orbits of sizes 16, 192 and 240;
- the repository pentagon model lies in the 192-orbit, which has a PPT Choi matrix;
- there is a non-stabiliser κ = 3 equality family y_t ∝ (1, it, −it, 1).

**Reproduced independently here**: 448, orbits [16, 192, 240], PPT only for the 192-orbit (min PT eigenvalue 0, versus −2 and −6), and the y_t identity Σ M|y_t⟩⟨y_t|M† = I + 2|v_t⟩⟨v_t| with spectrum (3,1,1,1) and ⟨XX⟩ = −3/5 at t = 2.

**New observation.** The two-moment proof of Pass 12652 uses exactly this 448-support property, so **κ ≤ 3 holds on every support**: Tr G = 6 and Tr G² = 12 were checked on all 448.
- The bound is **attained on the 192- and 240-orbits** (κ = 3).
- It is **not attained on the 16-orbit**, the twisted Werner–Holevo channel, where κ = 2.
- So the inequality and its proof do not see PPT-ness: the PPT orbit (192) and the NPT orbit (240) are both tight.

Rank-6 lattice states and the PPT classification are prior art (arXiv:0803.1778, as cited by the other track); the identification is theirs, and the uniform bound is the moment argument's.

## 2. Three routes to exact 1/d, closed (each with a passing control)

**(a) Self-dual Pauli-spectrum LP** (`w33_selfdual_pauli_lp.py`).
- For pure states, m_b = ⟨P_b⟩² satisfies Σ_b (−1)^{ω(a,b)} m_b = d·m_a (verified to 4×10⁻¹⁵ at n = 2, 3, 4).
- The LP max Σ_U m_b subject to m ≥ 0, m₀ = 1 and self-duality (with or without anticommuting-triple cuts) gives **exactly the trivial d − 1** for:
  - the three-qubit five-set;
  - both four-qubit five-set types;
  - the five-qubit 9-set.
- **Valid, useless.** Squares cannot see the sign structure that the Lovász SDP or the moment argument uses.

**(b) Conditioning** (`w33_five_qubit_conditioning_scan.py`, `w33_four_qubit_conditioning_scan.py`).
- The Pass 12649 route at a general uncovered P0 gives Σ_U ≤ max(1 + λ_B, λ_B + κ_A). Here λ_B is the weighted commuting part (weight 2 for doubly uncovered cosets, Cauchy–Schwarz for single ones) and κ_A the paired anticommuting part.
- **Control:** at n = 3 the best P0 gives exactly 6, with coset multiplicities {1: 15} and 6 paired anticommuting classes, which is Pass 12649.
- **n = 4:** the best is 21 for both types A and B, over all 180 points (needed: 14). Type B's 120 lift points have multiplicities {0: 0, 1: 35, 2: 28}, with λ_B = 13 and κ_A = 8.
- **n = 5:** every one of 40 sampled points gives λ_B = 29, κ_A = 16 and bound 45 (needed: 30). Coset multiplicities run through {0: 13–22}.
- **The conditioning route is special to d = 8.**

**(c) Swap/Bell (Pass 12652 addendum B):** already negative.

## 3. The five-qubit 9-set is not a lift (`w33_five_qubit_lift_points.py`)

- **Control:** the same code finds 0 lift points for four-qubit type A and 120 for type B (Pass 12648).
- **Five qubits:** of the 744 uncovered points, **none** even has pairwise-disjoint images of the nine Lagrangians in p⊥/⟨p⟩ ≅ W(7,2).
- So an inductive proof of 1/32 through the certified four-qubit 9-sets (ϑ = 14, Passes 12644–12646) is not available for this set.

## 4. Type B: the coupled inequality, restated

In a basis i of the lifted set, each lift-point pair is {f_m ⊗ φ₊, f_m ⊗ φ₋}. So Σ_k p_k² = ½ Σ_m [(p_k + p_{σk})² + (p_k − p_{σk})²], where the first term depends only on ρ = Tr_qubit |v⟩⟨v|, a rank-2 three-qubit state. The 1/16 claim becomes:
- F̄₃(ρ) + Σ_{i,m} r_{i,m}² ≥ 1/8, where r is the qubit coherence of each block along that basis's axis;
- F̄₃ alone fails for mixed ρ (F̄₃(I/8) = 0), so the coherence terms carry the proof.

This is a reformulation, not a proof (Pass 12652 addendum C: max c = 36 > 28).

## 5. Five qubits, size 8: an exhaustive search (`w33_five_qubit_size8_dlx.py`)

**Method.** Exact-cover branching: pick the uncovered compatible T with the fewest killers, branch over the killers, and exclude earlier siblings. Add the valid top-r prune of Pass 12649. Then run 8 O(5)-orbit representatives of S₂ in parallel.

**Controls:**

| run | result | nodes | time | reference |
|---|---|---|---|---|
| n = 3, size 5 | exists | — | — | |
| n = 3, size 7 | none | — | — | |
| n = 5, size 9 | exists | 514 | 3 s | Pass 12650 |
| n = 5, size 7 | none | 4,194,657 | 517 s wall (8 orbits × ~510 s) | Pass 12649 DFS: 8,668,424 nodes, 2,695 s |

The per-orbit node counts at size 7 are nearly equal (522,808 to 525,273). The representatives come from distinct O(5)-orbits by construction, but **why the counts are so close has not been investigated**. It is flagged here because it is unusual.

**Size 8:** running when this note was committed, at about 17 s per top-level branch out of 1,408 per orbit. **Result: see addendum.**

## Open

- Exact 1/32 (five qubits) and exact 1/16 (type B): ϑ, conditioning, self-dual LP and swap bounds all fail. What remains is a coupled-moment argument, or exact SOS/facial reduction with symmetry.
- The six-qubit minimum, and the size-8 result (addendum).
