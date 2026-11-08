# Pass 12631: held-out shear on two independent surveys erases CPL's out-of-sample advantage, while the fading coupling keeps it; the natural (KLT) completion faces a dark-energy-or-quality choice

Claude track. Producer: `analysis/w33_pass12631_kids_heldout.py`. Test: `tests/test_w33_pass12631.py`. Scripts in `analysis/toe_uv/`: `shear_ppd.py` (`SURVEY=kids`, `MODELS`), `scorecard.py`, `class_klt_guess_patch.py`, `klt2_check.py`, `klt_ffit.py`. KLT out-of-sample and held-out shear tests are still running, for an addendum.

**Not a theory of everything.**

## 1. KiDS-Legacy held out

Train on everything except shear (Dovekie fits), draw 20 truncated Fisher samples per model, refit the KiDS nuisances per draw, and score the KiDS-Legacy ξ±. The likelihood is ours, not KiDS's pipeline; see Pass 12630 §1.

| elpd_shear relative to ΛCDM | fading c > 0 | fading c < 0 | CPL |
|---|---:|---:|---:|
| DES Y3, Dovekie training | −0.04 | −0.42 | −2.12 |
| DES Y3, DES-SN5YR training | +0.12 | −0.42 | −2.05 |
| **KiDS-Legacy, Dovekie training** | −0.06 | −0.55 | **−3.04** |

**[N, replication]** CPL predicts held-out shear worst in every case, by 2.5–3.0 against fading on KiDS. ΛCDM and fading c > 0 predict shear equally well (within 0.12). **Frozen S1 (fading beats CPL on shear) holds out of sample on two independent surveys.** Its formal scoring target, the next shear release, still lies ahead.

## 2. The combined out-of-sample ledger (Dovekie)

| elpd gain over ΛCDM | BAO+SN held out | + DES shear held out | **+ KiDS shear held out** |
|---|---:|---:|---:|
| fading c < 0 | +5.69 | +5.28 | **+4.72** |
| CPL | +5.48 | +3.36 | **+0.32** |

**Reading.**
- Once both shear surveys are predicted out of sample, **CPL's advantage over ΛCDM almost vanishes (+0.3), while the fading coupling keeps most of its gain (+4.7).**
- The evolving-dark-energy preference survives only in a form that does not over-grow structure.
- **Caveats:**
  - DES and KiDS overlap a little on the sky, so treating them as independent slightly overstates the combination.
  - Our shear likelihoods are simplified (NLA intrinsic alignments, no baryons, conservative cuts).
  - Only Dovekie has the full set; on DES-SN5YR, CPL's BAO+SN lead (+9.5 against +7.2) is larger.
- **Context:** KiDS's own w₀wₐ analysis (arXiv:2512.11041) finds lensing alone prefers ΛCDM (Bayes factor 0.07), and its all-probe w₀wₐ fit pushes S8 up by 2.3σ. That is the same tension, seen from their side. The new element here is that a dark-matter–dark-energy coupling largely avoids it while keeping the expansion-data gain.

## 3. The natural completion's dark-energy-or-quality choice

The KLT-family build (Pass 12630 addendum) uses no constant term (v = 0). With an improved shooting guess (`class_klt_guess_patch.py`; control reproduces the fit to 2253.299):

| f (M_P) | 0.05 | 0.10 | 0.12 | 0.15 | 0.20 | 0.25 (fit) | 0.50 |
|---|---|---|---|---|---|---|---|
| dark-energy solution | no | no | no | yes (χ² 13510, unfitted) | yes (2365, unfitted) | yes (2253.3) | yes (2272, unfitted) |

**Below f ≈ 0.12–0.15 M_P the field is too heavy to act as dark energy without a separate constant.** This gives a dichotomy for this family:
- **small f** needs a cosmological constant v, which brings back the cosmological-constant fine-tuning;
- **large f** (≳ 0.15 M_P) lets the axion itself be the dark energy, but Planck-suppressed operator quality then needs a protecting ℤ_N with **N ≳ 140** (Pass 12630 §2, O(1) coefficients).

KLT's own small-f model (f = 0.035 M_P) keeps v ≠ 0, consistent with this. A fit with f free is queued.

## 4. Not done, and why

A COSEBIs version of the KiDS likelihood (KiDS's fiducial statistic) needs the COSEBI filter functions T±(θ) from their code, not the data release. Deferred.

## Sources

KiDS-Legacy release (Wright et al. 2025, A&A 703, A158); arXiv:2512.11041 (KiDS-Legacy extended models); 2503.16415, 2607.16191 (Khoury, Lin and Trodden).

## Addendum: the mechanism is a tomographic tilt, not an amplitude excess (`shear_diag.py`)

At the fixed-background best fits (nuisances fitted), I compare the model and data ξ± per point and per tomographic pair.

| | S8 | Ω_m | σ8 | mean (model − data)/σ, ξ₊ | ξ₋ |
|---|---:|---:|---:|---:|---:|
| ΛCDM (KiDS / DES) | 0.807 | 0.300 | 0.806 | +0.09 / +0.07 | +0.41 / +0.25 |
| fading c < 0 | 0.833 | 0.306 | 0.825 | +0.14 / +0.11 | +0.50 / +0.34 |
| CPL | 0.827 | 0.312 | 0.812 | **+0.07 / +0.01** | +0.51 / +0.33 |

CPL / fading − 1 for ξ₊, by tomographic pair (low z → high z):
- KiDS: −3.9% (bins 1-1) … −1.7% (3-3) … +1.1% (6-6);
- DES: −4.4% (1-1) … −0.6% (3-3) … −0.3% (4-4).

**Reading.**
- On average, CPL over-predicts ξ₊ *less* than fading does, yet it is penalised more. The penalty comes from the **redshift tilt**: relative to fading, CPL moves about 4–5% of lensing power from the low-z bins toward the high-z bins.
- With strongly correlated covariances, a uniform amplitude offset is cheap, because the nuisances and correlated modes absorb it. A tilt across tomographic bins is expensive, and the Δz and intrinsic-alignment nuisances only partly absorb it.
- CPL's fit also needs a higher Ω_m (0.312, against 0.306 and 0.300), consistent with its phantom phase at z > 0.4 changing the growth history.
- The tilt has the same sign and size in both surveys, so it is structural, not survey-specific.

This is a diagnostic in our simplified likelihoods; whether the tilt survives full intrinsic-alignment and baryon modelling is open. It gives the next shear releases a specific target: **the low-z/high-z shear ratio**, not S8 alone.

## Correction (same day): where the penalty actually sits; frozen S7's mechanism clause is wrong

The first addendum read the CPL/fading *model ratio* (CPL lower at low z, −4%; equal or higher at high z) as "the penalty is a low-z deficit". Two checks show this was an over-read.

**(a) Diagonal residuals do not separate the models.** Summed (model − data)/σ over the three lowest and three highest pairs gives a tilt of +23.4 / +23.8 / +24.6 (KiDS) and −9.2 / −8.6 / −8.8 (DES) for ΛCDM / fading / CPL. All models share the same tilt relative to the data, so the penalty comes through the covariance.

**(b) χ² with proper sub-covariances** (low pairs: both bins in the lower half; high: both in the upper half; mixed: the rest):

| CPL − fading | low | high | mixed | all |
|---|---:|---:|---:|---:|
| KiDS-Legacy | +0.80 | +1.54 | +1.90 | +4.69 |
| DES Y3 | −1.12 | **+5.16** | −2.07 | +3.10 |

**Corrected statement.** CPL's shear penalty sits in the **high-z** (DES) and high-z plus mixed (KiDS) blocks. Relative to fading, CPL predicts more high-redshift lensing power than the data allow. Its lower low-z prediction is not what is penalised. (The blocks do not add to the total because of cross-covariance.)

**Frozen S7 (`prereg_tilt.json`, sha a05a56e8).** Its claim that the penalty is "driven by the low-z bins", and the matching falsification clause, are **already contradicted by DES Y3 and KiDS-Legacy**. The clause was mis-specified when frozen, from the model ratio. The frozen file stays unedited as a record. The sign part of S7 and S1 (CPL worse than fading on shear) still holds. Any future scoring should use the block result above: the discriminator is CPL's excess **high-z** shear.

## Addendum: the KLT-family model out of sample and on held-out shear (provisional)

| elpd relative to ΛCDM (Dovekie training) | SN held | BAO held | DES shear held | KiDS shear held | **total** |
|---|---:|---:|---:|---:|---:|
| fading c < 0 | +1.94 | +3.75 | −0.42 | −0.55 | **+4.72** |
| CPL | +0.89 | +4.59 | −2.12 | −3.04 | **+0.32** |
| **KLT family (f = 0.25 M_P)** | +2.00 | −0.40 | −0.67 | −0.83 | **+0.11** |

- **On shear, KLT behaves like fading** (−0.7/−0.8 against −0.4/−0.6), far from CPL.
- Its weak spot is BAO held out: −0.40 at the standard draw width, but **+2.75 at twice the width** (−8.72 against ΛCDM −11.47). Broadening a well-behaved Gaussian posterior should not help, so the Fisher draws misrepresent KLT's non-Gaussian, periodic posterior. **KLT's total is therefore provisional.**
- The BAO-held MCMC (`mcmc_holdout.py dovekie bao klt25`; smoke test reproduces the holdout row exactly) is queued to settle it.
- Only one of two declared starts succeeded in each KLT holdout; θ_i = 2.5 failed in CLASS shooting.

**f free (`klt_ffit.py`):** the optimiser did not move f from 0.250 (χ² unchanged at 2253.30, s = 0.0218, θ_i = 2.244). This says only that no improving direction was found from the start. f is strongly degenerate with θ_i (unrefitted χ² 2365 at f = 0.2 and 2272 at f = 0.5), so a joint scan or MCMC over (f, θ_i) is needed before f is called constrained.
