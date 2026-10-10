# TOE Round 33 — joint ternary space-time decoding, exact cover constraints, A6 torus obstruction, full Bloch spectral dimension, and measured C8 hardware gate

**Date:** 10 October 2026
**Repository:** wilcompute/W33-Theory, master
**Principle:** distinguish exact algebraic proof, deterministic computation, finite Monte Carlo, failed computational search, and physical data. Do not interpret representation matches as observed particle physics.

## Preexisting/parallel work consulted

- Round26 fixed the genuine native W33 edge-qutrit `[[160,1,8]]_3` CSS gauge/Wilson geometry.
- Round27 built a data-only radius-3 exact syndrome decoder.
- Round30 verified a Shor-style cat/GHZ circuit only at a narrowly stated single-fault level, with ideal verifier and readout; this packet does NOT claim gate-level fault tolerance.
- Round31 constructed the explicit connected 17-fold girth-10 cyclic W33 Levi cover and associated ternary HGP `[[9245281,1852321,10]]_3`; it also established a binary 2-fold voltage contradiction.
- Round32 tested a per-check ternary temporal filter and stochastic smaller cyclic covers down to p13, without finding a new distance-ten construction.
- Parallel Pass11843 **already** computed a finite-Lorentz Tits/W(E6) centralizer inside e8 of `su(3) + su(2)`, dimension11, centre0; earlier Weil embedding has different `u(1)` commutant. Parallel Pass11844–11848 **landed during this pass** and correct the earlier finite-Lorentz group identification: faithful A6 has su(5) commutant, while the Tits sign extension has su(3)+su(2). The parallel work also constructs the non-split 4D translation quotient and a hypercharge-rotation case. Our own modular obstruction below is therefore an INDEPENDENT REPRODUCTION of Pass11844, not a newly established priority claim. The new result of this pass is the combined-translation-plus-hypercharge obstruction in Section 3b.

The five research tracks below respond to Round32's independent next-step selection and are independently reproducible. A sixth small standalone theorem strengthens the second track.

## 1. Joint correlated space-time Pauli-event decoder; comparison on identical simulations

**Experiment:** exact same frozen-seed 180 trials for each of three Round32 measurement noise settings, five rounds, 160 data links, Pauli X and Z channels each independently erring with probability p_data=.0005 per link per round, wrong ternary measurement report with probability 1%, 2%, or 4%, uniformly offset ±1. All 80 Wilson-Z and 79 Gauss-X checks are the ACTUAL W33 matrices.

**New decoder:** enumerate candidate single-channel Pauli error events (X or Z, 160 links, exponent 1 or2) at ANY of the five time steps. Unlike the earlier 159 independent 3-state filters, a candidate affects a correlated vector of stabilizer outcomes in **every subsequent time bin**. Score its exact multi-check/multi-time measurement-likelihood improvement relative to `log((1-p_data)/(p_data/2))` event prior; greedily insert the maximally favorable event and repeat up to eight events. Compare all decoder results via the existing exact radius-three physical error decoder and full stabilizer-equivalent `logical_ok` certificate.

| Measurement wrong report | Raw final/180 | Round32 independent filter/180 | Round33 joint decoder/180 | Ideal true-syndrome/180 |
|---|---:|---:|---:|---:|
| 1% | 144 | 40 | **13** | 1 |
| 2% | 171 | 35 | **14** | 0 |
| 4% | 180 | 53 | **36** | 1 |

Total Round32 temporal failures `128/540` versus Round33 joint `63/540` = **50.8% fewer failures**, using the SAME event/noise realizations. The total wrong final syndrome values across the settings were raw `279,572,1186`; Round32 `80,127,147`; Round33 joint `14,23,61`.

**Limits:** The score is a greedy posterior-improvement approximation, not globally exact joint MAP/Viterbi or BP/OSD; the allowed sparse event list may omit multiple simultaneous gate faults. The physical circuit is NOT simulated: no cat verification, ancilla readout faults, cross-check correlated errors, coherent leakage, syndrome detector graph, real hardware or threshold. The code's 159 independent check generators do not imply arbitrary ternary syndrome vectors are impossible; the new constraint is joint **time-correlated physical Pauli support**, not an invented static syndrome parity relation.

Producer: `analysis/w33_20261010_toe33_joint_spacetime_decoder.py`. Frozen result: `data/w33_20261010_toe33_joint_spacetime_decoder.json`.

## 2. Degree-13 constraint programming and rigorous lower bounds for W33 covers

**Actual CP-SAT model:** Each connected W33 Levi cover can be voltage-gauge-transformed to set all 79 edges of a spanning tree to zero. On `Z13`, the remaining **81 chord voltages** are exhaustive free coordinates. For each of 1,620 signed eight-cycle rows, constrain its sum mod13 to be one of 1,...,12 (never zero). Encode that modular disequality using a signed integer carry and a nonzero remainder, in Google OR-Tools CP-SAT with eight workers and fixed seed. This is an **exact finite CSP model** of p13 eight-cycle elimination, but a solver can report UNKNOWN without a proof.

**Result after 75 seconds:** `UNKNOWN`. No validated p13 voltage assignment and no unsatisfiability certificate. It would be incorrect to call p13 impossible or to replace the previously verified degree17 distance-ten code. The model and solver statistics are frozen so a later exact SAT/CP-SAT backend can resume from a shared, transparent formulation.

**Independent exact Moore bound:** Any 4-regular bipartite graph of girth≥2r has at least

`N >= 2(1+3+...+3^(r-1)) = 3^r-1`

vertices by exploring nonintersecting breadth-first trees around an edge. Every degree-m W33 Levi cover has `N=80m`. Thus the following are hard cover-degree lower bounds even for non-cyclic, non-normal or nonabelian graph covers:

| Required girth | Min. vertices | Min. cover degree |
|---:|---:|---:|
| 8 | 80 | 1 |
| 10 | 242 | **4** |
| 12 | 728 | **10** |
| 14 | 2186 | **28** |
| 16 | 6560 | **82** |

These are lower bounds, not constructions. The exact p13 question remains OPEN, and no new girth12 construction was found.

Producers: `analysis/w33_20261010_toe33_p13_cpsat_cover.py`, `analysis/w33_20261010_toe33_girth_moore_bound.py`. Frozen ledger `data/w33_20261010_toe33_p13_cpsat_cover.json` plus Moore certificate.

## 3. E8 finite-Poincare route: A6-invariant four-translation submodule NO-GO in the A5 root torus

**Prior:** The parallel Pass11843 Tits/W(E6) Lorentz lift, under which the Lie algebra centralizer is `su3⊕su2`, is a distinct E8 representation from the Weil `u1` case. Round32 proved a general containment: extending the SAME Lorentz subgroup cannot increase its E8 commutant and add independent hypercharge while retaining all su3⊕su2.

**Independent exact modular representation reproduction (also established by parallel Pass11844):** For the standard A5 (SL6-type) root cocharacter lattice, the F3 reduction is the five-dimensional augmentation module

`S={x∈F3^6 | Σ_i x_i=0}`,

on which the derived Weyl group `W(A5)' = A6 ≅ PSL2(9)` permutes six coordinates. Since `6=0 mod3`, the vector `(1,1,1,1,1,1)` lies in S, giving a one-dimensional invariant C and a four-dimensional quotient `S/C`. **Does that desired 4D Lorentz translation module split back into an honest 4D invariant subgroup of S?**

Generate A6 with four 3-cycles and explicitly close group order **360**. Construct five-by-five F3 matrices on S; enumerate all **242 nonzero S vectors** and the submodule their A6 orbits span:

- 2 nonzero invariant vectors generate the one-dimensional constant submodule C.
- The other **240** generate all **five** dimensions of S.
- Invariant F3 linear functionals on S have dimension zero.

Therefore there are NO A6-invariant four-dimensional submodules; `0→C→S→S/C→0` is a **nonsplit modular extension**. In this specific standard A5 root-torus model, the desired 4D translations cannot be embedded as an invariant subgroup of that five-dimensional 3-torsion.

**Boundary:** This does not cover the whole E8 Cartan, non-Cartan translation groups, other 3-subgroups, central quotient subtleties of an embedded SU6×SU3×SU2, or alternative E8 representations. In particular it does NOT refute future parallel Pass11844–11848 approaches using additional torus degrees of freedom. A module quotient is not automatically a normal translation subgroup of E8.

Producer: `analysis/w33_20261010_toe33_a6_torus_translation_obstruction.py`. Frozen 360-group / 242-vector certificate.

## 3b. NEW cross-track hypercharge–translation compatibility theorem (correctly credited)

During this pass, parallel Pass11844–11848 were committed to master with exact actual Tits-lift computations. Their faithful A6 Lorentz group alone has e8 commutant su5 (dimension24); A6 plus a hypercharge Z7(Y) rotation has exactly su3+su2+u1_Y (dimension12, centre1), whereas the finite Poincare group with the central-extension translations Z3·M has exactly su3+su2 (dimension11, centre0). Parallel Pass11844 also exhibits the nonsplit modular F3^4 translation quotient; our Section3 calculation reproduces, rather than precedes, that result.

**New corollary combining these two separately verified branches:** Let L be that faithful A6 Tits lift, T its Z3·M translation group and R the same hypercharge Z7(Y) rotation. Every su3+su2 generator commutes with L, T and R, by the two parallel centralizer certificates. Conversely, any element commuting with all three groups must commute with L and T, whose full commutant equals su3+su2. Therefore

`c_e8(<L,T,R>) = su3 + su2` **exactly**, dimension11 and centre0.

The hypercharge direction surviving for A6+R alone is lost once T is imposed. One cannot identify *both* those specified translations and independent commuting U(1)_Y as the internal gauge symmetry of the SAME fixed E8 Tits action. This does not preclude other E8 embeddings, dynamical gauge structures, different translation actions or physical Standard Model physics. No new E8 matrix exponential was computed here: the conclusion is a rigorous Lie-centralizer containment/intersection derived from the *published parallel certificates*.

Producer: `analysis/w33_20261010_toe33_hypercharge_translation_incompatibility.py`; source `data/w33_pass11844_11846_e8_poincare_lifts_matter.json`; frozen combined-result certificate.

## 4. Full 1,360-site W33 cover Bloch spectrum: no robust diffusion dimension three or four

Use the **actual** 160 signed Z17 voltages from Round31, rather than a toy cubic lattice. Cyclic covering-deck symmetry diagonalizes the unweighted 1,360×1,360 adjacency matrix into **17 independent Hermitian 80×80 Bloch matrices** with edge phase `exp(2π i k z/17)`. Compute every eigenvalue with numpy Hermitian eigvalsh. Verify sum of Laplacian eigenvalues `1360·4=5440`, second moment `1360·20=27200`, unique zero mode and base-sector spectrum `±4^1, ±√6^24, 0^30`.

The smallest nonzero combinatorial Laplacian eigenvalue is about **0.67194052238**. Evaluate the complete finite-graph heat trace

`K(t)=(1/1360)Σ exp(−tλ_i)`, `d_s(t)=2t Σλ_i exp(−tλ_i)/Σexp(−tλ_i)`.

Predefine a ONE-DECADE plateau criterion: over a continuous diffusion-time interval of ratio≥10 the running spectral dimension must remain within ±0.25 of target d. Scan 220 geometric time samples from 0.03 to300:

- Around **d=3**, the longest qualifying near-three window has time span ratio **1.46**, not 10.
- Around **d=4**, longest window has ratio **1.23**, not 10.
- Finite graph d_s→0 as t→∞.

Thus this unweighted exact 17-fold W33 Levi cover has **no decade-long three- or four-dimensional diffusion plateau by this explicit criterion**. Mere crossings of 3 and4 cannot support an emergent physical continuum claim. Weight selection, longer covers, interacting bosonic dynamics and gravity are NOT excluded.

Producer: `analysis/w33_20261010_toe33_bloch_spectral_spacetime.py`, frozen complete heat/spectral certificate.

## 5. C8 platform feasibility grounded in actual published measurements

Target *proposed*, not observed, attractive 8-site Bose–Hubbard ring: `t/h=5MHz`, `U/t=32` (`|U/h|=160MHz`), first bound-pair band gap ≈0.18175MHz, 60μs Ramsey or a shorter ~20μs direct scan. Independent pair loss model: `P_two survive(t)=exp(-2t/T1)`; half survival requires `T1≥2t/ln 2`.

Unlike prior hypothetical T1 grids, this pass compares THREE actual published experimental measurements:

1. **Two tunably coupled superconducting transmons** (npj Quantum Information, 2018), https://doi.org/10.1038/s41534-018-0088-9 — shows tunable hopping, cross-Kerr and **measured typical T1 between 15 and 40 microseconds** across coupler biases. If one naively uses these actual lifetimes in the above conditional two-excitation Markov model at 60μs, expected survival is `exp(-120/15)=0.000335` through `exp(-120/40)=0.04979`, i.e. **0.0335% to 4.98%**, drastically under the target half-survival; and the published device has only two sites. It does not rule out future improved transmons.
2. **High-order nonlinear superconducting LC oscillator** (Nature Communications 2025), https://doi.org/10.1038/s41467-025-62047-8 — reports two-, three- and four-photon nonlinear processes each **over 70MHz** with sign-changing nonmonotonic spectrum, versus ~200kHz linewidth. These are impressive real device parameters but NOT confirmation of uniform attractive `U/h=160MHz` Kerr or eight-site coherent ring; its high-order spectrum is specifically non-Kerr.
3. **21-resonator driven-dissipative Bose–Hubbard chain** (PRX Quantum 2026), https://doi.org/10.1103/rvhv-ms4t — reports collective phase-switching from milliseconds up to **143 seconds**. This is a driven-dissipative switching TIME, **not T1 photon lifetime** and NOT evidence of 143 seconds of single/two-photon coherence.

No platform is demonstrated here meeting all eight-site ring, attractive binding, precise hopping, coherent two-photon loading, survival, and readout requirements. This is an empirical design-rejection *for the literal 2018 two-site platform under stated loss assumptions*, not a general no-go for future superconducting hardware.

Producer: `analysis/w33_20261010_toe33_C8_measured_comparator.py`. Frozen source-indexed hardware comparison certificate.

## Overall verdict, evidence quality

**Strongest computational:** joint sparse-data-event time decoder yields 13/14/36 failures vs 40/35/53 in the exact same 180-sample noise trials; all are simulations, not fault-tolerance thresholds.

**Strongest mathematics:** an exact independent reproduction of the non-split A6 translation-module obstruction (also in parallel Pass11844) and a NEW combined-generator corollary: once the central-extension finite translations are imposed in that faithful Tits lift, adjoining the discrete hypercharge rotation does not retain an independent commuting hypercharge u(1). Exact Moore lower bounds cover arbitrary W33 Levi graph coverings.

**Strongest negative physics control:** the complete 1,360-eigenmode cyclic W33 cover does not exhibit sustained 3D or4D diffusion spectral dimension. Standard two-transmon measured relaxation times are far below the proposed C8 two-photon 60us survival requirement under the explicit loss model.

**Unsolved:** p13 CP-SAT returns UNKNOWN after75sec—not a satisfiability verdict; no genuinely emergent GR/Standard Model or calibrated laboratory machine; no coherent verified-cat gate-level threshold, no all-E8 embedding classification.

Independent scripts, frozen JSON evidence, focused pytest, and a named-scope report are included. No parallel branch edits or unrelated dirty file changes should enter the commit.
