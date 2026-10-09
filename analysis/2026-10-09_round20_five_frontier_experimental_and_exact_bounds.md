# Round 20 — five independent W33 experiments and exact bounds

**9 October 2026; W33-Theory main/master branch.** Build on Round19's
native graph source, not solely the 2026-09-26 original forty-points paper.
Prior art and independently committed parallel work remain acknowledged.
The simulations are not experimental demonstrations; mathematical model
assumptions do not imply a theory of everything.

## I. Single-photon: optimize the *observable* rather than speculate about nonlinear hardware

For each of five native PSp selector orbits, program Peierls phases
`(.49,-.74,1.22)` on the specified three edges of the 80-vertex W33
Levi adjacency. Define

`h_j(t)=sort_{v in 80} |<v| exp(-i t A_j)|v>|^2`

and the worst distinguishability `d(t)=min_{j<k} ||h_j(t)-h_k(t)||_infty`.

A **finite grid** t=0.25,0.30,...,12.0 found
`d(2.0)=0.001996643829863892`;
`d(10.35)=0.083530550890556`, an improvement exceeding 41x.
These are **numerical**, not rigorous enclosures of the matrix exponential
and not guaranteed continuous-time/global best t.

Conservative independent-survival-shot design: 5 candidate configurations
x 80 sites = 400 measured empirical Bernoulli probabilities.
Hoeffding and the union bound establish, for delta=0.05 and eta=d/4,

`N >= ceil(log(2*400/0.05)/(2*(d/4)^2))`

independent preparations **per site per candidate** suffice for
all 400 estimates to be within eta simultaneously with probability
>=95%, and their **sorted** values to preserve at least half the
separation. At t=2, N=19,425,830 per site, total 7,770,332,000.
At t=10.35, N=11,100 per site, total 4,440,000
(all five reference-candidate libraries; unknown-orbit sensing uses
different experimental allocations). This is an exceptionally
conservative worst-case bound, **not** a power analysis including
source or detection losses, background, dead time, dark counts,
port crosstalk, or manufacturing variation.

Static link phase errors with absolute magnitude at most epsilon on
160 independent links induce ||A-A'|| <= sqrt(320)*epsilon (Frobenius),
|probability shift|<=2 t sqrt(320) epsilon per configuration, hence
worst pairwise separation >= d-4t sqrt(320) epsilon. Our displayed
tolerance uses epsilon <= d/(8t sqrt(320)) to preserve >=d/2.
This is sufficient, far from tight. The design requires long enough
coherence to implement t~10.35 and read 80 site-resolved probabilities.

## II. Global native frustrated plaquette geometry: exact lower bound and actual trial upper bound

Let C have the 1620 oriented 8-cycle rows and 160 oriented link columns
(W33 native point-line Levi). Previous Round19:
rank C=81 and 79 gradient gauges; 4320 three-plaquette theta
identities with signs F_a +/- F_b +/- F_c =0.

Round20 greedily exhibits **485 mutually plaquette-disjoint** theta
triples (a source-recomputable list of indices). Each obeys
`cos(2F_a)+cos(2F_b)+cos(2F_c)>=-3/2`, not -3. The other
1620-3*485=165 plaquettes individually obey >=-1. Thus
`V(theta)=sum_c cos(2(C theta)_c) >= -3/2*485-165 = -892.5`.
This is **rigorous** and strictly stronger than the naive -1620.
It proves global simultaneous plaquette-minimum frustration.

Fix a spanning tree (79 link coordinates) and optimize the
remaining 81 independent chord phases with exact analytic gradient
`dV/dtheta_e=-2 sum_c C_ce sin(2 Ctheta)_c`.
Nine deterministic L-BFGS-B starts achieve best **V~-328.40265854**,
with recorded gradient infinity norm ~7.5e-5. As evaluated, this
is a **numerical candidate upper bound**; not globally minimized or
interval-certified. Consequently
`-892.5 <= inf V <= about -328.403`.
The lattice is finite, and the chosen frustrated action is
postulated; no emergent 3+1 spacetime or chiral vacuum is implied.
Under theta->-theta the action remains even.

## III. Exact rational-interval global coherent-displacement *no-go* at each classical zero star

Take the **native 78-dimensional** W33 quantum current-square H
from Pass11769. Its optimized centered complex Gaussian has energy
about **128.887391415527**. For each of all 80 explicit classical-zero
star coherent directions (one point or one line at a time), keep the
Pass11769 exact centered covariance and quadratic phase **fixed**
and displace canonical means by real parameters `s*q_star,r*p_star`.

There are generally NONZERO cubic terms. Wick's formula yields

`E(s,r)-E0=A s²+B r²+T sr+W s²r+Z sr²+R s²r²`.

All 80 coefficient families were recomputed from **exact incidence
integers**, via rational quantities rx, ry; A,B,T depend on the
isolated algebraic values sqrt(10), m, t, f. The previously published
*exact rational isolating brackets* for sqrt10 and the stationary t
are reused. Outward rational interval arithmetic (Python Fraction)
proves for **each** of 80 stars:

- A>0, B>0, R>0;
- alpha(s)=B+Zs+Rs²>0 for every real s, by Z²-4BR<0;
- D(s)=4A alpha(s)-(T+Ws)²>0 for every real s, by the positive
  leading and constant terms and negative discriminant.

Now complete the square:

`E(s,r)-E0 = alpha(s) * [r+s(T+Ws)/(2alpha(s))]^2
             + s² * D(s)/(4alpha(s)) >= 0.`

Equality holds only at s=r=0. Thus **all 80** centered star-directed
two-amplitude displacement sectors have exact **global**, unique
minimum at zero at *fixed covariance/phase*. This is much stronger
than the Round19 local numerical Hessian check, and is NOT the
spectrum's lower bound, nor unrestricted Gaussian optimality.

Every rational strict sign is code-checked. Coarse displayed
numerical margins include:
min D(0)>231.33, min quadratic leading coefficient D2>16160,
max discr(D)<-1.4e7, max discr(alpha)<-11.9.
The exact intervals, not floating approximations, authorize the
conclusion.

## IV. Frozen heterotic Z6-II benchmark: 8 source-specific antisymmetric zeros

The frozen 176-field Z6-II model has 424 cubic monomials with exact
nine-U1 neutral charge, 90 passing the stored corrected-R/nonR necessary
rules. All 90 satisfy the point-group twist sum(k)=0 mod6, and
pass the earlier SU3xSU2xSU4xSU2 tensor-*existence* masks.

**New exact algebraic exclusion:** Eight of those 90 contain two
identical commuting chiral superfields whose only available gauge
singlet contraction in a non-Abelian SU2 (or SU3 epsilon) sector
is antisymmetric, so epsilon Phi Phi=0. Representatives:
`d_1 q_2 q_2`, `d_3 q_3 q_3`, `n_15 w_5 w_5`.
Thus only **82** retain all these necessary conditions.

This is a true zero-coupling conclusion for the eight affected
monomials, separate from worldsheet selection. It does NOT prove
that any of the remaining 82 are nonzero: the supplied field schema
does not provide full constructing space-group elements, oscillator
polarization, CFT picture-changing distribution, gamma phases,
worldsheet instanton solutions, or Kähler/complex moduli.
Literature: Kobayashi, Parameswaran, Ramos-Sanchez and Zavala,
*JHEP* 05 (2012) 008, arXiv:1107.2137;
*Demystifying stringy miracles with eclectic flavor symmetries*,
Phys Rev D (2026), DOI 10.1103/p6p2-46s1.
This is the Z6-II 176-field scope; the parallel Pass11810-11825
**Z6-I** Yukawa and gamma-corrected results must not be silently
translated to this separate frozen orbifold.

## V. Independent-actuator, blocked-light + calibrated reference design

A synthetic full-factorial experiment randomly chooses two independent
signed actuators r1,r2, optical blocker b in {0,1}, detector swap d.
The optical response is assumed proportional to `r1*r2*b`.
All eight additive first/second-order nuisance terms are included,
with the ninth parameter `r1*r2*b`; design rank **9**.

If the optical sensor contains `(beta_opt+beta_leak)*r1*r2*b`,
the optical signal remains unidentified by randomization alone.
A **second, independently calibrated dark electronics reference**
is assumed to measure `gain*beta_leak*r1*r2*b`, allowing the
conditional estimator `beta_opt=beta_Y-beta_Z/gain`.
For 16,000 synthetic draws with beta_opt=0.08 and leak=0.07,
calibrated estimator **0.08008285** and nominal standard error
~8.95e-5. However a **10% gain mismatch** biases beta_opt by
about **-0.00692**, dwarfing that synthetic standard error.
A 1% unknown gain produces a nontrivial systematic error floor
even with arbitrarily many shots.

This is **not** lab evidence or a complete causal identification:
a dark reference could fail to copy all leakage paths, couple to
real optical signal, or change transfer function upon blocking.
An operational experiment must measure those assumptions, not
declare them self-evident.

## Execution, source, novelty boundary

Producers:
- `analysis/w33_20261009_round20_photon_budget.py`
- `analysis/w33_20261009_round20_global_plaquette.py`
- `analysis/w33_20261009_round20_vacuum_star_hessian.py`
- `analysis/w33_20261009_round20_exact_star_interval.py`
- `analysis/w33_20261009_round20_heterotic_amplitude_obstructions.py`
- `analysis/w33_20261009_round20_two_actuator_dark_reference.py`
- `tests/test_w33_20261009_round20_five_fronts.py`

Outputs are six source-derived JSON certificates. Tests independently
recompute the key finite W33 theta relations, rational star intervals,
heterotic counts, and optical negative controls.

**No new full TOE, physical mass spectrum, gravity theory, or verified
photonic hardware is established.** Two rigorous mathematical advances
(global frustrated-action lower bound and all-star Gaussian coherent
non-improvement) plus experimental design and frozen-worldsheet
counterexamples constitute the results.
