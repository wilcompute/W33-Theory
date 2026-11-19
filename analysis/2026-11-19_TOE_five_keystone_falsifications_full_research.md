# TOE keystone falsification pass: global chirality, physical flavor, SU5 thresholds, causal variance, photon erasure

**2026-11-19 | Five fronts executed with executable certificates and independent regression tests. Scientific scope:** All results below are conditional cohomological, 4D EFT, 5D boundary-projector, two-loop-gauge-only, stochastic-causal, or standard quantum-information constructions. **They are not a compact singular G2 metric, an anomaly-free full Standard Model, a full 5D KK/proton calculation, a Lorentzian quantum Einstein theory or a completed Theory of Everything.**

## Five-front pass/fail gate summary

| Front | Mathematical or numerical test completed | Physical blocker that remains |
|---|---|---|
| Global topology / 3 families | Exact genus-4 handlebody C7 twisted H1=48, H2=0; unique spinor character5 | 148 adjoint H1 candidates, no bulk triple cup, compensating up-type twist/defect, no actual compact G2 or chiral Lorentzian operator |
| Source Yukawas | Exhaustive 12 charge-neutral two-ten entries and independent normalized Gaussian contact calculation | Severe nonphysical CKM mixing, zero original bulk cup, unknown genuine local overlap and wavefunctions, S3 family degeneracy if metric unbroken |
| GUT / proton | Rank8 SM-invariant octet boundary projector, complete two-loop extra 5 beta coefficients and 9 gauge/Yukawa threshold sensitivity scenarios | Full supersymmetric 5D brane/KK spectrum, GS/R anomaly closure, proton matrix elements and observed unified mass spectrum |
| Causal gravity | Exact thinning = Rao-Blackwell variance theorem; sampled SD and analytic constant-field bias/MSE reduction | Continuum locality/bias for arbitrary fields, spin-two first-class constraints and physical quantum action/state |
| Photon engineering | Exact 5-qubit code erasure threshold50%, concatenation resource counts for 50–100000 logical qubits | Nondemolition heralds, logical gate implementation/fault-tolerance, real source/detector noise; no derived non-QM experimental deviation |

**Status:** all five *specified finite research diagnostics* executed. This does not mean the user-requested **full physical** TOE/GR/SM/optical architecture is solved; none is.

## Provenance, parallel commits and literature

Reviewed live master beginning from **2438b3e188151ffc0193a4e59e62c4ee33f0f2fa**, including parallel 25207be (Pascal/Lucas multicopy photon SSR and loss), 4bf689 (order-derived 2D causal torus with overlap index), 8f9ffe (causal torus, matter center, history and flavor), d1a311 (Spin10 and BDG4), 7518edfe (1D causal-incidence Dirac/orientation). Later parallel commits **f73c83e** and **1c9771e** landed during this run; both full diffs were reviewed. The latter proves block-upper-triangular causal vacuum determinant blindness and separate Wilson-sensitive spectral/endpoint probes. The former: it audits causal-diamond holonomy, one-way DAG determinants, Witten SU2 global anomaly, optical control, Hodge zero-mode bias and flavor stiffness. Those are independent of the present H4/W7 16-versus-adjoint local-system proof, source two-ten Gaussian sieve, SU5 octet projector and two-loop scan, BDG4 conditional variance-and-bias test and five-qubit erasure concatenation. The established November18 lens local-system obstruction is in analysis/2026-11-18_optimal_W33_3D_symmetry_E6_global_Wilson_modular_memory.md. The established November3 exact five-qubit code is analysis/2026_11_03_five_qubit_algebraic_locality.py. We specifically avoid presenting those as novel.

External theory and experiment checked:
* Complex flat lens local-system acyclicity and CW chain calculation: Novikov survey, https://www.sas.rochester.edu/mth/sites/doug-ravenel/otherpapers/novikovsurv.pdf ; the earlier in-repo punctured-lens LES is not independently rediscovered.
* Chiral matter on G2 singularities: Acharya–Witten, https://arxiv.org/abs/hep-th/0109152 ; anomaly inflow https://arxiv.org/abs/hep-th/0108165 .
* G2 Wilson-line doublet–triplet splitting: Witten, https://arxiv.org/abs/hep-ph/0201018 ; SO10 G2 and vectorlike matter https://arxiv.org/abs/1502.01727 .
* Two-loop N=1 SUSY gauge coefficients check: https://escholarship.org/content/qt2wr537b1/qt2wr537b1_noSplash_385928294d15b1ce1e7a9b9a839d87bc.pdf (full extra 5+bar5 B matrix agrees with our sum); canonical MSSM gauge matrix [[199/25,27/5,88/5],[9/5,25,24],[11/5,9,14]].
* Proton constraint, Super-K p→e+π0 partial lifetime >2.4×10^34 years (90% CL): https://doi.org/10.1103/PhysRevD.102.112011 ; **this 2-body dimension-six-type benchmark is not a direct bound on an arbitrary dimension-five colored-triplet decay channel**. A distinct October 26, 2026 two-pion channel yields >7.2×10^33 yr: https://doi.org/10.1103/frxr-pk3t .
* Benincasa–Dowker 4D scalar d'Alembertian: https://doi.org/10.1103/PhysRevLett.104.181301 , review https://doi.org/10.1007/s41114-019-0023-1 .
* **Known** exact binomial decimation/smearing identity and end-to-end example: https://github.com/stelios-tsilioukas/topology-change-in-causal-set-theory/blob/main/verification/bd_decimate.py and verification/bd_full.py. We read the actual code via GitHub connector; the binomial identity is prior art, not a new TOE mechanism.
* Quantum 5-qubit code https://arxiv.org/abs/quant-ph/9602019 ; bosonic quantum erasure and loss coding are conventional quantum information, NOT deviation from quantum mechanics.

## I. Global compactification/topology: exact mirror-free W7 representation and the three-way cohomological penalty

Consider the orientable **genus-four three-dimensional handlebody H4**, homotopy equivalent to a wedge of four circles. Its CW cochain complex has C0=C, C1=C^4, and Ck=0 for k≥2. The fundamental group F4 surjects onto C7 by mapping the first free generator to order seven and the other three to identity. Choose the previously reconstructed W7=diag(zeta² I3,zeta⁴ I2) in SU5⊂Spin10.

Under SU5 the spinor 16=1+Lambda²5+bar5, whose W7 phases are (multiset counts): 0 one, 1 one, 3 two, 4 three, 5 three, 6 six, **phase2 absent**. Therefore there is exactly one extra uniform line character k=5 mod7 for which *every* spinor component has monodromy zeta^(k+w)≠1. The exact cyclotomic polynomial zeta^6+...+zeta+1 has inverse for zeta^e−1 for e=1,...,6 (symbolically verified). For this spinor local system the 16-component differential C0→C1 has rank16, yielding

    dim H0=0, dim H1=4*16−16=48=3*16, dim H2=dim H3=0.

This is **three degree-one modes per Standard Model component and zero degree-two mirrors** in the mathematical flat-bundle model. A physical 4D compactified chiral index is NOT established: a true G2/ALE operator and source boundary/domain conditions must be constructed.

Its direct tradeoff is severe. The 45-dimensional Spin10 adjoint under W7 has 13 invariant generators (SM12 + extra chi1) and 32 nontrivial. On the same H4 cochain complex, each invariant generator contributes FOUR H1 modes; each nontrivial contributes THREE. Thus

    dim H0(adP)=13, dim H1(adP)=4*13+3*32=148.

Of these, at least 52 belong to the unbroken gauge sector before physical boundary/domain/flux lifting. The handlebody has H2(M,L)=0 for **every flat local system** because it deformation retracts onto a graph. Every absolute twofold and triple degree-one cup is zero: ordinary bulk topological Yukawas remain absent. An exact chiral index, no mirrors, no adjoint exotics and a nonzero bulk triple cup do **not** follow simultaneously from this topology.

Compare to the already-established punctured-L(7,1) all-nonzero mixed-sign defects: for net index3, r−s=3 with s≥1, twisted b1=r and b2=s, hence at least one mirror. Changing topology removes that mirror but generates a worse adjoint/cup problem. The conclusion is a **conditional source-model trilemma**, not a theorem excluding all G2 compactifications, singular defect amplitudes or flux-lifted gauge modes.

### Extra derivation: family-cycle symmetry and Wilson-character obstruction to an up-type Yukawa

The three residual free handles can be permuted by S3 without changing which first handle carries the W7 holonomy. If the microscopic metric/flux/action respects this symmetry, a symmetric three-family Yukawa must be

    Y = aI+b(J−I), eigenvalues a+2b, a−b, a−b.

Any two such matrices commute, and a double family degeneracy persists. No such observed degeneracy is explained by a purely topological three-dimensional H1; family discrimination requires *dynamical* metric/defect/symmetry-breaking data. This is a conditional exact automorphism argument, not a claim that every handlebody metric preserves S3.

Under the same **uniform constant flat-character** assumptions, a weak 5 component of a real SO10 10 requires intrinsic C7 character3, while the weak bar5 needs character4. Both family 16 fields require intrinsic character5 to avoid any invariant/mismatched family component. The intrinsic trilinear product characters are then:

    UP:   5 + 5 + 3 = 6 (mod7), requires extra character1
    DOWN: 5 + 5 + 4 = 0 (mod7), allowed by this character criterion.

A nontrivial character-one flat line has **no global covariantly constant section**, so a *constant* singlet spurion cannot fix the up-type coupling. A localized/twisted defect operator with compensating character might. The real physical G2 mass operator must be evaluated; no universal GUT no-go follows.

**The first missing particle ingredient is thus a globally defined twisted matter+Higgs complex with localized interactions and a mechanism that eliminates adjoint moduli, not another family-counting integer.**

## II. Source E8 Yukawas: exact allowed charge dressings vs a deliberately failed normalized wavefunction model

Import exactly the three 16_i source charges and two source 10 fields (10_34 and 10_24) plus the previously constructed eight nonzero singlet VEVs. Exhaustively search holomorphic monomials of singlets through degree six (minimum degree chosen for each required charge). Every one of the six independent family pairs i≤j admits a charge-neutral dressing through **each of the two source tens**: 12 separate allowed couplings. This is a semigroup/charge computation; it does **not** prove any corresponding compactification overlap is nonzero.

To construct an independent *local contact* benchmark, choose 1D individually normalized Gaussian profiles for three family modes centered at (-2,0,2) of width0.7; the two Higgs profiles at (-0.75,+0.75), width1. For generic means x_i and widths sigma_i the exact triple overlap is

    I_abc = pi^(-3/4)*(prod sigma)^(-1/2)*sqrt(2pi/S)
            *exp(-0.5*(Q-R²/S)),
    S=sum sigma_i^-2, R=sum x_i sigma_i^-2, Q=sum x_i² sigma_i^-2.

Multiply I by the source's existing spurion product / M^degree with M10 and unit coefficients, and by the previously calculated light 5/bar5 projections from the two-ten Higgs mass matrix. Both 3×3 Yukawa matrices have rank3. Their singular values, low to high, are

    Yu: (0.00559193, 0.02882225, 0.05280288)
    Yd: (0.02149833, 0.03782107, 0.10118789).

The mass-squared commutator has nonzero Frobenius norm ~1.8709e−6: two independent Higgs source tensors can generate nontrivial CKM misalignment, while retaining only **one** source tensor would make Yu and Yd proportional and force a commuting, trivial-mixing sector (assuming nondegenerate masses).

However, the illustrative |CKM| has entries near0.997 in incompatible off-diagonal positions, **dramatically unlike the observed near-diagonal CKM**. These deliberately chosen Gaussian centers/widths and generic unit coefficients are NOT physical G2 wavefunctions, not a fit, not an actual localized source overlap or M2-instanton amplitude, and not a prediction. The original punctured-S3 ordinary relative-bulk triple cup remains ZERO. The numerical failure is preserved as a falsifier, not retroactively tuned away.

## III. GUT: representation-selective octet mass and genuine two-loop gauge integration

For SU5 breaking adjoint H=diag(2,2,2,-3,-3), set Pc=(H+3I)/5 and Pw=(2I-H)/5. Define on an arbitrary traceless Hermitian adjoint field X

    P8(X)=Pc X Pc − tr(Pc X)*Pc/3,
    P3(X)=Pw X Pw − tr(Pw X)*Pw/2.

Explicit 24-dimensional basis projection gives ranks8 and3. P8 commutes with SM block SU3×SU2 conjugations; it does NOT transform covariantly under full SU5 color/weak mixing (an explicit nonzero norm witness is in JSON). The boundary mass term m8 tr(P8 Psi_2 P8 Psi_2) is thus *SM boundary-gauge invariant* and genuinely octet-selective if SU5 is broken on that boundary. This closes a representation-algebra problem that the earlier scalar Robin boundary toy did not. It does **not** derive its 5D supersymmetric Majorana action, bulk parity/brane conditions, an actual quantized h, or the complete KK spectrum.

For N=1 SUSY gauge two-loop coefficients, independently derive the contributions of a **vectorlike extra** electroweak doublet pair vs color triplet pair from group-theoretic Dynkin indices T and Casimirs C:

    Delta b_a = Sum T_a
    Delta B_ab = 2 C_a(G) Delta b_a delta_ab + 4 Sum T_a(R) C_b(R).

Exact additional doublet coefficients:

    Delta b_D=(3/5,1,0)
    Delta B_D=[[9/25,9/5,0],[3/5,7,0],[0,0,0]].

Exact additional triplet coefficients:

    Delta b_T=(2/5,0,1)
    Delta B_T=[[8/75,0,32/15],[0,0,0],[4/15,0,34/3]].

Their sum at one loop is the universal (1,1,1), but at two loops the matrix is not universal. Starting with illustrative MZ αEM−1=127.95, sin²θ=.23122, αS=.1181, one-loop SM running to 1TeV, and integrating two-loop N=1 **gauge-only** terms to a fixed 2e16GeV, five scenarios give (α1−1−α2−1):

    MSSM baseline:−0.2755;
    MSSM + extra triplet pair at 1e14GeV:−0.6189;
    MSSM + extra triplet pair at 1e16GeV:−0.3204;
    extra TeV doublet pair + triplet at 1e14GeV:+1.4412;
    extra TeV doublet pair + triplet at 1e16GeV:+1.7398.

The code also outputs α1−1−α3−1 and α2−1−α3−1 and all three inverse couplings. **No claim of actual unification**: one-loop SM→MSSM matching is simplistic, third-family Yukawa contributions omitted, soft/weak/GUT/KK thresholds unknown, and model has not chosen whether this pair is the MSSM Higgs or an extra pair. Do not double-count it.

If colored triplet-mediated dimension-five proton amplitude is ∝1/M_T with all dressing and Yukawas held fixed, reducing M_T by100 raises rate by10^4. Experiment constrains proton lifetimes, but absolute prediction cannot be supplied without physical Wilson mass/projected Yukawas, supersymmetric dressing and matrix elements. The Super-K p→eπ0 bound cited above is not an adequate substitute.

### III-b. Third-family Yukawa-dependent two-loop RGE, explicitly varying input assumptions

To avoid describing a gauge-only integration as a complete two-loop MSSM scan, implement the known MSSM gauge-Yukawa coefficient matrix with columns (top,bottom,tau),

    C_a^x = [[26/5,14/5,18/5],[6,6,2],[4,4,0]].

Integrate d alpha_a^-1/dlnmu = -b_a/(2pi) - [(B alpha)_a - (C y²)_a/(4pi)]/(8pi²), simultaneously with **one-loop** third-family Yukawa running for yt,yb,ytau. Compare three deliberately supplied 1TeV choices (0,0,0), (0.8,0.1,0.08), (0.8,0.5,0.4), under the baseline and with an additional color-triplet pair entering at 1e14 or 1e16GeV. The zero-Yukawa setting exactly reproduces the independently solved gauge-only cases, a genuine cross-implementation consistency check.

For the baseline at 2e16GeV, mismatch alpha1^-1−alpha2^-1 goes from -0.2755 (all zero) to -0.2850 (top-dominated) and -0.2903 (top+large bottom/tau). With a triplet at 1e14GeV, it changes from -0.6189 to -0.6284 to -0.6337. These Yukawa-induced changes (0.01–0.015) are smaller than the factor-of-30-or-more change induced by the extra light multiplet spectrum under this scan. That comparison prioritizes representations/thresholds above precision-fitting unknown Yukawas. It is NOT a global fit, no tan(beta)/SUSY low-energy matching is derived, and Yukawa beta functions are one-loop only. Source for standard coefficients: https://inspirehep.net/files/73fc41f9fd2eb27542b4b5807e72e758 .

Producer: analysis/toe_20261119_SU5_3rd_family_RGE_sensitivity.py ; certificate: data/toe_20261119_SU5_yukawa_two_loop_sensitivity.json ; regression: tests/test_toe_20261119_SU5_3rd_family_RGE_sensitivity.py .

## IV. Causal gravity: binomial thinning as exact variance reduction, with an explicit bias/nonlocality price

The previous four-layer (1,−9,16,−8) Benincasa–Dowker scalar operator passes continuum **mean** tests on selected flat fields, but raw finite Poisson sprinklings had massive fluctuations. Known Sorkin smearing corresponds **exactly** to independent Bernoulli thinning of sprinkled elements. For an origin with interval cardinality n, define

    W_eps(n) = sum_{j=0}^3 w_j C(n,j) eps^j (1−eps)^(n−j)
    B_(rho,eps)[1] = 4sqrt(rho eps)/sqrt6 *
                     (eps * sum_{future events y} W_eps(Nbetween(0,y)) − 1).

This is the conditional expectation, given a full PPP(rho) causet, of the **sharp BDG operator on a Bernoulli-thinned PPP(rho eps)**. Therefore the law of total variance proves *exactly*

    Var(B_smoothed at parent rho) ≤ Var(B_sharp at effective rho eps).

For each parent rho=100,200, 300 independently sprinkled 4D Minkowski future cones 0<t<1 and independent sharp comparison cones at the same **effective** density were evaluated. The finite-sample variance ratios smooth/sharp were:

    parent100 eps.5:0.0554, eps.2:0.0263
    parent200 eps.5:0.0451, eps.2:0.0104.

At eps1 the two independent empirical variance estimates need not match exactly. These are a new-to-this-repo **quantitative bounded-variance comparison**, but the smoothing/decimation mathematics is prior art. The lower effective density introduces higher nonlocality and possible continuum bias; observing lower single-sprinkling variance does NOT establish a stable scalar continuum propagator or physical gravitational action, positive state, spin-two constraint closure, Einstein field equations or experimental departure from GR.

### IV-b. Exact finite-volume bias, not just variance

A separate executable computes the expected finite-ρ *constant-field* response by direct radial/temporal continuum quadrature on the same four-dimensional future cone. It evaluates the known BDG polynomial 1−9z+8z²−(4/3)z³ against the actual causal-interval volume V=π(t²−r²)²/24. The analytic continuum target is Box(1)=0, but finite-ρ/finite-cone expectation has a nonzero bias. Every Monte Carlo sample mean above lies within three standard errors of its independent continuum quadrature (maximum tested discrepancy ~2.31 SE), confirming the sampling/normalization on this probe.

For fixed parent rho100, the sharp eps1 estimator has SD≈1180.9 and analytic bias≈−1.1398; at eps.2 the conditional-smoothed estimator has SD≈25.65 and bias≈+1.2616. The estimated MSE=sample variance+(exact finite-volume bias)^2 declines from ~1,394,536 to ~659.3, **ratio 0.000473**. At parent rho200 the analogous MSE ratio is **0.000413** (eps.2 vs eps1). These are sample-variance MSE estimates for ONE constant field at ONE origin and THREE tested eps choices, not a universal proof of minimal continuum bias or Einstein dynamics. At smaller eps the corresponding effective density is much lower and nonlocality larger; full physical locality, arbitrary-field and quantum-state constraints remain.

Producer: analysis/toe_20261119_BDG4_bias_variance_gate.py ; independent exact-integral certificate: data/toe_20261119_BDG4_bias_variance_continuum_gate.json ; tests: tests/test_toe_20261119_BDG4_bias_variance_gate.py .

## V. Quantum photonics: exact [[5,1,3]] erasure-correction resource requirements

The existing repository's five-qubit perfect code has four commuting stabilizers and an explicit 32×32 Knill–Laflamme calculation. Reuse it as verified prior code, and independently enumerate **all ten size-three erased subsets**: each can support logical X and Z, so erasing ≥3 of 5 loses the encoded qubit, while erasing ≤2 is correctable when erasure positions are known.

For independent physical erasure probability p, the exact concatenated logical map is

    F(p)=Pr[3,4,5 erasures]=10p³−15p⁴+6p⁵.

Factor F(p)−p = p(p−1)(2p−1)(3p²−3p−1). The nontrivial threshold on [0,1] is p=.5, in line with the quantum erasure channel's positive unassisted-capacity range. At photon survival eta=.9:

    p0=.1; p1=.00856; p2≈6.1919606e−6; p3≈2.3739989e−15.

Two levels therefore encode 50 independent logical qubits in 1250 physical photon-qubits with union-bound total erasure failure ≤0.0003096; three levels encode 1000 logical qubits in 125000 photons with bound ≤2.374e−12. At eta=.75, 1000 logical qubits with target <1e−6 need FOUR concatenation levels (625000 physical photon-qubits) under this ideal calculation. At eta=.49, concatenation moves errors toward failure rather than removing them: threshold fails.

These costs assume perfect source, syndrome measurement, erasure-location flags, encoding/decoding and logical gates, and ignore loss during gate implementation. **The calculation does not produce fault-tolerant optical hardware or a nonstandard quantum prediction.** An uncorrected chain of heralded 75%-success two-photon gates still fails exponentially until active feedforward and fault-tolerant logical gate construction are supplied. An n-qubit register requires many photons here, not the original one-photon architecture. The recent parallel Pascal/Lucas photon SSR Bell analysis is an independent, standard-quantum operational resource and does not supply beyond-standard-QM effects.

## Combined dependency result: find the missing OBJECT, not another number

The particle-side "first thing" is **one actual global twisted family/Higgs Dirac complex with nonzero localized trilinear maps, controlled adjoint spectrum and anomaly inflow**. Counting index=3, selecting W7, constructing a 4D messenger tree and writing an SM-octet boundary projector are individually tractable but *incompatible until one compact source supports all of them*. In particular, the explicit mirror-free handlebody brings 148 adjoints, an S3 family degeneracy, a zero bulk cup and a uniform-character up-Higgs selection obstruction; a real dynamic defect construction must address all four at once.

The gravity-side "first thing" is **a physically selected quantum action/measure** that controls finite causal-set fluctuations *and* recovers a positive causal scalar/tensor propagator with first-class gravitational constraints. Rao–Blackwell smoothing is a known estimator technique, not quantum gravity.

The quantum-computation "first thing" is an **implementable, error-corrected photonic gate architecture** with demonstrably polynomial physical resources; only after that can a genuinely different physical prediction, if the TOE yields one, be registered as a falsifiable experiment.

### Reproducibility and pass/fail bars

    python analysis/toe_20261119_handlebody_W7_topological_trilemma.py
    python analysis/toe_20261119_source_two_ten_localized_flavor_sieve.py
    python analysis/toe_20261119_SU5_brane_projector_two_loop_RGE.py
    python analysis/toe_20261119_BDG4_Rao_Blackwell_smearing.py
    python analysis/toe_20261119_five_qubit_photon_erasure_concatenation.py
    python analysis/toe_20261119_SU5_3rd_family_RGE_sensitivity.py
    python analysis/toe_20261119_BDG4_bias_variance_gate.py
    python analysis/toe_20261119_full_physics_regression_runner.py
    python -m unittest discover -s tests -p test_toe_20261119_five_physics_keystone_crosslinks.py -v

Seven research machine-readable JSON certificates in data/ use corresponding 20261119 filenames; the broad daily physics regression runner emits an eighth manifest. Every declared result is regression-tested; nearby prior Higgs/Green–Schwarz/causal/photon suites are rerun. **Full repository CI and a genuine G2/quantum-gravity field solver are not claimed.**

## Five top independent next physics experiments

1. **Build the global singular G2 family/Higgs complex:** find a compact associative gauge locus, order-seven holonomy, boundary/flux lifting of 148 candidate adjoint H1 modes, localized 16+bar16 Higgs sources, truly three chiral matter families and actual nonzero compactification interaction maps. Reject if any one constraint fails.
2. **Derive an actual flavor/defect action:** require an S3-breaking geometric term that distinguishes the handle cycles, a character-one localized insertion to rescue the up-type interaction, and a full-rank Yukawa pair reproducing hierarchical masses plus near-diagonal CKM/PMNS *without choosing Gaussian centers to match the answer*.
3. **Construct the full anomaly-free supersymmetric GUT:** quantized discrete/Abelian GS couplings and R anomaly cancellation, true octet-selective boundary fermion action, full KK+two-loop Yukawa/gauge RGE and dimension-five/dimension-six proton-decay amplitudes from the same mass spectrum.
4. **Derive 3+1 causal quantum Einstein gravity:** establish a quantum measure and physical state, then compare smearing-bias vs variance for generic smooth fields and geometry changes, recover gauge-invariant massless spin-two propagator, local Dirac operator and the entire first-class Einstein constraint algebra.
5. **Compile the photonic fault-tolerant resource:** implement syndrome extraction, nondemolition loss flags and an actual logical entangler with calibrated source/detector efficiency, simulate scaling and then derive a preregistered non-QM prediction from the TOE (if the model possesses one).

**Conclusive status:** all five finite-model workstreams executed. They sharpen the foundational obstacles; none resolves the full physical problems or proves a TOE.
