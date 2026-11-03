# Passes 12542–12549: real supernovae, the true Higgs trajectory, and minimal chiral matter

Claude track. Continues `PASS12534_12541_TOE_UV_CONSTRAINTS.md` and **corrects two of its statements**. Producer: `analysis/w33_pass12542_to_12549_toe_uv2.py`. Test: `tests/test_w33_pass12542_to_12549.py`. Drivers in `analysis/toe_uv`: `sn_quint.py`, `higgs_trajectory.py`, `higgs_floor.py`, `robust_correlation.py`, `anomaly_enum.py`.

**This is not a theory of everything.** Gauge group, generations and Λ remain inputs.

## Corrections to the previous write-up

1. **"Single exponential quintessence never beats ΛCDM"** was true only for BAO + CMB. With supernovae it does, mildly (12542).
2. **"Asymptotic safety's Higgs mass is a near miss, 127.2–128.8 GeV"** used an algebraic estimate with y_t frozen at M_Pl. On the true trajectory, M_H at measured M_t runs from 126.2 up to 128.8 for f_λ > 0, and M_H = 125.20 can be reached at M_t within the measured error (12543).

## 12542: swampland dark energy against DESI + CMB + real supernovae

**Data.** DESI DR2 BAO as before. Pantheon+ (z > 0.01, 1590 SNe, full STAT+SYS covariance) and DES-Dovekie, the recalibration of DES-SN5YR (1820 SNe, inverse covariance as supplied). M is marginalised analytically. The large data files are not committed: `github.com/PantheonPlusSH0ES/DataRelease` and `github.com/des-science/DES-SN5YR`, `4_DISTANCES_COVMAT`. The CMB is still my compressed version (θ*, and an ω_m prior I chose), so significances are approximate.

**Controls [N].**

| | my w₀, wₐ | published | Δχ² vs ΛCDM |
|---|---|---|---|
| DESI + CMB + Pantheon+ | −0.856, −0.513 | −0.838 ± 0.055, −0.62 (+0.22, −0.19) | −8.2 |
| DESI + CMB + DES-Dovekie | −0.818, −0.653 | −0.803 ± 0.054, −0.72 ± 0.21 | −11.4 |

**Exponential quintessence, Δχ² relative to flat ΛCDM:**

| λ | Pantheon+ flat | Dovekie flat | Pantheon+ curved vs ΛCDM+k | Dovekie curved vs ΛCDM+k |
|---|---|---|---|---|
| 0.3 | −1.0 | −1.3 | −1.1 | −1.4 |
| **0.6** | **−2.2** | **−3.4** | −2.6 | −3.8 |
| **0.816 (√(2/3))** | **−0.4** | **−2.1** | −1.4 | −2.9 |
| 1.0 | +5.5 | +4.0 | +3.7 | +2.4 |
| 1.2 | +19.6 | +19.5 | +16.4 | +16.5 |
| **1.414 (√2)** | **+48.5** | **+52.1** | **+42.5** | **+46.3** |

Conclusions, for a single thawing exponential:

1. **λ = √2 (strong de Sitter) is excluded at about 7σ**, and curvature does not rescue it. Andriot et al. report that curvature weakens slope constraints; in my compressed setup it does so by far too little for √2.
2. **λ = √(2/3) (the TCC value) is viable**, no worse than ΛCDM on either sample. The best λ on my grid is near 0.6, matching the published 0.698 (+0.173, −0.202), at about 1.5 to 1.8σ over ΛCDM with one extra parameter.
3. **Quintessence captures only part of the w₀wₐ preference** (−3.4 against −11.4 on Dovekie). It cannot cross w = −1, so the phantom part of the fit is out of its reach.
4. **Curvature.** ΛCDM + Ω_k gains −5.6 to −5.7, with Ω_k = 0.0026. Published DESI + CMB has a value of the same size near 2σ. A compressed CMB is a weak test of curvature, so I would not lean on this.

Also, DES recalibration matters: the gain from w₀wₐ on Dovekie is much smaller here than the claims made for the original DES-SN5YR, which is consistent with the DES team's report of a weakened preference.

## 12543: the true Higgs trajectory

**[N]** `higgs_trajectory.py`: y_t, g₂, g₃, λ all flow above k = 10¹⁹ GeV, starting at the far-UV fixed point. Stable under the start (T = 400, 800, 2000: M_H = 127.87). Above M_Pl the running is one loop.

| f_λ | M_H at M_t = 172.57 | M_t needed for M_H = 125.20 |
|---|---|---|
| 0.0002, 0.0005, 0.001 | no real fixed point there | 173.18, 173.13, 172.98 |
| 0.002 | 126.2 | **172.44** |
| 0.005 | 127.4 | 171.89 |
| 0.0129 | 127.87 | 171.54 |
| 0.05 | 128.37 | 171.18 |
| 1.0 | 128.75 | 170.88 |

**What is robust.** M_H moves by only 2.5 GeV as f_λ changes by three orders of magnitude, unlike M_t, which moves tens of GeV with Λ*. So the correlation M_H(M_t) survives the regulator problem, even though M_t alone does not. Across all f_λ > 0, M_H = 125.20 corresponds to **M_t between 170.88 and 173.18**, which contains the measured value.

**What is not a prediction.** Picking f_λ ≈ 0.002 to match is one parameter for one number. And the value the Eichhorn–Held functions imply, once f_g and f_y are fitted, is f_λ = 0.0129 (at G* = 0.39, Λ* = −2.74), giving 127.87, 2.7 GeV high at measured M_t, or M_t = 171.54 at measured M_H.

**A near-hit that was an artefact.** The algebraic estimate gave M_H = 125.35 at f_λ = 0.015, which looked like a third number from two fits. The true trajectory gives 127.94. Checking the approximation is what killed it.

## 12544: does the regulator spread cancel?  Not for f_g

**[N]** `robust_correlation.py`. **Assumption, not a derivation:** f_g = (5/18π)[2/(1−2Λ) − 1/(1−2Λ)²] is the optimised form of (5/9π)[Φ¹₁(−2Λ) − Φ²₂(−2Λ)]. Under that mapping, G* f_g for SM matter ranges from 0.037 to 0.72 across five regulators, so the spread **grows** to about 280%. It is also far from the required 0.0098. So this partial test shows no cancellation. It says nothing about f_y, which I cannot derive for other regulators.

**Exponents.** θ ≈ (2.1, 3.9) for SM matter is close to the canonical (2, 4). That is why they are stable, and it also means they carry little information. I found no measured quantity that maps to them, so idea 1 in its original form produced nothing: what is robust is M_H(M_t) above.

## 12545: the smallest chiral theory is one Standard Model generation

**[E]** `anomaly_enum.py`: SU(N) × SU(2) × U(1), N = 3 to 7, shape (Q, two antifundamentals, up to 2 doublets, up to 2 singlets), integer charges |Y| ≤ 12, primitive. Conditions: all gauge and gravitational anomalies, Witten, no vector-like pair, no neutral field.

| N | solutions | smallest Weyl count | smallest |
|---|---|---|---|
| **3** | 14 | **15** | **Q 1, u −4, d 2, L −3, e 6: the SM generation** |
| 4 | 12 | 21 | no single Higgs gives all masses |
| 5 | 8 | 23 | Q 1, u −6, 4, L −5, e 10 |
| 6 | 8 | 29 | |
| 7 | 5 | 32 | |

**At N = 3 the smallest is unique on this grid, with Y up to overall scale, and has a Higgs doublet of charge ±3 giving all masses.** Scope: only this shape with one Q. N = 2 and N = 1 are not covered. Similar minimality statements are known (Geng–Marshak and later), so this is a check rather than a discovery.

It is the nearest thing here to "why this matter": minimal chiral anomaly-free matter with colour is one SM generation. **It does not explain three generations, or why N = 3 rather than a smaller or different structure in general**, and minimality is an assumption, not a principle anything derives.

## State of things

| route | status |
|---|---|
| Top mass from gravity | **Not predicted**: 91% regulator spread in Λ* |
| M_H(M_t) correlation | **Robust and consistent** with data for f_λ > 0; not a parameter-free prediction |
| Neutrino window | Alive, conditional on no-AdS₃ |
| Dark energy slope | √2 out at about 7σ; √(2/3) viable; λ ≈ 0.6 mildly preferred |
| Matter content | One generation is minimal; generation number unexplained |

## Sources

- D. Scolnic et al., Pantheon+. Popovic et al., DES-Dovekie reanalysis, arXiv:2511.07517, w₀ = −0.803 ± 0.054, wₐ = −0.72 ± 0.21. DESI: arXiv:2503.14738.
- arXiv:2510.21627, λ = 0.698 (+0.173, −0.202). arXiv:2609.10567, independent reanalysis.
- C. Q. Geng, R. E. Marshak (from memory, for hypercharge quantisation by anomalies).
