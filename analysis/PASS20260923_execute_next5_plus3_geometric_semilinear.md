# 2026-09-23 — Five more attacks + three outside-box physics probes

This pass starts from the geometric Hodge, full-similitude, E8 Kramers no-go,
FI-clock, and p=5 likelihood frontier and executes the five independent attacks
queued there.

Executable witness:

- `analysis/w33_20260923_execute_next5_plus3_geometric_semilinear.py`

Frozen certificate:

- `data/w33_20260923_execute_next5_plus3_geometric_semilinear_frozen.json`

Regression:

- `tests/test_w33_20260923_execute_next5_plus3_geometric_semilinear.py`

Remote Desktop Commander was explicitly requested.  The registered device
`TheHeavyCrown` was offline for this pass, and its ping returned that no remote
device was available.  The finite calculations were therefore executed in the
ChatGPT analysis runtime and frozen for later local replay rather than being
misreported as remote execution.

## 1. The exact geometric Hodge star changes the spectrum but not the 81-dimensional topology

The previous pass geometrized the clique complex using the rank-24 spherical
embedding and obtained the exact circumcentric Hodge weights

[
w_0=rac{5sqrt{30}}{108},
qquad
w_1=rac{sqrt{30}}{72},
qquad
w_2=rac{sqrt{30}}{15},
qquad
w_3=rac{18sqrt{30}}{25}.
]

Only weight ratios enter the cochain adjoints:

[
oxed{
rac{w_1}{w_0}=rac3{10},
qquad
rac{w_2}{w_1}=rac{24}{5},
qquad
rac{w_3}{w_2}=rac{54}{5}.
}
]

For scalar weights in each cochain degree,

[
d_k^dagger
=
rac{w_{k+1}}{w_k}d_k^{mathsf T}.
]

The unweighted W33 Hodge decomposition was already exact:

- on (operatorname{im}d_0), (d_0d_0^{mathsf T}) has
  (10^{24}+16^{15});
- on (operatorname{im}d_1^{mathsf T}),
  (d_1^{mathsf T}d_1=4) with multiplicity (120);
- (d_2d_2^{mathsf T}=4I_{40});
- (b_1=81).

Therefore the **geometric** weighted spectra are now

[
oxed{
L_0:
quad
0^1,;3^{24},;(24/5)^{15},
}
]

[
oxed{
L_1:
quad
0^{81},;3^{24},;(24/5)^{15},;(96/5)^{120},
}
]

[
oxed{
L_2:
quad
(96/5)^{120},;(216/5)^{40},
}
]

and

[
oxed{
L_3:
quad
(216/5)^{40}.
}
]

Across the complete de Rham/Dirac carrier,

[
oxed{
D^2:
quad
0^{82},
;3^{48},
;(24/5)^{30},
;(96/5)^{240},
;(216/5)^{80}.
}
]

Thus

[
D:
quad
0^{82}
]

together with symmetric pairs

[
pmsqrt3^{,24},
quad
pmsqrt{24/5}^{,15},
quad
pmsqrt{96/5}^{,120},
quad
pmsqrt{216/5}^{,40}.
]

### Maxwell consequence

For a 1-cochain gauge field (A),

[
C^1
=
operatorname{im}d_0
oplus
H^1
oplus
operatorname{im}d_1^dagger
]

with dimensions

[
39+81+120=240.
]

After quotienting the (39) exact gauge directions, the geometric Maxwell
carrier has

[
oxed{81}
]

zero harmonic/topological modes and one coexact band of

[
oxed{120}
]

modes at

[
oxed{lambda_{m Maxwell}=96/5}.
]

So metricization does **not** destroy the 81-dimensional topological sector.
It cleanly separates it from a single finite coexact photon band.

This is a finite dimensionless spectrum until a physical length/energy scale
is independently supplied.

## 2. The full-similitude construction closes for every odd prime power

Let (q=p^f) be any odd prime power and let (H_q) be the finite Heisenberg
group.  For each nonzero (tinmathbb F_q^	imes), let

[
mathcal H_t
]

be the (q)-dimensional Schrödinger irrep with center character

[
chi_t(z)
=
expleft(
rac{2pi i}{p}
operatorname{Tr}_{mathbb F_q/mathbb F_p}(tz)
ight).
]

Define

[
oxed{
mathcal H_{m full}
=
igoplus_{tinmathbb F_q^	imes}mathcal H_t,
qquad
dimmathcal H_{m full}=q(q-1).
}
]

On basis (|t,xangle),

[
X_u|t,xangle
=
|t,x+uangle,
]

[
Z_v|t,xangle
=
chi_t(vx)|t,xangle.
]

The ordinary Weil Fourier and quadratic-phase operators act blockwise in
(t).  A determinant similitude (ainmathbb F_q^	imes) acts by

[
oxed{
D_a|t,xangle
=
|a^{-1}t,xangle,
}
]

which implements

[
(u,v,z)
mapsto
(u,av,az).
]

For nonprime fields, Frobenius extends the construction semilinearly:

[
oxed{
U_sigma|t,xangle
=
|t^p,x^pangle.
}
]

Hence the same (q(q-1))-dimensional carrier realizes the full

[
H_q:Gamma L(2,q)
]

action.

### Exact Heisenberg character

Because the restriction contains every nontrivial central-character
Schrödinger irrep exactly once,

[
oxed{
chi(1)=q(q-1).
}
]

For a nontrivial central element (z),

[
sum_{t
e0}chi_t(z)=-1,
]

hence

[
oxed{
chi(0,0,z
e0)=-q.
}
]

Every noncentral Heisenberg element has trace zero:

[
oxed{chi(u,v,z)=0quad	ext{if }(u,v)
e(0,0).}
]

That is the complete restricted (H_q) character.

### The commutant collapses exactly

Restricted to (H_q), the (q-1) summands are pairwise inequivalent and
multiplicity-free.  Therefore

[
oxed{
dimoperatorname{End}_{H_q}
(mathcal H_{m full})
=q-1.
}
]

The commutant is just the diagonal algebra assigning one scalar to each center
character.

But determinant similitudes act transitively on those (q-1) sectors.
Anything commuting with the full action must therefore assign the same scalar
to every sector:

[
oxed{
operatorname{End}_{H_q:GL(2,q)}
(mathcal H_{m full})
=
mathbb C.
}
]

Frobenius does not enlarge the commutant, so also

[
oxed{
operatorname{End}_{H_q:Gamma L(2,q)}
(mathcal H_{m full})
=
mathbb C.
}
]

Thus the full carrier is irreducible.

### Minimality and uniqueness

The determinant map

[
GL(2,q)	woheadrightarrowmathbb F_q^	imes
]

moves any faithful center character through all (q-1) nontrivial
characters.  Finite Stone--von Neumann uniqueness makes the corresponding
Schrödinger irreps inequivalent.  Consequently any unitary representation
that contains one faithful Schrödinger sector and realizes every similitude
must have

[
oxed{
dimmathcal Hge q(q-1).
}
]

The construction attains the bound.

At minimal dimension, every nontrivial character sector occurs exactly once,
so the sector content is unique.  Weil-lift phase conventions or characters
of an external quotient may still modify phases without changing that forced
content.

Again,

[
q(q-1)=2q
iff
oxed{q=3}.
]

Only the qutrit needs no center-character sectors beyond the ordinary
charge-conjugate pair.

Finite-field Weil representations are precisely the standard mathematical
interface for the Heisenberg/Schrödinger and symplectic part of this
construction; the new W33-specific point is the all-character similitude
completion and its qutrit saturation.

## 3. Anti-linear E8 symmetries compatible with the physical Z3 grading

Let

[
C=Z_{m FI}
]

denote the physical grading automorphism

[
C:
quad
mathfrak g_0mapstomathfrak g_0,
quad
mathfrak g_1mapstoomegamathfrak g_1,
quad
mathfrak g_2mapstoomega^2mathfrak g_2.
]

The repo already supplies two exact operations.

### Coefficient conjugation K

Because the source Chevalley structure constants are integral, ordinary
coefficient conjugation is an anti-linear Lie automorphism:

[
K^2=1.
]

It preserves each grade label but reverses the complex grading phase:

[
oxed{
KCK^{-1}=C^{-1}.
}
]

### Root opposition theta and the certified real involution J

The exhaustive Chevalley certificate proves

[
	heta(h_i)=-h_i,
qquad
	heta(e_alpha)=e_{-alpha}
]

is a complex-linear Lie automorphism.  It exchanges the two matter grades and

[
	heta C	heta^{-1}=C^{-1}.
]

The already-certified split real structure is

[
J=	heta K.
]

Because both (	heta) and (K) invert (C),

[
oxed{
JCJ^{-1}=C
}
]

and

[
J^2=1.
]

### Full normalizer statement

Any anti-linear automorphism (A) normalizing the grading subgroup
(langle Cangle) becomes a **linear** normalizer after composition with
(K).

The linear normalizer maps to

[
operatorname{Aut}(C_3)cong C_2.
]

Its kernel is the grade-zero centralizer (G_0), while (	heta) realizes the
nontrivial inversion.  Therefore

[
oxed{
operatorname{AntiNorm}(langle Cangle)
=
G_0K
;sqcup;
G_0J.
}
]

So, modulo arbitrary continuous grade-zero dressing, there are exactly two
anti-linear normalizer classes:

1. grade-preserving (K)-type;
2. grade-exchanging (J)-type.

### Complete neutral-fixed scalar subclass

Now impose the more restrictive condition used by the finite compiler:
the neutral action is held fixed and only scalar phases may decorate the two
irreducible matter grades.

Write the matter phases as (alpha,eta).  Bracket closure gives

[
[mathfrak g_1,mathfrak g_1]subsetmathfrak g_2
quadLongrightarrowquad
eta=alpha^2,
]

and

[
[mathfrak g_1,mathfrak g_2]subsetmathfrak g_0
quadLongrightarrowquad
alphaeta=1.
]

Hence

[
oxed{alpha^3=1}.
]

There are therefore exactly six such anti-linear maps:

[
K,quad CK,quad C^2K,
]

all grade-preserving involutions with square (1), and

[
J,quad CJ,quad C^2J.
]

Their squares are

[
oxed{
J^2=1,
qquad
(CJ)^2=C^2,
qquad
(C^2J)^2=C.
}
]

The last two have exact order (6).

No member produces the forbidden Kramers square (-I) on both matter grades.
The prior 1620-bracket no-go is therefore not an accident: the compatible
nontrivial square is the physical (Z_3) center, not a uniform minus sign.

## 4. FI-center gate synthesis collapses from eight mixers to zero

The previous compiler implemented four explicit G25 Floquet ticks:

[
U_F^4=omega I_3.
]

Expanding those ticks costs

[
8
]

(F_3/F_3^dagger) traversals plus

[
12
]

selective ternary phase masks.

That is the correct circuit when the **purpose is to test the relation**
(U_F^4=omega I).

It is not the optimal circuit when the **purpose is simply to implement the
already-certified target**.

Because the target is scalar on the family qutrit, put the qutrit signal in
one arm of a phase-referenced interferometer and apply a uniform

[
oxed{+120^circ}
]

phase to that arm.

The exact synthesized operation is then

[
oxed{
0 F_3	ext{ traversals}
+
1	ext{ relative phase operation}.
}
]

Zero is the absolute mixer-count lower bound, so the result is globally
optimal under any nonnegative mixer cost.

If the complete E8 grade (0/1/2) is represented explicitly as a control
trit, the same center is simply

[
oxed{
operatorname{diag}(1,omega,omega^2),
}
]

again one diagonal grade-phase operation and no mixer.

This eliminates the earlier accumulated (F_3)-leakage problem for **using**
the FI-center operation.

It does not eliminate the long circuit from an experiment that claims to
**verify why** four G25 ticks equal that center.  Such a test should interfere
or tomographically compare the 20-primitive path with the compressed
one-phase reference.

The repo's existing `GLOBAL_FRAME_PHASE` was deliberately bookkeeping-only
on an isolated qutrit.  Turning it into an observable operation therefore
requires a reference/control arm and a new measured calibration packet; the
optimization is exact algebraically but remains fail-closed as a device claim.

## 5. Sequential holonomy experiments at q=5, q=7, and q=9

The full multiplier obstruction is

[
mathbb F_q^	imes/{pm1}.
]

Its label entropy is

[
H_q
=
log_2rac{q-1}{2}.
]

Thus

[
H_5=1,
qquad
H_7=log_2 3approx1.585,
qquad
H_9=2.
]

A key question was whether experimental shot complexity follows this entropy.

It does not.

The sequential simulation uses the same nominal optical model as the previous
p=5 design:

[
V=0.965,
qquad
b=0.01,
]

with posterior stopping threshold equal to one minus the one-sided Gaussian
(5sigma) tail.

### q=5

Cosine interferometry already identifies (m) and (-m), exactly the
quotient needed.  There are two hypotheses.

Over 5000 deterministic-seed trials, the posterior test required

[
oxed{	ext{mean }22.58}
]

detected events,

with median (21), 95th percentile (37), and 99th percentile (46).

### q=7

One central probe again distinguishes the three quotient cosets

[
{pm1},quad
{pm2},quad
{pm3}.
]

The same sequential posterior criterion required

[
oxed{	ext{mean }50.53}
]

events,

with median (47), 95th percentile about (76), and 99th percentile (96).

### q=9 reveals a new finite-geometric structure

Write

[
mathbb F_9
=
mathbb F_3[alpha]/(alpha^2+1).
]

Because

[
mathbb F_3^	imes={pm1},
]

the obstruction quotient is

[
oxed{
mathbb F_9^	imes/{pm1}
=
mathbb F_9^	imes/mathbb F_3^	imes
=
mathbb P^1(mathbb F_3).
}
]

So the four obstruction labels are literally the **four projective
directions** in a two-dimensional ternary vector space.

A single additive-character interferometer cannot distinguish all four after
the cosine readout removes sign.  Three trace probes suffice:

[
z=1,
qquad
z=alpha,
qquad
z=1+alpha.
]

The four projective cosets then have distinct high/low signatures

[
oxed{
LHL,quad HLL,quad LLH,quad LLL.
}
]

Cycling the three probes gives mean stopping count

[
35.87.
]

Choosing at each shot the probe with maximum expected posterior entropy
reduction cuts that to

[
oxed{16.90}
]

events,

with median (15), 95th percentile (27), and 99th percentile (32).

No errors occurred in the 5000 simulated trials for any q.  That fact is only
an ordinary-power diagnostic; it is not used as a rare-tail significance
claim.

### Important negative result

The obstruction entropy increases

[
1
	o
1.585
	o
2	ext{ bits}
]

for (q=5,7,9).

But the simulated shot costs are approximately

[
22.6,
quad
50.5,
quad
16.9
]

for q5, q7, and adaptive q9.

Therefore

[
oxed{
	ext{experimental sample cost}

e
f!left(log_2rac{q-1}{2}ight)
	ext{ alone}.
}
]

The log-index is the entropy of the hidden symmetry label.  The number of
photons required to learn that label also depends on the KL geometry and
available measurement settings.

This is exactly the distinction expected in sequential hypothesis testing:
stopping efficiency is controlled by both hypothesis entropy and the
per-sample information provided by the measurement channel.

# Three additional outside-box physics probes

## A. Metricization produces an exact n² spectral ladder

The total geometric Dirac-square spectrum contains

[
rac{24}{5},
qquad
rac{96}{5},
qquad
rac{216}{5}.
]

But

[
oxed{
left{
rac{24}{5},
rac{96}{5},
rac{216}{5}
ight}
=
rac{24}{5}
{1^2,2^2,3^2}.
}
]

The multiplicities in (D^2) are

[
30,quad240,quad80.
]

There is also a separate (3^{48}) band.

Thus the exact circumcentric metric unexpectedly manufactures a three-rung
integer-square tower inside the finite Dirac spectrum.

This resembles the (n^2) spectral law of a compact one-dimensional momentum
tower, but no compactification interpretation is asserted.  At present it is
an exact finite spectral identity that deserves its own representation-theory
explanation.

## B. E8 contains exactly the minimal qutrit full-similitude family completion

The E8 matter sector is

[
(27,3)oplus(overline{27},overline3),
]

dimension

[
81+81=162.
]

The minimal qutrit full-similitude family carrier derived above has dimension

[
3(3-1)=6.
]

Therefore

[
oxed{
162
=
27	imes6
=
27	imes[3(3-1)].
}
]

More importantly, this is not merely numerology.

The certified H27/FI center acts as

[
omega
]

on ((27,3)) and

[
omega^2
]

on ((overline{27},overline3)).

Those are **exactly all nontrivial qutrit Heisenberg center characters**.

So the E8 matter/antimatter pair already contains the complete minimal family
carrier required to close full qutrit similitude symmetry:

[
oxed{
	ext{no missing center-character sector at }q=3.
}
]

For (q>3), ordinary matter/antimatter doubling would leave additional
central-character sectors missing.

This is an exact representation-content match.  It is not a claim that
observed Standard Model matter is thereby derived.

## C. A Z3-valued anti-linear square replaces the failed Kramers square

The Kramers attempt asked for

[
T^2=-1
]

and failed the exact E8 bracket.

But the anti-linear classification above supplies

[
oxed{
T_+=CJ,
qquad
T_+^2=C^2,
}
]

and

[
oxed{
T_-=C^2J,
qquad
T_-^2=C.
}
]

Since

[
C=Z_{m FI}
=
exp(2pi iQ_psi/3),
]

both (T_pm) have exact order six.

So E8 does admit a bracket-compatible **generalized anti-linear clock** whose
square is a nontrivial internal (Z_3) symmetry.

This is structurally much closer to a symmetry extension than ordinary
Kramers theory: the anti-linear generator does not square to a scalar minus
sign; it squares to a physical finite grading automorphism.

No identification with measured time reversal, CPT, degeneracy, or a
spacetime operation is made.  It is an exact semilinear Lie-algebra symmetry
and a concrete candidate algebraic structure for future dynamics.

# Net result

All five attacks closed sharply:

- the geometric Hodge metric preserves the 81-dimensional harmonic sector and
  produces an exact weighted Maxwell/Dirac spectrum;
- the full-similitude representation is now symbolic for every odd prime
  power, irreducible after sector permutation, and minimal;
- the anti-linear E8 grading normalizer is classified into two full cosets and
  six canonical neutral-fixed scalar twists;
- FI-center implementation compresses to zero mixers, while relation testing
  remains a separate long-path experiment;
- sequential q5/q7/q9 discrimination shows that the log-index is label entropy,
  not a universal photon-count law.

The three extra probes then connect those results to an exact (n^2) spectral
ladder, the complete E8 qutrit matter-sector saturation, and a new
(T^2=Z_3) anti-linear symmetry class.

## Evidence boundary

The weighted spectra are dimensionless finite data; no physical energy scale
has been derived.  The all-character representation does not imply extra
particles.  The six anti-linear maps are the neutral-fixed scalar subclass
inside continuous (G_0)-dressed normalizer families.  The compressed FI gate
does not replace a laboratory test of the four-tick identity.  The sequential
study is a nominal calibrated simulation, not experimental significance.
