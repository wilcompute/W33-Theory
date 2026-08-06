# Passes 4057–4064 — advanced physics closure

## Evidence status

All eight promoted statements are exact finite graph, group-character, projector, polynomial, lattice, Floquet, or canonical-ensemble results. They do **not** establish fabricated hardware, measured fidelity, a many-body phase, a chiral Standard Model, quantized pumping, gravity, cosmology, or a theory of everything.

Frozen certificate: `data/PART_4057_4064_ADVANCED_PHYSICS.json`  
Semantic SHA-256: `131ba5f89474a0283eedd0ae1ec5e5e6618b6d3e2bd6eeb8654fd4df8abbcd72`

## 4057 — transitionless non-Abelian holonomies

For the instantaneous dark projector \(P_D\), add the Kato/Berry counterdiabatic term

\[
H_{\rm CD}=i[\dot P_D,P_D]
=i\bigl(|\dot B_\perp\rangle\langle B|-|B\rangle\langle\dot B_\perp|\bigr).
\]

The ideal dark-space parallel transport is then exact at arbitrary finite duration. The Fubini–Study actions of the two previously certified loops are

\[
L_X=2\arccos(1/4)+\frac{\pi\sqrt{15}}2=8.719900157\ldots,
\]

\[
L_Z=\frac\pi3+\frac{\pi\sqrt3}{2}=3.767896598\ldots.
\]

A constant-speed schedule of duration \(T\) needs peak counterdiabatic norm \(L/T\); with control cap \(A\), \(T\ge L/A\). Uniform loss gives no-jump survival \(e^{-\kappa T}\). This closes the ideal finite-time gate, not its hardware synthesis.

Primary background: Berry, *Transitionless quantum driving*, J. Phys. A **42**, 365303 (2009); Song et al., arXiv:1509.00097.

## 4058 — complete \(PSp(4,3)\) dark-pair character decomposition

The four projective symplectic transvections indexed by \(24,26,2,16\) generate a permutation group of order \(25,920\), with 20 conjugacy classes. For every class representative,

\[
\chi_{H_1}(g)=\chi_E(g)-\chi_V(g)+1,
\qquad
\chi_{\mathcal D}(g)=\frac{\chi_{H_1}(g)^2+\chi_{H_1}(g^2)}2-\chi_E(g).
\]

The 20-class center algebra was reconstructed directly and simultaneously diagonalized. Grouping equal-degree ordinary irreducibles, the 3,161-dimensional contact-dark module decomposes with multiplicities

| degree | multiplicities among equal-degree irreps |
|---:|:---|
| 1 | 0 |
| 5 | 1, 1 |
| 6 | 2 |
| 10 | 1, 1 |
| 15 | 1, 3 |
| 20 | 5 |
| 24 | 2 |
| 30 | 3, 6, 6 |
| 40 | 4, 4 |
| 45 | 4, 4 |
| 60 | 9 |
| 64 | 8 |
| 81 | 9 |

The weighted dimension is exactly 3,161. There is no trivial constituent. The rank-160 bright contact sector is an equivariant copy of the incidence-edge permutation module, and

\[
P_{\mathcal D}V_{\rm contact}P_{\mathcal D}=0.
\]

Thus contact-only first-order pair hopping inside the dark sector is exactly forbidden. Equal-degree ATLAS suffixes are deliberately not guessed.

## 4059 — local-query Hodge cooler

The nonzero Levi Laplacian spectrum is

\[
\{4-\sqrt6,4,4+\sqrt6,8\}.
\]

Therefore \(x^{-1/2}\) is represented **exactly on the physical spectrum** by the cubic Lagrange polynomial

\[
p_3(x)=\sum_{\lambda}\lambda^{-1/2}
\prod_{\mu\ne\lambda}\frac{x-\mu}{\lambda-\mu}.
\]

The polar map is

\[
Q=D^Tp_3(DD^T),
\qquad Q^TQ=I-J/80,
\qquad QQ^T=P_{\rm cut}.
\]

It requires three nearest-neighbour Levi-Laplacian applications and one incidence application. Together with the bounded degree-five sign/QSVT compiler from Pass 4049, the formerly dense polar swap has an exact local-query implementation. The collapsed matrix \(Q\) remains dense; the locality is circuit/query locality, not a single sparse static Hamiltonian.

## 4060 — gauge-covariant Wilson matter on the four-dimensional tower

With four anticommuting Hermitian gamma matrices and \(\gamma_5\), define

\[
H(k)=\sum_{\mu=1}^{4}\gamma_\mu\sin k_\mu
+\gamma_5\left[m+r\sum_\mu(1-\cos k_\mu)\right],
\]

tensored with \(I_{81}\) on the W33 harmonic fiber. It is nearest-neighbour and becomes exactly gauge covariant after inserting link variables \(U_\mu(x)\) and \(U_\mu(x)^\dagger\).

For \(m=0,r=0\), all 16 Brillouin-zone corners are zeros. For \(m=0,r=1\), only \(k=0\) remains gapless; the other corners acquire Wilson masses \(2,4,6,8\). The continuum expansion is Dirac-like,

\[
H(k)=\gamma\cdot k+m\gamma_5+O(|k|^2),
\]

but the Wilson term explicitly breaks exact chiral symmetry. This is a vectorlike lattice matter model, not a chiral gauge theory. The boundary is consistent with the Nielsen–Ninomiya no-go theorem.

Primary background: Nielsen and Ninomiya, Phys. Lett. B **105**, 219–223 (1981).

## 4061 — irrational Floquet clock plus Coulomb ports: exact no-pump result

For \(\cos\phi=1/80\), the Floquet source has components \(e^{\pm in\phi}\). A static linear Coulomb port gives

\[
V_n=Z_d(s)I_n.
\]

It preserves the input quasifrequencies and creates no sidebands. Moreover,

\[
\frac1N\sum_{n=0}^{N-1}e^{in\phi}\to0,
\qquad
\left|\sum_{n=0}^{N-1}e^{in\phi}\right|
\le\frac{2}{|1-e^{i\phi}|}=1.4231361339\ldots.
\]

Hence the DC current vanishes and cumulative transport is bounded. One irrational phase feeding a static response has no two-parameter Berry curvature, filled band, or integer Thouless pump. Quantized transport requires at least a second independently cycled control plus a maintained gap.

Primary background: Thouless, Phys. Rev. B **27**, 6083–6087 (1983).

## 4062 — outside-box distance-to-quasienergy transducer

For normalized projected link states, the distance law is

\[
|\langle u_e|u_f\rangle|=3^{-d},\qquad d=1,2,3,4.
\]

The product of their Householder reflections has nontrivial rotation angle

\[
\theta_d=2\arccos(3^{-d}),
\qquad
d=-\log_3|\cos(\theta_d/2)|.
\]

All four rotations have infinite order. This is an exact graph-distance spectrometer, not physical proper time or gravitational redshift.

## 4063 — outside-box dark-pair residual thermodynamics

The repulsive projected contact Hamiltonian has 3,161 exact zero modes. Consequently

\[
S(T\to0)=k_B\ln3161=8.058643712\ldots k_B,
\]

and the infinite-temperature probability of landing in the dark manifold is

\[
\frac{3161}{3321}=0.9518217404\ldots.
\]

The exact finite-spectrum heat capacity has a small Schottky peak near \(eta U=8.072\), with \(C/k_B=0.0253783\ldots\). Contact cooling therefore preserves a huge information reservoir instead of selecting a unique state.

## 4064 — outside-box supersymmetric fault odometer

The Levi incidence graph has edge connectivity four. Therefore any arbitrary removal of \(r\le3\) couplers leaves it connected and forces

\[
\dim H_1=81-r,
\qquad
\mathcal I_W=-80+r.
\]

At four failures, a minimum cut can isolate a degree-four vertex and the simple staircase can first break. Counting Hodge zero modes thus gives an exact topological odometer for up to three arbitrary missing couplers. It does not identify their locations and is not particle supersymmetry.
