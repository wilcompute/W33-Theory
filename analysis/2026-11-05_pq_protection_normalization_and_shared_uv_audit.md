# PQ-assisted unification: protection, numerical stability, and a shared gravity cutoff

November 5, 2026. These are necessary consistency controls of the actual repo candidate, not a solved Theory of Everything or an experimental exclusion.

The strongest result is a restricted model-building obstruction: the existing D+Q+Q candidate with mass signs (+,+,-), one Higgs and full-rank renormalizable SM Yukawas cannot protect its PQ scalar with an ordinary anomaly-free discrete or continuous gauge symmetry under the hypotheses below. The numerical follow-up also finds that positivity of a truncated RG solution was being mistaken for stability through the unification scale. Both problems need resolution before treating the separate unification, axion and scalar modules as one physical theory.

## What changed, what was actually read

The initial comparison is master59151dee68a85202d3770f7c92c30498f3de7d08 to6fdfcfefb0dcb5e9f78668b3e2a02d23b7849a68:60commits,550changed paths. I read the full text of all45 analysis reports in that snapshot, totaling516,007characters, in bounded batches; truncated outputs were reread. The path/commit inventory and report hashes are frozen in data/toe_20261105_change_reading_coverage.json. Four later commits through61fbe91c678c2d9b599de329c2bcec12eec473d3 added12609-12612; their combined report and pq_mass_ceiling.py were read too.

This does NOT mean every550file or every full commit patch has been semantically reviewed. The215-page papers/forty_points/main.pdf has585,966extracted characters; this continuation reread pages1-5 and visually inspected its cover, while earlier targeted readings remain separate. Full-PDF coverage is still incomplete. Neither a file hash nor a search hit is a claim of reading.

The new bounded result search covers23,404files across analysis, papers, docs, tests and scripts with py/json/md/tex/html/js/g/sage/txt extensions. It records123matching paths in data/toe_20261105_pq_result_search.json. These regexes are imperfect and can miss alternate notation; there is no corpus-wide priority claim. The useful matches were followed back to actual sources and certificates.

Key incoming corrections worth retaining:

-12609-12612 soften the old25-60micro-eV ceiling; the instability scale and top-mass interpretation matter, and GUT thresholds soften the one-of85 ranking. Their latest120micro-eV central ceiling still imports the same approximate scalar/Yukawa script audited here.
-The Nov4 graph25 A5 bridge lands mostly in the physically dark Witting operator kernel. A reciprocal class1 embedding gives eight real mixed-state parameters, not eight orthogonal quantum states. Later decoder work distinguishes one-copy information from repeated-label identifiability.
-The Nov5 independent4D overlap work checks U1 flux branches and an SU2 Cartan embedding. A genuine finite index is established, while an integrable interacting Weyl measure and a dynamically selected regulator/vacuum are not supplied. It overlaps our previously uncommitted4D mechanism study, rather than making the general index mechanism new.
-The nine-simplex Lorentzian principal-branch action has a nonzero flat gradient. Flat Euclidean Hessian nulls do not repair that Lorentzian failure or establish nonlinear ADM closure.

## 1. Canonical axion quality: sufficient protection dimensions

Producer: analysis/toe_20261105_pq_quality_gauge_obstruction.py. Certificate: data/toe_20261105_pq_quality_gauge_obstruction.json.

Use the declared canonical field Sigma=(fa+rho)/sqrt(2)*exp(i theta), domain-wall number1, chi=(0.0756GeV)^4, reduced Planck scale2.435e18GeV, and a supplied coefficient magnitude|c|=1:

    DeltaV = -[c Sigma^d/Mpl^(d-4) + h.c.]
    V/chi = 1-cos(theta)-r cos(d theta+delta)
    r = 2(fa/sqrt2)^d/[Mpl^(d-4) chi].

Comparison with theta0 bounds every global minimum by1-cos(theta)<=2r. On that neighborhood the curvature is at least1-(d²+2)r. If positive,

    |theta_min| <= d*r/[1-(d²+2)r]

uniformly in the unknown phase. This is a sufficient bound, not a claim that every phase fails below it. Large-r rows get no spurious perturbative small-angle answer. Independent global minimization checks and75-digit stationary roots verify the small-r cases.

For theta tolerance1e-10, the first sufficient leading operator dimension is12 at fa=9.5e10 or1e11GeV, and13 at fa=2e11 or2.28e11GeV. Thus protection must forbid lower operators; the table does not itself produce a protecting symmetry. Both canonical and bare-vev conventions are exported explicitly.

This scale of the quality requirement is established physics, also independently consistent with the June2026 primary study [Quality control for axions and ALPs](https://arxiv.org/abs/2606.14098). The older repo Pass11949 already rejects a DIFFERENT modular axiflavon due to an explicit Yukawa harmonic and its top-loop potential; its report and actual dirty certificate were read and preserved. The present Planck-operator check does not relabel that earlier obstruction.

## 2. Ordinary gauge protection fails for the unchanged inventory

The actual12603 candidate contains Dirac D=(3,1,-1/3),Q1,Q2=(3,2,1/6). Sigma,Sigma,Sigma-dagger mass terms give integer SU3 anomaly1+2-2=1 and E/N=2/3. These are prior results from analysis/toe_uv/pq_full_scan.json, not new predictions.

For an exact non-R Z_N with no Green-Schwarz cancellation or higher-dimensional anomaly inflow, full-rank SM quark Yukawa determinants with one Higgs imply that the light quark SU3-instanton charge vanishes moduloN. The heavy mass equations then give

    A3_integer = -(1+2-2)qSigma = -qSigma mod N.

An ordinary invariant instanton measure therefore requires qSigma=0modN. No pure Sigma power is forbidden. This proves the conditional statement for everyN; finite scans2..64 and independent server checks through257 are only arithmetic controls. Additional anomaly-cancelling sectors, nonstandard SM mass generation or inflow change the theorem's hypotheses.

For a continuous ordinary U1, let d,a,b denote the LH pair-charge sums of D,Q1,Q2, and z the full SM SU2²U1 anomaly. Single-Higgs renormalizable SM Yukawas imply SM_SU3=0 and SM_Y²=-SM_SU2. The necessary mixed-anomaly matrix is

    [1/2   1    1     0 ]
    [ 0   3/2  3/2    1 ]
    [1/3  1/6  1/6   -1 ].

Its exact kernel is(0,-t,t,0). In particular D cannot carry an axial pair charge. A renormalizable Sigma D Dbar mass therefore requires a neutral Sigma. Adding only SM-singlet sterile fermions cannot fix these mixed anomalies. This is a necessary-equation obstruction, not a complete anomaly classification.

A tempting two-scalar color cancellation uses qS2,qT3 and pair charges(-2,-2,3): SU3²U1 vanishes, but SU2²U1=3/2 and Y²U1=-1/2 do not. It also permits the low dimension5 scalar interlock S³(Tdag)². Color cancellation alone is not a protected axion model.

There are explicit escapes in primary literature. [Babu-Gogoladze-Wang](https://arxiv.org/abs/hep-ph/0212339) use discrete Green-Schwarz cancellation, outside the ordinary-no-inflow assumptions. [Babu-Dutta-Mohapatra](https://arxiv.org/abs/2412.21157) give anomaly-free gauged-U1 high-quality domain-wall-one models with different matter/scalar/mass ingredients. Their existence forbids any interpretation of this computation as a universal axion no-go. The repair task is to add and test the actual missing sector, including its beta functions and mass operators.

## 3. Normalization and numerical completion change the stability question

Producer: analysis/toe_20261105_pq_normalization_cutoff.py. Certificate: data/toe_20261105_pq_normalization_cutoff.json.

The parent's pq_gates.py docstring specifies Sigma=f/sqrt2 and mass ySigma, but initializes y=MQ/f. The canonical relation is MQ=yf/sqrt2, hence y=sqrt2*MQ/f. Hold physical MQ=27279937181.61975GeV and MU=3964835648946381GeV fixed. Retain the parent's approximate beta system to isolate the convention effect:

    16pi² lambda' = 20lambda²+60lambda*y²-30y^4
    16pi² y' = y(18y²-8g3²).

At f1e11GeV, the noncanonical run needs lambda approximately0.00776063 and radial mass1.24584e10GeV; the canonical run needs0.03156717 and2.51265e10GeV. At f2e11GeV these become0.000458092 versus0.00184188, and6.05370e9 versus1.21388e10GeV. This roughly factor-four quartic/factor-two mass change is a comparison within these equations, not a full precision stability prediction.

The old bisection checked only the minimum of returned lambda samples. It did not require solver success or arrival at MU. Our explicit counter-control starts f2.7e10GeV,lambda2: the returned quartic stays positive but reaches the declared perturbativity cutoff near1.70e11GeV, far belowMU. It is not a successful UV-stable trajectory. Large Yukawa rows fail independently of the quartic choice.

An exact independent check sets z=1/y². Its linear differential equation has a closed solution using the affine inverse alpha3. This agrees with numerical integration and separately locates the necessary Yukawa perturbativity boundary. Server-side V8 scalar RK4 with20,000steps gives y(MU)=0.37672164174086725 at canonical f1e11GeV, agreeing with the PC solver. These are independent execution paths on the supplied equations.

Limitations are material: the coefficients are inherited approximate beta functions, equal Yukawas are a boundary input, EW splitting and full portals/sterile/Higgs evolution are absent, and rows with f<MQ lack correct decoupling. A declared lambda<4pi,y²<4pi criterion is a diagnostic, not a theorem of perturbative control. Consequently the120micro-eV central ceiling and500micro-eV exclusion in12612 are not automatically inherited. A full matching/RG treatment must precede a defensible physical ceiling. The [scalar threshold mechanism](https://arxiv.org/abs/1203.0237) itself is established; this audit does not reject it.

## 4. Micron dimension plus high-scale unification needs a UV bridge

With an ordinary flat5D Einstein term,

    M4_reduced² = M5³ L.

For supplied R8-15micron and L=piR or2piR, the characteristic5D gravity scale is2.32e8-3.60e8GeV. The candidate MQ lies76-118times above it, and MU approximately11-17million times above it. The repo's earlier analysis/toe_uv/hw_wall_radius.py and its certificate ALREADY own M5=265054293.94261003GeV at R10micron,L2piR; the present calculation reproduces that value and tests compatibility with the later PQ benchmark. Neither the Planck relation nor this scale is newly discovered.

If both proposals inhabit the same conventional5D gravity EFT, a4D gauge fit above that scale is not by itself a controlled common UV theory. This does not forbid a brane gauge sector or a UV completion. [Heckman-Vafa-Weigand-Xu](https://arxiv.org/abs/2409.01405) explicitly discuss GUT vectors represented by stretched solitonic strings above the5D scale; their framework introduces additional structure rather than making an ordinary point-particle EFT automatically valid. We have not built that completion.

Reading the proposed stretched-string repair further gives a stronger, conditional compatibility diagnostic. Write MV=T*LX, T<=cT*M5², LX<=Lg and Lg<=1/KKmin. Then cT>=MV*KKmin/M5². If MV is identified with the fitted MU and the gauge KK lower bound is supplied as1TeV, our8-15micron radii require cT approximately31-74; at10TeV they require306-740. With unit tension factor, compatible radii would need to be below about0.05micron, depending on convention and KK input. The certificate exports exact values and factors1,10,100,1000. These are order-of-magnitude inequalities from the published proposal: unknown black-string normalization factors, a different vector mass or another UV construction can change the conclusion. It is not a model-independent exclusion. It does show that naming a stretched string alone does not complete this benchmark's UV repair.

A July2026 [Wilson-line axion model](https://arxiv.org/abs/2607.08814) supplies another escape from local scalar PQ breaking. Its interval relation f=1/(g5sqrtL) gives the coupling parameter g4=g5/sqrtL=1/(fL). If that interval is identified with the micron dimension, f1e11GeV requires g4 approximately2.1e-23-7.9e-23. This is an extra hierarchy input. The construction has no PQ radial scalar and its anomaly-sector masses need not equal yf/sqrt2, so it changes the scalar-stability and mass assumptions rather than preserving the old model unchanged. The printed g4 is a normalization parameter, not a surviving4D gauge zero mode.

## Validation and the earlier seven-mechanism packet

New producers both regenerate successfully. The initial seven new tests plus24 earlier mechanism tests passed together:31PASS. A further stretched-string/radius-scaling test extends the final suite to32tests; its actual run status is recorded in data/toe_20261105_pq_uv_validation.json alongside source/input/output hashes. The JS source and actual server V8 receipt are analysis/toe_20261105_pq_server_controls.js and data/toe_20261105_pq_server_controls.json. The tests check exact mixed-anomaly elimination, canonical suppression factors, phase bounds against global minimization, the independent Yukawa equation, incomplete-flow rejection, dimensional reduction and the UV-repair inequalities.

The earlier seven producers and their24tests were already validated and source-frozen: portal soft leakage, stationary nilpotent uplift, actual4D overlap flux, renormalizable neutrino messengers, calibrated gravity identifiability, a holomorphic breaking module and the topological-sector projector-rank obstruction. Their report is analysis/2026-11-03_toe_mechanism_completion.md. They remain separate conditional models; publication together does not create a common microscopic action. Established overlap topology, nilpotent SUGRA, anomaly methods and scalar thresholds retain their cited prior owners.

Remote Desktop Commander ran the local producer/replay work while server V8 and web research supplied independent checks. It accesses the same PC as local shell tools; it is not an additional physical machine. No laboratory experiment, unique new fundamental constant or completed TOE is claimed.

## Five independent next investigations

1. Construct a concrete anomaly-free protection sector for D+Q+Q, then rerun gauge unification with every added threshold.
2. Derive and integrate the complete nondegenerate Yukawa/portal/Higgs RG system with canonical matching and successful UV completion checks.
3. Build an explicit shared gravity completion, comparing localized brane and stretched-string options rather than extrapolating the4D EFT.
4. Test a globally integrable chiral Weyl measure across the actual finite flux sectors and all required admissibility conditions.
5. Obtain a causal Lorentzian Regge action with correct boost branches and boundary terms, before inferring gravity from flat Hessian nulls.
