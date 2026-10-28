# Acoustic current, shared singlets, finite density and gravitational backreaction

Continues `a03ff9dc0`. Producers:
`analysis/w33_20261027_acoustic_density_backreaction.py` and
`analysis/w33_20261027_shared_singlet_masses.py`; their complete outputs have
the corresponding names under `data/`. This packet executes investigations
on all five requested fronts. It does not complete the full chiral measure,
derive the string scalar potential, solve gravity or finish the content audit.

## 1. Exact harmonic response at finite density, and an exact cover obstruction

The previous one-up/one-down Hubbard probes did not supply a common electric
metric. Test a different, explicitly free model: the full-Fock grand-canonical
spinless determinant on all27 native sites and135 edges. Its single-particle
energies are -10,-1,5 with multiplicities1,20,6. Use the actual four rational
harmonic currents h, denominator9, and M=h^T h:

```
 10   5  -6   0
  5  10   0  -6
 -6   0  12  -6
  0  -6  -6  12
```

Polynomial spectral projectors have denominators27,54,90. With J_i the
Hermitian Peierls current vertices, exact integer arithmetic certifies
Tr(P_a J_i P_b J_j)=c_ab M_ij, where

```
c = [ 0    0     0
      0   5/3   1/6
      0   1/6    0 ]
```

Every current annihilates the uniform ground orbital. A second unimodular
period basis independently verifies the tensor covariance. Consequently,
writing f_g=f(-10), f_m=f(-1), f_p=f(5),

* regular electric coefficient: (f_m-f_p) M/648;
* regular zero-frequency harmonic susceptibility: (4f_g+5f_m-9f_p) M/54;
* additional static thermal term: -5 f_m(1-f_m) M/(3T).

These are exact formulas for this named operator, confirmed numerically at
nine(T,mu) choices. At T=0 with -1<mu<5 all21 lower orbitals are filled:
the static susceptibility is M/6, the electric coefficient M/648, and their
ratio108. The fully occupied20-fold shell gives one Slater ground state,
rather than the partially filled degeneracy that complicated the previous
fixed-sector probe. At finite temperature the zero-Matsubara limit can jump;
near half occupancy of that shell, the static harmonic curvature is negative.
Matching tensor shape is not the same as a stable thermal vacuum.

The calculation includes a spatial pure-gauge current and its temporal
density vertex, with the full diamagnetic contact. At nonzero Euclidean
frequency the spatial response alone need not vanish. The mixed-density
terms restore the null vector(1,-omega) in the stated Lehmann convention;
both tested bosonic frequencies satisfy the Ward identity for every sample.

**A necessary limit on this advance:** uniform harmonic susceptibility is a
finite-volume Wilson-line potential curvature. It is not a Maxwell magnetic
k^2 coefficient. No propagation speed follows from108. Four deck directions
plus supplied external time also do not derive physical3+1 spacetime.

Checking the actual nearest-edge Bloch operator makes the boundary sharper.
At two exact rational unit-circle momentum choices, integer congruence
certificates give the inertias of K(k)-71/25:

| Bloch point | Negative eigenvalues | Positive eigenvalues |
|---|---:|---:|
| First rational witness | 20 | 7 |
| Second rational witness | 22 | 5 |

Both witnesses include their complete integer complex change-of-basis
matrices. The resulting congruence matrices have exactly sign-separated
Gershgorin disks, using the rational bound |a+ib|<=|a|+|b|. A homotopy to the
diagonal preserves inertia. Nonsingularity proves the proposed bases are
invertible; Sylvester's law transfers the inertia counts. Floating
eigenvectors only proposed these integer bases and do not enter the proof.

Thus, with one-based band indices, lambda21(k_A)>71/25>lambda22(k_B).
There is **no global21-band insulating gap for this nearest-edge cover**.
The isolated-cell21-filled result cannot be promoted to an infinite-cover
band insulator. Other kernels, interactions and fillings remain possible.
This exact negative control is as material as the finite-cell tensor identity.

Prior owners: the Oct27 microscopic/current packets and canonical harmonic
geometry. Earlier TOE64--75 determinant/response caveats concern distinct
80-site or smaller-patch operators. The dual27 electrical-network note uses
a degree8 graph with108 edges, not this degree10 graph with135 edges.

## 2. An implemented finite acoustic comparison current

Audit the projector-comparison formula in
[Craig2026, Section5](https://arxiv.org/html/2610.09093v1#S5), rather than
treating anomaly cancellation alone as a measure construction. Implement
b_eta=i integral Tr P[d_t P,d_eta P]dt for a finite radial acoustic homotopy.
This uses a two-site coarse Wilson operator with common antiperiodic signs
in its first direction. Frechet derivatives use exact spectral divided-
difference formulas evaluated numerically; no eigenvector derivative gauge
is chosen. Controls cover the5 and the27=10+bar5+1+5+bar5+1 SU5 multiplets.
The fixed signed cubic intertwiner changes their basis, not these traces.

The computed exterior derivative of the current agrees with the endpoint
projector curvature to4.6e-9(5) and5.2e-8(27). Eight-versus-sixteen-point
radial quadrature differs below1.1e-13. Independently, integrate the current
around a closed parameter rectangle and compare its phase with projector
Kato transport at12 and24 steps per side. At24 steps the phase discrepancies
are3.2e-10 and5.4e-10, smaller than the observed discretization changes.

This constructs and checks an actual finite comparison one-form. It is
**not** the paper's coarse/fine refinement tower or its complete measure
current. Gauge-divergence correction, uniform convergence/locality,
noncontractible-loop phases and admissible-sector reconstruction remain
unimplemented. The free acoustic reference has a nonzero commutator with
an actual local SU5 transformation, unlike the onsite heavy reference.
Consequently the preceding heavy-frame proof cannot simply be reused.
The tested gapped finite chart is not asserted to lie in every admissibility
domain required by the external theorem.

## 3. Shared singlet coordinates and correlated mass operators

Pass12311 already owns a48-multiplet matching under selected space-group
rules; its graph has134 edges allowing degree up to8, with a selected
matching of degree at most2. The new probe reconstructs operators rather
than supplying21 independent threshold masses.

The scalar ledger has25 Scalar and25 conjugate-scalar singlet records.
They supply25 independent complex vevs. Exact charge, sector and conjugacy-
class checks match their CPT partners. The installed non-SUSY orbifolder
dump source and its COrbifold::CheckCPPartner routine were inspected:
the latter explicitly compares inverse constructing elements up to space-
group conjugacy. A fixed canonical representative is therefore too strict
for this identification.

Enumerate degree1/2 monomials on the25 shared coordinates, including
nonholomorphic |S|^2 operators and excluding bare mass terms. Necessary
space-group membership allows independent theta-orbit representatives,
tested with exact Hermite quotient-lattice classes. Gamma-eigenstate sums
and non-SUSY world-sheet vertices remain uncomputed. These are necessary
kinematic tests, not certificates of nonzero string amplitudes.

The degree-at-most2 graph has124 edges. A weighted matching covers all48
multiplets with10 degree1 and14 degree2 operators. Every selected edge
stores its monomial and point-group rotations. Shifting one partner by e5
rejects every tested edge, retaining the live selection-rule control. The
degree2 graph count should not be confused with the earlier degree8 count.

For a concrete shared **test potential**, take t_i=|S_i|^2/v^2 and

V/v^4=-sum_i t_i + t^T A t/2,
A=I+(1/1000000) Q^T Q.

Q is the actual5-by25 rational charge matrix. Exact arithmetic gives the
strictly positive solution t=A^-1 1. Since A>=I, this is the unique global
minimum in the nonnegative squared-modulus coordinates. Scalar phases
remain flat; this is not an isolated vacuum in the full field space.
The charge matrix has rank4, leaving one Abelian direction; nonabelian
singlets leave SU2R unbroken.

At v/Lambda=.1, with the selected operator coefficients set to1 and the
remaining pair coefficients set to0, all masses share this same minimum.
Their largest-to-smallest ratio is approximately10.067. The disjoint dual-
representation contractions are nonsingular, giving full conditional rank
on148 Weyl gauge components carried by the48 multiplets.

The test potential, scales, coefficient values and phase choice are supplied.
This is not the string potential, a complete exotic spectrum, SU2R breaking
or a reproduction of the previous independent-threshold fit. In particular,
singlet vevs cannot independently split components of an SU2R multiplet.
The missing string vertex calculation remains decisive.

## 4. Einstein stress matching and the graviton-loop correction

Couple the previous circle potential to a supplied five-dimensional Einstein
EFT. For AdS4(ell) x S1(R), the two independent Einstein equations require

3 M5^3/ell^2=-rho5, p5=-2rho5,
rho5=VJ/(2pi R), p5=-dVJ/dR/(2pi).

The second equation is R VJprime=2VJ, equivalent to stationarity of the
Einstein-frame potential VJ/R^2, not the Jordan potential alone.
The canonical radion gives mphi^2 ell^2=-2 x^2 vsecond/v at a stationary
point, where v=(A S-B zeta(5))/x^6 and x=2pi mR.

The positive-degree count matters. A5D graviton has five physical
polarizations, whose massless Casimir contribution cannot be omitted in a
one-loop field inventory. See the original gravitational Casimir work of
[Appelquist and Chodos](https://doi.org/10.1103/PhysRevD.28.772) and the
explicit field-count discussion in
[Wongjun2014](https://doi.org/10.1140/epjc/s10052-014-3237-0).

| Supplied field inventory | A massive fermion weight | B massless boson weight | Finite minimum |
|---|---:|---:|---|
| Previous matter, classical gravity only | 4 | 2 | Yes |
| Same matter plus graviton loop | 4 | 7 | No |
| Two massive Dirac fields, scalars and graviton | 8 | 7 | Yes |
| Same plus massless SU5 gauge fields | 8 | 79 | No |
| Massive Dirac27, SU5/twoU1 gauge fields, graviton, two scalars | 108 | 85 | Yes |

For this shape function, A>B is the exact existence criterion: D6 decreases
strictly from6zeta(5) to0, so Vprime has one zero precisely when A>B.
If A<=B the potential is strictly increasing and has no stationary radius.
Thus neither the original matter-only minimum nor the two-Dirac toy minimum
can stand in for a complete unified field inventory.

With A=8,B=7, mR=0.170917472892187. The two Einstein stress equations agree
to the recorded high-precision residual, and mphi^2 ell^2=55.5905358218>0.
At the illustrative M5/m=1000, the solutions have M5 R>100 and ell/R>8e5,
supporting a weak-curvature/large-radius derivative expansion. They have
negative vacuum energy. The Dirac27 completion is vectorlike5D matter,
not a derived4D chiral spectrum. Bulk cosmological constant subtraction,
field content and masses are supplied. This is a leading flat-circle
Casimir stress approximation on a weakly curved product background, not
the exact curved-space effective action or a native derivation of gravity.

## 5. Content audit and correction-chain review

All text on pages127-134 was read; page132 was rendered and inspected.
Pages127-130 distinguish fitted flavour existence from stable moduli and
retract the axiflavon interpretation. Page131 explicitly excludes numerical
coincidences as evidence. The following pages state engineering/compiler/
code results, which do not establish a field-theory vacuum.

Five additional full patches were read:7fb937f8a,31c150bc8,52515ea07,
00cf043ac,78ae741e3. Their finite Jordan tests, inverse-moment falsifiers,
bounded arithmetic tail and sampled signing results reinforce the exact/
numerical/global distinction used here. Imported complete producers were
not thereby read. Frozen page204 was also read in full. The ledger now records64/210 PDF pages and19/481 complete
historical patches. Full content review remains unfinished.

The complete12310--12333 correction chain was also checked in current source.
The empty-window assertion of12316 was withdrawn in12322. The current e6
window is conditional; e5 winding projections and the string-scale potential
remain unresolved. Neither the test singlet potential nor a5D circle model
settles that heterotic vacuum question.

During validation, upstream70278ece1 added Pass12334--12339 and a revised
paper. Its complete current tower/potential drivers, review note and displayed
JSON results were checked. The corrected tower rule matches15 lineage
variants; the truncated potential is monotone on the11 displayed radii,
with cutoff controls. This is not an analytic all-radius monotonicity proof
or the complete modular-invariant string potential with massive levels.
It strengthens the radius difficulty for the actual brother and must not
be conflated with the supplied field-theory AdS examples above. The17 new
three-doublet parent leads still require hypercharge and full vacuum checks.

The live PDF now has SHA256 c813e604...; pages86 and204 of that edition were
read in full. Historical64-page flags continue to refer to the frozen
c5b44ee9... edition. The producer can recover that exact PDF from its pinned
Git object without altering the user's live paper. The edition change is
recorded explicitly rather than silently transferring reading flags.
