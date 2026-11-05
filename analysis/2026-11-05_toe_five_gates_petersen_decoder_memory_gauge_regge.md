# Five TOE research gates + independent sixth: exact Witting/Petersen decoding, causal memory, connected gauge loops, and a 9-simplex Regge action

**2026-11-05 (New York time).** Baseline GitHub W33-Theory master commit 1adc8a0afdfd1a55e4c016a008e8b89507c367ba. All code ran in an isolated, preexisting clean remote Windows worktree. The main checkout's 57 existing dirty/uncommitted files were not modified. Distinguish mathematically reproducible toy-model statements, prior research and unsupported physical interpretation. There is NO new experimental result, derived Standard Model, Planck constant, photon time travel or Theory of Everything here.

## Priority, literature, and non-duplication

- **Existing**: the two-qutrit Pauli commutation W(3,3), the complex Witting 40 ququart rays, the SRG(40,12,2,4), and their association with E8 complexifications are prior art (Waegell/Aravind 2017, DOI 10.1016/j.physleta.2017.03.039; Vlasov 2022 arXiv:2210.15338 and Vlasov 2025 arXiv:2503.18431). The 440 nonorthogonal mixed states and class1 8-real-coordinate A5-covariant embedding were built in prior repo commit 8284ebbd9. The 30-versus-10 equal-single-copy-MI but unequal-collision issue was reported in 1adc8a0af.
- **CRITICAL older repo prior art located during novelty audit**: analysis/bt855_dark_sector_k5_complete.py ALREADY identifies a 10-object K5-duad Petersen quotient for dark charts; analysis/bt857_chirality_bookkeeping.py ALREADY treats A5 tetrad partitions and a Petersen schedule. The present computed A5/Petersen/spread mathematical structure is NOT claimed as an independently new abstract discovery. What THIS pass connects explicitly is the **particular 440 E8-root Born-probability decoder** (15 pairs of otherwise unusable contexts distinguish all440 labels; 30 other pairs leave 249 classes) and native A5-to-Witting physical operator certificate.
- **2026 actually measured Z2 loops**: Nature Physics October 2026, https://www.nature.com/articles/s41567-026-03400-6 , demonstrated Aharonov–Bohm interference with dynamical Z2 matter and flux on a trapped-ion hybrid processor. Our 2-loop Gauss simulation is NOT first experimental realization of matter/flux interference. Connected-loop charge/confinement prior art Domanti et al 2025 https://www.nature.com/articles/s42005-025-02284-x .
- **Quantum memory prior art**: Vieira/Ku/Budroni, PRR 2025 DOI https://doi.org/10.1103/r8lf-bb4p , warns EB channels alone do not force classical memory; Baecker et al PRR 2026 https://doi.org/10.1103/5bfc-znkj on operational quantum-memory witnesses. Our trusted qutrit intervention SWAP controls obey the required no-extra-quantum-bypass/reference assumptions.
- **Regge prior art**: Bahr/Dittrich https://arxiv.org/abs/0905.1670 proves curvature can break exact finite simplicial gauge and yield pseudo-constraints; Bahr/Dittrich Phys Rev D80 124030 (2009) on perfect action. Our Euclidean Hessian nulls do not derive the Lorentzian Einstein hypersurface-deformation algebra.
- **Measurement prior art**: classical Bhattacharyya likelihood-ratio Markov/union bounds, quantum Holevo and multiple-copy Chernoff discrimination; see Audenaert/Mosonyi/Verstraete JMP53 122205 (2012), DOI 10.1063/1.4768252. NO new information-theoretic theorem is claimed.

## Six reproducible producer/certificate pairs

Each source is analysis/toe_20261105_NAME.py and writes data/toe_20261105_NAME.json:

1. a5_tetrad_orbits_bhattacharyya
2. petersen_tetrad_duad_spread_certificate
3. readout_decoder_error_exponents_hardware_guard
4. quantum_memory_interventions_and_dimension_bound
5. two_connected_c4_gauge_matter_gauss
6. nine_simplex_regge_action_hessian_lorentz_diagnostic

Regression tests: tests/test_toe_20261105_six_falsifiable_fronts.py regenerates all producers and checks cross-front arithmetic, geometry, group actions, operational hypotheses, counterexamples and the deliberate Lorentzian failure. Existing older scripts and JSON are imported rather than copied. All outputs are deterministic.

## Front 1 and the sixth independent geometry: native A5 Petersen measurement schedule

Native class1 A5 inside PSp(4,3) has order60 and acts on actual 40 Witting orthogonal ququart tetrads with exact orbit sizes10 and30. The ten collision-prone tetrads are a SPREAD, partitioning all40 rays with one tetrad per ray. Every other tetrad intersects four distinct spread tetrads, one ray apiece.

Under the epsilon0.1 uniform 440-root ensemble, all forty tetrads have the same SINGLE-PHOTON mutual information, but the10 spread tetrads only generate109 distinct root conditional probability vectors each; thirty others generate440. All 45 UNORDERED PAIRS among the ten bad tetrads were tested, with settings known and each used with probability1/2. Exactly15 pairs yield440 distinguishable classes; the other30 pairs yield249 distinct classes. The 15 successful pairs form a 10-vertex 3-regular girth-five Petersen graph, isomorphic to KG(5,2), whose ten labels are unordered pairs of five objects and whose edges join disjoint pairs.

We computed actual isomorphism duad labels and checked all60 native A5 permutations coincide with all60 EVEN permutations of those five labels. This is an explicit operational extension of the older BT855/857 K5-duad/Petersen architecture, not a new group theorem. It yields a concrete 2-setting four-outcome root-label decoder, though not 8-real-parameter ququart tomography.

## Front 2: distinguishability and calibration, not just average information

The previous four-outcome SU4 basis maximized an empirical single-copy mutual-information objective and obtained ~25% higher average I(R;Y) than full Witting40, but it contains a pair with extremely similar conditional distributions. Using exact known 440-hypothesis IID models and ordinary maximum-likelihood decoding, for each true root i:

    P(error | i) <= Σ_{j≠i} [Σ_o sqrt(p_i(o)p_j(o))]^N
                 <= 439 * BCmax^N.

This is a VALID conservative SUFFICIENT budget for max_i P(error|i)<=.05 with exactly known state/POVM likelihoods; compare Fano's NECESSARY budget694 detected photons at epsilon.1:
- FULL Witting40: BCmax≈.99919232246, exponent≈.00080800389, sufficient11,238 DETECTED photons; at calibrated independent η=.85 with explicit no-click, sufficient13,222 INCIDENT photons; with .005 uniform background on detected 40 outcomes, sufficient11,353 detected.
- Previously optimized four-outcome basis: BCmax≈.99999778177, exponent≈.00000221823, sufficient4,093,456 DETECTED photons, or4,815,831 incident with independent η=.85.
- Seeded100-trial per-setting multinomial likelihood simulation at N700/12000 corroborates the operational contrast, but is NOT the proof or confidence bound. The large sufficient numbers are upper budgets, not optimized/necessary samples.

**Certified bounded systematic preparation drift:** for a four-rail state-preparation mesh of at most six 2-mode gates, each with independent-or-correlated unknown bounded mixing-angle and differential-phase deviation <=δ in absolute magnitude, ||Uactual−Uideal||op<=6*(2sin(δ/2)+2sin(δ/4)). Thus any ideal fixed POVM total-variation output changes by no more than this. If the classical eigenmode mixing probabilities are unchanged and analyzer ideal, requiring TWO such worst-case deviations < the Witting40 minimum root-root TV≈.03060712 gives SUFFICIENT δ<0.00170039575 radians. This is a deliberately pessimistic analytical guarantee, not a measured chip calibration tolerance. Source randomization errors, real detector drift, preparation mixing uncertainty, independently uncalibrated effects and correlated systematic errors must be separately modeled.

**Counterexample to a simplistic optimization objective:** higher AVERAGE one-copy information can be catastrophically worse for worst-pair repeated-message decoding. A two-setting Petersen scheme can cure exact collisions; its finite-shot worst-pair exponent must be optimized separately before calling it a practical implementation.

## Front 3: trusted time-intervention quantum-memory witness + storage dimension

The prior 27D qutrit R-S-E SWAP/storage/reset/SWAP memory simulation now includes SEVEN explicit trusted intermediate interventions on accessible S (identity, shift X, phase Z, qutrit Fourier, dephase, reset0, reset1). In the ideal model all leave restored R-S singlet fidelity1 when E stores the quantum input coherently. Classicalizing E by dephasing in the computational basis yields a separable reference-output state with F=1/3 under ALL interventions. Thirty-two seeded unrelated Haar measurement/dephasing bases for the environment also reach only F=1/3.

The standard Schmidt-number singlet bound for local dimension d3 is F<=m/3 for Schmidt number<=m. Therefore F>1/3 detects retained coherent quantum capacity; F>2/3 rules out an ONLY coherent memory bottleneck dimension2 (if no other quantum bypass); perfect F1 requires dimension>=3. With a qutrit depolarizing storage coherence p, previous exact F=(1+8p)/9, so F>2/3 iff p>5/8. Independent heralding-loss and exact binomial threshold at p.6, η=.85 are imported from the prior verified process. This is a trusted, synthetic experiment, not device-independent, retrocausal, or a single-photon cosmology claim. Classical adversaries with unmonitored quantum bypass, initial reference-environment correlations or adversarial detection may invalidate the inference.

## Front 4: connected two-plaquette Z2 matter+gauge sector and full-network barrier

Two four-vertex loops joined by a bridge comprise 8 sites, 9 edge qubits, two cycles. Include one coherent moving Z2 charge and a static compensating charge at vertex0. Raw Hilbert dimension8*512=4096. The exact +1 Gauss-invariant 32D subspace is built from 128-element gauge orbits; link-dressed matter hopping, both Wilson loops and all nine electric X terms preserve it, verified by the exact projected operator identity H Q = Q Hphys. A naked hopping term on any link leaks OUT of the physical subspace: thus appending ungauged same-sheet E8 root graph adjacency to a locally gauged model is invalid.

At J1, g=0 and K=0, two Wilson-flux sector ground kinetic energies are:
 (W1,W2)=(+,+): −2.34292; (+,−) or (−,+): −sqrt5≈−2.23607; (−,−): −2.
Connected matter dynamics again favors ZERO flux, not π flux; no desired topological sign was manufactured.

Minimal chain-of-120 squares with119 bridges has480 sites,599 edges,120 independent cycle holonomies. Its single mobile-charge gauge-invariant Hilbert dimension is480*2^120. This is NOT a full 480-root E8 hopping/gauge field Hamiltonian; it is a rigorous lower-complexity bottleneck/connected scaffold. More gauge-invariant graph links introduce further cycles. Need tensor-network or controlled effective theory, not naive exact diagonalization. Prior art includes actual 2026 ion hardware loop AB measurement.

## Front 5: true nine-simplex boundary Regge action and Lorentzian branch FAIL

Build nested Euclidean 4D 1->5 then 1->5 (nine nondegenerate four-simplices, two interior coordinate vertices, ten variable interior squared lengths, twenty internal triangle hinges, ten original boundary triangles). Compute actual inverse-Gram dihedral angles and hinge areas. The STANDARD boundary-complete Euclidean action is

    S_E = Σ_internal A_h(2π−Σ_simp θ_sh) + Σ_boundary A_h(π−Σ_simp θ_sh).

At flat embedding S_E exactly agrees with the original outer boundary simplex action S0=3π/2+4πsqrt3/3, and the interior hinge deficits/gradient vanish. The ten-by-ten numerical Hessian has EIGHT tiny eigenvalues (max absolute <~0.0001 with 5e-6 finite-difference step) aligned with the rank-eight two-interior-point coordinate-motion Jacobian, plus TWO positive finite eigenvalues ~48.45 and~244.07. Perturbing a normal edge-square mode gives nonzero deficit and Hessian response; numeric analytic Schlaefli hinge-force gradient agrees with finite differences within declared tolerance.

**Important triangulation pitfall:** changing nested interior coordinates too far can put the second nominal interior vertex OUTSIDE the subdivided parent simplex. All Gram matrices might still look Euclidean while the simplices overlap rather than tile the region, producing artificial hinge deficits. The flat-motion controls keep both vertices inside their parent and pass. This is an embedding/triangulation-validity condition.

The Lorentzian reference-subtracted complex principal-arccos/square-root continuation was separately evaluated on the same nine-simplex incidence with causal signature (-+++). Its flat-action finite-difference gradient has norm approximately **26.95566**, NONZERO, thus the naive principal branch is NOT a valid stationary Lorentzian gravity action. We store this failure explicitly; do NOT interpret its value as physical curvature. A causal time-oriented Lorentzian dihedral/boost and boundary term treatment, Regge momenta, and a genuine first-class ADM/Hamiltonian-momentum bracket remain unsolved. Neither the Euclidean 8 null modes nor the configuration-space interval constraints prove full GR or TOE.

## Five orthogonal research gates after this audit

1. Use the native five-duad/Petersen labeling to derive an analytical exact 440-root collision-class formula and evaluate/adaptively improve the two-setting finite-shot worst-pair error exponent.
2. Calibrate an actual four-rail ququart interferometer and mixed eigenmode source to an *empirical*, rather than simulated/adversarial theoretical, phase/detector/source error budget. Distinguish 40-effect tomography from four-output projective decoding.
3. Specify a real trusted reference-and-intervention process tensor experiment, prove dimension-adversary exclusion under a stated no-bypass and detection model, and report an experiment-specific witness threshold.
4. Derive a gauge-invariant **effective** many-loop E8 two-sheet Hamiltonian in a reduced Wilson-loop tensor-network formulation, then try to reverse or falsify the recurrent zero-flux kinetic preference with a justified microscopic interaction.
5. Implement causal Lorentzian Regge boost orientations and boundary action so that BOTH flat action gradient and vertex-motion Ward identities vanish on the nested nine-simplex complex. Only then compute nonlinear off-flat canonical brackets, without claiming a first-class result prematurely.

**Physics firewall**: Actual published optical/gauge experiments and historical geometry are distinguished from this project's code. Every numerical statement is conditional on the model and reproducible by the six producer scripts; none implies new particles, Planck units, time travel, gravity unification, or established physical reality of a single self-entangled photon.
