# Eight-front W33 quantum physics continuation: actual A5 × C2 torsion, gauge tests and non-Abelian category discrimination

**2026-10-31, third continuation of the local quantum-group branch.**

## Audit trail and scope

This packet builds on GitHub commit ad8846e599812d2327821521c53dacd6058bba06 and the independent local commit ccbd086d1f5b1cc204547766baced5449981d020 (read before starting). The latter *already* solved the exact eight-site 27/28 frustration bound, finite Jones parity 5+4, Gross-Wigner mana, 81-mode crosstalk and finite-depth-QCA no-go; those are not presented here as new. This packet executes five further tests and three independent outside-box ideas in separate reproducible functions. It does not claim a TOE, physical gravity, non-Abelian topological order, observed clock field or an anomaly-free Standard Model.

**New producers:** \`analysis/w33_20261031_same_subgroup_ambient_lift_audit.py\`, \`analysis/w33_20261031_full_subgroup_GF5_representation.py\`, \`analysis/w33_20261031_quantum_geometry_eight_new_falsifiers.py\`. Matching \`data/*.json\` and \`tests/test_w33_20261031_quantum_geometry_eight_new_falsifiers.py\` are frozen and tested.

## Front 1 — The full three-generator exceptional subgroup is ACTUAL and has order 120

The previous q9 48-line 240-point witness produced abstract line-graph automorphisms of orders 2,3,5. Only order5 had previously been lifted to an actual 4×4 projective similitude over GF9. Here *the same frozen indexed line orbit and exactly the previously chosen maps* are reconstructed from the actual GF9 lines. For each map we search GF9-linear and Frobenius-semilinear lifts by four independent point images and 8³ projective column scalings. Each of the three order2,3,5 maps has a **linear PGSp(4,9) lift**, not merely an accidental abstract graph symmetry. Tests confirm all 820 projective points and all 820 isotropic lines, group order and projective powers.

Generators of this common action on the 48 selected lines close into a group of **order 120**. Its derived subgroup has order60 and is perfect with trivial center; the whole group has center C2. Therefore the group is **A5 × C2**, not S5 (trivial center) and not binary icosahedral 2.A5 (perfect central extension). This corrects the earlier ambiguity. These are exact permutation/group computations; 3 separate subgroup generators are now demonstrated to live in one actual geometric group.

## Front 1 continued — Seven-dimensional canonical characteristic-five torsion action

Recompute the exact 24×24 q9 bipartite biadjacency B. The integer SNF reported earlier has 5^7 torsion, with six free zero factors. The mod5 right kernel is 13-dimensional. Build six integer solutions of Bx=0 from rational exact nullspaces, clearing denominators and dividing their gcd. Critically their images over GF5 are **rank six**.

This last fact resolves the earlier concern about saturation *for this prime*. Let S=ker(B:Z^24→Z^24). Since Z^24/S≅im(B) is torsion-free, S is saturated of rank6 and S/5S injects into (F5)^24 as a six-dimensional subspace. Six independently reduced integer nullvectors therefore span its **full image**, regardless of any index of their generated sublattice coprime to5. The exact sequence for reduction modulo5 gives a canonical isomorphism:

    ker_F5(B) / red(ker_Z B)  ≅  coker_Z(B)[5].

Our constructed seven-dimensional representation is consequently the **canonical characteristic-five torsion action** of the exact 24×24 biadjacency (not merely an arbitrary rational-kernel quotient).

For the *same actual A5×C2 subgroup*, reconstruct the right-partition permutation matrices and descend them to explicit 7×7 GF5 matrices. All 360 generator multiplication edges of the 120-element group check, and **all 120 matrices are distinct**: the action is faithful. The central involution acts with eigenspace dimensions **+1:4, −1:3**. The whole subgroup fixes a 1D subspace; its commutant has GF5 dimension **3**. The order5 generator has nilpotent (g−I) ranks **7,4,2,0,0,0**, i.e. Jordan type 3+3+1. The solver also checks whether the 1D invariant representation splits by pairing fixed vectors with invariant covectors. This is a major exact representation-theoretic improvement, but assigning any sector to a physical particle or generation would still be unsupported.

A further exact decomposition *has now been completed*: a unique fixed vector and fixed covector pair to the nonzero element 3 in GF5, giving an equivariant 1D direct summand. The 4D center-even space splits as 1_even ⊕ 3_even; the center-odd space is 3_odd. Restrict the two 3D pieces to explicit generators of the perfect derived A5: in each block neither the representation nor its dual has any fixed vector. Since A5 is perfect, it has no nontrivial one-dimensional characters; the absence of invariant lines and dual invariant lines proves both 3D blocks irreducible over GF5. An exact 9-variable intertwiner calculation finds Hom_A5(3_even,3_odd) dimension ONE, so the two 3D spaces carry isomorphic A5 modules, distinguished only by the central C2 sign. Thus the complete seven-dimensional module is **1_+ ⊕ 3_+ ⊕ 3_-**, with the same irreducible 3D A5 type in both sectors. This is a genuine modular decomposition, not a particle-spectrum claim.

## Front 2 — The three-mode orientation is a genuine local-U(1)-gauge-distinct loop

The oriented coupler F has F12 F23 F31 = +6; reversing F changes it to −6. For diagonal local rail rephasings F↦D F D†, the complex loop product is unchanged because all local phases cancel around the triangle. Tested on 200 independently randomized diagonal U(1) matrices; maximum numerical residual below 1e−13.

Thus phase redefinition alone cannot equate the two signed weighted triangles. The ideal pure-state overlap remains −3/7 and the one-photon Helstrom Bayes error is (1−2sqrt10/7)/2. We additionally test common phase drift, not refitting each hypothesis separately. However unknown *hypothesis-dependent* detector gain patterns can spoof the output likelihood; output reference phases and rail calibration remain physically supplied. This is a gauge-invariant optical *synthetic flux* observation, not spontaneous CP violation.

## Front 3 — Quantum, not just classical, geometry-sensitive clock model

From actual W33 directions choose four with mixed commuting/noncommuting relations; fix one outcome and use the earlier exact pair costs E_ab=0 for same a, =2J for commuting distinct directions, =2J−4K/3 for noncommuting. Construct finite quantum models on three distinct spatial graphs (2-site chain, 3-site triangle, 4-site ring) with local four-dimensional label Hilbert spaces and supplied transverse projector mixing \`-h sum_i |+><+|_i\`. For J=1,K=2, numerically diagonalize the *full* matrices and record ground energy and excitation gaps for h=0,.1,.4,1.

Positive h makes the finite mixing matrix irreducible stoquastic, so Perron–Frobenius implies a unique ground state; numerically verified positive gaps. Therefore finite-state avoidance of level crossings is not by itself an actual bulk symmetry-breaking phase transition. A 120-event Hilbert space, thermodynamic limit and microscopic couplings are still to be built.

## Front 4 — Why native Bloch rotations alone cannot bootstrap a Chern phase

Construct 2D momentum-dependent native projector family

    U(k)=exp(i kx P1) exp(i ky P2), P(k)=U(k)P0U(k)†,

using three actual nine-dimensional W33 rank-three projectors, with a supplied periodic momentum torus. Each exponential is globally smooth and periodic because P is a genuine projector. Hence the bundle P(k) has the explicit global rank-three frame U(k)|u_a>, so its first Chern class **must be exactly zero**, irrespective of nonzero local Berry curvature. Independent non-Abelian determinant-link Chern calculations verify C1≈0 on 7×7,11×11,17×17 grids. A genuine chiral topological phase requires a nontrivial patching obstruction, boundary anomaly or additional spatial dynamics; merely composing native gates by k-dependent global conjugations cannot create it.

## Front 5 — A genuine local gauge-connection Ward identity, not a spin-two metric

Add a two-component dynamical frame e(x) and SO(2) link connection a(x,μ) on a *supplied* periodic 3×3 lattice with action

    S = (1/2) sum_edges ||e(x+μ) − R(a(x,μ)) e(x)||²
      + β sum_plaquettes [1−cos(curl a)], β=.7.

Under independent vertex rotations theta_x, e(x)↦R(theta_x)e(x) and a(x,μ)↦a(x,μ)+theta_{x+μ}−theta_x. The supplied model has exact gauge covariance; calculate the action before/after a random nonuniform local rotation and independently test the infinitesimal Ward identity at one vertex by centered differences. Both pass numerical tolerances. This is a constructive step from an acoustic scalar to a frame/connection gauge model, but **SO(2) in 2D is not Lorentzian SO(1,3) Einstein–Cartan**: no Einstein constraints, spin2, continuum gravity, diffeomorphism group or quantum matter dynamics has been derived. See Duque, *Hamiltonian gravity in tetrad-connection variables*, Phys. Rev. D 112, 124046 (2025), DOI 10.1103/3r98-k11x for what a complete constraint analysis demands.

## Outside-box idea A — Explicit categorical obstruction: native SU(2)4 is not D(S3)

The native Jones braid lives in a nine-dimensional two-qutrit Clifford representation at delta=sqrt3, associated with SU(2)_4 fusion theory. This is NOT the same topological theory as the non-Abelian S3 quantum double now used in quantum hardware. Build S3=Z3⋊Z2 explicitly, exhaust all 6³ associativity tests and conjugacy classes, classify centralizers and resulting Drinfeld double anyon quantum dimensions:

    D(S3):      8 types, dims 1,1,2,2,2,2,3,3, total D²=36.
    SU(2)_4:    5 types, dims 1,sqrt3,2,sqrt3,1, total D²=12.

The different ranks and global quantum dimensions prove the braided fusion categories are inequivalent. A D(S3) edge has six local states (qubit×qutrit), not the native nine-state two-qutrit carrier. This is a valuable *negative* connection preventing a mistaken category identification.

Literature: Lo et al, *Universal gates from braiding and fusing anyons on quantum hardware*, Nature 655, 591–597 (2026), DOI 10.1038/s41586-026-10709-y, prepared a 54-qubit D(S3) ground state and combined braiding/fusion; Chen et al, *A universal circuit set using the S3 quantum double*, npj QI 11,112 (2025), DOI 10.1038/s41534-025-01063-4; Bols et al, *Category of Anyon Sectors for Non-Abelian Quantum Double Models*, CMP 407,2 (2026), DOI 10.1007/s00220-025-05492-2.

## Outside-box idea B — Ten full, exactly mutually unbiased W33 measurement contexts

Enumerate all 40 four-point totally isotropic lines and solve an exact-cover problem for ten disjoint lines partitioning all forty W33 Pauli directions. For each line choose two commuting independent rank-three Pauli projectors P_(p,k), P_(q,l). Their nine products P_(p,k)P_(q,l) are orthogonal rank-one joint eigenspace projectors summing to I9. Between any two different contexts, \`Tr(P_i Q_j)=1/9\` for all 81 pairs, in all 45 pairs of bases. The program verifies this with max numerical error under 1e−12.

This is a *complete set of ten MUBs in dimension nine*. It supplies an actual tomography/uncertainty frame: measuring one basis constrains the entropic uncertainty in another by H(Bi)+H(Bj)≥ln9. This fact and its relation to symplectic spreads are established prior art and documented elsewhere in W33, so the new increment is an independent projector-level operational audit, not a claim of discovering MUBs.

## Outside-box idea C — Spectral dimension from native W33 can be manufactured without spacetime

The native W33 adjacency spectrum is {12¹, 2²⁴, (−4)¹⁵}, hence graph Laplacian eigenvalues {0¹,10²⁴,16¹⁵}. Its finite heat trace and scale-dependent effective spectral dimension are exactly

    Z(t)=1+24 exp(−10t)+15 exp(−16t),
    ds(t)=2t(240 exp(−10t)+240 exp(−16t))/Z(t).

The effective dimension goes to zero at short and long times, with a transient peak. For the Cartesian square graph G□G, L_square=L⊗I+I⊗L, so Z_square=Z² and **ds_square=2 ds** at every scale. For the n-fold Cartesian product the finite-scale spectral dimension multiplies by n while no continuum or physical time has been derived. This is a stringent no-go for claiming a 3+1 dimensional universe from a finite W33 heat-trace plateau or a chosen graph product alone. The definition of asymptotic spectral dimension properly requires a scale limit (see return-probability definitions in finite/infinite graph spectral theory).

## Top five independent next tests (new)

1. Decompose the canonical seven-dimensional A5×C2 GF5 module completely: check whether the central-even4 equals trivial1⊕irreducible3 or a nonsplit extension; determine modular irreducibility and compare with published ATLAS A5 F5 3D matrices.
2. Derive an experimentally identifiable synthetic-orientation signature robust to unknown but *common* detector gains using multi-input calibration, not inferred CP selection or an arbitrary rail gauge.
3. Quantize the entire 120-state W33-sensitive clock interaction on a genuine thermodynamic spatial family; seek a nontrivial phase only after extrapolation and a specified microscopic Hamiltonian.
4. Construct an actual locally gapped 2D model carrying native Jones generators and compute a bona fide nonzero chiral/bulk-boundary invariant, rather than globally conjugated Bloch states.
5. Test a 3+1D Lorentzian tetrad/spin-connection theory with first-class constraints, Ward identities, and propagating spin-two modes, avoiding the hand-chosen spatial and conformal substrates.

Reproduce from the repository root:

    python -m analysis.w33_20261031_same_subgroup_ambient_lift_audit
    python -m analysis.w33_20261031_full_subgroup_GF5_representation
    python -m analysis.w33_20261031_quantum_geometry_eight_new_falsifiers
    python -m pytest -q tests/test_w33_20261031_quantum_geometry_eight_new_falsifiers.py

**Boundary:** Algebraic certificates over GF9 and GF5 are exact. Quantum and optical/metric models carry clearly stated assumptions. Nothing in this report establishes physical particles, Planck constants, an anomaly-free Standard Model, a tested topological material, or a theory of everything.
