# Five physical mechanisms, plus a holomorphic compatibility test

This packet investigates the five targets in `analysis/2026-11-03_toe_physical_completion.md` through seven explicit calculations. The useful positive results are a stationary positive-energy **neutral** effective vacuum, a genuinely four-dimensional flux overlap operator, and a renormalizable full-rank Dirac messenger chain. Their limitations prevent calling them a solved TOE, a common UV action, or a complete interacting chiral Standard Model.

The previous packet owns its six audits, per decision-a2603691-8202-45e1-9a73-d8b3c62e6485 [cite:5c4ab4]. The computations here import its actual supergravity model and stored fading fit rather than replacing their inputs with convenient rounded numbers. Master was fetched and reviewed at `59151dee68a85202d3770f7c92c30498f3de7d08`; no newer remote commits were present at intake. Unrelated local work is protected by raw hashes. The GitKraken connector is unavailable, so ordinary CLI Git is the documented fallback. Continuity MCP points to the empty project mirror; deliberate changes were logged to the actual repository journal/local CLI.

## 1. Radiative protection: an actual portal transmits soft breaking

Producer: `analysis/toe_20261103_mechanism_portal_protection.py`; certificate: `data/toe_20261103_mechanism_portal_protection.json`.

Declare global SUSY with canonical K and

`W = m(Phi) D Dbar + M S²/2 + y S D Dbar`.

At `D=Dbar=S=0`, with `F_Phi=0`, the bosonic and fermionic spectra of the dark pair coincide for every Phi. Their one-loop vacuum determinants cancel pointwise. Perturbative Kähler corrections alone cannot lift an F-flat global-SUSY background. This is a real protection mechanism under these assumptions; it is not the positive-energy rolling cosmology.

Now give S a positive UV soft mass and set the dark UV soft masses and A term to zero. Above the S threshold, hold y fixed and use the declared one-loop equations

`16 pi² d m_i²/d ln(mu) = 2 y² (mS² + mD² + mDbar²)`.

The exact solution of these equations is

`mDsoft² = (mS_UV²/3) [exp(-6 y² L/(16 pi²)) - 1]`, `L=ln(UV/IR)>0`.

The IR contribution is **negative**, not automatically a positive mass splitting. A tachyon is possible if its magnitude exceeds the supersymmetric mass². Independent numerical integration of the three coupled equations checks the expression. An independent server RK4 calculation differs by less than `1.5e-16` in its dimensionless control.

The complete one-loop two-complex-scalar minus Dirac determinant is differentiated at high precision, including the negative soft shift. At subtraction scale `mu=m(today)`, its small-soft curvature is

`delta mPhi² = cprime² m² mDsoft²/(2 pi² Mpl²)`.

Using the actual stored Dovekie negative-c fit, `cprime=0.05004260057022673`, and **supplied** `mDM=1 GeV`, `mSsoft=1 TeV`, `L=10`, the absolute-curvature benchmark `|delta mPhi²|<=H0²` requires approximately

`|y| <= 8.753026297780048e-25`.

This is conditional naturalness in a specified subtraction prescription and portal model, not a measured coupling exclusion. It quantifies how badly a seemingly sequestered sector can fail once one explicit mediator sees soft breaking. No gauge, anomaly-mediated, A/B-term, thermal, or full running-Yukawa calculation is hidden inside this number. The complete common-soft determinant and exact-SUSY cancellation already occur on the different flavor texture in `analysis/w33_pass12034_12038_joint_mechanisms.py:radiative_fibre`, which credits11909/11935; these methods are reused controls. That packet's full MSSM trilinear-running model is also distinct from the simple explicit S-D-Dbar mediator here. General soft RG equations are established physics, including [Martin, section6.5](https://arxiv.org/abs/hep-ph/9709356). Coupled-dark-sector loop concerns have prior treatments, e.g. [D'Amico/Hamill/Kaloper](https://arxiv.org/abs/1605.00996). We do not claim a new protection theorem.

## 2. A stationary uplift, and why it still fails as a full completion

Producer: `analysis/toe_20261103_mechanism_stationary_uplift.py`; matching JSON in `data/`.

The previous minimal nilpotent uplift canceled the AdS energy but left a nonzero gradient. Here change the **declared Kähler metric**, rather than pretending that gradient vanished:

`K = K0 + exp(K0/Mp²) Xbar X`, `W = Wprior + f X`, `X²=0`.

At X=0,

`exp(K0/Mp²) K^(X Xbar) |f|² = |f|²`.

Thus `V=Vprior+|f|²` at every ordinary-field value. Every old critical point remains critical; its ordinary-field Hessian is unchanged. This follows from the general nilpotent supergravity potential, not an energy-only numerical check. See [Kallosh's matter-coupled construction](https://arxiv.org/abs/1509.02136) for the framework; the engineered function and energy are inputs here.

For the prior epsilon=.001 real branch and Mp=30:

| Quantity | Result in supplied common mass units |
|---|---:|
| Prior AdS energy | -4.788422495918651e-8 |
| Chosen f² | 5.267264745510516e-8 |
| Chosen positive energy | 4.788422495918651e-9 |
| Maximum ordinary DW residual | 3.13e-16 |
| Smallest neutral scalar mass² | 0.4396003282 |
| Largest neutral scalar mass² | 4.5828677113 |
| Gravitino mass | 4.2112822433e-6 |

The sixteen real neutral masses are positive. No eV/Planck calibration or observed dark energy follows from these input-unit values. Only the eight-complex-field neutral EFT plus the constrained goldstino is audited, not all charged matter, gauge modes, fermions, quantum corrections, or tunneling.

Three further tests expose the cost of the construction:

* **Metric sensitivity.** Multiplying the nilpotent metric by `exp[eta sum w_i |phi_i-phi0_i|²/Mp²]` leaves this point stationary and shifts every real canonical mass² by `-eta f²/Mp²`. The first neutral instability occurs near eta=`7.51e9` in this heavy neutral example; eta=1 is harmless. This is an explicit sensitivity calculation, not a claim that generic small deformations destabilize these heavy modes.
* **Light spectator.** Add a canonical Q with W independent of Q. The AdS mass `-2 mgr²` survives the constant uplift: here `-3.5469796266e-11`, a de Sitter tachyon. Excluding Q from the exponent instead adds `f²/Mp²` and yields `+2.3055367573e-11`. That repairs the sign but does not protect an ultralight quintessence mass. Independent symbolic expansion checks both signs.
* **Goldstino cutoff.** The order-of-magnitude Volkov-Akulov scale is `(f²)^(1/4)=0.0151494`, whereas the largest neutral mass is approximately141 times larger. The full heavy-matter/nilpotent EFT therefore needs a UV completion above that cutoff. A background and its formal Hessian are not evidence of controlled scattering at those heavy masses.

Positive-energy stationarity is achieved in the declared neutral potential. A realistic, controlled positive-energy vacuum with all required light sectors is **not** achieved. The cancellation function and target energy are chosen, not selected by a symmetry or derived from quantum gravity.

## 3. Four-dimensional chirality: leave the paired graph kernel explicitly

Producer: `analysis/toe_20261103_mechanism_four_dimensional_overlap.py`; matching JSON in `data/`.

The old owner `analysis/w33_20261010_toe41_w33_overlap_index_nogo.py` was read in full with its report. Its SVD proof forces index zero for every gauge configuration of its **specific paired** 40-by-40 W33 incidence kernel. It remains correct.

The new calculation instead supplies a periodic **Euclidean four-dimensional hypercubic lattice**, compact U(1) links, four-component spinors, and a nearest-neighbor Wilson operator. With m0=1 in lattice units:

`H=gamma5(DWilson-m0)`, `D=I+gamma5 sign(H)`,

`hat_gamma5=gamma5(1-D)=-sign(H)`,

`D hatPminus=Pplus D`.

These are standard [Neuberger overlap](https://arxiv.org/abs/hep-lat/9707022) and [Lüscher chiral symmetry](https://arxiv.org/abs/hep-lat/9802011) constructions. We implement actual matrices and the rectangular Weyl kinetic map in topological flux backgrounds:

| Lattice | Fluxes in12,34 | Index in the exported orientation | Dirac zero modes |
|---|---|---:|---:|
| 3^4 | 0,0 | 0 | 4 free zero spin components |
| 3^4 | 1,1 | -1 | 1 |
| 3^4 | 1,-1 | +1 | 1 |
| 3^4, perturbed links | 1,1 | -1 | 1 |
| 4^4 | 1,1 | -1 | 1 |

The largest matrix has1024 complex spinor dimensions. The index convention comes from the declared gamma ordering and oriented links. No sign is silently fitted. GW identities, projector intertwiners, full on-site gauge covariance, spectral gaps, the index-density trace, and the domain/codomain mismatch are checked. Free Brillouin corners have one zero species and fifteen lifted corners: this Wilson corner audit and the supplied4D gauge-covariant construction are already owned by `data/PART_4057_4064_ADVANCED_PHYSICS.json:pass4060_gauge_covariant_wilson_matter`, read in full after the guard surfaced it. They are prior controls, not a new discovery here. Server code independently checks486 and1536 plaquettes on the two sizes, with phase errors below9e-16.

The chiral charge example `[-9,-5,-1,7,8]` passes `sum q=sum q³=0`; this is only an anomaly-polynomial check. **An integrable gauge-field-dependent Weyl measure, determinant phase, fermionic backreaction, Ward identities and full interacting chiral dynamics are not implemented.** Wilson gauge action evaluation does not supply those objects. The literature contains an actual Abelian measure construction, [Lüscher1998](https://arxiv.org/abs/hep-lat/9811032), and recent Hamiltonian work discusses locality/chiral-charge tradeoffs, [Singh2025](https://arxiv.org/abs/2505.20419). We do not claim to reproduce either complete construction.

The geometry is supplied independently of W33. Nonzero index here neither refutes the paired-kernel obstruction nor derives spacetime, the SM gauge group, or three generations. A finite positive kernel gap also does not prove uniform locality or a continuum limit.

**Current-literature follow-through.** A fresh search found [Craig, October6,2026](https://arxiv.org/abs/2610.09093), which claims a gauge-invariant nonabelian overlap measure for a class including the SM. We read its reconstruction conditions and finite projector-comparison lemma, not all123pages/companions, and have not independently audited the claimed full theorem. It supplies a concrete candidate route rather than grounds to declare the measure problem solved in this repository. As a small independent geometric check, `analysis/toe_20261103_projector_cylinder_controls.js` computes Berry/Kato determinant transport on a rank-one projector cylinder. The endpoint-holonomy ratio converges to the integrated-curvature phase, with complex error2.70e-8 at8192steps. A separate flat connection on a circle has zero curvature but loop phase-1, demonstrating why local curvature checks alone cannot establish global integrability. These are prior geometric identities, not a reproduction of the4D current, refinement bounds, SU5 proof or gauge dynamics. The repo already uses Kato transport in `data/PART_4057_4064_ADVANCED_PHYSICS.json:pass4057_counterdiabatic_holonomy`; this does not reclaim that transport construction. The coarse flux examples are not shown to obey the new paper's admissibility threshold. The source and actual server result are stored in the matching JSON.

## 4. Neutrino UV messengers: full-rank construction with real costs

Producer: `analysis/toe_20261103_mechanism_neutrino_messengers.py`; matching JSON in `data/`.

Keep the previous left-handed sterile charges `(4,4,-5)` in ordinary B-L units, scalar Phi of charge3, and residual Z9 in the quark-normalized direct-product group. Add three pairs `(N,Nc)=(-1,+1)` and one pair `(B,Bc)=(-2,+2)`, all SM singlets. Each pair cancels its own gravitational/cubic anomaly. Use the renormalizable Weyl Lagrangian

`Y_ia (L_i H) Nc_a + MN_ab N_a Nc_b`

`+ lambda_ar N_a Phi^dag n_r + kappa_a N_a Phi B`

`+ xi_a Bc Phi^dag Nc_a + MB B Bc + eta Bc Phi nC + h.c.`

All vertex charges are audited. The **reverse xi vertex is allowed** and included; an attractive triangular diagram is not a reason to omit it. The exact tree Schur complement is

`mnu=-vH Y S^-1 [lambda Phi^dag, -kappa eta Phi²/MB]`,

`S=MN-kappa xi |Phi|²/MB`.

With n entry N messengers, `rank(mnu)<=rank(Y)<=n`. Hence two entry messengers cannot give three nonzero tree masses in this topology, regardless of how long the final chain is. Twelve random controls check rank2; the proof is matrix factorization. Scalar-mediated or loop-generated completions are outside this rank statement.

Three N pairs plus one B pair suffice. For the exported exact rational witness,

`det(mnu/vH)= -10 epsilon^4/(9 epsilon²-10)`.

The physical singular masses of the full seven-by-seven Dirac matrix agree with the low-energy Schur masses up to the expected small kinetic-normalization corrections. The two epsilon columns and one epsilon² column emerge from actual renormalizable vertices, not assigned Wilson coefficients alone.

The idea is established prior physics: [Ma/Srivastava2014](https://arxiv.org/abs/1411.5042) and their [2015 proceedings](https://arxiv.org/abs/1504.00111) discuss exotic-charge Dirac seesaws. A [September2026 alternative](https://arxiv.org/abs/2609.06494) uses different breaking charges and radiative inverse-seesaw assumptions; it must not be mistaken for this Phi-charge3 protected Dirac model.

Arbitrary complex Yukawas still permit rather than predict flavor data. Three generations, the breaking scale, ordering, CP phase, PMNS angles and absolute masses remain inputs or open questions. The new pairs add `28/3` to the one-loop BL beta coefficient **above their thresholds**, changing the nonsupersymmetric exotic value `149/3` to59 there. Applying59 all the way from TeV to a1e16GeV messenger mass would be wrong. An O(1) Y with such a large MN also gives an enormous conditional Higgs threshold estimate `Tr(YdagY) MN²/(8 pi²)`; no natural electroweak hierarchy is obtained for free.

## 5. Joint gravity observables: discriminate a model, preserve degeneracies

Producer: `analysis/toe_20261103_mechanism_gravity_identifiability.py`; matching JSON in `data/`.

Declare weak, unscreened universal conformal scalar-tensor gravity. Define alpha² as the massless scalar/tensor force ratio and lambda as the scalar range. Then

`Phi=-Gt M(1+alpha² exp(-r/lambda))/r`,

`Psi=-Gt M(1-alpha² exp(-r/lambda))/r`.

The optical potential `Phi+Psi=-2Gt M/r` has no leading conformal-scalar term. Slow-body force calibration at r instead measures

`Gforce=Gt[1+alpha²(1+r/lambda)exp(-r/lambda)]`.

The code evaluates actual branch potentials for the two-mass controlled phase and an independent ray integral for bending. Thus bending relative to GR with the **same finite-distance force calibration** is

`R=1/[1+alpha²(1+r/lambda)exp(-r/lambda)]`.

For a massless scalar, static mass-only phases match at every alpha after calibrating Gforce, while R=`1/(1+alpha²)`. The familiar gamma=`(1-alpha²)/(1+alpha²)` limit agrees with [Damour/Esposito-Farèse](https://arxiv.org/abs/gr-qc/9602056). For finite range, potential-slip gamma and force-calibrated R are different quantities; the radial derivative factor cannot be discarded.

Two ideal channels distinguish tensor/scalar strengths in this specified two-parameter model. Allow a third independent photon-response coefficient, however, and the response matrix has continuous null direction `(delta gt,delta gs,delta cg)=(1,-1,-1)`. Thus adding photons is still not a model-independent spin2 theorem or proof that every classical alternative is excluded. This respects the caveats of the prior gravity-entanglement audit, the [2026 matter-photon proposal](https://arxiv.org/abs/2604.24496), and [Di Biagio's discussion of gravity witnesses](https://doi.org/10.1103/r8ry-sp35).

For the deliberately microscopic source benchmark, the bending is only `7.4261602691e-38 rad`. No detector protocol, noise budget or feasible measurement is supplied. The first direct integration of this tiny signal failed an analytic relative check because its absolute tolerance was inappropriate. The corrected calculation integrates the dimensionless kernel before restoring units; the failed run is recorded, not counted as a successful check.

## 6. Extra bridge: holomorphy requires more than renaming Phi-dagger

Producer: `analysis/toe_20261103_mechanism_holomorphic_bridge.py`; matching JSON in `data/`.

The fourth mechanism is an ordinary nonsupersymmetric Weyl Lagrangian. Its Phi-dagger vertices cannot be inserted into a holomorphic SUSY W. Supply a **new independent chiral field** PhiMinus of charge-3, retain PhiPlus of charge+3, and introduce

`Wbreaking=lam Z(PhiPlus PhiMinus-v²)`.

At PhiPlus=PhiMinus=v real, Z=0, all three F equations and the gauge D equation vanish. The three-by-three holomorphic Hessian has one gauge tangent `(v,-v,0)` and two nonzero chiral masses `sqrt(2)|lam v|`; the broken vector multiplet has mass `6 g |v|` for vevs defined without a1/sqrt2. The residual Z9 persists. This supplies a real compatibility module, not a fictional conjugate chiral superfield.

The SUSY spectrum changes the beta coefficient again: with the stated supersymmetric SM, exotic steriles, messenger pairs and breaking pair, `bBL=13+57+14+18=102`, `bY=11`, mixed `bYBL=8`, above all thresholds. The previous nonsupersymmetric59 is not reusable. v, lam, soft terms and the coupling to gravity remain unspecified. This module alone has W=0 at its F-flat branch; it does not select a positive cosmological constant or repair dark-sector protection after SUSY breaking.

The three especially useful additional consistency tests beyond the five targets are the **goldstino cutoff**, the **Higgs/UV cost of the messenger chain**, and this **holomorphic/D-flat compatibility bridge**. None is silently assumed away to glue the models together.

## 7. Follow the repo connection: reference frames are sector-dependent

Producer: `analysis/toe_20261103_mechanism_sector_reference.py`; matching JSON in `data/`.

The deeper search found that Craig's paper was **already used** in12011–12038 and the October27 acoustic-density work. The latter already implements a finite comparison one-form, curvature/end-point identities and closed-loop Kato tests on5/27-dimensional SU5 multiplets. The new rank-one server cylinder is a small independent control, not an advance over that native calculation. We read `analysis/2026-10-27_acoustic_vacuum_density.md`, `analysis/PASS12026_12033_THETA_SOFT_HEAT_AND_DETERMINANT_TOPOLOGY.md`, `analysis/PASS12034_12038_JOINT_MECHANISM_TESTS.md`, the relevant CW source, and the full `analysis/w33_pass12002_native_path_overlap.py` heavy-frame producer. Those ownership connections are material.

A further concrete test follows from combining that machinery with the new physical flux index. On the actual3^4 matrices, the free positive spectral projector has rank162 and the flux projector rank163. Projecting a162-column free reference into the target cannot span it: its polar-normalized image necessarily misses at least one dimension and has projector operator-norm error1. This cannot be fixed by reducing the Kato step size.

For any continuous **gapped Hermitian** family on one fixed finite Hilbert space, the positive-projector rank is constant. Therefore these endpoints cannot be joined by such a family. An independent shift-matrix assembly of the Wilson kernel agrees with the site-block implementation. A28-step bisection of the affine Hermitian comparison path brackets a gap closure; intermediate affine matrices are not claimed to be Wilson operators of physical gauge fields. The exact rank argument is standard topology; the endpoints and deficient reference map are this regulator's explicit witnesses.

The12002 onsite-reference proof is for **heavy positive-mass optical blocks** and remains valid. It does not trivialize a different-index acoustic block. Likewise12030's nonzero toron Chern obstruction and12038's non-Abelian transition atlas remain prior results. A measure may be reconstructed separately on index components with appropriate reference data; this obstruction neither disproves that possibility nor refutes Craig/Lüscher. The required next calculation is sector-aware reconstruction and locality/global-integrability tests, rather than redoing already-implemented single-patch geometry.

## Reproduction and coverage

Run `py -3 analysis/toe_20261103_mechanisms_validation.py`. It regenerates seven producers in three concurrent local worker processes, then runs isolated pytest and a Node replay of the independent server controls. Source/input hashes are frozen during validation. Remote Desktop Commander launches the local job on TheHeavyCrown; it is the same Windows computer used by shell tools, not a second physical machine. Independent pure-JS numerical/flux calculations were performed in server V8 while local computation ran.

Validation, actual commands/stdout/failures, hashes and server checks are retained in `data/toe_20261103_mechanisms_validation.json`. The corrected earlier six-producer frozen-source run passed21tests in9.37seconds. The seventh producer adds three independent controls; its final validation receipt supplies the actual24-test outcome. The first expanded run had20passed/1failed because the exported symbolic spelling `lambda*v` is not parseable Python. The spelling is now `lam`; all artifacts were regenerated before the corrected run. The earlier failed receipt is retained. The later projector-cylinder check was executed independently on the server and replayed with Node; it is not added to the pytest count. Publication guard outcomes are recorded separately and are not conflated with physics tests.

The bounded corpus search inspected root analysis Python/Markdown, the results index, docs/index.html and local continuity records. It found the old paired overlap obstruction and the older `analysis/w33_pass11274_scale_and_sequestering.py` supertrace/global-sequestering audit; both were read and remain distinct from this local portal/nilpotent construction. This is not an exhaustive novelty search across every nested JSON/HTML/TeX file. No claim of priority for standard overlap, nilpotent supergravity, Dirac seesaw, or scalar-tensor formulas is made. The original whole-week-commit and entire-forty-points-PDF reading request is still not completely covered by this packet.

There is no tested common action that simultaneously gives controlled positive energy, radiatively stable rolling dark energy, the observed chiral SM, neutrino flavor and a verified gravity signal. The progress is constructive and falsifiable: the maps exist, and the failure controls identify where the next physical completion must do more.

## Five independent next investigations

1. Construct a linear goldstino/sgoldstino UV model whose scattering cutoff and full scalar spectrum remain controlled around the positive-energy vacuum.
2. Find a symmetry-based light dark sector with a calculable visible portal, including gravity/anomaly mediation and finite-density SUSY breaking.
3. Audit the October2026 refinement/measure construction and implement a four-dimensional Weyl measure with gauge Ward identities on the flux regulator.
4. Impose a justified flavor symmetry on the messenger matrices and test predictions against neutrino masses/mixing with threshold-matched RG running.
5. Calculate realistic matter-photon quantum observables and noise, retaining finite-range scalar and direct-photon degeneracies in model comparison.
