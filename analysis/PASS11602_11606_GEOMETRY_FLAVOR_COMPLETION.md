# Passes11602–11606: local geometry, a gapped CP vacuum and a dynamical seesaw interface

Reservation `235295388` preceded computation and was pushed to master.
Producer: [w33_pass11602_11606_geometry_flavor_completion.py](w33_pass11602_11606_geometry_flavor_completion.py).
Certificate: [source-bound JSON](../data/w33_pass11602_11606_geometry_flavor_completion.json).
Regressions: [independent tests](../tests/test_w33_pass11602_11606_geometry_flavor_completion.py).

All five requested investigations were executed. Additional probes compare
spectator repairs under the actual family symmetry, audit composite matter
parity, and construct an escape from the first seesaw's exchange obstruction.
**These are exact maps, algebraic results, numerical consistency checks and
conditional EFTs. They do not solve the TOE or predict measured parameters.**

## Prior work and intake

11601 owns the inverse-frame/principal-metric diagnosis and supplied-geometry
heat calibration;11600 owns the normalized Hesse tensor doublet, CP-odd Bloch
invariant, positive ray selector and its restricted degree16 obstruction.
11557/11559/11566 own the Clifford fiber, periodic refinement and flat Wilson
construction.11395 owns finite spin lifts;11397 already explains why a fixed
finite rotation group cannot approximate generic smooth curvature. Continuous
Spin links below are an additional supplied connection.

11482/11528 already own the homogeneous ADM/DeWitt constraint mechanism.
11381 owns the rotational-frustration counterexample to lapse linearity in
the native pair action. It remains valid. Neither a continuum Dirac operator
nor a homogeneous ADM constraint repairs that action automatically.

The October1 chiral-decuplet certificate owns the anomaly-compatible
91-Weyl/81-complex-scalar candidate.11271 owns an elementary28 spectator mass;
11276 owns its full-rank sextet-composite replacement. We read their code and
JSON before comparing them with the recent Hesse symmetry.11591 owns the
two-dimensional symmetric family tensor space;11595 owns the126 Majorana
channel. The standard10+126 Clebsches and seesaw are prior art.

Searches covered formula fragments, group identifiers, coefficient values,
the result index, topical aliases, scripts, reports, certified JSON,
`w33_paper.tex`, the current site and forty-points source. No claim is made
that local spin transport, G6, ADM, catalecticants or the seesaw is new.
The remote was current through0ed7ebe09 before reservation; the original
parallel working tree is preserved. This is not a fresh replay of every
historical commit or every historical script.

##11602 — an explicit local matched-metric Dirac operator

Write the coframe as E[a,i], J=detE and
C_i(x)=gamma^a(E^-1)[i,a]. Thus C(p)^2=p^T(E^TE)^-1p.
For a forward nearest-neighbor edge x→y=x+i, with Spin transport U_xy
mapping the spinor at y back to x, set

    D_xy=i[C_i(x)U_xy+U_xy C_i(y)]/(4h),
    D_yx=D_xy-dagger.

This is a concrete site-major sparse operator. At every site let S_x be a
Spin basis change. Transform C_i→S_x C_i S_x† and
U_xy→S_x U_xy S_y†. Rebuilding the operator gives exactly
D→S D S†. Hermiticity and locality are structural, not inferred from spectra.
The continuum compatibility identity is

    partial_i C_i+[Omega_i,C_i]+C_i partial_i logJ=0.

It identifies the symmetric flat-measure operator i{C_i,nabla_i}/2 with the
geometric Dirac conjugated by J^(1/2). Arbitrary independent links do not
satisfy this identity merely because they are unitary.

A regulator uses the same transport: a positive weighted graph Laplacian
with edge weight average(g^{ii}), coefficient r/(2h), multiplied by the
native Clifford grade. The grade commutes with Spin transport. It transforms
covariantly and vanishes as O(h) on smooth fields. Off-diagonal metric terms
are present in the Dirac symbol; this particular Wilson regulator uses
positive diagonal weights and is not asserted to be a finite-cutoff
coordinate-invariant scalar Laplacian.

On an invertible constant non-diagonal frame, the flat squared dispersion is

    |E^-T sin(ph)/h|^2
      +[r/h sum_i g^{ii}(1-cos(p_i h))]^2.

Only the zero corner is massless. An independent even-L4 matrix test counts
32 central-difference zero modes and only4 Wilson zero modes: one rank-four
species, with all seven doubler corners lifted.

For the supplied conformal E=exp(.12 cosx) I, exact torsion-free spin
transports are used. Plane-wave relative errors are:

|L|central operator|with Wilson regulator|
|---:|---:|---:|
|9|0.0805689123|0.1457001540|
|15|0.0295037401|0.0804885627|
|27|0.0091669573|0.0430422953|

L9/27 are3-power refinement rungs; L15 is an additional consistency control.
The central operator shows second-order consistency, while the regulator
adds a first-order term. Rebuilding after nonconstant spin rotations gives
residual below1e-13. This is not yet a non-diagonal curved heat-limit proof
or a derived W33 frame/connection dynamics.

##11603 — genuinely nonstatic4D coframes and a constraint control

Supply ds_E²=N(t)²dt²+sum a_i(t)² dx_i², a_i=expq_i. The torsion-free
connection is Omega_0=0 and Omega_i=a_i' gamma_i gamma_0/(2N).
Use the actual rank-four native spatial gammas and gamma_0=Y⊗I. Then

    D=i gamma_0/N(partial_t+sum q_i'/2)
      +sum i gamma_i/a_i partial_i.

Conjugating by sqrtJ, J=N product a_i, gives

    Dhat=i gamma_0[N^-1 partial_t-N'/(2N²)]
         +sum i gamma_i/a_i partial_i.

The volume/spin term cancels exactly. At N=1 and fixed transverse momentum,

    Dhat²=-partial_t²+sum k_i²/a_i²
          -i gamma_0 sum gamma_i k_i partial_t(1/a_i).

The last term rules out extending11601's static theta-factorization unchanged.

An independent Christoffel computation uses a_i=t^p_i with
p=(-2,3,6)/7. This nonstatic Euclidean radial Kasner metric has Ricci=0 and
Riemann²=576/(343t^4), so it is not flat. The bulk rank-four Dirac heat
coefficient has a2=0 but a4=-(4pi)^-2(7/360) integral sqrtg Riemann².
Boundary coefficients must be added on a truncated domain.

Separately, the supplied Lorentzian homogeneous ADM action has

    L=-M²V/N sum_(i<j) q_i' q_j' -rho N V,
    C=[sum p_i²-(sum p_i)²/2]/(2M²V)+rho V,
    H_total=N C+lambda p_N.

The Legendre map is exact. p_N=0 and C=0 are first class for this homogeneous
model and leave two homogeneous configuration degrees of freedom. This
checks a named time-dependent constraint system; it does not establish the
local hypersurface-deformation algebra, a Lorentzian continuation of the
native quantum model, or a ghost-free W33 multiframe action.

##11604 — the signed quantum budget differs from a bare Dirac trace

Use a declared Feynman-gauge common proper-time cutoff and the parity-even
one-loop determinant. Define

    Gamma_even=-1/2 integral_(Lambda^-2)^infinity H(t) dt/t,
    H=Ns Kscalar-Nw KWeyl+Nv(Kvector-2Kghost).

A real scalar contributes a0=1 and a2/R=1/6-xi; a rank-two Weyl trace has
2 and-1/6; a four-component gauge-vector trace has4 and-1/3; its signed
complex ghost has-2 and-1/3. Consequently

    C0=Ns-2Nw+2Nv,
    CR=(Ns+Nw-4Nv)/6-sum_scalar xi.

These power-divergent coefficients are regulator/gauge-dependent. They are
not physical predictions of the sign or value of Newton's constant.

|Conditional retained inventory|Ns|Nw|Nv|C0|CR at xi=0|
|---|---:|---:|---:|---:|---:|
|Prior E6×family SU3|162|91|86|152|-91/6|
|Spin10×family SU3, retaining all prior scalar/Weyl components|162|91|53|86|41/6|
|Spin10, finite family EFT, plus126 triplet, Hesse doublet and two neutral triplet flavons|934|91|45|842|845/6|

The10_H triplet is already in three27 scalars. The126 triplet adds756 real
components, the Hesse doublet4, and the two new gauge-singlet alignment
triplets12. The last row does not add a126 in an unbroken E6 theory without
its E6 representation completion. The finite family group is the actual
11591 X,Z,R triplet image; its linear lift and the continuous-family breaking
must be matched in a UV parent rather than assumed from a projective label.

The first inventory has CR=-91/6-162xi81. Its minimal-coupling sign is
negative; its zero occurs at xi81=-91/972. In this particular convention,

    rho_UV=-C0 Lambda^4/[4(4pi)^2],
    M_ind²=CR Lambda²/(4pi)^2.

Changing the active inventory can change that sign. It is not a derivation
of G: all rows are retention examples, not matched thresholds. Actual masses
insert exp(-m²t); massive gauge fields require Goldstone/ghost completion.
No row cancels C0. An independent symmetry-allowed vacuum-energy counterterm
remains. A bare fermion heat coefficient cannot settle the cosmological
constant or the complete quantum gravitational coefficient.

##11605 — degree-four phase completion preserves spontaneous CP breaking

On unnormalized pencil coordinates x=u0,y=sqrt2 u1, the actual11597/11600
matrices F and P generate48 elements, with (FP)^3=iI and scalar centerC4.
Their holomorphic invariant ring is the classical reflection-group G6 ring:

    f4=x^4+x y^3,
    f12=24x^12-440x^9y^3+264x^6y^6+y^12,
    Molien=1/[(1-t^4)(1-t^12)].

The finite closure, exact rational Molien sum, generator invariance and
nonzero Jacobian are computed. Independent fixed-space calculations check
all degrees1–12. This uses the stated scalar lift: changing generator phases
or imposing a larger scalar center changes the holomorphic invariant ring.

In canonical coordinates H4=u0^4+2sqrt2 u0 u1^3 and

    |H4|²=3/8(rho^4+p4)+(3sqrt3/2)rho p3.

It is constant and nonzero on the24 CP-breaking rays of11600. Add the
positive CP-even term lambda/M^4 |H4-c4|² with

    c4=v^4 sqrt(9/16+9sqrt42/196), real and positive.

Each ray has exactly four phases satisfying H4=c4. Thus there are96 vacuum
vectors in two48-element CP-conjugate G6 orbits. The old radial/angular
normal Hessian has rank3; H4 has nonzero phase derivative4ic4, so the added
term makes all four real tensor-field directions positive. The old U1
Goldstone is removed. The phase curvature along a fixed ray is
16lambda c4²/(M^4v²); angular mixing means this is not automatically a full
Hessian eigenvalue. Independent numerical orbit and phase-curvature checks
verify the count and CP separation.

This does not protect the suppression of the previously allowed p3/p4 terms
or derive the potential targets. The earlier phase-blind degree16 lower bound
retains exactly its stated scope. A useful further obstruction follows from
finite-group orbit separation: if BOTH f4 and f12 are fixed to real targets,
u and conjugate(u) belong to one group orbit. A selector of that single orbit
cannot spontaneously break generalized CP. Fixing only H4 while the angular
CP-odd invariant remains nonzero avoids that obstruction.

##11606 — a real alignment, its obstruction, and a constructed escape

Use two **additional gauge-singlet family-triplet flavons** h,r. Their
CP-even coercive polynomial potential is

    (|h|²-1)²+sum_i<j |h_i h_j|²+|sum h_i³-1|²
    +sum_i[(|r_i|²-1)²+|r_i³-1|²]
    +|r0r1r2-1|²+|h†r-1|².

All terms are invariant under the actual11591 X,Z,R image. Exactly27 minima
form one finite-group orbit: h=e_i r_i, r_i³=1, product r_i=1. At
h=(1,0,0),r=(1,1,1), all12 real flavon Hessian directions are positive.

These flavons align actual gauge-charged Higgs triplets through the map

    V_align_H=kH[|h|² sum_i ||H_i||²
                 -||sum_i conjugate(h_i) H_i||²],

and the analogous map for r and126bar R. Cauchy–Schwarz proves positivity;
its zeros give H_i=h_i H_common and R_i=r_i R_common. Gauge indices are
contracted with invariant Hermitian norms. This avoids putting non-gauge-
invariant cubic phase operators directly on EW doublets. The gauge direction
and magnitude of H_common/R_common are still unselected.

For supplied(a10,b10,a126,b126)=(2,1,4,1), down126 ratio1/10, up126=0,
typeII=0 and overall vR removed, the type-I seesaw gives exact light masses
(2±sqrt2)/3 and1/3. Charged singular values are(sqrt241±3)/20 and19/10.
Both charged and neutrino operators commute with the same family exchange.
Their mixing has one2×2 rotation and an isolated state; tan(2theta)=11sqrt2/64.
This branch cannot produce realistic three-angle mixing despite its stable
flavon vacuum.

**We then changed the alignment rather than ending there.** Put tau_i=|h_i|²
and choose positive squares fixing their elementary symmetric polynomials
to(14,49,36), plus|sum h_i³-36|²+|product h_i-6|². Keep the r selector and
use|h†r-6|². The tau roots are exactly1,4,9. Triangle equality and the cross
term give54 minima, one X,Z,R orbit: permutations of magnitudes(1,2,3),
h_i=|h_i|r_i, r_i³=1, product r_i=1. The degree12 potential is coercive and
its full12-field Hessian is positive. A separate magnitude/phase Jacobian
proves full normal rank.

Choose(a10,b10,a126,b126)=(2,i,4,1), with the same EW/seesaw ratios. Then
MD=[[2,3i,2i],[3i,4,i],[2i,i,6]] and MR=3I+J. In a two-component Weyl
convention use He=Me†Me and Hnu=mnu†mnu. Exactly,

    Im Tr[He,Hnu]^3=-94163140688/5625.

Their characteristic polynomials are stored as exact rational polynomials.
All spectra are nondegenerate and every mixing entry is nonzero. At the
supplied inputs, with ascending mass ordering,

    sin²theta13=.03347437762,
    sin²theta12=.14074016670,
    sin²theta23=.29767381000.

These values are a constructed example, **not a measured-parameter fit**.
The CP ratio b/a=i/2 is attainable from the canonical Hesse field
u=(sqrt(2/3),-i/sqrt3), whose CP-odd Bloch invariant is nonzero. The11600
angular targets can be changed to select its two CP-conjugate orbits and
11605 phase completion uses H4=4(1+i)/9 before the phase rotation. Relative
overall Yukawa/Higgs phases and the126 coefficient direction are still
inputs; the ratio interface does not select a common UV action automatically.

## Additional spectator and matter-parity probes

The old full-rank spectator construction is reused, not rediscovered.
The new question is whether it retains the recent finite family selection.
No nonzero sextet is fixed by X,Z: its fixed-space dimension is0. More
strongly, a single-sextet cube Sym(F^3) cannot preserve H27. If q_F³ is
invariant, each generator maps q_F to a cube-root scalar times itself.
That would give a common one-dimensional submodule of Sym²3; its nontrivial
center action forbids this. The prior mass remains full rank but breaks this
family subgroup.

An elementary28 sextic can retain it. The explicit

    sum_i x_i^6+lambda(x0x1x2)^2

gives a rank10 middle symmetric pairing. In the canonical Sym³ basis its
Takagi singular values are1(multiplicity3),|lambda|/30(multiplicity6) and
|lambda|/15(multiplicity1). Its determinant is
-lambda^7/(15*30^6). It is invariant under X,Z,R and the SU3-compatible lift `-R`. No exact sextic-stabilizer classification is claimed. The renormalizable
map chi_abc chi_def Sigma^{abcdef} uses SU3(6,0), dimension28, as in11271;
this is a different explicitly symmetry-preserving VEV pattern.

The price is56 real scalars and Dynkin index63. In the October1 inventory
alone this changes b_family from-15/2 to-57/2, worsens its Landau problem,
and gives C0=208, CR=-35/6 at minimal coupling. Spectator thresholds also
retain the broken-family Wess–Zumino matching required by11276. Dynamics
selecting this VEV is not established.

Finally, the126bar neutral VEV has(qBL,r,6Y)=(-6,2,0) and preserves matter
parity. A factorized composite from a scalar16bar singlet instead uses a
constituent VEV(-3,1,0), which is matter odd and breaks that parity. The
composite's even charge does not repair its vacuum. A genuine correlated
pair condensate with<phi>=0 and<phi phi>!=0 could avoid this obstruction;
its existence and gap need an actual dynamical construction. This also
changes the elementary scalar heat inventory and cannot be substituted
silently in the quantum budget.

## Parallel11607: preserve its kernel while lifting the scalar phase

During validation, Sage published11607 in7b12e442d and reserved11608–11613.
We read the complete code/report/tests/JSON, checked source hashes, ran
pre-integration guards and replayed its five tests (PASS in42.55s). Its
nonstandard PASS status is classified as a finite internal filter witness;
its physical boundaries remain unchanged. Formula commit44bf36191 only
indexes five additional unclassified formulas.

11607 owns H_gap=lambda[(15/343)rho^6 I+W Chi]^2 on the executable internal
Spin10 Dirac32. Since phase fixing changes neither the Bloch coordinates nor
W, it keeps an exact Weyl16 kernel and gap900lambda rho^12/117649 on all96
vectors of11605, while the scalar potential now has no phase Goldstone.
This combines two actual maps; the filter is an internal penalty, not a
Lorentz-invariant mass term or a chiral path-integral measure.

A separate lift audit prevents identifying two different actions. In the
exported real-gamma basis, Chi-star=-Chi. The unitary R=iGamma10 flips Chi,
as11607 states. Component conjugation K also flips it. Consequently the
antilinear map R K **preserves** Chi: the two flips cancel. K alone supplies
a different compatible semilinear sign action. The unitary adjoint action
chosen in11607 remains valid; neither choice is automatically microscopic
physical CP or the clock. Under a complex basis S, K has linear part S S^T
and R K has linear part S R S^T. An independent random complex-basis test
checks these statements rather than reusing naive component conjugation.

The corpus guard also flagged`hesse+levi`. Its four named candidate owners
were read completely: [1087–1091](../PASS1087_1091_FIVE_STREAM_RELEASE.md),
[BT1720–1723](BT1720_BT1723_repo_mining_execution.md),
[BT1741–1744](BT1741_BT1744_execution_summary.md), and
[10949](PASS10949_FREUDENTHAL_QUASICONFORMAL_CLOCK_CONE.md).
Their finite incidence, Hesse/exceptional and internal real-form results are
credited. Here the file-level compound also sees the standard Levi-Civita
connection; no new Hesse/Levi graph theorem or internal Lorentz-to-spacetime
map is asserted.

## Validation and remaining physical boundary

Nine producer sections PASS. **Final19 independent regressions PASS in42.74s.** The first18-test suite passed in45.68s. The final suite also checks the parallel phase/filter and complex-basis lift interface.
The initial run was15/16: the failure parsed the stored symbol`lambda` as a
Python keyword. A safe parser alias fixed it without changing the matrix.
A first19-test attempt had18 functional passes and a source-hash failure because regeneration overlapped test startup. The final regeneration completed before the full suite; the certificate then matched. An earlier draft incorrectly called h,r neutral Higgs components; the final
model uses extra gauge-singlet flavons and explicit gauge-invariant Higgs
alignment projectors, and counts their fields. No old certified result was
retracted. The initial intake found no forced arithmetic or certified-value contradiction; its named compound candidate was examined and cited above. **Final four-file intake PASS:** no rediscovery collisions, forced arithmetic or certified-value contradictions. Dedicated remote CI is checked in the publication receipt.

The strongest advances are a local metric-compatible operator, a fully
phase-gapped CP vacuum, and a dynamically selected family alignment with
an exact seesaw/CP interface. Smooth geometry, gauge-breaking directions,
a complete common parent action, coupling/scale selection, RG thresholds,
local gravitational constraints and renormalized vacuum energy remain open.

Primary external checks:

- [Vassilevich, heat-kernel coefficients, spin/vector operators and determinant conventions](https://arxiv.org/abs/hep-th/0306138).
- [Konishi–Minabe–Shiraishi, classical complex reflection groups including G6](https://arxiv.org/abs/1612.03643).
- [Brower et al., geometric lattice fermions and spin transport](https://arxiv.org/abs/1610.08587).
- [Sanyal et al., lapse/constraint analysis including BianchiI](https://arxiv.org/abs/1108.5869).
- [Babu–Macesanu, the standard10+126 SO10 seesaw](https://arxiv.org/abs/hep-ph/0505200).
- [Goh–Mohapatra–Ng, the126 versus16 matter-parity distinction](https://arxiv.org/abs/hep-ph/0311330).
- [Flavi, classical middle catalecticants](https://arxiv.org/abs/2208.07921).
