# Pass 12730: the hybrid's orbifold route now works on the published formula (mismatch cancels at ΛR ≈ 6.7, below 0.1 for ΛR = 3–14, overlapping protection at ΛR ≥ 9.8); B′ does not explain the low-N_eff hint (ΔN_eff ≈ −0.06 at most); A's large-field escape needs a model without parametric resonance; first-layer bits beat uniform ternary at a lower budget; a prior-art map, and a dark-matter candidate for the hybrid

Claude track. **Not a theory of everything.**
- Scripts: `explore_pass12730_round.py` and `explore_pass12730_alloc_qat.py` (≈25 min).
- Tests: `tests/test_toe_pass12730.py`, 4 tests passing.
- Page: [Quartic Zero Decision Map](https://claude.ai/artifact/P7DdJZNBnjeSPJgFZ4Wnoc), version 8.

## (1) The orbifold sign mapping for the hybrid
- **Inputs:**
  - The hybrid's two-loop mismatch is δ = α₃⁻¹(measured) − α₃⁻¹(predicted) = +0.26 (Pass 12702).
  - The localised orbifold threshold (Contino–Pilo–Rattazzi–Trincherini eq. 20, Hall–Nomura) raises the predicted α₃⁻¹ by (6/7) ln(ΛR)/2π.
  - So δ_new = 0.26 − (6/7) ln(ΛR)/2π.

| ΛR | 3 | 5 | **6.7** | 10 | 15 | 30 | 100 |
|---|---|---|---|---|---|---|---|
| threshold | +0.15 | +0.22 | +0.26 | +0.31 | +0.37 | +0.46 | +0.63 |
| hybrid mismatch | +0.11 | +0.04 | **0.00** | −0.05 | −0.11 | −0.20 | −0.37 |

- **Cancellation:** exact at ΛR = 6.7; |δ| < 0.1 for ΛR = 3.2–14.
- **Protection:** geometric protection of the accidental SO(10) needs M_*R ≥ 9.8 (Pass 12717).
- **Result:** **the hybrid's unification, orbifold doublet–triplet splitting and Goldstone protection are mutually consistent for ΛR ≈ 10–14,** taking Λ ≈ M_*. This replaces the withdrawn estimates of Passes 12724–12727.

## (2) Can A's large PQ field relax safely?
- **The generic outcome:** large-amplitude oscillations of the PQ field restore the symmetry non-thermally through parametric resonance (Kofman–Linde–Tkachev; Kearney–Orlofsky–Pierce 1601.03049). That returns A to the post-inflation regime, where the axion is only 19% of the dark matter.
- **The escape needs a dedicated model** where resonance is ineffective (Harigaya–Ibe–Kawasaki–Yanagida 1507.00119) or explicit PQ breaking is enhanced.
- **Status:** A's untuned route is model-dependent.

## (3) B′ and N_eff
- **Literature:** Barbieri et al. (2501.01369) tie T_RH > 5.96 MeV to N_eff > 2.98 (BBN + Planck + lensing + DESI). At the lower edge of its window, B′ lowers N_eff by only about 0.06.
- **Correction:** **B′ does not explain the ACT + helium hint (≈ 2.85).** This corrects Pass 12729's "2.9–3.0, partial account".

## (4) Allocation-aware ternary training (code, 2 layers, d = 64, 3000 steps)

| weights | bits/weight | bits/char |
|---|---|---|
| fp32 | 32 | 2.187 |
| uniform ternary | 1.6 | 2.941 |
| **layer 0 at 2-bit + layer 1 binary** | **1.5** | **2.846** |

**Moving bits to the first layer beats uniform ternary with 6% fewer bits** (−0.095 bits/char, 13% of the gap to fp32). The first-layer rule of Passes 12714 and 12726–12729 holds under quantisation-aware training at matched budget.

## (5) Prior-art map
- **A:** Redi–Strumia, "Axion–Higgs unification" (1208.6013): f_a ≈ 10¹¹ GeV from the quartic zero.
- **Hybrid:** the base is prior art:
  - Ibáñez–Valenzuela (1301.5167, 1403.6081): high-scale SUSY at 10¹⁰–10¹³ GeV with tan β ≈ 1.
  - Unwin (2609.28740, Sept 2026): SUSY at the quartic zero, with a heavy higgsino dark matter candidate near 10¹¹ GeV.
  - Hall–Harigaya Higgs parity (1803.08119).
  - Tavartkiladze (1803.11164): pseudo-Goldstone Higgs in SO(10).
- **The hybrid's distinctive parts were not found in the literature searched:** the TeV pseudo-Goldstone Q + U, the y′–M_VL correlation, and the orbifold window.
- **B′:** no paper combines the dark dimension with a vectorlike top partner and a species-scale quartic zero, or B-mesogenesis with the dark dimension. B′ appears new.
- **The universal y′ floor:** only upper bounds on vectorlike-quark Yukawas were found. The floor appears new.

## (exploration, web) Two more findings
- **A dark-matter candidate for the hybrid:** Unwin's heavy higgsino, produced by Boltzmann-suppressed freeze-in (T_RH ≈ m_χ/27), fits the hybrid's SUSY scale. It replaces the "generic" dark matter on the page.
- **E₆'s Z₃ centre cannot protect anything,** because it acts trivially on every gauge-invariant operator. Protection needs a symmetry outside the gauge group, such as the Z₁₀ of Pass 12718, or the outer Z₃ that cycles trinification's three SU(3) factors.
- **No Belle II B → baryon + missing-energy result yet.** Belle's 711 fb⁻¹ limits still stand.

## Status
- **A:** strained. Its untuned route needs a resonance-free PQ model, and its key coincidence is prior art (Redi–Strumia).
- **B′:** new and coherent. It does not explain N_eff. Its decisive test is Belle II.
- **Hybrid:** the most complete it has been. Q + U pseudo-Goldstones, orbifold splitting with protection at ΛR ≈ 10–14, and a heavy higgsino for dark matter.
- **Ternary:** spending bits on the first layer beats uniform ternary at a lower budget.
