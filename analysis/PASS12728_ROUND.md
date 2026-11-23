# Pass 12728: A's low-scale rescue clashes with ACT's spectral index (generic models 4.7–6.5σ low); the threshold sign convention passes a known check; a full-precision first layer still removes half the ternary gap at 4 layers; B′'s coupled component cannot address the N_eff hint; a year-by-year test forecast

Claude track. **Not a theory of everything.**
- Scripts: `explore_pass12728_round.py` and `explore_pass12728_deep.py` (≈40 min).
- Tests: `tests/test_toe_pass12728.py`, 4 tests passing.
- Page: [Quartic Zero Decision Map](https://claude.ai/artifact/P7DdJZNBnjeSPJgFZ4Wnoc), version 6, now with a timeline section.

## (1) Low-scale inflation for A
- **Scale:** H_I < 1.4×10⁵ GeV (Pass 12727) means V^{1/4} = 7.7×10¹¹ GeV. The e-fold number is N* = 42–48 for T_RH between 10⁴ GeV and instant reheating.

| T_RH | N* | n_s: hilltop p = 3 | p = 4 | p = 6 | plateau (1 − 2/N) | plateau vs ACT 0.9743 ± 0.0034 |
|---|---|---|---|---|---|---|
| 10⁴ GeV | 41.9 | 0.905 | 0.928 | 0.940 | 0.952 | −6.5σ |
| 10⁷ GeV | 44.2 | 0.910 | 0.932 | 0.943 | 0.955 | −5.8σ |
| instant | 47.9 | 0.917 | 0.937 | 0.948 | 0.958 | −4.7σ |

- **Generic low-scale inflation conflicts with ACT's n_s at 4.7σ or more,** because fewer e-folds push n_s down.
- **Only a tuned quadratic hilltop** (n_s = 1 − 2|η|, |η| = 0.013) fits.
- **Consequence:** A's near-π misalignment rescue (Passes 12726–12727) now carries two tunings: θᵢ to about 1%, and the inflaton curvature. **A is strained.**

## (2) A sign check of the threshold convention
- **The check:** a light colour-triplet pair at M_G/10 shifts the predicted α₃⁻¹ by **+0.80**, which lowers α_s.
- **The reference:** Hisano–Murayama–Yanagida require exactly this; unification with α_s = 0.118 prefers M_T below M_G.
- **Verdict:** the convention behind the Passes 12724–12727 orbifold numbers is correct, so the SO(10) orbifold deficit stands within the estimate.
- **Unresolved:** the contrast with Hall–Nomura's reported orbifold improvement. Their setup differs in matter placement and brane terms.

## (3) A full-precision first layer at depth (code, 4 layers, d = 48, 3000 steps)

| | fp32 | all-ternary | gap | ternary + fp32 layer 0 | gap | gap removed |
|---|---|---|---|---|---|---|
| code, 4 layers | 2.234 | 2.898 | 0.664 | 2.552 | 0.317 | **52%** |
| code, 2 layers (Pass 12727) | 2.187 | 2.941 | 0.755 | 2.368 | 0.181 | 76% |

- **At 4 layers the full-precision first layer (a quarter of the quantised weights) still removes half the gap.**
- **The benefit per fp32 weight holds roughly steady:** 76% for half the weights at 2 layers, 52% for a quarter at 4. **The first layer stays the high-value place to spend precision.**

## (4) B′'s coupled dark component
- **Requirements:** cold, ≥ 14–20% of the dark matter, outside the mesogenesis sector, with β ≈ 0.3.
- **Candidates:** an axion-like field with a field-dependent decay constant, or a heavy dark-dimension mode with a brane coupling to quintessence.
- **N_eff:** cold matter cannot lower N_eff, so **the −2σ low-N_eff hint stays unexplained** by all three completions.

## (5) Timeline: fraction of each completion's parameter space probed

| year | A | B′ | hybrid | event |
|---|---|---|---|---|
| 2030 | 18% | 0% | 0% | ALPHA I (40–80 μeV) |
| 2032 | 18% | 44% | 0% | Belle II 10 ab⁻¹ |
| 2035 | 60% | 44% | 0% | haloscopes to ~400 μeV |
| 2042 | 60% | 78% | 11% | Belle II 50 ab⁻¹, HL-LHC complete |
| 2045 | 96% | 78% | 11% | broadband axion searches to ~1.5 meV |
| late 2050s | 96% | 78% | 11% | FCC-ee settles whether the quartic zero exists (all three) |
| 2070s | 96% | 100% | 100% | FCC-hh: y′ and M_VL |

**Assumptions:**
- A's m_a is log-uniform over 34–1550 μeV.
- B′ combines Belle II with HL-LHC (VLQ up to 2 TeV on M_VL log-uniform over 1.74–6 TeV).
- The hybrid is probed only by HL-LHC until FCC-hh.

**Reading:** A and B′ are mostly decided by about 2045. The hybrid waits for FCC-hh.

## Status
- **A:** strained, with two tunings (θᵢ and the inflaton curvature) to survive the new top mass and ACT.
- **B′:** the most testable soonest (78% by 2042).
- **Hybrid:** doublet–triplet splitting is open, and it is untested until FCC-hh.
- **Ternary:** fp first layer plus ternary elsewhere; the benefit persists with depth.
