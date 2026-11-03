# 2026-11-03 — Five TOE fronts + three additional tests: full CLASS, ultralight waves, UV, chirality and evidence

**Executive result.** The existing fitted fading-CDM model has a measurable *mathematical* baryon/CDM transfer split in an actual patched-CLASS calculation, but at subpercent relative growth. An ultralight oscillating scalar can satisfy its *conditional* one-loop mass naturalness benchmark and be cold on conventional clustering scales, but the present work does not combine that oscillating axion with the real CLASS code. A viable TOE remains unestablished.

**Research and preservation.** At intake local and remote `master` were identical at `f98ea2929e2e0b3dbc78acd3f1bbee8a3c0b2686`; staged index empty, 54 preexisting dirty items preserved. No later GitHub commit was present. The independent local mechanism packet `analysis/2026-11-03_toe_mechanism_completion.md` and its untracked scripts were read; they already explore a nilpotent uplift, an actual four-dimensional overlap index, neutrino messengers, an operational gravitational signal, and a holomorphic bridge. Nothing from that still-uncommitted packet is staged here. This pass does **not** claim to have re-reviewed the entire enormous repository.

Relevant external state of research (consulted before coding):
- [Hu–Barkana–Gruzinov 2000](https://doi.org/10.1103/PhysRevLett.85.1158), [accurate effective-fluid axion treatment 2022](https://doi.org/10.1103/PhysRevD.105.123529), [2026 Lyman-alpha pure/mixed fuzzy-DM constraints](https://doi.org/10.1088/1475-7516/2026/09/051): scalar wave pressure and radiation-era transfer need a Boltzmann/hydrodynamics calculation.
- [DESI DR2 release](https://data.desi.lbl.gov/doc/papers/dr2/), [coupled-quintessence 2026 MCMC](https://doi.org/10.1088/1475-7516/2026/02/014), [DESI DR2 inference review](https://doi.org/10.1103/dqxw-yp1j), [cosmological model Bayesian evidence](https://doi.org/10.1038/s41550-025-02669-6): covariance, profile likelihoods and prior volume matter.
- [Vissani 1998 Higgs naturalness](https://doi.org/10.1103/PhysRevD.57.7027), [Thorngren–Preskill–Fidkowski 2026 chiral regulators](https://link.springer.com/article/10.1007/JHEP07%282026%29271), [Craig 2026 chiral lattice measure](https://arxiv.org/abs/2610.09093): chiral anomaly cancellation does not itself supply a local nonperturbative Weyl measure.
- [D'Amico–Hamill–Kaloper 2016 light axions/dark monodromies](https://doi.org/10.1103/PhysRevD.94.103526): symmetry and radiative light-DM protection precede this project; no foundational novelty is claimed.

## Front 1 — Ultralight oscillating DM perturbations, a non-relativistic benchmark

Producer: `analysis/toe_20261103_ultralight_subhorizon_growth_controls.py`; certificate `data/toe_20261103_ultralight_subhorizon_growth_controls.json`.

For a canonical real scalar of input mass `mchi=1e-20 eV`, the WKB/effective-fluid quantum pressure adds `k^4/(4a^4 mchi^2 H^2) delta_chi` to the subhorizon logarithmic-time evolution. Coupled quintessence modifies the dark friction and adds a scale-dependent unscreened `1+2beta²` dark force. The numerical two-species ODE integrates matter contrasts for 7 wavenumbers `k=0.05,0.2,1,10,100,300,500 h/Mpc` from `z=99` to today, using the actual repository fitted coupling `beta=0.0529975` and the fitted endpoint field excursion.

**This is an exploratory Newtonian emulator, not a cosmologically self-consistent full perturbation solver.** Specifically, its scalar field-clock interpolation `x(a)` is supplied rather than solved; an LCDM-like compensating dark-energy density does not obey the covariant scalar continuity equation. Primordial radiation-era transfer and quantum pressure initialization are absent. At `k=.2 h/Mpc`, the fully coupled-to-uncoupled model gives a `1.6323%` change of the simulated chi contrast and a baryon/chi ratio `0.99273` (both conditionally). At extreme `k=300,500`, the high-k initial conditions and oscillatory transfer are physically unreliable; they serve as pressure/non-pressure falsifiers only, not Ly-alpha predictions.

The pure-FDM 2026 Lyman-alpha bound `m>1.9e-21 eV` is **not a fit for interacting fuzzy dark matter**, so passing its numerical mass comparator cannot be counted as a confidence-level pass for this toy model. A full CLASS/CAMB implementation must use an accurate effective-fluid sound speed and radiation-era initialization.

## Front 2 — Actual patched CLASS with species-resolved transfer functions

Producer: `analysis/toe_20261103_real_CLASS_fading_species_transfers.py`; certificate `data/toe_20261103_real_CLASS_fading_species_transfers.json`. Executed on authorized Windows machine using installed Ubuntu `~/cosmo/class_fading/class` and `analysis/toe_uv/class_cmb.py`. Three **actual** background+lensed spectra+linear-perturbation calculations:

1. Stored full-Planck+DESI+Dovekie best-fit fading model `cp=0.05299751293406564`.
2. **Same cosmological input parameter values**, setting `cp=0` but retaining the declared exponential potential (not a refit).
3. Separately fitted native LCDM best-fit parameter inputs (different parameters, not a controlled coupling-only comparison).

CLASS emitted actual transfer functions at z=0,0.5,1,2,5; their headers explicitly confirm redshifts; files include `d_b,d_cdm,d_m,phi,psi`. For `k=0.1 h/Mpc`, the baryon/CDM contrast transfer ratio is `0.9880148` fading vs `0.9933781` same-parameter zero coupling; the normalized total-matter *growth from z=5 to 0* ratio is `1.0033195`. At k=.05,.2, the latter is `1.00332045`,`1.00331178`; the baryon/CDM ratios are `0.988276,0.990306` versus `0.993636,0.995699`. These are **solver predictions for the original pressureless fading-CDM model**, not the ultralight-axion proposal and **not an observed detection**. Full RSD/weak-lensing likelihood, galaxy/halo bias and survey covariance are not evaluated. Best-fit native LCDM differs in background parameters, so its z0 transfer ratio is confounded.

The actual CLASS calculation is more relevant than the earlier idealized phiMDE extrapolation; it finds a 0.33% change in normalized growth, distinct from the 1.6% toy emulator contrast effect. Comparison of two different time histories is expected to differ.

## Front 3 — radiative protection and controlled environment effects

Producer: `analysis/toe_20261103_ultralight_uv_density_clock.py`; data `data/toe_20261103_ultralight_uv_density_clock.json`. A rolling canonical scalar phi with ultralight DM potential `U=V(phi)+0.5*m0² exp(-2beta phi/Mpl)*chi²` can be adiabatically averaged when mchi≫H. Its one-real-boson Coleman–Weinberg potential in a declared MS-bar scheme at `mu=mchi(today)` has `d² V1 /d (phi/Mpl)²|today = -beta² mchi^4/(8pi²)`, hence a **negative** one-loop curvature; absolute size `2.8667e-74 H0²` for 1e-20 eV input. This tiny effect is NOT the full quantum stability condition: higher-mass fields, loops involving quintessence itself, gravity-mediated soft breaking, shift-symmetry breaking and finite-density physics remain.

The older uncommitted `analysis/toe_20261103_mechanism_portal_protection.py` already models one explicit soft RG portal; it is acknowledged, not replicated. A protected positive-energy microphysical completion was **not constructed** in this pass.

## Front 4 — 3+1D anomaly-free chiral/neutrino compatibility and electroweak cost

Producer: `analysis/toe_20261103_chiral_messenger_naturalness_floor.py`; corresponding data. Independent exact check of published sterile sector `data/toe_20261103_sterile_anomaly_operators.json`: per SM generation, `Q=3(B-L)` gives linear/cubic `(-3,-27)`; three generations plus left singlets `(-15,+12,+12)` cancel `(-9,-81)`. Mixed hypercharge anomalies also vanish; three vectorlike N pairs and a B pair do not alter gauge anomalies, and the SU2 Witten doublet count is even. This is an anomaly certificate, **not a global anomaly-free chiral lattice measure**.

For a minimal rank-one **Dirac** messenger with `mnu=vY epsilon`, `v=174 GeV`, `mnu>=0.05 eV`, `|epsilon|<=1`, and unprotected `delta mH²~Y² M²/(8pi²)`, requiring `|delta mH²| <=(125 GeV)²` gives `M<3.8653e15 epsilon GeV`. Example epsilons 1,0.1,0.01 lead to maxima `3.87e15,3.87e14,3.87e13 GeV`. At `M=1e16 GeV`, even the optimally mixed case has a lower correction 6.69 times the Higgs reference mass-squared. This conditional naturalness problem supplements the previously uncommitted explicit three-N-plus-B messenger chain, which still has unconstrained Yukawa/flavor parameters and a large Higgs threshold. Gauge and SUSY partner cancellations can evade the bound; no full 4D chiral lattice action is built here.

## Front 5 — cosmological model selection and honest holdout boundary

Producer `analysis/toe_20261103_model_selection_guard.py`. From actual jointly fitted Dovekie `analysis/toe_uv/class_fit_dovekie.json`, `DeltaChi²(fading-LCDM)=-10.653512481`, broken into CMB `-1.49536`, priors `-0.31258`, BAO `-3.77539`, supernovae `-5.07019`. The fading model and CPL each have two extra phenomenological parameters, and the existing best-fit CPL is better than fading by `1.22463` chi². With two extra parameters, `DeltaAIC=-6.6535`. Under **illustrative** independent-data Schwarz BIC, the sign changes at `N=exp(10.6535/2)=205.77` independent observations. Choosing raw SN+CMB bin count is not a legitimate estimate of evidence: covariance and broad nuisance structure matter.

**Not a Bayes factor and not a true holdout.** The same CMB, BAO and SN data were used to fit both models. Their separate chi² contributions at a *joint* optimum are cross-probe diagnostics only; no leave-one-probe-out reoptimization or independent later validation data was run. The answer to whether the fading scenario predicts independently is still open.

## Three additional independent ideas executed

### Additional I — WKB oscillator clock and environmental mass

For slowly varying `mchi(phi)`, the adiabatic invariant gives comoving number `n a³` constant, average energy `rhochi=n mchi`, and oscillation envelope `Achi∝a^(-3/2)mchi^(-1/2)`. With the actual fitted `mrec/m0=1.0149281`, the early envelope relative to naive fixed-mass dust is `0.99261848`: a *0.738% correction* usually neglected in a casual mass-varying CDM mapping.

At fixed comoving number, curvature of `rho=n m(phi)` is `beta²rho/Mpl²`. Today this is `3beta² Omega_chi H0²=0.00221328 H0²`, i.e. mass `0.0470455 H0`. At *fixed field amplitude chi*, the derivative of quadratic potential has twice this curvature. **These are distinct ensembles**, and mixing them gives a factor-of-two modeling error; not a new chameleon theorem.

### Additional II — clock sequestering requirement

The older repo frozen alpha-variation bound `analysis/toe_uv/dd_clocks.json` corresponds to an older background fit, with `|d ln alpha/d(phi/Mpl)| <~ 1.0007e-7`. Comparing only as an *illustrative* sequestering budget with the updated fitted dark coupling `beta=0.053` gives `beta_EM/beta_DM <~1.89e-6`. This is not a universal ordinary-matter limit and does not mean beta_dark is itself bounded by an electromagnetic clock: the electromagnetic coupling could be exactly absent by symmetry. It quantifies the protection a proposed unified coupling must provide. New CLASS phi'(today) could change the numerical clock budget.

### Additional III — Landau-pole checkpoint for messenger UV sector

The separate unpublished mechanism report derives `bBL=59` for a specified nonsupersymmetric messenger theory and `bBL=102` for a separate SUSY holomorphic variant, **both only above the named thresholds**. In a simple one-loop U(1) RG with high-scale threshold `M=1e16 GeV`, requiring the Landau pole above reduced Planck mass `2.435e18 GeV` implies `gBL(M)<0.49349` in the first model and `<0.37532` in the second. These are conditional normalisation-dependent thresholds, *not perturbative unification predictions*, and strong coupling may require stricter criteria than the formal Landau pole.

## Test contract, novelty and outstanding TOE barrier

Producer code and JSON are separately staged in `analysis/` and `data/`. Regression `tests/test_toe_20261103_class_ultralight_uv_eightfronts.py` verifies the 3 real CLASS transfer tables, source-matched numerical ratios, fixed-mass/quantum-pressure controls, anomaly cancellation, naturalness inequality, WKB/density/clock budget, and evidence-boundary warnings. All calculations are reproducible on the authorized local machine; only the CLASS producer requires Ubuntu with the patched binary and its cosmological assets. The exploratory code is NOT a physically complete Boltzmann or UV model.

**Not a TOE. Not a new likelihood fit. Not a fully coupled ultralight CLASS. Not a Bayes factor. Not a global anomaly-free chiral lattice measure.** This program has not derived three generations, a protected cosmological constant, particle mass spectrum, or gravity from one action.

## Top five next independent experiments

1. **Real coupled ultralight Boltzmann solver:** add a mass-varying axion fluid to CLASS while preserving background and perturbation energy-transfer and late matter pressure, checking against accurate-axion effective fluid literature. Only then confront Ly-alpha hydro transfer and DESI jointly.
2. **Actual holdout RSD/lensing likelihood:** extract redshift- and scale-dependent `f sigma8` and baryon bias from CLASS, propagate survey covariances and calibration/selection nuisance, and fit/reweight against independent RSD and lensing samples with reproducible split labels.
3. **Dark-sector UV protection:** specify shift symmetries, a positive cosmological vacuum, and all heavy portals, and calculate radiative corrections in a common renormalization scheme with UV threshold and quantum-gravity controls.
4. **Nonperturbative chiral action:** reconcile the actual 4D overlap index sector with the exotic `B-L` messenger matter and global gauge group; test index-sector Weyl phase reconstruction, Ward identities and local measure rather than counting anomalies only.
5. **Independent gravity falsifier:** find a counterexample or distinctive multi-probe effect combining gravity-mediated entanglement, gravitational lensing, scalar fifth-force spectroscopy and clock evolution without assuming an externally fixed physical c or a selected particle spectrum.
