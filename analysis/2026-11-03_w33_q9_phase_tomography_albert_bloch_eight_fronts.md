# 2026-11-03 — Eight executed W33 frontiers: q9 cubic, optical completeness, full permutation module, Albert frame no-go, Bloch 3D, and three creative falsifiers

**Reproducibility level:** q9 exact enumeration of all 91,558,740 point triples of ONE known 48-line hyperoval with Witt-group transfer to full orbit; PSp43 group calculations exact; 24-mode POVM span tests, representation spectral splits, optical state distinguishability, and three-voltage Bloch tensor numeric at declared tolerances. No observation of physical elementary particles, gravity or quantum hardware and no TOE claim.

**Parallel/earlier work priority:** Passes 12518–12525 already own the q9 48-line hyperoval and full size 3,586,680 orbit (not yet exclusion of every non-hyperoval even 48-set). Pass 12526 owns 36 regular 5-simplexes of the 216-frame. The earlier November 2 commits own the 216 POVM (rank 201), 4884-rotation Naimark compiler, the 15D blind irreducibility and the q7 full cubic theorem. Pass 10949/10950 owns an exact 27D **compact Albert algebra** reconstructed from the clock E8 bracket; do not misconstrue our no-go as disputing that separate result. Concurrent df1e1402c owns native deck/conditional vacuum studies; this pass does not reproduce them.

## 1. q9 cubic reconstruction via single-seed orbit averaging (new algorithm and theorem)

Frozen producer: analysis/w33_20261103_q9_seed_cubic_orbit_types.py (the expensive 91,558,740-triple pass). Compact checker: analysis/w33_20261103_q9_exact_full_orbit_cubic_certificate.py. Outputs: data/w33_20261103_q9_seed_cubic_orbit_types.json and q9_exact_full_orbit_cubic_certificate.json.

Set q=9; v=(q+1)(q²+1)=820; 48 isotropic lines twice cover exactly 240 points, leaving 580 uncovered. Set x_i=29 on covered points, -12 otherwise; sum_i x_i=0. Construct the cubic T_abc by averaging x_a x_b x_c over the full PSp4(9) orbit.

**Symmetry-reduced identity:** To obtain the full-orbit average for a fixed point-triple of a given G-orbit type, it suffices to sum x_a x_b x_c over all 3-subsets of that type on ONE seed, divided by their class size. No 3,586,680-support BFS is needed. We computed every 3-subset once, using the symplectic pairings in GF(9) and projective span test.

For q=9, -1 is a square in GF(9). Among triples with 0 collinear pairs, both the nonisotropic-line and projectively independent cases split into quadratic-character plus/minus orbits according to chi(omega_ab omega_bc omega_ca). These seven types are transitive under PSp4(9), via projective symplectic Gram matching and Witt extension for independent triples, PSL2(9) action for a nonisotropic projective line and PGL2(9) for isotropic lines. All seven type cardinalities divide |PSp4(9)|=1,721,606,400.

| Type | Triples | Exact cubic coefficient |
|---|---:|---:|
| Isotropic-line triple | 98,400 | **24616/15** |
| Exactly two collinear pairs | 2,988,900 | -141712/1215 |
| Exactly one collinear pair | 23,911,200 | 1768/243 |
| Nonisotropic line, plus | 398,520 | -30991/243 |
| Nonisotropic line, minus | 398,520 | -30991/243 |
| Independent, plus | 31,881,600 | 493/270 |
| Independent, minus | 31,881,600 | 493/270 |

The classes exhaust 91,558,740 triples. The coefficient for isotropic lines is unique. The exact weighted sum of all distinct-triple moments is 1,617,040, independently forced by (sum x_i)^3=0 and the repeated-index moments. Hence **for three DISTINCT points, T_abc=24616/15 precisely characterizes a W(3,9) isotropic line**. The equality of plus/minus cubic coefficients is an additional exact feature of this hyperoval orbit, not a failure to distinguish the geometric orbits. This theorem assumes the parallel-track 48-line hyperoval orbit is the complete hyperoval class; it does not assert no other 48-line even sets.

## 2. Fixed receiver plus three input phase settings gives numerical full complex tomography

Producer: analysis/w33_20261103_three_setting_ic_povm.py; certificate: data/w33_20261103_three_setting_ic_povm.json. The existing 216 rank-one real POVM on 24 complex modes has real Hermitian operator span rank 201 out of 576. Because the identity belongs to every span, m settings can have rank at most 1+200m; therefore at least THREE settings are necessary.

Seeded random 24-mode **diagonal phase masks**, with NO additional mode mixing, gave ranks 201, 401, **576** with one, two and three settings, respectively. For four settings rank remains 576 but can be better conditioned. This demonstrates an open numerical witness of full informational completeness with only phase shifts ahead of a fixed calibrated 216-output receiver. The generic three-setting completion is not a symmetric informationally complete POVM (SIC) and not a robust/photonic implementation. Reference: dynamic IC-POVM generation (Quantum Inf Process 20,105,2021, https://doi.org/10.1007/s11128-021-03045-9) and Clements balanced optical meshes (Optica 3,1460,2016, https://doi.org/10.1364/OPTICA.3.001460).

**Optical caution:** 216 output ports, complete calibration, phase control over all 24 logical modes, and statistically sufficient photon samples are still mandatory. The earlier 4884-rotation triangular mesh has unfavorable loss depth. No photon-number resolving model, hardware compiled layout, or experimental outcome is claimed.

## 3. Full 216D route permutation module and multiplicities

Producer: analysis/w33_20261103_216_permutation_isotypic_probe.py; output: data/w33_20261103_216_permutation_isotypic_probe.json. The exact G-action and its ten 216x216 equivariant orbital matrices are constructed from 25,920 PSp43 permutations and the route orbit. The squared effect-Gram K has exact integer spectral dimensions 1,24,80,81,15,15 for eigenvalues 14400,3168,2304,768,576,0, respectively.

Generic commuting-with-G self-adjoint orbital combinations show that the K=2304 eigenspace further splits **20+60**; K=0 and K=576 are 15D equivalent group modules (a nonzero isometric intertwiner couples precisely these). The real 60D piece admits a nonzero group-equivariant antisymmetric complex structure J, with J²=-c²I at numerical residual below 1e-11. It therefore splits over complex scalars into conjugate 30+30. The 20D module has no such antisymmetric structure in this generic test.

Thus the proposed complex irreducible degree multiset is **1,24,81,20,30,30,15,15**, with 15 counted twice as the same irreducible. Sum 216 and commutant dimension 1+1+1+1+1+1+2²=10, matching the exact ten orbitals. **Formal complex character identification/rational projectors remain open.** Crucially, the orbital algebra is noncommutative: do NOT assert that every equivariant orbital matrix commutes with K; equivariance alone is insufficient for repeated constituents.

## 4. Albert: a rigorous fixed-frame embedding obstruction, not an Albert no-go

Producer: analysis/w33_20261103_albert_fixed_frame_irrep_obstruction.py; certificate: data/w33_20261103_albert_fixed_frame_irrep_obstruction.json.

PSp4(3), order 25,920, has the rank-three action on the 40 points of W33. A point stabilizer (order 648) has orbits 1,12,27. The orbital commutant is spanned by I,A,J, so the 40D point permutation module decomposes over C into pairwise distinct **absolutely irreducibles 1+15+24**.

A 27D Albert algebra equipped with a fixed labelled Jordan frame has three invariant eight-dimensional Peirce off-diagonal components (8+8+8); its connected frame stabilizer is of D4/Spin8 triality type. The irreducible W33 carrier 24 cannot be PSp43-equivariantly identified with this reducible 8+8+8 carrier while keeping the frame fixed. As PSp43 is simple, a group action preserving the three-frame set cannot permute the three members nontrivially either. This excludes a specific broad **fixed-frame extension ansatz**, not non-frame/symmetry-breaking embeddings and not the preexisting clock Albert algebra. See McCrimmon, A Taste of Jordan Algebras and Garibaldi et al., Albert Algebras over Commutative Rings (2024), DOI:10.1017/9781009426862.007.

## 5. Three-dimensional cyclic-voltage Bloch tower and its limitations

Producer: analysis/w33_20261103_native_three_voltage_bloch.py; certificate: data/w33_20261103_native_three_voltage_bloch.json. A regular Z_m^3 cover is defined using three independent base edge voltages, chosen on disjoint vertex pairs. Without constructing 40m³ vertices, the 40x40 Hermitian Bloch normalized Laplacian is diagonalized at each momentum. Its lowest band obeys lambda0(k)=k^T D k + O(|k|^4) with

D eigenvalues approximately 0.001744790394, 0.001744790429, 0.001744790556, anisotropy ratio **1.000000093**. The sampled small-k relative quadratic error is at most 6.8e-6. Along lattice-axis momenta 2pi/m, the energy scales as O(m^-2). The near-isotropy is an observed property of this chosen three-edge arrangement; it is NOT 3+1 dimensional Lorentz invariance, a continuum quantum field theory, a derived value of c or massless particle dynamics.

For comparison, Lieb-Robinson locality bounds concern finite-speed propagation under local Hamiltonians (Wilming–Werner, Physical Review B 105,125101,2022, DOI:10.1103/PhysRevB.105.125101); our *Laplacian dispersion* alone is not a Lorentz cone.

## Independent creative experiments

**Creative A — Orbit averaging rather than materializing state orbit:** The q9 method reuses one hyperoval and a seven-class geometric orbit partition. It is an exact group-design compression of an orbit average; the full orbit size is used for provenance only. Future q=11 applications must classify square characters and projective dependence before assuming five orbit classes.

**Creative B — Minimal three-step phase-only IC:** The proof 1+200m bound shows three is optimal in setting count for this 201-dimensional effect span. The seeded numerical witness uses diagonal phases only, so the extra hardware can be phase control rather than additional 24-mode interferometers. The SVD condition number for the selected three random full-unitary witness was about 198 (four settings about 32); phase-only inversion conditioning needs separate optimization.

**Creative C — Limited discrete-phase/no-go and an imaginary-coherence witness:** Producer analysis/w33_20261103_two_bit_phase_witness.py. Three seeded trials with TWO-BIT phase masks (only 0,pi/2,pi,3pi/2 per mode) yielded ranks 499,515,499 rather than 576; these samples are NOT a theorem excluding all discrete masks. Two valid density matrices rho±=I24/24 ±(i/48)(|0><1|-|1><0|) give identical output probabilities under the original real POVM. Applying one 90deg phase on mode1 produces total variation **0.02651459**. This is basis-dependent imaginary-coherence discrimination and must NOT be misrepresented as detection of physical parity or CP violation.

## Reproduction and physical stop conditions

Run focused scripts from the repository root on a compatible NumPy/SciPy environment. The q9 full triple seed census visits 91,558,740 triples and takes about 265 seconds on the verified Windows machine; all compressed certificate verifiers take seconds. Every claim above distinguishes mathematical proof, numerical evidence, existing parallel ownership, and unresolved physical interpretation. Missing for a TOE: dynamical action/vacuum, quantitative dimensional scales, genuine particle spectrum/couplings, causal spacetime limit, falsifiable experimental deviations from existing quantum physics, and a practical single-photon implementation.
