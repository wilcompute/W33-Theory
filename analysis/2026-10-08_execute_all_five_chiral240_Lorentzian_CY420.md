# 2026-10-08 — Execute all five: F20 four-sheet chirality, 7,641 CSS faults, all-ratio Lorentzian H4, robust photon statistics, explicit smooth free CY (4,20)

**Scope/claim boundary:** Independent mathematics and simulation advances in all five requested directions. This is *not* a completed TOE, experimental device, complete quantum error-correction threshold, 4D Einstein gravity, anomaly-free string compactification or physical mass calculation. We preserve model inputs, explicit partial successes, negative obstructions and reproducible JSON certificates.

**Repository alignment:** Synced and inspected master, including parallel commit \`4610a53c7\` (Pass11767 global current algebra) after previous fundamental results \`85e2d7252\`. Built on a clean isolated research branch from the new remote master, preserving other researchers' dirty checkout files. Existing exact 600-cell coordinate generator, W33 selected 20-apartment CSS, paired chiral A5 Cayley bridge and optical matching schedules are authoritative rather than reimplemented approximately.

**External precedents**: Chao–Reichardt's flag-QEC framework (PRX Quantum 1, 010302, 2020), Lorentzian Regge calculus of simplicial hinges (Phys. Rev. D 47, 3254; Classical and Quantum Gravity 2024), standard Lefschetz hyperplane theorem/Chern-class formalism for CY hypersurfaces, published tetraquadric Z2xZ2 quotient Hodge classification. The novel claims below are explicitly checked against the project's finite coordinate data, not attributed to those papers.

## I. Connected 240-address Z2-squared four-sheet chiral voltage cover, with exact F20 action

Prior Oct8 certificates proved exactly 120 perfect F20-equivariant 60-address bijections embedding the W33 60-edge-qubit **line graph** into the union of two order5 A5 normal Cayley graph relations on the actual 600-cell antipodal address set, and proved that **no** such bijection embeds all 20 selected W33 Z octagons into the original native plus-only H4 adjacency. The 120 selectors split 108 with zero fully native octagons and 12 with five. Five quotient octagons have 16-edge lifts in the actual 120-vertex H4 geometry. **Do not erase that no-go**.

New solution to the **formal paired relation** problem: label every one of W33's 120 4-regular line-graph adjacency edges by an independent voltage in the group \(K=\mathbf Z_2^2\):
\[
c(e)=\begin{cases}(1,0),&e\in E_+\\(0,1),&e\in E_-.\end{cases}
\]
The voltage graph has vertices \((v,k)\) for \(v\in60\), \(k\in\mathbf Z_2^2\), and edge \((u,k)\sim(v,k+c(uv))\). Actual geometry produces exactly 60 plus and 60 minus edges. Full BFS confirms one **connected 240-vertex, 480-edge, 4-regular** graph.

Every selected W33 octagon contains an *even* number of plus and minus adjacency edges (histogram \(5\times(2,6),10\times(4,4),5\times(6,2)\)). Hence the **total Z2² voltage vanishes** and **all 20 octagon boundaries lift to closed length-eight loops in all four sheets**. Every W33 X-star support is a 3-edge line-graph triangle, necessarily has an odd number of plus or minus color edges; 20 triangles have voltage (1,0) and 20 voltage (0,1), and all four-sheet lifts are **length-six cycles**, not closed triangles.

The W33 F20 C5 generator preserves the colors and acts trivially on the voltage bits; its C4 generator exchanges the plus and minus class and *swaps the two Z2 coordinates*. Reconstruct the induced permutations of all 240 graph addresses and check **every 480 adjacency**, element orders \(r^5=s^4=1\), and the exact relation \(srs^{-1}=r^2\) on all 240 addresses. This is a genuine F20-equivariant 4-sheet **formal** covering graph—not a native 600-cell topological 4-fold cover, a photonic apparatus or proof of any spacetime structure.

**Critical follow-on topology:** Attach all four closed lifts of each of the 20 octagons as 80 formal 2-cells on the 240-vertex/480-edge graph. Exact GF2 cellular boundary ranks are \(\mathrm{rk}\,\partial_1=239\), \(\mathrm{rk}\,\partial_2=78\), with \(\partial_1\partial_2=0\). Thus
\[
\boxed{(V,E,F)=(240,480,80),\quad\chi=-160,\quad
(b_0,b_1,b_2)=(1,163,2).}
\]
All 80 boundary loops have eight distinct edges. However **160 lifted edges belong to zero octagons**, and **320 edges belong to exactly two**, so this two-complex is **not a closed 2-manifold**, and is not a lifted torus. Closure of Z-check paths is necessary but not sufficient for a physical CSS homological code or native H4 cell geometry.

Source/certificates:
\`analysis/w33_20261008_F20_chiral_Z2square_240cover.py\`
and \`data/w33_20261008_F20_chiral_Z2square_240voltage_cover.json\`;
\`analysis/w33_20261008_240sheet_chiral_CW_octagon_homology.py\`
and \`data/w33_20261008_chiral_240voltage_80octagon_CW_homology.json\`.

### Stronger full-CSS atlas test: all 80 lifted X-star hexagons plus all 80 Z-octagons still fail closed-manifold incidence

Since each original W33 3-edge star triangle has nonzero Z2² voltage of order 2, it lifts to **two distinct closed six-edge cycles** (not four independent cycles); all 40 stars therefore supply **80 X-check hexagons**. Every one of the 480 lifted graph edges lies in **exactly one X-star hexagon**. Now attach these 80 hexagonal 2-cells together with all **80 Z octagonal** 2-cells on the *same* formal 240-vertex cover, yielding
\[
(V,E,F)=(240,480,160),\quad\chi=-80,\quad
\mathrm{rk}(\partial_1,\partial_2)=(239,158),\quad
(b_0,b_1,b_2)=(1,83,2).
\]
The edge-face incidence histogram becomes **160 edges of incidence one and 320 edges of incidence three**: **not a single edge has the required incidence two for a closed 2-manifold**. All 160 chosen hexagon/octagon boundary chains are exact GF2 cycles; \(\partial_1\partial_2=0\) is verified. Thus even restoring *both* CSS check types as face attachments to this natural voltage carrier fails 2-manifold incidence. A more elaborate *branched, nonmanifold, higher-rank, or additional-face* construction is needed; the CSS code's operator commutation should not be confused with triangulated spacetime manifold gluing.

Producer \`analysis/w33_20261008_240sheet_CSS_hex_oct_manifold_no_go.py\`; frozen certificate \`data/w33_20261008_chiral_240cover_CSS_80hex_80oct_nonmanifold.json\`.

## II. Full 320-CNOT, 13-layer CSS stabilizer round: 7,641 single-fault scenarios, zero ideal follow-up ambiguities

Use previously frozen 3 data-disjoint X-check layers and 8 Z-check layers on the selected \([[60,2,6]]_2\) code. Insert **two global flag layers after Z data rounds 3 and 5**, one flag ancilla per Z-octagon:
- 60 data qubits, **80 ancillas** (40 X syndrome, 20 Z syndrome, 20 Z flags).
- 120 X-check CNOTs, 160 Z data/check CNOTs, 40 Z flag/check CNOTs = **320 two-qubit CNOT gates**.
- **13** disjoint-qubit entangling layers (3 X, 8 Z data, 2 flags).

The full 140-qubit Pauli simulator propagates exact X/Z bit masks under every CNOT of the 13-layer circuit, preserving actual check incidence, with a one-fault-at-a-time adversarial model:
- 4,800 nonidentity two-qubit Pauli faults, one **after** each of the 320 CNOTs;
- 240 single ancilla Pauli preparation faults, 3 types for each of 80 ancillas before extraction;
- 2,520 single data memory/idle Pauli faults, 3 types on each of 60 qubits at 14 layer boundaries;
- 80 individual X-syndrome, Z-syndrome or flag classical readout-bit flips;
- one fault-free control.

**Exactly 7,641 cases**, all measured syndrome/flag bits simulated and data residual Pauli cosets reduced modulo the original code's X/Z stabilizer rowspaces. Form the *joint ideal-readout key* \((40\text{ measured X syndrome},20\text{ measured Z syndrome},20\text{ measured flag},40\text{ future perfect X syndrome},20\text{ future perfect Z syndrome})\). With the repo's **frozen** reproducible matching schedule, these 7,641 cases produce **2,039 distinct keys**, with **zero keys leading to different residual stabilizer cosets**. One representative error coset per key therefore gives a correct lookup recovery *in this specified single-fault model and perfect future readout assumption*.

**Reproducibility correction:** using a freshly generated networkx bipartite maximum matching instead of a frozen schedule gave runs with 2,041 or 2,038 distinct keys. This was a schedule-ordering artifact, NOT a fault-protection failure. The new producer freezes the old audited 11-layer schedule and checks every check support against that fixed schedule, yielding **2,039 deterministically**. It does NOT claim this particular key count is schedule-independent. The zero-ambiguity property was checked for the frozen schedule.

**Outstanding critical limitations:** one fault *total* per full round; follow-up 60-check syndrome is ideal; no two simultaneous faults, faulty repeated syndrome extraction, time-like detector histories, actual circuit-level depolarizing Monte Carlo, layout locality, noisy ancilla re-use, or estimated threshold. The code remains \([[60,2,6]]_2\), not a demonstrated physical device. Stim/PyMatching are not installed on the linked Windows interpreter, so no assertion of Stim or PyMatching execution.

Producer \`analysis/w33_20261008_full_CSS_13layer_singlefault.py\`; certificate \`data/w33_20261008_full_13layer_CSS_1fault_preparation_idle_readout_certificate.json\`.

## III. Native H4 600-cell 4D slab: nondegenerate **Lorentzian** 4-simplex metric for *every* positive lapse-to-edge ratio

Earlier exact code triangulated the native 600-cell spatial \(S^3\) with \((120,720,1200,600)\) and lifted it to two time-slices with a prismatic staircase \(S^3\times[0,1]\) whose f-vector is
\[
(f_0,f_1,f_2,f_3,f_4)=(240,2280,6240,6600,2400).
\]
This pass supplies a **globally consistent nondegenerate local Lorentzian edge-square assignment**, not only abstract topology: \(s_{uv}=a^2\) for edges within one time slice, and \(s_{uv}=-\tau^2\) for edges crossing between time slices, with \(a,\tau>0\). For each of the 2,400 actual pentachora, form its 4×4 Lorentzian Gram matrix \(2G_{ij}=s_{0i}+s_{0j}-s_{ij}\).

The 2,400 simplices divide into 600 each of types \((1,4),(2,3),(3,2),(4,1)\) vertices by time slice. Let \(u=\tau^2/a^2>0\). At \(a=1\), **symbolic** Gram determinant factorization independently yields
\[
\boxed{
\begin{aligned}
\det G_{(1,4)}=\det G_{(4,1)}&=-\frac{8u+3}{16},\\
\det G_{(2,3)}=\det G_{(3,2)}&=-\frac{12u+7}{16}.
\end{aligned}}
\]
All are strictly negative for every \(u>0\). Checking signature \((3+,1-)\) at one positive \(u\), and continuity of eigenvalues while determinant never vanishes, proves this signature at **all positive ratios**; independently validate all 2,400 matrices at five \(u\) values. The corresponding positive 4-volumes for \(a=1\) are
\[
V_{(1,4)}=V_{(4,1)}=\frac{\sqrt{8u+3}}{96},\quad
V_{(2,3)}=V_{(3,2)}=\frac{\sqrt{12u+7}}{96}.
\]

The exact distinct triangle-hinge census is **2,400 spatial boundary triangles** (1,200 at each time) plus **3,840 mixed timelike interior triangles** (1,920 \((2,1)\) and 1,920 \((1,2)\)). All 6,240 triangles have independently verified 2D induced metric signatures: pure spatial (+,+), mixed (+,-). At \(a=1\) the area of each spacelike triangle is \(\sqrt3/4\) and each mixed timelike triangle has absolute area \(\sqrt{u+1/4}/2\); total interior mixed hinge area \(1920\sqrt{u+1/4}\). The code also enumerates every hinge-to-pentachoron incidence multiplicity. **Lorentzian realizability is a genuine advance over topological slab only, but is not a dynamical Einstein solution.**

Missing: 4D boost/rotation dihedral angle deficits for each hinge, timelike boundary terms, all independent edge variations and Schläfli identities, matter stress-energy coupling, actual Regge equations and their continuum/ADM constraint closure, causality/time-orientability proof beyond two-slice labelling, and a realistic quantization.

Producer \`analysis/w33_20261008_H4_4D_Lorentzian_Gram_certificate.py\`, certificate \`data/w33_20261008_H4_Lorentzian_4simplex_metric_signature.json\`.

## IV. Falsifiable 27-port known-input photon detector budget with uniform background + adversarial l1 calibration uncertainty

Previous exact model-specific known-input/labeled-detector test, at common coupler drift \(\Delta\theta\in\{-0.002,-0.001,0,0.001,0.002\}\) rad, used the Bhattacharyya coefficient \(B=\sum\sqrt{p_iq_i}\). Here include:
1. Uniform background/dark-admixture \(p_i^{(\beta)}=(1-\beta)p_i+\beta/27\) for **both** hypothesis distributions, with \(\beta\in\{0,.01,.05,.1\}\).
2. Separately adversarial per-hypothesis measurement-calibration \(\ell^1\) error at most \(\epsilon\in\{0,.001,.01\}\), which may differ between both hypotheses. Via Hellinger metric \(H(p,q)=\sqrt{1-B(p,q)}\), triangular inequality and \(H(p,p')\le\sqrt{\mathrm{TV}(p,p')}\le\sqrt{\epsilon/2}\), get a rigorous conservative upper bound
\[
\boxed{B_{\mathrm{true}}\le1-\max\left(0,\sqrt{1-B_{\mathrm{model}}}-\sqrt{2\epsilon}\right)^2.}
\]
3. Minimax optimized one *known* source among all 27, grid drift, independent survival \(\eta=0.99^{L}\), equal-prior binary Bayes bound \(B^n/2\le0.025\), exact binomial survival \(P(\mathrm{Bin}(N,\eta)\ge n)\ge0.975\), giving *model-conditional* joint ≥95% via union bound.

Exactly **36** (3 optical depths ×4 background levels ×3 l1 radii) budgets are stored. For the 36-layer controlled source (port 23):
- \(\beta=0,\epsilon=0\): **18** launched ideal photons;
- \(\beta=.05,\epsilon=.01\): **38** launches;
- \(\beta=.10,\epsilon=.01\): **44** launches.

These are conservative **theoretical test designs**, not measured quantities. A TV/norm bound only applies if an actual calibration establishes the per-hypothesis error radius; no real device, detector, or laboratory data was accessed. This does not cover anonymous port labels, time-correlated noise, unequal detector losses or arbitrary detunings outside the tested grid. The known-input protocol is fundamentally different from the older anonymous-source thousands-of-photons design.

Producer \`analysis/w33_20261008_27port_dark_TV_robust_budget.py\`; certificate \`data/w33_20261008_27port_darkcounts_TV_robust_binomial_budgets.json\`.

## V. **Explicit smooth free Klein-four tetraquadric CY3**: characteristic-zero geometric proof, Hodge (4,20), and line-bundle / hexality firewall

**Major positive result.** Previous runs rigorously established generic Bertini existence of smooth free invariant tetraquadrics over \(\mathbf C\), but failed to certify any specific integral example: the 3-term coefficient \((a,b)=(2,3)\) had *bad reduction* mod7 (nonunit modular Jacobian GB); a separate 21-orbit mod3 F3-rational-point sieve found a candidate with no F3-singularity but nonunit full geometric GB, and correctly declined to claim smoothness. **Neither obstruction disproves smoothness over characteristic zero**.

We now establish an explicit characteristic-zero smoothness proof **without numerical root sampling or modular-Groebner inference**. On \(A=(\mathbf P^1)^4\), coordinates \((x_i:y_i)\), let \(S_i=x_i^2+y_i^2\), \(D_i=x_i^2-y_i^2\), \(T_i=2x_iy_i\). The hypersurface
\[
\boxed{X_{2,3}:\quad \prod_i S_i+2\prod_iD_i+3\prod_iT_i=0}
\]
has multidegree \((2,2,2,2)\), trivial canonical bundle by adjunction, and is invariant under \(g:(x_i,y_i)\mapsto(x_i,-y_i)\) and \(h:(x_i,y_i)\mapsto(y_i,x_i)\) simultaneously in all four factors. They commute *projectively* and generate the Klein four-group \(G\).

**Exhaustive singularity proof in characteristic 0**. Write \(U=\prod S_i\), \(V=a\prod D_i\), \(W=b\prod T_i\), \(a=2,b=3\).
- If all three vanish at a point, each product has a vanishing factor at a different coordinate, since the zero sets of \(S,D,T\) are pairwise disjoint on each \(\mathbf P^1\). With only four coordinates, at least two products have a *single* vanishing factor. Their gradients are nonzero and supported at **distinct coordinates**; no cancellation can annihilate the full gradient (as \(a,b\ne0\)).
- If exactly one product vanishes and the remaining two cancel (e.g. \(U=0,V=-W\ne0\)), differentiating with respect to any coordinate where \(S_j\ne0\) yields \(V(D'_j/D_j-T'_j/T_j)\ne0\), since this log-derivative difference vanishes only at zeros of \(S_j\). Thus all four \(S_i\) must vanish, and the value \(V+W\) there can vanish only if \(b=\pm a\). Analogously \(V=0\) forces \(b=\pm1\); \(W=0\) forces \(a=\pm1\). All impossible for \(a=2,b=3\).
- If none vanishes, work on all four charts where \(x_i,y_i\ne0\), put \(t_i=y_i/x_i\) and \(d_i=D_i/S_i=(1-t_i^2)/(1+t_i^2)\). From \(U+V+W=0\) and \(\partial_iF=0\), direct symbolic rational elimination gives
  \(V/U=-d_i^2\) for every i. Hence \(d_i^2=q\) is constant, \(\prod_i d_i=\pm q^2\), and \(q=\pm1/a\). Since \((T_i/S_i)^2=1-d_i^2\), one also gets \(b=\pm1/(1-q)\). For \(a=2\), possible singular values are **only** \(b\in\{\pm2,\pm2/3\}\), whereas actual \(b=3\). Contradiction. This excludes **all complex singularities**.

The same explicit polynomial avoids all **48** nonidentity G fixed ambient points: at the three 16-point fixed families, \(F\) evaluates up to nonzero coordinate units as \(1\pm a\), \(16(1\pm b)\) and \(16(a\pm b)\), all nonzero at \((2,3)\). The two generators each have determinant \((-1)^4=+1\) on the homogeneous four-factor Poincaré residue form, hence preserve the holomorphic \(3,0\)-form. Therefore
\[
Y=X_{2,3}/G
\]
is an **explicit smooth free Calabi–Yau threefold**. The original tetraquadric has \((h^{1,1},h^{2,1})=(4,68)\) and \(\chi=-128\). Using Lefschetz \(H^2(X)\cong H^2((P^1)^4)\), G-invariance of the four ambient hyperplane classes, and free covering degree4:
\[
\boxed{\pi_1(Y)=G=\mathbf Z_2\times\mathbf Z_2,\quad
\chi(Y)=-32,\quad(h^{1,1},h^{2,1})=(4,20).}
\]
Chern-class code independently verifies \(\int_Xc_3=-128\), \(c_2(TX)=4\sum_{i<j}H_iH_j\), \(\int_Xc_2H_k=24\) for each k, and all distinct triple intersections \(\int_XH_iH_jH_k=2\).

**UV/charge no-go and physical boundaries:** Since \(\pi_1(Y)\) has exponent2, its flat Abelian \(U(1)\) Wilson holonomies have order at most two; thus **this fundamental group alone cannot produce a nontrivial order3 or order6 proton-hexality Wilson line**. This does *not* prohibit discrete Z6 originating instead from bundle/Higgs remnants, matter charges or extensions. Further, at one \(\mathbf P^1\) coordinate the chosen GL2 matrix lifts for g and h **anticommute** (\(gh=-hg\)), so an ambient line bundle \(\mathcal O(n_0,\ldots,n_3)\) has this G-linearization only if \(\sum_i n_i\) is **even**; in particular \(\mathcal O(1,0,0,0)\) cannot be naively descended integrally, but even-total-degree combinations can. This is a concrete equivariant bundle quantization firewall for the heterotic model.

**Not yet a heterotic vacuum or TOE:** No non-Abelian bundle satisfying Hermitian-Yang–Mills slope zero and integrated anomalies, no anomaly/FI-compatible GUT breaking, no full proton-hexality matter charges, no normalized harmonic zero-modes or physical Yukawa. A smooth free CY geometry is a necessary ingredient, not a physical compactification in itself.

Producers:
\`analysis/w33_20261008_explicit_Klein_CY_smooth_proof.py\`,
\`data/w33_20261008_explicit_smooth_free_Klein_tetraquadric_a2_b3.json\`;
\`analysis/w33_20261008_Klein_CY_Chern_bundle_parity.py\`,
\`data/w33_20261008_explicit_CY_Klein_heterotic_topology_2torsion_guards.json\`.

## Verification, nonclaims, and correspondence

Every producer emits deterministic JSON. The full five-front suite \`tests/test_w33_20261008_five_cy_Lorentzian_chiral_CSS_optical.py\` re-executes the algorithms, checks exact ranks, group actions, all covered fault outcomes, Lorentzian symbolic determinants, 36 detector-noise scenarios, complex algebraic singularity proof and Chern/Euler parity guards. Existing previous-pass focused regressions should be run together; local passing tests are **not hosted GitHub CI**.

**Strongest interpretation:** On one hand the finite W33 CSS/toroidal construction has a canonical F20-compatible **four-sheet chiral graph lift**, though its lifted face atlas remains nonmanifold. On another hand there is an explicit **Lorentzian H4 simplicial 4D edge metric**, but no derived dynamics. On a third hand, there is finally an **explicit proven smooth Klein quotient Calabi–Yau** with (4,20) and a precisely quantified Z6-Wilson-line obstruction. These are separate exact mathematical achievements. The missing Theory of Everything would have to formulate and experimentally test nontrivial, *derived* couplings between those sectors without spoiling locality, gauge consistency, anomalies or proven symmetries.

## Five strongest independent next steps

1. **Chiral branched geometry or native 600-cell two-chain bridge:** The proven 240-address, 80-face connected CW has \(b_1=163\) and **160 uncovered graph edges**. Attach additional F20-equivariant faces or quotient relations until every edge has the desired manifold incidence, while preserving all 20 W33 Z-check octagons and the F20 action. Verify all new Betti and torsion invariants; separately seek an authentic native 600-cell/BC-helix embedding rather than renaming the mirror relation native.
2. **Remove ideal syndrome assumptions and measure a real fault-tolerance threshold:** The deterministic 7,641-scenario 13-layer Pauli-1-fault test is a necessary step. Construct detector histories with repeated *noisy* checks, hard circuit layout, correlated faults and explicit decoders; use Stim/PyMatching after installation/verification and sweep error rates/logical failure versus distance. No threshold can be quoted from one-fault uniqueness alone.
3. **4D Lorentzian Einstein–Regge dynamics:** Compute each mixed triangle's dihedral boost deficit, all 4D boundary terms, independently vary all 2,280 edge lengths, implement lapse/shift matter-coupled constraints and test if the discrete Bianchi/Jacobi/ADM closure survives refinement. Analytic \(\det G<0\) proves realizability, **not** the Einstein equations.
4. **Physical 27-port calibration and discrimination:** Use one known source and labeled detectors, measure actual scattering probability matrices, detector efficiencies, cross-talk, time correlations and credible bounded l1 radii. Preregister the robust likelihood test and compare its 18/38/44 modeled photon budgets to real false-decision rates. Anonymous-port discrimination remains a separate experiment.
5. **Explicit heterotic bundle on proven smooth CY(4,20):** Now that \(X_{2,3}/G\) is smooth free by an exact proof, construct a non-Abelian, G-equivariant slope-stable bundle satisfying anomaly/tadpole and FI conditions. Respect \(\sum_i n_i\equiv0\pmod2\) for naive ambient line-bundle equivariance and the no-Z6-flat-Wilson character constraint. Derive a genuine \(Z_6\) remnant if possible, then compute harmonic metrics, canonical kinetic terms and normalized Yukawas.

**No changes to Holotrade this pass:** all new results concern foundational W33 mathematical and physics simulation work.