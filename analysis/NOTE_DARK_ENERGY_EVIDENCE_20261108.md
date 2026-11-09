# What the data say about evolving dark energy (one page; revised 2026-11-08 after the CLASS halofit correction)

> **PASS12632 WITHDRAWAL.** The previous version claimed that cosmic shear separates the models (fading +4.7 against CPL +0.3 on the combined ledger). A CLASS Halofit bug treated scalar-field dark energy as Ω_m ≈ 3 and suppressed the scalar-field nonlinear power by a factor of 0.4–0.7 relative to the corrected calculation. The bug is reproduced on stock CLASS and reported as lesgourg/class_public#682. The other track's retraction and fail-closed gate are in 5b2766be1. The previous text is in git history (44f94393d).

Claude track, Passes 12620–12633. All numbers come from committed JSON in `analysis/toe_uv/` and `data/`. **Not a theory of everything.**

**1. Evolving dark energy beats ΛCDM out of sample on expansion data, with two supernova compilations.** The models are trained without one probe and scored on predicting it (elpd, prior-truncated draws):

| elpd gain over ΛCDM (BAO + SN held out) | fading coupling (c < 0) | CPL (w₀wₐ) | thawing exponential |
|---|---:|---:|---:|
| Dovekie | +5.7 | +5.5 | +3.5 |
| DES-SN5YR | +7.2 | +9.5 | +6.0 |

- These probes are linear and never touched halofit. The training fits move by less than 1 in χ² under the patch, only through CMB lensing, and against ΛCDM rather than for it (`hf_impact.json`).
- The leader changes with the compilation, so the data prefer *evolving* dark energy, not a particular model.
- *Caveat (other track):* the significance still needs calibrated inference beyond Fisher draws. The MCMC replacements run so far agree.

**2. Cosmic shear does not separate the models.** With correct nonlinear power (patched halofit, confirmed by a matched-fluid check and by a patched HMcode):

| | fixed-background χ²_shear vs ΛCDM: fading c < 0 / CPL | held-out elpd vs ΛCDM: fading c < 0 / c > 0 / CPL |
|---|---|---|
| DES Y3 | +1.94 / +1.29 | −0.69 / −0.38 / −0.68 |
| KiDS-Legacy | +2.49 / +2.21 | *rerun in progress* |

- All the evolving models sit slightly behind ΛCDM on shear, by less than 2.5 in χ² and less than 0.7 in elpd, and |CPL − fading| < 0.7.
- This agrees with KiDS-Legacy's own extended-model analysis: no significant w₀wₐ improvement from shear plus CMB lensing (Reischke et al., A&A 709, A82, 2026; arXiv:2512.11041).
- Frozen S1 (fading beats CPL on shear) is not supported by current data. Frozen S8 and S7's sign clause would fail if scored now. Their formal targets are future releases.

**3. The sign of the coupling is undetermined, mildly favouring c < 0** (P(c > 0) = 0.25–0.30 from the expansion data). The shear-based odds are withdrawn. c < 0 gives the dark-matter mass a dip and rise with an apparent phantom crossing at z ≈ 0.8. That is the phenomenology of Khoury, Lin and Trodden's dark axion with dark baryons (arXiv:2503.16415, 2607.16191).

**4. A DESI-driven upward shift of n_s depends on the dark-energy model.** Adding BAO moves n_s by 1.7σ under ΛCDM and by 0.1σ under CPL or fading. SPT-3G D1's ΛCDM shift agrees. *Replication of arXiv:2512.05108's mechanism.*

**5. Naturalness and sequestering favour an axion-type completion.**
- An unprotected field-dependent mass must be lighter than about 0.02 eV (one-loop correction vs H₀²; old, Garny 2006).
- A protected mass needs a ℤ_N with N ≳ 100–170 for Planck-operator quality.
- **The dark-energy field cannot be the level-3 flavour modulus.** Atomic clocks are violated by at least 10⁶, fixed points included (Pass 12633). The flavour modulus must be stabilised, and the dark-energy field must couple to the visible sector at less than 5×10⁻⁵ of its dark-matter coupling.
- A shift-symmetric axion talking only to a dark gauge sector (the KLT structure) provides this by symmetry. A modulus-like fading coupling needs it added by hand.

**Frozen statements** (hashes in `analysis/toe_uv/*.sha256`): DR3 BAO (`dr3_prereg.json`), growth (`growth_prereg.json`), S1–S4, S5 (conditional), S6, S7, S8. They stay unedited as the record. The status of S1, S7 and S8 is given in §2.

**The main lesson.** When two models go through different code paths (scalar field against fluid), run the *same* physics through both paths and require identical outputs for every observable used. One such check, run after the shear claims were made, found the error.
