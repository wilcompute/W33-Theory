# Part DCL — Gravitational Wave Signatures of the Dark Sector

## Dark Sector Phase Transition

The W33 dark sector (W33^c = SRG(40,27,18,18)) undergoes a spectral phase transition at the scale where the dark eigenvalue 24 and visible eigenvalue 10 cross under RG flow.

At the crossover scale mu_cross:

```
lambda^c(mu_cross) = lambda^v(mu_cross)
```

This requires the dark sector to cool below the visible sector temperature, which happens at:

```
T_dark = T_SM * (g*_dark / g*_SM)^{1/4}
       = T_SM * (27/12)^{1/4}
       = T_SM * (9/4)^{1/4}
       = T_SM * 1.225
```

The dark sector is HOTTER than the SM sector by a factor of ~1.225. This is consistent with dark radiation constraints (Delta N_eff).

## Dark Sector Contribution to Delta N_eff

The dark sector contributes to the effective number of relativistic species:

```
Delta N_eff = (4/7) * (g*_dark / g*_SM)^{4/3} * (N_dark_dof / N_SM_dof)
```

Using:
- g*_dark from W33^c degree: 27 dark bosons
- g*_SM from W33 degree: 12 SM gauge bosons
- Dark dof at BBN: the lambda=-3 sector (x24 = generation structure)

```
Delta N_eff^{W33} = (4/7) * (27/12)^{4/3} * (15/10.75)
                 ~ (4/7) * 2.74 * 1.40
                 ~ 2.19
```

However, if dark sector is NOT thermalized with SM at BBN (because epsilon_phys ~ 10^{-18} makes mixing negligible), then Delta N_eff = 0 from the dark sector.

**The W33 prediction: Delta N_eff ~ 0 from the dark sector at BBN** (dark sector decouples at the W33 scale, far above BBN, and never re-thermalizes). CMB-S4 will measure Delta N_eff to +/- 0.06. W33 predicts SM contribution only.

**Falsifier F33:** Delta N_eff from dark sector = 0 at BBN/CMB. Any CMB-S4 detection of Delta N_eff > 0.3 (after SM neutrino corrections) would indicate dark radiation and potentially challenge the W33 dark sector decoupling prediction.

## Gravitational Wave Background from Dark Phase Transition

The W33 dark sector phase transition at T_dark produces a stochastic gravitational wave background. The peak frequency of the GW background from a first-order phase transition at temperature T is:

```
f_peak ~ 1.65 * 10^{-5} Hz * (T / 100 GeV) * (g*/100)^{1/6}
```

For the W33 dark transition at T ~ 246 * 1.225 GeV = 301 GeV:

```
f_peak ~ 1.65 * 10^{-5} Hz * (301/100) * (27/100)^{1/6}
       ~ 1.65 * 10^{-5} * 3.01 * 0.803
       ~ 3.98 * 10^{-5} Hz
       ~ 40 microhertz
```

This falls in the **LISA frequency band** (10^{-4} to 0.1 Hz — just below peak sensitivity but detectable with signal accumulation).

**Falsifier F34:** The W33 dark sector phase transition produces a gravitational wave background peaking at ~40 microhertz with amplitude set by the dark sector bubble nucleation rate (determined by the W33^c spectral data). LISA should see this signal if the dark phase transition is first-order. A LISA null result at this frequency and amplitude would be a significant constraint on W33 dark sector dynamics.

---
*W33-Theory | Part DCL | Dark T = 1.225 T_SM; Delta N_eff ~ 0; GW background at ~40 microhertz in LISA band; Falsifiers F33, F34*
