# Five W33/Q8 research fronts + two extra falsifiers — 2026-11-09

This is a **reproducible finite quantum-information and geometry research packet**, not a Theory of Everything, an experiment, or a measured cosmological likelihood. The work builds on prior Q8 72-unitary 2-designs and the eight-context 64-correlator and twelve-context tomography results.

## Front 1 — Conservatively improve the detector SDP bound

A full CVXPY/CLARABEL nuclear-norm SDP was solved in the synthetic expected-count model with 10 million accepted events per context, outcome-dependent efficiencies 0.63+0.045j known within ±0.1%, and a simultaneous 95% Hoeffding radius for all 72 detected probabilities.

Unlike the previous LP whose norm-dual W was constructed from the uncorrected estimate, the new LP chooses W from the **full SDP optimum**. W is then rounded to an integer matrix. The integer Gram G=WᵀW has exact absolute row sums; scaling by the integer ceiling of the square root of the largest row sum proves **||W||op ≤1** using rational arithmetic. Each of eight 19-variable LPs carries rational data, rational-rounded HiGHS dual multipliers, sign checks and **exact rational stationarity-residual correction**. The original 4,608 frame coefficients are recognized against the ideal qutrit-Clifford field m/18 or n√3/18. The resulting objective includes an explicit algebraic frame-model error allowance of 10⁻¹⁰ per coefficient, propagated through the witness norm.

| Known PPT source | Earlier dual LP | New rationally checked lower bound | Floating SDP |
|---|---:|---:|---:|
| Tiles | 0.687627 | **0.690064** | 0.693224 |
| Pyramids | 0.698033 | **0.698857** | 0.699643 |
| Separable threshold | 0.666667 | 0.666667 | 0.666667 |

**Interpretation:** these are rationally checked inequalities for the explicitly idealized algebraic/decimal **detector model**, NOT hardware results. The algebraic Clifford field membership is a project assumption checked against every generated coefficient; a separate formal derivation could strengthen that step. No physical detector-efficiency bounds were measured. Because the SDP optimum can be almost rank-deficient, its SVD polar W is not necessarily the optimal dual saddle point; the strict lower bound need not equal the SDP value. Full multipliers and residuals appear in the frozen JSON.

## Front 2 — An information-theoretically minimal 10-setting full state readout

Eight Q8 Bell MUB projective settings span exactly the 64 two-qutrit correlations but none of the 16 local Bloch parameters. Add two **generic non-MUB nine-mode orthonormal projective bases**. A seeded search over 250 candidate pairs produces rank 80 in the joint 90×80 traceless measurement matrix. Each nine-outcome orthonormal projective measurement has at most eight independent probabilities, hence at least ceil(80/8)=**10 settings** are required for full two-qutrit tomography in this measurement class. This design attains that elementary global information lower bound without needing a ten-MUB extension, so it is fully compatible with eight-MUB strong unextendibility. Sixty random pure/mixed density reconstructions pass at 3.49×10⁻¹⁵ maximum error. Its condition number is **29.468942**. The pair is exactly recoverable from the frozen RNG seed and winner index; a unitary-matrix SHA-256 is saved in the output. This is a W33-specific implementation of a known general tomography concept; no general novelty claim.

### Resolving the Horodecki PPT-entanglement blind spot

The previous 64-correlator nuclear-norm bound is exactly ||T(rho_a)||*=2/3 for every PPT-entangled Horodecki state 0<a<1, so it cannot flag these states. The ten-setting full density reconstruction permits the known **computable cross-norm/realignment criterion** ||R(rho)||*>1. Chen and Wu, Quantum Information and Computation 3:193–202 (2003), https://doi.org/10.26421/QIC3.3-1, applied realignment to this exact Horodecki family; Rudolph, Phys. Rev. A 67:032312 (2003), https://doi.org/10.1103/PhysRevA.67.032312, established CCNR-related methods. The criterion itself and detection of this family are prior art.

Our **independent exact symbolic all-parameter verification** constructs the unnormalized realigned matrix M=(8a+1)R(rho_a). Its squared-singular characteristic polynomial is

    z (z-a²)^5 [ z³ − (8a²+a+1)z² + (11a⁴−2a³+9a²)z/2 − a⁴(1−a)² ].

Thus five nonzero singular values equal a; a sixth vanishes; the remaining three sum to S. Writing e1=8a²+a+1, e2=(11a⁴−2a³+9a²)/2, sqrt(e3)=a²(1−a), the three-root identity yields F(S)=((S²−e1)/2)²−e2−2a²(1−a)S=0. Evaluated at S0=3a+1, F(S0)=a²(a−1)(3a+1)/4<0, and F has one zero for S≥sqrt(e1); hence S>3a+1. Therefore ||R(rho_a)||*=(5a+S)/(8a+1)>1 for **all 0<a<1**. SymPy checks the characteristic polynomial exactly. Fifteen reconstructed states pass, with max reconstruction error below 10⁻¹⁵; the CCNR margin gets extremely small near a=0 or 1.

## Front 3 — Explicit optical circuit plus a three-way precision tradeoff

The first eight Q8 Bell settings have verified factorizations using at most 18 two-mode couplers per 9-mode analyzer context, plus potential rail permutation routing. Each of the two additional **generic nine-mode** orthobases was independently synthesized with **36 adjacent complex Givens rotations**, with measured matrix-decomposition errors below 7×10⁻¹⁶. Nine output phase adjustments are sufficient. These are mathematical interferometer decompositions, not fabricated waveguides or detectors.

An extra candidate search adds a third generic basis, achieving an **11-setting** full-rank design with condition number **9.782844**. For comparison, the earlier 12-setting method adds four matched product-qutrit MUB bases, giving condition number **sqrt(2)=1.414214**. Ten settings minimize the number of complete nine-outcome projective configurations, but have substantially worse noise conditioning. The 11-setting improvement is a seeded search result (300 candidate third bases), not a global optimum.

Under architecture-specific upper coupling counts, 8×18+2×36=216 *per-configuration coupler operations summed over the ten programs*. For the twelve-setting protocol, the four matched product bases add an upper sum of 0+18+18+18=54 operations, yielding 198 across its twelve programs. These numbers **are not a simultaneous hardware-component count**; a reconfigurable mesh shares couplers. Photon loss, fabrication, phase-noise, crossovers, switching and feedforward still require engineering. Standard general mesh reference: Clements et al., Optica 3:1460 (2016), https://doi.org/10.1364/OPTICA.3.001460.

## Front 4 — Native W33 chirality obstruction

Construct the 40×40 W33 point–line incidence matrix B, containing 160 edges with degree four. An exact symbolic rational-rank calculation gives rank(B)=**25**; the exact eigenvalue spectrum of B Bᵀ is **16×1, 6×24, 0×15**. The naïve graded incidence Dirac operator D=[[0,B],[Bᵀ,0]] anticommutes with Gamma=diag(I40,−I40), but has precisely **15 plus and 15 minus zero modes**, so index(D)=**0**. Pure-gauge vertex/line rephasings preserve its singular values, whereas independently sampled edge holonomies generically lift the zero modes (numerically checked for nine draws).

This is a **no-go for unpaired protected chirality in this particular naive finite incidence Dirac model**, not a theorem excluding all chiral lattice systems. A domain-wall/overlap mechanism, boundary conditions, topological invariant or a different operator is needed before claiming a protected Standard Model chiral sector. A finite U(1) Ward/covariance identity by itself does not derive 3+1D Lorentz dynamics, anomaly cancellation, a continuum limit or gravity.

## Front 5 — DES Y6 S9 remains fail-closed

Fresh streaming GET checks on the connected Windows machine, without downloading large files:

| URL purpose | Response |
|---|---:|
| DES Y6 release Polymer web app | HTTP 200 |
| Previously indexed DES Y6 key-products directory | HTTP 404 |
| Previously indexed unblinded 22MB 3×2pt FITS | HTTP 404 |
| Previously indexed public pipeline notebook | HTTP 404 |
| Official Y6 papers | HTTP 200 |
| Public DES Y6 PPD GitHub repository | HTTP 200 |

The DES Y6 3×2pt ΛCDM S8 summary of 0.789±0.012 is published at https://www.darkenergysurvey.org/des-y6-cosmology-results-papers/. The previously indexed file is inaccessible directly. The public PPD repository https://github.com/des-science/y6-ppd-public explains that the actual 2pt FITS vector/covariance and properly matched model predictions are needed. The W33 repository's S9 preregistration was frozen on **2026-11-08**. We still have no validated unblinded xi± vector, complete covariance, consistent n(z), patched scalar-field CLASS/Halofit predictions and matched nuisance refits. **No S9 chi-squared or model comparison was computed.** This is a documented acquisition blocker, not a claimed success or failure.

## Extra: count/conditioning/resource Pareto frontier

| Complete design | Total settings | Condition number |
|---|---:|---:|
| W33 8 Bell + 2 general global bases | **10** | 29.468942 |
| W33 8 Bell + 3 general global bases | **11** | 9.782844 |
| W33 8 Bell + 4 matched product MUB bases | **12** | 1.414214 |

The extra protocols expose a useful engineering choice rather than a single ideal winner. Importantly, all three measurement designs remain finite quantum-information apparatus proposals, not standalone evidence for physical TOE dynamics.

## Reproduction

Python producers and frozen output files share the names:

- analysis/w33_20261109_q8_ten_context_tomography.py
- analysis/w33_20261109_q8_horodecki_ccnr_exact.py
- analysis/w33_20261109_q8_rational_detector_dual.py
- analysis/w33_20261109_q8_native_dirac_optics.py
- analysis/w33_20261109_q8_11_context_tradeoff.py
- analysis/w33_20261109_des_y6_s9_audit.py

For each, supply its matching data/...json filename as the first command-line argument. Run the regression suite with:

    py -3 -m unittest discover -s tests -p test_w33_20261109_q8_five_more.py -q

The DES audit makes HTTP requests; other producers run entirely from code and fixed random seeds. The paper's claimed evidence is bounded to exact linear algebra, exact rational arithmetic on a stated detector model, finite numerical simulations, and verified HTTP status. None is a laboratory demonstration.

**Top five independent continuations:** optimize structured ten-setting frames for stronger singular values; formulate a finite-shot loss-aware CCNR confidence witness; specify real time-bin/OAM nine-mode hardware and measured loss; build a nonzero-index chiral gauge system with an anomaly-controlled continuum; obtain accessible authoritative DES Y6 shear FITS/covariance products and execute the unchanged S9 test.
