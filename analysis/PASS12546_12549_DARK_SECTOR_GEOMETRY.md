# Passes 12546–12549: the phantom signal, the fading dark sector, and what its geometry requires

Claude track. Continues `PASS12542_12549_SUPERNOVAE_HIGGS_ANOMALIES.md`. Producer: `analysis/w33_pass12546_to_12549_dark_sector.py`. Test: `tests/test_w33_pass12546_to_12549.py`. Drivers in `analysis/toe_uv`: `dark_like.py`, `dark_ceiling.py`, `dark_refine.py`, `dark_lowz.py`, `dark_mocks.py`, `fading_ds.py`, `dd_geometry.py`.

**This is not a theory of everything.** It constrains one leading string-motivated reading of the DESI signal. It explains neither the gauge group, nor generations, nor Λ.

## Data and scope

DESI DR2 BAO; the DESI compressed CMB (θ*, ω_b, ω_bc) with its covariance, replacing the prior I chose in Pass 12542; Pantheon+, DES-Dovekie, and the original DES-SN5YR, taken from the repository's 2024 commit `97d8d0c`. M is marginalised. **Background only:** no ISW, lensing or growth. SN files are not committed; JSON results are.

## 12546: the ceiling for uncoupled dark energy

Any uncoupled dark energy obeying the null energy condition has w ≥ −1: canonical fields in any number, with any potential. Fitted as piecewise constant w on 13 bins up to z = 5, with w = −1 above that.

| Δχ² vs ΛCDM | Pantheon+ | DES-Dovekie | DES-SN5YR |
|---|---|---|---|
| exponential, c′ = 0 (1 extra) | −2.5 | −3.8 | −8.8 |
| **best w ≥ −1 found** | −5.2 | **−7.9** | **−14.8** |
| fading dark sector, c < 0 (2 extra) | −8.4 | −10.2 | −16.5 |
| CPL (2 extra) | −7.3 | −10.4 | −17.5 |
| free w | −16.7 | −18.8 | −24.5 |

**Status of the ceiling [N].** It is the best found, so strictly a lower limit on the true maximum. On the DES samples, differential evolution with two seeds agrees within 0.05, and it barely improves on the best local start. Local starts alone scatter by several units, so the Pantheon+ value, which is local only, is the weakest. The free-w row uses 9 bins on Pantheon+.

**Where the gain sits.** On both DES samples the best history has w ≈ −0.5 only below z = 0.07, and w within 0.05 of −1 above z = 0.12. BAO starts at z = 0.295, so **only supernovae see this**. All that w ≥ −1 can extract on these samples is a drop in ρ_DE in the last billion years or so, a shape close to a magnitude offset between nearby and distant supernovae. This does not show that it is a systematic (see 12549).

**Phantom premium.** Free w beats the ceiling by about 10 to 11 on the DES samples, with seven or eight bins below −1, and the highest bin at the search's lower limit of −6, which is noise rather than a measurement. As a rough guide, χ²(8) = 10 is p ≈ 0.27; that is not the correct one-sided mixture distribution, so treat it as indicative only. These data do not by themselves require crossing w = −1 in a binned fit. CPL's advantage is that it gets most of the way with two parameters.

## 12547: the fading dark sector, reproduced, and how strong c′ really is

Bedroya, Obied, Vafa, Wu (arXiv:2507.03090): V = V₀e^(−cφ), m_DM = m₀e^(−c′φ).

**Control [N].** c < 0 branch and c > 0 branch:

| | mine (c, c′) | published (c, c′) |
|---|---|---|
| Pantheon+, c < 0 | −0.852, 0.049 | −0.85, 0.05 |
| Pantheon+, c > 0 | 0.687, 0.053 | 0.65, 0.05 |
| DES-SN5YR, c < 0 | −1.043, 0.052 | −1.06, 0.05 |
| DES-SN5YR, c > 0 | 0.857, 0.056 | 0.83, 0.06 |

Their significances are higher than mine (2.9σ against my Δχ² = −8.4, about 2.4σ on 2 parameters, for Pantheon+), as expected with a compressed CMB. I also get DES-Dovekie, c = −0.89, c′ = 0.050, Δχ² = −10.2.

**c′ = 0.05 ± 0.01 is not a 5σ detection [N].** The paper describes "a strong preference for a non-zero c′". Profiling c:

| c′ (c < 0) | 0 | 0.0123 | 0.02 | 0.03 | 0.05 | 0.07 | 0.1 |
|---|---|---|---|---|---|---|---|
| DESI + CMB | 0.0 | −0.6 | −1.5 | −3.1 | −5.3 | −0.9 | +40 |
| + Pantheon+ | −2.5 | −3.4 | −4.4 | −6.1 | −8.3 | −2.2 | +52 |
| + DES-Dovekie | −3.8 | −4.7 | −5.9 | −7.7 | −10.2 | −4.5 | +49 |
| + DES-SN5YR | −8.8 | −9.9 | −11.2 | −13.2 | −16.4 | −11.7 | +39 |

Turning on c′ gains Δχ² of **5.3, 5.8, 6.4, 7.7**: about 2.3 to 2.8σ, not the 25 implied by the quoted width. The likelihood is strongly asymmetric: gentle to zero, a cliff above. The reason [I]: the field is sourced by c′ρ_DM, so the mass change goes roughly as c′², and that is what the distances see. The width of a posterior near such a cliff says little about distance from zero. The mass falls only 1.2% since recombination for c < 0, and 4 to 5% for c > 0.

Fits at c′ ≥ 0.1 are local, so read those columns as "strongly excluded in this background fit", not as exact values. This agrees with the bound c′ < 0.066 from Planck that Stewart (arXiv:2609.25230) cites.

## 12548: what the moduli metric requires

**[E]** `dd_geometry.py`. D = 5 + n, internal radii e^(σᵢ), with M_Pl² = M_D^(n+3) Vol. Einstein frame metric: ds² = Σdσᵢ² + ½(Σdσᵢ)². In Planck units m_KK = 1/(L Vol^(1/2)), and M_D = Vol^(−1/2).

Control: the pure 5D radion gives c′ = √(3/2), β = 1/√6, α = 1/3, γ = 1/2, which is the known Brans–Dicke ω = 0.

1. **The radius gradient is fixed.** |∇ln m_KK|² = 3/2 for every n, and with M_D held fixed it is n/(n+1), reproducing the paper's benchmark 1/√2 at n = 1. So c′ = 0.05 means **only c′²/(3/2) ≈ 0.17% of the field's kinetic energy is along the gradient of the dark-dimension scale**. Whatever is rolling is almost entirely not the radius. This assumes other fields do not change m_KK at this order.

2. **Brane matter.** If brane scales are fixed in units of M_D, then the coupling is β = −∂ ln(M_D/M_Pl), and

   **β / c′ = ξ / (2 + ξ), ξ = d ln Vol / d ln L.**

   Pure radius, ξ = 1: β = c′/3. At c′ = 0.05 that is β = 0.017, γ − 1 = −1.1 × 10⁻³.

3. **Bounds.** Cassini, γ − 1 = (2.1 ± 2.3) × 10⁻⁵: β < 0.0041 (conservative two-sided), or 0.0025 (one-sided, since a scalar gives γ < 1). LLR, Ġ/G = (7.1 ± 7.6) × 10⁻¹⁴/yr, with Ġ/G = 2βφ̇ in atomic units and the fitted φ′₀ ≈ −0.45 to −0.54: β < 0.0030 to 0.0036. Two independent observations agree in size.

4. **Consequences at c′ = 0.05.**
   - **ξ < 0.18** (0.11 one-sided). The other dimensions must cancel at least 82% of the volume change. So of the paper's two branches, the varying-volume one is restricted to a narrow range around fixed volume.
   - Pure radius is excluded by a factor of about 4 in β (16 in force). At its cap c′ = 0.0123 the coupling gains less than 1.1 over c′ = 0: the signal is gone.
   - With n = 1 and only L and Vol moving, there is no room: a unit vector gives 2c′² − 8c′β + 12β² = 1, so c′ = 0.05 forces β ≈ 0.31 or −0.27. **n = 1 needs fields beyond L and Vol.**

5. **What this does not exclude.** The paper's fixed-volume branch, ξ = 0, with other light fields carrying the motion. Its statement that visible matter "does not couple directly to φ" therefore holds in that branch, but not in general: it needs volume locked as above, and brane scales must really track M_D. I assume they do, with no cancellation from other moduli. A brane scale tracking M_Pl, or a tuned cancellation, escapes. Katayama et al. (arXiv:2603.19819, footnote 4) note qualitatively that a universal coupling is tightly constrained and fixed volume removes it. **I did not find the ξ bound or the n = 1 statement in the papers I read, but my search covered only those and a few web queries, so this is not a novelty claim.**

**The Casimir relation.** The dark dimension is motivated by Λ ~ m_KK⁴. With a constant coefficient, c = 4c′, a one-parameter model. Stewart notes c₁ → 4c₂ asymptotically; I did not find a fit along that line.

| | best c′ on c = 4c′ | Δχ² | cost vs free c > 0 | fitted c/c′ |
|---|---|---|---|---|
| Pantheon+ | 0.045 | −3.6 | 4.4 | 13 |
| DES-Dovekie | 0.045 | −3.5 | 6.0 | 13 |
| DES-SN5YR | 0.044 | −3.2 | 12.1 | 15 |

So exact Casimir scaling costs about 2.1σ, 2.5σ and 3.5σ on one parameter. On DES-SN5YR it does worse than uncoupled exponential with the same parameter count. **The potential must fall about 13 to 15 times as fast as ln m_KK along the path, not 4 times**, so most of the dark energy slope cannot come from a dark-dimension Casimir term with a constant coefficient. This fits item 1: both say the rolling field is mostly something else. A coefficient depending on other moduli escapes it. The negative branch, which the data slightly prefer, has the opposite sign from Casimir scaling.

## 12549: a suspicion withdrawn

Removing z < 0.1 supernovae looked decisive:

| Δχ² | Pantheon+ all / z > 0.1 | Dovekie all / z > 0.1 | SN5YR all / z > 0.1 |
|---|---|---|---|
| CPL | −7.3 / −5.9 | −10.4 / −2.6 | −17.5 / −3.6 |
| exponential, c′ = 0 | −2.5 / −0.8 | −3.8 / 0.0 | −8.8 / −0.1 |
| best w ≥ −1 | −5.2 / −2.7 | −7.9 / −0.3 | −14.8 / −0.5 |

(The z > 0.1 ceilings are local fits.) That invites the reading "the signal is a low-z artefact". **The control refutes that reading [N].** `dark_mocks.py` draws SN, BAO and CMB from their covariances with CPL as truth, and repeats both fits on each mock:

| truth CPL | mocks | mean gain all / cut | P(drop as large) | P(cut as weak) | P(cut as weak, given full as strong) |
|---|---|---|---|---|---|
| DES-SN5YR | 300 | −18.7 / −6.9 | 0.35 | 0.26 | 0.11 |
| DES-Dovekie | 300 | −12.0 / −6.0 | 0.34 | 0.26 | 0.12 |
| Pantheon+ | 150 | −9.3 / −5.1 | 0.71 | 0.67 | 0.52 |

Validity control: ΛCDM mocks on Dovekie give mean gain −1.98 and −2.02, as they should, and none in 150 reaches the real −10.4.

**So a large drop is what removing those supernovae does anyway**, because they supply the lever arm. It is not evidence against the signal. At most, the conditional 0.11 to 0.12 is mild. The cut cannot distinguish low-z systematics from real evolution on its own. CPL mocks test only that CPL is consistent, not that it is correct. Claims that the evidence is biased by low-z supernovae rest on other arguments too (Efstathiou's calibration offset, say), which this does not test.

## State of things

| question | status |
|---|---|
| Is uncoupled NEC dark energy dead? | **No.** It reaches −7.9 and −14.8 on DES, against CPL −10.4 and −17.5, but only through z < 0.07 |
| Is c′ ≠ 0 strongly detected? | **No**: about 2.3 to 2.8σ in this background fit |
| Is the rolling field the dark-dimension radius? | **Not at c′ = 0.05**: 0.17% of the kinetic energy, and c/c′ is 13 to 15, not 4 |
| Does varying volume survive? | Only with ξ < 0.18, if brane scales track M_D |
| Is the low-z drop evidence of a systematic? | **No**, by mocks |

## Sources

- A. Bedroya, G. Obied, C. Vafa, D. Wu, arXiv:2507.03090. A. Stewart, arXiv:2609.25230. T. Katayama et al., arXiv:2603.19819.
- DESI DR2, arXiv:2503.14738; CMB covariance as printed in Carloni, Luongo, Biesiada, arXiv:2608.01215. Popovic et al., arXiv:2511.07517. Chaudhary et al., EPJC 2026, DOI 10.1140/epjc/s10052-026-15806-w, for low-z bias claims and Efstathiou's offsets.
- From memory, not re-fetched: Cassini (Bertotti, Iess, Tortora 2003), LLR (Hofmann, Müller 2018).
