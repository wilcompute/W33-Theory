# Five TOE research fronts and a sixth spectral breakthrough
Date: November 4, 2026 UTC. Baseline: W33-Theory master 2f3791d0db5f594e7831b18b3eebdc4a4fc289f7. Computed on an isolated Windows worktree, preserving all 57 pre-existing dirty files in the main checkout. All claims are mathematical or controlled quantum/numerical models; none establishes an experimental or complete Theory of Everything.

## Source and priority audit

- Prior repo Pass999, analysis/w33_pass999_a5_double_class_census.py, already PROVES that PSp4(3) has exactly two A5 conjugacy classes (216 each) and both have W33 point orbits of sizes 20+20. Pass982 corrects a false A5 edge-orbit claim. Earlier W33 group automorphism order 51840 and PSp(4,3) 25920 are classical and repo-confirmed.
- Earlier repo analysis/w33_20260829_pg34_subgroup_zero_split.py treats S5/A5 40x45 permutation modules, not the current 25 packet to 40 W33 adjacency embedding. The A5-duad intertwiner is also an existing different construction. Crucially, Pass1000 (analysis/w33_pass1000_a5_signed_turn_spectral_fingerprint.py) ALREADY distinguished the two A5 classes by the signed-turn 240-edge operator; the present 25-packet versus W33 25D adjacency spectral compatibility is a DIFFERENT concrete class discriminator, not the first spectral class separation.
- Prior commit 6816ebb73 constructed the 25x60 Reye packet-to-600cell-axis rank17 map, its 8D A4+A4 kernel, and two E8 index-five glues. Commit 2f3791d0d proved the full-H4-to-W33 graph action obstruction and the 120 C4 intersheet Wilson flux models.
- Tomotope original paper: Monson/Pellicer/Williams (2012), https://bmonson.ext.unb.ca/fields/tom.pdf ; H4 and 25 inscribed 24cells: Denney et al, https://arxiv.org/abs/1912.06156 . Classical E8 lattice and icosian overlaps are not novel here.
- Di Pietra et al, Temporal Entanglement and Witnesses of Nonclassicality, Physical Review Letters accepted October 21 2026, https://journals.aps.org/prl/accepted/10.1103/h1rh-cld4 ; Vieira/Ku/Budroni, Entanglement-breaking channels are a quantum memory resource (2025), https://doi.org/10.1103/r8lf-bb4p . Temporal process witnesses require explicit operational assumptions.
- Prior photonic AB cages: PRL 121 075502 (2018), https://pubmed.ncbi.nlm.nih.gov/30169066/ ; recent time-bin postselection and loophole review https://www.nature.com/articles/s41534-025-01072-3 . Four-mode signed flux interference is established, not newly discovered physical effect.
- Dynamical Z2 lattice gauge and Elitzur theorem are standard, see lecture https://davidtong.org/pdfs/teaching/gauge-theory/gauge4.pdf .
- Lorentzian Regge dihedral branch/causal irregularity is discussed at https://doi.org/10.1088/1361-6382/ad37e9 . Earlier constraint problem Bahr/Dittrich https://arxiv.org/abs/0905.1670 and Galassi PRD47,3254 (1993). Our 4D branch control is NOT the full boundary action or canonical ADM brackets.

## Reproduce (each source produces matching data JSON)

1. analysis/toe_20261104_actual_a5_w33_25_to40_intertwiner.py
2. analysis/toe_20261104_a5_w33_spectral_25_embedding_criterion.py
3. analysis/toe_20261104_three_time_qutrit_process_tensor_witness.py
4. analysis/toe_20261104_two_e8_sheet_dynamical_z2_gauge.py
5. analysis/toe_20261104_fourrail_givens_drift_detector_validation.py
6. analysis/toe_20261104_lorentzian_four_simplex_deficit_branch_falsifier.py

All have corresponding data/toe_20261104_*.json certificates. Main regression tests/test_toe_20261104_actual_a5_temporal_gauge_hardware_lorentz.py; also rerun predecessor tests from commits 6816ebb73, 2f3791d0d and tomotope.

## Front 1: actual reduced A5 intertwiner on genuine W33 point labels

Full H4 25-packet symmetry is (A5xA5):C2 order7200, which cannot act faithfully on the W33 40-point graph, since the 3600 normal base cannot inject into W33 Aut order51840 (no factor25). Restrict to diagonal A5 of simultaneous permutations of the 5x5 packet grid.

Source A5 on 25 positions decomposes into diagonal 5 and offdiagonal20 transitive orbits. Both genuine PSp4(3) A5 classes on W33 40 vertices decompose as 20+20. Rebuild BOTH classes from actual F3^4 symplectic points, construct their five A4 overgroups and label each native 20-point orbit as ordered pairs(i,j) with i unequal j via a three-element stabilizer. Define real 40x25 map F by |i,j> to first-orbit point |i,j> if i!=j and |i,i> to (sum over j!=i of |i,j> in second orbit)/2. Check F^T F=I25 and rho40(g)F=F rho25(g) for ALL 60 group elements, both classes. A5-equivariant deterministic set mapping is impossible for source diagonal five-set into target20-set (A4 stabilizer order12 cannot lie in C3 order3).

Negative dynamic check: neither simple F has W33 adjacency-invariant image; squared leakage Frobenius is 75 for class0, 60 class1. The existence of an A5-equivariant isometric vector map does not imply physical W33 adjacency closure. These are 40 real point-label amplitudes, NOT a four-dimensional ququart Hilbert state.

## EXTRA major theorem: first A5 class has a unique 25-dimensional spectral-compatible representation type

W33 collinearity adjacency spectrum is 12(1),2(24),-4(15). Native exact rational spectral projectors are P12=J/40, P2=(40I+10A-4J)/60 and P-4=(32I-16A+4J)/96. Compute actual A5 class characters by summing projector matrix elements along permutations of all60 group elements.

Source 25 module has complex A5 irreducible multiplicities: 1:2, 3:1, 3prime:1, 4:3, 5:1. For actual class0, the W33 12+2 eigenspace has EXACTLY this module and hence admits an A5-equivariant 25D unitary equivalence. For class1, the same W33 spectral subspace has 1:1,3:1,3prime:1,4:2,5:2; only rank20 intertwiner possible. Thus the two classes, which had identical orbit-size profiles, are distinguished by actual adjacency spectral characters.

Projecting the preceding F onto the target spectral25 had rank21 for class0, so a character match alone did not make THAT map successful. Group-average a seeded generic 40x25 real operator over all60 actual A5 actions, project to P12+P2 and polar-normalize. For class0 this yields an explicitly stored full-rank 40x25 real isometric intertwiner W, closed under native W33 adjacency; for class1 rank20 only. Within source 2D trivial-isotypic multiplicity, make an A5-invariant Householder alignment so uniform packet amplitude maps exactly to W33 eigenvalue12 all-ones eigenvector. This alignment is a chosen basis, not canonical physics.

Most important: the E8-related eight-dimensional A4+A4 kernel of the exact 25x60 packet-axis incidence, represented by f(i,j)=u_i+v_j with both row/column sums zero, embeds under W entirely in the W33 eigenvalue2 eigenspace. This is a genuine matrix eigenspace inclusion, not a numerical 8-count coincidence. Transport source row/column swap S, which exchanges the two E8 glues, as Q=W S W^T+(I−WW^T) on W33 point amplitudes. Q is orthogonal, Q^2=I, [Q,A]=0, has +1 multiplicity30 and -1 multiplicity10, and is NOT a graph permutation. This spectral operator route is consistent with the previous no-faithful-full-H4 graph action theorem. It is NOT an identification of 240 E8 root Hilbert states or a physical four-mode Witting operation.

## Front 2: three-time qutrit Markov process, Choi witness, interventions and loss

Construct two depolarizing qutrit channels E_t(rho)=t rho+(1−t)Tr(rho)I/3 with two internal links and three time slices. Explicitly build their 9x9 normalized Choi matrices, valid 81x81 Markov two-link product comb, input marginals I/3, and four interventions at middle time: identity, cyclic unitary, dephase and reprepare|0>. Per-link negativity max(0,(4t−1)/3); end-to-end identity composition negativity max(0,(4t^2−1)/3). At t=.45 each segment retains Choi entanglement, but end-to-end is entanglement-breaking. At t=.6 end-to-end entangled. Dephase and reprepare destroy end-to-end Choi entanglement for all test t.

A trusted ancilla-referenced qutrit Choi singlet fidelity F>1/3 excludes entanglement-breaking transmission; full process tomography and trusted reference are required. At loss eta each link, both-link survival eta^2, and naive unconditioned witness thresholds become invalid if silently postselecting. A memoryless quantum Markov process can have temporally entangled links; this proves neither exotic time travel nor self-entangled single-photon universe. Literature indicates EB alone does not define every form of classical temporal memory.

## Front 3: real dynamical Z2 Gauss system and sheet-selection no-go

Four qubit-valued links on a C4 have Wilson B=Z0Z1Z2Z3, local Gv=X_prev X_next and H=−K B−g sum_e X_e. All [H,Gv]=0. Projecting Gauss Gv=+1 gives a two-dimensional physical Hilbert sector per isolated plaquette. Its eigenvalues are +/-sqrt(K^2+16g^2), gap2sqrt(K^2+16g^2), and ground Wilson expectation K/sqrt(K^2+16g^2). At nonzero g, Wilson flux not pinned exactly +/-1; gauge-odd link Z expectations vanish. The 120 disconnected C4s yield a tensor product of 120 two-level physical sectors, not a derived 4D gauge continuum.

A separate pair-of-glues qubit Hsheet=−Delta X−hZ has unbiased symmetric ground at h0 and Delta>0, with <Z>=0 and unique ground; explicit h breaks the sheet swap, while Delta=h=0 is degenerate. There is no finite-volume spontaneous selection and no dynamical derivation of uniform pi flux without an assumed sign(K) or frustration. No Elitzur-violating physical order parameter was asserted.

## Front 4: four-rail optical U(4) gate compiler with detector and quasi-static drift

For signed zero/π square use U=exp(−itH), t=π/2. Both exact complex 4x4 unitaries compile into SIX two-mode Givens gates plus diagonal phases (max reconstruction error under1e−12); serialized real+imag U2 blocks are stored. Perturb independently each gate mixing angle and differential phase with Gaussian sigma0,.005,.02,.05,.1 radians, held STATIC during each optical run. For each sigma scan 512 fixed-seed configurations. Assume detector efficiency eta=.85, dark-click probability .005, uniform loss rate gamma=.1 and pclick=dark+(1−dark)eta exp(−gamma*t)p_rail.

The minimum sampled zero-flux click probability remains above the maximum sampled pi-flux probability in every scan. Using WORST OBSERVED static calibration probabilities and exact binomial tails with nominal one-sided five-sigma target, required trial counts are [22,22,22,29,46] for the five sigmas. Those are NOT confidence-certified bounds for all real calibration errors; fixed miscalibration across shots invalidates any model averaging independent photons over calibration draws. A separate detector calculation applies the same readout to the previous exact Lindblad dephasing/loss output, without multiplying loss twice. No actual photonic measurements have been performed.

## Front 5: genuine Lorentzian 4D hinge and branch falsifier

Use four-dimensional Minkowski metric eta=diag(-1,1,1,1), boundary vertices 0,(2,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1), and interior barycenter (.4,.2,.2,.2). The 1-to-5 subdivision creates five signature(-+++) 4-simplices with individual coordinate volume1/60, summing to original1/12. Its ten interior triangles comprise seven timelike and three spacelike hinges.

The five squared intervals s_i between interior vertex and boundary vertices satisfy exactly C(s)=s0+T^2−X2^2−X3^2−X4^2=0 where T=(s1−s0+4)/4 and Xi=(1−si+s0)/2 for i=2,3,4. Its gradient annihilates the 4D rank-four vertex-motion Jacobian; genuine interior translations preserve zero curvature.

Naive principal-complex-arccos dihedral angle branches give spurious flat-space boost deficit magnitude 1.3169578969 on three spacelike hinges even though the entire triangulation lies in one flat Minkowski chart. A compatible choice of oriented branches for THIS explicit simplex cancels all deficits. Perturbing the squared intervals normal to C(s)=0 while preserving all child (-+++) signatures produces nonzero rotation and boost deficits; all numerical amplitudes and implicit residuals are saved.

This is NOT a complete Lorentzian Regge action: the flat-branch prescription is embedding-specific; correct boundary terms, globally causal analytic continuation, multiple interior vertices and canonical nonlinear lapse/shift algebra remain undone. Literature stresses branch and light-cone irregularity, https://doi.org/10.1088/1361-6382/ad37e9 . No Einstein field equation or first-class gravity demonstration is claimed.

## Five independent top next steps

1. Move from one class-specific 25-to-40 real spectral intertwiner to an explicitly CPTP, phase-compatible four-dimensional Witting ququart encoding, or derive a new no-go using Pauli commutator/Gram constraints.
2. Design an ancilla-assisted single-photon three-time intervention experiment with a witness that excludes a well-defined classical memory model, including heralding and no-click outcomes.
3. Couple the dynamical Z2 plaquette gauge fields to actual coherent 240-root photon hopping, derive flux and sheet choice from an action, and test gauge-invariant finite-volume signatures.
4. Convert the six U2 gates into calibrated hardware-native components and derive a finite-shot confidence criterion with measured systematic uncertainty rather than using worst of 512 simulated draws.
5. Implement a fully time-oriented Lorentzian Regge boundary action on a multi-interior-vertex causal triangulation and test nonperturbative canonical Hamiltonian/momentum constraint brackets.

**Claims firewall:** All mathematical statements above are finite constructions or ideal models with explicit tests, not empirical Standard Model parameters, spacetime gravity, experimentally demonstrated temporal self-entanglement, or a completed TOE.
