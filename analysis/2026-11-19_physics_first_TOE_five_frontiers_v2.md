# Beyond W33: five experimentally anchored Theory-of-Everything falsifiers (v2)

**2026-11-19.** Research status: five quantitative, reproducible physics-first checks, with a sixth exact one-loop threshold obstruction. **Not a Theory of Everything.** The W33 finite geometry and prior numerological conjectures are not assumptions or inputs to any calculation below. Repository is used only for recordkeeping and reproducibility.

## Prior-art/parallel-work firewall

We reviewed `8efe83ec6` (the initial model-independent six-sector checks) and `5b45a41af7` (parallel compact chirality, mirror-mass rank, UV parent, relativistic string constraints, one-photon capacity, one-loop RG benchmark). Both reports already cover the one-loop Standard Model GUT mismatch, charge-anomaly ambiguity, conditional Majorana electric-charge quantization, low-level inflation/quantum-gravity challenges, and cosmology caveats. We **do not** claim those known identities as new discoveries. This v2 packet instead:

- integrates coupled **two-loop SM gauge** and **one-loop top Yukawa** running, computes a corrected triple-coupling mismatch, and derives a specific **single split SU5 5+5bar threshold obstruction**;
- builds exact **neutrino Majorana phase envelopes** and a PMNS/Takagi mass-matrix reconstruction using *2026 preliminary fit* inputs;
- computes the **Starobinsky f(R)=R+R²/(6M²)** scalaron model's exact first-order slow-roll predictions for N=50,55,60 and normalizes its mass using As;
- solves **GR background expansion plus linear structure-growth ODEs** for the DES/DESI 2026 low-z CPL benchmark and a matched LambdaCDM model;
- calculates the entire **CHSH conditional probability table** for a Bell state and a hypothetical Popescu–Rohrlich no-signaling box, and certifies local-polytope feasibility using linear programming.

These results are model checks and transparent baseline calculations, not priority claims for textbook theorems, new experimental observations, a unique particle model, or fundamental gravitational dynamics.

## Front 1: genuine two-loop gauge running and a quantitative minimal split-threshold no-go

Initial representative MS-bar inputs at MZ=91.1876 GeV:

    alpha_EM^-1(MZ) = 127.930
    sin²theta_W(MZ) = 0.23122
    alpha_s(MZ) = 0.1180
    y_t(MZ) = 0.94 (illustrative approximation)

GUT-normalized alpha1=(5/3)alphaY. Let t=ln(mu/MZ). In a simplified SM without threshold matching, the gauge RG equations are

    dg_i/dt = b_i*g_i³/(16*pi²)
              + g_i³/(16*pi²)² * [sum_j B_ij*g_j² - c_i*y_t²]

    b = (41/10, -19/6, -7)

    B = [[199/50, 27/10, 44/5],
         [9/10,   35/6,  12],
         [11/10,  9/2,  -26]]
    c = (17/10, 3/2, 2)

The one-loop top Yukawa RGE is

    dy_t/dt = y_t/(16*pi²)*[(9/2)y_t² - (17/20)g1² - (9/4)g2² -8*g3²].

This is a partial two-loop treatment: no two-loop y_t, Higgs quartic, b/tau Yukawa, full threshold and matching, or gravity. Full precision GUT fits require more.

**Numerical outputs:** at the U1/SU2 crossing, one-loop mu12=1.0266e13 GeV with inverse U1 minus SU3 mismatch **5.58038**. Two-loop gauge with one-loop top y_t moves the crossing to **1.0848e13 GeV** and mismatch **4.90135**; the best spread of all three inverse couplings over 91 GeV--10^18 GeV is still **3.18696**. Thus corrected SM running remains nonunified. These are not observed scales; they are predictions of the specified running extrapolation from measured couplings.

**More specific obstruction:** one vectorlike Dirac SU5 5+5bar decomposes under the SM into a color triplet D and weak doublet L, with one-loop shifts

    delta_b_D = (4/15, 0, 2/3)
    delta_b_L = (2/5, 2/3, 0)
    sum = (2/3,2/3,2/3).

At a common threshold the equal shift cancels identically from inverse-coupling differences; a degenerate complete multiplet cannot fix one-loop differential running.

Allow D and L to have *different* masses, but demand both thresholds satisfy MZ <= m_D,m_L <= MU and a single exact crossing. For MU above both thresholds, all relative RGE effects depend only on one splitting parameter rho=ln(m_L/m_D). The two independent pairwise coupling-equality equations become

    (alpha1^-1-alpha2^-1, alpha1^-1-alpha3^-1)^T
       = (1/(2pi))*[[b1-b2, delta_b_D1-delta_b_D2],
                      [b1-b3, delta_b_D1-delta_b_D3]]
                      * (ln(MU/MZ),rho)^T.

Exact 2x2 inversion gives **MU=5.0531e13 GeV**, **ln(MU/MZ)=27.04069**, and **rho=-43.42974**, i.e. m_L/m_D~**1.376e-19**. But if *both* masses lie within [MZ,MU], the absolute splitting must obey |rho| <= ln(MU/MZ)=27.04, a contradiction.

**Conclusion at defined scope:** a single split vectorlike Dirac 5+5bar with both thresholds active between MZ and MU **cannot** achieve exact 1-loop SU5-normalized SM triple unification using those fixed boundary inputs. This does not exclude multiple split multiplets, GUT threshold corrections, representations other than 5, multiplets with masses outside the interval, higher loops, or specific BSM theories. This simple analytically solvable no-go is the sharpest added independent obstruction in this packet.

Sources: standard two-loop SM coefficients from https://link.springer.com/article/10.1140/epjc/s10052-017-4683-2 and https://academic.oup.com/ptep/article/2026/7/073B07/8702921 ; PDG gauge coupling reference https://pdg.lbl.gov/2025/reviews/rpp2025-rev-standard-model.pdf .

## Front 2: exact Majorana-neutrino observables, not just lower mass sums

For 2026 preliminary Bari (JUNO+atmospheric) fit, use:

    NO: delta_m21²=7.465e-5 eV², delta_m31²=2.5093e-3 eV²,
        sin²theta12=.3047, sin²theta13=.0222.
    IO: delta_m21²=7.439e-5 eV², |delta_m32²|=2.5182e-3 eV²,
        sin²theta12=.3036, sin²theta13=.0223.

For mass eigenvalues m_i and electron PMNS weights w_i=|U_ei|²,

    m_beta² = sum_i w_i*m_i²
    m_beta_beta = |sum_i w_i*m_i * exp(i alpha_i)|.

With two free Majorana phases, define a_i=w_i m_i. The **exact phase envelope** is

    max(0,2 max_i(a_i)-sum_i a_i)
      <= |m_beta_beta| <= sum_i a_i.

This is the triangle/polygon inequality and needs no Monte Carlo phase sampling.

At zero lightest mass:

| Ordering | sum m_i | m_beta | min |m_beta_beta| | max |m_beta_beta| |
| --- | ---: | ---: | ---: | ---: |
| NO | 0.05873 eV | 0.00883 eV | 0.001462 eV | 0.003686 eV |
| IO | 0.09962 eV | 0.04911 eV | 0.018763 eV | 0.048554 eV |

As the NO lightest mass becomes nonzero, a triangle of complex amplitudes closes for a small range of m1 near a few meV; **exact m_beta_beta=0 is mathematically possible** by phase cancellation. The IO central-value floor at m3=0 is ~18.76 meV. These are central-input phase envelopes, not full likelihood bands or detection sensitivity, and nuclear matrix elements are needed to translate to half-life.

An explicit unitary three-flavor PMNS matrix was constructed with the preliminary NO angles, sin²theta23=.4908 and delta_CP/pi=1.19. For one **chosen**, not predicted, NO mass m1=.006 eV, the Majorana mass matrix M=U*diag(m)U^dag is complex symmetric and satisfies the exact Takagi identity U^T M U=diag(m) to ~machine precision. This demonstrates mathematical realizability, **not** a dynamical seesaw or flavor explanation.

Source: https://global-nu.org/results.html (fit release and conventions). Do not conflate the Bari result with NuFIT 6.1 or with cosmological priors.

## Front 3: healthy R² gravitational EFT and inflationary predictions

Start with a gravitational EFT action

    S = (Mpl²/2) integral sqrt(-g) [R + R²/(6M²)].

For M²>0, its Einstein-frame scalaron potential is

    V(phi)=(3/4)Mpl² M² [1-exp(-sqrt(2/3)phi/Mpl)]².

Let y=exp(sqrt(2/3)phi/Mpl); the slow-roll expressions are

    epsilon=4/[3(y-1)²],
    eta=4(2-y)/[3(y-1)²],
    y_end=1+2/sqrt3,
    N=(3/4)[y-y_end-ln(y/y_end)],
    n_s=1-6epsilon+2eta,  r=16epsilon.

Solve N exactly by root finding and fix M by scalar amplitude As=2.1e-9:

    As=M² (1-1/y)²/[32 pi² Mpl² epsilon].

| e-folds N | scalar tilt ns | tensor ratio r | M/Mpl |
|---:|---:|---:|---:|
| 50 | 0.961570 | 0.004192 | 1.33674e-5 |
| 55 | 0.964977 | 0.003498 | 1.21963e-5 |
| 60 | 0.967827 | 0.002964 | 1.12149e-5 |

At N=55 the inferred scalaron mass is **2.970e13 GeV** (reduced Mpl=2.435e18 GeV).

Comparison: 2025 CMB combination reported ns=0.9682±0.0032 and r<0.034, while inclusion of DESI BAO shifted ns=0.9728±0.0029 (dataset-dependent). Inflationary fits must include reheating uncertainties and CMB likelihoods. Neither R² inflation nor its consistency with some observations constitutes a UV-complete gravity theory or resolves present-day dark energy.

Sources: https://arxiv.org/abs/2512.10613 , https://csnsdoc.ihep.ac.cn/article/doi/10.1088/1674-1137/ae8cf2 .

## Front 4: expansion AND linear structure growth for DES/DESI dark energy

Use flat GR with Omega_m0=.302, H0=68.3 km/s/Mpc, negligible radiation at z<=2, homogeneous smooth DE, and the DES Y6 + DESI DR2 *low-redshift-only* CPL best-fit w0=-.84, wa=-.53 (reported about 2.3 sigma from LambdaCDM). Compare with LambdaCDM w0=-1,wa=0 at the **same** H0 and Omega_m0.

    w(a)=w0+wa(1-a),
    E(a)^2=Omega_m0*a^-3+(1-Omega_m0)
            *a^[-3(1+w0+wa)] exp[3wa(a-1)].

Numerically integrate comoving distance chi(z)=(c/H0)int_0^z dz'/E(z') and the standard scale-independent linear growth ODE (prime=d/dln a):

    D''+[2+dlnH/dln a]D' -(3/2)Omega_m(a)*D=0.

Initial growing mode D(a_ini)=a_ini, D'(a_ini)=a_ini for a_ini=.001. Normalize growth D(1)=1 for each cosmology; assume sigma8(0)=.8 for both **by hand**, hence these are not CMB-amplitude-matched models.

| z | H_CPL/H_LCDM-1 | chi_CPL/chi_LCDM-1 | (f sigma8)_CPL/(f sigma8)_LCDM-1 |
|---:|---:|---:|---:|
| 0.1 | +1.246% | -0.679% | -1.397% |
| 0.3 | +1.996% | -1.358% | -1.864% |
| 0.5 | +1.677% | -1.539% | -1.277% |
| 0.7 | +1.081% | -1.498% | -0.490% |
| 1.0 | +0.290% | -1.298% | +0.442% |
| 2.0 | -0.583% | -0.728% | +1.207% |

The w=-1 crossing occurs at z=.432432; there is a dark-energy density extremum there, but **no such crossing is observationally proven**. A 2.0% H shift near z=.3 can coexist with a 0.29% H shift at z=1. Multi-redshift distances and growth are essential to distinguish evolving DE from ΛCDM. This numerically illustrates the need for joint background and perturbation tests.

The growth equation applies to homogeneous CPL fluid in minimally modified (here unmodified) GR, not automatically to interacting dark energy or modified gravity. This packet does NOT perform a full likelihood fit or claim the best-fit is favored by data at each plotted redshift.

Source: https://www.darkenergysurvey.org/des-y6-cosmology-results-papers/ .

## Front 5: a constructive boundary between local, quantum and no-signaling physics

Consider two choices and two binary outcomes per party. For a Bell state |Phi+> with A0=Z,A1=X, B0=(Z+X)/sqrt2,B1=(Z-X)/sqrt2, compute the complete **16-entry** quantum probability vector p(a,b|x,y) directly from Born projectors.

Also construct a hypothetical Popescu-Rohrlich box:

    p(a,b|x,y)=1/2 if a*b=(-1)^(x*y), else 0.

Both satisfy normalization and exact no-signaling marginals. Their CHSH values are respectively

    CHSH_quantum=2sqrt2 = 2.828427...
    CHSH_PR=4.

The PR box is **not** a quantum-state prediction. Exhaustively form all 16 deterministic local strategies (a0,a1,b0,b1) in {±1}^4 and solve for nonnegative convex weights using linear programming. For the isotropic family v*p_quantum + (1-v)*p_uniform, verify local feasibility at v=.70 and at the exact boundary v=1/sqrt2; verify failure at v=.72,.85,1. Consequently this CHSH setup has a local/noisy-quantum visibility threshold v=1/sqrt2, i.e. ~29.29% white-noise admixture.

**Implication:** no-signaling or causal speed limits alone are **strictly weaker** than the experimentally verified restrictions of quantum theory. A proposed information-theoretic TOE must explain the quantum admissible correlations (Born rule/Tsirelson), not merely signal prohibition. This demonstration proves none of those laws from more fundamental principles.

## Cross-front consistency and what the calculation does NOT establish

- Gauge-coupling integration, Majorana phase geometry, inflationary scalar tilt/tensors, dark-energy growth, and Bell correlations can all be reproduced numerically but are **not produced by one dynamical theory**.
- The scalaron inflation mass at ~3e13 GeV and Weinberg-neutrino suppression ratio ~6e14 GeV from prior work are independent parameters. A proximity or ratio of scales is **not** physical unification without a Lagrangian and calculable couplings.
- The single-split-5 multiplet obstruction is narrowly conditioned on 1-loop RG, given measured low-energy inputs, and both component thresholds inside [MZ,MU]. It is a useful falsifier of one repair, not a no-go for GUTs.
- Error tolerances, imported data sources, and model limitations are deliberately in the JSON rather than treated as discovered constants.

## Exact reproducibility

    python analysis/toe_20261119_physics_first_frontiers_v2.py
    python -m unittest discover -s tests -p test_toe_20261119_physics_first_frontiers_v2.py -v

Machine-readable output:

    data/toe_20261119_physics_first_five_frontiers_v2.json

The independent checks cover 2-loop gauge ODEs, exact threshold linear algebra, neutrino phase envelopes and Takagi reconstruction, R² inflation normalization, distance/growth integration, and the local Bell-polytope linear-programming boundary. All 12 focused tests passed in local execution before committing.

## Top five independent next physical research tasks

1. **Real particle spectrum and two-loop match:** build an actual anomaly-free BSM model with explicit masses and threshold matching; fit the gauge **and Yukawa** RGEs, proton lifetime, CKM/PMNS while demanding at least one new parameter-free prediction.
2. **Neutrino origin and observable tests:** derive Majorana/Dirac status and seesaw or alternative mass matrix from the candidate's fields, then predict beta-decay masses, 0νββ half-lives with nuclear uncertainties, and leptonic CP correlations.
3. **Complete quantum-gravity S-matrix:** construct a unitary and causal graviton sector with controlled UV amplitudes, absence of ghosts, gravitational constraints and horizon microstate counting. Inflationary R² is not this completion.
4. **Full dark-sector likelihood and perturbations:** evaluate DESI/DES/CMB/SNe data covariance on candidate H(z) and fσ8(z), including radiative and neutrino effects; reject effective phantom crossings incompatible with stability.
5. **Quantum operational derivation:** supply dynamical principles for Born weights and the Tsirelson limit while proving no-signaling and Lorentz-causal field propagation, beyond just matching Bell distributions.

**Bottom line:** This is an expanded falsification framework with a new narrow split-multiplet obstruction and reproducible quantitative predictions of known candidate models. No Theory of Everything has been solved.
