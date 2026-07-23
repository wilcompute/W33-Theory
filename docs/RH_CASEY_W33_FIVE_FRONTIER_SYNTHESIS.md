# Casey / W(3,3) Riemann Program: Five-Frontier Execution

## Executive result

Casey's invariant-tangent presentations are not yet a proof of the classical
Riemann Hypothesis, but their central intuition is closer to a rigorous object
than a purely visual reading suggests. Three ideas survive after correction:

1. the pole at `s=1` really can be replaced by finite analytic data, by using
   Riemann's completed entire function `xi(s)` with `xi(0)=xi(1)=1/2`;
2. the proposed phase torque is a legitimate logarithmic phase current,
   `tau(s)=Im(xi'(s)/xi(s))`, away from zeros;
3. the unequal-distance picture of an off-line reflected zero pair can be
   converted into a positive, no-cancellation defect energy.

The third item is the strongest constructive repair. It yields an exact
RH-equivalent orbit detector and matches the W(3,3) graph-RH geometry. What
remains missing is an analytic theorem forcing the total classical defect
energy to vanish.

## What Casey has genuinely identified

### 1. A valid regularization is hiding inside the "topological anchor"

The slide decks treat the zeta pole at `s=1` as an infinity that becomes a
finite stationary anchor under a compactifying map. An arbitrary
stereographic map does not prove that claim, but the completed function does:

```text
xi(s) = (1/2) s(s-1) pi^(-s/2) Gamma(s/2) zeta(s)
xi(0) = xi(1) = 1/2.
```

Thus the pole is not merely drawn as finite; it is analytically removed. The
correct anchor is the finite endpoint value of `xi`, not a postulated
orthogonal rotation.

This preserves the strongest part of the diagrams on pages 3-6 of the three
presentations while replacing the undefined "divide-by-zero event" with a
standard entire completion.

### 2. The phase-torque language has an exact analytic meaning

The decks define a phase field and differentiate it in the real direction.
Away from zeros this is rigorous:

```text
Phi(s) = arg xi(s),
tau(s) = partial_sigma Phi(s) = Im[xi'(s)/xi(s)].
```

The complete logarithmic derivative is

```text
xi'/xi = 1/s + 1/(s-1) - (1/2)log(pi)
         + (1/2)psi(s/2) + zeta'/zeta.
```

This formula incorporates the endpoint factors, gamma factor, trivial-zero
structure, and prime-sensitive zeta term. It is the correct global phase
current. Its contour integral is branch-independent:

```text
(1/(2 pi i)) integral_C xi'(s)/xi(s) ds = number of zeros inside C.
```

The executable certificate obtains winding number `1` on the rectangle
`0.1 <= Re(s) <= 0.9`, `10 <= Im(s) <= 18`, which contains the first
nontrivial zero.

### 3. The reflected same-height pair is the right orbit

If `rho=beta+i gamma` is a zero, functional equation plus conjugation gives
another zero at

```text
rho_star = 1-conj(rho) = 1-beta+i gamma.
```

That is exactly the same-height pair used in Casey's distance diagrams. The
geometric instinct is therefore sound: the horizontal displacement from the
critical line is the orbit defect

```text
delta = beta-1/2.
```

## The decisive sign correction

Pages 12-15 of the white presentations explicitly differentiate the two zero
factors and then add them. For the product of the reflected factors, the
current is

```text
P(s) = (s-rho)(s-rho_star),
partial_sigma arg P(s)
 = -(t-gamma)/((sigma-beta)^2+(t-gamma)^2)
   -(t-gamma)/((sigma-(1-beta))^2+(t-gamma)^2).
```

The terms add. They do not cancel when `delta=0`. At Casey's boundary
`sigma=1`, with `t=0`, `gamma=14`, the critical-line value is approximately
`0.1426751592`, not zero. The presentation's own plus sign therefore defeats
its final `delta=0` conclusion.

The claimed boundary condition also fails for the full completed function.
The exact certificate gives

```text
tau(1+0.1 i)  = 0.0046155053...
tau(1+5 i)    = 0.2409669170...
tau(1+14 i)   = 1.0719719578...
tau(1+30 i)   = 1.8250740016...
```

So `tau(1+it)=0` is not an identity imposed by completion or compactification.

## The constructive repair: reflection-cocycle energy

Casey's desired distance imbalance does become exact if the product is
replaced by the ratio of reflected factors:

```text
R_rho(s) = (s-rho)/(s-rho_star).
```

Its phase current is

```text
A_rho(s) = Im[d/ds log R_rho(s)]
 = -(t-gamma)/((sigma-beta)^2+(t-gamma)^2)
   +(t-gamma)/((sigma-(1-beta))^2+(t-gamma)^2).
```

This is the difference of the two geometric pulls. It is odd in `delta` and
vanishes identically when `beta=1/2`.

A pointwise current can still change sign, so the no-cancellation object is its
squared integral. Put `a=sigma-1/2` and assume `|delta|<a`. Exact integration
gives

```text
E_rho(sigma)
  = integral_R A_rho(sigma,t)^2 dt
  = pi delta^2 / (a(a^2-delta^2)).
```

At `sigma=1`,

```text
E_rho(1) = 8 pi delta^2/(1-4 delta^2).
```

Therefore

```text
E_rho >= 0,
E_rho = 0 iff Re(rho)=1/2.
```

This is a rigorous version of Casey's topological shear or torque imbalance.
It removes cancellation orbit by orbit. For a finite collection of reflected
orbits, the sum of these energies vanishes exactly when every orbit is on the
critical line.

For the classical zero set this is an equivalent detector, not a solution:
one still must derive, from `xi` itself, a convergent weighted identity forcing
the total energy to be zero. That missing identity is now sharply stated.

## Exact W(3,3) realization of the repaired idea

For the W(3,3) collinearity graph, the restricted adjacency spectrum is

```text
2^24, (-4)^15,
```

and the nontrivial Ihara factor is

```text
(1-2u+11u^2)^24 (1+4u+11u^2)^15.
```

The four distinct nontrivial pole locations are

```text
u = (1 +/- sqrt(-10))/11,  order 24,
u = (-2 +/- sqrt(-7))/11, order 15.
```

Every pole has modulus `1/sqrt(11)`. Under the correct coordinate

```text
u = 11^(-s),
```

the circle becomes `Re(s)=1/2`. Thus every W(3,3) orbit has `delta=0`, and the
repaired Casey defect energy is exactly zero.

The new exact Laurent engine computes all principal-part coefficients. It
also corrects the old counting language:

```text
39 restricted adjacency slots,
4 distinct nontrivial pole locations,
total nontrivial pole order 78.
```

The pole fields and coordinate denominator ideals are:

```text
Q(sqrt(-10)), discriminant -40,
  denominator generators 1 -/+ sqrt(-10), norm 11;
Q(sqrt(-7)), discriminant -7,
  denominator generators -2 -/+ sqrt(-7), norm 11.
```

Each coordinate is the inverse of the conjugate norm-11 generator. The
relevant denominator is a prime ideal factor above `11`, not the full ideal
`(11)`.

## Frontier 1: global argument-principle current - executed

Implemented `analysis/w33_casey_phase_current.py`.

Results:

- completed-xi regularization used instead of an arbitrary manifold map;
- exact decomposition of `xi'/xi` verified numerically to high precision;
- Casey's pointwise boundary-zero condition falsified;
- contour winding around the first zero certified;
- reflection-cocycle energy derived analytically and verified by numerical
  integration.

Certificate:

```text
data/w33_casey_phase_current_certificate.json
```

## Frontier 2: genuine self-adjoint W(3,3) operator - executed

Implemented `analysis/w33_rh_phase_operator.py`.

Let `A_perp` be adjacency restricted to the 39-dimensional nonconstant sector.
Because `A_perp/(2 sqrt(11))` is a self-adjoint contraction, define

```text
Theta_W = arccos(A_perp/(2 sqrt(11))).
```

This is a genuine self-adjoint phase operator, with two spectral angles:

```text
theta_2  = arccos(1/sqrt(11)), multiplicity 24,
theta_-4 = arccos(-2/sqrt(11)), multiplicity 15.
```

It gives the exact determinant identity

```text
det(I - 2 sqrt(11) u cos(Theta_W) + 11 u^2 I)
 = (1-2u+11u^2)^24(1+4u+11u^2)^15.
```

This is a finite Hilbert-Polya realization for graph-RH.

The classical transfer was tested rather than assumed. Taylor coefficients of
`log(xi(1/2+z)/xi(1/2))` were compared with both the principal W(3,3) phase
spectrum and its full logarithmic vertical tower. A scale can match the
quadratic coefficient, but the scale-free quartic and sextic ratios disagree.
Therefore the current operator is exact for Ihara zeta but does not reproduce
the classical Hadamard product.

Certificate:

```text
data/w33_rh_phase_operator_certificate.json
```

## Frontier 3: automated claim governance - executed

Implemented `scripts/rh_claim_linter.py` and
`data/rh_claim_policy.json`.

The linter distinguishes:

- exact finite graph-RH claims;
- standard completed-xi identities;
- equivalent positivity criteria;
- candidate transfer bridges;
- classical-solution claims requiring an actual transfer theorem.

It flags unqualified statements such as "we prove the classical Riemann
Hypothesis," "RH holds," or "Hilbert-Polya is realized," while allowing
explicitly scoped finite analogues and negative audit statements. It is
report-only by default and supports strict changed-file CI mode.

Self-audit:

```text
data/rh_claim_lint_self_audit.json
```

## Frontier 4: exact finite-zeta principal parts - executed

Implemented `analysis/w33_ihara_principal_parts.py`.

The script uses exact quadratic-field arithmetic and computes every negative
Laurent coefficient at all four distinct nontrivial pole locations. It
records:

- pole orders;
- exact leading Laurent coefficients;
- exact residues;
- all principal-part coefficients;
- residue fields and discriminants;
- coordinate denominator ideals;
- exact truncated-series inverse certificates.

Certificate:

```text
data/w33_ihara_principal_parts_exact.json
```

## Frontier 5: reflection-countermodel classification - executed

Implemented `analysis/w33_reflection_countermodels.py`.

Write `z=s-1/2`. Every real polynomial satisfying `F(1-s)=F(s)` has the form

```text
F(s)=Q(z^2), Q in R[y].
```

Its finite zero set lies on the critical line exactly when all roots of `Q` are
real and nonpositive. Equivalently, up to a real constant,

```text
F(s)=det(z^2 I + H^2)
```

for a finite self-adjoint `H`.

For Casey's reflected quartet,

```text
F=((z-delta)^2+gamma^2)((z+delta)^2+gamma^2),
Q(y)=y^2+2(gamma^2-delta^2)y+(gamma^2+delta^2)^2,
disc(Q)=-16 gamma^2 delta^2.
```

For nonzero `gamma`, `Q` has real nonpositive roots exactly when `delta=0`.
This pinpoints the extra axiom that symmetry lacks: an exact self-adjoint-square
determinant or an infinite-dimensional positivity theorem of comparable
strength.

Certificate:

```text
data/w33_reflection_countermodel_certificate.json
```

## Constructive criticism of Casey's current presentation

### Retain

- The completed-function anchor idea, rewritten as `xi(0)=xi(1)=1/2`.
- The phase-gradient/electrostatic visualization, with
  `tau=Im(xi'/xi)` stated explicitly.
- The same-height reflected pair and its geometric distance asymmetry.
- The language of equilibrium, provided equilibrium is defined by a positive
  functional rather than an asserted pointwise boundary condition.
- The manifold graphics as motivation, not as mathematical objects carrying
  unproved curvature or stability laws.

### Replace

- Replace `tan(theta)=Im(z)/Re(z)=tan(phi/2)` as a "metric" with either a
  specified conformal coordinate map or the involution `s -> 1-conj(s)`.
- Replace the arbitrary compactification of the zeta pole with the completed
  entire function.
- Replace phase values at zeros with contour winding or logarithmic derivatives
  on punctured domains.
- Replace the product-current cancellation claim with the reflection-cocycle
  ratio.
- Replace pointwise `tau(1+it)=0` with the positive orbit-energy target.
- Replace "manifold fracture" with a named coercive functional and a proof of
  its sign.

### Correct the functional-equation phase relation

For real-symmetric `xi`,

```text
xi(1-sigma+it)=conj(xi(sigma+it)).
```

Hence the phase is negated modulo `2 pi`; it is not generally identical. The
horizontal phase current is correspondingly even under reflection, not the odd
quantity asserted in the decks. The antisymmetric object must be deliberately
constructed as a cocycle.

## The combined Casey/W33 derivation now available

The collaboration yields the following exact chain:

1. `xi` supplies the legitimate analytic regularization and global phase
   current.
2. Casey's reflected-pair geometry supplies the orbit coordinate `delta`.
3. The corrected reflection cocycle supplies a local asymmetry current.
4. Squaring and integrating supplies a positive no-cancellation energy.
5. W(3,3) supplies a complete finite model in which that energy vanishes due
   to the Ramanujan/Ihara critical-circle theorem.
6. The self-adjoint W(3,3) phase operator realizes the graph determinant
   exactly.
7. Classical RH is reduced to finding a trace, positivity, or determinant
   theorem that identifies the classical completed-xi object with a limit or
   completion of this zero-defect architecture.

This is substantially stronger than either presentation alone. It does not
close classical RH, but it converts Casey's most promising geometric idea into
an exact functional and gives the repository a precise target for the missing
transfer theorem.

## Validation

```text
python -m py_compile analysis/*.py scripts/*.py
pytest -q tests/test_rh_five_frontiers.py
7 passed
```
