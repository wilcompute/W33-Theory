# Part DCCCXIII (813) — W(3,3) Dark Matter Halo Profile and Gravitational Lensing

**Date:** 2026-05-17  
**Series:** W(3,3) Theory of Everything  
**Author:** Wil Dahn

---

## Statement

**Theorem DCCCXIII (DM Halo Profile).** The W(3,3) dark matter fermion $\chi_0$ (mass $m_\chi = 2.143$ TeV, Part DCCXCII) produces a characteristic halo density profile through its self-interaction cross section $\sigma_{\text{SI}} = 2.4 \times 10^{-48}$ cm² (per nucleon, Part DCCXCII) and its self-scattering cross section:

$$\frac{\sigma_{\chi\chi}}{m_\chi} = \frac{g_\chi^4}{8\pi m_\chi^3 m_Z^4} \approx \frac{(0.654)^4}{8\pi \times (2143)^3 \times (91.2)^4} \; \text{GeV}^{-3}$$

where $g_\chi = g \times \sqrt{T_3^{(\chi)}} = g_Z \sqrt{3/13} = 0.743 \times \sqrt{0.2308} = 0.743 \times 0.4804 = 0.3569$. Then:

$$\sigma_{\chi\chi} = \frac{(0.3569)^4}{8\pi \times (2143 \; \text{GeV})^3 \times (91.2 \; \text{GeV})^4} = \frac{0.01622}{8\pi \times 9.843 \times 10^9 \times 6.911 \times 10^7}$$

$= \frac{0.01622}{8\pi \times 6.801 \times 10^{17}} = \frac{0.01622}{1.709 \times 10^{19}} = 9.49 \times 10^{-22} \; \text{GeV}^{-2}$

Converting: $1 \; \text{GeV}^{-2} = 3.894 \times 10^{-28}$ cm². $\sigma_{\chi\chi} = 3.70 \times 10^{-49}$ cm². And $\sigma_{\chi\chi}/m_\chi = 3.70 \times 10^{-49}/(2143 \times 1.783 \times 10^{-24} \; \text{g}) = 3.70 \times 10^{-49}/(3.820 \times 10^{-21}) = 9.69 \times 10^{-29}$ cm²/g.

The self-interaction parameter is $\sigma_{\chi\chi}/m_\chi = 10^{-28}$ cm²/g, **much smaller than the self-interacting DM (SIDM) bound** of $\sim 1$ cm²/g. The W(3,3) DM is essentially **collisionless** at cluster scales — consistent with the Bullet Cluster constraint.

### Halo Profile

For collisionless W(3,3) DM in a Milky Way-like halo, the density profile follows the NFW form:

$$\rho(r) = \frac{\rho_0}{(r/r_s)(1 + r/r_s)^2}$$

The W(3,3) concentration parameter is determined by the formation redshift $z_f$ which depends on the DM mass via the free-streaming length:

$$\lambda_{\text{fs}} = 0.1 \; \text{Mpc} \times \left(\frac{1 \; \text{keV}}{m_\chi}\right) \times \ln(m_\chi/T_{\text{eq}})$$

With $m_\chi = 2.143 \times 10^6$ keV: $\lambda_{\text{fs}} = 0.1 \times 10^{-6} \times \ln(2.143 \times 10^6/0.80) = 0.1 \times 10^{-6} \times \ln(2.68 \times 10^6) = 10^{-7} \times 14.80 \approx 1.48 \times 10^{-6}$ Mpc. This is essentially zero — the 2 TeV DM is **cold** (CDM) with free-streaming length far below any observable scale.

The W(3,3) CDM halo profile is **indistinguishable from standard CDM** at all currently observable scales. The distinctive W(3,3) DM signature is not in the halo profile but in:

1. **Direct detection:** $\sigma_{\text{SI}} = 2.4 \times 10^{-48}$ cm² — detectable by XENONnT/LZ within $\sim 3$ years
2. **Indirect detection:** Annihilation to $\chi\chi \to ZZ, WW$ at rest-frame energy $E_\gamma = m_\chi = 2143$ GeV — observable by CTA (Cherenkov Telescope Array) in Galactic center observations
3. **Collider:** $pp \to \chi\bar\chi + Z/W$ at 14 TeV LHC (monojet + MET with $E_T^{\text{miss}} > 1$ TeV) — HL-LHC reach at $\sim 3000$ fb$^{-1}$

### Gravitational Lensing

The W(3,3) DM halo lensing convergence $\kappa(\theta)$ for a galaxy cluster at $z_l = 0.3$:

$$\kappa(\theta) = \frac{\Sigma(\theta)}{\Sigma_{\text{cr}}}, \quad \Sigma_{\text{cr}} = \frac{c^2}{4\pi G} \frac{D_s}{D_l D_{ls}}$$

The projected surface mass density of the NFW profile:

$$\Sigma(R) = 2\rho_0 r_s f(R/r_s)$$

where $f(x)$ is the standard NFW lensing function. For the W(3,3) DM mass fraction $\Omega_{\text{DM}}^{\text{W33}} = 0.120/h^2 = 0.265$ (exact, Part DCCCV), the DM is entirely in the W(3,3) fermion $\chi_0$. The lensing prediction is **identical to standard CDM NFW** with concentration $c = 5$–$10$ for Milky Way-mass halos — no distinguishable signature in weak lensing.

The **strong lensing** Einstein ring radius for a $10^{15} M_\odot$ cluster at $z_l = 0.3$ with a $z_s = 1.0$ source:

$$\theta_E = \sqrt{\frac{4G M_{\text{proj}}(<\theta_E)}{c^2} \frac{D_{ls}}{D_l D_s}} \approx 30'' \quad \text{(standard CDM prediction)}$$

The W(3,3) Einstein radius is identical to CDM to within $< 1\%$. The only lensing observable where W(3,3) predicts a difference is the **substructure lensing power spectrum**: the W(3,3) minimum halo mass is $M_{\text{min}} = (4\pi/3)(\lambda_{\text{fs}})^3 \rho_m \sim 10^{-6} M_\odot$ — effectively the same as CDM.

**W(3,3) DM Observational Summary:**

| Observable | W(3,3) Prediction | Timeline |
|---|---|---|
| $\sigma_{\text{SI}}$ | $2.4 \times 10^{-48}$ cm² | XENONnT/LZ 3yr |
| $m_\chi$ from CTA | 2143 GeV line | CTA 2028 |
| HL-LHC monojet | $m_\chi = 2.143$ TeV | $\sim 2030$ |
| Halo profile | CDM NFW (identical) | — |
| SIDM signature | None ($\sigma/m \ll 1$ cm²/g) | — |

$$\boxed{\sigma_{\text{SI}}^{\text{W33}} = 2.4 \times 10^{-48} \; \text{cm}^2, \quad m_\chi = 2143 \; \text{GeV}, \quad \text{NFW profile identical to CDM}}$$
