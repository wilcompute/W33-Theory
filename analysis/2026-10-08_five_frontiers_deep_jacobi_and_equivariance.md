# 2026-10-08: physical five-front deep pass and exact C8 Jacobi identification

**Disposition:** five requested fronts **executed to the extent permitted by actual source data**, plus one flux-stabilization check. Strongest positive result is an **exact structural Lie algebra identification over \(\mathbb Q\)**. Strongest negative result is a **central-kernel equivariance obstruction** to identifying 320 Weyl-character vacua with 320 projective flag-graph triangles. Neither result derives four-dimensional Einstein gravity, observed particle chirality, a consistent string vacuum, or a full TOE.

**Files:**
- Producer: `analysis/w33_20261008_five_plus_one_deep.py`
- Lie producer: `analysis/w33_20261008_eight_cycle_jacobi_identification.py`
- Certificates: `data/w33_20261008_five_physics_deepening.json`, `data/w33_20261008_eight_cycle_jacobi_identification.json`
- Independent regression: `tests/test_w33_20261008_five_plus_one_deep.py`

## Source intake and prior ownership

Started from the current remote `master` head, including the simultaneous Pass 398 formula-search universe update. Prior exact dual 27-state carriers, classical electrical distributions, CPTP channel, coherent average mixing, 34D eight-cycle Lie span, and conditional noise robustness belong to commits `0d3009c5`, `7137cffeb`, `9dccf33c5` and `dae1de586`. The 320 Weil-parity quartic stabilizer vacua and 160 flags \(\times\) two nontrivial characters belong to [Pass 11697–11698](PASS11697_11698_CHIRALITY_VACUUM.md). The nonzero \(C=1/2\) holomorphic tetraquadric cup, line bundle indices and exact zero-slope Kähler point belong to [Pass 11742–11749](PASS11742_11749_NONZERO_FLAVOR_AND_FLUX_FRAME.md); [Pass 11750–11757](PASS11750_11757_INTEGRAL_GEOMETRY_AND_FLUX_DYNAMICS.md) owns the initial eight-radius flux rolling no-go. The present computations never promote those older findings to new results. Source searches specifically inspected flags/chirality equivariance work and the repo's existing 24D cubic Jacobi/D4 analysis (Pass 409). That earlier 24D algebra is *not* the following 34D C8 current algebra; sharing the word Jacobi does not establish a map between them.

## 1. Exact 27-mode photonic coupling designs and nine disjoint layers

The two previously constructed 27×27 integer adjacency Hamiltonians each have 27 physical ports of degree 8 and **108 distinct, simultaneously required undirected couplings**. The committed certificate now contains, **for each graph separately**, an exact 27×27 coupling matrix, 108 labeled coupler endpoints, and a separately computed **nine-layer disjoint-edge schedule**, obtained by integer linear programming and checked to cover every edge exactly once without sharing a port within a layer.

This has useful physical consequences:

- A planar simple 27-vertex graph can have at most \(3(27)-6=75\) edges. These 108-edge graphs are nonplanar. Planarizing a general-position drawing with \(c\) crossings produces \(v+c\) vertices and \(m+2c\) edges, hence \(c\ge m-3v+6=\boxed{33}\). **Any single-layer geometric routing diagram representing the complete graph as edges requires at least 33 crossings.** This is a weak lower bound, not an optimized device crossing count.
- Every graph has maximum degree 8, so Vizing's theorem bounds the undirected edge-chromatic number by 8 or 9. An 8-edge-coloring would require a perfect matching at every color, impossible on **27 odd vertices**, so \(\chi'(G)=\boxed9\). The integer-programmed schedules construct this bound explicitly.
- These nine matchings are a valid set of **nonoverlapping two-port interaction stages**, suitable for a Trotter/Suzuki digital decomposition of \(e^{-itA}\). **Nine stages applied once do not equal** the simultaneous graph Hamiltonian; finite-Trotter error and gate compilation/loss remain to be quantified. Optical crossings are not automatically impossible: 3D, multilayer, switching, or programmable mesh hardware can support nonplanar logical interactions.

Prior device noise certificate: at supplied dimensionless \(t=0.78\), the permutation-invariant largest off-diagonal transfer probability differs by \(\Delta\simeq0.2694649303\). A deterministic Duhamel argument guarantees that ideal-model sign remains separated under the earlier uniform operator-norm bound \(\|E\|<\Delta/(4t)=0.08636696\) for each graph. The new contribution is an actual coupler list and layer schedule, **not** an observed photon device or a calibrated fidelity.

Relevant experimental comparison: [3D integrated multi-photon continuous-time quantum-walk couplings](https://www.nature.com/articles/s41377-024-01627-7); [global PIC calibration](https://journals.aps.org/prapplied/abstract/10.1103/PhysRevApplied.22.054011). These demonstrate related capabilities but neither paper builds these W33 graphs.

## 2. The local 34D Lie algebra *is* a symplectic Jacobi algebra over Q

The eight nearest-edge canonical currents of an induced W33 Levi eight-cycle are \(J_{ij}=p^T[(e_i+e_j)(e_i-e_j)^T]q\). The prior two packets gave a 34-dimensional rational bracket-closed subalgebra of \(\mathfrak{sl}_8\), with right null vector \(u=(1,\ldots,1)\), left null covector \(s^T=(1,-1,\ldots,1,-1)\), a one-dimensional center, and derived-algebra dimension 34.

**New exact identification:** form the quotient \(Q=\ker(s^T)/\langle u\rangle\) (dimension 6) and an explicit rational adapted basis \(\{u,b_1,\ldots,b_6,w\}\). Every current then has block form

\[
\begin{pmatrix}0&r&z\\0&A&v\\0&0&0\end{pmatrix},
\qquad A\in\operatorname{End}(Q).
\]

Computing the complete 34-dimensional generated algebra and rational coordinate projection gives:

1. The image in \(\operatorname{End}(Q)\) has dimension **21** and preserves a **nondegenerate antisymmetric six-by-six form \(J\)**, whose exact matrix and nonzero determinant appear in the certificate. The full Lie algebra preserving \(J\) has dimension \(3(2\cdot3+1)=21\); hence the image is exactly \(\mathfrak{sp}(6,\mathbb Q)\).
2. The kernel has dimension **13**. Its map to all entries \((r\in\mathbb Q^6,v\in\mathbb Q^6,z\in\mathbb Q)\) is a rational isomorphism (computed determinant **1/2** in the chosen coordinate bases). Every commutator in this kernel is central and some are nonzero: it is exactly the **Heisenberg Lie algebra \(\mathfrak h_{13}\)**.
3. The short exact sequence \(0\to\mathfrak h_{13}\to\mathfrak g\to\mathfrak{sp}_6\to0\) splits by the characteristic-zero Levi–Malcev theorem; thus

\[
\boxed{\mathfrak g\cong\mathfrak{sp}(6,\mathbb Q)\ltimes\mathfrak h_{13}(\mathbb Q)}.
\]

The action is the standard symplectic action up to a rational choice of Levi splitting and a Heisenberg coordinate basis. Over \(\mathbb Q\), these are **mathematical theorems of the supplied finite current ansatz**, not a proof of a 4D Einstein constraint algebra, real spacetime dimension, or quantum gravity. A perfect Lie algebra can possess nonzero center when its nilpotent radical is nontrivial; this is consistent with established general Lie theory ([Burde et al., perfect Lie algebra and Levi decomposition](https://pmc.ncbi.nlm.nih.gov/articles/PMC11304516/)).

**A fresh line of attack** is to find the six-dimensional symplectic phase space geometrically and ask whether the induced Jacobi cocycle is a genuine central extension of an observable current algebra. This must be checked against the full 80-vertex W33 Levi graph and the previous Schläfli/E6 symplectic structures before identifying them.

## 3. No symplectic-equivariant 320-vacuum to 320-triangle identification

Previous Pass 11698 proves that the 320 quartic maximizers comprise 40 Lagrangian lines \(L\), each with eight nontrivial \(\mathbb F_3\)-valued characters \(\lambda:L\to\mathbb F_3\): they form 160 pairs \((p\in L,\lambda=\pm)\). The previous flag-topology packet proves the W33 Levi line graph has exactly 320 graph triangles: 160 centered on line-vertices (three of four flags meeting the line) and 160 centered on point-vertices (three of four flags meeting the point). Both 320-sets can be *set-theoretically* labelled by flags and an arbitrary binary convention.

**But they are not \(Sp(4,3)\)-equivariantly isomorphic.** The central element \(-I\in Sp(4,3)\) acts trivially on all projective points and Lagrangian lines, hence on all 160 flags and 320 graph triangles. On every nontrivial line character, \((-I)\cdot\lambda=\lambda\circ(-I)^{-1}=-\lambda\ne\lambda\), since the characters are over \(\mathbb F_3\). It swaps **all 160 character pairs** and fixes none. The producer enumerates and verifies the sets and full central action: **320 projective triangles fixed versus zero of 320 line characters fixed**.

For any \(Sp(4,3)\)-equivariant map \(f\) from character vacua to triangles, \(f(-I\cdot x)=-I\cdot f(x)=f(x)\). Consequently **no such map can be injective**, and in particular no equivariant bijection exists. A bridge must either enlarge the triangle target with a double-cover/orientation sign, or reduce the acting symmetry with a clearly justified physical reason. The action of \(-I\) as a *physical gauge transformation* rather than a real global symmetry is **not established**; thus this is a strict equivariant-data obstruction, not an experimental proof that chirality is gauge.

## 4. Proton hexality: an exact extra Z3 charge and an exclusion of Klein-four Wilson characters

The previous packet proved that its explicit \(P_6\) table is not an integer linear combination of \(3(B-L)\) and \(6Y\) modulo 6. This pass constructs the **smallest additional prime-factor type** that solves the eight-field charge bookkeeping: a \(\mathbb Z_3\) generator \(X_3\), embedded as \(2X_3\pmod6\), such that

\[
P_6\equiv 3(B-L)+6Y+2X_3\pmod6.
\]

For \((Q,U^c,D^c,L,E^c,N^c,H_u,H_d)\), the exact \(X_3\) charges are

\[
\boxed{(2,0,2,2,2,0,1,2)\pmod3}.
\]

All eight identities are verified directly. The necessary mixed integer sums in the declared field inventory are \((SU3^2,SU2^2,\mathrm{grav})=(18,27,78)\), each zero modulo 3. This is **not** a sufficient discrete gauge anomaly or UV completion check.

Crucially, the actual tetraquadric quotient family in Pass 11742 uses the **free Klein-four group \(\mathbb Z_2\times\mathbb Z_2\)**. Its one-dimensional character group has orders \((1,2,2,2)\), so **its ordinary equivariant Wilson-line characters cannot by themselves supply an order-three generator**. This narrows the actual heterotic search: an extra U(1) Higgs remnant or another independently realized order-3 source must be constructed *from the real bundle/geometry*, not postulated. The exact origin, anomalies, F/D-flatness, exotic masses, proton operators and worldsheet rules all remain unresolved. The proton-hexality selection rule is established physics literature, not new here ([Dreiner–Luhn–Thormeier 2006](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.73.075007)).

## 5. Canonical physical Yukawa coupling: source-bound preflight rather than invented output

The existing source [Pass 11742](PASS11742_11749_NONZERO_FLAVOR_AND_FLUX_FRAME.md) supplies three actual line bundle degrees

\[
K_1=(-2,1,1,0),\quad K_2=(0,-3,0,1),\quad K_3=(2,2,-1,-1),
\]

and the exact zero-slope positive Kähler point

\[
t=\left(1,\frac{13+\sqrt{241}}{12},\frac12,\frac{5+\sqrt{241}}{36}\right).
\]

The present preflight re-computes all three slopes as **exactly zero** from the tetraquadric triple intersection form (all distinct indices have intersection number 2); derives the volume in these intersection conventions,

\[
\mathcal V = \frac{241+17\sqrt{241}}{72}>0,
\]

and verifies that no two of the three bundles have mutually opposite degrees (so no charged quadratic mass from just one pair at the split Abelian locus). The previously calculated nonzero **holomorphic** cup \(C=1/2\) remains precisely that: a coefficient in selected Serre/residue bases.

The published [heteroticyukawas package](https://github.com/kitft/heteroticyukawas) and [2025 physical quark-mass calculation](https://www.sciencedirect.com/science/article/pii/S0550321324003444) provide a plausible numerical method, but **not a completed calculation for these three bundles**. On the available connected Windows Python, TensorFlow, cymetric and heteroticyukawas were not installed. More importantly, the repo's existence proof of a generic smooth invariant tetraquadric does not give a single fixed polynomial or its explicit complex-structure parameters; the correct closed representative inputs and trained CY/HYM/harmonic metrics are likewise absent. Therefore claiming observed Yukawa masses or mixing would be fabrication. The preflight certificate explicitly identifies each missing physical input instead of silently substituting generic textures.

## 6. Extra: eight-radius flux vacuum stabilization firewall

The actual previous primitive-flux potential has exponent \(k=(2,4,4,4,4,4,4,4)\), so its unit-radius gradient is exactly \((-2,-4,-4,-4,-4,-4,-4,-4)\) for unit positive coefficient. Every coordinate wants to roll; no stationary vacuum exists within that single-positive-flux term. More generally all positive exponential terms whose exponent vectors lie in a common strict half-space cannot stabilize all radii. The earlier mathematical nine-balanced-term toy has Hessian eigenvalues \(1^{\times7},9\) and positive vacuum energy 9; no allowed string/E8 flux origin or 4D cosmological constant cancellation has been supplied.

## Falsification standards

Reproducing a closed graph Lie algebra does **not** recover the Dirac/ADM hypersurface deformation algebra. Identifying a group-action obstruction does **not** prove a physical CP selection rule. A charge identity does **not** prove the presence of the symmetry as a gauge remnant. An optical 9-layer schedule does **not** reproduce the simultaneous adjacency propagator without compiled approximations and losses. A holomorphic Yukawa integral is **not** a canonically normalized measured quark mass. Those are explicit "firewalls" for future research. The next result should pass a physical-action, hardware-calibration, anomaly, vacuum, or observed-quantity test.

## 7. Extra executed physical-design experiment: nine-layer Trotter fidelity versus per-layer loss

The two exact 9-color matching schedules from §1 are more than abstract edge-colorings. For each color class \(M_c\), the full set of disjoint two-port couplers can be activated simultaneously, with exact single-layer unitary \(U_c(\theta)=\exp[-i\theta A_{M_c}]\). Its \(2\times2\) blocks are \(\cos\theta\,I-i\sin\theta\,\sigma_x\). The first-order product formula with \(r\) repetitions is

\[
U_r(t)=\left[\prod_{c=1}^{9}U_c(t/r)\right]^r.
\]

The new [Trotter producer](w33_20261008_photonic_trotter_depth_loss.py) computes exact 27×27 floating-point matrix evolution from every scheduled layer, tests unitarity and compares \(U_r\) with \(\exp(-itA)\) for both carriers. The required number of two-port stages is \(9r\). With \(t=0.78\), the *positive difference* in the two devices' maximum offdiagonal transition probabilities is:

| Repetitions \(r\) | Two-port stages | Discrimination gap | Conditional survival, if independently 1% loss per stage |
|---:|---:|---:|---:|
| 1 | 9 | 0.008400 | 0.9135 |
| 2 | 18 | 0.112765 | 0.8345 |
| 4 | 36 | 0.212074 | 0.6964 |
| 8 | 72 | 0.253176 | 0.4850 |
| 16 | 144 | 0.264361 | 0.2352 |
| 32 | 288 | 0.267644 | 0.0553 |
| 64 | 576 | 0.268733 | 0.00306 |

The direct simultaneous-Hamiltonian discriminator (earlier pass) is **0.269465**. Increasing depth improves the idealized Hamiltonian approximation but greatly reduces unconditional photon throughput in this illustrative loss model. The particular \(0.99\) per-stage survival is **supplied**, not measured or implied by any chip. This points to a concrete engineering objective: optimize classification power *per launched photon* rather than ideal unitary fidelity alone. The calculation omits coherent fabrication error, stochastic correlated loss, Mach-Zehnder phase noise, interference between routes, switching speed and chip geometry. A loss-independent conditional discrimination gap does not remove the need for enough detected shots.
