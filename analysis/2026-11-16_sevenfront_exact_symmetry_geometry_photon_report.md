# Seven-front independent TOE research: exact W33 copy-number no-go, four-photon resource spectrum, target steering, genus-six sign constraints, D9 monopole global gauge, F8 mixed-state theorem, and photonic calibration

**Date:** 2026-11-16. **Repository:** wilcompute/W33-Theory, master. **Scope:** Exact finite-dimensional mathematical theorems, a conditional D9 compact-gauge-bundle construction, a necessary genus-six embedding test, and prospective synthetic photonic statistics. None is a physical Theory of Everything.

**Prior art and concurrency:** Follow-up to 41fdba48e (270-mediator two-stage channel, 24-plane affine gauge, D9 compensators, F8 rank-five census, drift). Latest parallel results reviewed include Pass12679 and Pass12681: near-tight code-space F8 certificates, torus order-4 orbit classification and Clifford-factorization warnings. These do **not** provide a full-64D global pure-state minimum. New files here do not overwrite those authors' sources.

## Result 1 — The minimum number of symmetric input copies is EXACTLY FOUR under PSp(4,3) equivariance

**Producer:** analysis/toe_20261116_W33_symmetry_minimal_fourcopy.py
**Certificate:** data/toe_20261116_W33_symmetry_minimal_fourcopy.json

Build W(3,3) from the 40 projective points of F3^4 with symplectic form x1*y2-x2*y1+x3*y4-x4*y3. Independently enumerate **45 induced K4,4 octets** by all independent four-sets and their four independent common neighbors; their disjointness graph has **27 maximal five-cliques**, which carry the Schläfli cubic-line adjacency A with eigenvalues 10^(1),1^(20),(-5)^(6).

Use projective symplectic transvections with axes e1,e2,e3,e4,e1+e3. Exact permutation closure yields a **25,920-element group**, PSp(4,3). All five act consistently on the 40 rays, 45 octets and 27 cubic-line labels.

For a bosonic symmetric input power Sym^d(C40), a linear map M:Sym^d(C40) -> C27 that intertwines the prescribed PSp(4,3) actions has a coefficient matrix constant on the G-orbits of pairs (unordered degree-d input multisets, output line labels). The full Hom_G space is spanned by their zero-one orbit incidence matrices.

EXACT exhaustive orbit counts:
- d=1: input 40, 1 input-output orbit, maximum rank of an orbital matrix 1.
- d=2: input 820, **5 input-output orbits**; each orbit matrix has zero six-sector eigenvalue and rank <=21; some attain 21.
- d=3: input 11,480, **19 input-output orbits**; every one has zero six-sector eigenvalue and rank <=21; some attain 21.
- d=4: existing independently tested PSp4-equivariant 27x22680 map (extended by zero to Sym4) has **rank 27**, with Gram eigenvalues {2640^1,1344^20,1560^6}.

For each orbit matrix E, the exact integer Gram matrix E E^T is constant on the three Schläfli relations: diagonal=d0, adjacent=a, nonadjacent=b. The six-sector eigenvalue is **d0-5a+4b=0** for *every* one of 1+5+19 orbit matrices. Hence E^T P6=0 for the rank-six Schläfli projector P6=(3I-3A+J)/18. Arbitrary complex linear combinations also kill this six-dimensional sector.

**Theorem:** Degree four is the minimum bosonic copy number giving an exact full-rank PSp4-equivariant linear map from Sym^d(C40) to the specified 27-dimensional permutation representation. This improves the previous weaker no-go, which only ruled out the 45-octet-factored quadratic map. The claim is NOT universal across non-equivariant protocols, ancilla representations, different target labels, or all physical quantum computers. It is independent of assumptions about optics, Hamiltonians or emergent gauge fields.

## Result 2 — Exact entanglement spectrum of the perfect four-photon resource

**Producer:** analysis/toe_20261116_W33_E6_perfect_source_1RDM.py
**Certificate:** data/toe_20261116_W33_E6_perfect_source_entanglement.json

The previous abstract two-stage compiler has an ideal perfectly transmitted four-photon ket |Psi*> supported on 22,680 distinct four-rail boson occupations. Its coefficient m(S) is 1 for 6,480 quartets, 2 for 16,200 quartets, and zero for repeated-mode occupations. The exact normalization is 6,480 + 4(16,200)=71,280.

Construct the normalized single-particle reduced density gamma1 without floating-point arithmetic. Define H_pq=sum_{|T|=3} m(T union {p}) m(T union {q}); then gamma1=H/(4*71280). The **integer matrix** is H_diag=7,128, H_adj_W33=1,836, H_nonadj_W33=2,160. The W33 strongly regular graph has adjacency eigenvalues 12^1,2^24,(-4)^15; hence

spec(gamma1) = { (27/88)^1, (1/66)^24, (29/1320)^15 }.

All 40 eigenvalues are strictly positive; Tr(gamma1^2)=**194/1815 ≈0.1068870523**. The state cannot be an identical product |psi>^tensor4. In fact, monotonicity of pure-state fidelity under tracing out three bosons gives

|<psi^tensor4 | Psi*>|^2 <= <psi|gamma1|psi> <= **27/88 ≈0.306818**,

for EVERY normalized single-rail superposition psi. The bound need not be attainable. The particular uniform coherent product overlap is exactly **2187/11000≈0.198818**, matching its previous abstract heralding probability. This is a quantified state-preparation resource obstacle; it does not prohibit using different four-photon separable input states, adaptive measurement or entangling sources.

## Result 3 — Universal target-specific output steering with exact rational success bounds

**Producer:** analysis/toe_20261116_W33_E6_target_steering.py
**Certificate:** data/toe_20261116_W33_E6_universal_target_steering.json

Let K be the optimally normalized four-copy success Kraus map. Its positive definite output Gram operator H=KKdag satisfies

H=P1+(28/55)P20+(13/22)P6,

where P1=J/27, P6=(3I-3A+J)/18 and P20=I-P1-P6. An exact 27x27 rational-matrix calculation verifies the spectral projectors and H^-1=P1+(55/28)P20+(22/13)P6.

For any desired unit output y in C27, the normalized four-photon antecedent

|Psi_y>= Kdag H^-1 |y> / sqrt(<y|H^-1|y>)

succeeds in producing y with probability p(y)=1/<y|H^-1|y>. Thus

28/55 <= p(y) <= 1;  p(one cubic-line basis label)=**91/170**;
p(uniform line superposition)=1; pure six-sector p=13/22.

The lower endpoint is attained on the 20D Schläfli sector, not merely a loose numerical bound. The construction requires **target-dependent coherent entangled source preparation** and does not transmit arbitrary unknown states or compile the hard U stage into optics. This exact full-output controllability is nevertheless a useful design certificate.

## Result 4 — Genus-six dual 12-plane realization as 528 determinant-sign constraints

**Producer:** analysis/toe_20261116_genus6_matroid_crossing_signs.py
**Certificate:** data/toe_20261116_genus6_oriented_matroid_face_crossing_signs.json

The Császár vertex-complete and Szilassi face-complete toroidal formulas both follow from Euler characteristic and complete adjacency. At the next admissible genus six, an abstract 12-vertex neighborly triangulation has (V,E,F)=(12,66,44); its dual has (44,66,12) and twelve hendecagonal faces. The 12 dual face planes admit the 24-parameter generic affine gauge derived in 41fdba48e.

This pass converts **local simplicity** of those face polygons into explicit sign predicates on 3x3 normal minors and 4x4 homogeneous plane minors. For planes H_i=(n_i,-d_i), write v_ijk for the intersection of planes i,j,k, and D3_ijk=det(n_i,n_j,n_k), D4_ijkm=det(H_i,H_j,H_k,H_m). Then

sign(H_m(v_ijk))=sign(D4_ijkm) * sign(D3_ijk).

Given two nonadjacent boundary edges of face i, supported by planes j and m, a proper crossing occurs iff the signs of H_m at BOTH endpoints of the first edge differ, AND the signs of H_j at BOTH endpoints of the second edge differ. This is an exact polynomial-sign test, with **no reconstructed vertex coordinates required**.

There are 44 nonadjacent boundary-edge pairs per 11-gonal face, therefore exactly **528 necessary no-crossing predicates** for the 12 faces. The verifier evaluates all **220 normal 3x3 minors and 495 homogeneous 4x4 minors** as exact fractions: no minor vanishes in the saved generic 12-plane candidate. It independently recovers the previous **eight** face self-crossings, distributed [1,0,1,1,1,0,0,2,0,2,0,0], and exports the eight violated clauses and a hash of all 528 tested conditions. This provides a concrete **SAT-oriented sign skeleton**, not a proof of representability or nonrealizability. Sign assignments still need rank-four oriented-matroid consistency and real 24-variable realizability; global intersections between different faces must also vanish.

**External distinction:** Schewe's genus-six **triangular primal** nonrealizability theorem (https://arxiv.org/abs/0801.2582) does NOT prove the nontriangular planar-faced **dual** impossible. Bokowski and Kevin H. (2025, https://www.mdpi.com/2073-8994/17/4/622) describe unsuccessful geometric searches for those duals.

## Result 5 — D9 magnetic compactification has a flux-parity global gauge extension

**Producer:** analysis/toe_20261116_D9_monopole_global_group.py
**Certificate:** data/toe_20261116_D9_monopole_global_gauge_parity.json

The prior D9 AdS5 x S² x S² classical magnetic background has six SO3xSO3 Killing Lie-algebra directions, with flux-compensating moment maps mu_i=f_i r_i² n_i. For a **compact U(1)** Maxwell gauge field with unit electric charge and properly quantized monopole flux, the first Chern numbers are n_i=(1/(2pi))integral_S2 F_i = 2 f_i r_i² in Z. Thus the moment maps are mu_i=(n_i/2)n_i_vec.

The charge-one monopole bundle O(n_i) over CP1 is SU2-equivariant. Its degree-|n_i| homogeneous-section representation shows that the center -I of SU2 acts on the fiber by (-1)^n_i. A 2pi rotation on the sphere is an identity in SO3 but can therefore be a **nontrivial gauge operation** when n_i is odd.

The global symmetry of the total U1 monopole bundle is the quotient

(SU2_1 x SU2_2 x U1)/<(-I,I,(-1)^n1),(I,-I,(-1)^n2)>,

with central kernel of order four. It splits as SO3xSO3xU1 only if both n_i are even; odd monopoles lock a rotation-center element to the gauge center. This was verified for **81 charge pairs** n1,n2 in [-4,4], including homogeneous-section center action and explicit Z2xZ2 kernel. Lie-algebra gauge counting is unchanged, and no E6 enhancement follows. This result depends on assuming compact U1 flux quantization and a unit-charge line bundle, not just the original source-free continuous classical Maxwell equations.

See SU2-equivariant monopole bundles L_m = SU2 x_U1 C_m and O(m) over CP1, e.g. https://arxiv.org/abs/hep-th/0504025 . A genuinely mixed vector/scalar Einstein–Maxwell KK diagonalization is still missing.

## Result 6 — Rigorous global mixed-state F8 zero-certainty interval

**Producer:** analysis/toe_20261116_F8_global_mixed_purity_zero_interval.py
**Certificate:** data/toe_20261116_F8_exact_mixed_purity_zero_interval.json

Work in the 64-dimensional six-qubit state space with the nine F8-regulus MUBs. Define C(rho)=sum_{567 covered nonidentity Paulis} Tr(rho P)^2 >=0. The prior rank-five commuting subgroup S has exactly 31 uncovered nonidentity Paulis, so its rank-two common code projector Pi_2 has normalized density rho0=Pi_2/2 satisfying C(rho0)=0 and Tr(rho0²)=1/2. This pass verifies its GF8 multiplication, field-trace symplectic isotropy and covered-label orthogonality independently (pure Python, no numerical optimizer).

For every t in [0,1], rho_t=(1-t)I64/64 + t Pi2/2 has

C(rho_t)=0,     Tr(rho_t²)=(1+31t²)/64.

The purity fills the entire interval [1/64,1/2]. Since C is nonnegative, this PROVES the **GLOBAL minimum C_min(p)=0 for every fixed purity 1/64 <= p <= 1/2**. This statement concerns all density matrices, not only one particular code, and is an exact achieved **lower bound**. It does NOT imply that p=1/2 is the largest purity permitting C=0, and it does not settle the full-C64 pure-state minimum.

For p>1/2 this same code provides an attainable (not necessarily optimal) upper C=6p-3. Depolarizing the independently known exact pure c8 witness gives another attainable upper C=c8(64p-1)/63, where c8=(47-32cos(2pi/9))/9≈2.4985086467. The two explicit upper families intersect at p=(189-c8)/(378-64c8)≈0.855137. This crossing is NOT a proved true mixed-state transition. In parallel Pass12681, order-four torus code-orbit classification advances the evidence about the global pure-state problem but does not substitute for a full-dimensional proof.

## Result 7 — Target-aware shot optimization under validated drift regularity

**Producer:** analysis/toe_20261116_photonic_grid_shot_optimizer.py
**Certificate:** data/toe_20261116_photonic_time_grid_calibration_optimizer.json

The preceding five-setting 16-rail GHZ witness was **synthetic** with Fhat≈0.96327484 and 99%-allocated five-setting statistical halfwidth≈0.03216538; two parity-flip rates had separate finite calibration uncertainty. Direct contrast calibration uses 16 weighted observables per time anchor and a per-detection weight range R≈1.05511. This pass optimizes the number of equispaced time anchors and accepted calibration samples **for an explicit target F_lower>0.90**; it does not ask for unnecessarily precise full-channel reconstruction.

For m=k+1 time anchors, under a separately established derivative bound L on each detector contrast, linear interpolation error ≤L/(2k). If a stronger separately established second-derivative bound M exists, the interpolation error ≤M/(8k²). With empirical maximum anchor-to-nominal contrast deviation required ≤D, per-contrast Hoeffding confidence radius r, and 16*m simultaneous reference means, a sufficient readout failure probability is

32*m*exp[-2*n*r²/R²] <= α_C=.0025.

Choose α_parity=.0025, α_five-settings=.005 so total α=.01. Keeping the original 147,556 accepted references per parity rate, with illustrative unmeasured assumptions D<=0.002, M=0.2 or L=0.12 in normalized experimental time:
- **Curvature**: optimal tested grid m=3 at times 0,1/2,1, n=3,117 accepted preparations per rail per anchor; 149,616 rail preparations plus 295,112 parity references = **444,728 total**. Conditional 99% synthetic F_lower=0.90005.
- **Lipschitz only**: optimal tested grid m=5 at times 0,1/4,1/2,3/4,1, n=5,126 per rail per anchor; 410,080 rail preparations plus parity references = **705,192 total**. Conditional 99% synthetic F_lower=0.90005.

The optimizer exhaustively evaluates grids m=2..40 under fixed α allocations and the chosen target. It does NOT establish globally optimal shot allocation across all possible calibration schedules, or actual hardware accuracy. Compared with the earlier 2.1-million two-epoch plan, the savings exploit a **relaxed precision target** and additional drift assumptions, not a free enhancement at equal precision. If actual observed anchor deviations exceed D, acquisition-window stationarity fails, or the derivative bounds are false, the claimed conditional witness threshold does not follow. **No experiment was conducted.**

## Reproduce

Run the seven producers in the order listed above, then:

    set PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
    py -3 -m pytest tests/test_toe_20261116_sevenfront_exact_controls.py -q --disable-warnings

The new regression suite independently replays all seven constructions and cross-checks certificates, exact ranks and arithmetic identities. Existing worktree changes and parallel files were not modified.

## Top five orthogonal next research experiments

1. **Strong minimal-degree theorem to circuit lower bounds:** extend the PSp4-equivariant 1/2/3-copy orbit obstruction to ancilla representations and physically constrained multiphoton LOQC gates. Determine if an optical resource breaks the assumed symmetry or requires genuine four-body coherence.
2. **Genus-six solver:** translate 528 determinant-sign clauses into an exact rank-four oriented-matroid + SAT formulation with Plücker constraints, and require real, planar polygon and global face-face nonintersection witnesses for all 59 dual combinatorial types.
3. **D9 dynamics and global gauge:** derive mixed metric–Maxwell vector/scalar operators on a flux-quantized product and verify all globally twisted gauge zero modes; use parity sectors of monopole harmonics for spectral completeness.
4. **F8 certainty–purity boundary:** find the largest density-matrix purity permitting all 567 covered Pauli expectations to vanish and prove or falsify a global full-64D pure-state lower bound, separate from the code-space degree-eight SOS.
5. **Hardware readout with measured drift:** use interleaved known-rail preparations to empirically bound temporal derivatives and reference fidelity, then optimize a prespecified 99% acceptance threshold without synthetic detector parameters.
