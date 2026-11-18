# A quadric alternative with a local SU5 source and an SM Wilson subsector

Replacing the Klein cubic by the quadric cone gives a more direct local
gauge construction. A transverse C5 quotient produces an A4 singularity,
whose standard local M-theory gauge algebra is su5. A free real projection
gives a Spin7 / weak-G2 route and changes the gauge locus from RP3 to a
spherical3-manifold with fundamental groupC4. An explicit flat connection
then leaves su3+su2+u1. This supplies a localized SM gauge subsector, not
the complete SM: four extra geometric vector modes remain, no chiral
families are constructed, and neither the vacuum nor its scales are selected.

## Research path and inputs

The exact Klein analysis39c68b4ba found only genericA1 gauge strata and a
real-projection/Wilson-line tradeoff. This prompted a different cone,
rather than assigning an external SU5 bundle to the same smooth quotient.
The earlier conditional Wilson calculation is94d58a4d5. The parallel E6
Higgs/alignment work supplies a separate effective-theory gauge-breaking
mechanism; the present geometry is not asserted to be its ultraviolet origin.

The quadric and V5,2 are established objects, not new discoveries:
[Martelli and Sparks](https://arxiv.org/abs/0909.2036) study their AdS4
construction, while [Bergman and Herzog](https://arxiv.org/abs/hep-th/0108020)
calculate the normalized volume. The real Spin7 projection follows
[Forcella and Zaffaroni](https://arxiv.org/abs/0911.2595). The particular
cyclic action here fixes a3-dimensional gauge locus; it should not be
identified with another paper's free cyclic quotient merely from the
notation V5,2/Zk.

Repo searches covered V5,2, Stiefel/quadric gauge terms, RP3, the existing
SU5 adjoint producer and prior flux/Wilson reports. A Stiefel5x2 frame in
the adjoint potential is a different mathematical use. No repository-wide
or literature-priority claim is made for this assembled candidate.

## The local gauge algebra now has an explicit geometric source

Consider the smooth punctured quadric

    C={sum_(i=0)^4 w_i^2=0} minus{0} in C5,
    Y=C intersect S9 = V5,2.

It has the known homogeneous Sasaki-Einstein metric. Set
u=w3+i*w4, v=w3-i*w4. A real rotation in the(w3,w4) plane generates

    g:(z0,z1,z2,u,v)->(z0,z1,z2,zeta5*u,zeta5^-1*v).

It has determinant1 and preserves f=sum z_i^2+uv and the residue4-form.
Its fixed locus on the punctured cone is u=v=0, sum z_i^2=0. The normal
representation has weights(1,-1), so its transverse quotient is C2/C5,
typeA4. The standard unfrozen local ADE mechanism gives su5 on its
link Q=V3,2=RP3. This is an actual singularity source; the gauge algebra
is not inferred just from an order-five group or a chosen representation.

Complex conjugation K in the original w coordinates commutes with this
real rotation. In the(z,u,v) coordinates it sends(z,u,v) to(barz,barv,baru).
It has no fixed point on Y: its fixed real quadric is a positive sum of
five squares, zero only at the removed vertex. No g^a K has a fixed point
either. For a nonzero a, its square would force a fixed point into Q,
where g acts trivially and K is free. Thus the full group is C5 x C2,
with only C5 isotropy along the gauge locus.

K reverses J and conjugates Omega4, preserving J^2/2+ReOmega4. It projects
the standard SU4 singlet pair to one as in the exact Clifford/form control
in the Klein real-projection producer. The resulting geometry is a standard
N1 Spin7-cone candidate. This is not a derivation of the complete localized
supersymmetric action, flux/gluing data or quantum orbifold completion.

## The gauge locus has C4, even though the ambient space has only C2

The quadratic parametrization

    q(a,b)=(a^2-b^2, i(a^2+b^2), 2ab)

has sum q_i^2=0, norm squared2(|a|^2+|b|^2)^2 and kernel{+/-1} on the
unit sphere. It realizes S3 -> RP3 after constant normalization. K lifts to

    A(a,b)=(-i*barb, i*bara),   A^2=-1,   A^4=1.

All identities are checked symbolically. Hence Qprime=Q/K is S3/C4,
not S3/(C2 x C2). Its H1 is Z4, H2 is0 and H3 is Z. The same lift is
right multiplication by i*sigma_x on SU2, which will control its spectrum.

The ambient orbit space has fundamental group C2: its C5 isotropy is
normally killed, leaving the free real involution. This does not forbid
an order-four gauge holonomy on Qprime. The gauge theory is localized
on Qprime, whose inclusion maps C4 to ambient C2 by reduction modulo2.
Its connection need not extend to a nonexistent bulk SU5 bundle.

## Check the normal-cycle action before choosing the gauge connection

The normal real involution is (u,v)->(barv,baru). In the A4 resolution,
the holomorphic swap reverses the exceptional chain, while complex
conjugation reverses each curve's orientation. Thus

    [E_i] -> -[E_(5-i)].

This is the longest Weyl element of A4, not an unavoidable outer Dynkin
folding. The script verifies it on all four simple roots using the
determinant-one5x5 reversal matrix. Inner untwisting permits an SU5 bundle
description; it does not automatically choose a connection or break SU5.
Distinguishing inner from outer actions is central to current ADE engineering;
see [Khlaif and Najjar](https://arxiv.org/abs/2508.00564). Their
Bryant-Salamon examples are different geometries, not a validation of all
the present global physics.

Use the simply connected SU5 lift and choose

    W=diag(-1,-1,-1,i,i),    W^4=1, detW=1.

This defines a concrete flat bundle S3 x_W SU5 over Qprime. Its
centralizer is S(U3 x U2), with eight off-diagonal roots and four Cartans,
dimension12. The SU5 lift has no H2(Qprime,Z5) obstruction since4 and5
are coprime; the full M-theory global charge form is still not determined.

There are exactly three ordered3+2 character choices modulo4:
(color,weak)=(0,2),(2,1),(2,3). The first has order2; the latter two
have order4. All are checked. The adjoint flat local-system cohomology
has dimensions(12,0,0,12): use finite-group averaging on S3. This is an
exact cohomology statement, not the spectrum of every flux-coupled mode.

All flat sectors have F=0 and zero classical Yang-Mills energy, including
the trivial connection with unbroken SU5. Therefore the computation
does not dynamically select an SM sector. Its classical gauge-flatness
also does not replace the missing full localized supersymmetry equations.

## Explicit gauge-vector spectral data

For Ric(Y)=6g, the quadric index is3. The base Kahler class is(3pi/4)H,
the fixed conic has degree2 and area3pi/2, and the Reeb period is3pi/2.
Consequently

    Vol(V5,2)=27pi^4/128,
    Vol(Y/(C5 x K))=27pi^4/1280,
    Vol(Q)=9pi^2/4,    Vol(Qprime)=9pi^2/8.

The lift of Qprime to S3 is a Berger metric with horizontal radius
squared3/2 and fiber radius squared9/4, normalized so the round unit
S3 would have both radii1. Homogeneity of the conic fixes the horizontal
scale; the Reeb period fixes the fiber scale. The scalar harmonics obey

    lambda_(ell,m)=(2/3)ell(ell+2)-(2/9)m^2,
    m=-ell,-ell+2,...,ell.

Right multiplication by i*sigma_x acts on a nonzero|m| pair with characters
i^ell and -i^ell; the m=0 line has character i^ell. The lowest eigenvalues
in the four C4 characters are(0,16/9,40/9,16/9). The scan is backed by the
analytic increasing bound lambda >=(4/9)ell^2+(4/3)ell: ell>=3 lies above
all displayed nontrivial minima.

External vector components of the leading localized gauge action use
these internal scalar harmonics. The order-four SM holonomy's broken
roots have characters+/-i and lowest m_X^2 L_AdS^2=4/9; the order-two
choice gives10/9. This is a particular gauge-vector subsector, not a full
gravitino/scalar/fermion coupled calculation. It shows explicitly that
the broken gauge masses stay at the AdS curvature scale rather than
becoming parametrically separated GUT states.

At leading Freund-Rubin order, writing the Maxwell flux parameter as N,

    R^6/lp^6=(40960pi^2/81)N,
    g4^(-2)=8pi^3 sqrt(10N)/c,    g7^2=c*lp^3.

Trace normalization is left in c. Page shifts and allowed global flux
sectors have not been calculated. Standard SU5 normalization gives the
usual tree relations g3=g2=g5 and gY^2=3g5^2/5. These are unification
relations at an unmatched compactification scale, not observed couplings.

## Two further checks prevent an inflated physical claim

First, the undeformed quotient retains the real SO3 rotations of the
first three coordinates and the normal SO2 rotation. K commutes with
both. Exact so5 commutator constraints have rank6 out of10, leaving
so3+so2 dimension4; the Reeb U1 is odd under K. Thus four additional
geometric vector modes survive the simple construction. The localized
SM algebra is not the full gauge algebra of the background. No mechanism
removing or lifting those extra modes is supplied.

Second, adding u^5+v^5 suggests a simple way to remove the normal uv
phase symmetry while retaining C5. In the family

    z0^2+z1^2+z2^2+u^p+v^p=0,    p>=5,

the normalized u,v Reeb charge is4/(p/2+2), equal to8/9 at p=5 and less
than1 throughout. Its holomorphic scalar would have eigenvalueq(q+6)<7,
violating the Lichnerowicz bound for Ric=6g. This is the established
[Sasaki-Einstein obstruction](https://arxiv.org/abs/hep-th/0607080)
applied to that specific family. It does not rule out other cones,
flux-deformed metrics or gauge-sector completions.

## What the candidate does and does not supply

This route supplies an explicit local ADE gauge source, a global gauge
locus, an available flat SM-breaking connection and a calculable gauge
vector subsector in a known Einstein background. The cyclic order5 and
the holonomy choice are inputs. The construction has no isolated
rank-enhancement points furnishing chiral families; no chiral matter
mechanism is implemented. The full C-field/gluing/anomaly data, localized
supersymmetric action, vacuum selection, extra-vector removal, scale
separation and observed cosmology remain open.

Run `python analysis/toe_20261118_quadric_A4_C4_SM_gauge.py`. The certificate
records the symbolic double-cover/lift, root and holonomy census, volumes,
spectral controls and two limitations above. It is a candidate gauge
geometry with explicit tests, not a solved TOE.
