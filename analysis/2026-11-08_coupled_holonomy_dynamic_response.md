# Four native holonomies: coupled modes and a frequency-dependent scalar kernel

The preceding packet a040a352be811f6ebd5c104a985df49acb694025 derived a full27-band scalar Wilson potential but correctly withheld a finite-torus particle-mass interpretation. This packet computes the coupled four-coordinate Hessian, native electric inertia, observable spectral weights and a frequency-dependent scalar-loop response. It supplies poles of an explicitly retained quadratic model, not the complete gauge-theory propagator or a solved TOE.

## Prior ownership and reading

The native27-site/135-link four-period cover, harmonic profiles h and metric M belong to Pass11991 and the October27 propagation/response work. The preceding scalar packet owns the action, full-band trace square root, fourth-axis winding witness and finite-volume upper comparison.

The earlier TOE56 bosonic-holonomy source already proves a positive-walk log-determinant bound and tests a three-holonomy Hessian on the different80-site Levi cover. TOE57 already compares bosonic and spinless-fermion thermal determinants. They were reread before constructing this continuation. The general bosonic diamagnetic mechanism is not new.

The October27 acoustic vacuum-density report already emphasizes temporal density vertices when comparing gauge responses. We apply that lesson below. Pass11991's108-dimensional Euclidean Ginsparg–Wilson kernel is also prior work. Its definition and limitations were read; no Euclidean singular value is relabeled as a continuous-time fermion energy here.

[Kan–Shiraishi2212.07049, sectionII](https://arxiv.org/html/2212.07049v2#S2) provides standard scalar graph-propagator/holonomy context. The section was revisited, not the full paper. [Ghilencea–Hoover–Burgess–Quevedo0506164](https://arxiv.org/abs/hep-th/0506164) provides toroidal scalar Casimir context; its abstract was read, not the40-page analysis. An attempted v3 HTML link failed; the actual paper has a v1 abstract. The oscillator bubble, Schur complement and resolvent expansion below are standard Gaussian/spectral methods applied to the named native action. No priority claim follows from corpus searches.

## Four variables, rather than one held coordinate

Use finite periods s=(N,N,N,L), four holonomies Theta_i and one free complex scalar of bare mass m>0. Static momenta are k_i=(2pi n_i+Theta_i)/s_i; every27-dimensional Bloch band is retained. Potential and inertia are expressed per noncompact three-cell.

For the supplied microscopic link kinetic coefficient1/g², the tree electric metric is

\[
G=\frac{L}{g^2}\,\mathrm{diag}(s_i^{-1})\,M\,
\mathrm{diag}(s_i^{-1}),\qquad M=h^Th.
\]

The actual static normal modes solve K v=omega² G v with K=V_ThetaTheta(0), not a scalar division by an isolated diagonal coefficient.

Every winding walk contributes a nonnegative coefficient times1-cos(w.Theta). Four literal based paths with primitive periods e_i are constructed from the prior native loops. Their repeated winding witnesses imply

\[
K\succeq\mathrm{diag}(c_i)>0,\qquad
c_i=\frac{L\,\Gamma(r_i-\frac12)}
{\sqrt{\pi}\,r_i!\,(10+m^2)^{r_i-\frac12}},
\quad r_i=s_i\,\ell_i,
\]

where ell_i is that primitive path's length. This proves strict stability and a unique global minimum modulo2pi in each coordinate for the declared scalar-only finite torus. It does not select the periods or the scalar inventory, and the paths are not claimed shortest.

For G-orthonormal eigenvectors v_j, the fourth-holonomy observable has normalized static weights

\[
w_j=\frac{|(v_j)_4|^2}{(G^{-1})_{44}},\qquad \sum_jw_j=1.
\]

Individual weights inside an exactly degenerate eigenspace are basis dependent; their sum is physical within this quadratic model.

## A finite-volume counterexample to diagonal curvature as a mass

At N=L=2,m=0.8,g=0.5, the static generalized squared frequencies occur in two doublets:

*0.0002191244854* and *0.0002255707983*.

The old single-coordinate diagnostic K44*(G^-1)44 is0.0005012684407, equal to neither. The fourth-coordinate spectral weights sum to0.4 and0.6 over the two doublets.

The doublets connect directly to the prior native group theory. The equal-period torus preserves the supplied H27 controller. Its two inequivalent real two-dimensional C3 character planes give exact rank-two projectors P1,P2 with P1+P2=I and P1P2=0. Both are self-adjoint in the exact native G metric. Applying those **already-owned** character planes to the new response gives exact fourth-holonomy weights2/5 and3/5. The symmetry supplement checks all27 controller matrices: K and Z0 invariance residuals are below8e-17, and K=G(lambda1 P1+lambda2 P2) reconstructs to2.4e-17. Unequal periods need not preserve this controller and the doublets split. These are representation-sector weights, not particle generations or spins; the group classification belongs to Pass11991.

The H27 center acts trivially on this selected period quotient, as the supplement checks. It is not a faithful quantum Pauli carrier.

A second basis test keeps the physical fourth coordinate fixed while replacing Theta1 by chi1+chi4. The diagonal-curvature diagnostic changes, but generalized eigenfrequencies and properly transformed observable weights agree. Thus its failure is a coordinate issue, not a choice of plotting normalization.

For m=0.8,L=2, increasing N=2,3,4,6,8 gives static squared frequencies divided by g²:

| N | three lowest frequencies squared/g² | largest frequency squared/g² |
|---:|---|---:|
|2|0.00087650,0.00087650,0.00090228|0.00090228|
|3|0.00009967,0.00010785,0.00011306|0.00030468|
|4|0.00001425,0.00001625,0.00001757|0.00026236|
|6|3.78e-7,4.92e-7,5.52e-7|0.00025654|
|8|1.15e-8,1.76e-8,2.03e-8|0.00025642|

The fourth-holonomy weight in the largest-frequency mode is approximately0.99972 at N=3 and0.99999995 at N=4. This is finite-volume evidence approaching the previously stated one-scalar/noncompact limit. It is not a proof of a selected3+1-dimensional physical vacuum or a calibrated infinite-volume error estimate.

## Frequency dependence from the same scalar action

A time-dependent calculation must specify a spatial profile and temporal gauge. We use harmonic edge phases h_ei Theta_i(t)/s_i, with background A0=0. Integer-tree-gauge profiles V differ from h by a vertex gradient. They give the same static Hessian, but replacing h by V dynamically while discarding the transformed temporal density vertex changes the model. An explicit control finds equal static K and unequal loop kinetic response.

Let omega_a=sqrt(m²+lambda_a), p_ab=omega_a+omega_b and X_i=U†H_iU, with H_i differentiated along the harmonic profile. The exact zero-temperature scalar frequency integral is

\[
\int\frac{d\omega}{2\pi}
\frac{1}{(\omega^2+\omega_a^2)((\omega+\nu)^2+\omega_b^2)}
=\frac{p_{ab}}{2\omega_a\omega_b(p_{ab}^2+\nu^2)}.
\]

For C_ijab=Re[X_iab conj(X_jab)]/(2omega_a omega_b), including the compact/noncompact volume factor, the retained homogeneous one-loop kernel is

\[
\Pi(\nu)=D-\sum_{ab}\frac{C_{ab}p_{ab}}{p_{ab}^2+\nu^2},\qquad
K=\Pi(0),\qquad
Z(0)=\sum_{ab}\frac{C_{ab}}{p_{ab}^3}\succeq0.
\]

D is the actual diamagnetic contact. The minus sign and normalization match the independently differentiated full-band trace square root. Independent real-frequency quadrature checks the bubble integral.

Below the conservative pair threshold s=omega_physical²<4m², analytic continuation gives

\[
F(s)=K-s[G+Z(s)],\qquad
Z(s)=\sum_{ab}\frac{C_{ab}}{p_{ab}(p_{ab}^2-s)}.
\]

Each C_ab is a real positive Gram matrix. Therefore

\[
F'(s)=-G-\sum_{ab}\frac{C_{ab}p_{ab}}{(p_{ab}^2-s)^2}\prec0.
\]

For the benchmarks, F starts positive and is negative before the threshold, giving four subthreshold modes counted with multiplicity. The source checks these signs. Residues use the full derivative -F'(s), not just G. They are positive.

## Positive oscillator-bath representation and controlled root computation

Factor each positive C_ab*p_ab as WW^T. The kernel is the Schur complement of an auxiliary oscillator bath with squared frequencies p_ab² and contact D. Since K=D-sum C_ab/p_ab is positive and G is positive, this enlarged quadratic Hamiltonian is positive. The representation explains the positive residues and the reduction in low-frequency spectral weight. It is a spectral representation of the already-computed loop, not a new microscopic field inventory.

Direct native root searches took1577.12s. The accelerated constructor uses three resolvent moments,

\[
Z_r=\sum C/p^{3+2r},\qquad Z(s)\approx Z_0+sZ_1+s^2Z_2.
\]

For q=s/(4m²)<1, the omitted positive matrix is bounded by q³ Z0/(1-q). Every candidate root and residue is then checked against the **unexpanded** kernel. The constructor completed in9.49s with the same spectrum to numerical tolerance. The analytic bound controls series truncation, not floating roundoff.

For N=L=2,m=0.8,g=0.5, the dynamic squared frequencies are0.0002190882420 and0.0002255360536, each with multiplicity2. Their fourth-coordinate residue fractions are0.39993384 and0.59990758. The retained low modes carry about0.99984142 of the tree observable sum rule; scalar-pair modes carry the remainder in the bath representation. The shifts are around0.015–0.017% relative to the tree-inertia static frequencies for this benchmark.

## What was tested and what remains missing

The receipt records22 new controls plus22 preceding full-band controls: full mixed Hessian differences, the previous fourth curvature, harmonic/tree dynamic-profile distinction, positive response matrices, geometric remainder bounds, coupled roots/residues, coordinate changes, four literal paths and independent server calculations.

The separate symmetry producer also verifies the two exact rational character projectors, their G-self-adjointness, complementary images, all27 numerical K/G/Z0 symmetries and the reconstructed two-sector mass operator. It is regenerated after the main response and records both parent hashes.

The actual server V8 integrated the bubble and solved a generic two-channel/three-bath-mode Schur problem. A separate dense five-oscillator generalized eigenproblem reproduces its roots and residues. A70-digit mpmath determinant/root calculation confirms the server residues to about2e-15; ordinary dense double-precision eigenvector residues differed by4e-14, so their test uses an explicit1e-12 numerical budget.

This is **tree electric inertia plus a scalar-one-loop homogeneous quadratic kernel**. It is not a complete fixed-order gauge-QFT pole result: higher-loop potential corrections, local A0/Gauss response, inhomogeneous gauge fluctuations and other charged fields are absent. Solving this selected kernel exactly does not manufacture those missing contributions. Physical units, compactification selection, radius dynamics, chiral matter, production, observed cosmology, vacuum energy and gravity remain open.

Pass11991's108-dimensional Euclidean overlap kernel is not used as a fermion Hamiltonian. A suitable transfer/Hamiltonian construction with charge, parity and anomaly accounting is needed before adding its physical vacuum-energy loop. The older spinless thermal fermion determinant is a different matter model.

Full extracted PDF pages117–118 were read after checking the unchanged manuscript hash003b75482b6584e20e83a55d9e9ba0a181f93b8dff0f94c1d615039c21213cbb. Personal text coverage is now1–118 of215. The bosonic SU9 vacuum, charged-spectrum and hidden-modulus claims there were read, not independently re-proved. Full weekly/older-batch and manuscript reading remain unfinished.

Five independent next investigations:

1. Include temporal density and inhomogeneous gauge vertices in a common Gauss-reduced response.
2. Construct a compatible charged Dirac Hamiltonian/transfer operator on this cover.
3. Couple the four holonomies to a dynamical radius and complete charged inventory.
4. Solve matter occupation and finite-density backreaction in the same action.
5. Test interacting continuum cone selection and physical units before identifying particles.
