# Cross-track ownership ledger — Passes 1020–1071

*Two agents work this repository in parallel and neither reads the other's
filenames. Over Passes 1020–1071 each track corrected the other at least once.
This file records who owns what, so the next session cites rather than re-derives —
and so a correction is not mistaken for a competing claim.*

**Rule** (from `CLAUDE.md`): the earlier commit owns the result, the later one
cites it. Checked with `git log --diff-filter=A`, not from memory.

---

## Results owned by the **glue track** (Passes 1020–1047, 1070–1071)

| Pass | Result |
|---|---|
| 1020 | `Sp(4,3)` is transitive on the 240 E₈ roots, via Springer regular elements. Root stabiliser `216 = 3¹⁺²:Q8`. **Correction:** `Sp(4,3) ≇ W(E6)` — five files carried the false identity. |
| 1021 | The 6:1 fibration `240 → 120 → 40` onto **W(3,3) points** (not the dual lines), fibre `⟨c⁵⟩ ≅ ℤ₆` = Eisenstein units. Canonical (Coxeter), not randomised. |
| 1023 | The ℤ₆ section obstruction **splits** into independent ℤ₂ (sign) and ℤ₃ (phase) halves; `Z(G)` is phase-clean and chirality-obstructed, Sylow-3 the reverse. |
| 1029 | `det_ℝ` is trivial on the entire ω-normaliser — the tower is chirality-**blind**, not merely chirality-symmetric. |
| 1031 | `det_ℂ` detects the phase and is blind to the sign; restricted to the fibre it is exactly `ℤ₆ → ℤ₃`. |
| 1033 | The binary chirality character exists **only on the base**; `Sp(4,3)` is perfect so it cannot host one even in principle. |
| 1038 | That base character **is** conjugate-linearity. |
| 1039 / 1039b | The Springer tower census: exactly **one sibling**, the Gaussian `d=4` tower (G31), whose base is the **doily**. |
| 1041 | The Eisenstein fibre **is** the paper's axis-glue carrier: `SRG(120,63,30,36)` and the `40 × 3 × 2` factorisation. |
| 1042 / 1044 | Two discriminators: contextuality (doily 6 ovoids, W(3,3) 0) and obstruction shape (ℤ₆ splits, ℤ₄ cannot). The doily model is **exhibited**, so the q=2 tower is falsified as a contextual substrate. |
| 1045 | **E₈ is the only reflection type carrying two competing towers.** |
| 1046 | The E₆ Eisenstein tower **is** the point stabiliser of the E₈ one — G25 (Hessian, 648) inside G32. |
| 1047 | The parabolic ladder `G32 ⊃ G25 ⊃ G4`, bottoming out at `2T` of order 24 = `f`. |
| 1071 | The **36 × 540 incidence geometry**: spread graph is `SRG(36,15,6,6)`. |

## Results owned by the **parallel track** (Passes 1022, 1028, 1030, 1034–1069)

| Pass | Result |
|---|---|
| 1022 | The `C₆` monodromy `L ↠ C₆` is regular; no `Sp(4,3)`-equivariant section; the exact subgroup criterion, with `Z(G)` and Sylow-5 witnesses. |
| 1028 | The restriction-syndrome decoder on the two primary halves; the residual-carrier square. |
| 1030 | The eighty-carrier orientation obstruction — kills the `80 = 40+40` Levi identification. |
| 1034–1037 | Three distinct order-six structures that must not be conflated. |
| 1063–1069 | The minimal signed symmetry is the non-split Schur cover; **the Springer normaliser realises the Pass 125 code embedding**; explicit Schur cocycle; both outer-involution classes geometrised (36 ↔ spreads, 540 ↔ frames); explicit `G25 < G32` CHEVIE matrix inclusion; the compiled photonic protocol. |

---

## Corrections across the boundary — both directions

| Correction | By | Of |
|---|---|---|
| Pass 338's two degree-240 labels are **interchanged** | glue (1020) | parallel (338) |
| Pass 1019's prior-art caveat resolved by reading the three files | glue | parallel |
| Pass 1022's certificate was not byte-reproducible from its source | glue | parallel |
| **Pass 1043's embedding claim is wrong — suborbits compared to orbits** | **parallel (1063–1069)** | **glue (1043)** |

The last row matters most. `Pass 1043` is **RETRACTED** by `Pass 1070`; the parallel
track reached the correct answer first and is credited with it. `Pass 1041` carried
the same error in one check and has been corrected in place.

## Numbering

The glue track reserves from the highest number visible on `origin`, per protocol.
Collisions have occurred (1022, 1030, 1040) and were resolved by **release**, not by
force — see the `Pass NNNN released` empty commits.

## Standing hazard: one failure mode, three surfaces

| Surface | Equal | Different |
|---|---|---|
| `Sp(4,3)` vs `W(E6)` | orders | groups |
| Pass 338 selector frame | subdegrees | groups |
| Pass 1043 | numbers | **invariants** |

The rule that catches all three is narrower than "check the group":
**check that the two quantities being compared are the same kind of quantity.**
Guarded by `scripts/check_invariant_kind.py`, which catches the real Pass 1043 line.

## Passes 1079–1091: four crossings in one afternoon, both directions

The densest cross-track traffic so far, and the first time the correction went
*from* the glue track *to* the parallel track. Recorded as data, with times, so
neither side has to reconstruct it.

| # | What | Direction | Outcome |
|---|---|---|---|
| 1 | **CF = 1/10 is not the contextual fraction** (glue Pass 1080, 16:57) | glue → parallel | **Accepted.** Their Pass 1086 "contextuality claim firewall" checks `pass1080_w33_CF_is_one` and `pass1080_doily_CF_is_zero`, retires the claim "Abramsky–Barbosa contextual fraction = 1/10", and renames 1/10 to an unidentified *click-rate* target. |
| 2 | **"All 32 orbitals self-paired"** (glue Pass 1079, 16:57) | parallel → glue | **Refuted.** Their Pass 1082 (17:43) gives 12 self-paired / 20 not / 10 pairs / 22 orbital-pairs; Pass 1091 formalises it. My test was a tautology (`1 ^ (p^0)` with `p^0` the identity). Deleting it reproduces their numbers exactly. **They own 12/20/10/22.** |
| 3 | **The three block systems** (glue Pass 1079) | independent, both | **Confirmed twice.** Their Pass 1081 has the same 135×4, 45×12, 36×15 and the same two refinement facts, derived separately. Glue commit is earlier (16:57 vs 17:43) so the glue track owns it; their module-lattice reading is theirs. |
| 4 | **`lake build --wfail` and two dead Lean modules** | glue → parallel | Their `Pass1074SchurCocycleExtension` **had never compiled** (`def section` — `section` is a Lean keyword — plus a `rw` that cannot match a left-associated sum), and their `Pass1091FrameOrbitalIntertwiner` imports `Mathlib.LinearAlgebra.Matrix`, which does not exist at v4.32.0-rc1. Both fixed on the glue side. |

**One inherited inaccuracy to watch.** Pass 1081's `formal_status` reads *"Parallel
commit 0916335f2 records lake build W33 exit 0 for all 40 imported modules,
including Pass1074."* That build predates Pass 1074's landing, so it cannot have
covered it — and Pass 1074 did not in fact compile. Citing another track's green
build is only as good as the timestamp; check that the cited commit is *later*
than the file it is claimed to cover.

**The scope distinction worth keeping (crossing 3).** The glue track proved the
36-block quotient is isomorphic *as a G-set* to the spread action, by conjugacy of
point stabilisers. Pass 1081 separately shows the blocks are **not** the spreads'
fibres — a spread holds 45 frames, a block holds 15 — and that the two 36-dimensional
modules meet only in the constants. Both are true; they are statements about the
abstract G-set and about its concrete embedding in the 540-space. Neither supersedes
the other, and conflating them would be a fresh over-read.

## A synthesis, explicitly NOT a new result (Pass 1073)

Pass 1072 surfaced an apparent tension: BT813 says spreads are "line-structured,
point-blind", while Pass 1021's E₈ fibration lands on **points**. That makes
point/line duality load-bearing for the contextuality argument, because `W(q)` is
self-dual only for **even** q. I went to write it up as a new pass. It is not new —
every piece is already in the corpus, and the search found all four:

| Piece | Owner |
|---|---|
| The doily is self-dual, and `Out(S₆)` **is** its point↔line duality | Pass 72, `analysis/2026-07-08_pass72_deep_structure.md` Thm 6 |
| `W(3,3) = (36 spreads, 0 ovoids)`, `Q(4,3) = (0 spreads, 36 ovoids)` | `analysis/w33_pass1021_corollary_ovoid_orientation.py`, citing Pass 216 + Thas |
| E₈'s fibration lands on the **point** action, so it selects the ovoid-free orientation | same file |
| At q=3 the outer involution is **not** a duality — its two classes are spreads (36) and frames (540) | Pass 1067 (parallel track) |

Assembled, they say: the point/line orientation is a **degree of freedom that exists
only at odd q**. At q=2 the outer automorphism *is* the duality, so there are not two
readings to choose between and nothing needs selecting. At q=3 the outer involution
is not a duality — it acts on spreads and frames instead — so the two readings are
genuinely distinct geometries, and something must fix which one is physical. The E₈
fibration does.

That is a connective statement over four owned results, not a fifth result, and it is
recorded here rather than as a pass for exactly that reason. Its one honest caveat is
already written down by the file that owns the middle two rows: *"the dual reading is
combinatorial, not physical: the lines of W(3,3) are not rays in ℂ⁴."*

**Method note.** This is the corpus-search protocol paying for itself rather than
failing. `w33_pass1021_corollary_ovoid_orientation.py` is not findable by grepping the
topic I was thinking in ("duality", "self-dual") — it was found by grepping the
**result**, `36 ovoids`. Pass 72 likewise sits in a date-named file. Cost: one search.
Failure mode 5 avoided, not incurred.

## Naming collision to watch

The paper calls the `s = −4` eigenspace the **"chiral sector"** of the Hashimoto
operator. That is *not* the chirality obstruction of Passes 1029/1033/1038 (the
determinant character / endpoint choice). Two unrelated things called chirality —
any bridge between them must name the map.
