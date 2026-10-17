# Passes12026–12033: the theta-vacuum fibre, a linked-spurion theorem, native heat curvature and determinant topology

17 October2026. Reserved `d547e4175e908bb7cbdff2066cee5423c97d619f`. This investigates all five requested followups and three additional connections. **No complete TOE, selected theta vacuum, full precision MSSM threshold calculation, total strong-CP bound, nonlinear native Einstein action or global native chiral measure is established.** Papers are unchanged.

## Intake and ownership

Fetched/reviewed/pulled `f176e17a9`, a formula-catalogue-only update indexing12021–12025 and site line offsets. Further refreshes found no incoming science before publication preparation. Preserved peer files. Continuity context and theta decisions were searched before edits.

Read the12021–12025 sources/certificates,12022 parent,12009 density gate,12019 dispersion,12000 native words,12002 coarse/heavy factor and the forty-points paper's physics frontier. Result-first searches included linked-spurion/cubic gluino/Vandermonde, the heat-Hessian coefficients, toron determinant Chern numbers and fixed-density response. Earlier pump scripts already use Fukui–Hatsugai–Suzuki; this packet cites them and does not claim that algorithm. Earlier11601/12009 own the continuum density warning and factor-3 negative control. Standard Jarlskog invariants, Passarino–Veltman functions, covariant heat perturbation and determinant-line topology are prior art. New content is the named native/texture map, explicit coefficient and operator controls, not those general methods.

##12026 — what the matrix vacuum actually fixes in theta space

Pull the12022 parent back through the actual new theta/Barr texture:

```
V(x)=Uu(x)^dag Ud(x),
A=diag(1,2,4), B=V diag(1,3,7)V^dag,
X=A², Y=B².
```

Here x has ten real theta/Barr shape coordinates; the matching scale is held fixed. The six radial invariants are constant on this map. The four orientation invariants have rank4. Their pullback therefore has a **regular six-dimensional local vacuum fibre**, even though the parent has exactly two matrix-space orbits. The two statements concern different spaces and are compatible.

Explicit nonlinear continuations preserve all four mixing comparisons to better than1e-8 while changing quark mass ratios. One displayed step changes two logarithmic mass ratios by about.0387 and.0414. The full eleven charged/quark residuals have rank10 at fixed scale; adding data-target functions could isolate the fitted shape point, but would again fit the potential rather than derive its coefficients.

This names the missing map and the remaining stabilization problem. It neither retracts12022's correct global matrix-space theorem nor promotes engineered coefficients to a native prediction. A compactification/UV interaction must fix these actual theta directions, including their kinetic normalization and allowed counterterms.

##12027 — an exact linked-spurion family, and its first surviving gluino term

Let M be positive diagonal and E Hermitian. For real l,r,a,b define the positive squark family

```
S=[[l I+epsilon E, a M],
   [a M, r I+eta b M E M]].
```

### Exact quark-safe theorem

For every real spectral function f,

```
Im Tr(M^-1 f(S)_LR)=0,
Im Tr(M f(S)_LR)=0.
```

This covers arbitrary epsilon and eta as long as S stays positive; it is not just a low-order expansion. For real z outside the spectra define

```
A=(z-l)I-epsilon E,
D=(z-r)M^-2-eta b E,
Q=(D A-a² I)^-1.
```

Schur elimination gives `[(z-S)^-1]_LR=a Q M^-1`. Both A,D are Hermitian. The identities `Q^dag=(A D-a²)^-1`, `Q^dag A=A Q` and `Q D=D Q^dag` imply that TrQ,TrAQ,TrDQ are real. M^-2 is a real linear combination of D,A,I. Hence both weighted resolvent traces are real. Continuity handles zero epsilon or exceptional intermediate inverses; spectral residues give the real-function statement.

The first identity protects the specified quark determinant-trace self energy. The second would protect the gluino channel if every internal quark used the same loop function. **The actual gluino self energy uses B0(m_i²,S), different for each species**, so the second identity does not establish its full cancellation.

### First surviving response, with a positive coefficient

Write `J_E=Im(E12 E23 E31)`, `x_i=m_i²` and `Delta_i(q)=(q+l)(q+r)-a² x_i`. A symbolic2x2 path-product calculation proves

```
Im [R(VR)^3]_LR,ii
 = a b m_i (x_j-x_k)(q+r) J_E / prod Delta,
```

for cyclic i,j,k, where R=(q+S0)^-1. The quark and common-function gluino sums cancel. With the actual species weights,

```
sum_cyclic x_i(x_j-x_k)/(q+x_i)
 = q (x0-x1)(x1-x2)(x2-x0)/prod(q+x_i).
```

Therefore the coefficient of epsilon² eta in the stated one-loop gluino phase is exactly

```
3 alpha/(2 pi mg) * a b J_E * Vandermonde(x)
 * integral_0^infty (q+r)q²/[prod Delta_i(q) prod(q+x_i)] dq.
```

The integral is strictly positive for the declared positive baseline. Quadratic terms and the cubic epsilon eta² term vanish. This coefficient is nonzero precisely when the CP triangle, all three mass differences and the prefactors are nonzero. It is a concrete GIM/Jarlskog factor in an actual loop response, not a new discovery of the general invariant.

On the well-conditioned witness the coefficient is `-2.24783624948e-6`; finite-phase/t³ controls at t=.1,.05,.025 converge quadratically to it. CP conjugation flips the sign; simultaneous family permutations preserve it; a degenerate mass pair kills it. Mass-rescaling probes record the strong small-mass suppression without asserting a physical total theta bound.

**Boundary:** enforcing this linked relation through the complete UV/soft RG is not proved. Actual running may generate independent LR or opposite-side structures, neutral portals and higher-loop terms. The exact quark cancellation and the positive cubic gluino kernel concern only the stated colored channels.

##12028 — finite wave-function matching supplies the missing RG logarithm

The12024 threshold included only the leading tanbeta-enhanced SQCD chirality term. Now diagonalize each actual real2x2 up/down squark block, including quark mass squares, the declared EW D-terms and LR=`m(A-mu tanbeta)` or its up-type cotbeta partner. Include both p=0 SQCD terms:

```
delta_chirality = pref*M3/m [B0(M3²,S)]LR,
delta_wavefunction = -pref/2 sum_eigen B1(M3²,mSq²),
pref=2 alpha_s/(3pi),
B1(a,b;Q)=-integral_0^1(1-t) log([ta+(1-t)b]/Q²) dt.
```

Solve `mSM=mbare(1+delta(mbare))` self-consistently for all six quarks. Matching acts in each singular basis, then the matrices are restored and evolved through the same one-loop SM/MSSM EFTs. The benchmark spectrum and historical low-scale inputs remain supplied.

For the down sector, the chirality contribution is about.03570 and the additional wave-function term about.00198. Up-sector wave-function terms are about.00252–.00255, larger than their chirality term. Actual eleven-comparison rematching gives a fitted scale **27,767,815.50GeV**, versus30,103,970.50GeV in the previous leading-only benchmark.

The wave-function term has an exact structural check:

```
d delta/dlog Q = -2 alpha_s/(3pi)
 = beta_Y,SM,QCD/Y - beta_Y,MSSM,QCD/Y.
```

The chirality term alone misses this one-loop matching-scale logarithm. Independent inverse evolution through both EFTs and the finite matching map recovers the supplied low comparisons. Common rescaling of every mass, vev and Q leaves the dimensionless threshold unchanged.

This is the complete **declared p=0 aligned SQCD mass channel**, not complete MSSM threshold matching. Finite external momentum, electroweak/chargino/neutralino/Higgs/lepton diagrams, scheme conversion, full soft RG and an electroweak/UV vacuum remain uncomputed. No current experimental or pole-spectrum claim is made.

##12029 — curvature response from the actual native heat trace

Use all27 Bloch bands and135 midpoint-weighted native edges, with the12023 harmonic drawing. Set `sigma=epsilon cos x0`, capacities `M0 exp(4sigma)` and the actual symmetric operator `A=M^-1/2 L M^-1/2`. Compute its first and second epsilon derivatives exactly at zero. A1 couples neighbouring longitudinal momenta; the heat Hessian uses the exact divided difference of `fprime(lambda)=-t exp(-t lambda)`. No continuum R/6 coefficient is inserted into the native calculation.

The observable subtracts a local zero-derivative response using the **same native spectrum**:

```
C_a(t)=(4pi t)²/(Vol*t)
 [d_epsilon² Tr exp(-t A_cos)|0
  - onehalf*d_epsilon² Tr exp(-t A_uniform)|0].
```

At physical heat times t=(.08,.12,.18), the independent continuum torus benchmark is approximately(.43756803446,.46635276305,.50410876128). The actual native responses are:

| cells per direction | t=.08 | t=.12 | t=.18 |
|---:|---:|---:|---:|
|8|.6151812783|.5874954724|.5700783057|
|12|.5004554109|.5019086286|.5264608013|
|16|.4655407883|.4841189159|.5158715866|
|24|.4486275552|.4737166382|.5091163524|

The portable extended record adds N=32. Refinement improves every displayed continuum error. The inversion-related momentum reduction is independently checked against an unreduced sweep. A separate real-space assembly of the variable operator checks the heat Hessian by finite epsilon differences, agreeing within9e-8 on its declared test.

Keeping native capacities fixed instead gives negative responses, approximately(-1.1020,-1.0455,-.9841) at N=16. This is an actual native-spectrum density control, extending the already-owned continuum warning12009.

A generalized source-code parameterization initially omitted one continuum A2 contribution; the first unpublished reference certificate was rejected/recomputed. The corrected general coefficient is `(8c²+2-8c)lambda+4c² lambda_q`, and the geometric c=1 case recovers `2lambda+4lambda_q`. Only the corrected certificate is published.

**Boundary:** these are finite native heat responses and numerical fixed-time refinement, not a uniform spectral/heat-trace convergence theorem or a nonlinear Einstein derivation. The scalar determinant supplies evidence toward a curvature term only with stated regulator/counterterm and continuum assumptions. Physical G, Lambda, Lorentzian constraints and the native action remain open.

##12030 — beyond one frame patch: determinant topology on a whole torus

The finite4D Wilson family has two one-cell directions carrying Wilson-line parameters alpha,beta, and a6x6 magnetic plane with flux1. Charge q sees flux q. Compile the actual12000 native period words after the actual unimodular clock marking. Their links differ from straight magnetic links only by explicitly checked constant phases; the Chern computation uses those compiled phases.

Use arbitrary local positive-projector eigenframes and determinant overlaps across the entire parameter torus. This is a multi-patch calculation, unlike12025's single-reference rectangle. On resolved meshes the effective-charge torus gives C=-q. Physical Wilson-line parameters map `(alpha,beta)=(q theta0,q theta1)` with covering degree q², hence a contribution `-multiplicity*q³`.

For10+bar5 under integer6Y the charges/multiplicities are

```
q:       1,  2, -3, -4, 6
mult:    6,  3,  2,  3, 1
C_base: -1, -2,  3,  4,-6.
```

The physical contributions sum to zero. This is standard anomaly cancellation realized on the stated finite native-path-compatible determinant family; it does not select three generations or derive the flux.

There is a consequential failure control. N=8 gives a false aggregate Chern of-48. For charge6, even N=12 returns-2 instead of-6 while its kernel gap is positive and its sampled plaquette phases are below pi. N=16 and24 resolve the expected integer. Thus integer-valued output, a kernel gap and a sampled phase cutoff are insufficient resolution certificates.

Each toron derivative of the Hermitian kernel has norm1. A sampled minimum gap minus2pi/N is therefore a whole-torus Lipschitz lower bound, up to eigensolver rounding. The positive refined margins are recorded. They control the gap, not by themselves the mesh Chern integer. No interval-certified general index theorem is claimed.

A nonzero sector Chern obstructs a single smooth global sector frame; anomaly cancellation removes that tested sum on this two-cycle. It does **not** construct the non-Abelian current on every configuration component, settle every global anomaly, or give all-volume locality/admissibility bounds. The optical determinant lines still rely on12002's stated factorization. A global native measure remains open.

##12031 — the old parent and the new matching branch are different inputs

The12022 parent targeted the12011/12017 quark orientation. Substituting the12028 branch into that unchanged potential gives positive energy about1.79323e-7. Retargeting its four orientation coefficients makes the new branch a zero and retains28 positive modes/eight symmetry directions and the generic CP pair. The changed coefficients are stored explicitly.

This is a compatibility repair, not a coefficient prediction. It prevents separately fitted packets from being presented as a single already-selected vacuum.

##12032 — derive the heat form factor and keep the regulator limits separate

An independent Gaussian/Duhamel calculation supplies a continuum local benchmark. Let x=t qG0q, capacity exponent beta, c=beta/4, d=1-2c, v=u(1-u), b=d(1/2-v)-1/2. Completing the momentum square gives

```
C(t)=M0/t [-12d²-4c²x
 +2 integral_0^1 exp(-xv)
    {6d²+x[d²(2u-1)²/2+4db]+x²b²} du].
```

For geometric capacities its exact dimensionless series is

```
x + x²/2 -17x³/140 +x⁴/72 +O(x⁵).
```

Thus its small-time curvature coefficient is H00=10/27. Fixed capacities give leading-3x and coefficient-3H00. The coefficient is derived from Gaussian moments; it is not inserted from a presumed R/6 law. The factor-3 continuum observation belongs to12009; this independent form-factor/numerical native comparison connects it to the actual regulator.

Finite torus winding effects and finite proper time are kept distinct from lattice errors. Refining a->0 at fixed physical t and then taking t->0 is different from keeping t/a² fixed at a native cutoff. The present data do not prove that exchanging these limits gives the same induced G. Bare counterterms, matter inventory and physical cutoff remain inputs. Natural-unit rescaling leaves dimensionless matching/heat data invariant; integer counts do not select an absolute mass or Planck scale.

##12033 — a conditional neutrino curve instead of a single apparent prediction

Rematch the real Majorana ansatz on the new12028 branch, with one-loop C5 shape above/below Ms and the supplied atmospheric normalization. The four oscillation comparisons leave one local shape direction. A naive fixed-q4 chart and a large fixed tangent chart failed; these attempts are not global exclusions. Adaptive SVD arclength continuation and normal correction produce ten fitted points, with the bad-coordinate attempt retained as a negative control.

Along the displayed local segment, all four comparisons remain fitted while the lightest mass varies about.003950–.004558eV, m_beta_beta about.001055–.001087eV and J about-.02575 to-.00942. These are **local witness ranges and a conditional correlation**, not a global allowed interval, a unique physical prediction or an updated experimental fit. The source records every parameter point and residual. A shared CP source narrows a model family; it does not remove its remaining free coordinate.

## Primary external checks

- [SUSY Nelson–Barr](https://arxiv.org/abs/2002.04204), dangerous soft insertions; general Jarlskog/GIM invariants are established prior art.
- [Threshold corrections revisited](https://arxiv.org/html/1411.7035v1), AppendixA/equations26–29,41 and the warning against dominant-only matching. The implementation uses explicit Feynman-parameter B0/B1 definitions to fix signs and Q dependence.
- [Covariant heat perturbation](https://arxiv.org/abs/0811.1063); [Vassilevich](https://arxiv.org/abs/hep-th/0306138). These do not substitute for a native convergence proof.
- [Fukui–Hatsugai–Suzuki](https://arxiv.org/abs/cond-mat/0503172), determinant-link Chern method; [Lüscher](https://arxiv.org/abs/hep-lat/9904009), anomaly/determinant-line geometry.
- [Craig candidate measure](https://arxiv.org/html/2610.09093v1), the distinction between local curvature, all closed-loop integrability and uniform locality. No independent certification of its long proof is asserted.

## Reproduction

Three producers:12026–12033 connections,12029 native heat and12030 determinant torus. The heat producer accepts `--sizes 32 --output data/w33_pass12029_native_heat_extended.json` for the extended record. All computations use repository-relative paths. The focused regressions include inverse SQCD EFT matching, arbitrary-function trace identities, symbolic cubic kernels, an independent real-space heat operator and coarse-mesh topology failures. Publication receipts separately bind actual tests/artifacts to the science commit. One native microscopic action selecting the physical coefficients, vacuum, constants and Einstein dynamics remains missing.
