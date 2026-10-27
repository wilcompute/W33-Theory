# Canonical cubic bridge, native overlap operator and certified flux bounds

Continuation of `e674c9a82` in `C:/Repos/Theory of Everything`. All five requested
directions were investigated. The strongest positive results are an explicit
canonical-cubic intertwiner, a native finite-cell overlap operator, interacting
response on every native link, and exact infinite-electric-flux ground-energy
enclosures. Specific action/radius mechanisms and a split-threshold candidate
fail. A physical TOE and the complete content review remain unfinished.

Producers:

- `analysis/w33_20261027_native_operator_closure.py`
- `analysis/w33_20261027_certified_rotor_bounds.py`

Certificates have the same basenames under `data/`; controls are in
`tests/test_w33_20261027_native_operator_closure.py`.

## 1. Test mechanisms for the reflection action and radius

The previous infinite-cover reflection exchanges native edges0 and118. On the
27-vertex cell define the odd hopping deformationX as the difference of these
two real edge hoppings. Its reflection sendsX to-X while preservingK0=-adjacency.
Thus the determinant is even in the deformation parametereta. But it does not
selecteta=0: the exact one-particle ground-energy second derivative there is

`E0''(0)=-112/3645`.

The inverse of the native graph Laplacian on constants' orthogonal complement
certifies this rational value. Thermal grand-potential curvatures atT=.25,1,2
are respectively about-0.37869,-0.60061,-0.39726. These are different ensembles,
not temperatures of a single occupied state.

This is an explicit instance of free-energy concavity in a linear Hermitian
coupling. Fermions alone therefore destabilize the symmetric point along this
tested linear deformation. A positive bare stiffness, nonlinear field coupling
or another dynamical sector could change that result. No sign for such a term
is derived here. This does not contradict the earlier positive curvature in
nonlinear compact link angles, which includes a second-derivative contact term.

The radius candidate is also insufficient: with only massless scale-free
fields on one compact circle, the Casimir energy per remaining3D spatial volume
is`C/R^4`. It has no finite stationary radius forC nonzero, and is flat forC=0.
Reflection boundary conditions change the coefficient, not the homogeneity.
Massive sectors or localized terms can add scales; that is established prior art,
not a native derivation. See [Ponton–Poppitz2001](https://arxiv.org/abs/hep-ph/0105021).

**Outcome:** these two mechanisms fail to derive the selected action or radius.
The previous positive reflection-averaged action remains a supplied model.

## 2. Interacting response on the entire27-vertex,135-link cell

Use one up-spin and one down-spin fermion, each hopping along every native edge,
with supplied on-site Hubbard interaction`U sum_v n_up(v)n_down(v)`. The sector
has729 states. This includes actual fermion interaction, unlike the earlier free
determinant or one-particle hopping controls.

All135 link-current vertices are retained. With the nondegenerate many-body
ground state and excitation gapsDelta, the static and regular dynamic kernels
are computed from

```
B_ef = diamagnetic_ef -2 Re sum_n <0|J_e|n><n|J_f|0>/Delta_n,
E_ef = 2 Re sum_n <0|J_e|n><n|J_f|0>/Delta_n^3.
```

Both135x135 kernels are stored in full. Every tested static kernel annihilates
the native vertex incidence matrix to below4e-16. An independently transformed
many-body Hamiltonian obeys finite vertex-gauge covariance to below2e-15, and an
actual link-phase finite difference reproduces a static kernel entry to4e-8.
The electric kernel is positive semidefinite to numerical precision.

| U | Ground energy | Sector gap | Double occupancy |
| ---: | ---: | ---: | ---: |
| 0 | -20 | 9 | 0.0370370 |
| 2 | -19.9325042 | 8.9325042 | 0.0307412 |
| 8 | -19.7872715 | 8.7872715 | 0.0190310 |

The four period-twist stiffnesses remain nonzero and vary with interaction.
Their eigenvalues are coordinate-dependent; they are recorded as diagnostics,
not identified with masses or universal propagation speeds.

**Boundary:** this is a fixed two-particle sector on a periodic cell, responding
to external link fields. It is not all Fock sectors or dynamic-gauge matter on
the infinite translated cover. Uniform cell phases do not resolve all six
translated commutator fluxes, so these stiffnesses are not the earlier H0.

## 3. Rigorous ground-energy enclosures beyond the flux cutoff

TOE71–73 already use complement and interface bounds on a different native
two-loop gauge/matter patch. In particular
`analysis/2026-10-14_toe72_five_fronts.md` gives exact complement14.165 and
interface-norm-squared2.0034375 bounds, while retaining a numerical finite-block
gap premise. We credit that method and do not claim it was invented here.

For the present three- and six-cycle commutator patches, all calculations below
use the supplied positive compact potential from the previous packet. The new
certificate closes the finite-block numerical premise for **ground energy**.

LetP retain`|m_i|<=L`,Q be its infinite complement, andG=C C^T be the exact
integer cycle Gram matrix. We certify:

1. Choose a strictly positive **integer** vectorp onP. Exact rational arithmetic
   gives`PHP >= a I`, where`a=min_i (HPp)_i/p_i`. This follows from the weighted
   graph-Laplacian identity for a symmetric matrix with nonpositive off-diagonal
   entries. The exact Rayleigh quotient gives an upper boundb.
2. Since the compact potential is positive,`QHQ >= c I`, with
   `c=g^2 (L+1)^2/[2 max_i (G^-1)_ii]`. For any omittedm some coordinate exceeds
   the box, and`m^T G m >= m_i^2/(G^-1)_ii`.
3. Exact interface row and column sums give`||PHQ||^2<=beta2`.
4. Block comparison yields the exact algebraic lower endpoint
   `(a+c-sqrt((a-c)^2+4 beta2))/2` for the infinite-flux ground energy.

The stored certificate contains every positive integer vector and the exact
rational/algebraic endpoints. Tests rebuild each integer Hamiltonian and verify
these witnesses; an eigensolver result is not an accepted proof premise.
The eigensolver only proposes the vector. Positive, subtraction-free Jacobi
iterations repair its tiny tails before integerization. The first uncorrected
six-cycleL2 vector gave a valid but useless-34524 lower bound, illustrating why
an absolute Ritz residual does not certify relative tail accuracy.

| Cycles | L | Certified infinite ground interval, rounded |
| ---: | ---: | --- |
| 3 | 2 | [3.41867,3.56242] |
| 3 | 3 | [3.48415,3.56242] |
| 6 | 1 | [3.13428,3.68633] |
| 6 | 2 | [3.46917,3.68629] |

The numerical six-cycle ground estimate is3.686286991; the certified interval
is much wider. These enclose the infinite-electric-flux answer on a **finite
geometric patch**. They are not a certified spectral gap, infinite spatial-volume
limit, confinement theorem or continuum result.

## 4. Close the canonical cubic map and build a native overlap operator

### The exact map

Earlier packets supplied the standard internal decomposition
`10_(1,1)+bar5_(-3,1)+1_(5,1)+5_(-2,-2)+bar5_(2,-2)+1_(0,4)`
but explicitly lacked its map to the actual canonical signed45-term cubic.
This missing map is now constructed.

Use coordinates`(t_ij,p_i,z,u_i,v_i,S)`, witht antisymmetric andi=0..4. The
target cubic consists of`S u.v`, `z p.u`, `p_i t_ij v_j`, and the alternating
Pfaffian terms`t t u`. These have45 square-free monomials with signs.
The certificate gives a27x27 unitary signed permutationSmap such that

`N_canonical(x)=N_SU5(Smap x)`

**coefficient by coefficient for all45 terms**. The targetS coordinate is the
previous canonical anchor0, and the transported Qpsi matrix agrees exactly
with the existing charge dictionary. The24 sl5 basis generators and both U1
generators annihilate the entire polynomial in exact integer arithmetic.
A separate random finite SU5 transformation verifies invariance in canonical
coordinates. No equality of unrelated27-element carriers is asserted.

Prior owners include the Round12 exact first-Tits/Cayley chart map,
`analysis/w33_20261019_round12_full_octonion_intertwiner.py`, the Round13 anomaly
ledger, and the canonical artifact itself. They are different charts/carriers;
the present signed permutation explicitly connects the ones used in this packet.

### The native-cell operator

Supply four Euclidean Clifford spin matrices and use the actual harmonic
representativesh of the four native deck voltages. On native edges build an
antisymmetric gamma-weighted derivative plus half the gauge-covariant graph
Laplacian. Set

`HW=gamma5(DW-1)`, `Dov=1+gamma5 sign(HW)`.

This is an actual finite matrix on the native graph, rather than a count of
putative spinor components or a separate hypercubic torus. The construction
uses the established overlap formula; see
[Neuberger1998](https://arxiv.org/abs/hep-lat/9801031). TOE68 and Pass11984 already
own the earlier nonnative-torus and hybrid native-fiber controls.

The free native operator has dimension108. At zero momentum it has four zero
singular values; none occur at the other15 Brillouin corners. Forty-eight seeded
additional momentum points also have a nonzero Hermitian-kernel gap. This is
sampling, not a global no-doubling or locality theorem.

For seeded nonabelian links, actual5,bar5,10 operators have dimensions540,540,
1080 and kernel gaps about.98788,.98788,.98144. The Ginsparg–Wilson relation,
projector identity and Weyl intertwining law hold below3e-14. Kernel covariance
under independently transformed vertex frames holds below9e-16. The full27
block formula is transported to canonical cubic coordinates bySmap.

There is a metric issue rather than an automatic common cone. With bare delta
Clifford matrices the leading Dirac square has co-metric`G^2`, whereG=M/27,
while the prior engineered gauge action usesG. Supplying the metric-compatible
Clifford relation`{gamma^a,gamma^b}=2(G^-1)^ab`, equivalently replacingh by
`h G^-1/2`, aligns the leading symbols. Along the first period direction the
tested slopes change from0.4699473 to0.6085806, as the two exact leading metrics
require. This is an explicit geometric choice, not microscopic selection of a
shared relativistic speed.
An independent integer change of the four period coordinates preserves the
matched edge inner products`h G^-1 h^T`; this checks that the matching rule is
geometric rather than an artifact of the displayed period basis.

**Boundary:** Euclidean spin matrices and a Weyl projector are supplied. A global
fermion measure, uniform admissibility/locality theorem, topologically nontrivial
native gauge sectors, Lorentzian spacetime and a selected chiral vacuum remain
open. The paper's pages111–112 explicitly distinguish hosting chirality from
selecting it. A native finite overlap matrix does not overturn that distinction.

## 5. Content review and a stronger split-threshold exclusion

The frozen PDF ledger now records47/210 fully read text pages,72–118. New
pages111–118 cover chirality and antiunitary orientation, flavor alignment,
area-law limitations and modulus-dependent vacuum choices. Their finite symmetry
claims do not supply the missing field-theory measure or a handed vacuum.

Three further original patches were read in full: `c63b9ade1` honestly bounds
an earlier391-commit audit, `887c9718e` records a hosted replay receipt, and
`6a26f6bed` proves a faithful20-dimensional CSS logical-label action while
separating it from a physical gate. The cumulative frozen-week count is9/481,
including five empty reservations. The full requested review remains incomplete.

The new threshold test continues Pass12330 rather than treating its common
threshold obstruction as a theorem about all spectra. Re-reading the actual
field ledger gives Weyl contributions`(40/3,14,296/9)` and scalar contributions
`(14/3,28/3,148/9)`, in the orderSU3,SU2,Y. Keeping the Standard Model baseline
light, the excess contributions are

`deltaW=(28/3,10,236/9)`, `deltaS=(14/3,55/6,293/18)`.

Give those two categories independent thresholdsMF andMS. The numerical
feasibility problem for both in1TeV..1e16GeV, crossing below1e19GeV and positive
perturbative-domain inverse coupling is infeasible. More strongly, the exact
matching equations for`kY=8/3` give, with
`tauF=log(Mcross/MF)/(2pi)>=0`,

```
y = log(Mcross/MZ)/(2pi) = 69042999/26564750 -62 tauF/1801,
tS = log(MS/MZ)/(2pi) = 162709199/1328237500 +152 tauF/1801.
```

IfMF>=MZ, then`tauF<=y`, hence
`tauF<=23014333/9159750` and`tS<=153221179/457987500`.
Using`pi<22/7` and a rational40-term exponential Taylor sum with a geometric
remainder proves`MS<747GeV`. The exact rational upper bound is stored.
Thus **both excess-category thresholds cannot exceed1TeV** in this one-loop
model, independently of the LP. This strengthens the previous common-threshold
bound without claiming exclusion of representation-specific mass splittings,
full left-right gauge matching or string threshold corrections.

## Independent next directions

Publication validation: both producers regenerated their certificates. All29
focused controls across this packet and its three Oct27 predecessors passed
in18.01s. The rediscovery guard passed, and the results index was rebuilt over
12,767 files. Incoming`c4ac6b6bf` changes only the generated formula registry;
its metadata/path and initial diff were reviewed, without adding a full-patch
read flag. Unrelated shared dirty files are excluded from publication.

1. Prove a uniform overlap-kernel gap/locality bound and construct its Weyl measure.
2. Extend interacting matter to additional Fock sectors and translated cells.
3. Sharpen flux certificates to certify excited levels and the gap.
4. Test a massive, backreacting sector that can supply a compactification scale.
5. Complete the content audit and test mass-generating representation-specific thresholds.
