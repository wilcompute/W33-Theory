# Pascal–Sierpiński parity predicts a precise Bell-resource staircase under local particle-number SSR

2026-11-19. Independent five-front TOE continuation plus a sixth, deeper photonic-resource test. CONDITIONAL physics result; not a Theory of Everything. The companion research report analysis/2026-11-19_five_linked_physics_torus_center_SSR_histories_flavor.md, with 43 passing focused tests, examines: (I) a synthetic causal-incidence 2D torus whose reconstructed adjacency supports an externally chosen U1 overlap index; (II) fundamental matter breaking a pure adjoint SU2 center selection rule; (III) operational two-copy photon Bell nonlocality under local number superselection; (IV) exact Burnside counting of unlabeled three-layer causal histories; and (V) flavor-interaction rank constraints on anomaly-free hypercharges. This sixth result is new-to-repo and does not duplicate those calculations.

## Resource assumption and exact proof

Alice and Bob share n independent identical copies of the delocalized single photon

    |psi_1> = (|10> + |01>)/sqrt2.

There is no external shared phase reference. Each laboratory may perform arbitrary ideal **joint dichotomic observables commuting with its total local photon number**, but no postselection or borrowed reference frames. This grants ideal number-preserving collective mode measurements (not asserted feasible with only passive linear optics).

The local charge sector in which Alice has k photons occurs with probability C(n,k)/2^n. Conditional on that sector, the two laboratories share a maximally entangled state of Schmidt rank d=C(n,k). The exact optimal CHSH value of a maximally entangled d-dimensional bipartite state with dichotomic observables is 2sqrt2 for even d, and [2sqrt2(d−1)+2]/d for odd d. Jordan's lemma partitions each local measurement space into 2D blocks (Tsirelson bound) and an unavoidable single 1D classical block when d is odd. The program explicitly builds real Hermitian, involutory local measurement matrices and checks that each commutes with local number. It verifies their actual Bell expectation against the sector upper bound for n=0,...,8, with separate dense wavefunction checks for small n.

Lucas's theorem states that the number of odd entries of row n of Pascal's triangle equals 2^popcount(n). Each odd binomial coefficient leaves exactly one 1D classical remainder. Therefore the optimal **unconditional** ideal CHSH value, within the stated number-SSR scenario, is the exact expression

    S_n = 2 + (2sqrt2−2) [1−2^(popcount(n)−n)].

This is an independently derived consequence of established quantum-information and combinatorial results. References: Quantum 7,1054 (2023), doi:10.22331/q-2023-07-11-1054, for exact odd/even dimensional CHSH maximum; Lucas's theorem, MIT Stanley Enumerative Combinatorics https://math.mit.edu/~rstan/ec/ec1.pdf ; superselection copy-pair Bell tests PhysRevA.82.042116.

## Exact ideal operational scores

| copies n | odd entries in Pascal row | optimal CHSH |
|---:|---:|---:|
| 1 | 2 | 2.000000 |
| 2 | 2 | 2.414214 |
| 3 | 4 | 2.414214 |
| 4 | 2 | 2.724874 |
| 5 | 4 | 2.724874 |
| 6 | 4 | 2.776651 |
| 7 | 8 | 2.776651 |
| 8 | 2 | 2.821955 |

Thus S_(2m)=S_(2m+1) exactly: adding one odd-numbered copy does not increase this ideal Bell maximum. At power-of-two n, the gap to Tsirelson 2sqrt2 is (2sqrt2−2)*2/2^n. This makes the Pascal/Sierpiński parity pattern an **actual operational resource count**, not evidence that this combinatorics generates gravity or fundamental constants.

## Independent photon loss: ideal gain versus feasibility

In a separate, physically stricter toy model, each of n distinguishable photons survives independently with probability eta, all vacuum and reduced-photon outcomes are retained, and we reuse the identical number-conserving measurement construction optimized at eta=1. We explicitly sum all 2^n survivor subsets. In the two-copy case this independently reproduces the exact polynomial from the previous five-front research:

    S_2(eta) = 2−4eta+(3+sqrt2) eta²,
    eta_threshold=4/(3+sqrt2)=0.9061636786439.

| n copies | ideal CHSH | fixed-setting photon survival threshold |
|---:|---:|---:|
| 2 | 2.414214 | 0.906164 |
| 3 | 2.414214 | 0.935261 |
| 4 | 2.724874 | 0.933115 |
| 5 | 2.724874 | 0.933231 |
| 6 | 2.776651 | 0.939167 |

The finite-loss calculations do **not** minimize the threshold over arbitrary measurements or apparatus. The n=4 construction beats n=2 in the lossless score, but requires *higher* photon survival with these particular settings. It also requires powerful collective local operations. This is a precise counterexample to the naive assumption that increasing copy count must simplify a real single-photon quantum processor.

## November 14, 2026 literature cross-check: physically restricted optical circuits

Daniel J. Brod and Ernesto F. Galvão, Linear-optical nonlocality without postselection, arXiv:2611.19570v1 (submitted November 14, 2026), https://arxiv.org/html/2611.19570v1, prove the two-photon postselection-free maximum 1+sqrt2 for passive interferometers with number-resolving detection. Their implementation-oriented first-success ladder with 2k photons attains

    S_passive(2k)=2sqrt2-(2sqrt2-2)/2^k.

It gives 2.414214 at 2 photons, 2.621320 at 4 photons, and 2.724874 at 6 photons. Our exact SSR-sector upper bound for n copies, which allows ARBITRARY collective number-conserving local observables, gives 2.414214, 2.724874 and 2.776651 respectively. The difference is an operational restriction, not a contradiction.

The paper also derives a loss scenario in which first-success flags are read locally and the Bell threshold is eta>4/(3+sqrt2) for all k. This can improve on our fixed-setting thresholds for n=4 or n=6; the gains depend on the measurement choice and circuit. Thus the comparison suggests a more precise engineering objective: **maximize Bell violation conditional on a real optical gate set and loss model**, not maximum CHSH for unconstrained ideal observables. The source is an independent physics paper, not new research by this project.

## Cross-sector physics and remaining missing information

1. Causal topology: the synthetic torus's graph can be reconstructed from causal incidence, but real 3+1 Lorentzian topology and oriented Clifford/Dirac transport are not derived.
2. Global gauge form: center-blind pure gauge actions can become center sensitive when fundamental matter determinants are included; matter content and RG dynamics remain inputs.
3. Quantum operational physics: Pascal parity controls the **ideal** Bell resource under a precise SSR, while photon loss and measurement complexity determine its physical utility. This says nothing about deriving the Born rule.
4. Gravity: quotienting histories by layer-preserving automorphisms still leaves exp(O(N²)) entropy. A relative, positive, normalized 3+1 causal quantum history measure is still missing.
5. Flavor: anomaly cancellation permits charge deformations, and off-diagonal Yukawa connectivity can constrain them, but the physical flavor interaction graph and masses are not derived.

No measured physical constants, 3+1 Einstein graviton, complete chiral Standard Model, Born rule, efficient photonic BQP or complete TOE have been derived.

## Reproduce

    python analysis/toe_20261119_multicopy_particle_ssr_pascal_chsh.py
    python -m pytest -q tests/test_toe_20261119_multicopy_particle_ssr_pascal_chsh.py tests/test_toe_20261119_five_linked_torus_center_SSR_histories_flavor.py

Program: analysis/toe_20261119_multicopy_particle_ssr_pascal_chsh.py
Focused tests: tests/test_toe_20261119_multicopy_particle_ssr_pascal_chsh.py
Machine-readable certificate: data/toe_20261119_multicopy_particle_ssr_pascal_chsh.json

On Windows, 27 additional independent tests passed alongside the previous five-front 43: **70 passed**. Lucas parity was independently checked through row n=59; explicit SSR-valid observables and Bell expectations through n=8.

## Five independent next falsification priorities

1. Compile the n=4 and n=8 number-conserving collective Bell observables into actual interferometers, ancilla supplies and detectors, then price the depth/energy/loss budget. An exact CHSH theorem is not a scalable BQP implementation.
2. Derive a genuine Lorentzian 3+1 causal Dirac operator and physical oriented gauge flux without inserting a torus, gamma matrices or regulator-mass branch.
3. Couple real chiral fermion determinants to the SU2 center-sensitive line sectors, impose anomalies and RG, and see whether any one bare gauge-action family is selected dynamically.
4. Build an unlabeled causal-history quantum measure with automorphism weights, local causal propagators, a positive decoherence functional and a manifoldlike 3+1 Einstein comparator.
5. Obtain the observed neutrino, charged-lepton and quark flavor interaction graph and masses from the same microscopic causal spin/gauge structure rather than an assumed Yukawa edge set.

## Scientific conclusion

The Pascal-law discovery is an exact, conditional many-copy quantum-resource consequence of standard physics, not a new fundamental quantum law. The most consequential TOE keystone remains the intrinsic 3+1 **oriented causal Dirac construction plus its physically derived matter interactions**. A single such construction could turn multiple otherwise arbitrary choices—chirality, matter determinants, global spin/gauge sectors and quantum-history corrections—into calculations.
