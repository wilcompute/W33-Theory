# Five physics-frontier tests v4: complete adjoint GUTs, seesaw freedom, spectral positivity, DESI evidence, and two-copy photons

**2026-11-19. Status: conditional physics results, verified numerical scans and literature-grounded consistency tests. NOT a Theory of Everything. No W33 assumption.**

Prior work reviewed: commit 740af8b5b (first complete-adjoint obstruction, full DESI 13x13 covariance, one-copy photonic SSR), 40191f8e4 (two-triplet/one-octet one-loop benchmark), 0ec1074e4 (parallel adjoint and photon results), and 9d7b6aafb (global chiral/IR checks). Standard SU5 mass identities, Casas-Ibarra seesaw freedom, KL positivity and two-copy particle-entanglement activation are known prior art. This packet extends them through independent *new-to-this-repository* numerical tests and explicitly avoids broad novelty claims.

## Front 1 — Directly attempt a full renormalizable two-24F spectrum

The earlier toy model achieved a one-loop matching by choosing a GUT scale MU=2e16 GeV, two Majorana weak triplets at MT=2.171635484e7 GeV and one Majorana color octet at MO=4.542710799e5 GeV. Those three fields alone do not form complete SU5 representations. A Weyl 24F decomposes under SM as (8,1,0), (1,3,0), (1,1,0), and vectorlike (3,2,-5/6)+(bar3,2,+5/6). Renormalizable masses from one SU5 adjoint-Higgs VEV obey the signed Clebsch rule:

    MX=(M3+M8)/2.

The one-loop beta shifts for each 24F are:

    triplet: (0,4/3,0)
    octet:   (0,0,2)
    X pair:  (10/3,2,4/3)
    sum:     (10/3,10/3,10/3).

Keep the original MT, MO and MU. Vary the *second* triplet and octet mass over the entire [MZ,MU] interval, construct both forced X masses from the signed relation, and include all non-singlet 24F thresholds. Minimize the Euclidean mismatch norm:

    R=sqrt[(alpha1_inv-alpha2_inv)^2+(alpha1_inv-alpha3_inv)^2].

Differential evolution explores all four independent relative sign choices. **Best numerical R=7.2967835** inverse-coupling units, not zero. The optimizer pushes the extra triplet down to 91.4 GeV (near the lower MZ bound) and extra octet up to 2e16 GeV (the upper MU bound). The other sign combinations give R about 7.312. All four include the low X partner forced by the previous Clebsch relation.

**This is NOT an exhaustive analytic no-go for adjoint SU5.** It is a reproducible numerical scan of a fixed-benchmark, diagonal two-adjoint subspace, without offdiagonal generation mixing, scalar mass thresholds, two-loop running or higher-dimensional operators. The literature already constructs more flexible adjoint spectra with nonrenormalizable operators, for example https://doi.org/10.1016/j.nuclphysb.2021.115484 . No proton lifetime or full GUT model has been calculated.

## Front 2 — Heavy-neutrino nonunitarity and naturalness

For the chosen pair of equal heavy triplets at M=MT, the type-III seesaw has light matrix

    mnu=-(v^2/2) Y^T M^-1 Y, v=246.22 GeV.

Use the preliminary Bari 2026.a normal-ordering oscillation fit and the PMNS matrix as **inputs**, with massless m1 at tree level. The known complex-orthogonal Casas-Ibarra rotation z preserves the entire light mass matrix for all z. Define heavy-light mixing theta=v Y^T/(sqrt2 M) and epsilon=theta theta_dagger. For two degenerate triplets the exact identity is

    Tr epsilon=(m2+m3)/M * cosh(2 Im z).

Therefore Tr epsilon >= (m2+m3)/M = 2.70455e-18 for this chosen mass. Computed values:

| Im z | Tr epsilon | absolute epsilon_e_mu | Illustrative Higgs sensitivity / mh^2 |
|---:|---:|---:|---:|
| 0 | 2.70455e-18 | 1.39163e-19 | 24.0 |
| .5 | 4.17334e-18 | 7.07856e-19 | 37.1 |
| 1 | 1.01750e-17 | 2.05662e-18 | 90.4 |
| 2 | 7.38564e-17 | 1.53477e-17 | 656 |
| 3 | 5.45550e-16 | 1.13426e-16 | 4847 |

The electron-muon offdiagonal mixing is *not* the branching ratio for mu-to-e gamma or conversion; physical processes require full electroweak/tree/loop matching, plus nuclear matrix elements. The displayed Higgs sensitivity is convention/scheme-dependent, not a measured mass shift. Crucially, light-neutrino data alone do not select this hidden complex z or determine leptogenesis. Literature: https://doi.org/10.1093/ptep/ptz125 ; https://global-nu.org/results.html .

## Front 3 — A careful spectral positivity test for an exponentially damped scalar proxy

Assume an **ordinary positive Kallen-Lehmann/Stieltjes Euclidean two-point function** with unit massless pole residue and nonnegative massive spectral measure rho:

    G_E(q)=1/q + integral_0^infty rho(s)/(q+s) ds, rho>=0.

Then for every q>0, q G_E(q)>=1. However the entire-function UV-damped proxy

    D_E(q)=exp(-q/M^2)/q

obeys q D_E(q)=exp(-q/M^2)<1 for every q>0. Thus, under the precisely stated conventional positive spectral assumption, this D_E **cannot itself be that same ordinary physical two-point function**. The script checks six explicit q/M² values and a comparator with positive added massive spectral weight.

This is emphatically **not a no-go for interacting nonlocal quantum gravity or a disproof of all exponential form factors**. In nonlocal theories the modified propagator and time-ordered physical two-point correlator can differ, and ordinary locality/temperedness assumptions can fail. Published work explicitly develops spectral representation with positive density for nonlocal gravity despite those subtleties: https://doi.org/10.1007/JHEP08(2024)204 . More recent reflection-positivity work addresses exponential regulators: https://link.springer.com/article/10.1007/s11005-026-02191-4 . Gauge-fixed gravitons additionally require BRST/physical-state care. Our check solely illustrates why pole-counting alone is not an interacting unitary completion.

## Front 4 — Real DESI DR2 BAO **Bayesian model evidence**, with stated priors

The preceding 740af8b5b pass committed byte-identical source data from https://github.com/CobayaSampler/bao_data/tree/master/desi_bao_dr2, comprising 13 DESI DR2 BAO observables and the complete 13x13 positive-definite covariance. That pass fitted LambdaCDM chi2=10.284 and CPL chi2=5.646 (two more CPL parameters); AIC and BIC were inconclusive. It did **not** integrate model evidence.

Here theory predictions are y_theory=q*t(Omega_m,w0,wa), with q=c/(H0 rd). Fix flat GR and Omega_r=9e-5. Put the **normalized prior q uniform on [20,40]**, and integrate it analytically for each cosmological parameter point. With

    A=t^T C^-1 t, B=t^T C^-1 y,
    qhat=B/A, chi2min=y^T C^-1 y-B²/A,

the integrated likelihood (up to a common data Gaussian factor that cancels in model ratios) is

    Lbar= sqrt(2pi/A)/(qmax-qmin) * exp(-chi2min/2)
          * [Phi((qmax-qhat)*sqrt A)-Phi((qmin-qhat)*sqrt A)].

Take a common uniform Omega_m prior [0.15,0.5]. Integrate LambdaCDM using 120-point Gauss-Legendre quadrature. For each CPL prior use **four independent scrambled Sobol sequences of 8192 points** over Omega_m,w0,wa, and numerical 48-point distance integration.

| CPL prior | w0 interval | wa interval | ln Bayes factor CPL / LCDM | numerical log integration SE |
|---|---|---|---:|---:|
| Narrow | [-1.5,-.5] | [-2,2] | **-0.8525** | .011 |
| Broad | [-2,0] | [-4,4] | **-1.0922** | .032 |
| Necessary nonphantom for z>=0 | [-1,0] | [0,2] | **-2.5505** | .017 |

Negative log factors favor LambdaCDM **for these BAO-only priors and this simplified background likelihood**. The nonphantom background condition w(a)>=-1 is only necessary, not a complete demonstration of a stable canonical scalar field.

**No CMB, SNe, weak lensing, growth likelihood, physical rd calculation, realistic neutrino transfer or Bayesian full-universe model comparison is present.** Evidence ratios are inherently sensitive to chosen priors, and a BAO-only preference cannot overrule a combined-data preference. Compare independent assessments https://doi.org/10.1140/epjc/s10052-026-15431-7 ; https://doi.org/10.1038/s41550-025-02669-6 ; https://arxiv.org/abs/2603.05472 . These are *our specified* sample integrations, not DESI collaboration model evidences.

## Front 5 — Two-copy photonic SSR activation and experimental resources

The earlier one-photon two-mode state (|10>+|01>)/sqrt2 has no operational Bell entanglement if Alice and Bob have only one mode each, no shared phase reference and strict local photon-number superselection. A **known escape** is two copies of that same state.

Represent four optical modes (A1,B1,A2,B2). For two independent copies, locally QND-herald N_A=N_B=1 **before choosing measurement settings**. Two out of four equiprobable basis terms survive, so ideal herald probability is **1/2**. After renormalization the local dual-rail Bell state is

    [|10>_A |01>_B + |01>_A |10>_B]/sqrt2.

Both local logical qubits have exactly one photon in two optical modes, so local dual-rail Pauli X,Z observables can be implemented with number-conserving interferometry and detection. The explicit constructed 16-state Fock simulator gives ideal conditional **CHSH=2sqrt2**.

With independent transmission probability eta per source photon and no other losses, the ideal success probability is

    P_herald(eta)=eta^2/2.

| eta | ideal herald probability |
|---:|---:|
| .5 | .125 |
| .8 | .320 |
| .9 | .405 |
| .95 | .45125 |
| 1 | .500 |

**Required experiment-level qualifications:** nondemolition *event-ready* number heralding must occur before random setting selection to avoid a detection/postselection loophole; destructive after-the-fact filtering is not sufficient. Source indistinguishability, interferometric phase, detector efficiency, timing and finite statistics are not modeled. This is the established Wiseman/Vaccaro two-copy activation, not a new Bell theorem, loophole-free experiment or single-photon universal computing demonstration: https://doi.org/10.1103/PhysRevLett.91.097902 .

## Extra executed track — event-ready photon Bell finite-statistics and emission cost

For the ideal heralded two-copy Bell state with unbiased random CHSH game settings, the quantum winning probability is cos²(pi/8)=0.85355339 versus the local-realistic bound 0.75. Under independent game wins and an ideally pre-setting event-ready herald, the one-sided Hoeffding null tail for an observed win fraction at least as high as the quantum expectation satisfies

    p_local_tail <= exp[-2 N (p_quantum-.75)^2].

To reach a conservative tail bound at most 1e-6 using this idealized expected winning fraction requires **645 valid heralded games**. At photon transmission eta=.8 per source photon and ideal herald probability .5*eta²=.32, this corresponds to approximately **2016 expected source-pair emissions**. The script calculates these exact figures and includes two extra regression tests.

This is **not a power calculation** or a claim of a loophole-free 645-shot experiment. It assumes ideal local detectors, independent fair settings, no drifts or memory, reliable QND pre-setting heralds, and the *observed* win fraction equals its quantum mean. Real statistics, source/detector loopholes and confidence intervals require more conservative experiment design. It provides a concrete experimental resource cost to replace a purely abstract Bell-state claim.

## Scientific outcome and next steps

The five fronts produce independently reproducible conditional constraints, a real-model cosmology evidence calculation and a constructive photonic resource protocol. None of them derives Standard Model particle masses, a dynamical SU5 vacuum, quantum gravity, the Born rule, dark matter or observed constants from a single fundamental Lagrangian. **No TOE is solved.**

Reproduce with:

    python analysis/toe_20261119_physics_five_frontiers_v4.py
    python -m unittest discover -s tests -p test_toe_20261119_physics_five_frontiers_v4.py -v

Code: analysis/toe_20261119_physics_five_frontiers_v4.py

Numerical certificate: data/toe_20261119_five_front_physics_v4.json

Focused tests: **21 passed**, covering GUT full-partner beta shifts and mass constraints, five heavy-neutrino angles, positive-KL proxy inequality, published DESI covariance priors and four Sobol integration replicates, two-photon dual-rail Bell protocol/loss probabilities, and the separate event-ready finite-statistics resource check.

Top five **independent** next steps:

1. **True UV completion:** derive all adjoint and Higgs masses from one symmetry-breaking vacuum, include two-loop BSM thresholds, and predict proton-decay partial lifetimes without hidden mass tuning.
2. **Neutrino mechanism:** simultaneously predict leptogenesis, flavor-violating branching/conversion observables and Higgs radiative stability from the same heavy Yukawas, then compare with oscillation/CP data.
3. **Physical quantum gravity:** construct a gauge-invariant positive-norm causal graviton S matrix, recover GR at low energies, and derive horizon entropy microscopically.
4. **Full cosmic inference:** couple the DESI covariance likelihood to CMB, SN, and lensing, compute rd and dark-energy perturbations, and report explicit Bayesian prior dependence.
5. **Photonic hardware resource model:** build an event-ready two-copy heralded Bell experiment simulator with quantum nondemolition detection, interferometers, finite loss, detector efficiency and scalability analyses.

Outside-box idea to test next: search for one constructive algebra of **positive operational correlations** that simultaneously constrains quantum Tsirelson/SSR resource feasibility and positive physical spectral densities, without assuming either rule as an axiom.
