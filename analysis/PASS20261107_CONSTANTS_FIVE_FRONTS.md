# November 7, 2026 — Five constants fronts: executable audit and obstruction certificates

**Repository:** wilcompute/W33-Theory, master. **Owner of this packet:** \`analysis/w33_20261107_constants_five_fronts.py\`; tests: \`tests/test_w33_20261107_constants_five_fronts.py\`. Certificate producer: \`python analysis/w33_20261107_constants_five_fronts.py --root . --output data/w33_20261107_constants_five_fronts.json\`. The repository's existing \`analysis/w33_pass398_formula_search_universe.py\` and \`analysis/w33_frozen_formula_null_audit.py\` remain the more extensive frozen-family scanners; our scanner is a targeted provenance/conflict **cross-check**, not a replacement.

## Intake and novelty audit
Inspected current \`docs/index.html\` public evidence firewall, \`W36_PAPER.tex\`, \`papers/standalone/toe_constants_companion.tex\`, \`papers/standalone/toe_master_synthesis.tex\`, \`data/w33_prediction_registry_v1.json\`, \`analysis/w33_20261010_toe36_qed_running_alpha_gate.py\`, \`analysis/w33_20261019_round6_scale_nogo.py\`, \`analysis/PASS20261001_DFLAT_CARTAN_MASS_LOOP.md\`, \`analysis/PASS11602_11606_GEOMETRY_FLAVOR_COMPLETION.md\`, \`analysis/PASS11608_11613_CHIRAL_UNIFICATION.md\`, and \`analysis/w33_pass398_formula_search_universe.py\`. Relevant filenames/claims were searched by formula and result, rather than claiming novelty from a newly named file. No new physical constant is claimed.

## Front 1 — Electromagnetic coupling as a running observable
**Exact frozen outside physics input:** in the on-shell scheme with one electron of independently supplied mass, for spacelike momentum x=Q/m_e:
\[
\alpha^{-1}(Q^2)=\alpha^{-1}(0)-{2\over\pi}\int_0^1 dz\,z(1-z)\log(1+x^2z(1-z)).
\]
The signs and positive-momentum monotonicity are checked by Simpson quadrature at **predeclared** x∈{0,1,10,100}; source script returns the inverse-alpha shift. It is QED physics, **not** a beta function extracted from W33 incidence. Running the W33 boundary and the independent CODATA boundary through the same functional leaves their difference constant at each x. A continuous W33 gauge normalization / vertex action needed to select alpha(0) and radiative thresholds is absent. Hence **no prospective alpha(Q) prediction** was possible, and none is claimed.

New source-aware CODATA comparison (latest NIST recommendation available, 2022 adjustment, inverse alpha 137.035999177(21)):
- \`137+1/28+4/14045=137.035999084575...\` → **−4.4012 σ**.
- \`137+880/24445=137.035999181837...\` → **+0.2303 σ**.
- \`137+40/1111=137.036003600360...\` → **+210.636 σ**.
- Graph integer skeleton \`137\` → approximately −1.714 million σ.
The better 2022 match from a different existing expression is a **selection effect** and not allowed as prospective validation. Do not silently promote this value in the catalog because it was chosen using measured data.

**Source for experimental value:** https://physics.nist.gov/cuu/Reference/versioncon.shtml and 2022 CODATA RMP 97, 025002 (2025). **Prior repo work:** October 10 TOE36 source cited above.

## Front 2 — Shared CKM/PMNS 3×3 source operator and exact falsifier
Take the qutrit cyclic shift X, X³=I, and its Hermitian real adjacency K=X+X†. Define P=(1/3)11^T. Then K=3P-I and the **single common** alignment is exactly
\[
U(t)=\exp(itK)=e^{2it}P+e^{-it}(I-P),
\quad t=q/\Phi_3=3/13 .
\]
Specify actual Hermitian mass-squared operators:
\[
H_u=D_u,\ H_d=UD_dU^\dagger,\ H_e=D_e,\ H_\nu=UD_\nu U^\dagger,
\]
where the explicit diagonal **fixtures** \`D_u=(1,3,9), D_d=(2,4,8), D_e=(1,4,16), D_nu=(1,2,3)\` are dimensionless, supplied and **not predicted physical masses**. Algebraic diagonalization yields **CKM=PMNS=U**, regardless of those four spectra. Unitarity and Hermiticity are explicitly checked. CP is not accidentally forced to vanish: \`Im(U00 U11 U01* U10*)≈0.010886\` at t=3/13.

The exact common-spurion mixing identity
\[
\sin^2\theta_{12}^{PMNS}={|V_{us}|^2\over1-|V_{us}|^2}
\]
is incompatible with observation: the construction gives \`|V_us|≈0.22619\` (near the CKM value) but \`sin²theta12≈0.05392\` versus the observed solar value around 0.30–0.31. **It fails**, and therefore rules out this particular single-identical-alignment mechanism, not all W33 flavor theories.

To get independent CKM and PMNS matrices, one must introduce **at least one extra physically justified independent left-handed rotation or operator**. Their relative phase, mass eigenvalues, seesaw couplings and sector Clebsches then need a dynamical action, not numerical matching. This is a constructive **conditional no-go** and does not supersede the advanced 81-component D-flat/E6 mass operators already in repo.

## Front 3 — Prove the absolute-scale obstruction and the additional gauge normalization freedom
For finite H with eigenvalues (0,2,4) and independently specified T,t, the transformations \`H->sH, T->sT, t->t/s\` preserve both normalized Gibbs populations and \`exp(-iHt)\`. The source evaluates s∈{0.1,0.5,1,3,10} with numerical residuals near machine epsilon, extending the earlier, more sophisticated October 19 proof by a minimal stdlib-independent regression.

A *separate continuous ambiguity* appears even for dimensionless electromagnetism: on a fixed incidence graph, append a Maxwell-like continuum term \`S_g=(4g²)^-1∫F²\`. With no canonical gauge normalization/matter charge assignment, \`g=1\` and \`g=2\` are equally compatible with W33 incidence, but correspond to action coefficients 1/4 and 1/16 and different couplings. **Incidence alone does not select alpha**. This is a model-family identifiability proof, not a claim that all UV-complete theories leave g arbitrary.

**Needed next object:** a normalized, gauge- and Lorentz-consistent action with internal units, kinetic normalization, selected matter charges and a renormalization scheme. Until then, c, G, hbar, Planck mass, EW masses, Hubble and Lambda cannot be independently extracted from dimensionless W33 combinatorics. Existing curved spectral and matched-Dirac actions still supply metric, clock, or cutoff externally.

## Front 4 — Machine-readable source/variant provenance
The new producer has a **full-checkout** scanner over \`.tex, .py, .md, .html, .json, .lean, .g, .sage\` (including \`analysis\`, \`papers\`, \`docs\`, \`data\`, \`archive\`); file/line references for the first twelve hits per category, deterministic normalized-line SHA-256 IDs, family totals, skipped oversized files, and bounded-memory summary output. The default walks the whole repository when a checkout is present, omitting only git/build/virtual environments. It is explicitly **syntactic**: equivalent formulas often occupy different line signatures and syntactically similar formulas may have different semantics. The CI producer must run against a complete checkout; a GitHub API code-search response alone cannot prove exhaustive coverage.

Use \`python analysis/w33_20261107_constants_five_fronts.py --root .\` to generate \`data/w33_20261107_constants_five_fronts.json\`; the focused tests run a three-file fixture as an independent scanner sanity test. Before claiming semantic conflicts, match schemes, scales, species definitions and source histories. The original Pass398 frozen search universe must still count against any prospective discovery.

## Front 5 — Selection effects and competing rational null
At MS-bar weak-angle reference value 0.23122, the W33 postselected \`3/13+1/2200≈0.231223776\` differs by 0.000003776 (roughly 0.126σ if illustrative σ=0.00003).

As a reproducible **adversarial competitor**, enumerate all reduced \`a/b\` with b≤20,100,500,1000 and numerators within ±1 of round(reference*b), using standard gcd. This is a predeclared algorithm with no W33 primitives. At b≤1000 it finds \`197/852=0.2312206573\`, closer (≈0.022σ), showing a tight post hoc rational match is not uniquely identifying.

The producer also returns a sensitivity table for a **hypothetical** family of M independent numbers uniform on [0,1] and a target interval ±δ:
\[
\Pr(\mathrm{at\ least\ one\ match}\mid M,\delta)=1-(1-2\delta)^M .
\]
This is **not** the statistical law of W33-derived formulas. Real formula families are correlated, adaptively searched, heterogeneous and typically data-informed. The exercise does not yield a publishable p-value or evidence of a physical correspondence. Genuine analysis requires the exact frozen Pass398 candidate universe, prospective target release, measurement covariance and an explicitly justified null generator; no such prospective release has occurred during this pass.

## Executed claim and limitations
- The tests certify exact matrix identities, the scalar rescaling proof, a fixed one-loop QED **conditional** calculation, a reproducible rational search and scanner fixtures.
- Existing repo results get full attribution: QED work October 10, absolute-scale theorem October 19, advanced D-flat flavor work October 1, Pass398 formula freeze, and Pass391 prospective registry.
- We did **not** discover a novel constant, fully predictive flavor action, independent alpha(Q), a unique absolute physical scale, or a statistical detection of a W33 law.
- A numerical fit evaluated against data already used to choose the formula is never called a prospective test.

## Commands
\`\`\`bash
python -m pytest -q tests/test_w33_20261107_constants_five_fronts.py
python analysis/w33_20261107_constants_five_fronts.py --no-scan
python analysis/w33_20261107_constants_five_fronts.py --root .
\`\`\`

## Five most valuable independent continuations
1. Construct a gauge-normalized alpha action with physical charges and fixed loops; make **one** frozen \`alpha(Q)\` prediction for a future independent precision release.
2. Couple the actual D-flat E6 mass pencil to one complete chiral family action, and derive all four fermion-sector left rotations together with controlled thresholds; compare against the **entire** mixing covariance.
3. Prove a UV/IR dynamical scale-breaking mechanism with experimentally defined units, then evaluate c/G/hbar and Lambda without inserting the measured target.
4. Use the Pass398 frozen universe to generate an algebraically canonicalized provenance graph; audit equivalence classes and withdrawn candidates, not merely line-shape hashes.
5. Register a calibrated null family and untouched holdout data **before** exploring any new rational corrections, then report the joint likelihood and familywise selection penalty.
