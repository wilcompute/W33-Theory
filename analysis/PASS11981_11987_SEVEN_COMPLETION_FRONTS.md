# Passes11981–11987: a CP-breaking mediator vacuum and continuous atlas holonomy

All five requested directions were executed, plus logical-module descent and
a spinor gate construction. Two concrete advances emerged: a supplied scalar
UV model with stable weak-CP-breaking vacua, and an exact O(6) compact holonomy
closure for a specified native atlas connection. Neither is a physical TOE.

## 11981 — actual mediator matching transmits weak CP

The two-triplet self-cubic and mixed-cubic attempts were retained as negative
controls: sixteen local minima were stable but weak-CP blind. They preserved
too much common family symmetry. These are finite search outcomes, not a
universal no-go theorem.

Add a third E6-gauge-singlet family triplet t and a positive-mass scalar
antitriplet chi carrying the reflection-sign character. Let tau be a real,
CP-odd and reflection-odd neutral singlet source, normalized to tau=-1 on the
prior singlet branch. Real UV couplings permit

    V_chi = M_chi^2 |chi|^2
            + 2 Re chi† [g (h cross phi) + i mu tau t*].

The two source terms transform identically. Eliminating chi gives, at M_chi=1,

    -g^2 |h cross phi|^2 - mu^2 tau^2 |t|^2
    -2 g mu tau Im det(h,phi,t).

This names the map and the mediator. The determinant is the alternating
**family** tensor; it is not being mislabeled as the E6 fundamental cubic.
All three triplets are E6 gauge singlets in this experiment. Existing real
Gaussian current mediators and real self-cubic mediators supply the remaining
orientation terms. Positive degree-eight radial terms bound the potential
after the induced negative sextics are retained.

Twelve supplied parameter draws, fourteen starts each, yield five local
minima with nondegenerate up/down Gram spectra and robust nonzero weak-CP
invariants. The effective Hessian includes all eighteen real triplet fields.
The thirteen complex mediators add twenty-six real fields: direct UV energy
matching and the positive-heavy-block Schur complement give the complete
**44-real-field UV Hessian**, with the neutral source held fixed.

| draw | normalized Jarlskog invariant | smallest effective curvature | smallest UV curvature |
|---|---:|---:|---:|
| 2 | -0.00236083 | 0.153930 | 0.128294 |
| 3 | +0.01440371 | 0.424486 | 0.120204 |
| 6 | -0.02843770 | 0.173445 | 0.148924 |
| 9 | +0.00009823 | 0.299496 | 0.148309 |
| 10 | +0.01806347 | 0.021381 | 0.011263 |

The fixed-source potential retains combined CP/reflection. Each of these
vacua has an equal-energy partner with opposite weak-CP trace, explicitly
constructed by that transformation. Thus the retained symmetry is broken by
these local triplet vacua; it is not merely a complex VEV relabeled as CP.

Two opposite-sign mediator squares, with weights (1+epsilon)/2 and
(1-epsilon)/2, independently vary the determinant interference while keeping
the CP-even diagonal terms fixed. Re-minimizing the five cases at epsilon=0
gave weak-CP traces below 1e-12. This is a useful finite mechanism control,
not a certified global phase diagram.

**Limits:** the couplings, field inventory and normalized source are supplied.
The singlet source is not re-minimized jointly with this sector. The vacua are
numerical local witnesses, not global minima or interval proofs. No observed
hierarchy is fitted: draw3 has up ratios roughly (0.0319,0.1899,1) and down
ratios (0.1204,0.5295,1). This is a CP-transmission construction, not a realistic
three-family physical flavour vacuum or an E6-breaking vacuum.
The displayed Yukawa texture's mass-determinant phase is recorded separately;
it is generically nonzero. A Nelson–Barr/axion or other strong-CP completion is
not supplied by the determinant portal. The diagnostic is not a complete
threshold calculation of physical theta.

Prior owners:11924 misaligned-triplet mechanism;11975 Gaussian current
matching;11978 supplied singlet branch;34e149d79 earlier H27-covariant cubic
idea. General discrete-triplet CP potentials are established literature:
[de Medeiros Varzielas et al.](https://arxiv.org/abs/1706.07606).

## 11982 — quantize the gauge coordinates and distinguish external backgrounds

Construct the full six-state two-fermion Fock sector on an actual ring with
one unbounded electric coordinate, exact vertex Gauss reconstruction and
nearest-neighbor repulsion. Cutoffs L=2,3,4 give dimensions30,42,54. Every hop
changes precisely its own electric link by the required unit, including the
closing link. The L=4 numerical same-N gap is0.6177966110.

A supplied external flat phase phi is removed by the diagonal rotor unitary
exp(-i phi m), with exact finite-cutoff matrix equality. This is a **change
of dynamical link variables**, not a claim that H0 commutes with this unitary
or that the Born–Oppenheimer potential is constant. Static backgrounds should
not be counted as separate quantum sectors without additional constraints.

For the actual27-vertex/135-edge native tritangent complex, construct the
Coulomb-projected metric on all64 flat coordinates:

    M=C[I-B^T(BB^T)^+B]C^T,
    H_scalarBO = (g^2/2) p^T M^-1 p + E18(theta).

At the11980 stable order-nine background, the leading local oscillator
frequencies and link fluctuations are computed in all64 directions. At
g=.001, the maximum frequency/fermion-gap ratio is0.000150912 and maximum
link-phase RMS is0.102872. The metric is unchanged under adding a vertex-gauge
representative. A first-order density interaction expectation is recorded.

This native calculation is a **scalar harmonic Born–Oppenheimer/strong-flatness
approximation**: it omits Berry/Born–Huang terms, nonflat magnetic modes and
global tunneling. It is not a full135-link interacting spectrum or mass gap.
The interacting Gauss ring is a separate exact finite-cutoff control.
Prior11969/11974/11979 gauge constructions are credited.
The135-edge tritangent geometry is prior
`analysis/2026-10-14_toe80_native_octagon_e6_weyl_root_system.md`,
`analysis/BT816_cubic_surface_flags_reconstructed.md` and
`analysis/PASS11980_DISCRETE_HEISENBERG_HOLONOMIES.md`;
`analysis/PASS4992_4999_EXECUTED_OUTCOMES.md` owns earlier135-object
tritangent constructions as well.

## 11983 — local E6 frames assemble into the prior15, and yield O(6) holonomy

TOE79 owns the canonical27-point opposite shell and its completion by nine
central triangles. TOE80 owns its rank-six projector. Rebuild these at every
one of the forty W33 points. With R_p the scalar restriction to that shell,

    sum_p R_p^T P6(p) R_p = 16 P15,
    P15=(8I-4A_W33+J)/24.

The target is exactly the known15D point-line incidence null sector. BT771,
BT772, BT774 and BT1538 already construct this projector and the related
octet Gram. **The15-sector is not new**; this forty-chart factorization is the
specific additional bridge. Every embedded local six-space lies in that15.

Two different centers share eighteen labels. Their induced E6 graphs differ
on36 edges for collinear centers (240 pairs) and16 edges for noncollinear
centers (540 pairs). Therefore the partial identity on point labels cannot
glue the minuscule Gram matrices as isometries.

There is nevertheless an actual connection. Projection between local six-spaces
has rank2 on collinear-center pairs and rank6 on noncollinear-center pairs.
On the latter, the squared principal cosines are

    1, 1/3,1/3,1/3,1/3, 1/9.

Use the unique positive polar isometry on each of those540 full-rank edges.
It lies in Q(sqrt3), with the explicit integer polynomial in Q_r Q_p frozen in
the source/certificate. All540 exact isometry identities are checked, with
integer-overflow bounds. No invertible transport is asserted on rank2 edges.

### Exact compact closure proof

Three based triangles suffice:

    H0: (0,1,2), H1: (0,1,29), H2: (0,2,19).

Their6x6 Q(sqrt3) matrices and source Gram are stored explicitly. Each has
determinant -1. The exact product trace is

    tr(H0 H1) = -3/8.

Any finite-order matrix has roots of unity as eigenvalues, hence algebraic-
integer trace. A rational algebraic integer is an integer. Thus H0 H1 has
infinite order, and the compact holonomy closure has a nonzero Lie algebra.

Identify so(6) with the exterior square of the real six-space. Commutant
equations for the three induced15D exterior-square actions have225 unknowns
and exact rank224. Rank progress is168,221,224, independently reproduced
over F1009 and F1021 using valid residues of sqrt3. A nonzero modular minor
proves the same lower rank in characteristic zero; scalars give the upper
bound224. Thus the real commutant consists only of scalars. Because this is
an orthogonal representation, a proper invariant subspace would give a
nonscalar commuting orthogonal projector, so the exterior-square action is
irreducible.

The holonomy Lie algebra is a nonzero invariant subspace of so(6), hence is
all of so(6). The connected closure is **SO(6)**. An orientation-reversing
generator then gives full compact closure **O(6)**.

This is an exact finite-generator closure result for a **specified polar
connection**. It is not an E6 Weyl-group count, a physical gauge field,
selected coupling constant, spin structure or Einstein dynamics. The earlier
rational-polar guess failed its exact polynomial test and was corrected to
Q(sqrt3) before publication. Result searches for the map/trace/closure found
no earlier copy of this construction; generic polar and compact-group methods
are established mathematics.

## 11984 — a local hybrid chiral regulator with optical decoupling

Build the matrix-free25920-component kernel

    Q_total=I80 tensor Q_T4 + L_native80 tensor gamma5.

This uses nearest-neighbor links on a **supplied4D torus** plus the160 actual
internal W33 Levi links. The native optical eigenvalues are4-sqrt6,4,
4+sqrt6,8. Since their positive shifts exceed Wilson mass1, the optical
blocks have positive real Dirac part and deform to balanced massive blocks
without closing a gap. The acoustic block retains the conventional charge1
index+1 in the supplied unit-flux background. Direct local and spectral tensor
actions agree. This is not the earlier11977 native-cover kernel.

As a concrete chiral matter choice, construct all24 SU(5) generators on
10 plus conjugate5 and check all13824 ordered cubic anomaly traces. Maximum
residual is5.56e-16. This representation is chiral, whereas its selected U(1)
restriction has four charges of each sign and seven zeros. The charge±1
indices are explicitly checked. The E6 primitive-root27-charge control has
six charges of each sign and fifteen zeros.

The SU(5) content is standard and supplied, not a family derived from W33.
A global non-Abelian Weyl measure, native4D base, three families, admissible
uniform locality theorem and interacting continuum remain open. The coarse
torus fails a standard sufficient locality bound; nonzero finite index is not
being promoted to a locality proof. PriorTOE68/69 controls and aliasing warning
are preserved. Overlap construction: [Neuberger](https://arxiv.org/abs/hep-lat/9801031).

## 11985 — nonlinear metric and interacting matter clocks close exactly

Prior11306 already constructs quadratic80-clock dressing. Extend the actual
canonical calculation to a native-edge relative scalar(q,p), a positive
metric coefficient(a,pi), quartic scalar interaction and quartic metric
potential. The bare two-clock bracket is

    p^2 pi/2 - p q - p q^3/a^2.

The exact h1=a p^2/2 flow sends q->q+a p t and pi->pi-p^2 t/2. Dressing h2
by the inverse flow gives two independent constraints C1=P1+h1,C2=P2+h2(t)
with **identically zero** off-shell bracket. No small-field truncation is used.

The original two physical canonical pairs survive: extended phase dimension8,
two first-class constraints, physical dimension4. This proves a nonlinear
parametrized metric/matter model can close, while also exposing why mere
closure does not produce GR. It does not repair11976's different pointwise
hypersurface bracket or construct nonlinear Einstein gravity.
Prior [parametrized field theory](https://arxiv.org/abs/1011.2463) is credited.

## 11986 — the parallel logical code preserves some, not all, order-nine vacua

Use TOE83's54 square faces and TOE84's logical action, rather than rebuilding
their code parameters as new. Construct the explicit quotient of11980's
64D module by their38D boundary image. The26D F3 radical dimensions are

    26,24,21,15,11,6,3,1,0;
    ranks(z-I)^k =16,7,0;
    invariant dimension=coinvariant dimension=2.

Integral homology coinvariants become Z/3 plus Z/9. Exactly27 of the243 old
fixed flat classes survive the new faces. The originally displayed stable
representative does not, but **four of the48 original N18 discrete minimizers
do survive**, with unchanged static minimum energy. That is a direct code/
gauge-model compatibility test, not a conclusion from the number26 alone.

## 11987 — explicit spin lifts give a dense two-qubit gate library

The orientation-even kernel of the three holonomy generators is generated
by five Schreier words:

    H0^2, H1 H0^-1, H2 H0^-1, H0 H1, H0 H2.

Its closure is SO(6). Construct algebraic Spin(6) lifts using even products
of normalized Householder Clifford vectors, then restrict the8D Clifford
module to one4D chirality. Spin(6)=SU(4), so the compact closure of the lifted
gate group is **SU(4)**. The conclusion follows from the exact11983 closure
proof and the covering map, not a numerical Lie-rank heuristic.

The five explicit4x4 gates are evaluated, with unitary/determinant checks and
full six-gamma cover checks. A Pauli-conjugation witness is0.624334, so these
are not merely quantum Clifford gates. One gate gives concurrence0.690307 on
the declared|00> input. Clifford algebra used for the lift must not be confused
with the finite quantum Clifford gate group.

This is a mathematical two-qubit library, with adjoints, after declaring a
C4=C2 tensor C2 identification. It is **not** TOE84's26-logical-qutrit action,
a physical spinor encoding, a Hamiltonian control sequence, a noise threshold
or a scalable machine. Pair addressing, preparation and measurement are not
derived. General holonomic computation and the Spin6/SU4 gate correspondence
are prior art: [Zanardi–Rasetti](https://arxiv.org/abs/quant-ph/9904011),
[Glaudell et al.](https://doi.org/10.1038/s41534-021-00424-z).

## Reproduction and publication boundaries

Seven named producers and JSON certificates, twelve focused regression tests,
and a dedicated source-regenerating workflow accompany this report. The tests
also run the prior11980 and TOE82 controls. Actual hosted completion is recorded
separately in the publication receipt. Existing papers and unrelated peer files
are preserved. Reservations daf6e39c8 and d2797b590 preceded computation.
Local verification:19 combined tests passed in23.24s; final12 new checks passed
in13.88s. The guard's initial tritangent135 collisions were prior geometry,
read and cited. An81 warning arose from a prior pass-number shorthand, not a
claimed homology dimension; the three candidates were read and the ambiguous
comment rewritten. No source correction to those prior files was inferred.

The physical targets are still open: realistic masses/mixing/couplings, a
jointly stabilized singlet/flavour/E6 vacuum, nonlinear GR, an interacting native
chiral4D continuum and the cosmological constant. The exact mathematical
transport/universality result and supplied-model CP vacuum are concrete inputs
to that work; they do not establish those physical conclusions.
