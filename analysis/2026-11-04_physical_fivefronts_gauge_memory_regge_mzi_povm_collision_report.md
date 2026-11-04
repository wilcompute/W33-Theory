# Six falsifiable fronts: E8/W33 ququart hardware, measurement, temporal memory, Z2 matter gauge, and Lorentzian two-vertex geometry

**November 4, 2026 UTC.** Baseline W33-Theory commit 8284ebbd99209aff3f447884ee7bf03c8199d252. Executed on an isolated Windows Git worktree without altering the main checkout's 57 pre-existing uncommitted changes. This report records finite exact arithmetic, quantum toy models, and simulations, NOT a complete Theory of Everything or measured physics.

## Research sources and novelty boundaries

- The Witting 40 ququart rays, their W33 graph, and E8 complexification connections are established in Waegell/Aravind (2017) DOI 10.1016/j.physleta.2017.03.039; Vlasov (2022) arxiv:2210.15338 and Vlasov (2025) arxiv:2503.18431. Previous repo commit 8284ebbd9 already builds the specific 440 E8-derived physical mixed ququart codebook. This round tests and corrects its physical-readout assumptions.
- Reck (1994) and Clements (2016) universal four-mode photonic beam-splitter decompositions are classical: https://github.com/clementsw/interferometer . Calibrated 8x8 photonic processors exist (Nature Photonics 2026, https://www.nature.com/articles/s41566-026-01997-x). There is no fabricated chip in this research.
- Vieira/Ku/Budroni (2025), https://doi.org/10.1103/r8lf-bb4p , show that an entanglement-breaking channel alone does NOT identify classical memory. The new witness requires a trusted ancilla/reference, trusted intermediate reset and an explicit no-quantum-bypass condition.
- Kogut-Susskind Gauss-law lattice gauge models and Wilson plaquettes are established (https://pmc.ncbi.nlm.nih.gov/articles/PMC11999872/ and https://pmc.ncbi.nlm.nih.gov/articles/PMC8886423/). Elementary four-site Aharonov-Bohm matter kinetic energy depends on flux; this is not a new fundamental interaction.
- Flat/discrete Lorentzian Regge kinematics, canonical constraints and curved Regge pseudo-constraints are established: Bahr/Dittrich https://arxiv.org/abs/0905.1670 ; Dittrich/Hohn https://doi.org/10.1088/0264-9381/27/15/155001 ; Borissova/Dittrich https://arxiv.org/abs/2303.07367 .

## Reproducible code and frozen certificates

1. analysis/toe_20261104_witting_mixed_state_mzi_preparation_controls.py and corresponding data/*.json
2. analysis/toe_20261104_ququart_povm_local_unitary_optimizer.py and corresponding data/*.json
3. analysis/toe_20261104_reset_immune_quantum_memory_falsifier.py and corresponding data/*.json
4. analysis/toe_20261104_matter_dynamical_z2_flux_competition.py and corresponding data/*.json
5. analysis/toe_20261104_two_interior_vertex_lorentzian_regge_kinematics.py and corresponding data/*.json
6. analysis/toe_20261104_single_tetrad_440_decode_collision_nogo.py and corresponding data/*.json
- Regression: tests/test_toe_20261104_physical_fivefronts_and_readout_no_go.py . The six JSON certificates use exactly the .py stems in data/.

## 1. Real ququart optical compilation and randomized mixed-state source

Import the ACTUAL four native W33 A5-class unitary generators from prior tested certificates, compile each 4x4 into exactly SIX two-mode complex Givens plus phases, verify complex reconstruction residual under 1e-11 and verify order3/order5 modulo scalar phase.

For all 440 E8-root-derived full-rank mixed ququart states at both epsilon=.1 and .2, find eigendecomposition rho=V diag(w) Vdagger. Compile every V into at most six complex two-mode gates. The source must CLASSICALLY RANDOMIZE among the four input eigenmodes according to w, or use an ancillary state and partial trace: a passive four-mode unitary alone on a fixed PURE input CANNOT produce mixed rho. All 880 reconstructions pass under 1e-11.

Simulate independent STATIC Gaussian mixing-angle and phase drift across each mesh; for sixteen signed-axis preparations I4/4 +/- .1 O_j, 128 calibration draws per state and sigma=0,.005,.02,.05,.1, mean total-variation deviation of Witting40 readout is approximately 0, 0.000676, 0.002725, 0.006758, 0.013409. These are finite Monte Carlo envelopes, not calibrated hardware tolerances. The Witting40 POVM itself needs a suitable larger-effect analyzer, whereas a four-output tetrad is an ordinary 4x4 projective readout.

## 2. Fifteen-parameter SU4 measurement optimization and a sixth no-go

Optimize the uniform 440-label classical mutual information over a LOCAL 15-real-parameter SU4 Hermitian exponential chart around the best of the previously tested 320 seeded Haar bases, with two independent restarts and verified Udagger U=I. Results:
- epsilon=.1: Witting40 0.01161775728 bits/detected photon, Haar-best 0.01443977804, local winner 0.01454879693 (25.23% better than Witting). Ensemble-specific Holevo bound 0.05906012870.
- epsilon=.2: Witting40 0.04748117086, Haar-best 0.05938471748, local winner 0.05985714468 (26.07% better than Witting). Neither winner is proved globally optimal; general nonprojective POVMs are not optimized.
- All candidates' actual complex 4x4 bases, iteration counts, unitarity and comparison against the Holevo bound are saved.

**Extra hard result: single-shot information is NOT infinite-copy identifiability.** Prior round showed all 40 Witting orthogonal tetrads have the SAME one-copy mutual information about a uniform 440-root label as the full Witting40 POVM. But their actual 440-by-4 probability tables reveal:
- 30 fixed tetrads yield all 440 distinct distributions. Their smallest total-variation separation can be as low as approximately 0.00015653, much below the full Witting40 minimum ~0.030607.
- 10 fixed tetrads yield only 109 distinct distributions, with exact probability-equivalence class histogram: 20 singleton classes, 64 triples, 24 ninefold classes and one 12-fold class (20+192+216+12=440).
- Even with INFINITE independent samples from one of those 10 tetrads, the best uniform-prior root-identification success is at most 109/440=24.7727%. The other 30 tetrads and the sampled generic basis are injective on 440 FINITE labels, but any one four-outcome basis has at most three independent REAL output probabilities, and cannot continuously tomograph all eight E8 packet parameters. Full Witting40 tomography has rank8.

Therefore equal single-shot mutual information does not guarantee a usable repeated-label decoder. Both the collision families and the arbitrarily small gaps within nominally injective bases are hardware design blockers requiring a separate error-exponent objective.

## 3. Three-time quantum memory with an intermediate entanglement-breaking RESET

Prepare a qutrit reference R maximally entangled with system S; environment memory E starts |0>. Apply SWAP(S,E), then a TRUSTED entanglement-breaking reset on S to |0>, then SWAP(S,E) again. A coherent quantum E retains and later restores the original reference-output singlet (F=1). A dephased classical E yields separable reference/output correlation with F=1/3, and an environmentless Markov reset yields F=1/9. Depolarizing E_p yields F=(1+8p)/9 and negativity max(0,(4p-1)/3); NPT precisely p>1/4.

The script implements full 27x27 R/S/E states and partial traces and exact binomial comparisons under state-independent herald efficiency eta in [.6,.85,1]. Trusted no-click is assigned to a random qutrit output, giving unconditioned effective F=eta F+(1-eta)/9 and null separable upper bound eta/3+(1-eta)/9. An untrusted quantum bypass, state-dependent detector acceptance, or untrusted ancilla invalidates the classical-memory conclusion. THIS IS STANDARD quantum-memory physics in a tested three-time architecture, NOT retrocausality or photon self-entanglement.

## 4. One coherent charged matter particle changes the plaquette vacuum preference

For each of the previously derived 120 inter-E8 four-cycles, construct a local 4-node Z2 gauge-matter toy: one mobile charge, four two-level link fields, and a compensating fixed background charge at v0. Total raw dimension 4*16=64; exact local Gauss generators G_v=(-1)^(n_v+delta_v0) X_(v-1)X_v leave an 8D physical sector. The gauge-covariant hopping -J sum_v (|v+1><v|+h.c.)Z_v commutes exactly with Gauss, as do -K B and -g sum X where B=product(Z links).

At g=0 the matter spectra are:
- zero Wilson flux B+1: (-2J,0,0,2J);
- pi Wilson flux B-1: (-sqrt2 J,-sqrt2 J,sqrt2 J,sqrt2 J).

Thus matter hopping at J>0 and K=0 energetically prefers ZERO flux by (2-sqrt2)J. Pi wins only when an imposed negative magnetic K crosses K_c=-(2-sqrt2)J/2, about -0.292893 J, under this particular one-excitation model. Electric mixing g>0 does not commute with Wilson B and generically unpins its expectation.

This is a useful NEGATIVE prediction for the project: the model does not spontaneously generate the previously desired uniform pi flux. A different sign of K, frustrated connections or other matter content must be derived from independent physics. The full 480-mode E8 root adjacency coupled to ALL 120 local link fields is not yet implemented.

## 5. Two-interior-vertex Lorentzian 4D triangulation, kinematics versus true GR

Start with a 4D flat Minkowski 4-simplex (metric diag(-1,1,1,1)). Insert its barycenter c and then the barycenter b of one resulting child. The nested Pachner 1-to-5 refinements yield 9 Lorentzian-signature 4-simplices, 20 interior triangle hinges, and total coordinate 4-volume 1/12. There are 10 interior squared lengths (five from c, five from b) but only 8 interior coordinate DOF.

Explicit Lorentzian Gram inversion gives two independent rational flat-embedding relations C_c=0 and C_b=0. The geometric 10x8 internal-edge Jacobian has rank8; the two normal constraint gradients are independent (rank2) and annihilate all eight flat vertex-motion directions. All nine child Gram matrices have signature (-+++); off-flat normal squared-length perturbations violate the flat relations without violating simplex signature.

CRUCIAL: these two are CONFIGURATION-SPACE flat interval constraints, not ADM lapse, shift or nonlinear first-class Dirac constraints. A Poisson bracket of functions only of lengths vanishes tautologically, and would NOT prove Einstein gravity. A complete causal Regge boundary action, conjugate momenta, curvature solutions and nonlinear brackets remain unconstructed, even though the computational kinematics now involves TWO genuinely independent interior vertices. Prior broken-symmetry Regge literature cautions against conflating this with gravitational dynamics.

## Five independent next research gates

1. Build and calibrate a real four-rail photonic device for mixed-state classical eigenmode randomization plus native A5 U4 generators, including measured phase drift, source coherence and full POVM readout.
2. Optimize actual 440-root multi-copy root-label classification error exponent with a finite-shot decoder, compare one injected tetrad vs a sequence of bases and robustly bound the ten 109-class failures.
3. Extend the trusted three-time SWAP memory experiment to an explicit process tensor with independent interventions and a quantified classical hidden-memory adversary under detector loss and bypass constraints.
4. Couple a many-body 240+240 E8 root-network Hamiltonian to all 120 gauge plaquettes and derive, rather than stipulate, the sign of the magnetic/kinetic competition and its continuum relevance.
5. Build the actual causal two-interior Lorentzian Regge action with correct boundary terms and calculate nonlinear Hamiltonian/momentum Poisson brackets off flat space, looking for a genuine first-class algebra OR a decisive no-go.

**Claim firewall:** No physical experiment has been performed, and there is no completed TOE, Standard Model prediction or Einstein-equation derivation. The exact flux threshold and ten collision-prone tetrads are finite-model diagnostics, not newly discovered laws of nature.
