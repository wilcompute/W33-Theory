# Two E8 sheets from 25 Reye packets: symmetry obstruction, 120 C4 loops and a four-rail Wilson-flux falsifier

**Executed:** November 4, 2026 UTC. **Starting commit:** 6816ebb73aafbe485d5bb2cd24985a068511f55a. Seven-front predecessor tested the exact 25x60 packet-axis incidence and its A4+A4 integral kernel; this round tests compatibility, possible hopping networks, and physical falsifiability. These are finite mathematics and ideal models; no complete TOE or evidence of retrocausality is claimed.

## Published and repository prior art

- Monson, Pellicer and Williams, The Tomotope (2012): https://bmonson.ext.unb.ca/fields/tom.pdf . Proposition 6.1 proves tomotope rank-(1,2) medial = Reye (12_4,16_3), NOT the complete tomotope is a 24-cell.
- Denney et al, Geometry of H4 Polytopes (2020): https://arxiv.org/abs/1912.06156 ; 25 inscribed 24-cells, 60 antipodal 600-cell axes, 5x5/PG(3,4) construction.
- Koca, E8 lattice with icosians and Z5 symmetry (1989): https://doi.org/10.1088/0305-4470/22/19/007 ; Moody/Patera, Quasicrystals and icosians (1993): https://doi.org/10.1088/0305-4470/26/12/022 . A4+A4 index-five glue to E8 is classical, not new to this project.
- The full W33 point-graph automorphism group is PGSp(4,3) order 51840 (W(E6)); inner PSp(4,3) has order25920. The repo documents and verifies the distinction in docs/index.html, analysis/w33_suzuki_w33_stabilizer_projective_quotient.py and https://wilcompute.github.io/W33-Theory/ . Preexisting scripts/w33_h4_orbital_no_go.py rules out a different full-PSp-invariant 600-cell adjacency on 120 line-matchings.
- Photonic Aharonov-Bohm cages are established experimentally: 2018 PRL121 075502 https://pubmed.ncbi.nlm.nih.gov/30169066/ ; 2020 Nature Communications https://www.nature.com/articles/s41467-020-14692-4 ; 2024 four-site plaquette experiment https://pmc.ncbi.nlm.nih.gov/articles/PMC11649071/ . The 4-rail zero/π square is NOT a novel general quantum effect. Our integration is the specific source of the 120 C4s and their group-compatible flux classes.

## Reproducible code and frozen data

- analysis/toe_20261104_two_e8_glues_w33_symmetry_nogo.py and data/toe_20261104_two_e8_glues_w33_symmetry_nogo.json
- analysis/toe_20261104_double_e8_interlayer_c4_hamiltonian.py and data/toe_20261104_double_e8_interlayer_c4_hamiltonian.json
- analysis/toe_20261104_two_e8_pi_flux_gauge_frame.py and data/toe_20261104_two_e8_pi_flux_gauge_frame.json
- analysis/toe_20261104_e8_c4_flux_photonic_falsifier.py and data/toe_20261104_e8_c4_flux_photonic_falsifier.json
- tests/test_toe_20261104_two_e8_glue_pi_flux_group_nogo.py

## Finding 1. Two E8 glues cannot share one integral root lattice

The exact 25x60 Reye-to-600-cell axis incidence M has rank17 and eight-dimensional kernel A4+A4, determinant25 after metric normalization. Its discriminant (Z5)^2 has two isotropic order-five lines H+={(k,2k)} and H-={(k,-2k)}. The two E8 overlattices L+,L- each have 240 norm-two roots, but their intersection is exactly the A4+A4 lattice. The 240-root sets share 40 roots; their union has 440 distinct roots.

The glue groups intersect only in (0,0) and sum to all25 discriminant classes; therefore:

    L+ ∩ L- = A4 + A4, determinant25;
    L+ + L- = A4* + A4*, determinant 1/25 (not integral).

The two norm-four glue vectors g+=(ω,2ω), g-=(ω,-2ω), with ω=(4,-1,-1,-1,-1)/5, have scalar product -12/5. 40,000 of the 57,600 mixed root pairs have noninteger products. They cannot be treated as two descriptions of the SAME embedded integral E8 root lattice. This is a rigorous arithmetic obstruction for that specific proposal.

## Finding 2. Full H4 packet action cannot act nontrivially on W33 point graph except possibly C2

The effective 25-cell symmetry is G=(A5×A5)⋊C2 of order7200, with C2 exchanging the row and column A5 factors. The full W33 point graph Aut has order51840 and has only one factor5 (no factor25), so no injection from A5×A5 (order3600) exists.

For any homomorphism f:G→Aut(W33), its kernel intersection with the normal A5×A5 base is a swap-stable normal subgroup of the base. Since A5 is simple and center-free, the only swap-stable normal subgroups of A5×A5 are {1} and the entire A5×A5. The first contradicts Lagrange's divisibility, so the entire base is annihilated. Therefore the image of f has order at most2.

This rules out a faithful fully H4-equivariant map on W33's **40 graph labels**. A subgroup/diagonal A5 construction, larger representation, symmetry breaking or non-homomorphic categorical correspondence remains possible. This is not a no-go theorem for arbitrary continuous quantum-Hilbert representations.

## Finding 3. Symmetry completion forces 120 intersheet C4 loops

Lattice maps F1(u,v)=(-u,v) and F2(u,v)=(u,-v) each send roots in L+ to roots in L-. Each matching is invariant under A5×A5, but the row/column involution exchanges F1,F2. The full H4 completion of the two matchings gives 480 root-mode vertices, two intersheet edges per vertex and exactly120 independent four-cycles C4. Its adjacency A0 has A0^3=4A0 and spectrum -2(120), 0(240), +2(120): half its modes are dark to intersheet coupling.

Add, separately within each E8 sheet, the familiar inner-product-one root graph of degree56 (6720 edges/sheet). The combined graph is 58-regular, has13920 total edges, is connected and preserves all five explicitly constructed H4 generators. Exactly, after conjugating the minus root indices by F2, its 480x480 adjacency becomes:

    [[T, I+N], [I+N, T]]

where T is the 240-root E8 adjacency and N is antipodal root inversion, N²=I, TN=NT. T has even-N spectrum 56(1),8(35),-4(84) and odd-N spectrum 28(8),-2(112). All these eigenspace polynomial identities were verified with integer matrix arithmetic. The full combined graph has only seven eigenvalues:

    -6 (84), -2 (308), 6 (35), 10 (35), 28 (16), 54 (1), 58 (1).

The 240 inversion-odd modes remain interlayer-decoupled even though intralayer E8 hopping connects the overall graph. This is an ideal 480-mode root-network mathematical model; 13,920 static couplers would be a high hardware cost and are not claimed feasible.

## Finding 4. Strict H4 edge symmetry and H4-invariant Wilson flux are not the same

Set one negative hopping on each of the 120 four-cycles: every cycle carries Z2 Wilson product -1. The signed adjacency Aπ satisfies EXACTLY Aπ²=2I480 and has spectrum +sqrt2(240), -sqrt2(240), with NO zero modes. Its ideal tick U=-i Aπ/sqrt2 is unitary, U²=-I and each input root becomes a two-neighbor, opposite-sheet equal-probability superposition.

This sign assignment is not strictly preserved by H4 permutation generators. Nonetheless all five generators preserve it **up to explicitly reconstructed vertexwise ±1 gauge transformations**; this is an H4-invariant gauge-equivalence class, not literal equality of the raw signed couplers.

The 480 interlayer edges fall into six strict full-H4 orbits of sizes 40,40,100,100,100,100. The 20 C4 supported by roots in the common A4+A4 shell intersect each orbit in even edge count, so they are FORCED to have Wilson +1 under any strictly invariant orbitwise sign choice. The remaining100 C4 can have Wilson -1, achieved by putting negative signs on exactly one of the four 100-edge orbits. This exact strictly invariant 100π+20zero assignment has spectrum:

    -2 (20), 0 (40), 2 (20), -sqrt2 (200), sqrt2 (200).

The 40 interlayer-dark modes are exactly two null eigenvectors per each of the 20 common-shell loops. Their dimension equals the number of W33 rays, but the group no-go above prevents interpreting this as a faithful W33 label identification without additional symmetry breaking.

The bare pi-flux square has well-known quantum interference properties. The contribution here is the exact arithmetic 20/100 strict split and the H4 gauge-covariance of all120 pi flux loops.

## Finding 5. A four-rail photonic falsifier with noise and exact binomial error controls

One independent interlayer C4 can be built as a four-mode device with equal hopping amplitudes around a square. Set one edge phase to π for the negative Wilson loop, or leave all positive for zero flux. For an input photon at rail0, the opposite rail2 has exactly:

    P(opposite, zero flux, t)=sin(t)^4;
    P(opposite, pi flux, t)=0 for all t.

At t=π/2, ideal zero flux transfers to rail2 with probability1 while π flux transfers0 (the two paths cancel). That is ordinary Aharonov-Bohm caging, and has close experimental counterparts already published; what is new to this repo is the local control attached to the H4 two-glue sectors.

A five-level Lindblad master equation (four rails and a loss vacuum) was evaluated with independent site dephasing kappa and loss gamma, in units where the magnitude of each unperturbed hopping is one; simulated (not experimentally measured) probabilities for gamma=.1, kappa=.1 at t=π/2:

    p_rail2(zero)=0.8024075069181063;
    p_rail2(pi)=0.018623900471373876;
    contrast=0.7837836064467324.

Loss-only controls verify survival exp(-gamma*t); π-edge phase miscalibration causes finite leakage into the opposite port. For the FIXED KNOWN iid rates above, an exact binomial classifier using 22 trials of the unknown device and threshold seven opposite-port clicks has both false-positive and false-negative probabilities below the nominal one-sided Gaussian five-sigma tail 2.87e-7. This is NOT a hardware-level confidence statement: calibration uncertainty, drift, detector dark counts, dead time and pulse/gate errors are not modeled.

One four-rail unit only tests local flux interference. It does not validate full 25-packet H4 symmetry, a W33 quantum encoding, temporal self-entanglement or cosmology.

## Top five independent follow-up gates

1. Find an explicit subgroup-equivariant W33 ↔ A4+A4 bridge, especially diagonal A5 representations; test characters, root/projector Gram data, and any actual Hilbert intertwiners. The full H4 graph action is proved impossible.
2. Build an operational three-time single-photon causal process tensor with interventions, Choi entanglement witnesses and classical-memory null models. Ordinary four-port flux localization is NOT a temporal-entanglement witness.
3. Derive a local action or microscopic dynamics on the two glued E8 sheets that selects the relative gluing without an imposed sign bias; test the gauge lift under a dynamical and not just static Z2 gauge field.
4. Compile and calibrate one of the four-rail loops into physical beam splitters, phase shifters, photon losses and detector models; then test robust finite-shot confidence using real calibration uncertainty rather than the ideal iid 22-trial model.
5. Upgrade the action-derived Euclidean Regge 1→5 control to Lorentzian multi-simplex curvature and calculate nonlinear lapse/shift constraint brackets with precise falsification criteria.

**Main boundary:** We have built a new explicit mathematical connection between the actual 25 Reye packets, two incompatible embedded E8 lattice completions, an H4-symmetric intersheet root graph, and locally testable Wilson flux. We have also proved a strong obstruction to preserving full H4 symmetry on W33's 40 point labels. None of these results supplies a complete physical Theory of Everything.
