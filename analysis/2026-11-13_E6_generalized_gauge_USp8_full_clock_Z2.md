# 2026-11-13 — E6 generalized gauge closure, complete USp8 intertwiner, and the Z2 clock double cover

## Executive result and explicit evidence levels

This pass independently tests the other assistant's section/clock hints against the LIVE W33-Theory repository after commit dc4a64588fab0e797109e33ca90277a958cfa433. Source files were checked; computations were executed locally on the authorized Windows host, not inferred from matching dimension counts. All scoped producers and JSON certificates are deterministic; a 14-test integration suite independently reruns the key results.

**Strongest mathematical result:** we now have a fully constructed **28x27 complex isometric intertwiner for all 36 generators** of the compact real Lie algebra usp(8) acting on the signed E6 27, and an explicit lift of the cubic-preserving Albert order-three clock to an **order-six** symplectic 8x8 element with cube -I8. The central -I8 disappears on Lambda²_0(C8). A proposed 35-mode two-representation interferometer would be able to distinguish that relative Z2 center phase.

**Additional advances:** exact affine and quadratic generalized E6 diffeomorphism closure on representative valid five- and six-coordinate sections, explicit constraint-breaking negative control, nonzero-but-trivial E-bracket Jacobiators, connected 53/57-dimensional Lie stabilizers with nilpotent radicals, an exact non-flat compact cubic gauge lattice, a restricted photonic repetition-code demonstration, and a fail-closed further size-eight MUB SAT pass.

These are mathematically precise embeddings of known exceptional Lie/gauge structures in this project's coordinate gauge. **They are NOT a new unification of gravity and quantum mechanics, a dynamical spacetime vacuum, a measured photonic implementation, or an independent replay of the parallel assistant's completed 433-million-node size-eight MUB exclusion.**

## 1. Provenance firewall: the two cubic files have different bytes, identical parsed invariants

The user-supplied parallel note claimed byte equality at pinned snapshot. On this local tree the two JSON files do NOT have the same byte hash or size:

| source | bytes | SHA-256 |
| --- | ---: | --- |
| artifacts/canonical_su3_gauge_and_cubic.json | 433282 | 13ea38ed37a8c1c9723db7168e1e056a2827ebf060bc096e227f8d9047d78cb1 |
| extracted_v13/W33-Theory-master/artifacts/canonical_su3_gauge_and_cubic.json | 406854 | 81444a3d3f2c93a2078bf23e3eea52f6b043ccb39b115aed4a9fbc62062ce135 |

**Important positive check:** the FULL parsed JSON objects compare equal under Python structural equality; all 45 signed cubic terms are identical. The seven exact ±1 coordinate rephasings reproduce the full det(A)+det(B)+det(C)-tr(ABC) polynomial term-by-term. Thus no mathematical input mismatch was found; the byte-identity assertion is corrected to SEMANTIC identity. Program: analysis/toe_20261113_E6_cubic_source_semantic_audit.py.

## 2. Generalized diffeomorphism closure on the actual sections

Prior pass constructed normalized dual tensors d_MNK=d^MNK=t_MNK/sqrt(10) IN THE SPECIFIC fixed signed Chevalley basis, with t integer ±1 on 270 permutations of 45 distinct cubic terms and full 78-generator covariant/contragredient checks. The section equation uses d^MNK partial_M⊗partial_N=0, not an arbitrary Euclidean scalar product.

For a generalized vector of weight 1/3 the published E6 generalized Lie derivative is, with Y^{MK}{}_{NL}=10 d^{MKR}d_{NLR},

 L_X V^M = X^K∂_K V^M - V^K ∂_K X^M
           + Y^{MK}{}_{NL}(∂_K X^L)V^N.

The exact integer coefficient identity tested is

 2( L_X L_Z V - L_Z L_X V )
      = L_(L_X Z - L_Z X) V.

An initial exact implementation treating 27-component fields and parameters as affine polynomials performed **32 independent closure controls on each** of the five- and six-axis representative sections, with zero residual, and verified a d-gradient trivial gauge parameter. On an intentionally forbidden derivative pair (E6 indices 0,17), the same code found **a nonzero integer closure residual of 12**. A closure implementation that always returned zero would fail that negative control.

A second **independent polynomial-dictionary engine** checks degree-at-most-two generalized parameter and vector fields: 10 randomized sparse exact-integer cases per section. All passed. In all 20 quadratic trials the E-bracket Jacobiator was a NONZERO vector-field parameter but its generalized Lie action was exactly zero, as the published tensor-hierarchy/Leibniz structure predicts. Tests distinguish "Jacobiator =0" (FALSE) from "Jacobiator is gauge trivial" (TRUE).

This is a finite reproducible coefficient test. The generalized-Lie formula and closure are established exceptional field theory, NOT a discovery that follows from the 27-line graph alone. Full smooth-field gauge closure and the 2-form tensor hierarchy are literature results but are not newly proved here.

Sources: Hohm–Samtleben, *Exceptional field theory I*, Phys Rev D 89 066016 (2014), arxiv:1312.0614; Kreutzer, *The canonical formulation of E6(6) exceptional field theory*, JHEP07(2021)145; see also https://edoc.hu-berlin.de/server/api/core/bitstreams/c2e61a8e-6617-4d02-a91b-df26fe5ff80a/content .

## 3. Connected Lie stabilizers, nonlinear maximality, and M/IIB Levi structure

For each representative S, build exact 78-generator linear equations X_{outside,S}=0. The nullspace is the full signed-cubic infinitesimal stabilizer of the coordinate section. Restrict the operators to S; verify their span is all gl(dim S). The kernel is a Lie ideal with a trace-form radical; its commutators are tested by explicit matrix multiplication.

| exact Lie invariant | S5 | S6 |
| --- | ---: | ---: |
| Ann(S) dimension | 5 | 6 |
| Full stabilizer dimension | 53 | 57 |
| Lie restriction image | gl5 dimension 25 | gl6 dimension 36 |
| Restriction kernel | 28 | 21 |
| Real-skew stabilizer | 11 | 15 |
| Kernel trace form rank | 3 | 0 |
| Two-step nilpotent radical | 25 | 21 |
| Nilradical derived algebra | 5 | 1 |
| Nilradical center | 5 | 1 |
| Levi quotient of restriction kernel | 3 | 0 |

Ann(S)=S proves the selected coordinate representatives are maximal against ANY extra 27D real linear direction, not only another coordinate axis. The rank-three kernel quotient on S5 is consistent with sl2; a separate explicit sl2 triple remains available from the parallel assistant, but the current script does not claim that it reconstructed an explicit E,H,F triple from scratch.

These exact stabilizer structures agree with the distinct parabolic types GL5xSL2 (IIB) and GL6 (M). Prior pass already exhaustively verified all 51840 W(E6) graph automorphisms, their 216/72 coordinate-section orbits and stabilizers 240/720. This strengthens the constructive dictionary, but neither orbit nor parabolic dimension is a physical derivation of gravity.

## 4. The Albert determinant/trace clock and its section action

The parallel assistant's explicit clock T(A,B,C)=(RA,B,CR^-1) with det R=1 was transported independently through the signed dictionary back to the original 27 E6 coordinates. It is a **signed permutation with 9 fixed coordinates and six 3-cycles**, exact orthogonal, order three, preserves all 45 signed monomials. Its infinitesimal S=(T-T^T)/sqrt(3) also preserves N exactly and has rank 12, S³=-S.

Across all maximal coordinate sections:
- 216 five-sections: 18 fixed, 66 three-cycles; restricted eigen spectrum (3,1,1).
- 72 six-sections: 12 fixed, 20 three-cycles; restricted eigen spectrum (4,1,1).

The generator uses 18 extra edges outside the original 108 chiral-null edges. Thus it is not a replacement for the earlier six-edge root-packet locality optimum with only THREE new edges. It is a distinct, exceptionally simple clock in the Albert determinant/trace geometry. These are algebraic compatibility facts, not a vacuum selection theorem.

## 5. FULL 36-generator USp8 defining representation — constructive highest-weight intertwiner

The old 28x27 map matched only four commuting Cartan generators. An independent audit against the explicit 36D standard compact usp8 Lie algebra found the old map fit exactly **4 of 36**, with worst non-Cartan relative residual ~0.99715. This prevented us from confusing equal weight characters with a complete matrix intertwiner.

The corrective construction directly builds four simple Chevalley root operators of C4 in both models:
- the repo's 27 real cubic representation from adjoint eigenvectors of its 36 exact skew packet matrices;
- the conventional 8 complex symplectic representation and its induced 28 antisymmetric wedge, with the symplectic singlet deleted.

Normalize the simple-root operator norms, choose the unique highest-weight vector of the 27 (omega2), and descend through all simple-root lowering paths. **108 lowering attempts construct a 27-vector basis**, with worst path-invariance residual about 1.08e-14, and an explicit 28x27 map T has isometry residual ~1.24e-14.

For **all 36** repo generators K_i, independent projection gives real linear combinations of standard complex 8x8 usp8 matrices A_i satisfying

 T K_i = rho_Lambda2(A_i) T,

with maximum relative norm residual ~1.09e-14 in the producer. An independent group check (reconstructing the 8x8 matrices from serialized 12-decimal T) gives max residual <9e-13, and checks several noncommuting Lie brackets. The actual T (real/imag separate arrays) is persisted under data/toe_20261113_USp8_full36_highest_weight_intertwiner.json.

The proof is **numerically high precision with exact root-system input**. For a fully computer-algebra certified closed-form representation, one should reconstruct the entries in an appropriate algebraic number field and verify equality coefficientwise. That is open.

## 6. STRONGER RESULT: order-6 defining clock projects to order-3 cubic clock

Transport the exact order-three Albert 27D clock U through full T into the defining 8D usp8 Lie algebra. Its uniquely induced 8x8 generator A8 has (numerically to <1e-9)

  A8^2 = -(1/4) I8,
  spec(-i A8) = {-1/2 (multiplicity 4), +1/2 (multiplicity 4)}.

Thus define

  g8 = exp[(2pi/3) A8] = (1/2) I8 + sqrt(3) A8.

Then

  g8^3 = -I8, g8^6 = +I8,
  spec(g8) = {exp(+i pi/3) x4, exp(-i pi/3) x4}.

But -I8 is the **order-two center of USp8**, and acts trivially on the exterior square Λ²_0(8). Consequently the induced cubic 27D action has **U³=I27**, with 27 eigen multiplicities (15,6,6). The explicit group calculation checks

  Lambda²_0(g8) T = T U,

to maximum elementwise residual 7.69e-13, along with unitarity, symplectic form preservation, and exact source U³=I. The underlying E6/Usp8 representation theory is established mathematics; the contribution is an explicit matrix-level dictionary to THIS repository's signed Albert clock, with an unexpected central double-cover structure relative to the clock interpretation.

An important correction during the independent test: the first conjecture that A8 had rank TWO (one active symplectic pair) was FALSE. It has full rank eight with four positive and four negative half-frequency modes. The code's final certificate explicitly tests this and rejects the earlier speculation.

## 7. Outside-the-box experimentally falsifiable Z2 center witness using both irreps

On an ideal 35-mode optical direct sum C8 ⊕ C27, coherently apply the representation-compatible clock gate G=diag(g8,U27). After THREE steps, G³=diag(-I8,+I27), while after SIX steps G⁶=I35.

For any normalized states |a> in C8 and |b> in C27, take balanced coherent superposition (|a>⊕|b>)/sqrt(2). The return probability is **zero after three steps** and **one after six steps** (numeric certificates: ~8.2e-27 and 1.00000000000014). The central sign would be completely unobservable as an absolute phase within either standalone irrep, but appears as an INTER-IRREP relative pi phase.

A simple independent Gaussian relative phase jitter sigma=0.10 radians gives ideal expected nominal dark-channel probability (1-exp(-sigma²/2))/2 = 0.00249376, versus bright ~0.99750624. A physical experiment would require coherent interfacing of the two representation encodings, true gates, calibrated reference phase, and loss. This is a TESTABLE PROPOSAL rather than evidence for physical time, and the 8D group does not magically implement the 27D gate on eight paths.

## 8. Non-flat 729D compact cubic gauge lattice, exact Yang–Mills-like controls

Previous lifted clock was pure relabeling and flat. Construct 27 sites h in F3³ with 27 real cubic modes per site. Use two distinct noncommuting root packet rotations exp(pi/2 K_i), each an INTEGER signed 27x27 permutation and exact signed-cubic automorphism. Choose constant but NONCOMMUTING links along x/y; the plaquette Wilson commutator is nonidentity, has trace9 and order3.

Build the sparse 2187x729 covariant finite-difference operator D with two per-row nonzeros (4374 total). Its matter kinetic energy is the nonnegative integer psi^T D^T D psi and transforms exactly under independent site-dependent cubic-preserving compact E6 gauge matrices Q_h. Tests show
  L'=Q L Q^T, L=D^T D,
  E'[Q psi]=E[psi],
  N(Q_h psi_h)=N(psi_h),
  W'_h=Q_h W_h Q_h^T.
Every equation was explicitly checked as an exact integer matrix/vector identity. The chosen Wilson holonomy fixes 18 five-sections and 12 six-sections, resembling the Albert clock's section action; no equality or special conjugacy is inferred from matching counts alone.

This is a genuine NONFLAT finite lattice gauge configuration, but link matrices are external inputs, not selected by a derived Yang–Mills action; no anomaly-free chiral fermion matter or gravitational equations are demonstrated.

## 9. Encoded single-photon magic with restricted 3-qutrit shift protection

The 27-path compatible root clock creates a two-support nonstabilizer active output, with Wigner mana ln(1+1/sqrt3). Two active E6 addresses correspond under the H27 bridge to distinct F3³ mode labels. An explicit GL3(F3) affine Clifford permutation maps the output superposition into logical codeword support |000> and |111> of the 3-qutrit repetition code.

For the error set {I,X_1,X_1²,X_2,X_2²,X_3,X_3²} (seven operators), **all 49 Knill–Laflamme overlap matrices** were checked and equal δ_ab I3. In a toy independent shift error model with per-qutrit probability p=.02, the guaranteed correctly recoverable at-most-one-shift probability is (1-p)^3+3p(1-p)^2=0.998816.

Critical physical limitations: A single Z phase error is NOT correctable; the code has arbitrary-Pauli distance 1. A loss event erases the ONLY photon and cannot be recovered merely by these virtual-qutrit syndromes. Three qutrits here are tensor factors of one 27-path photon, NOT three physically independent photons; thus no fault-tolerant three-photon quantum gate was established.

## 10. Five-qubit size-eight maximal partial Pauli MUB — parallel complete 8-orbit negative search cross-audited

Our independently developed **bounded lazy-compatibility CP-SAT** solver starts with 2336 exact covering clauses for each of the two S3 classes 692/694, chooses four additional symmetric matrices, detects pairwise incompatibilities, and adds sound no-good cuts. Each class produced an incompatible fake cover, six learned cuts, and then UNKNOWN under an 18-second per-solve limit. This narrower experiment, on its own, remains UNDECIDED.

**Important new parallel commit detected before publication:** cc65eb5d2dd3f806fc0168c9dff0314ba29c4e65 (Pass 12654) reports a **COMPLETED exhaustive size-eight no-go search** in the original eight O(5) representatives 692,693,694,695,700,701,702,703, using **433,517,130 exact-cover DFS nodes** with all eight flags timeout=false and no witnesses. The raw certificate is data/w33_five_qubit_size8_dlx_full.json. It is a substantial computational improvement that was produced INDEPENDENTLY BY THE PARALLEL ASSISTANT, not by our bounded solver. Its author also preserved the original 245-second fixture and reports an independent reversed-traversal two-class re-run as an additional pending crosscheck.

Our new analysis/toe_20261113_pass12654_MUB_size8_complete_crossaudit.py checked all eight representatives, all completed/no-witness flags, the sum of every per-orbit node count, n=3 control outcomes (freshly rerun), and a fresh five-qubit size-nine witness found in nine DFS nodes. A quick audit of the solver's logic confirms the most-constrained pivot is branched over ALL possible killers and the top-r coverage prune is a safe union bound. **Caution:** this is a certificate/algorithm audit, NOT an independent replay of 433 million nodes, and does not produce an external proof-checkable UNSAT trace. Conditional on the completed search being correct, its result closes the minimum as N=9, matching the earlier size-seven exclusion and size-nine existence. It is no longer accurate to describe the REPOSITORY as having no negative size-eight computation.

## Reproduction, test suite, and source references

New analysis scripts:
- analysis/toe_20261113_E6_cubic_source_semantic_audit.py
- analysis/toe_20261113_E6_exft_generalized_closure_affine.py
- analysis/toe_20261113_E6_exft_quadratic_Jacobiator.py
- analysis/toe_20261113_E6_exact_parabolic_stabilizer.py
- analysis/toe_20261113_Albert_cyclic_clock_sections.py
- analysis/toe_20261113_USp8_full36_intertwiner_audit.py
- analysis/toe_20261113_USp8_highest_weight_intertwiner.py
- analysis/toe_20261113_USp8_8mode_Albert_clock.py
- analysis/toe_20261113_USp8_E6_Z2_interferometric_witness.py
- analysis/toe_20261113_E6_nonflat_compact_lattice_gauge.py
- analysis/toe_20261113_E6_photonic_magic_repetition.py
- analysis/toe_20261113_fivequbit_size8_CPSAT_lazy_compatibility.py
- analysis/toe_20261113_pass12654_MUB_size8_complete_crossaudit.py

13 matching JSON certificates under data/toe_20261113_*. The integration suite tests/test_toe_20261113_e6_gauge_full_us8.py replays 14 checks (excluding the 100-second bounded MUB optimization, whose saved fail-closed result is independently inspected). It also verifies the completed earlier W(E6) 51840 automorphism certificate.

External context:
- Hohm–Samtleben, *Exceptional field theory I*, https://arxiv.org/abs/1312.0614 .
- Kreutzer, *Canonical formulation of E6(6) exceptional field theory*, https://edoc.hu-berlin.de/server/api/core/bitstreams/c2e61a8e-6617-4d02-a91b-df26fe5ff80a/content .
- USp8 27-dimensional antisymmetric traceless and 78=36+42 decomposition, https://inspirehep.net/files/3b57a71547d3445d26ffe3e55e28d667 .
- USp8 central Z2 and wedge² parity, standard compact Lie-group representation theory; see https://www.staff.science.uu.nl/~wit00103/ecole.pdf .
- The cubic 27 lines and classical Schläfli/E6 Weyl configuration are prior art and not patented physical predictions.

## Top five independent research branches

1. **Exact closed-form matrix proof:** Reconstruct every 28x27 entry of T in an explicit algebraic number field, verify all 36 generators symbolically, and express the signed Albert cubic as the standard USp8 symplectic-traceless invariant tr(ΩZΩZΩZ) with certified normalization.

2. **Full exceptional field-theory gauge hierarchy:** Extend the polynomial generalized Lie tests to 2-form gauge transformations, tensor hierarchy closure, Bianchi identities and a generalized metric; reject any candidate that fails known diffeomorphism invariance.

3. **Dynamical section-holonomy selection:** Search non-flat compact E6 gauge backgrounds whose Wilson loops preserve a common maximal five- or six-coordinate section, then test stability and curvature against a specified gauge action, avoiding assumed physical dimensional preference.

4. **Lab-facing Z2 interferometry plus proper photonic QEC:** Design a coherent 8+27 mode interferometer that resolves the central relative pi phase and a separate optical code that can actually handle phase noise and photon loss, not just single virtual-qutrit X shifts.

5. **Independently certify the parallel complete size-eight no-go:** Replay the Pass12654 433-million-node result using a second implementation and reversed two-class traversal, and seek a compact externally checkable unsatisfiability certificate.

**Bottom line:** The signed E6 cubic, full compact USp8 intertwiner, section-dependent gauge closure and order-6/3 clock reduction form a tightly verified and reproducible mathematical bridge. The decisive open scientific leap is an independently justified dynamical action and experimentally discriminating predictions, not the existence of beautiful Lie-algebra patterns.
