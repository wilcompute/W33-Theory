# TOE51 — Execute all five: spectrum, strong CP, lepton branches, covariant decoder and native dynamics

13 October 2026. Baseline TOE50: e8d5908263c0ea22cc7cd93b70d897e6833fba02. One newer Pass398 inventory commit was observed. Holotrade has no newer scientific commits than b0264880d7c5fd24c6af932b892324247ab57808. All five fronts below have executable producers and frozen JSON certificates; none is a complete Standard Model, quantum device, theory of general relativity or TOE. Reviewed the relevant TOE47/TOE50 producers, Pass11950–11961 reports and calculations, existing exact spread ETF proofs, and Holotrade K81 representation notes. This is a focused semantic review, not a line-by-line reread of all historical files and flagship papers.

## 1. Inverse-spectral W33 tomography — rank 6 to 18 locally

Source: analysis/w33_20261013_toe51_spectral_moment_rank.py
Certificate: data/w33_20261013_toe51_spectral_moment_rank.json

On the 160-link native Maxwell graph, let W=diag(w)>0, P(k) the supplied native Bloch magnetic row matrix, M(k)=W^-1/2 P(k)^dag P(k) W^-1/2. For spectral moments T_n(k)=Tr(M(k)^n), cyclic trace differentiation gives dT_n/dw_e=-n[M(k)^n]_ee/w_e.

The existing Gauss-reduced acoustic tensor G(w) has six independent coefficients, derivative rank6 and an EXACT positive isotropic root by Pass11956. We added twelve moments: orders n=1,2,3 at k=(0,0,0),(.83,0,0),(0,.91,0),(0,0,1.01), and stacked their analytic gradients with the six existing acoustic derivatives. Finite differences on three link coordinates and all three orders confirm derivatives with max relative error 2.20e-8.

The normalized 18×160 Jacobian has NUMERICAL rank18 at relative SVD cutoff 1e-8 (and 1e-6). Rank depends strongly on practical relative tolerance:

| relative SVD cutoff | retained rank |
|---:|---:|
| 1e-3 | 9 |
| 1e-4 | 12 |
| 1e-5 | 15 |
| 1e-6 | 18 |
| 1e-8 | 18 |

Condition number is about 519,849. Thus mathematical local observability has advanced by twelve directions from the rank-six cone (and eleven beyond TOE50's rank-seven first-moment audit), but a NOISE-INDEPENDENT rank-18 experimental claim would be misleading. The remaining local nullity is 142 when all 18 derivatives clear the strict 1e-8 relative SVD cutoff; at conservative 1e-4 tolerance the retained rank is only 12 (nullity 148). No unique 160-weight reconstruction, quantum light speed, or measured photonic spectra result.

## 2. Strong CP — finite EFT control radius for the color-enhancement pole

Source: analysis/w33_20261013_toe51_physics_three_fronts.py
Certificate: data/w33_20261013_toe51_color_threshold_domain.json

Pass11957 constructed an SU5_color -> SU4_color -> SU3_color holomorphic matching model with v1=v2=v0 z, m=m0 z. Its declared relation is Lambda3^(9-n)=m0 Lambda5^(12-n)/(v0^4 z^3). For n=0, Lambda3 scales |z|^(-1/3) but ALL heavy Higgs and matter thresholds vanish proportional to |z|. Their ratio to the strong scale therefore tends to zero as |z|^(4/3): the weakly coupled SU3 threshold calculation cannot be extrapolated all the way to the separating divisor. This does not refute the formal local holomorphic pole nor produce a strongly coupled UV completion.

For illustrative arbitrary mass units v0=100, m0=50, Lambda5=1, min(heavy threshold)/Lambda3 crosses 1 at |z|=0.0158740105. Values: at |z|=.03 the ratio is2.3366, at .01 is.5400, at .001 is.0251. Near equality perturbation theory is already marginal. No global modular phase, colored spectrum, gluino phase, or neutron EDM prediction is supplied. Pass11949 already retracted the axiflavon solution; it is not reinstated.

Known alternative Nelson–Barr prior art includes Alves–Nishi–Vecchi, PRD114(2026)015025, https://arxiv.org/abs/2604.02506. Their vectorlike doublet model is NOT the repo's declared E6/vectorlike model.

## 3. Charged-neutrino fitted-branch discrimination

Source: analysis/w33_20261013_toe51_physics_three_fronts.py
Certificate: data/w33_20261013_toe51_lepton_branch_observables.json

Reconstructed all FIVE distinct stored parameter roots from Pass11960's actual fitted real Majorana matrices, shared Weyl kernel and charged-lepton Clebsch matrices, preserving mass ordering and its physical CKM convention. Chose Delta m31²=0.0025 eV² only as an EXTERNAL illustrative absolute normalization (not dynamically derived). In the fitted charged basis computed conditional m_bb=|M_nu,ee| and sum of all three light masses.

Three distinct outcomes (two additional Clebsch fits duplicate these roots):

| fitted Dirac delta | conditional m_bb (eV) | sum m (eV) | lightest m (eV) |
|---:|---:|---:|---:|
| 280.615° | 0.002969 | 0.068709 | 0.007074 |
| 112.576° | 0.002184 | 0.060927 | 0.002044 |
| 57.492° | 0.003049 | 0.063100 | 0.003631 |

All five m_bb values lie in the rigorous triangle-inequality envelope when the two independent Majorana phases are freely varied at the same masses and PMNS first-row magnitudes. The phase-free envelopes overlap. The numerically different central examples are conditional consequences of the supplied fitted matrices, **not predictions**; four observed oscillation inputs were used to fit four real model parameters. No stabilized vacuum, high-scale running, nuclear-matrix conversion or unmeasured Majorana phase determination has been established.

## 4. W33 covariant dual decoder plus detector-independent linear noise baseline

Source: analysis/w33_20261013_toe51_covariant_dual_compiler.py
Certificate: data/w33_20261013_toe51_covariant_dual_compiler.json

Start from the exact TOE50 integer-derived identity on the shared 40 W33 line labels:
I40 = (3/4)G_cusp + (1/18)B B^T - (1/4)J,
and the orthogonal projector resolution 40=1+24+15.

Explicitly construct permutations on 40 lines and 36 spreads for each of SEVEN native symplectic generators. Verify objectwise L_g B=B S_g, and L_g P_r L_g^T=P_r for all three orthogonal projectors r=1,24,15. Max computed equivariance error <6e-15; 80 random signal covariance checks pass.

For *independent, equal-variance, additive Gaussian noise* on 40 cusp readings and 36 spread readings, assuming an EXACT independent global sum, the elementary linear decoder has
E||yhat-y||² = sigma²[40*(3/4)² + Tr(BBt)/18²] = sigma²*(23.611111...).
At sigma=.001, theory2.361111e-5 versus 1500 simulated trials2.354833e-5. This is analysis-readout noise only; no photonic SPAM/loss theory.

Holotrade's current K81 certificate gives THREE 81D regular H27×C3 carriers. No Sp4(3) action or equivariant map from the 40-line representation into those K81 modules has been constructed. A trivial coordinate embedding 40->81 isometric map exists and was checked, but DOES NOT establish group equivariance or a photonic compiler. This is an explicit remaining representation-theoretic gate.

## 5. Native dynamically weighted Maxwell model preserves Gauss but does not close gravity

Source: analysis/w33_20261013_toe51_physics_three_fronts.py
Certificate: data/w33_20261013_toe51_dynamic_metric_gauss.json

To remove the previous frozen-weight secondary-constraint problem, declare 160 positive canonical weight-coordinate/p-momentum pairs and

H = Σ_e [E_e²/(2w_e) + p_e²/(2M) + κ(w_e-w0)²/2] + ||P A||²/2.

Its canonical equations are dot w=p/M; dot p=E²/(2w²)-κ(w-w0); dot A=E/w; dot E=-P†P A. On the native complex P B=0, so Gauss B†E=0 is conserved. Random initial data projected to Gauss and their computed time derivatives have residual <1e-8. The one-link equilibria κ(w-w0)=E²/(2w²) have positive local scalar curvature κ+E²/w³ and nonzero electric fields.

This is a well-defined dynamical Maxwell-plus-SCALAR system. It adds 160 scalar degrees of freedom, NO gravitational Hamiltonian/diffeomorphism constraints or two-polarization spin-two dynamics. Therefore it does NOT solve Einstein gravity. Discrete canonical gravity algebra has specific known constructions in other sectors: Bonzom–Dittrich (2013) https://arxiv.org/abs/1304.5983. None is automatically inherited by our finite graph.

## Reproducibility

Tests regenerate every certificate from three stand-alone producers:
py -3 -m pytest -q tests/test_w33_20261013_toe51_five_fronts.py tests/test_w33_20261013_toe50_spectral_and_dual_decoder.py tests/test_w33_pass11957_11961_selection_completion.py

Only TOE51 source/report/test and five frozen JSON certificates are eligible for staging. Preserve all preexisting collaborative dirty files and untracked research scratch.

## Five independent next research proposals

1. Choose wavevectors/moments maximizing the smallest Jacobian singular value subject to finite-shot hardware bounds; test noisy multi-defect weight recovery rather than another ill-conditioned exact rank.
2. Build a full colored threshold with proven UV matching and phase across the nonperturbative enhancement region, compute all gluino/scalar phases and the physical neutron-EDM quantity.
3. Derive Clebsch/Majorana parameters from one stable common E6 vacuum; independently constrain Majorana phases, beta-beta, absolute masses and full lepton CP.
4. Compute restricted H27 characters of the 40-line 1+24+15 representation and Holotrade's three K81 regular slices; produce an actual H27-equivariant intertwiner or a character-theoretic no-go, then consider lossy photonic hardware.
5. Construct nontrivial first-class native gravitational Hamiltonian/diffeomorphism constraints with a correctly counted physical phase space, verify Poisson closure, and obtain a continuum two-graviton limit instead of declaring the Maxwell-scalar system a gravity theory.
