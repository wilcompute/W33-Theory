# TOE Round 37 — intrinsic chirality, finite Poincaré action, dynamical rank, wave flat bands and Maxwell normalization

Date: 2026-10-10. Repository: wilcompute/W33-Theory.

## Scope and prior art

Responds directly to Round36's five independent next-step challenges. Checked the latest W33 and Holotrade master histories before work. Passes 11854–11868 have ALREADY proved major chirality and Lorentz constraints: no Weyl spinor in the finite SL(2,9) Di carrier, no chirality from one E8 automorphism, unique Lorentz-invariant Majorana/B−L condensate yielding the standard-model compact stabilizer, and spinorial Lorentz × central colour triality Z3 has commutant su3+so5+u1. Round36 already built an EXTERNALLY imposed domain-wall chiral index, an abstract three-deck linear wave Hamiltonian and the 210.6σ bare alpha discrepancy. No result below claims to supersede those barriers.

In the Holotrade repo parallel work on K81 compiler carriers and frame/source provenance remains independent; no code from this pass belongs in its production model without an explicit operational requirement and independent tests. Other agents' worktrees are dirty: do not stage their changes.

## 1. Native chiral-index calculation: balanced W33 cannot make one Weyl generation

Producer: `analysis/w33_20261010_toe37_native_chiral_index.py`; frozen result `data/w33_20261010_toe37_native_chiral_index.json`.

Construct the exact 40×40 point–line incidence matrix F for the Levi graph W(3,3). Every row and column has degree4. Singular values: 4(1), √6(24), 0(15); real rank25. Both chiral sublattice sectors have 15 null vectors, and therefore **index dim ker F − dim ker F† = 15−15 = 0**. Independent finite-field rank over F3 and direct 80×160 gradient rank cross-check.

On a connected 80-vertex/160-edge Levi graph, H0=1, H1=81, Euler characteristic −80. Degree-p covers have Euler characteristic −80p. This **vertex/edge cochain Euler index is not a physical Weyl index**, despite the tempting abundance of flat bands. In particular it neither counts 80 generations nor selects 3.

This is a precise native-index obstruction for the unmodified point–line bipartite carrier. Round36's rectangular domain wall gets index1 by inserting a new unbalanced extra-dimensional boundary. Flux-index/orbifold models with new geometric structure remain possible, but no spontaneous native 16 or mirror removal follows.

## 2. Exact ABSTRACT full finite Poincaré group and a Heisenberg-extension obstruction

Producer: `analysis/w33_20261010_toe37_finite_translation_form_obstruction.py`; frozen result `data/w33_20261010_toe37_finite_translation_form_obstruction.json`.

Construct the A6 action on the 5D augmentation module `S={x∈F3^6:Σx=0}`, with central fixed constant vector c and nonsplit 4D quotient `M=S/<c>`. Calculate explicit 5×5 generator matrices, plus the 4×4 quotient matrices from the four 3-cycle generators of A6. The full spinorial double cover SL2(9) of order720 acts on S **through its A6 quotient**; its central order2 element acts trivially on translations, as required for Lorentz–momentum conjugation. This gives an exact abstract group

`G = F3^5 ⋊ SL2(9), |G| = 3^5×720 = 174,960`,

with fixed central translation subgroup C3; its quotient by C3 has 58,320 elements. The absence of invariant functionals on S re-establishes that the 4D Minkowski quotient has no equivariant 4D embedding as a subgroup of the chosen S.

**New compatibility test:** The 4D A6 quotient has nondegenerate symmetric Gram `I+J4` over F3. Solve ALL invariant alternating forms `GᵀΩG=Ω` for the four quotient generators, as a 6-unknown linear system over F3. Its constraint matrix has full rank6, so invariant alternating dimension **0**. Therefore an A6-compatible nonabelian class-two, exponent-three Heisenberg central extension of THIS M with centre acted on trivially cannot use a nonzero commutator `Λ²M→F3`. This does **not** contradict the existing abelian nonsplit central extension S, whose translations commute.

The group presentation is rigorous and explicit **as an abstract semidirect product**, not a 248-dimensional E8 matrix realization. Whether all its noncentral F3^4 momentum generators can be embedded in E8 while retaining hypercharge and the required chirality is STILL UNSOLVED. Central colour triality is only one element, never the entire translation group.

## 3. First quantum rank-changing toy Hamiltonian: choice is not intrinsic

Producer: `analysis/w33_20261010_toe37_quantum_graph_rank_selector.py`; frozen result `data/w33_20261010_toe37_quantum_graph_rank_selector.json`.

For three W33 Levi covers `Z3^r` with r=1,2,3 (240,720,2160 vertices), compute complete 80×80 Hermitian Bloch blocks and normalized Gaussian scalar determinant energy densities

`f_r(m)= (1/(2|V_r|)) Σ_{λ∈spec L_r} log(λ+m²)`.

Build and exactly diagonalize a Hermitian **rank-sector** 3×3 model

`H_rank = diag(f_r(m)+κr) − g(|1><2|+|2><1|+|2><3|+|3><2|)`.

This genuinely mixes the abstract rank sectors, unlike Round36's completely separate fixed-rank Hamiltonians. However the offdiagonal terms are **global topology-changing transitions inserted by hand**, not derived from microscopic local graph moves. With m=0.5, g=0.03 and κ=0, rank probabilities ≈(0.2520,0.5000,0.2481). Adding κ=+0.05 makes rank1 probability ~0.7776; κ=−0.05 makes rank3 probability ~0.7757. Other masses and g tested. Therefore a rank3 superposition/selection is model-parameter dependent; neither W33 itself nor scalar determinant forces a 3D vacuum. Normalization, scalar mass, quantum measure, counterterms, local moves and thermodynamic stability are all missing.

## 4. Removing 80 flat bands: a quantified locality–linearity conflict

Producer: `analysis/w33_20261010_toe37_flat_band_locality_tradeoff.py`; frozen result `data/w33_20261010_toe37_flat_band_locality_tradeoff.json`.

For Round36's three-deck Bloch gradient `B(k):C80→C160`, local Hamiltonian `H0=[0,B†;B,0]`, 80 edge null bands exist at generic k and acoustic modes have `E±=±sqrt(λ(k))~±|k|`. Test TWO remedies:

1. **Local edge onsite mass** `H_local=[0,B†;B,mI160]` moves 80 zero modes to E=m, but each acoustic pair changes to `E±=(m±sqrt(m²+4λ))/2`, and near zero momentum `E_−≈−λ/m~−k²`. Direct momentum halving gives |E(k)/E(k/2)|≈**3.9998**, rather than 2.
2. **Cycle-only mass** `H_project=[0,B†;B,m(I−P)]`, with `P=B(B†B)^−1B†`, shifts exactly the cycle null bands to E=m while preserving `E±=±sqrt λ` (halving ratio ≈**1.99995**). Numerical projector Hermiticity, idempotence and annihilation residuals <1e−8. Yet this P is ~**96.34% nonzero off-diagonal** across the 160 edge coordinates at tested k, hence is a long-range/nonlocal interaction. It is also singular/nonanalytic at the zero Bloch mode.

Consequently neither naive scheme simultaneously provides **locality, a cleared flat-band spectrum and relativistic z=1 acoustic propagation**. A genuine local gauge constraint with auxiliary fields or higher-dimensional physics is still needed. This is a two-mechanism obstruction, NOT a theorem against every future local completion.

## 5. Lattice U(1) gauge normalization: exact graph ratio but alpha remains free

Producer: `analysis/w33_20261010_toe37_maxwell_normalization_audit.py`; frozen result `data/w33_20261010_toe37_maxwell_normalization_audit.json`.

Build the 40-vertex W33 point adjacency A directly from the 40 Levi lines and confirm the SRG identity `A²=8I−2A+4J`. Graph Laplacian `L=12I−A` has spectrum `0(1),10(24),16(15)` and exact pseudoinverse

`L+ = (7/80)I+(1/160)A−(13/3200)J`.

Thus equal-resistor effective resistances are `R_adj=13/80`, `R_nonadj=7/40`, giving **ratio 13/14**. THESE exact effective resistances are **ALREADY known** in the repo (`analysis/w33_poisson_kemeny_green_kernel.py`); this script checks them independently rather than asserting novel prior art.

The physically important NEW boundary is an explicit normalization audit of the proposed Gaussian graph U(1) potential action:
`S(φ)=(κ/2)φᵀLφ−ρᵀφ`.
For neutral point charges ±1, integrating out φ gives pair action magnitude `R_pair/(2κ)`. κ is an arbitrary positive continuous gauge stiffness, not set by v,k,lambda,mu, the E8 decomposition or the QED beta function. Changing κ by factor ten changes the absolute pair energy by factor ten while preserving **all** graph topological identities and ratio13/14. No parameter-free physical `α(0)` or empirical Coulomb law follows.

An equal-conductance 40-node synthetic resistor network could verify this conditional shell ratio, but this is a classical graph test, NOT a measurement of QED coupling.

## Reproducibility discipline

Each producer accepts `run(write=False)` for side-effect-free regression evaluation. Frozen JSON certificates are preserved during tests. Exact group/rank/fraction values compare exactly; floating-point eigenvalues, eigenvectors, residual norms and probabilities compare recursively with explicit relative tolerance 1e−8 and absolute tolerance 1e−10, avoiding false divergences from BLAS execution-order rounding. All five Round37 focused tests pass under constrained BLAS threading. This is a numerical reproducibility improvement, not a changed mathematical or physics claim.

## Integrative verdict

- Native balanced graph index **0**, 15+15 exact point-line null modes: chirality needs a physically derived boundary/index, and Pass11864 rules out Weyl helicity for the original finite Lorentz Di carrier.
- Abstract finite-Poincaré presentation of order174960 is explicit, but embedding full translations INSIDE E8 is still open; the quadratic four-momentum module has **no invariant alternating form**, excluding a naive compatible Heisenberg commutator.
- Rank-sector quantum mixing can be written and diagonalized; vacuum rank is sensitive to externally imposed cost and topology-hopping, not derived from W33.
- Local edge mass clears flat bands only by collapsing z=1 to z=2, while precise cycle-only projected mass preserves z=1 but requires a dense coupling.
- Graph electric shell ratios are exact but already in the repo. Maxwell stiffness κ—and thus a physical coupling—remains unfixed without a true dynamical action and normalization.

**No experimental TOE, observed chiral fermion generations, real Lorentzian gravity, Standard Model couplings or physical photon has been derived.** These are five rigorous/controlled falsification and model-selection gates with numerical certificates and focused regression tests.
