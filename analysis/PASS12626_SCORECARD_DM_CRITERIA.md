# Pass 12626: CPL leads out of sample on DES-SN5YR once draws stay in the priors; a coupled dark matter must be Higgs-sequestered and light-vev, like a sterile neutrino; its decay line would drift with source redshift, and the sign of the drift is the sign of c

Claude track. Producer: `analysis/w33_pass12626_scorecard_dm_criteria.py`. Test: `tests/test_w33_pass12626.py`. Scripts: `analysis/toe_uv/scorecard.py` (regenerable), `line_drift.py`, and `class_ppd.py`, where prior truncation is now the default. The MCMC chain and the joint CPL+DES refit are running, for Pass 12627.

**Not a theory of everything.**

## 1. Prior-truncated posterior predictive (corrects Pass 12622)

Draws outside the flat priors (c ∈ [−3, 3], c′ ∈ [0, 0.2], w₀+wₐ < 0, τ ∈ [0.01, 0.2]) are now resampled, and the rejections and CLASS failures are recorded. Rows with failures were rerun:

| row | before | truncated | rejected / failed |
|---|---:|---:|---|
| Dovekie SN-held, exp | −816.68 (8 draws) | −816.64 | 36 / 9 |
| DES-SN5YR SN-held, exp | −821.15 (20) | −820.75 | 18 / 10 |
| Dovekie BAO-held, fading | −7.37 | −7.72 | 56 / 2 |
| DES-SN5YR BAO-held, fading | −13.13 | **−9.84** | 81 / 3 |

Out-of-sample gain over ΛCDM:

| | fading c<0 | CPL | exponential |
|---|---:|---:|---:|
| Dovekie | +5.7 | +5.5 | +3.5 |
| DES-SN5YR | +7.2 | **+9.5** | +6.0 |

- Pass 12622's fading figure on DES-SN5YR (+3.9) was dragged down by draws outside the priors; the corrected value is +7.2.
- **Correction to my last report:** I said the three evolving models sit "within 2.3 elpd". On DES-SN5YR the spread is 3.5, and CPL leads by 2.3 over fading. On Dovekie the spread is 2.2.
- Even inside the priors, 9 to 11 of 40 exponential draws still fail in CLASS, so that row stays rough.

## 2. Scorecard (`scorecard.py`, refresh after every run)

| model | full_chi2_gain | oos_gain_dovekie | oos_gain_desy5 | ns_bao_pull_sigma | des_shear_fixed_bg_rel_lcdm | joint_des_chi2_gain | dr3_bao_vs_lcdm_dovekie | mcmc_desy5_bao_elpd |
|---|---|---|---|---|---|---|---|---|
| LCDM | +0.00 | +0.00 | +0.00 | +1.73 | +0.00 | +0.00 |  |  |
| fading_cneg | +10.65 | +5.69 | +7.18 | +0.11 | +1.58 | +10.71 | +5.94 |  |
| fading_cpos | +8.42 |  |  |  | +0.23 |  | +4.48 |  |
| CPL | +11.88 | +5.48 | +9.46 | +0.11 | +4.58 |  | +4.47 |  |
| exp | +3.79 | +3.46 | +5.99 | +1.39 |  | +2.97 |  |  |

Columns:
- `full_chi2_gain`: Dovekie full-data fit without lensing or fσ8.
- `oos_gain_*`: out-of-sample elpd gain over ΛCDM.
- `ns_bao_pull_sigma`: from Pass 12623.
- `des_shear_fixed_bg_rel_lcdm`: Δχ² at fixed background (Pass 12625 addendum); positive is worse.
- `joint_des_chi2_gain`: joint refit including DES shear (CPL pending).
- `dr3_bao_vs_lcdm_dovekie`: Asimov upper bound.

**Reading:** CPL and fading c < 0 lead on every column except shear, where CPL pays 4.6 against 1.6 for fading. The joint CPL refit (Pass 12627) decides whether that survives.

## 3. What a coupled dark matter must satisfy

The fading coupling makes the dark-matter mass vary as m_DM ∝ e^(−c′φ), with c′ ≈ 0.05. For a field this light (mass ~H₀), the candidate must satisfy:
- **(i)** no tree-level coupling to baryons or electrons above the clock limit, about 2×10⁻⁶ in Planck units;
- **(ii)** a mass not set by Λ_QCD or the Higgs vev;
- **(iii)** a Higgs portal of the mass-giving scalar below α_max m_h²/(b v_S²).

Portal cap as a function of the dark scalar's vev (1+w = 0.05, the most forgiving case):

| v_S | 100 GeV | 1 TeV | 10 TeV | 10¹¹ GeV (axion) |
|---|---:|---:|---:|---:|
| λ_hS cap | 7×10⁻⁵ | 7×10⁻⁷ | 7×10⁻⁹ | 7×10⁻²³ |

Candidates:
- **PQ axion:** excluded (Pass 12625).
- **Radion/KK tower on an SM brane:** excluded unless D3-type (Passes 12593–12602, cited, not redone).
- **Sterile neutrino** with Majorana mass from a gauge-singlet vev ≲ 10 TeV: survives. Its radiative portal is negligible, because the Yukawas are tiny (y_ν ~ 10⁻¹¹ for keV M).
- **E6 10-plet** (W36 draft): carries SM gauge charges, so it fails (i) or (iii) at loop level unless its mass comes from a sequestered sector (not checked).

## 4. Seesaw consequence: active neutrinos drift by only percent

With M ∝ m_DM, the seesaw gives m_ν ∝ 1/M. Since recombination, m_ν grows by +1.5% (c < 0) to +4–5% (c > 0). That is far too little to explain DESI's preference for small or negative Σm_ν, so this mass-varying-neutrino link is a **negative result**. The general mass-varying-neutrino idea is old (Fardon–Nelson–Weiner 2004); it is cited, not claimed.

## 5. Outside idea: the decay line's rest energy drifts with source redshift

If the coupled dark matter decays to a line at E = M/2, the rest-frame line energy of a source at redshift z differs from a local one by M(z)/M(0) − 1 (`line_drift.py`, full-data fits):

| z | 0.1 | 0.3 | 0.5 | 1.0 |
|---|---:|---:|---:|---:|
| c < 0, Dovekie / DES-SN5YR | −0.22 / −0.27% | −0.54 / −0.66% | **−0.74 / −0.90%** | −0.96 / −1.18% |
| c > 0, Dovekie / DES-SN5YR | +0.21 / +0.26% | +0.52 / +0.65% | **+0.75 / +0.94%** | +1.10 / +1.38% |

- **The sign of the drift is the sign of c**: for c < 0 the field turns around late, and the mass grows today. BAO cannot see the sign at all (Pass 12625), so this would be an independent probe of it.
- An offset of about 0.8% between local and z ≈ 0.5 sources is several times the energy resolution of an X-ray microcalorimeter (XRISM; Athena X-IFU later), but only in principle.
- **Conditions:** a line must exist; the full coupling must act on the decaying particle; and cluster redshift errors of about 10⁻⁴ are negligible, while line-centroid systematics are not assessed.
- A narrow search found X-ray intensity-mapping proposals (arXiv:1911.09120) but nothing on a redshift-dependent rest energy. No novelty is claimed until a wider search is done.

## Sources

arXiv:1602.04816, 1911.09120, astro-ph/0603368; Pass 12625 for the clock and Cassini inputs.
