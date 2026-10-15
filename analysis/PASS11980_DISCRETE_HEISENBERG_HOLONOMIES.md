# Pass11980: discrete order-nine holonomies survive zero continuous invariants

## Result and ownership

TOE81 constructed the native 27-octagon tritangent complex X with 135 edges,
45 edge-disjoint filled triangles, and integral H1(X)=Z^64. TOE82 computed its
characteristic-zero H27 character and proved H1(X;C)^H27=0. That theorem is
correct. It leaves both integral torsion after taking homology coinvariants
and modular invariants undetermined.

This pass computes the **homology coinvariant lattice** exactly:

    H1(X;Z)_H27 = Z/3 + Z/9 + Z/9.

Consequently there are exactly **243 H27-fixed flat U(1) gauge-equivalence
classes**, despite there being no continuous invariant direction. Their orders
are 1 (one class), 3 (26 classes), and 9 (216 classes). This is a statement
about fixed *gauge classes*, not strictly invariant edge phases.

Prior source owners:

- `analysis/w33_20261015_toe81_native_tritangent_css.py`: X and its free H1.
- `analysis/w33_20261015_toe82_native_H27_h1_character.py`: the complex character.
- `analysis/w33_pass11560_translation_coinvariant_arrow_torsion.py`: an earlier,
  distinct abelian translation **coinvariant-chain** construction. Taking
  homology and taking coinvariants do not commute here. Its (Z/3)^4 does not
  answer this question.
- `analysis/PASS461_INTEGRAL_REPRESENTATION_LATTICES.md`: distinct cyclotomic
  trace-lattice Smith factors containing 3 and 9; not this H1 quotient.
- `docs/index.html` BT865: the **different** 81D building H1 restricts to three
  regular H27 modules. Its modular center ranks 54,27,0 must not be imported
  into this 64D tritangent complex.
- `analysis/w33_20260901_building_chain_injections.py`: the **same abstract
  cubic geometry's** 64D Levi-building homology was already constructed and
  embedded into a 1080D module. The rediscovery guard prompted a full reread.
  This pass explicitly connects the native triangle realization to that
  incidence-graph model: send each oriented triangle edge a->b to
  a->face-center->b. The induced 64x64 cycle transport has determinant +/-1
  and intertwines both H27 generators integrally. This is an actual map,
  not a claim that matching dimensions alone identify representations.
- `analysis/BT816_cubic_surface_flags_reconstructed.md`,
  `analysis/PASS4992_4999_EXECUTED_OUTCOMES.md` and
  `analysis/PASS5000_5007_EXECUTED_OUTCOMES.md` already own the classical
  135 cubic flags and other tritangent uses. The guard's tritangent@135
  warning is prior geometry, not novelty for this quotient.

Result searches included `3,9,9`, `3, 9, 9`, `40,16,0`, the radical sequence,
coinvariants, fixed holonomies and Schur multipliers. No earlier certificate
for this specific integral quotient was identified. Generic Smith and
cohomological methods are established mathematics.

## Exact construction

Use TOE82's explicit H27 multiplication and five right-coset directions.
Collapse one free edge per triangle integrally, then choose a spanning tree
of the remaining 90-edge graph. The 64 fundamental cycles form a **unimodular
integral** H1 basis: cycle coordinates and basis satisfy C B=I64, and all
face boundaries map to zero. No rational eigenspace approximation is used.

All 27 left translations induce integer 64x64 matrices A_g. Every one of the
729 multiplication identities A_g A_h=A_(gh) is checked. For generators x,y,
the 64x128 relation matrix is R=[A_x-I | A_y-I]. Its Smith diagonal is

    1 repeated 61 times, then 3,9,9.

A separate Smith decomposition checks the exact identity D=U R V and builds
the three dual character generators from U. The certificate records all
243 characters, explicit order-nine phases on all 135 edges and vertex gauge
compensators for both H27 generators. Triangle fluxes and compensator equations
are checked **modulo nine with integers**, not complex floating point.

For a connected complex, flat U(1) classes are Hom(H1,U(1)); fixed characters
annihilate every (A_g-I)H1, so they are precisely Hom(H1_H27,U(1)). This uses
standard degree-one cohomology / universal coefficients, not a new general
topology theorem. See [Hatcher, Algebraic Topology, Chapter 3](https://pi.math.cornell.edu/~hatcher/AT/ATchapters.html).

## Modular result

Over F3:

    dim H1^H27 = 4; dim H1_H27 = 3.
    radical dimensions = 64,61,55,43,32,19,10,3,0.
    radical layers     = 3,6,12,11,13,9,7,3.
    ranks (z-I)^k      = 40,16,0 for k=1,2,3.

The central Jordan form has sixteen size-three and eight size-two blocks.
Over F2,F5,F7 both invariant and coinvariant dimensions are zero, consistent
with the characteristic-zero character. Four fixed homology directions and
three fixed *dual cohomology* directions over F3 are different objects; the
number three here does not derive three physical families.

## A finite matter experiment and its transverse stability test

On this 27-address graph, choose unit negative nearest-neighbor hopping
H_ab=-exp(i theta_ab), and spinless free fermions at fixed particle number N.
These are explicit additional model choices. Enumerate all 243 flat sectors.

| N | Minimum energy | Minimizing classes | Their orders | Full flat-direction audit of one representative |
|---|---:|---:|---|---|
| 1 | -10 | 1 | 1 | 64 positive numerical curvatures |
| 9 | -37.1456142984 | 24 | 9 | 8 negative curvatures: saddle |
| 13 | -39.1246117975 | 8 | 3 | 12 negative curvatures: saddle |
| 14 | -37.4423225519 | 48 | 9 | degenerate Fermi level; no smooth Hessian asserted |
| 18 | -33.3476552576 | 48 | 9 | 64 positive numerical curvatures |
| 26 | -5 | 19 | 1 or 3 | degenerate Fermi level; no smooth Hessian asserted |

At the selected N=18 representative, the Fermi gap is 2.7742482693, the largest
gradient component is below 1.1e-15, and the smallest numerical Hessian eigenvalue
is approximately 0.00052347 in the declared cycle coordinates. Its energy is
below the trivial sector's -27. All 64 continuous flat directions are included;
the positivity is a **numerical local stability finding**, not an interval
certificate or proof of global minimality over (U(1))^64. The Hessian uses
spectral perturbation theory and is independently checked against direct
energy differences along its extreme eigenvectors.

At smooth fixed points, vanishing first derivative also follows from H27
symmetry and the absence of invariant characteristic-zero tangent covectors.
The N=9 and N=13 saddles show why symmetry-fixed stationarity alone is insufficient.

Repeating the entire lattice/module construction with a different spanning-tree
root preserves Smith factors, modular ranks, radical filtration, sector energies
and minimizer counts. Hessian eigenvalues themselves are coordinate dependent;
the tests check positive inertia, not equality of those eigenvalues.

Ordinary complex conjugation pairs the 242 nontrivial classes into 121 pairs;
all paired spectra agree. This **does not establish physical CP violation**:
combined graph/gauge/antiunitary symmetries have not been classified. In particular
a preferred non-real connection can still preserve a generalized conjugation.
There is no interacting Gauss-sector calculation, mass prediction, native 4D
continuum or gravitational dynamics in this probe.

## Intake, verification and reproducibility

GitKraken fetched and fast-forwarded 81 incoming commits from local d183f38e2
to cb3c2cbb0. The receipt `PASS11980_INTAKE.json` inventories and LF-hashes all
139 incoming paths from the full 1,784,548-character diff. Focused semantic
review covered TOE77-82 reports, relevant actual source and certificates,
the index and linked prior owners. This inventory is **not** a claim of
sentence-by-sentence review of every incoming file. Important incoming themes
include embedding-sensitive flux reversal, H27-by-D8 octagon symmetry, native
E6 roots and E8 dictionaries, followed by tritangent homology and its character.

Pass11980 was reserved and pushed as 3f37205ad before computation. Initial local
verification: **7 tests passed in 14.59 s**, including two prior TOE82 controls.
The dedicated workflow repeats these tests and regenerates the full certificate;
hosted success must be verified separately.

    OPENBLAS_NUM_THREADS=1 python analysis/w33_pass11980_heisenberg_fixed_holonomies.py

The paper is unchanged. Three-family physical flavour, nonlinear GR, a native
interacting chiral continuum and the cosmological constant remain open.
