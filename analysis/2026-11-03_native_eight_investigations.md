# Eight executed investigations: native dynamics, symmetry and quantum control

This packet follows `df1e1402c` and executes the five requested investigations,
then three additional investigations of gauge consistency, quantum geometry and
measurement holonomy. Every front supplies a runnable producer and JSON. Exact
finite results, conditional field theory and numerical controls are separated.
The packet does not establish a complete physical TOE.

## Intake and ownership

The two intervening published packets were read: the November3 q9/phase-mask/
module/Albert/Bloch report, and `PASS12527_12533_FRAMES_KNOTS_MERMIN_BURKHARDT.md`.
Their q9 tensor, phase-only tomography, three-voltage continuum controls,
Burkhardt and Jones results are not reproduced or claimed here. The newly
available q5 orthonormal-frame description directly informs investigation2.

The native projector tensor, unique chiral completion, 810 quartets and 9,720
ground states come from the October31/November1/2 tick work. The previous
Clifford/cubic action, induced common cover and conditional classical vacuum
come from the November2 packet. Per decision
`343ae948-2d2e-4380-a966-c24c33030909` (CLI, `induced324_cover_producer`), the
324-coordinate carrier preserves the old27 action on its reference block;
investigation3 retains that contract.

The full original weekly patch/PDF reading audit is not represented as completed
by this packet. The parallel PDF text-coverage audit is a separate artifact.

| Front | Concrete result | Producer stem after `w33_20261103_` |
|---|---|---|
| 1. Vacuum stability | Exact17-parameter F-flat chart; conditional Sp4 ADS obstruction | `vacuum_effective_quantum_audit` |
| 2. W(D5) map | Actual native word, Klein bijection, q5 hyperoval and Clebsch actions | `wd5_native_klein_intertwiner` |
| 3. Common carrier | 324 to313 homogeneous cubic coordinates, faithful kernel retained | `induced_cubic_compression` |
| 4. All quartets | Exact9,720-state leading tunneling graph and positive order12 coefficient | `all_quartet_tunneling` |
| 5. Cocycle selection | Four A4-invariant classes; two non-Abelian choices; no canonical selection | `deck_cocycle_symmetry_selection` |
| Additional A | Global gauge form, anomalies, vacuum topology and perturbative cancellation | `gauge_global_form_audit` |
| Additional B | Native Yang-bundle charge, noncommuting loops and covariance obstruction | `clifford_yang_monopole_controls` |
| Additional C | Exact postselected logical qutrit Clifford group, including scalar kernel | `native_projector_holonomic_qutrit` |

## 1. The classical vacuum is an exact flat chart, but quantum stability fails a conditional test

The previous vacuum was a checked F/D-flat family under supplied4D N=1 SU4
gauging, canonical Kahler potential and the native cubic superpotential. It had
not been shown isolated or quantum stable. The next calculation improves the
classical statement and supplies a quantum warning with an actual mechanism.

Choose native coordinate x12 nonzero. The45 signed terms split into

```
W = x12 * Q(V10) + sum_i V_i B_i(S16).
```

The Hessian J of the nondegenerate quadratic Q is invertible. Solving the ten
F_V equations gives **V=-J^-1 B(S)/x12**. Substitution into all27 gradients
gives zero identically, and W itself vanishes identically. Thus x12 and the
sixteen S coordinates parametrize an exact **17-complex-dimensional open
F-flat chart** containing the previous vacuum. The rational coordinate map is
exported. This is the familiar exceptional cubic rank-one geometry realized in
the actual signed coordinates; it is not a new classification of that variety.

An independent SL6-coordinate Hessian calculation identifies eight charged
zero modes. Their USp4 Cartan weights are two copies of {a,b,-a,-b}: **two
fundamentals**, or Nf=1 in the convention where Sp(Nc) has2Nf fundamentals and
USp4 means Nc=2. Four neutral light chiral fields remain after the five complex
Goldstone directions and ten massive chiral directions are removed. The17
parameters are not17 gauge-invariant moduli.

Now assume the standard weakly Higgsed supersymmetric gauge dynamics. The
[Intriligator-Pouliot exact Sp superpotential](https://arxiv.org/abs/hep-th/9505006),
equation5, gives a nonzero term proportional to

```
Wdyn ~ (Lambda_low^8 / M)^(1/2),
```

for this Nc=2,Nf=1 theory. M is the meson. At fixed other moduli its derivative
with respect to M is nonzero at every finite nonzero M; M=0 is singular.
The exact flat chart supplies no stabilizing tree superpotential. Along the
one-scale Higgs branch, holomorphic threshold matching has the power law
Lambda_low^8=C*Lambda_SU4^9/t, up to a nonzero threshold/scheme constant.
With M=q², the hierarchical direction t=R*Lambda, q=sqrt(R)*Lambda has
q/t tending to zero and Wdyn proportional to1/R. It exhibits the effective
theory's runaway tendency while keeping the quark scale below the original
Higgs scale. Kähler metrics and strong-coupling endpoints are not computed.

Consequently the earlier **classical** candidate cannot be promoted to a
selected stable quantum vacuum on this evidence. This conclusion is conditional
on the stated gauge/SUSY assumptions and standard Sp dynamics; it is not a
global no-go for every vacuum of the native cubic or a physical SUSY claim.

## 2. An explicit native W(D5) -> q5 -> Clebsch dictionary

Pass12525 owns the q5 hyperoval stabilizer W(D5), and Pass12527 identifies its
20 points on Q(4,5) as the weight-two shell of an orthonormal five-frame.
BT3418-3429 already owns the Clebsch, half-spin and network correspondences.
The missing ingredient was a map from our actual native spinor matrices.

The new word in the seven native spinor generators is

```
[6,5,5,2,5,6,5,5,6]     (application order)
```

Its exact4x4 matrix fixes Omega. Together with the original six generators it
generates the full3,840-element finite spinor stabilizer, whose six-form image
has order1,920. Restrict that image to the five coordinates perpendicular to
iOmega. These are integral signed matrices, so reduction modulo5 is literal.

Independently construct all156 points and156 isotropic lines of W(3,5). The
Plucker coordinates of a line satisfy p02+p13=0. The explicit map

```
(3(p01+p23),4(p01-p23),3(p03+p12),4(p03-p12),p02) mod5
```

is a bijection to the156 projective null points of sum x_i²=0. The20 null
points of weight two correspond to20 selected W-lines, covering60 W-points
twice and leaving96 uncovered. Each chosen native generator induces exported
permutations of all156 lines and all156 points; every incidence is checked.
The complete native group has1,920 distinct actions on the20 selected lines.

For the Clebsch action, convert rotational signed R5 to even-sign
Q5=(-1)^parity(permutation)*R5. Act affinely on the sixteen even-weight
five-bit vectors; Hamming-four pairs are Clebsch edges. This again gives1,920
distinct actions. Thus the native group, the ambient q5 geometry and the
existing checksum network are connected by actual maps, rather than their
equal group orders. Finite-field reduction here is algebra, not physical
evolution from a complex Hilbert space into a finite-field spacetime.

## 3. A313-coordinate homogeneous carrier preserves the old local27

The previous324-dimensional induced module has coordinate orbits12,120,192.
Its60-dimensional diagonal sign kernel has one zero character repeated twelve
times, sixty nonzero characters repeated twice, and192 distinct characters.
The zero characters are precisely the twelve local scalar coordinates.

Identify these twelve scalars with one common scalar. The resulting
**313-dimensional carrier** still preserves a homogeneous cubic with540 terms.
All seven signed generators are exported, and the first six restrict exactly
to the original signed27 action on the reference subspace. Restricting the
cubic to that subspace returns exactly the original45 signed terms.

The sign kernel remains faithful and has rank60. Its restriction to the
120-coordinate orbit has rank48, whereas its restriction to the192-coordinate
orbit has rank60. Compression has not secretly quotiented the common cover.
Its order remains46,080*2^60.

There is a scoped obstruction to further group quotienting: a normal subgroup
of this cover's sign kernel acting trivially on the original reference27 must,
by conjugation, act trivially on every block. Faithfulness then forces it to
be trivial. This is not a minimal-degree theorem for all representations or a
no-go for differently constructed common covers.

## 4. All810 quartets participate in controlled torus tunneling

Use the declared face-count H0 on the16-site torus and the **full120-state**
single-site driver -h*sum_v A(K120)_v. The native development theorem supplies
9,720 classical ground configurations, comprising twelve orientations of
each of810 quartets. No full120^16 matrix is materialized.

Two different native quartets share at most one label. Consequently every
distinct ground pair differs on twelve or sixteen sites, with exact counts

```
distance12: 1,555,200 pairs
distance16: 45,679,140 pairs.
```

Build M with9,720 rows and480 columns indexed by (parity slot,native label).
Each ground row has four incidences. For the Hamming12 graph A,

```
M M^T = 4I + A,
M^T M = 81I4 tensor I120 + (J4-I4) tensor N120.
```

The actual noncommutation graph satisfies N=B40 tensor J3, with
B40²=9I+18J. Thus M has rank477 and the complete graph spectrum is

```
320^1, 104^15, 86^72, 77^320, 68^45, 50^24, (-4)^9243.
```

For any Hamming12 pair, every hybrid face is maximal exactly when all its
changing vertices choose the same endpoint. This makes the leading path
denominators universal, both within and between quartets. Exact subset dynamic
programming sums all12!=479,001,600 shortest paths and gives

```
c = 19657590887 / 45916502400000 > 0.
H_eff = d(h) I - c*h^12*A + O(h^13).
gap = (19657590887/212576400000)*h^12 + O(h^13).
```

Native Clifford transitivity on the9,720 seed edges forces equal diagonal
effective energies for all ground configurations. Their common second- and
third-order coefficients are -952/3 and -56168/9. An independent small-resolvent
iteration tests the leading coefficient without repeating the rational DP.

This is a finite small-h result, not a large protected gap. The driver norm is
1,904, and |h|<1/3808 is a sufficient norm bound isolating the original ground
cluster. Normalizing each local driver by119 further rescales c by119^-12.
Thermodynamic stability and a calibrated physical coupling remain unresolved.

## 5. The cover constrains twists without selecting one

The actual meridians1,2,4,7 carry the oriented tetrahedral A4 action. Apply
this action to the128 standard classes of H3(C2³,U1)=C2^7. Their seven
diagonal values q(g)=omega(g,g,g) distinguish these representatives and are
unchanged by normalized U1 coboundaries.

Exactly four classes are A4-invariant. Their negative-q flux sets are the
empty set, {1,2,4,7}, {3,5,6}, and all seven nonzero fluxes. The first two
are Abelian64-sector theories. The latter two have22 sectors and spin counts

```
q-negative {3,5,6}: 1^12, (-1)^4, i^3, (-i)^3
q-negative all7:    1^8, i^7, (-i)^7.
```

These are standard twisted-double data, checked here against the native
symmetry. The earlier ordered omega=(-1)^(a0*b1*c2) distinguishes branch111
and has a four-element A4 orbit: **its class breaks that native symmetry**.
Moreover the tempting fully alternating phase (-1)^det(a,b,c) is trivial:
the producer exports an explicit two-cochain whose coboundary equals it.

Canonical deck maps fix the native projector labels and compose strictly;
their associator is1. A nontrivial gauge action therefore remains extra input.
Symmetry leaves two non-Abelian possibilities, rather than selecting the
earlier twist. Compare the established
[twisted-double classification](https://link.aps.org/accepted/10.1103/PhysRevB.91.035134).
The October26,2026 [AlgebrasTQD framework](https://arxiv.org/abs/2610.36029)
provides relevant tools for a future explicit interface/condensation analysis;
its code has not been substituted for the present finite checks. Matching
anyon counts or spin multiplicities alone does not identify a braided category.

## Additional A. Gauge global form and anomalies

The actual27 has SU4 center-charge multiplicities (0,1,2,3)=(5,8,6,8).
Only the identity central element acts trivially. Hence these fields require
SU4 rather than SO6 or PSU4. The remaining USp4 fundamentals likewise prevent
replacing that group by SO5 while retaining the same matter.

For general traceless Cartan H, the complete27 satisfies Tr H=Tr H³=0
and Tr27 H²=6 Tr4 H². This checks the full perturbative cubic anomaly by
polarization, fixes total Dynkin index3 and ultraviolet beta coefficient9.
The low-energy two-fundamental mod2 USp4 count is even. This is not an audit
of every possible discrete/background anomaly. Global gauge data matter
independently of Lie algebra names; see
[Aharony-Seiberg-Tachikawa](https://arxiv.org/abs/1305.0318).

The fixed-radius vacuum orbit is SU4/USp4=S5, with no pi1, pi2 or pi3 defects
from this breaking. Its H5 permits a Wess-Zumino term, but the zero UV cubic
anomaly does not force a nonzero coefficient. Massive supersymmetric multiplets
cancel in the one-loop potential supertrace, so perturbative vacuum energy
does not select the scale t. This complements, rather than replaces, the
nonperturbative analysis in front1.

## Additional B. A native Yang bundle, with two decisive controls

Pass4153 already owns the standard synthetic rank-two Yang projector on S4.
Using the **actual native five gamma axes**, the oriented volume product is
-I4. The exact Clifford trace gives C2=+1 and C1=0. Two controlled northern
square loops in different tangent planes have noncommuting SU2 Wilson matrices;
their commutator Frobenius norm converges to about0.00288292. An independent
full-space Kato polar transport checks the frame-overlap computation.

The enlarged Clifford gate sends four of the five Hermitian gamma axes outside
their span. Thus this S4 family is not covariant under the full enlarged group.
Also H4(S5)=0: its Chern number belongs to the supplied S4 control manifold,
not to the conditional vacuum's S5 orbit. These controls prevent promoting a
synthetic invariant to a physical spacetime monopole. The Yang-monopole
phenomenon itself is established, including
[experimental synthetic realizations](https://arxiv.org/abs/1610.06228).

## Additional C. Native degenerate projections implement a logical qutrit Clifford

For every one of9,720 ordered noncommuting projector pairs,

```
Pa Pb Pa = Pa/3.
```

These rank-three subspaces are isoclinic. At P0, whose support is computational
indices0,3,6, enumerate all2,187 based unordered triangles. Their normalized
loop matrices are H=3sqrt3*(P0 Pb Pc P0)|support. There are28 distinct matrices.
All are exactly unitary and normalize a logical qutrit's X and Z operators.
Three exported loops generate the full **216-element projective qutrit
Clifford group**.

The linear group has order **2,592**. Exact native loop words exhibit iI and
omega²I; together they generate a12-element scalar center. All entries lie
in Q(sqrt3,i), and all determinants are12th roots; these facts bound the
scalar kernel by that same12-element group. This is a built group action,
not an identification from the number216 alone.

For the projector application sequence Pc, Pb, P0, success probability is
**1/27**, independently of the encoded input. Failures are not corrected here.
Every maximally positive chiral triangle gives only iI on the logical qutrit;
non-Abelian gates require other triangles. Thus the native scalar chirality
and useful non-Abelian logical control occupy different operational roles.
Degenerate-projection holonomy is a known method;
[Oi2014](https://arxiv.org/abs/1402.1104) is credited. This construction supplies
the actual native matrices, costs and finite Clifford group, not a deterministic
or non-Clifford-universal computer. Recent
[Clifford-hierarchy/twisted-double work](https://arxiv.org/abs/2610.00464)
does not remove these resource boundaries; its odd-prime realization statements
also cannot be silently applied to the qubit deck group.

## Reproduction and limits

Run `py -3 analysis/w33_20261103_native_eight_validation.py`. It regenerates
all eight outputs, verifies ten parent input hashes, then runs22 independent
pytest cases. The tests have no fixtures; `--noconftest` explicitly avoids the
repository-wide legacy fixture preparation and subprocess rewriting. The
validation JSON records actual stdout, stderr, return codes and timings.
Repository guard outcomes are recorded separately, including nonzero outcomes.

The eight fronts supply concrete maps, exact finite coefficients, consistency
tests and a conditional quantum instability. Gauging, supersymmetry, the
ququart/qudit driver, physical scale, topology and synthetic controls are still
model inputs. No observed particle spectrum, Lorentzian gravitational dynamics,
selected cosmological vacuum or completed TOE is claimed.

Five independent next investigations: stabilize the ADS branch with explicitly
audited interactions; synthesize a repeat-until-success native qutrit receiver;
prove a thermodynamic tunneling bound; construct symmetry-compatible twisted
interfaces; classify genuinely smaller alternative common covers.
