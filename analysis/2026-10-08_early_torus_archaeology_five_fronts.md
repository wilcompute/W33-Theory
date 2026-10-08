# 2026-10-08 — Early W33 torus archaeology and five independent fronts: Singer quotient, symmetry-protected flux, gauge curvature, photonic confidence and smooth tetraquadrics

**Scope.** This packet explicitly follows the user's recollection of *early torus work* and executes five subsequent investigations, with reproducible scripts, JSON certificates and independent tests. Every finite geometry and cohomology claim is distinguished from an assumed physical interpretation. The computations do **not** demonstrate a Theory of Everything, Einstein dynamics, UV-complete proton hexality, a manufactured 27-mode photon device or numerical fermion masses.

**Source branch:** isolated research branch from current `origin-https/master` after inspecting parallel formula-search commit `f0203a694`. Never reset/stash the user's dirty main working tree.

## 0. Verified early-history archaeology: there were multiple distinct tori

Git's history (not retrospective memory) dates the repo's root commit `b8961bcbd` to **2026-01-16**. Its earliest recovered explicit torus refinement program was **2026-03-09**, in commit `589d3069f`, `exploration/w33_torus_refinement_bridge.py`.

That is a **scaled external 4D discrete torus** `(C_n)^4`, with `n^2`-rescaled graph Laplacian and convergent positive-time heat trace for the external factor. It multiplies an internal W33 finite-factor heat trace through an almost-commutative product. **This was an externally supplied refinement geometry**, not a proof that W33's incidence building itself embeds as a toroidal surface.

On **May 18, 2026**, commit `a2c43a398` added `analysis/2026-05-18_toroidal_edge_data_parser.md`, based on the Császár (7 vertices, 21 edges, 14 triangles) and Szilassi (14 vertices, 21 edges, 7 hexagons) genus-one dual polyhedra, with several Euclidean coordinate/edge-length realizations. On **May 31**, `analysis/2026-05-31_heawood_eight_toroidal_face_systems.md` identified an orbit of **eight** Szilassi-style seven-hexagon face systems on the Heawood graph, with automorphism group index **336/42=8**.

On **June 11**, the separate `analysis/BT796_torus_cell_orbit_census.md` discussed **5,400 seven-mutually-skew-line** candidate cells in W33 and *conjectured* orbit decomposition 2,160+3,240. That split was explicitly **conjectural** in the original source; do not promote it to a verified orbit result without running its group action. Crucially, these 7-line sets are different carriers from a collection of Levi eight-cycles.

**October's new complex** is neither the March external `(C_n)^4` nor the May Császár/Szilassi embeddings nor the June 5,400 sets. It comes from a particular **20-octagon integral relation inside a 45-apartment commuting-center subset**, and earlier Oct 8 code already certified its 40 vertices, 60 edges, 20 octagonal 2-cells and exact `pi1=Z²`. The present work constructs a symmetry quotient and carries out explicit topological-to-gauge comparisons; it does not identify the three other old constructions by equal genus.

Prior related owners:
- `analysis/BT744_tits_building_dictionary.md`: W33's 1,620 Levi eight-cycles are apartments of the type-C2 spherical Tits building; 81 apartment cycles form a Steinberg basis.
- `analysis/w33_pass2474_f20_lifted_normalizer_hom.py`: the projective Sylow-5 normalizer is (F_{20}=C_5{:}C_4); its full symplectic preimage is a nonsplit (5{:}8) with central-sign obstruction.
- `analysis/w33_pass5617_z3_gauge_harper.py`: finite magnetic-translation (Z_3) phases and Harper-type physics were already investigated.
- `analysis/2026-10-08_twenty_apartment_torus_F20_H27_physical_packet.md`: prior selected CW torus, fundamental-group Tietze proof, F20 stabilizer, H27 holonomy census and imperfect optical budget.

## 1. Fivefold Singer quotient: precise small CW torus, *not* the Császár

A previously proved *actual* order-five subgroup (C_5\triangleleft F_{20}\subset PSp(4,3)) preserves the chosen 20 octagonal cells. Act on **all vertices, edges and faces**, not just their counts. Every orbit has exactly five elements. The quotient cellular data are therefore

\[
(40,60,20)/C_5\quad\longrightarrow\quad (8,12,4),\qquad\chi=8-12+4=0.
\]

The new exhaustive orbit generator explicitly builds the quotient's integer boundary matrices (\partial_1:\mathbf Z^{12}\to\mathbf Z^8) and (\partial_2:\mathbf Z^{4}\to\mathbf Z^{12}), verifies (\partial_1\partial_2=0), then computes Smith forms:

\[
\mathrm{SNF}(\partial_1)=\operatorname{diag}(1^7,0),\quad
\mathrm{SNF}(\partial_2)=\operatorname{diag}(1^3,0).
\]

So (H_0=\mathbf Z,H_1=\mathbf Z^2,H_2=\mathbf Z) with no torsion. The quotient has a 7-edge spanning tree; after its collapse it has five fundamental-group generators/four face relators. Three exact Tietze eliminations leave

\[
\pi_1(X/C_5)=\langle a,b\mid a b^{-1}a^{-1}b=1\rangle=\mathbf Z^2.
\]

Hence we have an *explicit regular fivefold CW covering* between two finite branched torus-homotopy complexes. The (C_5) action is free on open cells as well (no order-five automorphism of an octagon can stabilize and rotate/reflect an individual cell), so this really is a finite covering, not a merely numerical cell orbit ratio.

**Crucial corrected false lead:** I initially tested whether 8 vertices and 12 edges force the quotient skeleton to be (Q_3). **It is not the cube**, because **four of the 12 quotient edge orbits form parallel duplicate edges**. The quotient *simple* graph has **8 vertices and 8 edges and is exactly the cycle (C_8)**; four alternate cycle edges are doubled, producing 12 edges in the multigraph. Four projected octagonal face walks each traverse all eight simple cycle vertices but differ in the parallel-edge choice. This correction is stored in the JSON and tested. Matching 8/12 alone would have falsely merged the construction with the previous hypercube/knight-tour program.

It is also **not** the standard Császár seven-vertex polyhedral triangulation or the Heawood/Szilassi seven-hexagon map. Maps to them remain to be constructed, not assumed.

Producer: `analysis/w33_20261008_early_torus_singer_quotient.py`.
Certificate: `data/w33_20261008_early_torus_singer_quotient.json`.

## 2. Exact (F_{20})-equivariance: electric Wilson classes disappear, magnetic class survives

The older (20)-face set is preserved by the exact Sylow-5 normalizer (F_{20}) (Pass 2474 comparison), not solely by (C_5). The present code acts on all 40 vertices, 60 oriented edges and 20 faces, then constructs invariant cellular cochains over (\mathbf F_3).

Because (3\nmid |F_{20}|=20), averaging is permitted: the invariant-cochain complex computes the invariant subspace of cohomology. The cochain ranks give:

| Group | Vertex orbit sizes | Edge orbit sizes | Face orbit sizes | Dimension (H^1(X;\mathbf F_3)^G) |
|---|---|---|---|---|
| Singer (C_5) | (5^8) | (5^{12}) | (5^4) | **2** |
| Full (F_{20}) | (20^2) | (20^3) | (5,5,10) | **0** |

The full group's **20 elements preserve the exact oriented top homology generator** (orientation character (+1) for every element). Thus

\[
\boxed{H^1(X;\mathbf F_3)^{C_5}=\mathbf F_3^2,\quad
H^1(X;\mathbf F_3)^{F_{20}}=0,\quad
H^2(X;\mathbf F_3)^{F_{20}}=\mathbf F_3.}
\]

This **corrects earlier prose** in which we guessed that the 20 faces formed two orbits of ten: the actual face orbit sizes are **5,5,10**. A single sampled face orbit of size ten never certified the remaining orbit count. Tests now lock the correct complete census.

**Physical significance, with a strict boundary:** nine flat (Z_3) Wilson-line characters exist before imposing this full symmetry, but only the trivial one is (F_{20})-invariant. Therefore an **unbroken-(F_{20})-equivariant Wilson character cannot independently supply** the nontrivial order-three (X_3) part of proposed proton hexality; a broken symmetry, different bundle, different matter carrier or UV gauge origin is required. Conversely the top mod-three flux cohomology class *is* symmetry invariant. This is a mathematical obstruction/selection rule, not a physical vacuum construction. Not all equivariant bundles or projective representations reduce to invariant line characters.

Producer: `analysis/w33_20261008_F20_torus_mod3_equivariance.py`.
Certificate: `data/w33_20261008_F20_torus_mod3_equivariance.json`.

## 3. Genuine finite (Z_3) lattice gauge cochains and flux obstruction

Place (a\in C^1(X;\mathbf F_3)=\mathbf F_3^{60}) on the 60 oriented links. Its plaquette field is (F=\delta a\in C^2(X;\mathbf F_3)=\mathbf F_3^{20}), with vertex gauge transformations (a\mapsto a+\delta\phi) for (\phi\in C^0(X;\mathbf F_3)=\mathbf F_3^{40}). Exact integer boundaries satisfy (\partial_1\partial_2=0); reduced mod three their ranks are

\[
\mathrm{rank}_3\partial_1=39,\qquad\mathrm{rank}_3\partial_2=19.
\]

The 60D link-space therefore has a 41D *flat* kernel, modulo the rank-39 vertex-gauge image, yielding

\[
\boxed{H^1(X;\mathbf F_3)=\mathbf F_3^2,\qquad\#\text{flat }Z_3\text{ gauge classes}=3^2=9.}
\]

The 20 signed face coefficients (w_i\in\{\pm1\}) of the primitive apartment relation impose one **necessary and sufficient** exact-curvature criterion

\[
F=\delta a \quad\Longleftrightarrow\quad
\sum_{i=1}^{20}w_i F_i=0\pmod3.
\]

Thus *all* (3^{20}) formal plaquette flux assignments fall into three (H^2\cong\mathbf F_3) classes; only the (3^{19}) assignments in the zero-total-class hyperplane arise as globally exact link curvatures without external background. The corresponding ternary linear **face-curvature code is ([20,19,2]_3)**; a single plaquette flux cannot be exact, but an exactly constructed balanced two-plaquette flux can.

For illustration only, one can define a standard positive Euclidean (Z_3) Wilson-plaquette toy action

\[
S_{\mathrm{toy}}(a)=\sum_{i=1}^{20}\bigl[1-\cos(2\pi F_i/3)\bigr]
=\frac32\,\#\{i:F_i\neq0\}.
\]

Its smallest nonzero exact-curvature action is 3 in these **chosen dimensionless units**. This is not an observed Yang–Mills coupling or a derivation of Einstein/ADM dynamics. The nine flat torus sectors and three flux sectors are standard finite gauge-topological phenomena, here realized on the **specific W33-derived branched CW carrier**. The earlier Pass 5617 magnetic translation work remains independently valid.

Producer: `analysis/w33_20261008_torus_Z3_lattice_gauge.py`.
Certificate: `data/w33_20261008_torus_Z3_lattice_gauge.json`.

## 4. Photonic measurement: exact 95% *launch* budget, not only expected launches

Previous photonic passes compared two ideal 27-mode Hamiltonians with a label-invariant sorted-outcome classifier. The earlier 2,217 at 72 stages was **expected launches** to reach 1,075 conditional successes for a *conditional* 95%-error classifier. This is not itself a 95%-guaranteed launch count.

We now separately budget two sources of failure:

1. Hoeffding/union bound gives conditional misclassification probability at most **0.025** after (n\) successful detections, where (n=\lceil8\log(54/0.025)/\delta_{\rm robust}^2\rceil) and (\delta_{\rm robust}=(1-\beta)\delta-2\epsilon>0\).
2. For (N\) independent launched photons with per-stage survival (\eta=0.99\) through (d\) stages, each launch succeeds with probability (p=0.99^d\). Invert the **exact binomial survival tail** to find the minimum integer (N\) satisfying \(\Pr[\mathrm{Binomial}(N,p)\ge n]\ge0.975\).

The union bound implies **total correct classification probability at least 0.95** under the supplied ideal transfer matrices, bounded errors and independent survival/detection model. Every candidate's minimality is checked using the binomial tail at (N-1).

| Declared uniform background (\beta\) | Per-outcome model mismatch (\epsilon\) | Best among tested 36/72/144 stages | Successful detections (n\) | Certified joint 95% launches (N\) |
|---:|---:|---:|---:|---:|
| 0 | 0 | 72 | 1,182 | **2,538** |
| 0.05 | 0.01 | 72 | 1,590 | **3,396** |
| 0.10 | 0.02 | 72 | 2,251 | **4,780** |
| 0.20 | 0.05 | 72 | 9,048 | **18,933** |

This is a **true model-conditional confidence statement about launched photons**, not lab calibration or device validation. It has not been measured. Unknown coherent multiport errors, source-pulse correlation, input uncertainty beyond label permutations and nonuniform detector response may void the assumptions. The optical design remains an experimental proposal rather than a physical prototype.

Producer: `analysis/w33_20261008_photon_binomial_launch_cert.py`.
Certificate: `data/w33_20261008_photon_binomial_launch_cert.json`.

## 5. Tetraquadric: rigorous *existence* of a smooth free Klein-four member (not explicit metric)

Earlier calculations tested one explicit 21-coefficient Klein-four-invariant polynomial of multidegree (2,2,2,2) in ( (\mathbf P^1)^4\). Several primes had singular reduction points, but **bad reduction does not imply the characteristic-zero polynomial is singular**, and bounded rational searches found no proof of smoothness.

This pass addresses a different, foundational question: whether the **entire invariant linear system** contains *some* smooth fixed-point-avoiding member. Under the stated diagonal sign-flip and simultaneous homogeneous-coordinate-swap Klein-four action, the invariant multidegree-(2,2,2,2) sections have **dimension 21**:

- 8 symmetric pairs of pure-square binary exponent monomials, `M_b + M_(1-b)`.
- 12 sections having exactly two (x_iy_i) factors, with the remaining two square factors symmetrized.
- 1 all-(x_iy_i) monomial.

We now prove **basepoint-freeness over (\mathbf C\)** explicitly. At any coordinate boundary, select a pure-square monomial using the nonzero homogeneous coordinate in each factor; its complementary monomial vanishes and the orbit-sum does not. Inside the dense torus, write (t_i=(x_i/y_i)^2\). If *all eight* pure-square paired sections vanish, the 0000 section gives (P=\prod_i t_i=-1\), and each singleton section forces (t_i^2=1\). Thus every (t_i=\pm1\), with an odd number negative. For every such four-sign assignment, choose a pair with product (+1\); the corresponding two-(x_iy_i)-factor invariant section evaluates to a nonzero multiple of (1+t_it_j=2\). All 80 noninterior support patterns and eight exceptional interior sign patterns are exhaustively encoded as witnesses.

There are therefore no common zeros of the 21 basis sections on the smooth ambient fourfold. **Bertini's theorem** over characteristic zero implies a generic invariant divisor is smooth. The finite Klein-four action has 48 nontrivial ambient fixed points (16 for each of the three nonidentity involutions); basepoint-freeness implies generic invariant divisors avoid all 48. Consequently

\[
\boxed{\text{Smooth, fixed-point-free invariant tetraquadrics exist over }\mathbf C.}
\]

This proof is an **existence theorem**, not an explicit smooth integer-coefficient polynomial certificate. It does not fix a physical vacuum; no normalized Yukawa or mass is computed. Additional verification of the quotient's holomorphic volume-form linearization and a specific physical line bundle/HYM vacuum remains necessary. For actual metric and Yukawa computations, compare the published `heteroticyukawas` numerical package (https://github.com/kitft/heteroticyukawas) and *Precision string phenomenology*, Phys. Rev. D 111, 086007 (2025), https://doi.org/10.1103/PhysRevD.111.086007 .

Producer: `analysis/w33_20261008_tetraquadric_free_Bertini_existence.py`.
Certificate: `data/w33_20261008_tetraquadric_free_Bertini_existence.json`.

## Scientific and source boundaries

- **Old March four-torus**: controlled external heat-trace family, not W33 incidence topology.
- **Old May Császár/Szilassi**: concrete genus-one cell embeddings, not the current 20 Levi apartments.
- **Old June BT796 5,400 sets**: different 7-skew-line combinatorics, with at least the displayed 2,160+3,240 split a *conjecture* in its original document.
- **Old BT744/Pass 2474/Pass 5617**: owns apartment/Steinberg, Sylow-5 normalizer, and magnetic translations, respectively.
- **New here**: explicit fivefold C5 CW covering down to an 8-cycle with four doubled alternate edges; corrected full F20 face-orbit census; invariant cohomology in degrees one and two; exact gauge/cohomology curvature code; 95%-joint photonic launch certificate; algebraic basepoint-free/Bertini smooth-free existence proof.

No continuum action, physical gauge scale, proton lifetime, Lorentzian metric, measured optical device, physically normalized fermion mass or complete theory is asserted. In particular the preserved invariant **magnetic (H^2\)** should not be conflated with a dynamically sourced physical monopole or GUT flux.

## Next five independent fronts

1. **C5 quotient and early toroidal maps:** construct an explicit chain map between the 8-cycle-with-alternating-doubles quotient and the May Császár/Heawood torus maps, verify degree, induced (H^1/H^2\) maps and F20 compatibility. A homotopy equivalence without an explicit cellular map is not an identification.
2. **Gauge dynamics and gravity:** add a physically defined local coupling and Wilson action beyond a kinematic toy, test curvature/gauge invariance plus Jacobi/Bianchi/ADM constraint closure and compare to previous local C8 center noncommutation obstruction.
3. **Photonic experiment:** build waveguide hardware transfer matrices and true port-dependent loss/detector calibration distributions, then recompute a conditional confidence budget under instrument-estimated uncertainties and compare to the 2,538 benchmark.
4. **UV proton hexality:** seek a (Z_3\) charge in an actual physical representation/bundle away from the full-F20-invariant torus Wilson sector (which has none), exhibit compatible (Z_2\), and prove mixed/cubic discrete anomalies and FI/Higgs constraints.
5. **Construct an explicitly certified smooth tetraquadric and physical Yukawa:** obtain a rational polynomial from the proven basepoint-free linear system, certify all characteristic-zero Jacobian charts or a globally smooth mod-p specialization, then fix moduli and compute numerical kinetic/HYM/harmonic normalization with error bounds.
