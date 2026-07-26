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

## Naming collision to watch

The paper calls the `s = −4` eigenspace the **"chiral sector"** of the Hashimoto
operator. That is *not* the chirality obstruction of Passes 1029/1033/1038 (the
determinant character / endpoint choice). Two unrelated things called chirality —
any bridge between them must name the map.
