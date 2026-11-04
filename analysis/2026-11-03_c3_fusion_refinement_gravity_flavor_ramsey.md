# Independent five-front TOE follow-through: C3 apartment fusion, metric-graph refinement, gravity bracket, E6 flavor, phase-sensitive hardware

**Date:** 2026-11-03. **Classification:** exact finite mathematical witnesses + numerical controlled toy experiments. **Not a complete TOE**. No derived 3+1 Lorentzian spacetime, general relativity, light speed, observed masses/mixing, measured flux or hardware experiment.

**Producers**
- analysis/toe_20261103_c3_symmetry_selector.py
- analysis/toe_20261103_c3_tightframe_fusion.py
- analysis/toe_20261103_continuum_gravity_flavor_ramsey.py

**Certificates**
- data/toe_20261103_c3_symmetry_selector.json
- data/toe_20261103_c3_tightframe_fusion.json
- data/toe_20261103_continuum_gravity_flavor_ramsey.json

**Regression**
- tests/test_toe_20261103_c3_fusion.py
- tests/test_toe_20261103_continuum_gravity_flavor_ramsey.py

## Repo intake and ownership

The prior audited baseline is commit 2b5d253ab, which added 81-apartment load-five H=BB^T and conditional locality/flat-band controls, a 33-seed condition-number search, a local gauge-bracket counterexample and signed triangle census. Earlier BT545-BT551 and BT744 own the first Betti rank 81 and the apartment/Steinberg frame, with 1620 W33 Levi apartments. The local Maxwell 2-complex was addressed in analysis/w33_20261010_toe38_local_maxwell_2complex.py. Existing symplectic and transvection studies include analysis/w33_pass4472_4479_apartment_module_thermo_ihara_pauli.py and analysis/w33_20261022_allfive_deeper_frontiers.py. Existing linear ADM and Regge-like controls include analysis/w33_pass11620_11624_covariant_pair_vacuum.py, and the E6 anomaly baseline is analysis/w33_20261019_round13_chiral_anomaly_27.py.

The **new** finite certificates specifically provide (i) a C3-invariant shortest-apartment basis with explicit congestion six; (ii) three-frame invariant spectral equalization; (iii) actual edge-subdivision convergence towards a one-dimensional metric graph; (iv) a closed symbolic overlap law for the naive local Gauss-constraint failure; (v) a single-Yukawa flavor no-go and two-spurion CP witness; (vi) a phase-sensitive and disorder-controlled pi-flux triangle measurement. Do not claim general priority of frame averaging, quantum graph spectra, E6 flavor structure or synthetic gauge interferometry.

## A. Transvection symmetry selection: an 81-cycle C3-equivariant basis exists

Use symplectic projective T_v(x)=x+<x,v>v for the first normalized nonzero v in GF(3)^4. On the native Levi building this order-three symmetry fixes exactly 13 of the 40 points, 4 of the 40 isotropic lines, 16 of the 160 incidence flags. The chain-complex trace identity yields:

trace(T|H1) = trace(T|C1) - trace(T|C0) + trace(T|H0)
            = 16 - (13+4) + 1 = 0.

For an order-three rational action on the 81-dimensional carrier, that character is 27 regular C3 representations (27 trivial eigenvalues and 27 conjugate pairs of nontrivial roots). All 1620 apartments form 540 support-orbits of length three, no fixed apartment supports for this T. A deterministic orbit-by-orbit GF(2) elimination with seed 2 selects 27 complete three-orbits, an independent 81-apartment basis, maximum per-flag participation **six**. Signed cycle matrix B satisfies D B=0; H=BB^T satisfies H D^T=0, Aflag H=-2H and exact T H T^T=H. The orbit basis carries 1985 offdiagonal undirected coupling pairs and numerical condition number 4537.986. This is non-scalar, *not* a dynamical reason for nature to select this transvection.

**No claim that maximum load six is necessary for an invariant basis.** A 0-1 incidence-feasible 27-orbit selection with load five exists without GF(2) rank guarantee; proving feasibility/infeasibility with the rank requirement is open.

External finite-building context: https://link.springer.com/article/10.1007/s00029-025-01051-8 .

## B. New frame-fusion route: keep C3 and improve conditioning by ~182x

Independently generated symmetry-closed 81-cycle bases at seeds **5, 9, 18** all have maximum flag participation six and GF(2) rank 81. Form the positive semidefinite local operator H_fused = B5 B5^T + B9 B9^T + B18 B18^T. Exact integer tests check H_fused D^T=0, D H_fused=0, T H_fused T^T=H_fused, and each constituent cycle is eight-edge supported.

| Construction | Condition number | Nonzero undirected hoppings |
| --- | ---: | ---: |
| Baseline seed33 load-five | 1272.31099 | 1896 |
| Two equivariant frames, seeds 5+13 | 14.10574 | 3267 |
| Three equivariant frames, seeds 5+9+18 | **6.99780214** | **4320** |

The fused Hermitian 81D active spectrum lies numerically from 7.6990176 to 53.8762019. Its interaction graph has maximum 72 offdiagonal neighbors per flag, with **29,418 triangles and 13,066 negative-product pi-flux triangles**. This sign frustration cannot be gauged into a uniformly positive real-hopping network.

This is a **mathematical Pareto tradeoff**: much better conditioning and a preserved exact C3 require more interactions, more flux calibration, and combined maximum flag load up to 18. The frame sum *is not* a new Lorentzian dispersion law, and there is no claimed globally optimal conditioning.

## C. Actual refinement: 81 cycles persist but dimension stays one

Replace each edge of the 80-vertex/160-edge Levi graph with L unit combinatorial segments. The refined connected graph has V_L=80+160(L-1), E_L=160L, first Betti E_L-V_L+1=81 **exactly** for every positive integer L. Numerically compute the first positive ordinary graph-Laplacian eigenvalue lambda1(L) using shift-invert sparse Hermitian eigensolvers, and inspect L² lambda1(L) as L grows.

| L | V_L | L² lambda1(L) |
| ---: | ---: | ---: |
| 1 | 80 | 1.5505102572 |
| 2 | 240 | 1.0824986428 |
| 4 | 560 | 0.9445853357 |
| 8 | 1200 | 0.8854412178 |
| 16 | 2480 | 0.8577843912 |
| 32 | 5040 | 0.8443886988 |

The equal-unit-edge Kirchhoff metric-graph target is **acos(sqrt(6)/4)^2 = 0.8312667112181387**. It follows from original four-regular Levi adjacency eigenvalue sqrt(6) and the metric-graph vertex condition. The observed scaled gap approaches the prediction. The limiting compact metric graph has **spectral/Weyl dimension one**, not four; edge subdivision is not spatial-dimensional emergence. This is an actual deformation/refinement negative control.

Additional analytic null control: explicitly impose Cartesian product of four cycles C_64^4 with W33 internal fiber, so the heat trace factorizes K(t)=K_C64(t)^4 K_W33(t). At t=64 the heat spectral dimension is **4.007839**, but 4 was explicitly inserted, not predicted. Do not cite this as positive dimension selection.

Literature: metric-graph Laplacian/Weyl law https://doi.org/10.1007/s00023-020-00979-1 ; compact metric graph and spectral properties https://link.springer.com/article/10.1007/s00020-021-02635-7 ; subdivision conventions https://d-nb.info/1256429279/34 .

## D. Gravity: simple local cycle invariance does not close a GR constraint algebra

On canonical 160 edge pairs (x,p) with Gauss G=Dp, define h_i=(c_i·x)^2/2 + (sum_{e in supp(c_i)}p_e²)/2 for any signed eight-cycle c_i. Because D c_i=0, each h_i is Gauss invariant. Direct differentiation gives:

{h_i,h_j}|_(x=c_i,p=c_j) = (c_i·c_j)(8 - |supp(c_i) intersect supp(c_j)|).

The derivation is exact for these local quadratic densities; it does not invoke approximations. For a selected seed33 basis cycle pair (0,20), the two shortest cycles meet in one flag with signed inner product +1; therefore **{h0,h20}=+7 although Dp=0**. The earlier seed1 audit supplied a different -7 witness. This proves that these *particular* constraints cannot close into the Gauss constraints alone. It does **not** exclude additional spatial-diffeomorphism constraints, an improved perfect action, or any actual gravitational theory; no hypersurface-deformation algebra is yet implemented.

Literature: Dittrich & Höhn (2010), https://arxiv.org/abs/0912.1817 ; Bahr & Dittrich (2009), https://arxiv.org/abs/0905.1670 ; improved perfect actions https://doi.org/10.1103/PhysRevD.80.124030 .

## E. E6 particle physics: one flavor spurion cannot yield observed CKM mixing

Standard 27 under SO10×U1: 16_1+10_-2+1_4. Under SU5 the components read (10+5bar+1)+(5+5bar)+1: **one chiral SU5 generation plus a vectorlike 5+5bar pair**. This algebra does not select 27 over 27bar nor three copies.

Conditioned hypothesis: if an E6 implementation has just one flavor matrix Y and gives Yu=aY and Yd=bY, the Hermitian matrices Hu=Yu Yu† and Hd=Yd Yd† are proportional, hence [Hu,Hd]=0. For non-degenerate spectra their left diagonalizers agree, CKM has no physical mixing, and all Jarlskog CP invariants vanish. Thus such a one-spurion reduction is **experimentally excluded**, not a successful CKM derivation.

Independent symbolic two-spurion existence witness:
Yu=diag(1,2,4);
Yd=[[1,1,i],[1,2,1],[i,1,3]], symmetric.
Sympy computes Im tr([Hu,Hd]^3) = **-97200** exactly. This confirms two independent complex-symmetric flavor structures can permit nonzero CP-odd mixing; it **does not** fit data or derive the spurions. Two symmetric Yukawa matrices are already standard in realistic E6 models, not novel: Babu/Bajc/Susič (2015), https://link.springer.com/article/10.1007/JHEP05%282015%29108 ; and decomposition https://doi.org/10.1140/epjc/s10052-025-15043-7 .

## F. Hardware: triangle pi-flux phase cannot be measured by site populations alone

Minimal 3-site flux-zero and pi-flux hopping matrices (site order 0,1,2):
H+=[[0,1,1],[1,0,1],[1,1,0]];
H-=[[0,-1,1],[-1,0,1],[1,1,0]].

Let Q=diag(1,1,-1). Exactly H-=-Q H+ Q. Hence U-(t)=Q U+(t)* Q for these real matrices, and the **entire site-to-site probability matrices |U_ij(t)|² are identical for all t**. Site-population-only measurements cannot distinguish these two uniform real triangles. A claimed site-probability-only pi-flux witness would therefore be a false positive.

However, an independent Ramsey/idling phase reference accesses Im U_00. Flux-sign difference is **0.04098706248 at t=0.4** in units of reciprocal hopping, with leading short-time contrast 2t³/3. Sympy with arbitrary equal-in-both-protocol onsite detunings proves [(H+³)-(H-³)]_00=4 independent of these detunings; the cubic-phase contrast survives paired static onsite shifts. A deterministic 500-trial paired perturbation test with Gaussian onsite sigma=0.05 and hopping sigma=0.02 gives contrast mean **0.041049**, standard deviation **0.001397**, minimum **0.037396**, and 500/500 positive in this sampled model. Uniform amplitude loss gamma=0.1 multiplies coherent amplitude by exp(-gamma*t/2), 0.9802 at t=0.4; no full Lindblad detector fidelity or pulse-compilation claim.

This is a **proposed phase-sensitive three-site laboratory falsifier** and a deterministic software simulation, not an actual implemented experiment. Hardware references: tunable synthetic magnetic vector potentials in superconducting qubit arrays https://www.nature.com/articles/s41567-024-02661-3 ; driven superconducting circuits https://doi.org/10.1103/PhysRevA.102.032610 ; photonic flat-band and synthetic-gauge structures are distinct implementation pathways.

## Five independent next experimental/theoretical gates

1. **Dimension:** Find a local dynamical rewriting/renormalization whose dimension-four result is stable under model variation without inserting four spatial factors.
2. **Symmetry:** Derive a physical selection functional over invariant apartment frames, with a natural scale and a penalty for high coupler connectivity.
3. **Gravity:** Produce a covariant action, discrete phase space, momentum constraints and a first-class hypersurface-deformation algebra with a controlled continuum.
4. **Flavor:** Derive two independent Yukawa structures and a nontrivial Jarlskog invariant from symmetry breaking with fewer free parameters than precision flavor data; include chirality selection.
5. **Hardware:** Implement Ramsey phase reference on a signed 3-cycle, then a native eight-cycle, and compare loop flux and finite-time leakage under calibrated noise and loss.

**Stop line:** The finite mathematical developments are exact where indicated and materially sharpen the physics questions. They do not solve all five physical problems or establish a TOE.
