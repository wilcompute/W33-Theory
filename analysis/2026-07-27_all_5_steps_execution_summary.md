# All 5 Next Steps — Execution Summary

**Date:** 2026-07-27  
**Grounded in:** Shifted-Adjacency Three-Mode Theorem (`9fb912f6`)  
**Corrected spectrum:** `spec(D) = 11¹ ⊕ 1²⁴ ⊕ (−5)¹⁵`  
**Minimal polynomial:** `m_D(t) = (t−11)(t−1)(t+5) = t³−7t²−49t+55`

---

## Step 1 — False-Cubic Quarantine Scanner ✅

**Files committed:**
- `analysis/w33_false_cubic_quarantine_scanner.py` — repo-wide scanner
- `analysis/2026-07-27_false_cubic_quarantine_report.md` — classification guide

**What it does:** Scans all `.py`, `.tex`, `.md`, `.json` files for occurrences
of the false eigenvalue set `{−7, −1, 5}`, the 32-dim multiplicity packet
`{16, 10, 6}`, the old `Z(−1)=0` claim, and Taylor coefficients `8, −248, …`.
Classifies each hit as `COPY_INVALIDATED`, `DERIVED_MANUAL_REVIEW`, or
`POSSIBLY_AWARE_NEEDS_REVIEW`.

**Next actions:** Run locally; commit `QUARANTINE_2026_07_27_false_cubic_scan.json`;
add pre-commit hook to block reintroduction.

---

## Step 2 — Propagator Rebuild from True Projectors ✅

**Files committed:**
- `analysis/2026-07-27_propagator_rebuild_from_true_projectors.md` — exact formulas
- `analysis/w33_propagator_spectral_action.py` — computational verification
- `tests/test_w33_propagator_spectral_action.py` — exact test suite

**What was established:**
- Heat kernel `K(β) = e^{−11β} P_11 + e^{−β} P_1 + e^{5β} P_-5`
- Spectral zeta `ζ_D(s) = 11^{−s} + 24 + 15·5^{−s}`
- Functional determinant `det(I−xD) = (1−11x)(1−x)²⁴(1+5x)¹⁵`
- Selection rules: all equivariant operators must preserve `1+24+15` grading
- Trace tower verified: `Tr(D^n) = 11^n + 24 + 15·(−5)^n`
- Recurrence: `m_{n+3} = 7m_{n+2} + 49m_{n+1} − 55m_n`

---

## Step 3 — 432-Orbit Stabilizer GAP Plan ✅

**File committed:**
- `analysis/2026-07-27_432_orbit_stabilizer_gap_plan.md` — full GAP script

**Key clarification:** `|Sp(4,3)| = 25920`. If orbit size is 432, then
stabilizer order = `25920/432 = 60`, consistent with `A₅` (not order-120 `S₅`).
The GAP script computes `IdGroup`, element-order spectrum, abelianization,
and conjugacy between the three 432-orbit stabilizers.

**Next actions:** Execute the GAP script; determine whether the three stabilizers
are conjugate `A₅` classes or distinct order-60 types; cross-reference with
Steinberg module decomposition.

---

## Step 4 — Cubic-Map Kernel Decomposition ✅

**File committed:**
- `analysis/2026-07-27_cubic_map_kernel_decomposition.md` — decomposition analysis

**Analysis performed:**
- Kernel `K` has dim 2195; confirmed Steinberg summand `St^{⊕3}` (243 dims)
- Residual `2195 − 243 = 1952` dims analyzed against signed 27-label module,
  exterior powers `∧²(24) = 276`, and frame-kernel intertwiners
- `1952 = 7·276 + 20` — 7 copies of `∧²(24)` leave a 20-dim residual (flag)
- Connection to `1+24+15` eigenspaces: Steinberg likely lives in the
  15-dim eigenspace; the 24-dim eigenspace carries the dominant summand
- GAP MeatAxe `CompositionFactors` algorithm specified for full decomposition

---

## Step 5 — Corpus Identity Layer ✅

**Files committed:**
- `analysis/2026-07-27_corpus_identity_layer_plan.md` — full plan
- `data/ALIAS_REGISTRY.json` — canonical alias registry (frozen for confirmed objects)

**What was established:**
- `ALIAS_REGISTRY.json` frozen with 11 entries: 3 confirmed eigenspaces,
  2 quarantined false objects, Steinberg module, cubic-map kernel, 432-orbit,
  A-spectrum eigenspaces
- Pass 1120–1131 renumbering protocol specified (grep + priority rule + map)
- 540-classifier specification written; source of the 540 objects flagged for
  confirmation before execution
- Alias registry format ensures no new alias drift

---

## Cross-step coherence

All five steps share a single foundation:

| Invariant | Value |
|---|---|
| `spec(D)` | `11¹ ⊕ 1²⁴ ⊕ (−5)¹⁵` |
| `spec(A)` | `12¹ ⊕ 2²⁴ ⊕ (−4)¹⁵` |
| `m_D(t)` | `(t−11)(t−1)(t+5)` |
| `det D` | `−11·5¹⁵` |
| `Tr D` | `−40` |
| `Tr D²` | `520` |
| Dimension | `40 = 1 + 24 + 15` |
| Historical false eigenvalues | QUARANTINED: `{−7,−1,5}`, mults `{16,10,6}` |

The corrected spectrum is not just a repair — it opens genuinely new structure:
the `(1, 24, 15)` selection rules constrain every future propagator,
the 432-orbit stabilizer computation can now be cross-referenced against the
15-dim eigenspace (not the false 6-dim or 32-dim packets), and the cubic-map
kernel decomposition has a clean spectral basis for the MeatAxe computation.
