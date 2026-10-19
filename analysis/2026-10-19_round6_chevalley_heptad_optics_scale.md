# W33 Theory — Five more independently executed research fronts (Round 6)
**Date: 19 October 2026.** Baseline: master with Pass 12059 + Pass 398 parallel commits. All experiments ran in the clean separate W33 worktree, not the modified user checkout. **Scientific status:** exact group/representation algebra and conditional finite-circuit computations, not a physical TOE proof, new experimentally established law, or built hardware.

## 1. E8 fermion matter-sector obstruction, alternatives and chemical-potential status
Prior repo Passes 11681, 11687–91, 11879–83 already construct sl9 + Lambda3(C9) + Lambda3(C9)* with dimensions 80+84+84 and discuss its quantum/geometric meaning.

**Exact branching under three block diagonal SU(3) factors:** choose C9=V_a+V_b+V_c, each V_i=C3. Then
Lambda3(C9)= (Lambda3 Va+Lambda3 Vb+Lambda3 Vc) + (Va tensor Vb tensor Vc) + sum_(i ne j) [Lambda2 Vi tensor Vj],
giving dimensions **3 +27+54=84**. Thus the three-fermion 84 decomposes into singlets, trinification matter, and six 9-dimensional tensor representations. The six 9s are **3bar_i tensor 3_j** (charged bifundamentals), *not* the nine-dimensional SU9 fundamental or nine independent globally selected one-particle modes.

**Central obstruction:** omega I9 in SU9 acts trivially on sl9, Lambda3, Lambda6, so the embedded gauge group factors through SU9/mu3; the SU9 fundamental 9 has nontrivial central character. It cannot be IDENTIFIED as one of these adjoint E8 modules. A full SU9 gauge lift or separately added matter multiplet is a consistent option, but would be an additional assumption. A broken gauge theory might contain restricted 9D sectors, but it must show selection, masses and coupling explicitly.

**Chemical potential:** The previous sign reversal of the *postulated* nine independent free-fermion modes at mu=0.5 is an exact theorem for the specified H=I-(P+Q)/2; not a spontaneously selected mu from E8. Both projector competitors have equal mean particle number at that mu, equal to 3+3/(1+exp(1/(2T))), tending to 3/9 at T->0 (NOT literal half filling). Shifting all orbital energies E->E+c and mu->mu+c leaves the grand partition unchanged, so the absolute value of mu is reference-dependent. A physical filling mechanism must fix mu relative to the Hamiltonian spectrum.

## 2. All 2,880 heptads, 27 Pauli-translation orbits, five EXACT characteristic-polynomial families
Starting from the 40 projective two-qutrit Paulis, construct five actual Clifford-generator permutations (F1, S1, CZ, SUM, SWAP). Breadth-first search from a noncommuting 7-clique reaches **all 2,880** maximal noncommuting seven-sets, proving one orbit under these generators. This transfers any uniform-weight spectral census of a fixed heptad to all 2,880, up to conjugation and outcome relabelling.

For one heptad (seven rank-three Pauli eigenspace ticks at each weight 1/7), enumerate **all 3^7=2,187 outcomes**. The 81 projective Pauli translations F3^4 act freely on outcome labels, forming **27 orbits of length 81**. The 27 translation classes coalesce into five spectral families with counts 81,162,486,486,972, or translation-orbit multiplicities 1,2,6,6,12. An independent exact Eisenstein-integer algorithm verifies the spectral separation: for every outcome sample of the 27 translation orbits, form M=21Q in Mat9(Z[omega]), omega²+omega+1=0. Exact integer-pair matrix multiplication computes Tr M^k for k=1,...,9; Newton identities then produce integer coefficients of charpoly(M). The 27 orbits group into exactly FIVE DISTINCT INTEGER polynomials with multiplicities 1,2,6,6,12. Since the translation operator acts by exact unitary conjugation, these fingerprints classify all 2187 assignments EXACTLY, and Clifford transitivity transfers this result across 2880 heptads. The explicit coefficients are in data/w33_20261019_round6_heptad_exact_charpoly.json.

**Remaining variational boundary:** all results here fix equal masses on seven mutually noncommuting points. They do not optimize masses continuously, prove seven-support optimal for any finite negative kappa, or exhaust all 40-point support types. Fixed-outcome k=0 is already known not to minimize all heptads.

## 3. Optical single-photon 18-mode machine: actual component-level unitary synthesis and loss control
Implement the earlier exact 18-mode unitary (H2 tensor I9) diag(I9,W)(H2 tensor I9), where a SINGLE photon carries path(2) x 9 spatial-waveguide labels. Internally W has four rank-three projector phase pulses, two G and two Gdag, with G=CZ(F3 tensor I3). **New explicit complex Givens construction:** F3 is decomposed into THREE SU2 two-mode rotations plus a diagonal three-mode phase block, with machine verified reconstruction at floating precision. Lift each SU2 across the three values of the other qutrit: **9 two-mode rotations per 9-mode G**. CZ has exactly four computational modes carrying nonzero phase.

An unoptimized conservative component budget for one W is **36 tunable two-mode couplers**, 36 Fourier diagonal-phase slots, 16 CZ nonzero phase slots, and 12 rank-three-projector phase slots, plus two path Hadamard couplers and two output paths (internal nine-mode detection/summing). Some phase elements could be combined or implemented statically; counts are logical upper bounds, NOT minimum hardware or a verified chip layout. The generic Clements universal nine-mode mesh uses 9*8/2=36 two-mode couplers for an arbitrary U9, while our structure uses 9 for one G. References: Reck et al. 1994, https://doi.org/10.1103/PhysRevLett.73.58; Clements et al., *Optica* 2016 https://doi.org/10.1364/OPTICA.3.001460.

**Exact unbalanced-arm loss correction:** If signal-arm intensity transmission is eta, reference arm loss-free, the unconditional port difference is sqrt(eta)*Re(W_jj); total click probability is (1+eta)/2. CONDITIONED on detecting the photon the difference is V Re(W_jj), with V=2sqrt(eta)/(1+eta). A W=I reference run cancels state-independent stationary V. If one neglects the visibility calibration, an ideal W=I would appear to have a false normalized deficit 1-V. This is analytically verified for eta values .2,.5,.75,.9,.99,1. Real losses may depend on input mode and time; optical source, chip, detectors, power and calibrated leakage have NOT been measured.

## 4. Normalized E8 Chevalley SIMPLE-ROOT GENERATORS in the repo's 248 elementary basis
Upgrade from Round5's 80->248 injection. Take existing Pass11681 E8 bracket with gamma=-1 and choose **eight Chevalley simple positive/negative generator pairs**: for i=0,...,6, e_i=E_(i,i+1), f_i=E_(i+1,i) in sl9; eighth e_7 is the dual-trivector basis element with support (0,1,2), f_7 is the NEGATIVE corresponding primal trivector. Define h_i=[e_i,f_i]. Verify in the existing full 248 algebra:
- [h_i,h_j]=0; [e_i,f_j]=delta_ij h_i; [h_i,e_j]=A_ij e_j and [h_i,f_j]=-A_ij f_j.
- Cartan A has diagonal 2, edges 0--1--...--6 with eighth vertex 7 attached to vertex 2, the **E8 Dynkin diagram** with determinant **1**.
- All Serre relations (ad e_i)^(1-A_ij) e_j=0 and corresponding negative relations vanish exactly in the elementary coordinate operations.
- Weyl reflection closure yields **240 roots**; iterative brackets construct **120 positive, 120 negative root vectors** and with eight Cartans give a full rank **248** spanning matrix.
- Maximum reported root-weight residual 2.22e-16; all checked Serre residuals 0.

**This IS a normalized simple-root Chevalley–Serre presentation and computational 248-dimensional coordinate generation in the existing repo algebra**, resolving part of the previous explicit normalization task. It is standard E8 mathematics applied constructively, not the discovery of E8 itself.

**Real-form firewall:** all generator coefficients can be chosen real; the existing Pass11681 real tensor algebra realizes SPLIT E8(8), Killing signature (+128,-120). The user's physically discussed E8(-24) has signature (+112,-136) and requires a DIFFERENT antilinear involution/twisted real structure. A complex algebra isomorphism does not automatically identify the two distinct real forms. The present test does not build a real-form-preserving intertwiner to E8(-24).

## 5. Exact physical-scale identifiability no-go (for the CURRENT finite Hamiltonian)
For any s>0, in the current dimensionless W33 rate model replace H->sH, temperature T->sT, interaction kappa->s*kappa, and physical time t->t/s. Then Gibbs weights and the propagator are unchanged:
\[
\exp[-sH/(sT)]=\exp[-H/T],\quad
F_{sT}(sH)=sF_T(H),\quad
\exp[-i(sH)(t/s)]=\exp[-iHt].
\]
The nine-mode fermionic grand potential also scales with (H,T,mu)->s(H,T,mu). Numerical checks across scaling factors .001 to 100 reproduce the invariances to <1e-10.

**Consequence:** W33 incidence counts (40,120,480), E8 Lie brackets, or normalized 8/27 interferometric contrasts by themselves cannot select a physical energy unit, a time unit, speed of light, Newton constant, Planck constant or particle mass. A dimensionful physical action or independently fixed standard of units is necessary. This is a conditional no-absolute-scale theorem for the PRESENT simple Hamiltonian, not a universal prohibition on dynamical dimensional transmutation, renormalization scales, boundary conditions, or new physical coupling terms.

The candidate parameter-free W33 echo prediction **8/27** and 240/540 incidence are already standard two-qutrit quantum mechanics, so NOT TOE-specific. No parameter-free novel fundamental-physics observable survived this round's hard test.

## Reproduction
- analysis/w33_20261019_round6_matter_lift_branch.py -> data/w33_20261019_round6_matter_lift_branch.json
- analysis/w33_20261019_round6_heptad_symmetry.py -> data/w33_20261019_round6_heptad_symmetry.json
- analysis/w33_20261019_round6_heptad_exact_charpoly.py -> data/w33_20261019_round6_heptad_exact_charpoly.json
- analysis/w33_20261019_round6_optics_component_budget.py -> data/w33_20261019_round6_optics_component_budget.json
- analysis/w33_20261019_round6_chevalley_realform.py -> data/w33_20261019_round6_chevalley_realform.json
- analysis/w33_20261019_round6_scale_nogo.py -> data/w33_20261019_round6_scale_nogo.json
- tests/test_w33_20261019_round6.py reproduces five independent checks.

**Summary:** rigorously classifies all equal-weight heptad EXACT characteristic polynomials via group transitivity, Eisenstein-integer traces and 27 translation orbits; constructs normalized E8 simple-root generators in existing repo 248; derives concrete nine-mode optical mesh budget and loss calibration; rules out free fundamental-nine matter under only the old E8 adjoint and absolute scales from only the current dimensionless rates. No device built and TOE remains unverified.
