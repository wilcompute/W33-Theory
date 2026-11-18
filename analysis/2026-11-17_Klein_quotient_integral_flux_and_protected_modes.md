# Integral flux topology and protected modes of the Klein-link quotient

For the free quotient M=Y/(C11:C5) of the Klein cubic seven-link, the new
calculation gives H4(M,Z)=Z15 and lambda(TM)=p1(TM)/2=0, including torsion.
Consequently the flat degree-four C-field group is Z15. This finishes the
additive integral cohomology left open in parent commit3095ad3e9; it does
not finish the linking/quadratic refinement, electric Page-charge, metric
spectrum or Standard Model problem. The zero internal gravitational shift
does not select one of the fifteen flat sectors.

## Inputs and prior work

The parent `analysis/2026-11-17_11cell_Klitzing_Klein_cubic_11D.md` and its
two producers supply the explicit invariant cubic, free F55 action,
cover cohomology and KE existence input. They distinguish local projectivity
of the11-cell from an11D manifold and distinguish a shared symmetry group
from an unconstructed map of incidence structures.

The earlier `analysis/PASS11750_11757_INTEGRAL_GEOMETRY_AND_FLUX_DYNAMICS.md`
already uses Cartan-Leray on a different free CY quotient. The translation
coinvariant module11560 explicitly concerns a nonfree action, so its chain
quotient is not applicable here. The parallel
`analysis/toe_20261117_Cfield_integral_torsion_linking.py` owns the separate
circle-bundle torsion-linking calculation; it does not determine this
F55 quotient's integral groups. These methods are established mathematics,
not a claim of new topology machinery.

## The missing order-eleven coinvariants

Let X be the smooth cubic threefold, L=H3(X,Z), and let B be its unimodular
alternating intersection form. The parent character calculation gives
rank(L)=10 and characteristic polynomial Phi11 for D. Thus

    A=L/(D-1)L = Z11,

because det(D-1)=11. P has order5, preserves B, and P D P^-1=D^9.
It is important not to replace L by an arbitrary rationally equivalent
integral representation: the intersection form supplies the needed control.

There is a perfect symmetric mod-Z pairing on A,

    b(x,y)=B(x,(D-1)^(-1)y) mod Z.

It is well-defined since B is integral and D preserves B; its radical is
(D-1)L because B is unimodular. Transposition changes it only by an integral
form, so it is symmetric modulo Z. For k not divisible by11,

    (D^k-1)=(D-1)(1+D+...+D^(k-1))

implies that replacing D by D^k multiplies this pairing by k^-1 mod11.
Since P^-1 D P=D^5, this gives b(Px,Py)=9 b(x,y). If P acts on the cyclic
group A by alpha, then alpha^2=9 and alpha^5=1 in F11. The only solution
is alpha=3. Therefore the full F55 coinvariant group L_F55 vanishes:
the relation (P-1) is multiplication by2 on Z11, an automorphism.

The producer checks Smith form and all ten inverse-power pairing identities
on an explicit rank10 unimodular symplectic companion model. That model is
an arithmetic control for the argument, not a calculated cubic period basis.
The conclusion for the actual cubic lattice follows from the preceding
basis-independent proof and its established symplectic hypotheses.

A negative control checks why the integral argument matters. The natural
semilinear action zeta -> zeta^9 on Z[zeta11] has the same rational character
as the actual rank10 representation, but acts trivially on its Z11
coinvariant. It would leave a spurious order11 sector in this calculation.
The producer constructs that action and verifies its order and conjugation
relation, then verifies that it fails to preserve the unimodular symplectic
form. The actual Poincare-duality lattice cannot have that coinvariant
action, by the pairing proof. Rational character matching alone is insufficient.

A positive control is explicit as well. On the stable ideal
(zeta11-1)^3 Z[zeta11], the same field automorphism has matrix
P=(1+D+...+D^8)^3 T, where T is the preceding natural semilinear matrix.
There is an invariant integral alternating form with circulant coefficients
(0,3,-4,3,-2,2,-2,2,-3,4,-3). Its rank10 matrix has determinant1, and both
D and P preserve it. Direct Smith reduction of the concatenated matrix
[D-1 | P-1] gives ten unit entries, independently verifying zero full-group
coinvariants in this admissible model. The certificate stores P and the
form coefficients. Identification of this model with the actual cubic
period lattice is not needed or asserted; the universal pairing proof
already fixes the relevant coinvariant action for every admissible lattice.

## Cartan-Leray and all additive integral groups

Use the homological spectral sequence

    E2_(p,q)=H_p(F55,H_q(Y,Z)) => H_(p+q)(M,Z).

The standard construction and transfer identities are explained in
[Brown's group-cohomology lectures](https://pi.math.cornell.edu/~kbrown/papers/cohomology_hangzhou.pdf),
especially sections3 and5. For the group extension C11 -> F55 -> C5,
the prime11 part of H_(2k-1)(C11,Z)=Z11 is acted on by9^k. In degrees1
and3 these coinvariants vanish. Localizing at5 kills positive C11 homology,
leaving C5. Thus H1(F55)=Z5, H2(F55)=0, H3(F55)=Z5 and H4(F55)=0.

The cover is2-connected. Its circle-bundle homology sequence gives
0 -> Z3 -> H3(Y,Z) -> L -> 0 equivariantly. At prime3, order55 is invertible,
so taking coinvariants is exact; the Z3 action is trivial because F55 has
odd order and Aut(Z3)=Z2. At the other primes the preceding lattice argument
applies. Hence H3(Y,Z)_F55=Z3.

In total degree3 the only nonzero spectral-sequence entries are (0,3)=Z3
and (3,0)=Z5. The only possible incoming differential to (0,3) is d4 from
(4,0)=H4(F55)=0. All other relevant maps vanish by2-connectivity or first
quadrant degree bounds. This gives

    0 -> Z3 -> H3(M,Z) -> Z5 -> 0,

which is Z15 since the two orders are coprime. In lower degrees H1(M)=Z5
and H2(M)=0. Rational middle Betti numbers vanish by the parent calculation.
Integral universal coefficients and oriented seven-dimensional Poincare
duality now determine every additive group:

| Degree | Homology H_k(M,Z) | Cohomology H^k(M,Z) |
| --- | --- | --- |
| 0 | Z | Z |
| 1 | Z5 | 0 |
| 2 | 0 | Z5 |
| 3 | Z15 | 0 |
| 4 | 0 | Z15 |
| 5 | Z5 | 0 |
| 6 | 0 | Z5 |
| 7 | Z | Z |

The ring also follows at prime5: D-1 has determinant11, so its middle
lattice coinvariants and invariants vanish over Z_(5). Normal C11 invariants
then kill both middle rows in cohomological Cartan-Leray, including their
positive group-cohomology terms. Below degree7, the edge map from BF55 is
an isomorphism. The C5 quotient gives a generator u in degree2 with5u=0;
u^2 and u^3 are nonzero generators of the5-primary parts of H4 and H6.
Let v generate the3-primary H4. All other products of positive-degree
classes vanish by dimension or coprime torsion. This specifies the integral
cohomology ring as well as its additive groups. It does not specify the
torsion linking units or a Chern-Simons quadratic refinement.

In particular, H3(M,R/Z)=Z15 is the group of flat degree-four differential
characters. The parent correctly established only its Z3 primary subgroup;
the new result adds Z5 and excludes11-primary torsion. These sectors are
holonomies, not nonzero real G4 curvature and not a matter-family count.

## An integral gravitational-shift check downstairs

There is an independent argument that does not need the preceding integral
cohomology table. The polynomial f is F55 invariant, so its differential on
the punctured cone has a trivial complex line as target. Equivariantly,

    T(cone) + C = C^5_rho.

Restricting radially to the link and descending through the free action gives
TM + R3 = (E_rho)_R stably. The representation rho lands in SU5. On C11 its
weights are(1,9,4,3,5); on C5 they are(0,1,2,3,4). Their elementary Chern
coefficients c1,c2 are(22,176) and(10,35), respectively: both reduce to zero
modulo the corresponding prime. Thus c2(rho) restricts to zero on both Sylow
subgroups. Restriction followed by transfer multiplies by their indices5
and11, so c2(rho)=0 integrally on BF55.

For the underlying real SU bundle lambda=-c2. Pullback proves
lambda(TM)=0, including torsion invisible on the universal cover. The spin
structure is unique because H1(M,Z2)=0. A string structure exists, with a
single homotopy class because H3(M,Z)=0. This is the topological term
"string structure", not a derivation of physical string dynamics.

Applying [Witten's shifted flux law](https://arxiv.org/abs/hep-th/9609122)
therefore introduces no internal lambda/2 shift. This is not a calculation
of the Chern-Simons quadratic refinement, the one-loop electric charge,
the M2 Page lattice or finite-N corrections.

## Protected invariant harmonics and a second volume calculation

Let t count ordinary polynomial degree. The ambient invariant series is

    H_ambient(t)=(H_C11(t)+4/(1-t^5))/5,
    H_cone(t)=(1-t^3) H_ambient(t).

The producer computes H_C11 by reducing each coordinate exponent modulo11;
independent enumeration of C5 monomial orbits verifies all coefficients
through degree18. Multiplication by f is injective before quotienting, and
finite-group invariants are exact in characteristic zero, justifying the
(1-t^3) factor. The quotient ring begins

    H_cone=1+t^4+3t^5+3t^6+5t^7+6t^8+9t^9+13t^10+... .

There are no nonconstant functions in degrees1,2 or3. The first invariant is

    g=sum_i x_i^2 x_(i+2) x_(i+4), indices modulo5.

It is not a multiple of f: such a multiple would require an invariant linear
factor, which does not exist. The exact rational series obeys
H(1/t)=t^2 H(t), as expected for the Gorenstein cone with a-invariant-2.
The residue four-form has ordinary degree2, so normalizing its Reeb charge
to4 gives charge2 per coordinate. The series pole gives

    lim_(t->1) (1-t)^4 H_cone(t)=3/55,
    Vol(M)/Vol(S7)=(3/55)/2^4=3/880.

This independently reproduces the parent's circle-bundle volume calculation.

For a homogeneous holomorphic function of Reeb charge q, harmonicity on
the Ricci-flat cone gives scalar-link eigenvalue q(q+6). The first invariant
has q=8 and eigenvalue112 for Ric(M)=6g. Its standard AdS4 spin-two lift has
m^2 L_AdS^2=28 and dimension7. This only identifies a holomorphic subsector;
nonholomorphic eigenfunctions can lie below it. No full spectral gap or
complete KK stability calculation is being claimed.

There is also a deformation test: the standard supersymmetric marginal-flux
construction requires a holomorphic function of Reeb charge4; see
[Ashmore, section3.1](https://arxiv.org/abs/1809.03503). Here that would have
ordinary degree2, and the invariant space is zero. The quotient removes all
15 such quadratic functions of the cover. Its real H3 also vanishes, removing
continuous flat C3 directions. This rules out the indicated holomorphic
and closed-three-form deformation classes, not all quantum moduli or all
possible compactification deformations. The number15 of projected functions
has no demonstrated physical relation to the15 discrete torsion sectors.

## Reproduction and physical limits

Run `python analysis/toe_20261117_klein_quotient_integral_and_protected.py`.
The JSON records exact Smith/pairing, Sylow Chern, group-homology,
UCT/Poincare-duality, invariant-series and volume checks. The first Remote
Desktop Commander run passed in7.02s. The independent GAP/HAP control
`analysis/toe_20261117_klein_F55_hap_control.g` constructs the affine F55
permutation group and a finite-group resolution, then computes its integral
H1 through H4 as(Z5,0,Z5,0). It passed in35.70s under GAP4.16.0; optional
plotting-tool warnings did not affect the homology computation. This checks
the group terms independently of the Python LHS arithmetic, not the entire
manifold homology. See the [HAP resolution documentation](https://gap-packages.github.io/hap/doc/chap5_mj.html).
The topological derivation above is
part of the evidence; arithmetic assertions alone are not a substitute for
its hypotheses. No explicit Einstein metric, full KK spectrum, observed
gauge/chiral sector, cosmology or complete TOE is supplied.
