# TOE76 — Six W33 research fronts, with a new exact twisted-Ihara / 120° fermion bridge

**Date:** 14 October 2026. **Repository:** wilcompute/W33-Theory. **Research protocol:** read recent parallel GitHub commits; compare prior proof/error ledger; build new source-regenerating scripts, independent cross-checks and tests; publish to \`master\` with GitHub Actions evidence. These are finite combinatorial and Hamiltonian models, **not** the classical Riemann hypothesis, a gauge-field mass-gap proof, or the physical Theory of Everything.

## Existing RH / Ramanujan work reviewed

The graph-theoretic RH program is **already extensive**. We checked the original manuscript source \`manuscripts/tex/part27_graph_rh_theorem.tex\` (which is input by the \`w33_paper.tex\` manuscript), \`analysis/w33_ihara_zeta.py\`, \`w33_pass74_zeta_frontier.py\` (important separate Levi incidence-graph prime-cycle census), \`manuscripts/parts/PART_MCLIII_IHARA_ZETA.md\`, \`analysis/2026-07-15_pass89_ihara_zeta_ramanujan.md\`, \`analysis/w33_pass3080_3082_bass_regular_audit.py\` (explicit past **irregular-graph** correction), \`analysis/BT872_ihara_zeta_spanning_bridge.md\`, \`exploration/w33_ramanujan_bridge.py\`, \`docs/PART_CDI_IHARA_ZETA_DETERMINANT.md\`, plus latest TOE73–75 native theta/fermion/quantum-cover source.

**Parent theorem:** the *40-vertex degree-12 collinearity graph* SRG(40,12,2,4) has spectrum \(\{12^1,2^{24},(-4)^{15}\}\). Bass yields
\[
Z_{40}(u)^{-1}=(1-u^2)^{200}(1-u)(1-11u)
 (1-2u+11u^2)^{24}(1+4u+11u^2)^{15}.
\]
The nontrivial poles indeed have modulus \(11^{-1/2}\) by the negative quadratic discriminants. This is the precise **regular Ramanujan-graph / graph RH statement**, and it **does not prove classical RH**. The associated *80-vertex degree-four Levi incidence graph* is a second distinct regular graph; the *11-vertex native theta patch is a THIRD, irregular graph*.

**Source-quality corrections worth preserving:** \`manuscripts/parts/PART_MCLIII_IHARA_ZETA.md\` incorrectly writes \((1-12u)\) rather than \((1-u)(1-11u)\) in one displayed determinant factorization, and misattributes the trivial \(\pm1\) Hashimoto multiplicities. The full original TeX part27 has the correct factorization. Also \`analysis/2026-07-15_pass89_ihara_zeta_ramanujan.md\` includes the misleading general assertion that every SRG with \(\mu>0\) must be Ramanujan; this is **not** a general theorem. W33's actual eigenvalues are sufficient for the particular Ramanujan conclusion. The later irregular-graph correction in Pass3080 should guide all 11-site comparisons.

### **Sixth front — exact bridge: the same holonomy invariant controls the 11-site fermions AND the twisted Ihara zeta**

The native 11-site / 12-link graph is the equal-arm \(\Theta(4,4,4)\): three internally disjoint length-four paths between two degree-three hubs, with nine degree-two internal vertices. It is exactly the **fourfold subdivision of the multigraph with two vertices connected by three parallel edges**. This observation makes its Ihara algebra unusually tractable and also explains the three eight-cycles and \(b_1=12-11+1=2\).

Set \(z_1=1,z_2=e^{i\phi_1},z_3=e^{i\phi_2}\) and
\[
s^2=|z_1+z_2+z_3|^2.
\]
For the *unitarily twisted*, 24-dimensional non-backtracking Hashimoto operator \(B_\phi\), the exact theorem is
\[
\boxed{\det(I-uB_\phi)=(1-u^8)\left(1+(4-s^2)u^8+4u^{16}\right).}
\]
Equivalently, with \(t=u^4\), this is the **unitarily twisted Ihara-Bass determinant of the degree-three three-edge dipole**, pulled back under \(t=u^4\):
\[
\det(I-uB_\phi)=(1-t^2)
 \left[(1+2t^2)^2-s^2t^2\right].
\]
**Proof in three routes:** (i) contract each length-four directed arm into a weighted edge, with continuation matrix \(K=J_3-I_3\), and compute \(\det(I-u^8 KZ^{-1}KZ)\); the resulting characteristic polynomial has trace \(s^2-3\), second coefficient \(s^2\), and determinant \(4\). (ii) Compute \(\det(I-uB_\phi)\) directly on 24 oriented edges. (iii) Independently apply the **irregular** Bass determinant
\((1-u^2)^{12-11}\det(I-uA_\phi+u^2(D-I))\) on all eleven vertices. All three paths agree on six holonomies and four spectral parameters in the CI test.

Specializations:
\[
\boxed{Z_{\Theta,0}(u)^{-1}=(1-u^8)^2(1-4u^8)}
\quad\text{and}\quad
\boxed{Z_{\Theta,120^\circ}(u)^{-1}=(1-u^8)(1+2u^8)^2}.
\]
The three non-backtracking primitive undirected octagons account for the first cyclic trace:
\[
\operatorname{tr} B_\phi^8=8(s^2-3)
=16\sum_{i<j}\cos(\phi_i-\phi_j).
\]
At zero flux the trace is \(+48\); at the exactly selected free **120-degree flux** (\(z_1+z_2+z_3=0\)) it is \(-24\). The 120-degree interference also **eliminates the untwisted Perron/geodesic growth factor** \(1-4u^8\), replacing it with \((1+2u^8)^2\).

Crucially the **same \(s\)** determines the exact five-spinless-fermion free ground energy, already derived in TOE75:
\[
E_0(s)=-\sqrt2-\sqrt{5+2\sqrt{3+s}}
              -\sqrt{5+2\sqrt{3-s}}.
\]
The strict concavity argument uniquely picks \(s=0\) as its global minimum: equivalently, the 120-degree flux is simultaneously an exact *fermionic energetic optimum* and a *magnetically twisted prime-geodesic cancellation point*. **This is the substantive new W33-subgraph-to-Ihara bridge.**

**Ramanujan/graph-RH scope:** the theta graph itself is **irregular**: two degree-three hubs and nine degree-two sites; DO NOT test its adjacency eigenvalues against \(2\sqrt{11}\) or claim a universal \(u=11^{-1/2}\) pole circle. The contracted degree-three three-edge dipole instead has magnetic adjacency eigenvalues \(\pm s\). Its **unitary-twisted nontrivial quadratic factor is tempered** iff \(s\le2\sqrt2\), equivalently \(s^2\le8\). On the subdivided graph its nontrivial quadratic poles satisfy \(|u|=2^{-1/8}\) (since \(t=u^4\)); the \((1-u^8)\) factor has poles of modulus 1. At \(s=0\), our 120-degree optimum is strictly inside this twisted Ramanujan band; at the trivial character \(s=3\), the distinguished Perron pole is at \(|u|=2^{-1/4}\). This is a **graph zeta analog**, not a proof of the classical Riemann hypothesis or of a novel uniquely W33-specific spectral phenomenon. In fact every uniform equal-arm theta graph of the same lengths has the same theorem.

**Producer:** \`analysis/w33_20261014_toe76_theta_twisted_ihara.py\`.

## First front — exact robust hopping with two arbitrary edges

For each of \(\binom{160}{2}=12{,}720\) choices of TWO independently varied native edges, build the exact three-by-three Hessian of the leading high-temperature W33 flat-holonomy potential as an integer **multiaffine** function of their hopping weights. Check all \(4\binom{160}{2}=50{,}880\) corners with each weight in \(\{0,2\}\), all other weights 1. Sylvester's 3-by-3 criterion is performed with **integer principal minors**, not floating eigenvalue tolerances. Since each interior Hessian is a convex combination of the four endpoint Hessians, all-positive corners imply strict positivity for the entire two-edge \([0,2]^2\) box. Coupled with TOE64's exact signed-square identity (mixed Fourier cycle coefficients remain nonnegative under nonnegative edge weights), this implies the **unique global 3π leading-potential minimum for that restricted two-edge disorder class**—if all 50,880 tested corner Hessians pass. If any fails, the producer emits explicit counterexample edge indices and endpoint amplitudes rather than asserting an invalid theorem. This is a 2-sparse disorder problem, **not** a general 160-edge disorder threshold.

**Producer:** \`analysis/w33_20261014_toe76_four_fronts.py\`.

## Second front — eight mathematically ordered gauge eigenvalue upper bounds

The native two-loop Gauss-constrained patch has 11 sites, 12 links, five mobile fermions, 462 Fock occupations, two unbounded electric flux coordinates, and a 22,638-dimensional \(L=3\) variational block. Exhaustively find eight low-diagonal states which are **pairwise not connected by any fermion or magnetic off-diagonal transition**. Their exact rational energy expectations form a diagonal 8-by-8 Rayleigh compression. By the Courant–Fischer principle they provide **unconditional upper bounds on ordered full unbounded-electric-rotor eigenvalues \(E_0,\dots,E_7\)**; no sparse numerical Ritz eigenvalue ordering is assumed. This establishes a low-energy spectral multiplicity window and extends TOE75's E1 bound. **It does not give any ordered E1 lower bound or a positive spectral gap.**

**Producer:** \`analysis/w33_20261014_toe76_four_fronts.py\`.

## Third front — actual 27-orbit connected quantum pairing subgraph

TOE75 established at least 27 pairwise distinct, **regular** \(PGSp(4,3)\) orbits of 20-octagon ground covers, each with group size 51,840. This pass builds the exact adjacency among seven legacy seed covers and 20 newly classified seed covers from *actual validated local two-pairing-flip moves*. Compute its exact edge count, triangles, connected components and cycle rank; since each of these orbit actions is regular/free, each chosen seed edge transports to a **perfect matching of 51,840 states**. The compressed adjacency on 27×51,840 covers comprises 51,840 identical copies of a computable 27-vertex seed transition graph with exact integral edge count and verified connectivity. It is **a guaranteed selected subgraph** rather than the full induced quantum Hamiltonian. The computations do not assume 27 exhausts all covers.

**Producer:** \`analysis/w33_20261014_toe76_four_fronts.py\`.

## Fourth front — integer four-dimensional spin index and anomalies

For a *chosen* closed W33-derived product manifold \(M=\Sigma_{81}\times\Sigma_{81}\), examine two mixed degree-two cohomology classes \(\alpha\wedge\gamma\) and \(\beta\wedge\delta\), built from symplectic \(H^1\) pairs on each surface. The cup-intersection matrix is
\[
\begin{pmatrix}0&-1\\-1&0\end{pmatrix}.
\]
For the **externally supplied** integral Chern class \(c_1=a(\alpha\wedge\gamma)+b(\beta\wedge\delta)\), the topological twisted spin-Dirac index is
\[
\boxed{\operatorname{ind}D_L^+=-ab.}
\]
All graph-inherited-only Lagrangian mixed flux classes have zero index; the nonzero index requires a **dual boundary flux choice**. A 49-pair integer scan over \((a,b)\in[-3,3]^2\) tests the parity/linearity. This is a mathematical index formula, not a local W33 overlap-Dirac lattice realization or an anomaly-free Standard Model chiral spectrum.

**Producer:** \`analysis/w33_20261014_toe76_four_fronts.py\`.

## Fifth front — persistent-current and thermal-flux stiffness tests

Use the full 462-state canonical many-body Hamiltonian on the native theta subgraph. Around the 120-degree phase pair, differentiate the \(V=0,.2,1,4\) ground energy numerically and the full finite-temperature Helmholtz free energy at beta=2. Cross-check the \(V=0\) Hessian against the **exact** curvature
\[
H^{(0)}=(-g''(3))
\begin{pmatrix}2&-1\\-1&2\end{pmatrix},
\qquad g(t)=\sqrt{5+2\sqrt t}.
\]
Finite interacting currents/stiffness are strictly numerical. A matched **generic Theta(4,4,4)** with equal-arm hopping has the same exact free spectral formula: this is an essential negative control on claims of W33 specificity. To obtain a W33-only prediction, an embedding-sensitive observable must be constructed and tested.

**Producer:** \`analysis/w33_20261014_toe76_flux_currents.py\`.

## Verification and scientific boundaries

Independent six-test GitHub Actions workflow: \`.github/workflows/w33_toe76_six_fronts.yml\`. It checks the 24-state twisted Hashimoto determinant, the independent 11-by-11 irregular Bass identity, the 3-by-3 transfer, all two-edge Hessian corners, eight exact Gauss rotor trial states, native 27-orbit adjacency, integral spin-index parity, and finite-temperature currents. Four resulting JSON certificates are regenerated into an Actions artifact. **A passing CI status must be checked before claiming completion.**

**Relevant independent mathematics:** Sunada/Hashimoto/Bass graph zeta theory; Rangarajan, FSTTCS 2017 DOI 10.4230/LIPIcs.FSTTCS.2017.46; the unitary representation Ihara-zeta literature including *Scattering matrices of regular coverings of graphs*, DOI 10.1016/j.disc.2009.09.009. All are prior graph mathematics, not evidence that classical RH or TOE has been proved.

## Five independent highest-value next steps

1. Prove exact 160-edge **realizable** W33 Hessian minimax bounds using symmetry/interval arithmetic and sparse-support certificates; extend successful low-support robustness in the number of deviating links.
2. Produce a mathematically certified **positive infinite-rotor spectral gap**, requiring an ordered E1 lower bound from verified finite-block inertia plus exact Schur-tail inequalities.
3. Complete the 27-orbit-to-beyond **quantum pairing transition quotient**, compute its full symmetry-reduced matrix and low-spectrum phases, and search for more ground-cover orbits.
4. Construct a local admissible **4D overlap-Dirac** operator with a genuinely W33-determined spin connection/curvature; verify integral index, cubic/mixed anomalies and nonnative controls.
5. Build a **holonomy-sensitive Ihara–fermion physical test**: design interferometric phase/length imperfections that separate the exact 120° generic-theta prediction from W33-specific surrounding edges, and verify robustness plus nonbacktracking geodesic cancellations.

**Physical Theory of Everything and the classical Riemann hypothesis both remain open.**


## Verified results and exact two-edge stability correction

**Final checks:** [GitHub Actions run 38642922578](https://github.com/wilcompute/W33-Theory/actions/runs/38642922578), **7/7 passed in 19.54 seconds**. Four source-generating certificate scripts plus the independent summary completed successfully; artifact \`toe76-six-front-certificates\`. The previously published six-test run [38642389278](https://github.com/wilcompute/W33-Theory/actions/runs/38642389278) also passed, but the present run adds the independent 80-site Levi Ramanujan and sparse nonbacktracking audit.

### 1. Exact result: all two-edge perturbation Hessians are positive **semidefinite**

The initial 50,880-corner Sylvester census reported 951 Hessians that were **not strictly positive definite**. **That does not imply any negative curvature**. An additional independent exact test of **all seven principal minors** of every 3×3 Hessian matrix (three one-by-one, three two-by-two, and the full determinant) showed:

| Classification | Exact count |
|---|---:|
| Native edge pairs | 12,720 |
| Two-edge endpoints with each hopping weight 0 or 2 | **50,880** |
| Endpoints strictly positive definite | **49,929** |
| Endpoints positive semidefinite but singular | **951** |
| Endpoints with a negative Hessian eigenvalue | **0** |
| Single-edge endpoints examined | 320 |
| Single-edge singular endpoints | 3 (edge IDs 59, 93 and 139, each at hopping weight 0) |
| Single-edge non-PSD endpoints | **0** |

The minimum exact full determinant was **zero**, first attained at original native edge indices (0,59), with both varied weights zero. Its singularity reflects a flat quadratic direction, **not an instability**.

**Theorem (restricted two-link box):** Fix the other 158 native W33 link hopping magnitudes to 1, and allow **any two** remaining hopping magnitudes to vary independently in \([0,2]\). The leading \(\beta^7\) flat-holonomy W33 potential retains three-\(\pi\) as **a global minimum**. Proof: the full Hessian in these two positive link weights is multiaffine, so its matrix at any point of the square is a convex combination of its four endpoint Hessians. The exact 50,880 endpoint principal-minor audit shows all are PSD. TOE64's exact trigonometric signed-square identity expresses the entire potential difference as a quadratic sine term with this Hessian plus nonnegative quartic remainders, because all weighted mixed Fourier coefficients remain nonnegative for nonnegative edge weights. Therefore the potential difference is everywhere nonnegative. **Uniqueness need not hold at singular endpoints.** This is a **strong new sparse-disorder theorem**, not a proof of the unknown all-160-edge sharp threshold.

**Correction to provisional work-in-progress narration:** Earlier "951 failures" meant failure of *strict* positivity; they did **not** demonstrate that two-link disorder destabilizes the \(\pi\) flux. They instead led to the stronger global-semidefinite stability result above. The original TOE65 **17-link** native negative-curvature adversary remains valid because it changes many links at once.

### 2. Eight ordered full-rotor variational bounds

The actual 22,638-state \(L=3\) Gauss block contains eight pairwise off-diagonal-uncoupled exact Fock-flux states, yielding the unconditional Courant–Fischer inequalities
\[
\boxed{E_0\le3/8,\qquad E_j\le387/200=1.935\quad (1\le j\le7)}
\]
for the **ordered full unbounded** native two-loop electric-rotor eigenvalues. There are therefore **at least eight eigenvalues below the exact Q-complement lower barrier** \(14.165\), but the result supplies no positive \(E_1-E_0\) lower bound. These upper bounds do not supersede the much stronger variational E0 upper bound from TOE74; they add low-state counting without assigning numerical eigenvalue order.

### 3. Selected exact 27-orbit transition adjacency

The chosen twenty-octagon representative graph contains **27 vertices**, **41 directly witnessed two-vertex pairing-flip edges**, **three triangles**, and cycle rank **15**. Every vertex is connected by the selected edges. Since all 27 \(PGSp(4,3)\) orbit stabilizers have order 1, the chosen 41 equivariant edge types transport to
\[
\boxed{41\cdot51840=2{,}125{,}440}
\]
distinct transitions in the **selected 1,399,680-cover** compression, decomposing into **51,840 connected components of 27 states each**, when only these 41 chosen matching types are retained. **This is not the full induced pairing Hamiltonian**; additional transitions may join or alter those components.

### 4. Spin-index constraints

The W33-derived but noncanonically thickened closed four-manifold \(\Sigma_{81}\times\Sigma_{81}\) has zero untwisted spin index and zero twisted index for graph-inherited mixed Lagrangian flux. Choosing an independent dual mixed curvature class gives the exact finite-subsystem formula
\[
\operatorname{ind}D_L^+=-ab
\]
for \(c_1=a(\alpha\wedge\gamma)+b(\beta\wedge\delta)\). Forty-nine integer \((a,b)\) combinations were checked. A nonzero index from **externally chosen** curvature is not a physical W33-derived chiral spectrum or an anomaly-free theory.

### 5. Interacting persistent-current and finite-temperature flux stiffness

On the 462-state 11-site theta model, finite-difference ground-energy current gradients vanish numerically at the 120° flux by the arm symmetry. Both ground-state and beta=2 Helmholtz free-energy Hessians have **positive numeric eigenvalues** at V=0,.2,1,4:

| V | ground Hessian smallest eigenvalue | beta=2 thermal Hessian smallest eigenvalue |
|---:|---:|---:|
| 0 | 0.01992157 | 0.00527735 |
| 0.2 | 0.02033328 | 0.00573336 |
| 1 | 0.02004409 | 0.00690773 |
| 4 | 0.00173637 | 0.00147882 |

For V=0 the Hessian also agrees with the exact concavity-derived tensor \(-g''(3)\begin{psmallmatrix}2&-1\\-1&2\end{psmallmatrix}\). The V>0 results establish numerical local stiffness at the evaluated phases, **not a globally certified interacting flux preference**.

### 6. Verified three-level Ihara / Ramanujan hierarchy

The new [Levi hierarchy producer](https://github.com/wilcompute/W33-Theory/blob/master/analysis/w33_20261014_toe76_levi_ihara_hierarchy.py) independently computed the 80-vertex **4-regular** Levi graph's actual eigenvalues \(\pm4,\pm\sqrt6,0\) with multiplicities \(1,24,30\), proving a second regular Ramanujan-graph condition \(\sqrt6<2\sqrt3\). Its full factorization is
\[
\boxed{Z_{\mathrm{Levi}}(u)^{-1}=(1-u^2)^{81}(1-9u^2)(1+9u^4)^{24}(1+3u^2)^{30}.}
\]
The **exact** 320×320 native Hashimoto walk count gives \(\mathrm{tr}B^n=0\) for \(1\le n\le7\), and \(\mathrm{tr}B^8=25{,}920=16\times1620\): the Levi graph has 1620 primitive unoriented octagons. The theta's three octagons constitute exactly \(1/540\) of this census, but this combinatorial ratio implies no physical 540-fold sector.

The hierarchy of **different objects** is now explicit:
- Collinearity graph (40, 12-regular), graph-RH nontrivial pole circle \(11^{-1/2}\).
- Levi graph (80, 4-regular), graph-RH nontrivial pole circle \(3^{-1/2}\).
- Theta patch (11, irregular), **twisted** three-parallel-edge transfer, with selected nontrivial pole circle \(2^{-1/8}\) for \(s^2\le8\).

These are linked by W33 incidence/subgraph structure, not interchangeable critical circles. The classical Riemann hypothesis is **not** proved, and the generic equal-arm theta result cannot yet distinguish a uniquely W33 realization. A ready-to-include source proof is in \`manuscripts/tex/toe76_theta_twisted_ihara_bridge.tex\`.

**Independent literature:** Rangarajan, *A Combinatorial Proof of Ihara–Bass's Formula*, DOI 10.4230/LIPIcs.FSTTCS.2017.46; the unitary-representation graph-zeta literature, DOI 10.1016/j.disc.2009.09.009.
