# 2026-09-23 — Execute the five post-frontier attacks

This pass executes all five independent next attacks from the prior Wigner /
extended-Clifford / FI-clock frontier.  The strongest feature of the pass is
that it does not force every attack to succeed: one proposed Kramers extension
is killed exactly, and the current photonic leakage envelope fails sequence
admission.

Executable witness:

- `analysis/w33_20260923_execute_five_post_frontier_attacks.py`

Frozen certificate:

- `data/w33_20260923_execute_five_post_frontier_attacks_frozen.json`

Regression:

- `tests/test_w33_20260923_execute_five_post_frontier_attacks.py`

## 1. The doubled Hodge carrier acquires an exact geometric metric

Let (A) be the W33 adjacency matrix.  The primitive idempotent for the
adjacency eigenvalue (r=2) is

[
E_2=rac{1}{6}
left(
A+4I-rac{16}{40}J
ight).
]

Since (operatorname{rank}E_2=24), normalize the corresponding spherical
embedding to unit vectors.  Its exact Gram matrix is

[
oxed{
G=rac{5A+20I-2J}{18}.
}
]

Hence

[
G_{ii}=1,
qquad
G_{ij}=
egin{cases}
1/6,&isim j,\
-1/9,&i
otsim j.
end{cases}
]

The transvection generators were rebuilt directly and the orbit of one edge
has size (240), equal to the entire edge set.  Therefore an
(operatorname{Aut}(W33))-invariant edge metric has exactly one free scale.

With the spherical normalization,

[
a^2=2-2(1/6)=oxed{rac53}.
]

Every (K_4) clique-line is therefore a regular tetrahedron of edge length

[
a=sqrt{rac53}.
]

The clique incidence census is especially rigid:

[
oxed{
4	ext{ tetrahedra/vertex},
qquad
1	ext{ tetrahedron/edge},
qquad
1	ext{ tetrahedron/triangle}.
}
]

For a regular tetrahedron, the primal measures are

[
|e|=a,qquad
|f|=rac{sqrt3}{4}a^2,qquad
|T|=rac{a^3}{6sqrt2}.
]

The corresponding local circumcentric dual measures are

[
|*v|=|T|,
qquad
|*e|=rac{sqrt2}{24}a^2,
qquad
|*f|=rac{sqrt6}{12}a,
qquad
|*T|=1.
]

At (a^2=5/3), the diagonal DEC Hodge weights are therefore

[
oxed{
left(
rac{5sqrt{30}}{108},
rac{sqrt{30}}{72},
rac{sqrt{30}}{15},
rac{18sqrt{30}}{25}
ight).
}
]

All are strictly positive.

This advances the previous formal (Koplus K^ee) construction: there is now
an exact (operatorname{Aut}(W33))-invariant piecewise-Euclidean geometry
whose simplexwise circumcentric star has positive volume ratios.

There is also a clean boundary.  W33's clique complex is not a 3-manifold.
Each triangle has one tetrahedral coface rather than two, and the dual
three-cell at a vertex is a branched union of four tetrahedral Voronoi pieces.
So the result is a genuine positive piecewise-Euclidean circumcentric metric on
the abstract simplicial complex, not a proof that W33 triangulates a smooth
three-manifold.

This distinction matches the DEC literature: circumcentric Hodge stars are
ratios of dual/primal volumes, and positivity is tied to appropriate
well-centered/Delaunay geometry.  Our regular tetrahedra satisfy the local
positivity condition; global manifold topology does not magically follow.

## 2. Full similitudes are explicitly unitarized at q=5 and q=9 — minimally

For each nonzero central character (tinmathbb F_q^	imes), let

[
mathcal H_tcongmathbb C^q
]

be its Schrödinger representation.  Work on

[
mathcal H_{m full}
=
igoplus_{tinmathbb F_q^	imes}mathcal H_t,
qquad
dimmathcal H_{m full}=q(q-1).
]

Use basis states

[
|t,xangle,
qquad
tinmathbb F_q^	imes, xinmathbb F_q.
]

The global Weyl operators are

[
X_u|t,xangle=|t,x+uangle,
]

[
Z_v|t,xangle
=
psi(tvx)|t,xangle.
]

Three explicit generators suffice for the witness.

### Fourier generator

On each fixed (t),

[
S|t,xangle
=
rac1{sqrt q}
sum_ypsi(txy)|t,yangle,
]

giving

[
(u,v,z)mapsto(-v,u,z).
]

### Chirp generator

[
N|t,xangle
=
psi!left(rac{t x^2}{2}ight)|t,xangle,
]

giving

[
(u,v,z)mapsto(u,v+u,z).
]

### Determinant similitude

For primitive (ainmathbb F_q^	imes),

[
oxed{
D_a|t,xangle
=
|a^{-1}t,xangle.
}
]

This is literally a permutation of central-character sectors, and it gives

[
(u,v,z)mapsto(u,av,az),
]

so its symplectic multiplier is (det D_a=a).

The full matrices were materialized and their covariance checked.

For (q=5):

[
oxed{dim=20},
]

the determinant-sector cycle has length (4), and the maximum numerical
covariance residual over the generator checks is approximately

[
1.4	imes10^{-15}.
]

For (q=9=mathbb F_3[alpha]/(alpha^2+1)):

[
oxed{dim=72},
]

(1+alpha) has multiplicative order (8), the sector cycle has length (8),
and the maximum covariance residual is approximately

[
5.8	imes10^{-15}.
]

The dimension is not merely sufficient; it is necessary.

Because

[
det:GL(2,q)	woheadrightarrowmathbb F_q^	imes
]

is surjective, the determinant similitudes act transitively on all
(q-1) nontrivial center characters.  Finite Stone--von Neumann uniqueness
makes the corresponding (q)-dimensional Schrödinger irreps inequivalent.
Therefore any unitary extension containing one faithful central-character
sector must contain their entire orbit:

[
oxed{
dimmathcal Hge q(q-1).
}
]

The construction above attains the bound.

This sharpens the qutrit result:

[
q(q-1)=2q
iff
oxed{q=3}.
]

Only at (q=3) does an ordinary conjugate pair already have enough sectors to
unitarize every similitude.

## 3. The 162-dimensional Kramers idea fails as an E8 bracket symmetry

The proposed doubled antiunitary has

[
T^2=A,
]

where (A) acts as

[
+Iquad	ext{on }mathfrak g_0,
qquad
-Iquad	ext{on }mathfrak g_1oplusmathfrak g_2.
]

If (T) were either a Lie automorphism or a Lie anti-automorphism, (T^2)
would have to be a linear Lie automorphism.

But for any nonzero

[
[x,y]in[mathfrak g_1,mathfrak g_1]subsetmathfrak g_2,
]

one gets

[
A[x,y]=-[x,y]
]

while

[
[Ax,Ay]=[-x,-y]=[x,y].
]

So (A) cannot preserve the bracket.

The committed exact E8 structure table makes the obstruction quantitative:

[
oxed{
810	ext{ nonzero }mathfrak g_1mathfrak g_1	omathfrak g_2
	ext{ pairs},
}
]

[
oxed{
810	ext{ nonzero }mathfrak g_2mathfrak g_2	omathfrak g_1
	ext{ pairs},
}
]

for

[
oxed{1620}
]

exact sign violations of the proposed square.

The first frozen witness is source-basis indices

[
(a,b;k)=(10,167;20)
]

with coefficient (-1) and grades

[
(1,1;2).
]

Therefore the quaternionic (T^2=-1) construction may still be imposed on a
state-space Hamiltonian that does not claim to preserve the E8 Lie product, but
it **cannot** be promoted to an E8 bracket symmetry.  The existing certified
anti-linear real involution (J^2=+1) remains the compatible Lie-algebra
structure.

## 4. Four Floquet ticks lower to an exact Holonet pulse word — but hardware admission fails closed

In the canonical qutrit labels (0,1,2),

[
R_1=operatorname{diag}(1,1,omega),
]

[
R_3=operatorname{diag}(1,omega,1),
]

and

[
R_2=F_3operatorname{diag}(omega,1,1)F_3^dagger.
]

Thus for

[
U_F=R_1R_2R_3,
]

one right-to-left physical tick is

1. (+120^circ) phase on label (1);
2. (F_3^dagger);
3. (+120^circ) phase on label (0);
4. (F_3);
5. (+120^circ) phase on label (2).

The repository's centered OAM basis is

[
(ell=-1,0,+1)
leftrightarrow
(2,0,1),
]

so the phase masks physically sweep

[
ell=+1, 0, -1.
]

Exact matrix multiplication gives

[
|U_F^4-omega I|<2	imes10^{-15},
qquad
|U_F^{12}-I|<6	imes10^{-15}.
]

Four ticks require

[
oxed{8}
]

(F_3/F_3^dagger) traversals and

[
oxed{12}
]

ternary phase masks.  Adjacent diagonal masks can be merged, reducing the raw
20 primitive operations to

[
oxed{17}
]

hardware layers.

### The readout issue

Because

[
U_F^4=omega I
]

is a global phase on an isolated qutrit, direct projective qutrit measurement
cannot see it.  A valid FI-center readout therefore needs a bypass/reference
arm or a controlled-(U_F^4) Ramsey construction.  The signal arm should
acquire a relative

[
oxed{120^circ}
]

phase.

A sufficient nearest-(Z_3) classification condition is total coherent phase
error below (60^circ).  Splitting that budget evenly between the 12 phase
masks and 8 Fourier traversals gives the simple sufficient bounds

[
epsilon_{m mask}<2.5^circ,
qquad
epsilon_{F_3}<3.75^circ,
]

or, more generally,

[
oxed{
12epsilon_{m mask}+8epsilon_{F_3}<60^circ.
}
]

### Sequence-level leakage exposes the real bottleneck

The repo's current engineering envelopes are

[
eta_{F_3}le0.10,
qquad
eta_Zle0.02.
]

If those maxima were interpreted as independent per-traversal leakage and all
were saturated, four-tick survival would be only

[
(0.9)^8(0.98)^{12}
=
oxed{0.3378}.
]

So those single-gate envelopes absolutely do **not** certify the complete
sequence.

For (90%) total survival, a uniform 20-primitive leakage budget would require

[
oxed{eta<0.00525}
]

per primitive.  If phase masks were ideal, the eight Fourier traversals alone
would require

[
eta_{F_3}<0.0131.
]

If Fourier gates were ideal, the twelve masks would require

[
eta_{m mask}<0.00874.
]

The pulse compiler is therefore exact but the device admission result is

[
oxed{	ext{FAIL CLOSED}.}
]

This agrees with the repository's independent FI-clock falsifier: an internal
finite (C_{12}) identity is not evidence for physical time, and an
implementation claim requires measured transfer matrices, phase stability,
loss and reproducibility.

## 5. The p=5 falsifier now has a nuisance-profiled exact likelihood

The earlier (N=128) estimate used a conservative Gaussian separation proxy.
This pass replaces it with a two-port count model.

Let

[
p(phi,V,b,delta)
=
rac{
1+V(1-b)cos(phi+delta)
}{2}.
]

Independent Poisson counts in the two output ports, with an unknown common
rate, profile exactly to the corresponding binomial likelihood conditioned on
the total detected count.

The two phase hypotheses are

[
H_A:phi=rac{2pi}{5},
qquad
H_F:phi=rac{4pi}{5}.
]

The calibration nuisance model is

[
V=0.965pm0.005,
]

[
b=0.010pm0.002,
]

[
delta=0pm1^circ,
]

with a Gaussian profile penalty and a full (pm3sigma) grid of

[
oxed{2873}
]

nuisance points.

Across that box,

[
p_Ain[0.620972, 0.674898],
]

[
p_Fin[0.090695, 0.136762].
]

For each detected total (N), the penalized profile-likelihood ratio is
monotone in the reference-port count (k), producing an exact threshold rule.

At

[
N=87,
]

the rule is

[
oxed{kge31Rightarrow H_A}.
]

The nominal misclassification probabilities are

[
8.97	imes10^{-9},
qquad
2.79	imes10^{-9}.
]

More importantly, the exact worst tails over the full declared (3sigma)
nuisance box are

[
oxed{
1.70	imes10^{-7},
qquad
2.15	imes10^{-7}.
}
]

Both are below the one-sided Gaussian (5sigma) tail

[
2.8665	imes10^{-7}.
]

An exhaustive search over (60le Nle100) finds

[
oxed{N_{min}=87}.
]

So the old (128)-event design was conservative.

At (N=128), the decision threshold is (kge45), and the two worst declared
nuisance-box tails fall to approximately

[
2.03	imes10^{-10},
qquad
7.47	imes10^{-10}.
]

A deterministic 100,000-trial-per-hypothesis nuisance-marginalized Monte Carlo
was also run at (N=32,48,64,87,128).  It is used only as an ordinary-power
cross-check.  In particular, zero errors in (10^5) trials only support a
rough (3	imes10^{-5}) 95% rule-of-three bound; the (5sigma) conclusion
comes from the exact binomial tails, not from Monte Carlo extrapolation.

## Net result

The five attacks did not all move in the same direction:

- **Hodge geometry:** strengthened.  The formal dual now has a canonical
  invariant regular-tetrahedral metric and positive circumcentric weights.
- **Full similitudes:** strengthened.  Explicit (q=5) and (q=9) unitary
  matrices attain a proved minimal dimension (q(q-1)).
- **Kramers/E8:** killed.  (T^2=-1) cannot preserve the E8 bracket.
- **FI pulse compiler:** algebraically closed, physically fail-closed under the
  current sequence-level leakage envelope.
- **p=5 falsifier:** statistically strengthened.  The stated nuisance model
  lowers the conservative detected-event target from 128 to 87.

## External interfaces used

- Desbrun--Hirani--Leok--Marsden, *Discrete Exterior Calculus*.
- Hirani--Kalyanaraman--VanderZee, *Delaunay Hodge Star*.
- finite Stone--von Neumann / Weil representation theory over finite fields.
- integrated high-dimensional photonic processors using multiports and
  programmable phase shifters.
- standard Poisson/binomial likelihood profiling and calibrated nuisance
  treatment.

## Hard boundary

No result here derives a smooth spacetime, physical E8 Hamiltonian, observed
new central-character particles, fabricated FI-clock device, or laboratory
significance.  The metric is piecewise Euclidean on a non-manifold complex,
the (T^2=-1) E8 extension is explicitly false, the optical sequence currently
fails device admission, and the (p=5) likelihood is a preregisterable design
calculation rather than measured evidence.
