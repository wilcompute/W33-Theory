# Projective qutrit holonomies settle the H27 torsion rank question

For Y=(S5×T2)/H27 with the specified free action, every nonzero torsion
class in H3(Y;Z)=(Z3)² has period and topological index exactly three.
Each admits a rank-three twisted complex vector bundle, constructed from
an explicit flat PU(3) representation of pi1(Y). This closes the rank-existence
question left open in `2026-11-18_six_front_SUSY_SIC_and_TOE_falsifiers.md`.
It does not compute the entire twisted K group or produce a physical G2
compactification.

## The topology that identifies the obstruction

Use the deck group already constructed in
`toe_20261119_h27_integral_torsion_gerbes.py`:

    Gamma = <x,y,c | c³=1, [x,y]=c, [x,c]=[y,c]=1>.

Its elements (a,b,c) have a,b integral and c mod3, with product cocycle
a*b'. The universal cover S5×R² is four-connected. In particular the
classifying map Y→B Gamma identifies H2(Y;Z) with group H2(Gamma;Z).

For the central extension C3→Gamma→Z², the homology spectral sequence has
E²_(1,1)=H1(T²;Z3)=(Z3)² and E²_(2,0)=Z in total degree two.
There is no differential into or out of (1,1). The d2 from (2,0) to (0,1)
is reduction mod3: the extension has commutator [x,y]=c, a generator.
Thus E∞_(2,0)=3Z. The other degree-two term E²_(0,2) is zero since
H2(BC3;Z)=0. Consequently

    0 → (Z3)² → H2(Y;Z) → 3Z → 0.

The quotient is free, so the sequence splits as abelian groups. The two
torsion generators are the commuting tori (x,c) and (y,c). They represent
the cross products of the base generators with the fiber's H1 generator
in E∞_(1,1). This also independently recovers H2=Z⊕(Z3)² and, by the
universal coefficient theorem, Tor H3=(Z3)².

A flat projective-unitary representation defines a multiplier in
H2(Y;R/Z). On a commuting torus its holonomy is the scalar commutator
of unitary lifts. The exponential-sequence Bockstein sends that multiplier
to the Dixmier-Douady class in Tor H3(Y;Z). The exact sequence and universal
coefficient theorem identify this class by its values on Tor H2: real
cohomology classes evaluate trivially on torsion. Thus the two scalar
commutator exponents label all nine torsion classes, up to the harmless
overall convention for the Bockstein sign.

## A concrete projective representation

Let omega=exp(2πi/3), X|j>=|j+1 mod3>, and D=diag(1,1,omega).
With [U,V]=UVU^-1V^-1, direct exact multiplication gives

    C=[X,D]=diag(omega,1,omega²),
    C³=I,   [X,C]=omega I,   [D,C]=I.

Passing to PU3 removes the scalar phases. Therefore x↦[X], y↦[D],
c↦[C] satisfies every defining relation of Gamma. It has torsion-torus
pairings (1,0), so its Dixmier-Douady class is nonzero. The projective
image is H27 of order 27, while the displayed U3 lift group has order 81.

For each nonzero pair (a,b) mod3, choose an integral matrix

    M = [[p,q],[r,s]], det M=1, (p,q)=(a,b) mod3.

Such matrices exist; the producer supplies explicit entries between -2 and 2
for every pair. Set U=X^p D^r, V=X^q D^s, and C_M=[U,V]. In PU3 this is
a determinant-one change of Heisenberg generators, so the Gamma relations
still hold. Scalar commutators with C_M are omega^p and omega^q. We obtain
all eight nonzero Dixmier-Douady classes, rather than only one projective
ray. No diffeomorphism implementing M on Y is required: each is a directly
constructed representation of the same Gamma presentation.

The representation constructs the flat principal bundle

    P = (Y_universal × PU3)/Gamma

and its associated M3(C) algebra bundle, using conjugation on matrices.
This is a degree-three Azumaya algebra representing the corresponding
torsion class. Equivalently, local U3 lifts yield a rank-three twisted
vector bundle with the same gerbe cocycle (or its negative by convention).

For a torsion Brauer class, its period divides its index, and the index
divides the degree of any representing Azumaya algebra. Here

    3 = period | index | 3,

so index=3. The minimal positive twisted-bundle rank is also three:
existence gives the upper bound, and d3(1)=±H or the period bound excludes
ranks one and two. This establishes that higher AHSS differentials cannot
force the rank subgroup below 3Z for these twists; it does not determine
all other AHSS differentials or extension problems.

The general PU(n)/Azumaya and period-index framework is established in
[Antieau and Williams, introduction](https://msp.org/gt/2014/18-2/gt-v18-n2-p13-s.pdf).
Our inference applies it to these explicit representations and this Y;
it is not a new general period-index theorem.

## Verification and connection to parallel work

The producer uses exact monomial permutations and phase exponents mod3,
without floating-point matrix comparisons. For each of eight twists it checks
729 projective products and 19,683 scalar 2-cocycle identities, the two
torsion-torus pairings, and image/lift group orders. The companion tests
also use independent dense numerical 3×3 matrices to check the seed
commutators and use the supplied integral matrices' determinants.

The seed is an ordinary qutrit Clifford phase, not a non-Clifford gate.
The earlier `2026-11-18_native_E8_C9_Clifford_link_Higgs_G2_qutrit.md`
already distinguishes projective Clifford order three from SU3 lift order
nine. We reuse that central-lift mechanism in a different role: the scalar
commutators now detect a genuine obstruction to an ordinary vector-bundle
lift. The matrix algebra descends despite the obstruction because scalars
act trivially by conjugation.

This strengthens the parallel first-AHSS packet by constructing its formerly
missing rank-three objects. It does not revise its necessary-rank calculation.
It also does not repair the geometric no-go: Y has infinite pi1, b1=2 and
b3=0, and cannot be the proposed torsion-free or positive nearly-parallel
G2 space. A twisted projective bundle is not an ordinary fundamental SU3
bundle; inserting it into E8 requires an explicit compatible global lift.
The B-field's degree-three class is not by itself an M-theory C-field
degree-four class, and the bundle rank does not count chiral families.

## A further connection: the projective obstruction cancels inside E8

There is an actual compatible global E8 holonomy construction, beyond the
single projective factor. Use the standard E6 trinification branching

    27 = (3,3bar,1)+(3bar,1,3)+(1,3,3bar).

For g in SU3, the homomorphism r(g)=(1,conj(g),g) into that subgroup
restricts 27 to seven copies of 3 plus 6bar: the first two summands each
give three triplets, while 3bar tensor 3bar gives 6bar plus 3.
In particular r(omega I) acts by omega I on all 27 components, so it is
the corresponding generator of the E6 center. The standard branching is
reviewed by [Slansky](https://www.iitg.ac.in/cet/gian/2017/ppoulose/gian_ksb/Slansky_GT.pdf)
and used in the parallel trinification anomaly probe. Conjugation choices
here fix our convention for the 27 and the common Z3.

Consequently the map

    [g] in PSU3 -> [(r(conj(g)),g)] in (E6×SU3)/Z3 -> E8

is well-defined: changing g to omega*g changes the two factors by the
opposite center elements already identified in the parallel shared-center
packet. Thus every flat PU3 bundle above extends to a genuine flat E8
bundle on the same Y. This is not merely cancellation on an unrelated
9-dimensional tensor product.

The producer checks it on the faithful (27,3) representation of the
quotient group. First it normalizes the qutrit lifts to determinant one,
using ninth-root phases; omitting this normalization would not justify an
E6 embedding. On the compensating factor the 27 is seven 3bar blocks plus
Sym²(3). Tensoring with the flavor triplet cancels every central multiplier.
All 729 group products are verified exactly as ordinary 81×81 monomial
matrices for each twist, and the finite holonomy image has order 27.

There is also an exact gauge-dimension gate. The E6 adjoint under this SU3
is 14 trivial copies plus eight adjoints, as follows directly by restricting
the trinification 78. Hence the full E8 adjoint character is

    chi248 = 14 + 9 chi8 + chi81 + conjugate(chi81).

The producer sums this character over the 27 holonomies in the exact
cyclotomic ring Z[zeta9]/(zeta9^6+zeta9^3+1). The sum is 810, giving
**30 parallel adjoint generators**. This already exceeds the SM's 12.
The Lie type and further breaking have not been established by this
dimension calculation.

These matrices use a standard abstract branching basis. We have not built
the intertwiner to the repo's native Albert/Peirce coordinates. This flat holonomy has not been made
compatible with the nonproportional PW profiles in the other new packet.
It also cannot evade the round-product Dirac gap or the topological G2
obstructions. It resolves the global center-lift question for this particular
construction, while leaving the physical vacuum question open.

Run `python analysis/toe_20261119_h27_projective_period_index.py` and
`python -m unittest discover -s tests -p test_toe_20261119_h27_projective_period_index.py`.
