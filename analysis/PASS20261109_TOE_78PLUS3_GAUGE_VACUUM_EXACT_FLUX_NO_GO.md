# TOE research pass: W33 gauge vacuum, exact flux counterexample, photonic hardware, and falsifiers

**Research date:** November 9, 2026, US Eastern (remote process logs may read November 10 UTC).
**Repository:** wilcompute/W33-Theory, master.
**Scope:** Seven new executable physics/mathematics experiments, frozen data, and twenty dedicated regressions. This pass derives exact finite-geometry theorems and synthetic source/detector consequences. It does **not** derive the Standard Model, spacetime, gravity, fundamental constants, or a physical theory of everything.

## Core reconciliation of October TOE38/TOE61 and November 9 15-link exact determinant work

Already established, not newly claimed:

- W33 Levi incidence graph: 40 point nodes, 40 line nodes, 160 edges, 1,620 shortest octagonal cycles, 81 full graph fundamental cycles.
- TOE38's three-deck embedded construction: 1,382 *zero-deck-winding* shortest octagons and 238 winding octagons. The 1,382 local rows have rank 78; three topological holonomies remain.
- TOE61's exact all-positive-temperature finite free-fermion theorem: within **eight** selected Z2 deck holonomy sectors, the three-\pi corner dominates all others, even with a common staggered mass. This was NEVER established as global selection among all Z2/U1 link phases.
- The preceding November 9 pass: native W33 incidence rank 25 and 30 balanced dark states; 15 phase-only link changes are both necessary and sufficient to lift all 30. For one explicit set, det B(z)=-2(z-1)^15; exact signed determinant 65536 at z=-1. No physical gauge action was derived.

This pass connects the discrete deck sector to the wider gauge space, tests whether all shortest cycles provide a globally faithful U1 gauge action, and moves several photon experiments toward physically meaningful controls.

## Front 1. Exact integer octagon basis: 81 real shortest cycles suffice to detect every U1 holonomy

**Scripts:** analysis/w33_20261109_full_octagon_integer_gauge_basis.py and analysis/w33_20261109_deck_octagon_78_3_basis.py.
**Frozen data:** correspondingly named data/*.json.

Gauge-fix a spanning tree of the 80-node connected Levi graph, removing 79 vertex rephasing freedoms. The residual physical U1 connections live on the 81 graph chords. For each of 1,620 ordinary shortest 8-cycles, record its **oriented integer** passage over each chord. The result is a 1,620×81 signed integer matrix C.

The rank of C is exactly 81 mod each of 2,3,5,7,11. More importantly, a deterministic mod-2 independent-row selection found an **81×81 integer minor with det +1**, verified with SymPy's exact integer determinant. This proves those eighty-one shortest loops form a *unimodular* Z-basis of the full graph cycle lattice, not merely a basis over R or over a few finite fields.

An independent construction on the older TOE38 three-deck graph, ordering the 1,382 local zero-winding octagons before the 238 winding octagons, produced the exact finer splitting:

    78 selected zero-deck-winding shortest octagons,
     3 selected winding shortest octagons,
    81 basis loops, exact determinant = +1.

Selected winding vectors are (0,-1,0),(-1,0,0),(0,0,1): an integer basis of all three deck cycles, up to orientation. The zero-deck set has exact modular rank 78, the full set rank 81.

**Proof-level consequence:** If every one of these 81 selected Wilson phases is zero modulo 2π, all 81 chord phases are zero modulo 2π because an integer unimodular inverse exists. Therefore a compact U1 action

    S_alloct = κ * Σ_(all 1620 shortest octagons) [1-cos Φ_C], κ>0,

has a **unique zero-action gauge orbit**, namely pure gauge / flat. There is no hidden torsion or invisible discrete flat connection.

**CRITICAL PHYSICAL DISTINCTION:** The TOE38 *local* three-deck plaquette action contains only 1,382 **zero-winding** octagons. It has three harmonic flat directions and all eight 0/π deck sectors are degenerate under its magnetic term. Adding 238 winding shortest cycles to make the all-octagon action imposes new constraints; those shortest graph loops may wrap the deck and need not be local in any desired spatial embedding. The two are genuinely different **chosen** actions. The mathematics does not select which constitutes physical local dynamics.

## Front 2. Exact all-beta counterexample to extrapolating TOE61's eight-sector minimum

**Script:** analysis/w33_20261109_outside_deck_flux_counterexample.py.
**Data:** data/w33_20261109_outside_deck_flux_counterexample.json.
**Focused tests:** tests/test_w33_20261109_outside_deck.py.

Let K_c=B_c B_c^T with B_c a real signed unit-hopping 40×40 W33 incidence matrix. Exact polynomials P_c(t)=det(I+t K_c) have forty-one **integer** elementary-symmetric coefficients. Reconstructed the old TOE61 c=000 and c=111 coefficient arrays exactly from the current independent representation, despite differing point/line vertex order.

For BOTH the original fifteen-link and independently gap-optimized fifteen-link π phase assignments, exact SymPy characteristic polynomials satisfy

    P_15(t)-P_111(t) has 41 coefficients:
    0 negative; 37 strictly positive; first strict difference at degree 4.

Thus P_15(t)>P_111(t) for EVERY t>0. By precisely TOE61's Weierstrass product for cosh,

    F_beta(15-link π) < F_beta(three-π deck) for ALL beta>0

at zero chemical potential for the specified finite half-filled spinless free-fermion Hamiltonian. The old fifteen-link configuration also coefficientwise dominates the gap-optimized fifteen-link version in 36 coefficients, so it has strictly lower fermion F for all beta>0 despite a smaller spectral gap.

At beta=1:
- flat F=-87.5934482707;
- three-π deck F=-87.6225006604;
- original 15-link F=-87.6879510277;
- gap-optimized 15-link F=-87.6857318783.

This is a new **exact counterexample to any proposed unrestricted-global-minimum inference** from TOE61's eight-deck-sector theorem. It **does not contradict** TOE61, which was correctly scoped to just eight sectors. It also does NOT prove the 15-link pattern is globally optimal over all 2^160 Z2 edge assignments or the continuous U1 connection space, or that a dynamical gauge theory selects it.

## Front 3. Local positive magnetic octagon action versus fermion free energy

**Script:** analysis/w33_20261109_octagon_gauge_matter_tradeoff.py.
**Data:** corresponding frozen JSON.

Enumerate all 1,620 ordinary simple 8-cycles and compute the π-flux parity from explicit signed edge assignments. For action coefficient κ>0, each π-frustrated octagon contributes **2κ** to S_mag.

| π-link sector | Frustrated eight-cycles | S_mag / κ |
| --- | ---: | ---: |
| flat | 0 | 0 |
| TOE61 three-π deck | 233 | 466 |
| original 15-link | 745 | 1490 |
| gap-optimized 15-link | 729 | 1458 |

At beta=1, fermionic free-energy gains relative to flat are respectively 0, 0.02905239, 0.09450276 and 0.09228361. If ONLY flat and gap-optimized fifteen-link sectors are allowed, their static energy/free-energy order crosses at κ=0.0000632946554 in the **explicit arbitrary graph hopping and Wilson normalization**. This crossing is *not* global 81-dimensional minimization and not an experimentally derived coupling. At fixed finite size, call it a level crossing of restricted sectors, not a thermodynamic phase transition.

The distinction between 1,382 local zero-winding octagons and all 1,620 graph-shortest cycles is crucial. Under the local-1382 model, 0/π deck sectors have zero *magnetic* cost and TOE61's free-fermion prior selects c=111 among those eight. Under the all-1620 model, c=111 carries a nonzero magnetic cost and the pure-gauge vacuum is uniquely flat. An actual physical flux selection must specify the permitted noncontractible terms, gauge dynamics, matter backreaction and coupling strength.

## Front 4. Improved 15-link spectral gap and 15D low-phase mass splitting

**Script:** analysis/w33_20261109_flux_mass_gap_design.py.
**Data:** corresponding JSON.

For B(theta)=B+(e^(i theta)-1)E_S supported on fifteen links, restrict the perturbation to the 15 point-dark and 15 line-dark singular subspaces. Their 15×15 projected coupling M_dark=U0†E_S V0 governs the small-angle splitting:

    15 positive near-zero singular energies =
    |e^(i theta)-1| singular_values(M_dark) + O(theta²).

An independently seeded 500-support search, with 2,400 unsuccessful local swap attempts, found a second valid 15-link configuration. At θ=π its full signed 40×40 matrix is invertible and has smallest singular energy **0.15596086806**, up from the previously frozen **0.11547329685**: a **35.1% increase** in the minimum spectral gap with the same number of flipped edges. Its exact signed determinant is −65536.

This is a discrete 15-link **device-design** improvement, not a global spectral-gap optimum and not derived Standard Model mass eigenvalues. The fermion free energy and positive Wilson cost actually favor different 15-link objectives; optimizing a single numerical criterion cannot be substituted for a physical field action.

## Front 5. Actual nearest-neighbor chain optical preparation and independent losses

**Script:** analysis/w33_20261109_dark_nearest_neighbor_loss.py.
**Data:** corresponding JSON.

For a 40-rail one-dimensional nearest-neighbor optical network fed from one END port, depth d can populate only ports 0 through d. The exact W33 dark-frame target has nonzero amplitude on port39, so **depth≥39**. Constructed 39 sequential nearest-neighbor Givens rotations with 12 π phase corrections: reaches the target vector exactly and saturates the locality lower bound.

The earlier **six-layer** 39-coupler tree assumes arbitrary long-range mode pairings: its fast depth cannot simply be claimed for a one-dimensional chip. At intensity survival 0.99 for each physically addressed pair, actual gate-by-gate nonuniform mode attenuation yields source survival 0.90449878 in the native-label chain, or 0.93084214 if ports are arranged in decreasing target intensity. The latter is not free: it changes the physical W33 incidence wiring and may require extra routing/switches. Conditional target fidelity in the natural-label chain is 0.9974813 for this loss-only model. No actual fabricated chip, source heralding or 80-mode graph evolution demonstrated.

## Front 6. Exact all-trials photon-dark null hypothesis test

**Script:** analysis/w33_20261109_dark_photon_binomial_gate.py.
**Data:** corresponding JSON.

Initialize the previously derived 40-port W33 dark-frame state, evolve using H=[[0,T],[T†,0]], and measure whether a line-sector photon is present, counting **all** launched trials including no-clicks. The singular-value formula for P_line(t) was verified independently against an 80×80 matrix exponential. Maximize P_line for t in [0.01,6] under a precisely known test Hamiltonian:

| Selected π edges | Chiral exact zero modes of H | Maximum line probability for the original initial dark state |
| --- | ---: | ---: |
| 0 | 30 | 0 |
| 1 | 28 | 0.01109 |
| 14 | 2 | 0.59223 |
| 15 | 0 | 0.68015 |

At **assumed, independently known** source survival .95, line photon detector efficiency .85, and dark background probability between .0008 and .0012 per launched trial, the exact one-sided binomial test with false-positive size≤5% and power≥95% gives optimistic trial counts **793**, **5**, **4** for one, fourteen, fifteen flips respectively. The small counts for large perturbations are only possible because the *ideal specified alternative* is extremely far from the null and every hardware/model parameter is assumed separately calibrated. They are NOT achievable real-photon counts, physical black-box model identification, universal Bell certification or spectral-nullity measurements. Fixed-initial-state leakage cannot distinguish that two exact zero modes still exist at fourteen flips; direct spectral probes would be needed.

The actual laboratory may have internal graph loss/dephasing, mode-dependent detectors, source-state preparation errors, unknown phases, altered propagation and unheralded trials. None are covered by this small binomial model.

## Front 7. Independent DES Y6 release review and immutable S9 test

The publicly available DES Y6 3x2pt paper has been accepted in Physical Review D on 2 November 2026, DOI https://doi.org/10.1103/nnlj-gyr2; its published ΛCDM S8=0.789±0.012 and wCDM parameters are **not** equivalent to the frozen user S9 full-vector shear likelihood.

Ran the existing strict provenance/evidence gate live again against the official DES Y6 archive and release portal. All three inspected official pages returned HTTP 200 HTML, but **no authenticated complete unblinded xi± FITS vector, matching covariance, source n(z), unmodified angular cuts, corrected scalar-field CLASS/Halofit theory outputs, and nuisance refits** was acquired together. The manifest attack suite rejects five deliberately incomplete/fabricated evidence manifests; the 2026-11-08 frozen claim SHA-256 remains unchanged. S9 stays **UNSCORED**.

Original live audit code: analysis/w33_20261109_s9_frozen_manifest_attack.py; original corresponding frozen JSON is updated by the read-only rescan. Public source: https://www.darkenergysurvey.org/des-y6-cosmology-results-papers/ .

## Verification

The new tests, tests/test_w33_20261109_flux_five_plus.py (15 tests), independently regenerate the graph integer minor det=1, compare the three-deck 78+3 split, re-evaluate exact 15-link signed determinant, the local octagon penalties and free-fermion values, nearest-neighbor preparation, and binomial sample-size confidence.

Five additional tests, tests/test_w33_20261109_outside_deck.py, independently recompute EXACT characteristic arrays for TOE61 c=111 and both fifteen-link sectors. The first run caught a mistaken elementwise B support comparison across **different vertex labelings**; the code was corrected to verify 160 unit-magnitude hopping links and native-support conservation for the two fifteen-link patterns. After this correction **all 20 new tests pass**. Previous seven-front and minimal-flux test suites remain available and should be rerun in the main checkout after synchronization.

No all-positive-temperature claim is based solely on sampled beta values: it rests on 41 exact integer characteristic coefficients and TOE61's proved Weierstrass product reduction.

## Top five independent next TOE research directions

1. **Find the physical gauge action, not just a gauge invariant:** compare local zero-winding plaquettes to all-shortest-octagon and higher-dimensional local cellulations. Build an actual constrained U1/Z2 Gauss Hamiltonian, include fermion determinant and finite temperature, and test the global vacuum across the complete link configuration space. Optimize gauge energy, not a handpicked 15-link ansatz.
2. **Derive 3+1D local chiral matter:** prove a growing spatial/lattice limit with a genuinely nonzero protected chiral index, anomaly-free representations, correct mass hierarchy and locality. W33's finite balanced 15+15 dark modes and gap manipulations alone are not a Weyl fermion or SM generation.
3. **Compile and falsify the 80-mode photonic network:** quantify two-mode routing depth, end-to-end internal loss, mode-dependent source/detector efficiency, all-trial null controls, singular-spectrum measurements, and the 15-link θ-dependent determinant signature on real supported hardware.
4. **Solve robust entanglement certification beyond optimistic Fisher budgets:** independently calibrate full POVM effects, source preparation and detector efficiency, establish valid finite-count coverage under drift and misspecification, and verify an arbitrary mixed PPT-entangled state witness with proper statistical independence.
5. **Score strictly preregistered physical predictions:** preserve the S9 claim and execute genuine DES Y6 likelihood using full official raw data and corrected models when verified; separately preregister photon Bell and spectral-flux tests with negative controls and equipment-level timing/noise assumptions.

**Bottom line:** the new mathematically exact contribution is the **78+3 unimodular octagon gauge basis** and an **all-temperature counterexample** to extrapolating the three-π restricted-sector flux ordering. These make the candidate gauge vacuum question precise and falsifiable. Neither derives a TOE or demonstrates new observed physics.
