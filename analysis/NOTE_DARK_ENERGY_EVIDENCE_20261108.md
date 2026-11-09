# What the data say about evolving dark energy (one page, 2026-11-08)

> **PARTIAL RETRACTION — PASS12632, 2026-11-08.** Every post-Pass12629 scalar-field cosmic-shear, joint-held-out, and S8 power/geometry comparison below is WITHDRAWN due to the CLASS/Halofit scalar-field nonlinear-power bug. Expansion-only BAO/SN statements from earlier passes are distinct, though their significance also needs calibrated inference. Do not treat prior shear claims as established. See `analysis/PASS12632_HALOFIT_SCF_BUG.md`.

Claude track, Passes 12620–12630. All numbers come from committed JSON certificates in `analysis/toe_uv/` and `data/`. **Not a theory of everything.**

**1. Evolving dark energy beats ΛCDM out of sample, on two supernova compilations.**

The models are trained without one probe and then scored on predicting it (elpd, prior-truncated draws):

| elpd gain over ΛCDM | fading coupling (c < 0) | CPL (w₀wₐ) | thawing exponential |
|---|---:|---:|---:|
| Dovekie | +5.7 | +5.5 | +3.5 |
| DES-SN5YR | +7.2 | +9.5 | +6.0 |

The leader changes with the compilation, so the data prefer evolving dark energy, not a particular model. *Robust.*

**2. Cosmic shear separates the models; BAO cannot.**

Held-out DES Y3 shear prefers fading (and ΛCDM) over CPL by 1.6–2.2 elpd, with either SN training set. CPL's shear penalty survives a joint refit (Δχ² = 3.2). 

**Update (Pass 12631):** KiDS-Legacy held out replicates this. CPL is worst by 2.5–3.0 on KiDS, and fading matches ΛCDM. With BAO+SN, DES and KiDS all held out (Dovekie), the gain over ΛCDM is **fading +4.7, CPL +0.3**. CPL's advantage nearly vanishes once structure growth is predicted. KiDS's own w₀wₐ analysis (arXiv:2512.11041) sees the same S8 tension.

BAO at DESI DR3 depth cannot split fading from CPL (Δχ² < 4) or fix the sign of the coupling (Δχ² < 0.3, and below 3.4 even at 0.2% precision). *Moderate: a 1–2σ effect from one survey so far.*

**3. The sign of the coupling is undetermined, mildly c < 0.**

Profile and Laplace estimates agree: P(c > 0) = 0.25–0.30, falling to about 0.3 odds once shear is added. The sign fixes a lot: c < 0 means the dark-matter mass dips and then rises, with an apparent phantom crossing at z ≈ 0.8. That is the published dark-axion/dark-baryon phenomenology of Khoury, Lin and Trodden (arXiv:2503.16415, 2607.16191). c > 0 never goes phantom. *Robust that it is undetermined.*

**4. A DESI-driven upward shift of n_s depends on the dark-energy model.**

Adding BAO moves n_s by 1.7σ under ΛCDM and by 0.1σ under CPL or fading. SPT-3G D1's ΛCDM shift agrees. *Replication of arXiv:2512.05108's mechanism.*

**5. Any particle carrier of the coupling is unnatural unless a large discrete symmetry protects it.**

- An unprotected field-dependent mass must be lighter than about 0.02 eV, because otherwise the one-loop correction exceeds H₀². This is old (Garny 2006; Doran and Jaeckel 2002), reproduced here and in Chat's audit.
- Protected options cost a cyclic symmetry ℤ_N. Loop cancellation needs N ≳ 11–21.
- A monotonic mass history over the fitted field excursion needs f ≳ 0.1 M_P. Planck-suppressed operator quality then needs **N ≳ 100–170**.
- Among qutrit symplectic groups, single elements reach orders of 18 (two qutrits), 36 (three), 90 (four) and 252 (five), from sampling.

*Conditional on O(1) Planck-operator coefficients.*

**Frozen, falsifiable statements** (hashes in `analysis/toe_uv/*.sha256`):

| file | what it freezes |
|---|---|
| `dr3_prereg.json` | DESI DR3 BAO predictions |
| `growth_prereg.json` | S8 and fσ8 predictions |
| `prereg_statements.json` | S1 shear (fading beats CPL), S2 phantom iff c < 0, S3 line drift, S4 DR3 BAO no split |
| `prereg_corridor.json` | S5, the sterile-neutrino corridor (now conditional) |
| `prereg_mono.json` | S6, the running floor |

**Corrections made along the way:** see `analysis/SUMMARY_PASSES_12620_12628.md` and the addenda of Passes 12627–12629. The main ones are the point-estimate CV lead, the inflation-prior band, the Lyman-α edge, the sign grid and the single-cosine mapping.
