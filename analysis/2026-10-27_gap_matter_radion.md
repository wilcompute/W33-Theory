# Five follow-ups: certified patch gap, matter, heavy measure, radius and thresholds

This packet continues `ff82f52e5`, after integrating upstream `a4ac80b85`.
Producer: `analysis/w33_20261027_gap_matter_radion.py`. All quantitative
outputs, rational witnesses and boundaries are in
`data/w33_20261027_gap_matter_radion.json`.

## 1. A positive rotor gap with no numerical excited-state premise

For the existing three- and six-loop patches at g=1, let
T(m)=m^T G m/2 and retain the supplied positive compact potential from the
previous packets. Exact enumeration on [-2,2]^d gives minimum nonzero norm12.
Cauchy-Schwarz in the G inner product bounds every omitted integer vector by
9/max diag(G^-1): 3888/41 for d=3 and 385236/5567 for d=6. Both exceed12,
so the enumeration is complete. Thus lambda1(T)=6, counting multiplicity
from lambda0(T)=0.

Since V>=0, min-max gives lambda1(H)>=6. The previously certified positive
integer ground trial vector is symmetrized under m->-m; its exact Rayleigh
quotient b gives E0<=b. An odd two-delta trial vector is orthogonal to that
even vector both in norm and in Hamiltonian form, providing an exact
two-dimensional variational upper bound on lambda1.

| Loops | First excited energy enclosure | Gap enclosure |
|---|---|---|
| 3 | [6, 1453/150] | [2.43758865328849, 6.20251415536478] |
| 6 | [6, 583/60] | [2.31371300900479, 6.24749234591742] |

Decimal endpoints summarize exact rational/algebraic certificates in JSON;
they are not directed-rounded interval data. The bounds concern the full
infinite electric-flux Hilbert space of these **finite spatial patches**.
Compact resolvent follows because T grows quadratically and V is bounded.
This is not a spatial infinite-volume Yang-Mills mass gap or confinement proof.
TOE72/75 already own complement/min-max methods; the new step here is the
complete shortest-vector certificate combined with V>=0, closing an excited
lower-bound premise for these current operators.

## 2. Translated and larger interacting matter

The first primitive direction is doubled using every actual integer edge
voltage. The two-cell periodic cover has54 sites and270 links. At Hubbard
U=2, the one-up/one-down sector has2916 states, E0=-19.9665539957414,
and its next computed energy is -14.7597071678024. Sparse resolvents compute
four deck-twist currents, four physical harmonic currents and an exact gauge direction.
The static Ward error is1.29e-12; the largest recorded resolvent residual is
5.28e-11. An independently constructed complex hopping Hamiltonian checks
the first twist curvature by a centered energy finite difference.

The two static4x4 blocks agree as gauge invariance requires. Their relative
deviation from a scalar multiple of h^T h is only1.26e-5 at U=2. The physical
electric block, however, has relative shape error0.673: it does not supply the
same metric. Its fitted scale is1.06e-8. At U=0 the harmonic currents annihilate
the uniform product ground state and the electric harmonic response vanishes
to numerical precision. An additional U=8 control is recorded. Using deck
twists alone would mix in gradient responses and obscure this failure. This
fixed-sector model does not establish a common Lorentzian light cone.

The one-cell two-up/one-down sector has9477 states, with correct fermionic
hopping signs. Its sampled lowest energy is -20.8690125371096; twelve returned
Ritz vectors lie at that energy. ARPACK may miss vectors in degenerate
eigenspaces, so twelve is an observed sample count, **not certified full
multiplicity**. The unique-ground Kubo expression is not applied there.
Neither computation includes a dynamical gauge field, all Fock sectors or
the thermodynamic limit. The electric response of a spatial pure-gauge
direction need not vanish without the corresponding temporal scalar vertex.

## 3. Nonabelian heavy frame and uniform locality: which operator?

Pass12002 already owns a finite-native-path/tree Wilson regulator, its
factorization and Abelian heavy frame. This packet extends its estimates to
noncommuting unitary representation links. For each direction,
Pminus T+Pplus Tdagger is unitary; hence its mass-zero Wilson term is
accretive. Every optical shift>=4 therefore gives
Re[(shift-1)I+t DW0]>=3I throughout t in[0,1], and the Hermitian gamma5 kernel
has gap>=3 for arbitrary unitary links. Kato transport from the onsite
projector gives a globally smooth gauge-covariant heavy frame. The finite
polar-step implementation is an endpoint-frame approximation, not a
measurement of the continuous Kato phase.

Controls use SU5 representations5,10 and the canonical signed-cubic27.
The latter is built by transporting the10+bar5+1+5+bar5+1 block action with
the previous exact cubic signed permutation. Endpoint projector and gauge
covariance errors are below1e-13. The heavy-frame numerical controls use one coarse
cell; the all-volume assertion follows from operator inequalities and the
already-owned bounded-native-path factorization, rather than finite sampling.
In addition, ordered noncommuting SU5 transports on all135 actual native links
test every compiled period path and the zero-voltage tree at one periodic
native cell. Factorization errors are8.14e-16 (periods) and1.78e-15 (tree).

The actual compiled native hopping range and tree degree give a sufficient
representation-link norm radius1/234016 for a uniform full gap>=3/4. For
the underlying fundamental SU5 links the radius1/468032 suffices for every
block of the27: ||wedge2(U)-I||<=2||U-I||. A finite-range kernel with norm
bound M and gap g has sign-projector polynomial tails governed by
1-g^2/M^2<1, uniformly in volume. This is the standard locality argument,
not a new general overlap theorem.

This small-link condition is a sufficient neighborhood of the trivial
connection; it is not a constructed plaquette-admissible measure in every
topological sector. The heavy onsite reference transforms by representation
matrices; its SU5 determinant character is trivial. The acoustic current has
not been implemented or independently verified here; uniform locality of the
previous nearest-edge regulator remains open. The path/tree regulator supplies a tree, cycles,
spin structure and large optical coupling. It must not be silently identified
with that nearest-edge operator.

Primary locality source: [Hernandez, Jansen and Luscher](https://arxiv.org/abs/hep-lat/9808010).

A current literature check identifies a conditional acoustic route:
[Craig2026, Proposition11.1](https://arxiv.org/html/2610.09093v1#S11.SS1).
The canonical27 has zero cubic SU5 anomaly and restricts to the standard
embedded SU2 as six doublets plus fifteen singlets, verified by its exact
character6t+6/t+15. These pass the paper's representation conditions.
Assuming its theorem and remaining analytic hypotheses, the coarse acoustic
measure can be pulled back through bounded native paths and combined with
the heavy frame. This requires common real spin boundary signs and sufficiently
admissible coarse fields. This packet has not audited the paper's proof,
implemented its current, or constructed every native topological sector.
This check concerns the SU5 restriction; the joint two-U1 measure is not
implemented. The four Euclidean regulator directions also do not derive a
physical clock or a Lorentzian3+1 interpretation.

## 4. Massive fields supply a radius minimum, conditionally

Consider one periodic massive Dirac field and two massless real bosons on a
circle. Omitting a common positive normalization, write x=2pi*m*R and

S(x)=Li5(e^-x)+x Li4(e^-x)+(x^2/3)Li3(e^-x),
V(x)=[4S(x)-2zeta(5)]/x^p.

p=4 is the Jordan expression; p=6 includes the radius-dependent Weyl
rescaling into the four-dimensional Einstein frame. With Dp=pS-xSprime,
each summand has strictly negative derivative
-exp(-nx)*(nx)*[(p-2)(1+nx)+(nx)^2]/(3n^4).
Consequently Dp falls continuously from p*zeta(5) to0. The stationarity
equation Dp=p*zeta(5)/2 has exactly one solution, with Vsecond>0.
The endpoint behavior proves it is a global minimum.

The Einstein result is x=2.69136987880828, mR=0.428344819900973.
The Jordan control is x=2.91977669541004. Both minimum energies are negative.
The proof of existence and uniqueness is analytic; quoted root locations are
high-precision numerical evaluations, independently checked with direct sums.

This is standard massive Casimir stabilization with **supplied** field content,
boundary conditions and mass. The native vacuum has not generated that mass;
backreaction and cosmological constant matching remain open. See
[Ponton and Poppitz](https://arxiv.org/abs/hep-ph/0105021) for prior work on
massive/massless Casimir stabilization.

## 5. Independent representation thresholds reopen the frozen candidate

The previous two-category exclusion remains correct. Reparse the same full
left-right field ledger, split SU2R components, and group by spin category,
SU3 dimension, SU2L dimension and |Y|. Subtract exactly three light SM
families and one Higgs doublet. The21 remaining nonzero beta groups sum to
(14,115/6,85/2), exactly agreeing with the previous excess totals.

Unlike two common fermion/scalar masses, independent group masses admit a
strictly interior one-loop match at kY=8/3. A maximum-margin linear program
proposes a point; exact rational reconstruction then verifies both coupling
matching equations and positive inverse coupling. At this witness the crossing
is approximately1.78036e14 GeV, with group thresholds between2.20835e6 and
8.06195e10 GeV. Exact logarithmic thresholds and inverse couplings are stored.
The coupling inputs are the same frozen repository inputs as before, not an
updated experimental fit.

The exact reconstructed logs also satisfy1<t_j<4<y<5. Using3<pi<22/7,
e<3 and exp(6)>25 gives rational mass bounds certifying every threshold is
above1TeV, below1e16GeV and below the crossing, which is below1e19GeV.
Thus domain membership does not depend on the floating LP inequalities.

This is a **kinematic existence witness**, not a native mass prediction.
Pass12311's actual full space-group pairing driver and its JSON were checked:
48 fractional states,50 singlets,134 allowed pairings, all48 covered by a
matching through degree1/2 operators. Allowed pair operators do not determine
their coefficients, common singlet vevs, vacuum stability or the singular
values of a mass matrix. Independent SM group thresholds may fail to be
realizable in one left-right breaking vacuum. Full matching, correlated
thresholds and two-loop running remain necessary.

## Content review and validation

All PDF text pages119-126 were read. They expose flavour locks and supplied
soft parameters, reinforcing why a cubic intertwiner does not establish a
realistic flavour vacuum. Five additional full archived test-only patches
were read: d579880fe,752562e19,be700f9c7,da24b4f20,7acd13de0. Those tests
distinguish exact finite Levi/Frobenius results, numerical Weil checks and
failed Xi identifications; their imported producers were not thereby read.
The ledger now records55/210 PDF pages and14/481 historical full patches.
The remaining content audit is unfinished. Archival/extraction flags are
kept distinct from reading flags.

Eight new checks replay exact gap certificates, test the54-site graph and
Ward identity, independently finite-difference the twist energy, retain the
larger-sector degeneracy, check nonabelian heavy covariance, check radion
stationarity by a direct sum, reconstruct exact coupling matching, and verify
honest partial-reading counts. No claim here solves the TOE in entirety.

Final validation: all37 focused tests across the five Oct27 test files pass
in45.79s. The producer regenerated its complete JSON successfully. The
rediscovery guard and whitespace check pass; RESULTS_INDEX.md is regenerated
from the final source/report snapshot before publication. Two development
checks caught a few-ulps numerical gap comparison and an unintended floating
unit in an otherwise exact character; both were corrected before the final
passing run. GitKraken transport was unavailable, so local Git was used for
fetch/review and publication. Unrelated shared dirty files remain excluded.
