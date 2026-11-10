# W33/TOE: Seven executed physics fronts, one exact gauge decoder, and a correction

**Research: November 9, 2026 (Eastern).** Seven newly executed Python programs and their frozen JSON output, one new regression suite, plus explicit correction of an earlier invalid Fisher derivative and its published report. The findings are exact finite mathematics, statistical simulations, optical system design and public-data readiness checks. **They do NOT establish a theory of everything, a new particle, or a functioning single-photon device.**

## 1. A realizable mathematical dark-state target

For the native W33 40×40 point-line incidence B and point collinearity A=BB^T−4I, the exact rank-15 projector is P=(8I−4A+J)/24. Take psi=P[:,0]/sqrt(3/8). Then B^T psi=0, and a single photon prepared with mode amplitudes psi has the following exact mode intensities:

| Set of output modes | Number of modes | Intensity per mode | Sum |
| --- | ---: | ---: | ---: |
| Selected center | 1 | 3/8 | 3/8 |
| Collinear neighbors | 12 | 1/24 | 1/2 |
| Noncollinear others | 27 | 1/216 | 1/8 |

The twelve collinear amplitudes have a negative sign relative to the remaining 28. An explicit recursive balanced binary splitter construction prepares all 40 real amplitudes using **39 tunable two-mode split operations across six layers** with sizes [1,2,4,8,16,8], plus twelve relative pi-phase corrections. It was checked to ~machine precision.

With chiral Hamiltonian H0=[[0,B],[B^T,0]], this point-sector state has zero line-sector amplitude for all times. At a single incident edge phase theta, opposite-sector probability at small dimensionless t is P_line(t)=(3/2)sin²(theta/2)t²+O(t⁴). Propagation with the exact 80×80 unitary reproduces this law for t=.005,.02,.05,.1. But a single-center preparation attenuation eta yields an *indistinguishable sort of false-null-breaking signal*: raw leading line leakage coefficient (3/2)(1−sqrt(eta))², divided by survival 1−(3/8)(1−eta) for the conditional transmitted state.

**Physical caveat:** Six layers assume arbitrary optical mode pairings. Actual waveguides, routing losses, source/LO photons and detectors are not implemented. A zero in this chosen tight-binding Hamiltonian is not a physical TOE prediction without a principled derivation of the Hamiltonian.

Producer: analysis/w33_20261109_dark_frame_photonic_protocol.py.

## 2. Exact distinction between pure U(1) gauge and nonzero physical Wilson flux

The native W33 Levi graph has 80 vertices, 160 incidence edges and **81 independent cycles**, already known from earlier repo passes. The new test directly compares link phases in its complex incidence matrix.

Pure vertex gauge T=D_points B D_lines† leaves all singular values invariant: rank 25, 15 point and 15 line dark zero modes, and zero net phase around every cycle.

A genuine nontrivial phase at **one single incidence edge** changes rank to 26 and leaves **28** zero eigenvalues. Changing k incidence entries can increase rank by at most k, so >=max(0,30−2k) chiral zero modes remain, regardless of phase values. The numerical disjoint-edge controls confirm this bound; it can be loose. A seeded generic independent phase assignment across all 160 links made the matrix full rank40 and left *zero exact dark modes*. Full group-equivariant dynamics or pure gauge preserve the native degeneracy; arbitrary dynamical flux need not.

**Scientific meaning:** The 30-mode dark degeneracy is NOT protected under arbitrary gauge-invariant flux backgrounds. A TOE model must select its allowable gauge backgrounds dynamically rather than assume rank protection survives all phases. This is a finite graph rank theorem, not a dynamical Yang–Mills law, anomaly theorem or 3+1D chiral spectrum.

Producer: analysis/w33_20261109_flux_dark_mode_fragility.py.

### Bonus: constructive Wilson-loop syndrome decoder

Select a spanning tree of 79 Levi edges. All its phases are removable by 79 independent vertex-gauge differences; 81 chords remain. For the integer vertex-edge matrix D (80×160) and fundamental-cycle matrix C (81×160),

    rank(D)=79, C D^T=0, and C restricted to chord columns is diagonal ±1.

This proves rank(C)=81 **over integers**, not just numerically. A BFS algorithm removes all tree phases and returns 81 gauge-invariant chord-loop syndromes. Every 160-edge complex phase configuration is reconstructed from those syndromes plus vertex gauges to <7.1e−16 in our seeded test, and gauge-shifted syndromes agree to <1.4e−15.

**Pure gauge iff all 81 fundamental Wilson fluxes vanish modulo 2pi.** This guarantees the original dark structure only if hopping magnitudes and incidence support are unchanged. A real implementation requires noisy Wilson phase interferometry and calibration. The W33 81-cycle rank is prior repo work, not claimed new.

Producer: analysis/w33_20261109_81_wilson_flux_decoder.py.

## 3. Calibration: permanent correction plus finite-count multinomial MLE

**Critical erratum:** The prior analysis/w33_20261109_phase_fisher_information.py computed phase derivatives with one output/input index transposed. The originally published ratio **1.3693 is INVALID**. A finite-difference regression detected it. That script, its frozen JSON and the earlier PASS20261109_TOE_POINT_LINE_FLAT_BAND_CALIBRATION_BELL_S9.md were corrected and contain a visible correction notice.

The valid formula for phase theta_k is

    d p_r / d theta_k = 2 Re[conj(amplitude_r) * i * K_rk * psi_k * exp(i theta_k)].

The corrected forest/dense ratios in all ten W33-Q8 analyzers are

    [2.60417,3.64583,1.75000,3.29861,2.95139,1.16667,
     5.38194,4.16667,2.32188,5.23882], mean 3.25260.

They compare local asymptotic inverse-Fisher trace with equal total *launched* calibration photons. The redundant design outperforms minimal forest phase probes in all ten *local Fisher* benchmarks.

To check actual sampled performance, we implemented joint **multinomial maximum likelihood** using all nine click plus no-click outcomes, optimizing gauge-fixed relative phases at known stationary K_cal. Three contexts (0,2,8), 12 seeded independent repetitions each, compared minimal forest vs all observable coherent input pairs at approximately 640,000 launched phase-probe photons per context. Basis-state probes are phase-insensitive under the exact K_cal-only phase model, and are reserved for separately budgeted model falsification.

Empirical forest/dense mean maximum POVM effect error ratios were **1.2777, 0.9684, 1.3450**, respectively; mean 1.1970 across the three contexts. A weak finite-sample result for one setting is perfectly compatible with the stronger asymptotic Fisher prediction. All optimizations converged. The phase model, nuisance amplitudes and source state are *assumed*, so there is still no rigorous detector error bound below the required 0.00016483 or PPT entanglement certificate. Twelve repetitions do not establish 95% frequentist coverage.

Producer: analysis/w33_20261109_joint_phase_mle.py.
Corrected producer: analysis/w33_20261109_phase_fisher_information.py.

## 4. Four-way optical oracle source-shot allocation

For the frozen Horodecki a=.236 PPT test, we recomputed all four physically decomposed (including mode-dependent internal loss) POVM Fisher matrices. With known state and known fixed polar-dual CCNR witness, minimize h^T (sum_context w_context F_context)^(-1)h over all context shot fractions w, with at least 1% per setting and sum w=1.

| Analyzer | Equal-shot inverse-Fisher coefficient | Optimized coefficient | Reduction |
| --- | ---: | ---: | ---: |
| Generic 10-setting mesh | 12.2091 | 6.0193 | 50.7% |
| Fourier/permutation 10-setting | 10.5778 | 6.2412 | 41.0% |
| Two-CZ local 10-setting | 12.8492 | 7.3357 | 42.9% |
| **Product-MUB 12-setting** | **9.2551** | **4.9447** | **46.6%** |

The direction persists under one seeded moderate noncommuting-loss scenario. The nominal previously calculated **oracle asymptotic** 95%-size/95%-power launch lower budget for the 12-setting device is reduced from 10,705,188 to about **5,719,418**. It is emphatically NOT a laboratory sufficient-shot forecast. The witness is assumed known before allocation, estimator efficiency is hypothetical, finite-count confidence is absent, and the huge calibration uncertainty bottleneck remains. Pilot/held-out experiments and robust multi-state allocation are necessary.

Producer: analysis/w33_20261109_four_readout_shot_allocation.py.

## 5. One-signal-photon Bell detector and source thresholds

The existing physically motivated displacement/on-off qubit local POVM (with actual coherent reference resources) had nominal ideal-IID |CHSH|=2.0217899 at detector eta=.86, phase coherence gamma=.92, no global source erasure and dark-count mean 1e-4. The exact dependence on source survival s yields for those **fixed nominal settings**:

    source_survival_required = 0.9936392997815132 (99.36%).

At a distinct engineering envelope s=.98, gamma=.91, dark mean 2e-4, multistart optimization of four complex displacements gave

    eta=.85 -> 1.90652; .88 -> 2.02102; .90 -> 2.10120;
    eta=.92 -> 2.18174; .94 -> 2.26261; .96 -> 2.34378.

For the **fixed analyzer optimized at eta=.94**, the CHSH crossing occurs at eta=0.8762581457753132 (87.63%). These are model-specific feasible crossings, not universal detector thresholds, globally certified optimization or an actual Bell violation. In a real space-like arrangement the local oscillator/reference photons, no-click events, heralding and timing must be independently certified. Prior-art on/off photonic Bell calculations: https://arxiv.org/abs/2607.29012 .

Producer: analysis/w33_20261109_onoff_hardware_threshold.py.

## 6. DES Y6: immutable preregistration and adversarial source-data gate

The S9 scalar-field shear prediction was frozen **2026-11-08** in analysis/toe_uv/prereg_noshear.json. The new evidence-validator checks its SHA256 against the frozen prior research certificate and requires actual unblinded xi± FITS, publisher-authenticated digest, matching covariance and source n(z), xi+>10 arcmin and xi−>60 arcmin, corrected CLASS/Halofit-scf nonlinear theory and nuisance refits for all frozen four models.

The official DES/NCSA archive and landing page respond HTTP 200, but their HTML is **not** a verified complete unblinded survey data product. The previously indexed full FITS candidate returned HTTP 404 in earlier checks, and the public DES Y6 PPD repo describes analysis code rather than supplying the required full model likelihood: https://github.com/des-science/y6-ppd-public . The DES collaboration publishes recent Y6 cosmology papers and says further data products are still coming: https://www.darkenergysurvey.org/des-y6-cosmology-results-papers/ .

Five invalid evidence manifests were rejected: empty, publication summary masquerading as vector, fake FITS without authenticated digest, altered cuts/model set, and missing local file. Even an all-true *self-attested* manifest would not prove an independent publisher SHA. **NO REAL DES Y6 S9 DELTA-CHI-SQUARED WAS SCORED.** This is not positive or negative cosmological evidence.

Producer: analysis/w33_20261109_s9_frozen_manifest_attack.py.

## Regression and claims boundaries

Seven current producers write seven corresponding frozen JSON certificates. The additional code corrects the older analytic Fisher producer, frozen JSON and published report, and includes an independent finite-difference test to prevent relapse.

Run in the repo root:

    py -3 -m unittest discover -s tests -p test_w33_20261109_seven_physics_fronts.py -q

The suite verifies exact W33 graph ranks/cycle matrix, pure-gauge equivalence, U1 cycle reconstruction, 40-mode state preparation, phase and loss induced optical leakage, independent analytic gradients, the oracle shot allocation constraints, Bell numerical crossings, and the DES frozen evidence gate. Claims are limited to the specified finite models and simulations, not a verified TOE.

## Top five independent next projects

1. **Build an 80-mode interference falsifier:** implement a routed 40-mode dark-frame preparation plus the full 80-mode point-line walk, with 81 measured Wilson phases, separately calibrated optical loss, and blinded measurements of the predicted t² null leakage.
2. **Make calibration nonasymptotic and model-robust:** jointly infer physical splitter, phase, loss, source preparation and detector effects with a valid finite-shot error certificate beneath 1.65e−4, while maintaining independent held-out model rejection.
3. **Derive real chiral gauge dynamics beyond the rank-25 obstruction:** construct a controlled continuum/gauge theory and anomaly-free fermions from a principled W33 background, not a tunable extra Wilson mass or assigned generations.
4. **Complete S9 with authenticated DES cosmology data:** score unchanged frozen conditions only when full matched unblinded shear vectors, covariance, z-distributions and patched scalar-field CLASS theory refits are available.
5. **Co-design event-ready single-photon Bell hardware:** maximize worst-case CHSH while tracking heralded source survival, detector efficiency, phase mode match, local oscillator photon costs, causal clock separation and all-trial statistics.
