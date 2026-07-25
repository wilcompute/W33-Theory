# The W(3,3) Ihara zero phases do not reproduce CKM quark mixing

**Status:** null result, prepared for submission in place of the withdrawn
"CKM Full Matrix" claim.
**Supersedes:** `BREAKTHROUGH_PASS882_CKM_FULL_MATRIX.md`
**Certificates:** `data/w33_pass981_arxiv_batch_intake_audit.json`

---

## Why this replaces the previous draft

The previous draft reported four CKM parameters "derived from W33 eigenvalues
with zero fitting" and quoted agreement as percentages: 10%, 11%, 34%,
"order-correct". Percentage is the wrong unit. The CKM angles are measured to
parts in 10⁴, so agreement must be stated in experimental standard deviations.
In those units the predictions are excluded:

| Parameter | W(3,3) value | PDG | Discrepancy |
|---|---|---|---|
| θ₁₂ | 14.48° | 13.04° ± 0.05° | **28.8 σ** |
| θ₁₃ | 0.893° | 0.201° ± 0.011° | **62.9 σ** |
| λ_W | 0.250 | 0.2250 ± 0.0007 | **35.7 σ** |
| θ₂₃ | 3.18° | 2.38° ± 0.06° | **13.3 σ** |
| J (Jarlskog) | 2.06×10⁻⁵ | 3.18×10⁻⁵ ± 0.15×10⁻⁵ | **7.5 σ** |
| δ_CP | 72.45° | 65.5° ± 3.3° | 2.1 σ |

Five of six are excluded outright. Only δ_CP is even marginal, and only because
its experimental error is large.

A second problem is internal. The draft derives θ₁₂ four times —

| Formula | Value |
|---|---|
| arctan(sin φ / (2√11 − 1)) | 9.61° |
| the same × √(4/3) "ℤ₃ colour correction" | 11.10° |
| sin²θ = g²/(g²+k) | 60.0° ("Too large") |
| sin θ = μ/(k+μ) = 1/4 | 14.48° ("Closest yet") |

— and reports the last. Choosing among candidate formulas by proximity to the
measured value *is* fitting, so "parameter-free" and "zero fitting" cannot both
stand. The draft also gives θ₁₃ = 2.88° in its body with the note *"This formula
needs revision"*, against 0.893° in its own summary table.

---

## What the correct statement is

The Ihara zeta of W(3,3) has its non-trivial zeros on the circle
|u| = 1/√(k−1) = 1/√11, at phases

    φ = arccos( λ / (2√(k−1)) ),

giving φ_gauge = 72.45° from λ = 2 and φ_chiral = 127.09° from λ = −4. These are
correct, exact, and already established in `w33_paper.tex` (Corollary
`cor:ramanujan`, the remark "Phase angles and the photonic predictions", and the
closed-form Ihara zeta subsection). They are properties of the *graph spectrum*.

**The null result.** No assignment of these two phases to CKM mixing angles
reproduces the measured matrix. This is worth stating because the near-coincidence
δ_CP ≈ φ_gauge (72.45° against 65.5° ± 3.3°) is genuinely suggestive at the
2σ level and will occur to anyone who computes both numbers. The result is that
the suggestion does not extend: once θ₁₂, θ₁₃, θ₂₃ and λ_W are required
simultaneously, every proposed map is excluded at ≥ 7σ, and the one surviving
2σ coincidence is what one expects from a single angle drawn against a
3.3°-wide error bar.

---

## Why a null result is worth publishing here

1. **It closes a search.** The W(3,3) spectrum is small and rigid: two
   non-trivial eigenvalues, hence two phases. Showing that no assignment works
   removes an entire class of "flavour from graph spectra" proposals for this
   substrate, rather than leaving it open for rediscovery.

2. **It is a falsification with error bars, not an absence of evidence.** The
   exclusions are 7–63σ against precision data. That is a stronger statement
   than most positive claims in this area.

3. **It protects the results that do hold.** The Ihara-Ramanujan structure, the
   closed-form zeta, and the photonic phase prediction are solid. Publishing an
   over-claimed CKM derivation alongside them would put all of it under the same
   cloud.

---

## Recommended disposition

- **Withdraw** the CKM paper from the August PRL slot.
- **Retain** the photonic experiment paper, reframed: it measures an
  *already-predicted* pair of interference phases, which is an experimental
  contribution, not a new prediction.
- **Retain** the Ihara-zeta-as-Weil-zeta paper only after removing "Theorem
  885-2", which is the standard graph-RH equivalence (Terras), and the appeal to
  Deligne, which is not needed since polar-space collinearity graphs have
  closed-form eigenvalues.
- **Do not submit** the E₈-bijection or Leech-embedding material: the index
  [W(E₈):Sp(4,3)] is 13440, not 480, and five orthogonal E₈ sublattices cannot
  fit in the rank-24 Leech lattice.

---

## Guard added

`scripts/check_sigma_gate.py` now flags any file that compares to experiment,
quotes agreement as a percentage, and never reports a discrepancy in σ. Run on
the withdrawn draft it reports the 28.8σ Cabibbo exclusion directly.
