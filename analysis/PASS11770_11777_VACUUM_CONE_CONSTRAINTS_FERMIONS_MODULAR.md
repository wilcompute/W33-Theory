# Passes11770–11777: a positive vacuum floor and the missing continuum structure

All five requested directions were investigated with actual operators, plus
three independent dynamical probes. The strongest theorem is **H>=delta I for
some delta>0** for the proposed11769 current-square Hamiltonian. This excludes
the previously open possibility of normalized states approaching zero energy.
It does not prove an attained ground state or an excitation gap.

The constructive results are a common-cone quadratic lattice extension, an
explicit central-charge conversion and its degrees-of-freedom cost, a
Clifford-current supercharge with local spin curvature, and a sharper modular
obstruction with continuous-rapidity kinematics as a controlled alternative.
Three independent probes improve the symmetry-preserving vacuum trial to
127.6195090727, expose a rank-changing principal symbol and construct a bounded
current regulator with quantitative form errors.

These are investigations of a proposed dynamics, not a completed TOE.

## Inputs, prior work and execution map

The current algebra belongs to `w33_pass11767_global_current_algebra.py`;
its full rational closure is sl78 semidirect h157. The actual quantum
Hamiltonian, its Gaussian family and single-direction Hermite trial belong to
`w33_pass11769_quantized_current_vacuum.py` and its report.

Prior work was searched by results as well as topics, in RESULTS_INDEX,
analysis producers/reports, the paper and docs/index. Relevant earlier owners:

- BT4253_BT4260, pass4259, already has the point-line Gaussian modular
  spectrum with fifteen pure spectators for **K=5I-A**. Its certificate was
  read. The state below has a different covariance and a different modular
  scale; fifteen spectators themselves are not new.
- BT4057_BT4064, pass4060, already builds4D Wilson matter and16 doubling
  corners. BT4105_BT4112 and PASS11570_11579 already build overlap controls.
  Neither Wilson lifting nor fermion doubling is a new result here.
- BT921 already identifies the finite Hodge-Dirac10/16 spectral sectors.
  Their reappearance below is an explicitly derived variational response of
  the new interacting Hamiltonian, not a new spectral inventory or a mass fit.
- Pass5682 already separates graph-cover causality from metric/tick units.
  The spatial lattice, dimension and speed below are supplied and credited
  as additional physical input.
- `w33_ledger_modular_flow_firewall.py` already excludes nontrivial continuous
  modular flow inside the finite Pauli permutation skeleton. The obstruction
  below concerns the much larger typeI oscillator algebra, not that finite set.
- Parallel commits4b42fb759 through935e670ee construct the dressed antiunitary
  T(q,p)=(Dp,Dq), verify all160 currents and establish its balanced-bipartite
  scope. `2026-10-08_dressed_current_antiunitary.md` owns this symmetry.
  The additional Gaussian-family calculation below makes its action explicit.

| Requested direction | Executed object | What remains physically unresolved |
|---|---|---|
| Vacuum and gap |11770 proves a positive floor;11775 gives an explicit improved upper bound | Attainment, numerical lower bound, excitation gap |
| Relativistic propagation |11771 derives a kinetic-matched common quadratic cone on a supplied lattice | Selected spatial dimension, interacting Lorentz symmetry, native continuum |
| Consistent constraints |11772 cancels the central charge on an enlarged canonical space and performs the reduction | A nontrivial physical constraint algebra retaining matter |
| Chiral fermions and interactions |11773 builds an odd Clifford-current operator and its exact spin-curvature coupling | Spacetime Weyl chirality, nonzero index, SM representation/Yukawa dictionary |
| Geometry from observable algebras |11774 computes actual modular data, proves the eigenbasis obstruction and checks continuous-rapidity operators | A standard local algebra net, geometric inclusions and gravity |
| Additional probes |11775 symmetric trial;11776 principal degeneracy;11777 bounded propagation | Controlled infrared/thermodynamic limit of the original dynamics |

## 11770: proof of a strictly positive energy floor

Use W=(u,s)-perp, dim78, a=1/sqrt20, and the prior operators
J_e=(V_e.q+a)(U_e.p+a). Their inner product U_e.V_e is exactly zero.
Each current has the explicit unitary flow

\[
(e^{-itJ_e}\psi)(q)=
 e^{-ita(V_e.q+a)}\psi(q-t(V_e.q+a)U_e).
\]

The affine pullback has determinant1 and preserves Schwartz space; the phase
has modulus1. These flows integrate the standard Schrödinger representation
of the connected current group. Its Lie algebra is certified by11767 and
contains the real SL78 Levi algebra. On the Levi subgroup the representation
is the ordinary determinant-one coordinate action on L²(R78).

For a form-domain vector psi, a current-control path of total Euclidean
control length L satisfies

\[
\|\pi(g)\psi-\psi\|\le
 L\left(\sum_e\|J_e\psi\|^2\right)^{1/2}.
\]

For one exponential this is the spectral-theorem estimate
||(exp(-itJ_e)-I)psi||<=|t| ||J_e psi||. For a finite product, telescope with
unitary prefixes; all differences act on the original psi. Piecewise-constant
control approximation gives the path estimate. No assumption that energy is
invariant under the generated group is needed.

The currents bracket-generate the connected finite-dimensional group. The
associated control metric is finite and induces its topology: products of
the generating flows and their conjugates give local coordinates, and finite
translations cover a compact set. Hence the maximum control distance L_Q on
any compact subset Q of the Levi subgroup is finite.

SL78(R) has property(T), by
[Bekka–de la Harpe–Valette, Theorem1.4.15](https://perso.univ-rennes1.fr/bachir.bekka/KazhdanTotal.pdf).
Choose a compact Kazhdan pair(Q,epsilon), epsilon>0. The restricted
Schrödinger representation has **no** SL78-invariant L² vector: SL78 acts
transitively on R78 minus0; invariant measurable functions are constant almost
everywhere, and a nonzero constant is not square-integrable.

Consequently, for every psi,

\[
\epsilon\|\psi\|\le\sup_{g\in Q}\|\pi(g)\psi-\psi\|
 \le L_Q\sqrt{\langle H\rangle_\psi}.
\]

Thus the closed quadratic form satisfies

\[
\boxed{H\ge\delta I,\qquad \delta=(\epsilon/L_Q)^2>0.}
\]

This is a theorem about the actual fixed160-generator ansatz and its supplied
nonzero-center representation, not a finite Fock-cutoff estimate. The argument
does not give a numerical epsilon/L_Q, compact resolvent or a lowest
eigenvector. A gap **above zero** must not be called a gap **above a vacuum**.
The newer statement resolves only the spectral-infimum question explicitly
left open in11769; its classical zero remains valid.

## 11771: one common cone is a kinetic compatibility condition

Keep the optimized11769 Gaussian covariance fixed and vary its coherent
displacements. Put b=1/20 and denote the edge covariances by
vx=t m, vy=m/t+f²tm, c=ftm. The exact expectation yields the quadratic Hessian

\[
K=\begin{pmatrix}Q&R\\R^T&P_p\end{pmatrix},\quad
Q=2(vy+b)(4P-A),\quad P_p=2(vx+b)(4P+A),
\quad R=4(c+b)B_\Sigma^T.
\]

Here A is restricted Levi adjacency, P is the W identity and
B_Sigma=D(4P-A). This is variational small-oscillation dynamics, not the
exact quantum excitation spectrum. With

\[
\alpha=4[(vx+b)(vy+b)-4(c+b)^2]>0,
\]

the phase-space flow F=Omega K satisfies
F²=-diag(alpha(16P-A²),alpha(16P-A²)). There are48 variational modes at
omega²=10alpha and30 at16alpha.

On an externally supplied lattice of cells, a naive position spring adds
kappa ell(k) I to Q. The speed then depends on the kinetic eigenvalue
2(vx+b)(4+lambda). The +sqrt6,-sqrt6 and0 sectors generally see different
quadratic cones. A common speed has not emerged from the naive spring law.

Instead add kappa ell(k) P_p^-1 to Q. Exactly

\[
P_p^{-1}=\frac{P/4-A/10+A^2/40}{2(vx+b)}.
\]

The flow-square shifts by -kappa ell(k)I in every internal sector. On W the
inverse is a degree-two polynomial in full Levi adjacency, so it can be
implemented using internal paths of length at most two; a dense numerical
inverse is unnecessary.

On a supplied3D cubic lattice of spacing ell, choosing kappa=c0²/ell² gives

\[
\omega_j(k)^2=\omega_j(0)^2+
 \frac{4c_0^2}{\ell^2}\sum_i\sin^2(k_i\ell/2)
 \longrightarrow\omega_j(0)^2+c_0^2|k|^2.
\]

The same kinetic form fixes the gradient coupling for all sectors. This is a
constructive common-cone rule; the lattice,3 spatial dimensions, c0 and the
quadratic restriction are supplied. Interactions, renormalization and gravity
have not been shown to preserve this cone.

## 11772: cancelling the central obstruction has a physical cost

Tensor the original nonzero-center representation with an auxiliary opposite
central charge. The diagonal constraints satisfy
C_A=hat(A,+) tensor I+I tensor hat(A,-), [C_A,C_B]=i C_[A,B], C_Z=0.
For each canonical mode the Heisenberg constraints can be written

\[
C_q=q_1+q_2,\qquad C_p=p_1-p_2,\qquad[C_q,C_p]=0.
\]

They have independent Hamiltonian vector fields. The enlarged312-dimensional
phase space has156 independent first-class constraints, leaving
312-2*156=0 dimensions. The distribution delta(q1+q2), constant in the
relative coordinate, is a formal solution; it is not an L² vector. In a
rigged-space reduction, imposing the full Heisenberg set leaves one formal
state. The trace-zero Levi action preserves it.

This repairs the central algebra but eliminates the candidate canonical
matter. Imposing fewer constraints needs a physical selection principle;
the full current algebra cannot simply be renamed gravitational gauge symmetry.

## 11773: a fermionic extension forces a spin-curvature interaction

Supply a complex Clifford module with160 Hermitian gamma_e. The odd operator

\[
\mathcal D=\sum_e\gamma_e\otimes J_e
\]

has a2^80-dimensional spinor factor. Its exact square is

\[
\mathcal D^2=I\otimes H+
 \sum_{e<f}\gamma_e\gamma_f\otimes[J_e,J_f].
\]

Only480 adjacent edge pairs contribute; all disjoint-edge commutators vanish.
The added spin sector therefore couples to local current curvature, rather
than being a label pasted onto the scalar spectrum. Clifford chirality
anticommutes with D. The positive floor for H does not automatically apply to
D²: the spin-curvature term can cancel bosonic energy.

No Fredholm index,3+1 Weyl operator, SM fermion dictionary or E6 Yukawa map
follows. A supplied nearest-neighbor3D Weyl control sigma.sin(k) has eight
zeros with four positive and four negative Jacobian signs. The Wilson masses
are2 times the number of pi components; lifting mirrors changes the cutoff
chiral symmetry. This is standard prior
[Nielsen–Ninomiya](https://maggiexheuw.github.io/pdf/nielsen19812.pdf),
already used by the repo's earlier Wilson and overlap constructions.

## 11774: the missing structure is an observable algebra, not Fock dimension

For the actual11769 Gaussian family, the point subsystem has39 modes. Its
symplectic eigenvalues are exactly1/2, multiplicity15, and2/sqrt10,
multiplicity24, independent of t and the local phase fD. Thus the full point
algebra has a nonfaithful reduced state. The faithful thermal support has one
modular energy

\[
\varepsilon=\log\frac{4+\sqrt{10}}{4-\sqrt{10}},
\]

repeated24 times. Fifteen spectators were already present in pass4259's
different harmonic model. The new calculation binds the spectrum to the
actual interacting-model trial.

There is a stronger exact spectral obstruction. Suppose K has a complete
eigenbasis and Pplus>=0 obeys
exp(itK)Pplus exp(-itK)=exp(-ct)Pplus, c nonzero. In each K eigenvector, the
Pplus spectral probability measure is dilation invariant. Disjoint logarithmic
annuli have equal mass, forcing zero mass on(0,infinity). It is concentrated
at0; the complete eigenbasis is annihilated, so Pplus=0. This proof needs no
finite Pplus moments and avoids unbounded-commutator domain assumptions.

On the faithful24-mode support, the standard modular generator is
epsilon(N_left-N_right), with a complete occupation eigenbasis. More generally
every faithful normal state on a typeI factor B(K) has a trace-class density
operator with an eigenbasis; its standard modular generator has the same
pure-point feature. Infinite oscillator Fock dimension by itself is therefore
insufficient for nontrivial geometric modular translations. This is consistent
with the established
[half-sided modular inclusion theory](https://arxiv.org/abs/math/0412061),
not a claim of a new general modular theorem.

The symmetric11775 trial entangles the two kernel factors but has kernel
Schmidt rank at most2. It still is not separating for their full algebras.
An improved finite variational ansatz does not silently repair this boundary.

For comparison, on L²(R,dtheta) the supplied operators
B=-i partial_theta, Pplus=exp(theta), Pminus=M²exp(-theta) satisfy exact
dilation relations, positive translations and
[(Pplus+Pminus)/2]²-[(Pplus-Pminus)/2]²=M². Symbolic differential checks verify
this1+1 kinematics. It has continuous boost spectrum. It is not the current
Hamiltonian, a derived local net or a prediction of M.

A standard local-net construction needs additional algebra/state information.
Even half-sided inclusions can have trivial relative commutants, as explicit
[Lechner–Scotford examples](https://arxiv.org/abs/2111.03172) show. Nor does
the abstract Hilbert space L²(R78) itself prohibit typeIII subalgebras: a
separately constructed observable net could use them. What fails is the
automatic identification of ordinary finite-mode subsystem algebras with
geometric wedge algebras. A thermodynamic/continuum phase or another explicit
net construction is required on this route.

## 11775: a symmetry-preserving non-Gaussian state with a better bound

For every point i use the actual integer vector w_i=24(P_point15)e_i, with
entries9,-3,1. For every line use the analogous line kernel. The standard
normal variables Y_i=w_i.q/sqrt(108t) have pair correlations1,-1/3,1/9 with
multiplicities1,12,27. Define Phi_P as the sum of forty normalized He4(Y_i)
states, and similarly Phi_L. Their common squared sum norm is exactly

\[
N=40(1+12/81+27/6561)=11200/243.
\]

The normalized states psi,Phi_P,Phi_L are orthogonal and preserve all
bipartition-preserving incidence automorphisms. No point-line self-duality is
assumed. A degree-four Hamiltonian cannot transfer four Hermite quanta out of
one kernel and create four in the independent other kernel, so their mutual
Hamiltonian matrix element is zero. Their diagonal matrix elements agree;
the two couplings to psi are complex conjugates.

The resulting explicit3x3 Ritz matrix gives

\[
\boxed{E_{\rm trial}=127.61950907272602.}
\]

Seven-node and eight-node four-variable Gaussian quadrature independently
check the degree<=12 matrix elements. The certificate stores the actual
normalized complex coefficients and exact Gram norm. This improves the prior
single-point trial128.8680657318 while preserving the finite symmetry. It is
not an exact vacuum or a numerical lower bound.
The displayed decimal uses floating matrix elements and independent
degree-exact quadrature; it is not an outward-rounded interval for all digits.

### Connection to the new parallel antiunitary: the optimized Gaussian is fixed

The parallel construction fixes every current under the antiunitary Fourier
map T(q,p)=(Dp,Dq). It also acts within the actual11769 Gaussian family.
Write its precision G=C0^-1/t-i fD. Using D C0 D=C0^-1 on W,

\[
G\longmapsto D\overline G^{-1}D
=\frac{t}{1+f^2t^2}(C_0^{-1}-iftD),
\quad t'=\frac{1+f^2t^2}{t},\quad
f'=\frac{ft^2}{1+f^2t^2}.
\]

The Gaussian energy is exactly invariant under this involution. At the
optimized11769 parameters, f=-2b/(3mt+b) and the exact stationarity polynomial
(t²-1)(3mt+b)²-4b²t²=0 imply t²(1-f²)=1. Therefore t'=t, f'=f: **the
optimized Gaussian is a T-invariant ray despite its nonzero phase**. This
sharpens the parallel report's general discussion of how T acts on trial
states; the symmetry itself is credited to that track. Symbolic energy and
stationarity identities, precision-matrix checks away from the optimum, and
an independent full Wigner-covariance check establish the connection.

This concerns an internal antiunitary. Physical time reversal, observed CP
violation and a thermodynamic arrow remain separate unresolved questions.

## 11776: the principal symbol is rank-changing but bracket-generating

At q=0 the principal fields X_e=(V_e.q+a)U_e span all78 configuration
directions. At the prior classical star-zero configuration, only four fields
are nonzero. Their exact Gram eigenvalues are1,1,1,24/5: rank4, not78.

Forgetting multiplication blocks r,z in the certified full closure gives
sl78 semidirect R78, dimension6161. The translation part spans every tangent
space. Thus Lie brackets of the principal fields recover every tangent
direction, even at the rank4 points. Uniform ellipticity cannot be assumed;
bracket generation is a local regularity fact, not a proof of vacuum
attainment or compact resolvent at infinity.

## 11777: bounded current dynamics with a controlled regulator error

Define H_tau=(2/tau²)sum_e[I-cos(tau J_e)]. Each edge term has norm at most
4/tau², and disjoint terms still commute. On Schwartz vectors,

\[
0\le\langle H-H_\tau\rangle\le
 \frac{\tau^2}{12}\sum_e\|J_e^2\psi\|^2.
\]

This follows from the scalar cosine remainder and functional calculus. The
Gaussian fourth-current moment is computed by degree-exact quadrature and
independently checked by Wick recursion; the certificate gives actual
regularized energies and bounds for four tau values.

For fixed tau, bounded local terms permit commutator propagation estimates
of the usual [Lieb–Robinson](https://arxiv.org/abs/math-ph/0506030) kind. A
coarse degree-four weighted interaction sum is at most8J0 exp(mu), where
J0=4/tau²; the usual commutator iteration has a velocity parameter at most
64exp(mu)/(mu tau²). The argument uses commutation of disjoint local algebras;
an independent conservative finite-graph Taylor-tail bound is stored as well.

The bound diverges as tau tends to zero. Fixed-regulator locality therefore
does not prove finite propagation speed for the original unbounded H. Also,
H_tau<=H does not transfer the11770 lower bound to H_tau. Spectral convergence
needs more than convergence of form expectations on fixed Schwartz vectors.

## What this changes in the TOE search

The evidence points toward a **phase-selection problem**: a successful model
needs a state and observable net with geometric modular structure, a common
causal kinetic form and a nonzero physical chiral index, compatibly generated
by one dynamics. Finite representation counts alone do not impose those
conditions. This is a research hypothesis suggested by the executed tests,
not a demonstrated uniqueness principle.

The current-square model now has a proven positive floor, improved explicit
states, a constructive common-cone extension and precise tests for its
remaining structure. It still lacks a selected physical vacuum, a native
spacetime limit, observed masses/mixing/couplings, gravity and a cosmological
constant prediction. None of its dimensionless energies is inserted into
Einstein's equation.

## Validation

All three producers succeed. The focused suite has23 passing tests in10.68s:
13 new quantum-physics regressions, seven11769 regressions and three newly
reviewed parallel time-reversal regressions. The latter cover all1560
canonical-K witnesses, all160 dressed-current identities and balanced versus
unbalanced bipartite controls. The property(T) argument is an analytic proof
using the cited theorem and prior certified closure; numerical tests do not
replace it. A hosted workflow replays all three producers between two runs of
this same suite.

The rediscovery guard's alpha@16 candidates were inspected: BT1046 concerns
formal Higgs amplitudes on existing spectral sectors; BT818 concerns the graph
independence number; W36_PAPER contains the known10/16 spectrum. The existing
spectrum is credited above. The new claim is the actual Gaussian-displacement
Hessian and its kinetic-matched extension, not a new10/16 spectral law.
