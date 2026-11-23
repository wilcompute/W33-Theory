# Pass 12733: explicit evidence factors reverse the ranking (A with a SUSY PQ sector ≈ B′ ≈ 0.05 > hybrid ≈ 0.006, since bino freeze-in is finely tuned); matter on the SM brane keeps the hybrid's window but needs a brane baryon symmetry; Belle 2026 caps minimal mesogenesis at m_ψ < 2.5 GeV; a y′ floor figure for the draft note

Claude track. **Not a theory of everything.**
- Script: `explore_pass12733_round.py`.
- Figure: `analysis/figures/y_floor.png`.
- Tests: `tests/test_toe_pass12733.py`, 3 tests passing.
- Page: [Quartic Zero Decision Map](https://claude.ai/artifact/P7DdJZNBnjeSPJgFZ4Wnoc), version 11.
- The draft note has been updated.

## (3) Explicit evidence factors (corrects Pass 12732's heuristic ranking)
**What each completion is charged** (Bayes factors against the SM, SM m_t prior width W):
- **m_t:**
  - hybrid: W·|dy′/dm_t| with y′ ~ U(0, 1), giving 0.05·W;
  - B′: W·0.036·0.34·0.25 (surviving λ range, reheating overlap);
  - A: W·0.25·1.47.
- **Dark-matter production:**
  - the hybrid's bino freeze-in has Ω ∝ e^{−x} with x ≈ 24, and log T_RH spans 6 decades, giving a density **0.008** relative to the SM's generic 1/0.3;
  - A's pre-inflation misalignment gives 0.082;
  - B′'s second component is taken as generic.
- **Trials:** A's coincidence is divided by 8 for trials.

| W | hybrid | A (SUSY PQ escape) | B′ |
|---|---|---|---|
| 15 GeV | 0.0057 | **0.057** | **0.055** |
| 5 GeV | 0.0019 | 0.019 | 0.018 |
| 2 GeV | 0.0008 | 0.0075 | 0.0073 |

- **Counting the hybrid's exponentially sensitive dark-matter production drops it below A and B′.** Pass 12732's "hybrid leads" came from treating its dark matter as generic.
- **All three remain 20–1000× below the SM.**

## (1) Matter on the SM brane
- **The window is unchanged.** The localised running depends only on the even zero modes (gauge plus Higgs doublets). Brane matter comes in complete SM families, so it is universal at one loop, and the two-loop window ΛR ≳ 10 (Pass 12731) is unchanged at this order.
- **The cost:** brane matter has no GUT Yukawa relations (no b–τ unification prediction).

## (2) Brane-localised proton decay (matter on the SM brane)
- **What is removed:** the X,Y and coloured-Higgs wavefunctions vanish on the SM brane, so there is no tree-level dimension-6 or triplet dimension-5 decay.
- **What remains:** the leading term is a brane operator c·QQQL/Λ², with Λ = ΛR·M_c ≈ 10¹⁷ GeV.

| ΛR | Λ (GeV) | τ, c = 1 | τ, c = 16π² (NDA, strong coupling) |
|---|---|---|---|
| 10 | 9×10¹⁶ | 1×10³⁸ yr | 5×10³³ yr |
| 20 | 1.2×10¹⁷ | 3×10³⁸ yr | 1.3×10³⁴ yr |
| 40 | 1.5×10¹⁷ | 9×10³⁸ yr | 3.5×10³⁴ yr |

- **Weakly coupled brane operators are harmless.** At strong-coupling size they sit at the Super-K limit.
- **Requirement:** **the SM brane needs a baryon-number (or R-) symmetry,** or the hybrid predicts decay at Hyper-K.

## (4) The y′ floor figure
- **What it shows:** `analysis/figures/y_floor.png` plots the needed y′ against the matching scale for 1, 2 and 3 vectorlike families, with the one-family 95% floor band and the y′ < 0.35 falsifier line.
- **What it makes visible:** with two or three families the curve crosses the one-family falsifier above 10¹⁰–10¹² GeV. That is why the falsifier is stated as (Σy⁴)^{1/4} < 0.35.

## (5) 2026 data check for B′
- **Belle (2601.07104, Jan 2026, 711 fb⁻¹):** B⁺ → p + X_inv excludes minimal B-mesogenesis for **m_ψ > 2.5 GeV** and 2.15–2.3 GeV.
  - With minimal mesogenesis, ψ supplies at most 50% of the dark matter, so B′'s coupled component must be at least 50%.
  - The f = 0.5, β = 0.1 fit of Pass 12725 still works (χ² 3.3, σ8 0.993).
  - The Dark_CP variant (A_CP·BR ~ 10⁻⁷) lies below these exclusive limits.
- **No new 2026 LHC vectorlike-quark mass limit** was found; the 1.49–1.52 TeV recast stands. CMS's single-T → tφ (JHEP July 2026) is model-specific.

## Status
- **Evidence:** A (SUSY PQ escape) ≈ B′ (≈ 0.05) > hybrid (≈ 0.006). None is preferred over the SM.
- **Hybrid:** matter on the SM brane plus a brane baryon symmetry plus bino freeze-in (tuned) plus ΛR ≳ 10.
- **B′:** Belle 2026 pushes minimal mesogenesis to m_ψ < 2.5 GeV, and the dark sector becomes at least 50% coupled component.
- **Universal falsifier:** (Σy⁴)^{1/4} < 0.35, now with a figure.
