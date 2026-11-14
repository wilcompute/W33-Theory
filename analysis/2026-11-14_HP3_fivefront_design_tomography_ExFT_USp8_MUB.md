# 2026-11-14 — Five-front continuation: HP3 3-design, optimal hidden-qubit readout, all 288 ExFT sections, symplectic state preparation, MUB rank audit

## Scope and latest source priority

This pass starts from master 12a42f196d95b60eeac0bd9dd945fdd0fd74d8e5 and incorporates the later Pass 12669 reservation d96d66c8 (unrelated Shannon-capacity frontier). It checks against previous commits: Pass 12668's 1,080-to-180 fibers, Pass 12654's completed MUB size8 no-go, 2026-11-13 ExFT affine/quadratic closure, our 180-charge cubic cubature, and our exact 36-generator Pauli/USp8 dictionary. Parallel worktree changes and unrelated staged files are preserved, not reused as new discoveries.

Five independent Python producers emit JSON certificates under data/ and a single tests/test_toe_20261114_HP3_fivefront_continuation.py invokes all five.

## 1. All 180 charges form an exact quaternionic projective **3-design**, not 4-design

Producer: analysis/toe_20261114_HP3_180_quaternionic_3design.py
Certificate: data/toe_20261114_HP3_180_quaternionic_projective_3design.json

Let z_i=<psi|P_i|psi> for the 27 J-even signed three-qubit Pauli observables. The charge projector \(\Pi=(I+\sum_i z_iP_i)/4\) is rank-one quaternionic; the pushforward of complex Haar measure on CP7 under CP7 -> HP3 is uniform quaternionic Haar. The complete uniform 180-charge first/second/third moment tensors **exactly** agree with these Haar moments:
- E z_i=0;
- E z_i z_j=delta_ij/9;
- E z_i z_j z_k = s_ijk/45 on every **ordered** signed tritangent triple, zero otherwise.

The comparison was carried out over all 27^3=19,683 ordered entries. It follows analytically from the complex Haar pure-state cycle-trace formula with denominator 8*9*10 and the repo's exact signed Pauli dictionary; no random-state fit is used. The 180-point ensemble is a quaternionic projective 3-design in the natural polynomial-in-quaternionic-projector definition. It is not a 4-design, since for each Pauli coordinate z_i the finite fourth moment is 1/9 whereas Haar gives 1/33, from z_i = 2 Beta(4,4)-1. The earlier 180-charge cubature is now identified as exact third-order quaternionic Haar quadrature.

**Priority:** Kueng and Gross (2015) proved that all three-qubit stabilizer states form a complex projective 3-design; see https://arxiv.org/abs/1510.02767 . Zhu (2017) proved the multiqubit Clifford unitary 3-design, https://doi.org/10.1103/PhysRevA.96.062336 . The new element is explicit native signed E6 coordinate verification of the 180-point *projected* quaternionic design, not a claim of first discovery of stabilizer designs.

## 2. Optimal readout of the CP1 hidden qubit over **all 180 integral charge fibers**

Producer: analysis/toe_20261114_hidden_qubit_12_pauli_readout.py
Certificate: data/toe_20261114_hidden_qubit_12_pauli_global_tomography.json

For every one of the 45 signed tritangent supports, precisely 12 of the 36 J-odd Pauli axes commute with the relevant two stabilizer directions. They split into three disjoint four-label cosets, representing the three logical Pauli/Bloch axes; Pauli representatives from different classes anticommute. The requirement to choose a *fixed global menu* that can supply all three axes on **each** of 45 supports is an exact 0-1 hitting-set problem with **36 binary variables and 135 four-term covering constraints**. All 36 candidate variables occur in 15 constraints.

Two independent solvers agree: SciPy/HiGHS MILP finds OPTIMUM **12** and OR-Tools CP-SAT certifies **INFEASIBLE** for any menu of size <=11. One optimal menu in the exact six-bit label convention is

    1, 8, 9, 21, 28, 29, 35, 42, 43, 55, 62, 63.

For each known charge, select a representative from each covered coset. The fiber projector Pi and three logical Pauli operators L1,L2,L3 reconstruct an arbitrary pure fiber density matrix by
\[
\rho = \frac12(\Pi+r_1 L_1+r_2 L_2+r_3 L_3),\quad r_i=\operatorname{Tr}(\rho P_{a_i}).
\]
All 180 fibers were tested with four random states per fiber, 720 total, maximum matrix-entry residual 3.89e-16. Three scalar expectation values are topologically necessary for globally continuous recovery of S2 using fixed real-valued readings, since S2 does not embed in R2. The global **12**-axis optimum is restricted to this Pauli model and these 180 *integral* fibers; do not extrapolate to arbitrary POVMs or all points of HP3.

## 3. ExFT compatibility of all **288** maximal coordinate sections

Producer: analysis/toe_20261114_all288_E6_ExFT_sections_audit.py
Certificate: data/toe_20261114_all288_E6_ExFT_sections_clifford_gauge.json

Every 216 maximal five-axis and 72 maximal six-axis coordinate section satisfies the *strong* E6 generalized derivative constraint \(C^{ijk}\partial_j\otimes\partial_k=0\). The bilinear annihilator of each section S has dimension exactly |S|, verified by a rank (27-|S|) modulo 101 of the full constraint map. Since S lies in the rational kernel and the mod-101 rank provides a rational lower bound, this proves that **no additional arbitrary linear direction** may enlarge any listed section. Exactly 36 signed compact Pauli quarter-turns preserve all 45 signed cubic tritangents and act transitively in two separate section orbits (216 and 72).

Existing ExFT affine closure producer, independently rerun here, checks 32 exact integer gauge-closure tests for representatives in each dimension, and finds a deliberately prohibited derivative pair with nonzero closure residual 12. The previously certified exact quadratic Jacobiator checks are reused as checksums. The full generalized Lie derivative and E-bracket are the *published* E6(6) operations, not newly invented here; their smooth-field closure under the section condition is known from Hohm/Samtleben:
https://arxiv.org/abs/1312.0614 and https://pos.sissa.it/231/133/pdf .

These 288 are coordinate-supported representatives. The verified Clifford action propagates the representatives within each finite orbit, and E6 covariance relates more general E6-transported sections. This is not a classification of all arbitrary noncoordinate sections, nor a physical selection of IIB versus M-theory branch, nor a derivation of an action/tensor hierarchy.

## 4. Constructive USp8 pure-state preparation and sample gate compilation

Producer: analysis/toe_20261114_USp8_constructive_pure_state_compiler.py
Certificate: data/toe_20261114_USp8_constructive_pure_state_compiler.json

The group \(USp(8)\simeq Sp(4)\) acts transitively on the complex unit sphere \(S^{15}\). An explicit quaternionic Gram-Schmidt algorithm constructs a symplectic unitary U whose first column is any requested normalized eight-component complex state \(\psi\). The basis pairs are \((v, Jv)\); an explicit coordinate phase is included to satisfy \(U^T J U=J\). Sixty random targets pass U†U=I, U^T J U=J and U|000>=psi to <=7e-16.

At |000>, the real span of 36 generators \(iP_a\) on the state vector has rank **15**, the full sphere tangent dimension. A deterministic set of 15 independent axes, repeated in three layers (45 continuous Pauli rotations), is compiled by analytic-gradient L-BFGS for five random pure targets. Minimum simulated state fidelity is **0.9999999999999882**. This establishes an explicit finite-depth *sampled* compiler with arbitrary continuous angles, not that a single circuit pattern attains every target at that fidelity. The previously proved finite Clifford W(E6) plus ONE irrational fixed-angle Pauli rotation is **dense in** USp8, allowing asymptotic compilation but not guaranteeing efficient or short fixed-angle sequences. It remains a proper subgroup of SU8: pure-state controllability is not full-unitary controllability. No experiment, insertion loss or fault tolerance is claimed.

## 5. Five-qubit size-eight Pauli-MUB result — stronger audit without overclaim

Producer: analysis/toe_20261114_fivequbit_MUB_independent_rank_audit.py
Certificate: data/toe_20261114_fivequbit_MUB_fullrun_independent_rank_audit.json

The prior Pass12654 exhaustive rank-code exact-cover search reports no size-eight maximal Pauli-MUB spread on **all eight O(5) representative branches**, 433,517,130 nodes without timeout. A second complete traversal on the two S3 equivalence representatives (692,694) returned no witness with different node counts. Those runs are an existing computational result; this pass did **not** pretend to repeat the 433-million-node search.

New checks: a separately implemented GF(2) row-reduction routine agrees with the source's singular/nonsingular decisions on **all 32,768 five-by-five symmetric GF(2) matrices**. All eight completed output records, aggregate node counts, two reverse completion records and orbit representatives were checked. A second independent combinatorial solver reproduces the n=3 size-five positive and size-seven negative controls. A nine-base positive witness was found and tested independently for pairwise disjointness and maximality against every one of **13,888 nonsingular** candidate matrices.

**Evidence grade:** strong exhaustive *one-solver-family* computation for no size8, successful independent rank-model and positive-witness audit. There is still NO standalone DRAT/FRAT/LRAT UNSAT proof nor fully independent 433M-node negative replay. "No size-eight Pauli maximal partial spread" cannot be inflated to a no-go for arbitrary non-Pauli MUBs or for general quantum measurements. Relevant established literature: Kantor on maximal symplectic partial spreads https://arxiv.org/abs/1601.04194 ; Mandayam et al., Pauli unextendible MUBs https://arxiv.org/abs/1302.3709 .

## Combined scientific interpretation and next falsifiers

The project has an explicit **nested design**: 1,080 pure-state stabilizers as a complex projective 3-design in CP7; 180 twistor images as a quaternionic projective 3-design in HP3; and inside each of 180 fibers six discrete states forming a CP1 projective 2-design. These orders differ and must not be conflated.

The 27 E6 charge expectations are informationally incomplete for full pure-state tomography; the optimized 12-Pauli extension recovers the missing logical qubit on the 180 integral fibers. The two admissible ExFT section families are mathematical alternatives, not experimentally selected dimensions. Compact symplectic control can prepare any pure three-qubit state but not every three-qubit unitary. The Pauli-MUB minimum nine is based on a completed computational search but awaits a portable independent UNSAT certificate.

Independent further tests: higher-order HP3 frame potentials and approximate designs; noise/measurement sample complexity of the 12-axis menu; genuinely covariant discretization of ExFT tensor hierarchy and nonlinear gauge closure; efficient synthesis of the arbitrary symplectic compiler from one fixed-angle primitive; and externally independently checked proof logs for five-qubit MUB no-size8.

**No theoretical or experimental Theory of Everything is demonstrated by these five exact mathematical checks.**
