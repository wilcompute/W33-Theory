# Pass 11601: match the metric before extracting gravity from a heat trace

Reservation `5c1c6e4ae`, Codex track. The new construction identifies a specific
geometric mismatch in Pass 11594 and supplies an independently calibrated Dirac
operator. It recovers the standard curvature coefficient on supplied smooth
metrics, including a static four-dimensional extension. It does not derive
physical spacetime or its dynamics from W33.

## Intake and prior ownership

Read all 351 lines of the new `ChatNext.txt` handoff as evidence. GitKraken
reviewed the three remote commits after `2cdc68710`, through `5e2c7b33d`, and
integrated their six changed paths. The scientific change removes runtime
seconds from the 11594 certificate and repairs report formatting; its numerical
heat/curvature values remain unchanged. Its new workflow specifies a complete
packet replay. A workflow definition alone is not a claim that this session
verified its remote run status.

Relevant owners were read before computing:

- 11557: actual graded rank-four Cl(3) matrices used in the exact symbol check.
- 11559: constant-frame symbol and fixed-dimensional refinement tower. Its
  quadratic-form matrix is correctly computed; interpreting that coefficient
  as a covariant metric requires care because momenta are covectors.
- 11563, in `w33_pass11562_11569_canonical_spin_gauge_frontier.py`: local Cartan
  connection construction. The same packet owns the flat Wilson/species test.
- 11594: the preserved non-diagonal triad, curvature and finite heat table.
- `w33_einstein_field_equations_from_spectral_action.py`: earlier Christoffel,
  Ricci and conditional EH-variation work. Tests reuse only its pure geometry
  functions, not a claim that a native continuum action has been established.
- The native pair-vielbein and wound-wall results in 11335–11349 and 11379–11383
  address different supplied actions and constraints. They do not establish
  the continuum limit of this Dirac operator.

All heat coefficients below are standard results, credited to
[Vassilevich (2003), equations 3.26–3.27 and 4.13–4.15](https://arxiv.org/abs/hep-th/0306138).
The contribution is the map-level diagnosis and executable calibration, not
discovery of the Dirac heat expansion or Einstein-Hilbert action.

## Two metrics in the old comparison

Let E[a,i] be a coframe: theta^a=E[a,i] dx^i. Its covariant metric is
g=E^T E and its volume density is J=det E>0. The inverse frame coefficient is
e_a^i=(E^-1)[i,a]. Thus the geometric Clifford symbol must satisfy

    Q(p)=gamma^a e_a^i p_i, Q(p)^2=(p^T g^-1 p) I.

The 11594 Cartan and curvature calculations use E as a coframe, including E^-1
in the curvature contraction. But its Dirac derivative instead contracts
gamma^a E[a,i] partial_i. Its symbol square is p^T E^T E p. The same matrix
therefore denotes the covariant curvature metric and the contravariant symbol
metric. In general these are different geometries. Exact multiplication in the
actual native Clifford carrier proves both identities; an orthogonally rotated
coframe verifies the corrected quadratic form in a second realization.

This is not a retraction of the old finite numbers: they remain values of the
specified finite operator. This packet constructs a separate geometric benchmark.

## A leading volume obstruction, before scalar curvature

For the old continuum symbol the spectral volume is integral dx/J, whereas
the coframe volume is integral J dx. After 11594 normalizes the latter to
V=(2pi)^3, the nonconstant positive density obeys mean(J)=1 and

    mean(1/J)>1,

by strict Cauchy-Schwarz. Thus its flat-reference heat subtraction has a
nonzero leading volume term, not just the desired scalar-curvature term.
For the actual raw determinant positivity holds everywhere: it is bounded below
by exp(-3eps)-0.0175eps^3, which is positive at eps=0.12.
For the actual eps=0.12 determinant (including the cyclic off-diagonal product),
independent 16/32/64-point quadratures give

    V_geometry = 248.05021344239853,
    V_old_symbol = 253.46146265674554,
    unmatched volume = 5.411249214347001.

The corresponding continuum Delta a0 is
4(4pi)^(-3/2) times the unmatched volume. It multiplies t^(-3/2); curvature
multiplies t^(-1/2). Lower-order connection terms cannot fix a principal-symbol
volume mismatch. Wilson scaling and finite lattice cutoffs introduce additional
effects; this audit does not assert that this one obstruction explains every
entry of the old table.

## A separate operator with matched geometry and density

Use the standard geometric Dirac with inverse frame and Levi-Civita spin
connection on L2(J dx), then conjugate by the half-density map U=J^(1/2)
to ordinary L2(dx). Choose a volume-normalized conformal torus

    g=s^2 exp(2 sigma(x)) I3,
    sigma(x)=eps cos x, s=I0(3eps)^(-1/3).

Here I_n is the modified Bessel function. The transformed operator is exactly

    Dhat=f^(1/2) Dflat f^(1/2), f=exp(-sigma)/s.

The x derivative is the Hermitian anticommutator of f and Fourier momentum.
Transverse Fourier shells reduce the heat calculation to 2L-dimensional blocks;
the native rank-four carrier contains two spin irreps, giving the trace factor2.
This permits much finer resolution than a dense 4L^3 matrix. An independent
full three-dimensional matrix test checks that reduction and the species count.
No Wilson term or finite-difference doubler is used in this separate benchmark.
Fourier differentiation is nonlocal at finite cutoff; implementing its continuum
geometry through native finite-range links remains open.

The independently derived scalar curvature is
R=s^(-2)exp(-2sigma)(-4sigma''-2sigma'^2), hence

    integral sqrt(g) R = 2(2pi)^3 s eps I1(eps).

For rank-four spinors, define

    C3(t)=sqrt(t) [K_g(t)-K_flat(t)] / integral sqrt(g) R.

The standard coefficient is -1/[3(4pi)^(3/2)] = -0.007482796755215274.
The producer uses eps=0.12 and0.20, L=81/121/161, transverse cutoff80, and
t=0.05/0.025/0.0125/0.00625. At the finest resolution/time, the raw values are
-0.00748760195533004 and -0.007487846135705225. The raw relative discrepancies
are below0.07%. Coarser resolutions are stored, including their failures to
resolve the smallest heat time; a coarse cutoff is not mistaken for convergence.

## Predict the curvature-squared correction; do not fit it

The standard Dirac endomorphism is E_Laplace=-R/4. Independently contracting
spin curvature gives tr Omega_ij Omega^ij=-rank Riem^2/8. In three dimensions
Riem^2=4Ric^2-R^2, so the integrated rank-four coefficient simplifies to

    a4=(4pi)^(-3/2)/30 integral sqrt(g)(R^2-3Ric^2).

For the conformal family its integral is exactly
-2(2pi)^2/s times integral exp(-sigma)(sigma''-sigma'^2)^2 dx.
This is evaluated from the metric, independently of the heat eigenvalues.
The producer subtracts the resulting t a4/integral R from C3(t), and checks
agreement with the prescribed a2 coefficient within10 parts per million.
This subtraction isolates a heat coefficient; it is not a derived physical
renormalization prescription or cancellation of vacuum energy.

A second, nonconformal metric tests the distinction:
g=s^2 diag(1,f(x)^2,1), f=exp(eps cos x), s=I0(eps)^(-1/3).
Its integrated scalar curvature is exactly zero because
integral sqrt(g)R=-2s(2pi)^2 integral f'' dx=0. The heat deformation is still
nonzero and follows the independently predicted a4 term. It must not be
labelled an Einstein-Hilbert contribution merely because the metric varies.

## Static four-dimensional bridge

Take gamma_i=tau1 tensor sigma_i and gamma_time=tau2 tensor I. Then
D4=D3+gamma_time p_time and D4^2=D3^2+p_time^2 exactly. With a periodic time
circle of length2pi, K4=theta(t)K3 and integral R4=2pi integral R3.
Consequently t Delta K4/integral R4 approaches

    -1/[3(4pi)^2].

The finest finite benchmark agrees within0.2%. This is a static Riemannian
product calibration, not a result for arbitrary four-dimensional frames,
Lorentzian time evolution, native locality, frame dynamics or Newton's constant.
Cutoff/action moments, matter matching and the cosmological constant are open.

## Verification

Producer: `analysis/w33_pass11601_matched_metric_dirac.py`.
Certificate: `data/w33_pass11601_matched_metric_dirac.json`, bound by portable
SHA256 to the preserved 11594 source/certificate and native 11557/11559 sources.
Regressions: `tests/test_w33_pass11601_matched_metric_dirac.py`, including exact
symbols, independent Christoffel curvatures, a full 3D heat matrix, spin-curvature
contraction, both metric families and the 4D Clifford map. The initial symbolic
comparison needed polynomial expansion; the initial test suite had a wording
assertion failure. Neither incomplete run is counted as a verified packet.

Final producer: every section PASS, including the analytic a4 controls.
Final focused suite: nine tests PASS in35.55s. The primary-source coefficients
are prescribed before the numerical calculation, not fitted to it. Dedicated
CI replays the producer and tests; its remote status is reported separately.
