# Tomotope original paper: exact 24-cell / 600-cell / PG(3,4) bridge and five TOE falsifiers

**Date:** 2026-11-04 UTC. **Evidence:** original author paper text, earlier repository source/code, newly executed finite-algebra and controlled quantum simulations. **Not a TOE, not a physical self-entanglement experiment, not a claim of unprecedented H4 projective geometry.**

## Original article: where the 24-cell actually enters

Barry Monson, Daniel Pellicer and Gordon Williams, *The tomotope*, Ars Mathematica Contemporanea 5 (2012) 355–370; original author PDF https://bmonson.ext.unb.ca/fields/tom.pdf ; DOI https://doi.org/10.26493/1855-3974.189.e64 .

The paper's §§2–6 were inspected, including the rank-four abstract-polytope construction, its source tiling in Euclidean R3 by tetrahedra and octahedra (affine Coxeter B3 tilde), the complete tomotope face counts (4,12,16,4 tetrahedra+4 hemioctahedra, flags192), order96 automorphism action, order18432 monodromy, order36864 minimal regular cover, and Theorem 5.9's infinitely many incomparable minimal regular covers.

**Critical source distinction:** Section 6 Proposition 6.1 proves that the tomotope's rank-(1,2) edge–triangle medial graph is exactly the Reye (12_4,16_3) incidence graph. The paper does not itself directly construct the 24-cell, all 25 24-cells of the 600-cell, or a full tomotope as a subpolytope of the 24-/600-cell. The Reye=24-cell axes/hexagonal planes bridge is classical, and the 25-cell/E8 link is in later literature (Denney et al 2020).

Established repo prior art:
- manuscripts/parts/PART_MCXCIII_REYE_TOMOTOPE_24CELL_COMMON_SPINE.md: explicit Reye /24-cell spine;
- analysis/w33_schur_reye_288_action_bridge.py: older Schur/D4 stabilizer-to-Reye 288 embedding;
- analysis/w33_pass5643_5650_the_tomotope_w33_bridge_is_wf4_mod_centre.py: Reye576 = W(F4)/central inversion;
- analysis/w33_20261015_toe92_optical_givens_mesh.py: older Witting40 4-mode Givens compiler;
- analysis/2026-10-15_toe90_vlasov_witting_research.md: Witting2-design and proposed quantum communications;
- analysis/toe_20261104_reye_peres_critical_ks.py: 16 published 18-ray Peres/Aravind critical parity proofs.

Independent fully executable materials committed in this round:
- analysis/toe_20261104_pg34_icosian_quadric.py -> data/toe_20261104_pg34_icosian_quadric.json
- analysis/toe_20261104_h4_24cell_reye_index2.py -> data/toe_20261104_h4_24cell_reye_index2.json
- analysis/toe_20261104_temporal_witting_instrument_noise.py -> data/toe_20261104_temporal_witting_instrument_noise.json
- analysis/toe_20261104_ks18_witting_interferometer_compiler.py -> data/toe_20261104_ks18_witting_interferometer_compiler.json
- tests/test_toe_20261104_tomotope_pg34_fivefronts.py

## Front 1 / Extra discovery: entire PG(3,4) from 600-cell icosians, not just 85 counting

Use exact unit quaternions over Z[golden ratio] (binary icosahedral group 2I order120) and Hurwitz binary tetrahedral subgroup 2T order24. Its five conjugate subgroups and their five cosets each give 25 inscribed 24-cells. Their disjointness graph is the 5x5 rook graph SRG(25,8,3,2), which has ten maximum five-cell partitions.

Each 600-cell antipodal axis lies in exactly five 24-cells, one per row and column. It therefore defines a permutation of five elements. The 60 permutations form a parity class; after globally relabeling columns they are exactly the 60 even permutations A5.

Over GF4=GF2[alpha]/(alpha²+alpha+1), projective 2x2 matrices have (4^4-1)/3=85 points:
- The 25 singular rank-one matrices are the hyperbolic quadric Q+(3,4) = P1(F4) × P1(F4), the inscribed 24-cells.
- The 60 invertible projective matrices form PGL(2,4) ≅ A5, matched to antipodal 600-cell axes through the five-axis membership permutations.
- The exact determinant polarization B(X,Y)=det(X+Y)+det(X)+det(Y) equals the **300 geometric axis–24-cell membership relations**, not merely their counts.

The producer independently reconstructs all 357 projective lines of five points each, 21 lines through every point, and 85 polar planes of 21 points each. Classification of lines by rank-one/quadric points: 72 disjoint from Q, 75 tangent (one Q), 200 secant (two Q), 10 fully within Q (five rank-one points).

**Much stronger direct Reye statement, verified for every one of 25 cells:** Fix rank-one quadric point c. Its polar tangent plane has 21 points: nine on Q, twelve invertible/off-Q, corresponding exactly to the twelve antipodal axes of that inscribed 24-cell. The plane has 21 projective lines; five pass through c and the other sixteen each contain exactly three external axes and two quadric points. Independently detect central Euclidean hexagonal planes of the 24-cell by exact rank-two conditions on its golden-field four-vector axes. For ALL 25 cells, the 16 triples from this real Euclidean span agree **exactly** with the 16 3-axis triples on the PG(3,4) tangent-plane lines. Each of 12 axes belongs to four triples: the classical Reye (12_4,16_3).

Thus: tomotope medial = Reye = 24-cell axis/hexagonal planes = 25 PG(3,4) quadric tangent-plane secant configurations. This is an exact finite incidence statement, NOT 25 isomorphic full tomotopes or a selected physical cover.

**Extra pair-gluing theorem/test, and a caught incorrect guess:** Among the 300 unordered pairs of inscribed 24-cells, exactly 100 are disjoint (their two quadric points lie on a generator line); exactly 200 intersect in six Euclidean vertices/three antipodal axes. Those three axes are the common central hexagonal plane of the pair, and all 200 shared axis-triples are different. The direct test that incorrectly tried to put those axes on the secant PQ failed; the **correct duality** is that the three shared axes are the three invertible points on the **polar projective line (PQ)^perp = P^perp intersection Q^perp**. This polar line also contains two other rank-one points. Every one of the 200 pairs passes this exact test. For disjoint cells, PQ is a self-polar generator. This identifies the global gluing of the 25 Reye packets by finite-projective polarity rather than only their local 12/16 configurations.

Known priority: Denney, Hooker, Johnson, Robinson, Butler, Claiborne, *The Geometry of H4 Polytopes* arXiv:1912.06156, Adv Geom 2020, explicitly establishes 25 24-cells, 600-cell and PG(3,4) via E8/2E8. Rank-one/nonsingular 2x2 matrix coordinates and PGL2(4) ≅ A5 are classical. The new artifact is the independent concrete certificate of **all 25 Euclidean hexagon triplets against finite-field tangent-plane lines**. It does not itself implement E8/2E8 lattices.

## Front 2: correct explicit 288 H4 stabilizer to Reye map

The full W(H4) stabilizer of an inscribed 24-cell has 576 elements but central antipodal inversion; full typed Reye automorphism group also has order576 but trivial center and different element-order spectrum. They are NOT isomorphic.

The new source builds a 12-axis/16-central-hexagon Reye graph from Hurwitz quaternions, then enumerates 24×24×2 left/right/conjugation transformations. There are 576 distinct transformations of Hurwitz vertices, inducing exactly 288 transformations on 12 antipodal axes and 16 hexagons; the parameterized action has fourfold kernel, and the real 576 group has antipodal kernel order2 on the incidence system. A typed 28-node Reye isomorphism explicitly transports all 288 permutations into the enumerated complete Reye aut576 group as a normal index-two subgroup. The effective order histogram is 1:1, 2:27, 3:80, 4:36, 6:144.

This resolves the specific H4-icosian group-action map. Important older owner: analysis/w33_schur_reye_288_action_bridge.py already proves the analogous Schur/D4 -> Reye index-two subgroup, so the abstract phenomenon is NOT novel; only this explicit independent icosian-coordinate realization is new to this round.

## Fronts 3+4: one-qutrit temporal history to Witting ququart instrument, with a falsifier

A qutrit *state* lives in C3 and cannot host two independent faithful noncommuting qutrit factor algebras. Its two-time input/output **operator history** End(C3)=C3_out⊗(C3_in)* lives in C9 and can carry the commuting Weyl actions giving the two-qutrit Pauli commutation SRG(40,12,2,4). Witting40 lives in C4 and shares the graph but not state/projector Gram data.

The forty Witting ququart rays satisfy sum(P_i)=10I4 and sum(P_i⊗P_i)=2(I16+SWAP) (complex projective 2-design), as already known. For the isometric three-rail embedding V:C3→C4, construct 120 Kraus maps K_(i,a) = (P_i V)⊗<a| /sqrt10 from C9 to C4 for 40 rays and three input-basis indices. Directly verify sum K†K=I9 and ray measure-and-prepare: the channel is entanglement breaking.

**Sharp operational no-go**: ideal identity Choi J0=|Phi3><Phi3| and fully depolarizing Choi J1=I9/9 differ by full joint trace distance8/9, allowing equal-prior optimal discrimination success17/18. Their reduced output states are both I3/3, so the Witting POVM on output only has identical forty probabilities and cannot discriminate at all (success1/2). A useful experiment must preserve or probe input-output correlations, not merely observe final Witting rays.

Noise: for independent qutrit depolarizing p=.1 per exchange and m exchanges, t=(.9)^m. Choi fidelity F=(1+8t)/9; partial transpose negativity max(0,(4t-1)/3). The channel is non-entanglement-breaking through exchange13 but EB at14. Independent flagged photon-erasure survival eta multiplies unconditional negativity by eta but postselection gives no free improvement in detector cost (~1/eta attempts). Numerical 12×12 Choi partial transposes checked at m=0,1,4,8,13,14,20 and eta=1,.6,.2,0.

This is orthodox Choi/process quantum information, NOT proof of a self-entangled photon or retrocausal causal loop. Operational multi-time comb interventions or ancilla-assisted process tomography are required for a physical witness.

## Front 5: improved explicit 4-mode KS18 and Witting40 measurement-bank compiler

The earlier Witting optical Givens compiler in analysis/w33_20261015_toe92_optical_givens_mesh.py already produced all40 basis circuits: histogram {0:1,3:3,4:3,5:10,6:23}, **209** abstract two-mode operations total. This is prior art for Witting compilation. Our new producer permits all 24 free detector-output label permutations and decomposes preparation basis (then uses its adjoint for measurement). Every 4x4 numerical unitary reconstructed to worst residual below 5e-16.

The optimized Witting40 bank now has counts {0:1,3:6,4:33}, total **150 abstract two-mode operations** (59/209=28.2% fewer than prior stored gate bank), maximum four per setting. Output relabeling, phase settings, actual interferometer routing/swaps and hardware cross-talk may change physical cost.

Separately all sixteen *published* critical 18-ray Peres/Reye configurations were compiled into nine orthogonal four-mode basis measurements each. The lowest sampled full 9-context ideal bank has **28** Givens mixing operations, with per-context [2,1,1,5,3,4,5,3,4]. This is not a fair direct physical comparison to 40 different Witting settings; they are different quantum tasks.

For nine four-ray contexts, assign A_i=2P_i-I. Every orthogonal tetrad has product -I4 in quantum theory. The parity sum beta=-sum_j <prod_i A_i> is9 in the ideal quantum model. A noncontextual deterministic assignment has product of the nine context products +1 because each of 18 rays appears exactly twice, hence beta≤7. Exhaustive 2^18 assignments verify tightness: beta_NC=7. With simplified independent binary sign-flip noise epsilon per observable, beta_Q=9(1-2epsilon)^4 exceeds7 iff epsilon<0.0304477921. This is NOT a physical single-click 4-outcome detector noise model, nor loophole-free contextuality; compatibility, phase, calibration, readout and postselection require dedicated engineering.

Sources for the inequality: Cabello/Peres/Aravind and https://perimeterinstitute.ca/personal/gtabia/notes/cryptoContextuality.pdf .

## Necessary physics and provenance boundaries

- The tomotope does **not** simply become an inscribed 24-cell. The common object is a rank-(1,2) Reye medial graph, and the tomotope's regular-cover ambiguity survives.
- PG(3,4) has field characteristic2; W33 qutrit Pauli/symplectic geometry is over F3. No unital field embedding F3→F4 exists. Their connection must be nonlinear, representational, or via another ambient object, not a naive field-linear identification.
- E8/2E8 to PG(3,4) is published, but these computations prove a concrete isomorphic projective-incidence model from icosians, not yet a specific E8 lattice quotient map.
- Abstract 4-polytope rank, a four-dimensional ququart Hilbert space, and 4D Lorentzian spacetime are mathematically different notions.
- Proof of finite geometrical incidence and ideal numerical compiler does not establish Einstein gravity, a physically selected covering, QKD security, or an experimental contextuality violation.

## Five independent next gates

1. Single-photon three-bin multitime quantum-comb preparation/intervention readout that measures genuine history correlations with loss awareness.
2. Coherent C9-to-Witting C4 compression with explicit information loss bound, rather than entanglement-breaking output-only tomography.
3. Full 25-configuration H4 group orbit and stabilizer analysis on the twenty-five Reye tangent planes, with cover-independent observables.
4. Explicit E8/2E8 finite module plus F4-complex-structure map into the icosian-derived PG(3,4), not merely the incidence isomorphism.
5. Device-native implementation and finite-shot/compatibility-certified contextuality protocol for the 28-coupler KS test and the optimized 40-basis Witting bank.

**Verification scope:** exact quaternionic and GF4 arithmetic, all 25 geometric/projective Reye matches, exact finite permutation group embedding, 120 CPTP Kraus identity, Choi loss controls, 16×9 Peres and 40 Witting 4-mode unitary decompositions, exact 2^18 parity bound. Nothing here completes the physical Theory of Everything.
