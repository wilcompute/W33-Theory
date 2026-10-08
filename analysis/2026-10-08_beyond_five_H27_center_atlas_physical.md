# 2026-10-08 — Beyond five: W33 center-atlas construction, H27/H13 module obstruction, photon information, P6 and tetraquadric

**Status:** Executed five physics/mathematics research fronts and three additional outside-the-box follow-throughs from current remote master. Reproducible exact certificates, one selected 45-apartment commuting atlas, an explicit 20-term integral homology relation, a 95%-confidence model-conditional single-source photonic discriminator, and separate geometric/anomaly exclusions. **No unified spacetime action, observed particle masses, gauged P6 vacuum, physical photonic device, or complete TOE.**

## Ground truth and novelty boundary

This pass checked all incoming parallel commits before starting from `91aa1642e` (newest concurrent Pass 398 formula search). Previously landed project results include:
- `analysis/BT744_tits_building_dictionary.md`: the 80-vertex W33 Levi incidence graph is the type-C2 Tits building; its 1,620 eight-cycles are **apartments**, transitively permuted by PSp(4,3), stabilizer of order 16. Every chamber belongs to 81 apartments, which form a basis for rank-81 Solomon–Tits/Steinberg first homology. **None of these apartment/81-action results is claimed new.**
- `analysis/2026-10-08_polar13_global_atlas_physical_followthrough.md`: exact **1,311,390 pair** census of apartment center commutators: 1,048,950 commuting pairs and 262,440 incompatible. Already owned.
- `analysis/2026-10-08_h27_h13_five_frontiers_bridge.md`: W33 13+27 polar split, exact chosen H27 subgroup of mod-3 reduction of a locally constructed 13D Heisenberg Lie radical; a group-level isomorphism does not identify representations. Already owned.
- `analysis/2026-10-08_five_frontiers_deep_jacobi_and_equivariance.md`: local C8 Jacobi Lie algebra \(\mathfrak{sp}(6,\mathbf Q)\ltimes\mathfrak h_{13}\). Already owned.
- Passes 369–371, 5105 and 11043: Payne/regular H27, program F3^3, trinification/operator H27 and 9D commutant dressing. Already owned.
- Passes 11742–11749: holomorphic Serre-residue Yukawa and source line bundles; no canonical kinetic metric. Already owned.

The increments **new here** are the structure of the **noncommutation graph on apartment centers**, concrete commuting subsets and their homology, induced chamber-basis incompatibilities, a physically different **permutation-invariant photon binary decision** rather than full instrument reconstruction, and new polar/P6/finite-field preflight certificates.

## 1. Exactly 324 incompatible apartments per apartment

For an apartment \(A\), let \(C_A=u_As_A^T\) denote the previously specified rank-one, point/line-signed operator in 80D Levi coordinates. By the previously proved exact identity,

\[
[C_A,C_B]=m(A,B)(u_As_B^T-u_Bs_A^T),\quad
m=|A_P\cap B_P|-|A_L\cap B_L|.
\]

The 1,620-vertex graph \(\Gamma_{\mathrm{bad}}\) joins \(A,B\) iff \([C_A,C_B]\neq0\). On **all** 1,311,390 unordered pairs, it is a regular connected graph of degree **324**, with **262,440 edges**, 1,048,950 compatible pairs and exactly **6,981,120 triangles**. This is an exact finite graph theorem, reproducible from bitmasks and adjacency intersections. The degree equality \(324=4\cdot81\) matches the abstract order of the earlier local \(U_{81}\rtimes V_4\) group. It does **not** yet prove a Cayley graph or group action: do not promote an equal order to an identification.

Using 180 seeded min-degree randomized greedy searches, the largest encountered **pairwise-commuting subset contains 45 apartments**. The certificate contains all 45 cycles by native 80-vertex indices, and an independent verifier confirms all \(\binom{45}{2}=990\) commutators vanish. It is **inclusion-maximal**, since no remaining apartment can be added without incompatibility. **45 is only a lower bound for the independence number, not a proven maximum.** That the cubic E6 surface has 45 tritangent planes is striking but supplies *no natural equivariant bijection*.

## 2. Homology of the 45-apartment atlas: 44 dimensions and one 20-term relation

Map each selected apartment to its oriented edge cycle in the integral \(\mathbb Z^{160}\) Levi edge-chain group, with orientation positive from point to line. Each chain has eight nonzero coefficients \(\pm1\), and its 80-component boundary vanishes. As the Levi graph is one-dimensional, there are no cellular 2-boundaries; these are actual elements of \(H_1\).

Exact ranks of the 45×160 edge matrix:
\[
\operatorname{rank}_{\mathbf F_2}=
\operatorname{rank}_{\mathbf F_3}=
\operatorname{rank}_{\mathbf F_5}=
\operatorname{rank}_{\mathbf Q}=\boxed{44}.
\]

The one-dimensional rational kernel has a primitive integral witness in the JSON certificate: precisely **20 nonzero coefficients**, comprising **11 positive and 9 negative unit coefficients**, canceling *on every one* of the 160 oriented Levi edges. Remaining 25 coefficients vanish. This is an exact combinatorial 20-apartment relation inside a compatible 45-apartment atlas. It does not identify a standard E6 tritangent relation or physical quantum codeword. The full homology dimension remains 81 (the earlier Solomon–Tits theorem).

## 3. A caution from the 81 apartments through one chamber

The already-established BT744 apartment basis through a fixed W33 chamber contains 81 apartments and spans the full 81D cycle space. Applying the **new** center-commutator relation within those 81 gives an induced incompatibility graph of degree **32** on 81 vertices. Of its 3,240 pairs, **1,296 are incompatible and 1,944 compatible**. Thus being a homology basis is **not** synonymous with being a commuting-center basis.

The induced graph is **not strongly regular**: adjacent vertex pairs have 11, 12, 13 or 23 common neighbors, depending on their intersection; nonadjacent pairs have 10, 11, 12 or 22. Its numerical symmetric adjacency spectrum is certified, with extremes **−10** and **32**. Although \(81\) and \(32\) resemble classical affine polar/Hamming parameters, guessing an SRG(81,32,13,12) would be false. The exact computation and failed SRG hypothesis are retained as a guard.

The relevant physical mathematical next question is whether a nontrivial **gauge connection or cocycle** can consistently patch these central directions despite noncommuting overlaps. No Dirac hypersurface-deformation bracket or general-relativity action has been derived.

## 4. Thirteen polar-plane points versus Heisenberg-13: exact rank-two carrier

In the actual W33 point-stabilizer action on the 13 polar-plane points, `analysis/w33_20261008_polar13_symplectic_module.py` had established that the invariant alternating-form space in the characteristic-three **13D permutation module** is one-dimensional and vanishes on its 12D augmentation submodule.

This pass exhibits that form explicitly, using the all-ones vector \(\mathbf1\) and the fixed-anchor indicator \(e_p\):

\[
\Omega=\mathbf1e_p^T-e_p\mathbf1^T\pmod3.
\]

The matrix has rank **2**, an **11D radical**, and **zero restriction** to the 12D augmentation module. The induced two-dimensional alternating quotient carries trivial point-stabilizer action on its defining coordinate functionals. Consequently, even the *surviving* 2D symplectic quotient is not automatically the nontrivial qutrit Pauli/Clifford module. These exact action tests **block the naive canonical** 13-points \(\leftrightarrow\) 13D Heisenberg Lie algebra identification. They do **not** disprove the previously constructed noncanonical order-27 subgroup isomorphism.

Standard finite-Heisenberg representation theory starts with a nondegenerate symplectic carrier and then forms a Heisenberg extension and its Weil representation; a bare vector-space dimension does not suffice. See [Weil representations over finite fields](https://doi.org/10.1016/j.jalgebra.2013.05.004).

## 5. A label-invariant *single-source* photon experiment, not a full 1,404-port scan

The earlier optical producer created exact graph Hamiltonians for the two nonisomorphic 27-port candidates and nine disjoint coupler layers; the next pass bounded a **full 54-input-port scan** at 95% confidence with 1,404 offdiagonal probabilities. That question is different from **binary topology discrimination**.

Here the device has one chosen, possibly unknown source port and arbitrary output relabeling. For each Trotter depth \(d\), compute all 27 one-source output distributions under both hypotheses from actual 27×27 unitary matrices \(U_d\), then sort the 27 components of each distribution. Let

\[
\delta_d=\min_{i,j\in\{1,\ldots,27\}}
\bigl\|\operatorname{sort}P_d(\cdot|i)
-\operatorname{sort}Q_d(\cdot|j)\bigr\|_\infty.
\]

Because sorting is nonexpansive in \(\ell_\infty\), an observed sorted 27-bin histogram within \(\delta_d/4\) of the true sorted output stays closer to the correct hypothesis template set than the other set. Hoeffding plus a union bound over 27 detector frequencies yields, **conditional on n independent successful detections**,

\[
n\ge \left\lceil\frac{8\log(2\cdot27/0.05)}{\delta_d^2}\right\rceil
\quad\Longrightarrow\quad
\Pr(\mathrm{correct\;classification})\ge0.95
\]

under *either* ideal hypothesis, **uniformly over source/output port relabelings**. This is a valid permutation-invariant classifier, not the per-pair Neyman–Pearson test. No unknown physical coupler strengths, systematic detector deviations or pulse correlations are included. Expected launched counts follow a supplied independent per-stage survival \(\eta\) and equal \(\lceil n/\eta^d\rceil\), *not* a 95%-guaranteed number of launches.

| Per-stage photon survival | Lowest expected launches across seven tested depths | Stages | Detected samples per single source |
|---:|---:|---:|---:|
| 98% | 4,342 | 36 | 2,098 |
| 99% | **2,217** | 72 | 1,075 |
| 99.5% | 1,543 | 72 | 1,075 |
| 99.9% | 1,016 | 144 | 879 |

At 99% survival and 72 stages the worst-case sorted-probability separation is **\(\delta\approx0.2279950\)**. The earlier full-scan design needed \(\sim150,894\) expected launches at its best tested depth, but that scan asked a *much stronger tomography question*. The present 2,217 expected launches address *binary hypothesis separation*, not reconstructing the transport matrix.

For comparison only, we also calculated simple-hypothesis Bhattacharyya affinities; their much smaller numbers are valid only if the actual pair of relabeled hypotheses is specified and its likelihood-ratio test can be implemented. **Those are not claimed as a uniform unknown-label experimental budget**. Resource-aware quantum hypothesis testing is an established topic; e.g. [Shallow-depth variational quantum hypothesis testing](https://doi.org/10.1103/PhysRevA.110.032424). This experiment is still simulated.

## 6. Proton hexality: mixed anomaly bookkeeping, no UV completion

For the **existing supplied MSSM+right-neutrino P6 charge table** \((0,1,5,4,1,3,5,1)\), the family-universal three-generation plus two Higgs-doublet integer-weighted sums are:

| Necessary sum (declared normalization) | P6 integer value |
|---|---:|
| SU(3)²-Z6 in 2T convention | 18 |
| SU(2)²-Z6 in 2T convention | 18 |
| Gravity-Z6 | 102 |
| U(1)Y²-Z6 with Y multiplied by 6 | 756 |
| U(1)Y-Z6² with Y multiplied by 6 | 288 |
| Z6³ | 1,854 |

All are multiples of 3, consistent with the previously required *necessary* modulo-3 checks. Because different discrete anomaly conventions, heavy exotics, hypercharge normalization, Green–Schwarz effects and UV thresholds alter sufficiency conditions, **this is not a proof of gauged proton hexality**. The additional \(X_3\) charges alone vanish on \(QLD^c\) and \(LLE^c\), while the full P6 assigns both charge 3 mod6; thus its \(Z_2\) factor does genuine additional selection-rule work. No FI-consistent U(1) remnant or E6-breaking model was built.

## 7. Tetraquadric: two further bad-reduction probes, no invented Yukawa metric

The previous packet supplied a fixed 21-term-invariant-coefficient tetraquadric polynomial candidate avoiding all 48 nontrivial ambient Klein-four fixed points in characteristic zero. The previous exact modular sieve found singular F3/F5/F7 rational reduction points (8,12,2).

This pass exhaustively evaluated the same polynomial and all four affine-chart partial derivatives over **all projective ambient rational points** of \(\bigl(\mathbf P^1(\mathbf F_p)\bigr)^4\) for new primes:

| Prime | Ambient projective rational points | Hypersurface rational points | Singular rational points |
|---:|---:|---:|---:|
| 11 | 20,736 | 1,838 | **2** |
| 13 | 38,416 | 2,848 | **4** |

Exact singular witnesses are included in the JSON certificate. These are definite **bad reductions** for the stated polynomial, but they say nothing decisive about smoothness of its \(\mathbf C\)-fiber. A mod-p *non-unit Jacobian ideal* does not prove an integer-coefficient polynomial is singular in characteristic zero. Smoothness over C, Hermitian Yang–Mills bundle metrics, normalized Yukawas, moduli fixing and mass predictions all remain open. Related numerical geometry work exists, e.g. [group-invariant Calabi–Yau metrics on tetraquadrics](https://doi.org/10.1088/2632-2153/adb4bb).

## Reproducible files and tests

- `analysis/w33_20261008_cycle_center_atlas_constructive.py` → `data/w33_20261008_cycle_center_atlas_constructive.json`.
- `analysis/w33_20261008_cycle_atlas_homology_rank.py` → `data/w33_20261008_cycle_atlas_homology_rank.json`.
- `analysis/w33_20261008_chamber81_commutator_graph.py` → `data/w33_20261008_chamber81_commutator_graph.json`.
- `analysis/w33_20261008_chamber_atlas_crosscheck.py`: independent 81-chamber apartment intersection check against BT744.
- `analysis/w33_20261008_photon_likelihood_information.py` → `data/w33_20261008_photon_likelihood_information.json`.
- `analysis/w33_20261008_polar13_hexality_smoothness_guards.py` → `data/w33_20261008_polar13_hexality_smoothness_guards.json`.
- `tests/test_w33_20261008_beyond_five_atlas_photon_guards.py`: direct independent verification of 45 compatibility, inclusion maximality, 20-cycle relation, chamber81 graph, sorted-histogram separation, discrete anomalies, polar rank and tetraquadric caveats.

## Highest-value hypotheses for next pass

A. Construct the **PSp-equivariant structure** of the apartment *noncommutation* graph, starting with known BT744 apartment transitivity; determine whether its 324 neighbors form natural orbits of the \(U_{81}\rtimes V_4\) stabilizer. Do not confuse group order with degree.

B. Test the 45-apartment commuting atlas / 20-apartment integral cycle relation for **E6-equivariance**, not just equality with 45 tritangent planes. A negative intertwiner obstruction is useful.

C. Build an actual gauge-connection/higher-cocycle for the 1,620-apartment atlas and test Jacobi/Bianchi/Dirac brackets before claims of gravity.

D. Move the permutation-invariant photon test to an **instrument-identified likelihood model** with coherent fabrication errors and detector nonuniformity, then optimize source choice and worst-case design.

E. Prove one fixed smooth free tetraquadric over the rationals/complexes by exact saturation/Jacobian computation, fix moduli and compute a canonical normalized Yukawa coupling; without this a physical mass is not determined.

## 8. Outside-the-box: an exact branched integral-homology torus from 20 compatible apartments

The primitive rational/integral relation in §2 suggests filling its 20 supporting apartment octagons as 2-cells. That is *not* an abstract pictorial analogy: the script
`analysis/w33_20261008_twenty_apartment_cell_homology.py` builds the actual integral cellular boundary matrices
\(\partial_2:\mathbf Z^{20}\to\mathbf Z^{60}\) and
\(\partial_1:\mathbf Z^{60}\to\mathbf Z^{40}\), verifies
\(\partial_1\partial_2=0\), and checks the primitive signed sum of the 20 octagons is killed by \(\partial_2\).

The union's 1-skeleton consists of precisely **40 vertices and 60 edges**, connected and **3-regular** (20 point vertices, 20 line vertices in the native Levi graph); the 2-complex has **20 octagonal faces**. The edge-to-face incidence multiplicity histogram is **40 edges in two faces, 20 edges in four faces**. This is a branched **non-manifold** CW 2-complex, *not* a topological torus or genuine regular torus tiling merely because the Euler characteristic equals zero.

The exact Smith normal forms of the two boundary maps are exceptionally clean:

\[
\operatorname{SNF}(\partial_1):1^{39}\oplus0,\qquad
\operatorname{SNF}(\partial_2):1^{19}\oplus0.
\]

Therefore, over the **integers** rather than only fields,

\[
\boxed{H_0\cong\mathbf Z,\quad H_1\cong\mathbf Z^2,\quad H_2\cong\mathbf Z,\qquad \chi=40-60+20=0.}
\]

The proof does **not** assume absence of torsion: every nonzero Smith invariant is explicitly one, so \(H_1\) has no torsion. This is an **integral homology torus** (same integral Betti/homology groups as \(T^2\)), while not homeomorphic to a torus because 20 edges have four 2-cell sheets. The selected seed and atlas choices make the construction presently **noncanonical**. No orientable-manifold genus, fundamental-group identity, spacetime topology or physical toroidal vacuum is claimed.

The link to the pre-existing Császár/Szilassi/Tomotope toroidal studies is thus a **testable geometric conjecture**, not a proof of topological equivalence: compute the complex's fundamental group, seek actual cellular covering/quotient maps and establish compatibility with the W33 symplectic group action.

Frozen certificate: `data/w33_20261008_twenty_apartment_cell_homology.json`.
