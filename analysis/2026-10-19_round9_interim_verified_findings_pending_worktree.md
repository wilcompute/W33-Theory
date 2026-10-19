# W33 Round 9 — five research fronts (interim verified-findings packet)

**Date:** 2026-10-19. **Status:** All five self-contained producer scripts were executed individually in the isolated Windows worktree and their built-in checks passed. The subsequent combined seven-test pytest run began, but the remote Windows machine stopped responding before its result could be read. The source scripts, full local technical report, five JSON certificates and regression file have **NOT** been transferred to GitHub. This interim report preserves checked results without inventing a final test or commit claim.

Baseline: W33 master after a34780b6a, incorporating parallel Passes 12066–12070. These cover two-clock Spin(8) triality and exact one-vs-three fixed E6 Yukawa weight monomials; those orbit results are prior work, not a Round 9 discovery.

## 1. Clifford-equivariant 1440-vacuum frame and no unique invariant onsite vacuum
Using the previous Round 8 construction of all 1440 rank-two two-qutrit stabilizer-pair projectors Q, explicitly calculated the 81-dimensional Hilbert–Schmidt frame matrix. Results:
- Sum over the 1440 Q equals 320 I9.
- Frame eigenvalues are 640 (one identity direction) and 28 (80 traceless directions).
- Centered Qc=Q-2I9/9 yields frame eigenvalues 0 (once), 28 (80 times).
- For every rank-two Q, Tr(Qc^4)=182/243.
- For one reference Q, Tr(QR) varies across the orbit; hence there are nontrivial invariant relative two-vacuum couplings.

Since the entire 1440-object discrete set is ONE projective Clifford orbit, any Clifford-invariant on-site scalar potential V(Q), of any degree, is CONSTANT on that orbit. A single vacuum cannot be uniquely chosen by such an invariant potential. Two-site interactions may select relative configurations but remain equivariant under simultaneous conjugation. This does not classify continuous SU9-conjugate vacua or derive a physical Higgs potential.

## 2. Exact analytical support-two phase theorem for any T>0
All 4860 projective noncommuting outcome-projector pairs P,Q satisfy PQP=P/3 (matrix residual ~9.3e-16). For normalized two-tick mixtures M=(1-w)P+wQ, u=w(1-w), the eigenvalues are lambda_plus/minus=(1±sqrt(1-8u/3))/2, each multiplicity three, plus zero multiplicity three. Therefore
F_T(u)=1-T log{3[1+2 exp(1/(2T)) cosh(sqrt(1-8u/3)/(2T))]},
and commutator interaction C=4u/3.

This F_T is CONVEX in u. To prove it, put a=8/3, x=sqrt(1-au), z=x/(2T), c=exp(-1/(2T))/2 in (0,1/2), g(z)=sinh(z)/[z(cosh(z)+c)]. Then F'_T(u)=a*g(z)/(8T) and
-z²(cosh(z)+c)² g'(z) =
(1-c)(sinh(z)cosh(z)-z)+c(cosh(z)+1)(sinh(z)-z) >= 0.
As z decreases in u, F'_T is increasing. It follows that single tick globally minimizes energy WITHIN every two-tick Pauli subspace iff
kappa >= -(3/2)*(1-exp(-1/T))/(3+6exp(-1/T)).
At T=0.5 this is -0.3402395316. The earlier rounds already derived the local derivative threshold and its full-simplex global-exclusion consequence; new here is a COMPLETE support-two convexity theorem. **Not** a proof of the full 120-rate global critical boundary.

## 3. Trinification E6 cubic and classical Jordan Spin8 triality
Independent tensor enumeration verifies that the three 3×3 trinification sectors A=(3,bar3,1), B=(1,3,bar3), C=(bar3,1,3) support det(A),det(B),det(C),Tr(ABC): 18 determinant monomials plus 27 cross monomials, 45 distinct cubic weight monomials. A specific relative combination is needed for the full E6 cubic.

Separately, the classical J3(O)=R³+O³ realization gives 27=1+1+1+8+8+8 and cubic
abc-a||v||²-b||w||²-c||z||²+2Re[(vw)z].
Explicit 8D Cayley–Dickson octonion multiplication passed norm and cyclic triality checks. Parallel Pass12067 ALREADY found one fixed E6 weight monomial for noncollinear two-clock pairs, three disjoint fixed ones for collinear pairs. Conditional bipartite Yukawa illustrations have rank one versus diagonal rank three, but a canonical W33 weight-to-octonion basis map and physical VEVs were **not** found. No Yukawa magnitudes or physical mass ratios follow.

## 4. Fully specified 36-setting single-photon complex optical tomography
The 18-mode path×internal-mode circuit can be interrogated with Uref=F3 tensor F3 in the reference path, whose 81 complex entries all have modulus 1/3. Prepare each input basis mode j=0..8, choose reference phases 0 and pi/2, and resolve 9 output modes in each path plus erasure. For unknown transfer T, the two measured differences satisfy
D_phi(k,j)=Re[exp(i phi)conj(Uref_kj)T_kj],
so T_kj=[D_0(k,j)-i D_pi/2(k,j)]/conj(Uref_kj).
Use separate identity-loop calibration R=M and signal-loop transfer S=MW; compute W=R^-1 S. There are 2×9×2=36 configurations with 19 outcomes each.

Synthetic 19-outcome multinomial simulations with coherent first-qutrit mode mixing and heterogeneous arm loss: 40,000 source photons/configuration (1,440,000 total/run), 120 repetitions, ideal deficit 8/27=0.296296..., sample mean ~0.296562, std ~0.004508. This is NOT an experiment or foundry-ready chip, and assumes a known reference matrix, stable phase gauge and ideal detectors aside from simulated erasure/count statistics. Phase drift causes calibration bias.

## 5. Exactly solvable S3-symmetric toy scalar threshold potential
For x_i=Tr(Phi_i†Phi_i)>=0 and V=-m²Σx_i+bΣx_i²+cΣ_{i<j}x_i x_j (m²,b>0,c>=0), rewrite V=-m²S+(b-c/2)Σx_i²+(c/2)S², S=Σx_i, and apply S²/3<=Σx_i²<=S². Global minimizers are:
- c<2b: x1=x2=x3=m²/[2(b+c)];
- c>2b: one x=m²/(2b), other two zero (three symmetry-related choices);
- c=2b: flat simplex Σx_i=m²/(2b).

Even the equal-condensate phase does not set threshold ratios unless Yukawa couplings y_i are separately fixed: M_i=y_i sqrt(x_i). Conditional one-loop bUV=9,bIR=11 model with y=(1,2,4) gives scale ratio 4^(2/11)≈1.286665 versus unity when y=(1,1,1). The potential is an illustrative radial symmetry-breaking model, NOT an E8(-24) fundamental action; no parameter-free particle mass was predicted.

## Provenance and outstanding upload
Local worktree: C:\tmp\w33_tick_frame_20261019 (separate from the dirty main checkout). Individually passed producer scripts and generated JSON files: analysis/w33_20261019_round9_vacuum_frame_potential.py, analysis/w33_20261019_round9_two_tick_convexity.py, analysis/w33_20261019_round9_triality_cubic_texture.py, analysis/w33_20261019_round9_photon_tomography_shots.py, analysis/w33_20261019_round9_symmetric_higgs_thresholds.py; corresponding JSON in data. Also created tests/test_w33_20261019_round9.py and a full report with round9 in analysis. The machine disconnected during the combined test run, before staging/committing any of those files. They MUST be recovered, tests inspected and run, then staged/committed from the isolated worktree when connectivity returns. Do not claim they are already on master.
