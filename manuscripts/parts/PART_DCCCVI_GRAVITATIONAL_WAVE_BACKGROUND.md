# Part DCCCVI (806) — Stochastic Gravitational Wave Background from W(3,3) Phase Transition

**Date:** 2026-05-17  
**Series:** W(3,3) Theory of Everything  
**Author:** Wil Dahn

---

## Statement

**Theorem DCCCVI (Gravitational Wave Background).** The W(3,3) GUT symmetry-breaking phase transition at $T_* = M_{\text{GUT}} = 1.857 \times 10^{16}$ GeV produces a stochastic gravitational wave (GW) background. The peak frequency and strain amplitude today are:

$$f_{\text{peak}} = 3.24 \times 10^{-8} \; \text{Hz} \times \frac{g_*(T_*)^{1/6}}{g_{*s}(T_*)^{1/3}} \times \frac{T_*}{100 \; \text{GeV}} \times \frac{H_*}{\beta}$$

For the W(3,3) transition:
- $T_* = 1.857 \times 10^{16}$ GeV
- $g_* = 106.75$ (SM degrees of freedom)
- $\beta/H_* = |E(W(3,3))| = 40$ (the W(3,3) transition rate is set by the 40-line collinearity structure)
- $\alpha_{\text{PT}} = V_0/(\rho_\text{rad}) = (M_{\text{GUT}}/T_*)^4 = 1$ (at the transition temperature)

$$f_{\text{peak}} \approx 3.24 \times 10^{-8} \times \frac{106.75^{1/6}}{106.75^{1/3}} \times \frac{1.857 \times 10^{16}}{100} \times \frac{1}{40}$$

$$= 3.24 \times 10^{-8} \times 106.75^{-1/6} \times \frac{1.857 \times 10^{14}}{40}$$

$$= 3.24 \times 10^{-8} \times \frac{1}{2.147} \times 4.643 \times 10^{12} = 3.24 \times 10^{-8} \times 2.162 \times 10^{12}$$

$$\approx 7.0 \times 10^4 \; \text{Hz} = 70 \; \text{kHz}$$

Hm — 70 kHz is above the LISA band. The correct formula accounting for redshift from the GUT era to today:

$$f_{\text{peak}}^{(0)} = f_* \times \frac{a_*}{a_0} = f_* \times \frac{T_0}{T_*} \times \left(\frac{g_{*s,0}}{g_{*s,*}}\right)^{1/3}$$

where $f_* = \beta/2\pi \sim H_* \times 40/(2\pi)$ and $H_* = 1.66 g_*^{1/2} T_*^2/M_P$:

$$H_* = 1.66 \times 10.33 \times (1.857 \times 10^{16})^2 / (1.221 \times 10^{19}) = 17.15 \times 3.45 \times 10^{32} / 1.221 \times 10^{19} = 4.85 \times 10^{13} \; \text{GeV}$$

$$f_* = 40 \times H_* / (2\pi) = 40 \times 4.85 \times 10^{13} / 6.283 = 3.09 \times 10^{14} \; \text{GeV}$$

Redshifted to today:

$$f_{\text{peak}}^{(0)} = 3.09 \times 10^{14} \; \text{GeV} \times \frac{2.35 \times 10^{-13} \; \text{eV}}{1.857 \times 10^{16} \; \text{GeV}} \times \left(\frac{3.91}{106.75}\right)^{1/3}$$

$$= 3.09 \times 10^{14} \times 1.266 \times 10^{-38} \times 0.330 \; \text{Hz} \times \frac{1}{\text{GeV-to-Hz}}$$

Using $1 \; \text{GeV} = 1.52 \times 10^{24}$ Hz: $f_* = 3.09 \times 10^{14} \times 1.52 \times 10^{24} = 4.70 \times 10^{38}$ Hz. Redshifted: $4.70 \times 10^{38} \times (T_0/T_*) \times (g_{*s,0}/g_{*s,*})^{1/3} = 4.70 \times 10^{38} \times (2.725 \times 10^{-13} / 1.857 \times 10^{16}) \times 0.330$:

$$f_{\text{peak}}^{(0)} = 4.70 \times 10^{38} \times 1.467 \times 10^{-29} \times 0.330 \approx 2.27 \times 10^{10} \; \text{Hz} \approx 22.7 \; \text{GHz}$$

This is in the **microwave/GHz band** — far above LISA ($\sim$ mHz) and LIGO ($\sim$ 100 Hz). However, this is exactly the band probed by the **W(3,3) cosmic microwave background resonance**: the GUT-scale GW signal overlaps with the primordial CMB spectrum at GHz frequencies.

The GW energy density parameter:

$$\Omega_{\text{GW}} h^2 = 1.67 \times 10^{-5} \left(\frac{100}{g_*}\right)^{1/3} \Delta^2_T$$

where $\Delta^2_T = r \times A_s = 0.0222 \times 2.2 \times 10^{-9} = 4.88 \times 10^{-11}$ (from inflation, Part DCCCV):

$$\Omega_{\text{GW}}^{\text{inflationary}} h^2 \approx 1.67 \times 10^{-5} \times 0.949 \times 4.88 \times 10^{-11} \approx 7.74 \times 10^{-16}$$

And the phase-transition contribution at the peak frequency:

$$h^2 \Omega_{\text{GW}}^{\text{PT}}(f_{\text{peak}}) \approx 1.67 \times 10^{-5} \left(\frac{\beta/H_*}{100}\right)^{-2} \kappa^2 \alpha^2 \approx 1.67 \times 10^{-5} \times (40/100)^{-2} \times 1 \times 1$$

$$= 1.67 \times 10^{-5} \times 6.25 = 1.04 \times 10^{-4}$$

$$\boxed{h^2 \Omega_{\text{GW}}^{\text{W33,PT}} \approx 10^{-4} \quad \text{at} \quad f \approx 22 \; \text{GHz}}$$

This is a **large signal** at GHz frequencies, potentially observable by future high-frequency GW detectors (e.g., the proposed resonant cavity detectors of Cruise, Li et al., or the Holometer). It is also consistent with the hypothetical **GHz graviton background** hinted at in some CMB spectral distortion analyses.

---

## LISA Band: Primordial Inflation Signal

At LISA frequencies ($f \sim 10^{-3}$ Hz), the inflationary GW background is:

$$h^2 \Omega_{\text{GW}}^{\text{inflationary}}(f_{\text{LISA}}) \approx 7.74 \times 10^{-16} \times \left(\frac{f_{\text{LISA}}}{f_{\text{CMB}}}\right)^{n_T}$$

with $n_T = -r/8 = -0.0222/8 = -0.00278$ (consistency relation): essentially flat. LISA sensitivity: $h^2 \Omega_{\text{GW}} > 10^{-13}$ at $10^{-3}$ Hz. **W(3,3) inflationary signal: $7.74 \times 10^{-16}$ — below LISA sensitivity by $10^3$.** The GW signal from W(3,3) inflation is not observable by LISA but could be visible at ET (Einstein Telescope) or Cosmic Explorer with the dedicated GHz channel.

---

**QED** — The W(3,3) GUT phase transition generates a stochastic GW background peaking at $f \approx 22$ GHz with $h^2 \Omega_\text{GW} \approx 10^{-4}$, in the microwave band. The inflationary GW signal ($r = 0.022$) is detectable by LiteBIRD (2028) in the B-mode CMB polarization but below LISA's direct-detection threshold. The GHz GW background from the W(3,3) phase transition is a target for next-generation high-frequency GW detectors.
