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

The per-orbit node counts at size 7 are nearly equal (522,808 to 525,273). The representatives come from distinct O(5)-orbits by construction.
- **Explanation** (`w33_rank_code_s3_symmetry.py`): all 8 orbits have size 720 = |O(5)| (free action).
- The symplectic maps S → S⁻¹ and S → S + I permute the three fixed Lagrangians (S = 0, ∞, I) as S₃. They merge the 8 orbits into **two classes, {692, 693} and {694, 695, 700, 701, 702, 703}**. At n = 3 the 2 orbits merge into 1, consistent with the single Sp(6,2)-orbit.
- So the full symmetry of the anchored problem is O(5) × S₃ (order 4,320), and two representatives suffice.
- The 8-orbit run is therefore an internal consistency check: orbits in the same class must agree.

**Size 8:** running when this note was committed, at about 17 s per top-level branch out of 1,408 per orbit. **Result: see addendum.**

## Open

- Exact 1/32 (five qubits) and exact 1/16 (type B): ϑ, conditioning, self-dual LP and swap bounds all fail. What remains is a coupled-moment argument, or exact SOS/facial reduction with symmetry.
- The six-qubit minimum, and the size-8 result (addendum).

## Addendum A: perpendicular directions (same pass)

### A1. Shannon capacity of the W(3,3) collinearity graph: the Pass 51 theorem is an over-read; √57 ≤ Θ ≤ 10

**The flaw.** Pass 51 (`analysis/w33_shannon_capacity.py`, `papers/standalone/holonet_shannon_capacity.tex`, 2026-07-10) "proved" Θ(W(3,3)) = 10 from the lemma "for vertex-transitive G, Θ = ϑ (Lovász 1979)". **That lemma is false.**
- Lovász proves Θ ≤ ϑ, and ϑ(G)ϑ(Ḡ) = n for vertex-transitive G.
- Haemers' rank bound gives vertex-transitive counterexamples.

**Control** (`w33_shannon_capacity_audit.py`). For the meeting graph of the 27 lines on a cubic surface: ϑ = 9, the F₂ rank of A + I is 7, and α = 6. **So Θ ≤ 7 < ϑ = 9.**

**W(3,3).**
- α = 7: CP-SAT OPTIMAL, consistent with no ovoid for odd q.
- ϑ = 10.
- The best Haemers bound from A + cI over F_p, p ≤ 13, is 11, so it does not improve on ϑ.
- Local minrank search over F₂/F₃ reaches only 33/35 (C₅ control reaches 3), which is uninformative.

**New lower bound** (`w33_shannon_square.py`, verified by `w33_shannon_square_verify.py`). CP-SAT (900 s, 2 workers; C₅⊠C₅ control = 5) finds an **independent set of size 57 in G⊠G** (solver bound 101).
- It was re-checked on an independently constructed W(3): a different symplectic form and enumeration, the GQ axiom checked, and a VF2 isomorphism. Result: 0 conflicts.
- Hence **√57 ≈ 7.550 ≤ Θ(W(3,3)) ≤ 10**. Θ > α, and the exact value is open.
- The code is irregular (21 distinct first coordinates), so it is not a clean product construction.
- A standard literature search found no prior bound for this graph. For the dual GQ Q(4,3) (which has ovoids), α = ϑ = 10, so Θ = 10 there trivially; the two are easy to confuse.

**Corrections made:**
- `analysis/w33_shannon_capacity.py`: correction block, and the false PASS line replaced.
- `papers/standalone/holonet_shannon_capacity.tex`: correction box.

**Prior art: BT818 already found this** (`analysis/BT818_ovoid_nogo_theta_gap.md`): "the 'Shannon Θ = 10 = α' claims collapse ... Θ is only bracketed: 7 ≤ Θ ≤ 10".
- This pass **cites** that correction and does not claim it.
- What is new here: the explicit false-lemma control above, **the lower bound √57 > 7**, and the corrections to the Pass 51 witness and paper, which BT818 had not edited.

**Still repeating the Shannon claim (not edited, shared documents):** `docs/COMPLETE_SUMMARY.md` ("Θ = α = 10"), `docs/w33_monster_landauer.html` ("independence number = Shannon capacity = 10"), `manuscripts/parts/PART_CCCCCXLIV_D_BASE_RESULTS.md` ("Θ = 10 ... tight") and `manuscripts/parts/PART_CCCI_LOVASZ_THETA_BRIDGE.md` ("ϑ = 10 = α").

**False positives of the search:** `w33_paper_body.tex`, `manuscripts/tex/part6_cascade_breakthroughs.tex` and `PART_MCXLI_*` use Θ for other quantities. The "capacity–contextuality identity Θ = 1/CF" in the Pass 51 file has no support.

### A2. Neutrino prediction against data (`analysis/2026-11-13_neutrino_prediction_vs_data.md`)

The no-AdS₃ window (Dirac, normal ordering, Σm_ν ∈ [58.8, 69.9] meV; Pass 12536):
- **Ordering:** normal ordering favoured at 2.1–3.1σ (JUNO plus long-baseline; global fit), so consistent.
- **Mass sum:** DESI DR2 under ΛCDM caps Σ at 64.2 meV (Bayesian, 95%), and the Feldman–Cousins bound of 53 meV excludes the window. That bound also excludes all of normal ordering.
- **Coupling between arcs:** with evolving dark energy (the repo's own preferred dark sector, Passes 12593–12628) the window is free. The neutrino arc and the dark-energy arc are therefore coupled.

### A3. The parallel assistant's TY(ℤ₃², hyp, +1/3) Hopf algebras (`w33_ty_hopf_isomorphism.py`)

- The JSON attachment was transcribed. All coefficients are ω^k, times 1/3 on M₃⊗M₃ terms; group terms were spot-checked.
- **Independent check:** both are Hopf algebras (multiplicativity over all 324 pairs, coassociativity, counit, grouplike unit, to 10⁻¹⁶).
- **Frobenius–Schur indicators** of the 3-dim irrep, ν₂…ν₉ = 1, 0, 1, 0, 3, 0, 1, 0, are **identical for H₊ and H₋** (exponent 6). The control ν_n(trivial) = 1 passes.
- (A first run gave different values from a transposed recursion. It was caught by the impossible exponent-5 pattern and fixed; the control was added.)
- **Prediction** (Tambara: the two fiber functors come from the ordered isotropic decompositions, exchanged by the χ-preserving swap): H₊ ≅ H₋. Isomorphism search: see A4.

### A4. Type B: the √ coupling is essential (`w33_typeB_coupled_margin.py`)

- min (e − 2 + 2√(xy)) = 2×10⁻¹⁰ ≥ 0: the theorem holds numerically and is tight.
- The stronger, cleaner candidate e − 2 + 2·min(x, y) ≥ 0 is **false** (minimum −1.858).

### A5. The two TY Hopf algebras are isomorphic (resolves the other track's caveat)

The exact candidate search over π ∈ Aut(ℤ₃²) (48) and U ∈ {I, F, F*}·(permutation)·(ω-phases) finds **36 Hopf isomorphisms H₊ → H₋** (residual < 10⁻¹⁰).
- The first is **π: (u, v) ↦ (v, u)**, exactly the χ-preserving swap of the two isotropic lines that Tambara's classification predicts, with U = F* (inverse 3×3 DFT): E ↦ F* E F.
- So the two fiber-functor reconstructions give **one** Hopf algebra up to isomorphism.
- Status: closed-form U, float-verified at 10⁻¹⁰. All entries lie in Q(ω)/3, so an exact check is routine but was not run.
