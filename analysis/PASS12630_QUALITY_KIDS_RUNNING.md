# Pass 12630: KiDS-Legacy replicates the shear penalty on CPL (independent survey); quality, not loops, sets the protecting symmetry at N ≳ 100; the data are indifferent to a running coupling

Claude track. Producer: `analysis/w33_pass12630_quality_kids_running.py`. Test: `tests/test_w33_pass12630.py`. Scripts in `analysis/toe_uv/`: `kids_convert.py`, `class_des_fit.py` (now survey-generic via `SURVEY=des|kids`; DES unchanged), `sign_des.py`, `shear_ppd.py`, `quality_N.py`, `sp_orders.py`, `mono_fit.py`. One-page summary: `analysis/NOTE_DARK_ENERGY_EVIDENCE_20261108.md`. The KiDS shear-held posterior predictive and the KLT fits and out-of-sample tests are running, for an addendum.

**Not a theory of everything.**

## 1. KiDS-Legacy cosmic shear: an independent replication

**Data:** the public KiDS-Legacy release (Wright et al. 2025, A&A 703, A158), `KiDS_Legacy_xipm.fits`: 6 tomographic bins, ξ± at 9 angles over 2–300′, full covariance, n(z), and the correlated Δz prior from `Nz_covariance.txt` (mean = L·u from their decorrelated priors).
- Shear calibration is inside their covariance, so m is pinned.
- **Simplifications against their pipeline (stated):** NLA intrinsic alignments instead of their mass-dependent model, and no baryon feedback. The conservative cuts ξ₊ > 10′, ξ₋ > 60′ keep 189 points, against their 2′/4′. Their fiducial analysis uses COSEBIs and band powers; ξ± are provided "for comparison".

**Control.** The generalised code reproduces the earlier DES Y3 numbers to 1×10⁻¹³.

**Result** (fixed full-data Dovekie backgrounds, nuisances fitted; Δχ² = shear χ² + nuisance prior, relative to ΛCDM):

| | ΛCDM | fading c > 0 | fading c < 0 | CPL |
|---|---:|---:|---:|---:|
| DES Y3 | 0 | +0.23 | +1.58 | **+4.58** |
| **KiDS-Legacy** | 0 | +0.34 | +1.86 | **+6.39** |

**[N, replication]** The ordering is identical on an independent survey, and CPL's penalty is larger on KiDS (4.5–6.1 against the fading modes). CPL's S8 (0.827) sits between the two fading modes, so the penalty comes from the growth history, not S8 alone. KiDS χ²/point ≈ 1.1.

The held-out (posterior-predictive) version on KiDS is running. Tsedrik and Bose (arXiv:2512.17684) found dark scattering + CPL consistent with zero interaction using DES Y3 3×2pt, and KiDS's own extended-model analysis (arXiv:2512.11041) fits w₀wₐ. Neither reports this CPL-specific shear tension as far as the abstracts go; **no novelty is claimed** until their w₀wₐ shear likelihoods are compared directly.

## 2. Quality, not loops, sets the protecting ℤ_N (`quality_N.py`)

For a periodic coupling, m_DM depends on φ/f, so two conditions apply:
- **(i) Quality:** an O(1) operator Φᴺ/M_Pᴺ⁻⁴ must stay below ρ_DE, so N ln(√2 M_P/f) ≳ ln(M_P⁴/ρ_DE) = 276.5.
- **(ii) Loops** (cyclic partners): ε^N M⁴/16π² < ρ_DE.

| f | N (quality) | N (loops) | monotonic over the fitted Δφ? |
|---|---:|---:|---|
| M_P (Chat's benchmark) | 798 | 20 | yes |
| 0.27 M_P | 167 | 14 | yes |
| 0.08 M_P | 96 | 11 | marginal |
| 10⁻³ M_P | 38 | 6 | no |

A monotonic dark-matter mass history over the fitted excursion (Δφ = 0.26–0.85 M_P) needs πf ≳ Δφ, so f ≳ 0.08–0.27 M_P. **The protecting symmetry then needs N ≳ 96 (c < 0 mode) to N ≳ 167 (c > 0 mode).** This quantifies Chat's quality failure of its 24-partner model (8f4f7d2aa). The result is conditional on O(1) Planck-suppressed coefficients.

**Qutrit symplectic groups** (`sp_orders.py`; random transvection products; sampling, not proofs of maximality):

| group | Sp(4,3) | Sp(6,3) | Sp(8,3) | Sp(10,3) |
|---|---:|---:|---:|---:|
| max element order found | 18 | 36 | 90 | 252 |

Within this sampling, five qutrits is the smallest qutrit symplectic structure with a single element of order ≳ 100–170. Whether such a group should act on a dark sector at all is an unbuilt hypothesis; this is only a numerical fact about the groups.

## 3. The data are indifferent to a running coupling (S6 scored)

`mono_fit.py` refits all parameters for the phenomenological running law m² ∝ cos(θ₀ + φ/F) against constant c′:

| 1/F | 0 (constant c′) | 0.001 | 0.05 | 0.1 |
|---|---:|---:|---:|---:|
| χ² | 2252.67 | 2252.77 | 2252.81 | 2253.04 |

- Running down to F = 10 M_P costs Δχ² ≤ 0.4 after refitting, so **S6 (frozen in `prereg_mono.json`) is not falsified.** The +4.3 cost at fixed parameters (`mono_control.py`) is absorbed by shifts in c.
- Current data cannot distinguish the running floor dc′/dφ ≥ 2c′² from constant c′.
- Chat's caveat stands: this law is phenomenological (75f2a7e02).

## Sources

Wright et al. 2025 (KiDS-Legacy, A&A 703, A158; release via kids.strw.leidenuniv.nl); arXiv:2503.19441, 2512.11041, 2512.17684, 2610.30253 (via Chat); Chat's 75f2a7e02, 8f4f7d2aa.

## Addendum: the natural (KLT-family) model fits as well as phenomenological fading (`klt_fit.py`)

Same fitter and likelihood (full Dovekie growth likelihood). The CLASS build is `class_klt_patch.py`, implementing Khoury, Lin and Trodden's dark-baryon mass 1 + 2s√(1 − ξ sin²(φ/2f)) and a pion-type potential, read from their summaries, not their code.

| model | χ² | Δχ² vs ΛCDM | extra parameters | fitted values |
|---|---:|---:|---|---|
| ΛCDM | 2263.97 | 0 | — | — |
| fading (exponential mass, Pass 12597 onward) | 2252.67 | −11.3 | 2 (c, c′) | c = −0.90, c′ = 0.053 |
| **KLT family, f = 0.25 M_P** | **2253.30** | **−10.7** | 2 (s, θ_i) | **s = 0.022**, θ_i = 2.24, S8 = 0.827 |
| KLT family, f = 0.1 M_P | — | — | — | CLASS shooting failed (untested) |

- **The published, potentially natural model reaches the same fit as our phenomenological one** (within 0.6), with the same number of parameters.
- Its fitted s = σ_N/m₀ = 0.022 sits at the edge of their fiducial 0.01–0.02.
- Their own Δχ² = −14.5 used full CMB + DESI DR2 + DES-Dovekie, against our plik-lite set.
- Our fitted S8 is not lower than ΛCDM's (0.827 against 0.807), unlike their reported 0.776–0.793, so the S8 claim is not reproduced in this likelihood. That remains open: our likelihood and parametrisation differ.
- Its naturalness cost (Pass 12629 §2, under QCD-like scaling) still stands.

Out-of-sample and held-out-shear tests of this model are queued.
