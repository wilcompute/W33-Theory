# Cross-month W33 archaeology: five falsifiers and overlooked connections

Date: 2026-11-04 UTC (November 3 US Eastern). **Scope:** bounded repo-wide textual/commit-subject inventory, selected older source close reading, exact finite mathematical tests and idealized numerical engineering controls. This is NOT a completed Theory of Everything, unique scientific priority or a semantic reading of all files.

**Producers:** analysis/toe_20261104_corpus_archaeology.py; analysis/toe_20261104_c3_orbit_sparsification.py; analysis/toe_20261104_archaeological_fivefront_controls.py.

**Results:** data/toe_20261104_corpus_archaeology.json; data/toe_20261104_c3_orbit_sparsification.json; data/toe_20261104_archaeological_fivefront_controls.json.

**Regression:** tests/test_toe_20261104_archaeology_fivefronts.py.

## 0. Search protocol: do not mistake hits for the corpus

Starting head: 7749ee2590fb7d7ebb3e9f8c0ab3d0793dabbeb2. Native Git reported 43,960 tracked files and 23,792 commits. Five separate regex git-grep path searches covered analysis/, papers/, tests/ and docs/. Full-path hit lists are saved, not only the first 20 GitHub-ranked results. Separate git-log commit-subject searches across all refs split at October 1, 2026. These are NOT exhaustive semantic or historical diff searches; each code hit may be a mention of others' work.

| Front | Current matching file paths | Historical subject hits before October | Subject hits since October |
|---|---:|---:|---:|
| Spacetime/dimension | 558 | 38 | 27 |
| Symmetry/apartments | 1,538 | 375 | 23 |
| Gravity/constraints | 241 | 26 | 8 |
| Flavor/strong CP | 1,416 | 371 | 116 |
| Flux/photonic hardware | 138 | 14 | 4 |

## 1. Spacetime: the older KO-dimension derivation is not uniqueness or emergence

Historical owner: June 2026 analysis/W33_SPACETIME_DIMENSION_FROM_KO.md and analysis/w33_spacetime_dimension_from_KO.py. The cited Python script assigns the finite real-structure signs (+,+,-) literally, takes the total KO target to be 2 mod 8, and applies the sign table. For a presumed spin manifold M and presumed KO(F)=6, the conditional result is dim(M) congruent to 4 mod 8, **not exactly 4**. In particular dimensions 4,12,20,28,36,44,52,60 all satisfy the displayed condition. The derivation selects 4 only with an additional minimality assumption. That script does not itself build/verify the complete real spectral triple; any separate construction must be read separately rather than silently assumed absent.

Historical second owner: October analysis/w33_20261008_native_H4_4D_spacetime_slab.py proves 2400 four-simplices in an explicitly constructed product S3 x I derived from a native 600-cell S3; it does not derive a Lorentzian metric or Einstein dynamics. Earlier November graph subdivision gives a one-dimensional metric-graph limit, another distinct dimension notion. **Do not conflate KO congruence, topological cell dimension, spectral dimension, and physical Lorentzian spacetime.**

External NCG background: https://ncatlab.org/nlab/show/Connes-Lott-Chamseddine-Barrett%2Bmodel ; Barrett https://doi.org/10.1063/1.2408400 .

## 2. Symmetry: 540 orbit-frame spectral sparsification, with exact C3

Historical owner: analysis/w33_pass5396_5401_allq_apartment_tight_frame.py already proves the general-q full-apartment tight frame. q=3 gives 1620 apartment cycles, dimension81, K=C C^T=160 P_cycle, K²=160 K. The all-frame operator has condition number 1, but its native flag matrix contains 12,720 nonzero undirected couplings, every pair.

Specific new computation: use the previous certified GF2-independent 27-orbit C3 basis. The 1620 eight-cycles form 540 length-3 orbits of an anchored symplectic transvection. Greedily choose additional complete orbits to reduce normalized Frobenius frame discrepancy, preserving exact divergence-free identities and C3-equivariance. Stage data:

| C3 orbits | 8-cycle terms | Condition (numerical) | undirected hopping pairs | max flag neighbors |
|---:|---:|---:|---:|---:|
| 27 | 81 | 4537.9859 | 1985 | 35 |
| 36 | 108 | 41.7286 | 2538 | 47 |
| 54 | 162 | 8.8330 | 3489 | 49 |
| 81 | 243 | 5.0450 | 4650 | 65 |
| 108 | 324 | **3.0427** | **5546** | 75 |
| 135 | 405 | 2.6906 | 6332 | 89 |
| 162 | 486 | 2.3058 | 7045 | 98 |
| 216 | 648 | 1.9120 | 8225 | 109 |
| 270 | 810 | 1.7106 | 9186 | 120 |
| 405 | 1215 | 1.4201 | 11077 | 141 |
| 540 | 1620 | 1.0 | 12720 | 159 |

At 108 orbits, condition number 3.04 uses 43.6% as many coupling pairs as the complete frame. Versus the previous 3-frame Hamiltonian (condition 6.85, 4320 pairs), this is a different Pareto tradeoff, not a universal improvement in every resource. The subset selection is greedy and subgroup anchored; no physical mechanism selects it.

Spectral sparsification is established prior art: https://doi.org/10.1137/080734029 . The contribution is this particular symmetry-closed W33 design and measured resource curve.

## 3. Gravity: indefinite cycle constraints have physical zeros but fail a first-class pair test

Previous November 81 positive quadratic cycle constraints had only a pure gauge simultaneous zero locus. Test the alternative signed local ansatz g_i(x,p) = (c_i.x)^2 - (c_i.p)^2.

For every nonzero divergence-free cycle u, x=p=u gives all 81 g_i=0, Dp=0, and nonzero gauge-invariant cycle content in x. So indefiniteness avoids the previous trivial physical zero-set obstruction. But it does NOT guarantee a valid constraint algebra. For two selected cycles c0,c20, c0.c20=+1 and lengths squared 8, set x=(c0+c20)/9, p=(c0-c20)/7. Exact identities give Dp=0, g0=g20=0, while

    {g0,g20} = 4(c0.c20)[(c0.x)(c20.p)-(c0.p)(c20.x)] = -8.

This rejects closure of **that pair into the pair and Gauss alone at this point**. It does not prove nonclosure of the full 81-constraint set on their complete common zero locus, nor construct a nonlinear ADM algebra. Older owner analysis/w33_pass11968_native_spin2_constraint_completion.py has an independent native derivative-bracket failure and a nonlocal projected linear completion. No full physical gravitational action was obtained.

Reference: https://arxiv.org/abs/1304.5983 ; https://doi.org/10.1103/PhysRevD.91.124034 .

## 4. Flavor: a November CP example fails strong CP; October already owns the better model

The preceding symmetric four-state toy mass block with Y=diag(1,2,4), v=(1,1,1+i)^T and heavy mass3 yields weak CP invariant Im Tr([Hu,Hd]^3)=1600. Its exact full determinant is **12-4i** and arg det=-atan(1/3) approximately -0.32175. If that block were the complete colored quark mass sector with zero bare theta, it would be unacceptable for strong CP; it remains only a weak-CP existence example. No compensating axion or theta cancellation was derived.

**October 12 owner:** analysis/PASS11950_11951_STRONG_CP_COMPLETION.md, producer analysis/w33_pass11950_11951_strong_cp_divisor_and_vectorlike.py. This already contains a triangular Nelson-Barr mass block [[m,0],[B,mu]], exact real determinant, nonzero weak CP, a parity gate for ordinary E6 exotic quarks, an anomaly-checked parity-compatible extra field set, explicit scalar assumptions, and unresolved vacuum/radiative requirements.

Independent SymPy verification of that older witness with real m=[[1,1,0],[0,2,1],[1,0,3]], complex B=(1+i,2-i,1+2i), positive mu=2: det full=14, Im(H12 H23 H31)=119/64. **Do not claim these are new discoveries.**

Additional aligned-rank-one no-go: if real bare m is diagonal in the up-sector basis and only ONE complex heavy mixing row B enters the Hermitian light Schur complement, H_ij=-m_i*m_j*conj(B_i)*B_j/(mu²+|B|²) off diagonal. Therefore H12 H23 H31 is real, so this single complex row **alone** cannot generate physical weak CP in the aligned diagonal ansatz. Noncommuting real m, or additional independent flavor structures, remain necessary. The older example indeed uses a non-diagonal m.

Prior literature, including actual E6 Nelson-Barr: https://doi.org/10.1140/epjc/s10052-018-6388-6 . Radiative protection: https://doi.org/10.1007/JHEP09(2025)162 .

## 5. Hardware: change the loss-aware objective to total discrimination time

Historical October owner analysis/w33_20261008_photonic_trotter_depth_loss.py already tested nine-matching-layer photonic Trotter errors versus per-layer survival, so the generic depth-vs-loss tradeoff is prior art. Our previous five-state reference-arm Lindblad triangle simulation with loss=dephasing=0.1 and per-pulse deadtime0.003 found 16 slices (48 pulses) minimize signal approximation error relative to a simultaneously driven noisy target.

But experimental time-to-answer optimizes a different objective. Using the saved calibrated toy data, let physical duration for 3n sequential edge pulses be T_n=3(0.4)+3n(0.003); add independent reference dephasing k_ref=0.1, giving coherent contrast delta_eff=delta exp(-k_ref*T_n/2).

For two independent Ramsey +/-1 estimators, worst-case variance at most one and Gaussian/asymptotic target z=5, use N_per_flux=ceil(2 z²/delta_eff²) and combined interrogation time 2*N_per_flux*T_n, ignoring readout and reset. Approximate outcomes:

| slices | pulses | contrast after reference dephasing | shots per flux setting | total interrogation time |
|---:|---:|---:|---:|---:|
| 2 | 6 | 0.02561 | 76,200 | 185,700 |
| 4 | 12 | 0.03193 | 49,100 | 121,300 |
| **8** | **24** | **0.03334** | **45,000** | **114,400** |
| 16 | 48 | 0.03337 | 44,900 | 120,700 |
| 32 | 96 | 0.03276 | 46,600 | 138,700 |
| 64 | 192 | 0.03139 | 50,700 | 180,200 |

Thus **8 slices / 24 pulses** minimizes the tested idealized *time-to-discrimination* metric, while 16 slices optimizes *error to a specific noisy analog target*. No actual detector, calibration, reset overhead, readout fidelity, or real hardware is modeled. Shot figures are asymptotic benchmarks, not rigorous finite-sample p-values.

## 6. Additional overlooked connections and claim firewall

- Algebraic KO-dimension, an explicitly constructed 4D simplicial topological product, and 1D metric-graph spectral flow are different layers. Do not combine them into a single emergence proof.
- Full symplectic-frame perfection gives an exactly flat protected band but dense flag couplings. Anchored C3-subgroup invariance permits a certified locality/condition Pareto curve; a physical subgroup-selection action remains missing.
- A nonzero weak-CP invariant is insufficient for strong-CP safety. Correct model ancestry is the old parity-aware Nelson-Barr program; its radiative vacuum completion is not solved.
- Indefiniteness repairs a zero-set obstruction but does not imply first-class canonical gravity constraints. Action-derived lapse/shift and nonlinear closure remain open.
- Lowest simulator error, strongest coherent contrast and shortest experimental decision time are distinct objectives.

**Exact layers:** integer incidence and orbit symmetry; constrained-pair Poisson algebra; KO modular alternatives; SymPy determinant/CP identities; corpus keyword counts. **Numerical layers:** orbit spectral eigenvalues, greedy subset choice and shot-time benchmarks. **Missing physical outputs:** emergent 3+1 Lorentzian gravity, selection dynamics, a predictive gauge/vacuum flavor model, and actual hardware measurements.

## Five independent next gates

1. Dynamical four-cell growth that generates metric/causal 3+1 structure without prespecifying it.
2. Symmetry-respecting action or variational prior selecting C3 orbit subsets and weights with a real locality cost.
3. Discrete action-derived nonlinear Hamiltonian/momentum constraints with a verified first-class algebra.
4. Parity- and loop-complete E6 Nelson-Barr model with predicted (not input-reconstructed) flavor.
5. Device-specific flux Ramsey implementation, reference calibration, full shot/noise budget, phase identifiability and pulse scheduling.
