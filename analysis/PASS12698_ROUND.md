# Pass 12698: evidence with explanatory credit is prior-driven (no robust preference); the MeV ALP needs non-thermal production; a long-lived triplet is excluded to ~1.9 TeV; the lattice Δ_R^V halves the Cabibbo gap but cannot close it

Claude track. Follows Pass 12697. **Not a theory of everything.** Script: `toe_pass12698_round.py`; certificate: `data/toe_pass12698_round.json`.

## (1) Bayesian evidence with explanatory credit

Pass 12697's BIC counted parameters only. Here each model's predictions are integrated over explicit priors (docstring). The likelihoods are m_t, n_s and Ω_DM h²; the N_eff likelihood is common to all models.
- **Completion A:** one parameter f_a predicts both m_t (via λ(f_a) = 0) and Ω_DM (post-inflation axion).
- **Completion B:** m_t fixes y′ (dy′/dm_t = −0.038 GeV⁻¹, from three full runs at R = 1 μm), while Ω_DM requires tuning T_i (Ω ∝ T_i³).

Bayes factors relative to SM + ΛCDM + generic dark matter:

| model | P-ACT-LB n_s | P-ACT n_s |
|---|---|---|
| λ(√(v M_Pl)) = 0 boundary | 13.5 | 13.5 |
| completion A | 2.6 | 4.8 |
| completion B | 0.10 | 0.10 |

**Prior sensitivity and look-elsewhere.** The gains of the boundary and of A come from predicting m_t instead of fitting it, so they scale with the SM's m_t prior width. The boundary was also selected after seeing m_t, from about 8 candidate scales (Pass 12684). The P-ACT-LB column becomes:

| SM m_t prior width | boundary | boundary / 8 trials | A | A / 8 trials | B |
|---|---|---|---|---|---|
| 15 GeV | 13.5 | 1.7 | 2.6 | 0.33 | 0.10 |
| 5 GeV | 4.5 | 0.56 | 0.87 | 0.11 | 0.03 |
| 2 GeV | 1.8 | 0.23 | 0.35 | 0.04 | 0.01 |

> **Result.** With honest priors and the trials factor, **no model is robustly preferred over the SM.** The boundary is 0.2–1.7; completion A is 0.04–0.33 (better without DESI); completion B is ≈ 0.01–0.1, penalised because Ω_DM ∝ T_i³ needs a tuned reheating temperature. The impressive raw numbers (13.5, 2.6) are artefacts of a wide m_t prior. This closes the "is the intermediate-scale coincidence evidence?" question: **no, not by itself.**

## (2) The MeV ALP for the keV window needs non-thermal production

Primakoff freeze-in at T ~ m with g fixed by the lifetime (Pass 12697) gives Γ/H ~ 10⁻⁶–10⁻⁵, so ζ ≈ 10⁻⁹ GeV. That is **400–2,000× below** the ζ ≈ 1.7×10⁻⁶ GeV needed (order-of-magnitude estimate). The ALP would have to come from inflaton or modulus decay. The SM-plus-ALP explanation of the CMB N_eff deficit is therefore not minimal. SN1987A bounds near g ~ 10⁻⁹ GeV⁻¹ are uncertain by factors of a few, so the region is not robustly closed but also not motivated.

## (3) Completion B's long-lived regime (mixing < 10⁻⁸)

The lightest T then hadronises into R-hadrons. Starting from a stop-like R-hadron limit of ≈ 1.34 TeV, a fermion/scalar cross-section ratio of ≈ 7 (assumed) and the 3× triplet rate, the computed σ(M) slope gives a shift of +560 GeV. **The long-lived regime is excluded to ≈ 1.9 TeV**, stronger than the prompt regime (1.74 TeV). Across all mixing regimes B's triplet must lie above ~1.7–1.9 TeV.

## (4) The lattice inner correction and the Cabibbo gap

- The lattice γW box gives Δ_R^V = 0.02439(18) ([Ma et al., PRL 2024](https://arxiv.org/pdf/2308.16755)) and V_ud(0⁺) = 0.97386(30).
- The gap to the neutron value 0.97456(44) shrinks to **1.3σ**.
- Closing it would need Δ_R^V lower by another 0.0015, which is **8× the lattice uncertainty**.

The lattice moves the superallowed value toward the neutron by about half the gap but cannot close it. The remaining 0.15% sits with δ_NS for medium-mass emitters, the Zα² terms (Cao et al. 2025), or the neutron g_A.

## Cross-track summary

See `CROSS_TRACK_SUMMARY_12684_12698.md`.
