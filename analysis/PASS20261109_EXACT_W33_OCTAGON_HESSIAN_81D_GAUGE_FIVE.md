# W33 TOE — exact octagon gauge–fermion Hessian and five experimental falsifiers

**Research date:** November 9, 2026 (US Eastern; local logs may read November 10 UTC).
**Repo:** wilcompute/W33-Theory, master.
**Status:** One NEW exact finite-matrix theorem with complete integer certificates; one specified 81-dimensional variational gauge search; three conditional engineering/quantum tests; and one held-out cosmology source audit. **Not a derived theory of everything.**

## Executive result: exact W33 gauge–fermion quadratic response

The 80-node W33 point–line incidence graph has 160 links, 1,620 shortest 8-cycles and an 81-dimensional graph-cycle space. The 40×40 incidence matrix B at flat phases has singular spectrum (4)^1, (sqrt 6)^24, (0)^15. Prior November 9 results established 30 paired dark modes, the exact 15-link phase-only removal theorem, and a complete 78+3 unimodular octagon basis. October TOE38/TOE61 already supplied the three-deck topology and an *eight-sector-only* free-energy flux ordering. These are prior corpus, not novel claims of this note.

Let each of the 160 W33 incidence entries carry a U(1) phase φ_e and let C8 be the **1,620×160 signed integer matrix** recording oriented edge crossings of every shortest eight-edge graph cycle. Define

    P(t,φ) = det(I_40 + t B(φ) B(φ)†).

**EXACT THEOREM**, at flat φ=0 and every positive real t:

    Hess_φ log P(t,φ) |flat
         = [2 t^4 / ((1+16t)(1+6t)^2)] * C8ᵀ C8.

Consequences:
- rank(C8)=81, hence 81 physical positive quadratic directions and 79 pure-gauge zero directions of C8ᵀC8.
- For the half-filled zero-chemical-potential spinless finite fermion model, F_β(φ)=−(2/β)Σ_{j=1}^40 log[2 cosh(βσ_j(B(φ))/2)], the Weierstrass product gives

      Hess_φ F_β |flat = −κ_c(β) C8ᵀ C8,
      κ_c(β) = (4/β)Σ_{n>=0} t_n^4/[(1+16t_n)(1+6t_n)^2],
      t_n = β²/[π²(2n+1)²].

- Add the **specific all-octagon** positive compact magnetic Wilson action S_mag=κ Σ_{C∈1620}(1−cos Φ_C), κ>0. Its flat Hessian is κ C8ᵀC8. Therefore **the exact physical-coordinate quadratic response** is

      Hess(F_β+S_mag)|flat = [κ−κ_c(β)] C8ᵀC8.

- At β=1, κ_c≈0.0000622556774268. The flat sector is a strict **local minimum up to gauge** if κ>κ_c; it has unstable physical directions if 0≤κ<κ_c. At κ=κ_c the quadratic approximation is degenerate: quartic and higher terms decide local stability. This is not global minimization or a thermodynamic phase transition.
- At β=.3,.5,1,2,5,10, independent full 81D numerical Hessian directional tests reproduce the single-link Matsubara coefficient with strong agreement. The β=.1 signal is extremely small and roundoff limits its relative accuracy.

### Exact integer proof/certificate

**Producer:** analysis/w33_20261109_exact_octagon_hessian_theorem.py
**Data:** data/w33_20261109_exact_octagon_hessian_theorem.json
**One-edge producer:** analysis/w33_20261109_one_edge_flux_poly_curvature.py

1. The W33 association-scheme projectors for eigenvalues 0,6,16 of BBᵀ are 120P0=40I−20A+5J; 120P16=3J; 120P6=120I−120P0−120P16, with A=BBᵀ−4I. The script verifies their integer projector equations exactly.
2. Write Q=(I+tBBᵀ)^−1=N/(120D), where D=(1+16t)(1+6t) and N=D(120P0)+(1+16t)(120P6)+(1+6t)(120P16). N is an integer matrix polynomial of degree≤2 in t.
3. For phase variables on edges e=(p,l), f=(r,m), Jacobi's formula gives

     Hess_ef log P =
       −2t δ_ef (QB)_{p,l} + 2t δ_{l,m} Q_{p,r}
       +2t²[(QB)_{r,l}(QB)_{p,m}−Q_{p,r}(BᵀQB)_{l,m}].

4. Multiply both sides of the proposed identity by 120²D²/(2t). The resulting entries of the difference are **integer polynomials in t of degree at most 5**. Their proposed right-hand side is 120² t³(1+16t)(C8ᵀC8)_{ef}.
5. The script calculates the **entire 160×160** cleared-denominator difference for integer t=1,2,3,4,5,6; every one of the 25,600 entries equals zero at each of the six points. All intermediate integers are checked to lie comfortably within signed 64-bit bounds. Six roots of a degree≤5 polynomial imply the difference vanishes identically for all complex t, and by continuity for t=0. This proves the rational Hessian identity, not merely a numerical fit.

Independent sanity check: changing just one edge to phase π gives exactly

    P_π(t)−P_0(t)=324 t^4(1+6t)^22,
    P_0(t)=(1+16t)(1+6t)^24.

An arbitrary single-edge phase has P_θ(t)=P_0(t)+[|e^(iθ)−1|²/4] (P_π(t)−P_0(t)). Because 81 shortest octagons contain each link, the single-edge Hessian yields the same κ_c(β) independently. Producer: analysis/w33_20261109_one_edge_flux_poly_curvature.py. Strict novelty claims are limited to this exact W33-specific identity in the checked corpus; Jacobi, Weierstrass, spectral projectors and Wilson loop actions are standard tools.

## Front 1 — gauge + matter over all 81 continuous U1 coordinates

**Producer:** analysis/w33_20261109_full_u1_variational_vacuum.py
**Data:** data/w33_20261109_full_u1_variational_vacuum.json

Fix a spanning tree, parametrizing all 160 link phases by 81 gauge-invariant chord phases x. The optimized explicit model is

    J_κ(x) = −2 Σ_{j=1}^40 log[2 cosh(σ_j(B(x))/2)]
            + κ Σ_{1,620 octagons} [1−cos((C8 x)_C)].

The analytic gradient includes the exact spectral derivative of the fermion singular values and the Wilson sin(curl) term; finite-difference checks pass. Multistart L-BFGS-B optimization at β=1, with flat, both 15-link sectors and independent random phase seeds, yields these **trial-state upper bounds on the unknown global minimum**:

| κ | smallest energy discovered | flat reference |
| ---: | ---: | ---: |
| 0 | −87.72148006 | −87.59344827 |
| 0.00001 | −87.70166050 | −87.59344827 |
| 0.00005 | −87.62575371 | −87.59344827 |
| 0.0001 | −87.59344827 | −87.59344827 |
| 0.001 | −87.59344827 | −87.59344827 |
| 0.01 | −87.59344827 | −87.59344827 |

At κ=0 the best numerical candidate **did not fully converge** within its iteration limit (gradient sup ~4.45×10^-4). All above energies nevertheless correspond to explicitly generated feasible link-phase vectors, and thus are valid sampled values. The κ=.0001 flat outcome is **not** proof of global minimality; for κ=.00005 a found competing state numerically exhibits an objective below flat, subject to floating-point evaluation error. The exact theorem above certifies only local flat stability, which is stronger than interpreting numerical convergence as global physics.

This action includes 238 shortest octagons that wind the TOE38 three-deck cover; it should not be conflated with the TOE38 spatial-local 1,382-plaquette theory. No physical gauge coupling, Hamiltonian kinetic term or time-evolution law is derived.

## Front 2 — physical chiral index and added boundary-defect obstruction

**Producer:** analysis/w33_20261109_boundary_chiral_index_falsifier.py
**Data:** data/w33_20261109_boundary_chiral_index_falsifier.json

The finite bipartite Hamiltonian H(T)=[[0,T],[T†,0]] anticommutes with Γ=diag(+I_{n_p},−I_{n_l}). Its exact chiral index is dim ker(T†)−dim ker(T)=n_p−n_l, independent of flux. Therefore **every square W33 40×40 coupling has net index ZERO**, even at the fully gapped 15-link state. No unpaired 3+1D Weyl fermion can be inferred from its original balanced zero-mode multiplicities.

As a constructive alternative, append one physical point row with four unit-modulus couplings to the gapped 40×40 matrix. The 41×40 full-column-rank system has exactly ONE protected point-sector zero mode; an analytic null vector solves T†x+u†=0. Numerical random phase disorder preserves the index. This is a **sublattice-imbalance boundary defect** inserted as an extra primitive, not a dynamically derived SM chirality carrier, a 3D continuum, or anomaly cancellation. Its existence shows which ingredient a nonzero index minimally requires.

Literature no-go: Nielsen–Ninomiya, https://doi.org/10.1016/0370-2693(81)91026-1 ; finite bipartite sublattice imbalance is elementary linear algebra.

## Front 3 — photonic dark-state falsifier under actual serial 39-stage preparation loss

**Producer:** analysis/w33_20261109_photonic_loss_robust_null.py
**Data:** data/w33_20261109_photonic_loss_robust_null.json

Prior work compiled a 40-port end-fed 1D nearest-neighbor chain, necessarily depth 39, to prepare a target W33 point-dark state (3/8 intensity central, 1/24 each on 12 neighbors, 1/216 each on 27 other points). At **99% intensity survival on each addressed two-port coupler**, the model has input source survival 0.90449878 and normalized target fidelity 0.99748132. The earlier ideal-input photon dark-null model predicted strong 14/15-link leakage and much weaker 1-link leakage.

Here use a genuine worst-case state-distance propagation: if normalized pure preparation fidelity is f, then for ANY subsequent ideal unitary graph evolution and measurement effect, |p_real−p_ideal|≤sqrt(1−f); for the null ideal dark state, actual line probability ≤1−f. Include assumed source throughput, 85% detector efficiency and independently bounded dark-click interval [.0008,.0012] per launched trial.

**Negative result:** The fidelity f=0.99748 produced by 0.99 coupler transmission is not sufficient to **certify separation of the one-link alternative from the flat null** under this conservative calibration-only envelope, no matter how many counts are collected. The physical one-link experimental prediction cannot inherit the optimistic ideal 793-trial result without improved state preparation or more detailed independently validated error structure. The 14- and 15-link alternatives remain distinguishable in the envelope. The minimum per-addressed-pair intensity survival in this one-link fidelity-only model is **0.9979317859**, not a universal physical detector threshold.

All numbers concern a simulated ideal 80-mode graph after preparation, and ignore graph-internal phase drift, nonuniform Hamiltonian loss, chip routing, causal separation, and independent hardware calibration. No lab device was built.

## Front 4 — calibrated Q8 mixed-state Schmidt-number witness with launch budgets

**Producer:** analysis/w33_20261109_robust_q8_schmidt_photon_counts.py
**Data:** data/w33_20261109_robust_q8_schmidt_photon_counts.json

Prior repo proved for any two-qutrit mixed state the eight-basis collision witness F8 and exact Schmidt-number bounds:
- F8 >4/9 certifies entanglement, i.e. Schmidt number≥2.
- F8 >7/9 certifies Schmidt number3.

This pass adds **conditional finite-shot calibration and expected source-launch accounting**, not a new general Schmidt-number theorem. Assume eight settings with nine *complete, exclusive* detected outcomes per accepted preparation, independently calibrated **uniform mislabel response** q_base=(1−r)p+r/9 with r true .01 and certified in [.0095,.0105]. Assume the full residual deviation satisfies |qactual_bj−qbase_bj|≤2×10^-5 in each basis/outcome for all states; this is HYPOTHETICAL and was not physically established.

For any two complete categorical distributions p,q, |Σ_j p_j²−Σ_j q_j²|≤||p−q||_1, and therefore the systematic collision uncertainty over eight nine-outcome bases is ≤72 ε. Under uniform mislabeling F8(qbase)=(1−r)² F8(p). For M independent **accepted two-photon collision pairs per basis**, Hoeffding gives one-sided Pr(Fhat8−F8>=z)≤exp(−M z²/4). Combining independent readout calibration, a 5%-size lower confidence bound and 95%-power requirement yields conservative state-dependent accepted-pair budgets:

| Isotropic state mixing η | Schmidt 2 (entanglement), M per basis | Schmidt 3, M per basis |
| ---: | ---: | ---: |
| .80 | 3,324 | not certifiable by this bound |
| .94 | 435 | 1,717,931 |
| .95 | 395 | 101,343 |
| .99 | 277 | 6,004 |

An accepted collision pair requires two separately launched preparations. With hypothetical independent uniform detected-pair efficiency 0.85², the **expected total launched source preparations** are 16M/0.85², not 8M. Outcome-dependent detection invalidates the conditioning model: a synthetic efficiency profile reweights one basis by total variation (L1) 0.11111, far beyond the tiny certified tolerance. All these photon budgets depend on a stipulated calibration certificate, not actual measurements. They are neither device-independent Bell tests nor direct PPT-Horodecki certification.

Prior MUB Schmidt witnesses and finite-sample tomography confidence regions: https://doi.org/10.1038/s41534-025-00990-6 and https://doi.org/10.1103/PhysRevA.109.062417 .

## Front 5 — frozen S9 cosmology audit

**Existing source-audit rerun:** analysis/w33_20261109_s9_frozen_manifest_attack.py.
**Immutable preregistration:** analysis/toe_uv/prereg_noshear.json, frozen 2026-11-08, SHA256 over claim text 70951becb3bfe08644e11c56c6cf5939b8970b554810665f5fc60bd6525173da.

The authorized Windows machine again inspected three official DES Y6 public data/archive pages. Each returned HTML status 200; the automated release listing contained no authenticated complete unblinded DES Y6 xi± shear data vector and matching covariance, published digest, matching n(z), corrected scalar-field CLASS/Halofit predictions, and nuisance-refitted four-model comparison. Five deliberately invalid provenance manifests were rejected. **S9 remains UNSCORED**: published DES Y6 LCDM and wCDM summaries do not evaluate the frozen scalar-field prediction. DES reports further Y6 data-product releases pending: https://www.darkenergysurvey.org/des-y6-cosmology-results-papers/ . A public DES Y6 PPD code repository describes how to prepare a chain with full 2pt theory elements, but does not itself supply the required authenticated unblinded data and corrected fading-scalar model refits: https://github.com/des-science/y6-ppd-public .

## Reproducibility, controls, limitations

The new focused regression file is tests/test_w33_20261109_full_u1_hessian_five.py. It independently rechecks all six 160×160 integer-polynomial identities, 81-chord gradient finite differences, individual exact one-edge determinant factors, local Matsubara-vs-81D Hessian threshold, chiral boundary index, real serial-source loss, robust Q8 Schmidt budgets and frozen DES null. The original seven-front and 15-link/minimal phase-flux tests should also be rerun from the primary Windows checkout.

The finite model uses one chosen beta, dimensionless hoppings, user-chosen kappa and graph cycles. None produces physical 3+1D spacetime, gauge bosons, SM flavor representations, a calibrated photonic Bell violation or the measured values of physical constants. Avoid taking a local bifurcation of one finite action for a thermodynamic phase transition. Lieb's flux theorem requires lattice symmetries not automatically possessed by W33: https://doi.org/10.1103/PhysRevLett.73.2158. A 2026 fermion+Z2 lattice-gauge stability study has different assumptions: https://doi.org/10.1007/s10955-026-03617-y .

## Top five independently valuable next TOE research directions

1. **Globally certify the true gauge vacuum.** Convert the 81-chord U1 optimization into a rigorous lower-bound / branch-and-bound or special analytic gauge-action theorem, comparing **both** the spatially local 1,382-plaquette and all-1,620-octagon actions. Identify which shortest loops are physically local in any realizable 3D embedding.
2. **Construct real 3+1D chiral matter.** Go beyond balanced finite index zero and boundary-row tricks: specify a sequence of local growing graphs / overlap or domain-wall operators with protected net chirality, exact anomaly cancellation, realistic dispersion and independent low-energy predictions.
3. **Build an optical full-device falsifier.** Compile source-to-detector 80-mode mesh, implement measurable flux controls, quantify gate-dependent state-preparation errors, route count, internal loss and phase drift. Demonstrate directly measured spectral gap at 14 versus 15 pi-edge flips without relying on fixed-state leakage as a rank witness.
4. **Establish real detector/state calibration.** Replace hypothetical categorical-response residuals with independently sampled calibration probes, confidence regions, joint no-click POVM model, and outcome-dependent efficiency controls. Prove robust Schmidt number or PPT entanglement from independent data and a pre-fixed inference pipeline.
5. **Close an unchanged held-out observational likelihood.** Acquire authenticated Y6 shear vector, matching covariance and n(z), correct scalar-field nonlinear theory and identical nuisance refits, then score the frozen S9 comparison exactly once; retain and report null results.

**Conclusion:** An exact finite W33 identity links the complete fermionic gauge susceptibility to the Gram matrix of its 1,620 octagon cycles at every spectral parameter, and yields a non-arbitrary **model-internal** temperature-dependent flat-stability coupling. Whether nature uses this geometry, these cycles or this action remains open; the work is an exact testable mathematical component, not a TOE.
