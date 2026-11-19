# Native E8 holonomy, a rank-six flat-deformation gate, and degree-four torsion

This packet closes the coordinate gap in the previous projective E8
construction and identifies two further constraints. The compensated holonomy
is now explicit on the repo's native signed cubic and clock-Albert carrier.
Its compact connected centralizer has Lie algebra so8+u1+u1, not merely an
unclassified dimension 30. Nearby compact flat Wilson deformations preserve
rank at least six, so they cannot by themselves reach the rank-four Standard
Model. Separately, the specified Y7 has H4(Y;Z)=Z/9, with p1(TY)=6 eta²
and spin lambda=3 eta². These results do not construct a physical G2 vacuum.
There is a stronger phenomenological rejection: this centralizer cannot
contain commuting color su3 and weak su2 at all. Its direct Higgs descendants
therefore cannot be the SM gauge algebra.

## Provenance and what was already known

Starting published packet: d67b942e0, especially
`2026-11-19_H27_projective_qutrit_period_index.md`. It constructed all eight
nonzero degree-three twists as rank-three projective bundles and compensated
their phases inside (E6×SU3)/Z3, with 30 invariant E8 adjoint generators.

The native cubic-to-trinification coordinate map is **reused**, not discovered
here: `toe_20261113_h27_albert_cubic_coordinate_reconstruction.py` supplies
the signed permutation from 27 native coordinates to three 3×3 matrices.
The Gaussian clock carrier T and 2T^-1 are already certified in
`data/w33_pass11471_11475_frames_currents_matching.json`; Pass11561 checks
its tensor-level cubic identity. The manifest trinification cubic and its
flat branches already appear in
`toe_20261116_e6_trinification_cubic_flat_branches.py`.

The earlier parallel integral-topology packet established H3=(Z3)² and
a cup b=3 eta, but did not resolve the degree-four extension. The present
geometric model resolves that extension; it does not change those results.

## An explicit native holonomy map

Write the trinification cubic as

    N(A,B,C)=det A+det B+det C-Tr(ABC).

The compensating E6 factor r(conj(g)) acts by

    (A,B,C) -> (A g^-1, g B g^T, conj(g) C),   g in SU3.

This preserves the determinant terms and trace product. Pulling this action
through the existing signed coordinate map gives explicit native monomial
27×27 matrices. The qutrit determinant-one lifts use ninth roots; native
coordinate signs are stored uniformly as eighteenth-root phase exponents.
For all 27 holonomies and all eight twists, every one of the 45 native cubic
terms is checked exactly: **9,720 coefficient identities**. Tensoring with
the flavor triplet cancels the central multiplier. All **5,832** ordinary
81-block products are checked exactly in native coordinates.

The eight twists give the same finite E8 holonomy image as a matrix set;
their labeled representations of Gamma differ. This is not a claim that
their projective bundles or all characteristic classes are identical.
They therefore have the same parallel gauge centralizer, so choosing one
of these twists alone cannot select a different unbroken gauge algebra.

The clock matrices are explicitly U_clock=T^-1 U_native T. Their entries
are saved as sparse polynomials over Q(i) in zeta18, with the exact relation
zeta18^6-zeta18^3+1=0. The two generators have 96 and 45 nonzero entries.
The stored inverse satisfies T(2T^-1)=(2T^-1)T=2I exactly after converting
serialized numeric entries to rational numbers.

The matrices preserve the transported positive Hermitian form T†T and the
clock cubic. They belong to the complexified native algebra and its chosen
compact form. This does not identify them with the real E6(-26) Lorentzian
Peirce transformations. Transporting a compact metric is an explicit choice,
not a derivation of a spacetime metric.

## Identify the centralizer using representations, not dimension alone

On the repo's 78 native E6 matrices, commuting with the two compensating
holonomies gives an exact 14-dimensional algebra. It has a diagonal Cartan
of dimension two and twelve one-dimensional root spaces. With its intrinsic
Cartan trace form, six roots have squared length 1/12 and six 1/4. This is
G2, verified in native coordinates rather than inferred from the integer 14.

The monomial invariant subspace of the native (27,3) block has dimension
eight. Its action under these fourteen generators has exactly one singlet,
checked over Q(zeta18): a rational coefficient relation gives a kernel
vector, while specialization zeta18->2 in F19 has rank seven, proving a
nonzero seven-minor in characteristic zero. This avoids confusing rational
coefficient nullity with nullity over the cyclotomic field.
Since G2 is semisimple and its smallest nontrivial
representation has dimension seven, this module is 7+1. The dual block gives
another 7+1; the flavor adjoint has no invariant. Thus the full centralizer
as a G2 module is

    14 + 7 + 7 + 1 + 1.

This fixes its compact reductive Lie type. A nonzero embedding of G2 in a
simple compact algebra of dimension at most 30 can land in G2, so7 or so8:
the classical A and C possibilities in that size range have defining
representations of dimension at most six and cannot contain G2, whose
smallest nontrivial representation is seven-dimensional; the remaining
exceptional algebras are too large. A so7 factor supplies only one 7 in
addition to 14, and a G2 factor supplies none. A diagonal embedding in two
G2 factors would give 14+14, not the computed module; two factors involving
so7 are too large. Therefore the semisimple factor must be so8, accounting
for 14+7+7. The remaining two directions are central:

    Lie C_E8(rho(Gamma)) = so8 + u1 + u1,   rank=6.

This identifies the Lie algebra of the identity component. Its precise
global quotient and disconnected components have not been computed.
The standard E6 branching behind the comparison,
27=(3,7)+(6bar,1) under SU3×G2, is tabulated by
[Slansky](https://www.iitg.ac.in/cet/gian/2017/ppoulose/gian_ksb/Slansky_GT.pdf).

## Why a nearby flat Wilson deformation cannot remove two ranks

For Gamma=<x,y,c | c³=1,[x,y]=c,[x,c]=[y,c]=1>, x³ and y³ are central.
Near the finite representation rho0, take the unique small logarithms
A=log rho(x³), B=log rho(y³). They commute with the entire image and each
other. Dividing rho(x),rho(y) by exp(A/3),exp(B/3) produces an order-three
pair satisfying the same finite H27 relations. Finite-group representations
are locally rigid modulo conjugation in characteristic zero: averaging
kills their first cohomology. Thus locally every such flat deformation is
rho0 times a commuting pair in its centralizer, modulo conjugation.

Equivalently, the central extension 3Z²->Gamma->H27 gives
H1(Gamma;Ad rho0)=Hom(3Z²,Ad rho0)^H27, of dimension 2×30=60.
The 60 first-order parameters are not all unobstructed: their leading
integrability equation is [A,B]=0.

For compact holonomies, commuting pairs sufficiently near the identity lie
in a common maximal torus of the connected centralizer. Its rank is six.
Their remaining centralizer contains that torus, so its rank is at least
six; a generic pair leaves u1^6. An independent exact so8 matrix control
finds four commuting Cartans, plus the two preexisting central directions.
This excludes a nearby **compact-flat-Wilson-only** route to the SM gauge
algebra, whose rank is four. It does not exclude a Higgs condensate, nonflat
gauge curvature, singular boundary data, another component, or a sourced
noncompact PW/T-brane solution. In particular we do not apply this compact
rank argument to arbitrary nonnormal complex Higgs fields.

### A stronger gate: the SM semisimple algebra is absent altogether

Any embedding su3+su2 into so8 would make its faithful real vector8 a
faithful orthogonal representation of both factors. A nontrivial real SU3
representation needs at least six dimensions (the realification of 3);
the other possibility through dimension eight is the real adjoint8.
A nontrivial real SU2 representation needs at least three dimensions
(the adjoint3). Separate active summands therefore require at least nine.
An irreducible tensor active on both factors has dimension at least twelve:
the complex 3 tensor complex 2 remains complex and has real dimension12.
There is no faithful eight-dimensional real representation of su3+su2.

The central u1 directions cannot help, since a homomorphism from a perfect
semisimple algebra to an abelian algebra is zero. Thus **su3+su2, and hence
the SM gauge algebra, cannot embed in so8+u1²**. The code enumerates the
low-dimensional real representation types using the SU3 Weyl dimension
formula and SU2 real/quaternionic parity as a finite check of this argument.
This applies to arbitrary embeddings, not only regular root subsystems.

Consequently this exact holonomy cannot be a direct SM gauge parent even
after further ordinary Higgs breaking inside its unbroken algebra. A nearby
compact flat Wilson deformation only takes a further centralizer inside
that algebra and cannot fix this. The E8 embedding/background must change,
or genuinely new emergent gauge physics must be constructed. The projective
bundle and torsion results remain valid as mathematics; they are not a
successful SM compactification. The general SO8 gauge-embedding problem
also motivates going beyond SO8 in other work, for example
[Meissner and Nicolai](https://arxiv.org/abs/2503.13155); that paper is
context, not a construction of this background or proof of our new bundle.

## Resolve H4 by an explicit circle bundle

The original free quotient is a lens-space bundle L5(3)->Y->T². The lens
monodromies are the commuting projective clock and shift in PU3, with a
nonzero obstruction in H2(T²;Z3). Choose a rank-three unitary bundle F on
T² lifting this projective bundle, with c1(F)=t a primitive torus generator.
The choice of base orientation fixes its sign. Such a lift exists since
H3(T²;Z)=0, and its degree modulo three is the clock/shift obstruction.

Let Z=P(F) denote the bundle of complex lines, S its tautological line and
xi=c1(S*). The PU3-invariant line S^3 tensor det(F)^-1 has scalar weight
zero: a scalar lambda acts on its two factors as lambda³ and lambda^-3.
Its unit-circle bundle has fiber S5/Z3 and the specified projective
monodromy. Therefore it is the given Y. Its Euler class, up to circle
orientation, is e=3xi+t. The projective bundle ring is

    t²=0,   xi³+t xi²=0,

with the two independent degree-one torus classes understood. In the
bases (xi,t) for H2(Z) and (xi²,t xi) for H4(Z), multiplication by e is

    [[3,0],[1,3]].

The next Gysin map H3(Z)->H5(Z) is multiplication by 3 on each of its
two free generators, hence injective. Thus H4(Y) is exactly this matrix's
cokernel. Its Smith form is diag(1,9):

    H4(Y;Z)=Z/9, generated by eta²,  eta=pullback xi.

Explicitly t xi=-3xi² and 3t xi=0, so eta² has order nine, not three.
The earlier two graded Z3 terms form a **nonsplit** extension. As a control,
replacing the primitive determinant degree by zero gives the diagonal
matrix diag(3,3) and the split Z3+Z3 answer. The original convention
a cup b=3 eta may reverse eta's sign; its square is unaffected.

These are applications of the projective bundle theorem and Gysin sequence;
[Hatcher's text](https://pi.math.cornell.edu/~hatcher/VBKT/VB.pdf) provides
the general machinery. The 9 follows from the displayed integral Euler
matrix; it is not an independently selected family number.

## Pontryagin class and the C-field boundary

The circle direction in TY is trivial, so stably TY=pullback TZ plus a
trivial line. The relative projective Euler sequence gives

    p1(TZ)=3xi²+2t xi,

since the base has no degree-four classes. On Y, t=-3eta, hence

    p1(TY)=-3eta²=6eta² mod9.

Also w2(TZ) is the mod-two reduction of 3xi+t, which pulls back to zero,
so Y is spin. With no two-torsion in H4, its spin characteristic class is
uniquely lambda=p1/2=3eta². The unique half of lambda in this odd torsion
group is 6eta². These divisions are in the integral torsion group, not
division of a nonzero differential form.

Flat degree-four differential characters form H3(Y;R/Z)=Z/9: the real
third cohomology vanishes and the Bockstein identifies them with Tor H4.
Thus there are nine flat C-field **differences**, with a group different
from the B-field's Z3+Z3. Shifted C-fields form an affine torsor; a reference
is required to label them by these integers. The usual de Rham flux law
alone cannot see any of this torsion. [Witten's flux-quantization paper](https://arxiv.org/abs/hep-th/9609122)
explains the gravitational shift in M-theory; it does not supply a
compactification or a chosen torsion sector for this Y.

We have not computed a torsion Chern-Simons phase, quadratic refinement,
the E8 degree-four characteristic class, an anomaly cancellation action,
or a stabilized vacuum. The topology still excludes the proposed
torsion-free/positive nearly-parallel G2 structures. Flat C-field choices
do not repair the ordinary product Dirac gap or generate a real G4 flux.

## Reproduction and verification scope

Run `python analysis/toe_20261119_native_E8_Cfield_flat_gates.py` and
`python -m unittest discover -s tests -p test_toe_20261119_native_E8_Cfield_flat_gates.py`.
The six tests independently check dense cubic values, the reconstructed
clock matrices and metric, the root/module data, split versus nonsplit
Gysin controls, a generic compact so8 Wilson pair, and the SM subgroup gate. The topology and
classification arguments above are analytic inputs, not computer-derived
proofs of a physical TOE.
