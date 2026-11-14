# 2026-11-14 — Five TOE frontiers plus three orthogonal falsifiers

**Status:** finite exact theorem and specified-physics model certification, not an established Theory of Everything. Parent repo research pass: `3c373c924`. Another assistant was concurrently working on Pass 12672 (F8 rank-three code-space lower-bound search); this report deliberately avoids that same search. The prior uncommitted local Pass 12670 action/hexagonal-holonomy/E6 STU files were not edited.

**Code:** `analysis/toe_20261114_five_fronts_plus_three_field_eom_spectral.py`
**Machine-readable evidence:** `data/toe_20261114_five_fronts_plus_three_field_eom_spectral.json`
**Independent tests:** `tests/test_toe_20261114_five_fronts_plus_three_field_eom_spectral.py`

## 1. F8: exact two-copy Bell-spectrum obstruction to naive lower-bound certificates

For the nine F8-regulus MUBs in C^64 the Pauli formulation is

`c8(psi)=64[sum_{j=1}^9 sum_{b=1}^{64} p_{jb}^2 - 9/64] = sum_{P in C} <psi|P|psi>^2`

where `C` is the union of nine disjoint symplectic Lagrangian subspaces, each of 63 nonidentity Hermitian Pauli labels. We independently reconstructed all 567 labels from the GF(8) trace, the 8 chirped Fourier bases and the computational basis. All nine commuting subspaces have real-transposition parity q(u,z)=u·z=0. Their internal pairwise symplectic products vanish, and cross-subgroup intersections are empty.

Set `K=sum_{P in C} P tensor P`, acting on two copies of C^64. The operators `P tensor P` commute even when their single-copy Paulis anticommute. Simultaneous Bell eigenvectors are indexed by (u,z) in F2^12. For one Lagrangian subgroup `L`, its contribution is 63 on Bell labels belonging to L, and -1 otherwise. Therefore **the complete spectrum is exact**:

- full two-copy space, dimension 4096: **567^1, 55^567, (-9)^3528**;
- symmetric two-copy space, dimension 2080: **567^1, 55^567, (-9)^1512**;
- antisymmetric two-copy space, dimension 2016: **(-9)^2016**.

All 567 covered nonzero Bell labels have even swap parity. Our exact combinatorial enumeration confirms this. An independent numerical random-state contract verifies that the covered-Pauli quadratic form equals the nine-basis CZ fourth-moment formula within 1e-10.

**Consequence:** the simple Rayleigh–Ritz symmetric two-copy operator relaxation yields -9, despite the nonnegative pure-product objective and conjectured minimum 2.4985086467. Relaxing to any mixed one-copy density matrix also permits zero (maximally mixed). Thus neither an unconstrained two-copy eigensolver nor a mixed one-copy convex minimization can close the lower bound; the proof must retain nontrivial tensor-product / purity / PPT / higher-moment constraints. Previous PPT-type best exact bound is approximately 2.0818. Pass 12671 has already constructed an exact algebraic **upper** witness at (47-32cos(2pi/9))/9; no matching global lower proof follows here.

This is a precise, generalizable limitation of the simplest convex/spectral relaxation, not a novel global minimum.

## 2. Full higher-dimensional background equations: actual AdS5 x S2 x S2 Einstein–Maxwell solution

Upgrade from the prior homogeneous potential-only calculation. Specify the nine-dimensional theory with **one abelian two-form field strength**:

`S9 = integral d^9x sqrt(-g) [R - (1/4) F_MN F^MN]`.

Use a direct-product `AdS5 x S2 x S2` with both round sphere radii 1, and a closed, co-closed magnetic field strength

`F = f (vol_{S2,a} + vol_{S2,b}),  f^2=14/5`.

Then `F^2=4 f^2=56/5`. The D9 trace-reversed Einstein equations in these conventions are

`R_MN = (1/2) F_MP F_N^P - [F^2/(4(D-2))] g_MN`, D=9.

They give, **component by component**,

- external `R_mu,nu = -(2/5) g_mu,nu` → AdS5 curvature radius squared **10**;
- on EACH S2, `R_ab = g_ab`, consistent with unit round radius;
- nine-dimensional scalar `R9 = 2`, matching trace identity `(D-4)F^2/[4(D-2)] =2`;
- Maxwell `dF=0=d(*F)` on the specified product, using closed/co-closed volume forms.

The reduced d5 Einstein-frame homogeneous potential in `x=e^(u+v), y=e^(u-v)` is

`V(u,v)=(14/5) exp(-20u/3) cosh(4v) - 4 exp(-14u/3) cosh(2v)`.

At u=v=0: `V=-6/5`, gradient zero, Hessian **diag(112/3,144/5)**. `R_mu,nu = V/(d-2) g_mu,nu=-2/5 g_mu,nu` independently matches the higher-dimensional background.

**What is genuinely established:** a specified *nine-dimensional Einstein–Maxwell* on-shell direct-product AdS background with stabilized **homogeneous** radii and consistent Maxwell equations. This is not an E6 exceptional field-theory solution, not a proof of stability of all inhomogeneous/Kaluza–Klein fluctuations (some flux-product vacua can be unstable), and not a 4D vacuum or a solution to observations. A physical flux quantum requires specifying charge normalization, e.g. `integral_{S2}F=4pi f=2pi N/e`; the arbitrary coupling e is not derived.

## 3. A microscopic clock that actually has local, causal, reversible dynamics

A two-state coined quantum cellular automaton with one-site conditional shift S and onsite coin `C=exp(-i theta sigma_x)` has Floquet matrix

`U(k)=diag(exp(ik),exp(-ik)) C`,

exact **dispersion** `cos(omega(k))=cos(theta)cos(k)`, and group-speed limit

`|domega/dk|=|cos(theta)sin(k)|/sqrt(1-cos(theta)^2 cos(k)^2) <= |cos(theta)| <= 1`.

For theta=0.17, a 101-site local unitary walk passes norm preservation, exact reverse evolution, and a strict eleven-tick finite propagation cone. For small momentum and theta the dispersion tends to `omega ~ sqrt(k^2+theta^2)`, a Dirac-type limit. This is a **known quantum-walk phenomenon**, not discovered here: see Bialynicki-Birula 1993 https://arxiv.org/abs/hep-th/9304070 and Raynal 2017 https://doi.org/10.1103/PhysRevA.95.062344 . It is not a local dynamical model of the repository's 120 Clifford ticks nor a derivation of time curvature or the speed of light.

## 4. No four-dimensional continuum from intrinsic uniform W33 edge subdivision

Rather than inserting four external cycles, replace every one of W33 collinearity graph's 240 edges by a path of length L. The graph has `V(L)=40+240(L-1)` vertices, `E(L)=240L` edges. With symmetric normalized adjacency `P=D^-1/2 A D^-1/2`, the **exact spectral second moment** for L>=2 is

`Tr(P^2)/V(L) = (120L-200)/(240L-200) -> 1/2`.

Independently constructing the 40 projective symplectic F3^4 points and all 240 W33 edges, then explicitly subdividing for L=2,3,4, reproduces that rational identity without using the analytic formula.

At a uniformly rooted vertex, the share within fixed distance r of the original 40 high-degree branch vertices is at most `[40+480r]/[40+240(L-1)] ->0`. Thus local neighborhoods converge to the infinite degree-two path. Its symmetric-normalized adjacency moments are odd zero and even `binomial(2k,k)/4^k`. Consequently the fixed-time normalized heat trace limit is **H(t)=exp(-t) I0(t)**, where I0 is the modified Bessel function, and the sequential long-time spectral dimension tends to

`d_s(t)=2t[1-I1(t)/I0(t)] -> 1`,

**not 4**. This is a rigorous graph scaling obstruction for **this specific intrinsic refinement**, not an exclusion of all other graph-to-spacetime mechanisms. No Lorentz signature arises.

## 5. Physical photonic gate resource test: four logical qubits inside one 16-rail photon

The script explicitly constructs complex 16x16 unitaries and verifies exact four-logical-qubit internal GHZ preparation `(|0000>+|1111>)/sqrt(2)`: one Hadamard on logical bit 0 (eight independent 50:50 rail-pair couplers) followed by CNOT(0→1,2,3), each a mode permutation of four disjoint swaps. A controlled-Z on two logical bits is simply four individually programmed pi phases on the affected rails.

These are **ideal passive mode transformations of one photon**, not nonlinear gates between independent photons, and internal Hilbert-space entanglement is not loophole-free spacelike Bell nonlocality. To represent arbitrary n-qubit states in the one-particle sector requires at least **M >= 2^n orthogonal modes**. The elementary logical Hadamard requires at least `2^(n-1)` two-rail couplings; hence this scheme has exponential optical resources and **does not establish scalable BQP**.

A deliberately specified optical noise control uses four depth layers, photon transmission eta=0.98 per layer and independent Gaussian random phase noise sigma=0.1 on the two GHZ rails: conditional visibility `<X tensor4>=exp(-sigma^2)`. Loss-only survival is `eta^4`. For +-1 parity samples, Hoeffding's inequality requires **ceil[2 log(2/0.05) / 0.05^2]** accepted events for absolute error 0.05 at 95% confidence, before adjusting for loss; the code records the resulting raw-shot estimate. These are requirements of this specified idealized test, **not measured engineering performance**.

Related prior art on single-photon time-bin encoding: https://www.nature.com/articles/s41467-019-08951-2 . The repository already warned of one-photon internal-factor versus remote nonlocality confusion in `analysis/PASS20261109_W33_Q8_ADVANCED_FALSIFIERS.md`; this experiment respects that.

## Three outside-the-box tests

### 6. Gauge flux sign is invisible in unoriented ring spectroscopy

On a three-site U(1) flux ring, energies are `E_k(Phi)=2cos[(2pi k+Phi)/3]`. The **unordered energy spectrum is invariant** under `Phi -> -Phi`, although Wilson loop phase conjugates and oriented persistent current `-dE_k/dPhi` changes sign under the corresponding reversal. Tested at Phi=2pi/3. **A spectral match cannot, by itself, establish a chirality selector.** Oriented interference/current is an additional observable.

### 7. Topological flux grading prevents silently identifying the new background with flat T4

Kunneth cohomology: `b_k(T4)=[1,4,6,4,1]`, while `b_k(S2xS2)=[1,0,2,0,1]`. The torus has four independent third-cohomology flux classes; the sphere product has **zero**. Sphere product has two independent second-cohomology classes, compared with the torus's six. Their Euler characteristics are 0 and 4, respectively. No topology-preserving deformation identifies the earlier E6 T4 three-form scenario with this Maxwell S2xS2 two-form compactification. Topology-changing duality with further structure is not ruled out.

### 8. Speed of light remains underdetermined by integer tick counting

The identical dimensionless local quantum automaton can be embedded with spatial lattice spacing a and tick duration dt, yielding different **physical** maximum hop speeds `a/dt` under changes in external units. Four rational alternatives are exactly enumerated. Therefore a count of exchanges cannot fix a dimensionful SI value for c without an independent length/time scale or other matching principle. This is a dimensional-analysis obstruction, not a theorem against emergent kinematics.

## Evidence labels, crosschecks and boundaries

- **Exact combinatorial:** F8 Pauli/Bell 567/55/-9 eigenvalue multiplicities; GF8 group structure; graph subdivision second moments; Kunneth Betti numbers.
- **Exact classical field equations:** the specified Einstein-Maxwell `AdS5 x S2 x S2` background. **NOT** the E6 ExFT equations.
- **Known model mathematics:** local coined QCA dispersion and light cone; internal 16-rail single-photon unitaries; oriented ring flux spectrum.
- **Numerical controls:** floating-point independent Pauli-vs-CZ quartic check, finite unitary dynamics checks, Bessel numerical asymptotics, idealized photonic shot budget.
- **Unresolved:** global F8 lower bound; E6 true vacuum and full KK spectrum; native 3+1D continuum with physical Lorentzian Einstein dynamics; scalable efficient photonic universal quantum computing; a derived physical value for c.

External context: Bialynicki-Birula (1993) https://arxiv.org/abs/hep-th/9304070 ; Raynal (2017) https://doi.org/10.1103/PhysRevA.95.062344 ; Freund-Rubin compactification stability subtleties https://inspirehep.net/literature/556247 ; single-photon time-bin multi-mode experiments https://www.nature.com/articles/s41467-019-08951-2 ; linear-optical deterministic universal gates challenge https://www.nature.com/articles/s42005-024-01610-z .

**Bottom line:** this pass constructs and falsifies specific models instead of stretching finite incidence identities into unproved fundamental physics. The on-shell nine-dimensional flux background and exact Bell-spectrum no-go are the leading independent mathematical results.
