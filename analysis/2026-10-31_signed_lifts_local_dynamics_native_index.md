# Signed lifts, local dynamics, and a native finite phase-space index

This continues `97c806265` across the five requested investigations. It builds
the full complex two-qubit lift, transports the native signed cubic, proves
two sign-lift obstructions, gives an all-field obstruction to simple matching
formulas, constructs a local event-aligning mediator model, and certifies a
nonzero index on the native two-qutrit phase-space carrier. These results do
not solve a physical TOE or every broad research problem in the five targets.

## 1. The complete two-qubit lift is now explicit

Producer: `w33_20261031_unitary_stabilizer_lift.py`.

The preceding packet only supplied a kernel dictionary. For each of the six
actual Sp(4,5) generators, conjugate that kernel and solve the intertwining
equations on the complex four-dimensional Pauli carrier. Normalize the unique
solution to a unitary and choose its Gaussian-unit phase so that reduction
`i -> 2 mod5`, followed by the frozen basis S, gives the **actual generator**.
This identifies maps, not merely groups of the same order.

All six matrices lie in SU(4), preserve the same alternating complex form,
and have Gaussian integer entries divided by two. Exact integer-numerator
multiplication closes on **1,920 matrices**. Their mod5 reductions are all
distinct; their projective reductions number 960. Thus the complex central
`+/-I` extension is isomorphic to the actual finite-field stabilizer preimage.
It is a concrete two-qubit Clifford subgroup of USp(4)=Spin(5).

The five Hermitian involution axes in its extraspecial-minus kernel mutually
anticommute. Conjugating them by each lifted generator recovers a signed SO(5)
action. An exact orthogonal five-by-five intertwiner identifies that action
with the previous Petersen-stabilizer representation. The previous negative
result about identifying the twenty lines with twenty D5 root rays remains.

Clifford normalizers and orthogonal geometry are established mathematics;
Calderbank--Rains--Shor--Sloane is primary background:
https://arxiv.org/abs/quant-ph/9605005 . The repository's TOE91--95 four-mode
Witting lifts concern a different q=3 projective group of order25,920, with
different scalar extensions. This q=5 stabilizer lift is not identified with
that group, a physical gate implementation, or an E8 coupling.

## 2. The native signed E6 cubic lifts, but not with the desired real signs

Producer: `w33_20261031_signed_cubic_lift.py`.

Use the exact 45 signed triples in
`artifacts/canonical_su3_gauge_and_cubic.json`, not an all-positive hypergraph.
An explicit 27-coordinate incidence isomorphism transports them to the
previous `1_4+10_-2+16_1` weight model. For each unsigned generator p, solve

    product_(i in t) sign_i = coefficient(t)/coefficient(p(t))

for every cubic triple t, fixing the singlet sign. Exact signed-permutation
closure gives **30,720 elements**, unsigned image960 and diagonal sign kernel32.
The coefficients, coordinate map, six signed generators, diagonal kernel and
closure hash are frozen. This completes a finite native signed-cubic lift.
Pass11185 owns the sector counts and TOE41 already uses these native signs;
neither the cubic nor its standard representation theory is claimed as new.

### Can a different sign choice remove the extension?

There are162 generator-sign unknowns. Choose a spanning-tree word for each
unsigned group element. Its 27 signs are linear functions of those unknowns.
Every other Cayley edge must produce the same signs; cubic preservation adds
further linear equations. This is a necessary and sufficient linear test for
a homomorphic signed-monomial section over phases `+/-1`.

The test is **inconsistent**. The certificate contains explicit cubic equations
and word relations whose XOR is `0=1`. Verification independently reconstructs
each word and coefficient row before checking that contradiction. Thus the
30,720 count cannot simply be replaced with960 by selecting better real signs.

### Does the new unitary double cover fix this?

We also tried the actual 1,920-element Sp(4,5)/SU(4) extension as the domain,
requiring its central -I to act as minus on16 and plus on1+10. Another explicit
word-equation contradiction excludes this **real signed-monomial** action too.
The option with central -I acting trivially already reduces to the rejected
960 section. On a diagonal central action, cubic invariance forces the vector
and singlet signs positive, leaving precisely the spinor sign as the possible
nontrivial choice.

Consequently the unitary and cubic lifts cannot be silently welded merely
because they share the same projective group. A representation using arbitrary
complex torus phases, a larger common extension, or nonmonomial matrices has
not been excluded or constructed. No physical Yukawa coefficient follows.

## 3. All fields: a theorem about rational matching formulas

Producer: `w33_20261031_arc_degree_obstruction.py`.

Let a good matching of the conic over any odd prime-power field be represented
by a degree-d rational **morphism** f:P1->P1, meaning coprime homogeneous
numerator and denominator, with no base point even at infinity. Its matching
action is an involution on all q+1 rational points.

The homogeneous cross-product of `f composed with f` and the identity has
degree `d^2+1`. It vanishes at those q+1 points. If `q>d^2`, it is identically
zero, so degree multiplicativity gives d=1. In odd characteristic a nontrivial
projective involution has a trace-zero matrix. Its paired conic chords all
pass through one fixed center; their poles are collinear. A good matching at
q>3 needs at least three noncollinear poles. Therefore:

> For every odd prime power q>3, a good matching represented by a rational
> morphism of degree d must satisfy `d^2>=q`.

This excludes every uniformly bounded-degree rational parametrization at
sufficiently large fields. It **does not exclude arbitrary matchings** or
degree growing with q, and it is not an all-q exterior-arc classification.
The degree/zero-count argument uses classical facts, not a new theory of
rational maps. The no-concurrence condition is essential.

Complete projective coefficient enumeration for the frozen witnesses gives
minimum morphism degrees5 at q=7 and7 at q=11. The lower-degree interpolation
spaces that do exist consist of candidates with common homogeneous factors;
counting them as valid maps would be an error. An initial computational guard
on coefficient-space dimension was too restrictive and was corrected before
accepting these results. All lower-degree projective coefficient choices were
examined, including the point at infinity.

An additional exact connection reorders the classical skew Paley conference
matrix by the matching pairs. Its off-diagonal2x2 blocks are Hadamard matrices,
and `C C^T=qI`. The block condition is equivalent to the nonsquare cross-ratio
predicate. It does not encode nonconcurrence; a classification based only on
these blocks would drop a necessary hypothesis. Prior finite exclusions and
the q=1 mod4 literature theorem remain as recorded in the preceding packet.

## 4. A local mediator and reversible event-aligning dynamics

Producer: `w33_20261031_local_tick_mediator.py`.

The existing October21 local bond-quantum chain was read in full: its exact
transfer spectrum stays mixing even at zero temperature. That result is not
overwritten by changing the interaction. Round13 already owns positive
Gaussian matrix elimination for1440 rank-two vacua, and Round14 already owns
a different pair-current mediator. Here the mediator is placed on spatial
edges for the actual120 rank-three tick projectors.

On each edge e=(u,v), supply a Hermitian9x9 field Phi_e with action

    mu^2/2 Tr(Phi_e^2) - g Tr[Phi_e(Pi_(a_u)+Pi_(a_v))], mu^2>0.

Exact Gaussian integration, including its label-independent determinant,
leaves the nearest-neighbor energy

    J sum_edges [3-Tr(Pi_a Pi_b)], J=g^2/mu^2.

The pair costs are0 for the same tick,3J for different outcomes of the same
direction, and2J for different directions. The action is bounded below after
completing the square. On a connected graph its label ground states are
exactly the120 constant event configurations. Optional independent onsite
quantum copies of h_a give the same partition factor for every tick and do
not alter this label result.

An explicit local continuous-time heat-bath dynamics replaces a site label
with probability proportional to its conditional Boltzmann weight. It obeys
detailed balance. A local conditional Ornstein--Uhlenbeck process can update
the Gaussian mediator too. This supplies a thermal stochastic kinetics,
**not** a fundamental arrow of time or unitary physical clock dynamics.

On graphs of maximum degree z, changing one neighboring label changes the
conditional energy by a function of oscillation at most6J. The standard
Dobrushin estimate gives uniqueness when `z tanh(3 beta J/2)<1`.
For the supplied square lattice this includes `beta J<0.1702752079`.

On a supplied Z^d lattice, d>=2, the model has120 symmetry-related constant
periodic ground states. Each disagreeing edge costs at least2J. The number
of bad sites is at most twice the number of disagreeing edges, giving a
Peierls bound at least J per bad site. Applying the standard Pirogov--Sinai
theorem therefore gives120 ordered phases at sufficiently low temperature.
This is an application of existing theory, not a computed critical temperature
or complete phase diagram; see Zahradnik,
https://doi.org/10.1007/BF01212295 .

The one-dimensional transfer spectrum is independently exact. For
`x=exp(-beta J)`, its eigenvalues are

    1+2x^3+117x^2                       multiplicity1
    1+2x^3-3x^2=(1-x)^2(1+2x)          multiplicity39
    1-x^3                              multiplicity80.

At any positive temperature a finite system has a unique symmetric Gibbs
state. Infinite-volume boundary conditions can choose an ordered phase.
No preferred one of the120 symmetry-related events is predicted.

**A decisive limitation:** the pair interaction has accidental symmetry
`S3 wr S40`. It cannot tell commuting from noncommuting distinct directions.
The October19 variance audit already owns that overlap blindness. The
positive mediator can supply conditional local event ordering, but it cannot
by itself select W33 collinearity, an E8 real form or a physical vacuum.
Spatial geometry, field content, couplings and temperature remain inputs.

## 5. A native finite phase-space kernel escapes the paired-index obstruction

Producer: `w33_20261031_native_phase_space_overlap.py`.

Take four gamma matrices from the new exact two-qubit Clifford axes and the
native two-qutrit Pauli translations

    T1=X tensor I, T2=Z tensor I, T3=I tensor X, T4=I tensor Z.

On C^4 tensor C^9, supply the Wilson operator

    D_W=(4-m)I - 1/2 sum_mu [(I-gamma_mu) tensor T_mu
                              +(I+gamma_mu) tensor T_mu^dagger],
    Gamma=gamma1 gamma2 gamma3 gamma4 tensor I9, H=Gamma D_W,
    D_ov=I+Gamma sign(H).

H is Hermitian. This is a36-dimensional operator on the two actual finite
carriers, outside the balanced `f(MM*)` incidence construction. It uses no
added external spatial torus, but **internal Pauli phase space is not thereby
identified with spacetime**. Two of these translations are diagonal clocks
in the chosen9-state basis. Neither four-dimensional locality nor a continuum
refinement follows from four labels mu.

| Wilson mass | index | number of zero modes | net chirality | numerical gap |
|---|---:|---:|---:|---:|
|7/5|-1|1|-1|0.1320508076|
|9/5|+1|3|+1|0.1176412030|

At9/5 the three zero modes have chiralities(-1,+1,+1). Counting zero modes
alone would misidentify the protected net index. The opposite mass phases
also prevent interpreting this construction as a unique family-number law.
The exploratory m=3 scan hits a gap closing; its raw floating sign count there
is explicitly not accepted as an index certificate.

### Exact certificates, not only numerical sign counting

The realification of H is a72x72 real symmetric matrix
`(A+sqrt3 B)/denominator`, with integer A,B. An eigensolver only proposes a
rational congruence matrix Q. The published verifier then uses **integer
arithmetic only**:

- a rational interval enclosing sqrt3 is checked by squaring integers;
- diagonal dominance proves Q is invertible;
- every signed Gershgorin disc of `Q^T H Q` excludes zero;
- Sylvester inertia gives the exact signature, hence index;
- the congruence margins and an upper bound on `||Q||^2` give a rigorous
  Wilson-gap lower bound greater than0.1 at both masses.

Ginsparg--Wilson residuals are below7e-15 numerically. Reversing one flux
plane reverses the index; commuting translations give index0. A small link
perturbation has operator-norm change below the proved gap and preserves the
index. More generally any Hermitian perturbation below that gap cannot change
inertia. This is a finite-matrix stability theorem, not a chiral gauge measure.

Noncommutative overlap indices are established prior art:
https://doi.org/10.1103/PhysRevD.67.085005 and
https://arxiv.org/abs/hep-th/0602078 . Pass11592 already implements external
four-torus indices, and Pass12015 already builds an external internal-torus
index and an H27 zero-mode module. The contribution here is this explicit
native9D phase-space/spinor36D construction and its exact signature certificate,
not the invention of finite-matrix chirality. The Wilson form, mass, gamma
assignment and translation selection remain supplied choices.

## Validation and remaining scope

The new tests check exact unitarity and finite-field intertwiners, the actual
native signed coefficients, independent reconstruction of contradiction words,
integer inertia certificates and tampering, native-operator binding, chirality
versus zero-mode counts, projective interpolation at infinity, Paley blocks,
local detailed balance and the transfer spectrum. Earlier19 controls remain.
Actual test output and source/input/result hashes accompany this report.

Remote Desktop Commander reports TheHeavyCrown offline. Work used local
processes; no additional remote computation is claimed. GitKraken remains
unavailable, so the explained Git CLI fallback is used. Existing unrelated
working-tree edits are preserved. Local Continuity records were used because
the connected MCP memory endpoint reports an empty, different workspace.

The full unitary finite-group lift is completed. The signed-cubic lift is
completed with explicit restricted descent obstructions. The all-field arc
classification, a UV-derived physical local action, and a native chiral gauge
continuum remain open. Full intellectual review of the previous215-page
paper and every weekly commit also remains incomplete. No TOE completion is
claimed.

## Five independent next investigations

- Classify complex-phase cubic lifts and compare their extension classes with the exact SU4 lift.
- Prove an exterior-arc bound for unrestricted matching functions, beyond rational formulas of bounded degree.
- Add a derived local interaction that resolves W33 collinearity without the mediator's accidental wreath-product symmetry.
- Construct a controlled refinement family for the finite phase-space kernel and test locality, anomalies and gauge measure.
- Couple the actual signed E6 matter carrier to a dynamically selected spacetime/vacuum sector with positive physical kinetic terms.
