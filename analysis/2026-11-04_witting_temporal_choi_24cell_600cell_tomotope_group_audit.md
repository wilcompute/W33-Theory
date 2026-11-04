# Witting, Pauli W(3,3), one-qutrit temporal history, tomotope, 24-cell and 600-cell

**Date:** November 4, 2026 UTC; **status:** executable finite mathematics, group-theoretic no-go, and conditional process-level quantum model. **NOT** a discovered physical self-entanglement mechanism, a causal time machine, a physical GUT, an emergent metric, or a universal quantum computer.

Producers:
- analysis/toe_20261104_temporal_choi_witting_bridge.py
- analysis/toe_20261104_icosian_24cell_tomotope_obstruction.py

Machine-readable certificates:
- data/toe_20261104_temporal_choi_witting_bridge.json
- data/toe_20261104_icosian_24cell_tomotope_obstruction.json

Regression:
- tests/test_toe_20261104_icosian_temporal_witting.py

## Original publications: distinguish the different geometric objects

1. Barry Monson, Daniel Pellicer and Gordon Williams, **The tomotope**, Ars Mathematica Contemporanea **5** (2012), 355–370, author manuscript https://bmonson.ext.unb.ca/fields/tom.pdf , DOI https://doi.org/10.26493/1855-3974.189.e64 .
   - §2: abstract polytopes, monodromy and string C-group intersection condition.
   - §3: tetrahedral–octahedral uniform honeycomb U, Wythoff geometry and affine Coxeter/B3.
   - §4: finite quotient tomotope T, 4 vertices, 12 edges, 16 triangles, 4 tetrahedral and 4 hemioctahedral cells, 192 flags, automorphism order 96. **The tomotope IS an abstract uniform 4-polytope.** Its non-string automorphism Wythoff presentation is not an assertion that the object fails the polytope axioms.
   - §5: Mon(T) order 18432 fails the string C-group intersection condition; Theorem 5.9 proves infinitely many incomparable minimal regular covers. The R2 automorphism group has order 36864.
   - §6: T's 12-edge/16-triangle medial incidence graph is the classical Reye (12_4,16_3) configuration (48 incidences).
   - Citation boundary: The authors **do not** prove an abstract tomotope subgroup of the 600-cell, a physical Lorentzian metric, or a photonic device from this alone.
2. Alexander Yu. Vlasov, **Scheme of quantum communications based on Witting polytope**, arXiv:2503.18431 (2025), https://arxiv.org/abs/2503.18431 (8 pages). The 240 **complex** Witting polytope vertices in C^4 become 40 rays after identifying six phase multiples. The 40 orthogonal tetrads give a contextual ququart **measurement** scheme; a proposed QKD protocol uses two entangled **ququarts** |Φ4> in C^4⊗C^4. The paper does **not** construct a two-qutrit state implementation or prove composable finite-key security. The 40/40/160 orthogonality incidence agrees exactly with SRG(40,12,2,4), an **already known** Witting/Penrose geometry and repo result, NOT discovered by that paper.
3. M. Waegell and P. K. Aravind, **The Penrose dodecahedron and the Witting polytope are identical in CP(3)**, Physics Letters A **381** (2017), 1853–1857, https://arxiv.org/abs/1701.06512 . They already prove the 40-ray ququart equivalence and discuss the 240 E8 root version in R8; a 2020 erratum is registered and should be checked before relying on fine details. In particular, 240 complex Witting vertices, 240 real E8 roots and 120 real H4 600-cell vertices are different geometric realizations. Matching 240 counts does not identify them.
4. P. K. Aravind, **How Reye's configuration helps in proving the Bell-Kochen-Specker theorem** (2000), https://users.wpi.edu/~paravind/Publications/REYE.pdf . Previous same-day producer analysis/toe_20261104_reye_peres_critical_ks.py independently reconstructed all sixteen critical eighteen-ray Peres parity proofs. These are **published results**, not novel TOE discoveries.
5. Tomme Denney, Da'Shay Hooker, De'Janeke Johnson, Tianna Robinson, Majid Butler, and Sandernishe Claiborne, **The Geometry of H4 Polytopes**, Advances in Geometry 20 (2020), 433–444, arXiv:1912.06156, https://arxiv.org/abs/1912.06156 . The 25 inscribed 24-cells, 5x5 array, 10 complete partitions and their E8/2E8/PG(3,4) connection are **published and proved**. The exact code here reproduces these identities rather than claiming original priority.
6. Subsequent tomotope citations to inspect: Monson–Pellicer–Williams **Mixing and monodromy of abstract polytopes** (2014); Cunningham–Mixer–Williams **Reflexible covers of prisms** (2024), which establishes a contrasting unique minimal regular cover family.

## Prior-repo ownership and where the present work begins

Already in the repo long before this pass:
- exploration/w33_witting_srg_bridge.py: Witting orthogonality = projective two-qutrit symplectic commutation graph W(3,3).
- analysis/2026-10-15_toe90_vlasov_witting_research.md: 40 rays make an exact ququart projective 2-design; already audited Vlasov's limitations and an entanglement witness.
- analysis/w33_20261015_toe91_symplectic_unitary_lift.py: four Witting triflection unitary lifts in U(4).
- analysis/w33_20260924_m36_temporal_triangle_dictionary.py: an existing 36 oriented temporal triangle mapping, no spacetime physics automatically.
- scripts/w33_witting_deck_control_audit.py: 36 symplectic spreads as full quantum-card decks and SRG overlap controls.
- manuscripts/parts/PART_MCXCIII_REYE_TOMOTOPE_24CELL_COMMON_SPINE.md and its producer: 12 24-cell antipodal axes plus 16 hexagon planes provide EXACT Reye medial incidence; the tomotope's Reye layer is **prior art**.
- analysis/w33_pass5309_hoffman_tomotope_degree12_action.py and analysis/w33_pass5643_5650_the_tomotope_w33_bridge_is_wf4_mod_centre.py: Gamma(T)=W(D4)/Z order96; full color-preserving Reye graph Aut576 ≅ W(F4)/Z.
- prior 25 24-cell 600-cell scripts and papers, including PART_MCCCXCIX_MCCCCXVI_600cell_trihedra_theorem.md. Counts alone were never a physical link.

**Executed here:** independently build the operator-history C9 two-qutrit commutation graph and verify its graph isomorphism but unequal Gram matrix to Witting C4; calculate a process-level depolarizing entanglement-breaking threshold; reconstruct the 600-cell from exact golden-field quaternions and distinguish TWO groups of order 576 that the repo's order-based "24-cell/tomotope common spine" might accidentally conflate.

## A. Time-frame fusion has a rigorous kinematic version but needs 9D history space

Let H be a qutrit Hilbert space C3. A single state |ψ>∈H does not contain two independent matrix-algebra factors M3⊗M3. In particular if X and Z generate an irreducible M3 on C3, their commutant on C3 consists only of scalars; a second noncommutative qutrit algebra cannot act independently on that same three-dimensional state space.

But the **space of input-output operators**, End(H)≅H_out⊗H_in*, is nine-dimensional. Vectorize a process operator A∈End(H) into |A>>. Then

    L_B |A>> = |B A>>          => B⊗I_3
    R_C |A>> = |A C†>>         => I_3⊗C*.

Every L_B commutes with every R_C. The four operations L_X,L_Z,R_X,R_Z generate an operator basis of dimension 81. Using the qutrit Weyl generators X,Z with ZX=ωXZ, create 3^4−1=80 nonidentity Pauli classes, group the two order-three generators v and 2v as the same projective cyclic subgroup, obtaining **40 points**.

The **commutation graph** of these 40 temporal-history Pauli classes is SRG(40,12,2,4), 240 commuting unordered pairs. The independent Witting 40 C4 ray orthogonality graph is EXACTLY graph-isomorphic by an explicit 40-element index permutation in the JSON certificate. This reproduces an established abstract graph identification but supplies a precise **two-time Choi realization** of the one-qutrit hypothesis.

Crucial no-go: choose one generalized Pauli representative per point. The 40 representatives are pairwise **Hilbert–Schmidt orthogonal**, Tr(Pi†Pj)/9=δij. The Witting unit rays, instead, have squared offdiagonal overlaps **0 or 1/3**. Therefore even though the 40-vertex graph is the same, **the natural Pauli operators are not the 40 Witting state rays under an overlap-preserving map**. Witting lives in C4, temporal operator history in C9. The graph alone does not define a physical state encoding.

### Operational Choi falsifier, not retrocausality proof

The normalized identity-process vector is |Φ3>=Σ_j|j_out,j_in*>/sqrt3, of Schmidt rank3. Its reduced density is I3/3. This is a **Choi representation** of a channel, not a proof that a single photon is literally entangled with itself at two coexisting times, nor a violation of standard causal dynamics.

For the qutrit depolarizing channel E_p(ρ)=(1−p)ρ+p I3/3 the Choi state is

    J_p=(1−p)|Φ3><Φ3|+p I9/9.

An exactly computed and standard witness is fidelity F_p=<Φ3|J_p|Φ3>=1−8p/9. Any separable normalized Choi state has F≤1/3. Partial-transpose negativity is

    N_p=max(0,1−4p/3).

Thus the channel is non-entanglement-breaking for 0≤p<3/4; at p≥3/4 the qutrit depolarizing channel is entanglement breaking. The producer verifies p=0,1/4,1/2,3/4,1.

This provides a concrete trusted-process-tomography or ancilla-assisted **quantum-memory benchmark**. Testing a physically single propagating photon without a simultaneous ancilla would need a properly specified multitime/comb preparation and intervention scheme and a justified temporal witness; the Choi isomorphism by itself is just standard quantum mechanics. Existing operational Choi literature: https://pmc.ncbi.nlm.nih.gov/articles/PMC7597141/ .

### Frame fusion is not automatically a tensor product

The previous **sums of 81-cycle Hamiltonians** H=Σ w_i B_i B_i^T are frame *operator fusion* and conditioning. In contrast End(H)=H_out⊗H_in* is a tensor product of input-output representations. An explicit functor/intertwiner or physical measurement protocol is required before identifying these two meanings of “fusing frames.” Nothing in this pass supplies one.

## B. Reproduce the 600-cell/24-cell array from binary icosians

Represent φ=(1+sqrt5)/2 symbolically using φ²=φ+1 and each quaternion coordinate as (a+bφ)/2. The 120 unit icosians are 8 axis units, 16 half-coordinate units, and 96 signed even permutations of (0,1,φ,φ−1)/2. Exact integer multiplication checks closure of the binary icosahedral group 2I (order120).

The 24 Hurwitz units form a subgroup 2T (order24); its five conjugates each have five left cosets of 24 vertices, yielding **25 distinct** inscribed 24-cells. Every one of 120 vertices belongs to five. Among the 300 unordered pairs of 24-cells, exactly 100 pairs are disjoint; the other 200 intersect in **six vertices**. The graph of disjointness is canonically (up to relabeling) the 5×5 rook graph SRG(25,8,3,2), with **10 maximum 5-cliques**, giving the five row and five column complete partitions. This is an independent coordinate verification of Denney et al's established result.

The 600-cell has **60 antipodal axes**. Each axis appears in five of the 24 inscribed 24-cells, making **60+25=85** labeled objects, the known numerical point count of PG(3,4). Denney et al construct the nontrivial F4 structure from E8/2E8; this producer verifies the counts, **not** the full field-reduction projective incidence theorem. Do not confuse F4 with the Weyl group W(F4).

## C. NEW precise falsifier: two different groups of order 576 at the 24-cell–tomotope junction

There are two natural groups of order576:

1. **Stabilizer of one inscribed 24-cell in the full H4 symmetry of the 600-cell.** Its faithful 120-vertex permutation representation is given explicitly by

       x -> a x b^{-1},    x -> a overline(x) b^{-1},   a,b ∈ 2T,

   modulo the common (a,b) sign. It has **576 distinct permutations**, a central antipodal involution x→−x and the following full order distribution:

       1:1, 2:43, 3:80, 4:84, 6:272, 12:96.

2. **Full color-preserving automorphism group of the classical Reye (12_4,16_3) incidence graph**, also the TOMOTOPE MEDIAL symmetry, exactly independently enumerated on its 28 vertices. It has **576** elements, **trivial center**, and distribution:

       1:1, 2:75, 3:80, 4:180, 6:240.

Consequently these are **NOT ISOMORPHIC**: the first has 96 elements of order12 and nontrivial center; the second has no order12 element and center1. Order coincidence is a false friend. This corrects any interpretation of a "common 576 symmetry" as an equality of the two complete groups. It does **not** contradict the existing exact Reye incidence graph common spine; the *configurations* agree, but the *selected group actions* require precision.

**Proper relationship:** the **FULL** 24-cell Coxeter group W(F4), order1152, acts on its 12 antipodal axes and 16 central hexagonal planes, with central kernel ±I. Its quotient W(F4)/{±I}, order576, is the Reye graph symmetry. The **orientation-preserving** W(F4)^+ of order576 still contains the antipode (det(−I4)=+1) and acts on axes/planes only through an order288 image. Do not identify W(F4)^+ with W(F4)/{±I}. This aligns the exact structural theorem in the repo's Pass5643/MCXCIII with the H4 stabilizer's different action and resolves the "same number 576" temptation.

## D. How this changes physical research

- The tomotope *rank* four is not emergent 3+1 spacetime; the two-time Choi tensor C3⊗C3* is not a four-dimensional spatial manifold; the 24-cell and 600-cell are rank-four **Euclidean** polytopes. To obtain GR we still need a Lorentzian metric, action and closed constraints.
- The established Reye/Peres contextuality witness is an appropriate known quantum *nonclassicality* test; it does not imply a particle-generation selection or a cosmological time-arrow.
- The 2020 5×5 24-cell array is a useful finite algebraic address space, but it has ten equivalent full partitions. A TOE physical selection rule must choose a gauge/cover or produce invariant observables, rather than choosing one row by hand.
- The 40 Witting measurement bases are **ququart** contexts with nonorthogonal overlap 1/3, whereas the 40 projective temporal Pauli classes are operators in C9 with Hilbert–Schmidt overlap0. A real operational bridge requires a quantum channel/instrument, not only graph labels.
- QKD security needs actual keys, finite-key proof and noise; the original Vlasov proposal is geometric context, not an experimental security guarantee.
- A 600-cell inscribed 24-cell stabilizer and tomotope Reye Aut576 have different element-order spectra. A physical map intertwining both **whole** groups is impossible without restricting/quotienting/change of representation.

## Five independent next gates

1. **Temporal physics:** Construct a causally valid single-photon multi-time process tensor and a genuine temporal-entanglement witness; test entanglement-breaking thresholds under realistic loss and memory with a detector protocol.
2. **Witting measurement:** Build a CPTP instrument that maps chosen W33 Pauli histories into the 40 Witting ququart projectors while preserving chosen operational probabilities. State explicitly which incompatibilities cannot be preserved.
3. **600-cell symmetry:** Replace the false 576 identification with a 2-group/center-sensitive branching diagram H4 → 2T → 24-cell → W(F4)/Z → Reye → Gamma(T), and calculate any true common subgroup using concrete generators.
4. **Quantum contextuality:** Compile one of the published critical 18-ray Peres configurations into a 4-mode measurement sequence and compare its contextuality noise budget with a 40-ray Witting protocol, with measurement-trust assumptions.
5. **Gravitational dynamics:** Use the 24-cell / 600-cell cells as explicit finite spatial or spacetime combinatorial data, then introduce Lorentzian edge lengths and test an action-derived discrete lapse/shift algebra; do not assert a physical spacetime solely from polytopal rank.

## Verification and novelty firewall

**Mathematical identities independently certified:** binary icosian closure, 25 cells, 5×5 rook graph, center/order histogram obstruction, temporal Choi Weyl-commutation SRG identity, Witting graph isomorphism, non-equality of operator/ray Gram matrices and isotropic qutrit Choi negativity. **Previously established:** most geometry, the Pauli–Witting graph bridge, Choi isomorphism, 24-cell array, Peres contextuality, tomotope covers. **Not established:** self-entangled physical photon, time-symmetric universe, 3+1 gravitational metric, dynamical E6 matter selection, or measured quantum advantage. No priority claims for established mathematics.
