# Native E6 modes, a specified chiral operator, and a conditional index-three model

The previous bi-Cayley packet supplied a family gauge representation.
This packet adds an explicit twisted fermion operator with a normalizable
local mode and an independently checked relative-cohomology count on a
specified punctured3-manifold. A four-negative/one-positive boundary
pattern gives net index three. The number of defects is an input, not
a prediction of the theory.

The same checks expose three obstacles to calling this a realistic
compactification: the C4 twist leaves vectorlike matter, its full
Spin10-sector gauge group is larger than the SM, and an unlifted U1_Psi
is anomalous with the counted modes. No complete7D geometry or quantum
completion is constructed.

## Framework and prior results

The operator uses the partially twisted7D gauge-theory framework of
[Pantev and Wijnholt](https://arxiv.org/abs/0905.1968) and
[Braun, Cizel, Hubner and Schafer-Nameki](https://arxiv.org/abs/1812.06072).
Their source/boundary formulation identifies chiral and conjugate-chiral
modes with first and second relative cohomology. Point-charge and Morse
localization mechanisms are established results, not discoveries of
this packet. Here we compute an explicit native E6 module, local
operator and flat-character mapping-cone model together.

Parents include Pass10950, Pass10961, the Spin10 matter/normalization
work in Pass11580/11596, and27665720c. The earlier quadric C4 Wilson
calculation is d84e57a8e. Those calculations had different scopes:
a centralizer12 in a local SU5 source does not imply centralizer12 in
a larger Spin10 source. The unrelated monopole analysis in
`2026-11-10_monopole_core_channels.md` explicitly lacked a gapped radial
Callias problem; the PW operator here is a different background and
does not resolve that monopole's radial spectrum.

During verification, parallel commit50229956d added
`2026-11-18_fivefront_Klein_gauge_F4_RG_winding_quantum_memory_3D_W33.md`.
Its full Klein residual quotient has rational b1=b2=0, reinforcing the
conditional smooth-Abelian-localizer obstruction on that different
gauge locus. It also tests the real-F4 kinetic boundary with SM running
and constructs a three-periodic scalar W33 graph cover. All six files
in that commit were read; its five calculation fronts were replayed
through non-writing functions, including the finite covers and Bloch
check, without modifying the parallel artifacts. Neither the graph's
chosen voltage rank nor the present chosen defect count derives a
physical number of dimensions or generations.

## The charged16 comes from the actual native E6 adjoint

Rebuild the Albert product and its complexified E6 on27. With c=e26,
use the existing Peirce generator

    Psi=6L_c-2I,
    27=1_(4)+16_(1)+10_(-2).

Exact commutator eigenspaces give

    78=16_(-3)+46_(0)+16_(+3).

For every matrix M in the charge-minus3 space, the map M -> M c lands
in the native Peirce16; its exact rank is16. The charge-plus3 space
maps the dual16 back to c. This identifies the localized representation
objectwise rather than attaching an unrelated16 to E6 by dimension.

The full27 hypercharge matrix from27665720c commutes with Psi and
annihilates c. The induced charge-minus3 representation has

    6Y=1^6, 2^3, (-4)^3, (-3)^2, 6^1, 0^1,

while the charge-plus3 sector has the opposite census. Hence the Higgs
charge used by the operator is tied to the previously checked SM family.

## An exact local operator and Gaussian mode

Choose the supplied Abelian Higgs background Phi=Psi df with

    f=x²-y²/2-z²/2,   Delta f=0.

With zero gauge connection it satisfies the Abelian torsion-free PW
equations away from sources. On forms valued in charge q, define

    d_q=d+q df wedge,
    D_q=d_q+d_q^dagger.

The code constructs all eight exterior-form states and their three
creation/annihilation operators. It verifies the canonical relations,
the Gaussian first-order residual, and the separable spectrum:

    D_q²=-Delta+sum_i kappa_i² x_i²
                    +sum_i kappa_i(2N_i-1),
    kappa=q(2,-1,-1).

For q=-3 there is one L2 zero profile per gauge component,

    psi=N exp[-(6x²+3y²+3z²)/2] dx,
    N=(54/pi³)^(1/4).

It has form degree1. For q=+3 the same Gaussian multiplies dy wedge dz
and has degree2. Under the twisted7D dictionary these are a chiral
family/CPT-conjugate pair, not two left-handed families. Reversing the
chosen background sign reverses the result.

The exact Witten-Laplacian gap is6 in these supplied coordinate/field
units: every bosonic excitation or fermion occupation flip costs at
least2 min|kappa_i|. This is not a measured4D mass scale. The complete
noncompact quadratic operator is solved here; its Gaussian is only a
local approximation to a more general defect background.

## Four poles give exactly three nondegenerate saddles

As a separate explicit harmonic control, take

    f16=-sum_(a=-3,-1,1,3) 1/sqrt((x-a)²+y²+z²).

Away from the four poles, Delta f16=0. Its transverse derivatives are
(y,z) times a strictly positive sum, so all critical points lie on the
x axis. On each interval between neighboring poles, the axial gradient
strictly decreases from positive infinity to negative infinity. Outside
the poles it has one sign. Thus there are exactly three critical points,
at -r,0,r with2<r<21/10. A rational isolating interval for r is in the JSON.

At every critical point the Hessian is diag(-2S,S,S), S>0, so all three
have Morse index1. At the origin S=56/27. Four sufficiently small inner
spheres have negative outward normal derivative; a sufficiently large
outer sphere has positive derivative. The domain is a ball with four
balls removed, equivalently S3 with five balls removed.

With relative conditions on the four inner boundaries and absolute
conditions on the outer one, its first and second relative Betti
numbers are3 and0. This verifies a minimal three-mode control rather
than multiplying a one-mode Gaussian by an arbitrary family label.
It still chooses four poles externally and supplies boundary data.

## A punctured lens version retains C4 holonomy

To test compatibility with the earlier gauge-locus topology, use the
round L(4,1)=S3/C4 with five disjoint small balls excised. Removing balls
does not change its fundamental group C4. There is an explicit harmonic
effective potential away from five chosen defect orbits:

    f16(x)=sum_a r_a sum_(k=0)^3 G_S3(dist(x,J^k p_a)),
    G_S3(chi)=(pi-chi)cot(chi)/(4pi²),
    r=(-1,-1,-1,-1,+4).

J is simultaneous90-degree rotation in both real2-planes. Its action
on S3 is free; the producer names five disjoint pole orbits. The radial
Laplacian of G away from its pole is1/(2pi²). The constant terms cancel
because the residues sum to zero. This constructs a C4-invariant
harmonic Higgs function away from the defects. Its gauge function is
f=f16/(-3), so the native charge-minus3 family sees the desired effective
potential. The defect residues and positions remain supplied data.

Near the poles, the four negative-potential boundaries and one positive
boundary have the required nonzero normal derivatives. No critical-point
census is asserted for this lens Green function. Its mode count below
uses the global relative complex, which includes possible Morse pairing.

For a one-dimensional flat character t with t^4=1, a punctured-lens
cell model has one0-cell, one1-cell and five2-cells, with

    d1=t-1,  d2=(1+t+t²+t³,0,0,0,0).

Boundary-sphere inclusion columns are e1,...,e4 and
(t-1)e0-e1-e2-e3-e4. The producer builds their mapping cone, checks
d²=0 and computes all ranks over exact complex numbers. With four
relative boundaries it gives:

| C4 character | b0 | b1 | b2 | b3 |
|---|---:|---:|---:|---:|
| trivial | 0 | 3 | 0 | 0 |
| each nontrivial character | 0 | 4 | 1 | 0 |

Conjugating the character and exchanging positive/negative boundaries
swaps b1 and b2, checked independently. We define the chiral excess
as nu=b1-b2; the relative Euler characteristic has the opposite sign.
Every character has nu=3, but their total massless spectra differ.

## The C4 twist produces vectorlike extras

Use W=diag(-1,-1,-1,i,i) in SU5, as in d84e57a8e. Its characters on
the family are computed from the certified even-Fock occupations of
27665720c, not assumed from the SM labels:

| SM sector | Character modulo4 | Chiral copies | Conjugate-chiral copies |
|---|---:|---:|---:|
| Q | 3 | 4 | 1 |
| dc | 2 | 4 | 1 |
| uc | 0 | 3 | 0 |
| L | 3 | 4 | 1 |
| ec | 2 | 4 | 1 |
| nc | 0 | 3 | 0 |

The net index is three complete family representations. However,
vectorlike Q,dc,L,ec pairs remain:60 chiral and12 conjugate-chiral
complex gauge components, with net48. There is no derived mass term
lifting those pairs in this background. Removing them would require
changing or coupling the operator/boundary system; a net-index statement
cannot silently discard its other exact zero modes.

This obstruction is stable under moving the poles while preserving the
boundary signs and local system. More generally in this five-boundary
model, for a flat bundle V one has b2=dimV-dim(V^holonomy). Eliminating
all conjugate modes would require trivial holonomy on the family16.
The16 is faithful for Spin10 alone. Adding a compensating Psi phase
can hide a central Spin10 action on this module, but a central action
does not break its adjoint gauge algebra; no stronger faithfulness
claim for the full product group is being assumed.
The code also tests all three SU5 C4 choices with all four additional
U1_Psi C4 phases: none removes the problem. The minimum is eight
conjugate-chiral gauge components. For the chosen order-four SU5 element,
the four Psi phases give conjugate-component counts12,8,12,16.
Thus a phase retuning can change the extras, but cannot give a clean
three-family spectrum within this point-defect/flat-bundle model.

## The full gauge group is larger than the SM

W=exp(2pi i*3(6Y)/4) has centralizer12 inside SU5. In the Spin10 sector,
six additional roots survive. The native charge-zero E6 matrices give
dimension20 for the full Wilson-invariant algebra,

    su4+su2+u1+u1_Psi,

with dimension19 before U1_Psi. An independent D5-root calculation
agrees. Exhausting the three ordered3+2 SU5 C4 choices gives:

| Color/weak charges | Spin10 centralizer dimension |
|---|---:|
| (0,2) | 21 |
| (2,1) | 19 |
| (2,3) | 19 |

Thus changing among these phases cannot produce an exact SM gauge
sector in the larger model. The extra su4 joins Q with L and dc with
ec, consistently with their equal copy counts. Standard Spin10 Wilson
rank/extra-U1 issues are established; see
[Ovrut, Purves and Spinner](https://arxiv.org/abs/1203.1325).

The earlier native E6 fixed-vector constraints can lower the gauge rank
algebraically. They cannot just be appended as constant physical Higgs
VEVs without solving their coupled equations with this nonzero Phi and
the defect sources. No such coupled solution is supplied.

There is a further necessary-condition test using the counted scalar
zero modes. With the original Psi phase, the only elementary SM singlets
are three nc fields of(chi,Psi)=(-5,-3). With zero FI parameter,
D_Psi=-3 sum|N_i|² cannot vanish for a nonzero singlet VEV. The CPT
conjugate is not an additional independent opposite-charge chiral field.
Other Psi phases supply a conjugate singlet as well, permitting a paired
moment-map cancellation algebraically. But those charges span only one
direction:3chi-5Psi still annihilates every such VEV. These elementary
singlets alone cannot remove both extra Cartan directions. This does not
exclude new singlet sectors, coupled non-Abelian backgrounds, strong
composite dynamics or supersymmetry-breaking vacua; none is constructed
in this packet.

The bare cubic interactions also fail a necessary Yukawa test. All120
pairwise brackets between the native charge-minus3 generators vanish,
checked on the27x27 matrices. Their bracket would have charge-minus6,
which is absent from the E6 adjoint. Thus the adjoint PW cubic cannot
give a direct two-family Yukawa from this one charged16 sector. Merely
having three different spatial profiles does not change this gauge
selection rule. New charged sectors, derived higher operators or a
changed Higgs configuration would be needed; this is not a general
nonperturbative/Yukawa no-go.

## An additional anomaly and the global geometry remain open

If U1_Psi remains a4D gauge field, net three16s of charge-3 give

    sum Psi=-144,  sum Psi³=-1296,
    SU3²-Psi=SU2²-Psi=-18,  Y²-Psi=-30.

The vectorlike pairs cancel in these anomaly sums. Standard-SM anomaly
cancellation of each family does not cancel these extra-U1 anomalies.
Additional states, boundary inflow or a derived Green-Schwarz/Stueckelberg
completion are needed. None has been computed here.

The round punctured3-metric and Abelian Higgs background do not establish
a complete ALE-fibered G2 metric, allowed defect charge quantization,
global C-field action or quantum compactification. In particular they
are not the earlier weak-G2 Freund-Rubin AdS geometry with new matter
attached. Torsion-free PW equations cannot be assumed unchanged in that
flux background. On smooth closed S3/C4, H1real=0 and the source-free
Abelian mechanism has no nonzero harmonic Higgs one-form; the added
defects are a substantive change.

Run `python analysis/toe_20261118_E6_Morse_relative_families.py`. The
certificate records the native adjoint-module map, local operator,
three-saddle proof, Green-function control, mapping-cone spectra, full
Wilson centralizer and anomalous-U1 limitation. The result is a specified
chiral gauge-theory test with explicit compatibility failures, not a
prediction of three families or a solved TOE.
