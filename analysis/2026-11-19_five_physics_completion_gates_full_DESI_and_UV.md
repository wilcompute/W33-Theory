# Five physics completion gates: SU(5), neutrinos, gravity, DESI DR2 and photonic operational resources

**Date: 2026-11-19. Status: reproducible, conditional physics tests; NOT a Theory of Everything.** The finite W33 geometry is not an input. This pass audits and stress-tests the earlier 40191f8e4 adjoint/unification toy model, alongside parallel 7106f22ae and 9d7b6aafb sector constraints. Parallel commit 0ec1074e4 landed during this pass and independently gives the same unmixed single-adjoint SU(5) Clebsch relation and initial one-loop X-shift, as well as a photon superselection diagnostic. Those established results are NOT claimed as our discoveries. Our distinct increments are the arbitrary two-generation complex Takagi-mixing singular-value theorem, a seven-angle type-III naturalness scan, and the publicly released full 13x13 BAO covariance and model-fit comparison, plus reproducibility fixtures and independent tests.

## 1. A concrete obstruction to the simplest renormalizable SU(5) completion

The preceding toy theory had two Majorana electroweak triplets (1,3,0) at M_T=2.171635484e7 GeV, one Majorana color octet (8,1,0) at M_O=4.542710799e5 GeV, and a chosen gauge-coupling crossing at M_U=2e16 GeV. These fields alone do not constitute complete SU(5) representations.

Take two fermionic 24_F generations, with only renormalizable symmetric Majorana masses from an SU(5)-invariant bilinear and a single 24_H adjoint-Higgs VEV in the direction diag(2,2,2,-3,-3). Under the SM, a 24_F decomposes into

    (8,1,0) + (1,3,0) + (1,1,0)
    + (3,2,-5/6) + (3bar,2,+5/6).

For 2x2 complex symmetric generation matrices M and K, the triplet, octet, and leptoquark-like mass matrices obey

    M8 = M + 2 K; M3 = M - 3 K;
    MX = M - K/2 = (M8+M3)/2.

The matrix singular-value perturbation inequality yields the exact bound

    s_min(MX) <= (s_min(M8) + ||M3||_2)/2.

Assume both triplet masses remain at most M_T and at least one octet mass remains at most M_O, as required to retain the specific old benchmark. Then at least one X mass is at most

    (M_T+M_O)/2 = 1.108531296e7 GeV.

This holds under arbitrary complex flavor mixing. The implementation verifies 200 randomized complex-symmetric Takagi realizations in addition to the algebraic proof. An explicit, illustrative aligned realization uses M3=diag(M_T,M_T), M8=diag(M_O,M_U), giving MX=diag((M_T+M_O)/2,(M_T+M_U)/2).

The complete Weyl 24_F beta-function shifts are

    triplet (0,4/3,0), octet (0,0,2),
    X+Xbar (10/3,2,4/3),
    total (10/3,10/3,10/3).

The forced light X alone, if the previous toy matching is not retuned, produces a spread about **6.7843** between the inverse gauge coupling shifts at M_U. Therefore the earlier 2-triplet+1-octet one-loop crossing is NOT an already physically completed SU(5) prediction.

**Scope:** this only applies to two 24_F multiplets with the stated renormalizable mass terms and one adjoint spurion. Additional Higgs reps, higher-dimensional operators, extra fermions or new mixing can evade it. All threshold masses must be refit; a light X is not automatically phenomenologically excluded. No proton decay or complete two-loop GUT calculation was performed.

Prior-art background: https://www.sciencedirect.com/science/article/pii/S0370269307008775 and https://academic.oup.com/ptep/article/2024/8/08C101/7687822 . The SU(5) relation is established group theory, not a claimed novel discovery.

## 2. Neutrino flavor degeneracy and heavy-sector naturalness

For two type-III Majorana triplets of degenerate mass M=M_T, the tree-level seesaw mass matrix is

    mnu = -(v²/2) Y^T M^-1 Y,  v=246.22 GeV.

Fix normal-ordering light oscillation inputs from the preliminary Bari 2026.a fit (not derived in this model), one massless active neutrino at tree level, and the reference PMNS matrix. In Casas–Ibarra notation, for any complex angle z,

    R(z) = [[0,cos(z),sin(z)],[0,-sin(z),cos(z)]]
    Y(z) = i sqrt(2M)/v R(z) sqrt(diag(m_i)) U^dagger.

The **same** light mass matrix is obtained for every z, with numerical reconstruction error below 1e-22 GeV. Yet the heavy Yukawa norm obeys exactly

    Tr(Y^dagger Y) = [2M(m2+m3)/v²] cosh(2 Im(z)).

The illustrative convention-dependent Higgs-mass threshold sensitivity

    abs(delta mH²) ~ [3/(16 pi²)] M² Tr(Y^dagger Y)

equals about 24 times the squared 125.25 GeV Higgs mass at Im(z)=0 and about 4.85e3 times this value at Im(z)=3. These numbers are naturalness diagnostics, not scheme-independent observables. Real Casas–Ibarra rotations reshuffle flavors; imaginary angles exponentially enhance couplings without altering the measured light spectrum. The model does not predict ordering, CP phase, charged LFV, leptogenesis or this free complex angle.

Prior art: Casas–Ibarra seesaw parametrization; preliminary data https://global-nu.org/results.html .

## 3. Gravity: pole positivity is a necessary condition, not a Theory of Everything

For a local polynomial higher-derivative quadratic spin-2 propagator,

    1/[p²(1+p²/M2²)] = 1/p² - 1/(p²+M2²).

The massive pole has residue -1. A fundamental propagating positive-norm, positive-energy massive spin-2 interpretation of this local truncation is inconsistent with spectral positivity. The script tests the identity over 41 momenta. This is an established higher-derivative-gravity ghost diagnostic; a heavy EFT pole beyond the cutoff need not be a physical ghost, and nonlocal or other UV completions may evade it.

The earlier healthy R+R² inflationary scalaron is spin 0 rather than this extra ghostly spin 2 and has Compton range about 6.64e-30 m at the calibrated N=55 inflationary benchmark. Neither calculation establishes microscopic black-hole entropy, graviton unitarity, an ultraviolet completion or the dark-energy constant.

Background: https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2018.00077/full .

## 4. Complete published DESI DR2 BAO covariance replaces the two-point diagonal toy score

The following upstream Cobaya DESI DR2 files are saved **byte-for-byte** in this commit. Regression tests recheck their Git blob SHA-1 identities:

    data/desi_dr2_13_mean_20261119.txt
        sha 8aff444fdb42c0946342aa0011ab287eda097c4c
    data/desi_dr2_13_cov_20261119.txt
        sha fd8e5697ab61379b07b52efb781ea6713417a4d9

Source: https://github.com/CobayaSampler/bao_data/tree/master/desi_bao_dr2 . The measurements comprise 13 published DESI DR2 BAO quantities, D_V/rd, D_M/rd and D_H/rd, at redshifts 0.295–2.33. The 13x13 covariance is positive-definite and retains the measured transverse/radial anticorrelations. This is an actual **BAO-only Gaussian likelihood**, not yet a combined CMB/SN/lensing cosmological analysis.

For flat GR, fix a small present radiation component Omega_r=9e-5 and model E(z) with LambdaCDM or CPL w(a)=w0+wa(1-a). Predict the background BAO distances by 64-point Gauss-Legendre integration. In each cosmological fit, **do not fix H0 or rd separately**: BAO only constrains q=c/(H0 rd). Profile this common amplitude exactly with covariance C:

    theory_i = q t_i(Omega_m,w0,wa)
    q_best = (t^T C^-1 y)/(t^T C^-1 t)
    chi² = (q_best*t-y)^T C^-1(q_best*t-y).

Numerically minimize across Omega_m for LambdaCDM, and Omega_m,w0,wa for CPL, with multistart bounded optimization. Results:

| Model | chi² (13-point DESI DR2) | Omega_m | w0 | wa |
|---|---:|---:|---:|---:|
| LambdaCDM (2 fitted parameters including q) | **10.2837** | .29714 | -1 fixed | 0 fixed |
| CPL (4 parameters, baseline bounds) | **5.6458** | .37890 | -.25 boundary | -2.4722 |
| CPL (wider bounds) | **5.6184** | ~.38 | -.1798 | -2.7116 |

The CPL chi² improvement for two extra parameters is 4.638. Information-criterion differences, CPL minus LambdaCDM: **Delta AIC=-0.638, Delta BIC=+0.492**. These criteria are not statistically decisive. Widening the allowed w0 range moves the best-fit parameter significantly while improving chi² by only .0274. It is inappropriate to claim a stable BAO-only dark-energy evolution detection from this. The best-fit CPL crosses the phantom divide; it cannot everywhere be a minimally coupled canonical scalar with positive kinetic energy.

As a separately labeled **simplified diagnostic**, include the DES Year 6 overlap-excised angular BAO measurement D_M(.851)/rd=19.74±.60 as a fourteenth scalar with zero assumed cross-survey covariance. The resulting baseline chi² is **10.845** for LambdaCDM versus **6.140** for CPL; again no decisive evidence.

**Limits:** no full DESI selection/systematic likelihood beyond this published BAO Gaussian compression, no supernova or CMB constraints, no Boltzmann code or primordial sound-horizon prediction, no realistic neutrino/radiation perturbation parameter scan, no joint survey cross-systematic covariance, no Bayesian parameter-prior integration. AIC/BIC offer only rough complexity penalties. The fitted H0 rd product is not two separately measured physical constants.

Source papers: https://journals.aps.org/prd/abstract/10.1103/tr6y-kpc6 ; https://journals.aps.org/prd/abstract/10.1103/d474-zzzf .

## 5. Photonic quantum foundations: the operational phase-reference requirement

A single photon spread between two separated local optical modes is represented by

    |psi> = (|10> + |01>)/sqrt(2).

With unrestricted local two-qubit observables it has negativity 1/2 and CHSH capacity 2sqrt2. With **strictly one mode per lab, no ancillary systems and local U(1) photon-number superselection**, only diagonal local number-conserving observables can be measured. Operational local phase twirling then reduces the state to

    rho_twirled = (|10><10| + |01><01|)/2.

The resulting negativity is zero and optimal CHSH falls to **2**. The script independently checks the partial-transpose spectra, Horodecki CHSH values and 120 random products of allowed local number-conserving observables, proving raw and twirled states indistinguishable under those operations.

**Scope:** this is not a universal no-go for single-photon Bell tests. Additional photons, ancillas, local oscillators and cleverly designed reference-frame-independent protocols can restore Bell accessibility; phase-resource accounting must be explicit. A single system's path/polarization contextuality test also does not itself prove spacelike Bell nonlocality.

Prior art: https://journals.aps.org/pra/abstract/10.1103/PhysRevA.79.032109 ; https://journals.aps.org/pra/abstract/10.1103/PhysRevA.88.012111 ; https://www.nature.com/articles/s41598-018-20034-8 .

## Synthesis: what is and is not established

We have (i) a conditional refutation of the previous toy matching as a complete minimal renormalizable SU(5) spectrum, (ii) quantified seesaw Yukawa/naturalness freedom, (iii) a familiar fourth-derivative gravity spectral obstruction, (iv) real DESI DR2 covariance fitting that is **not** decisive on evolving dark energy, and (v) an operational photon reference-frame constraint. These are established *separate* consistency conditions, not a unified physical dynamical model. No TOE discovered, no unique particle constants predicted.

### Reproduce

    python analysis/toe_20261119_physics_full_covariance_uv_operational.py
    python -m unittest discover -s tests -p test_toe_20261119_physics_full_covariance_uv_operational.py -v

Reproducible result JSON: data/toe_20261119_five_physical_completion_gates.json.
All **17 focused tests pass** (including the two exact external file Git blob hashes).

### Five independent top next steps

1. **UV-complete the full adjoint mass spectrum:** Construct and test all 24_F/Higgs partner masses, complete 2-loop gauge/Yukawa thresholds and proton decay, with explicit symmetry breaking and F/D or scalar vacuum stability.
2. **Neutrino flavor and leptogenesis:** Determine complex Casas–Ibarra freedom from a real flavor symmetry, compute lepton-flavor violation, thermal leptogenesis and loop sensitivity, then predict observable CP and 0vbb.
3. **Quantum gravity amplitudes:** Establish positive-norm, causal, cutoff-controlled graviton propagation and scattering, recover the Einstein low-energy limit and microscopic black-hole entropy.
4. **Full data likelihood:** Incorporate the CMB/SNe and lensing likelihood products with covariance and rd calculation, including dynamical-DE perturbation stability and actual Bayesian model evidence.
5. **Quantum operational derivation:** Account for realistic phase reference and photonic SSR resources and derive Born probabilities/Tsirelson plus experimentally viable device-independent protocols without inappropriate postselection.

**The central progress is a sharper physics falsification framework, not a solved theory of everything.**
