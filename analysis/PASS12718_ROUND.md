# Pass 12718: 24 anomaly-free Z₁₀ assignments make the whole hybrid consistent (quality to dimension 11, a BBN-safe decay for the pseudo-Goldstone quarks, no dimension-5 proton decay); vectorlike-squark mixing lowers the hybrid's y′ by up to 0.037; the optimal flash cell goes 8 → 4 → 3 → 2 levels as lifetime grows; a 2-layer ternary transformer works but the task saturates; a decision table for the programme

Claude track. **Not a theory of everything.**
- Scripts:
  - `explore_pass12718_round.py` (≈6 min, mostly transformer training);
  - `explore_pass12718_flash.py`;
  - `tinygrad_np.py`, a new minimal numpy autodiff engine.
- Certificates: `data/explore_pass12718_round.json` and `data/explore_pass12718_flash.json`.
- Tests: `tests/test_toe_pass12718.py`, 4 tests passing.
- Decision table: **`TOE_DECISION_TABLE.md`**.

## (3) A Z₁₀ charge table for the whole hybrid
**Fields:** matter 16_i, Higgs 10_H, Σ (45), S (54), H and H̄ (16, 16̄), and a driver Y.

**Required terms:**
- 16·16·10;
- Σ², S², Σ²S and S³ (the renormalisable B−L vacuum of Pass 12717);
- Y and Y(H̄H)⁵;
- a neutrino operator 16·16·H̄H̄(H̄H)^c.

**Searched over all Z₁₀ charges:**

| condition | assignments |
|---|---|
| harmful SO(10)_Σ-violating operators (all fields with VEVs) absent below dimension 11 | 640 |
| + a decay operator Σ·16·H̄·(…) for the pseudo-Goldstone Q + U, with mixing mass a(a/M_Pl)^{n−3} ∈ [1.7×10⁻¹⁰, 300] GeV (decays before BBN, mixing ≤ 0.18) | 120 |
| + Z₁₀–SO(10)² anomaly-free (Σq·T(R) ≡ 0 mod 5) | **24** |
| + forbidding 16⁴ (dimension-5 proton decay) | 24 |

**Example:** q₁₆ = 1, q₁₀ = 8, q₄₅ = 0, q₅₄ = 0, q_H = 1, q_H̄ = 7, q_Y = 0.
- Harmful operators start at dimension 11.
- The Q + U decay operator also appears at dimension 11, giving a mixing mass of 260 GeV (mixing ≈ 0.15).

**Why the decay operator matters (new):**
- Without it, the pseudo-Goldstone vectorlike quarks would be stable coloured relics, which cosmology excludes.
- The same discrete symmetry that protects their lightness must allow their decay at a high dimension. The two requirements are compatible.

## (2) The vectorlike-squark threshold at M_SS
**Setup:**
- The scalar partners of Q + U sit at M_SS (8.4×10⁹ GeV, from the pseudo-Goldstone relation at c = 1).
- A-term mixing gives λ(M_SS) = 3y′⁴/(8π²)(X − X²/12) instead of 0.

| X = A²/M_SS² | λ(M_SS) | hybrid y′ |
|---|---|---|
| 0 | 0 | 0.472 |
| 2 | 0.0026 | 0.450 |
| 6 (maximal) | 0.0041 | 0.435 |

**Effect on the predictions:**
- Squark mixing moves the hybrid's y′ down by up to 0.037, more than the uncertainty in c.
- The hybrid's band widens downward to 0.43–0.48, away from B′ (0.49–0.51). The discrimination of Passes 12715–12716 survives or improves.
- The slope of y′ against M_VL now has an X-dependent offset.

## (1) A 2-layer ternary transformer
- **Implementation:** a new 60-line reverse-mode autodiff (`tinygrad_np.py`), checked against finite differences, runs a pre-LN 2-layer transformer: single head, d = 32, d_ff = 64.
- **Task:** associative recall: four key–value pairs and a query, chance 1/8.

| weights (attention + MLP) | test accuracy, 2 seeds | zero weights |
|---|---|---|
| fp32 | 1.000, 1.000 | 0% |
| binary | 1.000, 1.000 | 0% |
| ternary | 1.000, 1.000 | 43% |
| 2-bit | 1.000, 1.000 | 0% |

- **The task saturates:** every format, binary included, solves it.
- **What this does show:** a quantised 2-layer transformer, including ternary with 43% zeros, trains to perfect accuracy with straight-through training.
- **What it doesn't show:** it cannot discriminate between formats, unlike the single-layer pointer task of Pass 12717, where binary failed. A harder task (longer context, more pairs, arithmetic) is needed.

## (4) Flash endurance (the add-on replaces the artefacted section (4))
- **Wear model (illustrative):** SNR(N) = 40/(1 + (N/1000)^0.6).
- **Sustainable density:** 0.95·I_q(SNR) bits per cell at a target lifetime of N cycles.

| lifetime (cycles) | SNR | bits/cell, q = 2 / 3 / 4 / 8 | best q | ternary vs binary |
|---|---|---|---|---|
| 10²–10³ | 32–20 | 0.95 / 1.51 / 1.90 / 2.4–2.8 | 8 | +58% |
| 3×10³ | 13.6 | 0.95 / 1.50 / 1.83 / 1.95 | 8 | +58% |
| 10⁴ | 8.0 | 0.95 / 1.40 / 1.45 / 1.35 | 4 | +47% |
| **3×10⁴** | **4.6** | 0.91 / **0.97** / 0.90 / 0.79 | **3** | +7% |
| 10⁵ | 2.4 | **0.57** / 0.45 / 0.39 / 0.32 | 2 | −21% |

- **The optimal number of levels falls monotonically with required endurance: 8 → 4 → 3 → 2.**
- **Ternary cells are optimal in a window** around a few ×10⁴ cycles. That makes them a natural high-endurance compromise between MLC and SLC.

## (5) Decision table
`TOE_DECISION_TABLE.md` collects the three completions (A, B′, hybrid) and the decisive experiments:
- FCC-ee m_t;
- HL-LHC and FCC-hh vectorlike-quark mass and y′;
- Belle II inclusive B → baryon + missing energy;
- Hyper-K;
- haloscopes.

It states which result kills which model, and includes a table of the ternary findings.

## Status
- **Hybrid:**
  - It now has a consistent symmetry structure: gauged SO(10) "Goldstones instead of fine tuning", a 45 + 54 vacuum, and an anomaly-free Z₁₀ that gives quality, decay and proton stability.
  - Its prediction is y′ ≈ 0.43–0.48 with a falling M_VL dependence, and no proton decay at Hyper-K.
- **Ternary:**
  - the best flash cell at about 3×10⁴ cycles;
  - matches full precision in single-layer attention;
  - multi-layer transformers need a harder test.
