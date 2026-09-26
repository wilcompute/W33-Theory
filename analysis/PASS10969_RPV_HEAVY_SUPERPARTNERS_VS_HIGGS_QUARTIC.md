# Pass 10969 — harmless R-parity violation needs superpartners above ~10^15 GeV; the Higgs quartic caps them near 3×10^10 GeV

Producer: `analysis/w33_pass10969_rpv_heavy_superpartners_vs_higgs_quartic.py`
Certificate: `data/w33_pass10969_rpv_heavy_superpartners_vs_higgs_quartic.json`
Regression: `tests/test_w33_pass10969_rpv_heavy_superpartners_vs_higgs_quartic.py`

## The cross-track question

* **Claude track (Passes 10960–10967):** in the W(3,3) heterotic class, the Fayet–Iliopoulos
  term forces a ν^c-type condensate with ⟨n⟩/M_s ≈ 0.19–0.39 (cfdc1f2). That condensate
  regenerates u^c d^c d^c, q l d^c and l l e^c with strength about ⟨n⟩/M_s.
* **Physics track** (`analysis/w33_two_susy_scales.py`): supersymmetry is "structural", with no
  light superpartners.

Heavy squarks make R-parity violation harmless. So how heavy must they be, and is that compatible
with the measured Higgs?

## Results

| quantity | value |
| --- | --- |
| squark mass needed (λ′λ″ ≲ 10⁻²⁷ (m̃/100 GeV)², λ ~ ⟨n⟩/M_s) | 6×10¹⁴ – 1.2×10¹⁵ GeV |
| SM two-loop control: λ(M_Pl) ours vs Buttazzo et al. three-loop fit | −0.0150 vs −0.0143 |
| λ turns negative (PDG m_t = 172.57) | 3.2×10¹⁰ GeV |
| λ(10¹⁵ GeV), λ(10¹⁶ GeV) | −0.0102, −0.0109 |
| m_t needed for λ ≥ 0 up to 10¹³ / 10¹⁴ / 10¹⁵ / 10¹⁶ GeV | 171.41 / 171.16 / 171.00 / 170.89 GeV |
| distance below PDG (experimental 0.29 GeV only) | 4.0 / 4.9 / 5.4 / 5.8 σ |

MSSM matching at M_S gives λ(M_S) = (g² + g_Y²)/8 · cos²2β + Δλ_stop. The one-loop stop
threshold (3y_t⁴/8π²) X̃²(1 − X̃²/12) is non-negative for X̃² ≤ 12, and colour/charge-breaking-safe
mixing lies well inside that range. Hence λ(M_S) ≥ 0, so M_S cannot exceed the scale where the
Standard Model λ turns negative.

**Reading.** The class cannot be rescued by heavy "structural" supersymmetry with MSSM
matching. The two tracks' positions are jointly consistent only if one of these holds:

* m_t is about 1.5 GeV lighter than measured (≈2.5–3σ once a ±0.5 GeV pole-mass interpretation
  uncertainty is included; 5.4σ on the experimental error alone);
* the stop mixing lies beyond the colour-breaking-safe range;
* the high-scale theory is not the MSSM (for example no superpartners at all, SUSY broken at
  M_s). In that case the D-flatness requirement behind Passes 10960–10967 must itself be revisited.

## Audit (cross-track, read-only)

`analysis/w33_BREAKTHROUGH_475_modified_gravity_sphaleron_higgs_vacuum.py` asserts
λ_h(GUT) = 1/40 = +0.025. The measured running gives λ(10¹⁶ GeV) = −0.0109. The claim would
require m_t ≈ 166.9 GeV. This is failure mode 4 (an unbuilt half: a dimensionless number asserted
as a physical coupling).

## Scope

* Two-loop running with NNLO matching. The three-loop offset is 0.0007 in λ(M_Pl), about 0.1 GeV
  in m_t.
* The RPV bound is the tree-level p → e⁺π⁰ bound on first-generation products. The generation
  structure of the regenerated couplings is not computed; a texture suppression ε of those entries
  lowers the squark bound by √ε.
* Loop-level bounds on other index combinations are stronger and are not used.
