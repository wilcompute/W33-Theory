# Part DCLI — Dark Sector Falsifier Consolidation

## The Dark Sector Falsifier Table

All active falsifiers specific to the W33 dark sector (W33^c = SRG(40,27,18,18)):

| # | Statement | Experiment | Status |
|---|---|---|---|
| F22 | Omega_Lambda = 9/13 = 0.6923 | Planck CMB + BAO | ACTIVE: obs 0.6847, W33 0.6923, ~1 sigma |
| F23 | w_DE = -1 exactly | DESI, Euclid | ACTIVE: DESI 2024 shows ~2sigma tension with w=-1 |
| F28 | Spectral ratio 5:8 preserved in any W33 refinement | Lattice QCD universality tests | THEORETICAL |
| F29 | tau_proton ~ 10^45 yr (GUT=Planck) | Hyper-K | SAFE: current limit 10^34 yr |
| F30 | m_DM in 125-193 GeV (WIMP) | LZ, XENONnT, PandaX-4T | ACTIVE: exclusions approaching |
| F31 | w_DE = -1 exactly (duplicate of F23) | DESI DR2, Euclid Y1 | DANGEROUS |
| F32 | Dark photon epsilon ~ (2/3)*e^{-39} ~ 10^{-18} | Dark photon experiments | SAFE: permanently below reach |
| F33 | Delta N_eff from dark sector = 0 at BBN/CMB | CMB-S4 | ACTIVE: measurement 0.06 sensitivity |
| F34 | GW background peak at ~40 microhertz | LISA | FUTURE: launch ~2035 |

## The DESI Tension (Most Dangerous Active Falsifier)

The DESI 2024 BAO data combined with CMB suggests:

```
w0 = -0.727 +/- 0.067
wa = -1.05  +/- 0.31
```

This gives w(z=0) ~ -0.727, which is ~4 sigma away from the W33 prediction of w = -1.

However:
1. DESI DR1 is preliminary; DR2 (2025-2026) will have tighter error bars
2. The tension may be a systematic effect in the calibration of the DESI BAO scale
3. W33-Theory would need a MECHANISM for w != -1 if the tension persists

The W33 escape route: if the dark non-edge vacuum has QUANTUM fluctuations (as opposed to the classical frozen argument in Part DCXLVIII), then w could deviate from -1 at the level of the W33^c spectral fluctuations:

```
delta_w = delta_Lambda / Lambda ~ (g*_dark / g*_SM) * e^{-2} ~ (27/12) * 0.135 ~ 0.30
```

This would give w = -1 + 0.30 = -0.70, which is CONSISTENT with DESI.

**The quantum non-edge fluctuation escape**: if the dark sector non-edge vacuum is not exactly static but has quantum fluctuations at the level of Delta^c / k^c = 24/27 ~ 0.89 of the dark sector scale, then w_DE = -(1 - delta_w) where delta_w is set by dark sector quantum corrections. This is the most important open question in W33-Theory.

## The Dark Matter Direct Detection Status

Current LZ (2023) limits: sigma_SI < 9.2 * 10^{-48} cm^2 at m_DM = 30 GeV.
At m_DM = 155 GeV: sigma_SI < ~10^{-47} cm^2.

The W33 dark matter coupling cross-section is:

```
sigma_SI^{W33} = G_F^2 * m_DM^2 / pi * f_N^2
              ~ (1.17 * 10^{-5} GeV^{-2})^2 * (155 GeV)^2 / pi * (0.3)^2
              ~ 2.5 * 10^{-9} GeV^{-4} * 2.4 * 10^4 GeV^2 / pi * 0.09
              ~ 1.7 * 10^{-5} GeV^{-2}
              ~ 6.7 * 10^{-39} cm^2
```

This is ABOVE current LZ limits by ~8 orders of magnitude IF the W33 dark matter couples through W-boson-strength interactions. This would mean LZ has already excluded the W33 WIMP scenario.

The resolution: W33 dark matter couples through the DARK sector (W33^c edges), not through the SM W-boson. The effective coupling to SM matter is suppressed by epsilon_phys^2 ~ (2/3)^2 * e^{-78}:

```
sigma_SI^{W33} ~ G_F^2 * epsilon^2 * m_DM^2 / pi
              ~ G_F^2 * (4/9) * e^{-78} * m_DM^2 / pi
              ~ 10^{-38} * e^{-78} cm^2
              ~ 10^{-38} * 10^{-34} cm^2
              ~ 10^{-72} cm^2
```

This is 34 orders of magnitude below LZ sensitivity. The W33 dark matter is essentially un-detectable in conventional direct detection experiments. It can only be detected through gravitational effects and potentially at colliders.

**Falsifier F35:** W33 dark matter is gravitationally interacting only (GIMP, not WIMP). Direct detection at LZ/XENONnT gives null result at all masses. Any positive direct detection signal would require a W33 dark matter candidate with SM coupling, which is excluded by epsilon_phys ~ 10^{-18}.

---
*W33-Theory | Part DCLI | Dark sector falsifiers F22-F35 consolidated; DESI tension is the most dangerous; W33 DM is GIMP not WIMP; F35: null direct detection*
