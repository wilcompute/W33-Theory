# Nonproportional E8 localization: net three, but a vacuum obstruction

The explicit local Cartan background below has net three Spin(10) spinor
families. It also has three conjugate spinor families, eight vector multiplets,
17 charged singlets, anomalous Abelian symmetries and no constructed compact
gravity sector. Its only nonzero Standard-Model-singlet D-flat direction is
incompatible with an invertible cubic overlap matrix in the specified massless
cubic truncation. The overlap calculation supplies strong numerical evidence
for that invertibility, not an interval-certified theorem.

This improves the testable local construction; it does not solve the TOE.

## Inputs and relation to previous work

Set r²=x²+y² and use the four harmonic real functions

    f1 = Re(x+iy)^4/4 - r²/2 + z² - x
    f2 = Re(x+iy)^3/3 - r² + 2z² - 4x
    f3 = tau*r²/2 - tau*z²
    f4 = -f1-f2-f3.

For A=0 and phi=diag(df1,df2,df3,df4), the commuting flat-Cartan PW equations
hold because each fi is harmonic. These are supplied noncompact polynomial
profiles. We use 0<tau<3, omitting tau=1,3/2,2 where a charged sector loses
its z confinement. The four open chambers are represented by 1/2,5/4,7/4,5/2.

The previous common-profile parity result in
`toe_20261118_E8_H27_wire_index_parity.py` (ccdd3fe07) assumes all profiles
are multiples of one function. This example abandons that premise. It also
abandons the fixed common H27 flavor holonomy; it is not a completion of that
same global bundle. The actual exterior-Clifford and L2 conventions follow
`2026-11-18_PW_Clifford_A3_chiral_localizer.md` and
`2026-11-18_PW_tilt_perfect_Morse.md`, rather than an auxiliary matrix mass.

Multi-Cartan localization and wedge-product Yukawas are established tools:
[Braun, Cizel, Hübner and Schäfer-Nameki, sections 4.2 and 6.2](https://arxiv.org/html/1812.06072v2).
The broader colored-SQM and nonsplit-cover framework is discussed by
[Hübner](https://arxiv.org/html/2009.07136v2).
The contribution here is the explicit profile, complete charged census and
vacuum tests, not the first appearance of E8 three-family model building.
[Gonzalez et al.](https://scoap3-prod-backend.s3.cern.ch/media/files/63082/10.1103/PhysRevD.103.126027.pdf)
already investigate localized three-family mass matrices, with different
geometric and phenomenological inputs. Their construction cannot supply this
model's missing global data by analogy.

## Complete charged census and implementation checks

The E8 branching used is

    248 = (45,1)+(1,15)+(16,4)+(16bar,4bar)+(10,6).

The SU4 weights are q1=(1,0,0), q2=(0,1,0), q3=(0,0,1),
q4=(-1,-1,-1), with profile q.f. The producer enumerates all 240 E8 roots,
checks the branching multiplicities and 57,600 root reflections, and matches
64 spinor hypercharge weights against the native Peirce/Fock certificate
`data/toe_20261118_biCayley_Peirce16_SM.json`. It also checks 16 nonzero E8
root triangles for the candidate 16_3/bar16_4/S43 cubic. This is not a full
isomorphism between the Albert implementation and an E8 Lie bracket.

For each nonquadratic profile, its planar leading term is a nonzero multiple
of Re(w^m). The planar gradient is proper with degree -(m-1); the even planar
L2 kernels vanish. The z Gaussian is a zero-form for positive z² coefficient
and a one-form for negative coefficient. The quadratic profile uses its exact
Hessian signature. These facts give the complete L2 counts in this separable
model, including all charged vector and singlet sectors.

All four chambers have the following left-chiral inventory:

| Spin(10) representation | Multiplicity |
| --- | ---: |
| 16 | 6 = 3+2+1 on sheets 1,2,3 |
| 16bar | 3 on conjugate sheet 4 |
| 10 | 8 = 3+3+2 |
| 1, charged under residual U1s | 17 |

An independent root-by-root selection of H1, without the branching table's
orientation choices, agrees charge by charge: 241 left components. Net
spinor index is therefore 6-3=3. The neutral 40 D5 roots plus eight Cartans
give the candidate Spin(10)×U1³ algebra. Constant gauge modes are not L2 on
R³, and the neutral operator has essential spectrum at zero. We do not call
the entire adjoint operator Fredholm or claim a normalizable 4D gauge theory.

## D-flat cone and cubic F-flatness

Take the SM-singlet component Nc of each 16, its conjugate in a 16bar, and
the charged Spin(10) singlets. Append the conventional Spin(10) U1_chi charge
-5,+5,0 respectively. The producer enumerates every minimally supported
positive rational circuit of this rank-four charge matrix. This gives every
extreme ray of the nonnegative zero-FI D-flat cone of these field types.
Flavor multiplicities enter as sums of norms for each type.

For tau<3/2, the cone has only the origin. For tau>3/2 it has exactly one
extreme ray:

    |Nc3|² = sum_a |barNc4_a|² = sum_b |S43_b|² > 0.

This uses the single sheet-3 Nc mode, three conjugate sheet-4 modes and three
S43 modes. Their charge span has rank two. Even an allowed VEV on this ray
would leave at least SU5×U1², rather than precisely the Standard Model.

The only charge-allowed cubic made solely from these massless SM singlets is

    W = N B^T Y S.

If the 3×3 matrix Y is invertible, F_B=N Y S and F_S=N Y^T B imply B=S=0
when N is nonzero. That contradicts the nonzero D-flat ray. Hence the cubic
truncation has no nonzero simultaneous D/F-flat vacuum in that case. This
conditional algebraic argument is exact. The rank of the continuum Y below
is supported numerically. Higher operators, a nonzero FI/GS sector, massive
fields or another background can change this conclusion. We have not solved
their equations, and do not elevate this conditional result to an E8 no-go.

## Actual internal cubic overlap

At tau=7/4, the relevant planar one-form modes have profiles h=-f4 and
g=f4-f3; both have three L2 modes. Nc3 has the exact planar Gaussian and a
dz one-form. We compute the integral of their wedge product using normalized
internal modes. The z integral is analytic, with factor 0.6905267750. The
Hermite multiplication quadrature integrates the finite polynomial Gaussian
matrix elements exactly; the continuum modes remain Galerkin approximations.

| Hermite size per axis | Width omega | Singular values of geometric overlap |
| ---: | ---: | --- |
| 24 | 3 | 0.06669857684, 0.02551975540, 0.02551692565 |
| 40 | 3 | 0.06666527357, 0.02551211993, 0.02551027493 |
| 56 | 3 | 0.06666513858, 0.02551210852, 0.02551026408 |
| 96 | 4 | 0.06666513799, 0.02551210849, 0.02551026406 |

Changing both width and cutoff changes the last three singular values by
less than 1e-8. At size 96 the maximum full-operator residual, evaluated
in a larger polynomial basis, is below 1.5e-6. These are full operator
residuals, not only projected Ritz residuals. Numerical rank is comfortably
three. A certified subspace-error estimate is still needed for a strict
continuum invertibility theorem. The overall 7D gauge coupling, compact
volume and gauge-trace normalization are unspecified, so these are not
predicted physical Yukawa constants or particle masses.

## Anomaly and bare-Yukawa constraints

At tau=7/4 the full charged spectrum gives

    Tr Q = (102,141,49),   Tr Spin10² Q = (12,15,7).

The primitive common kernel is u=(14,-7,-9), but Tr(u.Q)^3=49032.
Consider the restricted 4D Green-Schwarz factorization
I6=sum_r L_r(F) X_r(F,R), where each Lr is linear in the three Abelian
field strengths. With at most two such factors, the independent gravitational
and Spin(10)-mixed anomaly vectors would have to span them. Their common
kernel would then annihilate the entire anomaly polynomial, contradicting
49032. Thus this factorization requires at least three independent linear
factors for this unchanged spectrum. Three suffice algebraically by expansion
in the three coordinate field strengths. No quantized axions, Stückelberg
mass matrix or M-theory inflow have been constructed. Additional charged
matter or a different inflow mechanism changes the premise.

Every charge-allowed bare 16-16-10 cubic in these chambers includes the
single sheet-3 mode. The resulting symmetric six-family mass matrix is a
star coupling a five-dimensional subspace to one dimension, and has rank at
most two for arbitrary vector-Higgs VEVs. Bare channels alone therefore do
not deliver full-rank light-family Yukawas. Mirror mixing or additional
interactions must actually be calculated, not assumed to repair it.

## Parallel-work review and consequences

Reviewed all 15 new science reports and their producers in the 16 parallel
commits 6ec21609b through 3edb3b915 after 9321eb27e. Read the accompanying
tests and the two whole-week inventory producers. The inventories hash full
patches and PDF text; that is not equivalent to personally proving every
older claim or reading every page's mathematics. This review does not claim
that the entire repository or all historical patches were read line by line.

The reusable `toe_20261119_parallel_review.py` redirects producer writes to
temporary storage and records a receipt: 379 tests passed across 16 modules,
19 regenerated JSONs matched exactly, and all 19 source JSON hashes remained
unchanged. This verifies repeatability and regression coverage, not independent
proof of all claims. In particular:

- `2026-11-18_E8_full248_LES_Psi3_weakG2_localMUB.md` corrects relative
  cohomology: b1_rel=2d-r1. The full adjoint's relative index 248 is an input
  rank effect, not a physical three-family index. Our charged L2 calculation
  uses different operators and domains.
- `2026-11-18_H27_G2_sphere_Higgs_family_multiplicity_qutrit_memory.md`
  correctly warns that three spatial modes times an independent rank-three
  H27 fiber makes nine. No additional H27 triplet is tensored onto our modes.
- `2026-11-19_H27_Y7_torsion_gerbes_and_positive_Ricci_no_go.md` establishes
  torsion H3=(Z3)² for (S5×T2)/H27; this does not supply an M-theory C-field
  compactification or remove that space's G2 obstructions.
- `2026-11-18_six_front_SUSY_SIC_and_TOE_falsifiers.md` constructs an
  anomaly-free classical SU3 SIC sector with a cubic superpotential and
  Higgs Hessian rank 98/106. Its ten flavor pairs give beta coefficient -1,
  so renormalizability does not establish UV completeness. The alternative
  nine-pair baryonic construction in the five-frontier report is an EFT.
  Neither provides this E8 model's missing dynamical fields by itself.
- `2026-11-19_five_frontiers_SUSY_SIC_W33_40_qutrit_CSS.md` certifies the
  asymmetric point-code distances (4,6). Its finite stabilizer algebra does
  not furnish a gravitational continuum limit.
- The subsequent `2026-11-19_W33_ninth_root_gates_natural_SIC_and_finite_calculus.md`
  gives a 70-row finite-field obstruction to non-Clifford transversal T9
  phases in its specified diagonal family, and an unencoded magic-injection
  identity. Its torus-only magnetic-flux Dirac bound also reinforces that
  flat projective bundle data cannot supply the missing fermion zero modes.

The useful connection is methodological and physical: explicit vacuum
equations are decisive. A tuned SIC sector can satisfy them in an engineered
model, while the present minimal localized E8 sector encounters a concrete
conditional obstruction. Transplanting the tuned sector would change the
theory and requires an actual embedding, anomaly and mass calculation.

## Reproduction and open boundaries

Run `python analysis/toe_20261119_E8_nonproportional_PW.py` and
`python analysis/toe_20261119_parallel_review.py`. Both write owned JSON
receipts. The latter preserves the reviewed parallel certificates.

Open requirements include a finite-energy/global source construction,
normalizable gauge modes, a consistent anomaly/inflow sector, a supersymmetric
SM-breaking vacuum, removal of the conjugate families and eight 10s, viable
light-family masses, and gravitational dynamics with empirical predictions.
The degree and polynomial coefficients are inputs. None of these global or
phenomenological requirements follows just from the integer three.
