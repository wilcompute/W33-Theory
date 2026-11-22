# Six operational Witting/W33 falsifiers: actual-channel capacity, loss-calibrated Schmidt number, three-plaquette gauge controls, triple-copy moments, detector confusion, and fake purity

**Date:** 2026-11-22. **Repo:** wilcompute/W33-Theory (master). This work follows the preceding five-front physical continuation. Six executable analyses, 22 new regression tests, and a dedicated GitHub Actions workflow are committed. None constitutes a discovery of new fundamental field equations, a physical photon experiment, fault tolerance, device independence or a Theory of Everything.

**New standalone sources**
- analysis/toe_20261122_native_capacity_input_witness.py
- analysis/toe_20261122_loss_calibrated_witting_schmidt_witness.py
- analysis/toe_20261122_three_plaquette_W33_gauge_null_control.py
- analysis/toe_20261122_witting_triple_collision_finite_shots.py
- analysis/toe_20261122_confusion_aware_Witting_detector_pareto.py
- analysis/toe_20261122_witting_loss_fakes_purity.py

Regression: tests/test_toe_20261122_physical_next5_plus.py (22 tests).
CI: .github/workflows/witting-20261122_next5_operational_falsifiers.yml.
Each producer emits a structured JSON certificate in data/ with the same basename. The underlying prior 40-ray ququart geometry and Gauss-constrained W33 squares are read from committed scripts rather than rebuilt from historical descriptions.

## I. The native routed Witting 4-to-9 channel has positive quantum capacity even at 30% output-rail dephasing

The immediately preceding output-rail dephasing study computed coherent information only for the maximally mixed input. Its zero crossing around lambda=0.22982 was strictly a **one-input witness boundary**, not a capacity threshold. We reconstructed the actual, committed five-Kraus Witting optical channel from its routed 45-row/40-ray 4D isometry, the nine retained rails and the five-dimensional environment. Each K_j has shape 9-by-4, and sum K_j†K_j=I4.

Set N_lambda=(1-lambda)N+lambda(Delta_rail applied to N), where Delta_rail removes all nine-rail offdiagonals. For a ququart input rho with purification, compute one-use coherent information I_c(rho,N_lambda)=S(N_lambda(rho))-S[(id_4 tensor N_lambda)(|psi_rho><psi_rho|)]. The calculation uses the full 36-by-36 reference/output density matrix, not a ratio proxy.

Numerical optimization over valid density matrices exposed a better **rank-two** input. A simple fixed two-column 4-by-2 complex factor W, stored to nine decimals in the committed source and result certificate, defines rho=W W†/Tr(W W†), with eigenvalues ~0.31546,0.68454 and two zero eigenvalues. Rerunning the native Kraus calculation with this *fixed input* gives:

| Output-rail dephasing | Maximally mixed I_c | Fixed rank-two witness I_c |
|---:|---:|---:|
| 20% | +0.106319 | positive, stronger than max mixed |
| 23% | -0.000620 | positive |
| 25% | -0.068905 | positive |
| 27% | -0.134964 | positive |
| 30% | **-0.230149** | **+0.007891** |
| 30.5% | negative | **+0.000676** |

Since coherent information is an achievable asymptotic quantum-capacity lower bound, **Q(N_0.30)>0** follows for the exact specified mathematical channel and this explicit input. We also get a positive fixed-witness point at 30.5%. This improves a previous *certified positive witness range*, **not** the actual unknown capacity boundary. We have not globally optimized the input, decoded an error-correcting scheme, modeled all photonic noise, or proved capacity vanishes at any intermediate lambda. At full output dephasing lambda=1 the channel is entanglement-breaking and Q=0.

This is the most important correction in the pass: a negative I_c on the maximally mixed input cannot justify declaring a photonic channel quantum-capacity zero. Native encoded input choice matters.

## II. The 150-rotation Witting interferometer still certifies entanglement with correctly calibrated state-dependent loss

The previous Naimark compiler builds a 40-by-4 isometry realizing the complete trusted Witting POVM. It uses 150 active two-mode operations. An idealized loss model attenuates **only the two rails touched by each operation** by sqrt(1-ell), so survival depends on input state. In particular this cannot be accounted for by simply multiplying all POVM outcomes by one detector efficiency.

Let W_ell be the resulting lossy 40-by-4 optical transfer, M_i=|W_ell[i]><W_ell[i]| the positive ququart effects, and S_ell=sum_i M_i tensor conjugate(M_i) the two-ququart effect for matching Alice/Bob ray labels. The exact probability on the ideal maximally entangled target is p_Phi=<Phi4|S_ell|Phi4>.

For **every separable two-ququart density matrix rho**, its partial transpose rho^Gamma remains a positive trace-one operator, hence

Tr(rho S_ell)=Tr(rho^Gamma S_ell^Gamma) <= lambda_max(S_ell^Gamma).

This is a rigorous state-independent separable **upper bound** for the particular known instrument, even when the losses are state dependent. It is not claimed tight or experimentally calibrated.

| Active two-mode element power loss | Target p_same | PPT separable upper bound | Gap |
|---:|---:|---:|---:|
| 0% | 0.100000 | 0.040000 | 0.060000 |
| 1% | 0.066089 | 0.031645 | 0.034444 |
| 2% | 0.045822 | 0.025671 | 0.020151 |
| 3% | 0.033244 | 0.021304 | 0.011940 |
| 5% | 0.019651 | 0.015602 | 0.004049 |

At 3% or 5% optical power loss per gate, the true entangled target's same-label coincidence falls below the LOSSLESS 4% entanglement threshold, yet the CALIBRATED separable bound falls even more. This is a direct practical reason to certify the actual implemented effects rather than reuse ideal inequalities.

If the calibrated effects are treated as exact and launched pairs as iid, one-sided 5sigma exact binomial tail alpha=2.8665e-7 with at least 90% power can be achieved with sufficient pair launches of approximately N=642 (0% loss), 1429 (1%), **3130 (2%)**, 6998 (3%), or 40831 (5%). These are constructive points, not globally optimal sample sizes because discrete binomial cutoffs can create nonmonotone N acceptance. Real detector uncertainty, crosstalk, multiphoton backgrounds, incomplete calibration, drifts and adversarial source errors are excluded. Experimental high-dimensional entanglement certification is known to be vulnerable to underestimated measurement errors; see 2026 work https://arxiv.org/abs/2606.20396 and multi-mode photonic experimental calibration https://www.nature.com/articles/s41534-026-01183-5.

## III. A three-plaquette, 1024-state Gauss-exact patch—and a no-go for claiming it is W33-specific

The previous two-plaquette study covered six matter sites, seven dynamical links and a 128-dimensional physical Gauss sector. This pass selects **three W33 4-cycles** all sharing edge 0—36:

(0,36,9,37), (0,36,3,6), (0,36,12,1).

They form eight sites, ten unique edges and three independent graph cycles. With one matter spin at each site and one Z2 gauge spin at each edge, the kinematic space is 2^18=262144 dimensional. The eight local Gauss laws G_v=(-1)^n_v product_(incident links) X_e=+1 reduce it to **2^10=1024 physical states**. Enumerating them in the electric X basis makes site charge equal to incident negative-link parity and implies total matter parity even.

The producer verifies that flipping an edge X bit toggles precisely its two endpoint matter occupations, preserving all Gauss constraints. Each Wilson plaquette W_p is the product of four magnetic Z_e operators, and its anticommutation with electric X_e occurs if and only if link e lies on that plaquette (30 explicit link/plaquette checks).

A finite sparse Hamiltonian includes gauge-invariant matter-pair/hopping terms, electric field energies, plaquette flux flips and a matter mass. At couplings J=.35, h=.7, B=.3, m=.6 and starting from the zero-electric-flux vacuum, mean dynamical matter counts at times t=.5,1,2 are approximately **0.500620, 1.145240, 0.784281**. This is a true finite, Gauss-constrained quantum state, but not a claim of observed particle creation in nature, non-Abelian gauge dynamics or thermodynamic confinement.

**Essential independent negative control:** all these Hamiltonian terms depend only on the abstract eight-site, ten-edge patch and its chosen face cycles. Relabel the vertices and edges to an otherwise unrelated graph-isomorphic finite device; the matrix dynamics and all local observables remain unitarily equivalent. Thus a small-patch gauge phenomenon on W33 is **not by itself a signature distinguishing W33 from unrelated geometries**. A W33-specific claim requires a global embedding-sensitive invariant, constrained automorphism, or higher-order geometry to affect a measurable prediction. This is consistent with modern 2026 dynamical Z2 gauge experiments, which characterize actual Hamiltonians and flux operators rather than deducing cosmology from a graph: https://www.nature.com/articles/s41567-026-03422-0 and https://www.nature.com/articles/s41567-026-03400-6.

## IV. Third-moment collision experiments need surprisingly many independently prepared photons

The known Witting 40-ray projective 3-design gives, with full ideal calibrated 40-outcome POVM on independent identical ququart copies, pair and triple same-label collision probabilities

C2=(1+Tr(rho^2))/50,
C3=(1+3Tr(rho^2)+2Tr(rho^3))/3000.

For any pure ququart input C2=.04 and C3=.002 irrespective of the input. We verified three explicit pure states, one Witting ray, one ray from a **different complete five-MUB ququart design**, and an independent generic superposition.

The 20-ray five-MUB POVM is a 2-design but **not** a 3-design. It produces pair collisions .08 for every pure input; its triple collisions depend on the input. For the test inputs, the same five-MUB detector yields C3=**7/900≈0.0077778** when fed one chosen Witting ray, and **0.010000** when fed a ray from its own basis. These exact differences give an experimentally falsifiable contrast to Witting 3-design uniformity.

Under iid, stable, ideally resolved MUB measurements, an exact one-sided binomial test with 5sigma null size and at least 90% power distinguishing the two specified triple probabilities can be achieved with **68,886 independent triplets**, consuming **206,658 individually prepared ququarts**, not 68,886 single photons. To estimate Tr(rho^3) by the Witting triple probability alone, even if purity were known exactly, the standard deviation of this moment estimator for a pure state is roughly **0.1 after 450,000 independent triplets**, or 1.35 million independent ququart preparations. Joint purity-estimation error must be added in realistic designs.

These are unusually high photon resources for a seemingly simple 3-design identity. The result is a meaningful project-level resource falsifier; the 3-design itself is prior mathematical knowledge, not a new universal law.

## V. The improved compressed POVM maintains its advantage under *known symmetric wrong-label noise*

For each of the same full40, older25, privacy/Fisher25 and newly optimized variance25 detectors, simulate a calibrated random-label confusion before pooling: with probability 1-epsilon retain the true ray label, and with probability epsilon replace it with a fresh uniform draw from 40 rays. The effective local POVM is transformed by a known stochastic 40-by-40 confusion matrix, and both parties have independent instances. The full two-party outcome distribution is transformed by the same matrices, and the original maximally-entangled fidelity is reconstructed with an explicit Moore–Penrose dual.

All four layouts remain locally informationally complete at epsilon<1. On the ideal maximally entangled state, the unbiased per-event fidelity-score standard deviations are:

| Known uniform random-label replacement epsilon | Full40 | Old25 | Privacy/Fisher25 | New variance25 |
|---:|---:|---:|---:|---:|
| 0% | 1.250 | 7.708 | 5.128 | **4.710** |
| 5% | 1.415 | 8.340 | 5.552 | **5.093** |
| 15% | 1.811 | 9.934 | 6.617 | **6.056** |
| 30% | 2.686 | 13.656 | 9.095 | **8.290** |

The newly selected 24-ray layout stays ahead of the older compressed candidates in *this calibrated symmetric confusion model*, but its worst-case unknown gain-drift amplification was worse in the prior work. It is not globally dominant. Known stochastic crosstalk can be mathematically inverted at a variance cost; **unknown asymmetric drift cannot be canceled by applying the wrong inverse**. These are ideal target-state estimator variances and do not include finite-sample bias from estimating the confusion matrix.

## VI. Bonus falsifier: optical path-dependent loss can fake an unphysical ququart purity

The Witting 3-design collision relations are only valid for the ideal complete Witting POVM. If instead we use the lossy 150-rotation interferometer and normalize its detected-output distribution, different **pure** input rays yield different conditional collision values.

At 1% per-active-element power loss:

| Input ray (all pure) | Ideal C3 | Conditional lossy C3 |
|---:|---:|---:|
| 0 | .002000 | **.002738** |
| 5 | .002000 | .002466 |
| 39 | .002000 | **.001670** |

Ray0 produces C2≈.043585 and the **incorrect** ideal purity inversion Tr(rho^2)=50C2−1 gives ≈1.179, which is physically impossible. Ray39 gives an inferred purity below .93, suggesting a pure state has become mixed when in fact only its detection statistics were distorted.

As a negative control, uniform common attenuation of all 40 outcome amplitudes preserves the *conditional* Witting collision identities. The failure occurs because the actual network attenuates different optical paths differently. These counterexamples must inform any proposed experimental 3-design measurement: calibration of the implemented POVM is part of the hypothesis.

## Verification, reproducibility and scope

Five requested independent research threads and this sixth negative control were numerically investigated with the prior committed Witting geometry. The source files listed above, a dedicated test suite (22 tests) and isolated CI workflow were pushed to master. Analytic expressions were checked independently in the current sandbox, including 4-to-9 coherent information, actual optical Givens loss, binomial tails, three-face 1024D Gauss dynamics, 3-copy collision controls and calibrated confusion variances. The GitHub Actions jobs were queued during writing, so the repository-side tests are **not** claimed to have passed CI until runners finish. All work is scoped to mathematical models and idealized hardware; no experimental observation or universal TOE is asserted.

## Five orthogonal next investigations

1. **Physical-device witness calibration:** build independent high-confidence bounded-error intervals for all 40 implemented POVM effects, and replace nominal PPT thresholds by rigorous worst-case intervals with no-click events.
2. **Large W33 versus isomorphic controls:** seek observables requiring *global* W33 incidence or cohomology; a three-square Z2 Hamiltonian that only sees an abstract graph cannot distinguish the Theory of Everything hypotheses.
3. **Low-cost purity estimator:** compare calibrated pair/triple collisions against Pauli classical shadows and randomized measurements under equal photon preparation and detector budgets.
4. **Native channel capacity beyond one use:** explore actual 4-to-9 channel code inputs and coherent-information additivity/superadditivity; explicitly document environmental and rail-mode access.
5. **Coupled experiment design optimization:** choose full40 versus 25-bin readout based on task (Schmidt number, purity, channel calibration or private chart estimation) with explicit unknown confusion, drift and hardware costs.

**Bottom line:** A reproducible finite geometric architecture is only physically persuasive when its predictions survive independent noise models, graph-isomorphic controls, a valid sampling model and the operational distinction between quantum capacity and finite-dimensional entanglement.


## VII. Calibration operator-norm tolerance from the entanglement-witness margin

The lossy measurement effects M_i must actually be known, not only assumed from an ideal Givens compiler. Suppose each of Alice and Bob's nominal positive Hermitian effects has a calibrated unknown perturbation of operator norm at most epsilon. If each party is bounded the same way, the corresponding same-label operator's deviation is bounded in norm by

||S_actual-S_nominal|| <= 2 epsilon sum_i ||M_i|| + 40 epsilon²,

where ||M_i|| is the ququart effect's largest eigenvalue. For any state, the associated probability changes by at most that norm bound. In particular the true separable upper bound could move up, and the true target probability could move down, by at most one such bound each. A sufficient robustness criterion is thus

2[2 epsilon sum_i ||M_i|| + 40 epsilon²] < nominal entanglement witness gap.

The strict positive root gives a sufficient **absolute per-effect operator-norm calibration tolerance**. At 2% optical power loss per active element, the nominal same-label gap is ≈0.02015078, the trace of all known lossy effects is ≈2.63860973, and epsilon must be less than approximately **0.00188236556836**. Since an ideal Witting effect has norm0.1, this is about1.88% of its effect norm, but it is **not** 0.188% relative error; this is an absolute operator-norm tolerance.

The bound is conservative, treats individual errors as potentially worst-aligned, does not use constraints enforcing complete POVM plus no-click and does not model the experimental procedure for *establishing* those effect-norm bounds. Its value is providing an explicit calibration target rather than an unquantified warning. The source producer and dedicated test suite now calculate and regress this tolerance.
