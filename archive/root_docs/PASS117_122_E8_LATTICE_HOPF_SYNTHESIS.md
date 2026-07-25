# Passes 98-103: exceptional glue, exact lattice arithmetic, and the Hopf boundary

## Verified results

### 1. The subgroup bridge is explicit

GAP constructs the full orthogonal group `GO+(8,2)` of order `348364800`.
Its nonzero vectors split into orbits of sizes `135` and `120`.  Fixing an
ordered pair in the 56-suborbit of the anisotropic orbit gives a pointwise
stabilizer of order `51840`, and GAP proves that this stabilizer is isomorphic
to `W(E6)`.

More strongly, this embedded `W(E6)` splits the 120 anisotropic vectors as

```text
120 = 1 + 1 + 1 + 27 + 27 + 27 + 36.
```

This is exactly the `E8 -> E6 x A2` root branching modulo sign:

- the six `A2` roots become three fixed root pairs;
- the 162 mixed roots become three 27-orbits after quotienting by sign;
- the 72 `E6` roots become 36 root pairs.

The isotropic companion splits as `135 = 27 + 36 + 36 + 36`.

### 2. The two r=2 lattices meet through the full glue quotient

The Construction-A lattice `Lambda_C` has rank 40.  The integer
`+2`-eigenlattice `L2` has rank 24.  They cannot be equal or rescalings of
one another.

Reduction modulo 2 maps `L2` onto `Cperp`, while the vectors reducing into
`C` form a sublattice `L2^C` of index `2^8`.  Hence

```text
0 -> L2^C -> L2 -> Cperp/C -> 0
```

and `L2/L2^C ~= (Z/2)^8`.  Inside the common real eigenspace,

```text
sqrt(2)L2 subset (1/sqrt(2))L2^C
  = Lambda_C intersection ((1/sqrt(2)) L2_R).
```

The scaled intersection has determinant `2^8 * 3^10 * 5`.

### 3. The actual 2-adic genus mass

For the Jordan symbol `1^+32 2^+8`, both constituents are free type II.
The Conway-Sloane local factor contributes the cross term
`2^(32*8/2)=2^128`, the type-II term `2^-40`, and the two plus-type
diagonal factors.  Relative to the rank-40 even-unimodular mass, the exact
correction is

```text
524422438829426130254793883968303680565 / 2.
```

The resulting genus mass is approximately `1.1519e90`.  The implementation
checks the normalization on `E8` and verifies that moving the sole E8
constituent from scale 1 to scale 2, i.e. scaling by `sqrt(2)`, leaves the
local p-mass unchanged.

### 4. The anisotropic companion graph

The 120 minimum-weight-6 glue cosets, joined when their binary inner product
is zero, form

```text
SRG(120,63,30,36), spectrum {63^1, 3^84, (-9)^35}.
```

These are the 240 E8 roots modulo sign.  Together with the 135 isotropic
vertices of Pass 93, they exhaust the 255 nonzero vectors of `E8/2E8`.

### 5. The theta form is identified

The exact code weight enumerator gives

```text
Theta_Lambda = 1 + 80 q + 14640 q^2 + 5403840 q^3 + ...
```

It lies in the six-dimensional space `M_20(Gamma_0(2))`.  PARI/GP gives its
exact decomposition in the basis

```text
E20(tau), E20(2tau),
Delta*E8(tau), Delta*E8(2tau),
f_+(tau), f_-(tau),
```

where the two level-2 newforms satisfy `a_2=+512` and `a_2=-512`.  The first
six coefficients meet the level-2 weight-20 Sturm bound, and the verifier
also checks the identity through `q^20`.

## Deep dive: the complex Hopf-fibration preprint

The reviewed source is Jennifer Lorraine Nielsen, *The Complex Hopf
Fibration as the Canonical Space for Gauge-Gravity Unification*, v4,
3 July 2026, DOI
[10.20944/preprints202604.0315.v4](https://doi.org/10.20944/preprints202604.0315.v4).
It is explicitly a non-peer-reviewed preprint.

### What is mathematically solid

- Principal `U(1)` bundles are classified by maps into `BU(1)`, and
  `BU(1)` is homotopy equivalent to `CP^infinity`.
- The Milnor universal `U(1)` bundle can be represented by the infinite
  complex Hopf fibration.
- The finite Hopf fibrations `S1 -> S^(2n+1) -> CP^n`, Fourier decomposition
  along the circle, contact structures on odd spheres, and discrete spectra
  of elliptic operators on compact manifolds are standard.
- Chern-Simons formulations genuinely describe gravity in **2+1
  dimensions**, as the literature consistently states; that fact does not
  automatically extend to 3+1 dimensions.

### Where the claimed forcing fails

1. **Completeness is an added physical premise.**  The classification theorem
   says what represents all `U(1)` bundles once one demands a universal
   representing object.  Charge quantization alone does not require nature's
   field space to realize every bundle over every paracompact base.

2. **`Z[c1]` does not forbid all product-valued classifying maps.**  A
   one-generator cohomology ring does not imply that every larger structure
   group or every bundle with additional sectors is indecomposable.

3. **The `S3` transitivity uniqueness argument is false as stated.**
   `U(2)` acts effectively and transitively on `S3` with nontrivial isotropy;
   the extra factor need not act trivially.  Additional hypotheses are needed
   to single out `SU(2)`.

4. **The `S5` shell does not by itself force QCD.**  The homogeneous-space
   identity `S5 ~= SU(3)/SU(2)` is real, but identifying that action with the
   physical color gauge group is a physical assignment, not a uniqueness
   theorem from the Hopf bundle.

5. **First Chern class is not spacetime torsion.**  `c1` controls the curvature
   class of a `U(1)` connection.  Einstein-Cartan torsion is a different
   tensor tied to a coframe and spin connection.  A nonzero `c1` does not
   imply nonzero Cartan torsion.

6. **The 3D Chern-Simons result does not derive 4D Einstein equations.**
   Varying a torsion-squared action gives a torsion equation; the Bianchi
   identity does not turn that equation into the Einstein-Hilbert field
   equation without the missing curvature/vielbein term.

7. **Maxwell's equations do not require generator overlap.**  The homogeneous
   Maxwell equations follow from the abelian Bianchi identity `dF=0`; the
   sourced equations follow from varying the Maxwell action.  They are not
   consequences of a shared gauge/spacetime generator.

8. **The mass, coupling, dark-sector, and precision-number claims therefore
   remain model hypotheses.**  Their numerical agreement cannot repair the
   missing implications upstream.

This boundary agrees with the repo's later variational spectral-action
decision: the defensible route to Einstein equations is an explicit
Einstein-Hilbert term in a continuum spectral action and its metric
variation, with higher-curvature and cosmological terms retained.

## The useful finite Hopf analogy for W(3,3)

There is an exact finite projectivization:

```text
F3^x -> F3^4 \ {0} -> PG(3,3)
 C2          80           40.
```

This is the finite-field analogue of quotienting nonzero vectors by scalar
phase.  It explains the 40 W33 points without claiming a homotopy
equivalence to the complex Hopf bundle.

The repo also has a **different** three-sheet qutrit phase bundle,
`40 lines * 3 phases = 120`.  Combining its phase count with the projective
sign count gives `40*3*2=240`.  This is structurally suggestive because 240
is both the signed lift of the 120 anisotropic E8 root pairs and the W33 edge
count, but an equivariant bijection between these 240-sets remains required.
The `C2` projective-scalar fiber and `C3` qutrit-phase fiber must not be
conflated.

## Evidence files

- `analysis/w33_pass117_o8_e6_embedding.g`
- `w33_pass117_o8_e6_embedding.py`
- `w33_pass118_lattice_intersection.py`
- `w33_pass119_exact_2adic_mass.py`
- `w33_pass120_srg120_anisotropic.py`
- `w33_pass121_weight20_theta.py`
- `w33_pass122_hopf_synthesis.py`
