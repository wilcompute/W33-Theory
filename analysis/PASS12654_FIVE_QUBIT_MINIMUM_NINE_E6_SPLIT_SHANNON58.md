# Pass 12654: no five-qubit maximal Pauli MUB set has 8 elements (exhaustive search), so the minimum is 9; Θ(W(3,3)) ≥ √58; independent confirmations of E6(6) and of the frame dictionary

Claude track. Follows Pass 12653. **Not a theory of everything.**

## 1. Five qubits: size 8 does not exist (`w33_five_qubit_size8_dlx.py`, `data/w33_five_qubit_size8_dlx_full.json`)

**Method.** Exact-cover search in the rank-code form (Pass 12653 §5):
- S₁ = I, and S₂ over all 8 O(5)-orbit representatives;
- branching on the most constrained uncovered T with sibling exclusion;
- the valid top-r coverage prune of Pass 12649.

**Controls**, all passed: n = 3 size 5 exists; n = 3 size 7 none; n = 5 size 7 none (4,194,657 nodes, agreeing with the Pass 12649 DFS); n = 5 size 9 found in 514 nodes.

**Result:** **every one of the 8 orbits completes with no size-8 maximal partial spread.**

| orbit rep | nodes | seconds |
|---|---|---|
| 692 | 54,189,927 | 16,073 |
| 693 | 54,173,796 | 16,401 |
| 694 | 54,241,976 | 15,970 |
| 695 | 54,102,646 | 15,695 |
| 700 | 54,174,654 | 15,973 |
| 701 | 54,206,027 | 16,137 |
| 702 | 54,190,137 | 15,907 |
| 703 | 54,237,967 | 16,128 |

Total: **433,517,130 nodes**, no timeouts.

With Pass 12649 (none ≤ 7) and the verified 9-set (Pass 12650): **the smallest maximal Pauli MUB set (maximal partial spread of W(9,2)) for five qubits has exactly 9 elements.** The sequence 3, 5, 5, 9 for n = 2…5 matches 2^⌈n/2⌉ + 1 (still a conjecture beyond n = 5).

**Status of the claim.** This is one implementation with passing controls. The search is internally consistent with the S₃ symmetry (S → S⁻¹, S → S + I) of Pass 12653: both S₃ classes, and all orbits within each class, give "none".

An **independent re-run** with a different traversal order is in progress: last-index tie-break and reversed killer order, on the two class representatives 692 and 694 (`DLX_REVERSE=1`). It will be added as an addendum.

The parallel track's runs of the same code (245 s, and 150 s per orbit in `toe_20261113_fivequbit_s3_two_class_dlx.py`) timed out as "undecided". That is consistent; they are not a contradiction. Their fixture `data/w33_five_qubit_size8_dlx.json` (the 245 s snapshot) is left untouched; the full run is saved separately.

Literature: Mathematics 9(12) 1388 (2021), cited by the other track, reports five-qubit sizes 9, 11, 13, 15, 17 without excluding 8. Kantor (Adv. Geom. 2017) Remark 4.7 predicts 9 at n = 5. As far as the searched literature goes, this is the first exclusion of 8.

## 2. Shannon capacity of W(3,3): Θ ≥ √58 (`w33_shannon_square.py`, hinted 1 h run; `w33_shannon_square_verify.py`)

- A hinted CP-SAT run (3,600 s, 2 workers, started from the 57-set) finds an **independent set of size 58 in G⊠G** (solver bound 100 = ϑ²).
- It was **independently verified** on a separately built W(3) (different symplectic form and enumeration, GQ axiom checked, VF2 isomorphism): 0 conflicts.
- So **√58 ≈ 7.616 ≤ Θ(W(3,3)) ≤ 10** (Pass 12653: √57). The exact value remains open.

## 3. Independent confirmations (cited, not claimed)

**E6(6)** (`w33_e6_cubic_real_form.py`). The repository's signed cubic has a 78-dimensional stabiliser that is **closed under transpose** (residual 5×10⁻¹⁵). Hence:
- k = g ∩ so(27) has dim 36 and p = g ∩ sym(27) has dim 42;
- the Killing form computed from the adjoint representation has signature (42+, 36−);
- so the real form is **split E6(6)**.

This independently confirms the other track's C4/usp(8) identification (`analysis/2026-11-13_compact_c4_fermat_sixers_e6_clocks_fivefronts.md`). The root-level and extracted_v13 cubic files define the **same signed polynomial** (identical hashes 13ea38ed…), which settles the source-matching question raised in the other track's continuation.

**Projection of the chiral clock onto the compact stabiliser** (`w33_e6_cubic_skew_stabilizer_projection.py`):
- with D transported on both sides through the fixed address table, the projection carries **26.6 % of ‖D‖**, and the residual carries 96.4 %;
- the projection is not a 3-step clock (its spectrum is generic);
- same scope as the source: one fixed identification.

**Trinification frames** (`w33_trinification_frames.py`). The 40 A₂³ subsystems of E6 under "disjoint root sets" form SRG(40,12,2,4), **isomorphic to the W(3,3) line graph and not the point graph** (control: the two graphs are non-isomorphic).
- So frames ↔ lines, and points ↔ partitions of the 72 roots into four frames.
- The side was predicted in advance: the frame stabiliser has an abelian 3³, and the point stabiliser has a Heisenberg 3^{1+2} (Pass 12059).
- **This is a reproduction of the Pass 12635 addendum** (57a4c02a3, same dictionary by VF2) and is not claimed as new.
- It places the other track's clock T(A,B,C) = (RA, B, CR⁻¹), which lives in one SL(3)³ frame, on a **line** of W(3,3).

## Open

- The reversed-order size-8 cross-check (in progress).
- The exact five-qubit min F = 1/32, and the exact 1/16 for type B.
- The exact Θ(W(3,3)), now in [√58, 10].
- The six-qubit minimum: the dense search would need about 1.4×10¹¹ root entries, so it needs a redesign.
