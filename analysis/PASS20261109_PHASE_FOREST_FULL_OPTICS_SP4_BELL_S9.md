# W33 / TOE: five additional fronts executed and independently tested

**November 9, 2026.** Reproducible research on GitHub master and the authorized Windows worktree. Five new Python programs, five frozen JSON outputs, and sixteen regression tests. This packet contains exact finite mathematics, synthetic detector/optics studies, and a read-only public DES data audit. **No physical photon device, Standard Model particle dynamics, or observed cosmological likelihood has been verified.**

## Front 1 — A 242-configuration phase-forest calibration; the conservative bound gets worse

Previous complete full-POVM tomography used 81 trusted calibration probes for each of 10 nine-mode analyzers, 810 probe/context configurations total. We studied a restricted physical model K_actual=K_cal diag(exp(i theta_j)), allowing **only input-mode diagonal phase drift** on a precisely known, possibly lossy 9x9 K_cal. Number-basis and pair-superposition probes give input-phase differences only when two modes interfere at some detector.

The original fixed-mode-zero reference **failed** for two W33 Bell analyzers whose support graph has three disconnected components. These components' relative phases are unobservable, but cancel from every true POVM effect. We instead use a weighted maximum-interference spanning **forest**, with one arbitrary reference phase per observable component. On the ten analyzers, support-component counts are [1,1,3,1,1,3,1,1,1,1]. The required trusted probes are [25,25,21,25,25,21,25,25,25,25] = **242 total**, versus 810 in the general model-free scheme. The effects reconstruct to error below 4e-13 at exact expected probabilities.

Under independent launched trials, explicit no-click registration and the true restricted phase-only model, the simultaneous 95% Hoeffding phase-chord propagation bounds for N=1e4,1e6,1e8,1e10 trials per probe are respectively [2.0000,1.5612,.14748,.014667] in operator norm. Actual seeded sample errors were [.05731,.00456,.000396,.0000542]. **Negative result:** at N=1e8, this conservative forest bound (.1475) is roughly 24x weaker than the older full 81-probe model-free Frobenius bound (.00609), even though it uses 70% fewer probe configurations. A globally fitted joint detector model, tighter inference, and optimized probes are needed. We have NOT solved practical calibration sample complexity.

A genuinely sampled model falsifier applies unknown 0.09-rad inter-mode mixing, impossible under diagonal phase drift. Number-basis click frequencies should be phase invariant. At 100,000 trials per input, their largest observed deviation from the model was .031965 against simultaneous 95% null threshold .006399, rejecting the wrong model. The 28 held-out superposition discrepancies are reported separately as **expected** frequencies, not misrepresented as measured confidence.

**Code:** analysis/w33_20261109_phase25_structured_calibration.py

## Front 2 — Four explicitly composed noncommuting lossy analyzers

We reconstructed four full optical measurement designs from previously frozen W33/Q8 matrices and simulated **loss between the actual mixing gates**. The generic device uses nine-mode Givens, the Fourier/permutation device uses fixed qutrit Fourier stages and lossy adjacent SWAP crossings, the two-CZ device uses local qutrit transformations and two independently perturbed phase masks, and the twelve-setting alternative uses four extra product MUB contexts. All eight original W33 Bell contexts were held ideal, so the comparison isolates the additional analyzers.

Each circuit's complete nonunitary K defines nine click POVM effects E_j=K†|j><j|K and an explicit no-click effect I−K†K. Fisher information is evaluated at the same PPT Horodecki state a=.236, **per launched source photon**, with equal total photon budget distributed across settings. The CCNR polar-dual Cramér–Rao variance coefficient, lower being better, is:

| Architecture | Ideal | Moderate | Harsh |
| --- | ---: | ---: | ---: |
| Generic 10-setting | 12.2091 | 12.1860 | 12.1435 |
| Fourier/permutation 10-setting | 10.5778 | 10.5890 | 10.6632 |
| Two-CZ 10-setting | 12.8492 | 12.8470 | 12.8525 |
| **Product-MUB 12-setting** | **9.2551** | **9.2876** | **9.3876** |

The lossy averages use **seven independent randomized phase configurations**. Moderate component intensities: gate=.995, crossing=.99, mask=.999, phase drift RMS=.003 rad; harsh=.98,.97,.995,.010 rad. All tested Fisher matrices are full rank and their ideal CRLBs reproduce the earlier fixed-source-shot benchmark. The twelve-setting design leads under these assumptions; Fourier/permutation leads among tested ten-setting designs.

The generic device's small apparent CRLB improvement with loss has a specific explanation: mode-dependent noncommuting attenuation changes the entire POVM and introduces **state-dependent no-click information**. This is not a claim that random loss improves a fixed instrument's information content or that actual fabricated devices share these ideal assumptions. This remains a synthetic, locally asymptotic benchmark without uncertain calibration, photon drift or finite-shot entanglement confidence.

**Code:** analysis/w33_20261109_four_architectures_full_loss_povm.py

## Front 3 — Exact projective symplectic commutant excludes native three-dimensional invariant generations

We generated and checked all 40 projective symplectic transvections of the W33 point representation on F3^4. Under the group they generate, the 40² ordered point pairs have exactly **three orbits**: (same point) 40, (distinct collinear) 480, and (distinct noncollinear) 1080. Hence the complex commutant of the full projective symplectic action on the native 40-point vector space is three-dimensional, spanned by I40, collinearity adjacency A, and J−I−A.

The point graph is strongly regular SRG(40,12,2,4). Its adjacency eigenvalues and dimensions are [12 with 1], [2 with 24], [−4 with 15]. The permutation representation is multiplicity-free with **three irreducible modules of dimensions 1,24,15**. Any one-body operator preserving the full symplectic W33 point symmetry acts as scalar on each. There is **no invariant three-dimensional subspace** in this exact module from which to derive three generations without adding other representations, explicit extra structure or symmetry breaking.

This is a precise, verified obstruction **only for this 40-point permutation module**. It does NOT rule out generations from other W33 tensor modules, symmetry-broken regimes, nontrivial spinor bundles or higher interactions. It supplies no continuum, gauge anomaly cancellation or emergent spacetime.

**Code:** analysis/w33_20261109_sp4_commutant_generation_obstruction.py

## Front 4 — Official DES Y6 data discovery; frozen S9 remains unscored

The S9 preregistration in analysis/toe_uv/prereg_noshear.json is unchanged, frozen November 8, 2026. It requires an official unblinded new cosmic-shear xi± data vector, matching covariance/n(z), strict xi+>10 and xi−>60 arcminute cuts, corrected scalar-field CLASS/Halofit theoretical predictions and matched nuisance refits. Its numerical predictions on new surveys have **not** been independently tested.

The new read-only official link audit inspected HTML hyperlinks from DES's Y6 release portal and papers page and verified direct candidate FITS first-card availability, along with two public DES GitHub repository endpoints.

- DES Y6 release portal and DES papers: HTTP 200 (HTML).
- Formerly indexed NCSA unblinded 3x2pt FITS: HTTP **404**.
- Public DES y6-ppd-public GitHub analysis code: HTTP 200, but no verified full likelihood data.
- Public des-science/y6-3x2pt GitHub path: HTTP 404 in this environment (could be relocated or not public).
- No fully authenticated and downloaded unblinded xi±+covariance+n(z), corrected theories or matching nuisance refits acquired.

**S9 is UNSCORED.** No DES Y6 χ² comparison was invented from the published conditional S8 constraints. DES says some cosmology products are released and more forthcoming: https://www.darkenergysurvey.org/des-y6-cosmology-results-papers/ . The relevant 3x2pt cosmology paper was accepted November 2, 2026: https://doi.org/10.1103/nnlj-gyr2 .

**Code:** analysis/w33_20261109_des_y6_official_link_audit.py

## Front 5 — Single-photon CHSH with realizable displaced on/off observables

We replaced ideal, freely available local sigma-X/Y Fock observables with the physically motivated **displacement + on/off detector** POVM. In the local {|0>,|1>} basis, with photon detector efficiency η, displacement α and dark-count mean ν,

    E_no(α)=exp(−ν−η|α|²) *
       [[1, −η α*],
        [−η α, 1−η+η²|α|²]],     O=2E_no−I.

The globally erased/path-dephased single-photon signal rho includes independent source survival, relative phase coherence, and *local detector inefficiency*. Numerical optimization searches four complex local displacements to maximize **absolute** CHSH (the strong on/off branch has negative signed CHSH, so maximizing signed CHSH alone was wrong). Results:

| Model | Optimized |CHSH| |
| --- | ---: |
| Ideal source, modes and detectors | **2.688399** |
| 95% detector efficiency | 2.477116 |
| 86% detector efficiency, 92% relative-coherence proxy | **2.021790** |
| Same detector with 10% further source loss | 1.759381 |
| Phase-randomized reference negative control | 1.716641 |

The ideal optimum agrees with published single-photon displaced on/off work: C. Wildfeuer (2026), https://arxiv.org/html/2607.29012, which reports efficiency threshold about .8258 under its full assumptions. Our 92% factor is a **simplified coherence/dephasing proxy**, not that paper's full mode-mismatch parameter. The 86% case has only .02179 Bell margin in the model and the extra source loss destroys it. A 150,000-trial synthetic IID run including all click/no-click outcomes passed a conservative one-sided 95% Bell bound under *ideal* parameters; phase randomization did not.

These calculations are numerical reproductions and engineering controls, not a novel Bell inequality or any laboratory violation. Actual loophole-free single-photon claims additionally require accurate phase-reference/LO photon budgeting, physically separate stations, independent settings, event-ready heralding, total detection logs, no-click events, source quality and causal timing. Two-copy 2026 prior art: https://dakic.univie.ac.at/details/news/testing-single-photon-entanglement-using-self-referential-measurements/ .

**Code:** analysis/w33_20261109_onoff_single_photon_real_detector.py

## Verification and claims boundary

Five scripts each produce a frozen matching JSON under data/. Regression command:

    py -3 -m unittest discover -s tests -p test_w33_20261109_five_advanced_next_executed.py -q

**16 tests passed** on the authorized Windows machine. They check the observable forest/gauge ambiguity, phase-model false-positive detection with independent sampling, all four lossy optical POVMs and their source-shot Fisher benchmarks, exact W33 Sp4 orbit counts, DES S9 fail-closed readiness, and Bell POVM positivity, the 2.6884 prior-art ideal benchmark, negative controls and all-trial confidence.

No global discovery claim: W33's finite mathematics is interesting, but its symmetries do not currently derive Standard Model chirality, generations or gravitational dynamics. The photonic work measures *theoretical engineering feasibility*, not experimental reality.

## Top five independent next investigations

1. **Jointly calibrated, falsifiable optical instrument** — infer physical splitter/phase/loss parameters from trusted probe data with sharply calibrated finite-shot confidence, rejecting wrong phase-only models before quantum claims.
2. **Pareto comparison of real architectures** — compare full loss/no-click POVMs, detector drift, conversion throughput, source photons, and end-to-end PPT entanglement certificate coverage for ten- and twelve-setting designs.
3. **Beyond 40-point one-body symmetry** — search concrete W33 spinor/tensor representations with native three-family labeling, interaction terms, gauge Ward constraints, anomaly consistency and demonstrable continuum behavior.
4. **Actual DES Y6 frozen falsification** — obtain official complete unblinded xi±/covariance/redshift products and patched CLASS/Halofit model predictions with independently refitted nuisances. No S9 score without them.
5. **Operational Bell hardware** — design spatial, independent two-party displaced on/off test with measured reference-photon resources, heralding, all-trial sampling, real event timestamps and a confidence interval robust to actual losses.
