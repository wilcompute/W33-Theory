# E6 ExFT section selection: isotropic no-go, 1080 shared-four bridges, SL2 flux shape and volume runaway

Date: 2026-11-14. Independent continuation using the committed signed E6 cubic and 78 generators. This is a mathematical and conditional-physics research note, NOT a derived dynamical spacetime selector.

## 1. Exact scalar-potential audit

Producer: analysis/toe_20261114_E6_ExFT_scalar_potential_isotropy_nogo.py
Certificate: data/toe_20261114_E6_ExFT_scalar_potential_isotropy_nogo.json

For a symmetric E6 cubic-preserving generator h in the 42D scalar coset E6(6)/USp8 and a coordinate-space derivative covector q, at generalized metric M=I and constant external metric, the two surviving published E6 ExFT scalar potential terms give the exact quadratic contribution:

V2(h,q) = Tr(h²)|q|²/24 - |h q|²/2.

The repository's 36 symmetric root packets have Hilbert-Schmidt Gram 12 I36 and the six Cartan generators have a full-rank Gram. The sum of squares over ANY orthonormal coset basis is (14/9) I27: symmetric root contribution 4/3 I and Cartan contribution 2/9 I. The isotropic unit-h average is therefore exactly (5/216)|q|², regardless of whether q is admissible in a five-coordinate IIB-type section or six-coordinate M-type section.

A shared coordinate four-subspace has 168 direct exact scalar comparison checks. On the other hand, 42 explicit anisotropic reference generators give normalized five-minus-six potential differences of BOTH signs (22 positive, 20 negative). These signs reflect CHOSEN anisotropy, not an intrinsic E6 branch selection. Unnormalized sums over five versus six mode directions are also not comparable physical vacuum energies without a dynamical mode measure.

Scalar source: https://arxiv.org/abs/1312.0614 and canonical formulation https://edoc.hu-berlin.de/server/api/core/bitstreams/c2e61a8e-6617-4d02-a91b-df26fe5ff80a/content .

## 2. Exact finite M/IIB common-four incidence and mathematical duality transfer

Producer: analysis/toe_20261114_E6_M_IIB_9D_common4_incidence_noselector.py
Certificate: data/toe_20261114_E6_M_IIB_9D_common_four_incidence_noselector.json

The 72 maximal coordinate six-sections and 216 maximal coordinate five-sections share EXACTLY 1080 admissible coordinate four-spaces. Every such four-space has precisely one maximal five-extension and one maximal six-extension. The associated 72 by 216 incidence matrix B is connected and biregular with M degree 15 and IIB degree 5, 1080 edges.

The four-coordinate annihilator is 7D. Its three transverse directions obey the strong section condition xy=xz=0: geometrically the union of a line and a plane. This is a finite realization of mutually exclusive full section dependence, not a proof of dimension-changing dynamics.

An exact integer annihilating polynomial and five power traces prove the full Gram spectrum of B B^T:
eigenvalue 3 multiplicity 15, 9 mult 30, 21 mult 20, 45 mult 6, 75 mult 1.
Thus rank B=72, nullity of B acting on 216 IIB-section functions=144, nonzero singular-value condition number=5. The two-step M-to-M incidence random walk has spectrum 1, 3/5, 7/25, 3/25, 1/25 (with corresponding multiplicities).

A uniform prior PER SECTION counts IIB:M =216:72=3:1. The canonical UNDIRECTED EDGE random walk has equal stationary branch masses, each contributing 1080 half-edges. The graph alone therefore does not define a physical branch probability. Using raw section counts as vacuum-selection odds is unjustified.

Known physical duality is M theory on T2 versus type IIB on S1, both with nine-dimensional effective descriptions. A published linear parameterization map exists: Sakatani & Uehara, PTEP2017 043B05, https://academic.oup.com/ptep/article/2017/4/043B05/3605261 . Our finite incidence graph is NOT a derivation of that map or Buscher transformations.

## 3. Exact SL(2,Z)-invariant flux shape contribution

Producer: analysis/toe_20261114_E6_9D_flux_doublet_moduli_stabilizer.py
Certificate: data/toe_20261114_E6_9D_flux_doublet_moduli_stabilization.json

Take integral 3-form flux components F,H on an ADDITIONALLY COMPACTIFIED T4, a fixed Euclidean reference shape, volume and all other fields. The positive flux-doublet kinetic term is:

E(tau) = [||F||² - 2 Re(tau) (F.H) + |tau|² ||H||²]/Im(tau).

D = ||F||² ||H||² -(F.H)² is an integer sum of squared 2x2 minors. If D>0, the unique shape minimum is tau*=(F.H+i sqrt D)/||H||² with E_min=2 sqrt D and positive shape Hessian 2||H||^4/sqrt D times I2. Rank-one flux has zero-energy infimum on the boundary instead. Checks: 450 exact SL2Z transformations, square tau=i for independent unit fluxes, hexagonal tau=(1+i sqrt3)/2 for F=(1,1,0,0), H=(0,1,1,0).

This is a familiar IIB flux kinetic term, not yet the ExFT action evaluated on a globally consistent compactification. If the shared four physical directions of nine-dimensional M/IIB physics are themselves compactified on T4, the remaining external spacetime is FIVE-dimensional. One must not call this a nine-dimensional stabilized flux vacuum.

## 4. The decisive missing modulus: exact Einstein-frame volume runaway

Producer: analysis/toe_20261114_E6_flux_shape_volume_runaway_nogo.py
Certificate: data/toe_20261114_E6_flux_shape_vs_volume_runaway_nogo.json

Release the T4 volume R while retaining a minimal unwarped nine-to-five reduction, a 3-form with fixed integral periods, and no additional sources or fields. The squared flux norm scales R^-6 and the T4 measure contributes R^4. The external 5D Einstein-frame Weyl rescaling contributes R^(-20/3), yielding

V_E(R,tau)=R^(-26/3) E(tau).

For any nonzero rank-two flux, at the positive shape minimum,
d V_E / d(log R) = -(26/3) V_E < 0.

The exact symbolic verification includes the hexagonal case, positive shape Hessian (8 sqrt3 / 3) I2, and monotonic energies at R=1,2,3,10. Therefore the flux-shape minimum is NOT a simultaneous stationary point of volume and shape. No finite-volume vacuum or section choice was derived.

To advance: construct a consistent E6 generalized Scherk-Schwarz twist U(Y), verify its embedding tensor and quadratic constraints, solve the complete reduced Einstein/scalar/flux/tensor-hierarchy equations, add physically justified sources and global flux quantization, and compare both M/IIB parameterizations without changing the chosen observable physics. Standard consistent truncation framework: https://link.springer.com/article/10.1007/JHEP01%282015%29131 .

## Evidentiary boundary

All four scripts have exact assertions and JSON certificates. They establish finite incidence algebra, a local scalar quadratic identity, a duality-invariant positive flux toy kinetic term, and a failure of that toy term to stabilize the complete moduli. They do NOT establish cosmological vacuum stability, a physical 5D versus 6D selector, a dynamical transition between ExFT sections, a new field-theory action, experimental predictions, or a Theory of Everything.
