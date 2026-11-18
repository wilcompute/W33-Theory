# A C11 quotient with an SM Wilson-line option and a torsion-to-Klein orbit bridge

The free C11 subgroup gives an alternative to gauging the full F55=C11:C5
on the Klein cubic seven-link. It permits a conditional SU5 Wilson line
with exactly the standard SM centralizer, while retaining the absence of
charge-four holomorphic marginal functions and continuous flat C3 modes.
The gauge sector itself and chiral matter are not derived here.

An independent connection comes from its integral torsion. The residual
normalizer C5 forces the eleven-primary linking form to be hyperbolic.
The corresponding finite quadratic model has modular matrices that, after
an explicit partial Fourier transform, contain exactly the same60-point
PSL2(11)/C11 permutation action as the parallel Klein-cubic orbit. Even the
commuting right-normalizer C5 action agrees. This is a concrete dictionary
between topology, finite quantum data and incidence, not an observed TOE.

## Inputs, parallel work and source ownership

Parent3095ad3e9 constructs the Klein cubic link Y and its free F55 action.
The integral F55 follow-up a3408dcce proves its cohomology/ring, lambda=0,
and protected harmonic controls. These supply the cover and coinvariant
arguments; the present calculation changes the quotient to M11=Y/C11.

The parallel bdf464270 report, orbit producer and660-flag producer were
read. They own the60-point Klein orbit and the11x60 flag dictionary, not
this report. The new script validates all660 stored rows rather than
claiming that result again. Parallel c2f8f23a7 supplies the ordinary Dirac
gap for flat unitary twists. The same standard theorem applies to M11,
so the new Wilson line does not evade that fermion constraint.

The familiar SU5 determinant obstruction is already in
[Anderson, Gray, Lukas and Palti, section4.2](https://arxiv.org/abs/1202.1757).
The new application is to the two explicit free quotients and their
different physical options. [Slansky](https://cds.cern.ch/record/134739/files/198109187.pdf)
supplies the E6 branching input. The finite quantum-double framework is
standard; see [Kitaev](https://arxiv.org/abs/quant-ph/9707021). No priority
claim is made for Wilson-line breaking, Cartan-Leray, or quantum doubles.

The rediscovery guard's alpha@121 candidates were read:
`analysis/w33_MCXXI_MCXXX_six_headlines_lloyd_exceptional.py` and
`analysis/w33_connes_lott_sm_action.py` use121 in an arithmetic
fine-structure proxy; `analysis/w33_pass75_zeta_equidistribution.py`
uses121 as a polynomial coefficient. None supplies the cyclic
extension, linking or Wilson-line calculation below. Topic/result searches
also distinguish the older Klein quartic and quadric constructions from
this cubic seven-link.

## The integral extension splits because its two characters differ

Write U=C11 and retain the order-five diffeomorphism P induced by its
normalizer. It acts freely on M11, with quotient M55. The cover is2-connected
and H3(Y,Z) fits equivariantly into0 -> Z3 -> H3(Y) -> L ->0, where
L=H3(X,Z) is the cubic's unimodular symplectic rank10 lattice.

The parent symplectic coinvariant argument gives L_U=Z11 and P action3
on that group: P D P^-1=D^9, the perfect coinvariant pairing scales by9,
and alpha^2=9 with alpha^5=1 forces alpha=3.

Homological Cartan-Leray in total degree3 has only
H0(U,H3(Y))=Z3+Z11 and H3(U,Z)=Z11. The latter is acted on by9^2=4.
No differential changes these entries: H1(Y)=H2(Y)=0 and H4(U,Z)=0.
After separating the prime3 part, the remaining extension is

    0 -> Z11_(action3) -> Tor_11 H3(M11) -> Z11_(action4) ->0.

A nonsplit abelian extension would be Z121. Every automorphism of Z121
has the same scalar modulo11 on its unique order11 subgroup and its
order11 quotient. The two scalars3 and4 are distinct, so that extension
is impossible. Thus Tor_11 H3(M11)=Z11+Z11. This use of the normalizer
settles an integral ambiguity that rational character data cannot settle.

Low-degree Cartan-Leray, universal coefficients and oriented7D Poincare
duality determine all additive groups:

| Degree | H_k(M11,Z) | H^k(M11,Z) |
| --- | --- | --- |
| 0 | Z | Z |
| 1 | Z11 | 0 |
| 2 | 0 | Z11 |
| 3 | Z11 + Z33 | 0 |
| 4 | 0 | Z11 + Z33 |
| 5 | Z11 | 0 |
| 6 | 0 | Z11 |
| 7 | Z | Z |

Consequently H3(M11,R/Z)=Z3+Z11+Z11 has363 flat degree-four C-field sectors.
The3-primary part follows from coprime-order transfer. The stable tangent
representation is the same SU5 representation as before; its restriction
has c2=176u^2=0 in H4(BC11,Z). Hence lambda(TM11)=0 integrally as well.
These facts do not determine electric Page charges or select a sector.

## A hyperbolic linking form fixed by the surviving symmetry

On the two eleven-primary H4 eigenlines P acts by3 and4. The torsion
linking form on an oriented7-manifold is perfect and symmetric in degree4.
Since3^2 and4^2 are not1 modulo11, P-invariance forces both self-pairings
to vanish. Since3*4=1, the cross-pairing can be nonzero, and perfectness
forces it to be nonzero. Rescaling dual generators gives

    b=((0,1),(1,0))/11 mod Z.

This specifies the eleven-primary pairing up to isometry, not named
geometric brane representatives. Its homogeneous mathematical quadratic
refinement is q(x,y)=xy/11. We do not identify this choice automatically
with the full physical M-theory Chern-Simons/Page refinement.

## Fourier transform closes the quantum-data / Klein-orbit dictionary

The finite quadratic group A=F11^2 has121 labels and K-matrix11*sigma_x.
Its conventional finite modular matrices are

    S_(v,w)=exp(-2pi i b(v,w))/11,
    T_(v,v)=exp(2pi i q(v)).

For the partial Fourier basis

    |x,k> = (1/sqrt11) sum_y zeta11^(k*y) |x,y>,

direct calculation gives the permutation actions

    S:(x,k)->(k,-x),    T:(x,k)->(x,k+x).

They are the standard SL2(F11) generators. Charge conjugation is
(x,k)->(-x,-k). Its even subspace has dimension61: one origin state and
60 nonzero sign classes. Removing the origin gives a transitive
PSL2(11) permutation action of order660 and stabilizer order11.

This is exactly G/U. In the peer matrix dictionary, a coset gU is labeled
by the first column of g modulo sign. The producer verifies that each of
the60 peer point IDs has a single such label across all660 flag rows,
and that the labels exhaust the60 nonzero sign classes. Thus the
Fourier-even modular orbit and the distinguished Klein-cubic point orbit
are explicitly equivariantly identified. The peer11x60 flag dictionary
can now be read as an11-face /60-state dictionary in this auxiliary model.

There is an additional commuting-action check. The inherited C5 acts on
linking coordinates by(x,y)->(3x,4y). In the Fourier basis it becomes
(x,k)->(3x,3k), commuting with the SL2 action. On G/U this is right
multiplication by diag(3,4). Its12 orbits of5 are precisely the projective
directions P1(F11), matching the12 Sylow C11 subgroups and their five
Klein eigenlines. This matches both the left G action and its right
normalizer action, not merely the number60.

The exact finite-permutation checks are supplemented by numerical121x121
Fourier-matrix checks, including(ST)^3=S^2. The q-values occur21 times at0
and10 times at every nonzero residue; the normalized Gauss sum is exactly1.

The auxiliary model is the untwisted D(Z11) quantum double. It is Abelian;
braiding alone is not a universal computer. Its121 labels are the
eleven-primary quadratic data, not all363 flat C-field sectors. Its60
Fourier-even states are not60 particle species. Its modular PSL2 action
is not a new metric-isometry group of M11, whose inherited normalizer
quotient is only C5. Establishing a physical boundary theory or topological
sector requires an actual reduction of the full11D action.

## Why the smaller quotient improves a conditional gauge option

For any SU5 holonomy that leaves the standard SU3 x SU2 unbroken,
Schur's lemma makes its defining5 representation block-scalar on3+2.
The image is therefore Abelian and factors through the fundamental
group's abelianization. For M55 that is C5. Writing its two characters
as zeta5^a and zeta5^b, determinant1 requires3a+2b=0 modulo5, so a=b.
The image is central and does not break SU5. This rules out that standard
flat Wilson-line route on M55, including non-Abelian F55 homomorphisms
whose image would have to commute with the desired SM algebra.

For M11, choose instead

    W=diag(zeta11^2,zeta11^2,zeta11^2,zeta11^-3,zeta11^-3).

It has determinant1, exact order11, and centralizer S(U3 x U2), the
standard SM global subgroup of SU5. Exact root-phase enumeration retains
eight off-diagonal roots and four Cartans, dimension12. Its eigenvalue
multiset differs from that of W^9, so no P can extend it to F55. This
explains why gauging the extra C5 loses the option.

The separate natural faithful embedding F55 -> SU6 x SU2 -> E6 also
fails to produce the SM: the6 is5+1, and neither wedge2(6) nor wedge3(6)
has a C11 invariant. From78=(35,1)+(1,3)+(20,2), the centralizer is
su2+u1 for a trivial external SU2 holonomy, or u1+u1 for its nontrivial
C5 characters. All five cases are checked; this is not a classification
of all E6 embeddings.

In the parallel E6 rank-breaking chart, two parallel singlet Higgs VEVs
have SU5 stabilizer. The M55 flat holonomy cannot replace the hypercharge
adjoint A there. M11 permits a Wilson-line alternative inside that supplied
SU5, but neither geometry supplies that gauge theory by itself. A smooth
11D metric/C3 compactification has no automatic E6 gauge bundle.

## Tradeoffs, torsion defects and the remaining physics

Both quotients have no invariant degree2 holomorphic functions (Reeb
charge4), no continuous flat C3 modes and no invariant cubic deformations
of the original polynomial. The standard marginal-flux and flat-C3
classes therefore stay absent. For M11 the first nonconstant holomorphic
functions are four degree3 functions, charge6 and scalar eigenvalue72;
for M55 the first is degree4, charge8 and eigenvalue112. Neither is a
full scalar spectral gap. Vol(M11)/Vol(S7)=3/176, versus3/880 for M55,
in Ric=6g normalization.

Tor H1(M11)=Tor H5(M11)=Z11 admits an untwisted particle/string BF shadow
11/(2pi) integral B2 wedge dA1: an M2 on the1-cycle is an external string,
and an M5 on its dual5-cycle is a particle. Dual generators have an
Aharonov-Bohm phase exp(2pi i/11). This is the standard torsion-linking
mechanism, related to [Camara, Ibanez and Marchesano](https://arxiv.org/abs/1106.0060).
It does not calculate masses, calibrated representatives, stability,
screening, flux-induced twists or the coupled topological action.

The ordinary flat-twisted Dirac lower bound49/4 still applies on M11.
A Wilson-line gauge centralizer alone is not a massless chiral spectrum.
The appropriate flux-coupled or localized-sector operator remains needed.
Recent [line-bundle model searches](https://arxiv.org/abs/2607.00078) likewise
separate gauge breaking from bundle equivariance and spectrum constraints;
their heterotic CY constructions are not transplanted to this Fano link.

Run `python analysis/toe_20261118_klein_C11_Wilson_and_linking.py` for the
certificate. The final remote run passed in4.77s. Maximum Fourier errors
for S,T and the inherited C5 are below1.7e-15. An independent GAP/HAP
functorial resolution calculation passed in70.26s, computing
H1..H4(C11)=(Z11,0,Z11,0) and checking explicitly that z->z^9 induces
multiplication by4 on H3. The exact GAP input was:

```gap
LoadPackage("hap");;
u:=Group((1,2,3,4,5,6,7,8,9,10,11));;
z:=GeneratorsOfGroup(u)[1];;
r:=ResolutionFiniteGroup(u,5);;
phi:=GroupHomomorphismByImages(u,u,[z],[z^9]);;
f:=TensorWithIntegers(EquivariantChainMap(r,r,phi));;
h:=Homology(f,3);;
v:=GeneratorsOfGroup(Source(h))[1];;
if Order(v)<>11 or Image(h,v)<>v^4 then Error("Wrong H3 action"); fi;
Print(List([1..4],n->Homology(TensorWithIntegers(r),n)),"\n");
QUIT;
```

This independently checks the second character used in the extension
splitting. See the [HAP functorial-map documentation](https://gap-packages.github.io/hap/doc/chap2_mj.html).
Its written topology argument above is essential evidence;
finite arithmetic alone cannot establish its geometric hypotheses.
The results identify a more flexible candidate and a precise mathematical
bridge. They do not establish observed chirality, couplings, cosmology
or a complete TOE.
