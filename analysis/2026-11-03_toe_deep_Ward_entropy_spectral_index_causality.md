# 2026-11-03 — Deep TOE-pattern audit: Ward identities, gauge-invariant entropy, topological index, spectral continuum and causal observables

**Status:** Five physics fronts attacked with six executable producers and six result certificates plus a focused regression suite. They include an actual modified-CLASS calculation, a 40,000-dimensional sparse overlap-sign *vector* action, and exact geometry/field-space constraints. **No theory of everything, full coupled-ultralight Boltzmann solver, full survey likelihood, global chiral Weyl measure, or quantized gravity is claimed.** This pass is new research rather than execution of every production-scale solver to completion.

## Intake, prior ownership and external literature

At intake, local checkout `C:\Repos\Theory of Everything` and remote `wilcompute/W33-Theory:master` matched at `f3593b2ae0675debc14521dd10d3669fab53f387`, with 54 pre-existing unrelated uncommitted files and no staged changes. The parallel 2026-11-03 physics commits and a separate uncommitted local mechanism package were checked before choosing this pass. Prior work already owns the fading CLASS fit, the first baryon/CDM transfer comparison, original small-L overlap flux index, the Q15 *Wilson kernel*, a first real-KG test, spectral graph normalized gap no-go, gravity phase/Bell counterexamples, and hyperbolic/moduli concepts. This pass's new additions are the **specific exact hyperbolic Ward calculation**, **tensor fiber/base scaling bridge**, **actual CLASS gauge-invariant relative entropy correction**, **large-Q15 matrix-free sign-vector calculation**, **retarded phase frequency resolution** and **wave Jeans history**; do not count preexisting parent results as our discoveries.

Research references:
- [Gauge conditions in dark energy and dark matter, Christopherson 2010](https://doi.org/10.1103/PhysRevD.82.083515); [Doran et al. gauge-invariant quintessence initial conditions 2003](https://doi.org/10.1103/PhysRevD.68.063505). Gauge-invariant relative entropy `S_bc=3(zeta_b-zeta_c)` is established literature.
- [Passaglia–Hu accurate axion EFA, PRD 2022](https://doi.org/10.1103/PhysRevD.105.123529); [Moss et al. 2025 axion CAMB EFA](https://doi.org/10.1103/fy1y-rjst): wave Jeans pressure is not a radiation-era Boltzmann substitute.
- [Aoki et al., lattice Dirac K-theory index, 2026](https://doi.org/10.1007/s11005-026-02080-w): overlap index `index=-Tr sign(H)/2` and stable topological spectral flow.
- [Singh 2026 spectral trace-dynamics framework](https://doi.org/10.3390/universe12070205): nearby ambitious, **hypothetical** unification framework, not an accepted proof that a finite graph yields the SM or spacetime.
- [Di Biagio 2026 gravity-induced entanglement locality qualification](https://doi.org/10.1103/r8ry-sp35); [Mitrakos et al. 2026 retardation/graviton thought experiment](https://doi.org/10.1103/lq47-1hfg): useful precisely because low-frequency static phase accumulation does not establish a quantum mediator.

## Front I — coupled ultralight oscillator: a dimensionful Jeans pressure boundary

`analysis/toe_20261103_ultralight_wave_Jeans_clock.py` and `data/toe_20261103_ultralight_wave_Jeans_clock.json`. The earlier repository implemented an exact finite-H homogeneous KG test and a separate approximate two-fluid growth simulation, **not** one validated relativistic EFA in CLASS. Here we connect the canonical WKB number `rho_c(a)=rho_c0 a^-3 m(a)/m0` to the ordinary nonrelativistic wave-pressure Jeans condition `k_J^4=16pi G rho_c mbar² a⁴/c⁴`, where `mbar=m_energy/hbar` in s^-1.

Thus `k_J(a)=k_J(0)*a^(1/4)*[m(a)/m0]^(3/4)` with no independent adjustable exponent. Using the *actual stored fading fit* beta and field excursion, m(recomb)/m(today)=**1.014928119**. With **illustrative input** m(today)=1e-20 eV, actual fitted Omega_c and H0 give `k_J(today)=982.615 h/Mpc`, `k_J(z~1090)=172.490 h/Mpc`, and mass variation shifts the latter by +1.118% vs constant mass. At k=0.2 h/Mpc wave pressure is tiny; at k=500 h/Mpc it overwhelms gravitational driving around recombination, so the pressureless CLASS spectrum CANNOT be extrapolated to those early small scales.

**Limit:** no full CLASS axion perturbation hierarchy, switching from exact KG to EFA, radiation transfer, Lyman-alpha hydrodynamics or lensing likelihood. The full first requested front is *partially executed* by its falsifier/scale analysis.

## Front II — a new gauge-invariant relative-entropy observable from actual CLASS

`analysis/toe_20261103_CLASS_gauge_invariant_species_entropy.py` and corresponding JSON. Two new **actual patched CLASS runs**: frozen fitted coupled model, and identical cosmological input with cprime=0. For each, used CLASS `o_background.dat` values of rho_b and rho_cdm to **measure** their logarithmic derivatives `r_i=dlnrho_i/dln a`; `o_z*_tk.dat` supplies d_b,d_cdm at z=0,1 and k=.05,.1,.2,1 h/Mpc.

At z=0, k=.1 h/Mpc: `delta_b/delta_c=.988014797` coupled vs `.993378090` cprime-off. The **naive** `(delta_b-delta_c)/delta_c=-.01198520` coupled is **not gauge invariant**, because r_c=-2.97507340, r_b=-3, unlike cprime-off where both are -3. Instead use **exact linear gauge-invariant entropy**
`S_bc=3(zeta_b-zeta_c)=3(delta_c/r_c-delta_b/r_b)`.
Under the common time slicing shift `delta_i->delta_i+r_i eps`, the S difference is exactly unchanged; this was tested numerically at ~1e-12 absolute. The ratio `S_bc/delta_c=-.02036368` coupled vs `-.00662191` control, more distinct than the naive ratio. **Important:** `S_bc` is gauge invariant; **S_bc/delta_c is not**, and neither ratio is directly observed. A tracer+lensing model must handle the normalizing perturbation and gravitational potentials in a chosen gauge. The CLASS background check also confirms `-3-r_c=beta*phi_N=-.024926596` in the fit, which independently validates the mass-exchange convention. No actual RSD or lensing likelihood added.

This is a stronger response to the previous `C_l^phiphi` nuisance projection: `S_bc` cancels the primordial overall amplitude in a **ratio** at fixed k while also properly incorporating coupled species dilution. But real galaxy bias and baryonic astrophysics can mimic it, so identifiability remains unproven.

## Front III — hyperbolic sigma-model Killing symmetry vs fading canonical mass

`analysis/toe_20261103_hyperbolic_isometry_ward.py`, JSON. Exact sympy test of a proposed unified two-field metric `ds²=dx²+exp(-2beta*x)dy²`, scalar curvature `R_field=-2beta²/Mpl²`, and Killing generator `K=partial_x+beta*y*partial_y` (x=phi/Mpl, y=chi/Mpl). Its finite flow preserves the kinetic metric exactly. Yet the canonical chi mass `mphys²=m0²exp(-2gamma*x)` arises from potential `Uchi=1/2 exp(-2beta x) mphys² y²`. Along K the potential has exact Ward variation `K Uchi=-2gamma Uchi`; for rolling V=V0 exp(-lambda*x), `K V=-lambda V`. Thus **within this specific model**, protecting both terms with a single exact isometry requires gamma=lambda=0 or absent terms. An exact kinetic isometry does NOT protect a varying canonical dark mass **and** rolling exponential dark energy.

This is not a general no-go against SUSY, a noncompact modulus, spurionic transformations, enlarged field space, axion monodromy or spontaneous symmetry breaking. In a genuinely unified EFT, however, the K Ward identity and its breaking terms must be explicitly specified instead of treating a hyperbolic metric as a quantum-protection mechanism.

## Front IV — W33 internal fiber and 4D torus continuum: exact two-scale obstruction

`analysis/toe_20261103_W33_fiber_4D_continuum_scale.py`, JSON. Constructed the 40 W(3,3) symplectic projective points and adjacency `A²=8I-2A+4J` from first principles; spectrum `A:{12:1, 2:24,-4:15}`, hence internal graph Laplacian `L:{0:1,10:24,16:15}`. A **supplied external 4D Cartesian torus base** `(Z/LZ)^4` with degree8 has first Laplacian eigen `4sin²(pi/L)`; combined Cartesian product graph has degree20, first normalized gap `[4sin²(pi/L)]/20`. Exact numerical L4 4D torus spectrum was cross-checked.

As L increases, base modes approach a gapless continuum while W33 24-dimensional modes retain internal eigenvalue 10. At fixed physical 4D linear size with lattice spacing a=1/L and the **same kinetic normalization** of base and fiber, physical base first Laplacian ->4pi², while internal first excited 24-plet ->10 L² **diverges**. To keep finite internal modes, an additional internal coupling scaling as `a²` or distinct internal radius must be specified. This is a **conditional scale separation**, not a no-go for weighted lattice fiber bundles, almost-commutative spectral triples, KK radii or actual finite internal geometries. The 4D torus topology and all other particle fields remain externally supplied. The bare W(3,q) normalized point graph gap tends 1 with q, so a tower of those alone does not produce ordinary continuum propagation.

This is an actionable bridge between the repo's finite information geometry and real 4D chiral overlap work: a valid TOE should DERIVE both the spacetime base and the internal/continuum scale ratio, rather than adding them by hand.

## Front V — Q15 overlap SIGN action and causal gravity bounds

**Chiral computational component:** `analysis/toe_20261103_Q15_krylov_sign_action.py`, JSON. Built upon the previously committed **40,000-dimensional Q=15 sparse Wilson kernel**, not a new discovery of the kernel itself. Actual matrix-free fully reorthogonalized 24/48/72/96/128-step Lanczos approximations to the nonlinear `sign(H_W)v` were computed on a reproducible normalized complex random vector. At m=128, `||sign_m(H)^2 v-v||=1.4587456e-7` in the double-action test; local U(1) gauge transformation of the vector and all links gives `||sign_96(H_g)Gv-Gsign_96(H)v||=2.31e-15`. The operator action now exists without a dense 40k eigensolve. A three-vector `H²` LOBPCG produced Ritz values ~.0126 but **did not reach its requested 1e-4 tolerance** (residuals ~.005); these are only variational *upper bounds* on the smallest eigenvalues, **not** certified spectral gaps.

**Still unproved:** exact large-Q15 index (expected magnitude q²=225 in the appropriate continuum flux sector), trace of sign(H), full sign matrix, uniform overlap locality, Weyl determinant bundle and gauge-Ward measure. Sparse matrix-vector tests do not certify a chiral QFT.

**Gravity component:** `analysis/toe_20261103_retarded_gravity_frequency_null.py` + JSON. For linear wave propagators, retarded massless Green at source frequency omega has `G_omega∝exp(i omega r/c)/r`; over r=200 μm one-way light travel is `6.6713e-13s`, so a 1 kHz drive produces only `4.1917e-9 rad` phase lag. To get a 0.01 rad delay requires **2.386 GHz**, while a **0.1 rad** delay needs **23.857 GHz** source modulation. A hypothetical 150 μm-range massive KG mediator switches from evanescent static to propagating at **318.09 GHz**. For mesoscopic masses, rapid modulation is plainly an engineering roadblock. The retarded Green-function response is **not** the measured entanglement fringe phase and does not prove a quantum graviton. Previously modeled classical static nuisance forces can mimic the phase response.

## Three out-of-sequence creative connections tested

1. **Ward identity as a cross-sector invariant:** A single sigma-model geometric symmetry creates simultaneous algebraic conditions on the kinetic metric, canonical dark mass and cosmological rolling potential. This is a more restrictive candidate unification principle than matching eigenvalue counts.
2. **Two-scale spectral fiber construction:** Finite W33 geometry can be tensored with a refining spacetime base and exactly decomposed, but the internal-vs-external kinetic normalization cannot be omitted. Here topology and graph spectra meet the **need for a 4D index-carrying regulator**; the bridge is currently conditional.
3. **Gauge-covariant observable versus fake signal:** What appears to be a baryon/CDM split in synchronous perturbations must first satisfy background-dependent slicing invariance. The actual CLASS gauge-invariant entropy test avoids this pitfall and provides a distinct, potentially amplitude-orthogonal target.

## Regression, preservation, and falsification policy

Producer outputs and exact computational assumptions are frozen separately in `data/`, code in `analysis/`, and scope assertions in `tests/`. Full CLASS producer requires the previously installed patched binary in authorized Ubuntu WSL; pure math uses Python, NumPy, SciPy, SymPy. Only explicit new files are staged; the 54 unrelated dirty entries are preserved. Focused tests and existing TOE cross-domain suites check the results, but **no full monorepo suite** is claimed. Reference commitments to lattice and gravity literature are priors, not achievements of our project.

**Remaining TOE gap:** No common local quantum action derives 4D causal geometry, chiral gauge matter, fermion generations, protected scalar vacuum, interacting ultralight dark sector, and gravity with numerical predictions and controlled renormalization. Our experimental/structural controls reveal where a future model must be tested.

### Top five orthogonal follow-ups

1. Derive and implement the full coupled-ultralight *linearized* CLASS hierarchy from a covariant field+particle-number action with correct gauge transformation, comparing exact KG to effective fluid through radiation era; follow the correct Jeans scaling.
2. Find an actual **gauge-invariant, experimentally extractable relative-entropy statistic** from baryon tracers plus lensing with transfer functions, bias calibration and public survey covariance, and fit it jointly with primordial As/ns.
3. Construct an exact quantum-protected two-field *or larger* Lagrangian with a clearly stated Noether/shift/supergravity symmetry, all portal thresholds and radiative breaking, and a rolling positive-energy solution.
4. Obtain a **certified spectral gap** and trace/index of the L10 Q15 overlap SIGN kernel using a rational-sign or spectral-flow method with error bounds, then test the global Weyl gauge measure and anomaly canceling reps.
5. Propose a causal, retardation-sensitive gravity test beyond quasistatic micrometer phases; compute realistic source bandwidth, decoherence, electromagnetic/Casimir backgrounds and mediator locality countermodels.
