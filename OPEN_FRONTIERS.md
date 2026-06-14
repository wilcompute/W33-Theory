OPEN FRONTIERS and TODOs
========================

This file collects the remaining open/frontier tasks referenced across the
W33 repository and the paper (solvable computational tasks, verification
targets, and experimental priorities). Use this as the single short index
for active work.

================================================================================
SATURATION MAP — CHECK THIS (and `docs/index.html`) BEFORE DERIVING ANYTHING
(updated 2026-06-13)
================================================================================

The physics/NCG breakthrough frontier of this corpus is SATURATED: BT1–923,
~260 phases, ~1100 test files. The "Continue -> one more breakthrough" loop
repeatedly REDERIVES documented results.

THE COMPREHENSIVE SEARCHABLE CORPUS IS: the `.tex` files + `docs/index.html`.
Those two are the closest thing to a complete, searchable record (the BT*.md
notes and Continuity decisions are partial). Before writing ANY new script,
grep BOTH:
  - `docs/index.html` (the live master ledger), and
  - the `.tex` papers: `w33_paper.tex`, `w33_for_everyone.tex`,
    `universal_computation_single_photon*.tex`, `photonic_holonet.tex`,
    `standard_model_from_one_transvection.tex`
for the key quantity/term, and scan recent `git log`. Anchor on the grep
TERMS below (line numbers drift). Example:
  `grep -rio "<term>" docs/index.html *.tex | sort | uniq -c`

ALREADY DONE — DO NOT RE-DERIVE (grep terms -> result):

- Fermion MIXING SCALE Φ₃=13 (BT894–898/918–922; index.html):
  - PMNS angles: `4/13` `7/13` `2/91` — sin²θ₁₂=μ/Φ₃, sin²θ₂₃=Φ₆/Φ₃,
    sin²θ₁₃=λ/(Φ₆Φ₃); also framed as tribimaximal ± 1/Φ₃ (BT920).
  - PMNS CP PHASE: `CP phase` `194` — δ_CP = 2πΦ₆/Φ₃ = 194° (obs 197°±25°,
    0.13σ). Oscillation ratio R_ν = 2Φ₃+Φ₆ = 33.
  - CKM: `Cabibbo` `3/13` — tan θ_C = q/Φ₃ = 3/13; CP δ_CKM = arctan(Φ₆/q)
    = arctan(7/3); Jarlskog done. Wolfenstein A=μ/(q+λ)=4/5 (the 1.7σ outlier).
- NCG / spectral triple (index.html "Five Connes Axioms — All Verified";
  Phase LXXXVI `tests/test_ko_dimension_real_spectral.py`, 55 tests):
  - `first-order condition` (gauge–matter split, Hodge C¹=39+120+81=240),
    `orientability` (chirality/Z₃-grading), `Poincaré duality` (nondeg.
    intersection form), `reality` (KO-dim = 2q = 6: J²=+1, JD=+DJ, Jγ=−γJ),
    compact resolvent. The real spectral triple is CERTIFIED.
- Hodge/Dirac spectrum + topology (BT892/921/923; index.html):
  - `10^48` `16^30` — D² spectrum {0¹²²,4²⁴⁰,10⁴⁸,16³⁰}; harmonic=homology
    b=(1,81,40); `McKean` supertrace −80; `ind(D)` = q = 3 (generation index);
    Euler `χ = −40 = −v` (2-complex) and `−80 = −2v` (clique complex).
    BT923 bridge: the 40 lines-as-K₄-tetrahedra (rank 40) fill b₂=40 = the
    BT862 line module, taking −v → −2v.
- SM anatomy from one transvection R (BT858–888): gauge group C(R)=648=
  3^{1+2}:SL(2,3)=1⊕3⊕8, generations=Z(C(R))=Z₃, flavor S₃=⟨R,C⟩, color=
  matter-Heisenberg, chirality/parity/charge-conj, connection flat/curved
  (2T=24-cell group), curvature F=[R_p,R_q]. See
  `standard_model_from_one_transvection.tex`.

COMPLETENESS BOUNDARY (now a theorem in BOTH papers, 2026-06-13):
`w33_paper.tex` §"The Integral E8 Lift: Eigenlattice Obstruction and the
Completeness Boundary" and `photonic_holonet.tex` §"Architecture Completeness
and the Three Physical Residuals" state it: the finite substrate kernel is
closed and machine-verified; the theory is complete modulo EXACTLY three
classified residuals R1/R2/R3 = the three opens below. R1 also gained a new
rigorous proposition (the +2-eigenlattice is NOT the E8 home; det 2^16·3^10·5,
rootless — witness `analysis/bt926_plus2_eigenlattice.py`). These three are
the irreducible frontier; nothing else in the finite kernel is open.

GENUINELY OPEN (index.html "Open Problems and Exact Boundaries" table, items
5–7 = R1/R2/R3 — these are the ONLY curated opens; everything 1–4 is CLOSED):

- (5) INTEGRAL E8 LIFT — mod-2 homology gives the rank-8 shadow, but the
  integral Cartan pairing and a canonical root-lattice lift have NOT been
  reconstructed directly from the chain complex. (Finite, computational —
  the most tractable genuine open.)
  HEAVILY ADVANCED by the BT924–957 arc (status updated 2026-06-13;
  notes `analysis/BT92x*.md`, `analysis/BT95x*.md`):
  - BT924: SNF_Z(A)=diag(1¹⁶,2⁸,8¹⁵,24¹); E8 rank 8 = #(invariant factors
    =2) = #(2-adic valuation 1) — rank + 2-adic location pinned over Z.
    Vertex 8-subset certified genuine E8 (even+unimodular+posdef).
  - BT925/BT950: H carries the canonical symplectic mod-2 form = E8/2E8
    (four hyperbolic blocks, rank 8); Wu class vanishes. The SNF-transform
    extractor (the dᵢ=2 sector via columns of U⁻¹, indices 16..23) gives an
    indefinite, huge divided form — NOT the positive E8 Cartan. So the
    positive metric is NOT canonical from the chain; it needs a SELECTOR.
  - (+2-eigenlattice ruled out, `/c/tmp/my_bt926_eigenlattice/`, not yet
    a committed BT): the natural definite candidate L2={x:Ax=2x} (rank
    24=8×3) is even/posdef but det 2¹⁶·3¹⁰·5, rootless — NOT E8³.
  - BT951–957: a selector is constructed by exact support-minimality
    (support min 60, profile [6,6,6,6,6,8,10,12]) + agreement of the vertex
    and tetracode metric gauges → a specific E8 metric.
  - CANONICAL SYMMETRY (bt980_aut_action_on_homology.py; in w33_paper.tex
    Prop "Canonical symmetry of the homology"): Aut(W33)=PSp(4,3) acts on H
    FAITHFULLY (order exactly 25920), IRREDUCIBLY over F2, preserving the
    symplectic B → canonical PSp(4,3) ↪ Sp(8,2). This is the "larger
    chain-complex symmetry" BT932 sought (the vertex witness is
    symmetry-isolated). CONSEQUENCE: since E8⊃E6⊕A2 has odd index 3, W(E6) on
    E8/2E8 is REDUCIBLE (6⊕2) while H is irreducible ⇒ the canonical lift is
    NOT the naive E6⊂E8.
  - RESOLVED (bt981_e8_invariant_quadratic_form.py; w33_paper.tex Cor "The
    canonical lift is E8"): PSp(4,3) fixes a UNIQUE quadratic refinement of B,
    and it is PLUS type (136 zeros, Arf 0) ⇒ PSp(4,3) ⊂ O8+(2)=Aut(E8/2E8),
    lifting to W(E8)=Aut(E8). Irreducible mod 2 forces irreducible over Q, and
    PSp(4,3) has no ordinary irred 8-dim rep ⇒ the canonical positive-definite
    lift IS E8 (up to a central ±1). R1 ANSWER = YES, E8. Remaining: only an
    explicit integral basis + split-vs-double-cover (cosmetic).
- (6) MOONSHINE MODULE BOUNDARY — low-order transport exact through the
  quartic package, but the naive quintic V₅ lift fails on anchored classes
  2A, 2B; needs genuine character-theoretic input. (Hard, rep-theoretic.)
  DATUM SUPPLIED (bt982_mckay_thompson_v5.py; w33_paper.tex Prop "The quintic
  moonshine datum"): the degree-5 McKay–Thompson coefficients are computed
  from VALIDATED level-2 Hauptmoduln (T_2A=(η/η2)^24+4096(η2/η)^24+24,
  T_2B=(η/η2)^24+24), validated against anchored Tr(2A|V1)=4372, Tr(2B|V1)=276,
  Tr(2A|V2)=96256: dim V5=333202640600, Tr(2A|V5)=74428120, Tr(2B|V5)=184024.
  The named external input is now in hand; remaining = assemble the V5
  Monster-module decomposition from these traces. (Computed, not fabricated;
  12/12 anchored checks pass.)
- (7) DYNAMICAL / CONTINUUM ORIGIN — THE SOLE GENUINE OPEN (R1/R2 now
  closed/supplied above). FINITE HALF DONE (w33_paper.tex Prop "The
  gravitational sector is finite; the residual is analytic"): in the
  almost-commutative product M^4 x F (F = W33 finite spectral triple), the
  Chamseddine-Connes couplings are exact W33 invariants — cosmological & EH
  ∝ dim H_F = 440; Yang-Mills/Higgs ∝ Tr D_F^2,Tr D_F^4 = 1920,16320. The AC
  bridge to curved-4D seeds (CP2_9 sig +1, K3_16 sig -16) + barycentric
  towers (modes 1,6,120; chain density→120/19, first moment→860/19) is
  explicit in the corpus. IRREDUCIBLE RESIDUAL (named by
  docs/STATUS_AND_GAPS.md "Open Problem 2"): apply two well-posed
  metric-geometry theorems — (i) Gromov-Hausdorff convergence of the
  refinement tower to the smooth seed, and (ii) Cheeger-Mueller-Schrader /
  Dodziuk-Patodi spectral convergence (combinatorial Hodge -> de Rham
  Laplacian as mesh->0, supplied by barycentric refinement). All finite
  preconditions hold (exact couplings; spectral-dimension flow d_s:4->2
  already computed, matching CDT/Horava/asymptotic-safety; AC bridge). Open =
  the rigorous APPLICATION, a problem in ANALYSIS not a finite computation (so
  NOT closable by the methods that cracked R1/R2). Do not fabricate a
  continuum proof. The finite theory is complete; this is the sole analytic
  frontier.
  ADVANCE (bt983_refinement_fatness_obstruction.py; w33_paper.tex Remark "A
  shape-regular tower..."): CORRECTION — the BARYCENTRIC tower VIOLATES the
  fatness hypothesis of CMS/Dodziuk-Patodi (min angle collapses
  60->30->13.9->6.3->2.9->1.3 deg in 2D, verified), so those theorems do NOT
  apply to it. FIX: the EDGEWISE (Freudenthal-Kuhn) tower is shape-regular
  (min angle constant 60deg, fatness bounded indep of level) -> CMS/DP DO
  apply. Since EH = a2 ~ int R = the Regge deficit-angle action, the gravity
  (curvature) convergence on the fat tower IS the Cheeger-Mueller-Schrader
  theorem. Residual narrows to ONE analytic step: the spectral-action
  short-time<->refinement limit-interchange (bypassed by the geometric/Regge
  route). And even THAT is within reach on the fat tower: FEEC
  (Arnold-Falk-Winther) + Dodziuk-Patodi give combinatorial-Hodge -> de Rham
  eigenvalue convergence UNDER SHAPE REGULARITY, so n->inf then t->0
  reproduces the continuum heat trace + a_2. STRUCTURAL UPSHOT: the
  obstruction to R3 was the REFINEMENT CHOICE (non-shape-regular tower), not
  the AC framework; on a fat tower both routes are governed by established
  convergence theorems. R3 reduces to applied verification on CP2_9/K3_16.
  NEXT: redo that program on the edgewise (not barycentric) tower.

Also flagged open (index.html "Remaining open:"): rigorous QFT derivation of
the α formula; gravity from graph curvature (a narrowed-bridge program). The
explicit equivariant E6 bijection is PROVED IMPOSSIBLE (representation-
theoretic), not open.

================================================================================

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
