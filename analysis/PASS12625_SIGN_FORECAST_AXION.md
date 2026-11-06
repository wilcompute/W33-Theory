# Pass 12625: BAO cannot see the sign of the fading coupling, S8 can; DR3 BAO will not pick a dark-energy model; a fading coupling cannot live on a PQ-axion dark matter

Claude track. Continues Pass 12622. Producer: `analysis/w33_pass12625_sign_forecast_axion.py`. Test: `tests/test_w33_pass12625.py`. Scripts in `analysis/toe_uv/`: `modes_laplace.py`, `dr3_prereg.py` (frozen, sha256 6d76b63b, committed 2375fad84), `dr3_forecast.py`, `sign_growth.py`, `axion_de_route.py`. The MCMC chains and the prior-truncated reruns are still running; they go to Pass 12626.

**Not a theory of everything.**

## 1. Which sign of c? Laplace weights of the two optima

| case | c < 0 (χ², c, c′) | c > 0 | P(c > 0) |
|---|---|---|---:|
| Dovekie, full data | 2243.75, −0.90, 0.053 | 2245.78, +0.67, 0.053 | **0.26** |
| DES-SN5YR, BAO held out | 2252.28, −0.73, 0.004 | 2253.18, +0.77, 0.033 | 0.11 (invalid) |

- **Dovekie:** the full data mildly prefer c < 0 (Δχ² = 2.0, Laplace odds about 3:1).
- **DES-SN5YR:** the Laplace approximation fails here, because the c < 0 mode sits at c′ ≈ 0.004, where c is unconstrained. Its σ(c′) = 0.22 is wider than the prior [0, 0.2], so the Gaussian overstates that mode's volume.

## 2. BAO is blind to the sign; S8 is not

Growth at the full-data fits (`sign_growth.py`):

| | S8, ΛCDM | S8, c < 0 | S8, c > 0 | S8, CPL | max \|Δfσ8\| between signs |
|---|---:|---:|---:|---:|---:|
| Dovekie | 0.807 | 0.833 | 0.822 | 0.827 | 0.002 |
| DES-SN5YR | 0.809 | 0.837 | 0.823 | 0.829 | 0.002 |

- The two signs differ by ΔS8 = 0.011–0.015. In BAO they differ by only Δχ² 0.13–0.27, even at DR3 depth (§3).
- **The sign is a weak-lensing question:** S8 to ±0.004 would separate the two signs at about 3σ.
- These are true S8 values. Pass 12550-era work found that the S8 a ΛCDM shear analysis would infer is about 0.012 lower for fading.

## 3. Frozen DR3 BAO predictions and what DR3 can decide

`dr3_prereg.json` holds D_M/r_d and D_H/r_d at the DR2 redshifts plus z = 2.8, 3.2, 3.5, for ΛCDM, CPL and fading of both signs, on both compilations. It is hashed and was committed before any DR3 release; DESI DR3 is still described as upcoming (arXiv:2603.09973).

**Forecast (`dr3_forecast.py`):** DR2 errors scaled by √(3/5), with DR2 correlations kept. The Asimov Δχ² values are upper bounds, since no model is refitted to another's mock data.

| Δχ² | Dovekie fits | DES-SN5YR fits |
|---|---:|---:|
| ΛCDM vs CPL | 4.5 | 5.3 |
| ΛCDM vs fading | 5.9 | 7.8 |
| CPL vs fading | 3.3 | 3.9 |
| fading c<0 vs c>0 | 0.22 | 0.27 |

With the actual DR2 errors (control), the numbers are smaller (2.0–4.7), as they should be. **Reading:** DR3 BAO alone will strengthen "evolving vs ΛCDM", but it cannot choose between fading and CPL or fix the sign of c. The √(3/5) scaling is my assumption.

## 4. Outside idea: a fading coupling cannot sit on PQ-axion dark matter

If the dark matter is the PQ axion of Models A or trinification, the coupling b = d ln m_DM/d(φ/M_P) ≈ 0.053 must act on m_a = √χ_QCD/f_a.

| route | consequence | Cassini (\|γ−1\| < 2.3×10⁻⁵) | atomic clocks (\|μ̇/μ\| < 5×10⁻¹⁷/yr) |
|---|---|---|---|
| Λ_QCD | nucleon coupling 2b/3 = 0.035 | ×110 | ×2–4×10⁴ |
| Higgs vev | electron and quark masses move | ×1000 | ×4–10×10⁴ |
| f_a | no tree-level matter coupling | — | — |

The f_a route leaks back through the Higgs portal λ_hσ|H|²|σ|²:
- d ln v/dφ = λ_hσ f_a² b/m_h², so clocks require **λ_hσ < 7×10⁻¹⁹, 7×10⁻²³, 1×10⁻²⁶** for f_a = 10⁹, 10¹¹, 7×10¹² GeV.
- That is against λ_hσ ~ 0.1 needed by the Higgs-stability threshold of Pass 12612, and a rough two-loop floor of 10⁻⁷–10⁻⁵ from PQ quarks that carry SM charges.

**Conclusion [N, conditional]:** a b ≈ 0.05 fading coupling and PQ-axion dark matter are incompatible. The coupled dark matter must be sequestered from the Higgs, such as the KK dark matter of Passes 12558–12592, or the axion must be only a subdominant component.

Caveats:
- 1 + w for φ̇ ranges over 0.05–0.3.
- The clock bound is an order-of-magnitude figure from memory.
- A φ-dependent bare Higgs mass could cancel the leak only by tuning in φ.
- The general mechanism (quintessence couplings constrained through the Higgs and by clocks and the equivalence principle) is old, so novelty is claimed only for the chain through the σ threshold, and only after a search I have not done.

## 5. Neutrino link (cross-boundary)

Chat's Z9 seesaw (2930cbe03) maps onto every non-singular light-neutrino matrix. So it allows any Σm_ν ≥ 0.0588 eV for normal ordering (≥ 0.099 eV inverted, using NuFIT-like splittings from memory); the rank-2 ansatz fixes 0.0588 eV. The fading fit gain grows with Σm_ν (Passes 12558–12592), so fading is what makes the generic seesaw's larger masses compatible with DESI. That is compatibility, not a prediction.

## 6. SPT-3G D1 external check

Recorded in the Pass 12623 addendum: the ΛCDM n_s shift from adding DESI is +0.0047 there and +0.0066 here, and SPT+Pantheon+ w₀wₐ = (−0.83, −0.66) matches my CPL fit (−0.81, −0.69). SPT prints no n_s under w₀wₐ, so it is not prior art for Pass 12623's number.

## Sources

arXiv:2506.20707, 2603.09973, 2507.03090; Bertotti et al. 2003 (Cassini).
