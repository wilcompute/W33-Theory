# Five executed follow-ups: detector-norm SDP, PPT family blind spot, routing depth, gauge no-go, DES Y6 acquisition

**November 9, 2026.** Self-contained reproducible extension of PASS20261109_Q8_CORRELATION_FIVE.md and PASS20261109_Q8_TILES_PPT_EXACT.md. Producer: analysis/w33_20261109_q8_five_extensions.py; frozen data: data/w33_20261109_q8_five_extensions.json; tests: tests/test_w33_20261109_q8_five_extensions.py. Evidence tiers are distinguished below. No new physical TOE, laboratory observation, or cosmological likelihood is asserted.

## 1. Numerical full nuclear-norm SDP versus a conservative fixed-dual LP

The previously published instrument supplies 72 reported conditional probabilities q_(b,j), with unknown ideal p_(b,j), unknown efficiency eta_j in independently calibrated bounds [ell_j,h_j], unnormalized click masses v_(b,j) and each basis acceptance mass s_b. The physical measurement-preparation constraints tested are:

    sum_j p_(b,j)=1, sum_j v_(b,j)=s_b,
    ell_j p_(b,j)<=v_(b,j)<=h_j p_(b,j),
    (qhat_(b,j)-eps) s_b <= v_(b,j) <= (qhat_(b,j)+eps) s_b.

The 64-element correlation tensor is T=reshape(A.T@(p-1/9),(8,8)), with exact A.T A=I_64. The new **convex nuclear-norm SDP** minimizes ||T||_* over all eight basis distributions simultaneously rather than minimizing a single preselected dual test matrix. This solves the tighter **probability-relaxed** worst-case tomography problem; it does not impose a common PSD density operator for all settings, so it is conservative relative to a quantum-physical feasible set.

Using CLARABEL via CVXPY 1.9.2 with nominal expected conditional frequencies (no random shots), relative per-outcome efficiency uncertainty 0.1%, N=10,000,000 accepted shots per basis, and 72-fold Hoeffding simultaneous 95% radius 0.00063109213167:

| Known PPT target | Actual ||T||_* | Previous LP lower estimate | Full numerical SDP minimum |
|---|---:|---:|---:|
| Tiles UPB | 0.7022810882 | 0.6876268626 | **0.6932236036** |
| Pyramids UPB | 0.7114378384 | 0.6980325633 | **0.6996433209** |

Both exceed the separability bound 2/3 under this synthetic design-point model. The SDP improves over the fixed-dual linear objective but **these optimum values remain numerical**, not certified interval-arithmetic lower bounds. A future rigorous lower certificate needs a verified SDP dual plus residual accounting. Detector drift, unknown mode mixing, dark counts, correlation between trials, and uncertain physical source remain unmodeled. Crucially, setting reported frequencies equal to their expectations is not a power calculation and is not an empirical experiment.

### Beyond optimization: the known Pyramids example beats Tiles

Pyramids uses five known UPB product vectors v_k tensor v_(2k mod5), k=0..4, where v_k=[cos(2 pi k/5),sin(2 pi k/5),sqrt(cos(pi/5))] / sqrt(1+cos(pi/5)). The vectors are mutually orthogonal because each pair has either index difference ±2 in the first factor or the second factor. The orthogonal complement rho=(I-sum projectors)/4 is a PPT rank-four entangled state (Bennett et al. 1999, https://doi.org/10.1103/PhysRevLett.82.5385). Rebuilding all five vectors gave |orthogonality residual| <2e-14 and the Q8 correlation trace norm **0.7114378384**, versus **0.7022810882** for Tiles. The Pyramids correlation witness has an 0.0447712 margin above 2/3, versus Tiles' 0.0356144 margin. This is a benchmark improvement, not a new state.

## 2. Exact Horodecki PPT family no-go, not just a sampled failure

The standard two-qutrit family rho_a of Paweł Horodecki (1997), 0<a<1, is PPT entangled; see https://arxiv.org/abs/quant-ph/9703004 ; explicit density matrix https://doi.org/10.1016/j.physleta.2010.11.069. The exact 8x8 correlation tensor in the repo's Hermitian orthonormal frame contains five independent singular values a/(8a+1); its remaining 2x3 nontrivial block has Frobenius norm squared

    (7a^2-2a+4) / (9(8a+1)^2)

and Gram determinant

    a^2(a-1)^2 / (9(8a+1)^4).

For 0<a<1, the sum of the block's two singular values is exactly (a+2)/(3(8a+1)). Therefore

    ||T(rho_a)||_* = 5a/(8a+1) + (a+2)/(3(8a+1)) = 2/3.

This is an **exact blind spot for every member** of the PPT-entangled Horodecki family: no fixed-number measurement precision or nuclear-norm reconstruction can make THIS criterion pass. The producer symbolically constructs the full 9x9 rho_a, all eight Gell-Mann generators, verifies each of the 64 symbolic correlations, and checks the closed-form SVD/block identity with SymPy; a 12-point numeric sweep checks PPT and positivity. This does NOT mean the underlying eight-MUB data cannot be used to design a different nonlinear or nonlocal witness.

## 3. Previously omitted nine-rail permutation: 13 swaps, six physical routing layers

In the code's input rail ordering i=3r+c, the Bell transform must group by a=c-r mod3, with target output rail 3a+r. Thus the fixed 9-mode permutation is

    [0,3,6,7,1,4,5,8,2].

It has exactly **13 inversions**, and hence requires 13 adjacent swaps if implemented using a single linear nearest-neighbor rail ordering with adjacent SWAP primitives. Odd-even transposition sorting realizes those swaps in **six parallel layers** (the producer records every pair). The longest-affected rail participates in six swaps. Under a toy independent per-swap 0.5% intensity-loss assumption, its conditional transmission is 0.995^6=0.9703725; the initially unaffected rail is 1.0. This is an explicitly specified *routing* error model, not a photonic-chip measurement. Depending on architecture, crossings may be realized by fixed routing and do NOT have to consume tunable two-mode couplers. If each of these 13 swaps instead requires a 2-mode device, the earlier 18-coupler Bell/context network rises to an abstract upper budget of **31 elements per setting**. Not a universal lower bound on all photonic layouts; crossing count, insertion loss and depth depend on physical architecture.

## 4. Finite Ward identity is exact; W33 alone still selects no physical continuum

The native W33 Levi incidence graph has 80 vertices, 160 edges and an 81-dimensional U(1) cycle-flux space. The previously published gauge-action verifier is reexecuted: local phase gauge transformations leave the graph scalar action and Laplacian transport covariant at numerical ~1e-15. This is a correct *finite lattice U(1) Ward identity* but neither gravity nor a time-evolving relativistic continuum. Its 1620 eight-cycles span only 81 flux directions; no 3+1D Weyl law follows from the fixed graph. Adding an explicit external Z_256^d product produces running spectral dimensions 3.0059 at t=64 when we manually choose d=3, or 4.0079 when we manually choose d=4: the dimension is input, not derived. Without an independently selected continuum, anomaly-safe chiral matter and Lorentz/gauge dynamics, no TOE claim is justified.

### A stronger information-theoretic no-go

ALL 24 Clifford Choi measurement bases (three cosets) are totally blind to the 16 local Bloch components. An exact pair of witnesses is

    rho0=I9/9, purity=1/9,
    rho1=|0><0| tensor I3/3, purity=1/3.

Every maximally entangled Choi projector in all 24 bases gives p_j=1/9 for BOTH states. Numerically the maximal probability difference was 5.6e-17. This shows that even a collection of every Q8 coset **cannot certify input purity from its own measurements**; the pure-state entropy formula needs an external trust assumption or extra local measurements. It does not obstruct the trace-norm mixed Schmidt-number witness.

## 5. DES Y6 full-covariance acquisition: previously indexed file now returns HTTP 404

External 2026 literature describes the public DES Y6 3x2pt analysis and pipeline (https://www.darkenergysurvey.org/des-y6-cosmology-results-papers/ and https://github.com/des-science/y6-ppd-public/). An index cached approximately three months before Nov 9 advertised a 22 MB unblinded FITS at

    https://desdr-server.ncsa.illinois.edu/despublic/y6a2_files/y6key_products/final_version/3x2pt_2025-07-28-20h_UNBLINDED_wmask_nob2.fits

We attempted a DIRECT HTTPS GET from the authorized connected Windows research machine on Nov 9 using requests with a 35-second timeout. The endpoint returned **HTTP 404**, so no 2pt data-vector bytes were downloaded or verified. The parent directory's web index also returned 404 to an independent HTTP fetch. A cached search index is not proof of current file accessibility, and it does not justify any cosmological model-fit score. Public Y6 LambdaCDM S8=0.789±0.012 is an externally derived conditional summary, not the frozen S9 model comparison.

The frozen S9 preregistration (analysis/toe_uv/prereg_noshear.json, 2026-11-08) requires matched public xi+/xi- vector, covariance, n(z), NLA nuisance priors, corrected scalar-field CLASS/Halofit predictions, cuts xi+>10 arcmin and xi->60 arcmin, and held-out parameter refits. Without these, **S9 remains UNSCORED**. This is an acquisition failure and explicit prerequisite ledger, not a claim of cosmological falsification or endorsement. The 2026 NCSA directory may be moved or permissions changed; seek official updated links rather than guessing.

## Reproduce and audit

    py -3 analysis/w33_20261109_q8_five_extensions.py data/w33_20261109_q8_five_extensions.json
    py -3 -m unittest discover -s tests -p test_w33_20261109_q8_five_extensions.py -q

Exact: symbolic Horodecki norm, W33 Q8 measurement-kernel identity, combinatorial 13-swap inversion count. Numerical: SDP solver results; complete finite-source/geometry checks; toy detector and crossing losses. External data: verified 404 and cited DES survey pages. No physical experiment, dynamical TOE, or original PPT-entangled state has been presented.

Five independent follow-up research tracks: (1) derive an interval-verified SDP dual, (2) optimize a nonlinear witness that detects Horodecki despite 2/3 saturation, (3) budget nine-waveguide crossings, phases and measured losses on a specific chip, (4) derive locality/chirality and a 3+1D continuum dynamically, (5) locate a current official DES Y6 xi±/covariance archive and run the corrected-model frozen S9 likelihood.
