# Complex phases, cross-field stabilizers, conic codes and refinement

Continuation of `10b626834`, executing the five next investigations. There are
two completed finite-group results, an unrestricted all-field reduction of the
arc problem, an explicit geometry-sensitive local interaction, and a controlled
free refinement with a charged-index resolution diagnostic. This is not a
complete exterior-arc classification or a physical TOE.

## 1. Arbitrary complex phases do not repair the prescribed cubic action

Producer: `w33_20261031_complex_cubic_obstruction.py`.

The previous obstruction only tested signs. This calculation allows every
nonzero complex monomial coefficient, not just a finite selection of roots
of unity. The unsigned action on the spinor16 orbit has a60-element point
stabilizer. Exact group multiplication verifies that this stabilizer is
perfect, as is the whole960-element projective group.

For a transitive monomial representation, phases on the stabilizer of a
coordinate give a one-dimensional character. A perfect stabilizer has no
nontrivial such character. Choose an orbit-transversal basis gauge: every
spinor action becomes an unsigned permutation after diagonal rescaling.
The singlet action is trivial because the whole group is perfect.

Let u_i be the16 nonzero gauge scalars. For a cubic term t=(v,a,b), with v
in the vector10 and a,b in the spinor16, its preserved sign determines the
generator phase on v in terms of u_a,u_b,u_g(a),u_g(b). Each v has four such
terms; equating them, then imposing the five singlet-vector-vector terms,
gives210 multiplicative equations in16 nonzero variables.

**Nine of those equations already multiply to `1=-1`.** The certificate lists
their exact exponent vectors, integer powers, signs and original cubic terms.
Their integer-weighted exponent sum is exactly zero and their sign exponent
is odd. The verifier reconstructs them from the native cubic, so this is an
integer identity, not floating-point phase fitting or an XOR-only argument.

An important exploratory failure was caught: individually primitive vectors
from a rational nullspace basis did not generate its full integer lattice.
They missed the odd relation. Saturating at2 exposed the nine-equation
certificate. A fourth-root search also failed, but it is not the reason the
arbitrary-complex theorem holds.

The corresponding120-element point stabilizer in the actual1920 cover is
also perfect. Its central -I must act trivially on all spinor coordinates
in any prescribed monomial action. Cubic invariance then forces it trivial
on the other coordinates too. Such a representation would factor through
the already excluded960 action. Thus neither domain admits this prescribed
27-coordinate cubic action with arbitrary nonzero complex monomial phases.

This completes the phase question **for this permutation action**. It does
not exclude different nonmonomial embeddings, another carrier, or a larger
common extension. The30720 signed lift remains valid. Monomial induction and
Tits/normalizer extensions are classical background; see
https://arxiv.org/abs/1912.02006 . The explicit restricted action and certificate
are the repository computation, not a claim to classify all E6 embeddings.

## 2. The q=3 and q=5 stabilizers agree by an explicit map

Producer: `w33_20261031_cross_field_stabilizers.py`.

Reconstruct the45 factorisations and27 frames from Pass11177. Exhaust all
51840 Sp(4,3) matrices and retain the1920 preserving one actual five-octet
frame. Their27-frame image has order960. A named incidence isomorphism takes
the q=5 weight action to this actual q=3 frame action.

Transport all six q=5 projective generators and select q=3 matrix preimages.
Their signs matter. Solving six binary sign unknowns corrects the first four
canonical representatives and leaves the other two. The resulting map checks
**all11520 Cayley edges** of the1920-element domain, is bijective, and sends
central -I to central -I. The corrected generators, actual frame octets and
27-coordinate transporter are frozen.

Therefore the actual frame stabilizer in Sp(4,3) and the actual Petersen-set
stabilizer preimage in Sp(4,5) are isomorphic, including their central extension.
The exact SU4 representation from the preceding packet also represents this
q=3 subgroup through the explicit map.

This resolves the cross-field comparison without identifying the ambient
groups or assuming equality from an order count. Both1920 groups have a
central involution, whereas W(D5) has trivial center. Pass11185 owns the
frame counts; its old parenthetical W(D5) identification by order was already
flagged in the preceding report. Counts and incidence actions are retained.
Unsigned cubic incidence symmetry still does not give the forbidden linear
complex monomial cubic action established above.

## 3. The unrestricted arc problem is a binary minimum-distance problem

Producer: `w33_20261031_exterior_arc_code.py`.

For every odd prime power q, let H be incidence between passant lines and
external points of a conic. Consider the classical binary code ker(H).
There are q(q+1)/2 coordinates and q(q-1)/2 checks. Each coordinate is on
(q-1)/2 checks; each check contains(q+1)/2 coordinates. Two points share at
most one check.

Any selected point of a nonzero even codeword needs another selected point
on each of its(q-1)/2 passants. None of those points can serve two checks.
Thus every nonzero codeword has weight at least(q+1)/2, the standard
no-four-cycle parity-check counting bound.

At equality every other selected point lies on a different passant through
each selected point. All pair joins are passants and no three points are
collinear. Conversely a half-sized exterior arc exhausts the passants through
each of its points, so every passant meets it in0 or2 points. Its tangent
contacts partition all q+1 conic points, giving the matching back.

> **Unrestricted good matchings are exactly codewords attaining this bound.**

This equivalence has no rational-degree hypothesis. Proving an all-field
exclusion outside3,7,11 is equivalent to proving strictness of this code's
distance bound there. The equivalence supplies a new route for this research
target, not the completed classification.

These conic-incidence codes are established prior art, constructed by Droms
and collaborators and studied by Sin--Wu--Xiang and others. Their family and
dimension theory are not discoveries of this packet. See
https://arxiv.org/abs/0911.2018 and
https://doi.org/10.1016/j.jcta.2010.11.010 .

Exact small controls give[6,3,2] at q=3,[15,6,5] at q=5,[28,13,4] at q=7,
and distance6 for the length66, dimension31 code at q=11. For3,5,7 all words
were enumerated; at11 the bound and an explicit word prove the distance.
Larger finite ranks are recorded as computations, not new general formulas.
Independent CP-SAT equality searches at19,23,31 returned UNKNOWN after their
limits; they are archived as such. Earlier matching exclusions are not
relabelled as completed runs of this solver. Coordinates implemented here
use primes only; the counting theorem itself applies to all odd prime powers.

## 4. A local interaction that sees W33 collinearity

Producer: `w33_20261031_geometry_sensitive_mediator.py`.

The preceding positive Gaussian edge interaction forgot commutation between
distinct directions. Add one traceless Hermitian matrix B_e **per spatial
edge**, sourced by `j_ab=i[Pi_a,Pi_b]`, with action

    mu_c^2/2 Tr(B_e^2)-g_c Tr(B_e j_ab), mu_c^2>0.

Completing the square gives `-K ||[Pi_a,Pi_b]||^2`, with
`K=g_c^2/(2mu_c^2)>=0`. Together with the previous alignment term:

    E_ab=J(3-Tr Pi_a Pi_b)-K ||[Pi_a,Pi_b]||^2.

All14400 native projector pairs verify the four costs:

| Relation | Cost |
|---|---:|
|same tick|0|
|same direction, different outcome|3J|
|distinct commuting directions|2J|
|noncommuting directions|2J-4K/3|

For J>0 and0<=K<3J/2, unlike ticks have positive cost and connected-graph
ground configurations are constant events. For K>3J/2 on a supplied bipartite
spatial graph, a noncommuting two-sublattice pair minimizes every edge;
constant events cease to be ground states. At equality many patterns coexist.
This is an exact zero-temperature threshold, not a full finite-T phase diagram.

With o=e^-3betaJ,c=e^-2betaJ,n=e^-beta(2J-4K/3), the exact chain transfer
spectrum is

    1+2o+36c+81n       (1)
    1+2o+6c-9n        (24)
    1+2o-12c+9n       (15)
    1-o               (80).

The39 direction modes now split into the actual24+15 W33 eigenspaces. For
positive J,K the colored pair relations recover the direction triples and
W33 collinearity. Their symmetry is `S3^40 semidirect Aut(W33)`, reducing the
previous accidental S40 direction freedom. Independent outcome relabelings
remain, so this is still more symmetric than a physical Clifford action.

Round14 already owns positive-mass current elimination for rank-two vacuum
mixtures. This packet puts the actual rank-three tick current on spatial
edges and computes its relation costs, transfer sectors and threshold.
Local heat-bath kinetics obey detailed balance, including negative bond costs.
The mediators, spatial graph, couplings and temperature remain supplied inputs;
no ultraviolet completion, physical clock or unique E8 real form is derived.

## 5. A controlled refinement must specify its fermion module

Producer: `w33_20261031_phase_space_refinement.py`.

Replace qutrit clocks/shifts by N-level clocks/shifts; N is a register size,
not a claim to use a field of composite order. Fundamental spinors use C^4
tensor C^(N^2). Numerical Hermitian signatures at several N retain index-1
in the tested mass7/5 region. These are numerical refinement samples, not
an all-N index theorem or interval certificates like the previous N3 result.

The full matrix module Mat_(N^2) is different. On it translations act by
conjugation. Their central commutators cancel, so all four adjoint translations
commute. Its N^4 Pauli monomials supply every Fourier momentum in(Z/N)^4.
Each free Wilson block has eigenvalues

    +/-sqrt(sum sin^2 p+(sum(1-cos p)-m)^2), each twice.

Its index is exactly zero at every noncritical mass, for every N. At m=1,

    H(p)^2=1+2 sum_(mu<nu)(1-cos p_mu)(1-cos p_nu),
    1<=H^2<=49.

This gives a uniform gap and an explicit locality estimate. The binomial
series for sign(H), normalized by7, has truncation error at most
`49(48/49)^(K+1)` at polynomial degree2K+1. In the Fourier-dual position
basis the polynomial has range at most2K+1. Thus the free refinement is
uniformly exponentially local. For p=a k, `Dov(p)/a` tends to
`i sum gamma_mu k_mu`, with an O(a) scalar correction.

This is a controlled flat Euclidean free-Dirac refinement on a supplied
operator-module/Fourier interpretation. It does not turn the original
fundamental index into a derived4D chiral spacetime index. Central flux being
invisible in an adjoint is prior Pass5709; the80 Pauli translation characters
are prior October19. Standard overlap locality background is
https://arxiv.org/abs/hep-lat/9808010 .

### A concrete charged resolution gate

At a common N, test the necessary weighted-index ledger for the declared
`16_1+10_-2+1_4` inventory. Charge q uses Z^q in both clock planes, with the
same Wilson mass7/5 and register size for all species.

| N | indices at charges(1,-2,4) | sum multiplicity*charge*index |
|---|---|---:|
|15|(-1,-4,-1)|60|
|23|(-1,-4,-16)|0|

The coarse regulator puts charge4 in the wrong spectral phase. Merely writing
the continuum charge-cubic cancellation would hide this failure. The finer
tested resolution realizes the expected index ledger. These are numerical
signatures with recorded gaps, not a local anomaly primitive, integrable chiral
measure or a proof of anomaly cancellation in a completed quantum field theory.
Pass11592 already owns charge-dependent resolution controls on external tori;
the new calculation is on this finite Pauli module at common resolution.
See https://arxiv.org/abs/hep-lat/9811032 for the much stronger measure conditions.

## Validation, intake and remaining scope

All five producers were executed. Fourteen new controls and the preceding31
tests pass, for45 focused tests. The actual replay log, input/source/result
hashes and exploratory archive accompany this report. Archive entries include
the limited conic-code solver runs and failed phase-search approaches, not
only successful outcomes. The first cross-field probe hit a JSON NumPy-integer
serialization error after its algebra checks; the published producer uses
ordinary integers and replayed successfully.

GitKraken is available again and is used for Git operations. The additional
Desktop Commander host remains offline. Continuity's connected memory endpoint
still reports a different empty workspace, so logging uses the local journal.
Unrelated shared edits and synced project references are preserved.

The prescribed complex-phase descent and actual cross-field comparison are
resolved. The arc code strictness theorem, a UV-selected local interaction,
and a physical chiral gauge continuum remain open. Full intellectual reading
of the earlier215-page paper and every weekly patch remains incomplete.
No physical TOE completion is claimed.

## Five independent next investigations

- Construct a larger common extension carrying both actual spinor and signed-cubic operators.
- Prove strict conic-code distance bounds outside the known small-field equality cases.
- Determine the loop-sensitive phase diagram of the geometry-sensitive local current model.
- Build a local chiral measure on the chosen refinement module, beyond the weighted-index ledger.
- Derive a common physical metric and kinetic action for the actual matter and gauge carriers.
