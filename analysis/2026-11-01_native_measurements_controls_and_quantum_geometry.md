# Native measurements, controls and quantum geometry

This continuation executes the five finite targets following `8f5a8ce879f77c406aa5d215252478a50ec9934e`: frame tomography, octahedron frustration, parent control compilation, perturbation guarantees, and a common cubic/spinor cover. It also tests two further bridges: Markov traces and real operator geometry. Results refer to the repository's actual 120 rank-three projectors on C9, not dimension matching with an unrelated exceptional object.

The three descriptive `w33_20261101_*` producers and `tests/test_w33_20261101_native_five_fronts.py` implement the maps below. Corresponding JSON files contain the outcome dictionaries, Clifford words, exact counting records and relation certificate. The earlier native construction is in `w33_20261031_chiral_tetrahedron_strange_bridge.py`; exact loop arithmetic and Clifford actions are in `w33_20261031_tick_loop_rigidity.py`.

## 1. All 27 frames become explicit tomography measurements

The existing 810 tetrahedron complements Q_i have rank three. The 45 complementary-plane factorisations admit 27 partitions into five disjoint octets. Every partition supplies 90 distinct Q_i and a POVM

    E_i = Q_i/30,     sum_i E_i = I9.

The Q Gram spectrum is 90 once, 9/4 eighty times, and zero nine times. Thus every density matrix is reconstructed from its Born probabilities by

    rho = (40/3) sum_i p_i Q_i - (13/3) I9.

For probability errors summing to zero, the sharp synthesis bound is `||delta rho||F <= 20 ||delta p||2`. All 27 measurements and random-state reconstructions are checked; a separate test reconstructs every matrix unit. Choosing orthonormal columns W_i spanning Q_i and stacking W_i dagger/sqrt(30) gives an explicit 270-by-9 Naimark isometry. Its 90 three-rail blocks implement the effects. The dimension 270 is minimal because each orthogonal outcome block must accommodate a rank-three effect. All 27 isometries and their blocks are numerically verified; the chosen eigenvector bases are gauge dependent.

The same POVM supports different state dynamics. Declaring that outcome i prepares Q_i/3 gives

    Phi(rho) = rho/40 + (13/120) I9,

an entanglement-breaking channel. The Luders instrument instead gives

    L(rho) = (13/40) rho + (3/40) I9.

Its normalized Choi partial transpose has eigenvalues 2/45 with multiplicity 45 and -1/36 with multiplicity 36, so it is not entanglement breaking. Each choice is independent of which of the 27 frames is used. Outcome geometry does not determine the instrument.

Each complement belongs to three frames. For the 810-by-27 incidence matrix M, `M^T M = 90 I + 18 A`, where A is the (27,10,1,5) strongly regular graph. Its Gram spectrum is 270 once, 108 twenty times and zero six times. An exported coordinate bijection maps the 45 shared-factor triples to the actual cubic support in `artifacts/canonical_su3_gauge_and_cubic.json`. The unitary Clifford image on frames has order 25920; adding the stored antiunitary gives 51840. Antiunitary symmetries are not physical quantum channels.

The incidence rank 21, tritangent geometry and E6 support are prior repository mathematics, including `PASS11194_11198_FIVE_TOE_FRONTIERS.md` and `w33_hesse36_e8_matter81_root_lift_boundary.py`. The 45 factorisations and 27 frames are explicitly credited in `PASS11177_PERFECT_GATES_TRITANGENT.md`; `2026-10-10_toe45_cusp_tomography_parallel_research_audit.md` already investigates tomography. `PASS4984_4991_EXECUTED_OUTCOMES.md` contains a different tight incidence reader, and `PASS5044_5051_EXECUTED_OUTCOMES.md` contains a different local channel compiler. These are not the present C9 POVM. The contribution here is the operator-level 810-outcome dictionary, reconstruction and instrument calculations, not a discovery of E6 incidence or of informational completeness. Tight informationally complete measurement theory is established [Scott, 2006](https://arxiv.org/abs/quant-ph/0604049). No cubic signs, Yukawa coefficients or particle assignments are dynamically selected here.

## 2. Exact octahedron frustration and tetrahedron density of states

Write `B_abc = 2 sqrt(3) Im Tr(P_a P_b P_c)`, an integer obtained from the existing Eisenstein trace routine. Only three distinct directions in a nondegenerate plane contribute. We evaluate all 58,320 such ordered entries; Pauli trace orthogonality sets the remainder to zero. Exact invariance under the nine Clifford generators is checked.

For opposite vertex pairs (a,b), (c,d), (e,f), orient the eight octahedron faces with sign (-1)^(i+j+k). Their chirality is

    chi = Im Tr((P_a-P_b)(P_c-P_d)(P_e-P_f)).

At J=1, K=2, lambda=sqrt(3), use integer energy 6E: pair costs are 0,18,12,-4 and each face contributes -3B. Ordered opposite pairs have four Clifford orbits of sizes 120,240,4320,9720. For each representative and all 120^2 choices c,d, the last pair minimisation separates into `min_e(L_e-3v_e) + min_f(L_f+3v_f)`, because e and f have no edge. This is exact coverage of all 120^6 = 2,985,984,000,000 labelings, not a claim to have individually enumerated them.

The maximum integer octahedral chirality is 9. The witness `[0,1,12,13,17,15]` simultaneously minimises all twelve bonds and has chi=3sqrt(3)/2. Consequently, throughout J>0, K>3J/2 and any real lambda,

    E_min = 12(2J-4K/3) - (3sqrt(3)/2)|lambda|.

Swapping e,f supplies the other chirality. At the reference couplings, E_min=-25/2. The unattainable separate-face lower bound is -16, leaving an exact frustration defect 7/2. There are 622,080 ordered ground configurations: 466,560 from the same-direction/different-outcome opposite-pair orbit and 155,520 from the noncommuting orbit. This degeneracy count is for the reference couplings; extra degeneracies can appear at lambda=0.

An independent weighted enumeration covers all 120^4 = 207,360,000 tetrahedron labelings and exports every energy level, multiplicity and witness. The reference ground energy is -8, multiplicity 9,720; the exact first gap is 3. These are finite classical energy models with supplied couplings, not a derived thermodynamic phase or physical energy scale.

## 3. Compile every parent, identify the supplied universal resource

All 810 complements lie in the known Clifford orbit. Breadth-first transport exports actual words of length at most nine, and checks their 9-by-9 matrix action. For the canonical complement `Q = I3 tensor |S><S|`, S=(0,1,-1)/sqrt(2), the gap-one parent is H=I-Q. Its active evolution is

    exp(-itH) = exp(-it) V diag(1,1,exp(it)) V dagger,

with V a balanced mixer of the last two active rails and an identity spectator. Each parent therefore has its exported Clifford conjugation, two balanced mixers and one phase. A coherent controlled evolution must also retain the global phase reference.

The gate is Clifford, up to scalar, exactly when t lies in pi Z. The conjugated Z fixes the first rail, so a Pauli image must be diagonal; its off-diagonal magnitude is sqrt(3)|sin(t)|/2. At pi multiples the gate is identity or parity.

There is a further controllability consequence: the 90 parents I-Q_i from any tomography frame have Gram spectrum 360 once, 9/4 eighty times and zero nine times, hence span Herm9. One continuous parent evolution together with Clifford conjugation generates u(9). Period 2pi supplies inverses. This uses a continuous non-Clifford control resource; finite braid images alone have not become universal, and efficient compilation under noise is not proved.

For a supplied Gibbs bath at dimensionless inverse temperature beta, the active ground fidelity is `F=1/(1+2 exp(-beta))`. Wigner negativity appears exactly at beta>log(2), and mana is `max(0,log((1+4F)/3))`. The energy scale, bath and cooling protocol remain inputs. Earlier parity-heralding and magic-state results retain ownership of those established mechanisms.

## 4. Certified finite perturbation bounds

Assume four true rank-three orthoprojectors have operator error at most epsilon<1/4. Then `||delta H||op<=2epsilon`, the three-low/six-high cluster gap is at least `1-4epsilon`, and its spectral projector obeys

    ||Q_tilde-Q||op <= 2epsilon/(1-2epsilon).

Weyl separates the clusters; projecting the perturbed low eigenvector equation onto the original high space gives the stated angle bound. This preserves a cluster, not an exact common kernel or its internal degeneracy.

Cyclic trace telescoping bounds each complex triple-trace error by 9epsilon. For J,K>=0, the pair-energy error is at most `(6J+12sqrt(2)K)epsilon`; summing six edges and four faces bounds the tetrahedron energy error by `(36J+72sqrt(2)K+36|lambda|)epsilon`. The commutator Frobenius variation is at most 4sqrt(3)epsilon, while a rank-three projector commutator has Frobenius norm at most sqrt(3/2).

At the reference couplings, the exact classical gap 3 gives the sufficient condition epsilon<0.004966877844396899 for perturbed minimisers to remain inside the former ground set. Degeneracy may split. Random independent unitary perturbations and separate direct matrix tests check the inequalities; they do not replace their proofs or constitute laboratory calibration.

## 5. Smallest compatible cubic/spinor cover: 61,440

Use the actual signed cubic group L of order 30,720, its prescribed permutation quotient K of order 960, and the existing unitary spinor group G of order 1,920 with the same quotient. All 30,720 signed elements and all 184,320 generator edges are checked. Every tree-word spinor lift differs from another lift by a sign. The six-generator GF2 lifting system is inconsistent; independent enumeration excludes all 64 central-sign choices.

The obstruction has a short independently checked certificate: signed generators 0 and 1 commute, but their actual spinor matrices anticommute. Rephasing either matrix by any scalar cannot change this. Thus the prescribed signed action cannot itself carry the prescribed spinor lift.

The explicit solution is the fibre product `H={(l,g): l and g have the same K image}`, of order 61,440. Its kernel over K is C2^6; its centre is C2 x C2. The central signed parity changes sixteen of the 27 coordinates and is independent of the spinor -I. Six paired generators are exported; all 1,920 dyadic Gaussian unitary matrices are rebuilt and checked, including faithfulness and the quotient projection. The combined 27+4 representation is faithful.

Any compatible common cover maps into this fibre product. A subdirect image has order 30,720 or 61,440; the excluded lift rules out the smaller option. Minimality is for these prescribed quotient maps and actual representations, not every possible E6 embedding. No interaction or matter assignment follows merely from the cover.

## Further bridge A: Markov trace failure and a fresh-register repair

The existing nine-dimensional five-projector chain satisfies its braid/TL relations. But its normalised ordinary trace does not realise the full six-strand Markov trace: for the native f4 and last projector R,

    tau9(f4 R)=1/9,   whereas tau9(f4)/3=1/27.

Retain the first four projectors tensored with I3 and replace the last by the eigenvalue-one projector of Z_first tensor I_second tensor Z_third. The resulting 27-dimensional chain satisfies the TL relations. The new projector's partial trace over the fresh qutrit is I9, proving the Markov extension for every x in Mat9, not just sampled braid words.

The SU(2)_4 fusion-path ledger gives minimal ordinary-trace carrier dimension 3^floor(n/2) for the full positive Markov trace on the semisimple Jones quotient. At six strands the path dimensions are 5,9,4 with multiplicities 1,2,1, giving 27. This does not bound arbitrary fixed-charge braid representations. Fusion and localisation are established theory [Rowell and Wang](https://arxiv.org/abs/1009.0241); the contribution here is the actual native counterexample and repair. This 27-dimensional carrier is not automatically the different E6 coordinate space.

## Further bridge B: explicit real first-order operator geometry

On fundamental C9, Mat9 has scalar commutant, preventing a faithful commuting right Mat9 action through an antiunitary reality operator. A nonzero faithful bimodule must have dimension divisible by 81, since Mat9 tensor Mat9^op is Mat81.

The minimum is attained on the Hilbert-Schmidt space Mat9, with `L_a(M)=aM`, `R_b(M)=Mb`, `J(M)=M dagger`, and `D(M)=[H,M]`. Direct identities give J^2=1, JD=-DJ, order zero and the first-order condition. D has spectrum -1 eighteen times, zero forty-five times and +1 eighteen times. However, a grading commuting with all left multiplications is a right multiplication, and anticommuting it with D forces H to be scalar. This chosen nonconstant parent therefore has no such even grading.

Its spectral action is `45 f(0)+36 f(1/Lambda^2)`, identical for all 810 conjugate parents and both orientations. This is the expected isospectral invariance of this family; it is not a no-go theorem for every noncommutative geometry. Nor is this operator-space 81 automatically the different Steinberg homology representation.

The [Connes-Chamseddine spectral action](https://arxiv.org/abs/hep-th/9606001) and [their later programme](https://arxiv.org/abs/1004.0464) make concrete algebra, representation, reality, grading and Dirac data essential. The present construction supplies some and exposes a missing grading; it is not an orientable, Poincare-dual Standard Model triple. Likewise [EPRL spin foams](https://arxiv.org/abs/0711.0146) require four-dimensional geometric and vertex-amplitude data. A finite TL representation alone supplies neither those dynamics nor Lorentzian gravity.

## Repository reconciliation and validation

Incoming commit `8fa5cb6b6` was reviewed: its four-anyon order-648 group, Hesse quotient, and independent codeword chirality split are a complementary finite braid result, not the continuous resource above. Its q=9 minimality search remains UNKNOWN. Its site audit rejects interpreting matching low-complexity constants as evidence; no such inference is made here. The earlier incidence spectra and tomography are credited above. Result searches included Python, JSON, Markdown, HTML, TeX and RESULTS_INDEX.

While validation ran, the shared checkout advanced through `23f720456` and `5a72b00cd`. Their reports `2026-11-01_five_plus_three_w33_physics_continuation.md` and `PASS12514_12521_EXPLICIT_BRAID_ISO_MAGIC_AXES.md` were read. The former supplies a sparse optical cycle encoder, stabilizer-basis fidelity verification and an actual three-site 120-state quantum chain, alongside distinct loss and Lorentz-action obstructions. The latter now constructs the explicit projective four-anyon braid isomorphism and its 1+2+3+3 decomposition, improving on the earlier group-profile comparison. Those results belong to those packets. They complement the fresh-register Markov trace audit and supplied continuous-control distinction here; neither finite braid-image equivalence nor a spatial quantum-chain computation by itself derives a physical TOE. This packet's nine frozen baseline input files still match committed blobs at `5a72b00cd`.

There are 19 focused new tests; the publication validation also replays the preceding 56 connected tests, regenerates all three producers and archives the actual command output and hashes. The temporary validation harness initially omitted the repository root from its import path; the resulting nine loader errors are retained in the log. After correcting that path, all 75 real tests passed in 11.195 seconds. This unittest suite does not collect pytest-style function tests. Exact portions are integer/group enumeration and the exported relation witness; operator spectra, transport, channels and dilations use floating-point checks of the displayed algebraic identities. Remote Desktop Commander independently replayed the 19 tests successfully on TheHeavyCrown. The execution host has the same hostname: this is another worker on the same hardware, not extra physical compute or a separate server.

This packet completes the five finite investigations as scoped here and adds two audits. It does not solve a physical TOE. The originally requested entire weekly commit corpus and entire forty_points PDF reading remain incomplete; this report makes no completion claim for them. The native quantum carrier, supplied controls, finite classical energy and speculative particle/gravity interpretation remain distinct.

Five independent next investigations:

1. Classify the lowest mixed cubic/spinor invariant interactions of the 61,440 cover and test whether proposed matter couplings actually survive its two centres.
2. Construct charge projectors and F-move maps for the repaired 27-dimensional Markov carrier, with an explicit comparison to the existing anyon representations.
3. Analyse finite-shot tomography, loss and readout noise, and operationally distinguish the Luders and measure/prepare instruments.
4. Test whether saturated chiral faces on closed triangulations force a tetrahedral target map or a branched-cover constraint; no such theorem is asserted yet.
5. Build a graded real Dirac completion and test first order, orientability and duality before using spectral geometry for a particle or gravity claim.
