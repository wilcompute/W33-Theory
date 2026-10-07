# Passes11615–11619: a parity-even pair phase and explicit parent/threshold interfaces

Reservation `40c974480` was pushed before computation. All five requested
targets were investigated, followed by five additional cross-connections.
[Producer](w33_pass11615_11619_parent_pairs_constraints.py),
[certificate](../data/w33_pass11615_11619_parent_pairs_constraints.json),
[independent regressions](../tests/test_w33_pass11615_11619_parent_pairs_constraints.py).

The strongest constructive result is an exact paired, parity-even ground
sector on the native W33 Levi graph, with a positive odd-particle gap and
extensive pair density-matrix eigenvalue. A separate elementary45+126 gauge
interface supplies the full Spin10 vector mass matrix. These are added
models at supplied couplings/VEVs, not a solved TOE or measured predictions.

## Intake, prior ownership and literature

Remote18e3ce03f and d35239ea2 were read in full: producers, reports,
certificates and regressions. Ten parallel tests pass in74.30s; dedicated
CI37576749382 and37577431983 are green. Intake reports no forced arithmetic
or hard certified-value contradiction. Its two custom PASS vocabularies were
classified as finite algebra/operator witnesses; broad compound-name guard
candidates remain advisory and are not advertised as a clean intake.

11600 owns the normalized Hesse tensors, invariant geometry and ray selector;
11602–11606 owns phase completion, neutral-flavon alignment, conditional
seesaw, spectator and composite-parity interfaces.11591/11595 own the actual
family tensor and Majorana channel. The new chamber material11608–11614
owns the D3 discriminant/chiral-filter chain. We do not identify its internal
positive penalty with a relativistic mass in the threshold calculation.

11289 owns the native incidence/cycle basis;11301 owns the pointwise Leibniz
obstruction and site-Hamiltonian bracket audit;11306 owns the explicitly
parametrized graph completion, which is not gravity.11274/11284/11289 and
11546 own the sequestering mechanism and fixed-data shift criterion.

Deeper searches also found and read
[4057–4064](BT4057_BT4064_advanced_physics.md) and
[4081–4088](BT4081_BT4088_deep_physics.md), the complete4081–4088 producer and
its JSON.4082 already owns conditional mobile photon composites with
Jpair=2t²/Delta, and4083 a pair pump.11539/11543 owns a different neutral
antisymmetric81-pair register and exact exchange gate. The new occupation
code and scalar16bar-weight proxy are distinct carriers. Pair hopping and
generic encoded universality are not new discoveries.

Result searches covered the index, current papers/site, Python, Markdown,
JSON and older carriers, including Dicke/ODLRO, exact mass moments, the
odd-cycle closure and auxiliary counts. Bare decimal substrings in numerical
JSON are not treated as prior mathematical results.

Primary foundations used:

- [Diehl–Baranov–Daley–Zoller, three-body-constrained lattice Bose gas](https://arxiv.org/abs/0912.3196): pair order without atomic order is established physics. The exact positive parent below is a different model, not their phase diagram.
- [Bertolini–DiLuzio–Malinsky,45+126 SO10](https://arxiv.org/abs/1205.5637): this gauge-breaking inventory is established model building, not a newly invented unification.
- [Franchino-Viñas–dePaulaNetto–Zanusso, mass-dependent curved-space effective actions](https://arxiv.org/abs/1902.03167): local cutoff coefficients and physical renormalized thresholds are different objects.
- [Bahr–Dittrich, improved/perfect discrete gravity actions](https://arxiv.org/abs/0907.4323): finite symmetry completion does not automatically restore local Einstein dynamics.
- [Kaloper et al., local sequestering](https://arxiv.org/abs/1505.01492) and [Kaloper–Padilla, graviton loops](https://arxiv.org/abs/1606.04958): neither mechanism is derived from W33 here.
- [Bremner et al., entangling gates plus one-qubit controls](https://arxiv.org/abs/quant-ph/0207072): the universal-gate implication is standard.

##11615 — a named renormalizable tree parent, and its cost

For real fields x in an orthogonal representation, introduce dimension-one
symmetric-tensor fields Qd in Sym^d(x),d=2,...,D. Set Q1=x and

    Vchain = sum_d k_d ||M Qd-Sym(Q(d-1) tensor x)||².

Every summand has polynomial degree at most four and mass dimension four.
Terminal polynomial residuals become linear functions of Qd with dimensionful
coefficients. Their squared norms are again renormalizable interactions.
Use the induced invariant norms, including the symmetric-monomial
multiplicity factors; an arbitrary unweighted coordinate norm is unsuitable.

Every original zero lifts uniquely to Qd=x^d/M^(d-1), and conversely. The
auxiliary normal Jacobian is block triangular with diagonal M I. Therefore
full-rank original residual normals give positive lifted normals. This is
an exact zero-locus and local-stability statement. Eliminating finite-stiffness
auxiliaries does **not** reproduce the original potential at every off-shell
point: (z-q²)²+(z-1)² has relaxed value1/2 at q=0, versus1 for the original
(q²-1)². Its relaxed normal curvature at q=1 is4 rather than the unrelaxed8.

The holomorphic H4 term alone has a compact example:

    M A=x², M B=y², M C=yB,
    A²+2sqrt2 x C=H4/M².

Three complex auxiliary fields suffice for that term. The manifest full
symmetric-tensor construction for all prior scalar selectors is deliberately
conservative:490 real fields for four Hesse coordinates through degree8,
and18,551 for twelve neutral-flavon coordinates through degree6, totaling
19,041. This is an existence construction, not an optimized spectrum.

For the Yukawa map, add two complex Spin10-vector family triplets A0,A1:

    Vmed=sum_j ||M Aj+conjugate(uj) H||².

Use the prior diagonal family tensor/sqrt3 for A0 and off-diagonal
tensor/sqrt6 for A1. Tree substitution yields the prior normalized Hesse
coefficients a=conjugate(u0)/(sqrt3 M),b=conjugate(u1)/(sqrt6 M), up to a
real overall sign. Exact X,Z,R covariance is checked. The11606 canonical
field gives b/a=i/2 without inserting a complex fundamental Yukawa coefficient.

The two mediators add120 real components. Add an elementary real45 for
the gauge-breaking interface below. The parent has Spin10 gauge symmetry,
global realized finite family symmetry and coefficient CP; its u field is a
singlet under that finite subgroup. G6 acting on u alone is not a symmetry
of the complete interaction with fixed unequal Higgs alignment.

Targets, scales, channel coefficients and allowed counterterms remain input.
Power-counting renormalizability does not establish asymptotic UV completeness,
a protected flavor vacuum, a continuous-family gauge parent or observed masses.

##11616 — physical multiplicities and exact gauge thresholds

The elementary retention scenario starts with934 real scalars,91 Weyl
components and45 Spin10 gauge vectors from11604. Add120 mediator components,
56 from the global-family28 spectator scalar,45 real adjoint components and
Naux=19,041. Thus Ns=20,196. The91-Weyl spectator retention is optional
when family symmetry is global; it is retained explicitly for comparison.

The gauge interface is built from all45 standard Spin10 generators. In an
independent oscillator spinor basis choose the16bar weight |11111>, with
B-L=-1,T3R=+1/2. Its symmetric square has the126bar neutral charge(-6,2,0).
This is a representation coordinate for an elementary126 VEV; no physical
scalar16 VEV is used or assumed.

For a real45 VEV in the B-L direction and a complex126 VEV in that weight,

    Mvector²=g²[vA² GA+2v126² GS].

GA is the actual adjoint commutator Gram, with vector trace norm
-Tr(Ta Tb)/2=delta_ab. GS is the actual symmetric-spinor variation Gram,
not the single16 Gram. The factor2 follows from the complex scalar kinetic
term compared with the real adjoint kinetic term. Both matrices are stored
exactly; their ranks are30 and21, they commute, and their sum has rank33.

Writing a=vA²,b=v126², all massive eigenvalues divided by g² are

|Mass squared/g²|Multiplicity|
|---|---:|
|4a/9|12|
|16a/9+2b|6|
|4a/9+2b|12|
|2b|2|
|10b|1|

Twelve gauge generators remain massless. An independent D5-root calculation
and random complex spinor-basis change verify the complete spectrum. Exactly,

    sum_vectors m⁴/g⁴=640a²/27+64ab+180b².

This replaces the common-vector-mass benchmark when evaluating thresholds.
The45 and126 directions name an SM-preserving interface, but their dynamically
selected vacuum and scales are not proved.

Remove33 eaten Goldstones from the scalar inventory:20,163 physical real
scalars remain. In Feynman gauge a massive vector plus complex ghost plus
Goldstone gives K1-K0, with a0=3 and a2/R=-1/2 for minimal matching.
Hence the physical degree count agrees with the pre-breaking signed count:

    C0=20163+3(33)+2(12)-2(91)=20104,
    CR_minimal=20107/6.

The mass partition names45 SM Weyls,15 exotic Dirac fermions, three extra
singlet Majoranas, three right-handed-neutrino Majoranas and ten spectator
Majoranas. Actual prior maps give neutrino mass ratios3,3,6 and spectator
ratios1 (three),1/30 (six),1/15 (one), at supplied common coefficients.
The spectator fourth-mass moment is1215011/405000; the neutrino one is1458.

The declared MS/Landau one-loop vacuum threshold has scalar/Weyl/massive-vector
weights1,-2,3 and finite constants3/2,3/2,5/6. Its scale derivative is
-Str(m⁴)/(32pi²). Scalar eigenvalues and exotic masses remain unspecified;
the certificate's common-scalar/common-vector expressions are retention
benchmarks, not diagonalizations of the large parent's scalar Hessian.

Separate proper-time diagnostics include the exact mass kernels

    I0=Lambda⁴[(1-x)e^-x+x² E1(x)]/2,
    I1=Lambda²[e^-x-x E1(x)], x=m²/Lambda².

Direct quadrature verifies them; at x=25 the relative curvature kernel is
5.15694e-13. Cutoff curvature signs are not a physical prediction of Newton's
constant. Renormalized couplings and gauge-dependent finite terms still need
matching. Replacing elementary126 by a composite changes this inventory.

##11617 — test the local brackets before calling them gravity

On a supplied periodic cycle, let D be the skew central derivative and

    H[N]=(pᵀdiag(N)p+qᵀDᵀdiag(N)Dq)/2,
    G[v]=pᵀ{diag(v),D}q/2.

Canonical differentiation gives

    {H[N],H[M]}=pᵀ[diag(M)Dᵀdiag(N)D
                         -diag(N)Dᵀdiag(M)D]q.

At five sites, for adjacent unit-site lapses, that matrix has nonzero
symmetric part and is outside the five local shift generators: the augmented
span rank rises5→6. Shift-shift brackets also leave the nearest-neighbor
span, producing distance-two rotations. This is an explicit algebra failure,
not merely invoking the older Leibniz theorem.

On any odd cycle, v→edge coefficients v_i+v_(i+1) is invertible, with absolute
determinant2. Thus the local shifts span individual edge rotations.
Commutators along connected paths generate every pair rotation: the minimal
Lie completion is so(N), with dimension N(N-1)/2. Canonical moment maps for
that completion close exactly. The three-site control already has all pairs
as neighbors and is misleading; the nine-site native3-power control needs36
generators, including distant pairs.

Finite matrix observables instead admit exact nonzero inner derivations
[P,.], but this changes the observable algebra. Neither matrix closure nor
the all-pair completion gives the Einstein hypersurface algebra. This target
remains unresolved at the nonlinear gravitational level; the certificate
defines exactly what failed and what each alternative changes.

##11618 — an exact pair-ordered phase with an odd-particle gap

Put a constrained bosonic occupation {0,1,2} at every actual Levi vertex.
For Delta,J>0 use the explicitly added local Hamiltonian

    Hpair=Delta sum_i |1><1|_i+J sum_edges |v><v|_ij,
    v=(|0,2>-|2,0>)/sqrt2.

Every term is positive. A zero state has no odd-site occupations and is
symmetric under every connected edge swap of0/2. Connected swaps generate
all permutations. Therefore its exact ground space is the symmetric even
sector, dimension N+1. At fixed pair number k it is the unique Dicke state.

For different sites,

    <a_i† a_j>=0,
    <(a_i²)† a_j²>=2k(N-k)/[N(N-1)].

The pair density matrix has largest eigenvalue2k(N-k+1)/N, extensive at
fixed density. On W33's N=80 Levi vertices at k=40, the off-diagonal value
is40/79 and the largest eigenvalue41; the atomic largest eigenvalue is1.
At finite fixed number both one-point functions vanish. A broken-U1 ground
representative is the product

    sqrt(1-rho)|0>+e^(i theta)sqrt(rho)|2>,

with <a>=0 and <a²>=sqrt[2rho(1-rho)]e^(i theta), preserving matter parity.
Every globally odd state contains an odd site and costs at least Delta.
One odd site with all others empty saturates that lower bound exactly.

This proves the correlated-pair escape requested in11606 for a named
nonrelativistic weight-proxy model. The selected constituent16bar weight
squares into126bar because the symmetric10 contains no required charge.
The complete Spin10-covariant interaction, Lorentzian continuum and gauged
Higgs phase are not built. Pair order is not claimed to be a new general
many-body mechanism or an already selected W33 physical vacuum.

##11619 — quantum vacuum response without erasing field dynamics

Reuse the prior constrained gravitational source that removes a common
constant vacuum shift. For two domains with fractions1/3 and2/3, threshold
constants C1,C2 leave residuals2(C1-C2)/3 and-(C1-C2)/3. A common shift cancels;
unequal local contributions do not.

The actual family map has different quartic mass traces at h=(1,2,3) and
h=(1,1,1). For real a,b their difference is

    95a⁴+500a²b²+264ab³+374b⁴.

CP-conjugate branches with real parent couplings have equal singular spectra
and homogeneous loop energy. This preserves degeneracy, not the absolute
vacuum energy. Field-dependent thresholds retain their local forces and
scale dependence; local counterterms/running must be matched independently.
Wall gradients and tensions remain gravitational sources.

Adding cI to the pair Hamiltonian leaves its parity, order, gap and states
unchanged. Its engineered zero ground energy therefore determines no
cosmological constant. Native four-form/gravity dynamics, graviton-loop
completion and measured residual vacuum energy remain open.

## Five additional probes

1. **Actual gauge-threshold map:** full45×45 mass Gram and exact five-group
   spectrum above, beyond the retention table.
2. **Residual parity holonomy:** on an actual fundamental Levi cycle, a pi
   constituent holonomy is-1 while pair holonomy is+1. Pair hopping dressed
   with Uij² remains frustration free in this flat pair-connection witness.
   Wilson-line dressing is required for gauge-invariant pair correlations;
   no dynamical confinement/Higgs phase follows.
3. **Even-occupation computation:** b=a²/sqrt2 gives exact Pauli operators on
   {|0>,|2>}. J(b_i†b_j+b_j†b_i) for time pi/(4J) produces an entangling
   square-root-iSWAP-type gate with zero odd-sector leakage. With supplied
   pair Pauli controls this is a conditional universal encoded architecture.
   X/Y need a charge-two reference. The2^N code exceeds the N+1 ground space;
   the specified gates require aligning drift to be disabled or compensated.
   No passive protected universal ground-space computation is claimed.
4. **Perturbation control:** total matter parity survives atomic hopping,
   local parity does not. At four sites, Delta=2,J=1,t=.1, the odd gap is
   1.62695, pair correlation.65918 and atomic correlation.01507. The exact
   norm bound Delta-4|E|t is finite-volume and not uniform, so thermodynamic
   robustness is not proved.
5. **Loop symmetry and parent budget:** Tr(Y†Y)=14rho/3 is radial at the
   unequal alignment, but Tr[(Y†Y)²] is not invariant under standalone G6 on u.
   At u=(1,0), its F-transform defect is16/3. Thus a degree-four angular
   divergence is allowed in this parent; a high-degree scalar selector has
   no automatic protection. Its19,041 auxiliary fields also raise C0 rather
   than cancel it. These are compatibility tests, not blanket no-go theorems.

## Validation

The producer emits ten scoped PASS sections with portable source hashes.
Nineteen independent regressions cover alternative gauge/spinor bases,
actual D5 masses, tensor normals, numerical integral identities, canonical
brackets, separately assembled many-body Hamiltonians, density matrices,
parity holonomy, gates, perturbations, CP thresholds and source binding.
Final run/timing and publication CI are recorded in the receipt.

Initial replay errors are retained honestly: a complex Hesse symbol was
accidentally declared real through SymPy's nonzero assumption; a hand-written
spectator fraction was corrected before validation; the first17-test run had
16 passes and one parser-assumption failure. No upstream result was retracted.
Exact constructed results do not close the unselected coefficients/scales,
full scalar gauge vacuum, nonlinear gravity, quantum measure or physical CC.
