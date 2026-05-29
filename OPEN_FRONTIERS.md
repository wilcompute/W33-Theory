OPEN FRONTIERS and TODOs
========================

This file collects the remaining open/frontier tasks referenced across the
W33 repository and the paper (solvable computational tasks, verification
targets, and experimental priorities). Use this as the single short index
for active work.

Recent upstream breakthroughs
----------------------------

The repo recently accepted several E6-related theorem packets (see git
history). These close several algebraic/combinatorial frontiers and should be
referenced by downstream verification and transport tasks:

- MCCCXC: E6 Minuscule 27 × A2 phase factorization — `analysis/w33_e6_minuscule_27_a2_phase_factorization.py` and tests
- MCCCXCI: E6 45 tritangent zero-sum bridge — `analysis/w33_e6_45_tritangent_zero_sum_bridge.py` and tests
- MCCCXCII: E6 36 double-six bridge — `analysis/w33_e6_36_double_six_bridge.py` and tests
- MCCCXCIII: Spread / double-six association scheme — relation between 36 W33 spreads and 36 E6 double-sixes

These results mean many previously-listed combinatorial checks (Schlaefli graph
factorizations, triangle/triangle-cover certificates, and spread/double-six
overlap verifications) are now available as executable artifacts. When running
transport or continuum-lift audits, prefer the promoted E6 artifacts for any
Schlaefli/27-weight related lookups.

Latest tetracode / E8 developments
---------------------------------

Two recent pushes add a concrete E8 realization from a W33-derived tetracode
and a matching E8→E6×A2 coordinate decomposition. These provide an explicit
240-root E8 lift and a precise coordinate branching that is useful for
transport-to-curved lifts and for constructing exact finite Dirac/heat-trace
experiments.

Key artifacts:

- `analysis/w33_tetracode_e8_root_system_bridge.py` — constructs the 240 E8
  roots from a W33 tetracode over four A2 planes and verifies full reflection
  closure and simple-root extraction.
- `analysis/w33_e8_e6_a2_coordinate_decomposition.py` — coordinate branching
  E8 → E6 × A2 decomposition and the 240 = 72_E6 + 6_A2 + 81 + 81 split.
- `PART_MCCCLXXXVIII_TETRACODE_E8_ROOT_SYSTEM_BRIDGE.md`
- `PART_MCCCLXXXIX_E8_E6_A2_COORDINATE_DECOMPOSITION.md`

Use these artifacts when assembling finite-to-curved handoffs that require an
E8 lift or when cross-checking E6-sector decomposition claims. They also
strengthen the combinatorial base used by the transport/holonomy search
because the E8 realization provides exact lattice data and reflection
generators that are helpful for building canonical selectors and verifying
local curvature/cohomology checks.

1) Transport / Holonomy frontier

--------------------------------

- Goal: produce a concrete, executable selection of the holonomy/golden
  selector that lifts the W(3,3) internal 120-state matching to an H4/600-cell
  skeleton where required, or else provide a rigorous obstruction witness.
- Artifacts:
  - PART_CDIII_GOLDEN_SELECTOR_H4_HOLONOMY.md
  - PART_CDIII_GENUS_TOWER_VERIFIER.py
  - PART_CDVI_heterotic_verifier.py
  - PART_CDIX_COMPLETE_TOE_DICTIONARY.md
  - PART_CDVI_DISCRIMINANT_37_HETEROTIC.md
- TODO: implement a numerical search and symbolic classifier that either
  (a) finds consistent local holonomy assignments for small hosts, or
  (b) produces a certificate of obstruction (cohomology class / parity)
  for the full symmetric action. See scripts/g3_holonomy_analysis.py.

1) Continuum lift / Spectral Action

-----------------------------------

- Goal: complete the continuum spectral-action derivation from the finite
  Dirac/Hashimoto spectrum (trace-tower -> heat-kernel coefficients ->
  Einstein/Higgs couplings).
- Artifacts:
  - PART_CCCCXXXIV_FINITE_SPECTRAL_ACTION.md
  - PART_CCCCXIV_integrated_q4_packet_subsystem_matrix_results.json
  - scripts/V29_SPECTRAL_ACTION_STIFFNESS_Q.py
- TODO: run explicit numeric spectral truncation experiments and produce
  verified limits for a few heat-kernel coefficients. Add a notebook
  showing convergence rates.

1) Gold/icosahedral selector (H4) and no-go sharpening

------------------------------------------------------

- Goal: tighten the full-symmetry no-go theorem for a 600-cell skeleton on
  the 120 matching states; either (a) construct an explicit invariant
  embedding, or (b) give a computer-checked proof that none exists.
- Artifacts:
  - PART_L_M and PART_M (internal H4 shadow, obstruction proofs)
  - verify_dccliv_frobenius_selection_and_ouroboros.py
- TODO: exhaustive search across symmetry-preserving assignments for
  small stabilizer subgroups; formalize obstruction in group-cohomology
  language and add a unit test.

1) Delta-C (=14105) witness activation

--------------------------------------

- Goal: implement the witness activation script that constructs the exact
  affine witness point tied to the Delta-C = 14105 transport target and
  verify its invariants under the stabilizer subgroup.
- Artifacts:
  - PART_CDIII_DELTA_C_14105_WITNESS_ACTIVATION.md
  - scripts/verify_dcclxiv_reciprocity_rigidity_lazy_deformation_bridge.py
- TODO: produce a small Python module that constructs the affine witness
  (with exact integer arithmetic) and unit tests that certify its
  invariants (orbit sizes, inner-product checks).

1) Experimental falsifiers and forecast pipeline

-----------------------------------------------

- Short list of highest-priority tests: CMB-S4 (n_s), JUNO (theta_12), DUNE
  (theta_23), HL-LHC/FCC (Higgs self-coupling), H0 fixed-point analysis.
- Artifacts:
  - EXPERIMENTAL_HITLIST.md
  - PART_DCCCXIX_EXPERIMENTAL_ROADMAP.md
- TODO: add a small reproducible pipeline (notebook + scripts/W33_PREDICTIONS.json)
  that downloads current central values and computes deviations for the
  repository's predictions; add continuous-integration checks that fail if
  new experimental averages move beyond stated tolerances.

1) Cyclotomic defect / split-prime packet completion

----------------------------------------------------

- Goal: finalize the completed defect Dirichlet product analytics, complete
  the odd Taylor tower, and publish the cut-off error bounds as code and
  reference notebooks.
- Artifacts:
  - PART_MCIV_EISENSTEIN_LOCAL_GLOBAL_VALUATION_THEOREM.md
  - PART_DCMLXXXVIII_CYCLOTOMIC_CRT_BRANCH_FACTORIZATION.md
- TODO: implement numerical routines in scripts/ that compute the completed
  factors up to large cutoff and expose convergence diagnostics.

1) Small reproducibility and cleanup TODOs

-----------------------------------------

- Add short tests that assert the core SRG matrix (W33 adjacency) and
  the Dirac spectral determinant Z(x) coefficients (E8/Octonion checks).
- Ensure scripts/verify_substrate_predictions.py is used by CI (pytest).

How to use this file
--------------------

- Pick a frontier above and open an issue or PR naming the specific
  artifact you will modify. Link to the artifact paths above.
- Add unit tests under tests/ and reference them in the PR. Keep tests
  small, deterministic, and fast.

Contact
-------

If you pick a frontier and need orientation, open an issue and mention
"@repo-bot". See SESSION_HANDOFF.md for pointers.
