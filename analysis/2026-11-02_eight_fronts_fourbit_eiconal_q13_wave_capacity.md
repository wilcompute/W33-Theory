# 2026-11-02 local / November 3 UTC — eight new W33 fronts, exact falsifiers and photonic feasibility

> **Verification policy.** Mathematical exact identities, finite enumeration, numerical rank results, experimental assumptions and external prior art are distinguished throughout. None of these computations establish a theory of everything, a particle/force spectrum, quantum gravity, a physical vacuum, the measured value of c, or a calibrated optical experiment.

## Repository intake and parallel attribution

Initial local and GitHub HEAD: `31a40bf890a848607bda1f4a38c79167c639f436`. A concurrent update `fa513b2ad2dab9cd44f3c721e440eec2c407fdb4` added native postselected qutrit holonomy, Clifford/Yang-monopole controls, Klein/W(D5), quartic tunneling, and vacuum audits; none of our paths overlap. Local worktree contained preexisting modifications, preserved without reset or destructive checkout.

Previous exact 216-route POVM frame, 216/40 integer sign frame, positive 24D module, Naimark 4,884 Givens network, q9 seven-triple data and 24D invariant cubic basis are due to older `31a40bf89`, `9e0d5097`, `dd85b447` and their predecessors. The q13 weight-160 even line set and 0/2/4 histogram belong to parallel Pass12527. Prior TOE36/TOE35 already introduced square-root Laplacian waves on a different native Levi cover. This pass contributes exact new restrictions and controls, not a discovery claim for generic waves, Jordan cubics, Holevo limits or Wilson regulation.

Public research consulted before implementation:
- finite symplectic generalized quadrangle and incidence rank: de Caen–Moorhouse, [The p-rank of the Sp(4,p) GQ](https://www.ericmoorhouse.org/pub/sp4p.pdf)
- cubic norm structures and adjoint identity: [Albert algebras over Z and other rings](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/albert-algebras-over-mathbb-z-and-other-rings/12737A889070C49B9599490B96D089A4)
- complete eiconal cubic classification: Tkachev, [arXiv 1001.2387](https://arxiv.org/abs/1001.2387)
- quantum detection and Holevo capacity: [Preskill, Quantum Shannon Theory](https://ilorentz.org/quantumcomputers/literature/preskill_10.pdf)
- 2026 lattice fermions and overlap/Ginsparg–Wilson benchmark: [Phys Rev D 114,014511](https://doi.org/10.1103/756m-stz5), and [Nielsen–Ninomiya review](https://qft.org/lattice-hamiltonian/lattice-fermions-chirality/nielsen-ninomiya-obstruction/).

## Original next-step front 1 — GF(9) formal arithmetic

`lean/W33Q9ProjectiveSquareClass.lean` explicitly models the nine field elements as `a+b*i`, with `a,b in F3` and `i²=-1`, and states finite verification lemmas for associativity/distributivity/inverses, four nonzero squares and invariance of quadratic-character square status under a projective square multiplier. This is a **prerequisite**, not the complete q9 Witt-extension/classification proof. The existing `lean/W33Q9CubicClassArithmetic.lean` already kernel-verified the seven orbit-size and rational cubic checksum ledger. The new file was compiled successfully with Lean 4.32.0-rc1 in the authorized Windows checkout, with no errors in the final process output. This is not a full GF(9) orbit theorem.

## Original next-step front 2 — four-bit phase-only informational completeness

`analysis/w33_20261102_phase_signature_no_go_4bit.py` derives a general *analytic* collision theorem. With `n` modes, `m` phase settings including the reference, and `b`-bit phase shifters, each mode has a signature in `(Z/2^(b-1))^(m-1)`. Modes with identical signatures acquire only real relative phases in every setting. Each such pair contributes an independent invisible imaginary Hermitian coherence. Pigeonhole balanced class sizes give a minimum number of invisible pair directions, independently of what real-valued rank-one receiver is used.

For n=24 and m=3:
- b=2: at least 60 blind directions, rank <=516/576, **three settings can never be IC**.
- b=3: at least 8 blind directions, rank <=568/576, **three settings can never be IC**.
- b=4: no forced signature collision; numeric construction below reaches full rank.
- with b=2, at least SIX settings are required merely to avoid this pair-collision obstruction.

For 45 random injective four-bit phase-signature assignments (seed20261102), the best of the 24-mode 216-port receiver settings had minimum Hermitian-frame Gram eigenvalue **8.987376129419122e-6**, rank **576**, condition estimate **192.585**, versus prior seeded six-bit 1.990685e-6 and condition409.2. The complete two 24-entry masks are frozen in `data/w33_20261102_phase_signature_no_go_4bit.json`. Four-bit IC is *numerical*, whereas 2-/3-bit impossibility is a *theorem for any real receiver* with exactly three settings.

### Loss/stability model

`analysis/w33_20261102_fourbit_loss_fisher.py` projects the effect tensor onto the 575 trace-free Hermitian directions, explicitly includes each no-click detector outcome, and forms the local classical Fisher information at the maximally mixed input. In the 4-bit candidate:

| Port efficiency | Detected mean | CRB necessary launched shots per setting for weakest SD 0.01 |
|---|---:|---:|
| ideal | 1.0 | 5,151,259 |
| uniform | 0.70 | 7,358,941 |
| per-port uniform draw 0.35–0.90 | 0.6266 | 8,742,057 |

Calibrated phase noise of 0.01,0.05,0.1 radians further worsens the weakest Fisher eigenvalue, but the tested cases retain full rank. **CRB is a necessary asymptotic, local, unbiased-estimator constraint, not a sufficient finite-shot recovery guarantee.** Loss, dark counts and phase-calibration errors are not experimental measurements; nonuniform eta is synthetic. Real optical path-length and beam-splitter insertion losses remain open.

## Original next-step front 3 — exact obstruction for the full W33 invariant-cubic pencil

Earlier exact PSp4(3) Molien computation proved `dim (Sym³ V24*)^G=2`, with cubic basis `C_point=sum_i x_i³`, `C_route=sum_s (Z_s.x)³`; 24D carrier's positive inner product is unique up to scale as a G-invariant form. `analysis/w33_20261102_exact_eiconal_cubic_pencil_obstruction.py` tests **all** linear combinations `a C_point+b C_route` simultaneously.

For each integer x in the 24D module it computes the projected gradients of the two cubics in exact integer arithmetic, yielding a linear equation in `[a²,ab,b²,lambda]` if `|grad C(x)|²=lambda |x|⁴`. The first four sampled vectors give full rank with determinant

`-15535276243722783509857067335680000000000000000000`.

Therefore no nonzero cubic in that 2D invariant pencil satisfies the Euclidean cubic eiconal equation. By irreducibility, all invariant cubics are harmonic; Tkachev's classification independently excludes an irreducible eiconal Cartan cubic in real dimension24 (exceptional dimensions 5,8,14,26). This is **not a 27D Albert no-go**; restricting a genuine 27D norm to this 24D submodule need not itself solve the eiconal equation. The existing exact compact Albert algebra remains intact.

## Original next-step front 4 — q13 even-set arithmetic and systematic symplectic trades

**Crucial correction:** `NNᵀ=(q+1)I+A` implies every centered *line-incidence* column lies in the `q-1` point adjacency eigenspace, hence every centered line-subset coverage vector does too. The earlier q13 pure-positive observation is **generic**, not special to the 160-line frame orbit. The genuine new question is which positive-module integer lattice vectors come from even binary line selections with unusually low support.

`analysis/w33_20261102_q13_transvection_trades.py` reconstructs the parallel-origin 160-line set by a separate Klein map and tries its symmetric differences with `T_{a,c}` images, for ALL 2380 center points and c in {1,2,5}, **7140 distinct tests**. Every transformed 160-set is even. The maximum overlap in each family is **24**, so every tested nontrivial XOR has weight at least **272**, far above160. Negative local search, **not a global minimum proof**; arbitrary group words and mixing other codewords remain open.

Prior project Pass260 already computed binary rank `1275` at q13 and its general odd-prime rank law, so we do **not** claim a novel incidence binary-rank observation.

## Original next-step front 5 — exact isotropic native scalar wave, with physical boundary

`analysis/w33_20261102_exact_isotropic_3deck_scalar_wave.py` replaces the previously approximate Hessian of the W33 three-voltage normalized Laplacian with an **exact rational** result. The base point adjacency has spectrum 12,2,-4. On zero-sum edge dipoles, the Laplacian pseudoinverse is `Lplus=(21/20)I+(3/40)A`. For voltage edges (0,1),(2,3),(4,7), the dipoles are orthogonal under I and A, and their effective-resistance Gram is `(39/20)I3`. Rayleigh–Schrödinger expansion yields

`D = (67/38400)*I3`, **exact isotropy**, correcting the prior 1e-7 numerical anisotropy artifact.

For the freely specified local scalar action `S=integral dt[1/2 sum (partial_t phi_v)² -1/24 sum_edges(phi_v-phi_w)²]`, `omega(k)=sqrt(lambda0(k))=sqrt(67/38400)|k|+O(k³)`. Numerically tested directions up to |k|=.03 agree within 3.6e-5. This is an **acoustic scalar**, not a Dirac/Weyl fermion, universal physical c, or derived Lorentz dynamics; three voltage axes and choice of time action/coupling are external. Generic square-root waves were already in TOE36, credited accordingly.

## Three additional independent creative fronts

### Creative I — exact 2-/3-bit phase-mask impossibility theorem

The phase-signature pigeonhole obstruction above is a new general mathematical **no-go** with minimal number of settings. Unlike the earlier failed finite random samples, it rules out *all* three-setting two-/three-bit masks for any real receiver on 24 modes. A constructive four-bit numerical witness simultaneously establishes achievability at the first precision level not ruled out by this obstruction.

### Creative II — information capacity of the 216-channel, not number of detector outcomes

`analysis/w33_20261102_216_route_holevo_capacity.py` derives the exact classical matched frame prepare/measure channel `P(t|s)=(Z_s.Z_t)²/14400`. Per-input squared-overlap histogram is `16:100, 64:95, 256:20, 1600:1`, denominator14400. Each row is a permutation of every other row, and every column sums1; hence this is a weakly symmetric classical channel whose *capacity for the fixed 216 input frame-state alphabet and matching POVM* equals

**C = log2(216) - H(P(.|s)) = 0.9459792209213997 bits / detected photon**.

It does not exceed the general Holevo bound log2(24)=4.5849625007 bits per 24D quantum signal. The 216 detector address labels themselves have log2(216)≈7.755 bits of entropy under uniform outputs, which is not the mutual information about the prepared state. This fixed-channel capacity is **not** the full accessible-information maximum over arbitrary quantum ensembles and POVMs.

### Creative III — Euclidean eiconal full-pencil no-go, not just a failed example

The integer rank4 gradient witness rules out every linear combination of the two G-invariant cubics on the native 24D Euclidean module, providing an exact algebraic falsifier and shrinking what would count as a meaningful Jordan/Albert embedding. This rests on direct exact arithmetic; the Tkachev theorem supplies external corroboration.

## Regression and reproduction

Test `tests/test_w33_20261102_eight_fronts_fourbit_eiconal_q13_wave.py` checks frozen exact certificates, four-bit uniqueness and rank, the integer 4×4 obstruction determinant, q13 transvection histogram and weights, exact metric, weak-channel Shannon entropy and Holevo firewall, no-click Fisher inequality, and the presence of the GF9 formal proof obligations. The phase-mask producer uses 45 eigensolves; the q13 producer explores 7140 symplectic transforms. The full repository suite is not claimed tested.

## Five next independent research directions

1. Formalize all q9 symplectic projective triple transitivity / Witt extension and cubic averaging in Lean, beyond the GF9 arithmetic and class-count certificates.
2. Numerically optimize a whole practical 216-port optical architecture including mode loss, phase drift, detector dead time and statistically efficient reconstruction, not just a perfectly known frame.
3. Search 27D Albert frame-moving trace forms and adjoint-preserving restrictions, now constrained by the exact full two-cubic basis and Euclidean 24D eiconal obstruction.
4. Search q13 and higher-q binary even sets by deeper multi-transvection/group-word trades, integer programming or symmetry breaking; use rank/module data already in repo as prior art.
5. Seek physical 3+1D continuum and chirality without inserting spinors and dynamics; enforce observational predictions and no-go constraints rather than interpreting an engineered scalar acoustic cone as light.
