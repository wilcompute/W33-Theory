# Pass11663: an odd-sector normal map and a conditional Witting mass phase

Reservation: `48ef215c6`. Producer: `w33_pass11663_odd_weil_normal_map.py`.
Certificate: `data/w33_pass11663_odd_weil_normal_map.json`.

The useful connection is a map, rather than a new identification of groups.
The Heisenberg-invariant cubic vanishes on the entire odd Weil sector. Its
**normal derivative**, however, is a nonzero skew five-by-five matrix. Its
Pfaffians recover the classical Maschke-to-Burkhardt parametrization, and its
rank drops precisely on the forty Witting rays. In a declared Dirac model this
leaves three zero singular masses. An independent finite-shell fermion
calculation opposes that rank drop; an explicit scalar alignment can overcome
it, with closed analytic phase boundaries.

This does not derive Standard Model chirality, three observed generations,
physical mass scales, spacetime, or a unique microscopic action.

## Ownership and intake

The decomposition of the two-qutrit Weil representation into even five and odd
four dimensions is already owned by
`analysis/w33_pass2448_2453_where_the_phase_lives.md`. The physical E8 parity lift
and its D8-fixed 120/128 decomposition are already in
`analysis/PASS20260918_physical_e8_holonomy_insert.tex` and
`analysis/w33_physical_holonomy_e8_chevalley_lift.py`.
Pass11651 owns the five-dimensional Heisenberg-invariant cubic space and its
dual-even representation; Pass11657 owns its point/eigenplane versus
line/stabilizer-state dictionary; Pass11659 owns the Burkhardt node calculation.
Their reports and certificates were inspected before this calculation.

The forty-points paper already gives the Witting/E8 six-to-one construction.
Its epilogue separates the available finite geometry from the unsolved physical
dynamics, chirality, masses, and cosmological constant. This packet preserves
that distinction and does not add its supplied EFT to the paper.

The quartic parametrization below is **classical**, explicitly printed in
[Bruin–Filatov, section3.1](https://arxiv.org/html/2207.04393v1#S3.SS1).
That source also identifies the degree-six map and its forty-point base locus.
The contribution here is its explicit normal-derivative realization in the
committed qutrit tensor, the normalized mass operator, and the conditional
quantum phase calculation. Searches for the normal-map formula, rank-two
Witting mass claim, Pfaffian connection, and exact result combinations were
performed across the result index, Python, JSON, Markdown, TeX, and public HTML.
No uniqueness or first-in-literature claim is made for this EFT interpretation.

## The named normal derivative

Label the nine amplitudes by F3 squared. Choose directions
`(0,1),(1,0),(1,1),(1,2)` and write

    psi(0)=b0, psi(+di)=bi+fi, psi(-di)=bi-fi.

The even basis has metric G=diag(1,2,2,2,2); the odd basis has metric 2I.
Take c0=sum(psi_a^3)/6 and, for each direction, cd=sum of the three parallel
line products. At b=0, every cubic vanishes identically. Differentiation gives,
with (a,b,c,d) denoting the four odd coordinates,

    K(f) = [ 0     a²     b²     c²     d²  ]
           [-a²    0     2cd    2bd    2bc  ]
           [-b²  -2cd     0    -2ad    2ac  ]
           [-c²  -2bd    2ad     0     -2ab ]
           [-d²  -2bc   -2ac    2ab      0  ].

In orthonormal bases the actual Pass11651 cubic tensor obeys

    u(O_normalized f + t E_normalized b)
      = t M(f)b + t³ u(E_normalized b),
    M(f) = G^(-1/2) K(f) G^(-1/2).

Thus the odd sector is invisible to the cubic restriction but visible to its
response to even perturbations. Twelve independent random mixed tensors test
this identity directly against Pass11651's stored construction, rather than
against another implementation of K.

The signed principal Pfaffians F satisfy KF=0 exactly:

    F0 = -12abcd
    F1 = 2a(b³+c³+d³)
    F2 = 2b(-a³-c³+d³)
    F3 = 2c(-a³+b³-d³)
    F4 = 2d(-a³-b³+c³).

Set y=(F0/4,F1/2,F2/2,F3/2,F4/2). Symbolic expansion proves

    y0(y0³+y1³+y2³+y3³+y4³)+3y1y2y3y4=0.

These are precisely Bruin–Filatov's formulas at source coordinates
`(t1,t2,t3,t4)=(a,b,c,-d)`. This is not a new Burkhardt parametrization.

Five determinant-one canonical Weil generators satisfy exactly over Q(omega)

    F(go f)=ge F(f),
    K(go f)=ge^(-T) K(f) ge^(-1).

The generators are two Fourier gates, two local quadratic phases and CZ.
The canonical common symplectic action is specified; the different central
extensions defining G32 and G33 are not silently identified.

## The forty-ray rank drop

F0=0 forces at least one coordinate to vanish. One nonzero coordinate gives
four axes; two nonzero coordinates cannot make every remaining Fi zero.
Three nonzero coordinates give nine cube-root phase choices for each omitted
coordinate. This proves the projective base consists of exactly 4+4*9=40 rays.
At each, K is nonzero but all principal four-by-four Pfaffians vanish. Since
K is skew, its rank is exactly two. Away from the base its rank is four.

For each projective Pauli label v form the actual zero-character projector
Lv=(I+Dv+Dv†)/3. Its odd restriction is rank one and its even restriction rank
two. The odd projector matches exactly one of the forty constructed rays;
the numerical dictionary is bijective with residual below 1e-12. With A the
ordinary symplectic point commutation graph, the operator Gram identities are

    odd:  (2I-A+J)/3, rank16;
    even: (4I+A+2J)/3, rank25.

These are projector identities in their respective Hilbert spaces, not a
point-line self-duality claim. The base and rank assertions are symbolic; the
explicit Pauli dictionary and Gram replay are floating-point checks.

## Scalar alignment and a declared Dirac operator

Define S(f)=F†GF. For dimensionless f, supply

    V_tree/m0^4 = lambda (||f||²-1)² + kappa S(f),
    m_D(f)=m0*y*M(f),

with positive lambda,kappa and supplied scale m0 and Yukawa y. A canonical
scalar kinetic normalization can be supplied separately; none is inferred
from the finite graph. The minimum set is exactly the forty projective rays,
each with a common U(1) phase. At an axis the eight-coordinate real Hessian is
proved symbolically to have spectrum `0,8lambda,16kappa` with the last value
sixfold. Unitary covariance extends this to all forty rays; independent
numerical Hessians check every ray. The continuous phase is still flat.

M can be a Dirac matrix between distinct left/right species with the declared
contragredient finite-family transformation. Its skewness does **not** make
it an allowed identical-Weyl Majorana mass. No Standard Model gauge charges,
anomaly-free chiral content, or five-dimensional gauge multiplet are implied.

The producer proves both Tr(M†M)=||f||⁴ and
Tr((M†M)²)=||f||⁸/2-S/4 symbolically. Together with the paired singular values of a
complex skew matrix, gives on the unit sphere

    squared singular masses = 0,m-²,m-²,m+²,m+²,
    m±² = (1 ± sqrt(1-S))/4,
    m-² m+² = S/16, hence 0 <= S <= 1.

The pairing is the standard unitary-congruence normal form of skew matrices
([Youla1961](https://doi.org/10.4153/CJM-1961-059-8)). The Pfaffian norm is S/16
in the orthonormal basis. At a Witting ray the spectrum is `0,0,0,1/2,1/2`;
at S=1 it is `0,1/4,1/4,1/4,1/4`. A normalized `(1,i,0,0)` reaches S=1;
a continuous path from an axis reaches every intermediate S. Three zero
Dirac singular masses are not three chiral Standard Model generations.

## Exact angular phase competition in a finite shell

Fix ||f||=1 and integrate one declared five-species Dirac determinant over the
Euclidean shell x=p²/m0² in [A,B], with 0<A<B. The radial measure is
`d4p/(2pi)^4 = m0^4*x dx/(16pi²)` and the Dirac spin determinant contributes
-2 per singular species. Using the two equal-mass pairs gives

    Vf(S)/m0^4 = -1/(4pi²) integral_A^B
        x log[1+y²/(2x)+y⁴S/(16x²)] dx.

This physical measure was audited independently of the reduced formula,
catching and correcting a preliminary factor-two error before publication.
The leading y² term cannot select an orientation because the second mass
moment is constant. The next terms do: Vf is strictly decreasing and strictly
convex in S. Fermions alone favor the balanced rank-four phase, opposing the
forty-ray rank-two phase.

Let d=y²/4. The two exact thresholds are

    kappa_high = y⁴/(64pi²) log[(B+y²/2)/(A+y²/2)],
    kappa_low  = y⁴/(64pi²) {
       log[(B+d)/(A+d)] + d/(B+d) - d/(A+d) }.

They obey 0<kappa_low<kappa_high for y>0. The full angular energy
`kappa*S+Vf(S)/m0^4` therefore has:

- S=0 for kappa>=kappa_high: precisely the forty projective Witting rays;
- S=1 for kappa<=kappa_low: balanced rank-four mass states;
- one intermediate S*, defined by kappa+Vf'(S*)/m0^4=0, between the thresholds.

The intermediate order parameter is unique; the vacuum on that level set need
not be. At a Witting ray the six projective real curvatures are
`16(kappa-kappa_high)`. Equality gives a vanishing quadratic curvature with a
positive quartic angular term; strict inequality gives a positive normal gap.
For A=.01,B=.25,y=.2, the thresholds are approximately
`kappa_high=5.56563487259e-6`, `kappa_low=5.32800204153e-6`.

These are analytic results for a supplied finite-shell action at fixed radius.
Scalar/gauge loops, running, radial relaxation, UV matching, spacetime dynamics
and measured mass scales remain outside the calculation. Forty equivalent
rays do not select one physical vacuum or explain why its parameters lie in
the rank-two region.

## Verification

The source-bound JSON stores exact cyclotomic generators, the forty rays,
normal matrix, quartic kernel, canonical normalization and phase benchmarks.
Five regressions independently check the committed cubic tensor, corrupted
quartic sign, every base ray/rank, generic paired spectra, the actual Dirac
inventory with its Euclidean measure, and intermediate phase convexity.
The dedicated workflow verifies frozen certificates, regenerates them and
repeats the controls. The current paper is unchanged.


## Additional intake correction: a radial runaway in Pass11649

The parallel report's unit-sphere arrow search and filter algebra survive.
However, its proposed unrestricted potential
`kappa*(||psi||²-v²)²-lambda*h6(psi)²` is unbounded below for every positive
lambda: the actual imported h6 is homogeneous of degree12, and along its
nonzero-arrow displayed ray the negative term is
`-lambda*r²⁴/1289945088`. No quartic radial term can dominate that growth.
The report and producer header now retain only the constrained-sphere selector
and distinguish200 optimization starts from a proof of the global maximizing
set. Two regressions call the actual invariant on unnormalized fields and
verify homogeneity and the runaway. No stable radial completion is substituted
without proof.

The incoming three-suite replay initially had17 passing tests and one missing
Windows-Temp fixture. Relocating that existing fixture at runtime, without a
source or environment-variable change, made the remaining live test pass.
That is a local18-test replay with an external fixture, not portable CI proof
of every parallel packet.

### Corpus guard triage

The broad guard emitted compound-token candidates; this is not a silent guard
or an unqualified clean intake. The `f4` token here is a component/coordinate,
not an assertion about the exceptional Lie algebra F4. Read candidates
`analysis/BT1720_BT1723_repo_mining_execution.md`,
`analysis/PASS11562_11569_CANONICAL_SPIN_GAUGE_FRONTIER.md`, its reservation,
`analysis/PASS10954_REGULAR_C8_CLOCK_COMPLETION.md`, and
`analysis/PASS11550_VERONESE_WEIL_HAMMING_ORIENTATION.md` own other finite
charts, continuous stabilizers and clock/cone maps. They do not provide the
normal derivative or this Dirac phase calculation. The old experiment
scoreboards `analysis/w33_BREAKTHROUGH_128_decisive_experiment.py`,
`analysis/w33_BREAKTHROUGH_130_falsification_scoreboard.py` and
`analysis/w33_BREAKTHROUGH_131_theorem_index.py` use F4 as a numbered
falsifier; their physical formulas are not imported here. The Witting section
of `W33_FOR_EVERYONE.tex` is historical prior context, with newer corrections
in the forty-points paper; its Weil mentions refer to finite-field zeta results.
`analysis/w33_pass2716_2723_the_photon_reads_its_own_character.md` is credited
for the earlier phase-carrier distinction. No guard candidate establishes a
conflicting version of the two exact mass moments or the angular thresholds.
