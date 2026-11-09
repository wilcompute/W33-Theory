# W33/Q8: full correlation tomography, robust witnesses, optical meter, scaling null, DES Y6 gate

**November 9, 2026.** Standalone quantitative continuation of PASS20261109_Q8_SCHMIDT_WITNESS.md and PASS20261109_FIVE_FRONTS_EXECUTED.md. Producer: analysis/w33_20261109_q8_correlation_five.py; frozen data: data/w33_20261109_q8_correlation_five.json; tests: tests/test_w33_20261109_q8_correlation_five.py. A second independent implementation on the server checked the first four tracks. These are finite quantum-information results, simulated hardware calibrations, an intentionally supplied-dimension toy geometry, and a preregistration gate. They are not a TOE, a device demonstration, or a fresh DES likelihood.

## 1. All 64 two-qutrit correlations from one eight-MUB family

Let H_a, a=1,...,8, be an orthonormal traceless Hermitian qutrit basis. The 64-component nonlocal tensor is T_ab=tr(rho H_a tensor H_b). Every maximally entangled Choi projector E_j in the known W33 Q8 family has no local Bloch coefficients. Define A_(j,ab)=tr(E_j H_a tensor H_b). Then

    p_j - 1/9 = sum_ab A_(j,ab) T_ab.

Each of eight mutually unbiased complete bases contributes eight orthogonal traceless rank-one-projector directions. They lie entirely in the 64D correlation subspace. Eight such sectors exhaust this subspace exactly, yielding

    A^T A = I_64,    T = reshape(A^T(p-1/9),(8,8)).

Numerics across all three Q8 cosets (40 random mixed density matrices) give Gram and reconstruction errors below 4e-12 (actually approximately 3e-15 and 6e-16). One Q8 coset provides complete CORRELATION tomography but not full state tomography: the 16 local single-qutrit Bloch coefficients remain unmeasured. The old F8 scalar is merely ||T||_F squared; retaining singular values carries strictly more information.

### Exact, tight mixed-state Schmidt-number trace-norm bound

For a pure Schmidt state sum_i sqrt(lambda_i)|ii>, local unitaries act as orthogonal basis rotations on T, leaving singular values invariant. Its off-diagonal tensor sector contributes nuclear norm 2 sum_(i<j) sqrt(lambda_i lambda_j). The 2x2 diagonal traceless block is positive semidefinite with trace 2/3. Hence

    ||T||_* = 2/3+2 sum_(i<j) sqrt(lambda_i lambda_j)
            = (sum_i sqrt(lambda_i))^2-1/3.

By Cauchy-Schwarz, Schmidt rank at most k gives ||T||_* <= k-1/3. Matrix nuclear norm is convex; therefore the same bound holds for any MIXED state of Schmidt number <=k. A uniform pure Schmidt-rank-k state saturates it, so the bound is tight.

    ||T||_*>2/3 witnesses mixed-state entanglement (Schmidt number >=2).
    ||T||_*>5/3 witnesses Schmidt number 3.

For isotropic two-qutrit states rho_eta=eta|Phi3><Phi3|+(1-eta)I/9, ||T||_*=8eta/3. Thus the visibility thresholds are eta>1/4 for entanglement and eta>5/8 for Schmidt number 3, compared with the earlier squared-collision-only thresholds 1/sqrt(2) and sqrt(7/8). The same eight settings suffice. The isotropic thresholds coincide with standard isotropic-state fidelity criteria: no broad priority is claimed. Physical tensor factors must be clearly defined; one photon with two encoded qutrit DOFs does not imply spatial Bell nonlocality.

## 2. Robust confidence bounds under uncertain outcome-dependent efficiency

Uncorrected conditioning on detector clicks is vulnerable to false entanglement claims. For each measurement basis let p_j be the ideal nine-outcome distribution, eta_j unknown efficiency in [ell_j,h_j], v_j=eta_j*p_j and s=sum_j v_j, so the conditional click distribution is q_j=v_j/s. Define auxiliary variables (p_j,v_j,s). Their feasibility constraints are LINEAR:

    sum_j p_j=1; sum_j v_j=s;
    ell_j*p_j <= v_j <= h_j*p_j;
    qlo_j*s <= v_j <= qhi_j*s.

The last line propagates a simultaneous confidence rectangle for the observed conditional probabilities q. Under N accepted IID observations per basis, choosing epsilon=sqrt(log(2*72/alpha)/(2N)) for all 72 outcomes yields at least 1-alpha coverage by Hoeffding and a union bound. It does not address non-IID source drift or uncharacterized losses.

Choose a data-dependent matrix W from the nominal correlation tensor polar decomposition, with operator norm one. Nuclear norm duality ensures ||T_true||_* >= tr(W^T T_true). Since T is linear in p, minimizing this RHS over the eight separate per-basis linear programs gives a *valid conservative* lower bound even when W was obtained from the same data: the dual inequality is pointwise for every W and the confidence event is simultaneous.

Independent seeded synthetic test: actual efficiencies eta_j=0.63+0.045*j; independently trusted bounds eta_j*(1+/-0.01); isotropic visibility 0.8; N=150000 accepted shots per basis; alpha=.05. Result:

    true ||T||_* = 2.1333333...
    robust lower bound (infinite-count limit) = 2.124506...
    95% lower confidence certificate (seeded finite sample) = 2.100084... > 5/3.

Thus Schmidt number 3 remains certified in the synthetic control. A pure PRODUCT input gave nuclear norm 2/3, lower LP value about 0.6453 under 1% intervals, about 0.2678 under broad [0.63,0.99] intervals: no false positive. This uses *trusted* efficiency intervals; unknown detector mixing, drift, dark counts, adversarial postselection and physical phase errors remain outside the model. The certificate optimizes a fixed dual lower bound, not the true minimum nuclear norm over all feasible measurements.

## 3. Exact nine-mode Choi/Bell analyzer and component budget

Let omega=e^(2pi i/3), and label a nine-mode single-photon space by (r,c) in F3^2. The Bell basis consists of vectors

    |B_ab> = 1/sqrt3 sum_r omega^(br)|r,r+a mod3>.

The inverse analyzer is a fixed permutation mapping (r,c) to (a=c-r mod3,r), followed by three 3-mode Fourier transforms. Its unitary rows are

    W_Bell[(a,b),(r,c)]=delta_(c-r,a mod3) omega^(-br)/sqrt3.

For a Clifford frame S with single-qutrit U_S, the measured basis is the local image of the Bell basis. The exact detector transform is

    W_S = W_Bell @ (conjugate(U_S) tensor I3).

All 24 frame matrices were reconstructed and compared with the independent Clifford-Choi source to below 2e-16. The Bell block uses three Fourier tritters. Each can be decomposed into at most three two-mode couplers; the context-local factor uses three copies of a 3x3 unitary, also at most three couplers each. Thus the abstract circuit needs **at most 18 two-mode couplers per nine-mode setting**, instead of 36 in a generic 9x9 mesh. Nine individually addressable modes, crossings/permutations, programmable phases, time-bin conversion, switch settings, loss, detection, and feedforward are NOT budgeted or demonstrated. Prior art: Clements et al., Optica 3, 1460 (2016), https://doi.org/10.1364/OPTICA.3.001460 .

## 4. Finite W33 cannot select 3D or 4D by an inserted lattice

The 80-vertex W33 Levi Laplacian has exact spectrum 0^1, (4-sqrt6)^24, 4^30, (4+sqrt6)^24, 8^1. Consider a product with an EXTERNALLY supplied periodic lattice Z_256^d:

    lambda(k) = lambda_internal + 4 sum_(i=1..d) sin^2(pi*k_i/256).

At diffusion t=64, the running spectral dimension is 3.0059057 when we manually choose d=3, and 4.0078743 when we manually choose d=4. The 79 internal nonzero modes have a finite gap; the uniform internal mode becomes the low-energy channel. This confirms that the dimension of the large lattice is an externally supplied assumption, NOT a W33 prediction. It neither identifies emergent spacetime nor supplies a Lorentz/gauge/chiral interacting continuum limit. Earlier related repo work: w33_20261009_spatial_product_spectral_dimension.py. This run is an independent finite-L numerical control, not an original no-go theorem for every imaginable extension.

## 5. Updated DES Y6 public source; frozen S9 cannot yet be scored responsibly

The public DES Y6 3x2pt ΛCDM result is S8=0.789 +/- 0.012 (68% confidence): https://www.darkenergysurvey.org/des-y6-cosmology-results-papers/ ; https://arxiv.org/abs/2601.14559 . The repo's previous PRE-PATCH-REFIT full-data Dovekie best-fit information gives S8(native LambdaCDM)=0.807255, S8(CPL)=0.827087, S8(fading c<0)=0.833128, S8(fading c>0)=0.822024. Simple differences divided by the published 0.012 may help diagnose model tension, but are NOT valid model-specific likelihood scores: DES Y6's public S8 posterior is conditional on its fitted model and nuisance assumptions.

The S9 statement was preregistered on 2026-11-08 in analysis/toe_uv/prereg_noshear.json. It specifies held-out DES Y6 shear xi+/- data, full covariance and prescribed angular cuts xi+>10 arcmin, xi->60 arcmin, nuisance fits, *patched* CLASS/Halofit predictions, and a threshold |Delta chi2(CPL - fading c<0)|<2 per survey, with individual envelopes relative to LambdaCDM. A one-number S8 constraint cannot evaluate this. S9 is therefore **NOT SCORED** here, and earlier pre-patch shear comparisons remain withdrawn. The DES Y6 public catalog/3x2pt results are actionable for a future full pipeline, but the necessary model-specific likelihood has not been run. The Euclid DR1 Foundation is scheduled for Nov 12, 2026, with higher-level weak-lensing products later: https://euclid.caltech.edu/page/data-release-timeline . Do not count future products as already released on Nov 9.

## Reproduction, evidence, and next independent research steps

    py -3 analysis/w33_20261109_q8_correlation_five.py data/w33_20261109_q8_correlation_five.json
    py -3 -m unittest discover -s tests -p test_w33_20261109_q8_correlation_five.py -q

Model operations and quantum-information proofs are exact algebra, checked to finite floating precision; detector and optical tests are simulations; continuum dimension is *inserted*; cosmology is a reading of a public source and frozen repository, not fresh empirical inference.

Top five independent extensions: (1) solve the exact efficiency-interval minimum nuclear-norm SDP rather than a fixed polar dual LP; (2) separate calibration/pilot shots from blind certification, with drift monitoring; (3) compile actual mode-crossing, phase, and switching hardware and infer loss budgets; (4) derive a local gauge-covariant continuum family with Ward identities and chiral anomaly constraints; (5) retrieve DES Y6 shear xi+/- vector/covariance and compute the frozen S9 statistic with the corrected CLASS/Halofit nuisance protocol.
