# 2026-10-08 — Eight-front TOE research: a genus-53 chiral W33 surface, F20 orbifold sphere, viable three-index CY bundle, and physical locality firewalls

**Status:** Five previously requested fronts were executed plus three additional outside-the-box analyses. Independent executable producers and frozen machine-readable certificates accompany each result. This report explicitly distinguishes mathematical discoveries, declared effective physical models, negative no-go tests, and uncompleted physical constructions. No Standard Model, local quantum gravity, experimental quantum computer, observed photonic chip, cosmological constants, or Theory of Everything has been derived.

## Parallel-work intake / precedence

At this pass's start, the live W33 master had newer parallel commits \`12af1f0df\`, \`32fe946a2\`, and \`f4ad72d98\` beyond our preceding master \`5975f1cbc\`. The large \`32fe946a2\` pass already implemented:
- Pass11767 exact rational \(\mathfrak{sl}_{78}\ltimes\mathfrak h_{157}\) global finite Levi scalar-current Lie algebra, **not** the gravitational Dirac algebra, plus branch/no-global-symplectic firewall.
- Pass11768 a **different** native H4 *product* Lorentzian metric, exact timelike hinge deficit, ADM minisuperspace coupled to an explicitly chosen W33 CSS energy source, and a static scale/lapse incompatibility plus unstable conditional excited equilibrium. **Do not reattribute any of those results to this pass**.
- Pass11758 numerical sampled metric/HYM/harmonic probes on the prior explicitly smooth \(X_{2,3}\); their finite-basis residuals do **not** supply normalized physical Yukawas or an anomaly-free spectrum.
This pass examined these scripts, built a new isolated research branch from fresh remote master and preserved the original checkout's unrelated modified files.

External prior-art context: tetraquadric \(\mathbf Z_2^2\) quotients with Hodge \((4,20)\) and heterotic Abelian line-bundle models occur in the literature. Neither their Hodge numbers nor the use of line-bundle rank-five sums is claimed new. Galassi, *Phys. Rev. D* 47 3254 (1993) already studied lapse and shift in Regge calculus; flag-QEC and repeated syndrome paradigms likewise have substantial prior art. New claims here are specifically the **checked selected 240-address chiral-face surgery**, its full finite symmetry/orbifold and the **specific explicit \(X_{2,3}\) bundle candidate / bounds**, not first invention of known general methods.

## Five original fronts executed

### 1. Full F20-equivariant chiral-face surgery: a genuine closed orientable genus-53 surface

The preceding four-sheeted chiral voltage cover is a connected 4-regular graph of **240 vertices and 480 edges**, with voltage group \(\mathbf Z_2^2\). Its 80 lifted X-star hexagons each cover every edge exactly once, and its original 80 lifted Z-check octagons cover **320 edges twice**, **160 not at all**. Attaching all faces produced incidence 3 or 1: not a 2-manifold.

**Independent exact repair:** The dual adjacency graph of the 80 octagonal faces is the disjoint union of **two bipartite, 4-regular components each with 40 vertices**. In each component select exactly one checkerboard color class. This retains **40 octagons**, covering each of the original 320 octagon-supported edges *exactly once*. The **160 previously uncovered edges** form **16 vertex-disjoint 10-cycles** (80 other vertices are isolated in the uncovered-edge subgraph). Attach these 16 as **decagons**. Retain all 80 X-star hexagons. The repaired finite CW 2-complex has
\[
\boxed{(V,E,F)=(240,480,136),\quad F=80F_6+40F_8+16F_{10},\quad\chi=-104.}
\]
All 480 edges have exactly two incident faces. The link at each of all **240 vertices** is a connected 4-cycle (one topological circle), proved by explicit oriented face incidences—not inferred from Euler characteristic alone. The graph is connected, so this is a genuine **connected closed 2-manifold**.

There are four independent checkerboard selections. The full cellular \(\mathbf F_2\) Betti numbers are \((1,106,1)\). An independently solved **integer face-orientation parity system** shows selections 0 and 3 are **orientable genus 53**, while selections 1 and 2 are **nonorientable genus 106**. Every choice preserves **all 20 elements of F20** as literal permutations of the 240 graph vertices, 480 edges and exactly the 136 selected faces. In the orientable selected atlas the entire F20 also **preserves the surface orientation**. This last check explicitly maps cyclic face boundary edge lists and solves the global orientation signs, rather than presuming it.

**Significant scope boundary:** This is a new formal finite abstract topological surface built from the **paired** native/mirror chiral line graph, **not a submanifold of the original native 600-cell**, **not** the earlier branched 20-apartment torus, and **not** equivalent to the original \([[60,2,6]]_2\) two-logical-qubit code. The ordinary toric code of an orientable genus53 surface instead has 106 logical qubits.

Key producers:
- \`analysis/w33_20261008_chiral_face_checkerboard_repair.py\`
- \`analysis/w33_20261008_chiral_surface_orientability_F20.py\`
with certificates \`data/w33_20261008_240chiral_face_selection_surface_repair.json\` and \`data/w33_20261008_240chiral_surface_genus_orientability_F20_certificate.json\`.

### 2. 13-layer [[60,2,6]] CSS syndrome: bounded two-fault diagnostic plus readout-only repetition control

Previous frozen original syndrome schedule had 60 data qubits, 80 syndrome/flag ancillas, 320 CNOT gates in 13 disjoint-gate layers. Its 7,641 selected single post-gate/preparation/idle/readout Pauli fault histories yield 2,039 unique joint keys (measured X/Z/flag and a subsequent *perfect* complete stabilizer syndrome), zero differing residual stabilizer cosets.

This pass exposed those raw single-fault linear Clifford signatures through a non-breaking optional \`include_records\` argument and performed **250,000** pair-XOR comparisons of *distinct recorded single-fault observation classes*, looking for different stabilizer cosets with identical total observation including a **perfect** future readout. **No conflict was found in that bounded search**. Those observations are a diagnostic only: the two fault locations were **not** independently reconstructed/verified, and the tested pair set is not exhaustive. This is explicitly **not** a proof of distance-four fault tolerance, a two-fault theorem, a noisy QEC decoder, or a physical logical failure threshold.

To isolate readout noise, implement an independent exact static-syndrome null-control model in which each of 80 measured syndrome/flag bits suffers an independent readout bit flip of probability \(p\), with *no gate/data noise and a constant true syndrome*. Majority vote of \(r\in\{1,3,5,7\}\) odd repeated readouts has
\[
P_r=\sum_{k=(r+1)/2}^r {r\choose k}p^k(1-p)^{r-k},
\quad P(\text{any of 80 wrong})=1-(1-P_r)^{80}.
\]
At \(p=.01\), any-bit wrong probabilities for \(r=(1,3,5,7)\) are approximately \((0.55248,\;0.02356,\;0.0007877,\;0.00002733)\). This is **not an actual repeated noisy 320-CNOT circuit simulation**: more gate operations may introduce additional faults, and data errors can evolve between rounds. The calculation is intentionally restricted to measuring the value of classical redundancy.

Producers:
\`analysis/w33_20261008_CSS_twofault_check.py\`,
\`analysis/w33_20261008_CSS_repeated_measurement_null_control.py\`,
\`data/w33_20261008_CSS13layer_twofault_diagnostic.json\`,
\`data/w33_20261008_CSS80check_repeated_readout_majority_exact.json\`. The existing source \`analysis/w33_20261008_full_CSS_13layer_singlefault.py\` was extended *only* with optional access to raw results; its default output and earlier guards remain unchanged.

### 3. Gravity–code locality interface: native-H4 versus chiral F20 exact obstruction

Parallel Pass11768 already constructs a product Lorentzian slab and a conditional homogeneous W33-code energy source. This pass instead tests the **missing equivariant local spatial kinetic operator** before a sourced local stress tensor could be defined. In the selected actual 600-cell antipodal address identification, partition the W33 60-address line-graph adjacency into 60 edges belonging to the **true native H4 class-5 adjacency** \((+)\) and 60 disjoint edges of its **nonnative mirror class** \((-)\). Let \(A_+,A_-\) be these 60×60 adjacency matrices.

Exact permutation conjugation on all 60 addresses gives:
\[
rA_\pm r^{-1}=A_\pm,\qquad sA_+s^{-1}=A_-,\quad sA_-s^{-1}=A_+,
\]
with F20 order-five generator \(r\) and order-four generator \(s\). Therefore within the real two-class hopping span,
\[
\boxed{aA_++bA_-\text{ is invariant under all }F_{20}\iff a=b.}
\]
The **unique** invariant line in this operator family is generated by \(A_++A_-\), with 4-regular Laplacian \(4I-A_+-A_-\). This necessarily includes the **mirror edges**, so is not the native 600-cell nearest-neighbor Laplacian. Hence retaining *both* strict native-H4 adjacency and the selected full F20 internal chiral exchange is impossible within this two-class ansatz; one must enlarge the geometric carrier, use a different representation, change the kinetic ansatz, or break the internal symmetry.

This is an exact restricted **symmetry-versus-native-locality** result, **not** a local Einstein constraint, continuum stress-energy tensor, no-go theorem for all H4 field theories, or an assertion that F20 is a physically exact symmetry.

The full-edge chain of the earlier nonmanifold 160-face CW complex is also found to be a **trivial** H1 class: all 480 edges form the boundary of the 80 hexagons. The issue was **integer edge-face incidence**, fixed by the genus-53 surgery; not an obstruction in mod2 homology. The earlier unsuccessful conjecture that the all-edge chain was nontrivial was deliberately rejected.

Producers \`analysis/w33_20261008_F20_chiral_locality_kinetic.py\` and \`analysis/w33_20261008_chiral_odd_edge_H1_F20_isometry.py\`; JSON same stems as frozen outputs in \`data/\`.

### 4. 27-port optical hypothesis: from **discrete detuning samples** to a **continuous interval** bound

Previous controlled known-source and labeled-detector optical discrimination had 36/72/144 two-mode-mixing layers, five common systematic detuning values \(\delta\in\{-0.002,-0.001,0,0.001,0.002\}\), uniform background \(\beta\), and per-hypothesis calibrated \(\ell^1\) error \(\epsilon\). Those *grid-only* 95% joint success model budgets included 18 launched photons at 36 layers with ideal noise, and 44 at \(\beta=.10,\epsilon=.01\).

**New rigorous gap closure:** Each disjoint-mode reciprocal two-mode stage \(U(\theta+\delta)\) has operator-norm detuning derivative bounded by 1; for \(L\) stages the product has \(\|\partial_\delta U\|_{\rm op}\le L\). Since measurement outcome probability total \(\ell^1\) distance is bounded by twice the pure-state vector norm distance, the nearest-point distance \(\Delta/2=0.0005\) introduces a per-hypothesis \(\ell^1\) uncertainty at most
\[
\boxed{\epsilon_{\rm total}=\epsilon+2L(0.0005).}
\]
Apply the Hellinger triangle bound to both hypotheses to get the conservative entire-interval overlap
\[
B_{\rm true}\le1-\max\bigl(0,\sqrt{1-B_{\rm grid}}-\sqrt{2\epsilon_{\rm total}}\bigr)^2.
\]
Recompute exact binomial survival launch thresholds. For 36 layers, continuous unknown \(\delta\) anywhere in \([-0.002,0.002]\), known source port23:
- \(\beta=0,\epsilon=0\): **62** launched modeled photons (vs just 18 for the five *fixed* grid values);
- \(\beta=.05,\epsilon=.01\): **111**;
- \(\beta=.10,\epsilon=.01\): **155**.
Other deeper models sometimes lose nontrivial certification under this conservative Lipschitz bound and correctly return **no finite bound**, not an invented number.

These are conditional sufficient limits for the mathematical device model, fixed equal-prior hypothesis set, independent postselected counts, uniform background, **known input and labeled outputs** and independently established \(\ell^1\) calibration radius. No actual chip measurements are performed, and the guarantee does not extend beyond the defined detuning interval or unknown-channel protocols.

Producer \`analysis/w33_20261008_photon_continuous_detuning_guard.py\`; certificate \`data/w33_20261008_photon_continuous_detuning_dark_TV_certificates.json\`.

### 5. Explicit CY(4,20) bundle pilot: exact topological **three-family index candidate**

Continue from the earlier proof of a smooth free Klein-four \(X_{2,3}/G\) tetraquadric Calabi–Yau with \((h^{1,1},h^{2,1})=(4,20)\), \(\pi_1=G=\mathbf Z_2^2\), cover Euler \(-128\), quotient Euler \(-32\), and \(c_2(TX)=4\sum_{i<j}H_iH_j\).

New deterministic seeded finite lattice search found **five distinct line-bundle multidegrees**
\[
\boxed{
\begin{pmatrix}
-1&1&0&0\\
0&-2&1&1\\
0&1&-2&1\\
0&-1&1&0\\
1&1&0&-2
\end{pmatrix}}
\]
and \(V=\oplus_{a=1}^5\mathcal O_X(n_a)\). Direct exact checks:
- \(\sum_a n_a=0\) in all four entries, so \(c_1(V)=0\), rank-five \(S(U(1)^5)\) holomorphic sum candidate;
- Each line-bundle degree sum \(\sum_i n_{ai}=0\); at the symmetric strictly positive Kähler class \(t=(1,1,1,1)\) each slope is **exactly zero**. Each rank-one holomorphic line is stable, so this split sum is **polystable at that Kähler point** (this does not select or approximate its Ricci-flat/HYM connection numerically);
- Each degree sum is even, satisfying the **selected** Klein-four projective commutator/linearization criterion for an individual ambient line bundle; equivariant structures still require explicit choice and verification for the exact physical gauge model;
- Exact Atiyah–Singer holomorphic Euler index on the cover \(\chi(X,V)=\sum_a\frac16\int_X c_1(L_a)^3=\frac12\int_X c_3(V)=-12\), using \(\int_X H_iH_jH_k=2\) for distinct \(i,j,k\); quotient index would be **\(-3\)** for a free equivariant descent, a **topological** three-net-family necessary condition, **not** a computed chiral particle spectrum;
- The four pairings \(\int_X(c_2(TX)-c_2(V))H_i\) are exactly \((6,18,14,14)\), all positive. This is a **necessary** four-nef-direction Bianchi/five-brane condition. It does not alone prove a genuine effective integral curve class or full anomaly/tadpole consistency.

Critically this candidate does **not** solve the earlier proton-hexality challenge: flat Abelian Wilson characters from \(\pi_1=\mathbf Z_2^2\) cannot supply order3 or order6. A physical gauge/Higgs remnant, full cohomological matter spectrum, freedom from exotics and dimension-four/five proton-decay operators, hypercharge Wilson breaking, Green–Schwarz conditions, heterotic Bianchi/five-branes, canonical kinetic metrics and harmonic Yukawas all remain **open**. The result is an exact **promising bundle-search input**, not an anomaly-free Standard Model.

Producer \`analysis/w33_20261008_CY_SU5_linebundle_index3_search.py\`; certificate \`data/w33_20261008_Klein_CY_SU5_linebundles_index3_candidates.json\`.

## Three independent outside-the-box ideas executed

### Outside box A: genus-53 surface's **F20 quotient is a 10-cone-point orbifold sphere**

From the explicit 240-vertex orientable genus53 atlas and its genuine all-20 orientation-preserving cellular F20 action, enumerate exact cell orbits:
\[
(f_0,f_1,f_2)_{/F20}=(12,24,14),\quad\chi=2.
\]
All vertices/edges have orbit size20. Faces split into 4 hexagon orbits of20, 6 octagon orbits of sizes \((5,5,5,5,10,10)\), and 4 decagon orbits of size4. Hence the underlying quotient is **topological sphere**, with **10 cyclic branch-point orbits of orders**
\[
\boxed{(2,2,4,4,4,4,5,5,5,5).}
\]
Exact Riemann–Hurwitz:
\[
2-2(53)=-104=20\left[2-2\left(1-\frac12\right)-4\left(1-\frac14\right)-4\left(1-\frac15\right)\right].
\]
The four order5 branch-point orbits are 16 decagon faces stabilized in 5fold cycles. This is a new explicit topological explanation for recurring 5fold symmetry *within the particular combinatorial construction*. It is **not** a predicted fundamental dimension or measured particle charge.

Producer \`analysis/w33_20261008_genus53_F20_orbifold.py\` and \`data/w33_20261008_chiral_genus53_F20_orbifold_C5_branching.json\`.

### Outside box B: exact **CY family duality** under chiral exchange, but **not** a same-vacuum symmetry

On each of the four \(\mathbf P^1\) coordinates act projectively by \(R:(x,y)\mapsto(x+y,x-y)\), the local Hadamard normalizer exchanging the two Klein generators. On \(S=x^2+y^2,D=x^2-y^2,T=2xy\), it gives \((S,D,T)\mapsto2(S,T,D)\). Hence for the explicit invariant tetraquadric family
\[
\boxed{R:\ F_{a,b}\mapsto16F_{b,a}.}
\]
It **exchanges** the certified free smooth \(F_{2,3}\) and its smooth isomorphic partner \(F_{3,2}\), but fails to act as an automorphism of the *specified defining polynomial* \(F_{2,3}\). In this **uniform-Hadamard ansatz**, a fixed family member would require \(a=b\), and then the original Klein \((gh)\)-fixed-point set intersects the hypersurface, making the quotient nonfree. This is a mathematically sharp reason a four-state algebraic chiral exchange need not correspond to an unbroken geometrical symmetry of one chosen CY vacuum. It does **not** rule out nonuniform, nonlinear, or moduli-space symmetries beyond this ansatz.

### Outside box C: the common **four-character Fourier representation** yields abstract SWAP, but no coupling

The logical Hilbert space of the \([[60,2,6]]_2\) code, the four deck voltages of the formal \(\mathbf Z_2^2\) cover, and the 4 complex Wilson-character states of \(\mathrm{Hom}(\pi_1(X/G),U(1))\simeq\mathbf Z_2^2\) are all four-dimensional vector spaces. Construct their **actual** 4×4 unitary Fourier matrix \(H_2\otimes H_2\), exchange involution \(P|i,j\rangle=|j,i\rangle\), and verify exactly:
\[
P(H_2\otimes H_2)=(H_2\otimes H_2)P,\quad
P X_1P=X_2,\quad P Z_1P=Z_2.
\]
The F20 C4 action on both 2-bit quotients has image order2 (SWAP), while C5 acts trivially. This is a **representation-level intertwiner**, not a physical derivation that the CY Wilson characters *are* W33 logical qubits. An actual interface requires a functorial, gauge-invariant operator map and a derivation of the action that preserves local dynamics; both are missing.

Shared producer \`analysis/w33_20261008_chiral_CY_duality_character_SWAP.py\`; certificate \`data/w33_20261008_chiral_CY_duality_Gcharacter_SWAP_no_go.json\`.

## The missing ingredient exposed by the eight experiments

There is a repeated mathematical theme, not yet a Theory of Everything: finite global symmetry acts naturally as a **permutation/Fourier transform on discrete topological sectors**, but it cannot simultaneously be regarded as **unbroken native-spacetime locality**, **a fixed CY vacuum automorphism**, and **a physical fault-tolerant quantum processor** without adding dynamical degrees of freedom or relaxing constraints.

Specifically: full F20 exchanges native H4 spatial adjacency with *nonnative* mirror adjacency; the natural chiral C4/Hadamard exchanges smooth CY polynomials \(F_{2,3}\leftrightarrow F_{3,2}\) rather than preserving one; and a legitimate 53-handle surface can now retain F20 only through checkerboard face surgery. These are **exact compatibility conditions** a future dynamical unification must satisfy. The putative missing piece may be a *moduli-dependent symmetry-breaking/duality transition*, but that is a **hypothesis**, not a recovered physical law.

## Top five independent next steps (nonsequential)

1. **Equivariant moduli dynamics:** Define one mathematically consistent field/moduli action on the paired CY vacua \(F_{2,3},F_{3,2}\), and test whether a domain wall carries the abstract SWAP/Fourier operation while preserving the Klein free quotient, the bundle's index and anomaly data. Reject if no equivariant bundle lift across the interpolating family.
2. **Genus53 surface quantum/code transport:** Construct the actual cellular X/Z incidence matrices for the repaired oriented surface, compare its \([[480,106,d]]_2\) toric-code subspaces and 106 homology generators to the original \([[60,2,6]]_2\) under an explicit chain map. Determine whether any 2D invariant subspace carries the earlier logical SWAP; do not infer one from matching four-state sectors.
3. **Noisy fault tolerance:** Replace perfect post-round syndrome in the bounded 2-fault diagnostic with actual 2-4 noisy repeated extraction rounds; verify distinct physical gate locations, flag readout faults, decoders and Monte Carlo scaling at real p. Install/verify Stim/PyMatching or independent detector-error-model backend before quoting any threshold.
4. **Local gravitational dynamics with chiral matter:** Go beyond the parallel product-Lorentzian ADM minisuperspace: specify a local stress tensor and measure/constraint algebra compatible with either the *chiral-doubled* kinetic geometry or controlled spontaneous F20 breaking. Test 4D hinge closure and discrete Bianchi/Regge identities independently of formal Lie-closure dimension6240.
5. **Heterotic index-three physical spectrum and optical device:** On the explicit five-line bundle candidate, calculate equivariant line-bundle cohomology, Higgs/exotic representations, full effective fivebrane class, anomaly cancellation and exact surviving proton-protection symmetry; separately benchmark the continuous-offset 27-port likelihood protocol against real calibrated measurements, not model-generated unitary matrices.

**Verification policy:** Every new analysis file has corresponding machine-generated JSON and regression checks; no unverified physical estimates are presented as measurements. Preserve parallel Pass11758-11768 ownership and all previous proofs. Do not call H4 native isometries what are only automorphisms of the chiral union graph.