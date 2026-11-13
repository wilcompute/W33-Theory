# 2026-11-13 — exact compact C4, corrected cubic clock, Fermat sections, and five-front falsification

**Status:** Independent finite mathematics with executable integer/rational certificates, not a derivation of observed physics. All code is scoped to the fixed repository canonical 45-term signed cubic and the H27 address table. The user's parallel assistant's uncommitted projection/no-go/clock claims were hypotheses to reproduce, not treated as source data.

## Parent repo, novelty checks, and critical coordinate correction

Start after master 557aa6b5b2d67862c80bd72fb29465e9024c53a1. Important parents: analysis/toe_20261108_exact_signed_cubic_stabilizer.py (78 exact cubic stabilizers and simple coroots); analysis/toe_20261113_chiral_null_order3_gate.py (original D^3=-27D); data/w33_e6id_current_h27_gauge_bridge.json (specific history-to-E6 address bijection); analysis/toe_20261113_h27_albert_cubic_coordinate_reconstruction.py (previous signed detA+detB+detC-trABC); analysis/w33_pass11054_cubic_jacobian_skew_orthogonal_flow.py (a distinct 81-dimensional Jacobian skew family, NOT the current 27D compact stabilizer); analysis/w33_pass12077_clock_dynamics_chooses_e6.py (different E8 clock-condensate dynamics); corrected size-eight MUB rank-code search.

The prior direct-compatibility script mistakenly permuted only **rows** of the 27x27 chiral matrix when converting history indices to E6 indices. A change of basis must conjugate **both**:
M_E6[i,j] = M_hist[history(E6_i),history(E6_j)].
Replaying the fixed code changes the first seven integer cubic-image numerators from [46,-32,-2,4,-2,28,1] to [46,28,-5,76,-2,-5,40]. Both reject the naive signed cubic automorphism, but ONLY the latter are values for a consistently conjugated operator. The original leading 46/729 happens to remain unchanged and is not proof the rest of the old computation was right. Tracked source, tracked JSON, and an explicit independent erratum producer were updated together.

## Exact 36-packet theorem: skew E6 compact subalgebra

From the 72 exact non-Cartan root generators of the cubic stabilizer, form K_r=E_r-E_r^T, pairing opposite roots. These reduce to **36** independent matrices. Each K_r has exactly six disjoint signed two-coordinate edges, satisfies
K_r^T=-K_r, K_r^3=-K_r, rank(K_r)=12,
and is cubic-infinitesimal-preserving (verified by differentiating all signed 45 monomials).

The six-edge supports of **distinct** K_r are disjoint. They cover 216 of the 351 possible undirected edges; 135 edge coordinates lie outside the entire 36D skew-compatible span. Orthogonality is exact: <K_r,K_s>_F=12 delta_rs. This is the structural reason the 36D skew stabilizer admits a sparse certificate.

Let D_E6 be the correctly doubly conjugated original skew clock, with 108 undirected null edges, rank8, Frobenius squared norm216. For each packet let
s_r = sum_{(i,j) upper in packet} D_E6[i,j] K_r[i,j].
The packet overlap census is 12 with zero old edges, 18 with two, six with three, and **none** with six. The direct projection is therefore

X_star = sum_r (s_r/6) K_r,

||X_star||_F² = (1/3) sum_r s_r² = 46/3,
||D_E6-X_star||_F² = 602/3,
||X_star||² / ||D||² = 23/324.

This exactly reproduces the supplied other assistant's nonzero-projection result **without** solving a dense 108-by-?? or 351-unknown least-squares system. The 108 original edge coefficients are individually constrained because no full six-edge packet is contained in that graph: if an X in this 36D space is supported on the original 108 edges, X=0. A stronger **sharp locality theorem** now follows: ANY NONZERO real-skew cubic-preserving X requires at least **three** edges outside the original 108-edge graph (the 36 packets have minimum three outside and distinct packets cannot cancel supports). Six individual packets attain the bound. This is specific to the fixed signed cubic, address map, Euclidean transpose, and 27 real coordinates.

## Explicit C4 identification; not an accidental 36

All 36 skew packets close under matrix commutators with integer structure constants: 360/630 unordered pairs have nonzero brackets. The computed 36x36 Killing matrix is negative definite. The generic adjoint centralizer has dimension four.

A clique of four exactly commuting skew packets supplies a Cartan basis. Simultaneously diagonalizing their adjoint actions reveals 32 nonzero joint roots: **24 D4-like vectors with two ±1 components**, and **eight all-four-sign ±1 vectors of a single parity class**. A four-vector Hadamard rotation takes them into 24 ordinary short roots ±e_i±e_j plus eight long roots ±2e_i. The combined integer adjoint matrix has exactly the predicted characteristic polynomial over Z (full polynomial identity independently checked via SymPy). The root system is **C4**. Hence the compact skew real Lie algebra is isomorphic to usp(8), the maximal compact algebra of split E6(6). This is an algebraic isomorphism, not yet a concrete 8D symplectic intertwiner or a physical gauge-field derivation.

The 24+8 root decomposition is an additional D4/triality clue: it is the D4 system together with one chirality of eight spinor-like long directions, seen here in a Hadamard-rotated compact root frame.

## Order-three torus exclusion and replacement clock

Use the repo-certified six simple coroots in the standard complex E6 27 representation and enumerate all 3^6=729 torus phase vectors. Exact 27-weight spectrum census:
(27,0,0),(0,27,0),(0,0,27): 1 each;
(15,6,6),(6,15,6),(6,6,15): 72 each;
(9,9,9): 510.
These are **points** in the 3-torsion torus, not conjugacy classes. The original 27-state U has spectrum (19,4,4), trace15; it is absent. By the standard conjugacy-to-maximal-torus theorem for connected complex algebraic groups, NO arbitrary similarity can put that exact order-three U in the connected complex E6 standard 27 representation.

An explicit alternative is K=one of the six locality-optimal skew root packets, so rank(K)=12 and K³=-K. The order-three finite pulse

V=I+(sqrt(3)/2)K+(3/2)K²

is SO(27), has eigenvalue multiplicities (15,6,6), trace9, V³=I and N(Vx)=N(x). The last identity is **not a numerical fit**: an exact coefficient-level expansion in Q(sqrt3) checks all cubic monomials. The pulse is six independent 120-degree rotations on two-mode subspaces, with 15 passthrough coordinates. It uses exactly three edges not in the original null graph.

## Translation and continuum falsifier

Conjugate the three 27-history translations of F3³ into the fixed E6 address gauge. Search all 36 cubic-compatible skew packets for combinations commuting with all three shifts. The resulting 1053x36 integer constraint matrix has full column rank 36 modulo BOTH 101 and 103; this proves rank36 over Q and R. Therefore **no nonzero real-skew cubic-preserving generator is homogeneous under the full original 27-history translation group** in this identification. Translation invariance plus nontrivial internal H27 gauge action, non-orthogonal E6 transformations, or an enlarged lattice/field representation are not excluded.

The compatible elementary clock can be scheduled as six pair-rotations in one externally imposed layer: 2x27=54 time-labeled nodes and 39 temporal arrows (12 active input modes have two nonzero output amplitudes each, and 15 unchanged modes have one). This is a DAG of operations, **not** a derived relativistic causal set. No Lorentz cone, gravitational action, scale hierarchy, or continuum limit is produced by the finite model.

## Six-leg Choi holographic trade-off across the 36 rank-12 clocks

Transport each candidate V back into the original 3x3x3 HISTORY tensor factorization, form its six-qutrit Choi vector, and check all C(6,3)=20 balanced three-vs-three bipartitions. The 36 root clocks split as:
- six with **3** new null-edge couplings and **4** maximally mixed cuts;
- eighteen with **4** new edges and **2** maximally mixed cuts;
- twelve with **6** new edges and **8** maximally mixed cuts.

The prior original incompatible chiral U had eight maximally mixed cuts. This is a rigorously enumerated Pareto **sample family**, not a complete optimization over the full E6 group. None of these data establishes a holographic entanglement wedge, complementary recovery, or an AME perfect tensor.

## Photonics: two-port implementation and honest model scope

On ONE photon encoded in 27 paths, any elementary compatible V needs six two-port beam-splitter rotation primitives, rather than the previous original-U compiler's six local qutrit Fourier layers plus CCZ-mode phases. The V eigenbasis contains 15 idle modes and six active pairs. Assuming power transmission eta in each active two-port and perfect passthrough elsewhere, uniformly distributed input probability has mean survival (15+12eta)/27. The conditional coherent input state fidelity for the uniform input is (15+12 sqrt(eta))²/[27(15+12eta)]. These are design-level equations, not measured fidelity numbers, and DO NOT construct deterministic non-Clifford gates across three separate photons.

## New outside-the-box result: explicit Fermat cubic realization and 72 six-dimensional coordinate sections

The signed 45-term cubic's two-section graph (connect labels that appear in a common monomial) has 27 vertices, regular degree10 and 135 edges. A coordinate span L obeys cubic polarization T(u,v,z)=0 for all u,v in L, arbitrary z exactly when no cubic monomial contains two distinct labels of L. Exhaustive clique enumeration of the graph complement gives **72 six-coordinate maximal null sections, 216 five-coordinate maximal null sections, no coordinate-supported seven-dimensional sections**. The 72 sixers split by the three b-fibres into 18 (0,3,3) and 54 (2,2,2) population patterns up to permuting fibres. This is a maximum among COORDINATE-SUPPORTED subspaces, not a global maximum among all linear null subspaces.

A wholly independent model now constructs **all 27 lines** on the Fermat cubic x0^3+x1^3+x2^3+x3^3=0: three coordinate pairings, with equations x_i+omega^p x_j=0 and x_k+omega^q x_l=0, p,q∈F3. All 351 pairwise line-intersection predicates use exact 4x4 determinants in Z[omega]. Their intersection graph has SRG parameters (27,10,1,5), and a concrete graph isomorphism to the repository's 45-triple E6 incidence graph **preserves the three nine-coordinate b-fibres** and all 45 tritangent triangles.

Enumerate all 27 diagonal cube-root coordinate scalings modulo global scalar and all 24 coordinate permutations. The 648 distinct projective transformations act exactly on the 27 lines and 72 sixers, generating **18- and 54-element sixer orbits**, with orbit membership distinguished precisely by the (0,3,3) versus (2,2,2) H27 sector profile.

This confirms the Fermat 18+54 result of Favacchio & Malara (arXiv:2608.23716, August 2026) by an independently derived full line-equation and orbit calculation, and explicitly identifies the Fermat 27-line configuration with our H27-fibred E6 45-triple incidence.

Crucial distinction: a subspace annihilating the POLARIZED LOWER-INDEX cubic is a finite *analogue* of the exceptional-field-theory section condition; one must STILL construct the appropriate upper-index dual invariant d^{MNK}, test the actual covariant section constraint, choose a physical polarization and build a valid action. E6 exceptional field theory already uses a 5+27 extended space with derivative section constraints and six physical internal coordinates (Hohm-Samtleben 2014), so none of the present geometry constitutes an independent derivation of that supergravity theory.

## Five-qubit size-eight MUB: substantially faster independent bounded search

The corrected symmetric rank-code S3 symmetry leaves two S2 representatives, 692 and 694. A new independent exact-cover engine uses integer bitsets instead of dense NumPy killer matrices, with valid sibling exclusion branching and sampled pivot selection (selection affects branch efficiency but not logical completeness). It explored **4,848,640** nodes for rep 692 and **5,506,048** for rep 694, over 10.35 million total, reaching a minimum of 24 uncovered extenders but finding no eight-set witness before the 45-second-per-representative budget. Both returned **UNDECIDED**, not a no-solution certificate; the global size-eight vs size-nine maximal Pauli MUB question remains open here. Prior n=3 controls and size-nine witness remain separately certified.

## References and publication boundaries

- Current repo's signed cubic and E6 root coroots, cited paths above (mathematical inputs).
- Hohm & Samtleben, *Exceptional field theory I: E6(6)-covariant form of M-theory and type IIB*, Phys Rev D 89 066016 (2014): https://arxiv.org/abs/1312.0614 .
- Musaev & Samtleben, *Fermions and supersymmetry in E6(6) exceptional field theory*, JHEP03(2015)027: https://link.springer.com/article/10.1007/JHEP03%282015%29027 .
- Favacchio & Malara (2026), *On the Geometry of Sixers on the Fermat Cubic Surface*: https://arxiv.org/abs/2608.23716 .
- Classical Schläfli configuration: https://www.ms.u-tokyo.ac.jp/models_e/27cubic_e.html ; https://mathworld.wolfram.com/SchlaefliGraph.html .
- Existing 2026 W33 optical compiler, cubic source, rank-code papers and code are explicitly differentiated above.

## Reproduction paths

Sources:
analysis/toe_20261113_e6_root_matching_projection_clock.py
analysis/toe_20261113_e6_c4_translation_holography.py
analysis/toe_20261113_albert_six_coordinate_sections.py
analysis/toe_20261113_fermat_cubic_h27_sixers.py
analysis/toe_20261113_e6_biaxial_address_compatibility_erratum.py
analysis/toe_20261113_fivequbit_size8_bitset_exactcover.py
analysis/toe_20261113_chiral_e6_cubic_compatibility.py (surgically corrected)
tests/test_toe_20261113_e6_fermat_clock_full.py

Machine certificates under data/toe_20261113_{e6_root_matching_projection_clock,e6_c4_compact_translation_holography,albert_six_coordinate_sections,fermat_cubic_h27_sixers,e6_biaxial_address_compatibility_erratum,fivequbit_two_s3_classes_bitset_search}.json and corrected earlier data/toe_20261113_chiral_e6_cubic_compatibility.json.

**Top five independent future steps:** (1) construct a complete 8D symplectic intertwiner for the compact usp8 identified in 27D, plus physical gauge dynamics; (2) use the explicit 648-element Fermat action and sixer orbit map to test dual upper-index E6 EFT section constraints without assuming spacetime; (3) build a translation-covariant or gauge-covariant continuum on an enlarged carrier and independently test Lorentz dispersion and anomaly cancellation; (4) simulate the six-two-port replacement optical clock with loss and a fault-tolerant logical code to test protected CCZ resource injection; (5) finish the two-orbit five-qubit size8 exact-cover search with an independently checkable complete no-solution certificate or a counterexample.

**Do not conflate:** compact C4 Lie isomorphism with physical USp8 gauging; signed cubic automorphism with actual gravity; Fermat incidence sixers with ExFT physical sections; one-photon multimode unitary with a scalable three-photon entangler; 10.35M nonwinning search nodes with a mathematical impossibility proof.
