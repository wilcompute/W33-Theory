# W33/TOE: five rigorous continuation fronts and an 80-mode symmetry no-go

**Research date:** 2026-11-09 (US Eastern); corresponding remote UTC logs can fall on Nov 10. **Source:** latest wilcompute/W33-Theory master plus established quantum optics and DES Y6 publications. **Reproducibility:** four new Python producers, one fresh official-data audit, five frozen JSON results, eleven regression tests. No physical TOE validation is claimed.

This round deliberately examines what finite geometry genuinely determines and which photonic tests are experimentally feasible, rather than assigning physics to numerical coincidences.

## 1. Exact PSp(4,3) point–line intertwiner theorem: thirty protected flat zero modes

The exact W33 generalized quadrangle has 40 points and 40 lines, each incident with four objects. Generate all 40 symplectic projective transvections on the native 40-point geometry, and induce their action on the 40 lines. They preserve the square point-by-line incidence matrix B. Exhaustive orbit closure on **all 1,600 ordered point/line pairs** gives exactly two group orbits:

- 160 incident pairs;
- 1,440 nonincident pairs.

A linear point–line intertwiner T commuting with full PSp(4,3) is therefore constant on each orbit. This proves

    Hom_G(C^lines,C^points) = span_C{B,J-B},
    T=a B+b(J-B).

Because B B^T has exact spectrum {16^1,6^24,0^15}, the B singular spectrum is {4^1, sqrt6^24,0^15}. J acts only on the one-dimensional all-ones sector. More explicitly:

- on the trivial sector T acts with singular value |4a+36b|;
- on the common 24-dimensional sector T acts with |a-b| sqrt6;
- on the unmatched 15-dimensional point and 15-dimensional line sectors T vanishes **for every** a,b.

Hence rank(T)<=25. For any *chiral* 80x80 Hamiltonian H=[[0,T],[T†,0]], the two sectors together supply at least **30 exact energy-zero modes**: 15 of grading + and 15 of grading −. Its net finite chiral index is 0. Generic a,b have precisely 30; the special case a=b has 78; a=b=0 gives 80. Six coupling controls were checked independently by direct matrix ranks and diagonalization.

The point and line permutation modules have commutant dimension 3 each; their two cross Hom spaces have dimensions 2 each, so the **80-dimensional direct-sum commutant dimension is exactly 3+3+2+2=10**. This also shows the 15-dimensional unmatched point and line modules cannot be mixed by a fully group-equivariant linear map.

**Constructive bonus: explicit 15D dark-state frame.** For the point and line collinearity adjacency matrices A=B B^T−4I and A'=B^T B−4I, the exact projector on their −4 eigenspaces is

    P_dark=(A−12I)(A−2I)/96=(8I−4A+J)/24.

It obeys P_dark²=P_dark, Tr P_dark=15, and B†P_dark=0 (point version) or B P_dark=0 (line version). Since every diagonal entry is 3/8, normalized projector columns give **40 unit real tight-frame vectors** spanning each 15D dark space, with Gram G=(8/3)P_dark. Their inner products are exactly −1/3 for distinct collinear points and +1/9 for noncollinear points. Thus G²=(8/3)G and every frame vector has exact zero coupling to the opposite 40-mode sector.

This also predicts a controlled perturbation: for the projector-column dark state centered at vertex 0, detuning a single incident edge by phase θ changes the line-sector infinitesimal leakage probability coefficient (in the chiral tight-binding dynamics with T=B) to

    P_line(t)= t²*(3/2)*sin²(θ/2)+O(t⁴).

An independent complex matrix calculation at θ=π/5 matches that expression to machine precision. This is an **actionable finite-Hamiltonian interference null**, not proof that such W33 coupling is realized physically. Tight frames from strongly regular graphs are established mathematical territory; no global priority claim is made.

**Interpretation:** W33's full finite symmetry produces an exact flat-band *obstruction*, not a unique three-family fermionic spectrum or unpaired 3+1D Weyl particle. The hypotheses are exact: linear one-body coupling, point/line native module, and preservation of the full group; zero energy also requires the chiral off-diagonal structure. Symmetry-breaking, gauge flux, other representations, nonlinear interactions and growing lattices may evade these finite constraints. Incidence spectra and representation theory are standard; this is an exact, auditable repo-specific consequence, not a new theory of nature.

Producer: analysis/w33_20261109_point_line_30_zero_modes.py

## 2. More probes beat minimum probes for estimating phase: Fisher information matters

The previous 25-or-21-probe forest calibration is information-theoretically sufficient for phase-only POVM inversion, yet its worst-case finite-shot confidence radius was poor. This round computes **the full click-plus-no-click classical Fisher matrix** for each known lossy 9x9 K_cal and phase-only K=K_cal diag(exp(i theta)), comparing:

- the maximum-overlap minimal observable spanning forest, with 9 computational probes + 2 per selected edge;
- all observable coherent input pairs, again with computational basis probes.

One gauge root per disconnected support component is removed; only physically observable relative phases are scored. Analytic derivatives use ∂p_click/∂theta_k = 2 Re(conj(amplitude) i K_jk exp(i theta_k) psi_k); the no-click derivative is the negative sum of the click derivatives. The Fisher matrices are normalized **per fixed total launched calibration pulse**, with equal allocation across each design's probes.

All ten contexts have positive nonsingular Fisher matrices on their gauge-fixed phase coordinates. The trace of the inverse Fisher matrix (A-optimal local phase variance lower bound) for the minimal tree divided by the redundant-pair design is:

    [2.427,1.238,1.295,1.137,1.242,1.558,1.124,1.194,1.144,1.336];

mean **1.3693**. Redundant pairs improve the local asymptotic variance in every tested context despite the extra configurations. But this is a **local Cramér–Rao lower bound**, not a rigorous finite-count calibration radius, a device-independent source calibration, or a proof that the dense design is globally optimal.

Producer: analysis/w33_20261109_phase_fisher_information.py

## 3. Four complete POVM architectures: optimistic entanglement-power versus calibration no-go

The previous noncommuting optical-loss construction explicitly modeled the full lossy nine-click-plus-no-click effects and computed a Cramér–Rao coefficient for the realignment/CCNR entanglement witness in the Horodecki a=.236 state. We now convert that *asymptotic information bound* to an **optimistic oracle-witness shot budget**: at one-sided test size alpha=.05 and nominal power=.95, assuming an asymptotically efficient unbiased estimator, the Gaussian benchmark requires

    N_source >= ceil((z_(1−alpha)+z_power)^2 * c / (Tr|realign(rho)|−1)^2),

with c=h^T F^−1 h per launched photon. The true trace norm separability excess is only 0.003058794098. The four ideal-device optimistic budgets are:

| Analyzer architecture | Minimum optimistic launched photon budget |
| --- | ---: |
| 12-context product MUB | 10,705,188 |
| 10-context Fourier/permutation | 12,235,095 |
| 10-context generic mesh | 14,122,041 |
| 10-context two-CZ local | 14,862,447 |

These are **optimistic lower budgets under an oracle efficient-estimator model**, not sufficient lab source counts or finite-shot certification. Calibration dominates: the earlier proof's dual row-sum amplification requires per-effect operator norm error **below 0.00016483** even with infinite physics shots. At 10^10 trusted calibration launches per probe/context, the 242-configuration phase-forest method rigorously allows operator error **0.014667**, approximately **89 times too large** for this certificate. So none of these source-shot figures alone establishes a usable calibrated Horodecki experiment. The oracle dual must be fixed independently, or adaptive witness-selection bias is another uncontrolled effect.

This is a concrete separation between the *statistical optical data budget* and the much harder *trusted device-identification budget*.

Producer: analysis/w33_20261109_oracle_ppt_optical_power.py

## 4. DES Y6: repeat live official survey acquisition gate, no S9 score

The original S9 preregistration in analysis/toe_uv/prereg_noshear.json remains frozen at **2026-11-08**. It requires the complete unblinded xi± shear vector with matching covariance, photo-z distributions, angular cuts, corrected scalar-field CLASS/Halofit theory predictions and fully matched nuisance likelihood for each competing model.

We reran the previously independently tested source-provenance audit **live** on the authorized Windows machine:

- official DES Y6 release portal: HTTP 200 HTML, not a verified unblinded full xi± FITS;
- official DES Y6 cosmology paper index: HTTP 200;
- historically indexed unblinded NCSA 3x2pt FITS candidate: **HTTP 404**;
- des-science/y6-ppd-public: HTTP 200; public statistical code, not the complete model likelihood dataset;
- des-science/y6-3x2pt public API lookup: HTTP 404;
- no complete official validated FITS plus covariance/n(z) and corrected CLASS/Halofit refits were obtained.

Independent literature confirms DES Y6 cosmic-shear cosmology is **scientifically published**. The cosmic-shear paper was accepted 9 October 2026, DOI https://doi.org/10.1103/fppy-s1pb, and reports NLA S8=0.798^(+0.014)_(-0.015). This published S8 is *not a valid stand-in* for our preregistered full vector and does not validate S9. Some public project pages state further data products are forthcoming: https://www.darkenergysurvey.org/des-y6-cosmology-results-papers/ . The public survey-independent MCP listing likewise marked the Y6 data-vector asset unavailable as of 2026-11-04, but that third-party listing is not an authoritative release record.

**S9 remains UNSCORED.** No new cosmological physical prediction was claimed.

Reexecuted live producer: analysis/w33_20261109_des_y6_official_link_audit.py
Frozen repeat: data/w33_20261109_des_y6_repeat_public_audit.json

## 5. Displaced single-photon Bell test: parameter robustness fails

The previous optimizer for local displacement followed by on/off photon detection found a nominal CHSH absolute value 2.021789903 in a *specific synthetic* system with detector efficiency eta=.86, relative phase coherence gamma=.92, full source survival and dark mean 1e-4. Such a ~0.022 violation could vanish under small parameter shifts.

This round **holds the optimized displacements fixed** rather than covertly reoptimizing a different device, and evaluates 16 extreme combinations from eta ∈{.85,.87}, gamma∈{.91,.93}, source survival∈{.98,1.0}, dark count per trial∈{0,.0002}. The pessimistic tested corner eta=.85, gamma=.91, survival=.98, dark=.0002 yields

    |CHSH| = 1.9034733435 < 2.

A separate 8-real-variable differential evolution reoptimization of the pessimistic corner (seed controlled, max 120 generations) gave 1.906517354, still below two. The *nominal* CHSH margin would need at least **807,612 independent trials** in a conservative ideal-IID Hoeffding size=.05, power=.95 schedule; the pessimistic model has no positive-violation sample budget, no matter how large N. Corner sampling is **not proof** of a global continuous-box worst case. The previous ideal displaced-on/off 2.6884 result is published prior art (Christoph Wildfeuer, arXiv:2607.29012), not our discovered inequality.

No actual two-party spacelike Bell apparatus or independent calibration was run. The experiment requires explicit local oscillator/reference photons, heralding, full outcome/no-click accounting, detector and mode-overlap calibration, source loss and independent spacelike choices.

Producer: analysis/w33_20261109_onoff_bell_robust_envelope.py

## Five independent next physics/engineering problems

1. **Anomaly-free dynamics beyond rank-10 centralizer:** Construct explicit W33-derived larger representations and *interacting/gauge-covariant* kinetic operators with a chiral index unlike the native point/line balanced 15+15 nullspace; prove anomaly cancellation and compare to realistic fermion masses, not just representational counts.
2. **Guaranteed calibrated quantum-witness coverage:** Joint likelihood fit for interferometer amplitudes/phases/losses with finite-shot confidence, stationary held-out controls and robust CCNR dual selection, reducing the 89x systematic uncertainty gap.
3. **Photonic readout Pareto envelope:** Introduce detector dead-time, independent source brightness, switching duty cycle, local oscillator photon resources, fabrication footprint, and finite-shot exact/non-Gaussian witness power into four-way optimization.
4. **DES S9 frozen test from actual artifacts:** Acquire complete official unblinded data vector/FITS, full covariance, n(z), cuts and corrected CLASS/Halofit refits. Keep currently UNSCORED and never score the published S8 summary.
5. **Causal Bell test under calibrated worst-case loss:** Design and test phase-reference delivery with actual mode match and 98–100% source survival, detector efficiencies and dark counts; certify space-time setting independence and all trials.

## Reproducibility

Run in repository root:

    py -3 -m unittest discover -s tests -p test_w33_20261109_toe_beyond_five.py -q

The tests validate exact 160/1440 cross orbits, 10-dimensional commutant, generic/special chiral nullspaces, full POVM gauge-fixed Fisher non-singularity, oracle optical budgets and their large calibration shortfall, independent on/off Bell scenario, and DES fail-closed S9 gate.

**Scientific boundary:** This pass rules out particular oversimplified TOE hypotheses under explicitly stated assumptions. No spacetime, gravity, fundamental constant, physical chirality or observed single-photon universality is derived. A rigorous negative constraint can be more valuable than an attractive but unsupported identification.
