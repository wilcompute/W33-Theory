# Pass11769: an interacting quantum dynamics from the actual edge currents

The user asked for a fresh attack on the missing physics. This investigation
replaces another finite-object correspondence with an explicit quantum energy
law and states on which it acts. It does **not** solve the TOE. The constructive
result is a positive interacting Hamiltonian built from the actual160 W33
currents, an algebraic Gaussian-family minimum, and an explicit non-Gaussian
state with lower energy. No observed parameters were fitted.

## Ownership and physical input

`analysis/w33_pass11767_global_current_algebra.py` owns the exact closure
sl78 semidirect h157. Its160 incidence generators are the input, not a new
discovery here. The older `analysis/W33_TWO_CONTINUA_symplectic_metric.md`
already discusses oscillator/phase-space representations; its proposed
two-mode continuum is a different carrier from the78-coordinate representation
below. This calculation supplies no finite-field-to-real limiting functor and
does not transfer that report's spacetime claims.

Schrödinger/Heisenberg quantization is standard prior mathematics; see
[de Gosson, math-ph/0505073](https://arxiv.org/abs/math-ph/0505073). The corpus
was searched for the construction and its resulting formulas, including
Stone–von Neumann, sum-of-squares currents, h157, positive energy, the numerical
trial values and their exact radicals. No novelty is claimed for quantization
itself, the incidence spectrum or general variational methods.

The proposal here is **H=sum of squared represented edge currents**. That law
is supplied and testable. It is invariant under bipartition-preserving incidence
automorphisms, but is not invariant under the full generated noncompact current
algebra. The latter acts as dynamical operators, not as an unbroken gauge
symmetry. Central charge and an overall energy unit remain supplied conventions.

## From finite matrices to quantum variables

Let u=ones80, s=(ones40,-ones40), W=(u,s)-perp, and P its orthogonal projector.
Use the adapted basis (u/sqrt80,W,s/sqrt80). Each incidence e=(i,j) has

\[
U_e=P(e_i+e_j),\quad V_e=P(e_i-e_j),\quad a=1/\sqrt{20}.
\]

The corresponding block matrix has B=U V^T, r=a V^T, v=a U, z=a².
Exactly U.V=0 and ||U||²=||V||²=39/20.

On L²(W), take [q_i,p_j]=i delta_ij, p=-i partial_q. The block algebra has the
Hermitian realization, on Schwartz space,

\[
\widehat A=p^T Bq+r q+v^T p+zI,
\qquad [\widehat A,\widehat C]=i\widehat{[A,C]}.
\]

The edge operator factorizes:

\[
J_e=(V_e\cdot q+a)(U_e\cdot p+a).
\]

The two factors commute, so J_e is symmetric on the common domain. The
proposed H=sum_e J_e² is nonnegative there and has a Friedrichs extension.
This is an interacting differential operator on78 continuous coordinates,
not a78-state quantum system. Nonzero Heisenberg central charge cannot act on
any finite-dimensional complex Hilbert space: tracing [Q,P]=iI rules it out.

The linear alternative fails as stable energy. Its sum is

\[
\sum_e J_e=p^T B_\Sigma q+8I,\quad
B_\Sigma=D(4P-A),\quad B_\Sigma^2=16P-A^2,
\]

where D=diag(+1 points,-1 lines), and A is the Levi adjacency restricted to W.
Its eigenvalues are +/-sqrt10, each24 times, and +/-4, each15 times.
Coherent displacements make the expectation arbitrarily positive or negative.
Lie closure alone therefore did not provide a lower-bounded energy.

There is an exact locality distinction. For disjoint edges e,f, both
U_e.V_f and U_f.V_e vanish, including the projection corrections. Thus
[J_e,J_f]=[J_e²,J_f²]=0. Every formal nested commutator ad_H^k(J_e) is a sum
of current words supported within distance k in the graph whose vertices are
incidence edges and whose neighbors share an endpoint. Consequently
[ad_H^k(J_e),J_f]=0 when that distance exceeds k+1. Induction uses only that
commutators with a disjoint local term vanish. The dense **Lie closure** does
not erase this **Hamiltonian interaction** structure. For these unbounded
operators the support identity is not a uniform propagation-speed bound, and
the finite W33 graph has not become a spacetime continuum.

## An exactly solved restricted vacuum problem

For psi proportional to exp(-q.C^-1.q/2), q covariance is C/2 and p covariance
C^-1/2. The actual incidence data give

\[
\sum_e U_eU_e^T=4P+A,\quad \sum_e V_eV_e^T=4P-A,
\quad A^3=6A.
\]

The A spectral dimensions on W are24,24,30 at +sqrt6,-sqrt6,0.
For a covariance constant on these three sectors, every edge has the same
position and momentum variances x,y. Its energy is160(x+a²)(y+a²).
Cauchy–Schwarz gives xy>=m², with

\[
m=\frac{48\sqrt{10}+120}{320}=\frac{6\sqrt{10}+15}{40}.
\]

Equality with x=y selects

\[
C_0=P+\frac A{\sqrt{10}}+
 \left(\frac4{\sqrt{10}}-1\right)\frac{A^2}{6},\quad
C_0^{-1}=D C_0 D.
\]

The centered real three-sector Gaussian minimum is exactly

\[
160(m+1/20)^2=\frac{649}{10}+\frac{102}{5}\sqrt{10}
\simeq129.4104642674.
\]

The isotropic Gaussian instead has energy168.1. These are variational
energies, not oscillator frequencies or physical particle masses.

Now include a phase and a scale:

\[
\psi_{t,f}\propto
\exp[-q.C_0^{-1}.q/(2t)+i f q.D.q/2].
\]

With b=1/20, Wick's rule gives

\[
E(t,f)/160=m^2+3f^2t^2m^2+
bm(t+t^{-1}+f^2t+4ft)+b^2.
\]

For each t>0, minimize with f=-2b/(3mt+b). The remaining stationary equation is

\[
(t^2-1)(3mt+b)^2-4b^2t^2=0.
\]

Dividing by the positive t²(3mt+b)² yields a strictly increasing function
1-t^-2-4b²/(3mt+b)², ranging from negative infinity to1. Thus exactly one
positive stationary root exists; it exceeds1 and is the global minimum in
this **two-parameter family**. Exact rational endpoint signs isolate it to
(1.000740516890,1.000740516891). The certificate also encloses sqrt10 between
strict rational bounds, rather than trusting a floating-point root.

Numerically t=1.0007405168900636, f=-0.03846284320128045 and
E=128.88739141552713. A separate exploratory ten-parameter Gaussian search
agrees to floating precision but reports optimizer precision loss. It is not
a global-minimum proof and is explicitly stored as such.

## An explicit non-Gaussian improvement

Fix a point and let w have point coordinates9 at that point, -3 at its12
collinear neighbors, and1 at the remaining27; all line coordinates vanish.
Then N^T w=0, sum w=0, ||w||²=216, sum w_i^4=7560, exactly.

For the optimized Gaussian, Y=w.q/sqrt(108t) is a standard normal variable in
the probability density. The two states psi and
Phi=He4(Y)psi/sqrt24 are orthonormal, where He4(Y)=Y^4-6Y²+3.

The exact off-diagonal matrix element is

\[
K=\langle\Phi,H\psi\rangle=
\frac{35\sqrt6}{108}(ft+i)^2\ne0.
\]

The producer records the full algebraic expression for D=<Phi,H Phi>.
Independently, it computes the same matrix elements using seven-node Gaussian
quadrature in three independent normal variables. The integrands have degree
at most12, so this quadrature is degree-exact in exact arithmetic; the two
numerical evaluations agree within2e-10. This is not Monte Carlo evidence.

The lower eigenvalue of the explicit two-state matrix is

\[
\frac{E+D-\sqrt{(D-E)^2+4|K|^2}}2
\simeq\boxed{128.86806573}.
\]

The certificate includes its normalized complex coefficients, so this is an
actual state, not an existence-only descent argument. The selected kernel
direction singles out a point; this state need not be invariant. No spontaneous
symmetry breaking is inferred from a variational trial.

Along q=lambda w, the quartic coefficient of Hpsi/psi is
30240(f+i/t)², which is nonzero. Hence the optimized Gaussian is provably not
an exact eigenstate. The variational success is the explicit non-Gaussian
state; identifying an attained vacuum or spectral gap remains open.

## Consequences and limits

All160 currents cannot annihilate a nonzero state at nonzero central charge:
their Lie closure includes the represented identity center. This also rules
out treating all these operators as anomaly-free gauge constraints without
altering the proposed physical interpretation. The positive H has no zero
eigenvector, but that does not prove its infimum is positive or attained.

This obstruction has a concrete classical comparison. Set q=39a at a selected
point, -a at the other39 points and0 on every line; set p=-a at the selected
point, a/39 at the others and0 on every line. Both vectors lie in W. Every
edge outside the selected four-edge star kills its position factor; every star
edge kills its momentum factor. Thus the classical sum of squared current
symbols is exactly zero. The quantum zero-state obstruction is therefore an
actual incompatibility of simultaneous current constraints, not the absence
of a classical solution. It still does not decide whether normalizable quantum
states can approach zero energy without attaining it.

The important new question is whether a relational energy law can generate
local low-energy excitations and an effective geometry. This model now gives
an actual operator and explicit states on which that question can be tested.
It supplies neither3+1 locality nor chiral matter, a gravitational constraint
algebra, measured couplings, an absolute mass scale or a cosmological constant.
Its dimensionless vacuum energy cannot be substituted into Einstein's equation.

Seven independent regressions verify actual edge blocks, the quantization
bracket and center, covariance positivity, exact root signs, Ritz quadrature,
the integer kernel direction and arbitrary coordinate relabeling. Producer,
certificate and tests all live in the original Theory of Everything checkout.
