# W33 Round 14: microscopic pair currents, certified phase band, D5 Lie generators, detector calibration, three-generation flux anomaly

**19 October 2026.** Five independent research fronts, extending Round13 with latest parallel Passes 12081–12085. Work conducted only in clean isolated research worktree. Main checkout with local modifications left untouched. Explicitly separate certified finite mathematical results, engineered couplings, partially compatible representations, calibrated literature, and proposed phenomenology.

## 1. Exact stable pair-current bosons CAN favor mixed vacuum weights (but are not a fundamental W33 interaction)

Round13: stable one-body auxiliary Hermitian matrix X induced an attractive *overlap* kernel that favors a concentrated vacuum. Round14 constructs an independently specified alternative, with a family of pair-labelled traceless Hermitian bosons X_ab coupled to Hermitian commutator currents j_ab=i[Qa,Qb] between two rank-two W33-derived discrete vacuum projectors. Let weights w_a>=0 sum to 1, m²>0 and real g. Specify

V[X,w] = (m²/2) sum_(a<b) Tr X_ab² - g sum_(a<b) w_a w_b Tr(X_ab j_ab).

Complete each square. Its unique stable X minimum yields exactly

Veff(w) = -(g²/2m²) sum_(a<b) (w_a w_b)² ||[Qa,Qb]||²_F.

This interaction is bounded below on the finite weight simplex and strictly favors SOME two-vacuum mixtures over pure singleton states: for balanced weights 1/2,1/2 on a noncommuting pair, Veff = -(g²/32m²)||[Qa,Qb]||²_F <0, while a singleton gives zero. The field action has positive Gaussian mass; its NEGATIVE induced sign comes from integrating out the sourced field. **Not** the same as bilinear κ C(w), however: it is a fourth-order weight interaction and requires a potentially extensive set of independently engineered pair fields. No actual bosonic mediator or fundamental interactions are derived.

Round10/11's 17 orbital reference types yield nonnegative commutator norms with rational values. Insert the coefficients of the symmetric commutator kernel Σ_i c_i A_i into the three EXACT rational M2 representations from Round12. Compute and store each resulting 2×2 matrix and symbolic eigenvalues. These spectra classify this invariant kernel's block action but do not fix physical masses nor distinguish all seventeen pair classes. If one wants a state-dependent selecting theory, derive why these fields exist, how they transform under the full gauge group, and why their couplings have this normalization.

Producer and JSON: analysis/w33_20261019_round14_pair_current_mediator.py, data/w33_20261019_round14_pair_current_mediator.json.

## 2. Major new EXACT PHASE certificate: entire T in [0.95,1.30]

Round12 proved at T=1 (rational cyclotomic Pauli representation) that a fixed rational seven-tick state beats singleton at the exact two-tick local coupling κ_local(T). Round13 extended this to the tiny interval [0.9999,1.0001]. Round14 proves a MUCH WIDER entire continuous temperature band **[19/20,13/10]=[0.95,1.30]** by finite rational arithmetic and a Lipschitz bridge.

Construct each two-qutrit Pauli rank3 projector exactly over Q(ω) with ω²+ω+1=0, using 18×18 rational blocks for each ω. The fixed seven heptad has point indices [0,23,27,28,34,36,39], labels [2,2,2,1,2,0,1], six rates 1473/10000 and one 1162/10000. All seven are pairwise noncommuting. Compute exactly Tr(Q^n), n=0,...,18; Tr exp(Q/T) has a lower bound by its positive Taylor terms for Q positive. Obtain exact rational lower/upper exp(1/T) via Taylor plus geometric tail. κ_local(T)=-(exp(1/T)-1)/[2(exp(1/T)+2)] is decreasing in exp(1/T), so bound it from above by the rational lower exp bound. Then degree-four Taylor of exp(κ_upper C/T) (negative argument) is an exact upper bound. Compare exact rational lower partition ratio and obtain a rigorous energy advantage lower bound at every grid midpoint.

The band is partitioned into **1750 equal intervals** of width 1/5000, from 0.95 to 1.30. At every midpoint, the exact lower energy advantage is greater than the worst interval drift given by the universal Gibbs entropy bound |d(Fsingle-Fseven)/dT|<=ln9<3 and |κ'_local|<2: halfwidth*(3+2C). The minimum exact certified positive margin INCLUDING coverage for all interior continuum T is **0.00017243546265**. Certificate stores all rational trace moments, minimum margin as exact fraction, grid count, and checks.

Conclusion: at EVERY T in [0.95,1.30], the local TWO-TICK singleton threshold is not the global transition; this fixed seven-point configuration has strictly lower energy. Still do NOT know true GLOBAL 120-variable critical κ, or whether the seven-tick state is globally optimal. This finite nine-dimensional Gibbs functional has no thermodynamic singularity. User's physical negative κ remains to be derived.

Producer and JSON: analysis/w33_20261019_round14_phase_grid_certificate.py, matching JSON.

## 3. EXACT 40 D5 root generators, with FAILED E6 cubic compatibility identified

Parallel Pass12076 identified three D5=so(10) root subsets in E6 (40 roots each) and Round13 transported their 1+10+16 U1 branch projectors into first Tits coordinates by the exact octonionic 27x27 cubic map T. Round14 constructs a **complete abstract D5 Lie representation** on that 27-vector decomposition:

Take 5 canonical fermionic creation/annihilation operators a†_i,a_i satisfying CAR on Fock space Λ C^5 (dim32). Even-degree spinor space Λeven C^5 has dimension 16. The 40 root operators are 20 a†_i a_j (i !=j), 10 a†_i a†_j (i<j), 10 a_j a_i (i<j), and 5 Cartans H_i=a†_i a_i -1/2. The 10-vector representation is C^5⊕(C^5)* with the action induced by their canonical commutators. Form block 1⊕10⊕16 and conjugate all 40 root generator matrices through the exact invertible Round12 Tits-octonion basis T. Their root weights, CAR, and opposite-root [E_alpha,E_-alpha]=H_alpha relations hold exactly; the entire 40×27×27 sparse matrix data is stored.

**CRUCIAL NEGATIVE FINDING:** A priori matching the vector 10 and spinor 16 coordinate orders to the Peirce octonion chart is *not* a cubic-compatible embedding. Explicit infinitesimal cubic tests give dN_Tits(x + t G x)/dt|_0 !=0 for the first four naive generators. Therefore these matrices are a rigorously valid 27-dimensional representation of the **abstract** D5 Lie algebra but are NOT certified as the specific Pass12076 D5 subalgebra of E6. An additional blockwise triality-compatible 10/16 basis alignment is required. This is a successful diagnostic/falsification of a premature embedding claim. No clock/tick equivariant identification is permitted (Pass12072 no-go).

Producer and JSON: analysis/w33_20261019_round14_so10_chevalley_transport.py, matching JSON.

## 4. A detailed response-matrix and recovery-time detector calibration specification

Published detector references: SNSPD review https://doi.org/10.1088/0953-2048/25/6/063001 explains kinetic-inductance dead time; a September 2026 experiment https://doi.org/10.1364/optcon.609425 describes loss-swept coherent-state calibration of parallel photon-number-resolving SNSPDs. Their equipment is NOT our photonic architecture.

Model 18 physical path×mode detector outputs plus one erasure outcome with an explicit **19×19 column-stochastic response matrix** R. Use openly hypothetical 75–98% channel efficiencies and 1% nearest-neighbour crosstalk; erasure absorbs missed events. Verify positivity, normalization, invertibility, condition number ≈2.11031, and covariance propagation R^-1 [diag(p_observed)-p_observed p_observed^T] (R^-1)^T/N. An actual machine must separately measure R, crosstalk and uncertainty for all physical channels. Record source power, detector recovery, phase reference and full counts including no-clicks, not just normalized surviving clicks.

Analyze a nonparalyzable recovery-time scenario: at 1 MHz pulse rate and perfect equal port sharing, 50 ns dead time produces ~0.277% throughput loss; if every pulse hits one hot detector, same dead time produces ~4.762% loss. Thus mode-selective readout can invalidate a calibration based on uniform port occupancy. Dead times 10,50,100,250 ns are *design assumptions*, not documented values for our 18 channels.

Practical acceptance plan: interleave calibration R, W33 loop S and commuting null N across 54 input-phase settings; acquire phase-reversed loop, electronics-sham and source-blocked dark controls; loss sweep each detector, independently measure 19×19 response and its uncertainty, estimate nonlinearity/recovery and include calibration covariance in final effect significance. No actual device constructed or measured; this is a reproducible calibration specification, not experimental validation.

Producer and JSON: analysis/w33_20261019_round14_optical_calibration_matrix.py, matching JSON.

## 5. Torus-flux index M=3: conditional three complete families versus ANOMALOUS internal flux

Classical Atiyah-Singer magnetic torus result: a 6D Weyl fermion of U1 charge q in T² flux M has net 4D chiral Dirac index qM under appropriate boundary assumptions; M=+3 gives 3 chiral zero modes for charge+1. Source: https://academic.oup.com/ptep/article/2024/5/053B06/7667937 , equations (23)-(26), and earlier magnetized orbifold literature. This INDEX THEOREM is established prior art and not proved by code.

Apply to E6 27 → SO10×U1: (16_+1,10_-2,1_+4). If M=3 is flux of this **internal GUT U1**, the chiral net multiplicities are **(3,-6,12)**, not three complete 27s. Four-dimensional residual gauge-anomaly coefficients become nonzero:
 gravitational-U1=216, U1³=1296, SO10²U1=18 (with twice-Dynkin indices (2,1,0)). Hence the simplest internal GUT U1 flux leaves an anomalous net 4D spectrum without additional sectors, inflow or Green-Schwarz cancellation. This is a concrete obstruction, not a self-consistent three-family theory.

Alternative: introduce an EXTERNAL flavor U1_F under which the entire E6 27 has uniform +1 charge and background M=3. Then all SO10×U1_E6 sectors receive three net chiral zero modes (3,3,3), preserving the usual SO10×U1_E6 anomaly cancellations *per complete 27*. BUT gauging U1_F itself yields mixed gravitational and cubic U1_F anomalies 81 each, so the full 4D/6D model needs anomaly inflow/spectator matter or treat U1_F as nondynamical. A 6D UV completion has not been constructed.

Finally **M=3 is inserted**, not derived from W33 q=3. The coincidence of two '3's is not a physical explanation. Orbifold projections, Higgsing, zero-mode localization, bulk anomaly and Yukawa overlaps remain unverified. This is an exact index/anomaly firewall identifying what an honest three-family mechanism must solve.

Producer and JSON: analysis/w33_20261019_round14_magnetic_three_generation.py, matching JSON.

## Evidence firewall

Five independent numerical/exact test producers + one regression suite, one detailed report, five JSON certificates. Exact: finite group operator construction, trace rational phase inequalities, CAR/D5 commutators, gauge charge anomaly sums, calibrated linear-response algebra. Conditional: Gaussian pair-labelled mediator, torus-index assumptions, detector efficiencies. Not established: physical TOE, global transition critical curve, real E6 cubic-compatible SO10 root generators, three family mechanism selected by dynamics, actual 18-channel device.
