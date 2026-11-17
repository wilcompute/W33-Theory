# From the locally projective 11-cell to a smooth seven-dimensional gravity candidate

The user's local-projectivity correction is essential. The 11-cell has
hemi-icosahedral facets and hemi-dodecahedral vertex figures, both maps on
RP2. It is an abstract rank-four polytope, not an eleven-dimensional
manifold. A more useful connection to 11D passes through its symmetry group
PSL2(11), the Klein cubic threefold, and a smooth seven-dimensional link.
An explicit order55 subgroup acts freely on that link. This gives a
standard supersymmetric AdS4 compactification route using published metric
existence results. No observed Standard Model or complete TOE is established.

## Material read and prior ownership

The intake covered the Klitzing source and the existing lines of work:

- `exploration/w33_exceptional_triad_bridge.py` distinguishes abstract from
  classical polychora by their local types.
- `analysis/BT836_gc_hemicells_in_spreads.md` locates the local A5 hemicell
  structures in W33 schedules and records the full-group obstruction.
- `analysis/BT839_gc_operation_euler_flag_audit.md` and its Python producer
  transcribe the base and operation counts; this report corrects the
  topological interpretation of their alternating sums.
- `analysis/BT840_BT842_gc_carrier_completion.md` and
  `analysis/bt841_eleven_cell_a5_boundary_carrier.py` give explicit finite
  carriers, carefully stopping short of a PSL2(11) action inside W33.
- `analysis/BT848_universal_amalgam_ladder.md` distinguishes the A5 amalgam
  completions; `analysis/bt849_maniplex_barren_rung.py` supplies earlier
  group searches. Its description of the tomotope itself needs the
  correction below; its monodromy calculation is a separate claim.
- `exploration/w33_tomotope_klitzing_ladder.py`, the partial-sheet and
  partial-operation modules, and the six-table parser distinguish directly
  transcribed mod_b rows from the inferred mod_a doubling ladder.
- `docs/PART_DCCXII_KLITZING_PARTIAL_OPERATION_COMMUTATION.md`,
  `docs/PART_DCCXIII_KLITZING_SIX_TABLE_LOCK.md` and
  `manuscripts/parts/PART_DCCXXIX_PAULI_KLITZING_CODEC_LADDER_BRIDGE.md`
  document these table operations.
- `manuscripts/parts/PART_CCLXXVI_KLEIN_57CELL_BRIDGE.md` uses the Klein
  quartic/PSL2(7), a different object from the Klein cubic/PSL2(11) here.
- `analysis/verify_dccxxvi_critical_dimension_hierarchy.py` explicitly calls
  its dimensional assignments a numerical scaffold, rather than a physical
  derivation. The eleven-cell count alone is not a spacetime dimension.

Klitzing's live page returned HTTP406 to the reader. The authorized cached
`C:/Users/wiljd/Downloads/Abstract polytopes.html` was read instead. It
describes the antipodal/elliptical construction, the11/57-cell families,
the two tomotope partial packets, operation tables and higher-rank examples.
The archived source and the earlier synchronized files were not modified.
[Leemans and Schulte](https://arxiv.org/abs/math/0606660) provide the primary
classification of the locally projective regular11/57-cell cases.

## Local projectivity changes the Euler calculation

The face-number sum V-E+F-C assumes that a facet attaches like a ball when
interpreted as the usual CW Euler sum. A projective facet has RP2 boundary,
not S2 boundary. In the order-complex realization its cone attaches with
relative Euler number1-1=0, whereas a ball contributes1-2=-1. Thus each such
facet requires a correction of+1 to that naive sum.

The script independently counts simplices in the proper-face order complex:
vertices are faces of all four ranks, edges are incident rank pairs,
triangles are rank-three chains and tetrahedra are full flags. Thinness
gives two triangles per full flag. The resulting exact counts are:

| Object | Face-number sum | Order-complex f-vector | Actual order-complex Euler |
| --- | --- | --- | --- |
| 11-cell | 0 | (132,781,1320,660) | 11 |
| 57-cell | 0 | (456,3819,6840,3420) | 57 |
| Tomotope | 0 | (40,228,384,192) | 4 |

The11-cell has22 singular order-complex vertices with RP2 links:11 original
vertices and11 facet centers. The corresponding numbers are114 for the
57-cell and8 for the tomotope. These links obstruct ordinary3-manifold
neighborhoods. The adjacent regular part cannot carry an ordinary global
orientation extending across their RP2 boundary links. A physical use needs
a covering, different realization, or an explicitly specified parity/defect
completion; the raw complex is not a smooth spin internal manifold.

For the11/57-cell, reversing the omnitruncated table counts gives exactly
the order-complex f-vector. This explains why the table sums are the
negatives -11 and-57. They are not a physical topological charge created by
Wythoff operations. For the tomotope, the cached omnitruncated leading
count96 is the previously recorded half-flag quantity; it is not identified
with the192 flags of the full order complex.

Another correction is supported directly by
[Monson, Pellicer and Williams, The tomotope](https://bmonson.ext.unb.ca/fields/tom.pdf):
the tomotope itself is an abstract uniform4-polytope, with192 flags and
automorphism group order96. Its monodromy group has order18432 and fails the
intersection property. The latter does not make the original tomotope a
non-polytope. Older repo tests that label the face-table sums as topological
Euler numbers, or18432 as its automorphism order, should not be used for
physical conclusions. Their historical arithmetic remains untouched here.

## A symmetry-based route to an actual seven-manifold

The automorphism group of the11-cell is PSL2(11), order660. The same group
acts faithfully on the smooth Klein cubic threefold

    X={f=x0^2 x1+x1^2 x2+x2^2 x3+x3^2 x4+x4^2 x0=0} in CP4.

This is published mathematics, not a new group identification: see
[Debarre, Some varieties with PSL(2,F11)-actions](https://perso.imj-prg.fr/wp-content/uploads/debarre-pub/psl.pdf)
and [Roulleau](https://arxiv.org/abs/1001.4853). No map from the11-cell's
face poset to this manifold is asserted. The concrete bridge is the shared
group together with an explicit subgroup action below.

The polynomial is smooth projectively by a short exact argument. Its
derivatives are2xi x(i+1)+x(i-1)^2. If one critical coordinate is zero,
all are zero. If none is zero, multiplying the five equations would give
32(product xi)^2=-(product xi)^2, a contradiction in characteristic zero.
The script also computes the Jacobian Hilbert dimensions
(1,5,10,10,5,1), with total32, and verifies the degree-three deformation
space dimension10.

Let Y={f=0} intersect S9 in C5. This is a smooth seven-dimensional link
and the primitive circle bundle over X. Its induced Euclidean metric is
not asserted to be Einstein. Instead,
[Liu and Xu](https://arxiv.org/abs/1706.01933) prove that every smooth cubic
threefold admits a positive Kähler-Einstein metric. The standard circle-link
construction then supplies a regular Sasaki-Einstein metric on Y. The
[link/KE correspondence](https://www.mdpi.com/2073-8994/11/7/947) and
Freund-Rubin construction are established inputs.

After normalizing Ric(Y)=6g, the standard eleven-dimensional solution is

    ds11^2=R^2[(1/4) ds_AdS4,unit^2+ds_Y^2],
    G4=(3 R^3/8) vol_AdS4,unit.

Thus4+7=11 follows from the geometric construction and field equations,
rather than from the number of abstract cells. The supersymmetric
orientation has the usual two internal real Killing spinors. This is a
classical AdS4 background, not an observed4D Minkowski or de Sitter vacuum.

## An explicit free quotient: C11 semidirect C5

Take zeta=exp(2pi i/11), weights a=(1,9,4,3,5), and

    D=diag(zeta^a_i),    (Pz)_i=z_(i+1).

Then D^11=P^5=1 and P D P^-1=D^9. Both preserve f and have determinant one.
The55 normal forms D^a P^b are distinct. Their action on Y is free:

- A nonidentity D power has no eigenvalue one, so fixes no nonzero vector.
- If b is nonzero, D^a P^b is conjugate by a D power to P^b. Its fixed
  line is D^s(t,t,t,t,t), where s=a/(1-9^b) modulo11. On that line f=5t^3.
  Thus it cannot meet the punctured cone.

The script checks all44 conjugating cases, as well as all10 diagonal ones.
The cone's holomorphic residue4-form is preserved because det(D)=det(P)=1
and f is fixed. The finite group preserves the lifted Einstein structure.
Its odd order also gives a unique spin lift; the volume-preserving action
retains the parallel cone spinors. Consequently Y/(C11:C5) is a smooth
supersymmetric Freund-Rubin route, without localized reflection singularities.

The C11 weights also give an exact equivariant control. The only invariant
cubic monomials are the five displayed terms; the weight-zero Jacobian
relations span all five (determinant magnitude33). Hence none of the10
cubic deformation directions is C11 invariant. H^(2,1)(X) is the degree-one
Jacobian space, with these five nonzero weights. The conjugate weights
complete all ten nonzero residues modulo11. Therefore the quotient retains
no rational H3 or H4 from the cover. This does not compute its complete KK
spectrum or prove absence of every physical modulus.

## Integral topology, spin and flat C-field sectors

Using H^2=3L and integral(H L)=1 on the cubic, the integral Gysin calculation
gives the cover's cohomology:

    H0=H7=Z,
    H3=Z^10,
    H4=Z^10 plus Z3,
    H1=H2=H5=H6=0.

The link is2-connected and has a unique spin structure. Its flat degree-four
C-field characters are U(1)^10 times Z3. The characteristic-class computation
is c(TX)=1+2H+4H^2-2H^3 and p1(X)=-4H^2=-12L. Its pullback to the link
vanishes, including the order-three torsion. Since there is no2-primary
torsion, lambda=p1/2 also vanishes here. This is a characteristic-class
check, not a full Page-charge or wrapped-brane dictionary.

For the free quotient, pi1=C11:C5 and its abelianization gives H1=Z5. Its
rational Betti numbers are(1,0,0,0,0,0,0,1): it is a rational homology
seven-sphere whose universal cover has nonzero middle cohomology. At prime3,
the group order55 is invertible, and its action on the cover's Z3 torsion is
trivial. Transfer therefore retains exactly a Z3 three-primary part in H4.
The full5- and11-primary integral torsion downstairs is not computed.
There are no continuous flat C-field modes downstairs, but at least the
three-primary discrete sectors remain. Three sectors are not three families.

## A normalized gravitational quantity

For the regular link, the base Kähler form is(pi/4)c1(X)=(pi/2)H and the
Reeb orbit has length pi. Thus Vol(Y)=pi^4/16 when Ric=6g. Freeness gives

    Vol(Y/(C11:C5))=pi^4/880,
    Vol(Y/(C11:C5))/Vol(S7)=3/880.

The standard large-N AdS4 formula then gives
F=pi sqrt(1760/27) N^(3/2)+o(N^(3/2)); see
[Operator counting and eigenvalue distributions](https://arxiv.org/abs/1106.5484).
This is a conditional holographic quantity for this background, not a
particle-physics prediction. Quantum flux shifts and finite-N terms have
not been evaluated.

## Spin check on the preceding CP3 comparison

The separate spin producer closes the determinant-one Witting matrices
modulo7 to51840 elements with scalar kernel+/-I. The exact projective closure
was25920; scalar SU4 matrices over Q(omega) can only be+/-I, so this fixes
the characteristic-zero order as well. CP3 has K^(1/2)=O(-2), and both kernel
elements act trivially on it. The projective Witting action therefore has
an equivariant spin structure.

The standard S5 quotient has a different answer: near a generic mirror an
involution rotates one real normal plane by pi. Both Spin lifts square to-1,
so neither is an order-two lift. This blocks an ordinary spin orbifold
structure there. A Spin-c or parity/gauge-twisted construction is an extra
choice, not a repair already supplied. The local odd/even cone criterion is
reviewed in [Belgun, Ginoux and Rademacher](https://arxiv.org/abs/math/0409136).

## Remaining physical requirements and reproduction

The new route has finite-symmetry-controlled geometry, a smooth free quotient
and a supersymmetric AdS construction. It still has no derived SM gauge
sector, chirality, Yukawas or observed cosmology. The continuous metric
isometry is the Reeb U1; rational b2 is zero, so the usual Betti-vector route
does not add a nonabelian SM gauge algebra. Additional ingredients need an
explicit action and consistency checks. The parallel E6 messenger/Higgs
inventory is not automatically part of this compactification.

Run the two owned producers:

    python analysis/toe_20261117_11cell_klein_cubic_link.py
    python analysis/toe_20261117_projective_spin_and_11cell_topology.py

Their corresponding JSON files record exact polynomial, Smith, characteristic
class, group, local spin and incidence checks. KE metric existence and the
standard supergravity construction are cited mathematical/physical inputs;
the scripts do not numerically solve for the metric or its full spectrum.
