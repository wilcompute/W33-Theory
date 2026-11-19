# Five fundamental TOE problems: exact closure gates, negative theorems, and two global observables

**Research date: 2026-11-19. Status: seven executable gates, NOT a solved Theory of Everything.** This report documents actual independent mathematical tests and finite calculations addressing the five requested research directions: intrinsic causal Spin/Spin-c topology, uniqueness of a microscopic gauge action, selection of a quantum vacuum, gravitational history dynamics and dimensional selection, and the physical matter-charge spectrum. Two additional tests link gauge-group centers to physical observables.

The work uses scientific literature, existing repository calculations and the connected Windows workstation. The calculations do not derive the Standard Model from first principles, physical 3+1 Lorentzian Einstein gravity, a Born rule, or fundamental observed constants. Those open physics requirements cannot honestly be declared solved.

## What was already in the repository

We inspected recent commits through 21e8ff606, the parallel ff5090ff5, and earlier causal/exchange/spectral work. In particular:
- analysis/toe_20261105_regge_s4_nonlinear_hessian.py ALREADY derived a nontrivial curved Euclidean 4D Regge action on a simplicial S4, a cosmological-term stationary configuration and a full 15x15 Hessian.
- analysis/toe_20261104_regge_4simplex_1to5_action.py ALREADY computed flat vertex-translation modes and curvature-induced pseudo-constraints in a Euclidean 4-simplex refinement.
- The latest causal work ALREADY tested 2D/4D overlap Dirac indices, Spin-c quotients, global holonomy and pure-state ambiguity.
- The E8 work ALREADY examined toric singlet F/D conditions, SU5 thresholds, and related model-building constraints.
Thus the present pass does NOT relabel established Regge, overlap, Spin-c or lattice facts as new physics. Its contribution is a unified, executable collection of more severe **uniqueness and global-completion counterexamples**, and a complete symbolic anomaly/charge lattice.

**Concurrent parallel-commit audit.** While these tests ran, master advanced to commit 4ea5ae0addde3a945500e0b65ff66cb8c836bc52, which we reviewed through its complete commit diff. That parallel research implements an E8 singlet messenger EFT, SU5 orbifold-boundary model, CP2 twisted Spin^c family index, causal lightcone-link thinning, and oscillator energy minimization, among other checks. We do NOT claim to have originated these earlier or concurrently executed approaches. The distinct present contributions are: the **bounded-poset order-complex cone obstruction**, the exact **SU2 fundamental-versus-adjoint action and center identity**, the KMS **noise-versus-response** comparison, the **exact closed-form positive-edge partition function** benchmarked against the preexisting 4D Regge code, the **two-parameter SM Z6/anomaly/Yukawa charge family**, and the **actual Haar-averaged Wilson expectation split**. These results do not certify either the E8 construction or an orbifold GUT as physical.

## I. The ordinary order complex of a bounded causal interval is contractible

The order complex K(P) of a finite poset has a vertex for each event and a simplex for each strictly increasing chain. If there is a least element e0, every simplex S is contained in the simplex S union {e0}; K(P) is a cone and has trivial reduced homology. The same holds with a greatest element.

Explicit independent GF2 boundary-matrix checks give:

| Poset | Betti 0 | Betti 1 |
|---|---:|---:|
| Four-event unbounded crown K(2,2) | 1 | 1 |
| Same causal diamond with minimum and maximum | 1 | 0 |
| Crown with just one canonical first event | 1 | 0 |

The bounded example also has zero Betti numbers in all higher degrees. This is an exact standard topological theorem, not our new discovery. It is a precise obstruction for a naive proposal that reads nontrivial torus spin holonomy from H1 of the ENTIRE bounded causal-interval order complex. It is NOT a no-go for general causal posets, spatially reconstructed neighborhoods, thickened antichains or global topology.

Reference: A new spectral sequence for homology of posets, https://doi.org/10.1016/j.topol.2016.12.001 .

## II. Local gauge symmetry and the correct weak-field F-squared term do not determine a unique action

For U in SU2 parametrized by U=cos(theta/2) I + i sin(theta/2) n.sigma, compare the fundamental action and a rescaled adjoint action:

    S_F=1-Re Tr_f(U)/2=1-cos(theta/2),
    S_A=(3/8)[1-Re Tr_adj(U)/3]=(1-cos theta)/4.

Both are positive local gauge-invariant class functions and both start with the same quadratic theta^2/8. The SU2 character identity Tr_adj(U)=(Tr_f(U))^2-1 yields EXACTLY

    S_A = S_F - S_F^2/2.

Consequently they differ at O(theta^4) and have different Euler-Lagrange forces at finite angles. At U=-I, which is invisible to the adjoint representation,

    S_F(-I)=2, S_A(-I)=0.

The interpolation S_lambda=S_F-lambda*S_F^2/2 has the same weak-field quadratic limit for any lambda between 0 and 1, yet has different finite-angle/global dynamics. This explicitly falsifies a claim that covariance, locality and the leading continuum Yang-Mills form uniquely determine the microscopic action.

Prior art: Scholarpedia Lattice Gauge Theories, https://www.scholarpedia.org/article/Lattice_gauge_theories ; mixed fundamental/adjoint SU2 studies, https://cds.cern.ch/record/1497911/files/Lattice%202012_252.pdf .

## III. The same retarded propagation coexists with different positive KMS noise correlations

For one oscillator H=(p^2+omega^2 q^2)/2 with [q,p]=i, the RETARDED response

    G_R(t)=i theta(t)<[q(t),q(0)]>
          =theta(t) sin(omega t)/omega

is identical for every thermal inverse temperature beta. But the SYMMETRIC fluctuations depend on state:

    F_beta(t)=< {q(t),q(0)} >/2
             =[n_beta+1/2] cos(omega t)/omega,
    n_beta=1/[exp(beta omega)-1].

We constructed full complex greater/lesser two-point functions, checked exact KMS W_greater(t-i beta)=W_lesser(t), verified six-time Wightman correlation matrix positivity, and verified that the commutator is state-independent. At omega=1.7 and t=0.41:

| beta | Symmetric noise | Retarded response |
|---:|---:|---|
| 0.4 | 0.688661270 | Same for all three |
| 2.0 | 0.241093449 | Same for all three |
| 10.0 | 0.225521017 | Same for all three |

These are different positive stationary states, all KMS at their own beta. Thus an event-exchange retarded kernel plus positivity does not select a unique vacuum/noise process or Born probabilities. A physical state/temperature, spectrum condition, time generator or deeper selection law is required. This is well-established FDT/KMS physics.

Reference: https://doi.org/10.1103/PhysRevResearch.6.023113 .

## IV. The real difficulty of gravity is the measure over histories, not merely an action on a preselected 4-manifold

We deliberately import and independently check the REAL curved 4D Euclidean Regge action that this repository already implemented. On the boundary of the five-simplex, with 15 edges, 20 triangle hinges and six four-simplices, for all unit edge lengths:

    S_Regge=20 sqrt(3)/4 [2 pi-3 arccos(1/4)]
           =20.16832083138985.

Its derivative with respect to one edge agrees independently with the Schlaefli identity:

    dS/dl = 2[2 pi-3 arccos(1/4)]/sqrt(3).

This is a genuine finite GR-action control, but the 4D manifold complex, Euclidean signature and edge-length metric are inputs; no Lorentzian 4D spacetime has emerged from the causal order.

Next, consider a family of explicitly labeled three-layer causal posets with stratum cardinalities N/4, N/2, N/4. Each adjacent lower-middle and middle-upper ordered pair is independently present or absent, and transitive closure defines the poset. There are

    M=N^2/4 independent binary cover links,
    number of distinct labeled posets in this family=2^M.

| N | Independent bits | Possible labeled histories | Mean links, equal weights |
|---:|---:|---:|---:|
| 8 | 16 | 2^16 | 8 |
| 16 | 64 | 2^64 | 32 |
| 32 | 256 | 2^256 | 128 |
| 64 | 1024 | 2^1024 | 512 |

All 65,536 possible N=8 patterns were enumerated; the exact histogram is binomial. With a positive simple edge-penalty action beta*L the exact partition function and expected link count are

    Z_N(beta)=[1+exp(-beta)]^(N^2/4),
    E[L]=[N^2/4]/[1+exp(beta)].

Any fixed finite beta gives O(N^2) links. To keep E[L]=O(N), beta must grow approximately like ln N. This is a size-dependent tuning, NOT a derived manifoldlike phase or 4D selector.

**Strong limitation:** this theorem concerns a deliberately simple POSITIVE edge-count weight. It is NOT a no-go on oscillatory quantum gravitational actions, and published work has demonstrated path-integral suppression of Kleitman-Rothschild orders under better dynamics. A true TOE would need to solve a much stronger quantum-measure problem and recover Lorentzian Einstein constraints and propagating degrees of freedom.

Prior works: Surya review https://doi.org/10.1007/s41114-019-0023-1 ; suppression of badly behaved causal sets https://arxiv.org/abs/2209.00327 ; Regge gravity overview https://pmc.ncbi.nlm.nih.gov/articles/PMC5253799/ .

## V. Fully symbolic hypercharge result: the global Z6 quotient plus anomalies plus Yukawas do not uniquely predict charges with a right-handed neutrino

Assume the familiar ONE-FAMILY non-Abelian left-Weyl representations as inputs:

    Q_L=(3,2), u_c=(bar3,1), d_c=(bar3,1),
    L_L=(1,2), e_c=(1,1), nu_c=(1,1).

Normalize integer Abelian hypercharge as y=6Y. For the chosen faithful global SM gauge group [SU3 x SU2 x U1]/Z6, the center representation must obey

    2t+3s+y = 0 modulo 6,

where t is the color triality in {0,+1,-1} and s is weak doublet parity in {0,1}.

Start from unknown charges (a,b,d,l,e,n) and impose all perturbative SU3^2-U1, SU2^2-U1, gravity^2-U1, and U1^3 anomalies. The linear equations give

    d=-2a-b, l=-3a, n=6a-e.

Symbolic factorization of the full remaining cubic anomaly gives EXACTLY

    A_U1^3=18*a*(2a-b-e)*(4a+b-e).

For a nonzero a there are two branches. Requiring four ordinary quark/lepton/neutrino Dirac Yukawas to a SINGLE weak Higgs doublet with integer hypercharge x selects the branch

    Q_L:a, u_c:-a-x, d_c:-a+x,
    L_L:-3a, e_c:3a+x, nu_c:3a-x,
    Higgs:x.

All perturbative anomalies and all four Yukawa charge sums vanish identically. The Witten SU2 obstruction is absent in this assumed family, since there are four left weak doublets counting color. The Z6 quotient condition restricts the integer lattice to

    a=1+6m, x=3+6n, with m,n integers,

but leaves INFINITELY MANY allowed families. For example:

| a | x | (Q,u,d,L,e,nu) integer y charges | upper lepton-doublet electric charge |
|---:|---:|---|---:|
| 1 | 3 | (1,-4,2,-3,6,0) | 0 |
| 1 | 9 | (1,-10,8,-3,12,-6) | +1/3 |

The unbroken electric generator uses Q_em=T3+y/(2x) because the lower Higgs component is electrically neutral. The second charge family is inconsistent with the observed neutral neutrino, despite satisfying all the tested local anomalies, quotient rules and Yukawa invariances.

Requiring the physical neutrino to be electrically neutral, or requiring nu_c to have a neutral Majorana mass, imposes x=3a; the known Standard Model relative hypercharges then follow from the assumed representations. If the nu_c field is omitted, the remaining gravitational-U1 anomaly equals x-3a and similarly fixes that ratio. Overall normalization/gauge coupling and the full matter content still require physical input.

This is an exact, independently executable demonstration of the known B-L-related freedom in anomaly-free U1 assignments, NOT a derivation of the Standard Model multiplets or number of generations.

Sources: https://doi.org/10.1103/PhysRevD.83.015009 ; https://lss.fnal.gov/archive/2008/pub/fermilab-pub-08-676-t.pdf ; global forms https://scoap3-prod-backend.s3.cern.ch/media/files/87510/10.1007/JHEP08%282024%29004_a.pdf .

## VI. Extra global center-spin-gauge compatibility gate

A pure adjoint SU2 plaquette action does not see the -I center, but a fundamental fermion doublet transforms by -1. A combined quotient of SU3, SU2 and U1 can cancel center actions in a full Standard Model multiplet. We independently check the central congruence for all assumed fermions and the Higgs. The Lie algebra alone does not specify these global representation rules, line operators or topological sectors.

## VII. Extra nonperturbative one-plaquette Haar observable test

Parametrize U=cos(phi) I+i sin(phi) n.sigma, phi in [0,pi]. The normalized SU2 Haar conjugacy-class measure is (2/pi)sin^2(phi) d phi. Using Boltzmann weight exp[-beta*S], calculate the normalized fundamental Wilson-loop trace W=Tr_f(U)/2=cos(phi).

For the FUNDAMENTAL action,

    <W>_F=[I1(beta)-I3(beta)]/[2(I0(beta)-I2(beta))]

where I_n are modified Bessel functions. For the CENTER-BLIND adjoint action, phi->pi-phi reverses W while leaving both measure and action invariant. Therefore

    <W>_A=0

EXACTLY. At beta=2 numerical quadrature and independent Bessel functions give

    <W>_F=0.4331274267223,
    <W>_A=0.

This is an actual finite statistical observable distinction, not just a difference between action formulae. If the fundamental global gauge group is SO3 rather than SU2, the fundamental Wilson line is not a genuine line operator; this is a SU2-lift single-plaquette test. It is NOT a full 4D Yang-Mills confinement or continuum calculation.

## Integrated interpretation and remaining fundamental work

These seven gates jointly identify a common structural gap:
- Order does not by itself provide nontrivial global spin topology on bounded intervals.
- A local gauge Lie algebra and correct F^2 matching do not determine global gauge form, matter representation or unique microscopic action.
- A causal retarded Green function is only response, not fluctuation statistics or a unique quantum vacuum.
- A 4D Regge action is insufficient to select manifoldlike Lorentzian histories against a gigantic nonmanifoldlike combinatorial sample space.
- Anomaly cancellation, a global Z6 quotient and gauge-invariant Yukawa couplings still do not determine exact matter charges with nu_c unless additional physical conditions are supplied.
- Fundamental doublets distinguish gauge-center physics that adjoint-only actions ignore.

A plausible candidate fundamental object would need order, recoverable topology, compatible spin/gauge transport, an action *selected by physical principles*, a quantum state-selection law, and a quantum gravitational measure. None of these tools currently derives all components from one unique axiom. No TOE has been solved.

## Reproduction and code

From the repo on the connected Windows machine:

    python analysis/toe_20261119_five_deep_closure_gates_v5.py
    python -m pytest -q tests/test_toe_20261119_five_deep_closure_gates_v5.py

New program: analysis/toe_20261119_five_deep_closure_gates_v5.py
New tests: tests/test_toe_20261119_five_deep_closure_gates_v5.py
Machine-readable certificate: data/toe_20261119_five_full_physics_gates_global_obstructions.json
This report: analysis/2026-11-19_five_deep_physics_gates_global_uniqueness_report.md

**36 new focused tests passed.** The full independently run related regression, also including the concurrently landed E8 messenger/orbifold causal-state suite, passed **270 tests** in 45.91 s on the connected Windows machine. The producer was independently rerun and reproduced its machine-readable result certificate. The local pre-commit hook may be absent, so use explicit pytest and git diff --cached --check rather than implying that hook checks executed.

## Top five independent ambitious next experiments

1. **Recover actual global spin topology from unembedded causal data:** test thickened spatial antichains, nerve reconstructions, functorial spin lifts and a Lorentzian chiral operator; demand the 4D flux index and full gauge-covariant Ward identities without preselecting a torus.
2. **Find a unique microscopic physical action despite the center counterexample:** require positivity, anomaly-free representation content, global Wilson sectors, causal locality and RG stability to eliminate the fundamental-adjoint action ambiguity and derive its gravitational counterpart.
3. **Predict vacuum fluctuations from causal dynamics:** go beyond a response Green function to a positive and physically selected noise kernel, prove a suitable spectrum/Hadamard condition, and recover Born statistics and interacting unitary scattering.
4. **Select 3+1 dimensions dynamically:** replace toy positive edge penalties with a controlled oscillatory unlabeled causal-history measure, test explicit KR suppression and a manifoldlike 4D phase, and derive Lorentzian Einstein constraints/gravitons against the repo's existing Regge controls.
5. **Derive the full matter spectrum, not just anomaly-admissible charge lattices:** obtain SU3xSU2xU1/Z6, three chiral generations, Higgs representation, charge neutrality and Yukawas from a common microscopic vacuum and topology; reject models needing free hypercharge parameters or exotic unobserved charged neutrinos.

The open-ended five objectives above are unsolved; the present pass has **actually executed** concrete mathematical attacks on them, not invented a final physical solution.
