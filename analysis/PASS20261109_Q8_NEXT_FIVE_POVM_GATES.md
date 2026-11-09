# W33/Q8 next five: optimized minimal tomography, finite-shot CCNR, optical-loss falsifier and correction, boundary index, DES Y6 data gate

**November 9, 2026.** These are reproducible finite-dimensional quantum-information calculations and explicit *negative* physics tests, not new particles, an experimentally realized photon device, or a theory of everything. All calculations were performed using the GitHub W33-Theory repo and its authorized synced Windows machine, and checked against parallel commits.

## Front 1 — Minimum ten-setting tomography substantially improved

Eight W33/Q8 maximally entangled MUB measurement contexts span 64 nonlocal qutrit correlations but have zero sensitivity to 16 local Bloch parameters. A full two-qutrit density operator has 80 traceless real parameters; a nine-outcome projective setting provides at most eight independent probabilities. Consequently ten projective settings is the information-theoretic minimum. The previously published 8+2 configuration has condition number 29.4689423.

A deterministic 1,600-candidate random complex Givens coordinate search, holding all eight Bell contexts fixed and changing the two extra generic nine-mode unitaries, accepted 186 improvements. It achieved 90×80 rank 80, condition number **9.3591265**, 68.24% better than the previous ten-setting configuration. All 60 random mixed/pure density reconstructions pass with maximum error **1.27e-15**. The reproducible seed is 20261109228; the saved JSON includes a SHA256 of the two generated bases. The twelve-setting four-product-MUB alternative still has the better condition sqrt(2), and no global optimum is claimed. The extra bases are not mutually unbiased and therefore do not contradict the eight-MUB strong-unextendibility theorem.

Program: analysis/w33_20261109_q8_ten_context_optimize.py
Result: data/w33_20261109_q8_ten_context_optimize.json

## Front 2 — Finite-shot, loss-aware realignment bound (and severe resource warning)

Full tomography enables the previously known computable cross-norm/realignment (CCNR) test, which detects the standard Horodecki PPT-entangled family, 0<a<1. This criterion and its application to that family are prior art: Chen and Wu, Quantum Information and Computation 3 (2003), doi:10.26421/QIC3.3-1; the W33/Q8 contribution is the concrete setting architecture.

A unit-norm realignment dual matrix gives a linear witness of ideal probabilities p. For each of K in {10,11,12} contexts, measured conditional click probabilities q are related to ideal p by unknown outcome efficiencies eta_j in independently trusted intervals: eta_j=0.63+0.045j, relative uncertainty ±0.1%. A future finite sample of N *accepted independent trials per context* admits a 95% simultaneous Hoeffding radius epsilon=sqrt(log(2*9K/0.05)/(2N)). Independent 19-variable linear programs per basis minimize the dual witness over ideal p, unnormalized detected v, and the unknown survival factor s. These deliver a conservative lower bound on the CCNR norm **conditional on the efficiency model and simultaneous confidence event**.

Only exact expected frequencies q were input, rather than sampled experimental data. For the Horodecki case a=0.236, true norm=1.0030587941, the first accepted-shot grid value where the synthetic LP bound crosses 1 is **10^10 per basis** for original ten, refined ten, and eleven contexts; **10^9 per basis** for the twelve-product-basis design. For a=0.5 the true margin is 0.0023272047, and the first tested success is 10^10 per basis even for the twelve-context design. These are not achieved experimental detection probabilities: they show that this conservative witness and concentration bound are highly resource-intensive. Detector crosstalk and internal chip loss are *not* covered by the simple output-efficiency model.

Program: analysis/w33_20261109_q8_ccnr_shot_calibration.py
Result: data/w33_20261109_q8_ccnr_shot_calibration.json

## Front 3 — Internal optical losses cause alarming false positives

Two generic nine-mode analyzers each decompose into 36 adjacent Givens two-mode rotations. In the explicit QR mesh, some rails participate in 15 interactions. Instead of approximating all optical loss by one outcome-dependent post-detection efficiency, we inserted sqrt(t) field attenuation into both rails after every two-mode mixing gate. The first eight Bell contexts were held ideal to isolate the two generic analyzers. Optional independent interstage phase errors were added.

Naively applying the ideal ten-context inverse to the resulting postselected probabilities wrongly classifies **all 12 generated pure separable product controls as CCNR-entangled** in every lossy test. The largest false CCNR norm in the t=0.999, 0.995, 0.990 no-phase controls is **1.006224, 1.031304, 1.063061**, respectively, against a separable upper bound of 1. Baseline t=1 gave zero false positives. This is a synthetic counterexample to an uncalibrated readout and not an observed laboratory false-positive rate. The effect is physical in the model because internal noncommuting gate losses modify the full measurement POVM, not just terminal detector efficiencies.

Program: analysis/w33_20261109_q8_optical_loss_povm.py
Result: data/w33_20261109_q8_optical_loss_povm.json

### Extra breakthrough — Calibrated complete POVMs correct the false positives even without known source brightness

For each setting b and nine detector ports j, let calibrated K_b include all known internal losses and phase shifts, E_bj=K_b†|j><j|K_b, and q_bj=tr(rho E_bj)/s_b be observed conditional click frequencies. The ten survival factors s_b are initially unknown. Expand rho=I9/9 + sum_(k=1..80) theta_k H_k in an orthonormal traceless operator basis. Then

    [A_effects | -Q(q)] [theta ; s] = -b_effects,

where A_bjk=tr(E_bj H_k), b_bj=tr(E_bj)/9, and Q(q) has one column per measured nine-outcome conditional vector. It is a **90×90 linear system**: 80 unknown state parameters plus 10 survival factors. In all five simulated loss/phase scenarios the system has full rank; it recovers 12 separable products, an interior Horodecki PPT-entangled state, and the maximally mixed state with maximum density-matrix error below **1.8e-15**. It restores zero false CCNR positives despite the internal noncommuting attenuation. It does not require independent calibration of absolute source brightness, but absolutely **does require trusted full complex-valued POVM calibration** and a model for drift. No finite-shot confidence or uncertainty in K_b has yet been certified.

Program: analysis/w33_20261109_q8_full_povm_selfnormalize.py
Result: data/w33_20261109_q8_full_povm_selfnormalize.json

Relevant nonidentical engineering prior art: nine-input self-configuring silicon photonic mode separation, Nature Photonics (2026), https://www.nature.com/articles/s41566-026-02035-6 ; standard tunable interferometer mesh, Clements et al., Optica 3, 1460 (2016), https://doi.org/10.1364/OPTICA.3.001460 .

## Front 4 — The closed W33 graph does not provide an intrinsic chiral index

The native 40×40 point-line incidence operator has exact rational rank 25. Its naive bipartite Dirac grading has 15 plus zero modes and 15 minus zero modes: **index zero**. Removing **any one** of the 40 points produces a 39×40 incidence matrix of exact rank 25, and a net index (39−25)−(40−25)=**−1**. Under eight independent random complex edge phases the closed matrix becomes full rank 40; the rectangular boundary matrix becomes full rank 39 with its one required minus null mode intact. Vertex gauge rephasing preserves singular values.

This apparent gauge-robust chiral index is **forced by imposing a sublattice-imbalanced boundary**, not predicted by the original closed W33 graph. This falsifies any identification of the naive W33 zero modes alone with physical, protected, anomaly-free Standard Model Weyl fermions. A genuine 3+1D dynamical chiral theory requires a local gauge-invariant regulator, continuum scaling, absence of unwanted mirrors and anomaly consistency. Existing alternatives include domain-wall/overlap lattice fermions: https://doi.org/10.1103/PhysRevD.65.074504 ; https://doi.org/10.1103/PhysRevLett.132.141603 .

We separately inserted the known five left-handed Standard Model multiplets and hypercharges by hand and verified **exactly with rational arithmetic**: SU(3)^2 U(1), SU(2)^2 U(1), U(1)^3 and gravitational-U(1) anomaly sums all vanish; there are four SU(2) doublets, meeting the even-doublet Witten global-anomaly requirement. The code does **not** derive the hypercharges, gauge groups or fermion content from W33.

Program: analysis/w33_20261109_boundary_chirality_anomalies.py
Result: data/w33_20261109_boundary_chirality_anomalies.json

## Front 5 — DES Y6 public-data/FITS gate, S9 still **unscored**

DES lists public Y6 cosmology papers and specifies that **some data products are released, with more coming**: https://www.darkenergysurvey.org/des-y6-cosmology-results-papers/ . A formerly indexed 2025-07-28 unblinded 3×2pt FITS and associated NCSA directory/notebook returned HTTP 404 in our last direct audit. The public Y6 LambdaCDM conditional S8=0.789±0.012 cannot substitute for the held-out cosmological shear data vector and corrected-model likelihood preregistered by the project on 2026-11-08.

A new Astropy FITS contract verifies extensions XIP, XIM, COVMAT and NZ_SOURCE, required data-vector columns and angular units, covariance dimensions/symmetry/positive definiteness, explicit unblinding, and frozen strict scale cuts xi+>10 arcmin, xi−>60 arcmin. A **clearly synthetic** eight-row toy FITS passes its schema (six retained rows); three deliberately invalid cases are blocked: missing unblinding, negative covariance eigenvalue, and misuse of a synthetic fixture as genuine data. No actual DES xi± vector was acquired and the fixed CPL-vs-fading CLASS/Halofit nuisance-refit test has **NOT** been scored. A schema pass does not prove official provenance, blinding status or scientific consistency of the covariances; actual archival data need a verified source and exact release metadata.

Program: analysis/w33_20261109_des_y6_s9_fits_contract.py
Result: data/w33_20261109_des_y6_s9_fits_contract.json

## Regression and scope

A dedicated test suite freezes deterministic JSON results and reruns key structural identities. The exact tests include the optimized measurement-frame SHA256, full 80-parameter rank, the finite-shot CCNR model's prospective bound, 12-product false positives before correction, 12-product zero false positives after full-POVM correction, exact boundary index and Standard Model anomaly-rational controls, and DES FITS negative controls.

    py -3 -m unittest discover -s tests -p test_w33_20261109_q8_five_more_continuation.py -q

**Nine tests passed** on the authorized Windows research machine. No claim here is an empirical observation of a new particle, a deployed chip, a cosmological preference, or a completed TOE.

## Five independent future tests

1. Build **finite-shot CCNR confidence regions under uncertainty in the complete full-POVM calibration matrices** rather than only final detector efficiencies.
2. Optimize **physically structured, shallow non-Bell measurement bases** using specific time-bin/path/OAM resources and real phase-switching/loss budgets.
3. Find a **gauge-covariant, anomaly-free, nonzero-index local overlap/domain-wall extension** in which chirality and continuum dimensionality are derived rather than imposed by deleting a vertex.
4. Acquire the **official full DES Y6 cosmic-shear FITS data vector and matched covariance** and rerun unchanged S9 with corrected CLASS/Halofit and consistent nuisance refits.
5. Test **photonic factorization versus spatial Bell nonlocality** with explicit independent-party causal and detection-loophole assumptions, avoiding a false inference from two qutrit encodings inside one photon.
