# 2026-10-08 — BC helices and the 20-apartment binary quantum code: five-front investigation and structural 600-cell bridge

**Evidence status:** Five distinct research fronts were attempted; the BC-helix hypothesis generated three exact computational results, a negative equivalence result, and a substantial algebraic explanation of the logical SWAP. A circuit-level fault-tolerance threshold, physical optical chip, UV-complete proton hexality, relativistic gravitational action and normalized Yukawa **were not obtained**. This document distinguishes mathematical theorems, executed finite experiments, numerical controls and missing physical derivations. All calculations use the actual repo's 20-apartment support and previous BC ring and Clifford selectors, not constructed-by-count 60-label guesses.

**Source baseline:** The isolated new worktree branch was forked from live master at parallel Pass398 corpus commit \`985fcf575\`, following user-facing CSS commit \`860607a27\`. The original working tree has unrelated local modifications; no reset/clean/stash operation used. The pre-existing BC and homological work was searched before writing new code.

## A. Recovered exact BC-helix owners and the correct hypotheses

The repo's **BT486–BT488**, \`analysis/2026-06-07_bc_ring_torus_lift.md\` and \`analysis/w33_bc_ring_boundary_torus.py\`, preceded the October construction by four months. Their model is the abstract cyclic 30-tetrahedron chain
\[
T_j=\{j,j+1,j+2,j+3\}\subset\mathbb Z/30.
\]
Its orientable **boundary** is a genuine triangulated genus-one surface with \((V,E,F)=(30,90,60)\), with the one-skeleton \(C_{30}^3=\mathrm{Circ}(30;\pm1,\pm2,\pm3)\). The graph automorphism group is the dihedral \(D_{30}\) of order 60; this was independently enumerated in the old verifier. It decomposes 90 edges into three step shells of 30 edges: \(C_{30}\), \(2C_{15}\), \(3C_{10}\).

The geometric literature describes the regular 600-cell as 20 cell-disjoint Boerdijk–Coxeter 30-tetrahedron rings, each bounded by three Clifford-parallel great decagons:
https://en.wikipedia.org/wiki/600-cell
https://en.wikipedia.org/wiki/Boerdijk%E2%80%93Coxeter_helix .
The historical verifier's *abstract* cyclic \(K_4\) ring is not itself a complete coordinate embedding into all 600 tetrahedral 600-cell facets; older BT1770/BT1779 explicitly distinguish these. Do not conflate an abstract model with a realized particular geometric Hopf fibration.

The *different* October **20-apartment CW** is built from 20 signed Levi eight-cycles, selected inside a commuting 45-apartment atlas. It has \((V,E,F)=(40,60,20)\), a trivalent Levi 1-skeleton, 40 edges incident to two octagons and 20 edges incident to four octagons. It is **branched, not a 2-manifold**, although its integral homology and fundamental group are those of the torus. Its setwise stabilizer under \(PSp(4,3)\) is \(F_{20}=C_5{:}C_4\). The October code lives on **60 edges**, while the old BC-ring boundary has **60 triangular faces**. These agree in number but are different chain degrees.

Other essential owners: \`analysis/BT808_600cell_icosahedral_orbits.md\` embeds the binary icosahedral \(2I\) into \(Sp(4,3)\), with W33 point orbits 20+20 and line orbits 10+30; \`analysis/w33_clifford_antipodal_a5_selector_group.py\` identifies the **60 antipodal Clifford 600-cell addresses** with an \(A_5\) torsor. It is a genuine A5 permutation carrier, but it is not automatically the 60 boundary triangles of a given BC ring.

## B. BC ring versus W33: derive both codes, not just a 60 count

Using the actual tetrahedra of \`w33_bc_ring_boundary_torus.py\`, list every boundary triangle and edge; each of 90 edges occurs in exactly two triangles, so \(\partial_1\partial_2=0\). Exact GF2 ranks:
\[
\mathrm{BC\ ring}:\quad n=90,\quad
\rank H_X=29,\quad\rank H_Z=59,\quad k=90-29-59=2 .
\]
Construct both primal-graph and face-dual-graph lifted four-sheet BFS problems and find nontrivial logical cycles. The **shortest primal/Z nontrivial** representative is the edge triangle \(0\!-\!1\!-\!2\!-\!0\), which is not a boundary 2-cell of this torus (the corresponding simplex is an internal tetrahedron face), of weight 3. The shortest dual/X representative has weight 6. Hence
\[
\boxed{\text{single abstract BC ring boundary code}=[[90,2,3]]_2,
\quad (d_X,d_Z)=(6,3).}
\]

Meanwhile the previous W33 selected 20-apartment proof yielded
\[
\boxed{\text{W33 apartment code}=[[60,2,6]]_2,\quad(d_X,d_Z)=(6,8).}
\]
Thus the two topologically genus-one carriers have different qubit counts and different protection distances. Topological equivalence does not preserve discretization-specific code distances.

Two explicit *incidence and symmetry no-gos*:
- The BC ring's triangle-dual adjacency graph has 60 vertices **degree 3**; the W33 CSS edge-qubit line graph has 60 vertices **degree 4**. Consequently the obvious equal-sized 60-set identification cannot preserve this graph incidence.
- The full BC torus boundary automorphism group \(D_{30}\) has **no order-four element**, whereas \(F_{20}\) has ten. Thus there is **no injective F20 realization within geometric automorphisms of a single BC ring**, and its order-four logical SWAP cannot be a geometric symmetry of that individual ring's boundary. This says nothing about other 600-cell *global* carriers or maps that do not preserve that one torus's full geometric structure.

Reproduction:
\`analysis/w33_20261008_BC_ring_CSS_comparison.py\`
and \`data/w33_20261008_BC_ring_CSS_vs_apartment.json\`.

## C. Positive breakthrough: exact F20-equivariant 60-address bridge through the A5/S5 coset torsor

The W33 support stabilizer acts **freely on all 60 selected edges** with exactly three orbits of length 20. Independently, the prior 600-cell Clifford antipodal construction exhibits exactly 60 labels carrying the regular action of \(A_5\). Their mere agreement at 60 is not yet an intertwiner.

Construct a *second* 60-object permutation carrier from
\[
S_5/\langle(0\ 1)\rangle,
\]
the right cosets of an **odd transposition**. Because the stabilizer has order2 and is disjoint from \(A_5\), \(A_5\) acts freely and transitively on all 60 cosets: the cosets form an **abstract A5 torsor**, just like the old Clifford antipodal selector.

Embed the Frobenius normalizer
\[
F_{20}=\mathrm{AGL}(1,5)\le S_5
\]
using \(r:x\mapsto x+1\), \(s:x\mapsto2x\) on \(\mathbf F_5\). These satisfy \(r^5=s^4=1,\ srs^{-1}=r^2\). No element of \(F_{20}\) is a lone transposition; hence its action on the 60 cosets is free, splitting into **three regular 20-element orbits**, exactly like the W33 edge action.

On the *actual W33* point-line permutations, select an order-five \(r\) and an order-four normalizer \(s\) with the same relation. Match the two 20-element groups by their normal forms \(r^a s^b\), then map three chosen W33 edge orbit representatives to three coset orbit representatives and extend by the group action. The program verifies:
- both exact 20-element group presentations and multiplication,
- three 20-element free orbits on both 60-point sets,
- bijection of all 60 points, **all 20×60=1,200 equivariance identities**,
- identifying each S5 coset with its unique *even* permutation yields 60 distinct \(A_5\) elements with group-order census \(1^1,2^{15},3^{20},5^{24}\),
- the **old *actual* Clifford antipodal address data** independently have exactly the same A5 element-order census.

Thus a genuine *abstract* \(F_{20}\)-equivariant 60-address bridge exists. It involves choices of generator orientation and one anchor in each of three free orbits; **it does not yet preserve the 600-cell's facet adjacency, helicity, Euclidean/H4 coordinates, 36 Clifford selector blocks or W33 CSS stabilizer checks**. An S5 coset permutation is not automatically a geometric symmetry of the 600-cell. This is the strongest positive representation-theoretic result of the BC hypothesis, not a completed H4↔W33 geometric equivalence.

Reproduction:
\`analysis/w33_20261008_F20_A5_600cell_antipodal_bridge.py\`
and \`data/w33_20261008_F20_A5_antipodal_60_bijection.json\`.

## D. Outside-box algebra: logical SWAP = reduction mod2 of integral torus modular S

The 20-apartment cell complex has **torsion-free \(H^1(X;\mathbf Z)=\mathbf Z^2\)**. Since the \(F_{20}\) action is induced by **genuine integral cellular automorphisms**, it yields a representation \(F_{20}\to GL_2(\mathbf Z)\). The Sylow5 subgroup acts trivially here because \(GL_2(\mathbf Z)\) has no element of order5.

Calculate the order-four generator's action directly on **40 vertex-coboundary and 20 oriented face-cochain matrices** modulo primes 2,3,5. With suitable cohomology bases the actual matrices are:
\[
S_2=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
S_3=\begin{pmatrix}0&2\\1&0\end{pmatrix},\quad
S_5=\begin{pmatrix}0&4\\1&0\end{pmatrix}.
\]
At odd primes \(S_p^2=-I\) and the action has order4, determinant1, trace0. Since the integral group element has order dividing4, nontrivial mod3 order4 implies the integral \(2\times2\) matrix has order4. Every integral rank-two lattice with an order-four automorphism is a rank-one module over \(\mathbf Z[i]\) and \(\mathbf Z[i]\) is a PID; up to an integral change of basis,
\[
\boxed{S_{\mathbf Z}=
\begin{pmatrix}0&-1\\1&0\end{pmatrix},\quad
S_{\mathbf Z}^2=-I,\ S_{\mathbf Z}^4=I.}
\]
The image of \(F_{20}\) on integral homology is therefore \(C_4\). Its mod2 reduction is the previously certified two-logical-qubit SWAP: **the logical qubit exchange is the binary shadow of a 90° modular transformation of the abstract torus homology lattice**.

One can equip that rank-two lattice with a C4-invariant positive quadratic form unique up to scale, algebraically identifying the corresponding square Gaussian torus \(\mathbf C/(\mathbf Z+i\mathbf Z)\). This does **not** establish a Euclidean embedding, flat physical metric, elliptic fibration of a 600-cell, string coupling or Einstein dynamics on the branched CW geometry.

Reproduction:
\`analysis/w33_20261008_20apt_integral_modular_S.py\`
and \`data/w33_20261008_20apt_integral_C4_modular_S.json\`.

## E. First requested front: an actual bounded-distance decoder and local logical gate route

From the stored binary stabilizer check matrices, build all low-weight error syndromes and select a minimum-weight representative; resolve any syndrome collisions by **exact stabilizer rowspace reduction**, not bitstring equality.

- All \(1+60+\binom{60}2+\binom{60}3=\mathbf{36,051}\) **Z-error patterns of weight≤3** are corrected (Z distance8).
- All \(1+60+\binom{60}2=\mathbf{1,831}\) **X-error patterns of weight≤2** are corrected (X distance6). These comprise 1,591 distinct X syndromes because 240 weight-two errors are stabilizer-equivalent collisions. Consequently *every* Pauli error on ≤2 physical qubits is correctable under the independent perfect X/Z syndrome model.
- A three-round majority-vote **syndrome readout toy** corrects at most one measurement bit flip *per stabilizer check* across the three rounds. It is not a fault-tolerant gate-extraction circuit or a threshold estimate.

For the exact logical-SWAP physical permutation, all 60 edge qubits form **15 disjoint four-cycles**. Thus the optimum unrestricted transposition count is 45. On the *selected W33 edge line-graph* degree-four nearest-neighbor coupling model, the sum of initial-to-final shortest-path distances for all 60 tokens is **196**, giving a rigorous lower bound of **98 adjacent SWAPs** (one SWAP moves at most two tokens one graph step each).

A constructive spanning-tree leaf-routing algorithm was executed for **all 60 root choices**. The best found **259 nearest-neighbor SWAPs** in **103 executable layers** of vertex-disjoint gates (each layer preserves gate dependencies). The code replays all 259 swaps and verifies the **exact same 60-element physical permutation**. Hence the physical routing cost is rigorously bracketed by **98≤adjacent SWAP count≤259** for this specified graph; 259 is not an optimum. Hardware connectivity, qubit geometry, ancilla readout, full circuit noise and thresholds remain open. Realistic graphlike detector-error models may use PyMatching/Stim, but its surface-code thresholds cannot be imported untested to this branched support (https://github.com/oscarhiggott/PyMatching).

Reproduction:
\`analysis/w33_20261008_20apt_decoder_routing.py\`,
\`analysis/w33_20261008_20apt_local_SWAP_schedule.py\` and JSON certificates.

## F. Second front: a Hamiltonian, exact energy gap, and a sharp gravity boundary

Place qubits on all 60 selected edges, choose 40 X vertex stars \(A_v\) and 20 Z octagons \(B_f\), and define the **explicit unit-coefficient stabilizer Hamiltonian**
\[
H=-\sum_{v=1}^{40}A_v-\sum_{f=1}^{20}B_f.
\]
All 800 nominal check pairs commute since \(\partial_1\partial_2=0\). Both check families have one independent global product relation, with ranks39 and19, hence exactly \(2^{60-39-19}=\mathbf4\) ground states, at energy \(E_0=-60\). Any nontrivial syndrome must violate at least two checks in a family (even parity), and one single-qubit Z flip produces two vertex defects, proving the **exact spectral gap is \(4\)** in the stated dimensionless coefficients. Every \(F_{20}\) cellular automorphism permutes stars among stars and plaquettes among plaquettes, hence the Hamiltonian is exactly **F20 invariant**. The shortest undetectable Pauli has weight6 as before.

This is a proper finite commuting-projector model, not an Einstein-Hilbert action or a dynamical 3+1-dimensional theory. A fixed 2-dimensional branched CW carrier has neither spatial 3-manifold data nor lapse/shift or a hypersurface-deformation constraint bracket. Such dynamics must be separately derived; no gravitational closure is claimed.

Reproduction: \`analysis/w33_20261008_20apt_Hamiltonian_Z6.py\` and JSON.

## G. Third front: device-level stochastic coherent coupler and detector model

The old ideal two-hypothesis 27-port transport experiment uses **nine disjoint matching layers per Trotter repetition** and a unitary \(2\times2\) beamsplitter rotation on each active pair. This pass instantiates *all* these unitary matrices, injects independent normally distributed angle offsets per pair and repetition and independent bounded per-output efficiency variations, renormalizes conditional detections, and checks \(U^\dagger U=I\). All 3 depths \(36,72,144\) and four declared fabrication regimes were evaluated for **12 seeded devices each**, 144 model comparisons total.

For 72 stages the exact nominal fully anonymous sorted-outcome minimum margin is \(0.227995\). Across 12 simulations at **angle std 0.001 rad per coupler and detector deviation ≤1%**, the **minimum perturbed-model margin remained positive**, about \(0.22794\); maximum nominal-template drift was about \(0.00418\). Other depths/severity results are retained in the certificate. This is sampled evidence of resilience, *not a confidence interval for fabrication yield*, nor an adversarial guarantee or measured optical transfer matrix. For a worst-case *bounded* error envelope the previous rigorously computed telescoping-norm and binomial/Hoeffding launch limits remain controlling, with 72-stage model-conditional baseline 2,538 launches for joint 95% success.

Reproduction:
\`analysis/w33_20261008_photon_calibrated_coupler_mc.py\`
and \`data/w33_20261008_photon_calibrated_coupler_mc.json\`.

## H. Fourth front: invariant flat Z6 cannot be the missing proton hexality

The previous exact \(F_{20}\) action on the specific 20-apartment torus cohomology gave
\[
H^1(X;\mathbf Z_2)^{F_{20}}\cong\mathbf Z_2,\quad
H^1(X;\mathbf Z_3)^{F_{20}}=0.
\]
Use Chinese remainder theorem on cochains with the **same group action**:
\[
H^1(X;\mathbf Z_6)^{F_{20}}
\cong H^1(X;\mathbf Z_2)^{F_{20}}\times H^1(X;\mathbf Z_3)^{F_{20}}
\cong\boxed{\mathbf Z_2}.
\]
In the chosen two-coordinate mod2 cohomology basis, these are \((0,0)\) and \((3,3)\) modulo6. There are **zero invariant elements of exact order 6**. Moreover the abstract group \(F_{20}\), of order20, cannot map onto \(\mathbf Z_6\) because 3 does not divide20. These are two distinct simple obstructions.

Thus a **fully F20-equivariant, ordinary flat line-Wilson holonomy** on this *specific* torus **cannot itself supply a full proton-hexality Z6**. This does *not* forbid some different non-flat gauge bundle, symmetry breaking, a larger UV extension, string-origin R-symmetry, or matter-field representation. The previous repo's FI-vacuum 0/215 non-R parity result (Pass10967) and its later retraction of an invalid non-prime-plane R-rule (Pass10974) remain decisive context. The prior exact MSSM-only non-R Z2 operator scan also vetoes all-five dangerous operators simultaneously: a lone parity is inadequate.

The new CRT/commuting-Hamiltonian certificate is in the Hamiltonian producer, and the old Pass10967 regression is intentionally included in combined tests. No anomaly-free UV vacuum or proton mass/lifetime follows.

## I. Fifth front: explicit free tetraquadric polynomial versus *smoothness and normalized Yukawa*

The repo *already* had a proof (Pass11742/Pass11750) that generic members of the 21-dimensional Klein-four-invariant tetraquadric system admit a smooth free quotient, plus a nonzero **holomorphic** cubic and certain line-bundle/Kähler data. It did **not** establish a full physical normalized Yukawa in the chosen vacuum.

For an actual explicit invariant integer candidate
\[
F=\prod_{i=0}^3(x_i^2+y_i^2)
 +2\prod_i(x_i^2-y_i^2)
 +3\prod_i(2x_i y_i)
\]
the previous pass exhaustively verified it avoids the 48 nonidentity ambient Klein-four fixed points over \(\mathbf C\), but its mod7 Jacobian ideal was nonunit in the first chart, so **good reduction at seven cannot certify its characteristic-zero smoothness**. This pass added an explicit **Gaussian-rational finite candidate sieve** over \(x_i/y_i\in\{0,1,-1,\pm i,\infty\}\): **1,296 projective-coordinate tuples checked**, **576 zeroes of F**, no critical zero among the finite set. That is a *negative finite-height search*, not proof of smoothness; it neither invalidates the polynomial nor certifies it. No exact characteristic-zero Jacobian saturation or physically normalized Yukawa was completed here.

The next reproducible effort requires an exact algebraic-geometry backend (e.g. Singular/Macaulay2) for the full saturated Jacobian, a specific smooth polynomial, actual moduli and Ricci-flat/HYM/harmonic field normalization. The published \`heteroticyukawas\` package (https://github.com/kitft/heteroticyukawas) explicitly requires moduli, line-bundle data and closed harmonic representatives; a holomorphic residue alone is insufficient. User-machine WSL has GAP but no detected Singular/sage command in default paths; no system software was installed or global environment changed.

Reproduction: \`analysis/w33_20261008_tetraquadric_Gaussian_singular_sieve.py\` and \`data/w33_20261008_tetraquadric_Gaussian_singular_sieve.json\`, plus prior \`analysis/w33_20261008_tetraquadric_sparse_good_reduction.py\`.

## Scientific boundaries and outside-the-box physics connections

- A single BC torus boundary and the selected W33 complex both have two logical qubits but **are not the same code or cellulation**. W33's mod-two SWAP is the reduction of a genuine order-four integral torus modular transformation; a BC single ring does not have an order-four geometric automorphism.
- The F20-equivariant 60-address bridge uses **S5/C2 ≅ A5 as a torsor**. It does not automatically identify a physical 600-cell rotation, tetrahedral cells, Clifford fibration blocks, local experimental couplers or standard 600-cell coordinates.
- An order-four integral automorphism of H1 permits a **square Gaussian complex structure** on the abstract rank-two lattice, not a microscopic metric or Ricci-flat geometry.
- Four ground states of a finite 60-qubit stabilizer Hamiltonian do not imply the 600-cell universe, a spacetime continuum, Standard Model chirality or a gravitational particle spectrum.
- Finite Monte Carlo device perturbations are distinct from the rigorous worst-case uncertainty bound and from physical device calibration.
- Full Z6 proton hexality needs actual UV charges and unbroken anomalously consistent gauge remnants. The selected torus invariant line holonomies supply at most Z2.
- A physically normalized Yukawa demands numerical kinetic inner products and a chosen smooth CY vacuum; the one explicit polynomial's status stays OPEN.

## Verification and how to rerun

Files are in \`analysis/w33_20261008_*.[py]\`, certificates in \`data/w33_20261008_*.json\`, and focused regression in \`tests/test_w33_20261008_BC60_five_physics_followthrough.py\`.

Commands from the repository root:

\`\`\`sh
python analysis/w33_20261008_BC_ring_CSS_comparison.py
python analysis/w33_20261008_F20_A5_600cell_antipodal_bridge.py
python analysis/w33_20261008_20apt_integral_modular_S.py
python analysis/w33_20261008_20apt_decoder_routing.py
python analysis/w33_20261008_20apt_local_SWAP_schedule.py
python analysis/w33_20261008_20apt_Hamiltonian_Z6.py
python analysis/w33_20261008_photon_calibrated_coupler_mc.py
python analysis/w33_20261008_tetraquadric_Gaussian_singular_sieve.py
python -m pytest -q tests/test_w33_20261008_BC60_five_physics_followthrough.py
\`\`\`

## Five best independent next steps

1. **Native BC/600-cell incidence selection:** transport the full 600-cell H4 coordinate facet graph and the 36 Clifford L/R blocks through the constructed F20-set bijection and test whether *any* orbit anchors preserve physically meaningful BC-ring or holonet incidence. Expect a negative result unless a new selector is found; no cardinality-only promotion.
2. **Real fault-tolerant readout and logical routing:** compile vertex-weight3 and octagon-weight8 check measurement with ancillas and circuit-level noisy measurement histories using Stim/PyMatching or equivalent. Optimize the current 98–259 NN SWAP interval and test performance under a local qubit-layout model.
3. **Non-topological dynamics/GR:** specify variable 3+1D spatial geometry and dynamical gauge/matter coupling, then derive any actual Einstein/ADM/Bianchi algebra in the enlarged system. The present commuting-projector 2D torus has a rigorous gap, but supplies no GR.
4. **Physical photonic falsifier:** model actual coupler transmission/phase distributions, calibrate a 27×27 transfer matrix and choose a single-source unknown-port measurement protocol with a verified experimental error budget. Demand falsifiable differences between the two transport Hamiltonians rather than count resonances.
5. **Heterotic vacuum and normalized Yukawa:** solve a characteristic-zero full Jacobian for one explicit invariant tetraquadric, specify an FI-compatible UV anomaly-free P6 or alternative proton protection, and numerically evaluate HYM/harmonic/kinetic normalization; keep each physical requirement separately falsifiable.
