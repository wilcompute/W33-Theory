# Passes 12341–12345: global Bloch classification and four physical controls

**Result:** the nonzero-momentum magnetic zero set of the specific native
three-mixed-loop model is classified on the **entire unitary Bloch torus**.
It is exactly one explicit complex quadratic equation in four phases. At
every point of that set there is exactly one complex nongauge magnetic null
direction. Both the earlier six-loop model and the positive 24- and 12-term
repairs have no such zeros at any nonidentity unitary character.

This is a theorem about a named finite-range quadratic lattice model. It is
not a derivation of a physical photon, gravity or a theory of everything.
The other four requested directions were tested on concrete, explicitly
limited models; none is claimed to have closed the full physical problem.

**Producers and data:** `analysis/w33_pass12341_12345_geometry.py`,
`analysis/w33_pass12341_12345_physics.py`, with the same basenames under
`data/`. Independent checks are in `tests/test_w33_pass12341_12345_geometry.py`
and `tests/test_w33_pass12341_12345_physics.py`.

## 12341. Complete exceptional-momentum equation

The setup is the existing 27-vertex, 135-link native four-period cover. Let
F be its 105 selected short-face rows, L the four based period paths, and
L6 the six based commutator rows. Let the period matrix be

```
W = [ 0  1  1 -1
     -1  0  1 -1
      0  0  1 -1
      0  0  1  0 ],   det W=1.
```

For Bloch character z=(z0,z1,z2,z3), define
h_i=product_j z_j^(W_ij) and d_i=h_i-1. The previously owned three-mixed
matrix is

```
R = [1 0 5 -5 1 0
     0 1 -1  0 1 0
     0 0 5 -5 0 1].
```

Define Q(d)=d^T N d/2, where

```
N = [10 -5  1 -6
     -5 10 -5  6
      1 -5 10 -6
     -6  6 -6 12].
```

**Theorem.** On the unitary torus, for every z other than the identity,

* if Q(d)=0, rank(F plus R L6)=107 and there is exactly one complex
  magnetic null direction after quotienting the rank-27 gauge gradients;
* if Q(d) is nonzero, this curl has rank108 and has no nongauge magnetic
  null directions;
* F plus all six commutator rows has rank108 at every nonidentity z.

At the identity, all six commutator rows vanish, F has rank105, the
gradient has rank26, and four global holonomies remain. At nonidentity
the rank conclusion for F and both curl matrices actually holds on the
whole algebraic torus `(C*)^4`; the positive-Hessian and gauge-orthogonal
language is restricted to unitary characters.

### Proof and certificates

1. The actual signed lifted chains satisfy the six integer Laurent
   identities `L_ij=(1-h_j)L_i+(h_i-1)L_j`. They are reconstructed from
   literal repository paths, not assumed from a continuum approximation.
2. Fraction-free elimination using only units `+/- z^v` constructs a
   **105-by-105 Laurent minor** of F equal to
   `-z0^-12 z1^2 z2^18 z3^-15`, and a **109-by-109 Laurent minor** of
   the stacked matrix `[F;L]` equal to
   `z0^-14 z1^2 z2^20 z3^-18`. These never vanish on `(C*)^4`. Every
   pivot, column and integer Laurent exponent is in the JSON certificate;
   direct determinants at three modular specializations check the signs.
   Consequently F has rank105 and the four period-path rows are
   independent modulo F for every such character.
3. Write the commutator symbol as C(d), whose `(i,j)` row is
   `d_i e_j - d_j e_i`. For d nonzero, C has rank3. Exact expansion of
   the four 3-by-3 minors of R C gives `d0 Q, -d1 Q, d2 Q, -d3 Q`.
   A Groebner calculation on each of the four projective charts `d_i=1`
   shows that its 2-by-2 minors cannot all vanish. Thus rank(R C)=2 on
   Q=0 and 3 off it. Independence of L modulo F transfers these ranks
   to the original 135-link curl without hidden exceptional cases.
4. W is unimodular. If z is nonidentity, some h_i differs from 1.
   A twisted vertex function with zero gradient must return to its
   root multiplied by h_i along the corresponding period path, so it
   vanishes. Hence the gradient is injective with rank27. At identity
   connectedness leaves only the constant vertex function.

This gives an actual all-momentum classification, including the
short-face exceptional-rank question left open by previous generic
specializations. The exact positive 12-term parallel repair from
`449bcd3c55`, and the earlier 24-term repair from Pass12340, both have
the same magnetic Hessian kernel as the six-loop model on every unitary
character. The theorem therefore closes their nonidentity zero-mode
question. It does not establish a volume-independent mass gap: the
acoustic eigenvalues approach zero at long wavelength.

### Geometry and a finite-cover count

At the previously known character `(omega,omega,1,1)`, the Jacobian of
`(Re Q, Im Q)` with respect to the first two loop angles has determinant
`-225 sqrt(3)/2`. The implicit-function theorem therefore gives a smooth
**two-dimensional sheet** of exceptional unitary characters nearby.
This refines the earlier isolated witness.

The reflection-fixed momentum slice z0=1 meets Q=0 at
`(1,1,omega,omega^2)`; a Jacobian minor there is `54 sqrt(3)`, so its
intersection contains a local smooth **one-dimensional curve**. Thus
merely choosing the reflection-fixed momentum subspace does not remove
the unprojected zero sheet.

For all `3^4=81` characters of a period-three cover, exact arithmetic
finds exactly ten nonidentity characters on Q=0, grouped in five complex
conjugate pairs. A separately implemented modular-rank test checks every
actual Bloch matrix at all 81 characters. The real magnetic kernel modulo
gauge has dimension **14**: four global holonomies plus ten real
nonidentity modes. For either repaired action or the six-loop action its
dimension is **4**.

The unwanted sheet is separated from zero momentum. If the four loop
angles t_i satisfy `max |t_i|<=1/20`, exact norm estimates give

```
|Q(exp(i t)-1)| >= (3051/7360) ||t||^2.
```

This conservative bound is not an optimal ultraviolet separation.

**Prior ownership:** the explicit order-three mode, 24-term repair and
zero-frequency response belong to Pass12340 (`52f055d773`). The three-loop
endpoint and 12-term repair belong to `9baf04f175` and `449bcd3c55`.
The global Laurent minors, full zero-set equation, exact finite-cover census
and quantitative zero-free neighborhood are the additional results here.

## 12342–12343. Matter-induced selection and a common interacting response

The actual six commutator loops generate a finite lifted patch with
43 vertices, 48 edges and six independent cycles. The code constructs
their flux-dual edge fields and computes static and frequency responses
from one Peierls-coupled fermion Hamiltonian, including its diamagnetic
contact and temporal-density vertex. This is a supplied finite patch,
not a thermodynamic cover.

For a full-Fock **free spinless** Gibbs model at T=0 and mu=0.3, the
static six-flux Hessian has eigenvalues ranging from approximately
**-0.08440 to +0.04978** while its electric coefficient is positive in
all six directions. The best fit of the static tensor to the supplied
common-cone family `a H0+b J` has relative Frobenius residual **0.9933**.
Thus this named determinant neither selects a positive endpoint action
nor supplies a common electric/magnetic tensor. It does not exclude a
different filling, interaction, bare term or infinite-volume model.

The promised interacting calculation uses one up and one down fermion
with supplied on-site Hubbard U on that same 43-site patch. The full fixed
two-particle Hilbert space has dimension 1849. At U=2, the numerical
ground-state energy is `-4.7669491621`, and the sampled lowest Ritz gap
is `0.0525006`. The relative best-fit residual is **0.5951** for the
static Hessian against `a H0+b J`; the residual between static and
electric tensors after optimizing one common scale is **0.6853**. U=0
and U=8 controls are also recorded. These are basis-dependent diagnostics
in the declared six-flux coordinates, not universal physical constants.

Both response tensors use the **same interacting Hamiltonian and ground
state**. Their projected-resolvent residuals are below `4e-11`; the
combined pure-gauge/current-density Ward residual is below `2e-13`;
independent finite differences of the actual ground energy check two
flux directions. The Ritz gap is numerical, not a certified infinite-volume
mass gap. The sector is neither all Fock sectors nor the canonical E6
matter regulator, and the gauge field is external rather than dynamical.
These are finite-patch loop-flux coefficients; they do not by themselves
give the nonzero-spatial-momentum Maxwell polarization tensor.

Reflection alone had already been shown in the prior work to send
`H(theta)` to `H(-theta)`, fixing theta=0 if reflection is imposed within
that family. The present matter computations do not derive the missing
physical selector or an interacting E6 effective action.

## 12344. Reflection projection and a chiral anomaly constraint

At `(1,1,omega,omega^2)`, the actual 135-link reflection lift squares to
the identity and intertwines vertex and edge gauge transformations, exactly
over Q(omega). Its **unprojected** mixed curl has one nongauge null direction.
Imposing either even or odd edge parity at this particular fixed character
removes that line after quotienting the correspondingly invariant vertex
gauges: joint ranks are120 and123; vertex parity-constraint ranks are12 and15.

This is a constrained linear calculation at one momentum. The selected
short-face action is not itself reflection-invariant, and the result is not
a constructed orbifold, proof of global parity-sector ellipticity, or a
selection of Lorentzian time.

There is a separate necessary charge check. In the canonical branching

```
27 = (10_(1,1) + bar5_(-3,1) + 1_(5,1))
     + (5_(-2,-2) + bar5_(2,-2)) + 1_(0,4),
```

the first parenthesis is a chiral16, with subscripts `(Q_chi,Q_psi)`.
Using left-handed Weyl conventions and `2T(5)=1, 2T(10)=3`, a spectrum
consisting only of that16 has

```
SU(5)^3 = 0,
SU(5)^2 U(1)_psi = 4,
gravity^2 U(1)_psi = 16,
U(1)_psi^3 = 16,
U(1)_chi^2 U(1)_psi = 80.
```

The complementary10 and1 cancel all of these in the complete27. Hence,
**if** a proposed reduction keeps only the16 while leaving U(1)_psi
gauged, it must supply compensating states or an anomaly-cancellation
mechanism. The calculation does not prove which modes the native theory
keeps or compute fixed-plane anomalies. The distinction matters: examples
of orbifold theories with vanishing integrated anomalies but localized
anomalies are known; see [Scrucca et al.](https://arxiv.org/abs/hep-th/0110073).

## 12345. What the truncated radius potential actually establishes

The Pass12335 potential is a **truncated** integral: integer-tower
coefficient -222, half-tower massless coefficient +288, and a 16-state
half-tower internal-tachyon coefficient -16. Massive internal levels and
some winding projections are not included. Its finite samples cannot prove
a minimum is absent in the complete string potential.

For each retained mode, write

```
a(R)=pi [n^2/R^2 + w^2 R^2 + 4 ell],
lo(x)=sqrt(1-x^2),
integral_lo^infinity dt exp(-a t)/t^3 = E3(a lo)/lo^2.
```

Thus the tau2 integral can be done analytically and the radius derivative
obtained from E2; only the remaining angular quadrature and integer mode
sums are numerical. Direct two-dimensional quadrature independently
checks this reduction. With larger converged mode and angular cutoffs,

```
R=0.4:      V=-250.3397110596,  V'=629.1184671907
R=sqrt(3/8): V=-164.8568360767, V'=165.7460351513  (left derivative)
```

The derivative is positive at **201 sampled radii** between0.1 and the
edge. This is numerical evidence, not an interval proof of monotonicity.
The previous finite-cutoff value at R=0.4 was `-251.0792897003`.
Reintegrating that same T=40 and n,w<=8 model exactly in tau2 gives
`-251.0666651319` with the previous endpoint-counting rectangular angular
sum, but `-250.2703360596` with Gauss angular integration. The difference
primarily comes from counting both angular endpoints with full rectangle
weights; the remaining finite-time discretization and cutoff effects are
separately visible. This corrects the stated numerical integral, not the
qualitative sampled trend.

There is also a precise threshold effect. For the n=+/-1/2,w=0 internal
tachyon pair let `a=pi/(4R^2)-2pi/3`. As a tends to zero from above, this
pair has finite value and first derivative, but

```
V''_pair = -(4096 pi^2 / 27) log(1/a) + O(1) -> -infinity.
```

The coefficient follows from the two momentum states, multiplicity16,
`a'(R)=-pi/(2R^3)` and `R^2=3/8`; it is exact in the stated normalization.
Numerical controls of the regularized second derivative are in the JSON.
This nonanalyticity is a threshold property of the retained contribution,
not proof of a stabilized or destabilized full vacuum. As R tends to zero,
the same truncated model has `V ~ -C/R`, where
`C=(444/5) integral_(-1/2)^(1/2) (1-x^2)^(-5/4) dx`.

The broader literature allows additional one-loop contributions, including
model-dependent D-term effects; see [Diaz Avalos et al.](https://arxiv.org/abs/2306.16878).
We have not constructed the complete modular-invariant partition function,
computed the omitted winding projections, or established the actual radius
potential of this model.

## Validation, parallel work and reading status

Ten focused tests pass for this packet, including all81 period-three actual
Bloch matrices, nearby real-torus samples, parity/gauge intertwining, a
second independent interacting finite difference, direct two-dimensional
string quadrature, and the symbolic threshold coefficient. All five tests
of the parallel 12-term repair also pass. Every new result is generated by
the committed producers; the previous 729 full patches are archived and
hash-verified, not fully read. The current 210-page PDF edition has SHA256
`c813e604f3cb2c8fc6f6417f85e7ed96a2eeb8faa191d7ccbc6b869d21e3f9a5`;
pages20–25 were read in full this continuation, in addition to the prior
complete-page record. Full paper and two-week semantic diff reading remain
unfinished. The source workstation remained offline; calculations ran on
the server.
