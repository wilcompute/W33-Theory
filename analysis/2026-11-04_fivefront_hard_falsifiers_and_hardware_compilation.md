# Five TOE hard falsifiers: spectral refinement, C3 dynamics, gravity constraint zero set, vectorlike CP, and Lindblad Ramsey

**Date:** November 4, 2026 UTC (November 3 US Eastern).
**Status:** finite mathematical certificates and idealized numerical quantum simulations; **NOT** a theory of everything, physical spacetime construction, Einstein dynamics, measured flavor, or experimental hardware data.

**Producer:** analysis/toe_20261104_fivefront_hard_falsifiers.py
**Certificate:** data/toe_20261104_fivefront_hard_falsifiers.json
**Regression:** tests/test_toe_20261104_fivefront_hard_falsifiers.py

## Cross-check against repository and parallel work

Prior owner at ff6d8322f: analysis/2026_11_03_optimal_5load_apartment_hamiltonian.py establishes a GF(2)-independent 81-cycle load-five basis. analysis/toe_20261103_c3_symmetry_selector.py establishes 81-cycle C3-invariant bases at max load six. analysis/toe_20261103_c3_tightframe_fusion.py fuses three frames (condition 6.997802; 4320 hopping pairs). analysis/toe_20261103_continuum_gravity_flavor_ramsey.py establishes the first subdivision limit, pairwise Poisson failure, proportional flavor no-mixing, and clean Ramsey triangle.

Parallel commit 659d352f includes a separate cosmology program (weak-lensing and N-body controls). Those results are conditional, do not derive the W33 spacetime or particles, and are not imported as physical validation.

This round extends the specific calculations rather than claiming novelty for general quantum graphs, frame theory, E6 vectorlike mixing or synthetic-flux interferometry.

## 1. Exact finite-size law of W33 edge subdivision

The W33 Levi graph has 80 vertices, 160 edges and valency four. Its positive nonconstant adjacency eigenvalue nearest four is mu=sqrt(6). Replace each original edge by L unit graph edges. The new graph has V(L)=80+160(L-1), E(L)=160L and first Betti number E-V+1=81 for every L.

For the first positive combinatorial graph-Laplacian eigenvalue lambda=2[1-cos(theta)], elimination of interior segment amplitudes yields the exact characteristic equation:

    sqrt(6) = 4 cos(L theta) + 2 tan(theta/2) sin(L theta).

Set alpha=acos(sqrt(6)/4). Expansion of the small positive root yields theta=alpha/L + alpha/(4L²) + O(L^-3), hence the **first finite-size correction**

    L² lambda_1(L) = alpha² [1 + 1/(2L) + O(L^-2)].

alpha²=0.8312667112181387. Certified roots: L=32 -> 0.84438869879; 64 -> 0.83779413695; 128 -> 0.83452210998; 256 -> 0.83289234164. The dimensionless correction coefficient L*(L²lambda/alpha²-1) is 0.500635 at L=256, approaching 1/2.

**Boundary:** The limit remains a one-dimensional finite metric graph with 81 topological cycles, not an emergent 3+1 Lorentzian continuum. The edge-to-vertex spectral relation is an established equilateral quantum-graph technique: https://kups.ub.uni-koeln.de/73182/1/weller_NumPDEMeGra_dissertation_24.pdf ; https://link.springer.com/article/10.1007/s00023-021-01077-6 .

## 2. Optimize an exactly C3-equivariant three-frame Hamiltonian without more couplers

Take the previously certified H5=B5B5^T, H9=B9B9^T, H18=B18B18^T, each positive semidefinite, cycle-cut decoupled and invariant under the same C3. Optimize weights w_i>0 with sum_i w_i=3. Five deterministic local optimizer starts produce the best sampled weights:

    (w5,w9,w18) = (0.8539646429, 0.9375553708, 1.2084799863).

Nonzero-sector condition drops from 6.9978021402 at equal weights to **6.8470924516** (a factor 1.02201). The weighted and unweighted operators have the same **4320 undirected nonzero hopping pairs** and max 72 offdiagonal neighbors. Exact C3 invariance and cycle-cut decoupling hold for all weights, since they hold separately for each Hi. The optimized weights have no established physical origin; sampled local optimum does not imply a global optimum.

Control: With C comprising all 1620 signed apartments, exact integer K=C C^T satisfies K²=160K, thus K=160 P_cycle and condition number one. However K has **12720 nonzero undirected hoppings**, coupling every one of the 160 flag modes to all 159 others. This identifies the price of a fully symmetric scalar projector in the native flag basis. Dense spectral perfection is not local continuum dynamics.

## 3. A global gravitational obstruction: the 81 positive Hamiltonian densities impose pure gauge

Previous work showed that two proposed local quadratic densities have a nonzero Poisson bracket on Gauss=0. Now impose all 81 densities simultaneously:

    h_i(x,p) = (c_i.x)^2/2 + sum_{e in support(ci)} p_e²/2.

The 81 cycle columns B span ker D, rank(D)=79, rank(B)=81, DB=0, and every edge occurs in at least three cycles. Since every term is a nonnegative square, all h_i=0 implies p_e=0 on all 160 edges and B^T x=0. Since im D^T=(ker D)^perp, x=D^T phi. The converse holds identically.

**Theorem for this ansatz:** the common zero set is exactly {(x,p): x=D^T phi, p=0}. After quotient by Abelian Gauss shifts x→x+D^T epsilon, there is one gauge orbit and **zero nontrivial physical degrees of freedom**. This is a no-go for interpreting THESE positive quadratic densities as a complete gravitational Hamiltonian constraint system, not a no-go for GR, Regge, indefinite ADM or other dynamical actions.

External background on broken discrete diffeomorphism constraints: https://arxiv.org/abs/0905.1670 and https://research-portal.uu.nl/en/publications/from-covariant-to-canonical-formulations-of-discrete-gravity/ .

## 4. E6 flavor: vectorlike Schur complement gives an exact CP-odd counterexample

The previous one-spurion theorem applies when effective Yu=aY and Yd=bY are proportional. A vectorlike sector can supply an *additional* independent flavor-sensitive mixing vector even with one bare Yukawa matrix.

Construct a complex symmetric four-state toy block:

    M_block = [[Y, v], [v^T, 3]],
    Y=diag(1,2,4), v=(1,1,1+i)^T.

Eliminate the heavy block: Yd_eff = Y - vv^T/3. SymPy verifies the Schur determinant identity det(M_block)=3 det(Yd_eff). With Yu=Y, define Hu=Yu Yu†, Hd=Yd_eff Yd_eff†, and compute EXACTLY

    Im Tr([Hu,Hd]^3) = 1600.

Replace v with a real vector: CP invariant=0. Complex-conjugate v: CP invariant=-1600. Thus independent vectorlike mixing can make effective CP-odd flavor dynamics possible. It does NOT derive the extra mixing vector, realistic gauge charges, Higgs vevs, observed quark masses or CKM.

**Prior-art boundary:** Actual E6 Nelson-Barr/vectorlike flavor constructions already exist and require full gauge-invariant sectors, e.g. https://doi.org/10.1140/epjc/s10052-018-6388-6 and the two-Yukawa analysis https://arxiv.org/abs/1504.00904 . This exact 4x4 witness is a conditioned model, not a novel general mechanism.

## 5. Phase-sensitive 3-site hardware: Lindblad noise plus an elementary pulse schedule

Use a five-dimensional Hilbert space: idle reference |r>, three triangle modes |0>,|1>,|2>, and loss vacuum |vac>. Initialize (|r>+|0>)/sqrt(2). The triangle Hamiltonian H+ has positive equal offdiagonal hopping, and H- has one negative link (pi flux). Per triangle site j use legitimate Markovian Lindblad jumps:

    L_loss,j = sqrt(gamma) |vac><j|,
    L_deph,j = sqrt(kappa) |j><j|.

Evolve the 25x25 Liouvillian exactly (the five-state density matrix). Measure phase-sensitive Ramsey signal |2 Im(rho_(r,0,+)-rho_(r,0,-))| at dimensionless t=0.4:

| gamma | kappa | Ramsey contrast |
| ---: | ---: | ---: |
| 0 | 0 | 0.04098706248 |
| 0.1 | 0 | 0.04017546426 |
| 0 | 0.1 | 0.04017546426 |
| 0.1 | 0.1 | **0.03937993677** |
| 0.5 | 0.2 | 0.03563244031 |

The chosen jump model keeps triangle site-population differences below numerical roundoff and preserves trace/positivity, while the coherent idle arm detects flux. Real reference-arm instability and detector imperfections are NOT included.

Compile the continuous Hamiltonian via three signed two-mode hopping pulses per slice:

    U_n = [U_01(t/n) U_02(t/n) U_12(t/n)]^n.

| Trotter slices n | edge pulses | Ramsey contrast error |
| ---: | ---: | ---: |
| 1 | 3 | 0.04098706 (false negative: signal zero) |
| 2 | 6 | 0.01024053 |
| 4 | 12 | 0.00255965 |
| 8 | 24 | 0.00063988 |
| 16 | 48 | 0.00015997 |
| 32 | 96 | 0.00003999 |
| 64 | 192 | **0.000009998** |

The Ramsey observable error displays approximately n^-2 convergence for this t even though the full unitary-entry error decreases only as n^-1. This is an observable-specific numerical finding, NOT a general Trotter error theorem. More pulses may make physical noise worse. Hardware sources include synthetic gauge fields in superconducting platforms, https://doi.org/10.1038/s41567-024-02661-3 , and quantum-graph transport, https://doi.org/10.1063/5.0239742 .

## Claim layers, falsifiers and further independent gates

**Exact:** integer cycle/edge identities, full apartment scalar projector, zero-locus proof, SymPy Schur complement and CP signs, each component's C3 symmetry. **Numerical:** frame-weight optimization, continuum roots, Lindblad exponential and pulse sequence approximation. **Not established:** actual spacetime dimension, Einstein action or constraint algebra, particle masses/chirality, physical symmetry-selection dynamics, quantum hardware implementation or a TOE.

Top independent physical gates:
1. Obtain four-dimensional Lorentzian spacetime as a stable output of a local higher-cell rewrite action, not by prescribing a product of four circles.
2. Derive frame weights and a coupler cost from a justified local dynamical action; allow operator-valued/feedback selection and check stability against disorder.
3. Construct action-derived indefinite gravitational constraints with lapse, shift and a first-class algebra; test nonlinear consistency and continuum closure.
4. Embed vectorlike CP mixing in a gauge-complete E6 model with viable anomalies, predictive parameter count, vacuum selection and out-of-sample CKM/mass tests.
5. Translate the three-coupler pulse schedule and idle reference into device-native hardware with timing, control-phase calibration, reference noise, detector infidelity and pulse-count optimization.


## 6. EXTRA hardware gate: sequential Lindblad pulse overhead selects finite depth

The ideal Trotter signal error improves monotonically with depth, but physically sequentially toggling three couplers consumes three intervals of duration t/n per slice. For n slices the active exposure is 3t, *not* the simultaneous-Hamiltonian t; and a fixed per-edge-pulse dead-time contributes another 3n tau to the sequence. A naive noiseless n=64 recommendation is not robust.

The producer now propagates the full five-state trace-preserving Lindblad channel through each of the three individual link pulses, repeating n times, with gamma=kappa=0.1 and a per-pulse idle/dead time tau=0.003 (same dimensionless units as t=0.4). The reference target is the simultaneous-coupler Lindblad signal at time t, 0.0393799367712. Unlike the noiseless pulse model, this **includes dissipative evolution during every sequential link window and every dead-time window**.

| n | signed-edge pulses | measured coherent contrast | absolute error vs simultaneous noisy target |
| ---: | ---: | ---: | ---: |
| 1 | 3 | 0.000000 | 0.039380 |
| 2 | 6 | 0.027221 | 0.012159 |
| 4 | 12 | 0.033960 | 0.005420 |
| 8 | 24 | 0.035528 | 0.003852 |
| 16 | 48 | 0.035693 | **0.003687** |
| 32 | 96 | 0.035286 | 0.004094 |
| 64 | 192 | 0.034309 | 0.005071 |

Thus **16 slices (48 edge pulses) minimize the tested error** within this explicit restricted grid. Deeper sequences become worse as accumulated dead time and decoherence overwhelm the Trotter approximation gain. At n=64 the loss-vacuum occupation grows to about 0.0814 vs about 0.0629 at n=16. This is a finite-grid software optimization, not a globally optimal hardware pulse depth; the entire comparison is conditioned on the assumed rates, perfect idle reference, no cross-talk and physical time accounting. Coherent parallel coupler activation would have a different budget.

The general experimental lesson is that a phase-flux witness must optimize **signal-to-noise and physical wall-clock time**, not just an isolated Hamiltonian simulation norm. No real equipment was accessed or measured in this round.
