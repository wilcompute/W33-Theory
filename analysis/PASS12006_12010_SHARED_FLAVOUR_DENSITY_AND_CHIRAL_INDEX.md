# Passes12006–12010: shared flavour matching, colored thresholds, native density and non-Abelian index

17 October 2026. Reserved `3abc76ff9d85d51abebe1c5044bd7a564bfe5824`, following the five targets after12005. **No complete TOE, dynamically selected flavour vacuum, radiatively complete strong-CP model, native Einstein action or global non-Abelian Weyl measure is established.** The five targets are pursued through explicit maps, constructive repairs and negative controls rather than assumed solved.

## Prior-result audit

GitKraken fetched/reviewed the incoming formula-catalogue update `67084c5d5`; it adds no independent physical mechanism. Result searches and full relevant sections were checked against:

-11942: theta homes, supplied quark/lepton comparators, charge rule `z_e=6z_d`.
-11951/11955: inverse Barr construction and common SU5 heavy5bar matching;11960: real Majorana and Clebsch fitting conventions.12005 keeps bare quark matrices in the theta family.
-11989: real fitted `C` transmitting an actual complex vacuum to `B`.11996: the bounded72-real-field local CP branch. Neither owns a parameter-free theta-modulus selection.
-11601: metric/density mismatch, half-density map, standard Dirac heat coefficients and static4D benchmark. The new density construction is on the actual11995 native conductance chart, not the first heat/metric audit.
-12000/12002: literal native period words and the tree/path Wilson regulator. TOE59/TOE68 and11588 already own external flux/index controls and the warning against reading copies as generations.

The paper's flavour/open-problem statements and the current site frontier remain boundaries. No paper was edited. Standard external methods are cited below; these passes do not claim discovery of the general Schur, SUSY alignment, heat-kernel or overlap theorems.

##12007 — One shared heavy mixing matrix fits quark and charged-lepton ratios

Keep the CP-real common left torus

`tau=1+0.8744698731421595 i`, `epsilon_u=0.005520606513514881 i`.

The fitted down parameters, in the producer's eight-coordinate order, are

```text
(log Im tau_d, Im epsilon_d, Im z_d) =
(-0.3497011260666278, 0.09754766874005429, 0.04188033188719437)
B/mu = (11.279482901951425,
         8.059823963649515 -1.904101410788516 i,
        -6.844437562070213 -11.79584423547314 i).
```

The original N40 theta sums are recomputed. Remove the common left CP phase `diag(exp(i*pi*a²/3))`, and the corresponding right up phase, to obtain real bare matrices. With `K=I-b†b/(1+|b|²)` and its positive Hermitian square root `A`, use **both**

`Md=md A`, `Me=A^T me_bare`,

where `me_bare=[Theta(Omega_d,6z_d)]^T` in the same real CP basis. Applying A on the wrong side of the charged matrix changes the spectrum and fails an independent control.

All eight supplied quark comparators remain fitted. The charged ratios are

`m_mu/m_tau=0.05882238409`, `m_e/m_mu=0.004736949707`.

No independent charged-lepton fit parameters were added. The six down-quark observables depend on eight down-sector parameters; the two charged ratios make eight constraints. Numerical Jacobians give rank6 and rank8 respectively; the smallest joint singular value is approximately0.006208. Thus the charged data remove the two *local fit* directions at this marked point. This is local identifiability, not a global census or a dynamical vacuum principle. Up/down overall couplings, scales and all texture parameters remain supplied.

### The held-out absolute intersector scale FAILS

Using the same normalization on down and charged theta matrices gives

`y_b/y_tau=1.00213434`,

while the same declared MZ comparison masses give `2.86/1.74624≈1.638`. The relative discrepancy is about−38.8%. **This is an additional comparator not among the fourteen fitted ratios/mixings below.** Setting a separate charged overall coupling would remove the test, not explain it. RG evolution, thresholds or a different gauge/texture completion must be explicitly supplied and recomputed. An appeal to GUT bottom–tau unification alone is not a numerical running calculation.

### The same complex source also permits a real bare Majorana sector

Use the real positive matrix `n=L L^T`, with

```text
L = [[exp(p0),0,0], [p2,exp(p1),0], [p3,p4,1]]
p = (-0.2025558637,-0.8307011736,0.6056483157,
     -0.4519628527,-0.3915948555).
```

The effective Majorana matrix is `A^T n A`, while the charged left rotation is computed in the same Weyl convention as11955/11960. Takagi/SVD checks reproduce the supplied

`sin²theta12=.304`, `sin²theta23=.573`, `sin²theta13=.02219`,
`Delta m21²/Delta m31²=7.42e-5/.002511`.

No new complex phase is introduced beyond the common B source. The displayed witness has masses approximately `(0.002947,0.009104,0.050196)`eV after fitting the overall `Delta m31²` scale, and a convention-dependent illustrative Dirac phase about8.86degrees. **These are not predictions:** five real shape parameters fit four oscillation comparators; a numerical rank-four Jacobian leaves a local direction free. CP conjugation flips J and preserves masses and angles. All signed-quark/lepton comparisons require consistent conjugation when translating the holomorphic11942 convention into the physical Weyl convention.

An initial four-parameter zero23 texture stalled at log-residual0.13845; an unbounded trial also hit a positivity assertion. Neither proves a global exclusion. Allowing the remaining real Cholesky entry found a fit on the first reproducible seed. Attempts to continue by fixing p0 at offsets±0.1 did not retain all targets; those failed continuations are not a prediction band.

There are now fourteen fitted dimensionless flavour comparators: eight quark, two charged-lepton, four neutrino. There are fifteen fitted shape parameters (two up, eight down, five Majorana), plus overall scales. The held-out b/tau failure remains. This is a shared-source compatibility construction, not an overconstrained predictive SM fit.

##12006 — Connect that B to the actual bounded CP vacuum, and separate fitting from selection

Use the actual11996 first triplet `h`, with independent real and imaginary parts. Define the explicit **real fitted** coefficient matrix

`C=[Re b,Im b] [Re h,Im h]^+`.

Then `C h=b` and `C h*=b*`.11989 already owns this inverse real-coefficient method; here its target retains the theta-constrained bare matrices and the shared charged fit.

A specified auxiliary neutral complex triplet beta with positive term

`Vextra=M_beta² |beta-C h|²`

has its minimum at beta=C h. For fluctuations, the full block Hessian

`[[H+J^T KJ,-J^T K],[-KJ,K]]`

is congruent to `diag(H,K)` under `delta_beta=J delta_q+delta_eta`. Positive K adds six positive modes and preserves every old gauge zero; it changes no old stationary condition after elimination. The certificate independently checks this congruence on the stored actual32-coordinate core Hessian in normalized coordinates. Positive multiplier/spectator/mediator blocks retain their old scope.

This is a concrete added EFT transmission sector. C is a spurion/coupling input, not a derived H27/E6 invariant, and beta's transformation type must be compatible with those declared spurions. The theta parameters are still fitted constants; an isolated data fit does not stabilize fields. A sum of squared data residuals would select them by construction but would not constitute a UV principle. A lone complex SU3 fundamental with an invariant potential depends only on its norm, so its orientation cannot itself supply the missing relative CP alignment. Existing h/f/t tensors or additional spurions are essential.

##12008 — Full colored one-loop alignment control, not only neutral-scalar loops

On the actual joint four-flavour mass `M=[[m,0],[B,mu]]`, construct an eight-squark benchmark

`Sq=[[M M†+msoft² I,a M],[a M†,M† M+msoft² I]]`.

Take real supplied `msoft²=4`, `a=.3`, `m_gluino=.7`, `alpha_s=.1`. The producer declares its zero-external-momentum finite B0 matching, calculates both the quark mass phase and the gluino phase, and stores their combination `ImTr(M^-1 deltaM)-3 Im(deltaMg/mg)`.

**Exact alignment argument:** if `M=U diag(s) V†`, rotation by `diag(U,V)` makes Sq a direct sum of four **real**2×2 blocks. Every real spectral loop function therefore gives `deltaM=U diag(real) V†`; its determinant trace is real. The gluino mixing products in that same quark basis are real too. This proves vanishing of these two specified mass-phase channels without expanding B/mu or assuming small mixing. Independent tests also use a new random complex mass matrix.

Real but nonuniversal A coefficients spoil this argument. The explicit `epsilon=.01` Hadamard-pattern perturbation produces a combined phase approximately `1.77e-9`, above the illustrative1e-10 target. CP conjugation reverses it. Scaling every dimensionful quantity together leaves this dimensionless diagnostic unchanged. Merely raising a common soft scale is not protection.

A second exact control distinguishes *generic* dangerous leakage from aligned leakage: an upper block `c=r m B†`, real r, gives

`det[[m,c],[B,mu]]=det(m)(mu-r|B|²)`.

It is real positive when the parenthesis is positive. The certificate includes nonzero safe examples and a generic real perturbation that restores a phase. This alignment has not been protected or derived, and changing c requires refitting light observables. Positive Hermitian normalization preserving determinant phase is already11950 prior work.

This is a **separate supplied SUSY colored-soft benchmark**, not a SUSY completion of11996's non-SUSY72-field scalar potential. Gauge mediation must enforce the needed universality, B-sector alignment and gluino reality after thresholds/running. The old neutral-scalar portal, allowed operators, tadpoles, Higgs/electroweak and higher-loop terms remain. No total radiative strong-CP solution follows.

##12009 — Conductance and vertex capacity must encode the same metric

Let H(w) be the actual four-cover harmonic Dirichlet/conductance tensor of11995. Give every vertex in a frozen27-site cell the positive capacity

`M(w)=sqrt(det H(w))`, `G(w)=H(w)/M(w)`.

Then `sqrt(det g)=M`, with `g=G^-1`, and `H=sqrt(g) g^-1`. In general dimension d≠2 the exponent is `M=(det H)^(1/(d-2))`. Dimension2 is exceptional: det H must be1 and a conformal scale is left undetermined.

Eight positive-weight native lifts of a supplied small conformal profile verify the map. Independent generalized Bloch eigenvalues of `M^-1 L(w)` approach `p^T G p`; the ten-component non-diagonal metric map remains locally invertible. The Euclidean scalar action is the edge Dirichlet energy with inner product `sum_vertices M|phi|²`. No extra continuous time is silently added to this4D construction.

The unit-capacity negative control is exact. For H=exp(2sigma)I4, its principal metric is g=exp(−2sigma)I4 but the graph measure is dx. Unitary transformation to the geometric measure exp(−4sigma)dx produces

`P=−Delta_g+V`, `V=2 exp(2sigma) sigma_xx`.

For periodic sigma=epsilon cos x, let `I=integral exp(−2sigma) sigma_x² dx d³y>0`. The standard scalar heat coefficient obeys

`integral sqrt(g) R/6=I`,
`integral sqrt(g)(R/6−V)=−3I`.

Thus a curvature interpretation can even get the sign wrong if capacity/measure is ignored. The symbolic operator identity and independent quadrature/Bessel identity are tested.11601 owns the general metric/density warning and standard heat calibration; the contribution here is its native conductance/capacity realization and this explicit scalar negative control.

With a supplied smooth covariant continuum limit, the repaired Laplace–Beltrami heat coefficient has the usual R/6 term. A quantum determinant or spectral action also generates a cosmological term and higher-curvature terms. Neither its continuum limit, regulator moments, Einstein coefficient, Lorentz sign nor cancellation of other terms has been derived. Conditional EH through this invertible chart inherits the old continuum ADM algebra; the finite pointwise11976 bracket obstruction is unchanged. This repairs a prerequisite for a gravity derivation, not the derivation itself.

### Units and the actual coordinate-group action

For a real coordinate change `x=T xprime`, the conductance **density** transforms as `Hprime=|detT| T^-1 H T^-T`. The capacity then transforms as `Mprime=|detT|M`, and `Gprime=T^-1 G T^-T`. Exact rational matrix checks and a non-unimodular control verify this GL(4,R) action. The native GL(4,Z) subgroup redescribes integral deck markings and preserves M; it is not automatically an isometry of the graph or a new physical global symmetry. Omitting the determinant factor would conflate an inverse tensor with a density.

Native weights and labels are dimensionless. Introducing physical spacing a gives eigenvalues and curvature dimensions a^-2. In four dimensions `H->lambda H` gives `M->lambda² M` and `G->lambda^-1 G`, exposing the unfixed scale. Setting hbar=c=1 fixes units; it does not determine a, Newton's constant, the cosmological constant or the physical duration of a clock tick. A predicted physical constant requires an invariant dimensionless combination and a derived scale-setting mechanism.

##12010 — Non-Abelian transport on literal native edges and a nonzero native-path index

The clock-adapted periods are `T0=e4`, `T1=e1−3e4`, `T2=e2`, `T3=e3−2e4`. Assign a primitive e1 pivot the ordered product `U1(x) U0(x+e1) U0(x+e1+e0) U0(x+e1+2e0)`, and analogously dress e3 with two clock factors. e2 and e4 receive U2 and U0. Tree edges are identity. The compiled native period words cancel the clock tails in reverse order, yielding **any prescribed coarse SU3 links**, including noncommuting ones. No Abelian rearrangement of factors is used.

Independent local SU3 transformations dress every original native edge. Literal path products and tree Laplacians transform covariantly. Two-cell tests use noncommuting root holonomies, followed by another volume/orientation and random gauge control. This is an extension of12002's supplied path/tree regulator, not a proof for the old nearest-edge11991 operator.

A diagonal but genuinely SU3 bundle on a3^4 torus has color-line flux vectors `a=(1,−1,0)`, `b=(1,0,−1)`. Both sums vanish, every link determinant is1, and `ch2=a·b=1`. The actual gamma5 Wilson spectral signatures give color indices `(−1,0,0)`, hence total−1, with minimum gap approximately0.34551. Reversing the second flux gives+1. The sign follows the declared gamma5 orientation. TOE68 owns the external U1 positive control; here the SU3 links are explicitly realizable by the actual native paths.

Bounded tree conjugation separates one coarse acoustic sector and26 optical shifts. Each optical shift has ReD≥3 for all unitary links and deforms to an onsite massive kernel, so its index is0. The index therefore transfers to the native path operator by exact factorization. A dense full26244-dimensional SU3 native Dirac matrix (8748 per color) is not diagonalized; the acoustic index is numerical, not an interval eigenspectrum certificate. Direct tests check Ginsparg–Wilson and the chiral projector on the actual gapped flux block.

The supplied left-Weyl inventory is `Q(3,2)_1`, `uc(bar3,1)_−4`, `dc(bar3,1)_2`, `L(1,2)_−3`, `ec(1,1)_6`, `nuc(1,1)_0`, with integer charges6Y. Exact sums cancel SU3³, SU3²Y, SU2²Y, Y³ and mixed gravitational anomalies; there are four SU2 doublets per family, so Witten's mod2 obstruction vanishes. Three **supplied** copies contain48 internal Weyl components. They are not derived from doublers or inferred from the index.

A gapped finite-range overlap construction provides covariant projectors; anomaly cancellation is necessary but does not construct the full global non-Abelian fermion measure. Three generations, spacetime selection and an interacting continuum limit remain open. The new result is an explicit native non-Abelian transport/index carrier with the correct *declared* anomaly inventory.

A common microscopic action tying these constructions together remains open. In particular, the SUSY colored-soft benchmark is separate from the bounded scalar source, and coupling the chiral path operator to the variable capacity metric with its spin connection has not been constructed.

## External checks

- [Cherchiglia–De Conto–Nishi, single-vectorlike Nelson–Barr flavour](https://arxiv.org/abs/2103.04798); [Schwichtenberg–Tremper–Ziegler, E6 Nelson–Barr](https://doi.org/10.1140/epjc/s10052-018-6388-6): matching mechanisms are prior art.
- [Evans–Han–Yanagida–Yokozaki, SUSY Nelson–Barr](https://arxiv.org/abs/2002.04204): real gluino and universal/MFV soft terms are substantive conditions, not automatic consequences of SUSY.
- [Vassilevich, Heat kernel expansion](https://arxiv.org/abs/hep-th/0306138): scalar a2=R/6−V and higher heat coefficients are standard.
- [Kikukawa–Yamada, overlap axial anomaly](https://arxiv.org/abs/hep-lat/9806013); [Hernandez–Jansen–Lüscher, locality](https://arxiv.org/abs/hep-lat/9808010): overlap/anomaly/locality methods are prior art.

## Reproduction

Five same-stem producers and JSON certificates are12006 `vacuum_source_identifiability`,12007 `shared_theta_leptons`,12008 `colored_soft_thresholds`,12009 `native_metric_density`,12010 `nonabelian_native_index`. Run12007 first. Portable joint-charged and real-Majorana search drivers are included; their fitted records are exploratory, while the producer independently reconstructs frozen witnesses. The test file is `tests/test_w33_pass12006_12010_shared_physics.py`; hosted workflow checks frozen certificates, regenerates all five and checks again. Publication receipts separately record actual checks/run status.
