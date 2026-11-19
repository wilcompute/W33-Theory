# Eight connected physics stress tests: a causal spectral-operator TOE candidate

**2026-11-19 · scientific status: conditional no-go/constructive finite models; NOT a Theory of Everything.** This packet follows 7cda851ce (causal chain massive propagation, constant-electric-field gauge tail) and audits recent GitHub work, including earlier Wilson-Dirac and heat-kernel/spectral-action efforts. The aim is to test a **single microscopic principle** that could encompass causality, spin, gauge connection, gravity and quantum state choice. W33 is not inserted as a fundamental axiom.

## Principle under investigation

A causal relation C specifies who may influence whom. An event count specifies volume only if its physical density rule is known. A Dirac-type kinetic operator also needs Clifford/spin structure and a gauge/internal representation. The quantum theory additionally needs a positive two-point state, and global topology introduces noncontractible holonomy sectors.

The central ambition is a causally defined, spin-gauge-covariant Dirac-type operator D and a non-ad-hoc quantum action. On a *given* smooth geometry, the established Lichnerowicz/Weitzenbock identity relates D^2, connection Laplacian, gravitational scalar curvature and spin-gauge field strength. Chamseddine-Connes spectral-action methods use related heat-kernel expansions to generate Einstein/Yang-Mills actions; this is substantial established prior art (https://arxiv.org/abs/hep-th/9606001). Here we test precisely which required ingredients are **not** determined by the bare causal order.

### Gate 1 — Chiral fermions and global spin structures in two dimensions

Use an even 8x8 periodic square lattice and the free naive 2D Dirac symbol D_n=i sigma_x sin(k_x)+i sigma_y sin(k_y), gamma5=sigma_z. The four Brillouin-corner momenta (0,0), (0,pi), (pi,0), (pi,pi) all have zero D_n, yielding 8 zero spinor components. Their orientation/chirality Jacobian signs are (+,-,-,+) and sum to zero. A Wilson mass W=(1-cos k_x)+(1-cos k_y) removes three cones, leaving 2 zero components at k=(0,0), but the anticommutator {gamma5,D_W} is no longer zero.

On the **same locally flat lattice**, the four global Z2 choices for periodic/antiperiodic boundary conditions alter the finite-volume spectrum; any antiperiodic direction removes the exact zero. This is a torus spin-structure effect, not local curvature. The Nielsen-Ninomiya species-doubling restriction and Wilson chiral tradeoff are established prior art, not an original proof: https://doi.org/10.1103/PhysRevD.105.114511 ; https://journals.aps.org/prd/abstract/10.1103/qd1t-wzy1 .

**Boundary:** a Euclidean square lattice is not an unembedded Lorentzian causal set. This experiment does not establish a chiral generation or forbid sophisticated overlap/Ginsparg-Wilson/domain-wall regulators.

### Gate 2 — Non-Abelian SU(2) curvature from noncommuting constant potentials

Let U_x=exp(i a sigma_x/2), U_y=exp(i b sigma_y/2), for a=.23 and b=.31. A closed elementary Wilson loop is

    P = U_x U_y U_x^-1 U_y^-1.

Its normalized Wilson action is S=1-(1/2) Re Tr(P)=**0.00062761447**, nonzero even though the connection matrices are spatially constant: their matrix commutator supplies curvature. When both connections lie in the same commuting Cartan direction, P=I. Four independent SU2 site-frame gauge transformations were applied and verified to conjugate P at the basepoint, preserving the traced action. The small-link coefficient is S/(a b)^2 -> 1/8 in this normalization.

**Boundary:** SU2, link transport and the Wilson action were supplied. The calculation does not derive the gauge group, Yang-Mills action, running coupling or Maxwell/Yang-Mills equations from C.

### Gate 3 — One spin-gauge Dirac operator carries a compulsory curvature interaction

Take gamma_x=sigma_x and gamma_y=sigma_y on spin indices and constant SU2 gauge matrices on color. Define nabla_mu=i A_mu (the sign conventions for F are fixed by the identity) and

    Dslash = gamma_x tensor nabla_x + gamma_y tensor nabla_y.

Exact multiplication gives

    Dslash^2 = 1 tensor(nabla_x^2+nabla_y^2)
             + gamma_x gamma_y tensor [nabla_x,nabla_y]
             = 1 tensor Laplacian + gamma5 tensor F,

where **F=-i[A_x,A_y]** under this specified sign convention. The numerical 4x4 identity holds to machine precision. Omitting the Pauli curvature piece leaves a Frobenius error **0.6674** for the chosen noncommuting fields. A constant color-frame SU2 rotation preserves the operator by conjugation.

This is the most promising cross-sector mathematical mechanism: a *single* kinetic operator determines matter's coupling to the curvature of its own connection. The smooth curved-space analogue adds a gravitational R/4 spin term, but **we have NOT derived it on a causal set**, nor have we proved a Lorentzian positive-norm or chiral regulator. See the original spectral-action literature (https://arxiv.org/abs/hep-th/9606001) and recent nonminimal heat-kernel analysis https://doi.org/10.1103/1njq-346g .

### Gate 4 — A causal commutator does not uniquely select the quantum vacuum

Construct a small acyclic causal relation matrix C on six events and its finite retarded massive kernel K=(1/2)C(I+alpha C)^(-1). Set Delta=K-K^T and Hermitian H=iDelta. The established Sorkin-Johnston Gaussian prescription takes its **positive spectral part**

    W_SJ=positive_part(i Delta).

We verify W_SJ is positive semidefinite and W_SJ-W_SJ^T=iDelta, and that it transforms correctly under any event relabeling. The naive half-commutator H/2 has negative eigenvalues and is not a valid positive two-point state. Crucially, W_SJ + epsilon I (epsilon=.15) is ALSO positive and has the same commutator. Thus the *retarded causal exchange kernel plus canonical commutator alone* admits more than one positive state.

Sorkin-Johnston state selection is prior art, including recent accounts of global vacuum principles (https://arxiv.org/abs/2412.07832) and causal-set in-in amplitudes (https://doi.org/10.1103/PhysRevD.109.106014). **This does not derive the Born rule, interacting state uniqueness or a Hadamard continuum vacuum.**

### Gate 5 — Same causal order, different gravitational curvature and volume

Consider two continuum Lorentzian metrics on the same 1+1 region: g_flat=(-dt^2+dx^2), and g_conformal=exp(2 epsilon t^2)g_flat, with epsilon=.12 and coordinate diamond height tau=2. Positive conformal rescalings leave all causal relations and light cones *identical*. But the weighted interval volume (computed independently by numerical quadrature and Monte Carlo) is **1.35177251 times** the flat interval volume. The vertical proper time also increases, and Ricci scalar at t=1 is R=4 epsilon exp(-2 epsilon) >0.

Therefore **order alone cannot yield the full metric or Einstein dynamics**; a physically normalized volume density and dynamics are essential. Prior causal-set literature emphasizes 'order plus number' in reconstructing continuum geometry, but a discrete model must supply the fundamental density/measure, not just cite the slogan: https://doi.org/10.1007/s41114-019-0023-1 ; https://doi.org/10.1007/s10714-024-03281-1 .

No dynamical 4D selection, gravitational wave, Einstein equation or quantum measure follows from this 2D kinematic example.

### Gate 6 — Local flat gauge curvature does not fix global quantum propagation

On an 8x8 spatial torus, choose a constant flat U1 link U_x=exp(i theta/8), U_y=1. Every elementary plaquette is I, so local field strength vanishes, but the noncontractible Wilson winding is exp(i theta). The covariant lattice Laplacian has eigenvalues

    lambda_nm(theta)=4-2 cos[(2pi n+theta)/8]-2 cos(2pi m/8).

For theta=0 and theta=pi all local plaquettes remain flat, but the long-time heat traces Tr exp(-8 Laplacian) differ by **0.43452213**. The periodic spectrum contains a zero mode and the pi-holonomy spectrum does not. This is a finite-lattice Aharonov-Bohm/global spectral effect, not new physics. It shows that **local plaquette curvature alone does not determine even the free charged-particle spectrum**.

### Gate 7 — Four-dimensional chirality and anomaly checks cannot be skipped

The naive Dirac symbol in *four* Euclidean momentum dimensions has **16** zero cones (2^4), each a 4-component Dirac mode; the alternating corner orientations sum to zero. A conventional Wilson mass retains one low-momentum cone but sacrifices the exact naive lattice chiral symmetry.

For comparison, we supplied the **known** Standard Model left-handed Weyl representation of one family:
Q_L=(3,2,1/6), u^c=(bar3,1,-2/3), d^c=(bar3,1,1/3), L_L=(1,2,-1/2), e^c=(1,1,1), and optionally neutral nu^c=(1,1,0). Exact rational arithmetic verifies U1^3, gravitational-U1, SU2^2-U1, SU3^2-U1 and SU3^3 anomaly cancellation, with four SU2 left doublets (even, avoiding Witten's Z2 anomaly).

This succeeds **only because the correct representations and hypercharges were inserted**. No causal graph, Clifford operator or spectral action in this packet predicts those numbers. Vectorlike and other anomaly-free alternatives exist. See the 2026 chiral lattice research https://doi.org/10.1007/JHEP07(2026)271 .

### Gate 8 — An unexpected common carrier: spin and gauge winding can compensate

A spatial torus's antiperiodic spinor boundary condition shifts fermionic momentum k_x by pi/L. A charge-one fermion on the periodic spin structure with a flat U1 Wilson winding theta=pi receives **exactly the same spectral shift**. With *both* minus signs present, the twists cancel and periodic zero modes reappear:

| Spin in x | Gauge winding | Naive zero spinor components |
|---|---|---:|
| Periodic | theta=0 | 8 |
| Periodic | theta=pi | 0 |
| Antiperiodic | theta=0 | 0 |
| Antiperiodic | theta=pi | 8 |

This is an exact toy-model relation between **two global holonomy representations**. It is a concrete motivation to investigate a combined spin-gauge groupoid or Spin^c-type transport system on causal events. It is NOT a general identification of spin structure with electromagnetic gauge: neutral particles and differing charges distinguish the sectors, and topological obstructions exist on more general manifolds.

## The conceptual synthesis and explicit required extra data

The experiments support a **conditional information architecture**, not a uniqueness theorem:

    causal order -> which influences are permitted
    interval counts + density -> approximate volume/time
    Clifford module + spin lift -> fermion kinematics
    internal connection and ALL loop holonomies -> local & global gauge data
    Dirac-type operator -> spin/curvature coupling
    positive two-point state/measure -> quantum expectations
    one dynamical action -> field equations and gravitational backreaction.

One Dirac-square identity is a promising **consistency filter** because it forces related curvature terms from one operator. But a true TOE must derive rather than hand-choose: dimension 3+1, the correct spin and gauge group, family/chirality, mass spectrum, quantum vacuum and state probabilities, an intrinsic gravitational measure, and a nonperturbative unitary continuum.

The strongest falsifiers are the **incompleteness of local data** (spin structures and winding) and **nonuniqueness of a positive quantum state from retarded propagation**. These reject any simplistic claim that causal links and their local Wilson loops uniquely define observable physics.

## Reproduction, provenance, tests

    python analysis/toe_20261119_spectral_exchange_seven_gates.py
    python -m unittest discover -s tests -p test_toe_20261119_spectral_exchange_seven_gates.py -v

Machine-readable data: data/toe_20261119_spectral_exchange_seven_gates.json
Focused new checks: **28** pass with seeded numerics and exact rational anomaly arithmetic. All 8 named gates are included in the data JSON. The script filename retains 'seven' from its first stage; an eighth cross-sector spin-gauge gate was added subsequently.

The identity and topology results are standard physics and math; the new-to-repository contribution is **one explicitly integrated and tested stress suite** and its prioritization of missing global/quantum information.

## Top five orthogonal 'home run' attempts from this result

1. **Microscopic causal spin-gauge groupoid:** specify a spin/Spin^c lift, all noncontractible parallel transports, internal representation and chiral anomaly constraints *intrinsically on unembedded causal sets*. Derive, do not assign, the group and representations.
2. **One operator yields both sectors:** construct a genuinely Lorentzian, causal, dynamically determined Dirac operator whose square recovers the gauge Pauli term and gravitational R/4 term with correct normalization and spin-statistics, then compute chiral spectrum/anomaly coefficients.
3. **Quantum vacuum without an extra axiom:** search for a selection principle for positive states and a causal unitary interacting S-matrix that distinguishes W_SJ from W_SJ+epsilon I, with Born probabilities and Hadamard/optical-theorem checks.
4. **Dimension and gravity attractor:** define a covariant quantum measure on unlabeled histories with no built-in d, penalize nonmanifoldlike degeneracy and recover 4D Einstein dynamics and propagating gravitons; compare to existing nonmanifold suppression results before claims.
5. **Non-Abelian gauge dynamics and predictions:** derive a Yang-Mills action and matter currents from the same microscopic action and show correct asymptotic freedom, one anomaly-free chiral family and the charged propagator's external-field tail, without independent per-sector mass or coupling fits.

**Scientific verdict:** Eight executed gates, no solved TOE. A mathematically unified transport-plus-operator framework is plausible, but the missing global sector, quantum-state prescription and metric dynamics are separate unfulfilled requirements. Those are the new precise targets.
