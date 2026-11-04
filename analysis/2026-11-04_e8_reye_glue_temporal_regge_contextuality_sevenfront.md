# Seven hard controls: E8, 25 Reye packets, temporal Witting, contextuality hardware, and Regge gravity

**Executed:** 2026-11-04 UTC on the connected Windows computer. **Baseline:** GitHub master 7dde67be41b005debebca6e11d3cd495a3ae4eb6. The worktree is isolated from the main checkout and its pre-existing uncommitted files.

**Source and novelty boundaries:** These are independently executed finite-geometry proofs, quantum-instrument models, and a Euclidean action-based Regge calculation, NOT a Theory of Everything or experimental claims. The 2012 primary paper by Monson, Pellicer and Williams establishes the tomotope's rank-(1,2) medial graph as Reye (12_4,16_3), not an isomorphism of full tomotope and 24-cell. Original author paper: https://bmonson.ext.unb.ca/fields/tom.pdf . Denney et al, The Geometry of H4 Polytopes, arxiv:1912.06156 already proves the 25 inscribed 24-cells, their 5x5 structure, and the 600-cell/E8/PG3(4) connection. Repo Pass8925-8940 and Pass9961-9984 already know E8/2E8 quadratic/Hermitian 135/120 and 45/40. Repo Pass176 gives a different W33-code E8 discriminant map. Prior repo w33_schur_reye_288_action_bridge.py owns a Schur-to-Reye 288 action; TOE92 owns a pre-existing Witting optical Givens mesh. Temporal Choi and Reye contextuality have substantial published prior art.

## Reproducible artifacts

- E8 orthogonal/Hermitian versus PG3(4): analysis/toe_20261104_e8_mod2_pg34_refinement.py, data/toe_20261104_e8_mod2_pg34_refinement.json
- All H4 packet pair/triple orbits: analysis/toe_20261104_h4_reye_25_orbits.py, data/toe_20261104_h4_reye_25_orbits.json
- Coherent heralded Witting/time compression: analysis/toe_20261104_coherent_witting_history_compression.py, data/toe_20261104_coherent_witting_history_compression.json
- Contextuality detector and cross-context calibration: analysis/toe_20261104_contextuality_compatibility_detection_budget.py, data/toe_20261104_contextuality_compatibility_detection_budget.json
- Action-derived 4D Euclidean Regge: analysis/toe_20261104_regge_4simplex_1to5_action.py, data/toe_20261104_regge_4simplex_1to5_action.json
- Extra 25x60 packet-axis fusion: analysis/toe_20261104_reye_axis_frame_fusion_kernel.py, data/toe_20261104_reye_axis_frame_fusion_kernel.json
- Extra E8 two-sheet index-five glue: analysis/toe_20261104_reye_kernel_a4a4_e8_glue.py, data/toe_20261104_reye_kernel_a4a4_e8_glue.json
- Automated regression: tests/test_toe_20261104_e8_reye_fivefronts_more.py

## 1. E8/2E8 through an explicit F4 structure: a mismatched 25-versus-45 stratification

E8 Cartan Gram determinant1 defines an eight-dimensional quadratic form q(v)=v^TGv/2 mod2, exactly 135 nonzero isotropic and 120 anisotropic vectors. The program independently constructs an eight-bit isometry to F4^4 with Hermitian quadratic norm sum, and transports multiplication by a primitive F4 element to a fixed-point-free order-three E8 mod2 orthogonal action. Its 85 nonzero triple-orbits comprise 45 Hermitian isotropic projective points and 40 others, a classical result already in repo Pass9961-9984.

By contrast, the icosian 25 inscribed 24-cells form the rank-one 2x2 determinant-zero Q+(3,4) quadric, not the Hermitian H(3,4). In the specified matrix coordinates those 25 have Hermitian q values 21 zero/4 one; the remaining 60 invertible axis points have 24 zero/36 one. A concrete determinant-preserving PGL2(4) left shear changes this chosen Hermitian q. No fully symmetric identification of the two varieties follows from their sharing an 85-point projective ambient space.

## 2. Full 25-packet H4 symmetry and all three-body patterns

Left/right binary icosian transformations and quaternion conjugation act on all 25 inscribed 24-cells as an exact order-7200 group, the image of full H4 order14400 modulo central inversion. Point action transitive; each packet has effective stabilizer288. Unordered pair orbits sizes 100 (disjoint) and 200 (intersect in 6 vertices). All C(25,3)=2300 triples split into four orbits of sizes 100, 400, 600, and 1200. Exactly the 600 orbit triples have a shared antipodal vertex pair; the other three triple orbits share no vertex across all three cells. No invariant single packet or distinguished triple under full H4. A physical three-generation selector requires additional action/dynamics.

## 3. Coherent Witting temporal compressor instead of correlation-destroying output-only channel

The one-qutrit two-time Choi operator space is C3_out tensor C3_in* (dimension9); Witting rays inhabit dimension4, although their abstract W33 graph matches the Pauli commutator graph. No deterministic faithful universal isometry C9 to C4 exists.

Build U9 with first vector ideal |Phi3> and U4 with first vector one Witting ray. K=U4[:,0:4] U9[:,0:4]^dagger maps9->4 coherently in a selected subspace; the five-dimensional complementary failure F gives K^dagger K+F^dagger F=I9. Ideal Choi identity state passes with probability1, uniform maximally mixed history with probability4/9. Measure surviving output with the full Witting40 POVM. The 41-outcome test (40 rays plus failure) distinguishes ideal identity-process Choi J0 versus fully depolarizing J1 with total variation31/45 and equal-prior optimal success 38/45=84.44%, better than the prior output-only 50% but below full joint Helstrom 17/18=94.44%. The exact J0 probabilities are one selected ray 1/10, 12 orthogonal rays0, and 27 nonorthogonal rays1/30; J1 yields each ray1/90 plus failure5/9.

With repeated independent depolarizing .1 per exchange, Choi entanglement negativity becomes zero from 14 exchanges, while this discrimination remains above chance. Therefore process distinguishability is NOT a temporal entanglement witness. The success branch is state-selective and heralded, not an optical physical implementation or literal single-photon time entanglement.

## 4. Contextuality hardware hard falsifier: one-hot beta=9 is not enough

Each ideal ququart orthogonal tetrad read out by a four-port single-click interferometer has one +1 and three -1 dichotomic outcomes, whose product is automatically -1. Thus all nine context products sum to beta=9 even if different physical ray measurements are secretly used in different contexts. A deterministic context-dependent classical one-hot model reproduces beta=9. The old 3.04% four-independent-sign-flip threshold was a conditional toy model, NOT a physical four-port noise bound.

This pass reconstructs all nine Peres and all forty Witting analyzers from the exact complex two-mode Givens blocks stored in the preceding commit. For 96 independent random realizations at each Gaussian mixing-angle and relative-phase sigma=0,.005,.02,.05,.1 radians, it computes true cross-context overlap fidelity of occurrences of the same nominal ray. Eighteen Peres ray-pair comparisons and 240 Witting pair comparisons per realization. At sigma0 mismatch=0; at nonzero sigma mismatch>0; all quantiles recorded in JSON. This operational-equivalence data is the needed type of calibration information, but no unjustified robust inequality is inferred from it.

For an explicitly declared no-click assignment, all four signs -1 on a missed photon, the context product is +1 instead of -1, so beta=9(2eta-1). Crossing the ideal noncontextual seven requires eta>8/9. At eta=.90, beta=7.2 and a simple iid Bernoulli normal-approximation five-sigma budget is 2025 trials per context, 18,225 total, ignoring calibration/noise-drift uncertainty. This is NOT a universal detection-loophole threshold. Relevant experiment: 2023 programmable photonic contextuality processor, PMC10624346; 2025 high-dimensional OAM bipartite nonlocality conversion, Phys Rev Lett 134 010203.

## 5. A real four-dimensional action test for Regge gravity, with a negative nonlinear result

Take boundary 4-simplex vertices 0,e1,e2,e3,e4 in Euclidean R4, insert interior c=(1/5,1/5,1/5,1/5); refine by 1-to-5 Pachner move, obtaining five 4-simplices, ten interior triangle hinges and ten boundary triangles. S=sum_internal A(2pi−sum dihedral angles)+sum_boundary A(pi−sum dihedral angles). All 4x4 simplex Gram matrices and boundary terms are evaluated; the Regge Schlaefli derivative is separately checked by finite differences.

Flat interior data have ten zero deficit angles to numerical precision; S0=3pi/2+4pi sqrt3/3≈11.9675864373, and action gradient zero. Translating the actual interior Euclidean vertex preserves S0 and zero deficits. Hessian on five interior edge lengths has four null modes from vertex motion and one nonzero eigenvalue≈128. A perturbation in the unique transverse direction creates curvature: at size+.005, Hessian eigenvalues roughly [-1.1349,-.9081,-.9081,-.9081,107.7507], so the four flat gauge nulls are lifted. This reproduces known broken nonlinear gauge / pseudo-constraint behavior of standard Regge actions (Bahr & Dittrich arxiv:0905.1670; Dittrich & Hohn 2010; Hohn 2015). It is NOT a Lorentzian/causal spacetime action nor nonlinear first-class ADM closure and is not yet based on a 600-cell metric.

## Extra 6. Eight blind directions of the native 25x60 frame-fusion map

Construct M with 25 rows of 24-cell Reye packets and 60 600-cell antipodal-axis columns. Every row has12 ones, every column5 ones. The exact integer Gram K=MM^T has eigenvalues 60 (1), 15 (16), 0 (8). Rank(M)=17, its positive singular-value condition number is2, and exact polynomial K(K−15I)(K−60I)=0.

The full eight-dimensional kernel of M^T is the space f(r,c)=u_r+v_c on the 5x5 packet grid with independent row and column zero-sum potentials: sum_r u_r=sum_c v_c=0. This proves that a naive linear packet-to-axis carrier irretrievably loses these eight amplitude directions. It does not identify these null amplitudes as physical gauge bosons.

The 600 triple orbit has a direct incidence description: each of 60 axes lies in5 packets and picks exactly C(5,3)=10 triples, and all 600 such triples are unique.

## Extra 7. An exact A4+A4 to two E8 lattices INSIDE that packet blind kernel

The 5x5 embedding f(u,v) obeys <f(u,v),f(u',v')>_25=5(<u,u'>+<v,v'>) for the two five-component zero-sum vectors. After dividing the metric by5, the integral kernel root lattice is exactly A4 plus A4, rank8 and determinant25, with discriminant group (Z/5)^2.

Let omega1=(4,-1,-1,-1,-1)/5. The two isotropic gluing slopes k with 1+k^2=0 mod5 are exactly k=+2 and k=-2. Adjoin g_plus=(omega1,+2omega1) or g_minus=(omega1,-2omega1). Both index-five overlattices are even, unimodular, positive-definite rank8; each is therefore E8. Explicit 8x8 integer basis Grams have determinant1 and even diagonal. Both root enumerations have exactly 240 norm-two roots, split by glue cosets 40+50+50+50+50, and their root pairs +/- occupy exactly 120 anisotropic E8/2E8 classes; the remaining 135 nonzero classes are quadratic-isotropic.

The subgroup A5xA5 of independent even row/column permutations preserves both E8 gluing lattices. The full packet symmetry includes row/column interchange, which sends the slope +2 to its inverse mod5 = -2, EXCHANGING THE TWO E8 extensions. Exact integral change-of-basis tests verify the inclusion each way and failure to preserve just one. The row-column swap also preserves original 25x60 axis-incidence up to inversion of its 60 A5 matchings.

**Interpretation and limit:** The specific packet-to-axis frame fusion naturally exposes an A4+A4 eight-dimensional null module; the established index-five A4+A4 gluing gives TWO concrete E8 lattice extensions. No full-H4-invariant mechanism selects one; selection needs a sheet datum or symmetry breaking. Past/future, chirality or topological self-entanglement are candidate metaphors to formalize, NOT demonstrated physical identifications. The A4² to E8 gluing is CLASSICAL lattice mathematics, not a claimed novel theorem. For published prior lattice-theoretic context see Griess and Lam, EE8-lattices and dihedral groups, Appendix D (https://dept.math.lsa.umich.edu/~rlg/researchandpublications/pdffiles/griesslamdihedral17jun08.pdf), which discusses A4-type sublattices, gluing, and E8.

## Five independent next gates

1. **E8 two-sheet dynamics:** construct an H4-equivariant two-sheet Hamiltonian or action on the pair of glues and a Z2-odd measurable order parameter; prove what gauge-breaking or superselection is actually required.
2. **Temporal process experiment:** define a causal three-time single-photon comb with intervention operations and an operational temporal-entanglement witness robust to loss and detection.
3. **Physical contextuality:** derive a context-equivalence-error-aware noncontextual inequality and a real no-click protocol; estimate finite-shot uncertainties in device-native four-mode settings.
4. **Lorentzian gravity:** extend beyond one flat Euclidean 4-simplex to Lorentzian multi-simplex action, causal cones, lapse/shift, and actual nonlinear Dirac closure tests.
5. **W33/E8 representation:** build or falsify a natural equivariant map from the two E8 kernel sheets to the two-qutrit W33 Pauli/temporal process operators, using representation characters and quantum Gram constraints rather than numerical analogy.

**Claim firewall:** Finite identities and ideal quantum models are exact/reproducible under declared assumptions. No new physical fundamental constants, experimental photon self-entanglement, derived CKM masses, Lorentzian gravity or completed TOE.
