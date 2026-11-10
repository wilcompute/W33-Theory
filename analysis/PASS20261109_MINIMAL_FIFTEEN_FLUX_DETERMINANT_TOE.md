# W33/TOE: minimum 15-link gauge-flux fragility and matched-graph falsifiers

**November 9, 2026 (US Eastern).** Companion to commit 38e3026827f7292db23303c41ade2668d31d8d27, which already published seven independent fronts: W33 gauge-phase fragility, photonic dark-state preparation, full phase calibration, 81-loop decoder, optical shot allocation, Bell detector thresholds, and the frozen DES S9 gate. This addendum supplies a *new exact determinant theorem* and independent matched-graph controls. It is not a theory of everything or observed particle physics.

## 1. Exact theorem — fifteen phase changes are necessary and sufficient

The 40×40 point-line W33 incidence matrix B has 160 entries equal to 1, four per row/column, and singular spectrum 4^1, (sqrt6)^24, 0^15. Thus rank(B)=25. Its 80-mode chiral Hamiltonian H(T)=[[0,T],[T†,0]] has 80−2rank(T) zero eigenvalues: 30 for T=B.

Changing k incidence entries is a sum of k rank-one matrix updates. Therefore rank(B+Δ) ≤ 25+k, so at least max(0,30−2k) chiral zero modes remain. **At least fifteen changed edges are necessary** to remove every exact zero mode, independent of the chosen phase shifts or modified amplitudes.

We used a deterministic seeded search to select **15 distinct incidences** whose projected point and line endpoint vectors each span the appropriate 15-dimensional dark kernel. Every selected edge receives the SAME unit-modulus phase z=e^(iθ), while all other incidences retain amplitude one. For this explicit support, the **exact determinant polynomial** is:

    det(B(z)) = −2 (z−1)^15.

Proof: B(z)=B+(z−1)UVᵀ with U,V each having fifteen columns, so the determinant is a polynomial of degree ≤15 in δ=z−1. Because rank(B)=25, every coefficient below δ^15 vanishes. Exact integer determinants from SymPy are det(B(0))=+2, det(B(−1))=+65536=2^16, and det(B(2))=−2, yielding the coefficient −2. The z=2 case is an algebra check, NOT a phase-only physical setting. For physical z on the unit circle every θ≠0 mod 2π gives det(B(z))≠0, so **all thirty original dark modes are lifted** without changing a single hopping magnitude.

At θ=π, the exact signed integer matrix has determinant 65536 and numerical minimum singular energy 0.115473296847 in unit hopping strength. Direct numerical checks at θ=π/6,π/3,π/2,π match the exact determinant phase to better than 4e−15. The 15 incident edges, listed with point and line indices in the frozen JSON file, are ordered so each successive π phase flip increases rank by one: 25,26,...,40; zero modes descend 30,28,...,0. The minimal required link-support cardinality is therefore **exactly 15**, not just an observed upper bound. Arbitrary 15-edge selections do NOT necessarily achieve full rank.

**Strict symmetry caution:** Full PSp(4,3) acts transitively on the 160 incidences. A strictly invariant hopping restricted to incidence edges is proportional to B and has only an overall removable phase. The explicit phase pattern must therefore break this strict symmetry, or a different physical theory must provide a gauge-compensated/projective magnetic action. No action, flux vacuum, chiral Standard Model representation, spacetime or gravitational dynamics is derived here. A square 40-by-40 chiral coupling has net chiral index zero, regardless of flux.

**Executable proof and exact outputs:** analysis/w33_20261109_minimal_15_flux_lift.py; data/w33_20261109_minimal_15_flux_lift.json; six independent test methods in tests/test_w33_20261109_minimal_flux_cert.py.

## 2. Matching size and degree does not explain the W33 flat band

All these incidence graphs have 40+40 vertices, 160 edges, and degree four at every vertex:

| Connected bipartite graph | Rank of 40×40 incidence | Zero modes of 80-mode chiral walk |
| --- | ---: | ---: |
| **W33** | **25** | **30** |
| Circular four-consecutive-neighbor graph | 37 | 6 |
| 128 seeded connected simple four-regular bipartite graph samples | 40 in all 128 | 0 in all 128 |

The random samples were made from four independent perfect matchings, rejecting repeated edges and disconnected outcomes. **This is not an unbiased sampler of all 4-regular bipartite graphs, nor an exhaustive enumeration.** The data show W33's large nullity is not forced by regularity or its simple counts; they do not show W33 is spectrally unique.

Producer: analysis/w33_20261109_dark_graph_specificity.py; data/w33_20261109_dark_graph_specificity.json; tests/test_w33_20261109_dark_graph_specificity.py.

## 3. Physical experimental route and cautions

The seven-front companion provides a concrete 40-port source dark-state probability distribution: 3/8 at the selected port, 1/24 at each of twelve adjacent ports and 1/216 at the other 27 ports. A conditional ideal optical preparation uses 39 two-mode tunable splits in six layers and 12 sign phases, assuming arbitrary mode-pair connectivity. An ideal 80-mode W33 incidence Hamiltonian yields zero line-sector occupancy; detuning one link yields calculable short-time leakage. The present theorem strengthens this to a **15-link minimal complete lifting pattern**.

A programmable test could compare (i) no physical flux, (ii) vertex gauge rephasings, (iii) one detuned edge, (iv) fourteen designated phase changes (at least two surviving exact dark eigenvectors), (v) fifteen designated π changes (no dark eigenvectors and measured finite spectral gap), and (vi) size-/degree-matched graph controls. After any flux change, the ORIGINAL prepared dark vector need not remain in the new zero eigenspace; compare spectral measurements or prepare the *new* dark eigenvectors.

Current work is **simulation and exact finite mathematics**, not fabricated optical hardware. A real apparatus needs connectivity compilation, phase stability, source heralding, detector/no-click calibration, measured propagation losses and energy-time units. Prior literature already treats graph chiral flat bands (https://doi.org/10.1103/PhysRevB.109.035140), flat-band disorder (https://doi.org/10.1103/8x11-bq9x), and photonic graph quantum walks on small processors (https://pmc.ncbi.nlm.nih.gov/articles/PMC7909884). No broad novelty or TOE discovery is claimed.

## 4. Parallel-track synchronization and held-out evidence

Commit 38e3026827f7292db23303c41ade2668d31d8d27 already published 17 tests and the seven-front packet. This addendum contains only the two new original producers, their frozen data, nine focused tests, and this report; it should not overwrite the other agents' artifacts.

Previously published companion results: joint phase-only maximum likelihood improves some contexts empirically, but provides no rigorous full-interferometer confidence guarantee. Oracle Fisher-optimized photonic shot distribution reduces the one-state Cramér–Rao coefficient, but it is NOT a finite-shot state certificate. The detector-realistic single-photon Bell model depends sensitively on source survival. Frozen DES Y6 S9 remains **UNSCORED** until an authenticated complete unblinded xi± vector, covariance, n(z), patched scalar-field CLASS/Halofit models and consistent nuisance refits exist. Published S8 summaries cannot replace that preregistered test (https://www.darkenergysurvey.org/des-y6-cosmology-results-papers/).

## 5. Five independent best next physics tests

1. **Derive, rather than stipulate, physical gauge flux.** Specify a gauge-covariant local action on W33's 81 cycle holonomies. Derive ground states and barriers, then test whether dynamics selects or excludes the fifteen-edge phase pattern without tuning its answer into arbitrary couplings.
2. **Prove a genuine protected chiral continuum.** Specify a growing graph / bundle limit producing emergent 3+1D locality, a nonzero protected Weyl index, gauge anomalies and mass terms. The balanced 15+15 finite dark band does not supply a Standard Model family by itself.
3. **Build a source-to-detector photonic falsifier.** Compile the 39-split state preparator into a layout-constrained 40+40-mode network, predict measured singular-value gaps at zero/one/fourteen/fifteen π-link changes with realistic loss and phase uncertainty, and use non-W33 controls.
4. **Close rigorous calibrated entanglement certification.** Infer full nine-/twelve-setting optical POVMs with finite-sample confidence, independent detector efficiency and source state controls, and robust mixed PPT entanglement witness selection; do not confuse oracle Fisher bounds with true coverage.
5. **Execute an unmodified held-out physical likelihood.** Obtain authenticated DES Y6 full shear data/covariance and corrected model predictions for frozen S9; independently audit single-photon Bell source survival, phase-reference photon resources and spacelike timing.

**Conclusion:** A provably minimal fifteen-edge phase-only lifting of all thirty native W33 dark modes has been established for a finite one-body tight-binding Hamiltonian. What has NOT been derived is a physical reason to select that flux, a continuum, gravitational dynamics, or Standard Model chirality.
