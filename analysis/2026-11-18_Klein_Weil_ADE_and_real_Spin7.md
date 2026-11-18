# Odd Weil matrices, actual A1 gauge loci, and a real Spin7 projection

Two tests make the Klein-link program more physical. First, exact odd-Weil
matrices construct the full PSL2(11) action and locate its genuine
codimension-four A1 strata, with a computable geometric gauge-kinetic
coefficient. Second, complex conjugation projects the known SU4 spinor
pair to one and gives a standard Spin7 / weak-G2 quotient route with A1
fixed strata. The latter destroys the previous ordinary C11 SM Wilson
line. The geometry supplies a local su2 gauge mechanism, not an observed
SM or a complete TOE.

## Sources, intake and ownership

The parent94d58a4d5 supplies the finite quadratic-module /60-point orbit
dictionary and the conditional C11 SU5 Wilson line. Parent3095ad3e9 supplies
the real Klein cubic, its isolated cone, SE metric existence and free F55
action. The parallel bdf464270 owns the60-point/660-flag dictionary, while
c2f8f23a7 owns the ordinary flat-twist Dirac bound. Those results are used,
not rediscovered as new physics. Searches also found the earlier
`analysis/w33_pass5361_qmod8_pair_weil_klein_clock.py`: it concerns a
different mod8 complex/modular Weil comparison, explicitly without
identifying its representations with each other.

The odd-Weil descent to a five-dimensional PSL2(11) representation is
published, for example in [Beauville, section3](https://arxiv.org/abs/1101.1372).
The non-Eckardt cubic-involution fixed curve/line geometry is studied in
[Casalaina-Martin, Marquand and Zhang](https://arxiv.org/abs/2210.14397).
The anti-holomorphic CY4-to-Spin7 construction and its AdS4 interpretation
are standard; see [Forcella and Zaffaroni](https://arxiv.org/abs/0911.2595).
The executed contribution here is the explicit cyclotomic Klein action,
fixed-space census, gauge-locus volume and the coupled spin/topology/
Wilson-line test on this particular family. No classification or priority
claim is made for the underlying methods.

The broad rediscovery tag g2+weil also points to
`analysis/2026-10-09_toe31_compact_cover_cat_spin16_lorentz_C8.md` and
`analysis/2026-10-21_local_phase_clock_and_rank_two_arithmetic_bridge.md`.
Those reports were read: their cover/Spin16 and arithmetic-clock results
are different calculations. The much larger
`analysis/THEORY_OF_EVERYTHING.py` was searched at its Weil entries
(arithmetic counting identities), not read in entirety. No claim of
repository-wide priority is made from this search. The present exact
matrices, fixed spaces and local geometry are given directly for review.

## An explicit five-dimensional action from an eleven-state Fourier system

Let zeta=exp(2pi i/11), g=sum_(a=0)^10 zeta^(a^2), so g^2=-11.
Use j=(1,3,2,5,4), eps=(1,1,-1,1,1), and define

    D=diag(zeta,zeta^9,zeta^4,zeta^3,zeta^5),
    S_ij=eps_i eps_j (zeta^(j_i j_j)-zeta^(-j_i j_j))/g.

This is the odd part of the11-state Fourier/Weil system after a real sign
change of basis. That sign change is essential: before it one cyclic cubic
term has a minus sign. In the displayed basis the invariant polynomial is
the same positive Klein cubic as the parent,

    f=sum_i x_i^2 x_(i+1).

GAP checks exactly in characteristic zero that S^2=1, det(S)=1,
trace(S)=1, D^11=1, f(Sx)=f(Dx)=f(x), and that <S,D> has660 elements and
trivial center. The certificate stores every S entry as integer cyclotomic
numerators over11. Python independently reads that export, checks the
real involution numerically, and closes660 matrices modulo23 with
zeta mapped to the order11 root2. The finite reduction is a cross-check;
the characteristic-zero closure is the actual GAP calculation.

## Fixed vectors, rather than merely projective fixed points

The exact conjugacy-class census, grouped by order, is:

| Order | Number of elements | Ambient eigenvalue1 dimension |
| --- | --- | --- |
| 1 | 1 | 5 |
| 2 | 55 | 3 |
| 3 | 110 | 1 |
| 5 | 264 | 1 |
| 6 | 110 | 1 |
| 11 | 120 | 0 |

Every noninvolution is free on the link. For fixed-space dimension0 this
is immediate. For dimension1, suppose a nonzero fixed vector x lies in
f=0. Invariance makes df_x vanish on all nontrivial eigenspaces; Euler's
identity df_x(x)=3f(x)=0 makes it vanish on the sole fixed line as well.
This contradicts smoothness of the punctured cone. Thus projective
eigenlines on the cubic need not be fixed link points.

For an involution, the ambient eigenspaces have dimensions3 and2. Its
positive plane cuts out a nonzero smooth plane cubic E. To see smoothness,
df at a positive fixed vector annihilates the negative eigenspace; a
critical point of the restricted cubic would therefore be a critical
point of the original cone. The negative eigenspace lies entirely in
f=0, because f(-x)=-f(x) while the involution leaves f unchanged. Thus
the projective fixed set is E plus a projective line. The line does not
give fixed link points: the involution acts there as minus identity.

The actual fixed link is Q, a circle bundle over E. On the tangent cone
the action is +1 on two complex directions and -1 on two. At generic
points the transverse quotient is C2/{+/-1}, typeA1. The standard local
M-theory singularity mechanism therefore supplies an su2 gauge algebra
along this3-dimensional locus. This uses the conventional local ADE
theory, not a derivation of all quantum degrees of freedom at the orbifold.

No higher ADE group occurs as a generic codimension-four stabilizer in
this holomorphic PSL quotient: any larger finite subgroup of SU2 has an
element of order greater than2, and the census proves those elements
have no fixed link point. This excludes that particular route to a
generic color-A2 locus, not every emergent gauge mechanism at intersections.

The V4 Sylow subgroup has a common two-dimensional ambient fixed space.
GAP restricts f to its binary cubic and checks its discriminant is nonzero.
There are three projective directions, hence three fixed circle directions
on the link. Locally the cone is C x(C3/V4), with three nontrivial sign
characters normal to the fixed direction. These are codimension-six
intersections of A1 strata, not a codimension-four A2 stratum. Their
localized interacting spectrum is not calculated.

## The gauge locus has a fixed geometric volume coefficient

E is an elliptic plane cubic, degree3 in the base X. The parent normalization
has base Kahler class omega=(pi/2)H and Reeb periodpi. Consequently

    area(E)=3pi/2,    Vol(Q)=3pi^2/2.

The bundle's Euler number is3. In particular H1(Q,Z)=Z^2+Z3,
H2(Q,Z)=Z^2 and H3(Q,Z)=Z. These topology/volume facts do not assume
a homogeneous Nil metric or calculate individual KK eigenvalues.

There is a single conjugacy class of55 involutions. GAP computes its
centralizer order12; after the trivially acting involution is removed,
the effective residual action on Q has order6. The generic stratum in
the full PSL quotient therefore has orbifold volume pi^2/4.

For a standard seven-dimensional gauge action with coupling g7, its
tree-level constant gauge-field mode has

    g4^(-2)=R^3 Vol(Q_unit)/g7^2.

The two coefficients are3pi^2/2 for the single-involution quotient and
pi^2/4 for the full-PSL generic stratum. The basic volume mechanism is
reviewed in [Acharya and Gukov, section8.2](https://arxiv.org/abs/hep-th/0409191).
Neither g7 normalization nor R is matched to observed parameters here;
intersection thresholds, flux terms and quantum corrections remain open.
These are geometric action coefficients, not numerical predictions for
the weak coupling.

## A different projection removes one of the known spinors

The preceding holomorphic actions preserve the SU4-invariant spinor pair.
To project that standard sector to one spinor, take K:x->bar(x). The real
cubic is invariant, and uniqueness of the base KE metric gives the real
isometric SE construction. On a local complex4 cone frame,

    K:J->-J,   K:Omega4->barOmega4,
    Phi=J^2/2+Re(Omega4) -> Phi.

Python checks all14 terms of this Cayley form exactly. It also constructs
the16-dimensional Clifford representation explicitly: the product of
the four imaginary-direction gamma matrices implements K, squares to+1,
and acts on the SU4 vacuum/volume singlets with eigenvalues+1 and-1.
Thus one of that known pair survives, unlike the codimension-two even
reflection whose Spin lift has order4 in the earlier CP3 comparison.

This is the standard Spin7-cone / weak-G2-link route to an N1 AdS sector.
We do not infer a complete localized supermultiplet spectrum or accidental
supersymmetry count from the two-dimensional singlet check alone. The
external Freund-Rubin flux is unchanged by this orientation-preserving
internal involution. An observed Minkowski/deSitter vacuum is not supplied.

The fixed set R=Y intersect R5 is a smooth nonempty real3-manifold. The
point(1,0,0,0,0) lies in it, with nonzero gradient. Smoothness on S4 follows
from Euler and isolated-cone smoothness, just as in the real producer.
It is special Legendrian and associative for the invariant weak-G2 form.
Its four real normal directions change sign, again giving localA1.
The topology and number of connected components of R are not computed,
so no count of global gauge factors is assigned.

## Isotropy changes the fundamental group and removes the old Wilson line

K normalizes D by inversion and commutes with the real5-cycle P.
Consider the two groups

    <D,K>=D22,     <D,P,K>=(C11:C5):C2 of order110.

Both have exactly eleven anti-holomorphic involutions D^aK. Their fixed
loci are conjugate copies of R and are pairwise disjoint: a common fixed
point would be fixed by their product, a nonidentity D power, impossible
by freeness. Every other anti-holomorphic element in the order110 group
has a nonidentity holomorphic square and therefore has no fixed point.
All isotropy is preciselyC2.

For a simply connected cover, the fundamental group of the underlying
orbit space is the acting group modulo the normal closure of its
stabilizers; see [Armstrong's theorem](https://wrap.warwick.ac.uk/id/eprint/74313/1/WRAP_Thesis_Armstrong_1966.pdf)
and [Brown-Higgins](https://arxiv.org/abs/math/0212271). The producer computes
that normal closure to have order22. It follows that:

| Quotient | Orbifold fundamental group | Underlying-space fundamental group | Singular set |
| --- | --- | --- | --- |
| Y/D22 | D22 | trivial | R |
| Y/group110 | group110 | C5 | R/C5 |

R may have multiple components. The table describes entire fixed sets,
not their connected decomposition. Crucially these are not free quotients;
neither the smooth363/15 C-field counts nor their cohomology tables can
be carried over without an orbifold calculation.

The old C11 SU5 holonomy W=diag(zeta11^2 I3,zeta11^-3 I2) also fails to
extend inside SU5: K D K=D^-1 would require W and W^-1 to be conjugate,
but their eigenvalue multisets differ. The underlying D22 quotient has
no nontrivial ordinary flat holonomy at all. The underlying order110
quotient has onlyC5, which still cannot implement the standard3+2 SU5
Wilson breaking proved in the parent.

An isotropy gauge parity diag(1,1,1,-1,-1) could conditionally project a
supplied SU5 theory to the SM algebra. That is an orbifold gauge embedding,
not a flat Wilson line on the underlying space, and the actual local
geometric gauge sector constructed here is only su2. A consistent SU5
source and localized chiral matter remain necessary.

## Reproduction and evidence boundaries

Run the GAP script first, then the Python script:

    analysis/toe_20261118_klein_odd_Weil_fixed_strata.g
    python analysis/toe_20261118_klein_real_Spin7_A1_projection.py

GAP supplies exact characteristic-zero matrices, polynomial invariance,
closure and fixed-space arithmetic. Python validates the serialized
generator, finite reduction, Clifford/form identities, extended groups
and their normal closures. The geometric arguments above and published
metric/local-ADE inputs are part of the evidence. No actual KE metric,
full flux-coupled fermion spectrum, chiral SM, quantum orbifold completion,
or solved TOE is asserted.
