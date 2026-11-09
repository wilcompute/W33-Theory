# W33/Q8 eight-MUB cosets as tight mixed-state Schmidt-number witnesses

**November 9, 2026.** Independent addendum to [Q8 design/purity](PASS20261109_Q8_DESIGN_PURITIES.md) and [five physical fronts](PASS20261109_FIVE_FRONTS_EXECUTED.md). Finite quantum-information theorem and calibrated ideal measurement protocol; **not a theory of everything, experimental observation, or claimed discovery of Schmidt witnesses in general**.

## 1. Exact new project-specific implication: purity is unnecessary to witness entanglement

Fix **any one** of the three normal-quaternion cosets in the 24 qutrit symplectic transformations. It supplies eight mutually unbiased nine-outcome orthonormal bases, each made of maximally entangled single-qutrit Clifford Choi rays. Let the probabilities for an *arbitrary* state rho on C^3 tensor C^3 be p[b,j], and define

    F8(rho) = sum_(b=1..8,j=1..9) (p[b,j] - 1/9)^2.

The previously proved unitary-2-design twirl yields the exact identity

    F8(rho) = tr(rho^2) + 1/9 - (tr(rho_A^2)+tr(rho_B^2))/3.

For a **pure** state with Schmidt coefficients sqrt(lambda_i), reduced purity is sum lambda_i^2 and

    F8(|psi>) = 10/9 - (2/3)*sum_i lambda_i^2.

If the Schmidt rank is at most k, Cauchy–Schwarz gives sum lambda_i^2 >= 1/k. Thus F8 <= 10/9 - 2/(3k).

Crucially, **F8 is convex** in the density matrix: every p[b,j] is linear in rho, and F8 is a sum of squares of affine real functionals. Therefore, every **mixed** state of Schmidt number <=k (convex mixtures of pure states of Schmidt rank <=k) obeys the **same sharp bound**:

    k=1: F8 <= 4/9   (violation certifies entanglement, with NO purity assumption).
    k=2: F8 <= 7/9   (violation certifies Schmidt number 3).
    k=3: F8 <= 8/9   (universal bound).

These bounds are tight: a pure uniform Schmidt-rank-k state attains equality. The tests reconstruct all three cosets and check 112 independent random mixed separable/Schmidt-number-2 preparations, all pure equality cases, and the original mixed-purity identity at machine precision. This proof is independent of hidden system dynamics. In a single photon carrying two internal qutrit degrees of freedom, the witness certifies tensor-degree-of-freedom entanglement, **not automatically spatial Bell nonlocality**.

### Isotropic noise benchmark

For rho_eta = eta |Phi_3><Phi_3| + (1-eta) I/9, F8 = (8/9)*eta^2. Thus the mixed entanglement witness fires only for eta > 1/sqrt(2) = 0.70710678; Schmidt number 3 is certified only for eta > sqrt(7/8) = 0.93541435. This is **much weaker** than an aligned |Phi_3> fidelity test: fidelity > 1/3 already certifies entanglement for eta>1/4, and fidelity > 2/3 certifies Schmidt number 3 for eta>5/8. The eight-basis benefit is a fixed *local-unitary invariant* statistic, not optimal noise sensitivity or minimum settings.

## 2. Equal mean, unequal noise: choose a coset by precision

The three Q8 cosets give precisely the same ideal F8 for *every* rho (their quadratic projective frame operators agree), but their higher outcome moments and estimator variances may differ. With M independent **shot pairs** in each basis, the observed proportion of matching outcome pairs is unbiased for c_b = sum_j p[b,j]^2. Set

    Fhat8 = sum_b (# matching pairs in basis b)/M - 8/9.

Its exact variance under IID ideal measurements is

    Var(Fhat8) = (1/M)*sum_b c_b*(1-c_b).

Take |Phi_3> = vec(I)/sqrt(3), aligned with one Clifford Choi ray. The three cosets have identical F8=8/9 but per-basis collision-probability profiles:

- aligned coset: one c_b=1 and seven c_b=1/9, giving **M*Var(Fhat8)=56/81**;
- each other coset: four c_b=1/3 and four c_b=1/9, giving **M*Var(Fhat8)=104/81**.

Thus the two nonaligned cosets have **13/7 = 1.857142857... times the variance** of the aligned coset, for equal shots. This suggests coarse reference calibration followed by selective allocation to the lower-variance coset. It does not change the exact mean or prove robustness against detector bias.

## 3. Exact frequentist false-positive control, plus a detection-power calculation

For each of eight bases, use M disjoint IID pairs of detected outcomes; let the paired collision indicators be Bernoulli. The one-sided distribution-free Hoeffding bound is

    Pr(Fhat8 - F8 >= epsilon) <= exp(-M*epsilon^2/4).

At significance alpha, the lower confidence bound is Fhat8 - sqrt(4 ln(1/alpha)/M). Certify Schmidt number >k only when this lower bound exceeds 10/9-2/(3k). This is valid **for mixed sources**, under ideal calibrated settings and IID sampling.

An exact reference-case **power** calculation (not just a confidence guarantee) uses the aligned maximally entangled Choi ray. Seven bases have uniformly distributed outcomes and the eighth is deterministic; consequently

    Fhat8 = 1/9 + Binomial(7M,1/9)/M.

At alpha=0.05, the smallest integer M found by evaluating this exact binomial survival function with >=95% detection power is:
- Schmidt number >1: **116 pairs per basis**, or **1,856 ideal accepted preparations** in all eight bases;
- Schmidt number >2: **1,882 pairs per basis**, or **30,112 ideal accepted preparations**.

These are **state-specific** power calculations for a perfectly aligned, maximally entangled target with no source drift, losses, dark counts, crosstalk or leakage. They are not universal experimental hardware budgets. Pairing is deliberately conservative; an all-pairs U-statistic can be more shot-efficient.

## 4. Fatal unless calibrated: fake positive even for a product state

The previous five-front pass exhibited a separable |00> state whose **same outcome-dependent detection efficiency in every basis**,
eta_j=0.63+0.045*j for j=0..8, generates an apparent positive pure-state entropy. Here the stronger mixed-state witness is attacked directly:

    F8_true(|00>) = 4/9 = 0.4444444444...
    F8_uncalibrated = 0.460137174211248...
    F8_after_ideal_efficiency_correction = 4/9 (floating precision).
    Cross-coset disagreement = 0.

Thus naive use of the **mixed-state entanglement witness** would falsely label a **product state** entangled even while all three cosets agree. Matched detector efficiencies cannot be inferred from coset agreement; independent per-setting/outcome calibration and uncertainty propagation are necessary. Conditioning on detected shots may open a detection loophole. None of these numerical exercises certifies an actual optical device.

## 5. Independent research and prior-art boundaries

Related methods are established: Gross, Audenaert, and Eisert, *Evenly distributed unitaries: on the structure of unitary designs* (2007), https://arxiv.org/abs/quant-ph/0611002 ; high-dimensional MUB Schmidt-number witnesses (npj Quantum Information, 2025), https://doi.org/10.1038/s41534-025-00990-6 ; purity-based random-correlation entanglement certification, https://www.nature.com/articles/s41534-020-0281-5 . The 72-unitary qutrit design also predates this work (see Q8 design/purity note). We make **no absolute novelty claim** about the general witness paradigm. This packet supplies a particular sharp quadratic inequality, a reproducible W33/Q8 family test, and a coset-dependent finite-shot variance calculation. It cannot establish physical TOE dynamics, spontaneous chirality, quantum gravity, or an empirical Standard Model prediction.

**Reproduce** from the repository root:

    py -3 analysis/w33_20261109_q8_schmidt_witness.py data/w33_20261109_q8_schmidt_witness.json
    py -3 -m unittest discover -s tests -p test_w33_20261109_q8_schmidt_witness.py -q

## Top five independent research continuations

1. Replace the nonconstructive convex proof with a **dual semidefinite/Schmidt-number relaxation** that improves isotropic visibility thresholds without losing reference invariance.
2. Optimize **adaptive basis allocation** using an initial low-shot pilot and a coverage-corrected final confidence test that avoids selection bias.
3. Construct **detector-efficient confidence regions** from bounded efficiency intervals rather than assuming exactly calibrated, postselected nine-outcome distributions.
4. Connect the 72 Clifford gates to a **physical 9-mode programmable Choi analyzer**, including unitary decompositions, leakage, feedforward and measurement-resource lower bounds.
5. Derive a real **continuum dynamical scaling limit** of the finite incidence gauge system; require Ward identities, Lorentz symmetry and anomaly-safe chiral fermions before relating any discrete witness to fundamental physics.
