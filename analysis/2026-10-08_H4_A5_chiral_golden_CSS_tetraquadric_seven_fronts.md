# Oct 8, 2026 — Seven-front W33/600-cell follow-through: chiral A5 Cayley doublet, exact golden-spectrum fusion, CSS hook audit, thermal partition, optical drift and tetraquadric singularity

**Status: executed, with exact positive results and explicit failures.** This packet follows the Oct 8 \`9369d26e9\` BC-helix / W33 binary-CSS / F20-equivariant bijection run. This is original finite algebra/engineering analysis, **not** proof of a Theory of Everything, completed 3+1D gravity, fault-tolerant hardware, a normalized quark/lepton mass, or a fabricated chip.

Scope: (1) actual 600-cell incidence selector, (2) quantum syndrome circuit, (3) gauge/gravitational dynamics, (4) photonic device protocol, (5) explicit tetraquadric/UV matter, plus (6) chiral outer automorphism and (7) rigorous spectral fusion. No Holotrade application files were changed.

## Repository archaeology and independent literature

Before developing, inspected latest parallel master commit \`c1596fdf8\` (Pass398 formula search), previous code \`analysis/w33_20261008_F20_A5_600cell_antipodal_bridge.py\`, \`analysis/w33_clifford_antipodal_a5_selector_group.py\`, \`analysis/w33_clifford_lr_spread_scheme_boundary.py\`, \`PART_MCCCCXVII_MCCCCXXXII_clifford_fibration_selector_verifier.py\`, \`analysis/w33_20261008_20apt_local_SWAP_schedule.py\`, the earlier 20-apartment code and Wilson Hamiltonian, previous finite-field tetraquadric pilot and June BT486 ring-torus theorem. Changes were built in a **new clean isolated worktree** \`research/bc600-next5-20261008\` from GitHub master, not the dirty original working directory or the older modified research worktree.

External checks:
- The actual 600-cell 20 Boerdijk–Coxeter ring decomposition and antipodal geometry: https://en.wikipedia.org/wiki/600-cell (background, not proof of the new A5 Cayley identity).
- Conjugacy classes of A5: 1 identity, 15 involutions, 20 order-three elements and **two separate order-five classes of 12**: https://www.math.columbia.edu/~harris/website/content/2-courses1/3-mathematics-gu4041-fall-2023/simplicityofa5.pdf .
- Clifford/stabilizer circuit simulations and graphlike detector modeling: https://github.com/quantumlib/Stim , https://pymatching.readthedocs.io/en/latest/toric-code-example.html . Stim and PyMatching were *not* installed on the user's Windows Python during this pass, so do **not** call this packet a Stim or detector-error-model simulation.

## Front 1 — 600-cell H4 antipodal incidence vs W33 60-edge line incidence: exact obstruction

From the repo's *actual* 120 H4 600-cell vertex coordinates and adjacency, quotient the antipodal pairs with \`antipodal_pair_index()\`. Its simple quotient graph has **60 vertices, 360 edges, degree 12, 600 triangles** (checked from the exact constructed coordinate graph); it is connected.

From the selected Oct 8 W33 20-apartment CW complex, form the line graph on its **60 qubit-carrying edges**: two qubits adjacent when their edges touch a CW vertex. Because the CW skeleton is cubic, the line graph has **60 vertices, 120 edges, degree 4, 40 triangles** and is connected. Thus their raw adjacency schemes cannot be isomorphic: degrees 12 vs 4, triangles 600 vs 40.

This is stronger than the previous single-BC-ring comparison, which compared 60 *faces* to 60 W33 *edges*. Here both are actual 60-address structures with their native geometric incidences: still unequal. The previous F20-equivariant **abstract address bijection** remains correct; it was never an incidence isomorphism. Distinguish the **single 30-tetra BC torus** (whose boundary CSS is [[90,2,3]]_2) from **all 60 antipodal 600-cell Clifford addresses** and their H4 geometry. The selected 20-apartment W33 code remains [[60,2,6]]_2.

Producer \`analysis/w33_20261008_H4_60_antipodal_incidence_obstruction.py\`, certificate \`data/w33_20261008_H4_60_antipodal_incidence_obstruction.json\`.

## Outside-box front 6 — the true 600-cell antipodal graph is a **normal Cayley graph of A5**

Independently construct the 60 Clifford group elements through the repo's \`clifford_antipodal_permutations()\`; each address is an exact degree-six permutation and the 60 permutations form **A5** under composition. Do *not* replace the actual 600-cell adjacency with an arbitrary Cayley graph.

For **every** of its 60 group elements \(\gamma\), act on the 60 addresses by \(L_\gamma(g)=\gamma g\) and by \(R_\gamma(g)=g\gamma\). Against the actual H4 graph, **every one of all 120 left/right translation maps preserves all 360 edges**. Therefore actual antipodal geometry is a *two-sided / normal Cayley graph*. The connection set \(C\) consists of the twelve vertices adjacent to identity. Verify each is order five, all form **one entire A5 conjugacy class of size 12**, and \(C=C^{-1}\).

\[
\boxed{\Gamma_+(H_4)=\mathrm{Cay}(A_5,C_{5a}),\quad
|V|=60,\quad \deg=12,\quad |E|=360.}
\]

There is another disjoint A5 conjugacy class \(C_{5b}\) of twelve order-five elements. It is exactly
\[
C_{5b}=\{g^2:g\in C_{5a}\}.
\]
It defines a **second edge-disjoint 12-regular graph** \(\Gamma_-=\mathrm{Cay}(A_5,C_{5b})\) on the same 60 group labels, with its own 360 edges. These are mathematically a chiral pair of normal Cayley relations; do not equate them with a physically measured polarization, handedness, CP operation or chirality of fermions.

Producer \`analysis/w33_20261008_H4_Clifford_A5_Cayley_audit.py\`; stronger generator \`analysis/w33_20261008_H4_A5_chiral_Cayley_pair.py\`, full certificates.

## Outside-box front 7 — the **order-four outer automorphism swaps** the two chiral graphs

Explicitly enumerate **all 720 permutations of six symbols**, testing conjugation normalizers of the *actual* 60 Clifford A5 subgroup. Exactly **120 permutations normalize A5**. Among them, 60 inner normalizers preserve \(C_{5a}\), while 60 outer normalizers exchange \(C_{5a}\leftrightarrow C_{5b}\).

A concrete order-four outer normalizer permutation of the six Clifford basis labels is
\[
h=[0,1,3,4,5,2]
\]
(the map \(2\to3\to4\to5\to2\), fixing 0 and 1). For a specific order-five generator \(r\in C_{5a}\), the program verifies **\(hrh^{-1}=r^2\)**. The induced group automorphism maps **all 360 original H4 edges to 360 edges in the disjoint mirror graph**, i.e. **no original edge remains in the same edge set under this outer operation**.

This directly links the prior W33 torus generator
\[
F_{20}=C_5{:}C_4,\quad srs^{-1}=r^2
\]
and its integral \(H^1(\mathbf Z)\) modular-S quarter-turn to the existence of an order-four generator which exchanges the two A5 5-cycle conjugacy classes. The algebraic relation is now **verified on the actual Clifford six-permutation representation**. It is *not* a constructed isomorphism of the W33 edge graph with either H4 graph: the latter have degree12 and the W33 edge graph degree4. It is a candidate for a *two-sheet or chiral-sector correspondence*, not yet a group equivariance bridge respecting stabilizer incidence.

Crucial: the outer automorphism **does not preserve** the single chosen H4 adjacency relation; it is an isomorphism between **two different** graphs. That distinction prevents an incorrect geometry-symmetry/CP claim.

Producer \`analysis/w33_20261008_H4_A5_chiral_Cayley_pair.py\`; \`data/w33_20261008_H4_A5_chiral_5cycle_normal_Cayley.json\`.

## Spectral payoff — **golden-ratio irrationality cancels upon chiral-class fusion**

In the five irreducible representations of A5 of dimensions \(1,3,3,4,5\), the class sum of twelve elements of \(C_{5a}\) is central; its eigenvalue on a dimension-\(d\) irrep is \(|C|\chi(g)/d\), with multiplicity \(d^2\) in the left regular module. Thus
\[
\operatorname{Spec} A_+
=\left\{12^1,\quad(2+2\sqrt5)^9,\quad
(2-2\sqrt5)^9,\quad(-3)^{16},\quad0^{25}\right\}.
\]
Same spectrum for \(A_-\) with the two inequivalent three-dimensional irreps interchanged. Upon summing the **disjoint** edge relations,
\[
\boxed{\operatorname{Spec}(A_++A_-)
=\{24^1,\;4^{18},\;(-6)^{16},\;0^{25}\}.}
\]

The union graph has 60 vertices and degree24, and **the golden-irrational splitting vanishes exactly**. Verify all three spectra directly from independently constructed 60×60 integer adjacency matrices by \`numpy.linalg.eigvalsh\` with max deviation below \(1.1\times10^{-14}\), plus exact 2nd/3rd spectral moment and edge-disjointness checks. Each chiral graph contains **600 triangles** (600 ≠ a proved canonical bijection to 600 tetrahedral cells). This is potentially a useful mathematical bridge between H4's golden-number sectors and W33's integral \(12,2,-4\) eigenvalues, but **not a derived physical mixing angle, mass or Planck-scale constant**.

Producer \`analysis/w33_20261008_H4_A5_golden_spectral_fusion.py\`, certificate \`data/w33_20261008_H4_A5_golden_spectrum_chiral_fusion.json\`.

## Front 2 — actual 60-qubit stabilizer extraction, 11 CNOT layers, exact single-fault hook audit

From the specific W33 CSS \(H_X\) (40 checks of weight3) and \(H_Z\) (20 checks of weight8), build the incidence bipartite graphs and **regularize** them to 60×60 bipartite multigraphs with dummy check edges. By repeated perfect matchings (constructive König edge-coloring), produce **three disjoint-data-qubit CNOT rounds for the 40 X-star checks** and **eight for the 20 Z-octagon checks**.

The ideal ancilla circuit uses **40 X ancillas, 20 Z ancillas, 120 X-check CNOTs +160 Z-check CNOTs =280 total**, 11 two-qubit CNOT layers, with each physical data qubit acted on at most once within each layer. *These are graph-coloring/readout-routing bounds under direct check-to-qubit connectivity*, not a native-device placement, verified Stim circuit, parallel detector graph or fault-tolerance threshold.

Adversarial propagation of a fault inserted at every possible position in the X-ancilla control / Z-ancilla target CNOT streams yields:
- For weight3 X stars, an ancilla-control X fault is **equivalent to weight ≤1** modulo the measured star stabilizer.
- For every weight8 Z face, an ancilla-target Z fault at the midpoint produces a four-data-qubit Z error, **not equivalent to any ≤3-weight Z error modulo the face stabilizer rowspace**. An exact 0,1,2,3 weight-coset lookup was used; the 20 weight-four hooks are **verified**, one per face. The full spectrum of **180 Z-ancilla insertion locations** contains 40 cases each of effective weight0,1,2,3 and **20 cases of weight4**.
- The ordinary code has \(d_Z=8\) and uniquely corrects Z weights≤3 in the ideal syndrome model, but the **naïve syndrome circuit has a single-fault propagation path to effective weight4**. A circuit-level proof of fault tolerance therefore requires flags, cat-state ancillas, careful spacetime decoding or other remedies. Do not quote a threshold yet.

Producer \`analysis/w33_20261008_60qubit_measurement_hook_audit.py\`, certificate with all 11 layers \`data/w33_20261008_60qubit_full_ancilla_measurement_hook_audit.json\`.

## Front 3 — exact all-eigenstate thermodynamics of the W33 commuting stabilizer Hamiltonian, and GR boundary

Old construction: \(H=-\sum_{v=1}^{40} A_v-\sum_{f=1}^{20}B_f\) with star rank39, face rank19; \(E_0=-60\), ground degeneracy \(4\), gap4.

Now compute **all 2^60 quantum states**, by joint eigenvalue sign-sector counting. There is one global product constraint in each family, so star-violation and plaquette-violation numbers \(k,j\) must be even. Each allowed full syndrome sector has **four logical states**:
\[
\boxed{g(E=-60+2(k+j))=4\binom{40}{k}\binom{20}{j},\qquad k,j\text{ even},}
\]
summed over repeated energies. Exact total degeneracy equals \(2^{60}=1,152,921,504,606,846,976\). There are exactly **31 energy levels**. Ground level \(E=-60\) has 4 states; first excited \(E=-56\) has **3880** states:
\(4[\binom{40}2+\binom{20}2]=4(780+190)\).

Its **entire finite-temperature partition function** is
\[
\boxed{Z(\beta)=4e^{60\beta}\,E_{40}(e^{-2\beta})\,E_{20}(e^{-2\beta}),\quad
E_n(t)=\frac{(1+t)^n+(1-t)^n}{2}.}
\]
Verified by summing every energy degeneracy and independently evaluating this product at five inverse temperatures. Finite-size partition functions are analytic in all finite real β, so **no finite-size thermodynamic phase transition**. This rigorous model has a gapped 60-qubit Hilbert space, not an ADM Hamiltonian/lapse-shift system, dynamical 3-metric, gravitons or a 3+1 spacetime. The five-front GR goal is explicitly **unresolved**: extending a fixed branched 2-complex to a correct continuum constraint algebra is a genuinely different construction.

Producer \`analysis/w33_20261008_20apt_exact_thermal_spectrum.py\` and \`data/w33_20261008_20apt_exact_thermal_spectrum.json\`.

## Front 4 — experimentally interpretable **correlated** coherent-pump angle miscalibration

Earlier source-independent 27-port graph-hypothesis discriminator used ideal matching-layer unitary blocks and independent random angle errors. Here instantiate the **same signed systematic coupler angle shift δ in every matching, every repetition** (a strong coherent/correlated calibration drift) for \(\delta\in\{-0.002,-0.001,-0.0005,0,0.0005,0.001,0.002\}\) rad, at 36,72,144 stages. For each depth, calculate the exact simulated 27×27 unitary and output distributions for **both 27-port graph models**, verify unitarity and compute the unknown-port-label **sorted template minimum sup-norm separation** and its maximum drift from nominal.

Model-conditional key values (δ=0 vs the more severe |δ|=0.002):
- 36 stages: nominal margin **0.163232**, conservative nominal-template lower bound δ=-0.002 **0.154666**.
- 72 stages: nominal **0.227995**, δ=-0.002 bound **0.209589**.
- 144 stages: nominal **0.252208**, δ=-0.002 bound **0.214529**.

Depth72 retains the best estimated launched-photon count among these three under the stated per-layer survival 0.99, but its precise number is *expected* launches (not a 95% worst-case guaranteed budget), whereas the prior rigorous Hoeffding/binomial launch calculation supports guaranteed counts under independent physical-detection trials and bounded adversarial uncertainty assumptions. These synthetic correlated offsets are not a photonic laboratory measurement.

Required physically falsifiable calibration observables are: actual pairwise optical mixer angles, frequency-dependent phase and loss, the 27×27 transfer probability matrix under a single known input, detector efficiency per channel and common-mode drift. **No actual coupler, detector, or photonic chip was accessed.**

Producer \`analysis/w33_20261008_27port_correlated_coherent_drift.py\`; \`data/w33_20261008_27port_correlated_coherent_drift.json\`.

## Front 5 — exact compactification no-go: **avoiding all 48 Klein-four fixed points need not mean a smooth Calabi–Yau**

Earlier Oct8 reports correctly established that the 21-orbit invariant tetraquadric *linear system* has generic smooth free members by Bertini (Pass11742). They did **not** exhibit one selected integer polynomial with an exact characteristic-zero saturated Jacobian proof, normalized Yukawa or FI/anomaly-free proton-hexality vacuum.

Consider the *special symmetric pencil*
\[
F_{a,b}=\prod_{i=0}^3 S_i+a\prod_{i=0}^3D_i+b\prod_{i=0}^3 T_i,
\quad S_i=x_i^2+y_i^2,\quad D_i=x_i^2-y_i^2,\quad T_i=2x_i y_i .
\]
It is invariant under the simultaneous \(g:(x_i,y_i)\mapsto(x_i,-y_i)\) and \(h:(x_i,y_i)\mapsto(y_i,x_i)\). Calculate **all 48 nonidentity group-fixed ambient points** (16 for each of \(g,h,gh\)) symbolically. The invariant hypersurface avoids them all **if and only if**
\[
\boxed{a\ne\pm1,\qquad b\ne\pm1,\qquad a\ne\pm b.}
\]
Indeed its polynomial evaluations at these fixed sets are, up to units, \(1\pm a,\ 16(1\pm b),\ 16(a\pm b)\).

**New exact no-go:** take *b=0* and a=2. These inequalities hold, so **all 48 fixed points are avoided**. Yet the hypersurface is singular at the explicit point
\[
\boxed{(x_i:y_i)=(1:i),\ (1:-i),\ (1:1),\ (1:-1).}
\]
At that point the first two \(S_i\) factors vanish, while the last two \(D_i\) factors vanish. Thus \(F_{a,0}=0\) and all **four affine partial derivatives vanish**, for *every* coefficient \(a\). The entire two-term \(b=0\) subfamily is geometrically singular, even though many such members have a free Klein-four action on their points. This directly blocks an attractive-but-invalid shortcut in the physical vacuum program: **free group action does not imply smoothness**, and a singular quotient does not furnish the desired nonsingular Calabi–Yau vacuum.

The previously tested \(a=2,b=3\) candidate still avoids all fixed points but smoothness over \(\mathbf C\) is *not* established (mod7 pilot was nonunit). An FI-compatible anomaly-free physical P6 remnant and normalized holomorphic/HYM/harmonic Yukawa remain entirely open. This packet does not infer uncalculated fermion masses.

Producer \`analysis/w33_20261008_Klein_tetraquadric_pencil_nogo.py\`, certificate \`data/w33_20261008_Klein_tetraquadric_pencil_exact_nogo.json\`.

## OUTSIDE-BOX FRONT 8 — 120 perfect F20-equivariant W33 selectors *inside the paired 600-cell geometry*

The Cayley doublet prompted a much stronger test than comparing the raw 12-regular graph with the W33 4-regular line graph. The **union** of both chiral A5 Cayley relations has degree24 and adjacency between distinct group elements exactly when their relative product has order5. Crucially this *pair union* is invariant under the full order20 F20 permutation action, because odd outer automorphisms exchange the two individual 12-element five-cycle classes while preserving their union.

The previous selected 20-apartment W33 qubit-line graph \(L\) has 60 vertices and 120 edges (4-regular), with three free 20-element F20 vertex orbits. The coset torsor \(S_5/\langle(01)\rangle\) also has three free 20-element F20 orbits.

**Completely enumerate all F20-equivariant bijections for one fixed identification of F20 generators**: there are exactly \(3!\cdot20^3=\mathbf{48,000}\), selecting which three group orbits correspond and one freely chosen image in each target orbit. For every mapping, test all **120 W33 adjacency edges** against the 60-vertex degree24 *union* A5 order-five adjacency matrix. Result:
- **120 complete selectors** out of 48,000 map **all 120 W33 edges** into the 720-edge H4-chiral-pair union;
- the other 47,880 bijections have partial overlaps of 0,20,40,60,80,100 matching edges, with exact histogram in JSON. The **full exact overlap histogram** is
\[
\begin{array}{c|rrrrrrr}
\text{preserved of 120}&0&20&40&60&80&100&120\\
\hline
\#\text{equivariant maps}&1920&8688&15384&13920&6576&1392&120.
\end{array}
\]
- One complete witness uses orbit assignment [0,1,2] and anchor offsets [2,11,7]. It is a **bijection of all 60 qubit addresses**, preserving *every* W33 edge adjacency into the H4 union.

To ensure this is not only an abstract \(S_5\) label trick, independently build a **full explicit group isomorphism \(A_5\) on five symbols \(\to A_5\) on the actual six Clifford symbols**, generated by a 5-cycle and a 3-cycle with product order2, verifying **all 3,600 multiplication products**. Transport the 60 W33 code qubits by this isomorphism onto **actual 600-cell antipodal-pair indices**.

Under that concrete H4 coordinate address map:
\[
\boxed{120\ \text{W33 qubit adjacency edges}
=60\ \text{in actual }H4_{+}+60\ \text{in actual }H4_{-}.}
\]
The W33 order-five normalizer generator **preserves both colored edge sets**, while the order-four normalizer generator **exchanges them exactly**. This verifies the matched group relation \(srs^{-1}=r^2\) on *concrete chiral-colored H4 adjacency*. The chosen embedding is noncanonical because different orbit anchors and group-isomorphism choices exist; **not** all 48,000 maps work, and a *single* H4 chiral adjacency graph does not contain all W33 edges.

Detailed local color profile (per W33 qubit): 10 addresses have (4,0) \((+,-)\) neighbors, 10 have (0,4), 20 have (3,1), and 20 have (1,3). Therefore the embedding uses both chiralities at an explicitly controlled, nonuniform rate, not a uniform (2,2) local mixing.

**This directly addresses the user's BC/600-cell hypothesis with actual incidence:** it is a genuine **spanning 4-regular subgraph embedding of W33's 60-edge-qubit adjacency into the 24-regular union of the two actual 600-cell antipodal A5 class-5 graph relations.** It is *stronger* than the previous 60-address-only F20-set equivalence, and is compatible with the original W33 integral modular-S action exchanging the chiral edge relations. It does not identify the W33 point graph (40 vertices) with the H4 graph (60), nor imply a continuum physical interaction.

Producers:
\`analysis/w33_20261008_F20_48000_H4_chiral_selector_census.py\`,
\`analysis/w33_20261008_W33_H4_chiral_4regular_embedding.py\`;
certificates with all 120 perfectly mapped adjacencies, 60 address assignment and exhaustive histogram.

## OUTSIDE-BOX FRONT 9 — transport every quantum check support onto paired H4 geometry

The 120-edge embedding immediately upgrades to a concrete **quantum-check support geometry**. The W33 code's 40 vertex X checks are 40 **triangles** in the W33 qubit line graph: under the selected H4 embedding, all three edges of *every triangle* lie in one of the two chiral H4 graphs. Their plus-edge counts distribute exactly \(\{0:10,1:10,2:10,3:10\}\).

Likewise each of the 20 selected W33 octagonal 2-cells has a cyclic order of eight incident edge qubits, and each consecutive qubit pair is adjacent in the qubit line graph. Thus all 20 length-eight check-boundary paths become actual **eight-edge cycles in the paired H4 chiral adjacency**. Their plus-colored edge counts distribute exactly \(\{2:5,4:10,6:5\}\). This is a newly explicit 40-triangle/20-octagon chiral-support atlas on the actual 60 antipodal 600-cell addresses.

Transporting the 40 binary star and 20 octagon incidence vectors through this **same bijection** yields unchanged GF2 ranks 39 and 19, vanishing star-face Pauli commutators, and a formal \([[60,2,6]]_2\) CSS code with actual H4-address labels. The algebraic CSS code is **the same code under relabeling**; the new substantive property is that *every check support follows actual local edges of the chiral-paired H4 graph*.

**Boundaries**: the 20 *selected* octagon paths are not native tetrahedral 2-faces of the regular 600-cell, and a triangle of antipodal-pair addresses is not by itself a native 600-cell triangle. We have not constructed a CW subcomplex embedding of the W33 original 40-vertex 20-face complex into a 600-cell tetrahedral cell complex, nor shown a hardware coupler/ancilla layout that can measure those checks without the previously identified weight-four Z-hook faults. It is a **local graph-support** realization, not yet a topological/native-face or physical-fault-tolerant implementation.

Producer \`analysis/w33_20261008_H4_chiral_W33_CSS_check_cycles.py\`, certificate with all **40 labeled triangles and 20 labeled octagons**, each with explicit H4 antipodal labels and chiral edge-color strings.

---

## Validation boundaries / implications

All new producer scripts give deterministic JSON certificates, with source audit and counterexamples retained; the companion \`tests/test_w33_20261008_H4_A5_chiral_CSS_physics.py\` checks actual adjacency, both chiral classes, the exact numerical spectra, bipartite CNOT scheduling, hook signatures, thermal degeneracies, optical coherent drift and the exact singular witness. A combined prior suite includes the older F20, H27, pi1, photon and Pass10967 proton-vacuum guards. **Do not describe a locally passed pytest suite as hosted GitHub CI**; those statuses need separate verification. No files in Holotrade were changed; the pass concerns foundational math in W33-Theory.

### Five highest-value independent next steps

1. **Complete the W33↔H4/BC-ring CW lift:** classify the **120 now-proven perfect F20-equivariant 4-regular embeddings**, identify their stabilizer/orbits in the full H4 symmetry group, and test whether any of the 20 selected W33 octagonal face supports bounds a native 600-cell two-chain or corresponds to an actual 30-tetrahedron BC-ring cycle. The chiral-paired incidence map is proven; the native-cell/BC-helix lift is not.
2. **Fault-tolerant CSS circuits:** construct flagged or cat-state extraction for all 20 weight-eight faces, prove single-fault safe equivalence or fail, then implement true circuit-level noisy detector histories in Stim/PyMatching after checking compatibility and resource requirements. Optimize local 98–259 SWAP interval separately.
3. **Geometric/relativistic physics:** design an actual dynamical three-spatial-dimensional carrier with a consistent constraint algebra, continuum family and locality assumptions; compare its low-energy modes and stress-energy coupling with a tested relativistic field theory rather than calling a 2D commuting Hamiltonian gravity.
4. **Single-photon photonic falsification:** determine fabricated component topology, calibrate 27-port coupling/loss/phases and run single-source unknown-label discrimination on real measured data; require device uncertainties small enough to separate the two Hamiltonians.
5. **Explicit heterotic vacuum/Yukawa:** use an exact saturation backend (Singular/Macaulay2 or equivalent) to certify one explicit *three-term or full 21-orbit* invariant smooth polynomial; select anomaly/FI-compatible P6 and compute all kinetic normalization factors and physical Yukawas. The two-term pencil is ruled out.
