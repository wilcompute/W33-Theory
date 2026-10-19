# Round 8 — Five W33/TOE research fronts, exact finite witnesses and physical no-go boundaries
**19 October 2026.** Worktree isolated from dirty main checkout. Baseline includes previous commit 33621aaa7 and parallel Passes 12061–12065 (two-clock selection, Spin8 matter branch) plus Pass398 freezes. These parallel results were read and credited. Status: exact finite geometry / analytical local stability, numerical finite quantum dynamics / optical noise. **NOT a physical TOE, fabricated device, or new independently measured fundamental constant.**

## 1. REAL-FORM VACUUM: full discrete Clifford orbit, not just five generator checks
Previous round constructed sigma_24 from D=diag(1^7,-1^2) in SU9, with 136 compact and 112 noncompact generators, compatible with the repository's prior Pass10949 E8(-24) identification.

**Exact classification of Clifford-compatible D vacua (within discrete stabilizer-state rank-two planes):** The two negative eigendirections of D are two computational-basis stabilizer rays. There are 40 maximal two-qutrit commuting Pauli contexts, each with nine orthogonal rank-one stabilizer projectors. Choosing an unordered pair yields 40*C(9,2)=**1,440** possible rank-two marked planes. Construct all 360 stabilizer-state rank-one projectors from commuting Pauli context intersections, compute the five concrete Clifford generator permutations F1,S1,CZ,SUM,SWAP on these 360 states, and BFS their induced action on 1,440 pairs. All 1,440 are reached from one seed: the group is transitive on this discrete orbit.

The projective 2-qutrit Clifford group has order 3^4*|Sp(4,3)|=81*51840=**4,199,040**, hence the stabilizer of this D-defined real form within it has order 4199040/1440=**2,916**. Its Pauli translation subgroup has order **9**; the remaining stabilizer quotient has order 324 (equivalently, 3^5*12=2,916 from diagonal quadratic phases and affine pair stabilizer). The previously tested five named gates preserve D only for S1 and CZ individually; many OTHER Cliffords in the generated group do preserve the same plane. The full complex Clifford group relates these 1,440 vacuum REAL-STRUCTURE CHOICES, not all elements preserve one choice.

**Important scope:** the 1,440 are discrete stabilizer-ray-pair involutions. Continuous SU9 conjugates of D are uncountably many and not classified here. This is group-theoretic vacuum selection, not a vacuum potential / observed rest-frame selection. Prior latest Pass12061–65 reports two-clock observer and Spin8 triality branching on a DIFFERENT clock-pair geometry; no claim those 1,440 vacua equal its observer set.

## 2. NEGATIVE-KAPPA: exact all-T instability criterion narrows the global phase interval
The earlier paper already computed the one-sided **local singleton threshold**. Here we make the stronger **global noncommutation consequence** explicit, using the previously proved global Gibbs lower bound on all C=0 states.

Let u=exp(-1/T), Pa and Pb rank-3 Pauli outcomes from distinct NONCOMMUTING W33 points. For Q_e=(1-e)Pa+ePb, C(e)=(4/3)e(1-e), and F_T(Q_e)=-T log Tr exp[-(I-Q_e)/T], the exact one-sided derivative at e=0 is
\[
\frac{d}{de}(F_T+\kappa C)\Big|_{0+}=
\frac{2(1-u)}{3+6u}+\frac43\kappa.
\]
So if
\[
\boxed{\kappa<\kappa_{\rm inst}(T):=-\frac32\frac{1-e^{-1/T}}{3+6e^{-1/T}}},
\]
an arbitrarily small *feasible two-tick perturbation* beats the singleton. Every C=0 state has free energy at least the singleton (global majorization theorem), so every GLOBAL minimizer must have C>0. This is an exact theorem for all T>0, NOT merely a sampled optimizer or a claim of heptad global optimality.

At T=.5: **noncommuting phase is necessary for kappa< -0.3402395316212**; earlier global singleton sufficient bound remains kappa>=-0.233732552702. The open interval between is smaller than before. All five equal-weight heptad spectral representatives also fail first-order stationarity at T=.5, so assuming an equal-weight seven-clique is a finite-kappa stationary solution is false for those representatives. Numerical SLSQP (7 continuous masses x five outcome classes) provides feasible trial energies, but NOT certified stationary/global minima.

**Optimizer-independent rational witness:** at T=.5, choose heptad points [0,4,5,9,24,27,30], outcome labels [0,0,1,0,0,2,1], mass 9/10 on point 9 and 1/60 on each other point. This rational state has C=0.12555555556 and F~-0.625757759; for kappa=-.35 its E=-0.66970220344 versus singleton -0.66907852744. The exact fixed-state crossing formula is kappa=(F_single-F_state)/C≈-0.345032669. These decimals are numerical but gaps are stable; exact derivative theorem above does NOT require trusting this optimizer.

**Open:** exact global critical boundary, complete 40-mass solution, order of transition, W33-specific physical value or sign of kappa.

## 3. CHIRAL MATTER: all Cartan-descendant anomaly coefficients from a standard trinification 27
Against the new parallel Pass12064 cubic/Spin8 branch, independently decompose the conventional
27=(3,bar3,1)+(bar3,1,3)+(1,3,bar3)
under SU3_C x SU2_L x SU2_R x U1_L x U1_R, with generator Q=diag(1,1,-2) on each SU3 fundamental (negative on antifundamental). Enumerate all 27 field components and compute exact INTEGER local anomaly coefficients:
- gravitational-U1_L and gravitational-U1_R =0;
- cubic U1_L³, U1_R³, mixed U1_L² U1_R and U1_L U1_R² =0;
- SU3_C² U1, SU2_L² U1, SU2_R² U1 (for each of L,R) =0, with doubled fundamental Dynkin index normalization;
- exactly six Weyl SU2_L doublets and six SU2_R doublets, both even, passing mod-2 Witten consistency under standard restrictions.
The mixed quadratic trace Tr QL QR=0 too.

The gauge-invariant **cubic tensor structure** admits one cross-sector trilinear contraction plus a determinant of each of the three bifundamental 3x3 blocks, four algebraically independent cubic structures. However their **Yukawa COEFFICIENTS, Higgs vacuum alignment and masses are NOT fixed** by W33 or the representation. Arbitrary linear combinations of U1_L and U1_R remain locally anomaly-free as descendants of the full SU3³ 27, so no unique observed hypercharge assignment follows from this certificate. This does not check the full E8 gauged matter theory, anomaly inflow or the physical Standard Model spectrum.

## 4. OPTICAL COHERENT CROSS-TALK: diagnostic failure and full 9x9 transfer-tomography remedy
Previous single-photon 18-mode optics packet corrected stationary DIAGONAL post-loop losses with nine scalar references. But a physically plausible coherent output mixing M invalidates that formula. Model signal-arm M(ε)=exp[i ε H] diag(ell_0...ell_8) with amp transmissions .68...96 and H coupling neighbouring first-qutrit rails (j ↔ j+3) with phase-graded complex Hermitian amplitudes. Reference arm uses I.

For input mode j, measured path port difference in the ideal balanced interferometer is Re (M W)_jj, and the identity calibration returns Re M_jj. The nine scalar ratios are generally NOT Re W_jj when M has offdiagonal elements. In sampled coherent mixing eps=0,.03,.09,.16,.30 rad, scalar-reference biases in inferred normalized W33 echo reached about **-0.01517** at .30.

**Full-complex 9x9 transfer tomography remedy (ideal model):** independently measure complex R=M and S=M W with coherent phase-stable references and input/output mode rotations, then reconstruct W=R^-1 S. All five noiseless cases recover the loop to floating accuracy; a commuting null likewise remains zero. Monte Carlo includes 300 independent additive complex-transfer-noise trials per noise level; drift between calibration and data shifts the inferred result and is NOT fixed by inverting a stale R. This assumes complex transfer matrices can be determined experimentally and the optical reference gauge is stable. No device, phase-space photon-count proof, or component layout for every tomography rotation was built.

## 5. GAUGE COUPLING NO-GO: equal E8 kinetic normalization is not a parameter-free mass ratio
An E8 simple Lie algebra determines its invariant symmetric bilinear form only UP TO an overall scalar. Even in normalized Chevalley coordinates, a gauge kinetic action S=(4g²)^-1 K(F,F) has an additional positive coefficient g^-2 not selected by structure constants or finite W33 incidence. In the normalized convention, UV g0 is free unless a separate physical boundary condition fixes it.

For the conditional standard asymptotically free SU3 toy action, above a charged-matter threshold M take b_UV=9 (three Dirac flavors), and below it b_IR=11 (none). One-loop matching yields
\[
\Lambda_{\rm IR}
=M^{\,1-b_{\rm UV}/b_{\rm IR}}\Lambda_{\rm UV}^{\,b_{\rm UV}/b_{\rm IR}}.
\]
So if a unified E8-breaking hypothesis supplies three IDENTICAL UV couplings and identical beta functions ABOVE their thresholds, but the **threshold masses differ**, the ratio is
\[
\Lambda_{\rm IR}^{(a)}/\Lambda_{\rm IR}^{(b)}
=(M_a/M_b)^{\,2/11}.
\]
For M_a/M_b=10^6 the IR scale ratio is **12.328467...**, despite equal UV couplings. This is a conditional demonstration that geometry alone does NOT predict a unique dimensionless mass ratio without thresholds and Yukawa data.

This is a one-loop theoretical toy example, not the true E8(-24) noncompact gauge action, and does not establish absence of ghosts, a quantum UV completion, SM masses, a real QCD parameter or physics beyond standard QFT. More dynamics would be necessary to fix coefficients.

## Reproducible artifacts
- analysis/w33_20261019_round8_clifford_vacuum_orbit.py -> data/w33_20261019_round8_clifford_vacuum_orbit.json
- analysis/w33_20261019_round8_exact_local_instability.py -> data/w33_20261019_round8_exact_local_instability.json
- analysis/w33_20261019_round8_phase_stationarity.py -> data/w33_20261019_round8_phase_stationarity.json
- analysis/w33_20261019_round8_matter_anomaly_cartan.py -> data/w33_20261019_round8_matter_anomaly_cartan.json
- analysis/w33_20261019_round8_optics_crosstalk_tomography.py -> data/w33_20261019_round8_optics_crosstalk_tomography.json
- analysis/w33_20261019_round8_rg_threshold_nogo.py -> data/w33_20261019_round8_rg_threshold_nogo.json
- tests/test_w33_20261019_round8.py

**Evidence ledger:** analytic theorem: all-T local instability implies global exclusion of C=0. Exact finite group orbit: 1440 D vacua, 2916 stabilizer. Exact integer anomalies: 27 field components. Synthetic optical transfer and optimized feasible masses: numerical examples, not measured physics. Fundamental energy scales and Yukawas: OPEN.
