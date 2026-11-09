# W33/Q8 Advanced Falsifiers — five independent fronts and two additional operational tests

**2026-11-09 | evidence tier: finite exact algebra, independent seeded numerical controls, prospective confidence bounds, and live HTTP endpoint audit.** This document extends PASS20261109_Q8_NEXT_FIVE_POVM_GATES.md. No physical quantum instrument, Bell test, dark-energy data analysis or theory of everything has been demonstrated. Claims below deliberately distinguish original repo-local implementations from established quantum-information theory.

## Executive findings

1. Full-POVM-calibration uncertainty can be bounded with a **data-adaptive linear CCNR dual certificate**, rather than requiring exact optical calibration, known brightness or a pure source. A finite-sample multinomial control passed prospectively under strict stated assumptions.
2. A shallow analyzer with only one controlled-phase diagonal after each local qutrit tensor product is **insufficient in 950 seeded pairs** (combined measurement rank 76/80). Two controlled-phase layers interleaved with four local three-mode transforms gave **rank 80/80 in 950 other seeded pairs**. The best had condition number 25.020259 and reconstructed 40 random mixed/pure density matrices at max error 1.49e-15.
3. W33 admits gauge-covariant **externally supplied** one-dimensional chiral extensions with exact AIII winding indices 0,15,24,39,40. Since the same native W33 geometry permits all these by tuning external m,t,lambda, it does not determine Standard Model chirality or even a unique 1D index.
4. A single photon's internal path/polarization Hilbert-space factorization can algebraically yield CHSH 2sqrt(2) with all measurements in one lab, but this is **not a spacelike Bell demonstration**. A spatial single photon shared in two Fock modes with only number-commuting local observables has accessible CHSH at most 2 until local phase reference and non-number-commuting measurement resources are supplied.
5. The publicly indexed DES Y6 3x2pt unblinded FITS link still returns HTTP 404 in a direct authorized-machine GET. Official survey papers and the release portal return HTTP 200 but do not supply a validated complete data vector/covariance via that path. Frozen S9 remains UNSCORED.

## 1. General full-POVM effect uncertainty theorem

Let rho be any positive trace-one two-qutrit state, with expansion rho=I9/9 + sum_(k=1..80) theta_k H_k in a Hilbert–Schmidt orthonormal traceless Hermitian basis. In setting b each physical effect is E_bj=K_b†|j><j|K_b and the observed accepted-click conditional probability is q_bj=Tr(rho E_bj)/s_b, with unknown but physical survival 0<s_b<=1.

Suppose the calibrated effects Ehat_bj obey a **verified operator-norm bound** ||Ehat_bj-E_bj||op<=delta, and the estimated conditional frequencies qhat_bj satisfy simultaneous |qhat_bj-q_bj|<=epsilon. The latter event has at least 1-alpha coverage for independent accepted multinomial trials with N accepted observations per setting when

    epsilon = sqrt( log( 2*(9K)/alpha ) / (2N) ).

Build the observed linear tomography system Mhat=[Ahat,-Q(qhat)], with Ahat_bjk=Tr(Ehat_bj H_k), Q one column per context containing its nine measured qhat values, and inhomogeneous b_bj=Tr(Ehat_bj)/9. If Mhat is invertible, define xhat=Mhat^-1(-b) and let rhohat be its first 80 coordinates' density reconstruction. For ANY matrix W with ||W||op<=1 (including a W selected adaptively as the unitary polar factor of realign(rhohat)), define h_k=Re Tr(W† realign(H_k)). Let

    y = Mhat^-T [h_1,...,h_80, 0,...,0]^T.

The true physical vector x=(theta,s) satisfies the residual **row-by-row** bound

    ||Mhat x + b||infinity <= delta+epsilon,

because each residual equals Tr[(Ehat-E)rho]+(q-qhat)s, and rho>=0, Tr rho=1, 0<=s<=1. Nuclear norm duality and this residual give the **pointwise valid certificate**

    ||realign(rho)||nuclear >= Re Tr(W†realign(rhohat))
                            - (delta+epsilon)*||y||1.

This is valid even when W was selected from observed data, because the operator-norm inequality is pointwise for every W and the simultaneous event protects all frequencies. No brightness or pure-state prior is required. It does rely on trusted calibration errors **for every full POVM effect**, IID accepted detection samples, accurate matrix inversion, and a stationary source. It does **not** automatically handle device-independent adversarial detection, preparation drift, or unbounded crosstalk.

If each actual analyzer K differs in operator norm by at most kappa from its calibrated Khat, then a conservative effect bound is delta=2*kappa+kappa^2 for contractions. The verifier creates perturbed Kactual=Khat exp(i kappa H), and independently checks each of the 90 effect norms against this bound.

For the standard Horodecki state with a=0.236, true CCNR norm approximately 1.003058794, the tested optimized ten-setting calibrated witness has ||y||1 approximately 18.5574. At synthetic exact expected frequencies, the first tested successful accepted-event grid value is **N=10^10 per basis** even with tested kappa values 0, 1e-7, 1e-6 and 1e-5. One explicitly sampled seeded **multinomial** realization at N=10^11 per basis also obeyed its simultaneous Hoeffding interval and gave a valid bound above 1. A separable pure product and the maximally mixed state were checked as negative controls: no falsely positive certificate at any tested calibration/shot setting. These resource figures are **not measured hardware event counts** or a general sample-complexity optimum; they are large and hard to realize.

Code: analysis/w33_20261109_full_povm_calibration_bound.py
Frozen output: data/w33_20261109_full_povm_calibration_bound.json

## 2. Controlled-phase depth versus informational completeness

The eight Q8 Bell contexts provide exactly 64 nonlocal two-qutrit correlation directions, with 16 missing local directions. A local product projective basis U3 tensor V3 contributes at most two diagonal traceless marginal directions per subsystem, or four total; consequently **two purely local added bases can contribute at most 8** of the missing 16 (and 20 seeded controls confirmed combined rank <=72).

A natural physical construction uses a diagonal phase mask

    CZ = diag(omega^(a*b)), omega=exp(2pi i/3),  a,b in {0,1,2}.

The shallow one-mask family CZ (A tensor B), A,B in U(3), yielded combined **rank 76, not 80, in every one of 950 seeded independent base pairs**. The tested rank deficiency is a serious limitation and should not be silently replaced by full-rank generic Haar assumptions. Its failure is a numerical claim over a specified family and seed, not a formal universal impossibility theorem for every degenerate parameter choice.

Instead, the two-mask family

    U = CZ (A tensor B) CZ (C tensor D)

reached full rank **80/80 in all 950 seeded independent pairs**. The best pair had condition number **25.020259**, mean reduced linear entropies 0.4483 and 0.3014 in its two analyzer bases, and reconstructed 40 random ranks 1,2,3,5,9 density operators to max error **1.49e-15**. There are four local U3 transforms and two nine-mode diagonal masks per extra analyzer. A local U3 in each three-rail block has at most three two-mode Givens; with three spectator settings, each U3 tensor U3 stage costs at most 18 operations. Thus each two-mask extra analyzer costs an upper 36 two-mode local rotations plus 18 programmed mode-dependent phases. Compared to the arbitrary 36-Givens all-nine-mode mesh, **the principal advantage is architectural factorization and local parallelizability, not a proven reduction in the total coupler count**. The previous generic optimized ten-setting design still had better conditioning 9.3591265; the twelve-setting product-MUB design was better again at sqrt(2).

Here CZ is a **linear, passive phase operation on the two internal qutrit addresses of ONE nine-mode photon**. It is not an entangling physical interaction between two remotely separated photons. No fabricated chip, measured loss budget, or causal Bell test is claimed.

Code: analysis/w33_20261109_shallow_cz_complete.py
Frozen output: data/w33_20261109_shallow_cz_complete.json

## 3. Spectral winding on a W33-equivariant external dimension: a positive model and a no-go for uniqueness

Let B be the native 40x40 integer incidence matrix, W33 points versus lines, and define C=B B^T/16. The exactly established point spectrum is

    spec(C) = {0 with multiplicity 15, 3/8 with multiplicity 24, 1 with multiplicity 1}.

We **add** a periodic one-dimensional Bloch coordinate k and a chiral AIII off-diagonal block

    Q(k) = m*I40 + lambda*C + t*exp(i*k)*I40,
    H(k) = [[0,Q(k)],[Q(k)†,0]], Gamma=diag(I40,-I40).

This does not insert 3+1D spacetime, gravitational geometry, or continuum Standard Model fermions. It is an explicit *external 1D hopping construction* with an internal W33 point-operator. The chiral winding of det Q equals the number of eigenvalues of (m*I+lambda*C) inside the circle of radius t. Using **exact rational comparisons** gives selectable indices:

| m | t | lambda | Exact winding |
|---|---|---|---:|
| 3/2 | 2/5 | 1 | 0 |
| 3/10 | 2/5 | 1 | 15 |
| -2/5 | 1/5 | 1 | 24 |
| 1/20 | 1/2 | 1 | 39 |
| 0 | 7/5 | 1 | 40 |

Independent numerical 8,192-step phase windings agreed in all five cases. The minimum gap is the rational min over s in {0,3/8,1} of ||m+lambda*s|-t|; norm-bounded perturbations smaller than that gap cannot close it, so the winding is homotopy stable. Point-gauge transformations B->U_points B U_lines† give C->U_points C U_points† and preserve the spectrum (tested error below 5e-16).

**The striking counterexample** is that one finite geometric input gives five distinct protected indices depending solely on external hopping coefficients. This rules out a claim that the native closed W33 incidence geometry by itself uniquely selects the new 1D chiral invariant. These one-dimensional AIII windings are not unpaired 3+1D Weyl fermions, nor anomaly cancellation.

Code: analysis/w33_20261109_chiral_spectral_winding.py
Frozen output: data/w33_20261109_chiral_spectral_winding.json

## 4. Operational single-photon nonlocality: source factorization is not remote locality

A single photon can encode two logical factors (for example path and polarization) in its **internal** 4D state space, and an internal |Phi+> state produces the algebraic CHSH expectation 2sqrt(2) if the corresponding factor observables are implemented. That is an entanglement/contextuality-style demonstration within one device, **not alone a Bell test between causally isolated laboratories**.

For a different physical resource, let a single photon be split between separate observer Fock spaces in the state (|1>_A|0>_B+|0>_A|1>_B)/sqrt(2). Without a shared local phase reference, restrict each local observable to commute with its local photon-number operator. Local U(1)xU(1) twirling makes all accessible statistics identical to the separable mixture (|10><10|+|01><01|)/2. Exhaustive enumeration of 4^4 dichotomic number-diagonal measurement-setting choices yields maximum accessible CHSH=2. If local phase-coherent non-number-commuting operations are *physically supplied* and parties separated, the same ideal two-qubit state admits CHSH=2sqrt(2). Demonstrating this under causal independence and without unfair postselection requires an actual Bell experiment with separately trusted resources.

For the very specific model of a maximally entangled state, equal independent per-party detection efficiency eta, zero one-party marginals, and assigning outcome +1 to no-click events, the measured CHSH is

    S(eta) = 2sqrt(2)*eta^2 + 2(1-eta)^2.

The threshold for S>2 is eta>2/(1+sqrt(2)) = 0.8284271. This is **not a universal detection-efficiency threshold**; different states and outcome strategies yield other results. The code tests 0.8 (fails), 0.85 (passes), and exact threshold.

Relevant prior work: Brask, Chaves, Brunner 2013, Phys Rev A 88 012111, https://doi.org/10.1103/PhysRevA.88.012111 ; Hessmo et al. 2004, Phys Rev Lett 92 180401, https://doi.org/10.1103/PhysRevLett.92.180401 ; NIST Shalm et al. 2015 loophole-free Bell test, https://www.nist.gov/publications/strong-loophole-free-test-local-realism . Related 2026 experimental path/transverse-mode encoding: Forbes et al., Optica Quantum, https://doi.org/10.1364/OPTICAQ.597128 . These show known quantum-foundations phenomena; this packet contributes a falsification **gate for interpreting our single-photon W33 machinery**, not an original Bell inequality.

Code: analysis/w33_20261109_single_photon_bell_locality.py
Frozen output: data/w33_20261109_single_photon_bell_locality.json

## 5. DES Y6 full-covariance S9 frozen likelihood: deliberately not scored

The DES collaboration confirms that some Y6 cosmology data products are available and more may be released: https://www.darkenergysurvey.org/des-y6-cosmology-results-papers/ . A search-indexed NCSA source previously showed a 22 MB unblinded 3x2pt FITS and redshift products, but **an index is not a live data file**.

Fresh streaming HTTPS GET checks from the authorized Windows research computer returned:

| Endpoint | HTTP |
|---|---:|
| Official DES Y6 data release web app | 200 (HTML, not verified FITS) |
| Official DES Y6 research-paper page | 200 |
| Formerly indexed NCSA y6key final_version directory | 404 |
| Formerly indexed UNBLINDED 3x2pt FITS | 404 |
| Formerly indexed source-redshift HDF5 | 404 |
| Formerly indexed public 3x2pt pipeline notebook | 404 |

No complete validated Y6 unblinded shear xi+/- data vector, exact covariance, redshift/calibration nuisance priors or properly refitted corrected scalar-field CLASS/Halofit predictions was obtained. The project S9 preregistration in analysis/toe_uv/prereg_noshear.json is frozen at 2026-11-08. **S9 remains UNSCORED**. Neither a published marginalized LambdaCDM S8 posterior nor a cosmology paper's conditional constraints constitute a substitute for the preregistered model-specific likelihood.

Code: analysis/w33_20261109_des_y6_live_frozen_gate.py
Frozen output: data/w33_20261109_des_y6_live_frozen_gate.json

## Independent prior-art and originality controls

The GitHub repo already contains a Nov-8 single-photon complexity/mode-count falsifier (analysis/PASS20261108_FIVE_BOUNDARY_BRIDGES.md), and a 2026-10-23 recursive fresh-time-trit exponential-mode warning. These were cross-checked rather than republished as new. The realignment/CCNR criterion and Horodecki family detection are known. W33 five/eight-MUB strong unextendibility and related theta/Kramers mirrors are under active separate parallel development; this packet does not claim to originate them.

## Reproducibility

The five executable producers and their JSON outputs are shown above. A regression suite independently checks the calibration-bound premises and controls, exact 76/80 CZ ranks in newly seeded pairs, exact rational winding and phase scan, CHSH/number-SSR separation, and the fail-closed DES data ledger.

Command (from repository root):

    py -3 -m unittest discover -s tests -p test_w33_20261109_five_advanced_falsifiers.py -q

**Ten regression tests pass** on the connected Windows machine. Frozen random seeds, exact parameters, assumptions and known limitations are recorded in scripts/data.

## Top five independent next steps

1. Replace assumed POVM-effect operator-norm calibration radii by a **physically measurable, statistically justified detector-and-interferometer calibration procedure**, including phase drift, source instability and confidence intervals on K.
2. Optimize the two-CZ structured bases to **improve their 25.02 condition number** while minimizing physical switching/crossover loss; test whether a fixed Fourier/twiddle multiport gives a cheaper implementation.
3. Supply a **dynamically selected W33 extension** with a nonzero protected chiral index and verified Ward/anomaly constraints instead of externally choosing 1D hopping coefficients.
4. Acquire an **authoritative, complete DES Y6 unblinded shear FITS/covariance bundle** and execute the unchanged frozen S9 model-specific likelihood with patched CLASS/Halofit and nuisance refits; never use S8 alone.
5. Convert the single-photon mode-encoding CHSH exercise into a **causal two-party experimental protocol** that explicitly budgets reference-frame photons, heralding, feedforward, detection loopholes and spacelike separation.
