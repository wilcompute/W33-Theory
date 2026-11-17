# Witting symmetry, CP3 modes, and two different quotients with the same coarse space

An exact invariant calculation links the native Witting action to a different
eleven-dimensional compactification. It removes the BF-saturating scalar
multiplet from the invariant subsector, together with two massless scalar
multiplets. It also removes every continuous isometry gauge field. A
comparison quotient shows why the coarse algebraic variety alone cannot
specify the physical spectrum.

This does not construct a stable quantum-gravity vacuum or a Standard Model.
The quotient is not free; its branch data and localized physics remain
essential. Restricting solutions to an invariant subsector does not remove
noninvariant excitations from the original unquotiented theory.

## Prior work and physics input

The exact forty rays and W33 identification already belong to
`exploration/w33_witting_srg_bridge.py`. The projective group and central
lifts have earlier certificates in `analysis/w33_20261017_toe95_group32.py`.
The invariant degrees (12,18,24,30) are already recorded in
`analysis/w33_witting_degrees_unify.py` and
`analysis/w33_hessian_polytope_e6.py`. The local G25/stabilizer program,
including `analysis/w33_pass1077_g32_g25_invariant_restriction.py`, is also
prior work. The present contribution is the specific KK fixed-space test
and the marked-quotient comparison, not discovery of these groups.

[Martin and Reall](https://arxiv.org/html/0810.2707v2) analyze the
nonsupersymmetric AdS5 x CP3 solution with F=c J wedge J and L^2=2/c^2.
The potentially negative scalar branch has m^2/c^2=(k-1)(k+2) in SU4
[k,2,k]. At k=0, the real 20prime=[0,2,0] saturates m^2L^2=-4.
Massless scalars include the 15 adjoint and [1,2,1] of dimension175, as well
as a universal axion. The unquotiented solution is linearly bosonically
stable at two derivatives, but [Ooguri and Spodyneiko](https://arxiv.org/html/1703.03105v2)
construct a finite-action decay in which the CP3 two-sphere fibers collapse.
Their asymptotic BF mode is nonzero. Thus linear stability is insufficient.

The earlier repo's blown-up CP3 Dirac-index construction in
`analysis/PASS11672_11679_NATIVE_DYNAMICS_INDEX.md` is a different space and
operator. It is not silently substituted for this homogeneous CP3 background.

## Exact action and fixed spaces

Let w^2+w+1=0 and take eight native Witting rays: the four coordinate rays
and (0,1,-1,1), (1,0,-1,-1), (1,-1,0,1), (1,1,1,0). Define

    R_v = I+(w-1) v v^dagger/(v^dagger v),    U_v=w^2 R_v.

For these generators the seed vectors are real; all matrices are computed
over Q(w). Each U is unitary, has determinant one and order three, and has
the same projective action as R. All eight ray permutations are verified
exactly against the full forty-ray list. Their permutation closure has
25920 elements, agreeing with the prior projective-group result. An
independent floating-point check confirms the existing ray ordering.

On V=Lambda^2 C4, let J be the symmetric wedge-volume pairing. For G=Lambda^2 U,
G^T J G=J and G J G^T=J. The representation Sym^2(V) has dimension21 and
decomposes as the invariant pairing plus the traceless20prime.

The script solves the generator fixed-vector conditions. Reduction at the
good prime7, w=2, gives rank20 in dimension21. The explicit tensor J supplies
the matching characteristic-zero upper bound. Since tr(JJ)=6, this invariant
is outside the traceless20prime. The same method gives full rank15 on the
adjoint and full rank300 on Hom(15,20prime). Full modular column rank is a
proof of absence of characteristic-zero fixed vectors, not a numerical rank
estimate. Denominators are powers of three and remain invertible modulo7.

An independent GL4 interlacing-character computation verifies the complete
SU4 tensor identity, with determinant shifts included:

    15 tensor 20prime = 175 + 45 + 45bar + 20prime + 15.

The adjoint is self-dual, so the zero-dimensional Hom fixed space means the
whole tensor product has no invariant vector. In particular the175 has none.

| Multiplet | Witting-invariant dimension | Consequence in the invariant subsector |
| --- | --- | --- |
| BF-saturating20prime | 0 | This entire marginal scalar multiplet is excluded |
| Massless scalar15 | 0 | No invariant mode from this multiplet |
| Massless scalar175 | 0 | No invariant mode from this multiplet |
| Isometry gauge fields15 | 0 | No continuous metric-isometry gauge fields survive |
| Universal scalar axion1 | 1 | It is not removed by this projection |

These statements do not mean finite symmetry alone protects all quantum
masses: invariant quadratic terms for noninvariant fields can still exist.
For an actual quotient, only the untwisted bulk conclusion follows. The
known decay's nonzero20prime asymptotic mode cannot lie in the strict
invariant subsector, but no exhaustive classification of quotient bounces
or localized instabilities has been supplied.

## The quotient carries the forty reflection mirrors

For example R_e0 fixes the whole CP2 given by z0=0 and the point [1,0,0,0].
Thus the projective action is not free. Its forty order-three mirror
hyperplanes are the orthogonal hyperplanes to the forty rays. Each contains
twelve native points; the exact point/mirror incidence recovers the prior
W33 adjacency relation. The script verifies A^2=8I-2A+4J_40.

The established polynomial invariant ring of G32 has degrees12,18,24,30.
Consequently its coarse projective quotient is P(2,3,4,5). This is already
explicit in [Prokhorov, Fields of invariants of finite linear groups,
section4](https://cims.nyu.edu/~tschinke/books/rationality/final-old/prokhorov/prokhorov.pdf).
The same source gives the S5 quotient used below. No new rationality or
reflection-group classification theorem is being asserted.

Write H for the rational hyperplane class on the weighted space and h for
the hyperplane class upstairs. Here pi^*H=6h. The reduced branch
discriminant has weighted degree20: its pullback is three times the forty
mirror hyperplanes. The canonical relation is therefore

    K_coarse = -14H,
    K_orbifold = K_coarse+(1-1/3)D = [-14+(2/3)*20]H = -(2/3)H,
    pi^*K_orbifold = -4h = K_CP3.

The Jacobian-degree check is 11+17+23+29=80=40*(3-1). These are exact
arithmetic consequences of the standard invariant-ring and ramification
description. The quotient Fubini-Study metric has cone angle2pi/3 normally
to a generic mirror. Omitting the branch divisor changes the object being
modeled even where the coarse complex space looks smooth.

## A control: the same weighted space retains a different massless mode

Let S5 act on its standard four-dimensional representation. Its invariant
degrees are2,3,4,5, so its coarse CP3 quotient is also P(2,3,4,5). However:

| Datum | Projective Witting | Standard S5 |
| --- | --- | --- |
| Projective group order | 25920 | 120 |
| Generic mirror inertia | 3 | 2 |
| Reduced branch weighted degree | 20 | 20 |
| Orbifold log canonical class | -(2/3)H | -4H |
| Pullback of H | 6h | h |
| Fixed dimension in20prime | 0 | 0 |
| Fixed dimension in15 | 0 | 0 |
| Fixed dimension in175 | 0 | 1 |

For S5, exact conjugacy-class character averaging gives the last three
entries. The175 character is computed with Jacobi-Trudi/Newton identities.
Odd permutations require a phase to lift to SU4; the20prime character
therefore includes the determinant sign. Omitting that sign would give a
wrong comparison. At the same upstairs Fubini-Study normalization, the
quotient volumes differ by a factor216. Flux quantization may require a
different normalization in a physical comparison; that is not imposed here.

This is an explicit spectral distinction between two quotients with the
same coarse algebraic variety. The one surviving S5-invariant175 scalar
allows, but does not prove, an invariant tadpole. In the Witting subsector
that particular linear term is excluded. Neither quotient has been furnished
with the localized-sector physics needed for a complete compactification.

## What this changes, and what remains

Witting symmetry gives a concrete way to eliminate marginal charged bulk
modes from a CP3 invariant sector. It simultaneously removes all continuous
bulk isometry gauge fields. Even unquotiented SU4 has rank3, whereas the
Standard Model gauge algebra has rank4; an isometry-only embedding was
already insufficient. New gauge sectors or a different mechanism are needed.

The essential missing work is a globally specified orbifold/defect completion,
its localized fields and anomalies, quantum corrections, flux quantization,
and nonperturbative decay channels. The existing E6 Higgs/messenger work has
an independent field inventory; no action unifying it with this quotient
has been constructed.

Run `python analysis/toe_20261117_witting_CP3_invariant_modes.py`.
The same-named data JSON contains the ranks, exact character table, mirror
incidence, ray permutations and canonical checks. It is a certificate for
these finite algebraic calculations, not for physical vacuum stability.
